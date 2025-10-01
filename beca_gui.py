"""
BECA GUI - Gradio interface for BECA agent
"""
import sys
import os
import gradio as gr
from typing import List, Tuple

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import the LangChain agent
try:
    from langchain_agent import chat_with_agent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import LangChain agent: {e}")
    AGENT_AVAILABLE = False


def chat_with_beca(message: str, history: List[Tuple[str, str]]) -> str:
    """
    Chat function for BECA using LangChain agent.

    Args:
        message: User's message
        history: Chat history (list of tuples: (user_msg, assistant_msg))

    Returns:
        Assistant's response
    """
    if not AGENT_AVAILABLE:
        return "ERROR: LangChain agent not available. Check the console for errors."

    if not message or not message.strip():
        return "Please enter a message."

    try:
        response = chat_with_agent(message)
        return response
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

# Create Gradio interface
with gr.Blocks(title="BECA - Your Autonomous Coding Agent") as demo:
    gr.Markdown("# 🤖 BECA - Build, Enhance, Code, Automate")
    gr.Markdown("Your personal AI coding assistant powered by local Qwen2.5-coder model")

    chatbot = gr.Chatbot(
        label="Chat with BECA",
        height=500,
        show_label=True,
        show_copy_button=True
    )

    with gr.Row():
        msg = gr.Textbox(
            label="Your Message",
            placeholder="Ask BECA to build something, fix a bug, or help with code...",
            scale=9
        )
        submit = gr.Button("Send", variant="primary", scale=1)

    with gr.Row():
        clear = gr.Button("Clear Chat")

    gr.Markdown("### Examples:")
    gr.Examples(
        examples=[
            "Create a React app for tracking my todo list",
            "Help me scaffold a Flask API",
            "Search the web for React best practices",
        ],
        inputs=msg
    )

    # Event handlers
    msg.submit(chat_with_beca, [msg, chatbot], [chatbot])
    submit.click(chat_with_beca, [msg, chatbot], [chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    print("Starting BECA GUI...")
    print("Open your browser to http://localhost:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)
