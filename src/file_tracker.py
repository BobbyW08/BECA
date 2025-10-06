"""
File operation tracker for GUI updates
This module tracks file operations to update the GUI file tree in real-time
"""
from typing import Set, Callable, Optional
from pathlib import Path


class FileOperationTracker:
    """
    Tracks file operations and notifies listeners.
    Used to update GUI when agent creates/modifies files.
    """

    def __init__(self):
        self.new_files: Set[str] = set()
        self.modified_files: Set[str] = set()
        self.deleted_files: Set[str] = set()
        self._update_callback: Optional[Callable] = None

    def mark_file_created(self, file_path: str):
        """Mark a file as newly created"""
        rel_path = self._get_relative_path(file_path)
        self.new_files.add(rel_path)
        self._notify_update()

    def mark_file_modified(self, file_path: str):
        """Mark a file as modified"""
        rel_path = self._get_relative_path(file_path)
        # Don't mark as modified if it was just created
        if rel_path not in self.new_files:
            self.modified_files.add(rel_path)
        self._notify_update()

    def mark_file_deleted(self, file_path: str):
        """Mark a file as deleted"""
        rel_path = self._get_relative_path(file_path)
        self.deleted_files.add(rel_path)
        # Remove from other sets
        self.new_files.discard(rel_path)
        self.modified_files.discard(rel_path)
        self._notify_update()

    def clear_status(self, file_path: str = None):
        """Clear status for a specific file or all files"""
        if file_path:
            rel_path = self._get_relative_path(file_path)
            self.new_files.discard(rel_path)
            self.modified_files.discard(rel_path)
            self.deleted_files.discard(rel_path)
        else:
            self.new_files.clear()
            self.modified_files.clear()
            self.deleted_files.clear()
        self._notify_update()

    def get_status(self, file_path: str) -> str:
        """Get the status of a file (new, modified, deleted, normal)"""
        rel_path = self._get_relative_path(file_path)
        if rel_path in self.new_files:
            return 'new'
        elif rel_path in self.modified_files:
            return 'modified'
        elif rel_path in self.deleted_files:
            return 'deleted'
        return 'normal'

    def set_update_callback(self, callback: Callable):
        """Set a callback to be called when files are updated"""
        self._update_callback = callback

    def _notify_update(self):
        """Notify registered callback of updates"""
        if self._update_callback:
            try:
                self._update_callback()
            except Exception as e:
                print(f"Error in file tracker callback: {e}")

    def _get_relative_path(self, file_path: str) -> str:
        """Convert absolute path to relative path"""
        try:
            path = Path(file_path)
            if path.is_absolute():
                return str(path.relative_to(Path.cwd()))
            return str(path)
        except ValueError:
            # If path is not relative to cwd, return as-is
            return file_path


# Global tracker instance
file_tracker = FileOperationTracker()
