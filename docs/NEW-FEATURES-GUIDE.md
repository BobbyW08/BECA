# BECA Enhanced Features Guide

Complete documentation for all new features added to BECA.

## 📋 Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Terminal Command Visibility](#terminal-command-visibility)
3. [Stop Button Functionality](#stop-button-functionality)
4. [File Upload Support](#file-upload-support)
5. [Google Drive Integration](#google-drive-integration)
6. [Enhanced Knowledge Base](#enhanced-knowledge-base)
7. [Improved Prompts](#improved-prompts)
8. [Virtual Environment](#virtual-environment)

---

## Setup & Installation

### Virtual Environment Setup

**Why use a virtual environment?**
- Isolates dependencies
- Prevents conflicts with system Python
- Makes deployments reproducible
- Required for production

**Setup Instructions:**

The virtual environment `beca-env/` has already been created. You just need to:

```bash
# Activate (Windows)
beca-env\Scripts\activate

# Activate (Linux/Mac)
source beca-env/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

**Note:** If you need to recreate it for any reason:
```bash
python -m venv beca-env
```

### New Dependencies

The following packages have been added:

```
# File Upload Support
PyPDF2              # PDF extraction
python-docx         # Word documents
pandas              # CSV/Excel
openpyxl            # Excel files
Pillow              # Image processing
tabulate            # Markdown tables

# Google Drive
google-auth-oauthlib
google-auth-httplib2
google-api-python-client

# Async Support
aiohttp
```

---

## Terminal Command Visibility

### Overview

See real-time terminal output as BECA executes commands.

### Features

- **Real-time Output**: Stream command output as it happens
- **Command History**: View past 100 commands with status
- **Status Indicators**: ⏳ Running, ✅ Success, ❌ Error, 🛑 Stopped
- **Error Tracking**: Separate stdout and stderr

### Usage

1. Terminal panel appears on the right side of the GUI
2. Automatically updates when BECA runs commands
3. Click "Refresh" to manually update

### API Usage

```python
from terminal_manager import terminal_manager

# Execute a command
result = terminal_manager.execute_command(
    command="npm install",
    cwd="/path/to/project"
)

# Check status
if result['success']:
    print(f"Output: {result['output']}")
else:
    print(f"Error: {result['error']}")

# Get command history
history = terminal_manager.get_history(limit=10)
formatted = terminal_manager.format_history()
```

### Technical Details

- Uses `subprocess.Popen` for command execution
- Thread-safe with threading.Event for cancellation
- Captures both stdout and stderr separately
- Stores last 100 commands in memory

---

## Stop Button Functionality

### Overview

Cancel long-running operations with a single click.

### Features

- **Graceful Termination**: Tries SIGTERM first, then SIGKILL
- **Immediate Feedback**: UI updates instantly
- **State Management**: Cleans up resources properly
- **Thread-Safe**: Works with concurrent operations

### Usage

1. Stop button appears when BECA is processing
2. Click to cancel the current operation
3. BECA will finish the current step and stop gracefully

### API Usage

```python
from terminal_manager import terminal_manager

# Check if command is running
if terminal_manager.is_running():
    # Stop the current command
    terminal_manager.stop_current_command()
```

### Implementation

The stop functionality uses a thread-safe Event flag:

```python
import threading

chat_stop_flag = threading.Event()

# In your long-running function
def long_operation():
    for i in range(1000):
        if chat_stop_flag.is_set():
            return "Stopped by user"
        # Do work
        process_item(i)
```

---

## File Upload Support

### Overview

Upload and process various file types for BECA to analyze.

### Supported File Types

**Text Files:**
- `.txt`, `.md`, `.markdown`, `.rst`

**Code Files:**
- `.py`, `.js`, `.ts`, `.jsx`, `.tsx`
- `.java`, `.c`, `.cpp`, `.h`, `.hpp`
- `.cs`, `.go`, `.rs`, `.rb`, `.php`
- `.swift`, `.kt`, `.scala`

**Web Files:**
- `.html`, `.htm`, `.css`, `.scss`, `.less`

**Config Files:**
- `.json`, `.yaml`, `.yml`, `.toml`
- `.ini`, `.cfg`, `.conf`, `.xml`, `.env`

**Data Files:**
- `.csv`, `.tsv`

**Documents:**
- `.pdf` (requires PyPDF2)
- `.docx` (requires python-docx)
- `.xlsx`, `.xls` (requires pandas + openpyxl)

**Images:**
- `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.svg`

### Usage

1. Click the "Upload File" button in the chat panel
2. Select your file
3. BECA automatically extracts and processes the content
4. The content is added to the conversation context

### API Usage

```python
from file_uploader import file_uploader

# Process an upload
result = file_uploader.process_upload(
    file_data=file_bytes,
    filename="document.pdf"
)

if result['success']:
    print(f"Content: {result['content']}")
    print(f"Metadata: {result['metadata']}")
```

### Content Extraction

- **Text files**: Direct reading with UTF-8 encoding
- **CSV files**: Converted to markdown tables
- **PDF files**: Text extraction from all pages
- **Word docs**: Paragraph extraction
- **Excel files**: All sheets converted to markdown
- **Images**: Metadata extraction (OCR optional with pytesseract)

### Example Output

```
✅ File uploaded successfully: report.pdf

Content preview:
# Annual Report 2024

This report summarizes...

Metadata: {'type': 'pdf', 'pages': 15}
```

---

## Google Drive Integration

### Overview

Connect BECA to Google Drive for seamless file access.

### Features

- **OAuth Authentication**: Secure login with Google
- **File Browsing**: List and search files
- **Upload/Download**: Transfer files bidirectionally
- **Folder Sync**: Sync entire directories
- **Persistent Auth**: Token saved for future sessions

### Setup

1. **Get Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Drive API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` and place in project root

2. **First-Time Authentication:**
   ```python
   from google_drive_manager import drive_manager
   
   # Authenticate (opens browser)
   success, message = drive_manager.authenticate()
   ```

3. **Token Storage:**
   - First auth creates `token.pickle`
   - Subsequent runs use saved token
   - Token auto-refreshes when expired

### Usage Examples

**List Files:**
```python
result = drive_manager.list_files(max_results=20)

for file in result['files']:
    print(f"{file['name']} - {file['id']}")
```

**Search Files:**
```python
result = drive_manager.search_files("quarterly report")
```

**Download File:**
```python
success, message = drive_manager.download_file(
    file_id="abc123xyz",
    destination="local_file.pdf"
)
```

**Upload File:**
```python
success, message, file_id = drive_manager.upload_file(
    file_path="report.pdf",
    folder_id="optional_folder_id"
)
```

**Create Folder:**
```python
success, message, folder_id = drive_manager.create_folder(
    folder_name="BECA Projects",
    parent_id=None  # None for root
)
```

**Sync Folder:**
```python
result = drive_manager.sync_folder(
    local_folder="./projects",
    drive_folder_id="folder_id",
    direction="both"  # 'upload', 'download', or 'both'
)

print(f"Uploaded: {result['results']['uploaded']}")
print(f"Downloaded: {result['results']['downloaded']}")
```

### GUI Usage

1. Go to "Advanced Features" → "Google Drive"
2. Click "Authenticate" (first time only)
3. Click "List Files" to see your Drive files
4. Use in chat: "Download my project from Google Drive"

---

## Enhanced Knowledge Base

### Overview

Pre-loaded with common algorithms, design patterns, and code examples.

### Built-in Datasets

1. **Common Algorithms**
   - Binary Search
   - Depth-First Search (DFS)
   - Dynamic Programming patterns
   - Memoization techniques

2. **Design Patterns**
   - Singleton Pattern
   - Observer Pattern
   - Rate Limiter
   - Context Manager

3. **Web Development**
   - REST API endpoints
   - React components with hooks
   - Async/await patterns

### Usage

**Load All Datasets:**
```python
from dataset_loader import dataset_loader

results = dataset_loader.load_all_builtin_datasets()
# Output: {'algorithms': 8, 'web_patterns': 2}
```

**Load Custom Dataset:**
```python
# Create JSON file with code patterns
patterns = [
    {
        "pattern_name": "Custom Pattern",
        "language": "Python",
        "code_snippet": "def example():\n    pass",
        "description": "Description here",
        "use_case": "When to use this",
        "tags": ["category1", "category2"]
    }
]

# Load from file
count = dataset_loader.load_code_patterns_from_file("patterns.json")
```

**Search Knowledge Base:**
```python
from knowledge_system import knowledge_base

results = knowledge_base.search_knowledge(
    query="binary search",
    category="code_patterns",
    limit=5
)

for result in results:
    print(f"{result['title']}: {result['description']}")
```

### Pattern Structure

Each code pattern includes:
- **Pattern Name**: Descriptive name
- **Language**: Programming language
- **Code Snippet**: Working code example
- **Description**: What it does
- **Use Case**: When to use it
- **Tags**: Searchable categories
- **Success Rate**: Tracked based on usage

### Extending the Knowledge Base

Add your own patterns:

```python
from knowledge_system import knowledge_base

knowledge_base.add_code_pattern(
    pattern_name="My Custom Pattern",
    language="Python",
    code_snippet="# Your code here",
    description="What it does",
    use_case="When to use",
    tags=["custom", "utility"]
)
```

---

## Improved Prompts

### Overview

Enhanced system prompts for better understanding of user intent.

### Key Improvements

1. **Intent Analysis**
   - Information seeking
   - Code generation
   - Project creation
   - Troubleshooting
   - Modifications

2. **Communication Guidelines**
   - Conversational but precise
   - Asks clarifying questions
   - Explains reasoning
   - Acknowledges limitations

3. **Context Awareness**
   - Leverages knowledge base
   - Applies past learnings
   - Considers user preferences

### Prompt Structure

```python
"""
UNDERSTANDING USER INTENT:
Before taking action, analyze what the user really wants:
1. Are they asking for information? → Search knowledge base
2. Do they want code written? → Ask clarifying questions
3. Are they requesting a project? → Identify scope
4. Do they want modifications? → Understand what to change
5. Are they troubleshooting? → Identify the problem first

COMMUNICATION GUIDELINES:
- Be conversational but precise
- If requirements are unclear, ask specific questions
- Break complex tasks into steps
- Explain your reasoning
- Acknowledge limitations honestly
"""
```

### Model Selection

BECA automatically selects the best model:

- **llama3.1:8b**: General tasks, reasoning, tool use
- **qwen2.5-coder:7b-instruct**: Code generation, debugging

The model is chosen based on keywords in your message:
- "write code", "create function", "debug" → Uses coder model
- General questions, file operations → Uses general model

### Customization

Modify the prompt in `src/langchain_agent.py`:

```python
react_prompt_template = """
Your custom instructions here...
"""
```

---

## Virtual Environment

### Benefits

- ✅ Dependency isolation
- ✅ No system Python conflicts
- ✅ Reproducible deployments
- ✅ Version control
- ✅ Multiple projects possible

### Setup

```bash
# Create
python -m venv beca-env

# Activate (Windows)
beca-env\Scripts\activate

# Activate (Linux/Mac)
source beca-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### Auto-Activation Scripts

**Windows (start-beca-enhanced.bat):**
```batch
@echo off
call beca-env\Scripts\activate.bat
python beca_gui_enhanced.py
```

**Linux/Mac (start-beca-enhanced.sh):**
```bash
#!/bin/bash
source beca-env/bin/activate
python beca_gui_enhanced.py
```

### Updating Dependencies

```bash
# Activate environment
source beca-env/bin/activate  # or beca-env\Scripts\activate

# Update a package
pip install --upgrade package-name

# Update all packages
pip install --upgrade -r requirements.txt

# Save current state
pip freeze > requirements.txt
```

---

## Testing & Troubleshooting

### Testing New Features

**Terminal Manager:**
```bash
cd src
python -m pytest test_terminal_manager.py
```

**File Uploader:**
```python
from file_uploader import file_uploader

# Test supported extensions
print(file_uploader.SUPPORTED_EXTENSIONS)

# Test upload
result = file_uploader.process_upload(
    open("test.pdf", "rb"),
    "test.pdf"
)
```

**Dataset Loader:**
```python
from dataset_loader import dataset_loader

results = dataset_loader.load_all_builtin_datasets()
print(f"Loaded {sum(results.values())} total patterns")
```

### Common Issues

**Issue: File upload fails**
- Check file extension is supported
- Ensure required library is installed (PyPDF2, python-docx, etc.)
- Try with a smaller file

**Issue: Google Drive auth fails**
- Verify credentials.json exists
- Check API is enabled in Google Cloud Console
- Delete token.pickle and re-authenticate

**Issue: Terminal output not showing**
- Check terminal_manager is imported correctly
- Verify commands are executing (check return values)
- Look for encoding issues on Windows

**Issue: Stop button doesn't work**
- Ensure threading.Event is being checked in long operations
- Verify stop_flag is set before termination
- Check process.terminate() is called

### Getting Help

1. Check the logs in the terminal
2. Review error messages in the GUI
3. Test individual components in Python console
4. Check GitHub issues for similar problems

---

## Next Steps

1. **Try the Enhanced GUI:**
   ```bash
   python beca_gui_enhanced.py
   ```

2. **Upload a test file**
3. **Load the built-in datasets**
4. **Try the stop button**
5. **Set up Google Drive** (optional)

## Additional Resources

- [BECA Main Documentation](readme.md)
- [Meta-Learning Guide](META-LEARNING-GUIDE.md)
- [Autonomous Learning](AUTONOMOUS-LEARNING.md)
- [Knowledge System](KNOWLEDGE-SYSTEM-SUMMARY.md)

---

**Last Updated:** October 16, 2025
**Version:** 2.0 - Enhanced Features Release
