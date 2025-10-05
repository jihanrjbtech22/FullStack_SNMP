#!/usr/bin/env python3
"""
Enhanced SNMP Agent Simulator with Explicit Message Logging
Shows actual SNMP protocol messages, MIB values, and OID mappings.
"""

import time
import math
import random
import threading
import json
from datetime import datetime
from pysnmp.hlapi import *

class EnhancedEngineSNMPAgent:
    """
    Enhanced SNMP agent that logs all SNMP messages and MIB interactions.
    Shows explicit SNMP protocol communication for educational purposes.
    """
    
    def __init__(self, engine_id, port, base_temp=45, base_rpm=1800, base_current=12.5, base_power=1500):
        self.engine_id = engine_id
        self.port = port
        self.running = False
        
        # Base values for realistic simulation
        self.base_temp = base_temp
        self.base_rpm = base_rpm
        self.base_current = base_current
        self.base_power = base_power
        
        # Time-based simulation variables
        self.start_time = time.time()
        self.cycle_time = 0
        
        # SNMP message log
        self.message_log = []
        self.max_log_entries = 100
        
        # Engine-specific MIB definitions
        self.mib_definitions = {
            '1.3.6.1.4.1.9999.1.1.1.0': {
                'name': 'engineTemperature',
                'description': 'Engine Temperature in Celsius',
                'type': 'Gauge32',
                'units': '°C',
                'access': 'read-only',
                'getter': self.get_temperature
            },
            '1.3.6.1.4.1.9999.1.1.2.0': {
                'name': 'engineRPM',
                'description': 'Engine RPM (Revolutions Per Minute)',
                'type': 'Gauge32',
                'units': 'RPM',
                'access': 'read-only',
                'getter': self.get_rpm
            },
            '1.3.6.1.4.1.9999.1.1.3.0': {
                'name': 'engineCurrent',
                'description': 'Engine Electrical Current',
                'type': 'Gauge32',
                'units': 'Amperes',
                'access': 'read-only',
                'getter': self.get_current
            },
            '1.3.6.1.4.1.9999.1.1.4.0': {
                'name': 'enginePowerOutput',
                'description': 'Engine Power Output',
                'type': 'Gauge32',
                'units': 'Watts',
                'access': 'read-only',
                'getter': self.get_power
            },
            '1.3.6.1.4.1.9999.1.1.5.0': {
                'name': 'engineStatus',
                'description': 'Engine Operational Status',
                'type': 'Integer32',
                'units': 'Status',
                'access': 'read-only',
                'getter': self.get_status
            },
            '1.3.6.1.4.1.9999.1.1.6.0': {
                'name': 'engineUptime',
                'description': 'Engine Uptime in seconds',
                'type': 'TimeTicks',
                'units': 'seconds',
                'access': 'read-only',
                'getter': self.get_uptime
            }
        }
        
        # SNMP community string
        self.community = 'public'
        
    def log_snmp_message(self, message_type, oid, value=None, error=None):
        """Log SNMP messages with professional detailed format"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        mib_info = self.mib_definitions.get(oid, {})
        mib_name = mib_info.get('name', 'Unknown')
        units = mib_info.get('units', '')
        
        log_entry = {
            'timestamp': timestamp,
            'engine_id': self.engine_id,
            'message_type': message_type,
            'oid': oid,
            'mib_name': mib_name,
            'value': value,
            'error': error,
            'port': self.port,
            'community': self.community,
            'data_type': mib_info.get('type', 'Unknown'),
            'access': mib_info.get('access', 'Unknown')
        }
        
        self.message_log.append(log_entry)
        
        # Keep only recent entries
        if len(self.message_log) > self.max_log_entries:
            self.message_log.pop(0)
            
        # Professional console logging with detailed format
        if message_type == 'GET_REQUEST':
            print(f"🔍 [{timestamp}] SNMP GET Request")
            print(f"   ├─ Engine: {self.engine_id} (Port {self.port})")
            print(f"   ├─ OID: {oid}")
            print(f"   ├─ MIB Name: {mib_name}")
            print(f"   ├─ Data Type: {mib_info.get('type', 'Unknown')}")
            print(f"   ├─ Access: {mib_info.get('access', 'Unknown')}")
            print(f"   └─ Community: {self.community}")
        elif message_type == 'GET_RESPONSE':
            print(f"📤 [{timestamp}] SNMP GET Response")
            print(f"   ├─ Engine: {self.engine_id} (Port {self.port})")
            print(f"   ├─ OID: {oid}")
            print(f"   ├─ MIB Name: {mib_name}")
            print(f"   ├─ Value: {value} {units}")
            print(f"   ├─ Data Type: {mib_info.get('type', 'Unknown')}")
            print(f"   └─ Response Time: <1ms")
        elif message_type == 'ERROR':
            print(f"❌ [{timestamp}] SNMP Error")
            print(f"   ├─ Engine: {self.engine_id} (Port {self.port})")
            print(f"   ├─ OID: {oid}")
            print(f"   ├─ MIB Name: {mib_name}")
            print(f"   ├─ Error: {error}")
            print(f"   └─ Community: {self.community}")
    
    def get_temperature(self):
        """Generate realistic temperature readings with gradual variations"""
        self.cycle_time = time.time() - self.start_time
        
        # Simulate realistic temperature patterns
        # Base temperature with daily cycle and random variations
        daily_cycle = 5 * math.sin(self.cycle_time / 3600 * 2 * math.pi)  # 5°C daily variation
        random_variation = random.uniform(-2, 2)
        load_factor = 0.3 * math.sin(self.cycle_time / 60)  # Simulate load changes
        
        temperature = self.base_temp + daily_cycle + random_variation + load_factor
        return round(max(20, min(120, temperature)), 1)  # Clamp between 20-120°C
    
    def get_rpm(self):
        """Generate realistic RPM readings"""
        self.cycle_time = time.time() - self.start_time
        
        # Simulate RPM with load variations
        base_rpm = self.base_rpm
        load_variation = 200 * math.sin(self.cycle_time / 30)  # 30-second load cycle
        random_noise = random.uniform(-50, 50)
        
        rpm = base_rpm + load_variation + random_noise
        return int(max(500, min(3500, rpm)))  # Clamp between 500-3500 RPM
    
    def get_current(self):
        """Generate realistic current readings"""
        self.cycle_time = time.time() - self.start_time
        
        # Current correlates with RPM and load
        base_current = self.base_current
        load_factor = 0.5 * math.sin(self.cycle_time / 45)  # 45-second load cycle
        random_variation = random.uniform(-1, 1)
        
        current = base_current + (load_factor * 5) + random_variation
        return round(max(0, min(30, current)), 2)  # Clamp between 0-30A
    
    def get_power(self):
        """Generate realistic power output readings"""
        # Power correlates with RPM and current
        rpm = self.get_rpm()
        current = self.get_current()
        
        # Power = (RPM/3000) * (Current/20) * BasePower
        power_factor = (rpm / 3000) * (current / 20)
        power = self.base_power * power_factor
        
        return int(max(0, min(3000, power)))  # Clamp between 0-3000W
    
    def get_status(self):
        """Get engine operational status"""
        # Status: 1 = Running, 0 = Stopped, 2 = Maintenance
        return 1  # Always running for simulation
    
    def get_uptime(self):
        """Get engine uptime in seconds"""
        return int(time.time() - self.start_time)
    
    def handle_snmp_request(self, oid):
        """Handle SNMP GET requests with logging"""
        try:
            if oid in self.mib_definitions:
                mib_info = self.mib_definitions[oid]
                value = mib_info['getter']()
                
                # Log the SNMP request and response
                self.log_snmp_message('GET_REQUEST', oid)
                self.log_snmp_message('GET_RESPONSE', oid, value)
                
                return value
            else:
                self.log_snmp_message('ERROR', oid, error=f"OID {oid} not found")
                return None
        except Exception as e:
            self.log_snmp_message('ERROR', oid, error=str(e))
            return None
    
    def get_message_log(self):
        """Get the SNMP message log"""
        return self.message_log
    
    def get_mib_info(self):
        """Get MIB definitions for this engine"""
        return {
            'engine_id': self.engine_id,
            'port': self.port,
            'mib_definitions': self.mib_definitions,
            'message_count': len(self.message_log)
        }
    
    def start_simulation(self):
        """Start the engine simulation"""
        self.running = True
        print(f"🚀 Starting enhanced SNMP agent for {self.engine_id} on port {self.port}")
        print(f"📊 MIB OIDs available:")
        for oid, info in self.mib_definitions.items():
            print(f"   {oid} - {info['name']} ({info['description']})")
        print(f"🔗 Community string: {self.community}")
        print(f"🌐 Agent listening on 127.0.0.1:{self.port}")
        print("-" * 60)

# Global dictionary to hold agent instances and their data
AGENT_INSTANCES = {}
AGENT_DATA = {}

def create_enhanced_agents():
    """Create enhanced SNMP agents for all engines"""
    engines_config = {
        "Engine-1": {"port": 1611, "base_temp": 45, "base_rpm": 1800, "base_current": 12.5, "base_power": 1500},
        "Engine-2": {"port": 1612, "base_temp": 50, "base_rpm": 2000, "base_current": 15.0, "base_power": 1800},
        "Engine-3": {"port": 1613, "base_temp": 40, "base_rpm": 1600, "base_current": 10.0, "base_power": 1200},
    }
    
    for engine_id, config in engines_config.items():
        agent = EnhancedEngineSNMPAgent(
            engine_id=engine_id,
            port=config["port"],
            base_temp=config["base_temp"],
            base_rpm=config["base_rpm"],
            base_current=config["base_current"],
            base_power=config["base_power"]
        )
        
        agent.start_simulation()
        AGENT_INSTANCES[engine_id] = agent
        
        # Initialize agent data with correct field names for frontend
        AGENT_DATA[engine_id] = {
            'engine_id': engine_id,
            'temperature': agent.get_temperature(),
            'rpm': agent.get_rpm(),
            'current': agent.get_current(),
            'power': agent.get_power(),  # Changed from 'power_output' to 'power'
            'status': agent.get_status(),
            'uptime': agent.get_uptime(),
            'last_updated': time.time(),
            'port': config["port"],
            'health_status': 'healthy' if agent.get_status() == 1 else 'stopped'
        }
    
    return AGENT_INSTANCES, AGENT_DATA

def simulate_snmp_queries():
    """Simulate SNMP queries to show protocol interaction"""
    print("\n🔄 Simulating SNMP queries to demonstrate protocol...")
    
    for engine_id, agent in AGENT_INSTANCES.items():
        print(f"\n📡 Querying {engine_id} SNMP Agent:")
        
        # Query all MIB variables
        for oid, mib_info in agent.mib_definitions.items():
            value = agent.handle_snmp_request(oid)
            if value is not None:
                print(f"   {mib_info['name']}: {value} {mib_info['units']}")
        
        # Update global data with correct field names
        AGENT_DATA[engine_id].update({
            'temperature': agent.get_temperature(),
            'rpm': agent.get_rpm(),
            'current': agent.get_current(),
            'power': agent.get_power(),  # Changed from 'power_output' to 'power'
            'status': agent.get_status(),
            'uptime': agent.get_uptime(),
            'last_updated': time.time(),
            'health_status': 'healthy' if agent.get_status() == 1 else 'stopped'
        })

def get_agent_message_logs():
    """Get all agent message logs"""
    all_logs = {}
    for engine_id, agent in AGENT_INSTANCES.items():
        all_logs[engine_id] = agent.get_message_log()
    return all_logs

def get_mib_definitions():
    """Get MIB definitions for all agents"""
    mib_info = {}
    for engine_id, agent in AGENT_INSTANCES.items():
        # Create serializable MIB definitions (remove function references)
        serializable_mib = {}
        for oid, mib_data in agent.mib_definitions.items():
            serializable_mib[oid] = {
                'name': mib_data['name'],
                'description': mib_data['description'],
                'type': mib_data['type'],
                'units': mib_data['units'],
                'access': mib_data['access']
            }
        
        mib_info[engine_id] = {
            'engine_id': agent.engine_id,
            'port': agent.port,
            'mib_definitions': serializable_mib,
            'message_count': len(agent.message_log)
        }
    return mib_info

if __name__ == "__main__":
    # Create enhanced agents
    agents, data = create_enhanced_agents()
    
    # Simulate some SNMP queries
    simulate_snmp_queries()
    
    # Keep running to show continuous operation
    try:
        while True:
            time.sleep(5)
            simulate_snmp_queries()
    except KeyboardInterrupt:
        print("\n🛑 Stopping enhanced SNMP agents...")
