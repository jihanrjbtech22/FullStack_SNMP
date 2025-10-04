# SNMP Management System with Real-Time Dashboard

## 🎯 Overview
A comprehensive SNMP management system that provides real-time system monitoring through a modern web dashboard. The system simulates SNMP agent behavior by collecting real system data and presenting it through a Flask-based web interface.

## ✨ Features

### 🖥️ System Monitoring
- **System Information**: Description, name, location, contact, uptime
- **Memory Management**: Total, used, free memory with status alerts
- **CPU Monitoring**: Core count, usage percentage, temperature
- **Load Averages**: 1-minute, 5-minute, 15-minute system load
- **Disk Usage**: Total, used, free disk space with critical alerts
- **Network Statistics**: Interface count, bytes/packets sent/received
- **Process Information**: Running processes count and system processes

### 🎨 User Interface
- **Responsive Design**: Modern, mobile-friendly dashboard
- **Real-time Updates**: Auto-refresh every 5 seconds
- **Status Indicators**: Color-coded alerts for memory and disk usage
- **Data Formatting**: Human-readable bytes, uptime, and percentages
- **Visual Cards**: Organized sections for different system metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS/Linux/Windows

### Installation & Setup

1. **Navigate to project directory:**
```bash
cd FullStack_SNMP/snmp_project
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python3 run.py
```

5. **Access the dashboard:**
Open your browser and visit: **http://127.0.0.1:5002**

## 📁 Project Structure
```
snmp_project/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── snmp_manager.py          # SNMP simulation & system data collection
│   ├── routes.py                # Flask API routes
│   └── templates/
│       └── index.html           # Web dashboard template
├── venv/                        # Virtual environment
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🔧 Technical Details

### SNMP Simulation
The system uses `psutil` and `platform` libraries to collect real system data and presents it as SNMP OID responses. This approach eliminates the need for a separate SNMP agent while providing authentic system monitoring.

### Supported OIDs
- **System Information (RFC 1213)**:
  - `1.3.6.1.2.1.1.1.0` - System Description
  - `1.3.6.1.2.1.1.3.0` - System Uptime
  - `1.3.6.1.2.1.1.5.0` - System Name
  - `1.3.6.1.2.1.1.6.0` - System Location
  - `1.3.6.1.2.1.1.4.0` - System Contact

- **Host Resources (RFC 2790)**:
  - `1.3.6.1.2.1.25.1.6.0` - System Processes
  - `1.3.6.1.2.1.25.2.2.0` - Memory Size
  - `1.3.6.1.2.1.25.3.2.1.5.1` - CPU Count

- **UCD-SNMP-MIB**:
  - `1.3.6.1.4.1.2021.4.3.0` - Memory Total
  - `1.3.6.1.4.1.2021.11.9.0` - CPU Usage
  - `1.3.6.1.4.1.2021.9.1.6.1` - Disk Total

### API Endpoints
- `GET /` - Main dashboard interface
- `GET /api/system` - JSON API for system data

## 🎨 Dashboard Sections

### 🖥️ System Information
- System description and hostname
- Physical location and contact information
- System uptime in human-readable format

### 🧠 Memory Information
- Total, used, and free memory
- Memory usage percentage with status indicators
- Color-coded alerts (Normal/Warning/Critical)

### ⚡ CPU Information
- Number of CPU cores
- Current CPU usage percentage
- CPU idle percentage
- Temperature (if available)

### 📊 Load Averages
- 1-minute, 5-minute, and 15-minute load averages
- System performance indicators

### 💾 Disk Information
- Total, used, and free disk space
- Disk usage percentage with status alerts
- Color-coded warnings for high usage

### 🌐 Network Information
- Number of network interfaces
- Bytes and packets sent/received
- Network traffic statistics

### ⚙️ Process Information
- Total number of running processes
- System process count

## 🛠️ Configuration

### Port Configuration
The application runs on port 5002 by default. To change the port, modify `run.py`:
```python
app.run(debug=True, port=YOUR_PORT)
```

### Data Collection
System data is collected in real-time using:
- `psutil` for system metrics (CPU, memory, disk, network, processes)
- `platform` for system information (OS, hostname, architecture)

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check what's using the port
   lsof -i :5002
   # Kill the process or use a different port
   ```

2. **Template Not Found**:
   - Ensure you're in the correct directory
   - Check that `app/templates/index.html` exists

3. **Dependencies Missing**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Permission Issues**:
   - Ensure you have read access to system files
   - On Linux, some metrics might require additional permissions

### Status Indicators
- 🟢 **Normal**: System operating within normal parameters
- 🟡 **Warning**: Resource usage above 70% (memory) or 80% (disk)
- 🔴 **Critical**: Resource usage above 90% (memory) or 90% (disk)

## 📊 Performance
- **Refresh Rate**: 5 seconds
- **Memory Usage**: ~50-100MB
- **CPU Usage**: Minimal (data collection only)
- **Response Time**: <100ms for API calls

## 🔮 Future Enhancements
- Historical data logging
- Alert notifications
- Multiple device monitoring
- SNMP trap handling
- Custom OID support
- Export functionality

## 📝 License
This project is for educational and demonstration purposes.

## 🤝 Contributing
Feel free to submit issues and enhancement requests!

---

**🎉 Enjoy monitoring your system with real-time SNMP data!**