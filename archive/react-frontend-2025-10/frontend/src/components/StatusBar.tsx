import React, { useEffect, useState } from 'react';
import { useBECA } from '../context/BECAContext';
import './StatusBar.css';

interface StatusBarProps {
  mode: 'plan' | 'act';
}

const StatusBar: React.FC<StatusBarProps> = ({ mode }) => {
  const { getStatus } = useBECA();
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getStatus();
        setStatus(data);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    // Refresh status every 30 seconds
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, [getStatus]);

  const getModeDescription = () => {
    if (mode === 'plan') {
      return '📋 Plan Mode: BECA will analyze and create a plan without executing';
    }
    return '⚡ Act Mode: BECA will execute changes immediately';
  };

  return (
    <div className="status-bar">
      <div className="status-section mode-status">
        {getModeDescription()}
      </div>
      
      {!loading && status && (
        <>
          <div className="status-section">
            <span className={`status-indicator ${status.agent_available ? 'online' : 'offline'}`}></span>
            {status.agent_available ? 'Agent Online' : 'Agent Offline'}
          </div>

          {status.autonomous_learning && (
            <div className="status-section">
              🧠 Auto-Learning: {status.autonomous_learning.active ? 'Active' : 'Inactive'}
            </div>
          )}

          {status.meta_learning && (
            <div className="status-section">
              📊 Meta-Learning: {status.meta_learning.features_built || 0} features
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default StatusBar;
