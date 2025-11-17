---
title: Learnbee-mcp
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.33.0
python_version: 3.13
app_file: app.py
pinned: true
license: mit
short_description: Interactive educational tutor for primary education.
thumbnail: https://huggingface.co/spaces/Agents-MCP-Hackathon/consilium_mcp/blob/main/assets/logo_learnbee.png
tags:
  - building-mcp-track-creative
  - building-mcp-track-consumer
  - mcp-in-action-track-consumer
  - mcp-in-action-track-creative
  - education
  - early-childhood
---

<!-- Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference -->


# Learnbee-mcp 🎓

## Website
access the live demo here: 
[Learnbee-mcp on Hugging Face Spaces](https://huggingface.co/spaces/MCP-1st-Birthday/learnbee_mcp)

## What is this?

**Learnbee-mcp** is an interactive educational system designed for children in early childhood education (ages 3-6). It uses the Model Context Protocol (MCP) to provide educational conversations and interactive activities based on lesson content.

The system allows children to interact with friendly educational tutors who guide learning through questions, hints, and age-appropriate explanations, rather than giving direct answers. This encourages curiosity, critical thinking, and active participation in the learning process.

### Key Features

- 🎯 **Customizable Educational Tutors**: Choose from different tutors with friendly personalities (Professor Owl, Star Explorer, Logic Bot, Nature Guide, Story Friend)
- 📚 **Customizable Lessons**: Load educational content from text files in the `./lessons` directory
- 🎚️ **Difficulty Levels**: Adjust the difficulty level (beginner, intermediate, advanced) according to the child's needs
- 🌍 **Multilingual**: Automatic language detection - the tutor responds in the same language the child uses
- 🧠 **Key Concept Extraction**: The system automatically identifies key educational concepts from each lesson
- 🛡️ **Child-Safe**: Built-in safety filters to keep conversations age-appropriate

### Demo

<p align="center">
  <img src="./assets/screenshot.png" alt="Screenshot" height="200"/><br>
  <span>Interactive educational interface</span>
</p>

## How to Use

1. **Select a Lesson**: Choose a lesson from the dropdown menu (lessons are loaded from `.txt` files in the `./lessons` directory)
2. **Choose a Tutor**: Select one of the available educational tutors
3. **Adjust Difficulty Level**: Select the appropriate level for the child
4. **Load the Lesson**: Click "Load Lesson & Prepare Tutor" to load the content and extract key concepts
5. **Start Learning!**: Begin a conversation with the tutor about the lesson content

### Tips

- The tutor will not give direct answers, but will ask follow-up questions and offer hints to encourage thinking
- If the child deviates from the topic, the tutor will gently redirect the conversation back to the lesson
- The tutor automatically detects and responds in the same language the child uses - just start chatting in your preferred language!

## Development

If you want to develop this project, here are the details to get you started.

### Prerequisites

- **Python 3.12+**
- **Gradio**: Provides the user interface for educational conversations
- **OpenAI API**: Used to generate tutor responses and extract key concepts
- This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Please install uv if you haven't already.

### Installation

After cloning the repository, you can run the following command to install dependencies:

```sh
uv sync --frozen
```

Or using pip:

```sh
pip install -r requirements.txt
```

### Configuration

1. **Set up environment variables**:
   - Copy the `.env.example` file to `.env`:
     ```sh
     cp .env.example .env
     ```
   - Edit the `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

2. **Prepare lessons**:
   - Create text files (`.txt`) in the `./lessons` directory with educational content
   - Each file should contain the lesson content in plain text
   - The system will automatically extract key concepts from each lesson

### Run Locally

```sh
uv run gradio app.py
```

Or using python directly:

```sh
python app.py
```

- Hot reloading is enabled by default.

### Project Structure

```
learnbee-mcp/
├── app.py                 # Main Gradio application
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not committed to repository)
├── .env.example           # Environment variables template
├── lessons/               # Directory with lesson files (.txt)
│   ├── example_colors.txt # Colors lesson
│   ├── numbers_1_to_10.txt # Numbers lesson
│   ├── shapes.txt         # Shapes lesson
│   ├── animals.txt        # Animals lesson
│   └── weather_and_seasons.txt # Weather and seasons lesson
└── src/
    └── learnbee/          # Main module
        ├── __init__.py
        ├── llm_call.py    # LLM client with OpenAI API
        ├── mcp_server.py  # MCP server for managing lessons
        └── mcp_client.py  # MCP client (optional)
```

### Deploy to Hugging Face Spaces

1. Make sure all dependencies are in `requirements.txt`
2. Set up the `OPENAI_API_KEY` environment variable in Hugging Face Spaces settings
3. Push the code to the repository

```sh
git add .
git commit -m "Deploy Learnbee-mcp"
git push
```

## Customization

### Adding New Tutors

You can add new tutors by editing the `TUTOR_NAMES` list in `app.py`:

```python
TUTOR_NAMES = ["Professor Owl", "Star Explorer", "Logic Bot", "Nature Guide", "Story Friend", "Your New Tutor"]
```

### Creating New Lessons

1. Create a text file in the `./lessons` directory
2. Write educational content appropriate for ages 3-6
3. The system will automatically detect and load the new lesson

### Adjusting Tutor Behavior

You can modify the `system_prompt` in the `custom_respond` function in `app.py` to adjust the tutor's pedagogical behavior.

## Technologies Used

- **Gradio**: Framework for interactive user interfaces
- **OpenAI API**: Language model for generating educational responses
- **Model Context Protocol (MCP)**: Protocol for managing lesson context
- **Python 3.12+**: Main programming language

## License

MIT License

## Contributing

Contributions are welcome. Please open an issue or pull request if you have suggestions or improvements.

---

**Learnbee-mcp** - Making learning interactive and fun for the little ones 🎓✨


### 📬 Contact info

* GitHub: @alexFocus92
* Hugging Face: @AlexFocus
* X: @alexFocus8