"""
Initialize BECA's Knowledge Enhancement System
Run this once to set up the knowledge base and seed initial data
"""
import os
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from knowledge_system import knowledge_base

def initialize_knowledge_system():
    """Initialize the knowledge system with some starter data"""

    print("=" * 60)
    print("🧠 BECA Knowledge Enhancement System Initialization")
    print("=" * 60)

    # The database is already initialized in knowledge_system.py
    # Let's just add some starter knowledge to help BECA

    print("\n✅ Knowledge database initialized: beca_knowledge.db")

    # Add some initial tool knowledge
    print("\n📚 Adding initial tool knowledge...")

    tools = [
        {
            "tool_name": "FastAPI",
            "category": "web-framework",
            "description": "Modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            "installation": "pip install fastapi uvicorn[standard]",
            "usage_examples": "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
            "official_docs_url": "https://fastapi.tiangolo.com/"
        },
        {
            "tool_name": "PyTorch",
            "category": "ml-framework",
            "description": "Open source machine learning framework that accelerates the path from research prototyping to production deployment.",
            "installation": "pip install torch torchvision torchaudio",
            "usage_examples": "import torch\nx = torch.tensor([1, 2, 3])\ny = x * 2",
            "official_docs_url": "https://pytorch.org/docs/stable/index.html"
        },
        {
            "tool_name": "Transformers",
            "category": "ml-library",
            "description": "State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX. Provides APIs and tools to easily download and train pre-trained models.",
            "installation": "pip install transformers",
            "usage_examples": "from transformers import pipeline\nclassifier = pipeline('sentiment-analysis')\nresult = classifier('I love BECA!')",
            "official_docs_url": "https://huggingface.co/docs/transformers"
        },
        {
            "tool_name": "LangChain",
            "category": "ai-framework",
            "description": "Framework for developing applications powered by language models. Enables building context-aware, reasoning applications.",
            "installation": "pip install langchain langchain-core",
            "usage_examples": "from langchain.agents import create_tool_calling_agent\nfrom langchain.tools import tool",
            "official_docs_url": "https://python.langchain.com/docs/get_started/introduction"
        },
        {
            "tool_name": "Ollama",
            "category": "ai-runtime",
            "description": "Get up and running with large language models locally. Run Llama 3, Mistral, CodeLlama, and other models.",
            "installation": "Download from https://ollama.ai",
            "usage_examples": "ollama run llama3.1\nollama pull codellama\nollama create custom-model -f Modelfile",
            "official_docs_url": "https://ollama.ai/docs"
        }
    ]

    for tool in tools:
        knowledge_base.add_tool_knowledge(**tool)
        print(f"   ✓ Added: {tool['tool_name']}")

    # Add some initial AI model knowledge
    print("\n🤖 Adding initial AI model knowledge...")

    models = [
        {
            "model_name": "Llama 3.1",
            "model_type": "LLM",
            "framework": "PyTorch",
            "description": "Meta's open-source large language model with excellent instruction following and tool use capabilities. Available in 8B, 70B, and 405B parameter versions.",
            "training_approach": "Pre-trained on web-scale data, then fine-tuned with supervised learning and RLHF (Reinforcement Learning from Human Feedback).",
            "fine_tuning_methods": "Can be fine-tuned using LoRA, QLoRA for parameter-efficient training. Use transformers Trainer or custom training loops.",
            "use_cases": "Chat, code generation, tool calling, reasoning, general assistance",
            "source_url": "https://llama.meta.com/"
        },
        {
            "model_name": "CodeLlama",
            "model_type": "Code LLM",
            "framework": "PyTorch",
            "description": "Specialized version of Llama 2 fine-tuned for code generation and understanding. Supports multiple programming languages.",
            "training_approach": "Built on Llama 2, further trained on code datasets from GitHub and other sources.",
            "fine_tuning_methods": "LoRA/QLoRA fine-tuning on code datasets. Can specialize for specific languages or frameworks.",
            "use_cases": "Code completion, code generation, code explanation, debugging assistance",
            "source_url": "https://github.com/facebookresearch/codellama"
        },
        {
            "model_name": "BERT",
            "model_type": "Encoder-only",
            "framework": "PyTorch/TensorFlow",
            "description": "Bidirectional Encoder Representations from Transformers. Excellent for understanding and classification tasks.",
            "training_approach": "Pre-trained with masked language modeling and next sentence prediction. Fine-tune on downstream tasks.",
            "fine_tuning_methods": "Add task-specific head (classification, QA, etc.) and fine-tune entire model or use adapter layers.",
            "use_cases": "Text classification, question answering, named entity recognition, sentiment analysis",
            "source_url": "https://github.com/google-research/bert"
        }
    ]

    for model in models:
        knowledge_base.add_ai_model_knowledge(**model)
        print(f"   ✓ Added: {model['model_name']}")

    # Add some initial learning resources
    print("\n📖 Adding initial learning resources...")

    resources = [
        {
            "resource_type": "documentation",
            "title": "Python Type Hints",
            "url": "https://docs.python.org/3/library/typing.html",
            "description": "Official Python documentation on type hints and annotations",
            "topics": ["python", "typing", "best-practices"],
            "difficulty_level": "intermediate",
            "priority": 0.7
        },
        {
            "resource_type": "tutorial",
            "title": "Hugging Face Fine-Tuning Guide",
            "url": "https://huggingface.co/docs/transformers/training",
            "description": "Complete guide to fine-tuning transformer models",
            "topics": ["ai", "ml", "fine-tuning", "transformers"],
            "difficulty_level": "advanced",
            "priority": 0.9
        },
        {
            "resource_type": "documentation",
            "title": "Async Programming in Python",
            "url": "https://docs.python.org/3/library/asyncio.html",
            "description": "Python asyncio documentation for concurrent programming",
            "topics": ["python", "async", "concurrency"],
            "difficulty_level": "intermediate",
            "priority": 0.6
        }
    ]

    for resource in resources:
        knowledge_base.add_learning_resource(**resource)
        print(f"   ✓ Added: {resource['title']}")

    # Add some initial code patterns
    print("\n💻 Adding initial code patterns...")

    patterns = [
        {
            "pattern_name": "async-context-manager",
            "language": "python",
            "description": "Async context manager for resource management in async code",
            "code_snippet": """class AsyncContextManager:
    async def __aenter__(self):
        # Setup code
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code
        await self.disconnect()

# Usage
async with AsyncContextManager() as manager:
    await manager.do_something()""",
            "use_case": "Managing async resources like database connections, API clients",
            "tags": ["async", "context-manager", "resource-management"]
        },
        {
            "pattern_name": "error-handling-with-retry",
            "language": "python",
            "description": "Retry pattern with exponential backoff for handling transient errors",
            "code_snippet": """import asyncio
from typing import Callable, Any

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Any:
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff_factor ** attempt
            await asyncio.sleep(wait_time)""",
            "use_case": "API calls, network requests, database operations",
            "tags": ["error-handling", "retry", "resilience"]
        },
        {
            "pattern_name": "factory-pattern",
            "language": "python",
            "description": "Factory pattern for creating objects based on type",
            "code_snippet": """class ModelFactory:
    _models = {}

    @classmethod
    def register(cls, model_type: str):
        def decorator(model_class):
            cls._models[model_type] = model_class
            return model_class
        return decorator

    @classmethod
    def create(cls, model_type: str, **kwargs):
        model_class = cls._models.get(model_type)
        if not model_class:
            raise ValueError(f"Unknown model type: {model_type}")
        return model_class(**kwargs)

# Usage
@ModelFactory.register('gpt')
class GPTModel:
    def __init__(self, **kwargs):
        pass

model = ModelFactory.create('gpt', temperature=0.7)""",
            "use_case": "Creating different types of models, strategies, or handlers dynamically",
            "tags": ["design-pattern", "factory", "oop"]
        }
    ]

    for pattern in patterns:
        knowledge_base.add_code_pattern(**pattern)
        print(f"   ✓ Added: {pattern['pattern_name']}")

    print("\n" + "=" * 60)
    print("✅ Knowledge system initialized successfully!")
    print("=" * 60)
    print("\n📊 Initial Knowledge Base Stats:")
    print(f"   • 5 development tools")
    print(f"   • 3 AI models")
    print(f"   • 3 learning resources")
    print(f"   • 3 code patterns")
    print("\n🚀 BECA is ready to learn and grow!")
    print("   Use the GUI or CLI to teach BECA more.\n")

    # Create the beca-learning directory structure
    os.makedirs("C:/beca-learning/repos", exist_ok=True)
    os.makedirs("C:/beca-learning/modelfiles", exist_ok=True)
    print("📁 Created learning directories:")
    print("   • C:/beca-learning/repos/ (for cloned repositories)")
    print("   • C:/beca-learning/modelfiles/ (for custom Ollama models)")

    print("\n📚 Next steps:")
    print("   1. Start BECA: python beca_gui.py")
    print("   2. Try: 'Learn from https://fastapi.tiangolo.com/'")
    print("   3. Try: 'Search your knowledge for async patterns'")
    print("   4. Try: 'Show me your learning queue'")
    print("   5. Read: BECA-LEARNING-GUIDE.md for full documentation\n")

if __name__ == "__main__":
    initialize_knowledge_system()
