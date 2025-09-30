import schedule
import time
import subprocess
import json
from datetime import datetime

def run_beca_task(task_name: str, args: str):
    """
    Runs a BECA task using the VS Code task runner.
    This is a placeholder for a more robust implementation.
    """
    print(f"[{datetime.now()}] Running task '{task_name}' with args: {args}")
    try:
        # This is a simplified way to trigger a VS Code task from an external script.
        # In a real-world scenario, this might involve calling the VS Code API
        # or using a different execution method.
        subprocess.run(
            ["python", "src/beca_agent.py", task_name, args],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[{datetime.now()}] Task '{task_name}' completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Task '{task_name}' failed.")
        print(f"Stderr: {e.stderr}")
        return False

def self_check_and_trigger():
    """
    Analyzes memory and decides if a new task should be triggered.
    """
    print(f"[{datetime.now()}] Performing self-check...")
    try:
        with open('src/memory.json', 'r') as f:
            memory = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Memory not found or is invalid. Skipping trigger.")
        return

    # Example heuristic: If a scaffold task succeeded, trigger a web search
    # to find a relevant library for the project.
    successful_scaffolds = [
        k for k in memory.get("successful_operations", {}) 
        if "scaffold" in k.lower()
    ]

    if successful_scaffolds:
        last_scaffold = successful_scaffolds[-1]
        app_name = last_scaffold.split("'")[1] # Fragile parsing, for demo only

        # Avoid re-triggering for the same app
        if f"web_search:find_library_for_{app_name}" in memory.get("successful_operations", {}):
            print(f"Already searched for libraries for {app_name}. Skipping.")
            return

        print(f"Found successful scaffold for '{app_name}'. Triggering web search.")
        run_beca_task(
            task_name="web_search", 
            args=f"find a UI library for a {app_name} React app"
        )

def main():
    """
    Main loop for the autonomy scheduler.
    """
    print("BECA Autonomy Agent started.")
    
    # Schedule the self-check to run every 5 minutes.
    schedule.every(5).minutes.do(self_check_and_trigger)

    # Initial run
    self_check_and_trigger()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
