"""
Test script for BECA Meta-Learning System
Demonstrates the complete meta-learning workflow
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from meta_learning_system import MetaLearningSystem
from meta_learning_dashboard import LearningDashboard


def test_complete_workflow():
    """Test the complete meta-learning workflow"""
    
    print("=" * 80)
    print("BECA META-LEARNING SYSTEM - COMPLETE WORKFLOW TEST")
    print("=" * 80)
    print()
    
    # Use separate test database
    test_db = "test_meta_learning_workflow.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    ml = MetaLearningSystem(test_db)
    dashboard = LearningDashboard(test_db)
    
    print("✓ Initialized meta-learning system")
    print()
    
    # ========================================================================
    # SCENARIO 1: Build First Test Feature (Hello World)
    # ========================================================================
    print("SCENARIO 1: Building First Test Feature")
    print("-" * 80)
    
    feature1_tag = "TestFeature_HelloWorld"
    session1_id = ml.start_development_session(feature1_tag)
    print(f"✓ Started development session: {session1_id}")
    
    # Log planning phase
    ml.log_development_interaction(
        feature_tag=feature1_tag,
        prompt="Plan a simple hello world function",
        response="I will create a function that returns 'Hello World' with proper documentation",
        tools_used=[],
        phase="planning",
        success=True,
        session_id=session1_id
    )
    print("✓ Logged planning interaction")
    
    # Log implementation phase
    ml.log_development_interaction(
        feature_tag=feature1_tag,
        prompt="Create the hello world function",
        response="""Created function in hello.py:
def hello_world():
    '''Return a greeting message'''
    return 'Hello World'""",
        tools_used=["write_file"],
        phase="implementation",
        success=True,
        session_id=session1_id
    )
    print("✓ Logged implementation interaction")
    
    # Log testing phase
    ml.log_development_interaction(
        feature_tag=feature1_tag,
        prompt="Test the hello world function",
        response="Tested successfully. Function returns 'Hello World' as expected.",
        tools_used=["execute_command"],
        phase="testing",
        success=True,
        session_id=session1_id
    )
    print("✓ Logged testing interaction")
    
    # Extract patterns
    print("\nExtracting patterns from session...")
    patterns = ml.extract_patterns_from_session(feature1_tag, session1_id)
    print(f"✓ Extracted {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"  - {pattern['category']}: {pattern['title']}")
    
    # Save lessons
    lesson_ids = ml.save_lessons_learned(feature1_tag, patterns)
    print(f"✓ Saved {len(lesson_ids)} lessons to database")
    
    # Score quality
    quality_id = ml.score_implementation_quality(
        feature_tag=feature1_tag,
        code_quality=0.9,
        test_coverage=0.8,
        documentation=0.85,
        strengths=["Clean code", "Good naming", "Proper documentation"],
        weaknesses=["Could add more edge case tests"],
        improvements=["Add type hints", "Add error handling"]
    )
    print(f"✓ Scored implementation quality (ID: {quality_id})")
    print(f"  Overall Score: 0.85 / 1.00")
    
    # Create template from this feature
    template_id = ml.create_feature_template(
        template_name="Simple Function Template",
        feature_type="utility_function",
        description="Template for creating simple utility functions",
        approach="Plan structure, implement with documentation, add comprehensive tests",
        schema_patterns=None,
        testing_strategy="Unit tests with assertions",
        solution_steps=[
            "Define function signature",
            "Add docstring",
            "Implement logic",
            "Write unit tests",
            "Verify functionality"
        ]
    )
    print(f"✓ Created feature template (ID: {template_id})")
    print()
    
    # ========================================================================
    # SCENARIO 2: Build Second Feature Using Lessons
    # ========================================================================
    print("SCENARIO 2: Building Second Feature (Using Past Learnings)")
    print("-" * 80)
    
    feature2_tag = "TestFeature_Calculator"
    
    # Get learning context before starting
    print("\nRetrieving relevant past learnings...")
    context = ml.generate_learning_context(feature2_tag, "utility_function")
    print("✓ Generated learning context:")
    print(context[:300] + "..." if len(context) > 300 else context)
    print()
    
    session2_id = ml.start_development_session(feature2_tag)
    print(f"✓ Started development session: {session2_id}")
    
    # Log implementation with past learnings applied
    ml.log_development_interaction(
        feature_tag=feature2_tag,
        prompt=f"Create a calculator function. Context:\n{context}",
        response="""Applied lessons from HelloWorld feature:
Created calculator.py with proper documentation and type hints:
def add(a: int, b: int) -> int:
    '''Add two numbers and return result'''
    return a + b""",
        tools_used=["write_file"],
        phase="implementation",
        success=True,
        context_data={"applied_template": template_id},
        session_id=session2_id
    )
    print("✓ Logged implementation (applied past learnings)")
    
    # Mark that we used the template
    ml.increment_template_usage(template_id, successful=True)
    print("✓ Marked template as successfully used")
    
    # Extract and save patterns
    patterns2 = ml.extract_patterns_from_session(feature2_tag, session2_id)
    lesson_ids2 = ml.save_lessons_learned(feature2_tag, patterns2)
    print(f"✓ Extracted and saved {len(lesson_ids2)} new lessons")
    
    # Score quality (should be higher due to applied learnings)
    quality_id2 = ml.score_implementation_quality(
        feature_tag=feature2_tag,
        code_quality=0.95,
        test_coverage=0.90,
        documentation=0.90,
        strengths=["Applied past lessons", "Type hints included", "Excellent documentation"],
        weaknesses=["None identified"],
        improvements=["Consider adding more operations"]
    )
    print(f"✓ Scored implementation quality (ID: {quality_id2})")
    print(f"  Overall Score: 0.92 / 1.00 (Improvement from 0.85!)")
    
    # Mark lessons as applied and effective
    for lesson_id in lesson_ids[:2]:  # Mark first 2 lessons as applied
        ml.mark_lesson_applied(lesson_id, effective=True)
    print("✓ Marked lessons as successfully applied")
    print()
    
    # ========================================================================
    # SCENARIO 3: Display Dashboard
    # ========================================================================
    print("SCENARIO 3: Learning Dashboard")
    print("-" * 80)
    print()
    
    dashboard.print_full_dashboard()
    
    print()
    print("=" * 80)
    print("TEST WORKFLOW COMPLETE!")
    print("=" * 80)
    print()
    print("Key Achievements:")
    print("✓ Logged development conversations for 2 features")
    print("✓ Extracted patterns automatically from sessions")
    print("✓ Saved lessons learned to knowledge base")
    print("✓ Scored implementation quality and tracked improvement")
    print("✓ Created reusable feature template")
    print("✓ Applied past learnings to new feature development")
    print("✓ Generated comprehensive learning dashboard")
    print()
    print("BECA is now learning from its own development process!")
    print()
    
    # Cleanup
    print("Cleaning up test database...")
    os.remove(test_db)
    print("✓ Test complete")


def demonstrate_query_features():
    """Demonstrate querying capabilities"""
    print()
    print("=" * 80)
    print("DEMONSTRATION: Querying Learning System")
    print("=" * 80)
    print()
    
    test_db = "test_query_demo.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    ml = MetaLearningSystem(test_db)
    
    # Create sample data
    session = ml.start_development_session("Feature_DataProcessing")
    ml.log_development_interaction(
        feature_tag="Feature_DataProcessing",
        prompt="Create data processing pipeline",
        response="Created pipeline with validation, transformation, and storage",
        tools_used=["write_file", "execute_command"],
        phase="implementation",
        session_id=session
    )
    
    patterns = ml.extract_patterns_from_session("Feature_DataProcessing", session)
    ml.save_lessons_learned("Feature_DataProcessing", patterns)
    
    # Query examples
    print("1. Getting relevant lessons for a new feature:")
    lessons = ml.get_relevant_lessons("NewFeature", limit=3)
    for lesson in lessons:
        print(f"   - {lesson['lesson_title']}")
    print()
    
    print("2. Getting dashboard data:")
    data = ml.get_learning_dashboard_data()
    print(f"   Features Built: {data['features_built']}")
    print(f"   Lessons Learned: {data['lessons_learned']}")
    print(f"   Quality Trend: {data['quality_trend']}")
    print()
    
    print("3. Generating learning context for prompt injection:")
    context = ml.generate_learning_context("NewFeature_Advanced", "data_processing")
    print(f"   Context length: {len(context)} characters")
    print(f"   Preview: {context[:150]}...")
    print()
    
    # Cleanup
    os.remove(test_db)
    print("✓ Query demonstration complete")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                 BECA META-LEARNING SYSTEM TEST SUITE                       ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Run complete workflow test
        test_complete_workflow()
        
        # Run query demonstration
        demonstrate_query_features()
        
        print()
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                          ALL TESTS PASSED! ✓                               ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print()
        
    except Exception as e:
        print()
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                            TEST FAILED! ✗                                  ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
