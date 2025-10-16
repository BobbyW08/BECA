# BECA Meta-Learning System Guide

## Overview

The Meta-Learning System enables BECA to learn from every interaction during the development process, creating a feedback loop where BECA gets progressively smarter with each feature built.

## What It Does

### 1. **Development Conversation Logging**
- Captures every prompt sent to Claude API and response received
- Tags interactions with feature identifiers and development phases
- Stores complete context for future analysis

### 2. **Automatic Pattern Extraction**
- Analyzes completed features to extract successful patterns
- Identifies effective approaches, schema patterns, and testing strategies
- Documents problems encountered and their solutions

### 3. **Quality Scoring**
- Evaluates code quality, test coverage, and documentation
- Tracks improvement trends over time
- Identifies strengths and areas for improvement

### 4. **Template Creation**
- Creates reusable templates from successful implementations
- Tracks template effectiveness and reuse rates
- Provides step-by-step solution patterns

### 5. **Self-Improvement**
- Injects relevant past learnings into new feature development
- Suggests approaches based on similar past work
- Continuously refines understanding of what works

## How to Use

### Basic Workflow

```python
from src.meta_learning_system import MetaLearningSystem

# Initialize the system
ml = MetaLearningSystem("beca_memory.db")

# Start a development session
feature_tag = "Phase3_ErrorRecovery"
session_id = ml.start_development_session(feature_tag)

# Log each interaction during development
ml.log_development_interaction(
    feature_tag=feature_tag,
    prompt="Your prompt here",
    response="Claude's response here",
    tools_used=["write_file", "execute_command"],
    phase="implementation",  # or "planning", "testing", etc.
    success=True,
    session_id=session_id
)

# After feature completion, extract patterns
patterns = ml.extract_patterns_from_session(feature_tag, session_id)

# Save lessons learned
lesson_ids = ml.save_lessons_learned(feature_tag, patterns)

# Score the implementation quality
ml.score_implementation_quality(
    feature_tag=feature_tag,
    code_quality=0.9,      # 0.0 to 1.0
    test_coverage=0.85,    # 0.0 to 1.0
    documentation=0.88,    # 0.0 to 1.0
    strengths=["Clean code", "Good tests"],
    weaknesses=["Could improve error handling"],
    improvements=["Add more edge case tests"]
)

# Create a template if the feature was successful
if overall_quality >= 0.8:
    ml.create_feature_template(
        template_name="Error Recovery Pattern",
        feature_type="error_handling",
        description="Pattern for implementing robust error recovery",
        approach="Try-except with logging and fallback strategies",
        solution_steps=[
            "Identify failure points",
            "Add try-except blocks",
            "Implement logging",
            "Create fallback logic",
            "Test edge cases"
        ]
    )
```

### Before Starting New Features

```python
# Get relevant past learnings
context = ml.generate_learning_context(
    feature_tag="NewFeature_Advanced",
    feature_type="error_handling"
)

# This context string can be injected into your prompts:
prompt = f"""
Build a new error handling feature.

{context}

Requirements:
- Handle network timeouts
- Implement retry logic
- Log all errors
"""
```

### Viewing Progress

```python
from src.meta_learning_dashboard import view_dashboard

# Display comprehensive dashboard
view_dashboard("beca_memory.db")
```

## Dashboard Features

The learning dashboard shows:

- **Features Built**: Total count of features developed
- **Lessons Learned**: Number of patterns extracted
- **Templates Created**: Reusable solution templates
- **Average Quality Score**: Overall implementation quality
- **Quality Trend**: Improving, stable, or declining
- **Top Reused Patterns**: Most effective lessons
- **Recent Features**: Latest development work
- **Quality History**: Detailed scoring over time

## Integration with BECA

### Automatic Logging During Development

Modify BECA's main agent loop to automatically log interactions:

```python
# In your main BECA agent code
from src.meta_learning_system import MetaLearningSystem

ml_system = MetaLearningSystem()
current_session = None

def handle_user_request(request):
    global current_session
    
    # Detect if this is a new feature request
    if is_feature_request(request):
        feature_tag = extract_feature_tag(request)
        current_session = ml_system.start_development_session(feature_tag)
    
    # Process the request normally
    prompt = build_prompt(request)
    response = call_claude_api(prompt)
    tools_used = extract_tools_used(response)
    
    # Log the interaction
    if current_session:
        ml_system.log_development_interaction(
            feature_tag=feature_tag,
            prompt=prompt,
            response=response,
            tools_used=tools_used,
            phase=detect_phase(request),
            session_id=current_session
        )
    
    return response
```

### Self-Improvement Prompts

```python
def build_enhanced_prompt(user_request, feature_type=None):
    """Build prompts with learning context"""
    
    # Get relevant learnings
    context = ml_system.generate_learning_context(
        feature_tag=f"Feature_{datetime.now().isoformat()}",
        feature_type=feature_type
    )
    
    # Inject into prompt
    enhanced_prompt = f"""
{user_request}

# Past Learnings
{context}

Apply relevant patterns from past experience while implementing this feature.
"""
    
    return enhanced_prompt
```

## Database Schema

### Tables Created

1. **development_conversations**
   - Logs all development interactions
   - Links to sessions and feature tags
   
2. **lessons_learned**
   - Extracted patterns and insights
   - Tracks effectiveness and application count
   
3. **implementation_quality**
   - Quality scores for each feature
   - Strengths, weaknesses, improvements
   
4. **feature_templates**
   - Reusable solution patterns
   - Success rates and reuse counts
   
5. **learning_metrics**
   - Time-series tracking of improvement
   - Overall system performance

## Best Practices

### 1. Tag Features Consistently

Use descriptive feature tags:
- Good: `Phase3_ErrorRecovery`, `Feature_UserAuthentication`
- Avoid: `feature1`, `test`, `fix`

### 2. Log All Phases

Track different development phases:
- `planning`: Initial design and approach
- `implementation`: Actual coding work
- `testing`: Verification and validation
- `debugging`: Problem solving
- `documentation`: Writing docs

### 3. Extract Patterns After Completion

Don't forget to extract and save patterns when a feature is done:
```python
patterns = ml.extract_patterns_from_session(feature_tag, session_id)
ml.save_lessons_learned(feature_tag, patterns)
```

### 4. Score Honestly

Provide accurate quality scores to track real improvement:
- **Code Quality**: Readability, maintainability, best practices
- **Test Coverage**: Comprehensive testing of functionality
- **Documentation**: Clear docs, comments, examples

### 5. Create Templates for Success

When a feature scores >= 0.8, create a template:
```python
if quality_score >= 0.8:
    ml.create_feature_template(...)
```

### 6. Use Learning Context

Always check for relevant past learnings before starting new work:
```python
context = ml.generate_learning_context(new_feature, feature_type)
# Inject context into prompt
```

### 7. Review Dashboard Regularly

Check the dashboard to:
- Track improvement trends
- Identify effective patterns
- Learn from high-quality features
- Spot areas needing improvement

## Example: Complete Feature Development

```python
from src.meta_learning_system import MetaLearningSystem
from src.meta_learning_dashboard import LearningDashboard

# Initialize
ml = MetaLearningSystem()
dashboard = LearningDashboard()

# 1. Start new feature
feature_tag = "Feature_APIRateLimiting"
session_id = ml.start_development_session(feature_tag)

# 2. Get past learnings
context = ml.generate_learning_context(feature_tag, "api_feature")
print("Relevant learnings:", context)

# 3. Log planning
ml.log_development_interaction(
    feature_tag=feature_tag,
    prompt="Design rate limiting system",
    response="Will use token bucket algorithm with Redis backend",
    phase="planning",
    session_id=session_id
)

# 4. Log implementation
ml.log_development_interaction(
    feature_tag=feature_tag,
    prompt="Implement rate limiter",
    response="Created RateLimiter class with configurable limits",
    tools_used=["write_file"],
    phase="implementation",
    session_id=session_id
)

# 5. Log testing
ml.log_development_interaction(
    feature_tag=feature_tag,
    prompt="Test rate limiting",
    response="All tests pass. Verified limits work correctly",
    tools_used=["execute_command"],
    phase="testing",
    session_id=session_id
)

# 6. Extract patterns
patterns = ml.extract_patterns_from_session(feature_tag, session_id)
print(f"Extracted {len(patterns)} patterns")

# 7. Save lessons
lesson_ids = ml.save_lessons_learned(feature_tag, patterns)

# 8. Score quality
quality_id = ml.score_implementation_quality(
    feature_tag=feature_tag,
    code_quality=0.92,
    test_coverage=0.88,
    documentation=0.85,
    strengths=["Clean implementation", "Good test coverage"],
    weaknesses=["Could add more examples"],
    improvements=["Add performance benchmarks"]
)

# 9. Create template (if high quality)
if (0.92 + 0.88 + 0.85) / 3 >= 0.8:
    ml.create_feature_template(
        template_name="API Rate Limiting Template",
        feature_type="api_feature",
        description="Token bucket rate limiting pattern",
        approach="Use Redis for distributed rate limiting",
        solution_steps=[
            "Choose algorithm (token bucket)",
            "Set up Redis connection",
            "Implement token tracking",
            "Add middleware integration",
            "Test with concurrent requests"
        ]
    )

# 10. View dashboard
dashboard.print_full_dashboard()
```

## Metrics and Insights

### Key Metrics Tracked

1. **Learning Rate**: Lessons per feature
2. **Quality Trend**: Improving/stable/declining
3. **Template Effectiveness**: Success rate of reused patterns
4. **Pattern Application**: How often lessons are applied
5. **Feature Velocity**: Development speed over time

### What BECA Learns

- **Approaches**: What methods work for different feature types
- **Schema Patterns**: Effective database designs
- **Testing Strategies**: How to thoroughly test implementations
- **Problem-Solving**: Common issues and their solutions
- **Code Patterns**: Reusable code structures
- **Best Practices**: What leads to high-quality implementations

## Troubleshooting

### No Patterns Extracted

- Ensure you're logging interactions with detailed responses
- Use descriptive tool names in `tools_used`
- Include phase information

### Low Quality Scores

- Be honest in scoring - it helps track real improvement
- Review what worked well in past high-scoring features
- Check dashboard for patterns to apply

### Templates Not Being Reused

- Create more specific, actionable templates
- Include detailed solution steps
- Tag templates with accurate feature types

## Advanced Usage

### Custom Pattern Extraction

Extend the pattern extraction system:

```python
class CustomMetaLearning(MetaLearningSystem):
    def _extract_custom_patterns(self, conversations):
        patterns = []
        # Your custom logic here
        return patterns
```

### Integration with Other Systems

```python
# Link with knowledge system
from src.knowledge_system import KnowledgeBase

kb = KnowledgeBase()
ml = MetaLearningSystem()

# When extracting patterns, also save to knowledge base
patterns = ml.extract_patterns_from_session(feature_tag, session_id)
for pattern in patterns:
    kb.add_code_pattern(
        pattern_name=pattern['title'],
        language="python",
        code_snippet=pattern.get('code_examples', ''),
        description=pattern['content']
    )
```

## Summary

The Meta-Learning System transforms BECA from a tool executor into a learning system that:

1. ✓ Captures every development interaction
2. ✓ Extracts valuable patterns automatically
3. ✓ Tracks quality and improvement over time
4. ✓ Creates reusable templates from success
5. ✓ Applies past learnings to new work
6. ✓ Provides insights through comprehensive dashboard

This creates a positive feedback loop where BECA continuously improves with each feature built.
