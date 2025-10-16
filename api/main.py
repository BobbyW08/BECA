"""
BECA FastAPI Backend
Modern REST API with Plan/Act mode support
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal
import sys
import os
from pathlib import Path
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import BECA components
try:
    from langchain_agent import chat_with_agent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import LangChain agent: {e}")
    AGENT_AVAILABLE = False

try:
    from file_tracker import file_tracker
    FILE_TRACKER_AVAILABLE = True
except ImportError:
    FILE_TRACKER_AVAILABLE = False

try:
    from autonomous_learning import get_learning_stats
    AUTONOMOUS_LEARNING_AVAILABLE = True
except ImportError:
    AUTONOMOUS_LEARNING_AVAILABLE = False

try:
    from meta_learning_system import MetaLearningSystem
    META_LEARNING_AVAILABLE = True
    meta_learning = MetaLearningSystem("beca_memory.db")
except ImportError:
    META_LEARNING_AVAILABLE = False
    meta_learning = None

# Initialize FastAPI
app = FastAPI(
    title="BECA API",
    description="Badass Expert Coding Agent - REST API with Plan/Act modes",
    version="2.0.0"
)

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Models
# ============================================================================

class ChatMode(str):
    PLAN = "plan"
    ACT = "act"

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    message: str
    mode: Literal["plan", "act"] = "plan"
    history: List[ChatMessage] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    mode: str
    files_changed: List[str] = []
    commands_executed: List[str] = []
    plan: Optional[str] = None

class FileTreeNode(BaseModel):
    name: str
    path: str
    type: Literal["file", "directory"]
    children: Optional[List['FileTreeNode']] = None
    status: Optional[Literal["new", "modified", "unchanged"]] = None

class FileReadRequest(BaseModel):
    path: str

class FileReadResponse(BaseModel):
    content: str
    language: str
    path: str

class DiffRequest(BaseModel):
    path: str
    original_content: Optional[str] = None

class DiffResponse(BaseModel):
    diff: str
    path: str
    has_changes: bool

class StatusResponse(BaseModel):
    agent_available: bool
    autonomous_learning: Optional[Dict[str, Any]] = None
    meta_learning: Optional[Dict[str, Any]] = None
    ollama_status: str = "unknown"

# ============================================================================
# Global State
# ============================================================================

# Track active sessions and their modes
sessions: Dict[str, Dict[str, Any]] = {}

# Store original file contents for diffing
file_cache: Dict[str, str] = {}

# ============================================================================
# Helper Functions
# ============================================================================

def get_file_tree(base_path: str = ".") -> FileTreeNode:
    """
    Build file tree structure
    """
    path = Path(base_path)
    
    # Directories to skip
    skip_dirs = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv',
        '.ollama', '.vscode', 'google-cloud-sdk'
    }
    
    def build_node(p: Path) -> Optional[FileTreeNode]:
        if p.name in skip_dirs:
            return None
            
        if p.is_file():
            # Check file status
            status = "unchanged"
            if FILE_TRACKER_AVAILABLE:
                if str(p) in file_tracker.new_files:
                    status = "new"
                elif str(p) in file_tracker.modified_files:
                    status = "modified"
            
            return FileTreeNode(
                name=p.name,
                path=str(p.relative_to(path)),
                type="file",
                status=status
            )
        elif p.is_dir():
            children = []
            try:
                for child in sorted(p.iterdir()):
                    node = build_node(child)
                    if node:
                        children.append(node)
            except PermissionError:
                pass
            
            return FileTreeNode(
                name=p.name,
                path=str(p.relative_to(path)),
                type="directory",
                children=children if children else None
            )
        return None
    
    root = build_node(path)
    return root if root else FileTreeNode(
        name=".",
        path=".",
        type="directory",
        children=[]
    )

def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.md': 'markdown',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.sh': 'bash',
        '.bat': 'batch',
        '.sql': 'sql',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
    }
    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, 'text')

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "BECA API",
        "version": "2.0.0",
        "status": "running",
        "modes": ["plan", "act"],
        "endpoints": [
            "/api/chat",
            "/api/files/tree",
            "/api/files/read",
            "/api/files/diff",
            "/api/status",
            "/health"
        ]
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_available": AGENT_AVAILABLE,
        "autonomous_learning": AUTONOMOUS_LEARNING_AVAILABLE,
        "meta_learning": META_LEARNING_AVAILABLE
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint with Plan/Act mode support
    
    Plan Mode: BECA analyzes and creates a plan without executing
    Act Mode: BECA executes the plan and makes changes
    """
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="Agent not available")
    
    try:
        # Add mode context to the message
        mode_context = ""
        if request.mode == "plan":
            mode_context = """
[PLAN MODE ACTIVE]
You are in PLAN mode. Your task is to:
1. Analyze the user's request carefully
2. Read relevant files to understand the context
3. Ask clarifying questions if needed
4. Create a detailed step-by-step plan
5. DO NOT execute any file writes or commands
6. Present the plan for user approval

Respond with your analysis and plan."""
        else:  # act mode
            mode_context = """
[ACT MODE ACTIVE]
You are in ACT mode. Your task is to:
1. Execute the approved plan
2. Create and modify files as needed
3. Run necessary commands
4. Provide progress updates
5. Show what you're changing

Execute the plan now."""
        
        # Combine context with user message
        full_message = f"{mode_context}\n\nUser Request: {request.message}"
        
        # Get response from agent
        response = chat_with_agent(full_message)
        
        # Track files and commands (would need to parse from response)
        # For now, check file tracker
        files_changed = []
        if FILE_TRACKER_AVAILABLE:
            files_changed = list(file_tracker.new_files) + list(file_tracker.modified_files)
        
        return ChatResponse(
            response=response,
            mode=request.mode,
            files_changed=files_changed,
            commands_executed=[],
            plan=response if request.mode == "plan" else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/tree", response_model=FileTreeNode)
async def get_files_tree():
    """Get project file tree"""
    try:
        return get_file_tree()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/read", response_model=FileReadResponse)
async def read_file(request: FileReadRequest):
    """Read a file with syntax highlighting support"""
    try:
        file_path = Path(request.path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cache original content for diffing
        file_cache[request.path] = content
        
        return FileReadResponse(
            content=content,
            language=detect_language(request.path),
            path=request.path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/diff", response_model=DiffResponse)
async def get_file_diff(request: DiffRequest):
    """Generate diff for a file"""
    try:
        file_path = Path(request.path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get current content
        with open(file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Get original content (from cache or request)
        original_content = request.original_content or file_cache.get(request.path, "")
        
        # Simple diff (in production, use difflib)
        has_changes = original_content != current_content
        
        diff_text = ""
        if has_changes:
            diff_text = f"--- Original\n+++ Modified\n\n{current_content}"
        else:
            diff_text = "No changes detected"
        
        return DiffResponse(
            diff=diff_text,
            path=request.path,
            has_changes=has_changes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    status = StatusResponse(agent_available=AGENT_AVAILABLE)
    
    # Get autonomous learning status
    if AUTONOMOUS_LEARNING_AVAILABLE:
        try:
            stats = get_learning_stats()
            status.autonomous_learning = stats
        except:
            pass
    
    # Get meta-learning status
    if META_LEARNING_AVAILABLE and meta_learning:
        try:
            data = meta_learning.get_learning_dashboard_data()
            status.meta_learning = data
        except:
            pass
    
    return status

# ============================================================================
# WebSocket for Real-time Updates (Optional - for streaming)
# ============================================================================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for streaming chat responses"""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")
            mode = data.get("mode", "plan")
            
            # Send response (would implement streaming here)
            await websocket.send_json({
                "type": "message",
                "content": f"Received: {message} in {mode} mode"
            })
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", "8000"))
    print(f"🚀 Starting BECA API on port {port}")
    print(f"📝 API docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
