import os
import json
from jinja2 import Template

class PromptManager:
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = prompts_dir
        self.templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.prompts_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    template_name = filename.replace(".json", "")
                    templates[template_name] = data
        return templates

    def render(self, template_name: str, **kwargs) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found.")
        
        template_data = self.templates[template_name]
        template_string = template_data.get("template", "")
        
        jinja_template = Template(template_string)
        return jinja_template.render(**kwargs)

if __name__ == '__main__':
    # Example usage:
    try:
        prompt_manager = PromptManager()
        
        # Render the React scaffold prompt
        react_prompt = prompt_manager.render("scaffold_react", app_name="my-awesome-app")
        print("--- Rendered React Prompt ---")
        print(react_prompt)
        
        # Render the Flask API prompt
        flask_prompt = prompt_manager.render("create_flask_api", api_name="my-cool-api")
        print("\n--- Rendered Flask API Prompt ---")
        print(flask_prompt)

    except Exception as e:
        print(f"An error occurred: {e}")
