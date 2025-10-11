"""
LangChain Agent for BECA using Ollama
"""
import sys
import subprocess
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

# Ollama configuration - Auto-detect VM IP (since it's preemptible and IP changes)
def get_ollama_url():
    """Get the current Ollama URL by fetching VM's external IP."""
    try:
        result = subprocess.run(
            ["gcloud", "compute", "instances", "describe", "beca-ollama",
             "--project=beca-0001", "--format=get(networkInterfaces[0].accessConfigs[0].natIP)"],
            capture_output=True, text=True, timeout=5, check=True
        )
        ip = result.stdout.strip()
        if ip:
            return f"http://{ip}:11434"
    except:
        pass
    # Fallback to last known IP
    return "http://35.226.49.146:11434"

OLLAMA_URL = get_ollama_url()

# Model definitions
LLAMA_MODEL = "llama3.1:8b"  # Best for: conversation, reasoning, tool use, general tasks
CODER_MODEL = "qwen2.5-coder:7b-instruct"  # Best for: code generation, debugging, code review

# Create LLMs for both models
llm_general = ChatOllama(
    model=LLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.4,  # Slightly higher for more diverse responses
    num_predict=512,  # Allow longer, more complete responses
    num_ctx=4096,  # Larger context to understand complex queries better
    top_k=40,  # More diversity in token selection
    top_p=0.9,
)

llm_coder = ChatOllama(
    model=CODER_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.2,  # Lower temp for more precise code
    num_predict=512,  # Longer responses for code
    num_ctx=4096,  # Larger context for code understanding
    top_k=20,
    top_p=0.9,
)

# Default to general model for agent
llm = llm_general

# Create agent prompt - using tool calling format (works best with llama3.1)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are BECA (Badass Expert Coding Agent), a self-improving AI coding assistant with advanced learning capabilities.

ABOUT YOU:
- Your codebase is in C:\\dev and C:\\dev\\src
- Your main files: beca_gui.py, langchain_agent.py, langchain_tools.py, knowledge_system.py, memory_db.py
- Your knowledge is stored in: beca_knowledge.db and beca_memory.db
- You run on Ollama with two models: llama3.1:8b (general) and qwen2.5-coder:7b-instruct (coding)

BE PROACTIVE WITH YOUR OWN CODE:
- When asked to review YOUR codebase → Use list_files("C:/dev") and list_files("C:/dev/src"), then read_file on key files
- When asked about YOUR capabilities → Use list_files and read_file to check langchain_tools.py
- When asked about YOUR architecture → Use read_file on langchain_agent.py and beca_gui.py
- DON'T suggest clone_and_learn for your own code - you already have access! Just read the files directly.

TOOL USAGE RULES:
- Questions about YOUR code/capabilities → Use list_files + read_file immediately
- General knowledge questions → Answer directly without tools
- User tasks (read/write files, git, run code, search web, create projects) → Use appropriate tools

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

EXAMPLE INTERACTIONS:
User: "What do you know about coding?"
You: Answer directly (no tools)

User: "Review your own codebase and understand your capabilities"
You: Use list_files("C:/dev"), list_files("C:/dev/src"), then read_file on langchain_tools.py to see all tools

User: "What tools do you have?"
You: Use read_file("C:/dev/src/langchain_tools.py") to check, then summarize

User: "Create a new app"
You: Ask: "What type of project? (react-vite/flask-api/fastapi/python-cli) And what should I name it?"

User: "Learn about FastAPI"
You: Use learn_from_documentation with FastAPI docs URL

Be direct, proactive, and action-oriented. When asked about yourself, immediately use tools to check your own code!""""),
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


def _should_use_coder_model(message: str) -> bool:
    """
    Determine if the coder model should be used based on the message content.

    Use qwen2.5-coder for:
    - Writing/generating code
    - Debugging code
    - Code review and analysis
    - Explaining complex code
    - Refactoring suggestions

    Use llama3.1 for:
    - General conversation
    - Tool use and file operations
    - Planning and reasoning
    - Documentation writing
    - General questions
    """
    message_lower = message.lower()

    # Keywords that indicate code-focused tasks
    code_keywords = [
        'write code', 'generate code', 'create function', 'create class',
        'write a function', 'write function', 'write a class', 'create a function',
        'create a class', 'create an algorithm', 'write an algorithm',
        'implement', 'code for', 'debug', 'fix this code', 'what\'s wrong with',
        'refactor', 'optimize code', 'improve this code', 'code review',
        'explain this code', 'how does this code', 'algorithm for',
        'function that', 'class that', 'method that', 'write a',
        'bug in', 'error in my code', 'syntax error', 'logic error',
        'python function', 'javascript function', 'java class', 'c++ code'
    ]

    # Check if message contains code-related keywords
    for keyword in code_keywords:
        if keyword in message_lower:
            return True

    # Check if message contains code blocks (triple backticks or indented code)
    if '```' in message or '\n    ' in message:
        return True

    return False


def chat_with_agent(message: str, force_model: str = None) -> str:
    """
    Send a message to the BECA agent and get a response.
    Automatically saves conversation to memory database.
    Intelligently selects between llama3.1 (general) and qwen2.5-coder (coding).

    Args:
        message: User's message
        force_model: Optional. Force a specific model ("general" or "coder")

    Returns:
        Agent's response
    """
    # Determine which model to use
    use_coder = force_model == "coder" if force_model else _should_use_coder_model(message)

    # Select the appropriate LLM and rebuild agent if needed
    global agent_executor
    if use_coder:
        # Use coder model for code-focused tasks
        coder_agent = create_tool_calling_agent(
            llm=llm_coder,
            tools=BECA_TOOLS,
            prompt=agent_prompt,
        )
        active_executor = AgentExecutor(
            agent=coder_agent,
            tools=BECA_TOOLS,
            verbose=True,
            handle_parsing_errors=handle_parsing_error,
            max_iterations=5,
            max_execution_time=30,
            return_intermediate_steps=True,
            early_stopping_method="generate",
        )
        model_used = CODER_MODEL
    else:
        # Use general model for everything else
        active_executor = agent_executor
        model_used = LLAMA_MODEL

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
        response = active_executor.invoke({"input": context_message})
        agent_response = response.get("output", "Sorry, I couldn't generate a response.")

        # Add model indicator to response (subtle, at the end)
        model_indicator = f"\n\n_[Using {model_used}]_" if use_coder else ""
        agent_response = agent_response + model_indicator

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
        error_msg = f"Error: {str(e)}\n\nMake sure Ollama is running at {OLLAMA_URL} with models: {LLAMA_MODEL} or {CODER_MODEL}."

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
    print(f"Using models: {LLAMA_MODEL} (general) and {CODER_MODEL} (coding)")
    print(f"Available tools: {[tool.name for tool in BECA_TOOLS]}")
    print("\n" + "="*50 + "\n")

    # Test query
    test_query = "List the files in the current directory"
    print(f"Test query: {test_query}\n")
    response = chat_with_agent(test_query)
    print(f"\nAgent response:\n{response}")
