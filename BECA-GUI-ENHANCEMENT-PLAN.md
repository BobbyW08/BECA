# BECA GUI Enhancement Plan

Plan to add visual features to BECA for better user experience.

---

## Current State

BECA currently uses a simple Gradio chat interface that is **text-only**:
- ✅ Works well for conversation
- ✅ Shows tool execution results as text
- ❌ No file tree visualization
- ❌ No syntax-highlighted code preview
- ❌ No visual diff comparisons
- ❌ No inline code editing

**User Feedback:** Users want to SEE their code like in Claude Code, not just read text descriptions.

---

## Proposed Enhancements

### Phase 1: File Tree Panel (High Priority)

**Goal:** Show project structure visually

**Implementation:**
1. Add a left sidebar panel to Gradio interface
2. Use Gradio's `gr.JSON()` or custom HTML component
3. Display file tree with:
   - 📁 Expandable/collapsible folders
   - 📄 File icons by type (.jsx, .py, .md, etc.)
   - 🟢 Green highlight for newly created files
   - 🟡 Yellow highlight for modified files

**Integration with Agent:**
- After each file operation, update the tree
- Allow users to click files to view contents
- Show current working directory

**Estimated Effort:** 2-3 hours

### Phase 2: Syntax-Highlighted Code Viewer (High Priority)

**Goal:** Show code with proper formatting

**Implementation:**
1. Use Monaco Editor (VS Code's editor) as a Gradio component
2. Or use Prism.js/Highlight.js for read-only highlighting
3. Display in right panel when user asks to "show" a file
4. Support popular languages: JavaScript, Python, TypeScript, CSS, HTML, JSON

**Features:**
- Read-only view (no editing yet)
- Line numbers
- Proper indentation
- Language-specific coloring
- Copy button

**Integration with Agent:**
- When BECA reads a file, display it formatted
- Auto-detect language from file extension
- Allow scrolling for long files

**Estimated Effort:** 2-4 hours

### Phase 3: Side-by-Side Diff Viewer (Medium Priority)

**Goal:** Show before/after comparisons visually

**Implementation:**
1. Use Monaco Diff Editor or similar
2. Show old vs new side-by-side
3. Highlight additions (green) and deletions (red)
4. Line-by-line comparison

**Integration with Agent:**
- Before modifying files, store original content
- After modification, show diff automatically
- Option to accept/reject changes (future enhancement)

**Estimated Effort:** 3-5 hours

### Phase 4: Inline Code Editing (Low Priority - Complex)

**Goal:** Edit code directly in BECA interface

**Implementation:**
1. Make Monaco Editor editable
2. Add "Save" button
3. Add "Ask BECA to improve this" button
4. Sync changes with filesystem

**Challenges:**
- File watching and auto-reload
- Conflict resolution if file changed externally
- Multi-file editing state management

**Estimated Effort:** 8-12 hours

---

## Technical Approach

### Option A: Enhance Gradio Interface (Recommended)

**Pros:**
- Keep existing codebase
- Gradio 4.x supports custom components
- Can embed HTML/JavaScript
- Easier to maintain

**Cons:**
- Limited by Gradio's capabilities
- May need custom components
- Performance concerns with large files

**Implementation:**
```python
import gradio as gr
from gradio import Blocks, Chatbot, Textbox, Row, Column

with gr.Blocks() as demo:
    with gr.Row():
        # Left: File Tree
        with gr.Column(scale=1):
            file_tree = gr.JSON(label="Project Files")

        # Middle: Chat
        with gr.Column(scale=2):
            chatbot = gr.Chatbot()
            msg = gr.Textbox()

        # Right: Code Viewer
        with gr.Column(scale=2):
            code_viewer = gr.Code(language="python", label="Code Preview")
```

### Option B: Custom Web App (More Work)

**Pros:**
- Complete control over UI
- Better performance
- Modern frameworks (React, Vue)
- Professional appearance

**Cons:**
- Rewrite entire GUI
- Need frontend expertise
- More maintenance burden
- Longer development time

**Tech Stack:**
- Frontend: React + Vite
- Code Editor: Monaco Editor
- File Tree: react-complex-tree
- Backend API: FastAPI (replace Gradio)

---

## Implementation Roadmap

### Week 1: File Tree Panel
- [ ] Design file tree data structure
- [ ] Create file system watcher
- [ ] Build Gradio file tree component
- [ ] Integrate with existing chat interface
- [ ] Test with multiple projects

### Week 2: Code Syntax Highlighting
- [ ] Research Monaco Editor integration with Gradio
- [ ] Create code viewer component
- [ ] Add language detection
- [ ] Wire up to agent's file operations
- [ ] Test with various file types

### Week 3: Diff Viewer
- [ ] Implement file change tracking
- [ ] Create diff component
- [ ] Add before/after comparison
- [ ] Test with file modifications
- [ ] Add user preferences (show diff always/on request)

### Week 4 (Optional): Polish & Testing
- [ ] Add keyboard shortcuts
- [ ] Improve mobile responsiveness
- [ ] Performance optimization
- [ ] User testing and feedback
- [ ] Documentation updates

---

## Required Dependencies

```txt
# Add to requirements.txt
gradio>=4.0.0
pygments  # For syntax highlighting fallback
watchdog  # For file system watching
```

### Optional (for advanced features):
```txt
monaco-editor-wrapper  # If using Monaco
diff-match-patch  # For better diff algorithms
```

---

## User Experience Mockup

```
┌─────────────────────────────────────────────────────────────┐
│  BECA - Badass Expert Coding Agent           🟢 Connected   │
├──────────┬──────────────────────────────┬───────────────────┤
│          │                              │                   │
│ 📁 Files │  💬 Chat                     │  📝 Code View     │
│          │                              │                   │
│ 📂 src/  │  You: Create a navbar        │  ```jsx           │
│  📄 App  │                              │  export default   │
│  📄 main │  BECA: ✓ Created Navbar.jsx  │  function Navbar  │
│  📂 comp │                              │    return (       │
│   📄 Nav │  [Shows file tree highlight] │      <nav>...     │
│          │                              │                   │
│ 📂 public│  You: Show me Navbar.jsx     │  [Syntax colored] │
│  📄 index│                              │                   │
│          │  BECA: [Displays code →]     │  [Line numbers]   │
│          │                              │                   │
└──────────┴──────────────────────────────┴───────────────────┘
```

---

## Success Metrics

### Phase 1 Success:
- ✅ File tree updates in real-time
- ✅ Users can see project structure at a glance
- ✅ Newly created files are visually highlighted

### Phase 2 Success:
- ✅ Code displays with proper syntax highlighting
- ✅ Supports at least 10 common languages
- ✅ Readable and matches VS Code appearance

### Phase 3 Success:
- ✅ Diffs show clearly what changed
- ✅ Users can review changes before accepting
- ✅ Side-by-side comparison is intuitive

---

## Risks & Mitigation

### Risk 1: Gradio Limitations
**Mitigation:** Research custom components early, have fallback to simpler visualizations

### Risk 2: Performance with Large Files
**Mitigation:** Implement lazy loading, limit file preview to first 1000 lines

### Risk 3: File Synchronization Issues
**Mitigation:** Use file system watchers, add refresh button as backup

### Risk 4: Cross-Platform Compatibility
**Mitigation:** Test on Windows, Mac, Linux early in development

---

## Alternative: Integrate with VS Code Extension

**Concept:** Instead of building a web GUI, create a VS Code extension that:
- Shows BECA chat in VS Code sidebar
- Uses VS Code's native file tree
- Leverages VS Code's editor for viewing/editing
- Integrates with VS Code's diff viewer

**Pros:**
- Don't reinvent the wheel
- Users already use VS Code
- Professional appearance out-of-the-box
- Access to VS Code API

**Cons:**
- Requires TypeScript/VS Code extension development
- Tied to VS Code only
- More complex deployment
- Learning curve for extension development

---

## Next Steps

1. **Get User Feedback:** Which features are most important?
2. **Choose Approach:** Enhanced Gradio vs Custom App vs VS Code Extension
3. **Prototype:** Build minimal file tree to validate approach
4. **Iterate:** Add features based on feedback
5. **Document:** Update user guide with new visual features

---

## Questions for Discussion

1. Should we keep Gradio or build a custom React app?
2. Is editing in BECA necessary, or is viewing enough?
3. Should we prioritize mobile/tablet support?
4. Do we want multi-tab support (work on multiple files)?
5. Should there be a light/dark theme toggle?

---

**Created:** 2025-10-06
**Status:** Planning Phase
**Estimated Total Effort:** 15-25 hours for Phases 1-3
**Target Completion:** TBD based on priorities
