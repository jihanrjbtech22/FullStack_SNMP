import React from 'react';
import './EngineCard.css';

/**
 * EngineCard Component
 * Displays individual engine data in a card format with health indicators
 */
const EngineCard = ({ engineData, isExpanded, onToggle }) => {
  if (!engineData) {
    return (
      <div className="engine-card loading">
        <div className="loading-spinner">⏳</div>
        <p>Loading engine data...</p>
      </div>
    );
  }

  const {
    engine_id,
    temperature,
    rpm,
    current,
    power,
    status,
    uptime,
    health_status,
    last_updated
  } = engineData;

  // Health status styling
  const getHealthClass = (status) => {
    switch (status) {
      case 'critical': return 'health-critical';
      case 'warning': return 'health-warning';
      case 'normal': return 'health-normal';
      default: return 'health-unknown';
    }
  };

  const getHealthIcon = (status) => {
    switch (status) {
      case 'critical': return '🔴';
      case 'warning': return '🟡';
      case 'normal': return '🟢';
      default: return '⚪';
    }
  };

  const getStatusText = (status) => {
    return status === 1 ? 'Running' : 'Stopped';
  };

  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const formatLastUpdated = (timestamp) => {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  return (
    <div className={`engine-card ${getHealthClass(health_status)} ${isExpanded ? 'expanded' : ''}`}>
      <div className="engine-header" onClick={onToggle}>
        <div className="engine-title">
          <h3>{engine_id}</h3>
          <span className="health-indicator">
            {getHealthIcon(health_status)} {health_status.toUpperCase()}
          </span>
        </div>
        <div className="engine-status">
          <span className={`status-badge ${status === 1 ? 'running' : 'stopped'}`}>
            {getStatusText(status)}
          </span>
          <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
        </div>
      </div>

      <div className="engine-metrics">
        <div className="metric-row">
          <div className="metric">
            <span className="metric-label">🌡️ Temperature</span>
            <span className="metric-value">{temperature}°C</span>
          </div>
          <div className="metric">
            <span className="metric-label">⚡ RPM</span>
            <span className="metric-value">{rpm.toLocaleString()}</span>
          </div>
        </div>

        <div className="metric-row">
          <div className="metric">
            <span className="metric-label">🔌 Current</span>
            <span className="metric-value">{current}A</span>
          </div>
          <div className="metric">
            <span className="metric-label">⚡ Power</span>
            <span className="metric-value">{power}W</span>
          </div>
        </div>

        {isExpanded && (
          <div className="engine-details">
            <div className="detail-row">
              <span className="detail-label">Uptime:</span>
              <span className="detail-value">{formatUptime(uptime)}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Last Updated:</span>
              <span className="detail-value">{formatLastUpdated(last_updated)}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EngineCard;
