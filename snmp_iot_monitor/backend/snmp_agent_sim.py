#!/usr/bin/env python3
"""
SNMP Agent Simulator for Industrial IoT Engines
Simulates 3 engines with realistic sensor data for temperature, RPM, current, and power output.
Each engine runs on a different port (1611, 1612, 1613) to simulate separate devices.
"""

import time
import math
import random
import threading
from datetime import datetime
from pysnmp.hlapi import *

class EngineSNMPAgent:
    """
    Simulates an SNMP agent for a single industrial engine.
    Provides realistic sensor data with smooth variations and realistic patterns.
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
        
        # Engine-specific OID mappings
        self.oids = {
            '1.3.6.1.4.1.9999.1.1.1.0': self.get_temperature,  # Engine Temperature
            '1.3.6.1.4.1.9999.1.1.2.0': self.get_rpm,          # Engine RPM
            '1.3.6.1.4.1.9999.1.1.3.0': self.get_current,      # Engine Current
            '1.3.6.1.4.1.9999.1.1.4.0': self.get_power,        # Engine Power Output
            '1.3.6.1.4.1.9999.1.1.5.0': self.get_status,       # Engine Status
            '1.3.6.1.4.1.9999.1.1.6.0': self.get_uptime,       # Engine Uptime
        }
        
        # SNMP community string
        self.community = 'public'
        
    def get_temperature(self):
        """Generate realistic temperature readings with gradual variations"""
        # Temperature varies with a sine wave + small random fluctuations
        # Base temperature varies by engine load and time
        time_factor = math.sin(self.cycle_time * 0.1) * 3  # ±3°C variation
        load_factor = math.sin(self.cycle_time * 0.05) * 5  # ±5°C load variation
        random_factor = random.uniform(-1, 1)  # ±1°C random noise
        
        temp = self.base_temp + time_factor + load_factor + random_factor
        
        # Add some realistic constraints
        if temp < 20:
            temp = 20
        elif temp > 120:
            temp = 120
            
        return round(temp, 1)
    
    def get_rpm(self):
        """Generate realistic RPM readings"""
        # RPM varies with load and has some natural fluctuation
        load_variation = math.sin(self.cycle_time * 0.08) * 50  # ±50 RPM
        random_variation = random.uniform(-20, 20)  # ±20 RPM noise
        
        rpm = self.base_rpm + load_variation + random_variation
        
        # Keep RPM within realistic bounds
        if rpm < 500:
            rpm = 500
        elif rpm > 3000:
            rpm = 3000
            
        return int(rpm)
    
    def get_current(self):
        """Generate realistic current readings"""
        # Current correlates with power output and load
        power_factor = (self.get_power() / self.base_power) * 2  # Current scales with power
        load_variation = math.sin(self.cycle_time * 0.12) * 1.5  # ±1.5A variation
        random_variation = random.uniform(-0.5, 0.5)  # ±0.5A noise
        
        current = (self.base_current * power_factor) + load_variation + random_variation
        
        # Keep current within realistic bounds
        if current < 0:
            current = 0
        elif current > 30:
            current = 30
            
        return round(current, 2)
    
    def get_power(self):
        """Generate realistic power output readings"""
        # Power output varies with load and efficiency
        load_factor = math.sin(self.cycle_time * 0.06) * 200  # ±200W load variation
        efficiency_factor = random.uniform(0.85, 0.95)  # 85-95% efficiency
        random_variation = random.uniform(-50, 50)  # ±50W noise
        
        power = (self.base_power + load_factor) * efficiency_factor + random_variation
        
        # Keep power within realistic bounds
        if power < 0:
            power = 0
        elif power > 2500:
            power = 2500
            
        return int(power)
    
    def get_status(self):
        """Generate engine status (1=Running, 0=Stopped)"""
        # For simulation, engine is always running
        return 1
    
    def get_uptime(self):
        """Generate engine uptime in seconds"""
        return int(time.time() - self.start_time)
    
    def update_cycle_time(self):
        """Update the cycle time for smooth variations"""
        self.cycle_time = time.time() - self.start_time
    
    def handle_snmp_request(self, oid):
        """Handle SNMP GET requests"""
        self.update_cycle_time()
        
        if oid in self.oids:
            value = self.oids[oid]()
            return str(value)
        else:
            return None
    
    def start_agent(self):
        """Start the SNMP agent simulation"""
        print(f"🚀 Starting Engine {self.engine_id} SNMP Agent on port {self.port}")
        self.running = True
        
        # Simulate SNMP agent behavior
        while self.running:
            try:
                # In a real implementation, this would handle actual SNMP requests
                # For simulation, we just update our data
                self.update_cycle_time()
                time.sleep(0.1)  # Update every 100ms
            except KeyboardInterrupt:
                self.stop_agent()
                break
    
    def stop_agent(self):
        """Stop the SNMP agent"""
        print(f"🛑 Stopping Engine {self.engine_id} SNMP Agent")
        self.running = False

def start_engine_agents():
    """Start all 3 engine SNMP agents in separate threads"""
    engines = [
        EngineSNMPAgent("Engine-1", 1611, base_temp=42, base_rpm=1750, base_current=11.8, base_power=1450),
        EngineSNMPAgent("Engine-2", 1612, base_temp=48, base_rpm=1850, base_current=13.2, base_power=1620),
        EngineSNMPAgent("Engine-3", 1613, base_temp=45, base_rpm=1800, base_current=12.5, base_power=1500)
    ]
    
    threads = []
    
    for engine in engines:
        thread = threading.Thread(target=engine.start_agent, daemon=True)
        thread.start()
        threads.append((engine, thread))
    
    print("🏭 All 3 Engine SNMP Agents started!")
    print("📊 Engine-1: Port 1611 (Cooler, Lower RPM)")
    print("📊 Engine-2: Port 1612 (Warmer, Higher RPM)")  
    print("📊 Engine-3: Port 1613 (Balanced)")
    print("\nPress Ctrl+C to stop all agents...")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all engine agents...")
        for engine, thread in threads:
            engine.stop_agent()
        print("✅ All agents stopped.")

if __name__ == "__main__":
    start_engine_agents()
