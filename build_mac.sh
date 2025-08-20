#!/bin/bash

# Shell script to build LBAT Desktop Application for macOS
# Make sure to run: chmod +x build_mac.sh

echo "🍎 Building LBAT Desktop Application for macOS..."
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
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Python dependencies"
    exit 1
fi
cd ..

# Step 3: Build React application
echo "⚛️  Step 3: Building React application..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build React application"
    exit 1
fi

# Step 4: Build Electron application for macOS
echo "🖥️  Step 4: Building Electron application for macOS..."
npm run dist-mac
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build Electron application"
    exit 1
fi

echo ""
echo "✅ Build completed successfully!"
echo "📱 The macOS application can be found in the 'dist' folder."
echo "🎯 Look for the .dmg file for distribution."
echo ""
