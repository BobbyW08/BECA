# BECA Development Plan
**Badass Expert Coding Agent**

## Vision
Build an autonomous AI coding assistant that helps developers create applications, fix bugs, and write code using local LLMs (no API costs).

---

## ✅ Phase 1: Foundation Cleanup - COMPLETE

### Accomplishments
- Removed 1.4M+ lines of unused Node.js/TypeScript code (~150MB)
- Deleted duplicate files (src/tools.py)
- Removed over-engineered autonomy scheduler
- Fixed Windows UTF-8 encoding issues
- Simplified to Python-only codebase
- Updated .gitignore with comprehensive exclusions
- Configured GitHub remote (BobbyW08/BECA)

---

## ✅ Phase 2: LangChain Integration & GUI - COMPLETE

### Accomplishments
**Gradio Chat Interface** ([beca_gui.py](beca_gui.py))
- Modern web-based chat UI
- Auto-port selection (handles conflicts)
- Chat history management
- Example prompts for user guidance
- Fixed Gradio list format compatibility

**LangChain Agent** ([src/langchain_agent.py](src/langchain_agent.py))
- ReAct pattern (Reason + Act)
- Ollama integration (qwen2.5-coder:3b-instruct-q4_K_M)
- Max 20 iterations, 120s timeout
- Verbose mode for transparency
- **Fixed**: Agent now includes full tool output in responses (not just summaries)

**LangChain Tools** ([src/langchain_tools.py](src/langchain_tools.py))
- `create_react_app` - Scaffold React projects
- `read_file` - Read file contents
- `write_file` - Write/create files
- `list_files` - List directory contents with icons

### Tech Stack
| Component | Technology |
|-----------|-----------|
| GUI | Gradio |
| Agent Framework | LangChain |
| LLM | Ollama + Qwen2.5-coder |
| Tools | LangChain @tool decorator |

### Issues Resolved
1. ✅ Port conflict (7860 in use) → Auto-port selection
2. ✅ Gradio format error → Switched tuples to lists
3. ✅ Agent iteration limit → Increased to 20
4. ✅ Vague responses → Updated prompt to include full details
5. ✅ Virtual environment setup → Documented activation process
6. ✅ GitHub branch confusion → Set master as default

---

## 🚧 Phase 3: Enhanced Tools & Templates - NEXT

### Goals
**More Tools** (Priority Order)
1. **Git Integration**
   - `git_commit(message)` - Commit changes
   - `git_status()` - Check repo status
   - `git_diff()` - View changes
   - `git_push()` - Push to remote

2. **Web Search** (DuckDuckGo - free!)
   - `web_search(query)` - Search the web
   - `fetch_url(url)` - Fetch web content
   - Use for docs, Stack Overflow, etc.

3. **Code Analysis**
   - `analyze_code(file_path)` - Static analysis
   - `find_bugs(file_path)` - Identify issues
   - `suggest_improvements(file_path)` - Refactoring ideas

4. **Testing**
   - `run_tests(path)` - Execute tests
   - `generate_tests(file_path)` - Create unit tests
   - `coverage_report()` - Test coverage stats

**Project Templates**
- Integrate Copier for professional scaffolding
- React + Vite template
- Flask API template
- Next.js template
- FastAPI template
- Custom template creation

**Memory & Learning**
- SQLite-backed conversation history
- Remember successful patterns
- Learn user preferences
- Context awareness across sessions

---

## 🔮 Phase 4: Advanced Features - FUTURE

### Ideas
**Enhanced GUI**
- Project dashboard with file tree
- Integrated code editor
- Side-by-side diff viewer
- Settings panel (model selection, temperature, etc.)
- Tool execution history

**Multi-Model Support**
- Llama 3.1/3.2 support
- DeepSeek Coder support
- Model switching based on task
- Fallback model chains

**Advanced Agent Capabilities**
- Multi-step planning with approval gates
- Parallel tool execution
- Error recovery strategies
- Self-correction loops

**Collaboration Features**
- Export conversations as markdown
- Share tool configurations
- Community template library

---

## How to Use BECA

### Prerequisites
1. **Install Ollama**: https://ollama.com/
2. **Pull model**: `ollama pull qwen2.5-coder:3b-instruct-q4_K_M`
3. **Ensure Ollama is running** (background service)

### Quick Start
```bash
cd c:\dev\beca
.venv\Scripts\activate  # Activate virtual environment
python beca_gui.py
```

Open browser to displayed URL (typically http://127.0.0.1:7861)

### Example Prompts
```
List the files in the current directory
Create a React app called my-portfolio
Read the file beca_gui.py and explain what it does
Create a file called notes.md with my project ideas
```

---

## Current Architecture

```
┌─────────────────┐
│  User (Browser) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Gradio GUI     │  (beca_gui.py)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ LangChain Agent │  (src/langchain_agent.py)
│  (ReAct)        │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Ollama Server   │  (qwen2.5-coder model)
│ (localhost:11434)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  LangChain      │  (src/langchain_tools.py)
│  Tools          │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ File System     │  (Create/Read/Write/List)
└─────────────────┘
```

---

## Development Notes

### Working Directory
- Main: `c:\dev\beca\`
- Virtual env: `c:\dev\beca\.venv\`
- Ollama models: `C:\dev\.ollama\`

### Git Configuration
- Remote: https://github.com/BobbyW08/BECA
- Default branch: `master`
- Commit format: Includes Claude Code attribution

### Key Lessons Learned
1. **Gradio** changed chat format from tuples to lists - always check deprecation warnings
2. **Agent iterations** matter - planning tasks need higher limits (20+ vs 10)
3. **Prompt engineering** critical - "include full details" drastically improved responses
4. **Port conflicts** happen - auto-selection better than hardcoded ports
5. **Virtual environments** prevent dependency conflicts

---

## Success Metrics

### Phase 2 ✅
- [x] GUI launches without errors
- [x] Agent connects to Ollama successfully
- [x] All 4 tools execute correctly
- [x] Agent responses include full tool output
- [x] End-to-end flow works reliably
- [x] Documentation complete

### Phase 3 (Target)
- [ ] 15+ tools available
- [ ] 5+ project templates working
- [ ] Conversation memory persists across sessions
- [ ] Agent can handle multi-step workflows
- [ ] 90%+ tool execution success rate

---

## Resources

### Documentation
- LangChain: https://python.langchain.com/docs/
- Gradio: https://www.gradio.app/docs
- Ollama: https://github.com/ollama/ollama/blob/main/docs/api.md

### Models
- Qwen2.5-Coder: https://ollama.com/library/qwen2.5-coder
- Llama 3.1: https://ollama.com/library/llama3.1
- DeepSeek Coder: https://ollama.com/library/deepseek-coder

---

**Last Updated**: 2025-09-30
**Current Phase**: Phase 2 Complete → Starting Phase 3
**Status**: 🟢 Production Ready (Basic Features)
