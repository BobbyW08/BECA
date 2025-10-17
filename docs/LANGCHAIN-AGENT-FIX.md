# LangChain Agent Fix - Tool Execution Issue

> **⚠️ DEPRECATED - This document describes fixes for the old Gradio-based architecture**
> 
> **BECA now uses a modern React frontend + FastAPI backend architecture.**
> 
> **📖 See [START-BECA.md](../START-BECA.md) for current usage instructions.**
> 
> This document is kept for historical reference only.

---

## Problem
BECA was returning raw JSON function calls like `{"type": "function", "name": "explore_ollama_models"}` instead of actually executing the tools and returning results to the user.

## Root Cause
The issue was with using `create_tool_calling_agent` with Ollama models. While llama3.1:8b supports tool calling, LangChain's implementation wasn't properly parsing and executing the tool calls with Ollama's response format.

## Solution
Switched from `create_tool_calling_agent` to `create_react_agent` which uses the ReAct (Reasoning + Acting) pattern. This approach:

1. **Better Compatibility**: ReAct agents work more reliably with Ollama models
2. **Explicit Format**: Uses a clear Thought/Action/Observation loop that the model can follow
3. **Tool Execution**: Properly executes tools and returns results instead of raw JSON

## Changes Made

### File: `src/langchain_agent.py`

**Before (Tool Calling Agent):**
```python
from langchain.agents import create_tool_calling_agent

llm_with_tools = llm.bind_tools(BECA_TOOLS)
agent = create_tool_calling_agent(
    llm=llm_with_tools,
    tools=BECA_TOOLS,
    prompt=agent_prompt,
)
```

**After (ReAct Agent):**
```python
from langchain.agents import create_react_agent

react_prompt_template = """You are BECA...

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""

agent = create_react_agent(
    llm=llm,
    tools=BECA_TOOLS,
    prompt=agent_prompt,
)
```

## Testing (OLD)
To verify the fix works:

1. Go to http://34.55.204.139:3000 (new React frontend) or http://34.55.204.139:8000/docs (API)
2. Ask BECA: "What models are you running?"
3. **Expected**: BECA should execute the `explore_ollama_models` tool and return a list of models
4. **Previous Behavior**: Would return raw JSON like `{"type": "function", "name": "explore_ollama_models"}`

> **Note:** Port 7860 was for the old Gradio GUI. Current deployment uses ports 3000 (frontend) and 8000 (backend).

## Other Test Cases
- "List files in the current directory" → Should use `list_files` tool
- "What tools do you have?" → Should use `read_file` to check langchain_tools.py
- "Create a new React app" → Should ask for project name first

## Deployment (OLD METHOD)
```bash
# Files updated
- src/langchain_agent.py

# Old deployment steps (replaced by git-based deployment):
1. Updated langchain_agent.py locally
2. Copied to VM: gcloud compute scp src/langchain_agent.py beca-ollama:/opt/beca/src/
3. Restarted container: sudo docker-compose -f docker/docker-compose.yml restart beca-backend
```

> **Note:** SCP-based deployment has been replaced by git-based deployment workflow. See docker/deploy-gcp.sh for current deployment process.

## Status (Historical)
✅ Fix was deployed to VM  
✅ Tool execution now works properly with React frontend at port 3000 and FastAPI backend at port 8000

## Technical Details

### ReAct Pattern Benefits
1. **Structured Format**: Model follows a clear pattern that's easier to parse
2. **Explicit Tool Use**: Model must explicitly state Action and wait for Observation
3. **Better Debugging**: Verbose output shows the Thought/Action/Observation loop
4. **Ollama Compatibility**: Works reliably with open-source models like llama3.1

### Agent Executor Settings
```python
AgentExecutor(
    agent=agent,
    tools=BECA_TOOLS,
    verbose=True,
    max_iterations=10,      # Allow multiple tool uses
    max_execution_time=60,  # 60 second timeout
    return_intermediate_steps=True,
    early_stopping_method="force",
)
```

## Next Steps (Historical)
1. ~~User tests BECA at http://34.55.204.139:7860~~ → Now at http://34.55.204.139:3000
2. ~~Verify tools are executed properly~~ → Completed
3. ~~Move to next set of tasks~~ → Architecture has since been updated to React + FastAPI
