"""
LangChain Agent for BECA using Ollama
"""
import sys
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_tools import BECA_TOOLS

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Ollama configuration
OLLAMA_MODEL = "qwen2.5-coder:3b-instruct-q4_K_M"
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
    """You are BECA, an autonomous coding assistant. Help users build applications, fix bugs, and write code.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

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
    max_iterations=10,
)


def chat_with_agent(message: str) -> str:
    """
    Send a message to the BECA agent and get a response.

    Args:
        message: User's message

    Returns:
        Agent's response
    """
    try:
        response = agent_executor.invoke({"input": message})
        return response.get("output", "Sorry, I couldn't generate a response.")
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running with the {OLLAMA_MODEL} model."


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
