import React from 'react';
import './PlanActToggle.css';

interface PlanActToggleProps {
  mode: 'plan' | 'act';
  onChange: (mode: 'plan' | 'act') => void;
}

const PlanActToggle: React.FC<PlanActToggleProps> = ({ mode, onChange }) => {
  return (
    <div className="plan-act-toggle">
      <button
        className={`toggle-button ${mode === 'plan' ? 'active' : ''}`}
        onClick={() => onChange('plan')}
        title="Plan Mode - BECA creates a plan without executing"
      >
        <span className="mode-icon">📋</span>
        <span className="mode-label">Plan</span>
      </button>
      
      <div className="toggle-slider" data-mode={mode}>
        <div className="slider-indicator"></div>
      </div>
      
      <button
        className={`toggle-button ${mode === 'act' ? 'active' : ''}`}
        onClick={() => onChange('act')}
        title="Act Mode - BECA executes immediately"
      >
        <span className="mode-icon">⚡</span>
        <span className="mode-label">Act</span>
      </button>
    </div>
  );
};

export default PlanActToggle;
