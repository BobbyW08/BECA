"""
LangChain tools for BECA memory management
"""
from langchain_core.tools import tool
from memory_db import BECAMemory
from typing import List

# Initialize memory instance
memory = BECAMemory()


@tool
def remember_preference(category: str, key: str, value: str) -> str:
    """
    Remember a user preference for future interactions.

    Use this when the user expresses a preference like:
    - "I prefer React over Vue"
    - "Always use TypeScript"
    - "I like pytest for testing"

    Args:
        category: Category of preference (e.g., 'framework', 'language', 'testing', 'style')
        key: Specific preference key (e.g., 'frontend_framework', 'type_checking')
        value: The preferred value (e.g., 'React', 'TypeScript', 'pytest')

    Returns:
        Confirmation message

    Examples:
        remember_preference('framework', 'frontend', 'React')
        remember_preference('language', 'type_system', 'TypeScript')
        remember_preference('testing', 'python_framework', 'pytest')
    """
    try:
        memory.save_preference(category, key, value, confidence=1.0)
        return f"✓ Remembered: {category}/{key} = {value}. I'll use this preference in future projects."
    except Exception as e:
        return f"Error saving preference: {str(e)}"


@tool
def recall_preferences() -> str:
    """
    Recall all stored user preferences.

    Use this to check what preferences the user has saved, so you can
    apply them automatically to new projects.

    Returns:
        Formatted list of all preferences
    """
    try:
        prefs = memory.get_all_preferences()

        if not prefs:
            return "No preferences stored yet. User hasn't specified any preferences."

        result = "📋 Stored User Preferences:\n\n"
        current_category = None

        for pref in prefs:
            if pref['category'] != current_category:
                current_category = pref['category']
                result += f"\n{current_category.upper()}:\n"

            result += f"  • {pref['preference_key']}: {pref['preference_value']}\n"

        return result
    except Exception as e:
        return f"Error recalling preferences: {str(e)}"


@tool
def search_past_conversations(search_term: str) -> str:
    """
    Search through past conversations with the user.

    Use this when the user asks about something you discussed before,
    like "what did we talk about yesterday?" or "how did I solve X last time?"

    Args:
        search_term: Term to search for in conversation history

    Returns:
        Matching conversations
    """
    try:
        conversations = memory.search_conversations(search_term, limit=5)

        if not conversations:
            return f"No past conversations found matching '{search_term}'"

        result = f"🔍 Found {len(conversations)} past conversation(s) about '{search_term}':\n\n"

        for i, conv in enumerate(conversations, 1):
            timestamp = conv['timestamp'].split('T')[0]  # Just the date
            result += f"{i}. {timestamp}\n"
            result += f"   User: {conv['user_message'][:100]}...\n"
            result += f"   You: {conv['agent_response'][:100]}...\n\n"

        return result
    except Exception as e:
        return f"Error searching conversations: {str(e)}"


@tool
def find_similar_solution(task_type: str) -> str:
    """
    Find similar successful solutions from the past.

    Use this when starting a new task that might be similar to something
    done before. Helps you apply successful patterns.

    Args:
        task_type: Type of task (e.g., 'react_app', 'flask_api', 'pytest_setup')

    Returns:
        Similar successful patterns, or message if none found
    """
    try:
        patterns = memory.find_similar_patterns(task_type, limit=3)

        if not patterns:
            return f"No similar patterns found for '{task_type}'. This appears to be a new type of task."

        result = f"💡 Found {len(patterns)} similar successful pattern(s) for '{task_type}':\n\n"

        for i, pattern in enumerate(patterns, 1):
            result += f"{i}. Request: {pattern['user_request']}\n"
            result += f"   Solution: {pattern['solution'][:150]}...\n"
            result += f"   Tools used: {', '.join(pattern['tools_used'])}\n"
            result += f"   Reused: {pattern['reuse_count']} times\n\n"

            # Increment reuse count for the most relevant pattern
            if i == 1:
                memory.increment_pattern_reuse(pattern['id'])

        return result
    except Exception as e:
        return f"Error finding patterns: {str(e)}"


@tool
def view_tool_statistics() -> str:
    """
    View statistics about which tools have been used and their success rates.

    Use this to understand which tools are most reliable or most frequently used.

    Returns:
        Tool usage statistics
    """
    try:
        stats = memory.get_tool_stats()

        if not stats:
            return "No tool usage data yet. Start using tools and they'll be tracked!"

        result = "📊 Tool Usage Statistics:\n\n"

        for stat in stats[:10]:  # Top 10 tools
            success_rate = stat.get('success_rate', 0)
            result += f"• {stat['tool_name']}:\n"
            result += f"  Used: {stat['usage_count']} times\n"
            result += f"  Success rate: {success_rate:.1f}%\n"
            result += f"  Last used: {stat['last_used'].split('T')[0]}\n\n"

        return result
    except Exception as e:
        return f"Error getting tool stats: {str(e)}"


@tool
def save_successful_approach(task_type: str, description: str, tools_used: str) -> str:
    """
    Save a successful approach for a task so it can be reused later.

    Use this after successfully completing a complex task, to remember
    how it was done for future similar requests.

    Args:
        task_type: Type of task (e.g., 'react_app', 'api_setup', 'deployment')
        description: Description of what was done and why it worked
        tools_used: Comma-separated list of tools used (e.g., 'create_react_app,write_file,git_commit')

    Returns:
        Confirmation message
    """
    try:
        tools_list = [t.strip() for t in tools_used.split(',')]

        # Get the recent conversation as context for user_request
        recent = memory.get_recent_conversations(limit=1)
        user_request = recent[0]['user_message'] if recent else "Task completed successfully"

        pattern_id = memory.save_successful_pattern(
            task_type=task_type,
            user_request=user_request,
            solution=description,
            tools_used=tools_list
        )

        return f"✓ Saved successful pattern #{pattern_id} for '{task_type}'. I can reference this approach in the future."
    except Exception as e:
        return f"Error saving pattern: {str(e)}"


# Export memory tools for LangChain agent
MEMORY_TOOLS = [
    remember_preference,
    recall_preferences,
    search_past_conversations,
    find_similar_solution,
    view_tool_statistics,
    save_successful_approach,
]
