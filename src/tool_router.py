from typing import Callable, List, Dict, Any
import re
from tools.scaffolding import create_react_scaffold, create_flask_api
from tools.web_search import web_search

class ToolRouter:
    """
    Maps natural language steps from a plan to executable Python functions.
    """
    def __init__(self):
        """
        Initializes the ToolRouter with a mapping of regex patterns to functions.
        """
        self.tool_mappings = [
            (re.compile(r"scaffold a react app named ['\"](.+?)['\"]", re.IGNORECASE), self._route_to_react_scaffold),
            (re.compile(r"create a flask api named ['\"](.+?)['\"]", re.IGNORECASE), self._route_to_flask_api),
            (re.compile(r"npx create-react-app (.+)", re.IGNORECASE), self._route_to_react_scaffold),
            (re.compile(r"perform a web search for ['\"](.+?)['\"]", re.IGNORECASE), self._route_to_web_search),
        ]

    def _route_to_react_scaffold(self, app_name: str) -> Callable[[], Any]:
        """Returns a callable for the create_react_scaffold tool."""
        return lambda: create_react_scaffold(app_name)

    def _route_to_flask_api(self, api_name: str) -> Callable[[], Any]:
        """Returns a callable for a hypothetical create_flask_api tool."""
        return lambda: create_flask_api(api_name)

    def _route_to_web_search(self, query: str) -> Callable[[], Any]:
        """Returns a callable for the web_search tool."""
        return lambda: web_search(query)

    def route(self, plan: Dict[str, Any]) -> List[Callable[[], Any]]:
        """
        Takes a parsed JSON plan and returns a list of callable functions.

        Args:
            plan (Dict[str, Any]): A dictionary with a "steps" key, which is a list of strings.

        Returns:
            List[Callable[[], Any]]: A list of functions to be executed.
                                     Raises ValueError for unrecognized steps.
        """
        callables = []
        steps = plan.get("steps", [])

        for step_obj in steps:
            # The step can be a string or a dictionary
            if isinstance(step_obj, dict):
                step = step_obj.get("description", "") or step_obj.get("command", "")
            elif isinstance(step_obj, str):
                step = step_obj
            else:
                continue # Or handle error

            matched = False
            for pattern, router_func in self.tool_mappings:
                match = pattern.search(step)
                if match:
                    # Extract arguments from the regex match
                    args = match.groups()
                    # Get the callable and add it to the list
                    tool_callable = router_func(*args)
                    if tool_callable:
                        callables.append(tool_callable)
                    matched = True
                    break
            
            if not matched:
                # For now, we'll just ignore steps that don't match.
                # In the future, this could raise an error or use a fallback tool.
                print(f"Warning: No tool found for step: '{step}'")

        return callables

if __name__ == '__main__':
    # Example Usage
    router = ToolRouter()

    # Example plan from the agent
    example_plan = {
        "title": "Scaffold a Test App",
        "steps": [
            "First, scaffold a React app named 'my-test-app'.",
            "Then, do something else that is not a tool.",
            "Finally, scaffold a react app named 'another-app'."
        ]
    }

    try:
        # Route the plan to get a list of functions to call
        functions_to_run = router.route(example_plan)

        # Execute the functions
        for func in functions_to_run:
            result = func()
            print(f"Executed tool: {result}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
