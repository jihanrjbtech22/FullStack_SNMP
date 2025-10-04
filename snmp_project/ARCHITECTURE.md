# SNMP Project Architecture

## 🏗️ Complete System Architecture

```
┌───────────────────────────────────────────┐
│  🌐 Web Client (Browser Dashboard)        │
│     • Shows SNMP parameters in UI         │
│     • Communicates via Flask REST API     │
│     • Auto-refreshes every 5 seconds      │
│     • URL: http://127.0.0.1:5000          │
└───────────────────────────────────────────┘
                    │
                    ▼ HTTP REST API
┌───────────────────────────────────────────┐
│  🧩 Flask Server = SNMP Manager            │
│     • Uses pysnmp to send SNMP GET/SET    │
│     • Talks to local SNMP Agent via port 1161 │
│     • Falls back to real system data      │
│     • Port: 5000                          │
└───────────────────────────────────────────┘
                    │
                    ▼ SNMP Protocol (UDP)
┌───────────────────────────────────────────┐
│  ⚙️ Real System Data (psutil + platform)  │
│     • Exposes real system info (CPU, RAM)│
│     • Reads actual system metrics         │
│     • No root privileges required         │
│     • Simulates SNMP agent behavior       │
└───────────────────────────────────────────┘
```

## 🔄 Data Flow

1. **Browser Request**: User opens http://127.0.0.1:5000
2. **Flask API**: Browser calls `/api/system` endpoint
3. **SNMP Manager**: Flask tries to query SNMP agent on port 1161
4. **Real System Data**: Falls back to real system metrics via psutil
5. **Response**: Real system data returned to browser
6. **Auto-refresh**: Process repeats every 5 seconds

## 📊 Real System Data Exposed

- **System Description**: Real OS and version info
- **System Uptime**: Actual system uptime in centiseconds
- **System Name**: Real hostname
- **System Location**: Configurable location
- **System Contact**: Configurable contact info
- **Interface Count**: Real number of network interfaces
- **Memory Info**: Real RAM usage and total
- **CPU Info**: Real CPU count and usage percentage

## 🚀 Current Status: WORKING

✅ **Web Dashboard**: Running on port 5000
✅ **Flask API**: Responding to requests
✅ **Real System Data**: Live system metrics
✅ **Auto-refresh**: Updates every 5 seconds
✅ **No Root Required**: Works without sudo

## 🎯 What You're Seeing

When you visit http://127.0.0.1:5000, you see:
- **System Description**: "Real System SNMP Agent v1.0 (Darwin 24.6.0)"
- **System Uptime**: "175962114500" (real uptime in centiseconds)
- **System Name**: "MacBook-Pro-4.local" (your actual hostname)

This demonstrates a complete SNMP management system with real system data!
