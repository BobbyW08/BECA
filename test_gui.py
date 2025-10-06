"""
Quick test script to verify GUI enhancements are working
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing GUI components...")

# Test 1: Import all modules
print("\n1. Testing imports...")
try:
    from gui_utils import file_tree_manager, code_viewer, diff_viewer
    from file_tracker import file_tracker
    print("   ✓ All modules imported successfully")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Build file tree
print("\n2. Testing file tree generation...")
try:
    tree = file_tree_manager.build_tree(max_depth=2)
    html = file_tree_manager.to_html(tree)
    assert len(html) > 100, "File tree HTML too short"
    print(f"   ✓ Generated file tree ({len(html)} chars)")
except Exception as e:
    print(f"   ✗ File tree failed: {e}")
    sys.exit(1)

# Test 3: Test code highlighting
print("\n3. Testing code viewer...")
try:
    test_code = "def hello():\n    print('Hello, World!')\n"
    highlighted = code_viewer.highlight_code(test_code, language='python')
    assert 'def' in highlighted
    print(f"   ✓ Code highlighting works ({len(highlighted)} chars)")
except Exception as e:
    print(f"   ✗ Code viewer failed: {e}")
    sys.exit(1)

# Test 4: Test diff viewer
print("\n4. Testing diff viewer...")
try:
    old_code = "line 1\nline 2\nline 3\n"
    new_code = "line 1\nline 2 modified\nline 3\nline 4\n"
    diff_html = diff_viewer.generate_diff(old_code, new_code, "test.py")
    assert 'modified' in diff_html or 'line 2' in diff_html
    print(f"   ✓ Diff generation works ({len(diff_html)} chars)")
except Exception as e:
    print(f"   ✗ Diff viewer failed: {e}")
    sys.exit(1)

# Test 5: Test file tracker
print("\n5. Testing file tracker...")
try:
    file_tracker.mark_file_created("test_file.py")
    status = file_tracker.get_status("test_file.py")
    assert status == 'new', f"Expected 'new', got '{status}'"
    file_tracker.clear_status()
    print("   ✓ File tracker works")
except Exception as e:
    print(f"   ✗ File tracker failed: {e}")
    sys.exit(1)

# Test 6: Test reading an actual file
print("\n6. Testing file reading...")
try:
    html, error = code_viewer.read_and_highlight("beca_gui.py")
    assert error is None, f"Got error: {error}"
    assert len(html) > 100, "Highlighted HTML too short"
    print(f"   ✓ File reading and highlighting works")
except Exception as e:
    print(f"   ✗ File reading failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ All tests passed! GUI enhancements are working.")
print("="*50)
print("\nYou can now run: python beca_gui.py")
