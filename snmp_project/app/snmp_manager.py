import time
import platform
import psutil

try:
    from pysnmp.hlapi import *
    PYSNMP_AVAILABLE = True
except ImportError:
    PYSNMP_AVAILABLE = False

def get_real_system_data():
    """Get real system information for SNMP simulation"""
    try:
        # System description
        sys_descr = f"Real System SNMP Agent v1.0 ({platform.system()} {platform.release()})"
        
        # System uptime (simulate with process uptime)
        uptime_seconds = int(time.time() - time.mktime(time.gmtime(0)))
        sys_uptime = str(uptime_seconds * 100)  # Convert to centiseconds
        
        # System name
        sys_name = platform.node()
        
        # System location
        sys_location = "Real System - Python SNMP Simulation"
        
        # System contact
        sys_contact = "admin@real-system.local"
        
        # Number of interfaces
        interfaces = len(psutil.net_if_addrs())
        
        # Memory info
        memory = psutil.virtual_memory()
        memory_total = str(memory.total)
        memory_used = str(memory.used)
        
        # CPU info
        cpu_count = str(psutil.cpu_count())
        cpu_percent = str(psutil.cpu_percent(interval=0.1))
        
        # Get additional system information
        boot_time = psutil.boot_time()
        current_time = time.time()
        boot_uptime = int(current_time - boot_time)
        
        # Disk information
        disk_usage = psutil.disk_usage('/')
        disk_total = str(disk_usage.total)
        disk_used = str(disk_usage.used)
        disk_free = str(disk_usage.free)
        
        # Network interfaces details
        net_io = psutil.net_io_counters()
        net_bytes_sent = str(net_io.bytes_sent)
        net_bytes_recv = str(net_io.bytes_recv)
        net_packets_sent = str(net_io.packets_sent)
        net_packets_recv = str(net_io.packets_recv)
        
        # Process information
        process_count = str(len(psutil.pids()))
        
        # Temperature (if available)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                cpu_temp = str(list(temps.values())[0][0].current) if list(temps.values())[0] else "N/A"
            else:
                cpu_temp = "N/A"
        except:
            cpu_temp = "N/A"
        
        # Load averages
        load_avg = psutil.getloadavg()
        load_1min = str(load_avg[0])
        load_5min = str(load_avg[1])
        load_15min = str(load_avg[2])
        
        return {
            # System Information (RFC 1213)
            '1.3.6.1.2.1.1.1.0': sys_descr,
            '1.3.6.1.2.1.1.2.0': '1.3.6.1.4.1.8072.3.2.10',  # sysObjectID
            '1.3.6.1.2.1.1.3.0': str(boot_uptime * 100),  # sysUpTime in centiseconds
            '1.3.6.1.2.1.1.4.0': sys_contact,
            '1.3.6.1.2.1.1.5.0': sys_name,
            '1.3.6.1.2.1.1.6.0': sys_location,
            '1.3.6.1.2.1.1.7.0': '3',  # sysServices
            
            # Interface Information
            '1.3.6.1.2.1.2.1.0': str(interfaces),  # ifNumber
            '1.3.6.1.2.1.2.2.1.1.1': '1',  # ifIndex
            '1.3.6.1.2.1.2.2.1.2.1': 'lo0',  # ifDescr
            '1.3.6.1.2.1.2.2.1.3.1': '24',  # ifType (softwareLoopback)
            '1.3.6.1.2.1.2.2.1.5.1': '65536',  # ifSpeed
            '1.3.6.1.2.1.2.2.1.8.1': '1',  # ifOperStatus (up)
            '1.3.6.1.2.1.2.2.1.10.1': '0',  # ifInOctets
            '1.3.6.1.2.1.2.2.1.16.1': '0',  # ifOutOctets
            
            # Host Resources (RFC 2790)
            '1.3.6.1.2.1.25.1.1.0': str(boot_uptime),  # hrSystemUptime
            '1.3.6.1.2.1.25.1.2.0': str(int(current_time)),  # hrSystemDate
            '1.3.6.1.2.1.25.1.3.0': '1',  # hrSystemInitialLoadDevice
            '1.3.6.1.2.1.25.1.4.0': '1',  # hrSystemInitialLoadParameters
            '1.3.6.1.2.1.25.1.5.0': '1',  # hrSystemNumUsers
            '1.3.6.1.2.1.25.1.6.0': process_count,  # hrSystemProcesses
            '1.3.6.1.2.1.25.1.7.0': '1',  # hrSystemMaxProcesses
            
            # Memory Information
            '1.3.6.1.2.1.25.2.1.1': '1',  # hrMemorySize
            '1.3.6.1.2.1.25.2.2.0': memory_total,  # hrMemorySize
            '1.3.6.1.2.1.25.2.3.1.1.1': '1',  # hrStorageIndex
            '1.3.6.1.2.1.25.2.3.1.2.1': '4',  # hrStorageType (ram)
            '1.3.6.1.2.1.25.2.3.1.3.1': 'Physical Memory',  # hrStorageDescr
            '1.3.6.1.2.1.25.2.3.1.4.1': '1024',  # hrStorageAllocationUnits
            '1.3.6.1.2.1.25.2.3.1.5.1': memory_used,  # hrStorageSize
            '1.3.6.1.2.1.25.2.3.1.6.1': str(int(memory_used) - int(memory_used) * 0.2),  # hrStorageUsed
            
            # CPU Information
            '1.3.6.1.2.1.25.3.2.1.1.1': '1',  # hrDeviceIndex
            '1.3.6.1.2.1.25.3.2.1.2.1': '3',  # hrDeviceType (processor)
            '1.3.6.1.2.1.25.3.2.1.3.1': 'CPU',  # hrDeviceDescr
            '1.3.6.1.2.1.25.3.2.1.4.1': '1',  # hrDeviceStatus
            '1.3.6.1.2.1.25.3.2.1.5.1': cpu_count,  # hrProcessorFrwID
            '1.3.6.1.2.1.25.3.3.1.1.1': '1',  # hrProcessorFrwID
            '1.3.6.1.2.1.25.3.3.1.2.1': cpu_percent,  # hrProcessorLoad
            
            # Disk Information
            '1.3.6.1.2.1.25.2.3.1.1.2': '2',  # hrStorageIndex
            '1.3.6.1.2.1.25.2.3.1.2.2': '4',  # hrStorageType (fixed disk)
            '1.3.6.1.2.1.25.2.3.1.3.2': 'Fixed Disk',  # hrStorageDescr
            '1.3.6.1.2.1.25.2.3.1.4.2': '1024',  # hrStorageAllocationUnits
            '1.3.6.1.2.1.25.2.3.1.5.2': disk_total,  # hrStorageSize
            '1.3.6.1.2.1.25.2.3.1.6.2': disk_used,  # hrStorageUsed
            
            # Network Statistics
            '1.3.6.1.2.1.2.2.1.10.2': net_bytes_recv,  # ifInOctets
            '1.3.6.1.2.1.2.2.1.11.2': net_packets_recv,  # ifInUcastPkts
            '1.3.6.1.2.1.2.2.1.16.2': net_bytes_sent,  # ifOutOctets
            '1.3.6.1.2.1.2.2.1.17.2': net_packets_sent,  # ifOutUcastPkts
            
            # Load Averages
            '1.3.6.1.4.1.2021.10.1.1.1': load_1min,  # laLoad.1
            '1.3.6.1.4.1.2021.10.1.1.2': load_5min,  # laLoad.2
            '1.3.6.1.4.1.2021.10.1.1.3': load_15min,  # laLoad.3
            
            # CPU Usage
            '1.3.6.1.4.1.2021.11.9.0': cpu_percent,  # ssCpuUser
            '1.3.6.1.4.1.2021.11.10.0': '0',  # ssCpuSystem
            '1.3.6.1.4.1.2021.11.11.0': '0',  # ssCpuIdle
            
            # Memory Usage
            '1.3.6.1.4.1.2021.4.3.0': memory_total,  # memTotalReal
            '1.3.6.1.4.1.2021.4.4.0': memory_used,  # memAvailReal
            '1.3.6.1.4.1.2021.4.5.0': str(int(memory_total) - int(memory_used)),  # memTotalFree
            
            # Disk Usage
            '1.3.6.1.4.1.2021.9.1.6.1': disk_total,  # dskTotal
            '1.3.6.1.4.1.2021.9.1.7.1': disk_used,  # dskUsed
            '1.3.6.1.4.1.2021.9.1.8.1': disk_free,  # dskAvail
            
            # Process Information
            '1.3.6.1.4.1.2021.2.1.1.0': process_count,  # prCount
            '1.3.6.1.4.1.2021.2.1.2.0': '1',  # prErrorFlag
            '1.3.6.1.4.1.2021.2.1.3.0': '0',  # prErrMessage
            '1.3.6.1.4.1.2021.2.1.4.0': '0',  # prErrFix
            '1.3.6.1.4.1.2021.2.1.5.0': '0',  # prErrFixCmd
            
            # Temperature (if available)
            '1.3.6.1.4.1.2021.13.16.2.1.1.1': cpu_temp,  # tempValue
            '1.3.6.1.4.1.2021.13.16.2.1.2.1': '1',  # tempScale (celsius)
        }
    except Exception as e:
        print(f"Error getting real system data: {e}")
        return {}

def get_snmp_data(oid, host='127.0.0.1', community='public', port=1161):
    # Get real system data
    real_data = get_real_system_data()
    
    # First try to get real SNMP data if pysnmp is available
    if PYSNMP_AVAILABLE:
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((host, port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                # If no real agent, return real system data
                return real_data.get(oid, f"Real system data for OID {oid}")
            elif errorStatus:
                # If error, return real system data
                return real_data.get(oid, f"Real system data for OID {oid}")
            else:
                for varBind in varBinds:
                    return f"{varBind.prettyPrint()}"
        except:
            # If any exception, return real system data
            return real_data.get(oid, f"Real system data for OID {oid}")
    else:
        # If pysnmp not available, return real system data
        return real_data.get(oid, f"Real system data for OID {oid}")
