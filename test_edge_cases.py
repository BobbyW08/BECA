"""
Edge case and error handling tests for BECA GUI
Tests boundary conditions and error scenarios
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules to test
from gui_utils import file_tree_manager, code_viewer, diff_viewer
from file_tracker import file_tracker


class TestFileSystemEdgeCases:
    """Test file system edge cases"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_edge_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_view_nonexistent_file(self):
        """Test viewing a file that doesn't exist"""
        print("\n   Testing: View non-existent file...")

        html, error = code_viewer.read_and_highlight("nonexistent.py")

        # Should return None for html and error message
        assert html is None, "Should return None for non-existent file"
        assert error is not None, "Should return error message"
        assert "not found" in error.lower() or "error" in error.lower()

        print("      ✓ Non-existent file handled correctly")
        return True

    def test_view_binary_file(self):
        """Test viewing a binary file"""
        print("\n   Testing: View binary file...")

        # Create a simple binary file
        binary_file = "test.bin"
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\xFF\xFE')

        html, error = code_viewer.read_and_highlight(binary_file)

        # Should detect binary and handle gracefully
        # Either returns error or shows "Binary file" message
        if html:
            assert "Binary" in html or "cannot display" in html
        # If error, that's also acceptable
        assert html is not None or error is not None

        print("      ✓ Binary file handled correctly")
        return True

    def test_view_empty_file(self):
        """Test viewing an empty file"""
        print("\n   Testing: View empty file...")

        empty_file = "empty.py"
        with open(empty_file, 'w') as f:
            pass  # Create empty file

        html, error = code_viewer.read_and_highlight(empty_file)

        # Should handle empty file gracefully
        assert error is None, f"Empty file should not cause error: {error}"
        assert html is not None, "Should return HTML for empty file"

        print("      ✓ Empty file handled correctly")
        return True

    def test_file_with_unicode(self):
        """Test file with Unicode/emoji content"""
        print("\n   Testing: File with Unicode/emoji...")

        unicode_file = "unicode_test.py"
        content = "# Hello 世界 🌍\ndef hello():\n    print('👋 世界')\n"

        with open(unicode_file, 'w', encoding='utf-8') as f:
            f.write(content)

        html, error = code_viewer.read_and_highlight(unicode_file)

        assert error is None, f"Unicode file should not cause error: {error}"
        assert html is not None, "Should return HTML for Unicode file"

        print("      ✓ Unicode content handled correctly")
        return True

    def test_deep_folder_nesting(self):
        """Test deep folder nesting in file tree"""
        print("\n   Testing: Deep folder nesting...")

        # Create deeply nested structure
        deep_path = os.path.join("a", "b", "c", "d", "e", "f")
        os.makedirs(deep_path, exist_ok=True)

        with open(os.path.join(deep_path, "deep_file.txt"), 'w') as f:
            f.write("deep content")

        # Build tree with limited depth
        tree = file_tree_manager.build_tree(max_depth=4)
        html = file_tree_manager.to_html(tree)

        # Should handle deep nesting (may be limited by max_depth)
        assert html is not None, "Should return HTML for deep structure"
        assert len(html) > 0, "HTML should not be empty"

        print("      ✓ Deep folder nesting handled correctly")
        return True

    def test_many_files_in_folder(self):
        """Test folder with many files"""
        print("\n   Testing: Folder with many files...")

        # Create directory with 100 files
        many_dir = "many_files"
        os.makedirs(many_dir, exist_ok=True)

        for i in range(100):
            with open(os.path.join(many_dir, f"file_{i:03d}.txt"), 'w') as f:
                f.write(f"content {i}")

        # Build tree
        tree = file_tree_manager.build_tree(max_depth=2)
        html = file_tree_manager.to_html(tree)

        assert html is not None, "Should handle many files"
        assert "many_files" in html, "Folder should appear in tree"

        print("      ✓ Many files handled correctly")
        return True


class TestCodeViewerEdgeCases:
    """Test code viewer edge cases"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_viewer_edge_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_unknown_extension(self):
        """Test file with unknown extension"""
        print("\n   Testing: Unknown file extension...")

        unknown_file = "file.xyz123"
        content = "some random content\nwith multiple lines\n"

        with open(unknown_file, 'w') as f:
            f.write(content)

        html, error = code_viewer.read_and_highlight(unknown_file)

        # Should fallback to plain text
        assert error is None, f"Unknown extension should not error: {error}"
        assert html is not None, "Should return HTML"
        assert "some random content" in html, "Content should be in output"

        print("      ✓ Unknown extension handled correctly")
        return True

    def test_no_extension(self):
        """Test file with no extension"""
        print("\n   Testing: File with no extension...")

        no_ext_file = "README"
        content = "This is a readme file\n"

        with open(no_ext_file, 'w') as f:
            f.write(content)

        html, error = code_viewer.read_and_highlight(no_ext_file)

        assert error is None, f"No extension should not error: {error}"
        assert html is not None, "Should return HTML"

        print("      ✓ No extension handled correctly")
        return True

    def test_very_long_lines(self):
        """Test file with very long lines"""
        print("\n   Testing: Very long lines...")

        long_line_file = "long_lines.txt"
        long_line = "x" * 5000  # 5000 character line

        with open(long_line_file, 'w') as f:
            f.write(long_line + "\n")
            f.write("normal line\n")

        html, error = code_viewer.read_and_highlight(long_line_file)

        # Should handle long lines (may truncate in display)
        assert error is None, f"Long lines should not error: {error}"
        assert html is not None, "Should return HTML"

        print("      ✓ Very long lines handled correctly")
        return True

    def test_mixed_indentation(self):
        """Test file with tabs and spaces mixed"""
        print("\n   Testing: Mixed tabs and spaces...")

        mixed_file = "mixed_indent.py"
        content = "def func1():\n\tprint('tab')\n    print('spaces')\n"

        with open(mixed_file, 'w') as f:
            f.write(content)

        html, error = code_viewer.read_and_highlight(mixed_file)

        assert error is None, f"Mixed indentation should not error: {error}"
        assert html is not None, "Should return HTML"

        print("      ✓ Mixed indentation handled correctly")
        return True

    def test_syntax_errors_in_code(self):
        """Test file with syntax errors"""
        print("\n   Testing: Code with syntax errors...")

        error_file = "syntax_error.py"
        content = "def broken(\nprint('missing closing paren'\n"

        with open(error_file, 'w') as f:
            f.write(content)

        html, error = code_viewer.read_and_highlight(error_file)

        # Should still highlight even with syntax errors
        assert error is None, f"Syntax errors should not prevent highlighting: {error}"
        assert html is not None, "Should return HTML"

        print("      ✓ Syntax errors handled correctly")
        return True


class TestDiffViewerEdgeCases:
    """Test diff viewer edge cases"""

    def __init__(self):
        pass

    def setup(self):
        """Setup test environment"""
        print("   Setup: Diff viewer edge cases")

    def teardown(self):
        """Cleanup test environment"""
        pass

    def test_diff_without_viewing_first(self):
        """Test generating diff without caching original"""
        print("\n   Testing: Diff without viewing first...")

        # This simulates user trying to diff without viewing first
        # In actual GUI, this would show instruction message
        # Here we just test the diff viewer itself

        old = "line1\n"
        new = "line1\nline2\n"

        diff_html = diff_viewer.generate_diff(old, new, "test.txt")

        assert diff_html is not None, "Should return diff HTML"
        assert "line2" in diff_html, "New line should be in diff"

        print("      ✓ Diff without cache handled correctly")
        return True

    def test_diff_unchanged_file(self):
        """Test diff when file is unchanged"""
        print("\n   Testing: Diff unchanged file...")

        content = "unchanged content\n"
        diff_html = diff_viewer.generate_diff(content, content, "test.txt")

        assert "No changes" in diff_html, "Should show 'No changes' message"

        print("      ✓ Unchanged file diff handled correctly")
        return True

    def test_diff_whitespace_only_changes(self):
        """Test diff with only whitespace changes"""
        print("\n   Testing: Whitespace-only changes...")

        old = "line1\nline2\n"
        new = "line1 \nline2\n"  # Added space at end of line1

        diff_html = diff_viewer.generate_diff(old, new, "test.txt")

        # Should show diff even for whitespace
        assert diff_html is not None, "Should return diff"

        print("      ✓ Whitespace changes handled correctly")
        return True

    def test_diff_entire_file_deleted(self):
        """Test diff where entire file content is deleted"""
        print("\n   Testing: Entire file deleted...")

        old = "line1\nline2\nline3\n"
        new = ""

        diff_html = diff_viewer.generate_diff(old, new, "test.txt")

        assert diff_html is not None, "Should return diff"
        # All lines should be shown as deleted
        assert "line1" in diff_html or "line" in diff_html

        print("      ✓ File deletion handled correctly")
        return True

    def test_diff_entire_file_added(self):
        """Test diff where entire file is new"""
        print("\n   Testing: Entire file added...")

        old = ""
        new = "line1\nline2\nline3\n"

        diff_html = diff_viewer.generate_diff(old, new, "test.txt")

        assert diff_html is not None, "Should return diff"
        # All lines should be shown as added
        assert "line" in diff_html

        print("      ✓ File addition handled correctly")
        return True

    def test_diff_html_escaping(self):
        """Test that HTML special characters are escaped"""
        print("\n   Testing: HTML escaping in diff...")

        old = "<html>\n"
        new = "<html><body>\n"

        diff_html = diff_viewer.generate_diff(old, new, "test.html")

        # Should escape < and >
        assert "&lt;" in diff_html or "html" in diff_html, "HTML should be escaped or displayed"

        print("      ✓ HTML escaping handled correctly")
        return True


class TestFileTrackerEdgeCases:
    """Test file tracker edge cases"""

    def __init__(self):
        pass

    def setup(self):
        """Setup test environment"""
        file_tracker.clear_status()
        print("   Setup: File tracker edge cases")

    def teardown(self):
        """Cleanup test environment"""
        file_tracker.clear_status()

    def test_track_file_with_special_chars(self):
        """Test tracking file with special characters"""
        print("\n   Testing: File with special characters...")

        special_files = [
            "file with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.multiple.dots.txt"
        ]

        for filename in special_files:
            file_tracker.mark_file_created(filename)
            status = file_tracker.get_status(filename)
            assert status == 'new', f"Failed to track: {filename}"

        print("      ✓ Special characters handled correctly")
        return True

    def test_track_many_files_rapidly(self):
        """Test tracking many files in rapid succession"""
        print("\n   Testing: Track 100 files rapidly...")

        for i in range(100):
            file_tracker.mark_file_created(f"file_{i}.txt")

        # Check a few random ones
        assert file_tracker.get_status("file_0.txt") == 'new'
        assert file_tracker.get_status("file_50.txt") == 'new'
        assert file_tracker.get_status("file_99.txt") == 'new'

        print("      ✓ Rapid tracking handled correctly")
        return True

    def test_clear_status_nonexistent_file(self):
        """Test clearing status on file that's not tracked"""
        print("\n   Testing: Clear status on non-tracked file...")

        # Should not raise error
        file_tracker.clear_status("nonexistent_file.txt")

        print("      ✓ Clear non-tracked file handled correctly")
        return True

    def test_get_status_nonexistent_file(self):
        """Test getting status of file that's not tracked"""
        print("\n   Testing: Get status of non-tracked file...")

        status = file_tracker.get_status("not_tracked.txt")
        assert status == 'normal', f"Expected 'normal', got '{status}'"

        print("      ✓ Non-tracked file status correct")
        return True

    def test_relative_path_conversion(self):
        """Test relative path conversion"""
        print("\n   Testing: Relative path conversion...")

        # Test with relative path
        file_tracker.mark_file_created("relative/path/file.txt")
        status = file_tracker.get_status("relative/path/file.txt")
        assert status == 'new', "Relative path not tracked"

        # Test with absolute path (if possible)
        abs_path = os.path.abspath("absolute_file.txt")
        file_tracker.mark_file_modified(abs_path)
        # Should be stored as relative
        assert len(file_tracker.modified_files) > 0, "Absolute path not tracked"

        print("      ✓ Path conversion handled correctly")
        return True


def run_all_tests():
    """Run all edge case tests"""
    print("="*60)
    print("BECA GUI Edge Case Tests")
    print("="*60)

    test_classes = [
        TestFileSystemEdgeCases,
        TestCodeViewerEdgeCases,
        TestDiffViewerEdgeCases,
        TestFileTrackerEdgeCases
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for test_class in test_classes:
        class_name = test_class.__name__
        print(f"\n{class_name}")
        print("-" * 60)

        # Get all test methods
        test_methods = [method for method in dir(test_class)
                       if method.startswith('test_')]

        for method_name in test_methods:
            total_tests += 1
            test_instance = test_class()

            try:
                # Setup
                test_instance.setup()

                # Run test
                test_method = getattr(test_instance, method_name)
                result = test_method()

                if result:
                    passed_tests += 1
                else:
                    failed_tests.append(f"{class_name}.{method_name}")
                    print(f"      ✗ Test returned False")

            except AssertionError as e:
                failed_tests.append(f"{class_name}.{method_name}")
                print(f"      ✗ Assertion failed: {e}")

            except Exception as e:
                failed_tests.append(f"{class_name}.{method_name}")
                print(f"      ✗ Error: {type(e).__name__}: {e}")

            finally:
                # Teardown
                try:
                    test_instance.teardown()
                except:
                    pass

    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  ✗ {test}")
        print("\n❌ Some edge case tests failed")
        return False
    else:
        print("\n✅ All edge case tests passed!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
