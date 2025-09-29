print("🚀 BECA agent starting…")

import requests
import json
from typing import Any, Dict
from tools import create_react_scaffold

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5-coder:3b-instruct-q4_K_M"

def ask_model(prompt: str) -> Dict[str, Any]:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    # 1) Ask the model for a JSON plan
    test_prompt = (
        "You are a scaffolding assistant. ALWAYS respond with valid JSON only "
        "and nothing else. Return exactly one JSON object with keys: "
        "\"title\" (string) and \"steps\" (array of strings). "
        "Example: {\"title\":\"x\",\"steps\":[\"a\",\"b\"]}. "
        "Now produce the scaffold plan for a React app named weather-app."
    )
    resp = ask_model(test_prompt)

    # 2) Show the full raw response from Ollama
    print("\n── Full Ollama Response ──")
    print(json.dumps(resp, indent=2))

    # 3) Extract the JSON string from the "response" field
    raw_plan = resp.get("response") or resp.get("output") or ""
    print("\n── Raw JSON String ──")
    print(raw_plan)

    # 4) Parse that string into a real Python dict
    try:
        plan = json.loads(raw_plan)
    except json.JSONDecodeError as e:
        print("\n❌ Failed to parse JSON:", e)
        exit(1)

    # 5) Show the parsed plan neatly
    print("\n── Parsed Plan ──")
    print(json.dumps(plan, indent=2))

    # 6) Dry-run your tool stub using the plan title as folder name
    folder_name = plan["title"].lower().replace(" ", "-")
    result = create_react_scaffold(folder_name)
    print(f"\n── create_react_scaffold('{folder_name}') returned ──")
    print(result)
