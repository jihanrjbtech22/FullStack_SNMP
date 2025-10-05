#!/usr/bin/env python3
"""
Flask Web Server for Industrial IoT SNMP Monitoring
Provides REST API for engine monitoring data and serves the frontend.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from snmp_manager import get_snmp_manager
from enhanced_snmp_agent import create_enhanced_agents, simulate_snmp_queries, get_agent_message_logs, get_mib_definitions, AGENT_DATA

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Get SNMP manager instance
snmp_manager = get_snmp_manager()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return jsonify({
        'service': 'Industrial IoT SNMP Monitor',
        'status': 'running',
        'endpoints': {
            'engines': '/api/engines',
            'health': '/api/health',
            'summary': '/api/summary'
        },
        'frontend': 'Use the React frontend at http://localhost:3000',
        'timestamp': time.time()
    })

@app.route('/api/engines')
def get_engines():
    """Get data for all engines"""
    try:
        data = snmp_manager.get_all_engines_data()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/engines/<engine_id>')
def get_engine(engine_id):
    """Get data for a specific engine"""
    try:
        data = snmp_manager.get_engine_data(engine_id)
        if data:
            return jsonify({
                'success': True,
                'data': data,
                'timestamp': time.time()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Engine {engine_id} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summary')
def get_summary():
    """Get summary statistics for all engines"""
    try:
        data = snmp_manager.get_engines_summary()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SNMP IoT Monitor',
        'timestamp': time.time()
    })

@app.route('/api/snmp/messages')
def get_snmp_messages():
    """Get SNMP message logs for all engines"""
    try:
        message_logs = get_agent_message_logs()
        return jsonify({
            'success': True,
            'data': message_logs,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/snmp/mib')
def get_mib_definitions_endpoint():
    """Get MIB definitions for all engines"""
    try:
        mib_info = get_mib_definitions()
        return jsonify({
            'success': True,
            'data': mib_info,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/snmp/simulate')
def simulate_snmp_queries_endpoint():
    """Manually trigger SNMP query simulation"""
    try:
        simulate_snmp_queries()
        return jsonify({
            'success': True,
            'message': 'SNMP queries simulated successfully',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/engines/enhanced')
def get_enhanced_engines_data():
    """Get enhanced engine data with SNMP details"""
    try:
        # Update data with latest values
        for engine_id, data in AGENT_DATA.items():
            data.update({
                'last_updated': time.time(),
                'snmp_port': data.get('port', 1611 + int(engine_id.split('-')[1]) - 1)
            })
        
        return jsonify({
            'success': True,
            'data': AGENT_DATA,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def start_enhanced_snmp_simulation():
    """Start enhanced SNMP simulation with explicit message logging"""
    print("🚀 Starting Enhanced SNMP Simulation...")
    
    # Create enhanced agents
    agents, data = create_enhanced_agents()
    
    def continuous_simulation():
        """Run continuous SNMP simulation"""
        while True:
            time.sleep(3)  # Simulate SNMP queries every 3 seconds
            simulate_snmp_queries()
    
    # Start simulation in background thread
    simulation_thread = threading.Thread(target=continuous_simulation, daemon=True)
    simulation_thread.start()
    
    print("✅ Enhanced SNMP simulation started with explicit message logging")

if __name__ == '__main__':
    # Start enhanced SNMP simulation
    start_enhanced_snmp_simulation()
    
    print("🌐 Starting Flask web server...")
    print("📊 Industrial IoT SNMP Monitor with Enhanced SNMP Simulation")
    print("🔗 API Endpoints:")
    print("   GET /api/engines - All engines data")
    print("   GET /api/engines/enhanced - Enhanced engines data with SNMP details")
    print("   GET /api/snmp/messages - SNMP message logs")
    print("   GET /api/snmp/mib - MIB definitions")
    print("   GET /api/snmp/simulate - Manually trigger SNMP queries")
    print("   GET /api/health - Health check")
    print("\n🌐 Web Dashboard: http://127.0.0.1:5003")
    print("📡 SNMP Protocol Messages: Check console output for real-time SNMP communication")
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5003)
