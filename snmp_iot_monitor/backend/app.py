#!/usr/bin/env python3
"""
Flask Web Server for Industrial IoT SNMP Monitoring
Provides REST API for engine monitoring data and serves the frontend.
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
from snmp_manager import get_snmp_manager

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Get SNMP manager instance
snmp_manager = get_snmp_manager()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

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

def start_snmp_polling():
    """Start SNMP polling in background thread"""
    print("🚀 Starting SNMP Manager polling...")
    snmp_manager.start_polling()

if __name__ == '__main__':
    # Start SNMP polling in background
    start_snmp_polling()
    
    print("🌐 Starting Flask web server...")
    print("📊 Industrial IoT SNMP Monitor")
    print("🔗 API Endpoints:")
    print("   GET /api/engines - All engines data")
    print("   GET /api/engines/<id> - Specific engine data")
    print("   GET /api/summary - Summary statistics")
    print("   GET /api/health - Health check")
    print("\n🌐 Web Dashboard: http://127.0.0.1:5003")
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5003)
