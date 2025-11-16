import os
import sys

# Add src directory to Python path for Hugging Face Spaces compatibility
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

import json

import gradio as gr
from numpy import add

from learnbee.llm_call import LLMCall
from learnbee.mcp_server import get_lesson_content, get_lesson_list


LESSON_CONTENT_MAX_LENGTH = 50000

# Available tutor names for early childhood education
TUTOR_NAMES = ["Professor Owl", "Star Explorer", "Logic Bot", "Nature Guide", "Story Friend"]


def load_lesson_content(lesson_name, selected_tutor, progress=gr.Progress()):
    """Load lesson content and extract key concepts. Returns introduction message for chatbot."""
    if not lesson_name:
        return "", "", "Please select a lesson first.", []
    
    # Get current chatbot state (empty list if none)
    chatbot_messages = []

    progress(0.1, desc="Loading lesson content...")

    lesson_content = get_lesson_content(lesson_name, LESSON_CONTENT_MAX_LENGTH)

    progress(0.5, desc="Extracting key concepts from the lesson...")

    # Extract key concepts using LLM
    try:
        call_llm = LLMCall()
        concepts = call_llm.extract_key_concepts(lesson_content)

        progress(0.7, desc="Generating lesson introduction...")

        # Generate lesson introduction with summary and example questions
        introduction = ""
        if concepts:
            try:
                introduction = call_llm.generate_lesson_introduction(
                    lesson_content, lesson_name, concepts
                )
            except Exception as e:
                print(f"Error generating introduction: {str(e)}")
                # Continue without introduction if it fails

        progress(1.0, desc="Complete!")

        if concepts:
            concepts_display = ', '.join(concepts[:5])
            if len(concepts) > 5:
                concepts_display += f" and {len(concepts) - 5} more"
            
            # Build simple status message (just confirmation)
            status_message = (
                f"✅ Successfully loaded '{lesson_name}'!\n\n"
                f"📚 Found {len(concepts)} key concepts: {concepts_display}\n\n"
                f"🎓 Your tutor is ready! Check the chat for a welcome message."
            )
            
            # Prepare chatbot message with introduction
            if introduction:
                # Format the introduction as a friendly greeting from the tutor
                tutor_greeting = (
                    f"Hello! 👋 I'm {selected_tutor}, and I'm so excited to learn with you today!\n\n"
                    f"{introduction}\n\n"
                    f"Let's start our learning adventure! What would you like to explore first? 🌟"
                )
                chatbot_messages = [{"role": "assistant", "content": tutor_greeting}]
            else:
                # Fallback greeting if introduction generation fails
                tutor_greeting = (
                    f"Hello! 👋 I'm {selected_tutor}, and I'm excited to learn with you today!\n\n"
                    f"We're going to explore: {concepts_display}\n\n"
                    f"What would you like to learn about first? 🌟"
                )
                chatbot_messages = [{"role": "assistant", "content": tutor_greeting}]
            
            return (
                lesson_name,
                lesson_content,
                status_message,
                chatbot_messages,
            )
        else:
            status_message = (
                f"⚠️ Loaded '{lesson_name}' but no key concepts were automatically detected.\n"
                f"You can still chat with your tutor about the lesson content!"
            )
            tutor_greeting = (
                f"Hello! 👋 I'm {selected_tutor}, and I'm ready to learn with you!\n\n"
                f"Let's explore the lesson '{lesson_name}' together. What would you like to know? 🌟"
            )
            chatbot_messages = [{"role": "assistant", "content": tutor_greeting}]
            return (
                lesson_name,
                lesson_content,
                status_message,
                chatbot_messages,
            )
    except Exception as e:
        status_message = (
            f"❌ Error extracting concepts: {str(e)}\n\n"
            f"You can still try chatting about the lesson content."
        )
        tutor_greeting = (
            f"Hello! 👋 I'm {selected_tutor}, and I'm here to help you learn!\n\n"
            f"Let's explore together. What would you like to know? 🌟"
        )
        chatbot_messages = [{"role": "assistant", "content": tutor_greeting}]
        return (
            lesson_name,
            lesson_content,
            status_message,
            chatbot_messages,
        )


def custom_respond(
    message, history, lesson_name, lesson_content, selected_tutor, difficulty_level
):
    """Custom respond function with educational system prompt."""
    if not lesson_name or not selected_tutor:
        yield "Please select a lesson and tutor first."
        return

    if not lesson_content:
        lesson_content = get_lesson_content(lesson_name, LESSON_CONTENT_MAX_LENGTH)

    # Generate educational system prompt with enhanced pedagogy
    # fmt: off
    system_prompt = (
        f"You are {selected_tutor}, a friendly and patient Educational Tutor specializing in early childhood education (ages 3-6).\n\n"
        
        "CORE PEDAGOGICAL PRINCIPLES:\n"
        "1. Socratic Method: Guide through questions, not answers. Help children discover knowledge themselves.\n"
        "2. Scaffolding: Break complex ideas into smaller, manageable steps. Build understanding gradually.\n"
        "3. Positive Reinforcement: Celebrate attempts, not just correct answers. Use encouraging phrases like 'Great thinking!' or 'You're on the right track!'\n"
        "4. Active Learning: Encourage hands-on thinking, examples from their world, and personal connections.\n"
        "5. Repetition with Variation: Reinforce concepts through different examples and contexts.\n\n"
        
        "COMMUNICATION GUIDELINES:\n"
        "- Use very simple, age-appropriate language (3-6 year olds).\n"
        "- Keep sentences short (5-10 words maximum).\n"
        "- Use concrete examples from children's daily lives (toys, family, pets, food, nature).\n"
        "- Incorporate playful elements: emojis, simple analogies, and fun comparisons.\n"
        "- Be warm, enthusiastic, and patient. Show excitement about learning!\n"
        "- Use the child's name when possible (refer to them as 'you' or 'little learner').\n\n"
        
        "TEACHING STRATEGIES BY DIFFICULTY LEVEL:\n"
        f"- {difficulty_level.upper()} level:\n"
        + ("  * Beginner: Use very simple words, lots of examples, visual descriptions, and yes/no questions.\n"
           if difficulty_level == "beginner" else
           "  * Intermediate: Introduce slightly more complex concepts, encourage longer explanations, use 'why' and 'how' questions.\n"
           if difficulty_level == "intermediate" else
           "  * Advanced: Challenge with problem-solving, encourage predictions, explore connections between concepts.\n") +
        "\n"
        
        "INTERACTION PATTERNS:\n"
        "- When a child asks a question: Respond with a guiding question first, then offer a hint if needed.\n"
        "- When a child gives an answer: Validate their thinking, then ask a follow-up to deepen understanding.\n"
        "- When a child seems confused: Break it down into smaller pieces, use a different example, or try a simpler approach.\n"
        "- When a child shows excitement: Match their energy and build on their interest.\n"
        "- When off-topic: Acknowledge their interest, then gently connect it back: 'That's interesting! Now, let's think about how that relates to our lesson...'\n\n"
        
        "SAFETY AND BOUNDARIES:\n"
        "- Only discuss topics appropriate for ages 3-12.\n"
        "- If asked about inappropriate topics, gently redirect: 'Let's focus on our fun lesson instead!'\n"
        "- Keep all content educational and positive.\n"
        "- Never provide medical, legal, or safety advice beyond basic age-appropriate concepts.\n\n"
        
        "LESSON CONTEXT:\n"
        "====================\n"
        f"{lesson_content}\n"
        "====================\n\n"
        
        "YOUR ROLE:\n"
        "You are teaching this lesson content to a young child. Make it engaging, interactive, and fun. "
        "Remember: the goal is not just to convey information, but to spark curiosity and build confidence in learning.\n\n"
        
        "LANGUAGE INSTRUCTION:\n"
        "IMPORTANT: Always respond in the EXACT same language that the child uses in their messages. "
        "If the child writes in Spanish, respond in Spanish. If they write in English, respond in English. "
        "If they write in French, respond in French. Match the child's language automatically. "
        "This is critical for effective communication with young learners.\n"
    )
    # fmt: on

    # Call the respond method with educational system prompt
    call_llm = LLMCall()
    for response in call_llm.respond(
        message, 
        history, 
        system_prompt=system_prompt,
        tutor_name=selected_tutor,
        difficulty_level=difficulty_level
    ):
        yield response


def gradio_ui():
    lesson_name = gr.BrowserState("")
    selected_tutor = gr.BrowserState(TUTOR_NAMES[0] if TUTOR_NAMES else "")

    lesson_choices = json.loads(get_lesson_list())

    with gr.Blocks() as demo:

        with gr.Tab("Chat"):
            # Title
            with gr.Row():
                gr.Markdown("# Learnbee-mcp - Educational Tutor")

            # Status
            with gr.Row():
                status_markdown = gr.Markdown(label="Status")
                status_markdown.value = (
                    # fmt: off
                    "👋 Welcome to Learnbee-mcp! 🎓<br><br>"
                    "📖 <strong>Getting Started:</strong><br>"
                    "1. Select a lesson from the dropdown<br>"
                    "2. Choose your favorite tutor<br>"
                    "3. Pick a difficulty level<br>"
                    "4. Click 'Load Lesson & Prepare Tutor'<br>"
                    "5. Start learning and chatting! 💬<br><br>"
                    "✨ This educational system is designed for early childhood education (ages 3-6)."
                    # fmt: on
                )

            # Hidden textbox for lesson content
            lesson_content = gr.Textbox(visible=False)

            with gr.Row():

                with gr.Column(scale=1):
                    # Lesson selection
                    with gr.Row():
                        lesson_dropdown = gr.Dropdown(
                            label="📚 Select a Lesson",
                            choices=lesson_choices,
                            interactive=True,
                        )

                    # Tutor selection
                    with gr.Row():
                        tutor_dropdown = gr.Dropdown(
                            label="🦸 Select a Tutor",
                            choices=TUTOR_NAMES,
                            value=TUTOR_NAMES[0] if TUTOR_NAMES else None,
                            interactive=True,
                        )

                    # Difficulty level selection
                    with gr.Row():
                        difficulty_dropdown = gr.Dropdown(
                            label="📊 Difficulty Level",
                            choices=["beginner", "intermediate", "advanced"],
                            value="beginner",
                            interactive=True,
                        )

                    with gr.Row():
                        load_button = gr.Button(
                            "Load Lesson & Prepare Tutor", variant="primary"
                        )

                        def update_tutor_selection(tutor):
                            """Update selected tutor."""
                            return tutor

                        tutor_dropdown.change(
                            fn=update_tutor_selection,
                            inputs=[tutor_dropdown],
                            outputs=[selected_tutor],
                        )

                    with gr.Row():
                        gr.Markdown(
                            "🌍 **Multilingual Support:** The tutor will automatically respond in the same language you use!<br>"
                            "Just start chatting in your preferred language (English, Spanish, French, etc.) and the tutor will match it.<br>"
                            "<br>"
                            "🔄 **Note:** Once you start chatting, you can't change the lesson or tutor. <br>"
                            "If you want to pick a different one, just hit the reset button and start fresh! 😊<br>"
                        )

                with gr.Column(scale=2):
                    # Chat interface - defined before use
                    chat_interface = gr.ChatInterface(
                        fn=custom_respond,
                        additional_inputs=[
                            lesson_dropdown,
                            lesson_content,
                            tutor_dropdown,
                            difficulty_dropdown,
                        ],
                        type="messages",
                        autofocus=False
                    )

                    # Connect load button after chat_interface is defined
                    load_button.click(
                        fn=load_lesson_content,
                        inputs=[lesson_dropdown, tutor_dropdown],
                        outputs=[
                            lesson_name,
                            lesson_content,
                            status_markdown,
                            chat_interface.chatbot_value,
                        ],
                    )

                    reset_button = gr.Button("Reset", variant="secondary")
                    reset_button.click(
                        lambda: (
                            gr.update(value=""),
                            gr.update(value=""),
                            gr.update(value=TUTOR_NAMES[0] if TUTOR_NAMES else None),
                            gr.update(value="beginner"),
                            "Status reset.",
                            [],
                        ),
                        outputs=[
                            lesson_dropdown,
                            lesson_content,
                            tutor_dropdown,
                            difficulty_dropdown,
                            status_markdown,
                            chat_interface.chatbot_value,
                        ],
                    )

        with gr.Tab("List Lessons"):
            gr.Markdown("📚 Get the list of available lessons.")
            btn = gr.Button("Get")
            output_text = gr.Textbox(label="Lessons")
            btn.click(get_lesson_list, None, output_text)

        with gr.Tab("Lesson Content"):
            gr.Markdown("📖 Get the content of a lesson by its name.")
            lesson_name_input = gr.Textbox(label="Lesson Name")
            lesson_len = gr.Number(label="Max Length", value=1000)
            lesson_content_output = gr.Textbox(label="Lesson Content", lines=20)
            btn = gr.Button("Get")
            btn.click(get_lesson_content, [lesson_name_input, lesson_len], lesson_content_output)

    return demo


if __name__ == "__main__":
    demo = gradio_ui()

    # Launch the Gradio app with MCP server enabled.
    # NOTE: It is required to restart the app when you add or remove MCP tools.
    demo.launch(mcp_server=True)
