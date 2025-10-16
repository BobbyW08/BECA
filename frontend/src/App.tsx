import React, { useState } from 'react';
import './App.css';
import FileTree from './components/FileTree';
import CodeViewer from './components/CodeViewer';
import DiffViewer from './components/DiffViewer';
import PlanActToggle from './components/PlanActToggle';
import StatusBar from './components/StatusBar';
import { BECAProvider } from './context/BECAContext';

function App() {
  const [currentMode, setCurrentMode] = useState<'plan' | 'act'>('plan');
  const [activePanel, setActivePanel] = useState<'files' | 'code' | 'diff'>('files');
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  return (
    <BECAProvider>
      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <div className="header-left">
            <h1>🤖 BECA</h1>
            <span className="subtitle">Badass Expert Coding Agent</span>
          </div>
          
          <div className="header-center">
            <PlanActToggle 
              mode={currentMode} 
              onChange={setCurrentMode}
            />
          </div>

          <div className="header-right">
            <button className="icon-button" title="Settings">
              ⚙️
            </button>
          </div>
        </header>

        {/* Status Bar */}
        <StatusBar mode={currentMode} />

        {/* Main Content */}
        <div className="main-content">
          {/* Left Sidebar - File Tree */}
          <aside className="left-sidebar">
            <div className="sidebar-tabs">
              <button 
                className={activePanel === 'files' ? 'active' : ''}
                onClick={() => setActivePanel('files')}
                title="File Explorer"
              >
                📁 Files
              </button>
            </div>
            <div className="sidebar-content">
              {activePanel === 'files' && (
                <FileTree onFileSelect={setSelectedFile} />
              )}
            </div>
          </aside>

          {/* Center - Chat Interface */}
          <main className="chat-container">
            <div className="chat-wrapper">
              <div className="chat-welcome">
                <h2>👋 Welcome to BECA!</h2>
                <p>Your AI coding assistant with Plan & Act modes</p>
                <div className="quick-actions">
                  <button>Create a React app</button>
                  <button>Help me fix a bug</button>
                  <button>Review my code</button>
                  <button>Explain this function</button>
                </div>
              </div>
              <div className="chat-messages">
                {/* Messages will go here */}
              </div>
              <div className="chat-input">
                <textarea
                  placeholder={
                    currentMode === 'plan' 
                      ? "Describe what you want to build (Plan Mode - I'll create a plan first)..."
                      : "What would you like me to build? (Act Mode - I'll execute immediately)"
                  }
                  rows={3}
                />
                <button className="send-button">Send</button>
              </div>
            </div>
          </main>

          {/* Right Sidebar - Code Viewer / Diff */}
          <aside className="right-sidebar">
            <div className="sidebar-tabs">
              <button 
                className={activePanel === 'code' ? 'active' : ''}
                onClick={() => setActivePanel('code')}
                title="Code Viewer"
              >
                💻 Code
              </button>
              <button 
                className={activePanel === 'diff' ? 'active' : ''}
                onClick={() => setActivePanel('diff')}
                title="Diff Viewer"
              >
                🔀 Diff
              </button>
            </div>
            <div className="sidebar-content">
              {activePanel === 'code' && (
                <CodeViewer filePath={selectedFile} />
              )}
              {activePanel === 'diff' && (
                <DiffViewer filePath={selectedFile} />
              )}
            </div>
          </aside>
        </div>
      </div>
    </BECAProvider>
  );
}

export default App;
