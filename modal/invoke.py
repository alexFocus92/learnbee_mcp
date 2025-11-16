import modal

APP_NAME = "llm-server"

ENABLE_STREAMING = True
SYSTEM_PROMPT = "You are a friendly Chatbot. Please respond in the same language as the user."


VLLMModel = modal.Cls.from_name(APP_NAME, "VLLMModel")
model = VLLMModel()

chat_history = []
chat_history.append(
    {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]}
)

# User prompt
user_prompt = "Hi!"
print(f"USER: {user_prompt}\n")
chat_history.append(
    {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
)

print("Calling chat function...")

# AI response
if ENABLE_STREAMING:
    """Streaming version"""
    print("AI: ", end="", flush=True)
    response = ""
    for chunk in model.generate_stream.remote_gen(chat_history):
        print(chunk, end="", flush=True)
        response += chunk
    print()

else:
    """Non-streaming version"""
    response = model.generate.remote(chat_history)
    print("AI:", response)


chat_history.append(
    {"role": "assistant", "content": [{"type": "text", "text": response}]}
)
