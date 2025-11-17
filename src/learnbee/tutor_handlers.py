"""Handler functions for tutor interactions and lesson management."""

import json
import gradio as gr

from learnbee.constants import LESSON_CONTENT_MAX_LENGTH, TUTOR_NAMES, get_tutor_names, get_tutor_description
from learnbee.llm_call import LLMCall
from learnbee.mcp_server import create_lesson, get_lesson_content, get_lesson_list
from learnbee.prompts import generate_tutor_system_prompt


def load_lesson_content(lesson_name, selected_tutor, selected_language, progress=gr.Progress()):
    """
    Load lesson content and extract key concepts.
    
    Returns introduction message for chatbot.
    
    Args:
        lesson_name: Name of the lesson to load
        selected_tutor: Name of the selected tutor
        selected_language: Language for the introduction
        progress: Gradio progress tracker
    
    Returns:
        Tuple of (lesson_name, lesson_content, status_message, chatbot_messages, welcome_visible, status_visible)
    """
    if not lesson_name:
        return "", "", "Please select a lesson first.", [], gr.update(visible=True), gr.update(visible=False)
    
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
                gr.update(visible=False),  # Hide welcome card
                gr.update(visible=True, value=status_message),  # Show status
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
                gr.update(visible=False),  # Hide welcome card
                gr.update(visible=True, value=status_message),  # Show status
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
            gr.update(visible=False),  # Hide welcome card
            gr.update(visible=True, value=status_message),  # Show status
        )


def reset_chat_interface():
    """
    Reset the chat interface to initial state.
    
    Returns:
        Tuple of Gradio update objects for resetting all interface elements
    """
    from learnbee.constants import TUTOR_NAMES, get_tutor_names
    
    # Format tutor with description for dropdown
    tutor_value = None
    if TUTOR_NAMES:
        first_tutor_name = get_tutor_names()[0]
        first_tutor_desc = TUTOR_NAMES[0][1]
        tutor_value = f"{first_tutor_name} - {first_tutor_desc}"
    
    return (
        gr.update(value=""),
        gr.update(value=""),
        gr.update(value=tutor_value),
        gr.update(value="beginner"),
        gr.update(value="English"),
        gr.update(visible=False),  # Hide status
        [],
        gr.update(visible=True),  # Show welcome card
    )


def create_new_lesson(topic, lesson_name, age_range, progress=gr.Progress()):
    """
    Create a new lesson from a topic using ChatGPT.
    
    Args:
        topic: Topic for the lesson
        lesson_name: Optional custom name for the lesson
        age_range: Target age range
        progress: Gradio progress tracker
    
    Returns:
        Tuple of (result_message, empty_topic, lesson_dropdown_update)
    """
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
    """
    Custom respond function with educational system prompt.
    
    Args:
        message: User's message
        history: Conversation history
        lesson_name: Name of the current lesson
        lesson_content: Content of the lesson
        selected_tutor: Name of the selected tutor
        difficulty_level: Difficulty level (beginner, intermediate, advanced)
    
    Yields:
        Response chunks from the LLM
    """
    if not lesson_name or not selected_tutor:
        yield "Please select a lesson and tutor first."
        return

    if not lesson_content:
        lesson_content = get_lesson_content(lesson_name, LESSON_CONTENT_MAX_LENGTH)

    # Get tutor description
    tutor_description = get_tutor_description(selected_tutor)
    if not tutor_description:
        tutor_description = "a friendly and patient educational tutor"

    # Generate educational system prompt with enhanced pedagogy focused on problem-solving
    system_prompt = generate_tutor_system_prompt(
        tutor_name=selected_tutor,
        tutor_description=tutor_description,
        difficulty_level=difficulty_level,
        lesson_content=lesson_content
    )

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

