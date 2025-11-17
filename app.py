"""Main entry point for the Learnbee MCP Educational Tutor application."""

import os
import sys

# Add src directory to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

from learnbee.ui import create_gradio_ui


if __name__ == "__main__":
    demo = create_gradio_ui()

    # Launch the Gradio app with MCP server enabled.
    # NOTE: It is required to restart the app when you add or remove MCP tools.
    demo.launch(mcp_server=True)
