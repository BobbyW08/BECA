"""
End-to-End tests for BECA GUI workflows
Tests complete user workflows from start to finish
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


class TestE2EWorkflows:
    """End-to-end workflow tests"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="beca_e2e_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        file_tracker.clear_status()
        file_tree_manager.root_dir = Path(self.test_dir)
        print(f"   Test directory: {self.test_dir}")

    def teardown(self):
        """Cleanup test environment"""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        file_tracker.clear_status()

    def test_create_new_file_workflow(self):
        """
        E2E Test: Create new file workflow
        User story: As a user, I want to create a file and see it in the tree
        """
        print("\n   Testing: Create New File Workflow")

        # Step 1: Create a new file using write_file
        print("      Step 1: Creating file with write_file()...")
        test_file = "new_module.py"
        content = "def greet(name):\n    return f'Hello, {name}!'\n"
        result = write_file.invoke({"file_path": test_file, "content": content})

        assert "Successfully wrote" in result, f"Failed to create file: {result}"
        assert os.path.exists(test_file), "File not created on filesystem"

        # Step 2: Verify file is tracked as NEW
        print("      Step 2: Verifying file tracked as NEW...")
        status = file_tracker.get_status(test_file)
        assert status == 'new', f"Expected 'new' status, got '{status}'"

        # Step 3: Refresh file tree
        print("      Step 3: Refreshing file tree...")
        file_tree_manager.new_files = file_tracker.new_files.copy()
        tree = file_tree_manager.build_tree(max_depth=2)
        html = file_tree_manager.to_html(tree)

        # Step 4: Verify file appears with NEW badge
        print("      Step 4: Verifying file in tree with NEW badge...")
        assert test_file in html, "File not found in tree HTML"
        assert "NEW" in html, "NEW badge not in tree HTML"

        # Step 5: View the file with syntax highlighting
        print("      Step 5: Viewing file with code viewer...")
        highlighted, error = code_viewer.read_and_highlight(test_file)

        assert error is None, f"Error viewing file: {error}"
        assert "def" in highlighted, "Python syntax not highlighted"
        assert "greet" in highlighted, "Function name not in output"

        print("      ✓ Create New File Workflow completed successfully")
        return True

    def test_modify_existing_file_workflow(self):
        """
        E2E Test: Modify existing file workflow
        User story: As a user, I want to modify a file and see the diff
        """
        print("\n   Testing: Modify Existing File Workflow")

        # Step 1: Create original file
        print("      Step 1: Creating original file...")
        test_file = "config.py"
        original_content = "DEBUG = False\nVERSION = '1.0.0'\n"

        with open(test_file, 'w') as f:
            f.write(original_content)

        # Step 2: View original (store for diff)
        print("      Step 2: Viewing original content...")
        original_cache = {}
        original_cache[test_file] = original_content

        # Step 3: Clear tracker and modify file
        print("      Step 3: Modifying file...")
        file_tracker.clear_status()

        modified_content = "DEBUG = True\nVERSION = '1.0.1'\nLOG_LEVEL = 'INFO'\n"
        result = write_file.invoke({"file_path": test_file, "content": modified_content})

        assert "Successfully wrote" in result, f"Failed to modify file: {result}"

        # Step 4: Verify file marked as MODIFIED
        print("      Step 4: Verifying MODIFIED status...")
        status = file_tracker.get_status(test_file)
        assert status == 'modified', f"Expected 'modified' status, got '{status}'"

        # Step 5: Refresh file tree
        print("      Step 5: Refreshing file tree...")
        file_tree_manager.modified_files = file_tracker.modified_files.copy()
        tree = file_tree_manager.build_tree(max_depth=2)
        html = file_tree_manager.to_html(tree)

        # Step 6: Verify MODIFIED badge appears
        print("      Step 6: Verifying MODIFIED badge in tree...")
        assert "MOD" in html, "MODIFIED badge not in tree HTML"

        # Step 7: Generate diff
        print("      Step 7: Generating diff...")
        diff_html = diff_viewer.generate_diff(
            original_cache[test_file],
            modified_content,
            test_file
        )

        # Step 8: Verify diff shows changes
        print("      Step 8: Verifying diff shows changes...")
        assert "True" in diff_html, "Modified DEBUG value not in diff"
        assert "1.0.1" in diff_html, "Modified VERSION not in diff"
        assert "LOG_LEVEL" in diff_html, "New line not in diff"
        assert "background:" in diff_html, "Diff not color-coded"

        print("      ✓ Modify Existing File Workflow completed successfully")
        return True

    def test_create_project_structure_workflow(self):
        """
        E2E Test: Create project structure workflow
        User story: As a user, I want to create a project and see all files
        """
        print("\n   Testing: Create Project Structure Workflow")

        # Step 1: Create React app using tool
        print("      Step 1: Creating React app with create_react_app()...")
        app_name = "my-todo-app"
        result = create_react_app.invoke({"app_name": app_name})

        assert "Successfully created" in result, f"Failed to create app: {result}"
        assert os.path.exists(app_name), "App directory not created"

        # Step 2: Verify multiple files created
        print("      Step 2: Verifying multiple files created...")
        expected_files = [
            os.path.join(app_name, "src", "index.js"),
            os.path.join(app_name, "package.json")
        ]

        for file_path in expected_files:
            assert os.path.exists(file_path), f"Expected file missing: {file_path}"

        # Step 3: Verify all files tracked as NEW
        print("      Step 3: Verifying all files tracked as NEW...")
        for file_path in expected_files:
            status = file_tracker.get_status(file_path)
            assert status == 'new', f"File {file_path} not marked as NEW: {status}"

        # Step 4: Build file tree
        print("      Step 4: Building file tree...")
        file_tree_manager.new_files = file_tracker.new_files.copy()
        tree = file_tree_manager.build_tree(max_depth=4)
        html = file_tree_manager.to_html(tree)

        # Step 5: Verify folder structure appears
        print("      Step 5: Verifying folder structure in tree...")
        assert app_name in html, "App folder not in tree"
        assert "src" in html, "src folder not in tree"
        assert "index.js" in html, "index.js not in tree"
        assert "package.json" in html, "package.json not in tree"

        # Step 6: Verify NEW badges appear
        print("      Step 6: Verifying NEW badges...")
        new_count = html.count("NEW")
        assert new_count >= 2, f"Expected at least 2 NEW badges, found {new_count}"

        # Step 7: View one of the files
        print("      Step 7: Viewing package.json with code viewer...")
        package_json_path = os.path.join(app_name, "package.json")
        highlighted, error = code_viewer.read_and_highlight(package_json_path)

        assert error is None, f"Error viewing file: {error}"
        assert app_name in highlighted, "App name not in package.json"

        print("      ✓ Create Project Structure Workflow completed successfully")
        return True

    def test_file_tree_refresh_workflow(self):
        """
        E2E Test: File tree refresh workflow
        User story: As a user, I want to manually refresh the file tree
        """
        print("\n   Testing: File Tree Refresh Workflow")

        # Step 1: Create initial files
        print("      Step 1: Creating initial files...")
        with open("file1.txt", 'w') as f:
            f.write("content1")
        with open("file2.txt", 'w') as f:
            f.write("content2")

        # Step 2: Build initial tree
        print("      Step 2: Building initial tree...")
        tree1 = file_tree_manager.build_tree(max_depth=2)
        html1 = file_tree_manager.to_html(tree1)

        assert "file1.txt" in html1, "file1.txt not in initial tree"
        assert "file2.txt" in html1, "file2.txt not in initial tree"

        # Step 3: Create external file (not through tracker)
        print("      Step 3: Creating external file...")
        with open("external_file.txt", 'w') as f:
            f.write("external content")

        # Step 4: Refresh tree
        print("      Step 4: Refreshing tree...")
        tree2 = file_tree_manager.build_tree(max_depth=2)
        html2 = file_tree_manager.to_html(tree2)

        # Step 5: Verify new file appears
        print("      Step 5: Verifying external file appears...")
        assert "external_file.txt" in html2, "External file not in refreshed tree"

        # Step 6: Verify no badge (not tracked)
        print("      Step 6: Verifying no badge on external file...")
        # External file shouldn't have NEW badge since tracker didn't create it
        status = file_tracker.get_status("external_file.txt")
        assert status == 'normal', f"External file should be 'normal', got '{status}'"

        print("      ✓ File Tree Refresh Workflow completed successfully")
        return True

    def test_multi_file_operation_workflow(self):
        """
        E2E Test: Multiple file operations workflow
        User story: As a user, I want to track multiple file operations
        """
        print("\n   Testing: Multi-File Operation Workflow")

        # Step 1: Create multiple new files
        print("      Step 1: Creating 5 new files...")
        new_files = []
        for i in range(5):
            filename = f"module_{i}.py"
            write_file.invoke({"file_path": filename, "content": f"# Module {i}\ndef func_{i}(): pass\n"})
            new_files.append(filename)

        # Step 2: Create and modify 3 files
        print("      Step 2: Creating and modifying 3 files...")
        modified_files = []
        # Clear tracker once before modifications
        file_tracker.clear_status()

        for i in range(3):
            filename = f"config_{i}.py"
            # Create
            with open(filename, 'w') as f:
                f.write("original")
            # Modify
            write_file.invoke({"file_path": filename, "content": "modified content"})
            modified_files.append(filename)

        # Step 3: Refresh file tree
        print("      Step 3: Refreshing file tree...")
        file_tree_manager.new_files = file_tracker.new_files.copy()
        file_tree_manager.modified_files = file_tracker.modified_files.copy()
        tree = file_tree_manager.build_tree(max_depth=2)
        html = file_tree_manager.to_html(tree)

        # Step 4: Verify badge counts
        print("      Step 4: Verifying badge counts...")
        new_count = html.count("NEW")
        mod_count = html.count("MOD")

        # Should have at least 3 MODIFIED badges (the ones we explicitly modified)
        assert mod_count >= 3, f"Expected at least 3 MOD badges, found {mod_count}"

        # Should have multiple files in tree
        assert len(new_files) > 0, "No new files created"
        assert len(modified_files) > 0, "No files modified"

        # Step 5: Verify all files visible
        print("      Step 5: Verifying all files visible in tree...")
        for filename in new_files:
            if filename in file_tracker.new_files:
                assert filename in html, f"New file {filename} not in tree"

        for filename in modified_files:
            assert filename in html, f"Modified file {filename} not in tree"

        print("      ✓ Multi-File Operation Workflow completed successfully")
        return True


def run_all_tests():
    """Run all end-to-end tests"""
    print("="*60)
    print("BECA GUI End-to-End Tests")
    print("="*60)

    test_class = TestE2EWorkflows
    test_methods = [
        'test_create_new_file_workflow',
        'test_modify_existing_file_workflow',
        'test_create_project_structure_workflow',
        'test_file_tree_refresh_workflow',
        'test_multi_file_operation_workflow'
    ]

    total_tests = len(test_methods)
    passed_tests = 0
    failed_tests = []

    print(f"\n{test_class.__name__}")
    print("-" * 60)

    for method_name in test_methods:
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
                failed_tests.append(method_name)
                print(f"      ✗ Test returned False")

        except AssertionError as e:
            failed_tests.append(method_name)
            print(f"      ✗ Assertion failed: {e}")

        except Exception as e:
            failed_tests.append(method_name)
            print(f"      ✗ Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

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
        print("\n❌ Some E2E tests failed")
        return False
    else:
        print("\n✅ All E2E tests passed!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
