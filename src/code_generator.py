"""
Code Generation Module using qwen2.5-coder
Specialized for high-quality code generation
"""
import sys
from langchain_ollama import ChatOllama
from typing import Optional

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Qwen2.5-Coder configuration
# Using 7B model since we have GPU resources
QWEN_CODER_MODEL = "qwen2.5-coder:7b-instruct"
# Use the same Ollama URL configuration as langchain_agent
import os

def get_ollama_url():
    """Get Ollama URL with same priority as langchain_agent"""
    env_url = os.getenv('OLLAMA_URL')
    if env_url:
        return env_url
    return "http://localhost:11434"

OLLAMA_URL = get_ollama_url()

# Create the specialized code generation LLM
code_llm = ChatOllama(
    model=QWEN_CODER_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.1,  # Lower temperature for more focused code
    num_predict=2048,  # Longer for complete code blocks
    num_ctx=8192,  # Larger context for understanding requirements
)


def generate_code(prompt: str, language: str = None, context: str = None) -> str:
    """
    Generate code using qwen2.5-coder model

    Args:
        prompt: What code to generate
        language: Programming language (python, javascript, go, etc.)
        context: Additional context or requirements

    Returns:
        Generated code
    """

    # Build the prompt for code generation
    system_context = """You are Qwen2.5-Coder, a specialized AI for code generation.
Generate clean, efficient, well-documented code following best practices.
Include comments explaining complex logic.
Follow language-specific conventions and style guides."""

    if language:
        system_context += f"\nGenerate code in {language}."

    if context:
        system_context += f"\n\nContext: {context}"

    full_prompt = f"{system_context}\n\nTask: {prompt}\n\nGenerate the code:"

    try:
        response = code_llm.invoke(full_prompt)

        # Extract content from response
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error generating code: {str(e)}"


def improve_code(code: str, improvement_type: str = "optimize") -> str:
    """
    Improve existing code

    Args:
        code: Code to improve
        improvement_type: Type of improvement (optimize, document, refactor, test)

    Returns:
        Improved code
    """

    improvement_prompts = {
        "optimize": "Optimize this code for better performance and efficiency:",
        "document": "Add comprehensive documentation and comments to this code:",
        "refactor": "Refactor this code following best practices and clean code principles:",
        "test": "Generate unit tests for this code:",
        "debug": "Review this code for potential bugs and fix them:"
    }

    prompt_text = improvement_prompts.get(improvement_type, "Improve this code:")

    full_prompt = f"""{prompt_text}

```
{code}
```

Provide the improved version:"""

    try:
        response = code_llm.invoke(full_prompt)

        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error improving code: {str(e)}"


def explain_code(code: str) -> str:
    """
    Generate explanation for code

    Args:
        code: Code to explain

    Returns:
        Detailed explanation
    """

    prompt = f"""Explain what this code does in detail:

```
{code}
```

Provide a clear explanation including:
1. Overall purpose
2. Key components and how they work
3. Inputs and outputs
4. Any important patterns or techniques used"""

    try:
        response = code_llm.invoke(prompt)

        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error explaining code: {str(e)}"


def complete_code(partial_code: str, context: str = None) -> str:
    """
    Complete partial/incomplete code

    Args:
        partial_code: Incomplete code snippet
        context: What the code should do

    Returns:
        Completed code
    """

    prompt = f"""Complete this code:

```
{partial_code}
```
"""

    if context:
        prompt += f"\nContext: {context}"

    prompt += "\n\nProvide the completed code:"

    try:
        response = code_llm.invoke(prompt)

        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error completing code: {str(e)}"


# Test function
if __name__ == "__main__":
    print("Testing qwen2.5-coder code generation...")
    print("=" * 60)

    # Test 1: Generate a simple function
    print("\nTest 1: Generate Python function")
    code = generate_code(
        "Create a function that calculates fibonacci numbers using memoization",
        language="python"
    )
    print(code)

    print("\n" + "=" * 60)
    print("Code generation module ready!")
