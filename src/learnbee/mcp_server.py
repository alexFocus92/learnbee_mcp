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


if __name__ == "__main__":
    print("Available lessons:", get_lesson_list())

    lesson_name = "example_lesson"
    lesson_content = get_lesson_content(lesson_name)
    print(f"Start of '{lesson_name}':\n{lesson_content[:500]}...\n")
    print(f"End of '{lesson_name}':\n{lesson_content[-500:]}\n")
