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


# Export all tools as a list
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
]
