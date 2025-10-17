"""
Quick Start: BECA Meta-Learning System
Demonstrates the meta-learning system with a simple example
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from meta_learning_system import MetaLearningSystem
from meta_learning_dashboard import view_dashboard


def quick_start_example():
    """Simple example showing meta-learning in action"""
    
    print("\n" + "=" * 70)
    print("BECA META-LEARNING QUICK START")
    print("=" * 70)
    print("\nThis demonstrates BECA learning from its development process.\n")
    
    # Initialize system (uses existing beca_memory.db)
    ml = MetaLearningSystem("beca_memory.db")
    
    print("Step 1: Starting a development session")
    print("-" * 70)
    feature_tag = "QuickStart_Example"
    session_id = ml.start_development_session(feature_tag)
    print(f"✓ Session started: {feature_tag}\n")
    
    print("Step 2: Logging development interactions")
    print("-" * 70)
    
    # Simulate a feature development process
    ml.log_development_interaction(
        feature_tag=feature_tag,
        prompt="Create a simple data validator",
        response="I'll create a validator class with email and phone validation",
        phase="planning",
        session_id=session_id
    )
    print("✓ Logged planning phase")
    
    ml.log_development_interaction(
        feature_tag=feature_tag,
        prompt="Implement the validator",
        response="""Created DataValidator class:
class DataValidator:
    def validate_email(self, email):
        return '@' in email and '.' in email
    def validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()""",
        tools_used=["write_file"],
        phase="implementation",
        session_id=session_id
    )
    print("✓ Logged implementation phase")
    
    ml.log_development_interaction(
        feature_tag=feature_tag,
        prompt="Test the validator",
        response="All tests passed. Validator working correctly.",
        tools_used=["execute_command"],
        phase="testing",
        session_id=session_id
    )
    print("✓ Logged testing phase\n")
    
    print("Step 3: Extracting patterns from the session")
    print("-" * 70)
    patterns = ml.extract_patterns_from_session(feature_tag, session_id)
    print(f"✓ Extracted {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"  • {pattern['category']}: {pattern['title']}")
    print()
    
    print("Step 4: Saving lessons learned")
    print("-" * 70)
    lesson_ids = ml.save_lessons_learned(feature_tag, patterns)
    print(f"✓ Saved {len(lesson_ids)} lessons to knowledge base\n")
    
    print("Step 5: Scoring implementation quality")
    print("-" * 70)
    quality_id = ml.score_implementation_quality(
        feature_tag=feature_tag,
        code_quality=0.88,
        test_coverage=0.85,
        documentation=0.80,
        strengths=["Clear implementation", "Good test coverage"],
        weaknesses=["Could add more validators"],
        improvements=["Add regex for email validation", "Support international phone formats"]
    )
    overall = (0.88 + 0.85 + 0.80) / 3
    print(f"✓ Quality scored: {overall:.2f} / 1.00\n")
    
    print("Step 6: Creating a feature template (optional)")
    print("-" * 70)
    if overall >= 0.8:
        template_id = ml.create_feature_template(
            template_name="Data Validator Pattern",
            feature_type="validation",
            description="Pattern for creating data validation classes",
            approach="Create class with specific validation methods",
            solution_steps=[
                "Define validator class",
                "Implement validation methods",
                "Add comprehensive tests",
                "Document validation rules"
            ]
        )
        print(f"✓ Template created (quality >= 0.8)\n")
    else:
        print("✗ Quality below 0.8, skipping template creation\n")
    
    print("Step 7: Viewing the learning dashboard")
    print("-" * 70)
    print()
    
    # Display dashboard
    view_dashboard("beca_memory.db")
    
    print("\n" + "=" * 70)
    print("QUICK START COMPLETE!")
    print("=" * 70)
    print("\nBECA has learned from this development session!")
    print("\nNext steps:")
    print("  • Build more features to accumulate knowledge")
    print("  • Use generate_learning_context() before new features")
    print("  • Review the dashboard regularly to track improvement")
    print("  • See docs/META-LEARNING-GUIDE.md for full documentation\n")


if __name__ == "__main__":
    try:
        quick_start_example()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
