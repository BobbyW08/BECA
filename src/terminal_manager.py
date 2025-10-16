"""
Terminal Manager for BECA
Captures and streams command outputs in real-time
"""
import subprocess
import threading
import queue
import time
from typing import Optional, Callable, Dict
from datetime import datetime


class TerminalManager:
    """Manages terminal command execution with real-time output capture"""
    
    def __init__(self):
        self.output_queue = queue.Queue()
        self.current_process: Optional[subprocess.Popen] = None
        self.stop_flag = threading.Event()
        self.command_history = []
        self.max_history = 100
        
    def execute_command(self, 
                       command: str, 
                       cwd: str = None,
                       callback: Optional[Callable] = None) -> Dict:
        """
        Execute a command and capture output in real-time
        
        Args:
            command: Command to execute
            cwd: Working directory (default: None for current)
            callback: Optional callback function for output updates
            
        Returns:
            Dict with status, output, and error information
        """
        self.stop_flag.clear()
        start_time = datetime.now()
        
        # Add to history
        history_entry = {
            'command': command,
            'timestamp': start_time.strftime('%H:%M:%S'),
            'status': 'running',
            'output': ''
        }
        self.command_history.append(history_entry)
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)
        
        try:
            # Execute command
            self.current_process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=cwd,
                universal_newlines=True
            )
            
            output_lines = []
            error_lines = []
            
            # Read output in real-time
            def read_output(pipe, is_error=False):
                try:
                    for line in iter(pipe.readline, ''):
                        if self.stop_flag.is_set():
                            break
                        
                        line = line.rstrip()
                        if line:
                            if is_error:
                                error_lines.append(line)
                                self.output_queue.put(('error', line))
                            else:
                                output_lines.append(line)
                                self.output_queue.put(('output', line))
                            
                            if callback:
                                callback(line, is_error)
                except Exception as e:
                    print(f"Error reading output: {e}")
                finally:
                    pipe.close()
            
            # Start threads for stdout and stderr
            stdout_thread = threading.Thread(
                target=read_output, 
                args=(self.current_process.stdout, False)
            )
            stderr_thread = threading.Thread(
                target=read_output, 
                args=(self.current_process.stderr, True)
            )
            
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
            
            # Wait for process to complete or stop flag
            while self.current_process.poll() is None:
                if self.stop_flag.is_set():
                    self.current_process.terminate()
                    time.sleep(0.5)
                    if self.current_process.poll() is None:
                        self.current_process.kill()
                    history_entry['status'] = 'stopped'
                    return {
                        'success': False,
                        'output': '\n'.join(output_lines),
                        'error': 'Command stopped by user',
                        'return_code': -1
                    }
                time.sleep(0.1)
            
            # Wait for threads to finish reading
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
            
            return_code = self.current_process.returncode
            success = return_code == 0
            
            # Update history
            history_entry['status'] = 'success' if success else 'error'
            history_entry['output'] = '\n'.join(output_lines)
            history_entry['return_code'] = return_code
            
            return {
                'success': success,
                'output': '\n'.join(output_lines),
                'error': '\n'.join(error_lines) if error_lines else None,
                'return_code': return_code
            }
            
        except Exception as e:
            history_entry['status'] = 'error'
            history_entry['output'] = str(e)
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1
            }
        finally:
            self.current_process = None
    
    def stop_current_command(self):
        """Stop the currently running command"""
        self.stop_flag.set()
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                time.sleep(0.5)
                if self.current_process.poll() is None:
                    self.current_process.kill()
            except:
                pass
    
    def is_running(self) -> bool:
        """Check if a command is currently running"""
        return self.current_process is not None and self.current_process.poll() is None
    
    def get_output_stream(self):
        """Generator for streaming output"""
        while True:
            try:
                output_type, line = self.output_queue.get(timeout=0.1)
                yield output_type, line
            except queue.Empty:
                if not self.is_running():
                    break
    
    def get_history(self, limit: int = 10) -> list:
        """Get command history"""
        return self.command_history[-limit:]
    
    def format_history(self, limit: int = 10) -> str:
        """Format command history as text"""
        history = self.get_history(limit)
        lines = []
        for entry in history:
            status_icon = {
                'running': '⏳',
                'success': '✅',
                'error': '❌',
                'stopped': '🛑'
            }.get(entry['status'], '❓')
            
            lines.append(f"{status_icon} [{entry['timestamp']}] {entry['command']}")
            if entry.get('return_code') is not None:
                lines.append(f"   Return code: {entry['return_code']}")
        
        return '\n'.join(lines) if lines else 'No command history'
    
    def clear_history(self):
        """Clear command history"""
        self.command_history.clear()


# Global terminal manager instance
terminal_manager = TerminalManager()
