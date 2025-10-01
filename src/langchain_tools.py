"""
LangChain-compatible tools for BECA
"""
from langchain_core.tools import tool
from typing import Dict, Any
import os
import subprocess
import urllib.request
import urllib.parse
import json


@tool
def create_react_app(app_name: str) -> str:
    """
    Creates a basic React application scaffold with folder structure.

    Args:
        app_name: Name of the React application to create

    Returns:
        Success message with created folder path
    """
    try:
        # Handle case where LLM passes JSON string instead of just app_name
        if app_name.startswith('{'):
            try:
                parsed = json.loads(app_name)
                app_name = parsed.get('app_name', app_name)
            except:
                pass  # If JSON parsing fails, use as-is

        # Clean app_name (remove invalid characters)
        app_name = app_name.strip().replace('"', '').replace("'", '')

        # Create the root folder for the React app
        os.makedirs(app_name, exist_ok=True)

        # Create a 'src' directory inside the root folder
        src_path = os.path.join(app_name, "src")
        os.makedirs(src_path, exist_ok=True)

        # Create a placeholder index.js file
        index_js_path = os.path.join(src_path, "index.js")
        with open(index_js_path, "w") as f:
            f.write("// Placeholder for React app\nimport React from 'react';\n")

        # Create package.json
        package_json_path = os.path.join(app_name, "package.json")
        with open(package_json_path, "w") as f:
            f.write(f'{{\n  "name": "{app_name}",\n  "version": "1.0.0"\n}}\n')

        return f"Successfully created React app scaffold in '{app_name}/' with src/index.js and package.json"
    except Exception as e:
        return f"Error creating React scaffold: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """
    Reads the contents of a file.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents or error message
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return f"File: {file_path}\n\n{content}"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file

    Returns:
        Success message or error
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{file_path}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_files(directory_path: str = ".") -> str:
    """
    Lists files and directories in the specified path.

    Args:
        directory_path: Path to directory to list (default: current directory)

    Returns:
        List of files and directories
    """
    try:
        items = os.listdir(directory_path)
        files = [f for f in items if os.path.isfile(os.path.join(directory_path, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(directory_path, d))]

        result = f"Directory: {directory_path}\n\n"
        if dirs:
            result += "Directories:\n" + "\n".join(f"  📁 {d}" for d in sorted(dirs)) + "\n\n"
        if files:
            result += "Files:\n" + "\n".join(f"  📄 {f}" for f in sorted(files))

        return result if (files or dirs) else f"Directory '{directory_path}' is empty"
    except FileNotFoundError:
        return f"Error: Directory '{directory_path}' not found"
    except Exception as e:
        return f"Error listing directory: {str(e)}"


@tool
def git_status() -> str:
    """
    Shows the current git repository status.

    Returns:
        Git status output or error message
    """
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Git Status:\n\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in PATH"
    except Exception as e:
        return f"Error running git status: {str(e)}"


@tool
def git_diff(file_path: str = "") -> str:
    """
    Shows git diff for changes. If file_path is provided, shows diff for that file only.

    Args:
        file_path: Optional specific file to diff (default: all changes)

    Returns:
        Git diff output or error message
    """
    try:
        cmd = ["git", "diff"]
        if file_path:
            cmd.append(file_path)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if not result.stdout:
            return "No changes detected in git diff"

        return f"Git Diff{' for ' + file_path if file_path else ''}:\n\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in PATH"
    except Exception as e:
        return f"Error running git diff: {str(e)}"


@tool
def git_commit(message: str) -> str:
    """
    Commits all staged changes with the provided message.
    Note: This does NOT stage files. Use git_add first if needed.

    Args:
        message: Commit message

    Returns:
        Success message or error
    """
    try:
        if not message or not message.strip():
            return "Error: Commit message cannot be empty"

        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Git Commit Success:\n\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Git commit error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in PATH"
    except Exception as e:
        return f"Error running git commit: {str(e)}"


@tool
def git_add(file_path: str) -> str:
    """
    Stages a file or directory for commit. Use '.' to stage all changes.

    Args:
        file_path: File, directory, or '.' for all changes

    Returns:
        Success message or error
    """
    try:
        result = subprocess.run(
            ["git", "add", file_path],
            capture_output=True,
            text=True,
            check=True
        )

        target = "all changes" if file_path == "." else file_path
        return f"Successfully staged {target} for commit"
    except subprocess.CalledProcessError as e:
        return f"Git add error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in PATH"
    except Exception as e:
        return f"Error running git add: {str(e)}"


@tool
def git_push() -> str:
    """
    Pushes committed changes to the remote repository.

    Returns:
        Success message or error
    """
    try:
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Git Push Success:\n\n{result.stdout}\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Git push error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in PATH"
    except Exception as e:
        return f"Error running git push: {str(e)}"


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Searches the web using DuckDuckGo and returns results.
    Useful for finding documentation, tutorials, Stack Overflow answers, etc.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Search results with titles, snippets, and URLs
    """
    try:
        # DuckDuckGo Instant Answer API
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        results = []

        # Add abstract if available
        if data.get('AbstractText'):
            results.append(f"📌 Summary:\n{data['AbstractText']}\nSource: {data.get('AbstractURL', 'N/A')}\n")

        # Add related topics
        if data.get('RelatedTopics'):
            results.append("\n🔍 Related Results:")
            count = 0
            for topic in data['RelatedTopics'][:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    text = topic.get('Text', 'N/A')
                    url = topic.get('FirstURL', 'N/A')
                    results.append(f"\n{count + 1}. {text}\n   URL: {url}")
                    count += 1
                    if count >= max_results:
                        break

        if not results:
            return f"No results found for query: '{query}'"

        return f"Search Results for: '{query}'\n\n" + "\n".join(results)

    except urllib.error.URLError as e:
        return f"Network error during web search: {str(e)}"
    except Exception as e:
        return f"Error performing web search: {str(e)}"


@tool
def fetch_url(url: str) -> str:
    """
    Fetches the content of a web page.
    Useful for reading documentation, articles, or web resources.

    Args:
        url: The URL to fetch

    Returns:
        The page content (first 5000 characters) or error message
    """
    try:
        if not url.startswith(('http://', 'https://')):
            return "Error: URL must start with http:// or https://"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')

        # Limit to first 5000 chars to avoid overwhelming the LLM
        if len(content) > 5000:
            content = content[:5000] + "\n\n... (content truncated)"

        return f"Content from {url}:\n\n{content}"

    except urllib.error.HTTPError as e:
        return f"HTTP Error {e.code}: {e.reason} for URL: {url}"
    except urllib.error.URLError as e:
        return f"URL Error: {str(e)} for URL: {url}"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


@tool
def run_python(code: str) -> str:
    """
    Executes Python code in a subprocess and returns the output.
    Useful for testing code snippets, running scripts, or calculations.

    Args:
        code: Python code to execute

    Returns:
        Output from the code execution or error message
    """
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []
        if result.stdout:
            output.append(f"Output:\n{result.stdout}")
        if result.stderr:
            output.append(f"Errors:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Exit code: {result.returncode}")

        return "\n\n".join(output) if output else "Code executed successfully (no output)"

    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out after 30 seconds"
    except FileNotFoundError:
        return "Error: Python is not installed or not in PATH"
    except Exception as e:
        return f"Error running Python code: {str(e)}"


@tool
def run_command(command: str) -> str:
    """
    Executes a shell command and returns the output.
    Useful for running npm, pip, tests, builds, etc.

    Args:
        command: Shell command to execute

    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = []
        output.append(f"Command: {command}")
        if result.stdout:
            output.append(f"Output:\n{result.stdout}")
        if result.stderr:
            output.append(f"Errors:\n{result.stderr}")
        output.append(f"Exit code: {result.returncode}")

        return "\n\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after 120 seconds"
    except Exception as e:
        return f"Error running command: {str(e)}"


@tool
def find_in_files(search_term: str, directory: str = ".", file_pattern: str = "*") -> str:
    """
    Searches for a term in files within a directory.
    Useful for finding function definitions, variable usage, etc.

    Args:
        search_term: Text to search for
        directory: Directory to search in (default: current directory)
        file_pattern: File pattern like "*.py" or "*.js" (default: all files)

    Returns:
        List of files and line numbers where the term was found
    """
    try:
        import fnmatch
        matches = []
        search_count = 0

        for root, dirs, files in os.walk(directory):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]

            for filename in files:
                if fnmatch.fnmatch(filename, file_pattern):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if search_term in line:
                                    matches.append(f"{filepath}:{line_num}: {line.strip()}")
                                    search_count += 1
                                    if search_count >= 50:  # Limit results
                                        break
                    except Exception:
                        continue

                if search_count >= 50:
                    break
            if search_count >= 50:
                break

        if not matches:
            return f"No matches found for '{search_term}' in {directory} (pattern: {file_pattern})"

        result = f"Found '{search_term}' in:\n\n" + "\n".join(matches)
        if search_count >= 50:
            result += "\n\n(Results limited to 50 matches)"
        return result

    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def analyze_code(file_path: str) -> str:
    """
    Performs basic static analysis on a code file.
    Checks for: file size, line count, function/class count, TODO comments.

    Args:
        file_path: Path to the file to analyze

    Returns:
        Analysis report with code metrics
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        total_lines = len(lines)
        non_empty_lines = len([l for l in lines if l.strip()])
        comment_lines = len([l for l in lines if l.strip().startswith(('#', '//', '/*', '*'))])

        # Count functions and classes (simple heuristic)
        functions = len([l for l in lines if 'def ' in l or 'function ' in l])
        classes = len([l for l in lines if 'class ' in l])

        # Find TODOs and FIXMEs
        todos = []
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line or 'HACK' in line:
                todos.append(f"  Line {i}: {line.strip()}")

        # File size
        file_size = os.path.getsize(file_path)
        size_kb = file_size / 1024

        report = f"""Code Analysis: {file_path}

📊 Metrics:
- Total Lines: {total_lines}
- Non-empty Lines: {non_empty_lines}
- Comment Lines: {comment_lines}
- Functions: {functions}
- Classes: {classes}
- File Size: {size_kb:.2f} KB

"""
        if todos:
            report += f"⚠️  TODOs/FIXMEs Found ({len(todos)}):\n" + "\n".join(todos[:10])
            if len(todos) > 10:
                report += f"\n  ... and {len(todos) - 10} more"
        else:
            report += "✅ No TODOs or FIXMEs found"

        return report

    except Exception as e:
        return f"Error analyzing code: {str(e)}"


@tool
def find_bugs(file_path: str) -> str:
    """
    Scans code for common bug patterns and code smells.
    Checks for: syntax errors, common mistakes, security issues.

    Args:
        file_path: Path to the file to check

    Returns:
        List of potential issues found
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        issues = []

        # Python-specific checks
        if file_path.endswith('.py'):
            # Check for syntax errors using compile
            try:
                compile(content, file_path, 'exec')
            except SyntaxError as e:
                issues.append(f"❌ Syntax Error: Line {e.lineno}: {e.msg}")

            # Common Python issues
            for i, line in enumerate(lines, 1):
                if 'import *' in line:
                    issues.append(f"⚠️  Line {i}: Wildcard import (import *) is discouraged")
                if 'eval(' in line or 'exec(' in line:
                    issues.append(f"🔒 Line {i}: Security risk - eval/exec detected")
                if 'password' in line.lower() and '=' in line and '"' in line:
                    issues.append(f"🔒 Line {i}: Possible hardcoded password")

        # JavaScript-specific checks
        if file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            for i, line in enumerate(lines, 1):
                if 'var ' in line:
                    issues.append(f"⚠️  Line {i}: Use 'let' or 'const' instead of 'var'")
                if '==' in line and '===' not in line:
                    issues.append(f"⚠️  Line {i}: Use '===' instead of '=='")
                if 'eval(' in line:
                    issues.append(f"🔒 Line {i}: Security risk - eval() detected")

        # General checks for all files
        for i, line in enumerate(lines, 1):
            if 'console.log' in line or 'print(' in line and 'debug' not in line.lower():
                issues.append(f"🐛 Line {i}: Debug statement left in code")

        if not issues:
            return f"✅ No obvious bugs or issues found in {file_path}"

        return f"Bug Check: {file_path}\n\nFound {len(issues)} potential issue(s):\n\n" + "\n".join(issues[:20])

    except Exception as e:
        return f"Error checking for bugs: {str(e)}"


@tool
def suggest_improvements(file_path: str) -> str:
    """
    Suggests code improvements and refactoring opportunities.
    Checks for: long functions, code duplication, complexity.

    Args:
        file_path: Path to the file to analyze

    Returns:
        List of suggested improvements
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        suggestions = []

        # Check for long lines
        long_lines = [(i+1, len(line)) for i, line in enumerate(lines) if len(line) > 100]
        if long_lines:
            suggestions.append(f"📏 Long Lines: {len(long_lines)} lines exceed 100 characters (consider wrapping)")

        # Check for long functions (simple heuristic)
        in_function = False
        func_start = 0
        func_lines = 0
        for i, line in enumerate(lines, 1):
            if 'def ' in line or 'function ' in line:
                if func_lines > 50:
                    suggestions.append(f"📦 Long Function: Lines {func_start}-{i-1} ({func_lines} lines - consider breaking into smaller functions)")
                in_function = True
                func_start = i
                func_lines = 0
            elif in_function:
                if line.strip() and not line.strip().startswith('#'):
                    func_lines += 1

        # Check for code duplication (very basic)
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith(('#', '//')):
                line_counts[stripped] = line_counts.get(stripped, 0) + 1

        duplicates = {line: count for line, count in line_counts.items() if count > 3 and len(line) > 30}
        if duplicates:
            suggestions.append(f"🔄 Possible Duplication: {len(duplicates)} code patterns repeated multiple times")

        # Check for deeply nested code
        for i, line in enumerate(lines, 1):
            indent_level = (len(line) - len(line.lstrip())) // 4
            if indent_level > 4:
                suggestions.append(f"🌲 Deep Nesting: Line {i} has {indent_level} levels of indentation (consider refactoring)")
                break

        # General suggestions
        if len(lines) > 500:
            suggestions.append(f"📄 Large File: {len(lines)} lines - consider splitting into multiple files")

        if not suggestions:
            return f"✅ Code looks good! No obvious improvements needed for {file_path}"

        return f"Improvement Suggestions: {file_path}\n\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(suggestions[:10]))

    except Exception as e:
        return f"Error generating suggestions: {str(e)}"


@tool
def run_tests(path: str = ".") -> str:
    """
    Runs tests in the specified path.
    Auto-detects test framework (pytest, unittest, jest, npm test).

    Args:
        path: Path to test file or directory (default: current directory)

    Returns:
        Test results or error message
    """
    try:
        # Check if it's a Python project with pytest
        if os.path.exists('pytest.ini') or any(f.startswith('test_') for f in os.listdir('.') if f.endswith('.py')):
            result = subprocess.run(
                ["python", "-m", "pytest", path, "-v"],
                capture_output=True,
                text=True,
                timeout=120
            )
            return f"Pytest Results:\n\n{result.stdout}\n{result.stderr}"

        # Check for Python unittest
        elif path.endswith('.py') or any(f.startswith('test_') for f in os.listdir('.') if f.endswith('.py')):
            result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-s", path],
                capture_output=True,
                text=True,
                timeout=120
            )
            return f"Unittest Results:\n\n{result.stdout}\n{result.stderr}"

        # Check for JavaScript/Node.js tests
        elif os.path.exists('package.json'):
            result = subprocess.run(
                ["npm", "test"],
                capture_output=True,
                text=True,
                timeout=120,
                shell=True
            )
            return f"NPM Test Results:\n\n{result.stdout}\n{result.stderr}"

        else:
            return "No test framework detected. Please specify pytest, unittest, or ensure package.json exists for npm test."

    except subprocess.TimeoutExpired:
        return "Error: Tests timed out after 120 seconds"
    except Exception as e:
        return f"Error running tests: {str(e)}"


@tool
def generate_tests(file_path: str) -> str:
    """
    Generates a basic test template for the specified file.
    Creates test file with boilerplate for functions found.

    Args:
        file_path: Path to the source file to generate tests for

    Returns:
        Path to generated test file or error message
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        # Find functions to test
        functions = []
        for line in lines:
            if file_path.endswith('.py') and 'def ' in line and not line.strip().startswith('#'):
                func_name = line.split('def ')[1].split('(')[0].strip()
                if not func_name.startswith('_'):  # Skip private functions
                    functions.append(func_name)
            elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')) and 'function ' in line:
                func_name = line.split('function ')[1].split('(')[0].strip()
                functions.append(func_name)

        if not functions:
            return f"No testable functions found in {file_path}"

        # Generate test file
        if file_path.endswith('.py'):
            base_name = os.path.basename(file_path).replace('.py', '')
            test_file = f"test_{base_name}.py"

            test_content = f'''"""Tests for {file_path}"""
import unittest
from {base_name} import {', '.join(functions[:5])}


class Test{base_name.title().replace('_', '')}(unittest.TestCase):
'''
            for func in functions[:5]:
                test_content += f'''
    def test_{func}(self):
        """Test {func} function"""
        # TODO: Implement test
        self.fail("Test not implemented")
'''

            test_content += '''

if __name__ == '__main__':
    unittest.main()
'''
        else:
            base_name = os.path.basename(file_path)
            test_file = f"{base_name}.test.js"

            test_content = f'''// Tests for {file_path}
import {{ {', '.join(functions[:5])} }} from './{base_name}';

describe('{base_name}', () => {{
'''
            for func in functions[:5]:
                test_content += f'''
  test('{func} should work correctly', () => {{
    // TODO: Implement test
    expect(true).toBe(false);
  }});
'''
            test_content += '});\n'

        # Write test file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)

        return f"✅ Generated test file: {test_file}\n\nFound {len(functions)} function(s) to test: {', '.join(functions)}\n\nTest templates created. Please implement the test logic."

    except Exception as e:
        return f"Error generating tests: {str(e)}"


@tool
def coverage_report(path: str = ".") -> str:
    """
    Generates test coverage report.
    Requires pytest-cov for Python or nyc for JavaScript.

    Args:
        path: Path to analyze (default: current directory)

    Returns:
        Coverage report or installation instructions
    """
    try:
        # Try Python coverage with pytest-cov
        result = subprocess.run(
            ["python", "-m", "pytest", "--cov", "--cov-report=term-missing"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0 or 'coverage' in result.stdout.lower():
            return f"Coverage Report:\n\n{result.stdout}"
        else:
            return """Coverage tools not found.

For Python: pip install pytest-cov
Then run: pytest --cov --cov-report=term-missing

For JavaScript: npm install --save-dev nyc
Then run: nyc npm test"""

    except FileNotFoundError:
        return "Error: pytest not found. Install with: pip install pytest pytest-cov"
    except subprocess.TimeoutExpired:
        return "Error: Coverage report timed out after 120 seconds"
    except Exception as e:
        return f"Error generating coverage report: {str(e)}"


@tool
def create_project_from_template(template_type: str, project_name: str) -> str:
    """
    Creates a new project from a template using Copier.
    Supports: react-vite, flask-api, nextjs, fastapi, python-cli.

    Args:
        template_type: Type of project (react-vite, flask-api, nextjs, fastapi, python-cli)
        project_name: Name for the new project

    Returns:
        Success message with project path or error
    """
    try:
        # Template URL mappings (using popular Copier templates)
        templates = {
            'react-vite': 'gh:copier-org/copier-templates-extensions',  # Placeholder
            'flask-api': 'https://github.com/copier-org/flask-template',
            'nextjs': 'https://github.com/vercel/next.js/tree/canary/examples/hello-world',
            'fastapi': 'https://github.com/tiangolo/full-stack-fastapi-template',
            'python-cli': 'https://github.com/pawamoy/copier-pdm',
        }

        if template_type not in templates:
            return f"Unknown template type: {template_type}. Available: {', '.join(templates.keys())}"

        # Check if copier is installed
        check_copier = subprocess.run(
            ["copier", "--version"],
            capture_output=True,
            text=True
        )

        if check_copier.returncode != 0:
            return """Copier not installed. Install with:
pip install copier

Then you can use templates like:
- react-vite: React + Vite
- flask-api: Flask REST API
- fastapi: FastAPI backend
- python-cli: Python CLI app"""

        # For now, create basic scaffolds without external templates
        # This avoids dependency on network/external repos
        if template_type == 'react-vite':
            return _create_react_vite_scaffold(project_name)
        elif template_type == 'flask-api':
            return _create_flask_api_scaffold(project_name)
        elif template_type == 'fastapi':
            return _create_fastapi_scaffold(project_name)
        elif template_type == 'python-cli':
            return _create_python_cli_scaffold(project_name)

        return f"Template '{template_type}' not yet implemented. Use create_react_app for React projects."

    except Exception as e:
        return f"Error creating project from template: {str(e)}"


def _create_react_vite_scaffold(project_name: str) -> str:
    """Helper to create React + Vite scaffold"""
    try:
        os.makedirs(project_name, exist_ok=True)
        os.makedirs(f"{project_name}/src", exist_ok=True)

        # package.json
        package_json_content = f'''{{
  "name": "{project_name}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }}
}}'''
        with open(f"{project_name}/package.json", "w") as f:
            f.write(package_json_content)

        # vite.config.js
        with open(f"{project_name}/vite.config.js", "w") as f:
            f.write('''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
''')

        # index.html
        with open(f"{project_name}/index.html", "w") as f:
            f.write(f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''')

        # src/main.jsx
        with open(f"{project_name}/src/main.jsx", "w") as f:
            f.write('''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''')

        # src/App.jsx
        with open(f"{project_name}/src/App.jsx", "w") as f:
            f.write(f'''function App() {{
  return (
    <div>
      <h1>Welcome to {project_name}</h1>
      <p>React + Vite project created by BECA</p>
    </div>
  )
}}

export default App
''')

        return f"✅ Created React + Vite project: {project_name}\n\nNext steps:\n  cd {project_name}\n  npm install\n  npm run dev"

    except Exception as e:
        return f"Error creating React Vite scaffold: {str(e)}"


def _create_flask_api_scaffold(project_name: str) -> str:
    """Helper to create Flask API scaffold"""
    try:
        os.makedirs(project_name, exist_ok=True)

        # app.py
        with open(f"{project_name}/app.py", "w") as f:
            f.write(f'''"""
{project_name} - Flask REST API
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({{"message": "Welcome to {project_name} API", "status": "running"}})


@app.route('/api/health')
def health():
    return jsonify({{"status": "healthy"}})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''')

        # requirements.txt
        with open(f"{project_name}/requirements.txt", "w") as f:
            f.write('flask>=3.0.0\nflask-cors>=4.0.0\n')

        # README.md
        with open(f"{project_name}/README.md", "w") as f:
            f.write(f'''# {project_name}

Flask REST API created by BECA

## Setup
```bash
pip install -r requirements.txt
python app.py
```

API will be available at http://localhost:5000
''')

        return f"✅ Created Flask API project: {project_name}\n\nNext steps:\n  cd {project_name}\n  pip install -r requirements.txt\n  python app.py"

    except Exception as e:
        return f"Error creating Flask API scaffold: {str(e)}"


def _create_fastapi_scaffold(project_name: str) -> str:
    """Helper to create FastAPI scaffold"""
    try:
        os.makedirs(project_name, exist_ok=True)

        # main.py
        with open(f"{project_name}/main.py", "w") as f:
            f.write(f'''"""
{project_name} - FastAPI application
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="{project_name}")


class Item(BaseModel):
    name: str
    description: str = None


@app.get("/")
async def root():
    return {{"message": "Welcome to {project_name} API"}}


@app.get("/health")
async def health():
    return {{"status": "healthy"}}


@app.post("/items/")
async def create_item(item: Item):
    return {{"item": item, "status": "created"}}
''')

        # requirements.txt
        with open(f"{project_name}/requirements.txt", "w") as f:
            f.write('fastapi>=0.109.0\nuvicorn[standard]>=0.27.0\n')

        # README.md
        with open(f"{project_name}/README.md", "w") as f:
            f.write(f'''# {project_name}

FastAPI application created by BECA

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs
''')

        return f"✅ Created FastAPI project: {project_name}\n\nNext steps:\n  cd {project_name}\n  pip install -r requirements.txt\n  uvicorn main:app --reload"

    except Exception as e:
        return f"Error creating FastAPI scaffold: {str(e)}"


def _create_python_cli_scaffold(project_name: str) -> str:
    """Helper to create Python CLI scaffold"""
    try:
        os.makedirs(project_name, exist_ok=True)
        os.makedirs(f"{project_name}/{project_name}", exist_ok=True)

        # cli.py
        with open(f"{project_name}/{project_name}/cli.py", "w") as f:
            f.write(f'''"""
{project_name} CLI
"""
import argparse


def main():
    parser = argparse.ArgumentParser(description="{project_name} command line tool")
    parser.add_argument('command', help='Command to run')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.command == 'hello':
        print(f"Hello from {project_name}!")
    else:
        print(f"Unknown command: {{args.command}}")


if __name__ == '__main__':
    main()
''')

        # __init__.py
        with open(f"{project_name}/{project_name}/__init__.py", "w") as f:
            f.write(f'"""\\n{project_name}\\n"""\n__version__ = "0.1.0"\n')

        # setup.py
        with open(f"{project_name}/setup.py", "w") as f:
            f.write(f'''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(),
    entry_points={{
        'console_scripts': [
            '{project_name}={project_name}.cli:main',
        ],
    }},
)
''')

        return f"✅ Created Python CLI project: {project_name}\n\nNext steps:\n  cd {project_name}\n  pip install -e .\n  {project_name} hello"

    except Exception as e:
        return f"Error creating Python CLI scaffold: {str(e)}"


# Export all tools as a list
# Import memory tools
try:
    from memory_tools import MEMORY_TOOLS
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_TOOLS = []
    MEMORY_AVAILABLE = False
    print("Warning: Memory tools not available")

BECA_TOOLS = [
    create_react_app,
    read_file,
    write_file,
    list_files,
    git_status,
    git_diff,
    git_add,
    git_commit,
    git_push,
    web_search,
    fetch_url,
    run_python,
    run_command,
    find_in_files,
    analyze_code,
    find_bugs,
    suggest_improvements,
    run_tests,
    generate_tests,
    coverage_report,
    create_project_from_template,
] + MEMORY_TOOLS  # Add memory tools if available
