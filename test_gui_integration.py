"""
Integration tests for BECA GUI components
Tests how GUI components work together
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
from langchain_tools import write_file, create_react_app


class TestFileTrackerIntegration:
    """Test file tracker integration with langchain tools"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp(prefix="beca_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        file_tracker.clear_status()
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        file_tracker.clear_status()

    def test_write_file_marks_new_file(self):
        """Test that write_file marks new files as created"""
        print("\n   Testing write_file() marks new files...")

        # Write a new file
        test_file = "test_new.py"
        content = "def test():\n    pass\n"
        result = write_file(test_file, content)

        assert "Successfully wrote" in result, f"write_file failed: {result}"
        assert os.path.exists(test_file), "File not created"

        # Check tracker status
        status = file_tracker.get_status(test_file)
        assert status == 'new', f"Expected status 'new', got '{status}'"

        print("      ✓ New file marked as 'new'")
        return True

    def test_write_file_marks_modified_file(self):
        """Test that write_file marks existing files as modified"""
        print("\n   Testing write_file() marks existing files as modified...")

        # Create file first
        test_file = "test_existing.py"
        with open(test_file, 'w') as f:
            f.write("original content")

        file_tracker.clear_status()  # Clear the NEW status

        # Modify the file using write_file
        new_content = "modified content\n"
        result = write_file(test_file, new_content)

        assert "Successfully wrote" in result, f"write_file failed: {result}"

        # Check tracker status
        status = file_tracker.get_status(test_file)
        assert status == 'modified', f"Expected status 'modified', got '{status}'"

        print("      ✓ Modified file marked as 'modified'")
        return True

    def test_create_react_app_tracks_files(self):
        """Test that create_react_app marks all created files"""
        print("\n   Testing create_react_app() tracks files...")

        app_name = "test-app"
        result = create_react_app(app_name)

        assert "Successfully created" in result, f"create_react_app failed: {result}"
        assert os.path.exists(app_name), "App directory not created"

        # Check that files are tracked
        expected_files = [
            os.path.join(app_name, "src", "index.js"),
            os.path.join(app_name, "package.json")
        ]

        for file_path in expected_files:
            assert os.path.exists(file_path), f"Expected file not created: {file_path}"
            status = file_tracker.get_status(file_path)
            assert status == 'new', f"File {file_path} not marked as 'new': {status}"

        print(f"      ✓ {len(expected_files)} files tracked correctly")
        return True


class TestFileTreeManagerIntegration:
    """Test file tree manager integration with file tracker"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_test_tree_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        file_tracker.clear_status()

        # Create some test files and folders
        os.makedirs("src", exist_ok=True)
        with open("src/main.py", 'w') as f:
            f.write("print('hello')")
        with open("README.md", 'w') as f:
            f.write("# Test")

        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        file_tracker.clear_status()

    def test_file_tree_syncs_with_tracker(self):
        """Test that file tree shows tracker status"""
        print("\n   Testing file tree syncs with file tracker...")

        # Mark files with different statuses
        file_tracker.mark_file_created("src/main.py")
        file_tracker.mark_file_modified("README.md")

        # Sync file tree with tracker
        file_tree_manager.new_files = file_tracker.new_files.copy()
        file_tree_manager.modified_files = file_tracker.modified_files.copy()

        # Build tree
        tree = file_tree_manager.build_tree(max_depth=3)
        html = file_tree_manager.to_html(tree)

        # Check that badges appear in HTML
        assert "NEW" in html, "NEW badge not found in tree HTML"
        assert "MOD" in html, "MODIFIED badge not found in tree HTML"
        assert "main.py" in html, "main.py not in tree"
        assert "README.md" in html, "README.md not in tree"

        print("      ✓ File tree synced with tracker status")
        return True

    def test_file_tree_shows_status_badges(self):
        """Test that status badges appear correctly"""
        print("\n   Testing file tree status badges...")

        # Create files and track them
        test_new = "new_file.py"
        test_modified = "modified_file.py"

        with open(test_new, 'w') as f:
            f.write("new")
        with open(test_modified, 'w') as f:
            f.write("modified")

        file_tracker.mark_file_created(test_new)
        file_tracker.mark_file_modified(test_modified)

        # Sync and build tree
        file_tree_manager.new_files = file_tracker.new_files.copy()
        file_tree_manager.modified_files = file_tracker.modified_files.copy()
        tree = file_tree_manager.build_tree(max_depth=2)
        html = file_tree_manager.to_html(tree)

        # Check badges
        assert 'style="background: #28a745' in html, "Green NEW badge not found"
        assert 'style="background: #ffc107' in html, "Yellow MODIFIED badge not found"

        print("      ✓ Status badges displayed correctly")
        return True


class TestCodeViewerIntegration:
    """Test code viewer integration with file operations"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_test_viewer_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_view_tracked_file(self):
        """Test viewing a file that was tracked"""
        print("\n   Testing view tracked file...")

        # Create and track a file
        test_file = "test_view.py"
        content = "def hello():\n    return 'world'\n"
        write_file(test_file, content)

        # View the file
        html, error = code_viewer.read_and_highlight(test_file)

        assert error is None, f"Error viewing file: {error}"
        assert "def" in html, "Code not highlighted"
        assert "hello" in html, "Function name not in output"

        print("      ✓ Tracked file viewed successfully")
        return True

    def test_view_multiple_languages(self):
        """Test viewing files of different languages"""
        print("\n   Testing multiple language support...")

        test_files = {
            "test.py": "print('Python')\n",
            "test.js": "console.log('JavaScript');\n",
            "test.html": "<html><body>HTML</body></html>\n",
            "test.json": '{"key": "value"}\n'
        }

        for filename, content in test_files.items():
            with open(filename, 'w') as f:
                f.write(content)

            html, error = code_viewer.read_and_highlight(filename)
            assert error is None, f"Error viewing {filename}: {error}"
            assert len(html) > len(content), f"No highlighting for {filename}"

        print(f"      ✓ {len(test_files)} languages highlighted correctly")
        return True


class TestDiffViewerIntegration:
    """Test diff viewer integration"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_test_diff_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_diff_after_modification(self):
        """Test diff shows changes after file modification"""
        print("\n   Testing diff after modification...")

        test_file = "test_diff.py"
        original = "line 1\nline 2\nline 3\n"
        modified = "line 1\nline 2 modified\nline 3\nline 4\n"

        # Create original
        with open(test_file, 'w') as f:
            f.write(original)

        # Modify
        with open(test_file, 'w') as f:
            f.write(modified)

        # Generate diff
        diff_html = diff_viewer.generate_diff(original, modified, test_file)

        assert "modified" in diff_html, "Modified line not in diff"
        assert "line 4" in diff_html, "Added line not in diff"
        assert "background:" in diff_html, "No color coding in diff"

        print("      ✓ Diff shows changes correctly")
        return True

    def test_diff_no_changes(self):
        """Test diff when file unchanged"""
        print("\n   Testing diff with no changes...")

        content = "unchanged content\n"
        diff_html = diff_viewer.generate_diff(content, content, "test.txt")

        assert "No changes" in diff_html, "Should show 'No changes' message"

        print("      ✓ No changes detected correctly")
        return True


def run_all_tests():
    """Run all integration tests"""
    print("="*60)
    print("BECA GUI Integration Tests")
    print("="*60)

    test_classes = [
        TestFileTrackerIntegration,
        TestFileTreeManagerIntegration,
        TestCodeViewerIntegration,
        TestDiffViewerIntegration
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
        print("\n❌ Some tests failed")
        return False
    else:
        print("\n✅ All integration tests passed!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
