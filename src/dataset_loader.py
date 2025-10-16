"""
Dataset Loader for BECA
Loads and indexes coding datasets into the knowledge base
"""
import json
from typing import List, Dict, Optional
from pathlib import Path
from knowledge_system import knowledge_base


class DatasetLoader:
    """Loads coding datasets into BECA's knowledge base"""
    
    def __init__(self):
        self.kb = knowledge_base
        self.loaded_datasets = []
    
    def load_code_patterns_from_file(self, file_path: str) -> int:
        """
        Load code patterns from a JSON file
        
        Expected format:
        [
            {
                "pattern_name": "...",
                "language": "...",
                "description": "...",
                "code_snippet": "...",
                "use_case": "...",
                "tags": [...]
            }
        ]
        
        Returns:
            Number of patterns loaded
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
            
            count = 0
            for pattern in patterns:
                self.kb.add_code_pattern(
                    pattern_name=pattern['pattern_name'],
                    language=pattern['language'],
                    code_snippet=pattern['code_snippet'],
                    description=pattern.get('description'),
                    use_case=pattern.get('use_case'),
                    tags=pattern.get('tags'),
                    source_url=pattern.get('source_url')
                )
                count += 1
            
            self.loaded_datasets.append(f"code_patterns:{file_path}")
            return count
            
        except Exception as e:
            print(f"Error loading code patterns: {e}")
            return 0
    
    def load_common_algorithms(self) -> int:
        """Load common algorithm patterns"""
        algorithms = [
            {
                "pattern_name": "Binary Search",
                "language": "Python",
                "description": "Efficiently search sorted arrays in O(log n) time",
                "code_snippet": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Target not found""",
                "use_case": "Searching in sorted data structures",
                "tags": ["search", "algorithm", "optimization"]
            },
            {
                "pattern_name": "Depth-First Search (DFS)",
                "language": "Python",
                "description": "Graph/tree traversal algorithm that explores as far as possible before backtracking",
                "code_snippet": """def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start)  # Process node
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited""",
                "use_case": "Graph traversal, maze solving, topological sorting",
                "tags": ["graph", "traversal", "recursion"]
            },
            {
                "pattern_name": "Dynamic Programming - Memoization",
                "language": "Python",
                "description": "Cache results of expensive function calls",
                "code_snippet": """from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Or manual memoization:
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]""",
                "use_case": "Optimization problems, avoiding redundant calculations",
                "tags": ["dynamic_programming", "optimization", "memoization"]
            },
            {
                "pattern_name": "API Rate Limiter",
                "language": "Python",
                "description": "Implement rate limiting for API calls",
                "code_snippet": """import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, time_window):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def allow_request(self):
        now = time.time()
        
        # Remove old calls outside time window
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        # Check if under limit
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

# Usage: limiter = RateLimiter(max_calls=10, time_window=60)""",
                "use_case": "API rate limiting, request throttling",
                "tags": ["api", "rate_limiting", "web"]
            },
            {
                "pattern_name": "Singleton Pattern",
                "language": "Python",
                "description": "Ensure a class has only one instance",
                "code_snippet": """class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Alternative with decorator:
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = None""",
                "use_case": "Database connections, configuration managers, loggers",
                "tags": ["design_pattern", "creational"]
            },
            {
                "pattern_name": "Observer Pattern",
                "language": "Python",
                "description": "Define one-to-many dependency for event handling",
                "code_snippet": """class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer:
    def update(self, event):
        print(f"Received event: {event}")

# Usage:
subject = Subject()
observer = Observer()
subject.attach(observer)
subject.notify("Something happened")""",
                "use_case": "Event systems, UI updates, pub-sub patterns",
                "tags": ["design_pattern", "behavioral", "events"]
            },
            {
                "pattern_name": "Async/Await API Call",
                "language": "Python",
                "description": "Modern asynchronous HTTP requests",
                "code_snippet": """import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_multiple(urls):
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Usage:
urls = ['https://api.example.com/1', 'https://api.example.com/2']
results = asyncio.run(fetch_multiple(urls))""",
                "use_case": "Concurrent API calls, async web scraping",
                "tags": ["async", "api", "concurrency"]
            },
            {
                "pattern_name": "Context Manager",
                "language": "Python",
                "description": "Manage resources with automatic cleanup",
                "code_snippet": """from contextlib import contextmanager

class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# Or with decorator:
@contextmanager
def file_manager(filename, mode):
    f = open(filename, mode)
    try:
        yield f
    finally:
        f.close()

# Usage:
with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")""",
                "use_case": "Resource management, file handling, database connections",
                "tags": ["resource_management", "context_manager"]
            }
        ]
        
        count = 0
        for algo in algorithms:
            self.kb.add_code_pattern(
                pattern_name=algo['pattern_name'],
                language=algo['language'],
                code_snippet=algo['code_snippet'],
                description=algo.get('description'),
                use_case=algo.get('use_case'),
                tags=algo.get('tags')
            )
            count += 1
        
        self.loaded_datasets.append("common_algorithms")
        return count
    
    def load_web_development_patterns(self) -> int:
        """Load common web development patterns"""
        patterns = [
            {
                "pattern_name": "REST API Endpoint",
                "language": "Python",
                "description": "Flask REST API endpoint with error handling",
                "code_snippet": """from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Fetch user from database
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # Validate and create user
    return jsonify(user.to_dict()), 201""",
                "use_case": "Building RESTful APIs",
                "tags": ["flask", "api", "rest", "web"]
            },
            {
                "pattern_name": "React Component with Hooks",
                "language": "JavaScript",
                "description": "Modern React component using hooks",
                "code_snippet": """import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        async function fetchUser() {
            try {
                const response = await fetch(`/api/users/${userId}`);
                const data = await response.json();
                setUser(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        
        fetchUser();
    }, [userId]);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    
    return (
        <div>
            <h2>{user.name}</h2>
            <p>{user.email}</p>
        </div>
    );
}

export default UserProfile;""",
                "use_case": "React frontend components with API integration",
                "tags": ["react", "hooks", "frontend", "javascript"]
            }
        ]
        
        count = 0
        for pattern in patterns:
            self.kb.add_code_pattern(
                pattern_name=pattern['pattern_name'],
                language=pattern['language'],
                code_snippet=pattern['code_snippet'],
                description=pattern.get('description'),
                use_case=pattern.get('use_case'),
                tags=pattern.get('tags')
            )
            count += 1
        
        self.loaded_datasets.append("web_development_patterns")
        return count
    
    def load_all_builtin_datasets(self) -> Dict[str, int]:
        """Load all built-in datasets"""
        results = {}
        
        results['algorithms'] = self.load_common_algorithms()
        results['web_patterns'] = self.load_web_development_patterns()
        
        return results
    
    def get_loaded_datasets(self) -> List[str]:
        """Get list of loaded datasets"""
        return self.loaded_datasets


# Global dataset loader instance
dataset_loader = DatasetLoader()
