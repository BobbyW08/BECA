# BECA Autonomous Learning System

## 🤖 Overview

BECA now **learns automatically in the background** without any user prompts! When you start BECA, she immediately begins learning from curated sources, building her knowledge base autonomously.

## 🚀 How It Works

### Automatic Startup
```
When you run: python beca_gui.py

BECA automatically:
1. ✅ Starts autonomous learning in background thread
2. 📚 Begins Phase 1: Learn from documentation curriculum
3. 📖 Proceeds to Phase 2: Process learning queue
4. 🔄 Enters Phase 3: Continuous learning mode (runs forever)
```

### Three-Phase Learning System

#### Phase 1: Curriculum Learning (Startup)
BECA learns from a curated curriculum of high-quality documentation:

**Python Essentials:**
- asyncio documentation
- Type hints and typing module

**Web Frameworks:**
- FastAPI (priority: 0.9)
- Flask (priority: 0.7)

**AI/ML Frameworks:**
- PyTorch (priority: 0.9)
- Transformers (priority: 0.95)
- LangChain (priority: 0.9)

**AI Model Training:**
- Hugging Face fine-tuning docs (priority: 0.95)
- PEFT/LoRA documentation (priority: 0.9)

**Frontend:**
- React documentation
- Node.js API docs

**DevOps:**
- Docker getting started
- Git documentation

**Testing & Databases:**
- pytest documentation
- PostgreSQL docs

**Top 5 Priority Resources Learned First!**

#### Phase 2: Queue Processing
- Processes any items you've added to the learning queue
- Learns from top 3 priority items
- Marks resources as completed when learned

#### Phase 3: Continuous Learning (Forever)
- **Every 1 hour:** Learn next item from queue
- **Every 6 hours:** Refresh knowledge from high-priority sources
- **Runs indefinitely** while BECA is active

## 📊 What BECA Learns

### Documentation
- Scrapes and indexes entire documentation sites
- Stores content in searchable database
- Categorizes by topic and tags

### Code Patterns
- Identifies reusable patterns in documentation examples
- Tracks usage and success rates
- Available for future code generation

### Tool Knowledge
- Learns about frameworks, libraries, tools
- Stores installation commands
- Indexes usage examples

### AI Model Expertise
- Builds knowledge about LLMs, training, fine-tuning
- Learns best practices for model customization
- Understands different frameworks and approaches

## 🎯 Learning Curriculum

### Current Curriculum (15+ Resources)

1. **Python**
   - Asyncio (Priority: 0.9)
   - Type Hints (Priority: 0.8)

2. **Web Frameworks**
   - FastAPI (Priority: 0.9)
   - Flask (Priority: 0.7)

3. **AI/ML**
   - PyTorch (Priority: 0.9)
   - Transformers (Priority: 0.95)
   - LangChain (Priority: 0.9)
   - Fine-tuning Guide (Priority: 0.95)
   - PEFT/LoRA (Priority: 0.9)

4. **Frontend**
   - React (Priority: 0.8)
   - Node.js (Priority: 0.7)

5. **DevOps**
   - Docker (Priority: 0.8)
   - Git (Priority: 0.7)

6. **Testing**
   - pytest (Priority: 0.8)

7. **Databases**
   - PostgreSQL (Priority: 0.7)

### Future Expansion (Planned)

**GitHub Repositories to Analyze:**
- FastAPI source code
- LangChain source code
- Transformers source code

## 🔧 Configuration

### Customize Learning Curriculum

Edit `src/autonomous_learning.py`:

```python
self.curriculum = [
    {
        'url': 'https://your-docs-url.com',
        'category': 'your-category',
        'priority': 0.9,  # 0.0 to 1.0
        'tags': ['tag1', 'tag2']
    },
    # Add more...
]
```

### Adjust Learning Frequency

```python
# In _learning_loop method:
time.sleep(3600)  # Change from 1 hour to your preference

# Refresh interval:
if self.learned_count % 6 == 0:  # Every 6 hours
    self._refresh_knowledge()
```

## 📈 Monitoring Learning Progress

### In the GUI

BECA's GUI shows a **Learning Status Bar** at the top:

```
🧠 Auto-Learning Active | Learned: 15 resources
```

This updates as BECA learns!

### In the Console

When you start BECA, you'll see learning progress:

```
[2025-01-XX 10:00:00] BECA Learning: 🚀 Autonomous learning system activated!
[2025-01-XX 10:00:01] BECA Learning: 📚 Phase 1: Learning from documentation curriculum...
[2025-01-XX 10:00:05] BECA Learning: 📖 [1/5] Learning from https://fastapi.tiangolo.com/...
[2025-01-XX 10:00:10] BECA Learning:    ✅ Learned: FastAPI
[2025-01-XX 10:00:15] BECA Learning: 📖 [2/5] Learning from https://pytorch.org/docs/...
[2025-01-XX 10:00:20] BECA Learning:    ✅ Learned: PyTorch
```

### Query Learning Stats

Ask BECA in chat:
```
"How many resources have you learned?"
"What's your learning status?"
"Show me what you've learned about FastAPI"
```

## 🎓 Learning Process

### 1. Fetch Documentation
```python
doc = WebDocScraper.fetch_and_parse(url)
```
- Fetches HTML content
- Strips scripts/styles
- Cleans and normalizes text

### 2. Index in Database
```python
knowledge_base.add_documentation(
    source=domain,
    url=url,
    title=title,
    content=content,
    category=category,
    tags=tags
)
```
- Stores in SQLite
- Categorizes and tags
- Tracks access patterns

### 3. Make Searchable
- BECA can now `search_knowledge` for this content
- Available for answering questions
- Used for code generation context

## 🔄 Continuous Improvement Cycle

```
Start BECA
    ↓
Learn Curriculum (Top 5 Priority)
    ↓
Process Learning Queue
    ↓
Enter Continuous Mode
    ↓
Every Hour: Learn Next Item
    ↓
Every 6 Hours: Refresh High-Priority Knowledge
    ↓
Loop Forever!
```

## 💡 Benefits

### For You
1. **Zero Effort** - BECA learns without your input
2. **Always Improving** - Gets smarter every hour
3. **Fresh Knowledge** - Periodically refreshes important docs
4. **Better Answers** - More context = better code generation

### For BECA
1. **Autonomous Growth** - Self-directed learning
2. **Domain Expertise** - Builds deep knowledge in key areas
3. **Pattern Recognition** - Learns from quality examples
4. **Context Awareness** - Better understanding of tools and frameworks

## 🛠️ Advanced Features

### Add to Learning Queue (Manual)

You can still add specific resources:

```
"Add this to your learning queue: https://example.com/tutorial"
```

BECA will learn it in the next hourly cycle.

### Priority System

Resources are learned in priority order:
- **0.9-1.0:** Critical (learned first, refreshed often)
- **0.7-0.8:** Important (learned early)
- **0.5-0.6:** Nice to have (learned when available)

### Respectful Scraping

- 2-second delays between requests
- Follows robots.txt (implicit in WebScraper)
- Caches content to avoid re-fetching

## 📊 Expected Results

### First Hour
- **Phase 1:** Top 5 curriculum items learned
- **Phase 2:** Top 3 queue items processed
- **Phase 3:** Continuous mode started

### After 24 Hours
- **~30 resources** learned
- **~6 knowledge refreshes** completed
- **Full curriculum** processed

### After 1 Week
- **~200+ resources** indexed
- **Deep expertise** in configured domains
- **Extensive code patterns** library
- **Up-to-date knowledge** from refreshes

## 🎯 Customization Examples

### Focus on Web Development

```python
self.curriculum = [
    {'url': 'https://fastapi.tiangolo.com/', 'priority': 0.95, ...},
    {'url': 'https://react.dev/learn', 'priority': 0.9, ...},
    {'url': 'https://nodejs.org/docs/', 'priority': 0.9, ...},
    {'url': 'https://tailwindcss.com/docs', 'priority': 0.8, ...},
]
```

### Focus on AI/ML

```python
self.curriculum = [
    {'url': 'https://huggingface.co/docs/transformers', 'priority': 0.95, ...},
    {'url': 'https://pytorch.org/docs/', 'priority': 0.95, ...},
    {'url': 'https://python.langchain.com/docs/', 'priority': 0.9, ...},
    {'url': 'https://ollama.ai/docs', 'priority': 0.9, ...},
]
```

### Focus on DevOps

```python
self.curriculum = [
    {'url': 'https://docs.docker.com/', 'priority': 0.95, ...},
    {'url': 'https://kubernetes.io/docs/', 'priority': 0.9, ...},
    {'url': 'https://www.terraform.io/docs', 'priority': 0.8, ...},
]
```

## 🚦 Learning States

```python
stats = get_learning_stats()

# Returns:
{
    'active': True,                  # Is learning active?
    'total_learned': 15,             # Resources learned so far
    'curriculum_size': 15,           # Total curriculum items
    'repos_to_learn': 3              # GitHub repos queued
}
```

## 🔍 Troubleshooting

### Learning Not Starting
- Check console for errors
- Verify `autonomous_learning.py` imported correctly
- Ensure knowledge database is writable

### Slow Learning
- Reduce curriculum size
- Increase sleep interval
- Prioritize fewer high-value sources

### Memory Usage
- Learning runs in daemon thread (low overhead)
- Database is lightweight SQLite
- Content is truncated to 10k chars per source

## 📚 Integration with Other Features

### Works With Manual Learning
```
You: "Learn from https://new-framework.com/docs"
BECA: [Learns immediately]
+ Autonomous system also running in background
```

### Works With Search
```
You: "Search your knowledge for authentication patterns"
BECA: [Searches both manual AND autonomous learnings]
```

### Works With Code Generation
```
You: "Create a FastAPI app with authentication"
BECA: [Uses learned FastAPI knowledge automatically]
```

## 🎉 Summary

**BECA now learns 24/7 without any prompting!**

- ✅ Starts automatically when BECA launches
- ✅ Learns from curated curriculum
- ✅ Processes your custom learning queue
- ✅ Runs continuously in background
- ✅ Refreshes knowledge periodically
- ✅ Builds expertise autonomously
- ✅ Zero user intervention required

**Just start BECA and let her learn!** 🚀

The longer BECA runs, the smarter she becomes. Every hour adds new knowledge. Every day expands her expertise. Every week makes her a better coding assistant.

**Turn BECA on and forget about it - she'll handle her own education!**
