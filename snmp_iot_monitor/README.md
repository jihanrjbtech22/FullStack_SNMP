# Industrial IoT SNMP Monitor

## 🏭 Project Overview

A comprehensive **Industrial IoT SNMP Monitoring System** that simulates 3 industrial engines with real-time sensor data monitoring. The system demonstrates SNMP Manager-Agent architecture with a modern web dashboard for visualizing engine parameters including temperature, RPM, current, and power output.

## 🎯 Key Features

### 🔧 Engine Simulation
- **3 Simulated Engines** running on different SNMP ports (1611, 1612, 1613)
- **Realistic Sensor Data** with smooth variations and time-based patterns
- **Health Status Monitoring** with color-coded alerts (Normal/Warning/Critical)
- **SNMP OID Support** for standard industrial monitoring parameters

### 📊 Real-Time Dashboard
- **Live Data Updates** every 2 seconds via API polling
- **Interactive Charts** with Chart.js for time-series visualization
- **Engine Cards** with expandable details and health indicators
- **Responsive Design** for desktop, tablet, and mobile devices
- **Parameter Selection** for different chart views (Temperature, RPM, Current, Power)

### 🌐 Full-Stack Architecture
- **Backend**: Python Flask with SNMP simulation
- **Frontend**: React with modern UI components
- **API**: RESTful endpoints for engine data
- **Real-time**: WebSocket-like polling for live updates

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Engine-1      │    │   Engine-2      │    │   Engine-3      │
│   Port: 1611    │    │   Port: 1612    │    │   Port: 1613    │
│   SNMP Agent    │    │   SNMP Agent    │    │   SNMP Agent    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     SNMP Manager          │
                    │   (Flask Backend)         │
                    │   Port: 5003              │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    React Frontend         │
                    │   Port: 3000              │
                    │   Web Dashboard           │
                    └───────────────────────────┘
```

## 📁 Project Structure

```
snmp_iot_monitor/
├── backend/
│   ├── app.py                 # Flask web server
│   ├── snmp_manager.py        # SNMP manager for querying agents
│   ├── snmp_agent_sim.py      # Simulated SNMP agents
│   └── requirements.txt       # Python dependencies
└── frontend/
    ├── package.json           # Node.js dependencies
    ├── public/
    │   └── index.html         # HTML template
    └── src/
        ├── App.jsx            # Main React component
        ├── App.css            # Main styles
        ├── index.js           # React entry point
        ├── api/
        │   └── fetchData.js   # API service functions
        └── components/
            ├── EngineCard.jsx # Engine status cards
            ├── EngineCard.css
            ├── Charts.jsx     # Time-series charts
            └── Charts.css
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd FullStack_SNMP/snmp_iot_monitor/backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python app.py
   ```

   The backend will start on `http://127.0.0.1:5003`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd FullStack_SNMP/snmp_iot_monitor/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will start on `http://127.0.0.1:3000`

### Access the Dashboard

Open your browser and visit: **http://127.0.0.1:3000**

## 📊 Monitored Parameters

### Engine Parameters
- **🌡️ Temperature**: Engine temperature in °C (20-120°C range)
- **⚡ RPM**: Engine revolutions per minute (500-3000 RPM)
- **🔌 Current**: Electrical current in Amperes (0-30A)
- **⚡ Power**: Power output in Watts (0-2500W)
- **⏱️ Uptime**: Engine running time in seconds
- **📊 Status**: Running/Stopped status

### Health Status
- **🟢 Normal**: Temperature < 80°C
- **🟡 Warning**: Temperature 80-100°C
- **🔴 Critical**: Temperature > 100°C

## 🔧 SNMP OIDs

The system uses custom OIDs for industrial engine monitoring:

```
1.3.6.1.4.1.9999.1.1.1.0  - Engine Temperature (°C)
1.3.6.1.4.1.9999.1.1.2.0  - Engine RPM
1.3.6.1.4.1.9999.1.1.3.0  - Engine Current (A)
1.3.6.1.4.1.9999.1.1.4.0  - Engine Power Output (W)
1.3.6.1.4.1.9999.1.1.5.0  - Engine Status (1=Running, 0=Stopped)
1.3.6.1.4.1.9999.1.1.6.0  - Engine Uptime (seconds)
```

## 🌐 API Endpoints

### REST API (Backend: Port 5003)

- `GET /api/engines` - Get data for all engines
- `GET /api/engines/<engine_id>` - Get data for specific engine
- `GET /api/summary` - Get summary statistics
- `GET /api/health` - Health check endpoint

### Example API Response

```json
{
  "success": true,
  "data": {
    "Engine-1": {
      "engine_id": "Engine-1",
      "port": 1611,
      "temperature": 42.3,
      "rpm": 1750,
      "current": 11.8,
      "power": 1450,
      "status": 1,
      "uptime": 3600,
      "health_status": "normal",
      "last_updated": "2024-01-15T10:30:00"
    }
  },
  "timestamp": 1705312200
}
```

## 🎨 Dashboard Features

### Real-Time Monitoring
- **Live Updates**: Data refreshes every 2 seconds
- **Status Indicators**: Color-coded health status for each engine
- **Summary Statistics**: Total engines, running count, averages

### Interactive Charts
- **Time-Series Visualization**: Chart.js powered charts
- **Parameter Selection**: Switch between Temperature, RPM, Current, Power
- **Time Range Control**: 30s, 1min, 5min, 10min views
- **Multi-Engine Comparison**: Overlay all engines on same chart

### Engine Cards
- **Expandable Details**: Click to show/hide additional information
- **Health Alerts**: Visual indicators for engine health
- **Real-Time Values**: Live parameter updates
- **Status Badges**: Running/Stopped status indicators

## 🛠️ Configuration

### Backend Configuration
- **Port**: 5003 (configurable in `app.py`)
- **Polling Interval**: 2 seconds (configurable in `snmp_manager.py`)
- **Engine Ports**: 1611, 1612, 1613 (configurable in `snmp_agent_sim.py`)

### Frontend Configuration
- **API URL**: `http://127.0.0.1:5003/api` (configurable via environment)
- **Polling Interval**: 2 seconds (configurable in `fetchData.js`)
- **Chart Time Range**: 60 seconds default (configurable in `Charts.jsx`)

## 🔍 Troubleshooting

### Common Issues

1. **Backend won't start:**
   - Check if port 5003 is available
   - Ensure all Python dependencies are installed
   - Check virtual environment is activated

2. **Frontend won't connect:**
   - Verify backend is running on port 5003
   - Check CORS settings in Flask app
   - Ensure API URL is correct

3. **No data showing:**
   - Check browser console for errors
   - Verify SNMP manager is polling engines
   - Check network connectivity

4. **Charts not updating:**
   - Verify polling is active (check browser network tab)
   - Check if data is being received from API
   - Ensure Chart.js is properly loaded

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export FLASK_DEBUG=1
export REACT_APP_DEBUG=1
```

## 🚀 Deployment

### Production Setup

1. **Backend (Gunicorn):**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5003 app:app
   ```

2. **Frontend (Build):**
   ```bash
   npm run build
   # Serve static files with nginx or similar
   ```

### Docker Deployment

Create `Dockerfile` for containerized deployment:
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5003
CMD ["python", "app.py"]
```

## 📚 Educational Value

This project demonstrates:

- **SNMP Protocol**: Understanding of SNMP Manager-Agent architecture
- **Industrial IoT**: Real-world industrial monitoring concepts
- **Full-Stack Development**: Backend API + Frontend dashboard integration
- **Real-Time Data**: Live data polling and visualization
- **Modern Web Technologies**: React, Chart.js, Flask, Python
- **System Simulation**: Realistic data generation and patterns

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional engine parameters
- More chart types and visualizations
- Alert notifications system
- Historical data storage
- Multi-site monitoring
- SNMP trap handling
- Mobile app development

## 📝 License

This project is created for educational and demonstration purposes.

## 🎉 Getting Started

1. **Clone or download** the project
2. **Follow the Quick Start** instructions above
3. **Open the dashboard** at http://127.0.0.1:3000
4. **Monitor your engines** in real-time!

---

**🏭 Start monitoring your industrial engines with SNMP!**
