"""
LangChain-compatible tools for BECA
"""
from langchain_core.tools import tool
from typing import Dict, Any
import os


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


# Export all tools as a list
BECA_TOOLS = [
    create_react_app,
    read_file,
    write_file,
    list_files,
]
