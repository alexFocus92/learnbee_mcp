import json
from pathlib import Path

from learnbee.llm_call import LLMCall


def get_lesson_list() -> str:
    """
    Get list of available lessons.

    Returns:
        str: JSON string containing the list of lesson names.
    """
    lessons_dir = Path("./lessons")
    if not lessons_dir.exists():
        return json.dumps("Error: Lessons directory not found.")

    text_files = []
    for file in lessons_dir.iterdir():
        if file.is_file() and file.suffix.lower() == ".txt":
            text_files.append(file.stem)

    return json.dumps(sorted(text_files))


def get_lesson_content(lesson_name: str, max_length: int = 0) -> str:
    """
    Get the content of a lesson.

    Args:
        lesson_name (str): The name of the lesson (without .txt extension).
        max_length (int): The maximum length of the content to return. If 0, return the full content.
    Returns:
        str: The content of the lesson, or an error message if the lesson is not found.
    """
    lessons_dir = Path("./lessons")
    lesson_file = lessons_dir / f"{lesson_name}.txt"
    if not lesson_file.exists():
        return f"Error: Lesson '{lesson_name}' not found."

    with open(lesson_file, "r", encoding="utf-8") as f:
        content = f.read()

    if not max_length:
        return content
    else:
        return content[:max_length]


def get_lesson_introduction(lesson_name: str) -> str:
    """
    Get an educational introduction for a lesson including summary, key concepts, and example questions.
    This function serves as an MCP tool to help guide children with their first message.

    Args:
        lesson_name (str): The name of the lesson (without .txt extension).

    Returns:
        str: A formatted introduction with summary, concepts, and example questions, or an error message.
    """
    lessons_dir = Path("./lessons")
    lesson_file = lessons_dir / f"{lesson_name}.txt"
    if not lesson_file.exists():
        return f"Error: Lesson '{lesson_name}' not found."

    # Get lesson content
    lesson_content = get_lesson_content(lesson_name, max_length=50000)
    
    if lesson_content.startswith("Error:"):
        return lesson_content

    try:
        # Extract key concepts
        call_llm = LLMCall()
        concepts = call_llm.extract_key_concepts(lesson_content)
        
        if not concepts:
            return f"Error: Could not extract key concepts from lesson '{lesson_name}'."
        
        # Generate introduction
        introduction = call_llm.generate_lesson_introduction(
            lesson_content, lesson_name, concepts
        )
        
        return introduction
    except Exception as e:
        return f"Error generating introduction: {str(e)}"


def create_lesson(topic: str, lesson_name: str = None, age_range: str = "3-6") -> str:
    """
    Create a new lesson by generating content with ChatGPT based on a topic.
    The lesson will be saved to the lessons directory and can be used immediately.
    
    Args:
        topic (str): The topic for the lesson (e.g., "dinosaurs", "space", "ocean animals").
        lesson_name (str): Optional name for the lesson file. If not provided, will be generated from topic.
        age_range (str): The target age range. Defaults to "3-6".
    
    Returns:
        str: Success message with the lesson name, or an error message if creation fails.
    """
    lessons_dir = Path("./lessons")
    
    # Create lessons directory if it doesn't exist
    lessons_dir.mkdir(exist_ok=True)
    
    # Generate lesson name from topic if not provided
    if not lesson_name:
        # Convert topic to a valid filename (lowercase, replace spaces with underscores)
        lesson_name = topic.lower().strip().replace(" ", "_").replace("/", "_").replace("\\", "_")
        # Remove special characters
        lesson_name = "".join(c for c in lesson_name if c.isalnum() or c in ("_", "-"))
    
    # Remove .txt extension if present
    if lesson_name.endswith(".txt"):
        lesson_name = lesson_name[:-4]
    
    lesson_file = lessons_dir / f"{lesson_name}.txt"
    
    # Check if lesson already exists
    if lesson_file.exists():
        return f"Error: A lesson named '{lesson_name}' already exists. Please choose a different name."
    
    try:
        # Generate lesson content using LLM
        call_llm = LLMCall()
        lesson_content = call_llm.generate_lesson(topic, age_range)
        
        # Save lesson to file
        with open(lesson_file, "w", encoding="utf-8") as f:
            f.write(lesson_content)
        
        return f"✅ Successfully created lesson '{lesson_name}' about '{topic}'! The lesson is now available in the lesson list and ready to use with the tutor."
    
    except Exception as e:
        return f"Error creating lesson: {str(e)}"


if __name__ == "__main__":
    print("Available lessons:", get_lesson_list())

    lesson_name = "example_lesson"
    lesson_content = get_lesson_content(lesson_name)
    print(f"Start of '{lesson_name}':\n{lesson_content[:500]}...\n")
    print(f"End of '{lesson_name}':\n{lesson_content[-500:]}\n")
