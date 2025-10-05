#!/usr/bin/env python3
"""
SNMP Simulation Demo Script
Demonstrates explicit SNMP message exchange and MIB values for educational purposes.
"""

import requests
import time
import json
from datetime import datetime

def demo_snmp_simulation():
    """Demonstrate SNMP simulation with explicit message logging"""
    
    print("🔍 SNMP Simulation Demo")
    print("=" * 60)
    print("This demo shows explicit SNMP protocol communication")
    print("between SNMP Manager and Engine Agents.")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5003"
    
    # Check if backend is running
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running. Please start the backend first.")
            return
    except requests.exceptions.RequestException:
        print("❌ Backend not running. Please start the backend first.")
        return
    
    print("✅ Backend is running")
    print()
    
    # Get MIB definitions
    print("📋 MIB Definitions:")
    print("-" * 40)
    try:
        mib_response = requests.get(f"{base_url}/api/snmp/mib")
        mib_data = mib_response.json()
        
        if mib_data['success']:
            for engine_id, engine_info in mib_data['data'].items():
                print(f"\n🔧 {engine_id} (Port {engine_info['port']}):")
                for oid, mib_def in engine_info['mib_definitions'].items():
                    print(f"   {oid}")
                    print(f"   ├─ Name: {mib_def['name']}")
                    print(f"   ├─ Description: {mib_def['description']}")
                    print(f"   ├─ Type: {mib_def['type']}")
                    print(f"   ├─ Units: {mib_def['units']}")
                    print(f"   └─ Access: {mib_def['access']}")
        else:
            print(f"❌ Error getting MIB definitions: {mib_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🔄 Simulating SNMP Queries...")
    print("=" * 60)
    
    # Trigger SNMP simulation
    for i in range(3):
        print(f"\n🔄 Round {i+1}: Triggering SNMP queries...")
        try:
            sim_response = requests.get(f"{base_url}/api/snmp/simulate")
            sim_data = sim_response.json()
            if sim_data['success']:
                print("✅ SNMP queries simulated successfully")
            else:
                print(f"❌ Error: {sim_data['error']}")
        except Exception as e:
            print(f"❌ Error triggering simulation: {e}")
        
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("📡 SNMP Message Log:")
    print("=" * 60)
    
    # Get SNMP messages
    try:
        messages_response = requests.get(f"{base_url}/api/snmp/messages")
        messages_data = messages_response.json()
        
        if messages_data['success']:
            for engine_id, messages in messages_data['data'].items():
                print(f"\n🔧 {engine_id} SNMP Messages:")
                print("-" * 30)
                
                # Show last 10 messages
                recent_messages = messages[-10:] if len(messages) > 10 else messages
                
                for msg in recent_messages:
                    timestamp = msg['timestamp']
                    msg_type = msg['message_type']
                    oid = msg['oid']
                    mib_name = msg['mib_name']
                    value = msg.get('value')
                    error = msg.get('error')
                    
                    if msg_type == 'GET_REQUEST':
                        print(f"🔍 [{timestamp}] GET Request: {oid} ({mib_name})")
                    elif msg_type == 'GET_RESPONSE':
                        print(f"📤 [{timestamp}] GET Response: {oid} = {value}")
                    elif msg_type == 'ERROR':
                        print(f"❌ [{timestamp}] Error: {error} for {oid}")
        else:
            print(f"❌ Error getting messages: {messages_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📊 Engine Data:")
    print("=" * 60)
    
    # Get current engine data
    try:
        engines_response = requests.get(f"{base_url}/api/engines")
        engines_data = engines_response.json()
        
        if engines_data['success']:
            for engine_id, engine_data in engines_data['data'].items():
                print(f"\n🔧 {engine_id}:")
                print(f"   🌡️  Temperature: {engine_data['temperature']}°C")
                print(f"   ⚡ RPM: {engine_data['rpm']}")
                print(f"   🔌 Current: {engine_data['current']}A")
                print(f"   ⚡ Power: {engine_data['power_output']}W")
                print(f"   📊 Status: {'Running' if engine_data['status'] == 1 else 'Stopped'}")
                print(f"   ⏱️  Uptime: {engine_data['uptime']}s")
        else:
            print(f"❌ Error getting engine data: {engines_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🌐 Web Dashboard URLs:")
    print("=" * 60)
    print("📊 Dashboard: http://localhost:3000")
    print("🔍 SNMP Monitor: http://localhost:3000 (Click 'SNMP Monitor' tab)")
    print("🔗 Backend API: http://127.0.0.1:5003")
    print("\n💡 The dashboard shows real-time SNMP communication!")
    print("   - Switch to 'SNMP Monitor' tab to see message logs")
    print("   - Watch the console for live SNMP protocol messages")
    print("   - MIB definitions show OID mappings and data types")

if __name__ == "__main__":
    demo_snmp_simulation()
