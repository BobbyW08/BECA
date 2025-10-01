"""
LangChain Agent for BECA using Ollama
"""
import sys
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
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
OLLAMA_URL = "http://127.0.0.1:11434"

# Create the LLM
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.1,  # Low temperature for more focused code generation
)

# Create agent prompt
# ReAct pattern: Thought, Action, Action Input, Observation, Thought, ...
agent_prompt = PromptTemplate.from_template(
    """You are BECA (Badass Expert Coding Agent), an autonomous coding assistant. Help users build applications, fix bugs, and write code.

IMPORTANT: For simple conversational questions (like "what's your name?" or "hello"), answer directly without using tools. Only use tools for actual coding tasks.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action

CRITICAL TOOL INPUT RULES:
- For tools with ONE parameter: provide ONLY the value, NOT JSON
  Example: create_react_app needs app_name → Action Input: my-todo-app
- For tools with MULTIPLE parameters: use JSON format
  Example: write_file needs file_path and content → Action Input: {{"file_path": "app.py", "content": "print('hi')"}}
- NEVER wrap single parameters in JSON objects

Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question. IMPORTANT: Include the full details from your observations, not just a summary.

Question: {input}
Thought: {agent_scratchpad}
"""
)

# Create the agent
agent = create_react_agent(
    llm=llm,
    tools=BECA_TOOLS,
    prompt=agent_prompt,
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=BECA_TOOLS,
    verbose=True,  # Show thinking process
    handle_parsing_errors=True,
    max_iterations=20,  # Increased for complex planning tasks
    max_execution_time=120,  # 2 minutes timeout
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
