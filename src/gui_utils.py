"""
GUI Utilities for BECA - File tree, code viewer, and diff components
"""
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
import difflib


class FileTreeManager:
    """Manages file tree generation and updates"""

    IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv',
                    '.pytest_cache', '.mypy_cache', 'dist', 'build', '.next',
                    'google-cloud-sdk'}
    IGNORED_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore'}

    def __init__(self, root_dir: str = None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.modified_files = set()
        self.new_files = set()

    def build_tree(self, max_depth: int = 4) -> Dict:
        """
        Build a tree structure of the file system

        Returns:
            Dict with tree structure
        """
        return self._scan_directory(self.root_dir, 0, max_depth)

    def _scan_directory(self, path: Path, depth: int, max_depth: int) -> Dict:
        """Recursively scan directory"""
        if depth >= max_depth:
            return None

        tree = {
            'name': path.name if path != self.root_dir else str(path),
            'type': 'directory',
            'path': str(path.relative_to(self.root_dir)),
            'children': []
        }

        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

            for item in items:
                # Skip ignored items
                if item.name in self.IGNORED_FILES:
                    continue
                if item.is_dir() and item.name in self.IGNORED_DIRS:
                    continue

                if item.is_dir():
                    child_tree = self._scan_directory(item, depth + 1, max_depth)
                    if child_tree:
                        tree['children'].append(child_tree)
                else:
                    rel_path = str(item.relative_to(self.root_dir))
                    status = self._get_file_status(rel_path)
                    tree['children'].append({
                        'name': item.name,
                        'type': 'file',
                        'path': rel_path,
                        'status': status,
                        'size': item.stat().st_size
                    })
        except PermissionError:
            pass

        return tree

    def _get_file_status(self, rel_path: str) -> str:
        """Get file status (new, modified, normal)"""
        if rel_path in self.new_files:
            return 'new'
        elif rel_path in self.modified_files:
            return 'modified'
        return 'normal'

    def mark_file_new(self, file_path: str):
        """Mark a file as newly created"""
        self.new_files.add(file_path)

    def mark_file_modified(self, file_path: str):
        """Mark a file as modified"""
        if file_path not in self.new_files:
            self.modified_files.add(file_path)

    def clear_status(self, file_path: str):
        """Clear status for a file"""
        self.new_files.discard(file_path)
        self.modified_files.discard(file_path)

    def to_html(self, tree: Dict) -> str:
        """Convert tree to HTML representation"""
        if not tree:
            return "<div>No files found</div>"

        return self._tree_to_html(tree, 0)

    def _tree_to_html(self, node: Dict, level: int) -> str:
        """Recursively convert tree node to HTML"""
        indent = '  ' * level
        html = []

        if node['type'] == 'directory':
            icon = '📁'
            html.append(f'{indent}<details open>')
            html.append(f'{indent}  <summary>{icon} <strong>{node["name"]}</strong></summary>')
            for child in node.get('children', []):
                html.append(self._tree_to_html(child, level + 1))
            html.append(f'{indent}</details>')
        else:
            icon = self._get_file_icon(node['name'])
            status_badge = self._get_status_badge(node.get('status', 'normal'))
            size = self._format_size(node.get('size', 0))
            html.append(
                f'{indent}<div style="margin-left: 20px; padding: 2px 0;">'
                f'{icon} {node["name"]} {status_badge} '
                f'<span style="color: #888; font-size: 0.9em;">({size})</span>'
                f'</div>'
            )

        return '\n'.join(html)

    def _get_file_icon(self, filename: str) -> str:
        """Get icon for file type"""
        ext = Path(filename).suffix.lower()
        icon_map = {
            '.py': '🐍',
            '.js': '📜',
            '.jsx': '⚛️',
            '.ts': '📘',
            '.tsx': '⚛️',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.md': '📝',
            '.txt': '📄',
            '.yml': '⚙️',
            '.yaml': '⚙️',
            '.sh': '🔧',
            '.bat': '🔧',
            '.ps1': '🔧',
        }
        return icon_map.get(ext, '📄')

    def _get_status_badge(self, status: str) -> str:
        """Get HTML badge for file status"""
        if status == 'new':
            return '<span style="background: #28a745; color: white; padding: 1px 6px; border-radius: 3px; font-size: 0.8em;">NEW</span>'
        elif status == 'modified':
            return '<span style="background: #ffc107; color: black; padding: 1px 6px; border-radius: 3px; font-size: 0.8em;">MOD</span>'
        return ''

    def _format_size(self, size: int) -> str:
        """Format file size"""
        if size < 1024:
            return f"{size}B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f}KB"
        else:
            return f"{size / (1024 * 1024):.1f}MB"


class CodeViewer:
    """Handles syntax highlighting for code display"""

    def __init__(self):
        self.formatter = HtmlFormatter(
            style='monokai',
            noclasses=True,
            linenos=True,
            linenostart=1,
            cssclass='code-highlight'
        )

    def highlight_code(self, code: str, filename: str = None, language: str = None) -> str:
        """
        Highlight code with syntax coloring

        Args:
            code: Source code to highlight
            filename: Filename to detect language
            language: Explicit language name

        Returns:
            HTML with syntax highlighting
        """
        if not code:
            return "<div>Empty file</div>"

        try:
            # Try to get lexer
            if language:
                lexer = get_lexer_by_name(language)
            elif filename:
                lexer = get_lexer_for_filename(filename, code)
            else:
                lexer = guess_lexer(code)

            highlighted = highlight(code, lexer, self.formatter)

            # Wrap in container with copy button
            return f"""
            <div style="position: relative;">
                <div style="max-height: 600px; overflow: auto;">
                    {highlighted}
                </div>
            </div>
            """
        except ClassNotFound:
            # Fallback to plain text
            lines = code.split('\n')
            numbered_lines = '\n'.join(
                f'<span style="color: #888;">{i+1:4d}</span>  {line}'
                for i, line in enumerate(lines)
            )
            return f'<pre style="background: #272822; color: #f8f8f2; padding: 10px; overflow: auto; max-height: 600px;">{numbered_lines}</pre>'

    def read_and_highlight(self, file_path: str) -> Tuple[str, str]:
        """
        Read file and return highlighted HTML

        Returns:
            Tuple of (highlighted_html, error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            html = self.highlight_code(code, filename=file_path)
            return html, None
        except UnicodeDecodeError:
            return "<div>⚠️ Binary file - cannot display</div>", None
        except Exception as e:
            return None, f"Error reading file: {str(e)}"


class DiffViewer:
    """Handles diff generation and display"""

    def __init__(self):
        self.formatter = HtmlFormatter(style='monokai', noclasses=True)

    def generate_diff(self, old_content: str, new_content: str,
                     filename: str = "file") -> str:
        """
        Generate HTML diff view

        Args:
            old_content: Original content
            new_content: Modified content
            filename: Name of the file

        Returns:
            HTML with side-by-side diff
        """
        if old_content == new_content:
            return "<div style='padding: 20px; color: #28a745;'>✓ No changes detected</div>"

        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f'a/{filename}',
            tofile=f'b/{filename}',
            lineterm=''
        )

        diff_html = ['<div style="font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 15px; overflow: auto; max-height: 600px;">']

        for line in diff:
            line = line.rstrip()
            if line.startswith('---') or line.startswith('+++'):
                diff_html.append(f'<div style="color: #888; font-weight: bold;">{self._escape_html(line)}</div>')
            elif line.startswith('@@'):
                diff_html.append(f'<div style="color: #569cd6; font-weight: bold; margin: 10px 0 5px 0;">{self._escape_html(line)}</div>')
            elif line.startswith('+'):
                diff_html.append(f'<div style="background: #1a3d1a; color: #4ec94e;">{self._escape_html(line)}</div>')
            elif line.startswith('-'):
                diff_html.append(f'<div style="background: #3d1a1a; color: #f14c4c;">{self._escape_html(line)}</div>')
            else:
                diff_html.append(f'<div style="color: #d4d4d4;">{self._escape_html(line)}</div>')

        diff_html.append('</div>')
        return ''.join(diff_html)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#39;'))


# Global instances
file_tree_manager = FileTreeManager()
code_viewer = CodeViewer()
diff_viewer = DiffViewer()
