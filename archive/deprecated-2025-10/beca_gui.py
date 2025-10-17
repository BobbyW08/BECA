"""
BECA GUI - Enhanced Gradio interface for BECA agent with visual features
"""
import sys
import os
import gradio as gr
from typing import List, Dict, Tuple
from pathlib import Path

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

# Import GUI utilities
try:
    from gui_utils import file_tree_manager, code_viewer, diff_viewer
    GUI_UTILS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import GUI utilities: {e}")
    GUI_UTILS_AVAILABLE = False

# Import file tracker
try:
    from file_tracker import file_tracker
    FILE_TRACKER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import file tracker: {e}")
    FILE_TRACKER_AVAILABLE = False

# Import autonomous learning system
try:
    from autonomous_learning import start_autonomous_learning, get_learning_stats
    AUTONOMOUS_LEARNING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import autonomous learning: {e}")
    AUTONOMOUS_LEARNING_AVAILABLE = False

# Import meta-learning system
try:
    from meta_learning_system import MetaLearningSystem
    from meta_learning_dashboard import LearningDashboard
    META_LEARNING_AVAILABLE = True
    # Initialize meta-learning system
    meta_learning = MetaLearningSystem("beca_memory.db")
    meta_dashboard = LearningDashboard("beca_memory.db")
except ImportError as e:
    print(f"Warning: Could not import meta-learning system: {e}")
    META_LEARNING_AVAILABLE = False
    meta_learning = None
    meta_dashboard = None

# Global state for file operations
current_file_content = {}  # Store original content for diffing

# Global state for meta-learning
meta_learning_enabled = True  # Auto-enabled by default
current_session_id = None
current_feature_tag = None


def refresh_file_tree() -> str:
    """Refresh and return the file tree HTML"""
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>"

    # Sync file tracker status with file tree manager
    if FILE_TRACKER_AVAILABLE:
        file_tree_manager.new_files = file_tracker.new_files.copy()
        file_tree_manager.modified_files = file_tracker.modified_files.copy()

    tree = file_tree_manager.build_tree()
    return file_tree_manager.to_html(tree)


def view_file(filepath: str) -> Tuple[str, str]:
    """
    View a file with syntax highlighting

    Args:
        filepath: Path to file relative to working directory

    Returns:
        Tuple of (highlighted_html, status_message)
    """
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>", "Error: GUI utilities not loaded"

    if not filepath or not filepath.strip():
        return "<div>No file selected</div>", ""

    try:
        full_path = Path.cwd() / filepath
        if not full_path.exists():
            return f"<div>File not found: {filepath}</div>", "Error: File not found"

        # Store original content for future diffing
        with open(full_path, 'r', encoding='utf-8') as f:
            current_file_content[filepath] = f.read()

        html, error = code_viewer.read_and_highlight(str(full_path))
        if error:
            return f"<div>Error: {error}</div>", error

        return html, f"Viewing: {filepath}"
    except Exception as e:
        return f"<div>Error viewing file: {str(e)}</div>", f"Error: {str(e)}"


def show_diff(filepath: str) -> Tuple[str, str]:
    """
    Show diff for a modified file

    Args:
        filepath: Path to file relative to working directory

    Returns:
        Tuple of (diff_html, status_message)
    """
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>", "Error"

    if filepath not in current_file_content:
        return "<div>No original content stored. View the file first.</div>", "No diff available"

    try:
        full_path = Path.cwd() / filepath
        if not full_path.exists():
            return f"<div>File not found: {filepath}</div>", "Error"

        with open(full_path, 'r', encoding='utf-8') as f:
            new_content = f.read()

        old_content = current_file_content[filepath]
        diff_html = diff_viewer.generate_diff(old_content, new_content, filepath)

        return diff_html, f"Diff for: {filepath}"
    except Exception as e:
        return f"<div>Error generating diff: {str(e)}</div>", f"Error: {str(e)}"


def chat_with_beca(message: str, history: List[Dict[str, str]]):
    """
    Chat function for BECA using LangChain agent.
    Uses generator pattern to immediately show user message.

    Args:
        message: User's message
        history: Chat history (list of message dicts with 'role' and 'content')

    Yields:
        Updated chat history, file tree HTML, status message
    """
    # Immediately show user's message
    history.append({"role": "user", "content": message})
    yield history, refresh_file_tree(), ""

    if not AGENT_AVAILABLE:
        history.append({"role": "assistant", "content": "ERROR: LangChain agent not available. Check the console for errors."})
        yield history, refresh_file_tree(), "Error: Agent not available"
        return

    if not message or not message.strip():
        history.append({"role": "assistant", "content": "Please enter a message."})
        yield history, refresh_file_tree(), ""
        return

    try:
        # Show thinking indicator
        history.append({"role": "assistant", "content": "🤔 Thinking..."})
        yield history, refresh_file_tree(), "Thinking..."

        # Get actual response
        response = chat_with_agent(message)

        # Replace thinking message with actual response
        history[-1] = {"role": "assistant", "content": response}

        # Refresh file tree after agent response (files may have been created/modified)
        yield history, refresh_file_tree(), "Response complete"

    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nMake sure Ollama is running."
        history[-1] = {"role": "assistant", "content": error_msg}
        yield history, refresh_file_tree(), f"Error: {str(e)}"

# Function to get learning status
def get_learning_status() -> str:
    """Get current autonomous learning status"""
    if AUTONOMOUS_LEARNING_AVAILABLE:
        try:
            stats = get_learning_stats()
            if stats['active']:
                return f"🧠 Auto-Learning Active | Learned: {stats['total_learned']} resources"
            else:
                return "🧠 Auto-Learning: Starting..."
        except:
            return "🧠 Auto-Learning: Initializing..."
    return "Auto-Learning: Not Available"

# Function to get meta-learning status
def get_meta_learning_status() -> str:
    """Get meta-learning system status"""
    if META_LEARNING_AVAILABLE and meta_learning_enabled:
        try:
            data = meta_dashboard.ml_system.get_learning_dashboard_data()
            return f"📊 Meta-Learning ON | Features: {data['features_built']} | Lessons: {data['lessons_learned']}"
        except:
            return "📊 Meta-Learning: Active"
    return "📊 Meta-Learning: OFF"

# Function to toggle meta-learning
def toggle_meta_learning(enabled: bool) -> str:
    """Toggle meta-learning on/off"""
    global meta_learning_enabled
    meta_learning_enabled = enabled
    if enabled:
        return "📊 Meta-Learning: Enabled - BECA will learn from your work"
    else:
        return "📊 Meta-Learning: Disabled - Learning paused"

# Function to view meta-learning dashboard
def view_meta_dashboard() -> str:
    """Generate and return meta-learning dashboard"""
    if not META_LEARNING_AVAILABLE:
        return "Meta-learning system not available"
    try:
        return meta_dashboard.generate_dashboard_report()
    except Exception as e:
        return f"Error generating dashboard: {str(e)}"

# Create Enhanced Gradio interface with three panels
with gr.Blocks(title="BECA - Your Autonomous Coding Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 BECA - Badass Expert Coding Agent")
    gr.Markdown("Your personal AI coding assistant with visual file management & autonomous learning 🧠")

    # Learning status bars
    with gr.Row():
        if AUTONOMOUS_LEARNING_AVAILABLE:
            learning_status = gr.Textbox(
                label="Autonomous Learning Status",
                value=get_learning_status(),
                interactive=False,
                max_lines=1,
                scale=1
            )
        if META_LEARNING_AVAILABLE:
            meta_status = gr.Textbox(
                label="Meta-Learning Status",
                value=get_meta_learning_status(),
                interactive=False,
                max_lines=1,
                scale=1
            )

    # Status bar
    status_bar = gr.Textbox(
        label="Status",
        value="Ready",
        interactive=False,
        max_lines=1
    )

    # Main three-panel layout
    with gr.Row():
        # Left Panel: File Tree
        with gr.Column(scale=1):
            gr.Markdown("### 📁 Project Files")
            file_tree = gr.HTML(
                value=refresh_file_tree() if GUI_UTILS_AVAILABLE else "<div>Loading...</div>",
                label="File Tree"
            )
            refresh_tree_btn = gr.Button("🔄 Refresh Tree", size="sm")

        # Middle Panel: Chat
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            chatbot = gr.Chatbot(
                label="Chat with BECA",
                height=500,
                show_label=False,
                show_copy_button=True,
                type="messages"
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Your Message",
                    placeholder="Ask BECA to build something, fix a bug, or help with code...",
                    scale=9,
                    lines=2
                )
                submit = gr.Button("Send", variant="primary", scale=1)

            with gr.Row():
                clear = gr.Button("Clear Chat", size="sm")

        # Right Panel: Code Viewer / Diff Viewer
        with gr.Column(scale=2):
            gr.Markdown("### 📝 Code View")

            with gr.Tabs():
                with gr.Tab("View File"):
                    file_path_input = gr.Textbox(
                        label="File Path",
                        placeholder="Enter file path (e.g., src/main.py)",
                        scale=8
                    )
                    with gr.Row():
                        view_btn = gr.Button("View", variant="primary", size="sm")
                        refresh_view_btn = gr.Button("Refresh", size="sm")

                    code_display = gr.HTML(
                        value="<div style='padding: 20px; color: #888;'>Enter a file path and click View</div>",
                        label="Code"
                    )

                with gr.Tab("Diff"):
                    diff_file_input = gr.Textbox(
                        label="File Path",
                        placeholder="Enter file path to show diff",
                        scale=8
                    )
                    diff_btn = gr.Button("Show Diff", variant="primary", size="sm")
                    diff_display = gr.HTML(
                        value="<div style='padding: 20px; color: #888;'>View a file first, then check diff after modifications</div>",
                        label="Diff"
                    )

    # Meta-Learning Control Panel
    if META_LEARNING_AVAILABLE:
        with gr.Accordion("📊 Meta-Learning Dashboard", open=False):
            gr.Markdown("### BECA learns from every feature you build!")
            
            meta_toggle = gr.Checkbox(
                label="Enable Meta-Learning",
                value=True,
                info="When enabled, BECA learns from development interactions"
            )
            
            meta_toggle_status = gr.Textbox(
                label="Toggle Status",
                value="📊 Meta-Learning: Enabled",
                interactive=False,
                max_lines=1
            )
            
            with gr.Row():
                refresh_dashboard_btn = gr.Button("🔄 Refresh Dashboard", size="sm")
            
            dashboard_display = gr.Code(
                label="Learning Dashboard",
                language="markdown",
                value="Click 'Refresh Dashboard' to view learning progress",
                lines=20
            )
            
            meta_toggle.change(
                toggle_meta_learning,
                [meta_toggle],
                [meta_toggle_status]
            )
            
            refresh_dashboard_btn.click(
                view_meta_dashboard,
                None,
                dashboard_display
            )

    # Examples section
    with gr.Accordion("💡 Examples & Help", open=False):
        gr.Markdown("### Quick Start Examples:")
        gr.Examples(
            examples=[
                "Create a React app for tracking my todo list",
                "Help me scaffold a Flask API",
                "Show me the contents of beca_gui.py",
                "Remember that I prefer TypeScript over JavaScript",
                "What are my saved preferences?",
            ],
            inputs=msg
        )

        gr.Markdown("""
        ### 🎯 Visual Features
        - **File Tree**: See your project structure in the left panel
        - **Code Viewer**: View files with syntax highlighting (right panel)
        - **Diff Viewer**: Compare before/after changes
        - **Real-time Updates**: File tree refreshes after BECA makes changes

        ### 🧠 Learning Features
        - **Memory**: BECA remembers conversations, preferences, and patterns
        - **Meta-Learning**: Learns from every feature built (toggle on/off above)
        - **Auto-Learning**: Continuously learns from documentation and code
        """)

    # Event handlers for chat
    msg.submit(
        chat_with_beca,
        [msg, chatbot],
        [chatbot, file_tree, status_bar]
    ).then(
        lambda: "", None, msg
    )

    submit.click(
        chat_with_beca,
        [msg, chatbot],
        [chatbot, file_tree, status_bar]
    ).then(
        lambda: "", None, msg
    )

    clear.click(lambda: None, None, chatbot, queue=False)

    # Event handlers for file viewing
    view_btn.click(
        view_file,
        [file_path_input],
        [code_display, status_bar]
    )

    refresh_view_btn.click(
        view_file,
        [file_path_input],
        [code_display, status_bar]
    )

    # Event handler for diff viewing
    diff_btn.click(
        show_diff,
        [diff_file_input],
        [diff_display, status_bar]
    )

    # Event handler for tree refresh
    refresh_tree_btn.click(
        refresh_file_tree,
        None,
        file_tree
    )

if __name__ == "__main__":
    print("Starting Enhanced BECA GUI...")
    print("=" * 60)
    print("🚀 BECA GUI with Visual Enhancements")
    print("=" * 60)
    print("Features:")
    print("  📁 File Tree Panel (left)")
    print("  💬 Chat Panel (center)")
    print("  📝 Code Viewer & Diff Panel (right)")
    print("=" * 60)

    # Start autonomous learning in background
    if AUTONOMOUS_LEARNING_AVAILABLE:
        print("\n🧠 Starting Autonomous Learning System...")
        print("   BECA will continuously learn in the background")
        print("   Learning from: Documentation, Code Patterns, AI Models")
        start_autonomous_learning()
        print("   ✅ Autonomous learning activated!")
    else:
        print("\n⚠️  Autonomous learning not available")
    
    # Initialize meta-learning system
    if META_LEARNING_AVAILABLE:
        print("\n📊 Meta-Learning System Ready")
        print("   BECA will learn from your development work")
        print("   - Logs every interaction during feature development")
        print("   - Extracts patterns and lessons automatically")
        print("   - Applies past learnings to new features")
        print("   - Toggle on/off in GUI if needed")
        print("   ✅ Meta-learning enabled by default!")
    else:
        print("\n⚠️  Meta-learning system not available")

    # Get port from environment variable or default to 7860
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    
    print("\n" + "=" * 60)
    print(f"🌐 Launching BECA GUI on http://{server_name}:{port}")
    print("=" * 60 + "\n")

    demo.launch(server_name=server_name, server_port=port, share=False)
