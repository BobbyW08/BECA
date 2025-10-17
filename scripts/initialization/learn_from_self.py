"""
BECA Self-Learning Script
Analyzes BECA's own codebase and extracts patterns to learn from

This demonstrates how BECA can learn from the work Claude/Cline does on her codebase
"""
import sys
sys.path.insert(0, 'src')

from knowledge_system import KnowledgeBase
import os

def learn_from_beca_codebase():
    """Analyze BECA's own codebase and save learnings"""
    
    print("🧠 BECA Self-Learning System")
    print("=" * 60)
    print("Analyzing BECA's own codebase to extract patterns...")
    print()
    
    kb = KnowledgeBase()
    
    # Key files to analyze for patterns
    key_files = [
        ("src/langchain_agent.py", "LangChain agent setup and dual-model routing"),
        ("src/langchain_tools.py", "Tool implementation patterns"),
        ("src/knowledge_system.py", "Thread-safe database patterns"),
        ("src/memory_db.py", "Conversation memory patterns"),
        ("src/code_generator.py", "AI code generation patterns"),
        ("src/codebase_explorer.py", "Repository analysis patterns"),
        ("beca_gui.py", "Gradio interface patterns"),
    ]
    
    print("🔍 Analyzing code patterns in key files...")
    print()
    
    patterns_found = []
    
    for file_path, description in key_files:
        full_path = os.path.join("C:/dev", file_path)
        if os.path.exists(full_path):
            print(f"📄 Analyzing {file_path}...")
            
            # Read file content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze patterns
            patterns = []
            lines = content.split('\n')
            
            # Python pattern detection
            if '@tool' in content:
                patterns.append("LangChain @tool decorator pattern")
            if 'threading.local()' in content:
                patterns.append("Thread-local storage pattern")
            if 'os.getenv' in content or 'os.environ' in content:
                patterns.append("Environment variable configuration")
            if 'def __enter__' in content or 'def __exit__' in content:
                patterns.append("Context manager pattern")
            if 'async def' in content or 'await ' in content:
                patterns.append("Async/await pattern")
            if ': str' in content or '-> ' in content:
                patterns.append("Type hints/annotations")
            if 'try:' in content and 'except' in content:
                patterns.append("Error handling pattern")
            if 'class ' in content:
                class_count = content.count('class ')
                patterns.append(f"OOP with {class_count} class(es)")
                
            print(f"   Found patterns: {', '.join(patterns) if patterns else 'Basic Python code'}")
            
            # Save to knowledge base
            kb.add_code_pattern(
                pattern_name=f"BECA - {description}",
                language="python",
                code_snippet=content[:500],  # First 500 chars as example
                description=f"Pattern learned from BECA's own {file_path}. Patterns: {', '.join(patterns)}",
                use_case=description,
                tags=["self-learning", "beca-architecture", file_path.split('/')[-1].replace('.py', '')],
                source_url=f"file:///{full_path}"
            )
            patterns_found.append(file_path)
            print(f"   ✓ Saved to knowledge base")
            print()
    
    print("="  * 60)
    print("✅ Saving architectural insights...")
    
    # Save high-level architecture insights
    architecture_insights = """
BECA Architecture Patterns Learned from Codebase Analysis:

1. **Dual-Model Routing Pattern** (langchain_agent.py)
   - Uses llama3.1:8b for general tasks, conversation, tool use
   - Uses qwen2.5-coder:7b for code generation and debugging
   - Automatically selects based on message keywords
   - Each model optimized for its specific use case
   
2. **Thread-Safe Database Pattern** (knowledge_system.py)
   - Uses threading.local() for connection pooling
   - Each thread gets its own database connection
   - Prevents SQLite "same thread" errors
   - Critical for autonomous learning background thread

3. **Configurable Endpoint Pattern** (langchain_agent.py, code_generator.py)
   - Environment variable (OLLAMA_URL) takes highest priority
   - Auto-detection fallback for cloud deployments
   - Localhost default for local development
   - Makes system portable across environments

4. **Tool-Based Architecture** (langchain_tools.py)
   - 50+ specialized tools using LangChain @tool decorator
   - Clean separation of concerns
   - Each tool is self-contained function
   - Easy to add new tools without changing core logic

5. **Memory & Learning Pattern** (memory_db.py, knowledge_system.py)
   - Conversations saved to memory_db (user interactions)
   - Knowledge saved to knowledge_db (learned information)
   - Can query past learnings for context
   - Tracks tool success rates for optimization

6. **Error Handling & Resilience** (throughout)
   - Graceful degradation when services unavailable
   - Try/except blocks with informative error messages
   - Fallback options when primary methods fail
   - User-friendly error reporting

7. **Type Safety** (most Python files)
   - Extensive use of type hints (: str, -> int, etc.)
   - Makes code more maintainable and IDE-friendly
   - Catches errors at development time
   - Self-documenting function signatures
"""
    
    kb.add_documentation(
        source="BECA Self-Analysis",
        url="file:///C:/dev",
        title="BECA Architectural Patterns (Learned from Own Codebase)",
        content=architecture_insights,
        category="architecture",
        tags=["self-learning", "architecture", "patterns", "beca"]
    )
    
    print("Saved architectural insights")
    
    # Save Claude/Cline development patterns observed in this codebase
    print("✅ Documenting development patterns from Claude/Cline work...")
    
    development_insights = """
Development Process Patterns Observed in BECA's Codebase:
(Extracted from recent Claude/Cline development sessions)

1. **Iterative Fix Pattern**
   - Issue: SQLite threading error breaking autonomous learning
   - Solution: Implement thread-local storage
   - Verification: Test with multiple threads
   - Documentation: Update docs with fix details
   
2. **Consistency Review Pattern**
   - Issue: Hard-coded Ollama endpoint in multiple files
   - Process: Search entire codebase for similar patterns
   - Action: Update all instances consistently
   - Result: No fragmentation, consistent behavior

3. **Configuration Over Hard-Coding**
   - Pattern: Use environment variables for deployment-specific values
   - Implementation: get_ollama_url() with priority chain
   - Benefits: Portability, flexibility, no code changes needed
   - Documentation: Clear usage examples in docs

4. **Thread-Safety First**
   - Pattern: Identify shared resources (database connections)
   - Solution: Use thread-local storage pattern
   - Testing: Multi-threaded test cases
   - Documentation: Explicit thread-safety guarantees

5. **Git-Based Recovery**
   - Pattern: When edits cause issues, restore from git
   - Command: git checkout <file>
   - Benefit: Clean slate without losing history
   - Practice: Commit working code frequently

6. **Defensive Programming**
   - Pattern: Assume operations may fail
   - Implementation: Try/except with specific error handling
   - User Experience: Helpful error messages
   - Logging: Capture errors for debugging

7. **Self-Referential Learning**
   - Pattern: BECA can analyze her own codebase
   - Tools: analyze_repository, analyze_code_patterns
   - Storage: Save learnings to knowledge_base
   - Application: Reference when building similar features
"""
    
    kb.add_documentation(
        source="BECA Self-Analysis",
        url="file:///C:/dev",
        title="Development Process Patterns (from Claude/Cline Sessions)",
        content=development_insights,
        category="development",
        tags=["self-learning", "development", "claude", "cline", "best-practices"]
    )
    
    print("Saved development process patterns")
    print()
    
    # Summary
    print("="  * 60)
    print("🎉 BECA Self-Learning Complete!")
    print()
    print(f"📊 Analyzed {len(patterns_found)} key files:")
    for f in patterns_found:
        print(f"   ✓ {f}")
    print()
    print(f"💾 Saved {len(patterns_found)} code patterns to knowledge base")
    print(f"🏗️  Documented architectural insights")
    print(f"🔧 Documented development patterns from Claude/Cline work")
    print()
    print("💡 BECA can now reference these patterns when:")
    print("   • Building similar features")
    print("   • Explaining her own architecture")
    print("   • Making improvements to codebase")
    print("   • Helping users understand the system")
    print("   • Applying learned patterns to new projects")
    print()
    print("🔍 Query the knowledge base:")
    print()
    print("   from src.knowledge_system import KnowledgeBase")
    print("   kb = KnowledgeBase()")
    print("   ")
    print("   # Search examples:")
    print("   results = kb.search_knowledge('thread-safe')")
    print("   results = kb.search_knowledge('dual model routing')")
    print("   results = kb.search_knowledge('configuration pattern')")
    print("   results = kb.search_knowledge('BECA architecture')")
    print()
    print("✨ BECA has now learned from her own development process!")

if __name__ == "__main__":
    try:
        learn_from_beca_codebase()
    except Exception as e:
        print(f"❌ Error during self-learning: {e}")
        import traceback
        traceback.print_exc()
