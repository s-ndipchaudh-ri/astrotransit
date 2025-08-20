#!/bin/bash

# macOS Development Script for LBAT Desktop Application
# This script starts the application in development mode

echo "🔧 Starting LBAT Desktop Application in development mode..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root directory."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install Node.js dependencies"
        exit 1
    fi
fi

# Check if Python backend dependencies are installed
if [ ! -d "python_backend/venv" ]; then
    echo "🐍 Setting up Python virtual environment..."
    cd python_backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo "✅ Python virtual environment created and dependencies installed"
else
    echo "✅ Python virtual environment already exists"
fi

# Start the application in development mode
echo "🚀 Starting Electron in development mode..."
echo "📱 This will open the desktop application with hot reloading enabled"
echo "🔍 Press F12 or Cmd+Option+I to open DevTools"
echo ""

# Activate Python virtual environment and start the app
cd python_backend
source venv/bin/activate
cd ..

npm run electron-dev
