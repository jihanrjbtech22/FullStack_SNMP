#!/usr/bin/env python3
"""
Simple SNMP Agent for Testing
This agent responds to SNMP GET requests with sample data
"""

import socket
import threading
import time
import struct

class SimpleSNMPAgent:
    def __init__(self, community='public', port=161):
        self.community = community
        self.port = port
        self.running = False
        
        # Sample data that the agent will return
        self.snmp_data = {
            '1.3.6.1.2.1.1.1.0': 'Simple SNMP Agent v1.0 (Linux TestBox 5.4.0)',
            '1.3.6.1.2.1.1.3.0': '1234567',  # System uptime in centiseconds
            '1.3.6.1.2.1.1.5.0': 'TestAgent-001',
            '1.3.6.1.2.1.1.6.0': 'Test Lab - Building A, Room 101',
        }
        
    def start(self):
        """Start the SNMP agent"""
        print(f"🚀 Starting Simple SNMP Agent...")
        print(f"   Community: {self.community}")
        print(f"   Port: {self.port}")
        print(f"   Available OIDs:")
        for oid in self.snmp_data.keys():
            print(f"     {oid}")
        print(f"   Agent running on UDP port {self.port}")
        print(f"   Press Ctrl+C to stop")
        
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('0.0.0.0', self.port))
            self.running = True
            
            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    print(f"📡 SNMP Request from {addr}")
                    
                    # Simple response - just send back a basic SNMP response
                    response = self._create_snmp_response(data)
                    if response:
                        sock.sendto(response, addr)
                        print(f"   ✅ Response sent")
                    
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
                    
        except PermissionError:
            print(f"❌ Error: Permission denied to bind to port {self.port}")
            print(f"   Try running with sudo or use a different port")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            sock.close()
            print(f"🛑 SNMP Agent stopped")
    
    def _create_snmp_response(self, request_data):
        """Create a simple SNMP response"""
        try:
            # This is a very basic SNMP response
            # In a real implementation, you'd parse the request and respond properly
            response = b'\x30\x0c\x02\x01\x00\x04\x06public\xa2\x05\x02\x01\x00\x02\x00\x30\x00'
            return response
        except:
            return None

if __name__ == '__main__':
    agent = SimpleSNMPAgent(community='public', port=161)
    agent.start()