#!/usr/bin/env python3
"""
Python SNMP Agent - Real SNMP implementation
This agent responds to actual SNMP GET requests using pysnmp
"""

import time
import threading
import psutil
import platform
from datetime import datetime, timedelta

try:
    from pysnmp.entity import engine, config
    from pysnmp.entity.rfc3413 import cmdrsp, context
    from pysnmp.carrier.udp import udp
    from pysnmp.smi import builder, view, rfc1902
    from pysnmp import debug
    PYSNMP_AVAILABLE = True
except ImportError:
    PYSNMP_AVAILABLE = False
    print("⚠️  pysnmp not available. Install with: pip install pysnmp")

class PythonSNMPAgent:
    def __init__(self, community='public', port=1161):
        self.community = community
        self.port = port
        self.running = False
        self.start_time = time.time()
        
    def get_system_info(self):
        """Get real system information"""
        try:
            # System description
            sys_descr = f"Python SNMP Agent v1.0 ({platform.system()} {platform.release()})"
            
            # System uptime in centiseconds
            uptime_seconds = int(time.time() - self.start_time)
            sys_uptime = str(uptime_seconds * 100)  # Convert to centiseconds
            
            # System name
            sys_name = platform.node()
            
            # System location
            sys_location = "Python SNMP Agent - Test Environment"
            
            # System contact
            sys_contact = "admin@python-snmp-agent.local"
            
            # Number of interfaces
            interfaces = len(psutil.net_if_addrs())
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_total = str(memory.total)
            memory_used = str(memory.used)
            
            # CPU info
            cpu_count = str(psutil.cpu_count())
            cpu_percent = str(psutil.cpu_percent(interval=1))
            
            return {
                '1.3.6.1.2.1.1.1.0': sys_descr,
                '1.3.6.1.2.1.1.3.0': sys_uptime,
                '1.3.6.1.2.1.1.5.0': sys_name,
                '1.3.6.1.2.1.1.6.0': sys_location,
                '1.3.6.1.2.1.1.4.0': sys_contact,
                '1.3.6.1.2.1.2.1.0': str(interfaces),
                '1.3.6.1.2.1.25.2.2.0': memory_total,
                '1.3.6.1.2.1.25.2.3.1.5.1': memory_used,
                '1.3.6.1.2.1.25.3.2.1.5.1': cpu_count,
                '1.3.6.1.4.1.2021.11.11.0': cpu_percent,
            }
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}
    
    def start(self):
        """Start the SNMP agent"""
        if not PYSNMP_AVAILABLE:
            print("❌ Cannot start SNMP agent: pysnmp not available")
            return
            
        print(f"🚀 Starting Python SNMP Agent...")
        print(f"   Community: {self.community}")
        print(f"   Port: {self.port}")
        print(f"   System Info Available:")
        
        system_info = self.get_system_info()
        for oid, value in system_info.items():
            print(f"     {oid}: {value}")
        
        print(f"   Agent running on UDP port {self.port}")
        print(f"   Press Ctrl+C to stop")
        
        # Create SNMP engine
        snmpEngine = engine.SnmpEngine()
        
        # Transport setup
        config.addTransport(
            snmpEngine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', self.port))
        )
        
        # SNMPv2c setup
        config.addV1System(snmpEngine, 'my-area', self.community)
        
        # MIB builder
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        mibBuilder.loadModules('SNMPv2-MIB')
        
        # Context
        snmpContext = context.SnmpContext(snmpEngine)
        
        # Command responder
        cmdrsp.GetCommandResponder(snmpEngine, snmpContext, self._cbFun)
        
        self.running = True
        
        try:
            snmpEngine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt:
            print(f"\n🛑 Stopping Python SNMP Agent...")
            self.running = False
            snmpEngine.transportDispatcher.closeDispatcher()
    
    def _cbFun(self, snmpEngine, stateReference, varName, varBind, cbCtx):
        """Callback function to handle SNMP requests"""
        oid, val = varBind[0]
        oid_str = '.'.join([str(x) for x in oid])
        
        print(f"📡 SNMP Request: {oid_str}")
        
        # Get current system info
        system_info = self.get_system_info()
        
        # Check if we have data for this OID
        if oid_str in system_info:
            value = system_info[oid_str]
            print(f"   ✅ Response: {value}")
            return varBind[0].__class__(oid, rfc1902.OctetString(value))
        else:
            print(f"   ❌ OID not found: {oid_str}")
            return varBind[0].__class__(oid, rfc1902.noSuchObject)

if __name__ == '__main__':
    agent = PythonSNMPAgent(community='public', port=1161)
    agent.start()
