import json
import os
from typing import Any, Dict, List

class MemoryManager:
    """
    Manages a simple JSON-based memory for the agent.
    """
    def __init__(self, memory_file: str = "src/memory.json"):
        """
        Initializes the MemoryManager.

        Args:
            memory_file (str): Path to the JSON file for storing memories.
        """
        self.memory_file = memory_file
        self._create_if_not_exists()

    def _create_if_not_exists(self):
        """Creates the memory file with an empty JSON object if it doesn't exist."""
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({}, f)

    def _read_memory(self) -> Dict[str, Any]:
        """Reads the entire memory from the JSON file."""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def _write_memory(self, memory_data: Dict[str, Any]):
        """Writes the entire memory to the JSON file."""
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=4)

    def save_memory(self, key: str, value: Any):
        """
        Saves or appends a value to a specific key in memory.

        Args:
            key (str): The key to store the value under.
            value (Any): The value to store. If the key exists and holds a list,
                         the new value is appended. Otherwise, the key is set to the new value.
        """
        memory = self._read_memory()
        if key in memory and isinstance(memory[key], list):
            memory[key].append(value)
        else:
            # If you want to always have lists for certain keys, you can enforce it here.
            # For now, we'll just overwrite or create.
            memory[key] = value
        self._write_memory(memory)

    def retrieve_memory(self, key: str) -> Any:
        """
        Retrieves a memory by key.

        Args:
            key (str): The key of the memory to retrieve.

        Returns:
            Any: The value associated with the key, or None if not found.
        """
        memory = self._read_memory()
        return memory.get(key)

    def retrieve_past_patterns(self, key_prefix: str) -> List[Any]:
        """
        Retrieves a list of memories where the key matches a prefix.
        Useful for finding all "react_scaffold_*" memories, for example.

        Args:
            key_prefix (str): The prefix to search for.

        Returns:
            List[Any]: A list of values for the matching keys.
        """
        memory = self._read_memory()
        return [value for key, value in memory.items() if key.startswith(key_prefix)]

if __name__ == '__main__':
    # Example Usage
    memory_manager = MemoryManager()

    # Save a simple memory
    memory_manager.save_memory("last_user", "BobbyW08")
    print(f"Retrieved 'last_user': {memory_manager.retrieve_memory('last_user')}")

    # Save a successful scaffold pattern
    scaffold_pattern = {
        "prompt": "Scaffold a React app named 'test-app'",
        "result": "Successfully created React scaffold in 'test-app'"
    }
    memory_manager.save_memory("react_scaffold_success_1", scaffold_pattern)

    # Retrieve all react scaffold patterns
    react_patterns = memory_manager.retrieve_past_patterns("react_scaffold")
    print("\n--- Past React Scaffold Patterns ---")
    print(json.dumps(react_patterns, indent=2))
