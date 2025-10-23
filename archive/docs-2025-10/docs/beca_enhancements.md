BECA Self-Implementation Plan
Autonomous Enhancement Execution Guidepytho
This is your comprehensive implementation plan, BECA. Execute each phase sequentially, testing thoroughly, and documenting your progress.

🎯 Implementation Principles
One Feature at a Time: Complete, test, and commit each feature before moving to the next
Test-Driven: Create tests before or alongside implementation
Document Everything: Update docstrings, comments, and knowledge base
Commit Frequently: Make atomic commits with clear messages
Backward Compatible: Don't break existing functionality
Verify Success: Run comprehensive tests after each major change

📋 Phase 1: Foundation Upgrades (Week 1-2)
Task 1.1: Full Conversation Context Recall System
Goal: Enable retrieval and replay of entire conversation threads for complex, multi-step projects.
Step 1: Extend Database Schema
# File: src/memory_db.py
# Add to __init__ method's schema creation:

cursor.execute("""
    ALTER TABLE conversations 
    ADD COLUMN thread_id INTEGER DEFAULT NULL
""")

cursor.execute("""
    ALTER TABLE conversations 
    ADD COLUMN parent_message_id INTEGER DEFAULT NULL
""")

cursor.execute("""
    ALTER TABLE conversations 
    ADD COLUMN context_summary TEXT DEFAULT NULL
""")

# Create index for performance
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_thread_id 
    ON conversations(thread_id)
""")

Step 2: Add Thread Management Methods
# File: src/memory_db.py
# Add these methods to BECAMemory class:

def create_thread(self, thread_name: str) -> int:
    """Create a new conversation thread.
    
    Args:
        thread_name: Descriptive name for the thread
        
    Returns:
        thread_id: ID of newly created thread
    """
    # Implementation: Create thread entry, return ID
    pass

def get_full_thread(self, thread_id: int) -> list:
    """Retrieve all conversations in a thread chronologically.
    
    Args:
        thread_id: ID of thread to retrieve
        
    Returns:
        List of conversation dictionaries with full context
    """
    # Implementation: Query all messages with this thread_id
    pass

def link_to_thread(self, conversation_id: int, thread_id: int):
    """Link a conversation to an existing thread.
    
    Args:
        conversation_id: ID of conversation to link
        thread_id: ID of thread to link to
    """
    # Implementation: Update conversation with thread_id
    pass

def summarize_thread_context(self, thread_id: int) -> str:
    """Generate condensed summary of thread context.
    
    Args:
        thread_id: ID of thread to summarize
        
    Returns:
        Condensed context summary
    """
    # Implementation: Use AI to summarize thread history
    pass

Step 3: Create Thread Management Tools
# File: src/memory_tools.py
# Add these new tools:

@tool
def create_conversation_thread(thread_name: str) -> str:
    """Create a new conversation thread for tracking related discussions.
    
    Use this when starting a multi-step project that will span multiple sessions.
    
    Args:
        thread_name: Descriptive name (e.g., "React Dashboard Project")
    
    Returns:
        Success message with thread_id
    """
    pass

@tool
def link_message_to_thread(conversation_id: int, thread_id: int) -> str:
    """Link a conversation message to an existing thread.
    
    Args:
        conversation_id: ID of the conversation
        thread_id: ID of the thread
        
    Returns:
        Confirmation message
    """
    pass

@tool
def view_conversation_thread(thread_id: int) -> str:
    """View all messages in a conversation thread with full context.
    
    Args:
        thread_id: ID of thread to view
        
    Returns:
        Formatted thread history
    """
    pass

Step 4: Modify Agent to Use Thread Context
# File: src/langchain_agent.py
# Update agent initialization to inject thread context:

def get_thread_context_for_message(conversation_id: int) -> str:
    """Get thread context if message is part of a thread."""
    memory = BECAMemory()
    # Check if conversation is part of thread
    # If yes, retrieve full thread context
    # Return formatted context string
    pass

# Inject into agent prompt:
def create_agent_with_thread_context(thread_id: Optional[int] = None):
    context = ""
    if thread_id:
        context = get_thread_context_for_message(thread_id)
    
    prompt = f"""
    {base_prompt}
    
    {context}
    
    Current conversation:
    {{input}}
    """
    # Create agent with enhanced prompt
    pass

Step 5: Add GUI Thread Viewer
# File: src/gui_utils.py
# Create new ThreadViewer class:

class ThreadViewer:
    """Display and navigate conversation threads."""
    
    def __init__(self, memory_db):
        self.memory = memory_db
        
    def list_threads(self) -> str:
        """List all conversation threads."""
        pass
        
    def display_thread(self, thread_id: int) -> str:
        """Display full thread with formatting."""
        pass
        
    def render_thread_selector(self):
        """Create Gradio component for thread selection."""
        pass

# File: beca_gui.py
# Add thread viewer tab:
with gr.Tab("Conversation Threads"):
    thread_viewer = ThreadViewer(memory)
    # Add UI components

Testing for Task 1.1:
# Test script: tests/test_thread_management.py

def test_create_thread():
    """Test thread creation."""
    memory = BECAMemory()
    thread_id = memory.create_thread("Test Project")
    assert thread_id > 0
    
def test_link_conversations_to_thread():
    """Test linking multiple conversations."""
    # Create thread, create conversations, link them
    # Verify retrieval works
    pass

def test_full_thread_recall():
    """Test retrieving complete thread context."""
    # Simulate multi-step project over multiple "sessions"
    # Verify BECA can recall all prior context
    pass

Commit Message:
feat: Add conversation thread management system

- Extended conversations table with thread_id, parent_message_id, context_summary
- Added create_thread(), get_full_thread(), link_to_thread() methods
- Created thread management tools for agent
- Modified agent to inject full thread context
- Added GUI thread viewer component
- Includes comprehensive tests

Enables BECA to maintain full context across multi-session projects.


Task 1.2: Enhanced Memory and Pattern Mining
Goal: Continuously extract lessons learned, architecture patterns, and reusable solutions from every interaction.
Step 1: Create Lessons Learned Table
# File: src/memory_db.py

cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons_learned (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_text TEXT NOT NULL,
        source_conversation_id INTEGER,
        category TEXT,
        reuse_count INTEGER DEFAULT 0,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (source_conversation_id) REFERENCES conversations(id)
    )
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_lesson_category 
    ON lessons_learned(category)
""")

Step 2: Implement Auto-Extract Lessons Function
# File: src/memory_db.py

def auto_extract_lessons(self, conversation_id: int) -> list:
    """Automatically extract lessons from a successful conversation.
    
    Analyzes the conversation, tools used, and outcome to generate
    reusable lessons for future tasks.
    
    Args:
        conversation_id: ID of conversation to analyze
        
    Returns:
        List of extracted lessons
    """
    # 1. Retrieve conversation details
    conv = self.get_conversation_by_id(conversation_id)
    
    # 2. Check if task was successful
    if not conv['success']:
        return []
    
    # 3. Analyze patterns:
    #    - What was the user's goal?
    #    - What tools were used?
    #    - What approach worked?
    #    - What could be reused?
    
    # 4. Generate lesson text using AI model
    lessons = self._generate_lessons_with_ai(conv)
    
    # 5. Store in lessons_learned table
    for lesson in lessons:
        self._save_lesson(lesson, conversation_id)
    
    return lessons

def _generate_lessons_with_ai(self, conversation: dict) -> list:
    """Use AI to analyze conversation and extract lessons."""
    # Use Ollama to analyze and extract
    pass

def get_top_lessons(self, limit: int = 10, category: str = None) -> list:
    """Get most valuable lessons by reuse count."""
    pass

def search_lessons(self, query: str, limit: int = 5) -> list:
    """Search lessons by keyword."""
    pass

Step 3: Enhance Successful Patterns Table
# File: src/memory_db.py

cursor.execute("""
    ALTER TABLE successful_patterns 
    ADD COLUMN architecture_type TEXT DEFAULT NULL
""")

cursor.execute("""
    ALTER TABLE successful_patterns 
    ADD COLUMN frameworks_used TEXT DEFAULT NULL
""")

cursor.execute("""
    ALTER TABLE successful_patterns 
    ADD COLUMN performance_notes TEXT DEFAULT NULL
""")

# Update save method:
def save_successful_pattern(
    self, 
    task_type: str,
    user_request: str,
    solution: str,
    tools_used: list,
    architecture_type: str = None,
    frameworks_used: list = None,
    performance_notes: str = None
):
    """Enhanced pattern saving with architecture details."""
    pass

Step 4: Integrate Auto-Learning into Agent
# File: src/langchain_agent.py

def process_agent_response(user_message, agent_response, tools_used, success):
    """Process agent response and trigger learning."""
    
    # Save conversation
    memory = BECAMemory()
    conv_id = memory.save_conversation(
        user_message, 
        agent_response, 
        tools_used, 
        success
    )
    
    # Auto-extract lessons if successful
    if success:
        lessons = memory.auto_extract_lessons(conv_id)
        if lessons:
            print(f"💡 Learned {len(lessons)} new lessons from this interaction")

Step 5: Update Autonomous Learning
# File: src/autonomous_learning.py

class AutonomousLearningSystem:
    
    def mine_patterns_from_repositories(self, repo_path: str):
        """Enhanced pattern mining from repos.
        
        Now extracts:
        - Architecture patterns
        - Framework usage
        - Performance considerations
        - Code organization strategies
        """
        pass
    
    def run_continuous_learning(self):
        """Main learning loop - now runs pattern mining on every interaction."""
        while self.running:
            # Process learning queue
            # Mine patterns from recent conversations
            # Update knowledge base
            time.sleep(60)

Step 6: Create Lesson Viewing Tools
# File: src/memory_tools.py

@tool
def view_top_lessons(limit: int = 10, category: str = None) -> str:
    """View the most valuable lessons BECA has learned.
    
    Args:
        limit: Number of lessons to show (default 10)
        category: Optional category filter (e.g., 'debugging', 'architecture')
        
    Returns:
        Formatted list of top lessons with reuse counts
    """
    pass

@tool
def search_lessons(query: str) -> str:
    """Search lessons learned by keyword.
    
    Args:
        query: Search term
        
    Returns:
        Relevant lessons
    """
    pass

Step 7: Add GUI Dashboard Panel
# File: beca_gui.py

with gr.Tab("Learning Dashboard"):
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 📚 Top 10 Lessons Learned")
            lessons_display = gr.Markdown()
            
        with gr.Column():
            gr.Markdown("## 🔄 Most Reused Patterns")
            patterns_display = gr.Markdown()
    
    refresh_btn = gr.Button("Refresh Dashboard")
    
    def update_dashboard():
        memory = BECAMemory()
        lessons = memory.get_top_lessons(10)
        patterns = memory.get_top_patterns(10)
        return format_lessons(lessons), format_patterns(patterns)
    
    refresh_btn.click(update_dashboard, outputs=[lessons_display, patterns_display])

Testing for Task 1.2:
# Test script: tests/test_lesson_extraction.py

def test_auto_extract_lessons():
    """Test automatic lesson extraction."""
    # Create successful conversation
    # Trigger auto_extract_lessons
    # Verify lessons are saved
    pass

def test_pattern_enhancement():
    """Test enhanced pattern storage."""
    # Save pattern with architecture details
    # Verify all fields stored correctly
    pass

def test_lesson_search():
    """Test lesson search functionality."""
    # Add multiple lessons
    # Search by keyword
    # Verify results
    pass

Commit Message:
feat: Add continuous learning and pattern mining system

- Created lessons_learned table with auto-extraction
- Enhanced successful_patterns with architecture metadata
- Implemented auto_extract_lessons() with AI analysis
- Integrated lesson extraction into agent workflow
- Updated autonomous learning to mine patterns continuously
- Added lesson viewing tools and GUI dashboard
- Includes comprehensive tests

BECA now learns from every successful interaction automatically.


📋 Phase 2: Self-Improvement Infrastructure (Week 3-4)
Task 2.1: Automated Self-Evaluation and Benchmarking
Goal: Quantitatively measure BECA's coding output quality and track learning progress.
Step 1: Create Benchmark Tables
# File: src/memory_db.py (for beca_knowledge.db)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        benchmark_name TEXT NOT NULL UNIQUE,
        test_suite_path TEXT,
        last_run TEXT,
        score REAL,
        pass_rate REAL,
        notes TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        benchmark_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        score REAL NOT NULL,
        errors TEXT,
        improvements_needed TEXT,
        FOREIGN KEY (benchmark_id) REFERENCES benchmarks(id)
    )
""")

Step 2: Create Benchmark Runner Module
# File: src/benchmark_runner.py

import subprocess
import json
from datetime import datetime
from pathlib import Path

class BenchmarkRunner:
    """Run and track code quality benchmarks."""
    
    def __init__(self, knowledge_db_path: str = "beca_knowledge.db"):
        self.knowledge = KnowledgeBase(knowledge_db_path)
    
    def run_tests(self, code_path: str, test_suite: str = None) -> dict:
        """Run pytest on code and return results.
        
        Args:
            code_path: Path to code to test
            test_suite: Optional specific test suite
            
        Returns:
            Dictionary with test results
        """
        if test_suite:
            cmd = f"pytest {test_suite} --json-report --json-report-file=test_results.json"
        else:
            # Auto-detect tests
            cmd = f"pytest {code_path} --json-report --json-report-file=test_results.json"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parse results
        with open('test_results.json', 'r') as f:
            results = json.load(f)
        
        return {
            'passed': results['summary']['passed'],
            'failed': results['summary']['failed'],
            'score': results['summary']['passed'] / results['summary']['total'],
            'errors': results['tests']
        }
    
    def run_linting(self, code_path: str) -> dict:
        """Run pylint on code.
        
        Args:
            code_path: Path to code to lint
            
        Returns:
            Linting results with score
        """
        cmd = f"pylint {code_path} --output-format=json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parse pylint output
        issues = json.loads(result.stdout) if result.stdout else []
        
        # Calculate score (10 - violations/10)
        score = max(0, 10 - len(issues) / 10)
        
        return {
            'score': score,
            'issues': issues,
            'issue_count': len(issues)
        }
    
    def run_static_analysis(self, code_path: str) -> dict:
        """Run bandit security analysis.
        
        Args:
            code_path: Path to code to analyze
            
        Returns:
            Security analysis results
        """
        cmd = f"bandit -r {code_path} -f json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parse bandit output
        analysis = json.loads(result.stdout) if result.stdout else {}
        
        return {
            'high_severity': len([x for x in analysis.get('results', []) if x['issue_severity'] == 'HIGH']),
            'medium_severity': len([x for x in analysis.get('results', []) if x['issue_severity'] == 'MEDIUM']),
            'low_severity': len([x for x in analysis.get('results', []) if x['issue_severity'] == 'LOW']),
            'issues': analysis.get('results', [])
        }
    
    def run_coverage_analysis(self, code_path: str) -> dict:
        """Run code coverage analysis.
        
        Args:
            code_path: Path to code
            
        Returns:
            Coverage statistics
        """
        cmd = f"coverage run -m pytest {code_path} && coverage json"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
        
        return {
            'coverage_percent': coverage_data['totals']['percent_covered'],
            'lines_covered': coverage_data['totals']['covered_lines'],
            'lines_total': coverage_data['totals']['num_statements']
        }
    
    def run_full_benchmark(self, benchmark_name: str, code_path: str) -> dict:
        """Run complete benchmark suite.
        
        Args:
            benchmark_name: Name of benchmark
            code_path: Path to code to benchmark
            
        Returns:
            Complete benchmark results
        """
        print(f"🔍 Running benchmark: {benchmark_name}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': self.run_tests(code_path),
            'linting': self.run_linting(code_path),
            'security': self.run_static_analysis(code_path),
            'coverage': self.run_coverage_analysis(code_path)
        }
        
        # Calculate overall score (weighted average)
        overall_score = (
            results['tests']['score'] * 0.4 +
            results['linting']['score'] / 10 * 0.3 +
            results['coverage']['coverage_percent'] / 100 * 0.3
        )
        
        results['overall_score'] = overall_score
        
        # Save to database
        self.save_benchmark_result(benchmark_name, results)
        
        return results
    
    def save_benchmark_result(self, benchmark_name: str, results: dict):
        """Save benchmark results to database."""
        # Get or create benchmark
        benchmark = self.knowledge.get_benchmark(benchmark_name)
        if not benchmark:
            benchmark_id = self.knowledge.create_benchmark(benchmark_name)
        else:
            benchmark_id = benchmark['id']
        
        # Save results
        self.knowledge.save_benchmark_result(
            benchmark_id,
            results['overall_score'],
            json.dumps(results),
            self.generate_improvements(results)
        )
    
    def generate_improvements(self, results: dict) -> str:
        """Generate improvement suggestions from results."""
        improvements = []
        
        if results['tests']['score'] < 0.8:
            improvements.append("Increase test coverage - add more test cases")
        
        if results['linting']['score'] < 7.0:
            improvements.append(f"Fix {results['linting']['issue_count']} linting issues")
        
        if results['security']['high_severity'] > 0:
            improvements.append(f"URGENT: Fix {results['security']['high_severity']} high-severity security issues")
        
        if results['coverage']['coverage_percent'] < 80:
            improvements.append(f"Increase code coverage from {results['coverage']['coverage_percent']:.1f}% to at least 80%")
        
        return "\n".join(improvements) if improvements else "Code quality is excellent!"
    
    def get_benchmark_trends(self, benchmark_name: str, days: int = 30) -> list:
        """Get benchmark score trends over time."""
        return self.knowledge.get_benchmark_trends(benchmark_name, days)

Step 3: Create Benchmark Tools
# File: src/langchain_tools.py (or new src/benchmark_tools.py)

@tool
def run_code_benchmark(benchmark_name: str, code_path: str) -> str:
    """Run quality benchmarks on generated code.
    
    Runs tests, linting, security analysis, and coverage checks.
    
    Args:
        benchmark_name: Name for this benchmark
        code_path: Path to code to benchmark
        
    Returns:
        Detailed benchmark results with score
    """
    runner = BenchmarkRunner()
    results = runner.run_full_benchmark(benchmark_name, code_path)
    
    return f"""
    Benchmark Results for {benchmark_name}:
    
    Overall Score: {results['overall_score']:.2f}/1.0
    
    Tests: {results['tests']['passed']}/{results['tests']['passed'] + results['tests']['failed']} passed
    Linting: {results['linting']['score']:.1f}/10
    Security: {results['security']['high_severity']} high, {results['security']['medium_severity']} medium issues
    Coverage: {results['coverage']['coverage_percent']:.1f}%
    
    Improvements Needed:
    {runner.generate_improvements(results)}
    """

@tool
def view_benchmark_progress(benchmark_name: str = None, days: int = 30) -> str:
    """View benchmark progress over time.
    
    Args:
        benchmark_name: Optional specific benchmark (shows all if None)
        days: Number of days of history to show
        
    Returns:
        Progress report with trends
    """
    runner = BenchmarkRunner()
    
    if benchmark_name:
        trends = runner.get_benchmark_trends(benchmark_name, days)
        return format_trend_report(benchmark_name, trends)
    else:
        # Show all benchmarks
        all_benchmarks = runner.knowledge.get_all_benchmarks()
        return format_all_benchmarks_report(all_benchmarks)

@tool
def analyze_benchmark_failures(benchmark_name: str) -> str:
    """Get detailed analysis of latest benchmark failures.
    
    Args:
        benchmark_name: Name of benchmark to analyze
        
    Returns:
        Detailed failure analysis with suggestions
    """
    runner = BenchmarkRunner()
    latest = runner.knowledge.get_latest_benchmark_result(benchmark_name)
    
    if not latest:
        return f"No results found for benchmark: {benchmark_name}"
    
    # Parse results and generate detailed analysis
    results = json.loads(latest['errors'])
    
    analysis = f"Analysis of {benchmark_name} (Latest Run):\n\n"
    
    # Analyze test failures
    if results['tests']['failed'] > 0:
        analysis += f"❌ {results['tests']['failed']} test failures:\n"
        # Add details about each failure
    
    # Analyze linting issues
    if results['linting']['issue_count'] > 0:
        analysis += f"\n⚠️  {results['linting']['issue_count']} linting issues:\n"
        # Top issues
    
    # Analyze security
    if results['security']['high_severity'] > 0:
        analysis += f"\n🔒 {results['security']['high_severity']} high-severity security issues:\n"
        # Security details
    
    return analysis

Step 4: Integrate with Agent Workflow
# File: src/langchain_agent.py

def post_code_generation_checks(code_path: str):
    """Run automatic benchmarks after code generation."""
    
    # Check if code generation was successful
    if not os.path.exists(code_path):
        return
    
    print("🔍 Running automatic quality checks...")
    
    runner = BenchmarkRunner()
    results = runner.run_full_benchmark(f"auto_{code_path}", code_path)
    
    if results['overall_score'] < 0.7:
        print(f"⚠️  Code quality score is low: {results['overall_score']:.2f}")
        print(f"Improvements needed:\n{runner.generate_improvements(results)}")
        
        # Add to learning queue if score is low
        memory = BECAMemory()
        memory.add_to_learning_queue(
            'benchmark_failure',
            f"Improve code quality for {code_path}",
            priority='high'
        )

Step 5: Add Knowledge Base Methods
# File: src/knowledge_system.py

class KnowledgeBase:
    
    def create_benchmark(self, name: str, test_suite_path: str = None) -> int:
        """Create a new benchmark."""
        pass
    
    def get_benchmark(self, name: str) -> dict:
        """Get benchmark by name."""
        pass
    
    def save_benchmark_result(
        self, 
        benchmark_id: int, 
        score: float, 
        errors: str,
        improvements: str
    ):
        """Save benchmark result."""
        pass
    
    def get_benchmark_trends(self, benchmark_name: str, days: int) -> list:
        """Get benchmark results over time period."""
        pass
    
    def get_latest_benchmark_result(self, benchmark_name: str) -> dict:
        """Get most recent benchmark result."""
        pass
    
    def get_all_benchmarks(self) -> list:
        """Get all benchmarks with latest scores."""
        pass

Step 6: Create GUI Dashboard
# File: beca_gui.py

with gr.Tab("Quality Benchmarks"):
    with gr.Row():
        benchmark_name = gr.Textbox(label="Benchmark Name")
        code_path = gr.Textbox(label="Code Path")
        run_benchmark_btn = gr.Button("Run Benchmark")
    
    benchmark_results = gr.Markdown()
    
    with gr.Row():
        gr.Markdown("## 📊 Benchmark Trends (Last 30 Days)")
        trends_chart = gr.Plot()
    
    def run_and_display_benchmark(name, path):
        runner = BenchmarkRunner()
        results = runner.run_full_benchmark(name, path)
        
        # Format results
        display = f"""
        # Results: {name}
        
        **Overall Score**: {results['overall_score']:.2%}
        
        ## Breakdown:
        - Tests: {results['tests']['score']:.2%}
        - Linting: {results['linting']['score']:.1f}/10
        - Coverage: {results['coverage']['coverage_percent']:.1f}%
        - Security: {results['security']['high_severity']} high-severity issues
        
        ## Improvements:
        {runner.generate_improvements(results)}
        """
        
        # Generate trend chart
        trends = runner.get_benchmark_trends(name, 30)
        chart = create_trend_chart(trends)
        
        return display, chart
    
    run_benchmark_btn.click(
        run_and_display_benchmark,
        inputs=[benchmark_name, code_path],
        outputs=[benchmark_results, trends_chart]
    )

Testing for Task 2.1:
# Test script: tests/test_benchmarking.py

def test_benchmark_runner():
    """Test benchmark execution."""
    # Create sample code
    # Run benchmark
    # Verify results saved
    pass

def test_benchmark_trends():
    """Test trend tracking."""
    # Run benchmark multiple times
    # Get trends
    # Verify historical data
    pass

def test_auto_benchmark_on_generation():
    """Test automatic benchmarking after code generation."""
    # Generate code
    # Verify benchmark runs automatically
    # Check results stored
    pass

Commit Message:
feat: Add automated code quality benchmarking system

- Created benchmarks and benchmark_results tables
- Implemented BenchmarkRunner with pytest, pylint, coverage, bandit
- Added benchmark tools for running and analyzing results
- Integrated automatic benchmarking into code generation workflow
- Created GUI dashboard for viewing trends
- Includes comprehensive tests

BECA now measures and tracks its own code quality automatically.


Task 2.2: Model Version Management
Goal: Allow easy switching, updating, and rollback of LLM models from GUI or CLI.
Step 1: Create Model Versions Table
# File: src/knowledge_system.py

cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        version TEXT NOT NULL,
        install_date TEXT NOT NULL,
        status TEXT DEFAULT 'inactive',
        performance_notes TEXT,
        UNIQUE(model_name, version)
    )
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_model_status 
    ON model_versions(status)
""")

Step 2: Create Model Manager Module
# File: src/model_manager.py

import subprocess
import json
from datetime import datetime
from typing import List, Dict, Optional

class ModelManager:
    """Manage LLM model versions and switching."""
    
    def __init__(self, knowledge_db_path: str = "beca_knowledge.db"):
        self.knowledge = KnowledgeBase(knowledge_db_path)
        self.ollama_url = "http://34.46.140.140:11434"
    
    def list_available_models(self) -> List[Dict]:
        """List all models available on Ollama server.
        
        Returns:
            List of model dictionaries with metadata
        """
        cmd = f"curl {self.ollama_url}/api/tags"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return []
        
        models = json.loads(result.stdout)
        return models.get('models', [])
    
    def get_active_models(self) -> Dict[str, str]:
        """Get currently active models.
        
        Returns:
            Dictionary mapping model type to model name
        """
        return self.knowledge.get_active_models()
    
    def switch_model(self, model_type: str, model_name: str) -> bool:
        """Switch to a different model.
        
        Args:
            model_type: 'general' or 'coding'
            model_name: Name of model to switch to (e.g., 'llama3.1:8b')
            
        Returns:
            True if successful
        """
        # Verify model exists on Ollama
        available = self.list_available_models()
        if not any(m['name'] == model_name for m in available):
            print(f"❌ Model {model_name} not found on Ollama server")
            return False
        
        # Test model before switching
        if not self.test_model(model_name):
            print(f"❌ Model {model_name} failed test")
            return False
        
        # Deactivate current model
        self.knowledge.deactivate_model(model_type)
        
        # Activate new model
        version = self.get_model_version(model_name)
        self.knowledge.add_model_version(
            model_name,
            version,
            datetime.now().isoformat(),
            'active',
            f"Switched to {model_name} for {model_type}"
        )
        
        # Update agent configuration
        self.update_agent_config(model_type, model_name)
        
        print(f"✅ Switched {model_type} model to {model_name}")
        return True
    
    def test_model(self, model_name: str) -> bool:
        """Test if a model works correctly.
        
        Args:
            model_name: Model to test
            
        Returns:
            True if model responds correctly
        """
        cmd = f"""curl {self.ollama_url}/api/generate -d '{{
            "model": "{model_name}",
            "prompt": "Say hello",
            "stream": false
        }}'"""
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        try:
            response = json.loads(result.stdout)
            return 'response' in response and len(response['response']) > 0
        except:
            return False
    
    def get_model_version(self, model_name: str) -> str:
        """Extract version from model name."""
        # Parse version from name (e.g., 'llama3.1:8b' -> '8b')
        if ':' in model_name:
            return model_name.split(':')[1]
        return 'latest'
    
    def rollback_to_version(self, model_type: str, version_id: int) -> bool:
        """Rollback to a previous model version.
        
        Args:
            model_type: 'general' or 'coding'
            version_id: ID from model_versions table
            
        Returns:
            True if successful
        """
        # Get version details
        version = self.knowledge.get_model_version_by_id(version_id)
        
        if not version:
            print(f"❌ Version ID {version_id} not found")
            return False
        
        # Switch to that model
        return self.switch_model(model_type, version['model_name'])
    
    def check_for_updates(self) -> List[Dict]:
        """Check for new model versions on Ollama.
        
        Returns:
            List of new models available
        """
        available = self.list_available_models()
        current = self.knowledge.get_all_model_versions()
        
        current_names = {f"{m['model_name']}:{m['version']}" for m in current}
        new_models = [m for m in available if m['name'] not in current_names]
        
        return new_models
    
    def update_agent_config(self, model_type: str, model_name: str):
        """Update agent configuration file with new model.
        
        Args:
            model_type: 'general' or 'coding'
            model_name: New model name
        """
        # Update src/langchain_agent.py configuration
        config_file = "src/langchain_agent.py"
        
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Replace model name in config
        if model_type == 'general':
            content = content.replace(
                'model="llama3.1:8b"',
                f'model="{model_name}"'
            )
        elif model_type == 'coding':
            content = content.replace(
                'model="qwen2.5-coder:7b-instruct"',
                f'model="{model_name}"'
            )
        
        with open(config_file, 'w') as f:
            f.write(content)
    
    def get_model_history(self, model_type: str = None) -> List[Dict]:
        """Get model version history.
        
        Args:
            model_type: Optional filter by type
            
        Returns:
            List of model versions with usage history
        """
        return self.knowledge.get_model_history(model_type)

Step 3: Add Knowledge Base Methods
# File: src/knowledge_system.py

class KnowledgeBase:
    
    def add_model_version(
        self,
        model_name: str,
        version: str,
        install_date: str,
        status: str,
        performance_notes: str = None
    ) -> int:
        """Add new model version to database."""
        pass
    
    def get_active_models(self) -> Dict[str, str]:
        """Get currently active models."""
        query = """
            SELECT model_name, version 
            FROM model_versions 
            WHERE status = 'active'
        """
        # Return dict like {'general': 'llama3.1:8b', 'coding': 'qwen2.5-coder:7b'}
        pass
    
    def deactivate_model(self, model_type: str):
        """Set current model as inactive."""
        pass
    
    def get_model_version_by_id(self, version_id: int) -> Dict:
        """Get model version details by ID."""
        pass
    
    def get_all_model_versions(self) -> List[Dict]:
        """Get all model versions ever installed."""
        pass
    
    def get_model_history(self, model_type: str = None) -> List[Dict]:
        """Get version history with usage stats."""
        pass

Step 4: Create Model Management Tools
# File: src/ai_model_tools.py (extend existing file)

@tool
def switch_active_model(model_type: str, model_name: str) -> str:
    """Switch BECA to use a different LLM model.
    
    Args:
        model_type: Either 'general' for conversation or 'coding' for code tasks
        model_name: Model name from Ollama (e.g., 'llama3.1:8b', 'qwen2.5-coder:7b')
        
    Returns:
        Success or error message
    """
    manager = ModelManager()
    
    if manager.switch_model(model_type, model_name):
        return f"✅ Successfully switched {model_type} model to {model_name}"
    else:
        return f"❌ Failed to switch to {model_name}. Check if model exists on Ollama."

@tool
def rollback_model(model_type: str, version_id: int) -> str:
    """Rollback to a previous model version.
    
    Args:
        model_type: 'general' or 'coding'
        version_id: ID from model version history
        
    Returns:
        Success or error message
    """
    manager = ModelManager()
    
    if manager.rollback_to_version(model_type, version_id):
        return f"✅ Successfully rolled back {model_type} model"
    else:
        return f"❌ Failed to rollback. Check version ID."

@tool
def check_model_updates() -> str:
    """Check for new model versions available on Ollama.
    
    Returns:
        List of new models available
    """
    manager = ModelManager()
    new_models = manager.check_for_updates()
    
    if not new_models:
        return "No new models available. You're up to date!"
    
    result = "🆕 New models available:\n\n"
    for model in new_models:
        result += f"- {model['name']} (size: {model['size']})\n"
    
    return result

@tool
def view_model_history(model_type: str = None) -> str:
    """View history of models used.
    
    Args:
        model_type: Optional filter ('general' or 'coding')
        
    Returns:
        Formatted model history with performance notes
    """
    manager = ModelManager()
    history = manager.get_model_history(model_type)
    
    result = "📚 Model Version History:\n\n"
    for entry in history:
        status_icon = "✅" if entry['status'] == 'active' else "⏸️"
        result += f"{status_icon} {entry['model_name']}:{entry['version']}\n"
        result += f"   Installed: {entry['install_date']}\n"
        if entry['performance_notes']:
            result += f"   Notes: {entry['performance_notes']}\n"
        result += "\n"
    
    return result

Step 5: Add GUI Controls
# File: beca_gui.py

with gr.Tab("Model Settings"):
    with gr.Row():
        with gr.Column():
            gr.Markdown("## General Model (Conversation)")
            general_model = gr.Dropdown(
                label="Select Model",
                choices=[],
                interactive=True
            )
            general_switch_btn = gr.Button("Switch General Model")
            general_status = gr.Markdown()
            
        with gr.Column():
            gr.Markdown("## Coding Model (Code Generation)")
            coding_model = gr.Dropdown(
                label="Select Model",
                choices=[],
                interactive=True
            )
            coding_switch_btn = gr.Button("Switch Coding Model")
            coding_status = gr.Markdown()
    
    with gr.Row():
        refresh_models_btn = gr.Button("🔄 Refresh Available Models")
        check_updates_btn = gr.Button("🆕 Check for Updates")
    
    gr.Markdown("## Model History")
    model_history = gr.Markdown()
    
    def load_available_models():
        """Load models from Ollama."""
        manager = ModelManager()
        models = manager.list_available_models()
        model_names = [m['name'] for m in models]
        return model_names, model_names
    
    def switch_general(model_name):
        """Switch general model."""
        manager = ModelManager()
        success = manager.switch_model('general', model_name)
        if success:
            return f"✅ Switched to {model_name}"
        return f"❌ Failed to switch"
    
    def switch_coding(model_name):
        """Switch coding model."""
        manager = ModelManager()
        success = manager.switch_model('coding', model_name)
        if success:
            return f"✅ Switched to {model_name}"
        return f"❌ Failed to switch"
    
    def display_history():
        """Display model history."""
        manager = ModelManager()
        history = manager.get_model_history()
        
        result = ""
        for entry in history:
            status_icon = "✅" if entry['status'] == 'active' else "⏸️"
            result += f"{status_icon} **{entry['model_name']}:{entry['version']}**\n"
            result += f"- Installed: {entry['install_date']}\n"
            if entry['performance_notes']:
                result += f"- Notes: {entry['performance_notes']}\n"
            result += "\n"
        
        return result
    
    # Wire up buttons
    refresh_models_btn.click(
        load_available_models,
        outputs=[general_model, coding_model]
    )
    
    general_switch_btn.click(
        switch_general,
        inputs=[general_model],
        outputs=[general_status]
    )
    
    coding_switch_btn.click(
        switch_coding,
        inputs=[coding_model],
        outputs=[coding_status]
    )
    
    # Load on startup
    demo.load(load_available_models, outputs=[general_model, coding_model])
    demo.load(display_history, outputs=[model_history])

Testing for Task 2.2:
# Test script: tests/test_model_management.py

def test_list_models():
    """Test listing available models."""
    manager = ModelManager()
    models = manager.list_available_models()
    assert len(models) > 0

def test_switch_model():
    """Test switching models."""
    manager = ModelManager()
    # Switch to different model
    # Verify config updated
    # Switch back
    pass

def test_rollback():
    """Test rolling back to previous version."""
    # Switch models a few times
    # Rollback to earlier version
    # Verify correct model active
    pass

Commit Message:
feat: Add model version management system

- Created model_versions table for tracking
- Implemented ModelManager with switch/rollback functionality
- Added model management tools (switch, rollback, updates)
- Created GUI for model selection and history
- Automatic model testing before switching
- Includes comprehensive tests

Easy model switching and rollback now available in GUI and via tools.


📋 Phase 3: Reliability and Security (Week 5-6)
Task 3.1: Enhanced Error Recovery System
Goal: Provide automatic fallback strategies, detailed troubleshooting, and interactive problem-solving in GUI.
Implementation Guide:
Follow similar detailed structure as above:
1. Extend error_log table
2. Create ErrorRecovery class
3. Implement fallback chain
4. Add error analysis tools
5. Integrate with agent
6. Create GUI troubleshooting panel
7. Test thoroughly

Task 3.2: Security Scanning for Secrets and Tokens
Goal: Detect and alert about sensitive data before storage or execution.
Implementation Guide:
Follow similar detailed structure as above:
1. Install detect-secrets library
2. Create SecurityScanner class
3. Create security_alerts table
4. Hook into file operations
5. Add scanning tools
6. Create GUI security panel
7. Test with dummy secrets


📋 Phase 4: Mobile Control and Monitoring (Week 7-8)
Task 4.1: Mobile-Friendly GUI
Task 4.2: Remote Instance Control API

📋 Phase 5: Smart Permissioning and Rate-Limiting (Week 9)
Task 5.1: Minimal Permissioning for High-Risk Operations
Task 5.2: Rate-Limiting for Costly Operations

📋 Phase 6: Optional Resource Analytics (Week 10)
Task 6.1: In-GUI Resource Monitoring Dashboard

🎯 After Each Task:
Run Tests: pytest tests/test_[feature].py -v
Update Documentation: Add docstrings, update readme
Save to Knowledge Base: Use save_code_pattern tool
Git Commit: Make atomic commit with clear message
Verify GUI: Check all UI components work
Update Learning Dashboard: Run auto_extract_lessons

📝 Implementation Notes for BECA:
How to Execute This Plan:
Start with Phase 1, Task 1.1
Read the entire task before starting
Implement each step sequentially
Test after each step
Don't skip testing - it's critical
Commit after each complete task
Update the readme.md after each phase
Ask for clarification if steps are unclear
Quality Standards:
All code must have docstrings
All functions must have type hints
All features must have tests
All changes must be committed
All features must be documented
Success Criteria:
For each task, success means:
✅ All code runs without errors
✅ All tests pass
✅ Feature works in GUI
✅ Changes committed to git
✅ Knowledge base updated
✅ README updated (if applicable)

🚀 Getting Started:
BECA, begin with:
Read the entire plan
Ask any clarifying questions
Start with Phase 1, Task 1.1, Step 1
Execute each step carefully
Test thoroughly
Commit your work
Move to next step
Remember: Quality over speed. Take time to implement features correctly.
Good luck! You've got this! 🎉

