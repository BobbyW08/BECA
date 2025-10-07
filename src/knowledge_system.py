"""
BECA Knowledge Enhancement System
Allows BECA to learn, scrape, index, and improve her knowledge autonomously
"""
import os
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import urllib.request
import urllib.parse
from pathlib import Path


class KnowledgeBase:
    """
    Manages BECA's knowledge storage and retrieval
    Uses SQLite for efficient storage and querying
    """

    def __init__(self, db_path: str = "beca_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self._init_database()

    def _init_database(self):
        """Initialize the knowledge database with tables"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Documentation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                usefulness_score REAL DEFAULT 0.5
            )
        """)

        # Code patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                language TEXT NOT NULL,
                description TEXT,
                code_snippet TEXT NOT NULL,
                use_case TEXT,
                tags TEXT,
                source_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                times_used INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0
            )
        """)

        # Learning resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_type TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                topics TEXT,
                difficulty_level TEXT,
                priority REAL DEFAULT 0.5,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        # Tool knowledge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                installation TEXT,
                usage_examples TEXT,
                tips_and_tricks TEXT,
                common_issues TEXT,
                official_docs_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP
            )
        """)

        # AI/ML model knowledge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_model_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                model_type TEXT,
                framework TEXT,
                description TEXT,
                training_approach TEXT,
                fine_tuning_methods TEXT,
                use_cases TEXT,
                code_examples TEXT,
                performance_notes TEXT,
                source_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP
            )
        """)

        # Codebase insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS codebase_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repo_name TEXT NOT NULL,
                repo_url TEXT,
                language TEXT,
                architecture_pattern TEXT,
                key_files TEXT,
                dependencies TEXT,
                insights TEXT,
                lessons_learned TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def add_documentation(self, source: str, url: str, title: str, content: str,
                         category: str = None, tags: List[str] = None) -> int:
        """Add documentation to knowledge base"""
        cursor = self.conn.cursor()
        tags_str = json.dumps(tags) if tags else None

        cursor.execute("""
            INSERT INTO documentation (source, url, title, content, category, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source, url, title, content, category, tags_str))

        self.conn.commit()
        return cursor.lastrowid

    def add_code_pattern(self, pattern_name: str, language: str, code_snippet: str,
                        description: str = None, use_case: str = None,
                        tags: List[str] = None, source_url: str = None) -> int:
        """Add a code pattern to knowledge base"""
        cursor = self.conn.cursor()
        tags_str = json.dumps(tags) if tags else None

        cursor.execute("""
            INSERT INTO code_patterns (pattern_name, language, description, code_snippet,
                                      use_case, tags, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pattern_name, language, description, code_snippet, use_case, tags_str, source_url))

        self.conn.commit()
        return cursor.lastrowid

    def add_learning_resource(self, resource_type: str, title: str, url: str,
                             description: str = None, topics: List[str] = None,
                             difficulty_level: str = 'intermediate', priority: float = 0.5) -> int:
        """Add a learning resource to study queue"""
        cursor = self.conn.cursor()
        topics_str = json.dumps(topics) if topics else None

        cursor.execute("""
            INSERT INTO learning_resources (resource_type, title, url, description,
                                           topics, difficulty_level, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (resource_type, title, url, description, topics_str, difficulty_level, priority))

        self.conn.commit()
        return cursor.lastrowid

    def add_tool_knowledge(self, tool_name: str, category: str, description: str,
                          installation: str = None, usage_examples: str = None,
                          official_docs_url: str = None) -> int:
        """Add knowledge about a development tool"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO tool_knowledge (tool_name, category, description, installation,
                                       usage_examples, official_docs_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tool_name, category, description, installation, usage_examples, official_docs_url))

        self.conn.commit()
        return cursor.lastrowid

    def add_ai_model_knowledge(self, model_name: str, model_type: str, framework: str,
                              description: str, training_approach: str = None,
                              fine_tuning_methods: str = None, use_cases: str = None,
                              code_examples: str = None, source_url: str = None) -> int:
        """Add knowledge about AI/ML models"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO ai_model_knowledge (model_name, model_type, framework, description,
                                           training_approach, fine_tuning_methods, use_cases,
                                           code_examples, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (model_name, model_type, framework, description, training_approach,
              fine_tuning_methods, use_cases, code_examples, source_url))

        self.conn.commit()
        return cursor.lastrowid

    def search_knowledge(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """Search across all knowledge with relevance scoring"""
        cursor = self.conn.cursor()

        results = []

        # Search documentation
        if not category or category == 'documentation':
            cursor.execute("""
                SELECT 'documentation' as type, title, content, source, url, usefulness_score
                FROM documentation
                WHERE content LIKE ? OR title LIKE ?
                ORDER BY usefulness_score DESC, access_count DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', limit))

            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'title': row[1],
                    'content': row[2][:500],  # Truncate for preview
                    'source': row[3],
                    'url': row[4],
                    'score': row[5]
                })

        # Search code patterns
        if not category or category == 'code_patterns':
            cursor.execute("""
                SELECT 'code_pattern' as type, pattern_name, description, code_snippet,
                       language, source_url, success_rate
                FROM code_patterns
                WHERE pattern_name LIKE ? OR description LIKE ? OR code_snippet LIKE ?
                ORDER BY success_rate DESC, times_used DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%', limit))

            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'title': row[1],
                    'description': row[2],
                    'code': row[3][:500],
                    'language': row[4],
                    'url': row[5],
                    'score': row[6]
                })

        # Search AI model knowledge
        if not category or category == 'ai_models':
            cursor.execute("""
                SELECT 'ai_model' as type, model_name, description, framework,
                       training_approach, code_examples, source_url
                FROM ai_model_knowledge
                WHERE model_name LIKE ? OR description LIKE ? OR training_approach LIKE ?
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%', limit))

            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'title': row[1],
                    'description': row[2],
                    'framework': row[3],
                    'training_approach': row[4],
                    'code_examples': row[5][:500] if row[5] else None,
                    'url': row[6]
                })

        return results

    def get_learning_queue(self, limit: int = 10, status: str = 'pending') -> List[Dict]:
        """Get prioritized learning resources"""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT id, resource_type, title, url, description, topics, difficulty_level, priority
            FROM learning_resources
            WHERE status = ?
            ORDER BY priority DESC, created_at ASC
            LIMIT ?
        """, (status, limit))

        resources = []
        for row in cursor.fetchall():
            resources.append({
                'id': row[0],
                'type': row[1],
                'title': row[2],
                'url': row[3],
                'description': row[4],
                'topics': json.loads(row[5]) if row[5] else [],
                'difficulty': row[6],
                'priority': row[7]
            })

        return resources

    def mark_resource_learned(self, resource_id: int):
        """Mark a learning resource as completed"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE learning_resources
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (resource_id,))
        self.conn.commit()

    def update_pattern_usage(self, pattern_id: int, success: bool):
        """Track code pattern usage and success rate"""
        cursor = self.conn.cursor()

        # Get current stats
        cursor.execute("""
            SELECT times_used, success_rate FROM code_patterns WHERE id = ?
        """, (pattern_id,))

        row = cursor.fetchone()
        if row:
            times_used = row[0]
            success_rate = row[1]

            # Update with weighted average
            new_times_used = times_used + 1
            new_success_rate = ((success_rate * times_used) + (1.0 if success else 0.0)) / new_times_used

            cursor.execute("""
                UPDATE code_patterns
                SET times_used = ?, success_rate = ?
                WHERE id = ?
            """, (new_times_used, new_success_rate, pattern_id))

            self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class WebDocScraper:
    """
    Scrapes and indexes web documentation for various tools and frameworks
    """

    @staticmethod
    def fetch_and_parse(url: str) -> Dict[str, str]:
        """Fetch and parse documentation from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8', errors='ignore')

            # Basic HTML cleaning (remove scripts, styles)
            import re
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<[^>]+>', ' ', content)  # Remove HTML tags
            content = re.sub(r'\s+', ' ', content).strip()  # Normalize whitespace

            # Extract title (simple heuristic)
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else url.split('/')[-1]

            return {
                'title': title,
                'content': content[:10000],  # Limit to 10k chars
                'url': url
            }

        except Exception as e:
            return {
                'title': 'Error',
                'content': f'Failed to fetch: {str(e)}',
                'url': url
            }

    @staticmethod
    def scrape_documentation_site(base_url: str, kb: KnowledgeBase,
                                  category: str, max_pages: int = 20) -> int:
        """
        Scrape multiple pages from a documentation site
        Returns number of pages scraped
        """
        # This is a simplified version - could be expanded with proper crawling
        pages_scraped = 0

        doc = WebDocScraper.fetch_and_parse(base_url)
        if doc['content'] and 'Failed to fetch' not in doc['content']:
            kb.add_documentation(
                source=base_url.split('/')[2],  # Extract domain
                url=base_url,
                title=doc['title'],
                content=doc['content'],
                category=category
            )
            pages_scraped += 1

        return pages_scraped


# Initialize global knowledge base
knowledge_base = KnowledgeBase()
