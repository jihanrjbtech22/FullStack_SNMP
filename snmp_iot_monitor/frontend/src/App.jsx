import React, { useState, useEffect } from 'react';
import EngineCard from './components/EngineCard';
import Charts from './components/Charts';
import { fetchAllEngines, startPolling } from './api/fetchData';
import './App.css';

/**
 * Main App Component
 * Industrial IoT SNMP Monitoring Dashboard
 */
const App = () => {
  const [enginesData, setEnginesData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedParameter, setSelectedParameter] = useState('temperature');
  const [expandedEngine, setExpandedEngine] = useState(null);
  const [isPolling, setIsPolling] = useState(false);

  // Available parameters for charting
  const parameters = [
    { value: 'temperature', label: 'Temperature', icon: '🌡️' },
    { value: 'rpm', label: 'RPM', icon: '⚡' },
    { value: 'current', label: 'Current', icon: '🔌' },
    { value: 'power', label: 'Power', icon: '⚡' },
  ];

  // Initialize data fetching and polling
  useEffect(() => {
    const initializeData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Initial data fetch
        const data = await fetchAllEngines();
        setEnginesData(data);
        
        // Start polling for real-time updates
        const stopPolling = startPolling((data) => {
          setEnginesData(data);
          setError(null);
        }, 2000); // Poll every 2 seconds
        
        setIsPolling(true);
        setLoading(false);
        
        // Cleanup function
        return () => {
          stopPolling();
          setIsPolling(false);
        };
      } catch (err) {
        console.error('Failed to initialize data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    const cleanup = initializeData();
    return () => {
      if (cleanup && typeof cleanup.then === 'function') {
        cleanup.then(cleanupFn => cleanupFn && cleanupFn());
      }
    };
  }, []);

  // Handle engine card expansion
  const handleEngineToggle = (engineId) => {
    setExpandedEngine(expandedEngine === engineId ? null : engineId);
  };

  // Handle parameter selection for charts
  const handleParameterChange = (parameter) => {
    setSelectedParameter(parameter);
  };

  // Get summary statistics
  const getSummaryStats = () => {
    if (!enginesData || !enginesData.data) return null;

    const engines = Object.values(enginesData.data);
    const totalEngines = engines.length;
    const runningEngines = engines.filter(engine => engine.status === 1).length;
    const avgTemperature = engines.reduce((sum, engine) => sum + engine.temperature, 0) / totalEngines;
    const avgPower = engines.reduce((sum, engine) => sum + engine.power, 0) / totalEngines;

    return {
      totalEngines,
      runningEngines,
      avgTemperature: Math.round(avgTemperature * 10) / 10,
      avgPower: Math.round(avgPower),
    };
  };

  // Render loading state
  if (loading) {
    return (
      <div className="app">
        <div className="app-header">
          <h1>🏭 Industrial IoT Monitor</h1>
          <p>SNMP Engine Monitoring Dashboard</p>
        </div>
        <div className="loading-container">
          <div className="loading-spinner">⏳</div>
          <h2>Initializing SNMP Monitoring...</h2>
          <p>Connecting to engine agents...</p>
        </div>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="app">
        <div className="app-header">
          <h1>🏭 Industrial IoT Monitor</h1>
          <p>SNMP Engine Monitoring Dashboard</p>
        </div>
        <div className="error-container">
          <div className="error-icon">❌</div>
          <h2>Connection Error</h2>
          <p>{error}</p>
          <button 
            className="retry-button"
            onClick={() => window.location.reload()}
          >
            🔄 Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const summary = getSummaryStats();

  return (
    <div className="app">
      {/* Header */}
      <div className="app-header">
        <div className="header-content">
          <h1>🏭 Industrial IoT Monitor</h1>
          <p>SNMP Engine Monitoring Dashboard</p>
        </div>
        <div className="header-status">
          <div className={`status-indicator ${isPolling ? 'connected' : 'disconnected'}`}>
            {isPolling ? '🟢 Connected' : '🔴 Disconnected'}
          </div>
          <div className="last-update">
            Last Update: {enginesData?.timestamp ? 
              new Date(enginesData.timestamp * 1000).toLocaleTimeString() : 
              'Never'
            }
          </div>
        </div>
      </div>

      {/* Summary Stats */}
      {summary && (
        <div className="summary-stats">
          <div className="stat-card">
            <div className="stat-icon">🏭</div>
            <div className="stat-content">
              <div className="stat-value">{summary.totalEngines}</div>
              <div className="stat-label">Total Engines</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <div className="stat-value">{summary.runningEngines}</div>
              <div className="stat-label">Running</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🌡️</div>
            <div className="stat-content">
              <div className="stat-value">{summary.avgTemperature}°C</div>
              <div className="stat-label">Avg Temperature</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <div className="stat-value">{summary.avgPower}W</div>
              <div className="stat-label">Avg Power</div>
            </div>
          </div>
        </div>
      )}

      {/* Parameter Selection */}
      <div className="parameter-selector">
        <h3>📊 Chart Parameter</h3>
        <div className="parameter-buttons">
          {parameters.map((param) => (
            <button
              key={param.value}
              className={`parameter-button ${selectedParameter === param.value ? 'active' : ''}`}
              onClick={() => handleParameterChange(param.value)}
            >
              <span className="param-icon">{param.icon}</span>
              <span className="param-label">{param.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Charts Section */}
      <Charts 
        enginesData={enginesData}
        selectedParameter={selectedParameter}
        timeRange={60}
      />

      {/* Engine Cards */}
      <div className="engines-section">
        <h3>🔧 Engine Status</h3>
        <div className="engines-grid">
          {enginesData?.data && Object.entries(enginesData.data).map(([engineId, engineData]) => (
            <EngineCard
              key={engineId}
              engineData={engineData}
              isExpanded={expandedEngine === engineId}
              onToggle={() => handleEngineToggle(engineId)}
            />
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="app-footer">
        <p>Industrial IoT SNMP Monitoring System | Real-time Engine Data</p>
        <p>Powered by SNMP Protocol & React Dashboard</p>
      </div>
    </div>
  );
};

export default App;
