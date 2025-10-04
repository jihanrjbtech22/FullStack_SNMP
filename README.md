# FullStack SNMP Management System

## 🎯 Project Overview
A comprehensive SNMP (Simple Network Management Protocol) management system built with modern web technologies. This project demonstrates real-time system monitoring through a Flask-based web dashboard that simulates SNMP agent behavior using real system data.

## 🏗️ Architecture

### Components
- **Web Dashboard**: React-based frontend for real-time monitoring
- **SNMP Manager**: Python Flask backend with SNMP simulation
- **Data Collection**: Real-time system metrics using `psutil` and `platform`
- **API Layer**: RESTful endpoints for system data

### Technology Stack
- **Backend**: Python 3.8+, Flask, pysnmp, psutil
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Format**: JSON APIs
- **System Integration**: Cross-platform system monitoring

## 📁 Project Structure
```
FullStack_SNMP/
├── snmp_project/                 # Main SNMP Management System
│   ├── app/
│   │   ├── __init__.py          # Flask application factory
│   │   ├── snmp_manager.py      # SNMP simulation & data collection
│   │   ├── routes.py            # API endpoints
│   │   └── templates/
│   │       └── index.html       # Web dashboard
│   ├── venv/                    # Python virtual environment
│   ├── requirements.txt         # Python dependencies
│   ├── run.py                   # Application entry point
│   └── README.md                # Detailed project documentation
└── README.md                    # This overview file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation
1. **Clone or navigate to the project:**
   ```bash
   cd FullStack_SNMP/snmp_project
   ```

2. **Set up Python environment:**
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
   Open your browser and go to: **http://127.0.0.1:5002**

## ✨ Key Features

### 🖥️ Real-Time System Monitoring
- **System Information**: Hostname, description, location, uptime
- **Resource Monitoring**: CPU usage, memory consumption, disk space
- **Network Statistics**: Interface count, traffic metrics
- **Process Management**: Running processes and system load
- **Performance Metrics**: Load averages and system health

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-Time Updates**: Auto-refresh every 5 seconds
- **Status Indicators**: Color-coded alerts for system health
- **Data Visualization**: Clean, organized display of metrics
- **User-Friendly**: Intuitive interface with clear information hierarchy

### 🔧 Technical Capabilities
- **SNMP Simulation**: Mimics real SNMP agent behavior
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **RESTful API**: JSON endpoints for system data
- **Modular Design**: Easy to extend and customize
- **Error Handling**: Graceful fallbacks and error management

## 📊 Monitoring Capabilities

### System Metrics
- **CPU**: Usage percentage, core count, temperature
- **Memory**: Total, used, free with percentage indicators
- **Disk**: Space usage with critical alerts
- **Network**: Interface statistics and traffic data
- **Processes**: Count and system process information
- **Load**: 1-minute, 5-minute, 15-minute averages

### Status Alerts
- 🟢 **Normal**: System operating within normal parameters
- 🟡 **Warning**: Resource usage above 70% (memory) or 80% (disk)
- 🔴 **Critical**: Resource usage above 90% (memory) or 90% (disk)

## 🛠️ Configuration

### Port Settings
- **Default Port**: 5002
- **Configurable**: Modify `run.py` to change port
- **Auto-Detection**: Automatically finds available ports

### Data Collection
- **Real-Time**: Live system data collection
- **Efficient**: Minimal resource usage
- **Accurate**: Direct system API calls
- **Reliable**: Fallback mechanisms for data collection

## 🔍 API Documentation

### Endpoints
- `GET /` - Main dashboard interface
- `GET /api/system` - Complete system data in JSON format

### Response Format
```json
{
  "sysDescr": "System description",
  "sysUpTime": "Uptime in centiseconds",
  "sysName": "Hostname",
  "memoryTotal": "Total memory in bytes",
  "memoryUsed": "Used memory in bytes",
  "cpuUsage": "CPU usage percentage",
  "diskTotal": "Total disk space",
  "load1min": "1-minute load average"
}
```

## 🐛 Troubleshooting

### Common Issues
1. **Port Conflicts**: Use `lsof -i :5002` to check port usage
2. **Dependencies**: Ensure all packages are installed with `pip install -r requirements.txt`
3. **Permissions**: Some system metrics may require appropriate permissions
4. **Browser Compatibility**: Use modern browsers for best experience

### Debug Mode
The application runs in debug mode by default, providing:
- Detailed error messages
- Auto-reload on code changes
- Debug console access

## 📈 Performance
- **Memory Usage**: ~50-100MB
- **CPU Impact**: Minimal (data collection only)
- **Response Time**: <100ms for API calls
- **Refresh Rate**: 5 seconds (configurable)

## 🔮 Future Roadmap
- **Historical Data**: Data logging and trend analysis
- **Multi-Device**: Monitor multiple systems simultaneously
- **Alert System**: Email/SMS notifications for critical events
- **SNMP Traps**: Real SNMP trap handling
- **Custom OIDs**: Support for custom SNMP object identifiers
- **Export Features**: Data export in various formats
- **Authentication**: User management and access control

## 📚 Educational Value
This project demonstrates:
- **SNMP Protocol**: Understanding of SNMP concepts and OIDs
- **Web Development**: Modern web application architecture
- **System Programming**: Cross-platform system monitoring
- **API Design**: RESTful API development
- **Real-Time Data**: Live data collection and display
- **User Interface**: Responsive web design principles

## 🤝 Contributing
Contributions are welcome! Areas for improvement:
- Additional system metrics
- Enhanced UI/UX features
- Performance optimizations
- Documentation improvements
- Test coverage expansion

## 📝 License
This project is created for educational and demonstration purposes.

---

**🎉 Start monitoring your system with real-time SNMP data!**

For detailed setup instructions and technical documentation, see the [snmp_project README](snmp_project/README.md).