"""Gradio UI components and interface definition."""

import json
import gradio as gr

from learnbee.constants import TUTOR_NAMES, LANGUAGES, DIFFICULTY_LEVELS, AGE_RANGES, get_tutor_names
from learnbee.mcp_server import get_lesson_list, get_lesson_content
from learnbee.theme import BEAUTIFUL_THEME, CUSTOM_CSS
from learnbee.tutor_handlers import (
    load_lesson_content,
    reset_chat_interface,
    create_new_lesson,
    custom_respond
)


def create_gradio_ui():
    """
    Create and return the Gradio interface for the Learnbee MCP application.
    
    Returns:
        Gradio Blocks interface
    """
    lesson_name = gr.BrowserState("")
    selected_tutor = gr.BrowserState(get_tutor_names()[0] if TUTOR_NAMES else "")

    lesson_choices = json.loads(get_lesson_list())

    with gr.Blocks(theme=BEAUTIFUL_THEME, css=CUSTOM_CSS, title="Learnbee MCP - Educational Tutor") as demo:

        # Beautiful Header
        gr.HTML("""
            <div class="header-banner">
                <h1>🎓 Learnbee MCP - Educational Tutor</h1>
                <p><strong>Intelligent Learning Assistant for Early Childhood Education</strong></p>
                <p>Interactive lessons • Personalized tutoring • Multilingual support 🌍</p>
                <p style="font-size: 0.95rem; margin-top: 0.5rem; opacity: 0.9;">
                    ✨ Designed for ages 3-12 • Powered by MCP Technology
                </p>
            </div>
        """)

        with gr.Tab("Chat"):
            # Welcome Card - Modern and User-Friendly
            welcome_card = gr.HTML("""
                <div class="welcome-card">
                    <div class="welcome-header">
                        <div class="welcome-icon">👋</div>
                        <h2 class="welcome-title">Welcome to Learnbee!</h2>
                        <p class="welcome-subtitle">Your intelligent learning companion for ages 3-12</p>
                    </div>
                    
                    <div class="getting-started-section">
                        <h3 class="section-title">
                            <span class="section-icon">🚀</span>
                            Getting Started
                        </h3>
                        <div class="steps-container">
                            <div class="step-item">
                                <div class="step-number">1</div>
                                <div class="step-content">
                                    <strong>Select a Lesson</strong>
                                    <p>Choose from our library of educational lessons</p>
                                </div>
                            </div>
                            <div class="step-item">
                                <div class="step-number">2</div>
                                <div class="step-content">
                                    <strong>Choose Your Tutor</strong>
                                    <p>Pick your favorite character to guide you</p>
                                </div>
                            </div>
                            <div class="step-item">
                                <div class="step-number">3</div>
                                <div class="step-content">
                                    <strong>Set Difficulty</strong>
                                    <p>Select your comfort level: Beginner, Intermediate, or Advanced</p>
                                </div>
                            </div>
                            <div class="step-item">
                                <div class="step-number">4</div>
                                <div class="step-content">
                                    <strong>Load & Start</strong>
                                    <p>Click 'Load Lesson & Prepare Tutor' to begin</p>
                                </div>
                            </div>
                            <div class="step-item step-final">
                                <div class="step-number">✨</div>
                                <div class="step-content">
                                    <strong>Start Learning!</strong>
                                    <p>Chat with your tutor and solve fun problems together</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info-badge">
                        <span class="badge-icon">🎓</span>
                        <span>Designed for ages 3-12 • Interactive problem-solving • Multilingual support</span>
                    </div>
                </div>
            """)
            
            # Status (hidden initially, shown after lesson is loaded)
            status_markdown = gr.Markdown(label="Status", visible=False)

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
                            choices=[f"{name} - {desc}" for name, desc in TUTOR_NAMES],
                            value=f"{get_tutor_names()[0]} - {TUTOR_NAMES[0][1]}" if TUTOR_NAMES else None,
                            interactive=True,
                            info="Choose your favorite tutor to guide your learning journey"
                        )

                    # Difficulty level selection
                    with gr.Row():
                        difficulty_dropdown = gr.Dropdown(
                            label="📊 Difficulty Level",
                            choices=DIFFICULTY_LEVELS,
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

                        def update_tutor_selection(tutor_with_desc):
                            """Update selected tutor, extracting just the name."""
                            if tutor_with_desc:
                                # Extract tutor name (before the " - " separator)
                                tutor_name = tutor_with_desc.split(" - ")[0]
                                return tutor_name
                            return get_tutor_names()[0] if TUTOR_NAMES else ""

                        tutor_dropdown.change(
                            fn=update_tutor_selection,
                            inputs=[tutor_dropdown],
                            outputs=[selected_tutor],
                        )

                    # Spacer where the multilingual card used to be (moved to footer)
                    with gr.Row():
                        gr.HTML('<div style="height:0.5rem;"></div>')

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
                            welcome_card,
                            status_markdown,
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
                            welcome_card,
                        ],
                    )
                    
                    # Helper function to format tutor for dropdown
                    def format_tutor_for_dropdown(tutor_name):
                        """Format tutor name with description for dropdown."""
                        if not tutor_name:
                            return f"{get_tutor_names()[0]} - {TUTOR_NAMES[0][1]}" if TUTOR_NAMES else None
                        for name, desc in TUTOR_NAMES:
                            if name == tutor_name:
                                return f"{name} - {desc}"
                        return f"{get_tutor_names()[0]} - {TUTOR_NAMES[0][1]}" if TUTOR_NAMES else None

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
                        choices=AGE_RANGES,
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
                    output_text = gr.Textbox(
                        label="Lessons",
                        lines=15,
                        placeholder="Click 'Get Lessons List' to see all available lessons..."
                    )
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
                    lesson_name_input = gr.Textbox(
                        label="Lesson Name",
                        placeholder="Enter the name of the lesson..."
                    )
                    lesson_len = gr.Number(
                        label="Max Length",
                        value=1000,
                        minimum=100,
                        maximum=100000,
                        step=100
                    )
                    btn = gr.Button("Get Lesson Content", variant="primary")
                with gr.Column(scale=2):
                    lesson_content_output = gr.Textbox(
                        label="Lesson Content",
                        lines=25,
                        placeholder="Enter a lesson name and click 'Get Lesson Content' to view it here..."
                    )
            btn.click(get_lesson_content, [lesson_name_input, lesson_len], lesson_content_output)

        # Footer: Multilingual Support (full-width)
        gr.HTML("""
            <footer class="multilingual-footer">
                <div>
                    <div class="multilingual-row">
                            <span class="multilingual-icon" aria-hidden="true">🌍</span>
                            <div class="multilingual-content">
                                <div class="multilingual-title">Multilingual Support</div>
                                <div class="multilingual-desc">The tutor automatically responds in your language. Chat in Spanish, English, French, or any language you prefer.</div>
                            </div>
                            <div class="multilingual-reset-wrap">
                                <small class="multilingual-reset">🔄 Use the 'Reset' button to change lesson or tutor during a session.</small>
                            </div>
                    </div>
                </div>
            </footer>
        """)

    return demo

