#!/usr/bin/env python3
"""
Mock SNMP Agent - Simulates SNMP responses for testing
This is a simplified version that returns mock data
"""

import time
import random

class MockSNMPAgent:
    def __init__(self):
        self.running = False
        
        # Mock data that simulates SNMP responses
        self.mock_responses = {
            '1.3.6.1.2.1.1.1.0': 'Mock SNMP Agent v1.0 (Linux TestBox 5.4.0)',
            '1.3.6.1.2.1.1.3.0': '1234567',  # System uptime
            '1.3.6.1.2.1.1.5.0': 'MockAgent-001',
            '1.3.6.1.2.1.1.6.0': 'Test Lab - Building A, Room 101',
        }
        
    def get_mock_data(self, oid):
        """Return mock SNMP data"""
        if oid in self.mock_responses:
            return self.mock_responses[oid]
        else:
            return f"Mock data for OID {oid}"
    
    def start_simulation(self):
        """Simulate agent running"""
        print("🎭 Mock SNMP Agent Simulation")
        print("   This simulates an SNMP agent with the following data:")
        for oid, value in self.mock_responses.items():
            print(f"     {oid}: {value}")
        print("   The Flask app will now show this mock data instead of errors!")
        print("   Press Ctrl+C to stop simulation")

if __name__ == '__main__':
    agent = MockSNMPAgent()
    agent.start_simulation()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Mock agent stopped")
