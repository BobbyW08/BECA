"""
BECA GUI Enhanced - Complete interface with all new features
Includes: Terminal visibility, Stop button, File upload, Google Drive, Dataset loading
"""
import sys
import os
import gradio as gr
import threading
from typing import List, Dict, Tuple
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import core systems
try:
    from langchain_agent import chat_with_agent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import LangChain agent: {e}")
    AGENT_AVAILABLE = False

try:
    from gui_utils import file_tree_manager, code_viewer, diff_viewer
    GUI_UTILS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import GUI utilities: {e}")
    GUI_UTILS_AVAILABLE = False

try:
    from file_tracker import file_tracker
    FILE_TRACKER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import file tracker: {e}")
    FILE_TRACKER_AVAILABLE = False

# Import new systems
try:
    from terminal_manager import terminal_manager
    TERMINAL_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import terminal manager: {e}")
    TERMINAL_AVAILABLE = False

try:
    from file_uploader import file_uploader
    FILE_UPLOAD_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import file uploader: {e}")
    FILE_UPLOAD_AVAILABLE = False

try:
    from google_drive_manager import drive_manager
    DRIVE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Google Drive manager: {e}")
    DRIVE_AVAILABLE = False

try:
    from dataset_loader import dataset_loader
    DATASET_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import dataset loader: {e}")
    DATASET_AVAILABLE = False

try:
    from autonomous_learning import start_autonomous_learning, get_learning_stats
    AUTONOMOUS_LEARNING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import autonomous learning: {e}")
    AUTONOMOUS_LEARNING_AVAILABLE = False

try:
    from meta_learning_system import MetaLearningSystem
    from meta_learning_dashboard import LearningDashboard
    META_LEARNING_AVAILABLE = True
    meta_learning = MetaLearningSystem("beca_memory.db")
    meta_dashboard = LearningDashboard("beca_memory.db")
except ImportError as e:
    print(f"Warning: Could not import meta-learning system: {e}")
    META_LEARNING_AVAILABLE = False
    meta_learning = None
    meta_dashboard = None

# Global state
current_file_content = {}
meta_learning_enabled = True
current_session_id = None
current_feature_tag = None
chat_stop_flag = threading.Event()


def refresh_file_tree() -> str:
    """Refresh and return the file tree HTML"""
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>"
    
    if FILE_TRACKER_AVAILABLE:
        file_tree_manager.new_files = file_tracker.new_files.copy()
        file_tree_manager.modified_files = file_tracker.modified_files.copy()
    
    tree = file_tree_manager.build_tree()
    return file_tree_manager.to_html(tree)


def view_file(filepath: str) -> Tuple[str, str]:
    """View a file with syntax highlighting"""
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>", "Error"
    
    if not filepath or not filepath.strip():
        return "<div>No file selected</div>", ""
    
    try:
        full_path = Path.cwd() / filepath
        if not full_path.exists():
            return f"<div>File not found: {filepath}</div>", "Error: File not found"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            current_file_content[filepath] = f.read()
        
        html, error = code_viewer.read_and_highlight(str(full_path))
        if error:
            return f"<div>Error: {error}</div>", error
        
        return html, f"Viewing: {filepath}"
    except Exception as e:
        return f"<div>Error: {str(e)}</div>", f"Error: {str(e)}"


def show_diff(filepath: str) -> Tuple[str, str]:
    """Show diff for a modified file"""
    if not GUI_UTILS_AVAILABLE:
        return "<div>GUI utilities not available</div>", "Error"
    
    if filepath not in current_file_content:
        return "<div>View the file first</div>", "No diff available"
    
    try:
        full_path = Path.cwd() / filepath
        if not full_path.exists():
            return f"<div>File not found</div>", "Error"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        old_content = current_file_content[filepath]
        diff_html = diff_viewer.generate_diff(old_content, new_content, filepath)
        
        return diff_html, f"Diff for: {filepath}"
    except Exception as e:
        return f"<div>Error: {str(e)}</div>", f"Error: {str(e)}"


def chat_with_beca(message: str, history: List[Dict[str, str]]):
    """Chat with BECA agent"""
    chat_stop_flag.clear()
    
    history.append({"role": "user", "content": message})
    yield history, refresh_file_tree(), "", gr.update(visible=True)
    
    if not AGENT_AVAILABLE:
        history.append({"role": "assistant", "content": "ERROR: Agent not available"})
        yield history, refresh_file_tree(), "Error", gr.update(visible=False)
        return
    
    if not message.strip():
        history.append({"role": "assistant", "content": "Please enter a message."})
        yield history, refresh_file_tree(), "", gr.update(visible=False)
        return
    
    try:
        history.append({"role": "assistant", "content": "🤔 Thinking..."})
        yield history, refresh_file_tree(), "Thinking...", gr.update(visible=True)
        
        if chat_stop_flag.is_set():
            history[-1] = {"role": "assistant", "content": "⛔ Stopped by user"}
            yield history, refresh_file_tree(), "Stopped", gr.update(visible=False)
            return
        
        response = chat_with_agent(message)
        history[-1] = {"role": "assistant", "content": response}
        
        yield history, refresh_file_tree(), "Complete", gr.update(visible=False)
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history[-1] = {"role": "assistant", "content": error_msg}
        yield history, refresh_file_tree(), error_msg, gr.update(visible=False)


def stop_chat():
    """Stop the current chat operation"""
    chat_stop_flag.set()
    if TERMINAL_AVAILABLE:
        terminal_manager.stop_current_command()
    return "Stopping..."


def get_terminal_output() -> str:
    """Get terminal output"""
    if TERMINAL_AVAILABLE:
        return terminal_manager.format_history(20)
    return "Terminal manager not available"


def handle_file_upload(file) -> str:
    """Handle file upload"""
    if not FILE_UPLOAD_AVAILABLE:
        return "File upload not available"
    
    if file is None:
        return "No file selected"
    
    try:
        result = file_uploader.process_upload(file, file.name)
        
        if result['success']:
            msg = f"✅ {result['message']}\n\n"
            if result.get('content'):
                msg += f"Content preview:\n{result['content'][:500]}..."
            if result.get('metadata'):
                msg += f"\n\nMetadata: {result['metadata']}"
            if result.get('error'):
                msg += f"\n\n⚠️ {result['error']}"
            return msg
        else:
            return f"❌ Upload failed: {result['message']}"
    
    except Exception as e:
        return f"Error: {str(e)}"


def authenticate_google_drive() -> str:
    """Authenticate with Google Drive"""
    if not DRIVE_AVAILABLE:
        return "Google Drive integration not available"
    
    success, message = drive_manager.authenticate()
    return f"{'✅' if success else '❌'} {message}"


def list_drive_files() -> str:
    """List Google Drive files"""
    if not DRIVE_AVAILABLE:
        return "Google Drive integration not available"
    
    result = drive_manager.list_files(max_results=20)
    
    if result['success']:
        files = result['files']
        if not files:
            return "No files found"
        
        output = "📁 Google Drive Files:\n\n"
        for f in files:
            output += f"• {f['name']} ({f.get('mimeType', 'unknown')})\n"
        return output
    else:
        return f"Error: {result['error']}"


def load_datasets() -> str:
    """Load built-in datasets"""
    if not DATASET_AVAILABLE:
        return "Dataset loader not available"
    
    try:
        results = dataset_loader.load_all_builtin_datasets()
        
        output = "✅ Datasets Loaded:\n\n"
        for name, count in results.items():
            output += f"• {name}: {count} patterns\n"
        
        return output
    except Exception as e:
        return f"Error: {str(e)}"


def get_learning_status() -> str:
    """Get learning status"""
    if AUTONOMOUS_LEARNING_AVAILABLE:
        try:
            stats = get_learning_stats()
            if stats['active']:
                return f"🧠 Active | Learned: {stats['total_learned']}"
            return "🧠 Starting..."
        except:
            return "🧠 Initializing..."
    return "Not Available"


def get_meta_learning_status() -> str:
    """Get meta-learning status"""
    if META_LEARNING_AVAILABLE and meta_learning_enabled:
        try:
            data = meta_dashboard.ml_system.get_learning_dashboard_data()
            return f"📊 ON | Features: {data['features_built']} | Lessons: {data['lessons_learned']}"
        except:
            return "📊 Active"
    return "📊 OFF"


def toggle_meta_learning(enabled: bool) -> str:
    """Toggle meta-learning"""
    global meta_learning_enabled
    meta_learning_enabled = enabled
    return f"📊 {'Enabled' if enabled else 'Disabled'}"


def view_meta_dashboard() -> str:
    """View meta-learning dashboard"""
    if not META_LEARNING_AVAILABLE:
        return "Meta-learning not available"
    try:
        return meta_dashboard.generate_dashboard_report()
    except Exception as e:
        return f"Error: {str(e)}"


# Create Enhanced Gradio Interface
with gr.Blocks(title="BECA Enhanced - Complete AI Coding Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 BECA Enhanced - Complete AI Coding Assistant")
    gr.Markdown("Terminal visibility • Stop button • File upload • Google Drive • Enhanced learning")
    
    # Status bars
    with gr.Row():
        if AUTONOMOUS_LEARNING_AVAILABLE:
            learning_status = gr.Textbox(
                label="Auto-Learning",
                value=get_learning_status(),
                interactive=False,
                max_lines=1,
                scale=1
            )
        if META_LEARNING_AVAILABLE:
            meta_status = gr.Textbox(
                label="Meta-Learning",
                value=get_meta_learning_status(),
                interactive=False,
                max_lines=1,
                scale=1
            )
        
        status_bar = gr.Textbox(
            label="Status",
            value="Ready",
            interactive=False,
            max_lines=1,
            scale=1
        )
    
    # Main layout with 4 panels
    with gr.Row():
        # Left: File Tree
        with gr.Column(scale=1):
            gr.Markdown("### 📁 Files")
            file_tree = gr.HTML(
                value=refresh_file_tree() if GUI_UTILS_AVAILABLE else "<div>Loading...</div>"
            )
            gr.Button("🔄 Refresh", size="sm").click(
                refresh_file_tree, None, file_tree
            )
        
        # Center-Left: Chat
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            chatbot = gr.Chatbot(
                height=400,
                show_copy_button=True,
                type="messages"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask BECA anything...",
                    scale=8,
                    lines=2,
                    show_label=False
                )
                submit_btn = gr.Button("Send", variant="primary", scale=1)
                stop_btn = gr.Button("⏹️ Stop", variant="stop", scale=1, visible=False)
            
            with gr.Row():
                gr.Button("Clear", size="sm").click(lambda: None, None, chatbot)
                
                if FILE_UPLOAD_AVAILABLE:
                    upload_file = gr.File(
                        label="Upload File",
                        file_types=[".txt", ".py", ".js", ".pdf", ".docx", ".csv", ".json"],
                        scale=2
                    )
        
        # Center-Right: Code Viewer
        with gr.Column(scale=2):
            gr.Markdown("### 📝 Code")
            
            with gr.Tabs():
                with gr.Tab("View"):
                    file_path_input = gr.Textbox(
                        placeholder="e.g., src/main.py",
                        show_label=False
                    )
                    gr.Button("View", size="sm").click(
                        view_file,
                        [file_path_input],
                        [gr.HTML(), status_bar]
                    )
                    code_display = gr.HTML()
                
                with gr.Tab("Diff"):
                    diff_file_input = gr.Textbox(
                        placeholder="File path",
                        show_label=False
                    )
                    gr.Button("Show Diff", size="sm").click(
                        show_diff,
                        [diff_file_input],
                        [gr.HTML(), status_bar]
                    )
                    diff_display = gr.HTML()
        
        # Right: Terminal
        if TERMINAL_AVAILABLE:
            with gr.Column(scale=1):
                gr.Markdown("### 🖥️ Terminal")
                terminal_output = gr.Code(
                    label="Command History",
                    language="bash",
                    lines=20,
                    value=get_terminal_output()
                )
                gr.Button("🔄 Refresh", size="sm").click(
                    get_terminal_output, None, terminal_output
                )
    
    # Advanced Features
    with gr.Accordion("🚀 Advanced Features", open=False):
        with gr.Tabs():
            # Google Drive Tab
            if DRIVE_AVAILABLE:
                with gr.Tab("☁️ Google Drive"):
                    gr.Markdown("### Google Drive Integration")
                    with gr.Row():
                        gr.Button("🔐 Authenticate").click(
                            authenticate_google_drive, None, gr.Textbox(label="Status")
                        )
                        gr.Button("📂 List Files").click(
                            list_drive_files, None, gr.Textbox(label="Files", lines=10)
                        )
            
            # Dataset Loading Tab
            if DATASET_AVAILABLE:
                with gr.Tab("📚 Datasets"):
                    gr.Markdown("### Load Coding Datasets")
                    gr.Markdown("Expand BECA's knowledge with built-in code patterns")
                    gr.Button("📥 Load All Datasets", variant="primary").click(
                        load_datasets, None, gr.Textbox(label="Results", lines=10)
                    )
            
            # Meta-Learning Tab
            if META_LEARNING_AVAILABLE:
                with gr.Tab("📊 Meta-Learning"):
                    gr.Markdown("### Meta-Learning Dashboard")
                    meta_toggle = gr.Checkbox(
                        label="Enable Meta-Learning",
                        value=True
                    )
                    meta_toggle.change(
                        toggle_meta_learning,
                        [meta_toggle],
                        gr.Textbox(label="Status")
                    )
                    gr.Button("🔄 Refresh Dashboard").click(
                        view_meta_dashboard,
                        None,
                        gr.Code(label="Dashboard", language="markdown", lines=15)
                    )
    
    # Examples
    with gr.Accordion("💡 Examples", open=False):
        gr.Examples(
            examples=[
                "Create a React todo app",
                "Write a Python function to sort a list",
                "Help me debug this error",
                "Upload this CSV and analyze it",
            ],
            inputs=msg
        )
        
        gr.Markdown("""
        ### ✨ New Features
        - **Terminal Output**: See command execution in real-time
        - **Stop Button**: Cancel long-running operations
        - **File Upload**: Upload PDFs, Word docs, CSVs, images, and more
        - **Google Drive**: Connect and sync with Google Drive
        - **Enhanced Datasets**: Pre-loaded with common algorithms and patterns
        """)
    
    # Event handlers
    chat_handler = msg.submit(
        chat_with_beca,
        [msg, chatbot],
        [chatbot, file_tree, status_bar, stop_btn]
    ).then(lambda: "", None, msg)
    
    submit_handler = submit_btn.click(
        chat_with_beca,
        [msg, chatbot],
        [chatbot, file_tree, status_bar, stop_btn]
    ).then(lambda: "", None, msg)
    
    stop_btn.click(
        stop_chat,
        None,
        status_bar
    )
    
    if FILE_UPLOAD_AVAILABLE:
        upload_file.upload(
            handle_file_upload,
            upload_file,
            gr.Textbox(label="Upload Result", lines=10)
        )


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 BECA Enhanced - Complete AI Coding Assistant")
    print("=" * 70)
    print("\nFeatures:")
    print("  ✅ Terminal command visibility")
    print("  ✅ Stop button for operations")
    print("  ✅ File upload support (PDF, Word, CSV, images, etc.)")
    print("  ✅ Google Drive integration")
    print("  ✅ Enhanced knowledge base with datasets")
    print("  ✅ Improved prompts for better understanding")
    print("=" * 70)
    
    # Start background systems
    if AUTONOMOUS_LEARNING_AVAILABLE:
        print("\n🧠 Starting Autonomous Learning...")
        start_autonomous_learning()
        print("   ✅ Active!")
    
    if META_LEARNING_AVAILABLE:
        print("\n📊 Meta-Learning System Ready")
        print("   ✅ Enabled!")
    
    if DATASET_AVAILABLE:
        print("\n📚 Loading built-in datasets...")
        results = dataset_loader.load_all_builtin_datasets()
        for name, count in results.items():
            print(f"   • {name}: {count} patterns")
    
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    
    print(f"\n🌐 Launching on http://{server_name}:{port}")
    print("=" * 70 + "\n")
    
    demo.launch(server_name=server_name, server_port=port, share=False)
