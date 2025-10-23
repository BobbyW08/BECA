import React, { useEffect, useState } from 'react';
import { useBECA } from '../context/BECAContext';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './CodeViewer.css';

interface CodeViewerProps {
  filePath: string | null;
}

const CodeViewer: React.FC<CodeViewerProps> = ({ filePath }) => {
  const { readFile } = useBECA();
  const [content, setContent] = useState<string>('');
  const [language, setLanguage] = useState<string>('text');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!filePath) {
      setContent('');
      return;
    }

    const fetchFile = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const data = await readFile(filePath);
        setContent(data.content);
        setLanguage(data.language);
      } catch (err: any) {
        setError(err.message || 'Failed to read file');
      } finally {
        setLoading(false);
      }
    };

    fetchFile();
  }, [filePath, readFile]);

  if (!filePath) {
    return (
      <div className="code-viewer empty">
        <div className="empty-state">
          <p>📄</p>
          <p>Select a file to view its contents</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="code-viewer loading">
        <p>Loading file...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="code-viewer error">
        <p>❌ Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="code-viewer">
      <div className="code-viewer-header">
        <span className="file-name">{filePath}</span>
        <span className="language-badge">{language}</span>
      </div>
      <div className="code-viewer-content">
        <SyntaxHighlighter
          language={language}
          style={vscDarkPlus}
          showLineNumbers={true}
          wrapLines={true}
          customStyle={{
            margin: 0,
            padding: '1rem',
            fontSize: '0.875rem',
            background: 'transparent',
          }}
        >
          {content}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeViewer;
