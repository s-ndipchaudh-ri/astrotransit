#!/usr/bin/env python3
"""
Python Backend for LBAT Desktop Application
Runs as a local server that Electron communicates with
"""

import sys
import os
import json
import asyncio
from datetime import datetime, date
from typing import Dict, Any, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Add the parent directory to Python path to import astrocsv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from astrocsv.ephem import get_sunrise_times, get_ascendant_at_time
    from astrocsv.mapping_library import (
        get_sign_and_lord, get_nakshatra_and_lord, get_kp_sub_lords,
        generate_degree_buckets
    )
    from astrocsv.csvout import generate_csv_rows_for_date, write_csv_to_file
except ImportError as e:
    logging.error(f"Failed to import astrocsv modules: {e}")
    # Create dummy functions for fallback
    def dummy_function(*args, **kwargs):
        raise Exception("AstroCSV modules not available")
    
    get_sunrise_times = dummy_function
    get_ascendant_at_time = dummy_function
    get_sign_and_lord = dummy_function
    get_nakshatra_and_lord = dummy_function
    get_kp_sub_lords = dummy_function
    generate_csv_rows_for_date = dummy_function
    write_csv_to_file = dummy_function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LBAT Desktop Backend",
    description="Python backend for LBAT Desktop application",
    version="1.0.0"
)

# Enable CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class AstroRequest(BaseModel):
    latitude: float
    longitude: float
    date: str
    include_degree_buckets: bool = True

class DateRangeRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    include_degree_buckets: bool = True

class AstroResponse(BaseModel):
    date: str
    sunrise_ist: str
    next_sunrise_ist: str
    latitude: float
    longitude: float
    ascendant_degree: float
    ascendant_sign: str
    ascendant_sign_lord: str
    ascendant_nakshatra: str
    ascendant_nakshatra_lord: str
    ascendant_sub_lord: str
    ascendant_sub_sub_lord: str
    degree_buckets: Optional[list] = None
    success: bool
    message: str

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    backend_version: str

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health information."""
    return HealthResponse(
        status="healthy",
        message="LBAT Desktop Backend is running",
        timestamp=datetime.now().isoformat(),
        backend_version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="LBAT Desktop Backend is running",
        timestamp=datetime.now().isoformat(),
        backend_version="1.0.0"
    )

@app.post("/calculate", response_model=AstroResponse)
async def calculate_astro_data(request: AstroRequest):
    """Calculate astrological data for a given location and date."""
    try:
        logger.info(f"Calculating astro data for {request.latitude}, {request.longitude} on {request.date}")
        
        # Validate coordinates
        if not -90 <= request.latitude <= 90:
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        if not -180 <= request.longitude <= 180:
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        
        # Parse date string to date object
        target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        
        # Calculate sunrise times
        sunrise, next_sunrise = get_sunrise_times(request.latitude, request.longitude, target_date)
        
        # Calculate ascendant at sunrise time
        ascendant = get_ascendant_at_time(request.latitude, request.longitude, sunrise)
        
        # Get astrological details for ascendant
        sign, sign_lord = get_sign_and_lord(ascendant)
        nakshatra, nakshatra_lord = get_nakshatra_and_lord(ascendant)
        sub_lord, sub_sub_lord = get_kp_sub_lords(ascendant)
        
        # Generate degree buckets if requested
        degree_buckets = None
        if request.include_degree_buckets:
            degree_buckets = generate_degree_buckets()
        
        return AstroResponse(
            date=request.date,
            sunrise_ist=sunrise.isoformat(),
            next_sunrise_ist=next_sunrise.isoformat(),
            latitude=request.latitude,
            longitude=request.longitude,
            ascendant_degree=round(ascendant, 3),
            ascendant_sign=sign,
            ascendant_sign_lord=sign_lord,
            ascendant_nakshatra=nakshatra,
            ascendant_nakshatra_lord=nakshatra_lord,
            ascendant_sub_lord=sub_lord,
            ascendant_sub_sub_lord=sub_sub_lord,
            degree_buckets=degree_buckets,
            success=True,
            message="Calculation completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in calculate_astro_data: {e}")
        return AstroResponse(
            date=request.date,
            sunrise_ist="",
            next_sunrise_ist="",
            latitude=request.latitude,
            longitude=request.longitude,
            ascendant_degree=0,
            ascendant_sign="",
            ascendant_sign_lord="",
            ascendant_nakshatra="",
            ascendant_nakshatra_lord="",
            ascendant_sub_lord="",
            ascendant_sub_sub_lord="",
            degree_buckets=None,
            success=False,
            message=f"Error: {str(e)}"
        )

@app.post("/calculate-range")
async def calculate_date_range(request: DateRangeRequest):
    """Calculate astrological data for a date range."""
    try:
        logger.info(f"Calculating astro data range for {request.latitude}, {request.longitude} from {request.start_date} to {request.end_date}")
        
        # Validate coordinates
        if not -90 <= request.latitude <= 90:
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        if not -180 <= request.longitude <= 180:
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        
        # Parse dates
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d").date()
        
        if start_date >= end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Calculate for current date
                sunrise, next_sunrise = get_sunrise_times(request.latitude, request.longitude, current_date)
                ascendant = get_ascendant_at_time(request.latitude, request.longitude, sunrise)
                
                sign, sign_lord = get_sign_and_lord(ascendant)
                nakshatra, nakshatra_lord = get_nakshatra_and_lord(ascendant)
                sub_lord, sub_sub_lord = get_kp_sub_lords(ascendant)
                
                results.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "sunrise_ist": sunrise.isoformat(),
                    "next_sunrise_ist": next_sunrise.isoformat(),
                    "latitude": request.latitude,
                    "longitude": request.longitude,
                    "ascendant_degree": round(ascendant, 3),
                    "ascendant_sign": sign,
                    "ascendant_sign_lord": sign_lord,
                    "ascendant_nakshatra": nakshatra,
                    "ascendant_nakshatra_lord": nakshatra_lord,
                    "ascendant_sub_lord": sub_lord,
                    "ascendant_sub_sub_lord": sub_sub_lord,
                    "success": True
                })
                
            except Exception as e:
                logger.error(f"Error calculating for date {current_date}: {e}")
                results.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "success": False,
                    "error": str(e)
                })
            
            current_date = current_date.replace(day=current_date.day + 1)
        
        return {
            "success": True,
            "message": f"Calculated data for {len(results)} dates",
            "results": results,
            "total_dates": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error in calculate_date_range: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-csv")
async def generate_csv(request: AstroRequest):
    """Generate CSV file for the given location and date."""
    try:
        logger.info(f"Generating CSV for {request.latitude}, {request.longitude} on {request.date}")
        
        # Validate coordinates
        if not -90 <= request.latitude <= 90:
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        if not -180 <= request.longitude <= 180:
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        
        # Parse date string to date object
        target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        
        # Calculate sunrise times
        sunrise, next_sunrise = get_sunrise_times(request.latitude, request.longitude, target_date)
        
        # Calculate ascendant at sunrise time
        ascendant = get_ascendant_at_time(request.latitude, request.longitude, sunrise)
        
        # Get astrological details for ascendant
        sign, sign_lord = get_sign_and_lord(ascendant)
        nakshatra, nakshatra_lord = get_nakshatra_and_lord(ascendant)
        sub_lord, sub_sub_lord = get_kp_sub_lords(ascendant)
        
        # Generate CSV rows
        rows = generate_csv_rows_for_date(
            target_date, sunrise, next_sunrise,
            request.latitude, request.longitude,
            ascendant, sign, sign_lord, nakshatra,
            nakshatra_lord, sub_lord, sub_sub_lord
        )
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filename
        output_file = os.path.join(output_dir, f"astro_data_{request.date}.csv")
        
        # Write CSV file
        write_csv_to_file(rows, output_file)
        
        return {
            "success": True,
            "message": f"CSV generated successfully",
            "output_file": output_file,
            "total_rows": len(rows)
        }
        
    except Exception as e:
        logger.error(f"Error in generate_csv: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    
    logger.info(f"Starting LBAT Desktop Backend on {host}:{port}")
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
