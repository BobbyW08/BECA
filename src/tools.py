import os

def create_react_scaffold(folder_name: str) -> str:
    """
    Creates a basic React scaffold in the specified folder.
    """
    try:
        # Create the root folder for the React app
        os.makedirs(folder_name, exist_ok=True)

        # Create a 'src' directory inside the root folder
        src_path = os.path.join(folder_name, "src")
        os.makedirs(src_path, exist_ok=True)

        # Create a placeholder index.js file
        index_js_path = os.path.join(src_path, "index.js")
        with open(index_js_path, "w") as f:
            f.write("// Placeholder for React app\n")

        return f"Successfully created React scaffold in '{folder_name}'"
    except Exception as e:
        return f"Error creating React scaffold: {e}"
