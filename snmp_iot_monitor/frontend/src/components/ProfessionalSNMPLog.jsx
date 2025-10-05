import React, { useState, useEffect } from 'react';
import './ProfessionalSNMPLog.css';

const ProfessionalSNMPLog = () => {
    const [snmpMessages, setSnmpMessages] = useState({});
    const [selectedEngine, setSelectedEngine] = useState('Engine-1');
    const [autoRefresh, setAutoRefresh] = useState(true);
    const [filterType, setFilterType] = useState('all');
    const [showDetails, setShowDetails] = useState(false);

    useEffect(() => {
        const fetchSNMPData = async () => {
            try {
                const messagesResponse = await fetch('/api/snmp/messages');
                const messagesData = await messagesResponse.json();
                if (messagesData.success) {
                    setSnmpMessages(messagesData.data);
                }
            } catch (error) {
                console.error('Error fetching SNMP data:', error);
            }
        };

        fetchSNMPData();

        if (autoRefresh) {
            const interval = setInterval(fetchSNMPData, 1000);
            return () => clearInterval(interval);
        }
    }, [autoRefresh]);

    const triggerSNMPSimulation = async () => {
        try {
            const response = await fetch('/api/snmp/simulate');
            const data = await response.json();
            if (data.success) {
                console.log('SNMP simulation triggered successfully');
            }
        } catch (error) {
            console.error('Error triggering SNMP simulation:', error);
        }
    };

    const getMessageTypeIcon = (messageType) => {
        switch (messageType) {
            case 'GET_REQUEST':
                return '🔍';
            case 'GET_RESPONSE':
                return '📤';
            case 'ERROR':
                return '❌';
            default:
                return '📡';
        }
    };

    const getMessageTypeColor = (messageType) => {
        switch (messageType) {
            case 'GET_REQUEST':
                return '#3b82f6';
            case 'GET_RESPONSE':
                return '#10b981';
            case 'ERROR':
                return '#ef4444';
            default:
                return '#6b7280';
        }
    };

    const getMessageTypeLabel = (messageType) => {
        switch (messageType) {
            case 'GET_REQUEST':
                return 'SNMP GET Request';
            case 'GET_RESPONSE':
                return 'SNMP GET Response';
            case 'ERROR':
                return 'SNMP Error';
            default:
                return 'SNMP Message';
        }
    };

    const formatOID = (oid) => {
        return oid.replace(/\./g, '.');
    };

    const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            fractionalSecondDigits: 3
        });
    };

    const currentMessages = snmpMessages[selectedEngine] || [];
    const filteredMessages = filterType === 'all' 
        ? currentMessages 
        : currentMessages.filter(msg => msg.message_type === filterType);
    const recentMessages = filteredMessages.slice(-50).reverse(); // Show last 50 messages

    return (
        <div className="professional-snmp-log">
            <div className="log-header">
                <h2>🔍 Professional SNMP Protocol Monitor</h2>
                <div className="log-controls">
                    <select 
                        value={selectedEngine} 
                        onChange={(e) => setSelectedEngine(e.target.value)}
                        className="engine-selector"
                    >
                        <option value="Engine-1">Engine-1 (Port 1611)</option>
                        <option value="Engine-2">Engine-2 (Port 1612)</option>
                        <option value="Engine-3">Engine-3 (Port 1613)</option>
                    </select>
                    
                    <select 
                        value={filterType} 
                        onChange={(e) => setFilterType(e.target.value)}
                        className="filter-selector"
                    >
                        <option value="all">All Messages</option>
                        <option value="GET_REQUEST">GET Requests</option>
                        <option value="GET_RESPONSE">GET Responses</option>
                        <option value="ERROR">Errors</option>
                    </select>
                    
                    <button 
                        onClick={triggerSNMPSimulation}
                        className="simulate-btn"
                    >
                        🔄 Trigger SNMP Query
                    </button>
                    
                    <label className="auto-refresh-toggle">
                        <input 
                            type="checkbox" 
                            checked={autoRefresh}
                            onChange={(e) => setAutoRefresh(e.target.checked)}
                        />
                        Auto Refresh
                    </label>
                    
                    <label className="details-toggle">
                        <input 
                            type="checkbox" 
                            checked={showDetails}
                            onChange={(e) => setShowDetails(e.target.checked)}
                        />
                        Show Details
                    </label>
                </div>
            </div>

            <div className="log-stats">
                <div className="stat-item">
                    <span className="stat-label">Total Messages:</span>
                    <span className="stat-value">{currentMessages.length}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Filtered:</span>
                    <span className="stat-value">{filteredMessages.length}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Last Update:</span>
                    <span className="stat-value">
                        {currentMessages.length > 0 
                            ? new Date(currentMessages[currentMessages.length - 1].timestamp).toLocaleTimeString()
                            : 'Never'
                        }
                    </span>
                </div>
            </div>

            <div className="log-content">
                <div className="messages-container">
                    {recentMessages.length > 0 ? (
                        recentMessages.map((message, index) => (
                            <div 
                                key={index} 
                                className={`message-item ${message.message_type.toLowerCase()}`}
                            >
                                <div className="message-header">
                                    <span className="message-icon">
                                        {getMessageTypeIcon(message.message_type)}
                                    </span>
                                    <span className="message-type" style={{color: getMessageTypeColor(message.message_type)}}>
                                        {getMessageTypeLabel(message.message_type)}
                                    </span>
                                    <span className="message-timestamp">{formatTimestamp(message.timestamp)}</span>
                                </div>
                                
                                <div className="message-details">
                                    <div className="detail-row">
                                        <span className="detail-label">Engine:</span>
                                        <span className="detail-value">{message.engine_id} (Port {message.port})</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="detail-label">OID:</span>
                                        <span className="detail-value oid-value">{formatOID(message.oid)}</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="detail-label">MIB Name:</span>
                                        <span className="detail-value">{message.mib_name}</span>
                                    </div>
                                    
                                    {showDetails && (
                                        <>
                                            <div className="detail-row">
                                                <span className="detail-label">Data Type:</span>
                                                <span className="detail-value">{message.data_type}</span>
                                            </div>
                                            <div className="detail-row">
                                                <span className="detail-label">Access:</span>
                                                <span className="detail-value">{message.access}</span>
                                            </div>
                                            <div className="detail-row">
                                                <span className="detail-label">Community:</span>
                                                <span className="detail-value">{message.community}</span>
                                            </div>
                                        </>
                                    )}
                                    
                                    {message.value !== undefined && (
                                        <div className="detail-row">
                                            <span className="detail-label">Value:</span>
                                            <span className="detail-value value-highlight">{message.value}</span>
                                        </div>
                                    )}
                                    
                                    {message.error && (
                                        <div className="detail-row error-row">
                                            <span className="detail-label">Error:</span>
                                            <span className="detail-value error-value">{message.error}</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="no-messages">
                            <div className="no-messages-icon">📡</div>
                            <p>No SNMP messages yet</p>
                            <p>Click "Trigger SNMP Query" to start simulation</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfessionalSNMPLog;
