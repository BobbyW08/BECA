# BECA - Badass Expert Coding Agent 🤖

BECA is an AI coding assistant powered by LangChain and Ollama, running on cloud GPU for fast responses.

## Quick Start

See [START-BECA.md](START-BECA.md) for complete startup instructions.

**TL;DR:**
```bash
# 1. Start cloud GPU
gcloud compute instances start beca-ollama --zone=us-central1-c --project=beca-0001

# 2. Launch BECA
cd C:\dev && .\.venv\Scripts\Activate.ps1 && python beca_gui.py
```

## Features

*   **27 Development Tools:** File operations, git integration, testing, code analysis, web search
*   **Persistent Memory:** Remembers your preferences and past conversations
*   **Project Templates:** Scaffold React, Flask, FastAPI, and Python CLI projects
*   **Cloud GPU Power:** Uses Google Cloud T4 GPU for fast inference
*   **Local-First:** No API keys needed, runs on your infrastructure

## Architecture

- **Frontend:** Gradio web interface ([beca_gui.py](beca_gui.py))
- **Agent:** LangChain ReAct agent ([src/langchain_agent.py](src/langchain_agent.py))
- **LLM:** Llama 3.1 8B via Ollama (cloud GPU)
- **Tools:** 27 tools for development tasks ([src/langchain_tools.py](src/langchain_tools.py), [src/memory_tools.py](src/memory_tools.py))
- **Memory:** SQLite database for conversations and preferences ([src/memory_db.py](src/memory_db.py))

## Files

- `START-BECA.md` - Complete startup guide
- `create_vm.py` - Create cloud GPU VM
- `setup_firewall.py` - Configure firewall
- `beca_gui.py` - Launch the web interface
- `src/` - Source code (agent, tools, memory)

## Cost Management

Cloud GPU costs ~$0.30/hour. Always stop the VM when not in use:
```bash
gcloud compute instances stop beca-ollama --zone=us-central1-c --project=beca-0001
```
