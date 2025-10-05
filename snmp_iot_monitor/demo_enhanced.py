#!/usr/bin/env python3
"""
Enhanced SNMP Simulation Demo Script
Demonstrates professional SNMP logging and real-time data display.
"""

import requests
import time
import json
from datetime import datetime

def demo_enhanced_snmp_system():
    """Demonstrate the enhanced SNMP system with professional logging"""
    
    print("🚀 Enhanced SNMP Industrial IoT Monitor Demo")
    print("=" * 70)
    print("This demo shows professional SNMP protocol communication")
    print("with detailed logging, MIB definitions, and real-time data.")
    print("=" * 70)
    
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
    
    # Get current engine data
    print("📊 Current Engine Data:")
    print("-" * 50)
    try:
        engines_response = requests.get(f"{base_url}/api/engines")
        engines_data = engines_response.json()
        
        if engines_data['success']:
            for engine_id, engine_data in engines_data['data'].items():
                print(f"\n🔧 {engine_id}:")
                print(f"   🌡️  Temperature: {engine_data['temperature']}°C")
                print(f"   ⚡ RPM: {engine_data['rpm']}")
                print(f"   🔌 Current: {engine_data['current']}A")
                print(f"   ⚡ Power: {engine_data['power']}W")
                print(f"   📊 Status: {'Running' if engine_data['status'] == 1 else 'Stopped'}")
                print(f"   🏥 Health: {engine_data['health_status']}")
                print(f"   ⏱️  Uptime: {engine_data['uptime']}s")
                print(f"   🔗 Port: {engine_data['port']}")
        else:
            print(f"❌ Error getting engine data: {engines_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("🔄 Triggering Enhanced SNMP Simulation...")
    print("=" * 70)
    
    # Trigger multiple SNMP simulations to show professional logging
    for i in range(3):
        print(f"\n🔄 Round {i+1}: Professional SNMP Query Simulation")
        print("-" * 50)
        try:
            sim_response = requests.get(f"{base_url}/api/snmp/simulate")
            sim_data = sim_response.json()
            if sim_data['success']:
                print("✅ SNMP queries simulated successfully")
                print("📡 Check the console output above for detailed SNMP protocol messages")
            else:
                print(f"❌ Error: {sim_data['error']}")
        except Exception as e:
            print(f"❌ Error triggering simulation: {e}")
        
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print("📋 MIB Definitions (Professional Format):")
    print("=" * 70)
    
    # Get MIB definitions
    try:
        mib_response = requests.get(f"{base_url}/api/snmp/mib")
        mib_data = mib_response.json()
        
        if mib_data['success']:
            for engine_id, engine_info in mib_data['data'].items():
                print(f"\n🔧 {engine_id} MIB Definitions (Port {engine_info['port']}):")
                print(f"   📊 Total Messages: {engine_info['message_count']}")
                print("   " + "-" * 60)
                
                for oid, mib_def in engine_info['mib_definitions'].items():
                    print(f"   📍 OID: {oid}")
                    print(f"   ├─ Name: {mib_def['name']}")
                    print(f"   ├─ Description: {mib_def['description']}")
                    print(f"   ├─ Data Type: {mib_def['type']}")
                    print(f"   ├─ Units: {mib_def['units']}")
                    print(f"   └─ Access: {mib_def['access']}")
                    print()
        else:
            print(f"❌ Error getting MIB definitions: {mib_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("📡 Professional SNMP Message Log:")
    print("=" * 70)
    
    # Get SNMP messages
    try:
        messages_response = requests.get(f"{base_url}/api/snmp/messages")
        messages_data = messages_response.json()
        
        if messages_data['success']:
            for engine_id, messages in messages_data['data'].items():
                print(f"\n🔧 {engine_id} Professional SNMP Log:")
                print("   " + "-" * 50)
                
                # Show last 5 messages with professional format
                recent_messages = messages[-5:] if len(messages) > 5 else messages
                
                for msg in recent_messages:
                    timestamp = msg['timestamp']
                    msg_type = msg['message_type']
                    oid = msg['oid']
                    mib_name = msg['mib_name']
                    value = msg.get('value')
                    error = msg.get('error')
                    data_type = msg.get('data_type', 'Unknown')
                    access = msg.get('access', 'Unknown')
                    community = msg.get('community', 'Unknown')
                    
                    print(f"   📅 {timestamp}")
                    if msg_type == 'GET_REQUEST':
                        print(f"   🔍 SNMP GET Request")
                        print(f"   ├─ Engine: {engine_id} (Port {msg['port']})")
                        print(f"   ├─ OID: {oid}")
                        print(f"   ├─ MIB Name: {mib_name}")
                        print(f"   ├─ Data Type: {data_type}")
                        print(f"   ├─ Access: {access}")
                        print(f"   └─ Community: {community}")
                    elif msg_type == 'GET_RESPONSE':
                        print(f"   📤 SNMP GET Response")
                        print(f"   ├─ Engine: {engine_id} (Port {msg['port']})")
                        print(f"   ├─ OID: {oid}")
                        print(f"   ├─ MIB Name: {mib_name}")
                        print(f"   ├─ Value: {value}")
                        print(f"   ├─ Data Type: {data_type}")
                        print(f"   └─ Response Time: <1ms")
                    elif msg_type == 'ERROR':
                        print(f"   ❌ SNMP Error")
                        print(f"   ├─ Engine: {engine_id} (Port {msg['port']})")
                        print(f"   ├─ OID: {oid}")
                        print(f"   ├─ MIB Name: {mib_name}")
                        print(f"   ├─ Error: {error}")
                        print(f"   └─ Community: {community}")
                    print()
        else:
            print(f"❌ Error getting messages: {messages_data['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("🌐 Enhanced Web Dashboard URLs:")
    print("=" * 70)
    print("📊 Dashboard: http://localhost:3000")
    print("   ├─ Real-time engine monitoring")
    print("   ├─ Interactive charts and graphs")
    print("   └─ Health status indicators")
    print()
    print("🔍 SNMP Monitor: http://localhost:3000 (Click 'SNMP Monitor' tab)")
    print("   ├─ Basic SNMP message logs")
    print("   ├─ MIB definitions display")
    print("   └─ Engine-specific filtering")
    print()
    print("📡 Professional Log: http://localhost:3000 (Click 'Professional Log' tab)")
    print("   ├─ Professional SNMP protocol logging")
    print("   ├─ Detailed message analysis")
    print("   ├─ Advanced filtering options")
    print("   └─ Real-time protocol monitoring")
    print()
    print("🔗 Backend API: http://127.0.0.1:5003")
    print("   ├─ /api/engines - Engine data")
    print("   ├─ /api/snmp/messages - SNMP message logs")
    print("   ├─ /api/snmp/mib - MIB definitions")
    print("   └─ /api/snmp/simulate - Trigger SNMP queries")
    print()
    print("💡 Professional Features:")
    print("   ✅ Real-time SNMP protocol communication")
    print("   ✅ Professional detailed logging format")
    print("   ✅ Complete MIB definitions with OID mappings")
    print("   ✅ Live engine data with realistic variations")
    print("   ✅ Three-tier dashboard (Dashboard, SNMP Monitor, Professional Log)")
    print("   ✅ Advanced filtering and message analysis")
    print("   ✅ Educational SNMP protocol demonstration")

if __name__ == "__main__":
    demo_enhanced_snmp_system()
