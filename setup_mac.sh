#!/bin/bash

# macOS Setup Script for LBAT Desktop Application
# This script installs prerequisites and sets up the development environment

echo "🍎 Setting up LBAT Desktop Application development environment on macOS..."
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for M1/M2 Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew is already installed"
fi

# Install Node.js
echo "📦 Installing Node.js..."
if ! command -v node &> /dev/null; then
    brew install node
else
    echo "✅ Node.js is already installed (version: $(node --version))"
fi

# Install Python
echo "🐍 Installing Python..."
if ! command -v python3 &> /dev/null; then
    brew install python@3.11
else
    echo "✅ Python is already installed (version: $(python3 --version))"
fi

# Install Xcode Command Line Tools (required for building)
echo "🛠️  Installing Xcode Command Line Tools..."
if ! xcode-select -p &> /dev/null; then
    xcode-select --install
    echo "⚠️  Please complete the Xcode Command Line Tools installation in the popup window"
    echo "   Then run this script again"
    exit 1
else
    echo "✅ Xcode Command Line Tools are already installed"
fi

# Install additional build tools
echo "🔧 Installing additional build tools..."
brew install git

# Check if all prerequisites are met
echo ""
echo "🔍 Checking prerequisites..."

PREREQS_MET=true

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    PREREQS_MET=false
else
    echo "✅ Node.js: $(node --version)"
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found"
    PREREQS_MET=false
else
    echo "✅ npm: $(npm --version)"
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    PREREQS_MET=false
else
    echo "✅ Python3: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found"
    PREREQS_MET=false
else
    echo "✅ pip3: $(pip3 --version)"
fi

if ! xcode-select -p &> /dev/null; then
    echo "❌ Xcode Command Line Tools not found"
    PREREQS_MET=false
else
    echo "✅ Xcode Command Line Tools: $(xcode-select -p)"
fi

echo ""

if [ "$PREREQS_MET" = true ]; then
    echo "🎉 All prerequisites are met!"
    echo ""
    echo "🚀 You can now build the application:"
    echo "   chmod +x build_mac.sh"
    echo "   ./build_mac.sh"
    echo ""
    echo "🔧 Or run in development mode:"
    echo "   npm run electron-dev"
else
    echo "❌ Some prerequisites are missing. Please install them and run this script again."
    exit 1
fi
