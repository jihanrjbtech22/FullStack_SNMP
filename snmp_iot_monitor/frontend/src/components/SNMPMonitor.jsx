import React, { useState, useEffect } from 'react';
import './SNMPMonitor.css';

const SNMPMonitor = () => {
    const [snmpMessages, setSnmpMessages] = useState({});
    const [mibDefinitions, setMibDefinitions] = useState({});
    const [selectedEngine, setSelectedEngine] = useState('Engine-1');
    const [autoRefresh, setAutoRefresh] = useState(true);

    useEffect(() => {
        const fetchSNMPData = async () => {
            try {
                // Fetch SNMP messages
                const messagesResponse = await fetch('/api/snmp/messages');
                const messagesData = await messagesResponse.json();
                if (messagesData.success) {
                    setSnmpMessages(messagesData.data);
                }

                // Fetch MIB definitions
                const mibResponse = await fetch('/api/snmp/mib');
                const mibData = await mibResponse.json();
                if (mibData.success) {
                    setMibDefinitions(mibData.data);
                }
            } catch (error) {
                console.error('Error fetching SNMP data:', error);
            }
        };

        fetchSNMPData();

        if (autoRefresh) {
            const interval = setInterval(fetchSNMPData, 2000);
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

    const formatOID = (oid) => {
        return oid.replace(/\./g, '.');
    };

    const getMIBName = (oid) => {
        const engine = mibDefinitions[selectedEngine];
        if (engine && engine.mib_definitions) {
            const mib = engine.mib_definitions[oid];
            return mib ? mib.name : 'Unknown';
        }
        return 'Unknown';
    };

    const getMIBDescription = (oid) => {
        const engine = mibDefinitions[selectedEngine];
        if (engine && engine.mib_definitions) {
            const mib = engine.mib_definitions[oid];
            return mib ? mib.description : 'Unknown';
        }
        return 'Unknown';
    };

    const getMIBUnits = (oid) => {
        const engine = mibDefinitions[selectedEngine];
        if (engine && engine.mib_definitions) {
            const mib = engine.mib_definitions[oid];
            return mib ? mib.units : '';
        }
        return '';
    };

    const currentMessages = snmpMessages[selectedEngine] || [];
    const recentMessages = currentMessages.slice(-20).reverse(); // Show last 20 messages

    return (
        <div className="snmp-monitor">
            <div className="snmp-header">
                <h2>🔍 SNMP Protocol Monitor</h2>
                <div className="snmp-controls">
                    <select 
                        value={selectedEngine} 
                        onChange={(e) => setSelectedEngine(e.target.value)}
                        className="engine-selector"
                    >
                        <option value="Engine-1">Engine-1 (Port 1611)</option>
                        <option value="Engine-2">Engine-2 (Port 1612)</option>
                        <option value="Engine-3">Engine-3 (Port 1613)</option>
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
                </div>
            </div>

            <div className="snmp-content">
                <div className="snmp-messages">
                    <h3>📡 SNMP Message Log</h3>
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
                                            {message.message_type}
                                        </span>
                                        <span className="message-timestamp">{message.timestamp}</span>
                                    </div>
                                    <div className="message-details">
                                        <div className="message-oid">
                                            <strong>OID:</strong> {formatOID(message.oid)}
                                        </div>
                                        <div className="message-mib">
                                            <strong>MIB Name:</strong> {message.mib_name}
                                        </div>
                                        {message.value !== undefined && (
                                            <div className="message-value">
                                                <strong>Value:</strong> {message.value} {getMIBUnits(message.oid)}
                                            </div>
                                        )}
                                        {message.error && (
                                            <div className="message-error">
                                                <strong>Error:</strong> {message.error}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="no-messages">
                                <p>No SNMP messages yet. Click "Trigger SNMP Query" to start simulation.</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="snmp-mib">
                    <h3>📋 MIB Definitions</h3>
                    <div className="mib-container">
                        {mibDefinitions[selectedEngine] && mibDefinitions[selectedEngine].mib_definitions ? (
                            Object.entries(mibDefinitions[selectedEngine].mib_definitions).map(([oid, mib]) => (
                                <div key={oid} className="mib-item">
                                    <div className="mib-oid">
                                        <strong>OID:</strong> {formatOID(oid)}
                                    </div>
                                    <div className="mib-name">
                                        <strong>Name:</strong> {mib.name}
                                    </div>
                                    <div className="mib-description">
                                        <strong>Description:</strong> {mib.description}
                                    </div>
                                    <div className="mib-details">
                                        <span className="mib-type">Type: {mib.type}</span>
                                        <span className="mib-units">Units: {mib.units}</span>
                                        <span className="mib-access">Access: {mib.access}</span>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="no-mib">
                                <p>Loading MIB definitions...</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SNMPMonitor;
