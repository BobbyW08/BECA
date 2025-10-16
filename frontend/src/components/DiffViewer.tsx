import React, { useEffect, useState } from 'react';
import { useBECA } from '../context/BECAContext';
import './DiffViewer.css';

interface DiffViewerProps {
  filePath: string | null;
}

const DiffViewer: React.FC<DiffViewerProps> = ({ filePath }) => {
  const { getDiff } = useBECA();
  const [diff, setDiff] = useState<string>('');
  const [hasChanges, setHasChanges] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!filePath) {
      setDiff('');
      setHasChanges(false);
      return;
    }

    const fetchDiff = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const data = await getDiff(filePath);
        setDiff(data.diff);
        setHasChanges(data.has_changes);
      } catch (err: any) {
        setError(err.message || 'Failed to get diff');
      } finally {
        setLoading(false);
      }
    };

    fetchDiff();
  }, [filePath, getDiff]);

  if (!filePath) {
    return (
      <div className="diff-viewer empty">
        <div className="empty-state">
          <p>🔄</p>
          <p>Select a file to view changes</p>
          <p className="hint">View a file in Code panel first, then check here for changes</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="diff-viewer loading">
        <p>Loading diff...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="diff-viewer error">
        <p>❌ Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="diff-viewer">
      <div className="diff-viewer-header">
        <span className="file-name">{filePath}</span>
        {hasChanges ? (
          <span className="changes-badge modified">Modified</span>
        ) : (
          <span className="changes-badge unchanged">No Changes</span>
        )}
      </div>
      <div className="diff-viewer-content">
        <pre className="diff-content">{diff}</pre>
      </div>
    </div>
  );
};

export default DiffViewer;
