#!/bin/bash

# Build Windows Application from macOS
# This script builds the Windows installer from a Mac

echo "🪟 Building LBAT Desktop Application for Windows from macOS..."
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    echo "   For Windows builds, use build_windows.bat on a Windows machine"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root directory."
    exit 1
fi

echo "📋 Prerequisites Check:"
echo "   - Node.js and npm installed"
echo "   - Python 3.11+ installed"
echo "   - All dependencies installed"
echo ""

# Step 1: Install Node.js dependencies
echo "📦 Step 1: Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Node.js dependencies"
    exit 1
fi

# Step 2: Install Python backend dependencies
echo "🐍 Step 2: Installing Python backend dependencies..."
cd python_backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "   Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "   Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Python dependencies"
    exit 1
fi

# Deactivate virtual environment
deactivate
cd ..

# Step 3: Build React application
echo "⚛️  Step 3: Building React application..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build React application"
    exit 1
fi

# Step 4: Build Electron application for Windows
echo "🪟 Step 4: Building Electron application for Windows..."
echo "   Note: This will create a Windows installer (.exe) file"
echo ""

npm run dist-win
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build Electron application for Windows"
    exit 1
fi

echo ""
echo "✅ Windows build completed successfully!"
echo ""
echo "📁 Build Output:"
echo "   - Windows Installer: dist/LBAT Desktop Setup 1.0.0.exe"
echo "   - Unpacked App: dist/win-unpacked/LBAT Desktop.exe"
echo "   - Update Info: dist/latest.yml"
echo ""
echo "🎯 What to give to Windows users:"
echo "   1. LBAT Desktop Setup 1.0.0.exe (main installer)"
echo "   2. Installation instructions (README_WINDOWS.md)"
echo "   3. System requirements info"
echo ""
echo "💡 The .exe file contains everything needed - users don't need to install Python or Node.js!"
echo ""
