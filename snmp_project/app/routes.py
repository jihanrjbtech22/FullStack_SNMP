from flask import Blueprint, render_template, jsonify
from .snmp_manager import get_snmp_data

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/system')
def system_info():
    data = {
        # Basic System Information
        "sysDescr": get_snmp_data('1.3.6.1.2.1.1.1.0'),
        "sysUpTime": get_snmp_data('1.3.6.1.2.1.1.3.0'),
        "sysName": get_snmp_data('1.3.6.1.2.1.1.5.0'),
        "sysLocation": get_snmp_data('1.3.6.1.2.1.1.6.0'),
        "sysContact": get_snmp_data('1.3.6.1.2.1.1.4.0'),
        
        # Memory Information
        "memoryTotal": get_snmp_data('1.3.6.1.4.1.2021.4.3.0'),
        "memoryUsed": get_snmp_data('1.3.6.1.4.1.2021.4.4.0'),
        "memoryFree": get_snmp_data('1.3.6.1.4.1.2021.4.5.0'),
        
        # CPU Information
        "cpuCount": get_snmp_data('1.3.6.1.2.1.25.3.2.1.5.1'),
        "cpuUsage": get_snmp_data('1.3.6.1.4.1.2021.11.9.0'),
        "cpuIdle": get_snmp_data('1.3.6.1.4.1.2021.11.11.0'),
        
        # Load Averages
        "load1min": get_snmp_data('1.3.6.1.4.1.2021.10.1.1.1'),
        "load5min": get_snmp_data('1.3.6.1.4.1.2021.10.1.1.2'),
        "load15min": get_snmp_data('1.3.6.1.4.1.2021.10.1.1.3'),
        
        # Disk Information
        "diskTotal": get_snmp_data('1.3.6.1.4.1.2021.9.1.6.1'),
        "diskUsed": get_snmp_data('1.3.6.1.4.1.2021.9.1.7.1'),
        "diskFree": get_snmp_data('1.3.6.1.4.1.2021.9.1.8.1'),
        
        # Network Information
        "networkInterfaces": get_snmp_data('1.3.6.1.2.1.2.1.0'),
        "bytesReceived": get_snmp_data('1.3.6.1.2.1.2.2.1.10.2'),
        "bytesSent": get_snmp_data('1.3.6.1.2.1.2.2.1.16.2'),
        "packetsReceived": get_snmp_data('1.3.6.1.2.1.2.2.1.11.2'),
        "packetsSent": get_snmp_data('1.3.6.1.2.1.2.2.1.17.2'),
        
        # Process Information
        "processCount": get_snmp_data('1.3.6.1.4.1.2021.2.1.1.0'),
        "systemProcesses": get_snmp_data('1.3.6.1.2.1.25.1.6.0'),
        
        # Temperature (if available)
        "cpuTemperature": get_snmp_data('1.3.6.1.4.1.2021.13.16.2.1.1.1'),
    }
    return jsonify(data)
