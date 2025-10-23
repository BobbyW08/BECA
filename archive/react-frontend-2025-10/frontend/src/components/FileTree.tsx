import React, { useEffect, useState } from 'react';
import { useBECA } from '../context/BECAContext';
import './FileTree.css';

interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: FileNode[];
  status?: 'new' | 'modified' | 'unchanged';
}

interface FileTreeProps {
  onFileSelect: (path: string) => void;
}

const FileTree: React.FC<FileTreeProps> = ({ onFileSelect }) => {
  const { getFileTree } = useBECA();
  const [tree, setTree] = useState<FileNode | null>(null);
  const [expanded, setExpanded] = useState<Set<string>>(new Set(['.']));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const data = await getFileTree();
        setTree(data);
      } catch (error) {
        console.error('Failed to fetch file tree:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTree();
  }, [getFileTree]);

  const toggleExpanded = (path: string) => {
    const newExpanded = new Set(expanded);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    setExpanded(newExpanded);
  };

  const renderNode = (node: FileNode, depth: number = 0): React.ReactElement => {
    const isExpanded = expanded.has(node.path);
    const hasChildren = node.children && node.children.length > 0;

    return (
      <div key={node.path} className="tree-node">
        <div 
          className={`tree-item ${node.type}`}
          style={{ paddingLeft: `${depth * 16}px` }}
          onClick={() => {
            if (node.type === 'directory') {
              toggleExpanded(node.path);
            } else {
              onFileSelect(node.path);
            }
          }}
        >
          {node.type === 'directory' && (
            <span className="tree-icon">
              {isExpanded ? '▼' : '▶'}
            </span>
          )}
          
          <span className="tree-icon">
            {node.type === 'directory' ? '📁' : '📄'}
          </span>
          
          <span className={`tree-label ${node.status}`}>
            {node.name}
            {node.status === 'new' && <span className="status-badge new">N</span>}
            {node.status === 'modified' && <span className="status-badge modified">M</span>}
          </span>
        </div>

        {node.type === 'directory' && isExpanded && hasChildren && (
          <div className="tree-children">
            {node.children!.map(child => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return <div className="file-tree loading">Loading files...</div>;
  }

  if (!tree) {
    return <div className="file-tree error">Failed to load files</div>;
  }

  return (
    <div className="file-tree">
      <div className="file-tree-header">
        <h3>Files</h3>
        <button className="refresh-button" onClick={() => window.location.reload()}>
          🔄
        </button>
      </div>
      <div className="file-tree-content">
        {tree.children && tree.children.map(child => renderNode(child, 0))}
      </div>
    </div>
  );
};

export default FileTree;
