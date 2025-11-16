import os
import sys

# test to update
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

import json

import gradio as gr
from numpy import add

from learnbee.llm_call import LLMCall
from learnbee.mcp_server import create_lesson, get_lesson_content, get_lesson_list

# Beautiful Ocean-inspired theme
beautiful_theme = gr.themes.Ocean(
    primary_hue="blue",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
)

# CLEAN, MODERN CSS - Compatible con modo claro y oscuro
custom_css = """
/* Main container */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 1rem !important;
}

/* Beautiful header - siempre visible en ambos modos */
.header-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
}

.header-banner h1 {
    color: white !important;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header-banner p {
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 1.1rem;
    margin: 0.25rem 0;
}

/* Status box - adaptativo */
.status-box {
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Chat messages - adaptativo para modo claro y oscuro */
.message {
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    animation: fadeIn 0.3s ease;
}

/* Bot messages - adaptativo */
.message.bot {
    border-left: 4px solid #667eea !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}

/* User messages - adaptativo */
.message.user {
    border-left: 4px solid #94a3b8 !important;
}

/* Code blocks - siempre oscuro para legibilidad */
.message pre {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Input fields - adaptativo */
textarea, input[type="text"], input[type="number"] {
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

textarea:focus, input[type="text"]:focus, input[type="number"]:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Dropdowns - adaptativo */
select, .gr-dropdown {
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

select:focus, .gr-dropdown:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0.75rem 1.5rem !important;
}

button:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
}

/* Tabs */
.tab-nav {
    border-radius: 12px 12px 0 0 !important;
}

.tab-nav button {
    border-radius: 12px 12px 0 0 !important;
    margin-right: 0.25rem !important;
}

/* Info boxes - adaptativo */
.info-box {
    border-radius: 12px;
    padding: 1.25rem;
    margin-top: 1rem;
    border-left: 4px solid #94a3b8;
    line-height: 1.7;
}

/* Footer - adaptativo */
.footer-text {
    text-align: center;
    padding: 2rem 1rem;
    line-height: 1.8;
}

.footer-text a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
}

/* Column styling - adaptativo */
.column-container {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Chat interface container - adaptativo */
.chat-container {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Asegurar que los textos en markdown sean legibles en ambos modos */
.markdown-text, .markdown p, .markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
    color: inherit !important;
}

/* Asegurar que los labels sean legibles */
label {
    color: inherit !important;
}

/* Textboxes y áreas de texto - adaptativo */
.gr-textbox textarea, .gr-textbox input {
    color: inherit !important;
    background-color: inherit !important;
}

/* Dropdowns - adaptativo */
.gr-dropdown select, .gr-dropdown {
    color: inherit !important;
    background-color: inherit !important;
}

/* Números - adaptativo */
.gr-number input {
    color: inherit !important;
    background-color: inherit !important;
}

/* Chatbot messages - asegurar legibilidad */
.chatbot {
    color: inherit !important;
}

.chatbot .message {
    color: inherit !important;
}

/* Status markdown - adaptativo */
.gr-markdown {
    color: inherit !important;
}

.gr-markdown p, .gr-markdown h1, .gr-markdown h2, .gr-markdown h3, 
.gr-markdown h4, .gr-markdown h5, .gr-markdown h6, .gr-markdown li, 
.gr-markdown ul, .gr-markdown ol {
    color: inherit !important;
}

/* Asegurar que los textos dentro de las cajas de información sean legibles */
.info-box p, .info-box strong {
    color: inherit !important;
}

/* Inputs dentro de componentes Gradio */
.gr-component input, .gr-component textarea, .gr-component select {
    color: inherit !important;
}

/* Labels de Gradio */
.gr-label {
    color: inherit !important;
}

/* Contenedores principales - usar colores del tema */
.dark .gradio-container {
    background: var(--background-fill-primary) !important;
}

/* Asegurar que los mensajes del chatbot usen colores del tema */
.chatbot .user-message, .chatbot .assistant-message {
    color: inherit !important;
}
"""


LESSON_CONTENT_MAX_LENGTH = 50000

# Available tutor names for early childhood education
TUTOR_NAMES = ["Professor Owl", "Star Explorer", "Logic Bot", "Nature Guide", "Story Friend"]

# Available languages
LANGUAGES = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean", "Arabic", "Russian", "Dutch", "Polish", "Turkish", "Hindi"]


def load_lesson_content(lesson_name, selected_tutor, selected_language, progress=gr.Progress()):
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

        # Generate lesson introduction with summary and example questions in selected language
        introduction = ""
        if concepts:
            try:
                introduction = call_llm.generate_lesson_introduction(
                    lesson_content, lesson_name, concepts, language=selected_language
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


def reset_chat_interface():
    """Reset the chat interface to initial state."""
    return (
        gr.update(value=""),
        gr.update(value=""),
        gr.update(value=TUTOR_NAMES[0] if TUTOR_NAMES else None),
        gr.update(value="beginner"),
        gr.update(value="English"),
        "Status reset.",
        [],
    )


def create_new_lesson(topic, lesson_name, age_range, progress=gr.Progress()):
    """Create a new lesson from a topic using ChatGPT."""
    if not topic or not topic.strip():
        return "❌ Please enter a topic for the lesson.", "", gr.update()
    
    progress(0.2, desc="Generating lesson content with ChatGPT...")
    
    # Use provided lesson_name or None to auto-generate
    name_to_use = lesson_name.strip() if lesson_name and lesson_name.strip() else None
    
    progress(0.6, desc="Saving lesson...")
    
    result = create_lesson(topic.strip(), name_to_use, age_range)
    
    progress(1.0, desc="Complete!")
    
    # If successful, return the lesson content preview and update lesson list
    lesson_content_preview = ""
    lesson_dropdown_update = gr.update()
    
    if result.startswith("✅"):
        # Extract lesson name from result
        if name_to_use:
            actual_name = name_to_use
        else:
            # Extract from topic
            actual_name = topic.lower().strip().replace(" ", "_").replace("/", "_").replace("\\", "_")
            actual_name = "".join(c for c in actual_name if c.isalnum() or c in ("_", "-"))
        
        # Get a preview of the lesson content
        try:
            content = get_lesson_content(actual_name, max_length=500)
            if not content.startswith("Error:"):
                lesson_content_preview = f"\n\n📖 Lesson Preview (first 500 characters):\n\n{content}"
        except:
            pass
        
        # Update lesson dropdown with new lesson list
        try:
            lesson_choices = json.loads(get_lesson_list())
            lesson_dropdown_update = gr.update(choices=lesson_choices, value=actual_name)
        except:
            lesson_dropdown_update = gr.update()
    
    return result + lesson_content_preview, "", lesson_dropdown_update


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

    with gr.Blocks(theme=beautiful_theme, css=custom_css, title="Learnbee MCP - Educational Tutor") as demo:

        # Beautiful Header
        gr.HTML("""
            <div class="header-banner">
                <h1>🎓 Learnbee MCP - Educational Tutor</h1>
                <p><strong>Intelligent Learning Assistant for Early Childhood Education</strong></p>
                <p>Interactive lessons • Personalized tutoring • Multilingual support 🌍</p>
                <p style="font-size: 0.95rem; margin-top: 0.5rem; opacity: 0.9;">
                    ✨ Designed for ages 3-6 • Powered by MCP Technology
                </p>
            </div>
        """)

        with gr.Tab("Chat"):
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

                    # Language selection
                    with gr.Row():
                        language_dropdown = gr.Dropdown(
                            label="🌍 Language",
                            choices=LANGUAGES,
                            value="English",
                            interactive=True,
                            info="Initial language for the lesson introduction. The tutor will then adapt to the child's language."
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
                        gr.HTML("""
                            <div class="info-box">
                                <p style="margin: 0 0 0.75rem 0; font-weight: 600;">
                                    🌍 <strong>Multilingual Support</strong>
                                </p>
                                <p style="margin: 0 0 0.75rem 0;">
                                    The tutor will automatically respond in the same language you use! Just start chatting in your preferred language (English, Spanish, French, etc.) and the tutor will match it.
                                </p>
                                <p style="margin: 0; font-weight: 600;">
                                    🔄 <strong>Note:</strong>
                                </p>
                                <p style="margin: 0.25rem 0 0 0;">
                                    Once you start chatting, you can't change the lesson or tutor. If you want to pick a different one, just hit the reset button and start fresh! 😊
                                </p>
                            </div>
                        """)

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
                        inputs=[lesson_dropdown, tutor_dropdown, language_dropdown],
                        outputs=[
                            lesson_name,
                            lesson_content,
                            status_markdown,
                            chat_interface.chatbot_value,
                        ],
                    )

                    reset_button = gr.Button("Reset", variant="secondary")
                    reset_button.click(
                        fn=reset_chat_interface,
                        outputs=[
                            lesson_dropdown,
                            lesson_content,
                            tutor_dropdown,
                            difficulty_dropdown,
                            language_dropdown,
                            status_markdown,
                            chat_interface.chatbot_value,
                        ],
                    )

        with gr.Tab("Create Lesson"):
            gr.Markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2 style="color: #667eea; margin-bottom: 0.5rem;">✨ Create New Lesson</h2>
                    <p>Generate a new educational lesson using ChatGPT. Just enter a topic and we'll create a complete lesson for you!</p>
                </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    topic_input = gr.Textbox(
                        label="📝 Lesson Topic",
                        placeholder="e.g., dinosaurs, space, ocean animals, colors, numbers...",
                        lines=2,
                        info="Enter the topic you want to create a lesson about"
                    )
                    
                    lesson_name_input = gr.Textbox(
                        label="📚 Lesson Name (Optional)",
                        placeholder="Leave empty to auto-generate from topic",
                        info="Custom name for the lesson file. If empty, will be generated from the topic."
                    )
                    
                    age_range_input = gr.Dropdown(
                        label="👶 Age Range",
                        choices=["3-6", "4-7", "5-8", "6-9", "7-10"],
                        value="3-6",
                        info="Target age range for the lesson"
                    )
                    
                    create_button = gr.Button("✨ Create Lesson with ChatGPT", variant="primary", size="lg")
                    
                    gr.HTML("""
                        <div class="info-box" style="margin-top: 1rem;">
                            <p style="margin: 0 0 0.5rem 0; font-weight: 600;">
                                💡 <strong>How it works:</strong>
                            </p>
                            <p style="margin: 0;">
                                1. Enter a topic you want to teach (e.g., "dinosaurs", "space")<br>
                                2. Optionally provide a custom lesson name<br>
                                3. Select the target age range<br>
                                4. Click "Create Lesson" and ChatGPT will generate the content<br>
                                5. Once created, the lesson will appear in the lesson list and can be used with the tutor!
                            </p>
                        </div>
                    """)
                
                with gr.Column(scale=2):
                    result_output = gr.Textbox(
                        label="Result",
                        lines=15,
                        placeholder="The result of lesson creation will appear here...",
                        interactive=False
                    )
            
            create_button.click(
                fn=create_new_lesson,
                inputs=[topic_input, lesson_name_input, age_range_input],
                outputs=[result_output, topic_input, lesson_dropdown],
            )

        with gr.Tab("List Lessons"):
            gr.Markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2 style="color: #667eea; margin-bottom: 0.5rem;">📚 Available Lessons</h2>
                    <p>Get the complete list of available lessons in the system.</p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    btn = gr.Button("Get Lessons List", variant="primary")
                with gr.Column(scale=3):
                    output_text = gr.Textbox(label="Lessons", lines=15, placeholder="Click 'Get Lessons List' to see all available lessons...")
            btn.click(get_lesson_list, None, output_text)

        with gr.Tab("Lesson Content"):
            gr.Markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2 style="color: #667eea; margin-bottom: 0.5rem;">📖 Lesson Content Viewer</h2>
                    <p>Retrieve and view the full content of any lesson by its name.</p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    lesson_name_input = gr.Textbox(label="Lesson Name", placeholder="Enter the name of the lesson...")
                    lesson_len = gr.Number(label="Max Length", value=1000, minimum=100, maximum=100000, step=100)
                    btn = gr.Button("Get Lesson Content", variant="primary")
                with gr.Column(scale=2):
                    lesson_content_output = gr.Textbox(label="Lesson Content", lines=25, placeholder="Enter a lesson name and click 'Get Lesson Content' to view it here...")
            btn.click(get_lesson_content, [lesson_name_input, lesson_len], lesson_content_output)

    return demo


if __name__ == "__main__":
    demo = gradio_ui()

    # Launch the Gradio app with MCP server enabled.
    # NOTE: It is required to restart the app when you add or remove MCP tools.
    demo.launch(mcp_server=True)
