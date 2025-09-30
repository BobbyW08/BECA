import json
import requests
from typing import Any, Dict

from prompt_manager import PromptManager
from memory_manager import MemoryManager
from tool_router import ToolRouter

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5-coder:3b-instruct-q4_K_M"

def ask_model(prompt: str) -> Dict[str, Any]:
    """Sends a prompt to the Ollama model and returns the JSON response."""
    print("🧠 Calling Ollama model...")
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"❌ Error calling Ollama: {e}")
        return {}

def main():
    """
    Main orchestration logic for the BECA agent.
    """
    print("🚀 BECA agent starting…")

    # 1. Initialize managers
    try:
        prompt_manager = PromptManager(prompts_dir="prompts")
        memory_manager = MemoryManager(memory_file="src/memory.json")
        tool_router = ToolRouter()
    except Exception as e:
        print(f"❌ Error initializing managers: {e}")
        return

    # 2. Define the task (for now, it's hardcoded)
    task_name = "scaffold_react"
    task_params = {"app_name": "my-new-weather-app"}

    # 3. Load prompt, inject memory, and render
    try:
        # Retrieve past successful patterns for context (optional)
        past_patterns = memory_manager.retrieve_past_patterns(task_name)
        # Here you could inject 'past_patterns' into the prompt if the template supports it
        
        final_prompt = prompt_manager.render(task_name, **task_params)
        print("\n── Rendered Prompt ──")
        print(final_prompt)
    except (ValueError, FileNotFoundError) as e:
        print(f"❌ Error rendering prompt: {e}")
        return

    # 4. Call the AI model
    model_response = ask_model(final_prompt)
    if not model_response:
        return

    raw_plan_str = model_response.get("response", "")
    print("\n── Raw JSON Plan from Model ──")
    print(raw_plan_str)

    # 5. Parse the JSON plan
    try:
        plan = json.loads(raw_plan_str)
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse JSON plan: {e}")
        # Optionally, save this failure to memory
        memory_manager.save_memory(f"{task_name}_failure_{model_response.get('created_at')}", {
            "prompt": final_prompt,
            "response": raw_plan_str,
            "error": str(e)
        })
        return

    print("\n── Parsed Plan ──")
    print(json.dumps(plan, indent=2))

    # 6. Route plan to tools
    try:
        callables = tool_router.route(plan)
        if not callables:
            print("🤔 No tools were routed for the given plan.")
            return
    except ValueError as e:
        print(f"❌ Error routing tools: {e}")
        return

    # 7. Execute tools
    print("\n── Executing Tools ──")
    for func in callables:
        try:
            result = func()
            print(f"✅ Tool executed successfully: {result}")
            # On success, save the pattern to memory
            memory_manager.save_memory(f"{task_name}_success_{model_response.get('created_at')}", {
                "prompt": final_prompt,
                "plan": plan,
                "result": result
            })
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            # Optionally, save the failure
            memory_manager.save_memory(f"{task_name}_tool_failure_{model_response.get('created_at')}", {
                "prompt": final_prompt,
                "plan": plan,
                "error": str(e)
            })

if __name__ == "__main__":
    main()
