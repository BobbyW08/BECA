"""
Codebase exploration and pattern extraction tools for BECA
Helps BECA learn from existing codebases and extract useful patterns
"""
from langchain_core.tools import tool
from typing import Dict, List
import os
import json
import subprocess


@tool
def analyze_repository(repo_path: str) -> str:
    """
    Analyze a local repository to understand its structure, patterns, and architecture.
    BECA will extract insights and save them for future reference.

    Args:
        repo_path: Path to the repository to analyze

    Returns:
        Analysis report with insights
    """
    try:
        if not os.path.exists(repo_path):
            return f"Error: Repository path '{repo_path}' does not exist"

        insights = {
            'repo_path': repo_path,
            'languages': {},
            'file_structure': {},
            'key_files': [],
            'dependencies': [],
            'architecture_notes': []
        }

        # Count files by language
        for root, dirs, files in os.walk(repo_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__',
                                                     '.venv', 'venv', 'dist', 'build']]

            for file in files:
                ext = os.path.splitext(file)[1]
                if ext:
                    insights['languages'][ext] = insights['languages'].get(ext, 0) + 1

        # Identify key files
        key_file_names = [
            'package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml',
            'Makefile', 'README.md', 'setup.py', 'pyproject.toml', 'Cargo.toml',
            'go.mod', 'pom.xml', 'build.gradle', '.env.example'
        ]

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file in key_file_names:
                    rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                    insights['key_files'].append(rel_path)

        # Try to detect architecture pattern
        if any('.py' in ext for ext in insights['languages']):
            # Check for common Python frameworks
            for root, dirs, files in os.walk(repo_path):
                if 'manage.py' in files:
                    insights['architecture_notes'].append("Django project detected")
                if 'app.py' in files or 'main.py' in files:
                    insights['architecture_notes'].append("Flask/FastAPI application detected")

        if '.js' in insights['languages'] or '.jsx' in insights['languages']:
            if 'package.json' in str(insights['key_files']):
                insights['architecture_notes'].append("Node.js/JavaScript project")

        # Generate report
        report = f"""📊 Repository Analysis: {repo_path}

📁 File Statistics:
"""
        for ext, count in sorted(insights['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"   {ext}: {count} files\n"

        report += f"\n🔑 Key Files Found ({len(insights['key_files'])}):\n"
        for kf in insights['key_files'][:15]:
            report += f"   • {kf}\n"

        if insights['architecture_notes']:
            report += f"\n🏗️  Architecture Notes:\n"
            for note in insights['architecture_notes']:
                report += f"   • {note}\n"

        report += "\n💡 Use analyze_code_patterns to extract reusable patterns from this repo."

        return report

    except Exception as e:
        return f"Error analyzing repository: {str(e)}"


@tool
def analyze_code_patterns(file_path: str, language: str = None) -> str:
    """
    Analyze a code file to extract reusable patterns and techniques.
    BECA will learn from the implementation details.

    Args:
        file_path: Path to the code file to analyze
        language: Programming language (auto-detected if not provided)

    Returns:
        Extracted patterns and insights
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist"

        # Auto-detect language
        if not language:
            ext = os.path.splitext(file_path)[1]
            lang_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.jsx': 'javascript',
                '.ts': 'typescript',
                '.tsx': 'typescript',
                '.go': 'go',
                '.rs': 'rust',
                '.java': 'java',
                '.cpp': 'cpp',
                '.c': 'c'
            }
            language = lang_map.get(ext, 'unknown')

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        patterns = []

        # Python-specific pattern detection
        if language == 'python':
            # Detect decorators
            decorator_lines = [l for l in lines if l.strip().startswith('@')]
            if decorator_lines:
                patterns.append({
                    'pattern': 'Python Decorators',
                    'usage': 'Function/method decoration',
                    'examples': decorator_lines[:3]
                })

            # Detect context managers
            if 'with ' in content and '__enter__' in content:
                patterns.append({
                    'pattern': 'Context Managers',
                    'usage': 'Resource management',
                    'note': 'Custom context manager implementation found'
                })

            # Detect async/await
            if 'async def' in content or 'await ' in content:
                patterns.append({
                    'pattern': 'Async/Await',
                    'usage': 'Asynchronous programming',
                    'note': 'Asynchronous functions detected'
                })

            # Detect type hints
            if ': str' in content or '-> ' in content:
                patterns.append({
                    'pattern': 'Type Hints',
                    'usage': 'Static type checking',
                    'note': 'Python type annotations used'
                })

        # JavaScript/TypeScript pattern detection
        elif language in ['javascript', 'typescript']:
            # Detect promises
            if 'Promise' in content or '.then(' in content:
                patterns.append({
                    'pattern': 'Promises',
                    'usage': 'Asynchronous operations',
                    'note': 'Promise-based async code'
                })

            # Detect React hooks
            if 'useState' in content or 'useEffect' in content:
                patterns.append({
                    'pattern': 'React Hooks',
                    'usage': 'React state and lifecycle management',
                    'note': 'React functional components with hooks'
                })

            # Detect arrow functions
            if '=>' in content:
                patterns.append({
                    'pattern': 'Arrow Functions',
                    'usage': 'Concise function syntax',
                    'note': 'Modern ES6+ syntax'
                })

        # Generate report
        if not patterns:
            return f"No specific patterns detected in {file_path}. File analyzed but no common patterns found."

        report = f"""🔍 Code Pattern Analysis: {file_path}
Language: {language}

Found {len(patterns)} pattern(s):

"""
        for i, pattern in enumerate(patterns, 1):
            report += f"{i}. {pattern['pattern']}\n"
            report += f"   Use case: {pattern['usage']}\n"
            if 'examples' in pattern:
                report += f"   Examples:\n"
                for ex in pattern['examples']:
                    report += f"      {ex.strip()}\n"
            if 'note' in pattern:
                report += f"   Note: {pattern['note']}\n"
            report += "\n"

        report += "💡 Use save_code_pattern to save useful patterns for future reuse."

        return report

    except Exception as e:
        return f"Error analyzing code patterns: {str(e)}"


@tool
def clone_and_learn(repo_url: str, clone_path: str = None) -> str:
    """
    Clone a GitHub repository and analyze it to learn from the codebase.
    BECA will extract patterns, architecture, and useful techniques.

    Args:
        repo_url: GitHub repository URL
        clone_path: Where to clone (default: C:/beca-learning/repos/)

    Returns:
        Analysis of the cloned repository
    """
    try:
        # Default clone path
        if not clone_path:
            clone_path = "C:/beca-learning/repos/"

        # Extract repo name from URL
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        full_path = os.path.join(clone_path, repo_name)

        # Create directory if needed
        os.makedirs(clone_path, exist_ok=True)

        # Clone the repository
        if os.path.exists(full_path):
            return f"Repository already exists at {full_path}. Use analyze_repository to analyze it."

        result = subprocess.run(
            ['git', 'clone', repo_url, full_path],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return f"Error cloning repository: {result.stderr}"

        # Analyze the cloned repo
        analysis = analyze_repository(full_path)

        return f"""✅ Repository cloned successfully!

📁 Location: {full_path}
🔗 Source: {repo_url}

{analysis}"""

    except subprocess.TimeoutExpired:
        return "Error: Repository cloning timed out (>5 minutes)"
    except Exception as e:
        return f"Error cloning and learning: {str(e)}"


@tool
def extract_function_signatures(file_path: str, language: str = None) -> str:
    """
    Extract all function/method signatures from a code file.
    Useful for understanding APIs and interfaces.

    Args:
        file_path: Path to the code file
        language: Programming language (auto-detected if not provided)

    Returns:
        List of function signatures
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist"

        # Auto-detect language
        if not language:
            ext = os.path.splitext(file_path)[1]
            lang_map = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                       '.go': 'go', '.rs': 'rust', '.java': 'java'}
            language = lang_map.get(ext, 'unknown')

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        signatures = []

        if language == 'python':
            for i, line in enumerate(lines, 1):
                if 'def ' in line and not line.strip().startswith('#'):
                    # Extract function signature
                    sig = line.strip()
                    signatures.append(f"Line {i}: {sig}")

        elif language in ['javascript', 'typescript']:
            for i, line in enumerate(lines, 1):
                if 'function ' in line or '=>' in line:
                    sig = line.strip()
                    if sig and not sig.startswith('//'):
                        signatures.append(f"Line {i}: {sig}")

        if not signatures:
            return f"No function signatures found in {file_path}"

        report = f"""📋 Function Signatures in {file_path}
Language: {language}

Found {len(signatures)} function(s):

"""
        for sig in signatures[:20]:  # Limit to 20
            report += f"   {sig}\n"

        if len(signatures) > 20:
            report += f"\n   ... and {len(signatures) - 20} more"

        return report

    except Exception as e:
        return f"Error extracting signatures: {str(e)}"


# Export codebase exploration tools
CODEBASE_TOOLS = [
    analyze_repository,
    analyze_code_patterns,
    clone_and_learn,
    extract_function_signatures,
]
