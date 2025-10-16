"""
BECA Meta-Learning Dashboard
Provides visual and text-based dashboard for tracking BECA's learning progress
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Handle imports whether running from src/ or root directory
try:
    from meta_learning_system import MetaLearningSystem
except ImportError:
    from src.meta_learning_system import MetaLearningSystem


class LearningDashboard:
    """
    Dashboard for visualizing BECA's learning progress
    """
    
    def __init__(self, db_path: str = "beca_memory.db"):
        """Initialize dashboard with meta-learning system"""
        self.ml_system = MetaLearningSystem(db_path)
    
    def generate_dashboard_report(self) -> str:
        """
        Generate comprehensive dashboard report
        
        Returns:
            Formatted dashboard report as string
        """
        data = self.ml_system.get_learning_dashboard_data()
        
        report = []
        report.append("=" * 70)
        report.append("BECA META-LEARNING DASHBOARD")
        report.append("=" * 70)
        report.append("")
        
        # Overview Section
        report.append("📊 OVERVIEW")
        report.append("-" * 70)
        report.append(f"Features Built:        {data['features_built']}")
        report.append(f"Lessons Learned:       {data['lessons_learned']}")
        report.append(f"Templates Created:     {data['templates_created']}")
        report.append(f"Average Quality Score: {data['average_quality']:.2f} / 1.00")
        report.append(f"Scored Features:       {data['scored_features']}")
        report.append("")
        
        # Quality Trend Section
        trend_emoji = {
            'improving': '📈',
            'declining': '📉',
            'stable': '➡️'
        }
        report.append("📈 QUALITY TREND")
        report.append("-" * 70)
        report.append(f"Status: {trend_emoji.get(data['quality_trend'], '➡️')} {data['quality_trend'].upper()}")
        
        if data['quality_trend'] == 'improving':
            report.append("BECA is getting better over time! Recent features show improved quality.")
        elif data['quality_trend'] == 'declining':
            report.append("Quality has decreased recently. Consider reviewing recent lessons.")
        else:
            report.append("Quality is consistent. Maintaining stable performance.")
        report.append("")
        
        # Top Patterns Section
        if data['top_patterns']:
            report.append("🏆 TOP REUSED PATTERNS")
            report.append("-" * 70)
            for i, pattern in enumerate(data['top_patterns'], 1):
                effectiveness_bar = "█" * int(pattern['effectiveness'] * 10)
                report.append(f"{i}. {pattern['title']}")
                report.append(f"   Applied: {pattern['times_applied']} times")
                report.append(f"   Effectiveness: {effectiveness_bar} {pattern['effectiveness']:.1%}")
                report.append("")
        
        # Recent Features Section
        if data['recent_features']:
            report.append("📝 RECENT FEATURES DEVELOPED")
            report.append("-" * 70)
            for feature in data['recent_features']:
                timestamp = datetime.fromisoformat(feature['timestamp'])
                time_ago = self._format_time_ago(timestamp)
                report.append(f"• {feature['feature']} ({time_ago})")
            report.append("")
        
        # Learning Insights
        report.append("💡 LEARNING INSIGHTS")
        report.append("-" * 70)
        
        if data['features_built'] == 0:
            report.append("No features built yet. Start building to begin learning!")
        elif data['lessons_learned'] == 0:
            report.append("Features built but no lessons extracted yet.")
            report.append("Tip: Use extract_patterns_from_session() after completing features.")
        elif data['templates_created'] == 0:
            report.append("Consider creating templates from successful implementations")
            report.append("to speed up future development.")
        else:
            learning_rate = data['lessons_learned'] / max(data['features_built'], 1)
            report.append(f"Learning Rate: {learning_rate:.1f} lessons per feature")
            
            if learning_rate >= 3:
                report.append("Excellent pattern extraction! BECA is learning efficiently.")
            elif learning_rate >= 2:
                report.append("Good learning progress. Keep extracting valuable patterns.")
            else:
                report.append("Consider extracting more detailed lessons from implementations.")
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def _format_time_ago(self, timestamp: datetime) -> str:
        """Format timestamp as 'X time ago'"""
        now = datetime.now(timestamp.tzinfo)
        delta = now - timestamp
        
        if delta.days > 30:
            months = delta.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"
    
    def get_lessons_summary(self, limit: int = 10) -> str:
        """
        Get summary of recent lessons learned
        
        Args:
            limit: Number of lessons to show
            
        Returns:
            Formatted lessons summary
        """
        lessons = self.ml_system.get_relevant_lessons("", limit=limit)
        
        if not lessons:
            return "No lessons learned yet."
        
        summary = []
        summary.append("📚 LESSONS LEARNED")
        summary.append("=" * 70)
        
        for i, lesson in enumerate(lessons, 1):
            summary.append(f"\n{i}. {lesson['lesson_title']}")
            summary.append(f"   Category: {lesson['lesson_category']}")
            summary.append(f"   From: {lesson['feature_tag']}")
            summary.append(f"   {lesson['lesson_content']}")
            summary.append(f"   Applied {lesson['times_applied']} times with {lesson['effectiveness_score']:.1%} effectiveness")
        
        return "\n".join(summary)
    
    def get_templates_summary(self) -> str:
        """
        Get summary of all available templates
        
        Returns:
            Formatted templates summary
        """
        import sqlite3
        
        conn = sqlite3.connect(self.ml_system.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM feature_templates
            ORDER BY success_rate DESC, times_reused DESC
        """)
        
        templates = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not templates:
            return "No templates created yet."
        
        summary = []
        summary.append("📋 FEATURE TEMPLATES")
        summary.append("=" * 70)
        
        for i, template in enumerate(templates, 1):
            summary.append(f"\n{i}. {template['template_name']}")
            summary.append(f"   Type: {template['feature_type']}")
            summary.append(f"   Description: {template['description']}")
            summary.append(f"   Reused: {template['times_reused']} times with {template['success_rate']:.1%} success")
        
        return "\n".join(summary)
    
    def get_quality_history(self, limit: int = 10) -> str:
        """
        Get quality score history
        
        Args:
            limit: Number of recent scores to show
            
        Returns:
            Formatted quality history
        """
        import sqlite3
        
        conn = sqlite3.connect(self.ml_system.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT feature_tag, code_quality_score, test_coverage_score,
                   documentation_score, overall_score, timestamp
            FROM implementation_quality
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        scores = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not scores:
            return "No quality scores recorded yet."
        
        summary = []
        summary.append("📊 QUALITY SCORE HISTORY")
        summary.append("=" * 70)
        summary.append("")
        
        for score in scores:
            timestamp = datetime.fromisoformat(score['timestamp'])
            time_ago = self._format_time_ago(timestamp)
            
            summary.append(f"Feature: {score['feature_tag']} ({time_ago})")
            summary.append(f"  Overall:       {self._score_bar(score['overall_score'])} {score['overall_score']:.2f}")
            summary.append(f"  Code Quality:  {self._score_bar(score['code_quality_score'])} {score['code_quality_score']:.2f}")
            summary.append(f"  Test Coverage: {self._score_bar(score['test_coverage_score'])} {score['test_coverage_score']:.2f}")
            summary.append(f"  Documentation: {self._score_bar(score['documentation_score'])} {score['documentation_score']:.2f}")
            summary.append("")
        
        return "\n".join(summary)
    
    def _score_bar(self, score: float) -> str:
        """Generate visual bar for score"""
        filled = int(score * 10)
        return "█" * filled + "░" * (10 - filled)
    
    def print_full_dashboard(self):
        """Print complete dashboard to console"""
        print(self.generate_dashboard_report())
        print()
        print(self.get_quality_history())
        print()
        print(self.get_lessons_summary())
        print()
        print(self.get_templates_summary())


def view_dashboard(db_path: str = "beca_memory.db"):
    """
    Quick function to view the learning dashboard
    
    Args:
        db_path: Path to BECA memory database
    """
    dashboard = LearningDashboard(db_path)
    dashboard.print_full_dashboard()


if __name__ == "__main__":
    # Test dashboard with sample data
    from meta_learning_system import MetaLearningSystem
    import os
    
    test_db = "test_dashboard.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create sample data
    ml = MetaLearningSystem(test_db)
    
    # Feature 1
    session_id = ml.start_development_session("Feature1_DatabaseMigration")
    ml.log_development_interaction(
        feature_tag="Feature1_DatabaseMigration",
        prompt="Create database migration system",
        response="Implemented migration with version tracking",
        tools_used=["write_file", "execute_command"],
        phase="implementation",
        session_id=session_id
    )
    patterns = ml.extract_patterns_from_session("Feature1_DatabaseMigration", session_id)
    ml.save_lessons_learned("Feature1_DatabaseMigration", patterns)
    ml.score_implementation_quality(
        "Feature1_DatabaseMigration",
        code_quality=0.85,
        test_coverage=0.75,
        documentation=0.90,
        strengths=["Clean code", "Well documented"],
        weaknesses=["Could use more tests"]
    )
    
    # Feature 2
    session_id = ml.start_development_session("Feature2_APIEndpoint")
    ml.log_development_interaction(
        feature_tag="Feature2_APIEndpoint",
        prompt="Create REST API endpoint",
        response="Built endpoint with validation",
        tools_used=["write_file", "execute_command"],
        phase="implementation",
        session_id=session_id
    )
    patterns = ml.extract_patterns_from_session("Feature2_APIEndpoint", session_id)
    ml.save_lessons_learned("Feature2_APIEndpoint", patterns)
    ml.score_implementation_quality(
        "Feature2_APIEndpoint",
        code_quality=0.90,
        test_coverage=0.85,
        documentation=0.88
    )
    
    # Display dashboard
    print("\n" + "=" * 70)
    print("TESTING LEARNING DASHBOARD")
    print("=" * 70 + "\n")
    
    view_dashboard(test_db)
    
    # Cleanup
    os.remove(test_db)
