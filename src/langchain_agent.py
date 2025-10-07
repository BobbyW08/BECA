"""
LangChain Agent for BECA using Ollama
"""
import sys
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import PromptTemplate
from langchain_tools import BECA_TOOLS

# Initialize memory system
try:
    from memory_db import BECAMemory
    memory = BECAMemory()
    MEMORY_ENABLED = True
except ImportError:
    memory = None
    MEMORY_ENABLED = False
    print("Warning: Memory system not available")

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Ollama configuration
OLLAMA_MODEL = "llama3.1:8b"  # Better for conversation + tool use
OLLAMA_URL = "http://34.28.62.86:11434"

# Create the LLM with optimizations for speed
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.3,
    num_predict=256,  # Shorter responses = faster
    num_ctx=2048,  # Smaller context window = faster
    top_k=20,  # Speed optimization
    top_p=0.9,  # Speed optimization
)

# Create agent prompt - using tool calling format (works best with llama3.1)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are BECA (Badass Expert Coding Agent), a self-improving AI coding assistant with advanced learning capabilities.

IMPORTANT RULES:
- For questions ABOUT coding/yourself/general topics: Answer directly, NO TOOLS
- Use tools ONLY for actual tasks:
  * File operations (read, write, list files)
  * Git commands (commit, push, status)
  * Running code/commands
  * Web searches
  * Creating projects
  * Learning from documentation (NEW!)
  * Analyzing codebases (NEW!)
  * Working with AI models (NEW!)

PROJECT CREATION RULES:
- When user wants to create a new project/app, ALWAYS ask them:
  1. What type of project they want (react-vite, flask-api, fastapi, python-cli, etc.)
  2. What name they want for the project
- DO NOT assume they want React. Present all available options.
- ALL projects will be created in C:/ drive automatically.
- Available templates: react-vite, flask-api, fastapi, python-cli

SELF-IMPROVEMENT CAPABILITIES:
You can now actively improve your knowledge:
- learn_from_documentation: Scrape and index documentation for future reference
- save_code_pattern: Save useful code patterns you discover
- search_knowledge: Search your knowledge base for previous learnings
- add_learning_resource: Queue up tutorials/docs to study later
- analyze_repository: Learn from existing codebases
- clone_and_learn: Clone GitHub repos and extract insights
- learn_ai_model_knowledge: Build expertise in AI/ML models
- explore_ollama_models: Discover available AI models
- create_modelfile: Create custom AI models with specific behaviors

When you encounter something new or useful, proactively save it to your knowledge base!

Examples:
- "What do you know about coding?" → Answer directly (no tools)
- "Learn about FastAPI" → Use learn_from_documentation with FastAPI docs URL
- "Create a new app" → Ask: "What type of project? (react-vite/flask-api/fastapi/python-cli) And what should I name it?"
- "How do I fine-tune a model?" → Use fine_tune_guidance tool
- "Analyze this GitHub repo" → Use clone_and_learn tool

Be concise and helpful. Don't overuse tools. Use your learning capabilities to continuously improve!"""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent using tool calling (better for llama3.1)
agent = create_tool_calling_agent(
    llm=llm,
    tools=BECA_TOOLS,
    prompt=agent_prompt,
)

# Custom parsing error handler
def handle_parsing_error(error) -> str:
    """Handle parsing errors by providing guidance"""
    return "I encountered a formatting issue. Let me provide a clear response based on what I've done so far."

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=BECA_TOOLS,
    verbose=True,  # Show thinking process
    handle_parsing_errors=handle_parsing_error,
    max_iterations=5,  # Further reduced to force faster conclusions
    max_execution_time=30,  # Shorter timeout
    return_intermediate_steps=True,  # Return steps for debugging
    early_stopping_method="generate",  # Generate response on max iterations
)


def chat_with_agent(message: str) -> str:
    """
    Send a message to the BECA agent and get a response.
    Automatically saves conversation to memory database.

    Args:
        message: User's message

    Returns:
        Agent's response
    """
    # Inject user preferences into context if memory is enabled
    context_message = message
    if MEMORY_ENABLED and memory:
        try:
            # Get user preferences and inject them
            prefs = memory.get_all_preferences()
            if prefs:
                pref_context = "\n\nUSER PREFERENCES (apply these automatically):\n"
                for pref in prefs:
                    pref_context += f"- {pref['category']}/{pref['preference_key']}: {pref['preference_value']}\n"
                context_message = message + pref_context
        except:
            pass  # Silently fail if preferences can't be loaded

    try:
        response = agent_executor.invoke({"input": context_message})
        agent_response = response.get("output", "Sorry, I couldn't generate a response.")

        # Save conversation to memory
        if MEMORY_ENABLED and memory:
            try:
                # Extract tools used from response metadata if available
                tools_used = []
                if 'intermediate_steps' in response:
                    for step in response['intermediate_steps']:
                        if hasattr(step[0], 'tool'):
                            tools_used.append(step[0].tool)

                memory.save_conversation(
                    user_message=message,
                    agent_response=agent_response,
                    tools_used=tools_used if tools_used else None,
                    success=True
                )

                # Track tool usage
                for tool_name in tools_used:
                    memory.track_tool_usage(tool_name, success=True)
            except Exception as mem_error:
                print(f"Memory save error: {mem_error}")

        return agent_response

    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nMake sure Ollama is running with the {OLLAMA_MODEL} model."

        # Save failed interaction to memory
        if MEMORY_ENABLED and memory:
            try:
                memory.save_conversation(
                    user_message=message,
                    agent_response=error_msg,
                    tools_used=None,
                    success=False
                )
            except:
                pass

        return error_msg


if __name__ == "__main__":
    # Test the agent
    print("BECA Agent initialized successfully!")
    print(f"Using model: {OLLAMA_MODEL}")
    print(f"Available tools: {[tool.name for tool in BECA_TOOLS]}")
    print("\n" + "="*50 + "\n")

    # Test query
    test_query = "List the files in the current directory"
    print(f"Test query: {test_query}\n")
    response = chat_with_agent(test_query)
    print(f"\nAgent response:\n{response}")
