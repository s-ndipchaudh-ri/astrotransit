# 🍎 LBAT Desktop Application - macOS Guide

Complete guide for building and running the LBAT Desktop Application on macOS.

## 🚀 Quick Start

### 1. Setup (One-time)
```bash
# Make scripts executable
chmod +x setup_mac.sh dev_mac.sh build_mac.sh

# Run setup script
./setup_mac.sh
```

### 2. Development Mode
```bash
# Start the app in development mode
./dev_mac.sh
```

### 3. Build for Distribution
```bash
# Create macOS .dmg file
./build_mac.sh
```

## 📋 Prerequisites

- **macOS** 10.15 (Catalina) or later
- **Xcode Command Line Tools** (required for building)
- **Homebrew** (for package management)
- **Node.js** 18.0 or higher
- **Python** 3.11 or higher

## 🛠️ Installation Steps

### Step 1: Install Xcode Command Line Tools
```bash
xcode-select --install
```
This will open a popup window. Click "Install" and wait for completion.

### Step 2: Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**For M1/M2 Macs (Apple Silicon):**
```bash
# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 3: Install Node.js and Python
```bash
brew install node python@3.11
```

### Step 4: Verify Installation
```bash
node --version    # Should be 18.0+
npm --version     # Should be 9.0+
python3 --version # Should be 3.11+
```

## 🔧 Development Setup

### Option 1: Automated Setup
```bash
./setup_mac.sh
```

### Option 2: Manual Setup
```bash
# Install Node.js dependencies
npm install

# Install Python backend dependencies
cd python_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

## 🚀 Running the Application

### Development Mode (Recommended for development)
```bash
./dev_mac.sh
```

This will:
- Start the React development server
- Launch Electron with hot reloading
- Open the desktop application
- Enable DevTools (F12 or Cmd+Option+I)

### Alternative: Manual Development
```bash
# Terminal 1: Start React
npm start

# Terminal 2: Start Electron
npm run electron
```

## 📱 Building for Distribution

### Create macOS .dmg File
```bash
./build_mac.sh
```

### Manual Build
```bash
npm run dist-mac
```

### Build All Platforms
```bash
npm run dist
```

## 📁 Project Structure (macOS)

```
LBAT/
├── public/
│   ├── electron.js          # Electron main process
│   ├── preload.js           # Secure API bridge
│   ├── icon.png             # Linux icon
│   ├── icon.icns            # macOS icon
│   └── index.html           # React entry point
├── src/                     # React components
├── python_backend/
│   ├── main.py              # FastAPI backend server
│   ├── requirements.txt     # Python dependencies
│   ├── venv/                # Python virtual environment
│   └── outputs/             # Generated CSV files
├── package.json             # Node.js configuration
├── setup_mac.sh             # macOS setup script
├── dev_mac.sh               # Development script
├── build_mac.sh             # Build script
└── dist/                    # Built application (after build)
```

## 🎯 macOS-Specific Features

### Native macOS Integration
- **Menu Bar**: Native macOS menu with app name
- **Dock Icon**: Custom icon in the dock
- **Window Management**: Native macOS window controls
- **File Dialogs**: Native macOS file picker dialogs

### Build Output
- **Target**: DMG file (macOS disk image)
- **Installation**: Drag and drop to Applications folder
- **Code Signing**: Ready for Apple Developer Program (optional)

## 🔍 Troubleshooting

### Common Issues

#### 1. "Permission Denied" Error
```bash
# Make scripts executable
chmod +x *.sh
```

#### 2. Python Virtual Environment Issues
```bash
# Remove and recreate virtual environment
cd python_backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

#### 3. Node.js Version Issues
```bash
# Check Node.js version
node --version

# If version is too old, update via Homebrew
brew upgrade node
```

#### 4. Xcode Command Line Tools Issues
```bash
# Reinstall Xcode Command Line Tools
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

#### 5. Build Failures
```bash
# Clear build cache
rm -rf node_modules
rm -rf build
rm -rf dist
npm install
```

### Getting Help

1. **Check Console Output**: Look for error messages in Terminal
2. **Verify Prerequisites**: Run `./setup_mac.sh` to check all requirements
3. **Check File Permissions**: Ensure scripts are executable
4. **Review Logs**: Check both Node.js and Python backend logs

## 🚀 Advanced Configuration

### Environment Variables
```bash
# Set custom port for Python backend
export PORT=8001
export HOST=127.0.0.1

# Run with custom configuration
npm run electron-dev
```

### Custom Build Configuration
Edit `package.json` build section:
```json
"build": {
  "mac": {
    "target": "dmg",
    "icon": "public/icon.icns",
    "category": "public.app-category.utilities",
    "hardenedRuntime": true,
    "gatekeeperAssess": false
  }
}
```

### Code Signing (for App Store)
```bash
# Set environment variables
export CSC_LINK=/path/to/certificate.p12
export CSC_KEY_PASSWORD=your_password

# Build with code signing
npm run dist-mac
```

## 📱 Distribution

### DMG File
- **Location**: `dist/` folder
- **Format**: macOS disk image
- **Installation**: Double-click and drag to Applications

### App Bundle
- **Location**: `dist/mac/` folder
- **Format**: `.app` bundle
- **Usage**: Can be run directly or copied to Applications

## 🔒 Security Features

- **Context Isolation**: Secure communication between processes
- **Preload Scripts**: Controlled API exposure
- **Sandboxing**: Process isolation
- **Code Signing**: Ready for macOS security features

## 📚 Additional Resources

- [Electron Documentation](https://www.electronjs.org/docs)
- [macOS Development Guide](https://developer.apple.com/macos/)
- [Homebrew Documentation](https://docs.brew.sh/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🆘 Support

If you encounter issues:

1. Check this README for troubleshooting steps
2. Verify all prerequisites are installed
3. Check the console output for error messages
4. Ensure you're running the latest version of macOS

---

**Happy coding on macOS! 🍎✨**
