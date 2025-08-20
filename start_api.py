#!/usr/bin/env python3
"""
Startup script for AstroCSV FastAPI server.
"""

import uvicorn
from api.main import app

if __name__ == "__main__":
    print("🚀 Starting AstroCSV API Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Interactive API: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
