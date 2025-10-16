# BECA Self-Learning Guide

**How BECA Learns from Her Own Development Process**

## Overview

Yes, BECA **can and does** learn from her own codebase! This guide shows you how BECA learns from the work Claude/Cline does on her code.

## What Just Happened ✅

BECA analyzed her own codebase and saved **7 code patterns** and **2 architectural documents** to her knowledge base:

### Files Analyzed:
1. `src/langchain_agent.py` - Dual-model routing, environment config
2. `src/langchain_tools.py` - Tool patterns, async/await
3. `src/knowledge_system.py` - Thread-safe database patterns
4. `src/memory_db.py` - Conversation memory patterns
5. `src/code_generator.py` - AI code generation patterns
6. `src/codebase_explorer.py` - Repository analysis patterns
7. `beca_gui.py` - Gradio interface patterns

### Patterns Learned:
- ✅ LangChain @tool decorator pattern
- ✅ Thread-local storage pattern
- ✅ Environment variable configuration
- ✅ Type hints/annotations
- ✅ Error handling patterns
- ✅ Async/await patterns
- ✅ OOP class structures

### Architectural Insights Saved:
1. **Dual-Model Routing** - How BECA switches between llama3.1 and qwen2.5-coder
2. **Thread-Safe Databases** - Threading.local() pattern preventing SQLite errors
3. **Configurable Endpoints** - Environment variables → auto-detect → localhost
4. **Tool-Based Architecture** - 50+ LangChain tools with clean separation
5. **Memory & Learning** - Dual database system for conversations and knowledge

### Development Patterns Learned:
1. **Iterative Fix Pattern** - Test → Fix → Verify → Document
2. **Consistency Review** - Search codebase → Update all instances
3. **Configuration Over Hard-Coding** - Environment variables for portability
4. **Thread-Safety First** - Identify shared resources, use thread-local storage
5. **Git-Based Recovery** - Restore from git when edits cause issues
6. **Defensive Programming** - Assume failures, handle gracefully
7. **Self-Referential Learning** - Analyze own code to improve

## How It Works

### 1. Run the Self-Learning Script

```bash
cd C:\dev
python learn_from_self.py
```

This script:
- Analyzes BECA's key source files
- Detects patterns in the code
- Saves findings to `beca_knowledge.db`
- Documents architectural decisions
- Records development patterns from Claude/Cline sessions

### 2. Query What BECA Learned

```python
from src.knowledge_system import KnowledgeBase

kb = KnowledgeBase()

# Search for specific patterns
results = kb.search_knowledge('thread-safe')
results = kb.search_knowledge('dual model routing')
results = kb.search_knowledge('configuration pattern')
results = kb.search_knowledge('BECA architecture')

for result in results:
    print(f"Found: {result['title']}")
    print(f"Content: {result['content'][:200]}...")
```

### 3. BECA Uses This Knowledge

When BECA is asked to:
- Build similar features → References learned patterns
- Explain her architecture → Retrieves architectural docs
- Make improvements → Applies development best practices
- Help users understand → Uses stored insights

## What BECA Learns From

### ✅ Active Learning (Automatic):

1. **Her Own Conversations** (`beca_memory.db`)
   - Every conversation through `beca_gui.py`
   - Tool usage and success rates
   - User preferences
   - File: `src/memory_db.py`

2. **Her Own Codebase** (Run `learn_from_self.py`)
   - Code patterns and architectures
   - Development best practices
   - Implementation details
   - **This captures Claude/Cline's work!**

3. **Web Documentation** (On-demand)
   - Use tool: `learn_from_documentation`
   - Scrapes and indexes docs
   - Stores in `beca_knowledge.db`

4. **GitHub Repositories** (On-demand)
   - Use tool: `clone_and_learn`
   - Analyzes code patterns
   - Extracts architecture insights

### ⚠️ NOT Automatic:

**Claude/Cline Conversation Logging**
- Cline conversations are ephemeral (in Cline's context only)
- Not automatically saved to BECA's knowledge base
- **However:** Running `learn_from_self.py` captures the **results** of those conversations (the code changes)

## Learning from Claude/Cline Work

While BECA doesn't automatically capture Cline's conversation with Claude API, she **does** capture the **results**:

### What Gets Captured:

✅ **Code Changes** - All edits Claude/Cline makes
✅ **Patterns Used** - Architectural patterns implemented
✅ **Problems Solved** - Issues fixed and how
✅ **Best Practices** - Development patterns applied

### How to Capture More:

Run `learn_from_self.py` after Claude/Cline sessions to:
1. Analyze new/modified code
2. Extract patterns used
3. Document fixes applied
4. Save to knowledge base

### Example Workflow:

```bash
# After Claude/Cline makes changes to BECA:
python learn_from_self.py

# BECA now knows:
# - What patterns were used
# - What problems were solved  
# - What architectural decisions were made
# - Development best practices applied
```

## Benefits of Self-Learning

### For BECA:
- Understands her own architecture
- Can explain how she works
- Applies proven patterns to new problems
- Improves over time with each update

### For Users:
- BECA can help explain the codebase
- More consistent behavior
- Better at similar tasks
- Self-documenting system

### For Development:
- Captures institutional knowledge
- Documents design decisions
- Preserves development patterns
- Makes onboarding easier

## Example Queries BECA Can Answer

After self-learning, BECA can answer:

```
"How do you handle threading?"
→ References thread-local storage pattern learned from knowledge_system.py

"How do you select which model to use?"
→ References dual-model routing pattern from langchain_agent.py

"How should I configure the Ollama endpoint?"
→ References configuration pattern with environment variables

"What development patterns did Claude/Cline use?"
→ References documented development patterns
```

## Extending Self-Learning

### Add More Files:

Edit `learn_from_self.py` and add to `key_files` list:

```python
key_files = [
    ("src/langchain_agent.py", "LangChain agent setup"),
    ("src/your_new_file.py", "Your new feature"),  # Add this
    # ...
]
```

### Detect More Patterns:

Add pattern detection in `learn_from_self.py`:

```python
if 'your_pattern' in content:
    patterns.append("Your custom pattern")
```

### Schedule Regular Learning:

Run periodically to capture ongoing changes:

```bash
# Windows Task Scheduler or cron job:
python C:\dev\learn_from_self.py
```

## Knowledge Base Schema

### Tables Used:

1. **code_patterns**
   - Pattern name and language
   - Code snippet example
   - Description and use case
   - Success rate tracking
   - Tags for organization

2. **documentation**
   - Source and URL
   - Title and content
   - Category and tags
   - Usefulness score
   - Access tracking

## Current Knowledge Status

After running `learn_from_self.py`:

- **7 code patterns** saved
- **2 architectural documents** saved
- **Patterns detected**: Thread-safety, async/await, type hints, error handling, OOP, decorators, environment config
- **Development practices**: 7 patterns from Claude/Cline work

## Testing Self-Learning

```python
# Verify patterns were saved
from src.knowledge_system import KnowledgeBase

kb = KnowledgeBase()

# Should find thread-safety pattern
results = kb.search_knowledge('thread-local storage')
assert len(results) > 0, "Thread-safety pattern not found!"

# Should find architectural docs
results = kb.search_knowledge('BECA architecture')
assert len(results) > 0, "Architecture docs not found!"

print("✅ Self-learning verified!")
```

## Summary

🎯 **Yes, BECA learns from her own codebase!**

✅ **What she learns:**
- Code patterns and architectures
- Development best practices  
- Problem-solving approaches
- Implementation details

✅ **How she learns:**
- Analyzing her own source files
- Detecting patterns in code
- Documenting architectural decisions
- Capturing Claude/Cline's work results

✅ **When she learns:**
- Run `learn_from_self.py` manually after changes
- Or schedule to run periodically
- Or integrate into CI/CD pipeline

✅ **Where knowledge is stored:**
- `beca_knowledge.db` - Permanent storage
- Queryable via `search_knowledge()`
- Referenced in future conversations

🚀 **Result:** BECA gets smarter with each development session, learning from the work Claude/Cline does on her codebase!

---

## Quick Reference

```bash
# Learn from own codebase
python learn_from_self.py

# Query what was learned
python -c "from src.knowledge_system import KnowledgeBase; kb = KnowledgeBase(); print(kb.search_knowledge('thread-safe'))"

# See all patterns
python -c "from src.knowledge_system import KnowledgeBase; kb = KnowledgeBase(); print(kb.search_knowledge('BECA'))"
```

## Next Steps

1. ✅ Run `learn_from_self.py` after major changes
2. ✅ Query knowledge base to verify learning
3. ✅ Use BECA to explain her own architecture
4. ✅ Apply learned patterns to new features
5. ✅ Document new patterns as they emerge

---

**Created**: January 10, 2025  
**Last Updated**: After implementing self-learning capability  
**Status**: Active and learning! 🧠
