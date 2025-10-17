# BECA - Badass Expert Coding Agent 🤖

BECA is a self-improving AI coding assistant powered by LangChain and Ollama, running on cloud GPU with autonomous learning capabilities.

## Quick Start

See **[START-BECA.md](START-BECA.md)** for complete Docker/cloud setup instructions.

**TL;DR:**
```batch
# 1. Double-click start-beca.bat (or start VM from Google Cloud Console)
start-beca.bat

# 2. Wait 60 seconds for containers to start

# 3. Open browser
http://34.55.204.139:3000
```

**✨ Docker Setup:** BECA runs in cloud containers - no local Python setup needed!

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [AI Models](#ai-models)
- [Tools & Capabilities](#tools--capabilities)
- [Memory & Learning System](#memory--learning-system)
- [Knowledge Enhancement](#knowledge-enhancement)
- [File Structure](#file-structure)
- [Data Models](#data-models)
- [Setup & Configuration](#setup--configuration)
- [Cost Management](#cost-management)

---

## Overview

BECA is an autonomous AI coding agent that:
- **Builds projects** from scratch using templates (React, Flask, FastAPI, Python CLI)
- **Remembers preferences** and past conversations
- **Learns continuously** from documentation, code patterns, and AI models
- **Analyzes codebases** to extract useful patterns
- **Self-improves** by indexing knowledge and applying learned patterns

### Key Features

- **39+ Development Tools** - File ops, git, testing, code analysis, web search, AI model tools
- **Persistent Memory** - SQLite-backed storage for conversations, preferences, and patterns
- **Autonomous Learning** - Background learning system that continuously improves knowledge
- **Multi-Model Architecture** - Dual LLMs for optimal performance (general + coding specialist)
- **Cloud GPU Power** - Google Cloud T4 GPU for fast inference (SPOT pricing ~$0.17/hr)
- **Local-First** - No API keys needed, runs on your infrastructure
- **Visual Interface** - Modern React frontend with Plan/Act modes, file tree, code viewer, and diff visualization

---

## Architecture

**Note:** The architecture diagrams below document the historical Gradio-based implementation. BECA now uses a modern **React frontend** (port 3000) and **FastAPI backend** (port 8000) in a Docker multi-container setup. See [START-BECA.md](START-BECA.md) for current architecture details.

BECA uses a modular, layered architecture designed for extensibility and autonomous improvement.

### System Architecture Diagram (Historical - Gradio)

```
┌─────────────────────────────────────────────────────────────┐
│                    BECA GUI (Gradio)                        │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐   │
│  │File Tree │  │   Chat   │  │ Code Viewer / Diff     │   │
│  └──────────┘  └──────────┘  └────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LangChain Agent (ReAct Pattern)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Agent Core: create_tool_calling_agent               │  │
│  │  • Reasoning loop                                     │  │
│  │  • Tool selection & execution                         │  │
│  │  • Response generation                                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│  Llama 3.1 8B    │          │ Qwen2.5-Coder 7B │
│  (General)       │          │  (Code Focused)  │
│                  │          │                  │
│ • Conversation   │          │ • Code gen       │
│ • Tool use       │          │ • Debugging      │
│ • Planning       │          │ • Code review    │
└──────────────────┘          └──────────────────┘
          ▲                             ▲
          └─────────────┬───────────────┘
                        │
              Ollama Server (Cloud GPU)
              34.46.140.140:11434
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│  T4 GPU (16GB)   │        │  SPOT Instance   │
│  us-central1-b   │        │  ~$0.17/hour     │
└──────────────────┘        └──────────────────┘
```

### Tool Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BECA_TOOLS (39 tools)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  Core Tools    │  │  Memory Tools  │  │ Knowledge    │ │
│  │  (20 tools)    │  │  (6 tools)     │  │ Tools (8)    │ │
│  ├────────────────┤  ├────────────────┤  ├──────────────┤ │
│  │• File ops      │  │• Preferences   │  │• Learn docs  │ │
│  │• Git commands  │  │• Conversations │  │• Save code   │ │
│  │• Web search    │  │• Patterns      │  │• AI models   │ │
│  │• Code exec     │  │• Tool stats    │  │• Queue       │ │
│  │• Testing       │  │• Recall        │  │• Search KB   │ │
│  │• Templates     │  │• Solutions     │  │• Scrape      │ │
│  └────────────────┘  └────────────────┘  └──────────────┘ │
│                                                             │
│  ┌────────────────┐  ┌────────────────────────────────┐   │
│  │ Codebase Tools │  │   AI Model Tools (5 tools)     │   │
│  │  (4 tools)     │  ├────────────────────────────────┤   │
│  ├────────────────┤  │• Explore Ollama models         │   │
│  │• Analyze repo  │  │• Model info                    │   │
│  │• Code patterns │  │• Create Modelfile              │   │
│  │• Clone & learn │  │• Fine-tune guidance            │   │
│  │• Extract funcs │  │• Setup training env            │   │
│  └────────────────┘  └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Memory & Learning Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Memory System                           │
│                (beca_memory.db - SQLite)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │Conversations │  │ Preferences  │  │ Tool Usage       │ │
│  │              │  │              │  │                  │ │
│  │• User msgs   │  │• Category    │  │• Tool name       │ │
│  │• Responses   │  │• Key/value   │  │• Success/fail    │ │
│  │• Tools used  │  │• Confidence  │  │• Last used       │ │
│  │• Timestamps  │  │• Updated     │  │• Success rate    │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Successful Patterns                         │  │
│  │                                                      │  │
│  │• Task type (e.g., 'react_app', 'flask_api')        │  │
│  │• User request                                       │  │
│  │• Solution steps                                     │  │
│  │• Tools used                                         │  │
│  │• Reuse count                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Knowledge System                          │
│              (beca_knowledge.db - SQLite)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │Documentation │  │Code Patterns │  │ AI Models        │ │
│  │              │  │              │  │                  │ │
│  │• Source      │  │• Language    │  │• Model name      │ │
│  │• URL         │  │• Pattern     │  │• Framework       │ │
│  │• Content     │  │• Code        │  │• Training info   │ │
│  │• Category    │  │• Use case    │  │• Fine-tuning     │ │
│  │• Tags        │  │• Success %   │  │• Examples        │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │Tool Knowledge│  │Learning Queue│  │ Codebase Insights│ │
│  │              │  │              │  │                  │ │
│  │• Tool name   │  │• Priority    │  │• Repo analysis   │ │
│  │• Category    │  │• Topics      │  │• Architecture    │ │
│  │• Usage       │  │• Status      │  │• Patterns        │ │
│  │• Examples    │  │• Difficulty  │  │• Lessons         │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## AI Models

BECA uses a **dual-model architecture** for optimal performance:

### Model Selection Strategy

```python
# Intelligent model routing based on task type
if task_contains(['write code', 'debug', 'refactor', 'code review']):
    use_model = "qwen2.5-coder:7b-instruct"
else:
    use_model = "llama3.1:8b"
```

### Model Configurations

#### 1. **Llama 3.1 8B** (General Tasks)
- **Base URL**: `http://34.46.140.140:11434`
- **Purpose**: Conversation, reasoning, tool use, planning
- **Parameters**:
  ```python
  temperature=0.3        # Balanced creativity
  num_predict=256        # Shorter responses for speed
  num_ctx=2048          # Context window
  top_k=20              # Speed optimization
  top_p=0.9             # Nucleus sampling
  ```

#### 2. **Qwen2.5-Coder 7B** (Code Specialist)
- **Base URL**: `http://34.46.140.140:11434`
- **Purpose**: Code generation, debugging, code review
- **Parameters**:
  ```python
  temperature=0.2        # More deterministic for code
  num_predict=512        # Longer responses for code
  num_ctx=4096          # Larger context for code
  top_k=20
  top_p=0.9
  ```

### Agent Configuration

- **Framework**: LangChain with ReAct pattern
- **Agent Type**: `create_tool_calling_agent` (optimized for Llama 3.1)
- **Max Iterations**: 5
- **Max Execution Time**: 30 seconds
- **Early Stopping**: Generate response on max iterations
- **Error Handling**: Custom parsing error handler

---

## Tools & Capabilities

### Core Development Tools (20 tools)

#### File Operations
- `read_file(file_path)` - Read file contents
- `write_file(file_path, content)` - Write/update files
- `list_files(directory_path)` - List directory contents
- `find_in_files(search_term, directory, pattern)` - Search across files

#### Git Integration
- `git_status()` - Show repository status
- `git_diff(file_path)` - Show changes
- `git_add(file_path)` - Stage files
- `git_commit(message)` - Commit changes
- `git_push()` - Push to remote

#### Code Analysis
- `analyze_code(file_path)` - Metrics & analysis
- `find_bugs(file_path)` - Bug detection
- `suggest_improvements(file_path)` - Refactoring suggestions

#### Testing
- `run_tests(path)` - Auto-detect & run tests
- `generate_tests(file_path)` - Create test templates
- `coverage_report(path)` - Test coverage analysis

#### Web & Research
- `web_search(query, max_results)` - DuckDuckGo search
- `fetch_url(url)` - Fetch web content

#### Execution
- `run_python(code)` - Execute Python code
- `run_command(command)` - Run shell commands

#### Project Templates
- `create_react_app(app_name)` - React scaffold
- `create_project_from_template(type, name)` - Multi-framework templates
  - `react-vite` - React + Vite
  - `flask-api` - Flask REST API
  - `fastapi` - FastAPI backend
  - `python-cli` - Python CLI tool

### Memory Tools (6 tools)

- `remember_preference(category, key, value)` - Save user preferences
- `recall_preferences()` - Get all preferences
- `search_past_conversations(term)` - Search history
- `find_similar_solution(task_type)` - Find past patterns
- `view_tool_statistics()` - Tool usage stats
- `save_successful_approach(type, desc, tools)` - Save patterns

### Knowledge Enhancement Tools (8 tools)

- `learn_from_documentation(url, category, tags)` - Scrape & index docs
- `save_code_pattern(name, language, code, desc)` - Save code patterns
- `search_knowledge(query, category)` - Search knowledge base
- `add_learning_resource(type, title, url, topics)` - Queue learning
- `get_learning_queue(limit)` - View study queue
- `learn_ai_model_knowledge(...)` - Save AI/ML knowledge
- `learn_tool_knowledge(...)` - Save tool documentation
- `auto_learn_from_urls(urls, category)` - Batch learning

### Codebase Analysis Tools (4 tools)

- `analyze_repository(repo_path)` - Analyze repo structure
- `analyze_code_patterns(file_path, language)` - Extract patterns
- `clone_and_learn(repo_url, clone_path)` - Clone & analyze GitHub repos
- `extract_function_signatures(file_path)` - Extract API interfaces

### AI Model Tools (5 tools)

- `explore_ollama_models()` - List available models
- `show_model_info(model_name)` - Model details
- `create_modelfile(name, base, prompt, ...)` - Custom model creation
- `fine_tune_guidance(task_type, framework)` - Fine-tuning instructions
- `setup_training_environment(project_name, framework)` - ML project scaffold

---

## Memory & Learning System

### Memory Database Schema

**File**: `beca_memory.db`

#### 1. Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    tools_used TEXT,              -- JSON array
    success BOOLEAN DEFAULT TRUE
)
```

#### 2. User Preferences Table
```sql
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,        -- e.g., 'framework', 'testing'
    preference_key TEXT NOT NULL,  -- e.g., 'frontend_framework'
    preference_value TEXT NOT NULL,-- e.g., 'React'
    confidence REAL DEFAULT 1.0,
    last_updated TEXT NOT NULL,
    UNIQUE(category, preference_key)
)
```

#### 3. Successful Patterns Table
```sql
CREATE TABLE successful_patterns (
    id INTEGER PRIMARY KEY,
    task_type TEXT NOT NULL,       -- e.g., 'react_app'
    user_request TEXT NOT NULL,
    solution TEXT NOT NULL,         -- What worked
    tools_used TEXT NOT NULL,       -- JSON array
    timestamp TEXT NOT NULL,
    reuse_count INTEGER DEFAULT 0
)
```

#### 4. Tool Usage Table
```sql
CREATE TABLE tool_usage (
    id INTEGER PRIMARY KEY,
    tool_name TEXT NOT NULL,
    usage_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_used TEXT NOT NULL,
    UNIQUE(tool_name)
)
```

### How Memory Works

1. **Conversation Storage**: Every interaction saved with metadata
2. **Preference Injection**: User preferences automatically added to context
3. **Pattern Matching**: Similar tasks retrieve past successful solutions
4. **Tool Analytics**: Success rates inform tool selection

---

## Knowledge Enhancement

### Knowledge Database Schema

**File**: `beca_knowledge.db`

#### 1. Documentation Table
- Scraped documentation from URLs
- Full-text search enabled
- Usefulness scoring
- Access tracking

#### 2. Code Patterns Table
- Reusable code snippets
- Language-specific patterns
- Success rate tracking
- Usage statistics

#### 3. AI Model Knowledge Table
- Model specifications
- Training approaches
- Fine-tuning methods
- Code examples

#### 4. Learning Resources Queue
- Prioritized study queue
- Topics & difficulty levels
- Completion tracking

#### 5. Tool Knowledge Table
- Tool documentation
- Installation instructions
- Usage examples
- Tips & tricks

#### 6. Codebase Insights Table
- Repository analysis
- Architecture patterns
- Lessons learned

### Autonomous Learning System

**File**: `src/autonomous_learning.py`

- **Background Processing**: Runs continuously in separate thread
- **Resource Queue**: Processes high-priority learning resources
- **Web Scraping**: Fetches and indexes documentation
- **Pattern Extraction**: Learns from code repositories
- **Self-Improvement**: Updates knowledge base automatically

---

## File Structure

```
C:\dev\
├── beca_gui.py                 # Main Gradio GUI application
├── requirements.txt            # Python dependencies
├── START-BECA.md              # Startup instructions
├── readme.md                  # This file
│
├── src/                       # Source code
│   ├── langchain_agent.py     # LangChain ReAct agent
│   ├── langchain_tools.py     # Core development tools (20)
│   ├── memory_db.py          # SQLite memory system
│   ├── memory_tools.py       # Memory management tools (6)
│   ├── knowledge_system.py   # Knowledge base & web scraper
│   ├── knowledge_tools.py    # Learning tools (8)
│   ├── codebase_explorer.py  # Codebase analysis tools (4)
│   ├── ai_model_tools.py     # AI model tools (5)
│   ├── autonomous_learning.py # Background learning system
│   ├── gui_utils.py          # File tree, code viewer, diff viewer
│   ├── file_tracker.py       # Track file changes for GUI
│   └── code_generator.py     # Code generation utilities
│
├── create_vm.py              # GCP VM creation script
├── setup_firewall.py         # Firewall configuration
├── start_beca_vm.py          # VM startup automation
│
└── Data Files (auto-generated)
    ├── beca_memory.db        # Memory database
    ├── beca_knowledge.db     # Knowledge database
    └── C:/beca-learning/     # Learning resources storage
```

---

## Data Models

### BECAMemory Class (`src/memory_db.py`)

```python
class BECAMemory:
    def __init__(db_path: str = "beca_memory.db")

    # Conversation management
    def save_conversation(user_message, agent_response, tools_used, success)
    def get_recent_conversations(limit=10)
    def search_conversations(search_term, limit=10)

    # Preferences
    def save_preference(category, key, value, confidence=1.0)
    def get_preference(category, key)
    def get_all_preferences()

    # Patterns
    def save_successful_pattern(task_type, user_request, solution, tools_used)
    def find_similar_patterns(task_type, limit=3)
    def increment_pattern_reuse(pattern_id)

    # Tool tracking
    def track_tool_usage(tool_name, success=True)
    def get_tool_stats()
```

### KnowledgeBase Class (`src/knowledge_system.py`)

```python
class KnowledgeBase:
    def __init__(db_path: str = "beca_knowledge.db")

    # Documentation
    def add_documentation(source, url, title, content, category, tags)

    # Code patterns
    def add_code_pattern(pattern_name, language, code_snippet, description, use_case, tags)
    def update_pattern_usage(pattern_id, success)

    # Learning resources
    def add_learning_resource(resource_type, title, url, topics, difficulty, priority)
    def get_learning_queue(limit=10, status='pending')
    def mark_resource_learned(resource_id)

    # AI/ML knowledge
    def add_ai_model_knowledge(model_name, model_type, framework, description, ...)

    # Tool knowledge
    def add_tool_knowledge(tool_name, category, description, installation, ...)

    # Search
    def search_knowledge(query, category=None, limit=10)
```

### WebDocScraper Class (`src/knowledge_system.py`)

```python
class WebDocScraper:
    @staticmethod
    def fetch_and_parse(url: str) -> Dict[str, str]

    @staticmethod
    def scrape_documentation_site(base_url, kb, category, max_pages=20)
```

---

## Setup & Configuration

### Prerequisites

- Python 3.8+
- Google Cloud SDK
- Git
- Virtual environment

### Installation

```bash
# 1. Clone repository
cd C:\dev

# 2. Create virtual environment
python -m venv .venv

# 3. Activate environment
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Unix/Mac

# 4. Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
# Core
requests
pydantic
jinja2

# LangChain
langchain
langchain-community
langchain-ollama

# GUI
gradio
pygments          # Syntax highlighting
watchdog          # File watching
```

### Cloud GPU Setup

1. **Create VM**:
   ```bash
   python create_vm.py
   ```

2. **Configure Firewall**:
   ```bash
   python setup_firewall.py
   ```

3. **Start VM**:
   ```bash
   gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001
   ```

### Environment Variables

BECA doesn't require API keys, but uses:
- `OLLAMA_URL = "http://34.46.140.140:11434"` (hardcoded in `src/langchain_agent.py`)

---

## Cost Management

### Current Configuration

- **Instance Type**: n1-standard-4 (SPOT)
- **GPU**: NVIDIA T4 (16GB)
- **Zone**: us-central1-b
- **Disk**: 50GB SSD

### Cost Breakdown

| Resource | Standard Price | SPOT Price | Savings |
|----------|---------------|------------|---------|
| Compute  | ~$0.30/hr     | ~$0.10/hr  | 67%     |
| GPU      | ~$0.35/hr     | ~$0.07/hr  | 80%     |
| **Total**| **~$0.65/hr** | **~$0.17/hr** | **~74%** |
| Monthly  | ~$470/mo      | ~$125/mo   | ~$345   |

**Disk Storage**: ~$0.07/day (persists when stopped)

### Cost-Saving Tips

1. **Always stop when not in use**:
   ```bash
   gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001
   ```

2. **Set up budget alerts** in Google Cloud Console

3. **Monitor usage**:
   ```bash
   gcloud compute instances list --project=beca-0001 --format="table(name,zone,status,creationTimestamp)"
   ```

4. **Daily workflow** (saves ~$3/day):
   - Morning: Start VM
   - Evening: Stop VM

---

## Developer Guide

### Adding New Tools

1. **Create tool in appropriate file**:
   ```python
   # In src/langchain_tools.py or new file
   from langchain_core.tools import tool

   @tool
   def my_new_tool(param: str) -> str:
       """Tool description for the agent"""
       # Implementation
       return result
   ```

2. **Export tool**:
   ```python
   # Add to BECA_TOOLS list
   BECA_TOOLS = [
       # ... existing tools
       my_new_tool,
   ]
   ```

### Extending Memory

Add new tables to `src/memory_db.py`:
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY,
        ...
    )
""")
```

### Customizing Models

Edit `src/langchain_agent.py`:
```python
# Add new model
new_model = ChatOllama(
    model="model-name",
    base_url=OLLAMA_URL,
    temperature=0.5,
    ...
)
```

### GUI Customization

Modify `beca_gui.py` for UI changes:
- File tree: `gui_utils.py` → `FileTreeManager`
- Code viewer: `gui_utils.py` → `CodeViewer`
- Diff viewer: `gui_utils.py` → `DiffViewer`

---

## Troubleshooting

### Common Issues

**1. Connection refused**
- VM is stopped → Start it
- Ollama not running → SSH and restart: `sudo systemctl restart ollama`

**2. ModuleNotFoundError**
- Wrong environment → Activate: `.\.venv\Scripts\Activate.ps1`
- Missing deps → Install: `pip install -r requirements.txt`

**3. Slow responses**
- High network latency → Check ping to `34.46.140.140`
- GPU not used → SSH and check: `nvidia-smi`

**4. Firewall blocking**
- IP changed → Run: `python setup_firewall.py`

---

## Architecture Benefits

### Why This Design?

1. **Dual Models**: Task-specific optimization (conversation vs code)
2. **SQLite Storage**: Fast, local, no external dependencies
3. **Autonomous Learning**: Continuous improvement without manual intervention
4. **Tool Modularity**: Easy to add/remove capabilities
5. **Cloud GPU**: Cost-effective power (SPOT instances)
6. **Memory System**: Context-aware responses using past learnings

### Scalability

- **Tools**: Add infinitely via decorator pattern
- **Models**: Swap/add models in agent config
- **Storage**: SQLite handles millions of records efficiently
- **Learning**: Background threads don't block main flow

---

## References

- **LangChain Docs**: https://python.langchain.com/
- **Ollama**: https://ollama.ai/
- **Gradio**: https://gradio.app/
- **Google Cloud**: https://cloud.google.com/

---

## License

MIT

---

## Contributing

This is a personal project, but feel free to fork and extend!

---

**Built with ❤️ by BECA's human companion**
