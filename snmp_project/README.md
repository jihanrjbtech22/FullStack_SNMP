# SNMP Mini Implementation with Flask and Web Dashboard

## 🎯 Objective
Build a minimal SNMP setup to show how a Manager queries an Agent and displays real-time device information through a web interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- An SNMP agent running on localhost:161 (or configure a different host)

### Setup and Run

1. **Create virtual environment:**
```bash
cd snmp_project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python run.py
```

4. **Open your browser:**
Visit http://127.0.0.1:5000

## 📁 Project Structure
```
snmp_project/
├── app/
│   ├── __init__.py
│   ├── snmp_manager.py    # SNMP query functions
│   ├── routes.py          # Flask routes
│   └── templates/
│       └── index.html     # Web dashboard
├── venv/                  # Virtual environment (auto-created)
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
└── README.md
```

## 🔧 Features
- Real-time SNMP data display
- System information queries (Description, Uptime, Name)
- Auto-refresh every 5 seconds
- Clean, responsive web interface

## 📡 SNMP OIDs Used
- `1.3.6.1.2.1.1.1.0` - System Description
- `1.3.6.1.2.1.1.3.0` - System Uptime
- `1.3.6.1.2.1.1.5.0` - System Name

## 🛠️ Configuration
To query a different SNMP agent, modify the `host` parameter in `app/snmp_manager.py`:
```python
def get_snmp_data(oid, host='YOUR_AGENT_IP', community='public'):
```

## 🐛 Troubleshooting
- **No SNMP agent running**: The dashboard will show connection errors
- **Port 161 blocked**: Ensure SNMP agent is accessible on UDP port 161
- **Community string**: Default is 'public', change if your agent uses different credentials
