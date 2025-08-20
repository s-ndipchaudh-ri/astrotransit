#!/usr/bin/env python3
"""
Startup script for AstroCSV React Frontend.
This script will install dependencies and start the React development server.
"""

import subprocess
import sys
import os
import time

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_node():
    """Check if Node.js is installed."""
    result = run_command("node --version")
    if result:
        print(f"✅ Node.js found: {result.strip()}")
        return True
    else:
        print("❌ Node.js not found. Please install Node.js first.")
        print("   Download from: https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed."""
    result = run_command("npm --version")
    if result:
        print(f"✅ npm found: {result.strip()}")
        return True
    else:
        print("❌ npm not found. Please install npm first.")
        return False

def install_dependencies():
    """Install React dependencies."""
    print("📦 Installing React dependencies...")
    result = run_command("npm install", cwd="frontend")
    if result:
        print("✅ Dependencies installed successfully!")
        return True
    else:
        print("❌ Failed to install dependencies.")
        return False

def start_frontend():
    """Start the React development server."""
    print("🚀 Starting React development server...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("🔗 API should be running at: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run("npm start", shell=True, cwd="frontend")
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped.")

def main():
    print("🌟 AstroCSV Frontend Startup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_node():
        sys.exit(1)
    
    if not check_npm():
        sys.exit(1)
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found.")
        print("   Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main()
