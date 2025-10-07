"""
LangChain tools for BECA's knowledge enhancement and self-improvement
"""
from langchain_core.tools import tool
from typing import List, Dict, Optional
import json
import os

from knowledge_system import knowledge_base, WebDocScraper


@tool
def learn_from_documentation(url: str, category: str = "general", tags: str = None) -> str:
    """
    Scrape and learn from a documentation URL. BECA will index this for future reference.
    Use this to learn about new tools, frameworks, or concepts.

    Args:
        url: URL of the documentation page to learn from
        category: Category (e.g., 'python', 'react', 'ai-models', 'fastapi')
        tags: Comma-separated tags for organization (optional)

    Returns:
        Success message with what was learned
    """
    try:
        doc = WebDocScraper.fetch_and_parse(url)

        if 'Failed to fetch' in doc['content']:
            return f"❌ Could not fetch documentation from {url}: {doc['content']}"

        # Parse tags
        tag_list = [t.strip() for t in tags.split(',')] if tags else []

        # Add to knowledge base
        doc_id = knowledge_base.add_documentation(
            source=url.split('/')[2],  # Domain name
            url=url,
            title=doc['title'],
            content=doc['content'],
            category=category,
            tags=tag_list
        )

        preview = doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']

        return f"""✅ Successfully learned from documentation!

📚 Title: {doc['title']}
🔗 URL: {url}
📁 Category: {category}
🏷️  Tags: {', '.join(tag_list) if tag_list else 'None'}

Preview: {preview}

This knowledge has been indexed and I can reference it in future conversations."""

    except Exception as e:
        return f"Error learning from documentation: {str(e)}"


@tool
def save_code_pattern(pattern_name: str, language: str, code_snippet: str,
                     description: str, use_case: str = None, tags: str = None) -> str:
    """
    Save a useful code pattern to BECA's knowledge base for future reuse.
    Use this when you discover patterns that work well.

    Args:
        pattern_name: Name of the pattern (e.g., "async-await-error-handling")
        language: Programming language (e.g., "python", "javascript", "go")
        code_snippet: The actual code
        description: What this pattern does
        use_case: When to use this pattern (optional)
        tags: Comma-separated tags (optional)

    Returns:
        Success message
    """
    try:
        tag_list = [t.strip() for t in tags.split(',')] if tags else []

        pattern_id = knowledge_base.add_code_pattern(
            pattern_name=pattern_name,
            language=language,
            code_snippet=code_snippet,
            description=description,
            use_case=use_case,
            tags=tag_list
        )

        return f"""✅ Code pattern saved!

📝 Pattern: {pattern_name}
💻 Language: {language}
🎯 Use case: {use_case if use_case else 'Not specified'}
🏷️  Tags: {', '.join(tag_list) if tag_list else 'None'}

I can now reference this pattern when building similar solutions."""

    except Exception as e:
        return f"Error saving code pattern: {str(e)}"


@tool
def search_knowledge(query: str, category: str = None, limit: int = 5) -> str:
    """
    Search BECA's knowledge base for relevant information.
    Use this to recall previous learnings, code patterns, or documentation.

    Args:
        query: What to search for
        category: Optional filter ('documentation', 'code_patterns', 'ai_models')
        limit: Maximum results to return (default: 5)

    Returns:
        Search results from knowledge base
    """
    try:
        results = knowledge_base.search_knowledge(query, category, limit)

        if not results:
            return f"No knowledge found for query: '{query}'\n\nConsider using learn_from_documentation to add this knowledge."

        output = [f"🔍 Found {len(results)} result(s) for '{query}':\n"]

        for i, result in enumerate(results, 1):
            output.append(f"\n{i}. [{result['type'].upper()}] {result['title']}")

            if result['type'] == 'documentation':
                output.append(f"   Source: {result['source']}")
                output.append(f"   URL: {result['url']}")
                output.append(f"   Preview: {result['content']}")

            elif result['type'] == 'code_pattern':
                output.append(f"   Language: {result['language']}")
                output.append(f"   Description: {result['description']}")
                output.append(f"   Code:\n{result['code']}")

            elif result['type'] == 'ai_model':
                output.append(f"   Framework: {result['framework']}")
                output.append(f"   Description: {result['description']}")
                if result['training_approach']:
                    output.append(f"   Training: {result['training_approach']}")

        return '\n'.join(output)

    except Exception as e:
        return f"Error searching knowledge: {str(e)}"


@tool
def add_learning_resource(resource_type: str, title: str, url: str,
                         topics: str, difficulty: str = "intermediate",
                         priority: float = 0.5) -> str:
    """
    Add a learning resource to BECA's study queue. BECA will learn from high-priority items.
    Use this to queue up tutorials, courses, or documentation to study.

    Args:
        resource_type: Type of resource ('tutorial', 'documentation', 'video', 'course', 'article')
        title: Title of the resource
        url: URL to the resource
        topics: Comma-separated topics covered
        difficulty: Difficulty level ('beginner', 'intermediate', 'advanced')
        priority: Priority score 0.0-1.0 (higher = more important)

    Returns:
        Success message
    """
    try:
        topic_list = [t.strip() for t in topics.split(',')]

        resource_id = knowledge_base.add_learning_resource(
            resource_type=resource_type,
            title=title,
            url=url,
            topics=topic_list,
            difficulty_level=difficulty,
            priority=float(priority)
        )

        return f"""✅ Learning resource added to study queue!

📖 Title: {title}
🔗 URL: {url}
📚 Type: {resource_type}
🎯 Topics: {', '.join(topic_list)}
📊 Difficulty: {difficulty}
⭐ Priority: {priority}

I will study this when processing my learning queue."""

    except Exception as e:
        return f"Error adding learning resource: {str(e)}"


@tool
def get_learning_queue(limit: int = 10) -> str:
    """
    View BECA's learning queue - what she plans to study next.
    Shows prioritized list of resources to learn from.

    Args:
        limit: Maximum number of items to show (default: 10)

    Returns:
        List of queued learning resources
    """
    try:
        resources = knowledge_base.get_learning_queue(limit=limit)

        if not resources:
            return "📚 Learning queue is empty. Use add_learning_resource to queue up things to learn!"

        output = [f"📚 BECA's Learning Queue (Top {len(resources)} items):\n"]

        for i, res in enumerate(resources, 1):
            output.append(f"{i}. [{res['type'].upper()}] {res['title']}")
            output.append(f"   🔗 {res['url']}")
            output.append(f"   Topics: {', '.join(res['topics'])}")
            output.append(f"   Difficulty: {res['difficulty']} | Priority: {res['priority']:.2f}\n")

        return '\n'.join(output)

    except Exception as e:
        return f"Error getting learning queue: {str(e)}"


@tool
def learn_ai_model_knowledge(model_name: str, model_type: str, framework: str,
                            description: str, training_approach: str = None,
                            fine_tuning_methods: str = None, source_url: str = None) -> str:
    """
    Save knowledge about AI/ML models, training approaches, and fine-tuning techniques.
    Use this to build expertise in working with AI models.

    Args:
        model_name: Name of the model (e.g., "Llama 3.1", "GPT-4", "BERT")
        model_type: Type (e.g., "LLM", "vision", "embedding", "diffusion")
        framework: Framework used (e.g., "PyTorch", "TensorFlow", "JAX", "Transformers")
        description: What the model does and its capabilities
        training_approach: How to train/fine-tune this model (optional)
        fine_tuning_methods: Specific fine-tuning techniques (LoRA, QLoRA, etc.)
        source_url: URL to documentation or paper (optional)

    Returns:
        Success message
    """
    try:
        model_id = knowledge_base.add_ai_model_knowledge(
            model_name=model_name,
            model_type=model_type,
            framework=framework,
            description=description,
            training_approach=training_approach,
            fine_tuning_methods=fine_tuning_methods,
            source_url=source_url
        )

        return f"""✅ AI Model knowledge saved!

🤖 Model: {model_name}
📊 Type: {model_type}
🛠️  Framework: {framework}
📝 Description: {description}
{f'🎓 Training: {training_approach}' if training_approach else ''}
{f'⚙️  Fine-tuning: {fine_tuning_methods}' if fine_tuning_methods else ''}
{f'🔗 Source: {source_url}' if source_url else ''}

This knowledge will help me work with AI models more effectively!"""

    except Exception as e:
        return f"Error saving AI model knowledge: {str(e)}"


@tool
def learn_tool_knowledge(tool_name: str, category: str, description: str,
                        installation: str = None, usage_examples: str = None,
                        official_docs_url: str = None) -> str:
    """
    Save knowledge about development tools, libraries, and frameworks.
    Use this to build expertise in various development tools.

    Args:
        tool_name: Name of the tool (e.g., "Docker", "pytest", "FastAPI")
        category: Category (e.g., "containerization", "testing", "web-framework")
        description: What the tool does
        installation: How to install it (optional)
        usage_examples: Basic usage examples (optional)
        official_docs_url: Link to official documentation (optional)

    Returns:
        Success message
    """
    try:
        tool_id = knowledge_base.add_tool_knowledge(
            tool_name=tool_name,
            category=category,
            description=description,
            installation=installation,
            usage_examples=usage_examples,
            official_docs_url=official_docs_url
        )

        return f"""✅ Tool knowledge saved!

🔧 Tool: {tool_name}
📁 Category: {category}
📝 Description: {description}
{f'💾 Installation: {installation}' if installation else ''}
{f'📖 Docs: {official_docs_url}' if official_docs_url else ''}

I can now better assist with {tool_name}-related tasks!"""

    except Exception as e:
        return f"Error saving tool knowledge: {str(e)}"


@tool
def auto_learn_from_urls(urls: str, category: str = "general") -> str:
    """
    Automatically learn from multiple URLs at once. BECA will scrape and index all.
    Great for batch learning from documentation sites.

    Args:
        urls: Comma-separated list of URLs to learn from
        category: Category for all URLs

    Returns:
        Summary of what was learned
    """
    try:
        url_list = [u.strip() for u in urls.split(',')]
        results = []
        success_count = 0

        for url in url_list:
            doc = WebDocScraper.fetch_and_parse(url)

            if 'Failed to fetch' not in doc['content']:
                knowledge_base.add_documentation(
                    source=url.split('/')[2],
                    url=url,
                    title=doc['title'],
                    content=doc['content'],
                    category=category
                )
                results.append(f"✅ {doc['title']}")
                success_count += 1
            else:
                results.append(f"❌ Failed: {url}")

        summary = f"📚 Batch Learning Complete: {success_count}/{len(url_list)} successful\n\n"
        summary += '\n'.join(results)

        return summary

    except Exception as e:
        return f"Error in batch learning: {str(e)}"


# Export all knowledge tools
KNOWLEDGE_TOOLS = [
    learn_from_documentation,
    save_code_pattern,
    search_knowledge,
    add_learning_resource,
    get_learning_queue,
    learn_ai_model_knowledge,
    learn_tool_knowledge,
    auto_learn_from_urls,
]
