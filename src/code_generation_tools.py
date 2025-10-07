"""
LangChain tools for code generation using qwen2.5-coder
"""
from langchain_core.tools import tool
from code_generator import generate_code, improve_code, explain_code, complete_code


@tool
def generate_code_file(task_description: str, language: str, filename: str = None) -> str:
    """
    Generate complete code file using qwen2.5-coder AI model.
    This model is specialized for high-quality code generation.

    Args:
        task_description: What the code should do
        language: Programming language (python, javascript, go, rust, java, etc.)
        filename: Optional filename to save the code

    Returns:
        Generated code
    """
    try:
        code = generate_code(task_description, language)

        # Save to file if filename provided
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                return f"✅ Code generated and saved to {filename}\n\n{code}"
            except Exception as e:
                return f"Code generated but couldn't save to file: {e}\n\n{code}"

        return f"✅ Code generated:\n\n{code}"

    except Exception as e:
        return f"Error generating code: {str(e)}"


@tool
def optimize_code(code: str) -> str:
    """
    Optimize existing code for better performance using qwen2.5-coder.

    Args:
        code: Code to optimize

    Returns:
        Optimized version of the code
    """
    try:
        optimized = improve_code(code, improvement_type="optimize")
        return f"✅ Code optimized:\n\n{optimized}"
    except Exception as e:
        return f"Error optimizing code: {str(e)}"


@tool
def add_documentation(code: str) -> str:
    """
    Add comprehensive documentation and comments to code using qwen2.5-coder.

    Args:
        code: Code to document

    Returns:
        Code with added documentation
    """
    try:
        documented = improve_code(code, improvement_type="document")
        return f"✅ Documentation added:\n\n{documented}"
    except Exception as e:
        return f"Error adding documentation: {str(e)}"


@tool
def refactor_code(code: str) -> str:
    """
    Refactor code following best practices using qwen2.5-coder.

    Args:
        code: Code to refactor

    Returns:
        Refactored code
    """
    try:
        refactored = improve_code(code, improvement_type="refactor")
        return f"✅ Code refactored:\n\n{refactored}"
    except Exception as e:
        return f"Error refactoring code: {str(e)}"


@tool
def generate_unit_tests(code: str) -> str:
    """
    Generate unit tests for code using qwen2.5-coder.

    Args:
        code: Code to generate tests for

    Returns:
        Unit tests for the code
    """
    try:
        tests = improve_code(code, improvement_type="test")
        return f"✅ Unit tests generated:\n\n{tests}"
    except Exception as e:
        return f"Error generating tests: {str(e)}"


@tool
def debug_code(code: str) -> str:
    """
    Review code for potential bugs and fix them using qwen2.5-coder.

    Args:
        code: Code to debug

    Returns:
        Debugged code with fixes
    """
    try:
        debugged = improve_code(code, improvement_type="debug")
        return f"✅ Code debugged:\n\n{debugged}"
    except Exception as e:
        return f"Error debugging code: {str(e)}"


@tool
def explain_code_snippet(code: str) -> str:
    """
    Get a detailed explanation of what code does using qwen2.5-coder.

    Args:
        code: Code to explain

    Returns:
        Detailed explanation of the code
    """
    try:
        explanation = explain_code(code)
        return f"✅ Code explanation:\n\n{explanation}"
    except Exception as e:
        return f"Error explaining code: {str(e)}"


@tool
def complete_partial_code(partial_code: str, context: str = None) -> str:
    """
    Complete partial or incomplete code using qwen2.5-coder.

    Args:
        partial_code: Incomplete code snippet
        context: What the code should do (optional)

    Returns:
        Completed code
    """
    try:
        completed = complete_code(partial_code, context)
        return f"✅ Code completed:\n\n{completed}"
    except Exception as e:
        return f"Error completing code: {str(e)}"


# Export code generation tools
CODE_GENERATION_TOOLS = [
    generate_code_file,
    optimize_code,
    add_documentation,
    refactor_code,
    generate_unit_tests,
    debug_code,
    explain_code_snippet,
    complete_partial_code,
]
