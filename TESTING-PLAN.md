# 🧪 BECA GUI Enhancement - Testing Plan

## Document Information
- **Project**: BECA GUI Enhancement
- **Version**: 1.0
- **Date**: 2025-10-06
- **Status**: Active Testing Phase

---

## Executive Summary

This document outlines the comprehensive testing strategy for the BECA GUI enhancements, covering all three implemented phases (File Tree Panel, Code Viewer, Diff Viewer) plus integration testing with the BECA agent.

**Test Coverage:**
- Unit Tests (Component-level)
- Integration Tests (Component interaction)
- End-to-End Tests (Full workflows)
- Manual Tests (UI/UX verification)
- Edge Case Tests (Error handling)
- Performance Tests (Load & stress)

---

## Test Environment

### Prerequisites
- Python 3.8+
- All dependencies installed (`pip install -r requirements.txt`)
- Ollama running (for agent tests)
- Working directory: `c:\dev`

### Test Execution Command
```bash
# Run specific test suite
python test_gui.py              # Unit tests
python test_gui_integration.py  # Integration tests
python test_gui_e2e.py          # End-to-end tests
python test_edge_cases.py       # Edge cases

# Run all tests
python -m pytest test_*.py -v   # If using pytest
```

---

## Test Categories & Priority

### Priority Levels
- **P0 (Critical)**: Must pass - blocking issues
- **P1 (High)**: Should pass - major features
- **P2 (Medium)**: Important but not blocking
- **P3 (Low)**: Nice to have - enhancements

---

## Phase 1: Unit Tests (Component-level)

**File:** `test_gui.py` (Already created)

### Test 1.1: Module Imports (P0)
```python
✓ Import gui_utils module
✓ Import file_tracker module
✓ Import langchain_tools with file tracking
✓ All modules load without errors
```

### Test 1.2: FileTreeManager (P0)
```python
✓ Build file tree from current directory
✓ Generate HTML from tree structure
✓ File tree contains expected folders
✓ File tree filters ignored directories (.git, node_modules)
✓ File icons display correctly for different types
✓ File size formatting works (B, KB, MB)
```

### Test 1.3: CodeViewer (P0)
```python
✓ Highlight Python code with Pygments
✓ Highlight JavaScript/TypeScript code
✓ Auto-detect programming language
✓ Line numbers display correctly
✓ Fallback for unknown languages
✓ Binary file detection
✓ Empty file handling
```

### Test 1.4: DiffViewer (P0)
```python
✓ Generate unified diff format
✓ Color-code additions (green)
✓ Color-code deletions (red)
✓ Handle no changes scenario
✓ HTML escape special characters
```

### Test 1.5: FileOperationTracker (P1)
```python
✓ Mark file as created
✓ Mark file as modified
✓ Clear file status
✓ Get file status (new/modified/normal)
✓ Relative path conversion
```

---

## Phase 2: Integration Tests

**File:** `test_gui_integration.py` (To be created)

### Test 2.1: GUI Functions Integration (P0)
```python
- refresh_file_tree() syncs with file tracker
- view_file() stores content for diffing
- show_diff() compares original vs modified
- chat_with_beca() updates file tree after response
```

### Test 2.2: File Tracker ↔ Tools Integration (P1)
```python
- write_file() marks new files as created
- write_file() marks existing files as modified
- create_react_app() marks all created files
- File tree shows NEW badges for tracker-created files
- File tree shows MODIFIED badges for tracker-modified files
```

### Test 2.3: File Tracker ↔ FileTreeManager Sync (P1)
```python
- FileTreeManager reads tracker status
- NEW files get green badges
- MODIFIED files get yellow badges
- Status persists across refreshes
- Clear status removes badges
```

### Test 2.4: Code Viewer ↔ Diff Viewer (P2)
```python
- View file stores original content
- Modify file externally
- Diff shows changes correctly
- Refresh updates both viewers
```

---

## Phase 3: End-to-End Tests

**File:** `test_gui_e2e.py` (To be created)

### Test 3.1: Create New File Workflow (P0)
```
User Story: As a user, I want to see newly created files in the file tree

Steps:
1. Start with clean state
2. Use write_file() to create "test_new.py"
3. Call refresh_file_tree()
4. Verify file appears in tree HTML
5. Verify NEW badge is present
6. View file with code viewer
7. Verify syntax highlighting applied
```

### Test 3.2: Modify Existing File Workflow (P0)
```
User Story: As a user, I want to track changes to existing files

Steps:
1. View existing file (e.g., beca_gui.py)
2. Store original content via view_file()
3. Modify file content with write_file()
4. Call refresh_file_tree()
5. Verify MODIFIED badge appears
6. Use show_diff() to compare
7. Verify diff shows changes in green/red
```

### Test 3.3: Create Project Structure Workflow (P1)
```
User Story: As a user, I want to see entire project structures created

Steps:
1. Use create_react_app("test-app")
2. Verify multiple files created
3. Call refresh_file_tree()
4. Verify folder structure appears
5. Verify all files have NEW badges
6. View package.json
7. Verify JSON syntax highlighting
```

### Test 3.4: File Tree Refresh Workflow (P1)
```
User Story: As a user, I want to manually refresh the file tree

Steps:
1. Note current tree state
2. Create file externally (outside tracker)
3. Call refresh_file_tree()
4. Verify new file appears
5. Verify no badge (tracker didn't create it)
```

### Test 3.5: Multi-File Operation Workflow (P2)
```
User Story: As a user, I want to track multiple file operations

Steps:
1. Create 5 new files rapidly
2. Modify 3 existing files
3. Call refresh_file_tree()
4. Verify 5 NEW badges
5. Verify 3 MODIFIED badges
6. View each file to verify highlighting
```

---

## Phase 4: Manual UI/UX Tests

**Execution:** Manual testing in browser

### Test 4.1: Layout & Responsiveness (P1)
```
Visual Checks:
□ Three panels display correctly (File Tree | Chat | Code)
□ Panel proportions correct (1:2:2 scale)
□ Status bar visible at top
□ Status bar updates during operations
□ Help section expands/collapses smoothly
□ Scrolling works in all panels
□ No horizontal overflow
□ Responsive on different window sizes
```

### Test 4.2: File Tree Visual Elements (P1)
```
Visual Checks:
□ Folder icons (📁) render correctly
□ File type icons render (🐍 Python, 📜 JS, etc.)
□ NEW badge is green with white text
□ MODIFIED badge is yellow with black text
□ File sizes display correctly (e.g., "1.2KB")
□ Folder expand/collapse animations smooth
□ Tree indentation is clear and consistent
□ Refresh button works and shows feedback
```

### Test 4.3: Code Viewer Visual Elements (P1)
```
Visual Checks:
□ Syntax highlighting uses Monokai colors
□ Line numbers visible and aligned
□ Code font is monospace and readable
□ Scrolling works for long files
□ Tab switching (View File ↔ Diff) smooth
□ Input fields accept text
□ Buttons respond on click
□ File path validation works
```

### Test 4.4: Diff Viewer Visual Elements (P2)
```
Visual Checks:
□ Added lines have green background
□ Deleted lines have red background
□ Context lines visible in white/gray
□ Diff header shows file names
□ Line markers (@@) visible
□ Scrolling works for long diffs
□ "No changes" message displays when equal
□ HTML special chars escaped properly
```

### Test 4.5: Chat Integration Visual (P0)
```
Visual Checks:
□ Chat messages display correctly
□ User messages appear immediately
□ Assistant messages stream in
□ Tool execution results show
□ File tree updates after chat response
□ Status bar updates during chat
□ Copy button on messages works
□ Input clears after send
```

---

## Phase 5: Edge Case Tests

**File:** `test_edge_cases.py` (To be created)

### Test 5.1: File System Edge Cases (P2)
```python
- View non-existent file → Error message
- View binary file (PNG) → "Binary file" message
- View empty file → Display empty or placeholder
- View file with Unicode/emoji → Proper encoding
- File with very long name (>255 chars) → Handled
- Deep folder nesting (>10 levels) → Handled or limited
- Folder with 1000+ files → Performance acceptable
```

### Test 5.2: Code Viewer Edge Cases (P2)
```python
- File with no extension → Fallback to plain text
- File with unknown extension (.xyz) → Plain text
- Very long lines (>1000 chars) → Wrapped or scrollable
- File with tabs and spaces mixed → Displays correctly
- File with syntax errors → Still highlights
- Large file (>5MB) → Handled or shows warning
```

### Test 5.3: Diff Viewer Edge Cases (P2)
```python
- Diff before viewing file → Error or instruction
- Diff unchanged file → "No changes" message
- Diff with only whitespace changes → Shows correctly
- Diff entire file deleted → Red for all lines
- Diff entire file added → Green for all lines
- Diff with encoding changes → Handles gracefully
```

### Test 5.4: File Tracker Edge Cases (P2)
```python
- Track file in non-existent directory → Handles path
- Track file with special chars (!, @, #) → Works
- Track 100 files rapidly → No performance issues
- Clear status on non-tracked file → No error
- Get status of non-existent file → Returns 'normal'
```

### Test 5.5: Error Handling (P1)
```python
- GUI utils not available → Fallback message
- File tracker not available → Graceful degradation
- Pygments not installed → Plain text fallback
- Invalid file path entered → Clear error message
- Permission denied on file → Error message
- Disk full scenario → Error message
- Network timeout (if applicable) → Timeout message
```

---

## Phase 6: Performance Tests

**Execution:** Automated with timing measurements

### Test 6.1: Load Time Tests (P2)
```python
Metrics:
- GUI startup time < 5 seconds
- File tree generation (100 files) < 2 seconds
- Code highlighting (1000 lines) < 1 second
- Diff generation (500 changes) < 1 second
- Refresh file tree < 2 seconds
```

### Test 6.2: Stress Tests (P3)
```python
Scenarios:
- File tree with 1000+ files → Still responsive
- Highlight file with 10,000 lines → Completes
- Generate diff with 5,000 changes → Completes
- Rapid refresh (10x in 10 seconds) → No crashes
- Create 100 files in sequence → All tracked
```

### Test 6.3: Memory Tests (P3)
```python
Metrics:
- Memory usage at startup < 200MB
- Memory after 100 operations < 500MB
- No memory leaks after repeated operations
- File content cache doesn't grow unbounded
```

---

## Phase 7: Cross-Platform Tests

### Test 7.1: Windows Tests (P0 - Primary)
```
Platform: Windows 10/11
- All features work correctly
- UTF-8 encoding handles emoji
- Path separators (\) work
- PowerShell files recognized (.ps1)
- Console output displays correctly
```

### Test 7.2: Linux Tests (P2)
```
Platform: Ubuntu 20.04+ / Debian
- All features work correctly
- UTF-8 encoding handles emoji
- Path separators (/) work
- Shell scripts recognized (.sh)
- Terminal output displays correctly
```

### Test 7.3: macOS Tests (P2)
```
Platform: macOS 11+
- All features work correctly
- UTF-8 encoding handles emoji
- Path separators (/) work
- Shell scripts recognized (.sh)
- Terminal output displays correctly
```

---

## Phase 8: Regression Tests

### Test 8.1: Original Features Still Work (P0)
```python
- Basic chat with BECA → Works
- Memory tools → Work
- Web search tool → Works
- Git operations → Work
- File read/write → Works
- Code analysis tools → Work
- Test generation → Works
```

### Test 8.2: Backward Compatibility (P1)
```python
- GUI works with gui_utils disabled → Fallback
- GUI works with file_tracker disabled → Fallback
- Agent works without GUI utilities → No errors
- Clear chat still works → Works
- Examples still populate input → Works
```

---

## Test Execution Order

### Day 1: Foundation Tests
1. ✓ Run existing unit tests (`test_gui.py`)
2. Create and run integration tests
3. Document any failures

### Day 2: Workflow Tests
4. Create and run E2E tests
5. Execute manual UI/UX tests
6. Document any issues

### Day 3: Edge Cases & Performance
7. Create and run edge case tests
8. Run performance tests
9. Document metrics

### Day 4: Final Validation
10. Run regression tests
11. Cross-platform testing (if applicable)
12. Create final test report

---

## Success Criteria

### ✅ Tests Pass If:
- **100%** of P0 (Critical) tests pass
- **90%+** of P1 (High) tests pass
- **75%+** of P2 (Medium) tests pass
- **50%+** of P3 (Low) tests pass
- No critical bugs (crash, data loss, security)
- Performance targets met
- All documentation complete

### 🐛 Bug Severity Levels
- **Critical**: GUI doesn't start, data loss, security issue
- **High**: Major feature broken, no workaround
- **Medium**: Feature partially broken, workaround exists
- **Low**: Minor UI issue, cosmetic problem

---

## Test Deliverables

### Test Artifacts:
1. ✓ `test_gui.py` - Unit tests (exists)
2. `test_gui_integration.py` - Integration tests
3. `test_gui_e2e.py` - End-to-end tests
4. `test_edge_cases.py` - Edge case tests
5. `TEST-RESULTS.md` - Test execution results
6. `TEST-REPORT-[DATE].md` - Detailed report
7. Screenshots (if failures)
8. Performance metrics

---

## Next Steps After Testing

### If All Tests Pass:
1. Mark all tests as ✓ Pass in TEST-RESULTS.md
2. Create TEST-REPORT with summary
3. Update README with test status badge
4. Mark GUI as production-ready
5. Create release notes

### If Tests Fail:
1. Log failures in TEST-RESULTS.md
2. Prioritize by severity (Critical → Low)
3. Create bug fix issues
4. Fix bugs in priority order
5. Re-run failed tests
6. Repeat until success criteria met

---

## Test Contacts

**Test Lead:** Claude
**Developers:** Claude
**Stakeholders:** User
**Date Started:** 2025-10-06

---

## Appendix A: Test Data

### Sample Files for Testing:
- **Python**: `beca_gui.py`, `src/langchain_agent.py`
- **JavaScript**: Create `test.js`, `test.jsx`
- **Markdown**: `README.md`, `TESTING-PLAN.md`
- **JSON**: `requirements.txt` (test as JSON)
- **Binary**: Any `.png` or `.jpg` file
- **Large**: Generate 10MB+ text file
- **Unicode**: File with emoji in content

### Sample Directories:
- `.git` (should be ignored)
- `node_modules` (should be ignored)
- `src/` (should be displayed)
- `__pycache__` (should be ignored)

---

## Appendix B: Manual Test Checklist

Print and check off during manual testing:

```
□ GUI launches without errors
□ File tree displays on left
□ Chat panel displays in center
□ Code viewer displays on right
□ Status bar shows "Ready"
□ Help section expands
□ Refresh tree button works
□ View file button works
□ Show diff button works
□ Clear chat button works
□ Send message button works
□ Examples populate input
□ File tree shows folders
□ File tree shows files
□ File icons display
□ NEW badge shows green
□ MODIFIED badge shows yellow
□ Code has syntax colors
□ Line numbers visible
□ Diff shows green/red
□ All text readable
□ No console errors
□ No broken images
□ No layout issues
□ Scrolling works everywhere
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-06
**Status:** Ready for Test Execution
