import subprocess

from huggingface_hub import snapshot_download
import vllm

import modal

APP_NAME = "llm-server"
VOLUME_NAME = APP_NAME + "-volume"
MOUNT_VOLUME = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
MOUNT_DIR = "/data"

# Model identifier for the Hugging Face model
# NOTE: Gemma-3 GGUF models are not supported by vLLM yet (2025-06-10).
# NOTE: vLLM allocate all GPU memory according to the value specified by `gpu_memory_utilization` at initialization.
# https://huggingface.co/google/gemma-3-4b-it
MODEL_IDENTIFIER = "google/gemma-3-4b-it"  # GPU memory requirements: 10GB when MAX_MODEL_TOKENS=2k, 20GB when MAX_MODEL_TOKENS=128k
# https://huggingface.co/google/gemma-3-12b-it
# MODEL_IDENTIFIER = "google/gemma-3-12b-it"
# https://huggingface.co/google/gemma-3-27b-it
# MODEL_IDENTIFIER = "google/gemma-3-27b-it"

# https://modal.com/docs/guide/gpu#specifying-gpu-type
GPU_NAME = "A100-40GB"
GPU_NUM = 1  # Number of GPUs to use
GPU = f"{GPU_NAME}:{GPU_NUM}"

# https://modal.com/pricing
# | GPU       | Memory | Price    |
# |-----------|--------|----------|
# | B200      | 180 GB | $6.25 /h |
# | H200      | 141 GB | $4.54 /h |
# | H100      |  80 GB | $3.95 /h |
# | A100-80GB |  80 GB | $2.50 /h |
# | A100-40GB |  40 GB | $2.10 /h |
# | L40S      |  48 GB | $1.95 /h |
# | A10G      |  24 GB | $1.10 /h |
# | L4        |  24 GB | $0.80 /h |
# | T4        |  16 GB | $0.59 /h |

# MAX_MODEL_TOKENS >= Input + Output
MAX_MODEL_TOKENS = 128 * 1024  # Gemma-3-4B~ has 128K context length
MAX_OUTPUT_TOKENS = 512

image = (
    # https://hub.docker.com/r/nvidia/cuda/tags?name=12.8
    # https://hub.docker.com/layers/nvidia/cuda/12.8.1-devel-ubuntu24.04
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu24.04", add_python="3.12")
    .pip_install(
        [
            "accelerate>=1.7.0",
            "bitsandbytes>=0.46.0",
            "sentencepiece>=0.2.0",
            "torch==2.8.0",
            "transformers>=4.52.4",
            "vllm>=0.9.0.1",
        ]
    )
    .env(
        {
            "HF_HOME": MOUNT_DIR + "/huggingface",
            "VLLM_CACHE_ROOT": MOUNT_DIR + "/vllm",
        }
    )
)

app = modal.App(APP_NAME, image=image)

# NOTE: `@app.cls`, `@modal.enter()`, and `@modal.method()` are used like `@app.function()`
# https://modal.com/docs/guide/lifecycle-functions


@app.cls(
    gpu=GPU,
    image=image,
    volumes={MOUNT_DIR: MOUNT_VOLUME},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    scaledown_window=15 * 60,
    timeout=30 * 60,
)
class VLLMModel:

    @modal.enter()
    def setup(self):
        # Ensure the cache volume is the latest
        MOUNT_VOLUME.reload()

        # NOTE:"HF_TOKEN" environment variable is required for Hugging Face authentication

        # self._download_model(MODEL_IDENTIFIER)  # This is not needed because vLLM can download the model automatically.

        self._load_model()

        # Commit the volume to ensure the model is saved
        MOUNT_VOLUME.commit()

    def _download_model(self, repo_id: str):
        """Download the model from Hugging Face if not already present."""
        # Ensure the cache volume is the latest
        MOUNT_VOLUME.reload()

        snapshot_download(
            repo_id=repo_id,
        )

        # Commit downloaded model
        MOUNT_VOLUME.commit()

    def _load_model(self):

        self.llm = vllm.LLM(
            model=MODEL_IDENTIFIER,
            tensor_parallel_size=1,
            dtype="auto",
            max_model_len=MAX_MODEL_TOKENS,
            gpu_memory_utilization=0.9,
            trust_remote_code=True,
        )

        # Show GPU information
        subprocess.run(["nvidia-smi"])

    @modal.method()
    def generate(self, chat_history):
        """Generate a response"""
        formatted_text = self._get_formatted_text(chat_history)

        input_token_len = self._check_input_length(formatted_text)
        if input_token_len + MAX_OUTPUT_TOKENS > MAX_MODEL_TOKENS:
            raise ValueError(
                f"Input length exceeds the maximum allowed tokens: {MAX_MODEL_TOKENS}. "
                f"Current input length: {input_token_len} tokens."
            )

        sampling_params = self._get_sampling_params()

        outputs = self.llm.generate([formatted_text], sampling_params)
        response = outputs[0].outputs[0].text

        return response

    @modal.method()
    def generate_stream(self, chat_history):
        """
        Generate a streaming response
        NOTE: This function may NOT generate streaming output as expected
        """
        formatted_text = self._get_formatted_text(chat_history)

        input_token_len = self._check_input_length(formatted_text)
        if input_token_len + MAX_OUTPUT_TOKENS > MAX_MODEL_TOKENS:
            raise ValueError(
                f"Input length exceeds the maximum allowed tokens: {MAX_MODEL_TOKENS}. "
                f"Current input length: {input_token_len} tokens."
            )

        sampling_params = self._get_sampling_params()

        # Streaming generation with vLLM
        for output in self.llm.generate([formatted_text], sampling_params):
            for completion_output in output.outputs:
                yield completion_output.text

    def _get_formatted_text(self, chat_history):
        """Format the chat history"""
        tokenizer = self.llm.get_tokenizer()
        return tokenizer.apply_chat_template(
            chat_history,
            tokenize=False,
            add_generation_prompt=True,
        )

    def _check_input_length(self, formatted_text):
        tokenizer = self.llm.get_tokenizer()
        input_token_len = len(tokenizer(formatted_text)["input_ids"])
        return input_token_len

    def _get_sampling_params(self):
        """Get sampling parameters for generation"""
        return vllm.SamplingParams(
            temperature=1.0,
            top_k=50,
            top_p=1.0,
            max_tokens=MAX_OUTPUT_TOKENS,
        )


@app.local_entrypoint()
def main():
    SYSTEM_PROMPT = (
        "You are a friendly Chatbot. Please respond in the same language as the user."
    )

    # Initialize chat history list
    chat_history = []
    chat_history.append(
        {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
    )

    user_prompt = "Hi!"
    print(f"USER: {user_prompt}\n")
    chat_history.append(
        {
            "role": "user",
            "content": [
                # {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
                {"type": "text", "text": user_prompt}
            ],
        }
    )

    model = VLLMModel()

    # Call non-streaming function
    response = model.generate.remote(chat_history)
    print("AI:", response)
    chat_history.append(
        {"role": "assistant", "content": [{"type": "text", "text": response}]}
    )

    user_prompt = "What is your name?"
    print(f"USER: {user_prompt}\n")
    chat_history.append(
        {
            "role": "user",
            "content": [{"type": "text", "text": user_prompt}],
        }
    )

    # Call streaming function
    print("AI: ", end="", flush=True)
    response = ""
    for chunk in model.generate_stream.remote_gen(chat_history):
        print(chunk, end="", flush=True)
        response += chunk
    print()
