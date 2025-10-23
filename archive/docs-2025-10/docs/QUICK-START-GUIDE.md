# BECA Enhanced GUI - Quick Start Guide

> **⚠️ DEPRECATED - This guide is for the old Gradio-based GUI**
> 
> **BECA now uses a modern React frontend + FastAPI backend architecture.**
> 
> **📖 See [START-BECA.md](../START-BECA.md) for current usage instructions.**
> 
> **Quick Start:** Run `start-beca.bat` and access http://34.55.204.139:3000
> 
> This document is kept for historical reference only.

---

## 🚀 Launch the Enhanced GUI (OLD - Gradio)

```bash
cd c:\dev
python beca_gui.py
```

Then open your browser to: **http://127.0.0.1:7860**

> **Note:** This local Gradio GUI has been replaced by a cloud-based Docker deployment with React frontend (port 3000) and FastAPI backend (port 8000).

---

## 📐 Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 BECA - Badass Expert Coding Agent                           │
│  Your personal AI coding assistant with visual file management  │
├─────────────────────────────────────────────────────────────────┤
│  Status: Ready                                                  │
├──────────────┬──────────────────────────┬──────────────────────┤
│              │                          │                      │
│  📁 PROJECT  │    💬 CHAT               │  📝 CODE VIEW        │
│    FILES     │                          │                      │
│              │                          │  [View File] [Diff]  │
│  📂 src/     │  You: Create a todo app  │                      │
│   🐍 gui.py  │                          │  File Path:          │
│   🐍 agent.py│  BECA: I'll create...    │  [____________]      │
│              │                          │  [View] [Refresh]    │
│  📂 beca/    │  BECA: ✓ Created files   │                      │
│   📄 NEW     │        - todo-app/       │  ┌─────────────────┐ │
│              │        - src/App.jsx     │  │ Syntax          │ │
│  📄 app.py   │                          │  │ Highlighted     │ │
│  📄 test.py  │  [Your Message____]      │  │ Code            │ │
│              │  [Send]                  │  │ Display         │ │
│  [🔄 Refresh]│                          │  └─────────────────┘ │
│              │  [Clear Chat]            │                      │
│              │                          │                      │
└──────────────┴──────────────────────────┴──────────────────────┘
```

---

## 🎯 Step-by-Step Tutorial

### Step 1: View Your Project Structure
Look at the **left panel** - you'll see your entire project file tree with:
- 📁 Folders (expandable)
- 📄 Files with type icons (🐍 Python, 📜 JS, etc.)
- File sizes
- Status badges (🟢 NEW, 🟡 MODIFIED)

### Step 2: Chat with BECA
In the **middle panel**, try these examples:

**Example 1: Create a new file**
```
You: Create a Flask API file called api.py with a health check endpoint
```
→ Watch the file tree update with api.py marked as NEW!

**Example 2: Modify existing file**
```
You: Add error handling to src/langchain_agent.py
```
→ The file gets a MODIFIED badge in the tree

**Example 3: Ask for code review**
```
You: Review the code in beca_gui.py and suggest improvements
```

### Step 3: View Syntax-Highlighted Code
In the **right panel**, "View File" tab:

1. Type a file path: `beca_gui.py`
2. Click **View**
3. See beautifully highlighted code with line numbers!

**Supported files:**
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- HTML, CSS, JSON, YAML
- And 200+ more languages!

### Step 4: Compare Changes (Diff)
After BECA modifies a file:

1. Switch to the **Diff** tab (right panel)
2. Enter the modified file path: `api.py`
3. Click **Show Diff**
4. See color-coded changes:
   - 🟢 Green = Added lines
   - 🔴 Red = Removed lines
   - ⚪ White = Unchanged context

---

## 💡 Pro Tips

### Tip 1: Keep the File Tree Fresh
- File tree auto-refreshes after BECA operations
- Click 🔄 **Refresh Tree** button anytime for manual update
- NEW badges = files just created
- MODIFIED badges = files just changed

### Tip 2: View Files Quickly
- Copy path from chat (e.g., "Created src/main.py")
- Paste into Code Viewer
- Click View
- See the code instantly!

### Tip 3: Track Your Changes
- Before asking BECA to modify a file, **view it first**
- This stores the original content
- After modification, check the **Diff** tab
- You'll see exactly what changed!

### Tip 4: Use Examples
- Click "💡 Examples & Help" accordion at bottom
- Click any example to auto-fill the chat input
- Modify and send!

---

## 🎬 Common Workflows

### Workflow 1: Create a New Project
```
1. You: "Create a FastAPI project called blog-api"
2. Watch file tree populate with new files
3. View main.py in Code Viewer
4. You: "Add authentication endpoints"
5. Check Diff to see what was added
```

### Workflow 2: Debug Existing Code
```
1. View problematic file in Code Viewer
2. You: "Find bugs in src/agent.py"
3. BECA analyzes and suggests fixes
4. You: "Apply those fixes"
5. View Diff to verify changes
```

### Workflow 3: Code Review
```
1. You: "Review all Python files for improvements"
2. BECA analyzes project
3. View each mentioned file
4. You: "Apply suggestions to src/tools.py"
5. Check Diff for confidence
```

---

## 🐛 Troubleshooting

### File Tree Not Showing Files?
- Click the 🔄 **Refresh Tree** button
- Check that you're in the correct working directory
- Large projects may take a moment to scan

### Code Not Highlighted?
- Ensure file extension is recognized (.py, .js, etc.)
- Binary files will show "cannot display" message
- Very large files may show simplified view

### Diff Not Working?
- You must **view the file first** (this caches original)
- Then have BECA modify it (or edit externally)
- Then click **Show Diff**

### Status Bar Shows Error?
- Check the error message in status bar
- Verify file path is correct
- Ensure file exists and is readable

---

## 🎨 Customization Ideas

### Future Enhancements You Could Add:
1. **Dark/Light theme toggle**
2. **Font size adjustment**
3. **Click file in tree → auto-view**
4. **Search in file tree**
5. **Multi-tab code viewing**
6. **Export diff to file**

---

## 📚 Learn More

- **Full Documentation**: See `GUI-ENHANCEMENT-COMPLETE.md`
- **Original Plan**: See `BECA-GUI-ENHANCEMENT-PLAN.md`
- **Test the Components**: Run `python test_gui.py`
- **Main GUI Code**: Check `beca_gui.py`
- **Utilities**: Explore `src/gui_utils.py`

---

## 🎉 You're Ready!

The enhanced BECA GUI gives you:
- ✅ **Visual project overview** (file tree)
- ✅ **Beautiful code display** (syntax highlighting)
- ✅ **Change tracking** (diff viewer)
- ✅ **Real-time updates** (auto-refresh)
- ✅ **Professional interface** (modern design)

**Now start building amazing projects with BECA! 🚀**

---

## 📞 Need Help?

If you encounter issues:
1. Run the test suite: `python test_gui.py`
2. Check console output for errors
3. Verify all dependencies installed: `pip install -r requirements.txt`
4. Review the status bar messages in the GUI

Happy coding! 🎊
