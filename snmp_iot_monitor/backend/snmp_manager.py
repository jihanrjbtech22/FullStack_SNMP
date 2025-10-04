#!/usr/bin/env python3
"""
SNMP Manager for Industrial IoT Engine Monitoring
Queries multiple SNMP agents (engines) and collects sensor data.
Handles communication with simulated engine agents and provides data to the web API.
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
import json

try:
    from pysnmp.hlapi import *
    PYSNMP_AVAILABLE = True
except ImportError:
    PYSNMP_AVAILABLE = False
    print("⚠️  pysnmp not available. Install with: pip install pysnmp")

class EngineData:
    """Data structure for engine sensor readings"""
    def __init__(self, engine_id: str, port: int):
        self.engine_id = engine_id
        self.port = port
        self.temperature = 0.0
        self.rpm = 0
        self.current = 0.0
        self.power = 0
        self.status = 0
        self.uptime = 0
        self.last_updated = None
        self.health_status = "unknown"
    
    def update_health_status(self):
        """Update health status based on temperature thresholds"""
        if self.temperature > 100:
            self.health_status = "critical"
        elif self.temperature > 80:
            self.health_status = "warning"
        else:
            self.health_status = "normal"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'engine_id': self.engine_id,
            'port': self.port,
            'temperature': self.temperature,
            'rpm': self.rpm,
            'current': self.current,
            'power': self.power,
            'status': self.status,
            'uptime': self.uptime,
            'last_updated': self.last_updated,
            'health_status': self.health_status
        }

class SNMPManager:
    """
    SNMP Manager that queries multiple engine agents and maintains data cache.
    Simulates real SNMP manager behavior for industrial IoT monitoring.
    """
    
    def __init__(self):
        self.engines = {
            'Engine-1': EngineData('Engine-1', 1611),
            'Engine-2': EngineData('Engine-2', 1612),
            'Engine-3': EngineData('Engine-3', 1613)
        }
        
        # SNMP OID mappings for engine parameters
        self.oids = {
            'temperature': '1.3.6.1.4.1.9999.1.1.1.0',
            'rpm': '1.3.6.1.4.1.9999.1.1.2.0',
            'current': '1.3.6.1.4.1.9999.1.1.3.0',
            'power': '1.3.6.1.4.1.9999.1.1.4.0',
            'status': '1.3.6.1.4.1.9999.1.1.5.0',
            'uptime': '1.3.6.1.4.1.9999.1.1.6.0'
        }
        
        self.community = 'public'
        self.host = '127.0.0.1'
        self.running = False
        self.poll_interval = 2  # Poll every 2 seconds
        
    def query_snmp_agent(self, oid: str, port: int) -> Optional[str]:
        """
        Query a specific SNMP agent for a given OID.
        In simulation mode, generates realistic data instead of actual SNMP queries.
        """
        if not PYSNMP_AVAILABLE:
            # Fallback to simulation data when pysnmp is not available
            return self._generate_simulation_data(oid, port)
        
        try:
            # Attempt real SNMP query
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                # If SNMP fails, fall back to simulation
                return self._generate_simulation_data(oid, port)
            elif errorStatus:
                return self._generate_simulation_data(oid, port)
            else:
                for varBind in varBinds:
                    return str(varBind.prettyPrint())
        except Exception:
            # If any exception, fall back to simulation
            return self._generate_simulation_data(oid, port)
    
    def _generate_simulation_data(self, oid: str, port: int) -> str:
        """
        Generate realistic simulation data for engine parameters.
        This simulates what would come from real SNMP agents.
        """
        import math
        import random
        
        # Get engine-specific base values
        engine_id = f"Engine-{port - 1610}"  # Port 1611 -> Engine-1, etc.
        base_values = {
            'Engine-1': {'temp': 42, 'rpm': 1750, 'current': 11.8, 'power': 1450},
            'Engine-2': {'temp': 48, 'rpm': 1850, 'current': 13.2, 'power': 1620},
            'Engine-3': {'temp': 45, 'rpm': 1800, 'current': 12.5, 'power': 1500}
        }
        
        base = base_values.get(engine_id, base_values['Engine-3'])
        current_time = time.time()
        
        # Generate time-based variations
        time_factor = math.sin(current_time * 0.1)
        cycle_factor = math.sin(current_time * 0.05)
        random_factor = random.uniform(-0.1, 0.1)
        
        if 'temperature' in oid:
            temp = base['temp'] + (time_factor * 3) + (cycle_factor * 5) + (random_factor * 2)
            return str(round(max(20, min(120, temp)), 1))
        
        elif 'rpm' in oid:
            rpm = base['rpm'] + (time_factor * 50) + (cycle_factor * 30) + (random_factor * 20)
            return str(int(max(500, min(3000, rpm))))
        
        elif 'current' in oid:
            current = base['current'] + (time_factor * 1.5) + (cycle_factor * 1.0) + (random_factor * 0.5)
            return str(round(max(0, min(30, current)), 2))
        
        elif 'power' in oid:
            power = base['power'] + (time_factor * 200) + (cycle_factor * 150) + (random_factor * 100)
            return str(int(max(0, min(2500, power))))
        
        elif 'status' in oid:
            return "1"  # Always running in simulation
        
        elif 'uptime' in oid:
            return str(int(current_time % 86400))  # Simulate uptime in seconds
        
        return "0"
    
    def update_engine_data(self, engine_id: str):
        """Update data for a specific engine by querying all OIDs"""
        engine = self.engines[engine_id]
        
        try:
            # Query all parameters for this engine
            for param, oid in self.oids.items():
                value = self.query_snmp_agent(oid, engine.port)
                if value:
                    if param == 'temperature':
                        engine.temperature = float(value)
                    elif param == 'rpm':
                        engine.rpm = int(value)
                    elif param == 'current':
                        engine.current = float(value)
                    elif param == 'power':
                        engine.power = int(value)
                    elif param == 'status':
                        engine.status = int(value)
                    elif param == 'uptime':
                        engine.uptime = int(value)
            
            # Update health status and timestamp
            engine.update_health_status()
            engine.last_updated = datetime.now().isoformat()
            
        except Exception as e:
            print(f"❌ Error updating {engine_id}: {e}")
    
    def poll_all_engines(self):
        """Poll all engines for updated data"""
        for engine_id in self.engines:
            self.update_engine_data(engine_id)
    
    def start_polling(self):
        """Start the SNMP polling loop in a separate thread"""
        self.running = True
        print("🔄 Starting SNMP polling for all engines...")
        
        def polling_loop():
            while self.running:
                try:
                    self.poll_all_engines()
                    time.sleep(self.poll_interval)
                except Exception as e:
                    print(f"❌ Polling error: {e}")
                    time.sleep(5)  # Wait longer on error
        
        thread = threading.Thread(target=polling_loop, daemon=True)
        thread.start()
        return thread
    
    def stop_polling(self):
        """Stop the SNMP polling"""
        self.running = False
        print("🛑 Stopped SNMP polling")
    
    def get_all_engines_data(self) -> Dict:
        """Get current data for all engines"""
        return {
            engine_id: engine.to_dict() 
            for engine_id, engine in self.engines.items()
        }
    
    def get_engine_data(self, engine_id: str) -> Optional[Dict]:
        """Get current data for a specific engine"""
        if engine_id in self.engines:
            return self.engines[engine_id].to_dict()
        return None
    
    def get_engines_summary(self) -> Dict:
        """Get summary statistics for all engines"""
        total_engines = len(self.engines)
        running_engines = sum(1 for engine in self.engines.values() if engine.status == 1)
        avg_temperature = sum(engine.temperature for engine in self.engines.values()) / total_engines
        avg_power = sum(engine.power for engine in self.engines.values()) / total_engines
        
        health_counts = {}
        for engine in self.engines.values():
            status = engine.health_status
            health_counts[status] = health_counts.get(status, 0) + 1
        
        return {
            'total_engines': total_engines,
            'running_engines': running_engines,
            'avg_temperature': round(avg_temperature, 1),
            'avg_power': round(avg_power, 0),
            'health_distribution': health_counts,
            'last_updated': datetime.now().isoformat()
        }

# Global SNMP manager instance
snmp_manager = SNMPManager()

def get_snmp_manager() -> SNMPManager:
    """Get the global SNMP manager instance"""
    return snmp_manager
