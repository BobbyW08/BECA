import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import FileTree from './components/FileTree';
import CodeViewer from './components/CodeViewer';
import DiffViewer from './components/DiffViewer';
import PlanActToggle from './components/PlanActToggle';
import StatusBar from './components/StatusBar';
import { BECAProvider, useBECA } from './context/BECAContext';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

function AppContent() {
  const { mode, setMode, sendMessage, apiUrl } = useBECA();
  const [currentMode, setCurrentMode] = useState<'plan' | 'act'>('plan');
  const [activePanel, setActivePanel] = useState<'files' | 'code' | 'diff'>('files');
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Sync local mode with context
  useEffect(() => {
    setMode(currentMode);
  }, [currentMode, setMode]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message?: string) => {
    const messageToSend = message || inputValue.trim();
    
    if (!messageToSend || isLoading) return;

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: messageToSend,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(messageToSend);
      
      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response || response.message || 'Response received',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Error sending message:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to connect to BECA backend';
      setError(errorMsg);
      
      // Add error message to chat
      const errorMessage: Message = {
        role: 'system',
        content: `Error: ${errorMsg}. Make sure the backend is running at ${apiUrl}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleQuickAction = (action: string) => {
    handleSendMessage(action);
  };

  return (
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
          <button 
            className="icon-button" 
            title="Settings"
            onClick={() => setShowSettings(!showSettings)}
          >
            ⚙️
          </button>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="settings-panel">
          <div className="settings-content">
            <h3>Settings</h3>
            <div className="setting-item">
              <label>API URL:</label>
              <input type="text" value={apiUrl} readOnly />
            </div>
            <div className="setting-item">
              <label>Current Mode:</label>
              <span>{currentMode === 'plan' ? 'Plan Mode' : 'Act Mode'}</span>
            </div>
            <button onClick={() => setShowSettings(false)}>Close</button>
          </div>
        </div>
      )}

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
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <h2>👋 Welcome to BECA!</h2>
                <p>Your AI coding assistant with Plan & Act modes</p>
                <div className="mode-info">
                  <div className="mode-badge">{currentMode === 'plan' ? '📋 Plan Mode' : '⚡ Act Mode'}</div>
                  <p>
                    {currentMode === 'plan' 
                      ? "I'll create a detailed plan before executing"
                      : "I'll execute your requests immediately"}
                  </p>
                </div>
                <div className="quick-actions">
                  <button onClick={() => handleQuickAction('Create a React app')}>
                    Create a React app
                  </button>
                  <button onClick={() => handleQuickAction('Help me fix a bug')}>
                    Help me fix a bug
                  </button>
                  <button onClick={() => handleQuickAction('Review my code')}>
                    Review my code
                  </button>
                  <button onClick={() => handleQuickAction('Explain this function')}>
                    Explain this function
                  </button>
                </div>
              </div>
            ) : (
              <div className="chat-messages">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`message message-${msg.role}`}>
                    <div className="message-header">
                      <span className="message-role">
                        {msg.role === 'user' ? '👤 You' : 
                         msg.role === 'assistant' ? '🤖 BECA' : 
                         '⚠️ System'}
                      </span>
                      <span className="message-time">
                        {msg.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="message-content">
                      {msg.content}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="message message-assistant message-loading">
                    <div className="message-header">
                      <span className="message-role">🤖 BECA</span>
                    </div>
                    <div className="message-content">
                      <span className="loading-dots">Thinking</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
            
            <div className="chat-input-container">
              {error && (
                <div className="error-banner">
                  ⚠️ {error}
                  <button onClick={() => setError(null)}>✕</button>
                </div>
              )}
              <div className="chat-input">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={
                    currentMode === 'plan' 
                      ? "Describe what you want to build (Plan Mode - I'll create a plan first)..."
                      : "What would you like me to build? (Act Mode - I'll execute immediately)"
                  }
                  rows={3}
                  disabled={isLoading}
                />
                <button 
                  className="send-button"
                  onClick={() => handleSendMessage()}
                  disabled={isLoading || !inputValue.trim()}
                  title="Send message (Enter)"
                >
                  {isLoading ? '⏳' : '📤'} Send
                </button>
              </div>
              <div className="input-hint">
                Press Enter to send • Shift+Enter for new line
              </div>
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
  );
}

function App() {
  return (
    <BECAProvider>
      <AppContent />
    </BECAProvider>
  );
}

export default App;
