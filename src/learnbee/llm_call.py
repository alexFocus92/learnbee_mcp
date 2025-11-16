import os
from typing import Generator

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


class LLMCall:
    """LLM client using OpenAI API for educational tutoring."""

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM client.

        Args:
            model (str): The OpenAI model to use. Defaults to "gpt-4o-mini".
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def _convert_history(self, message: str, gradio_history: list) -> list[dict]:
        """Convert Gradio history format to OpenAI API format."""
        messages = []
        for h in gradio_history:
            # Skip system messages in history (we'll add it separately)
            if h.get("role") == "system":
                continue
            messages.append(
                {
                    "role": h.get("role", "user"),
                    "content": h.get("content", ""),
                }
            )
        # Add current user input
        messages.append({"role": "user", "content": message})
        return messages

    def respond(
        self,
        message: str,
        history: list,
        system_prompt: str = None,
        tutor_name: str = None,
        difficulty_level: str = "beginner",
    ) -> Generator[str, None, None]:
        """
        Generate a response to the user message using the OpenAI LLM.

        Args:
            message (str): The user's message.
            history (list): The conversation history.
            system_prompt (str): The system prompt (optional, will be constructed if not provided).
            tutor_name (str): The name of the tutor.
            difficulty_level (str): The difficulty level (beginner, intermediate, advanced).

        Yields:
            str: Streaming response chunks.
        """
        # Construct messages for OpenAI API
        messages = []
        
        # Add system prompt
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history (excluding system messages)
        for h in history:
            if h.get("role") != "system":
                messages.append(
                    {
                        "role": h.get("role", "user"),
                        "content": h.get("content", ""),
                    }
                )
        
        # Add current user message
        messages.append({"role": "user", "content": message})

        # Make streaming API call with educational-appropriate settings
        # Lower temperature for more consistent, educational responses
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=0.6,  # Balanced: creative enough for engagement, consistent for learning
            max_tokens=500,  # Limit response length for age-appropriate brevity
        )

        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                response += content
                yield response

    def extract_key_concepts(self, lesson_content: str) -> list[str]:
        """
        Extract key concepts from the lesson content.

        Args:
            lesson_content (str): The content of the lesson.

        Returns:
            list[str]: A list of 5 to 10 key concepts from the lesson.
        """
        system_prompt = (
            "Your task is to extract 5 to 10 key educational concepts from the provided lesson content. "
            "These concepts should be appropriate for early childhood education (ages 3-6). "
            "Return only the concept names, one per line. "
            "Do not include any additional text, explanations, or numbering. "
            "Each concept should be a simple, clear phrase that a child could understand. "
            "Example output:\n"
            "Colors\n"
            "Numbers\n"
            "Shapes\n"
            "Animals\n"
            "Nature\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lesson_content},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
        )

        content = response.choices[0].message.content
        print("Response from LLM:", content)

        # Split the response by new lines and strip whitespace
        concepts = [concept.strip() for concept in content.split("\n") if concept.strip()]

        # Limit to 10 concepts
        return concepts[:10]

    def generate_lesson_introduction(
        self, lesson_content: str, lesson_name: str, concepts: list[str]
    ) -> str:
        """
        Generate an educational introduction for the lesson including:
        - A brief summary of the activity
        - Key concepts
        - Example questions to guide the child

        Args:
            lesson_content (str): The content of the lesson.
            lesson_name (str): The name of the lesson.
            concepts (list[str]): List of key concepts extracted from the lesson.

        Returns:
            str: A formatted introduction with summary, concepts, and example questions.
        """
        concepts_text = ", ".join(concepts[:8])  # Show up to 8 concepts
        
        system_prompt = (
            "You are an educational expert creating an introduction for a lesson for children ages 3-12. "
            "Create a friendly, engaging introduction that includes:\n\n"
            "1. A brief, exciting summary of what the child will learn (2-3 sentences, very simple language)\n"
            "2. A list of the key concepts they'll explore\n"
            "3. 2-3 example questions that the tutor could ask to start the conversation and guide the child\n\n"
            "Format your response as follows:\n"
            "SUMMARY:\n"
            "[Brief summary here]\n\n"
            "KEY CONCEPTS:\n"
            "[List concepts here, one per line with a bullet point]\n\n"
            "EXAMPLE QUESTIONS TO GET STARTED:\n"
            "[2-3 engaging questions, one per line with a bullet point]\n\n"
            "Use very simple, age-appropriate language. Make it fun and exciting! "
            "The questions should be open-ended and encourage exploration."
        )

        user_prompt = (
            f"Lesson Name: {lesson_name}\n\n"
            f"Key Concepts: {concepts_text}\n\n"
            f"Lesson Content:\n{lesson_content[:2000]}\n\n"
            "Create an engaging introduction for this lesson."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,  # Slightly higher for creativity
            max_tokens=400,
        )

        introduction = response.choices[0].message.content
        return introduction
