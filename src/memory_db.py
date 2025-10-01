"""
SQLite-backed memory system for BECA
Stores conversations, preferences, successful patterns, and tool usage
"""
import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import os


class BECAMemory:
    """SQLite-based memory system for BECA agent"""

    def __init__(self, db_path: str = "beca_memory.db"):
        """
        Initialize BECA memory database

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Conversations table - full chat history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                tools_used TEXT,
                success BOOLEAN DEFAULT TRUE
            )
        """)

        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                last_updated TEXT NOT NULL,
                UNIQUE(category, preference_key)
            )
        """)

        # Successful patterns table - remember what worked
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS successful_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT NOT NULL,
                user_request TEXT NOT NULL,
                solution TEXT NOT NULL,
                tools_used TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                reuse_count INTEGER DEFAULT 0
            )
        """)

        # Tool usage statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_used TEXT NOT NULL,
                UNIQUE(tool_name)
            )
        """)

        conn.commit()
        conn.close()

    def save_conversation(
        self,
        user_message: str,
        agent_response: str,
        tools_used: List[str] = None,
        success: bool = True
    ) -> int:
        """
        Save a conversation turn to database

        Args:
            user_message: User's input
            agent_response: Agent's response
            tools_used: List of tools used in this turn
            success: Whether the interaction was successful

        Returns:
            Conversation ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now(timezone.utc).isoformat()
        tools_json = json.dumps(tools_used) if tools_used else None

        cursor.execute("""
            INSERT INTO conversations (timestamp, user_message, agent_response, tools_used, success)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, user_message, agent_response, tools_json, success))

        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return conv_id

    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve recent conversations

        Args:
            limit: Number of recent conversations to retrieve

        Returns:
            List of conversation dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        conversations = []
        for row in rows:
            conv = dict(row)
            if conv['tools_used']:
                conv['tools_used'] = json.loads(conv['tools_used'])
            conversations.append(conv)

        return conversations

    def save_preference(
        self,
        category: str,
        key: str,
        value: str,
        confidence: float = 1.0
    ):
        """
        Save or update a user preference

        Args:
            category: Preference category (e.g., 'framework', 'testing', 'style')
            key: Specific preference key (e.g., 'frontend_framework')
            value: Preference value (e.g., 'React')
            confidence: Confidence level 0.0-1.0
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (category, preference_key, preference_value, confidence, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (category, key, value, confidence, timestamp))

        conn.commit()
        conn.close()

    def get_preference(self, category: str, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user preference

        Args:
            category: Preference category
            key: Preference key

        Returns:
            Preference dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM user_preferences
            WHERE category = ? AND preference_key = ?
        """, (category, key))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_all_preferences(self) -> List[Dict[str, Any]]:
        """Get all user preferences"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_preferences ORDER BY category, preference_key")
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def save_successful_pattern(
        self,
        task_type: str,
        user_request: str,
        solution: str,
        tools_used: List[str]
    ) -> int:
        """
        Save a successful task pattern for future reference

        Args:
            task_type: Type of task (e.g., 'react_app', 'api_endpoint')
            user_request: Original user request
            solution: What worked (steps taken)
            tools_used: Tools that were used

        Returns:
            Pattern ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now(timezone.utc).isoformat()
        tools_json = json.dumps(tools_used)

        cursor.execute("""
            INSERT INTO successful_patterns (task_type, user_request, solution, tools_used, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (task_type, user_request, solution, tools_json, timestamp))

        pattern_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return pattern_id

    def find_similar_patterns(self, task_type: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar successful patterns for a task type

        Args:
            task_type: Type of task to find patterns for
            limit: Maximum patterns to return

        Returns:
            List of pattern dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM successful_patterns
            WHERE task_type = ?
            ORDER BY reuse_count DESC, timestamp DESC
            LIMIT ?
        """, (task_type, limit))

        rows = cursor.fetchall()
        conn.close()

        patterns = []
        for row in rows:
            pattern = dict(row)
            pattern['tools_used'] = json.loads(pattern['tools_used'])
            patterns.append(pattern)

        return patterns

    def increment_pattern_reuse(self, pattern_id: int):
        """Increment reuse count for a pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE successful_patterns
            SET reuse_count = reuse_count + 1
            WHERE id = ?
        """, (pattern_id,))

        conn.commit()
        conn.close()

    def track_tool_usage(self, tool_name: str, success: bool = True):
        """
        Track tool usage statistics

        Args:
            tool_name: Name of the tool used
            success: Whether the tool execution was successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now(timezone.utc).isoformat()

        # Try to update existing record
        cursor.execute("""
            SELECT id FROM tool_usage WHERE tool_name = ?
        """, (tool_name,))

        existing = cursor.fetchone()

        if existing:
            if success:
                cursor.execute("""
                    UPDATE tool_usage
                    SET usage_count = usage_count + 1,
                        success_count = success_count + 1,
                        last_used = ?
                    WHERE tool_name = ?
                """, (timestamp, tool_name))
            else:
                cursor.execute("""
                    UPDATE tool_usage
                    SET usage_count = usage_count + 1,
                        failure_count = failure_count + 1,
                        last_used = ?
                    WHERE tool_name = ?
                """, (timestamp, tool_name))
        else:
            # Create new record
            cursor.execute("""
                INSERT INTO tool_usage (tool_name, usage_count, success_count, failure_count, last_used)
                VALUES (?, 1, ?, ?, ?)
            """, (tool_name, 1 if success else 0, 0 if success else 1, timestamp))

        conn.commit()
        conn.close()

    def get_tool_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all tools"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *,
                   CAST(success_count AS REAL) / usage_count * 100 as success_rate
            FROM tool_usage
            ORDER BY usage_count DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def search_conversations(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search past conversations

        Args:
            search_term: Term to search for in messages
            limit: Max results to return

        Returns:
            List of matching conversations
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        search_pattern = f"%{search_term}%"

        cursor.execute("""
            SELECT * FROM conversations
            WHERE user_message LIKE ? OR agent_response LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (search_pattern, search_pattern, limit))

        rows = cursor.fetchall()
        conn.close()

        conversations = []
        for row in rows:
            conv = dict(row)
            if conv['tools_used']:
                conv['tools_used'] = json.loads(conv['tools_used'])
            conversations.append(conv)

        return conversations

    def clear_all_data(self):
        """Clear all data from database (DANGER!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM conversations")
        cursor.execute("DELETE FROM user_preferences")
        cursor.execute("DELETE FROM successful_patterns")
        cursor.execute("DELETE FROM tool_usage")

        conn.commit()
        conn.close()


# Example usage
if __name__ == "__main__":
    memory = BECAMemory("test_memory.db")

    # Save a conversation
    conv_id = memory.save_conversation(
        "Create a React app",
        "I'll create a React app using create_react_app tool",
        tools_used=["create_react_app"]
    )
    print(f"Saved conversation {conv_id}")

    # Save a preference
    memory.save_preference("framework", "frontend", "React", confidence=0.9)
    print(f"Saved preference: {memory.get_preference('framework', 'frontend')}")

    # Save a successful pattern
    pattern_id = memory.save_successful_pattern(
        task_type="react_app",
        user_request="Create a React todo app",
        solution="Used create_project_from_template with react-vite type",
        tools_used=["create_project_from_template", "write_file"]
    )
    print(f"Saved pattern {pattern_id}")

    # Track tool usage
    memory.track_tool_usage("create_react_app", success=True)
    memory.track_tool_usage("write_file", success=True)

    # Get stats
    print("\nTool Stats:")
    for stat in memory.get_tool_stats():
        print(f"  {stat['tool_name']}: {stat['usage_count']} uses, {stat['success_rate']:.1f}% success")

    # Cleanup test db
    os.remove("test_memory.db")
