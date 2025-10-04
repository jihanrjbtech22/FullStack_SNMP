#!/bin/bash

# Industrial IoT SNMP Monitor Startup Script
# This script starts both backend and frontend services

echo "🏭 Starting Industrial IoT SNMP Monitor..."
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the snmp_iot_monitor directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected structure: snmp_iot_monitor/{backend,frontend}/"
    exit 1
fi

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $port is already in use"
        return 1
    fi
    return 0
}

# Check required ports
echo "🔍 Checking ports..."
if ! check_port 5003; then
    echo "❌ Backend port 5003 is in use. Please stop the service or change the port."
    exit 1
fi

if ! check_port 3000; then
    echo "❌ Frontend port 3000 is in use. Please stop the service or change the port."
    exit 1
fi

# Start backend
echo "🚀 Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Start backend in background
echo "🌐 Starting Flask server on port 5003..."
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Failed to start backend server"
    exit 1
fi

echo "✅ Backend started successfully (PID: $BACKEND_PID)"

# Start frontend
echo "🚀 Starting frontend server..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start frontend in background
echo "🌐 Starting React development server on port 3000..."
npm start &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Failed to start frontend server"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Industrial IoT SNMP Monitor is running!"
echo "=========================================="
echo "🌐 Frontend Dashboard: http://127.0.0.1:3000"
echo "🔧 Backend API: http://127.0.0.1:5003"
echo "📊 API Health: http://127.0.0.1:5003/api/health"
echo ""
echo "📋 Services:"
echo "   Backend (Flask): PID $BACKEND_PID"
echo "   Frontend (React): PID $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
