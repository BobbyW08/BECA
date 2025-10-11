#!/usr/bin/env python3
"""
Initialize BECA's self-knowledge - information about her own codebase
Run this once to populate the knowledge base with BECA's architecture
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from knowledge_system import knowledge_base

def initialize_self_knowledge():
    """Add BECA's self-knowledge to the knowledge base"""

    print("Initializing BECA's self-knowledge...")

    # Architecture overview
    knowledge_base.add_documentation(
        source="BECA-Architecture",
        url="local://beca-architecture",
        title="BECA System Architecture",
        content="""
        BECA (Badass Expert Coding Agent) Architecture:

        Core Components:
        1. beca_gui.py - Gradio web interface for user interaction
        2. langchain_agent.py - LangChain agent with LLM integration
        3. langchain_tools.py - Tool implementations for the agent
        4. knowledge_system.py - Knowledge base and documentation scraping
        5. memory_db.py - Conversation memory and user preferences
        6. autonomous_learning.py - Background learning system

        Storage:
        - beca_knowledge.db - Documentation, code patterns, learning resources
        - beca_memory.db - Conversation history, preferences, tool usage stats

        AI Models:
        - llama3.1:8b - General reasoning and tool use
        - qwen2.5-coder:7b-instruct - Code generation and debugging

        Location: C:\\dev (main), C:\\dev\\src (source code)
        """,
        category="beca-core",
        tags=["architecture", "self-knowledge", "system-design"]
    )

    # Tools and capabilities
    knowledge_base.add_documentation(
        source="BECA-Capabilities",
        url="local://beca-capabilities",
        title="BECA's Tools and Capabilities",
        content="""
        BECA's Tool Categories:

        File Operations:
        - read_file, write_file, list_files
        - find_in_files, analyze_code

        Git Operations:
        - git_status, git_diff, git_add, git_commit, git_push

        Code Quality:
        - find_bugs, suggest_improvements
        - run_tests, generate_tests, coverage_report

        Project Creation:
        - create_react_app, create_project_from_template
        - Supports: react-vite, flask-api, fastapi, python-cli

        Web & Research:
        - web_search, fetch_url

        Execution:
        - run_python, run_command

        Self-Improvement:
        - learn_from_documentation, save_code_pattern
        - search_knowledge, add_learning_resource
        - analyze_repository, clone_and_learn

        Memory:
        - save_user_preference, get_user_preferences
        - search_conversation_history
        """,
        category="beca-core",
        tags=["tools", "capabilities", "features"]
    )

    # File structure
    knowledge_base.add_documentation(
        source="BECA-Files",
        url="local://beca-files",
        title="BECA File Structure",
        content="""
        BECA Directory Structure:

        C:\\dev\\
        ├── beca_gui.py                    # Main GUI application
        ├── start_beca_vm.py              # GCP VM management
        ├── initialize_knowledge_system.py # Knowledge setup
        ├── beca_knowledge.db             # Knowledge storage
        ├── beca_memory.db                # Memory storage
        └── src/
            ├── langchain_agent.py        # Agent logic
            ├── langchain_tools.py        # Tool implementations
            ├── knowledge_system.py       # Knowledge base
            ├── knowledge_tools.py        # Learning tools
            ├── memory_db.py              # Memory system
            ├── memory_tools.py           # Memory tools
            ├── autonomous_learning.py    # Background learning
            ├── codebase_explorer.py      # Code analysis
            ├── ai_model_tools.py         # AI/ML tools
            ├── code_generator.py         # Code generation
            ├── code_generation_tools.py  # Generation tools
            ├── file_tracker.py           # File change tracking
            └── gui_utils.py              # GUI utilities
        """,
        category="beca-core",
        tags=["file-structure", "organization", "codebase"]
    )

    print("✅ Self-knowledge initialized successfully!")
    print("\nBECA now knows:")
    print("  - Her own architecture and components")
    print("  - All available tools and capabilities")
    print("  - File structure and organization")

if __name__ == "__main__":
    initialize_self_knowledge()
