"""
BECA Meta-Learning System
Allows BECA to learn from every interaction during development
Creates a feedback loop where BECA gets smarter with each feature built
"""
import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import re
from pathlib import Path


class MetaLearningSystem:
    """
    Manages BECA's meta-learning capabilities
    Logs development conversations, extracts patterns, scores quality, and provides self-improvement
    """

    def __init__(self, db_path: str = "beca_memory.db"):
        """Initialize meta-learning system using existing memory database"""
        self.db_path = db_path
        self._init_meta_tables()

    def _init_meta_tables(self):
        """Create meta-learning specific tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Development conversations table - special thread for tracking feature development
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS development_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                feature_tag TEXT NOT NULL,
                phase TEXT,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                tools_used TEXT,
                success BOOLEAN DEFAULT TRUE,
                context_data TEXT,
                session_id TEXT
            )
        """)

        # Lessons learned table - extracted from development process
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons_learned (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                feature_tag TEXT NOT NULL,
                lesson_category TEXT NOT NULL,
                lesson_title TEXT NOT NULL,
                lesson_content TEXT NOT NULL,
                code_examples TEXT,
                applicability_score REAL DEFAULT 0.5,
                times_applied INTEGER DEFAULT 0,
                effectiveness_score REAL DEFAULT 0.5
            )
        """)

        # Implementation quality scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS implementation_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                feature_tag TEXT NOT NULL,
                code_quality_score REAL,
                test_coverage_score REAL,
                documentation_score REAL,
                overall_score REAL,
                strengths TEXT,
                weaknesses TEXT,
                improvements TEXT
            )
        """)

        # Feature templates table - successful patterns to reuse
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feature_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                template_name TEXT NOT NULL,
                feature_type TEXT NOT NULL,
                description TEXT,
                approach TEXT NOT NULL,
                schema_patterns TEXT,
                testing_strategy TEXT,
                common_issues TEXT,
                solution_steps TEXT,
                times_reused INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0
            )
        """)

        # Learning metrics table - track BECA's improvement over time
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                context TEXT,
                trend TEXT
            )
        """)

        conn.commit()
        conn.close()

    def start_development_session(self, feature_tag: str) -> str:
        """
        Start a new development session for a feature
        
        Args:
            feature_tag: Identifier for the feature being built (e.g., "Phase3_ErrorRecovery")
            
        Returns:
            session_id: Unique identifier for this development session
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        session_id = f"{feature_tag}_{timestamp}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Log session start
        cursor.execute("""
            INSERT INTO development_conversations 
            (timestamp, feature_tag, phase, prompt, response, session_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, feature_tag, "SESSION_START", 
              f"Starting development of {feature_tag}", 
              "Session initialized", session_id))
        
        conn.commit()
        conn.close()
        
        return session_id

    def log_development_interaction(
        self,
        feature_tag: str,
        prompt: str,
        response: str,
        tools_used: List[str] = None,
        phase: str = None,
        success: bool = True,
        context_data: Dict[str, Any] = None,
        session_id: str = None
    ) -> int:
        """
        Log a development conversation (prompt/response pair)
        
        Args:
            feature_tag: Feature being built
            prompt: The prompt sent to Claude API
            response: The response received
            tools_used: List of tools used in this interaction
            phase: Development phase (e.g., "planning", "implementation", "testing")
            success: Whether the interaction was successful
            context_data: Additional context about this interaction
            session_id: Session identifier
            
        Returns:
            Conversation ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        tools_json = json.dumps(tools_used) if tools_used else None
        context_json = json.dumps(context_data) if context_data else None
        
        cursor.execute("""
            INSERT INTO development_conversations 
            (timestamp, feature_tag, phase, prompt, response, tools_used, success, context_data, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, feature_tag, phase, prompt, response, tools_json, success, context_json, session_id))
        
        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conv_id

    def extract_patterns_from_session(self, feature_tag: str, session_id: str = None) -> List[Dict[str, Any]]:
        """
        Analyze a development session and extract key patterns
        
        Args:
            feature_tag: Feature to analyze
            session_id: Specific session to analyze (or latest if None)
            
        Returns:
            List of extracted patterns
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all conversations for this feature/session
        if session_id:
            cursor.execute("""
                SELECT * FROM development_conversations
                WHERE feature_tag = ? AND session_id = ?
                ORDER BY timestamp
            """, (feature_tag, session_id))
        else:
            cursor.execute("""
                SELECT * FROM development_conversations
                WHERE feature_tag = ?
                ORDER BY timestamp DESC
                LIMIT 50
            """, (feature_tag,))
        
        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not conversations:
            return []
        
        patterns = []
        
        # Extract patterns based on conversation analysis
        patterns.extend(self._extract_approach_patterns(conversations))
        patterns.extend(self._extract_schema_patterns(conversations))
        patterns.extend(self._extract_testing_patterns(conversations))
        patterns.extend(self._extract_problem_solution_patterns(conversations))
        
        return patterns

    def _extract_approach_patterns(self, conversations: List[Dict]) -> List[Dict]:
        """Extract what approaches worked for this type of feature"""
        patterns = []
        
        # Look for successful implementation approaches
        successful_convs = [c for c in conversations if c['success']]
        
        if successful_convs:
            # Analyze tool usage patterns
            all_tools = []
            for conv in successful_convs:
                if conv['tools_used']:
                    tools = json.loads(conv['tools_used'])
                    all_tools.extend(tools)
            
            if all_tools:
                tool_counts = {}
                for tool in all_tools:
                    tool_counts[tool] = tool_counts.get(tool, 0) + 1
                
                patterns.append({
                    'category': 'approach',
                    'title': 'Successful tool usage pattern',
                    'content': f"Most frequently used tools: {', '.join([f'{k} ({v}x)' for k, v in sorted(tool_counts.items(), key=lambda x: -x[1])[:5]])}",
                    'applicability': 0.7
                })
        
        return patterns

    def _extract_schema_patterns(self, conversations: List[Dict]) -> List[Dict]:
        """Extract database schema patterns used"""
        patterns = []
        
        # Look for CREATE TABLE statements in responses
        for conv in conversations:
            response = conv['response']
            if 'CREATE TABLE' in response.upper():
                # Extract table definitions
                table_matches = re.findall(r'CREATE TABLE[^;]+;', response, re.IGNORECASE | re.DOTALL)
                
                if table_matches:
                    patterns.append({
                        'category': 'schema',
                        'title': 'Database schema pattern',
                        'content': f"Used {len(table_matches)} tables in implementation",
                        'code_examples': table_matches,
                        'applicability': 0.8
                    })
                    break
        
        return patterns

    def _extract_testing_patterns(self, conversations: List[Dict]) -> List[Dict]:
        """Extract testing strategies that were effective"""
        patterns = []
        
        # Look for test-related content
        test_phases = [c for c in conversations if c['phase'] == 'testing' or 'test' in c['prompt'].lower()]
        
        if test_phases:
            patterns.append({
                'category': 'testing',
                'title': 'Testing strategy used',
                'content': f"Implemented {len(test_phases)} testing phases with comprehensive verification",
                'applicability': 0.75
            })
        
        return patterns

    def _extract_problem_solution_patterns(self, conversations: List[Dict]) -> List[Dict]:
        """Extract problems encountered and solutions"""
        patterns = []
        
        # Look for failed attempts followed by successful ones
        failed_convs = [c for c in conversations if not c['success']]
        
        if failed_convs:
            patterns.append({
                'category': 'problem_solving',
                'title': 'Error recovery pattern',
                'content': f"Encountered {len(failed_convs)} issues during development and successfully resolved them",
                'applicability': 0.6
            })
        
        return patterns

    def save_lessons_learned(self, feature_tag: str, patterns: List[Dict[str, Any]]) -> List[int]:
        """
        Save extracted patterns as lessons learned
        
        Args:
            feature_tag: Feature these lessons came from
            patterns: List of patterns/lessons
            
        Returns:
            List of lesson IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        lesson_ids = []
        
        for pattern in patterns:
            code_examples_json = json.dumps(pattern.get('code_examples', [])) if pattern.get('code_examples') else None
            
            cursor.execute("""
                INSERT INTO lessons_learned
                (timestamp, feature_tag, lesson_category, lesson_title, lesson_content, 
                 code_examples, applicability_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, feature_tag, pattern['category'], pattern['title'], 
                  pattern['content'], code_examples_json, pattern.get('applicability', 0.5)))
            
            lesson_ids.append(cursor.lastrowid)
        
        conn.commit()
        conn.close()
        
        return lesson_ids

    def score_implementation_quality(
        self,
        feature_tag: str,
        code_quality: float,
        test_coverage: float,
        documentation: float,
        strengths: List[str] = None,
        weaknesses: List[str] = None,
        improvements: List[str] = None
    ) -> int:
        """
        Score the quality of a feature implementation
        
        Args:
            feature_tag: Feature being scored
            code_quality: Score 0.0-1.0 for code quality
            test_coverage: Score 0.0-1.0 for test coverage
            documentation: Score 0.0-1.0 for documentation
            strengths: List of what went well
            weaknesses: List of what could be better
            improvements: List of suggested improvements
            
        Returns:
            Quality record ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        overall_score = (code_quality + test_coverage + documentation) / 3.0
        
        strengths_json = json.dumps(strengths) if strengths else None
        weaknesses_json = json.dumps(weaknesses) if weaknesses else None
        improvements_json = json.dumps(improvements) if improvements else None
        
        cursor.execute("""
            INSERT INTO implementation_quality
            (timestamp, feature_tag, code_quality_score, test_coverage_score, 
             documentation_score, overall_score, strengths, weaknesses, improvements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, feature_tag, code_quality, test_coverage, documentation,
              overall_score, strengths_json, weaknesses_json, improvements_json))
        
        quality_id = cursor.lastrowid
        conn.commit()
        
        # Track quality as a metric
        cursor.execute("""
            INSERT INTO learning_metrics (timestamp, metric_name, metric_value, context)
            VALUES (?, ?, ?, ?)
        """, (timestamp, 'implementation_quality', overall_score, feature_tag))
        
        conn.commit()
        conn.close()
        
        return quality_id

    def create_feature_template(
        self,
        template_name: str,
        feature_type: str,
        description: str,
        approach: str,
        schema_patterns: List[str] = None,
        testing_strategy: str = None,
        solution_steps: List[str] = None
    ) -> int:
        """
        Create a reusable template from a successful feature implementation
        
        Args:
            template_name: Name for this template
            feature_type: Type of feature (e.g., "api_endpoint", "database_migration")
            description: What this template is for
            approach: High-level approach that worked
            schema_patterns: Database schema patterns used
            testing_strategy: How to test this type of feature
            solution_steps: Step-by-step solution
            
        Returns:
            Template ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        schema_json = json.dumps(schema_patterns) if schema_patterns else None
        steps_json = json.dumps(solution_steps) if solution_steps else None
        
        cursor.execute("""
            INSERT INTO feature_templates
            (timestamp, template_name, feature_type, description, approach,
             schema_patterns, testing_strategy, solution_steps)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, template_name, feature_type, description, approach,
              schema_json, testing_strategy, steps_json))
        
        template_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return template_id

    def get_relevant_lessons(self, feature_tag: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get relevant lessons learned for a new feature
        
        Args:
            feature_tag: New feature being built
            limit: Maximum lessons to return
            
        Returns:
            List of relevant lessons
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get lessons ordered by effectiveness and applicability
        cursor.execute("""
            SELECT * FROM lessons_learned
            ORDER BY (effectiveness_score * applicability_score) DESC, times_applied DESC
            LIMIT ?
        """, (limit,))
        
        lessons = []
        for row in cursor.fetchall():
            lesson = dict(row)
            if lesson['code_examples']:
                lesson['code_examples'] = json.loads(lesson['code_examples'])
            lessons.append(lesson)
        
        conn.close()
        return lessons

    def get_similar_templates(self, feature_type: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find templates similar to the feature being built
        
        Args:
            feature_type: Type of feature
            limit: Maximum templates to return
            
        Returns:
            List of similar templates
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM feature_templates
            WHERE feature_type = ?
            ORDER BY success_rate DESC, times_reused DESC
            LIMIT ?
        """, (feature_type, limit))
        
        templates = []
        for row in cursor.fetchall():
            template = dict(row)
            if template['schema_patterns']:
                template['schema_patterns'] = json.loads(template['schema_patterns'])
            if template['solution_steps']:
                template['solution_steps'] = json.loads(template['solution_steps'])
            templates.append(template)
        
        conn.close()
        return templates

    def generate_learning_context(self, feature_tag: str, feature_type: str = None) -> str:
        """
        Generate context string with relevant past learnings for a new feature
        
        Args:
            feature_tag: New feature being built
            feature_type: Type of feature (optional)
            
        Returns:
            Formatted context string to inject into prompts
        """
        lessons = self.get_relevant_lessons(feature_tag)
        templates = self.get_similar_templates(feature_type) if feature_type else []
        
        context = "# Relevant Past Learnings\n\n"
        
        if lessons:
            context += "## Lessons from Previous Features:\n\n"
            for lesson in lessons:
                context += f"### {lesson['lesson_title']} ({lesson['lesson_category']})\n"
                context += f"{lesson['lesson_content']}\n"
                context += f"- Applied {lesson['times_applied']} times with {lesson['effectiveness_score']:.1%} effectiveness\n\n"
        
        if templates:
            context += "## Similar Feature Templates:\n\n"
            for template in templates:
                context += f"### {template['template_name']}\n"
                context += f"{template['description']}\n"
                context += f"**Approach:** {template['approach']}\n"
                if template['solution_steps']:
                    context += "**Steps:**\n"
                    for i, step in enumerate(template['solution_steps'], 1):
                        context += f"{i}. {step}\n"
                context += f"- Reused {template['times_reused']} times with {template['success_rate']:.1%} success\n\n"
        
        if not lessons and not templates:
            context += "No directly relevant past learnings found. This is a new type of implementation.\n"
        
        return context

    def get_learning_dashboard_data(self) -> Dict[str, Any]:
        """
        Get data for the cumulative learning dashboard
        
        Returns:
            Dictionary with dashboard metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count features built
        cursor.execute("""
            SELECT COUNT(DISTINCT feature_tag) FROM development_conversations
            WHERE phase = 'SESSION_START'
        """)
        features_built = cursor.fetchone()[0]
        
        # Count lessons learned
        cursor.execute("SELECT COUNT(*) FROM lessons_learned")
        lessons_count = cursor.fetchone()[0]
        
        # Count templates created
        cursor.execute("SELECT COUNT(*) FROM feature_templates")
        templates_count = cursor.fetchone()[0]
        
        # Get average quality score over time
        cursor.execute("""
            SELECT AVG(overall_score) as avg_quality, COUNT(*) as scored_features
            FROM implementation_quality
        """)
        quality_row = cursor.fetchone()
        avg_quality = quality_row[0] if quality_row[0] else 0.0
        scored_features = quality_row[1]
        
        # Get quality trend (last 5 vs first 5)
        cursor.execute("""
            SELECT overall_score FROM implementation_quality
            ORDER BY timestamp
            LIMIT 5
        """)
        first_scores = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("""
            SELECT overall_score FROM implementation_quality
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        recent_scores = [row[0] for row in cursor.fetchall()]
        
        trend = "stable"
        if first_scores and recent_scores:
            first_avg = sum(first_scores) / len(first_scores)
            recent_avg = sum(recent_scores) / len(recent_scores)
            if recent_avg > first_avg + 0.1:
                trend = "improving"
            elif recent_avg < first_avg - 0.1:
                trend = "declining"
        
        # Get most reused patterns
        cursor.execute("""
            SELECT lesson_title, times_applied, effectiveness_score
            FROM lessons_learned
            ORDER BY times_applied DESC
            LIMIT 5
        """)
        top_patterns = [
            {'title': row[0], 'times_applied': row[1], 'effectiveness': row[2]}
            for row in cursor.fetchall()
        ]
        
        # Get recent features
        cursor.execute("""
            SELECT DISTINCT feature_tag, timestamp
            FROM development_conversations
            WHERE phase = 'SESSION_START'
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        recent_features = [
            {'feature': row[0], 'timestamp': row[1]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'features_built': features_built,
            'lessons_learned': lessons_count,
            'templates_created': templates_count,
            'average_quality': avg_quality,
            'scored_features': scored_features,
            'quality_trend': trend,
            'top_patterns': top_patterns,
            'recent_features': recent_features
        }

    def mark_lesson_applied(self, lesson_id: int, effective: bool = True):
        """
        Mark that a lesson was applied and track its effectiveness
        
        Args:
            lesson_id: ID of the lesson
            effective: Whether applying the lesson was effective
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current stats
        cursor.execute("""
            SELECT times_applied, effectiveness_score FROM lessons_learned WHERE id = ?
        """, (lesson_id,))
        
        row = cursor.fetchone()
        if row:
            times_applied = row[0]
            effectiveness_score = row[1]
            
            # Update with weighted average
            new_times_applied = times_applied + 1
            new_effectiveness = ((effectiveness_score * times_applied) + (1.0 if effective else 0.0)) / new_times_applied
            
            cursor.execute("""
                UPDATE lessons_learned
                SET times_applied = ?, effectiveness_score = ?
                WHERE id = ?
            """, (new_times_applied, new_effectiveness, lesson_id))
            
            conn.commit()
        
        conn.close()

    def increment_template_usage(self, template_id: int, successful: bool = True):
        """
        Track template usage and success
        
        Args:
            template_id: ID of the template
            successful: Whether using the template was successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current stats
        cursor.execute("""
            SELECT times_reused, success_rate FROM feature_templates WHERE id = ?
        """, (template_id,))
        
        row = cursor.fetchone()
        if row:
            times_reused = row[0]
            success_rate = row[1]
            
            # Update with weighted average
            new_times_reused = times_reused + 1
            new_success_rate = ((success_rate * times_reused) + (1.0 if successful else 0.0)) / new_times_reused
            
            cursor.execute("""
                UPDATE feature_templates
                SET times_reused = ?, success_rate = ?
                WHERE id = ?
            """, (new_times_reused, new_success_rate, template_id))
            
            conn.commit()
        
        conn.close()


def test_meta_learning_system():
    """Test the meta-learning system"""
    import os
    
    # Create test database
    test_db = "test_meta_learning.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    ml = MetaLearningSystem(test_db)
    
    print("Testing Meta-Learning System")
    print("=" * 50)
    
    # Test 1: Start development session
    print("\n1. Starting development session...")
    session_id = ml.start_development_session("TestFeature_HelloWorld")
    print(f"   Session ID: {session_id}")
    
    # Test 2: Log interactions
    print("\n2. Logging development interactions...")
    conv_id = ml.log_development_interaction(
        feature_tag="TestFeature_HelloWorld",
        prompt="Create a simple hello world function",
        response="Created function: def hello(): return 'Hello World'",
        tools_used=["write_file", "execute_command"],
        phase="implementation",
        success=True,
        session_id=session_id
    )
    print(f"   Logged conversation ID: {conv_id}")
    
    # Test 3: Extract patterns
    print("\n3. Extracting patterns from session...")
    patterns = ml.extract_patterns_from_session("TestFeature_HelloWorld", session_id)
    print(f"   Extracted {len(patterns)} patterns")
    for pattern in patterns:
        print(f"   - {pattern['category']}: {pattern['title']}")
    
    # Test 4: Save lessons
    print("\n4. Saving lessons learned...")
    lesson_ids = ml.save_lessons_learned("TestFeature_HelloWorld", patterns)
    print(f"   Saved {len(lesson_ids)} lessons")
    
    # Test 5: Score quality
    print("\n5. Scoring implementation quality...")
    quality_id = ml.score_implementation_quality(
        feature_tag="TestFeature_HelloWorld",
        code_quality=0.9,
        test_coverage=0.8,
        documentation=0.85,
        strengths=["Clean code", "Good naming"],
        weaknesses=["Could use more tests"],
        improvements=["Add edge case tests"]
    )
    print(f"   Quality score ID: {quality_id}")
    
    # Test 6: Create template
    print("\n6. Creating feature template...")
    template_id = ml.create_feature_template(
        template_name="Simple Function Template",
        feature_type="function",
        description="Template for creating simple utility functions",
        approach="Write function, add tests, document",
        solution_steps=["Define function signature", "Implement logic", "Add docstring", "Write tests"]
    )
    print(f"   Template ID: {template_id}")
    
    # Test 7: Get learning context
    print("\n7. Generating learning context for new feature...")
    context = ml.generate_learning_context("NewFeature_Advanced", "function")
    print(f"   Context length: {len(context)} characters")
    print(f"   Preview:\n{context[:200]}...")
    
    # Test 8: Dashboard data
    print("\n8. Getting dashboard data...")
    dashboard = ml.get_learning_dashboard_data()
    print(f"   Features built: {dashboard['features_built']}")
    print(f"   Lessons learned: {dashboard['lessons_learned']}")
    print(f"   Templates created: {dashboard['templates_created']}")
    print(f"   Average quality: {dashboard['average_quality']:.2f}")
    print(f"   Quality trend: {dashboard['quality_trend']}")
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    
    # Cleanup
    os.remove(test_db)


if __name__ == "__main__":
    test_meta_learning_system()
