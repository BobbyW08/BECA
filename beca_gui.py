"""
BECA GUI - Gradio interface for BECA agent
"""
import sys
import os
import gradio as gr
from typing import List, Dict

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


def chat_with_beca(message: str, history: List[Dict[str, str]]):
    """
    Chat function for BECA using LangChain agent.
    Uses generator pattern to immediately show user message.

    Args:
        message: User's message
        history: Chat history (list of message dicts with 'role' and 'content')

    Yields:
        Updated chat history at each step
    """
    # Immediately show user's message
    history.append({"role": "user", "content": message})
    yield history

    if not AGENT_AVAILABLE:
        history.append({"role": "assistant", "content": "ERROR: LangChain agent not available. Check the console for errors."})
        yield history
        return

    if not message or not message.strip():
        history.append({"role": "assistant", "content": "Please enter a message."})
        yield history
        return

    try:
        # Show thinking indicator
        history.append({"role": "assistant", "content": "🤔 Thinking..."})
        yield history

        # Get actual response
        response = chat_with_agent(message)

        # Replace thinking message with actual response
        history[-1] = {"role": "assistant", "content": response}
        yield history

    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nMake sure Ollama is running."
        history[-1] = {"role": "assistant", "content": error_msg}
        yield history

# Create Gradio interface
with gr.Blocks(title="BECA - Your Autonomous Coding Agent") as demo:
    gr.Markdown("# 🤖 BECA - Badass Expert Coding Agent")
    gr.Markdown("Your personal AI coding assistant powered by Llama 3.1 with persistent memory 🧠")

    chatbot = gr.Chatbot(
        label="Chat with BECA",
        height=500,
        show_label=True,
        show_copy_button=True,
        type="messages"  # Use modern message format
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
            "Remember that I prefer TypeScript over JavaScript",
            "What are my saved preferences?",
        ],
        inputs=msg
    )

    gr.Markdown("""
    ### 🧠 Memory Features
    BECA now remembers:
    - **Conversation history** - Recalls past discussions
    - **Your preferences** - Automatically applies your coding style
    - **Successful patterns** - Reuses solutions that worked before
    - **Tool statistics** - Tracks what tools work best

    Try asking: "Remember that I prefer React over Vue" or "What did we talk about yesterday?"
    """)

    # Event handlers
    msg.submit(chat_with_beca, [msg, chatbot], [chatbot]).then(
        lambda: "", None, msg  # Clear the input box after submitting
    )
    submit.click(chat_with_beca, [msg, chatbot], [chatbot]).then(
        lambda: "", None, msg  # Clear the input box after clicking
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    print("Starting BECA GUI...")
    demo.launch(server_name="127.0.0.1", share=False)
