"""
FastAPI backend for AstroCSV web application.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to Python path to import astrocsv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrocsv.ephem import get_sunrise_times, get_ascendant_at_time
from astrocsv.mapping_library import (
    get_sign_and_lord, get_nakshatra_and_lord, get_kp_sub_lords, 
    generate_ascendant_sub_sub_lord_changes
)

app = FastAPI(
    title="AstroCSV API",
    description="REST API for astrological calculations and CSV generation",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class AstroRequest(BaseModel):
    latitude: float
    longitude: float
    date: str
    include_ascendant_changes: bool = True

class AstroResponse(BaseModel):
    date: str
    latitude: float
    longitude: float
    sunrise: str
    next_sunrise: str
    ascendant: float
    ascendant_sign: str
    ascendant_sign_lord: str
    ascendant_nakshatra: str
    ascendant_nakshatra_lord: str
    ascendant_sub_lord: str
    ascendant_sub_sub_lord: str
    ascendant_changes: Optional[List[dict]] = None
    message: str

class DegreeBucketResponse(BaseModel):
    degree: float
    date: str
    time: str
    ascendant_degree: float
    sign: str
    sign_lord: str
    nakshatra: str
    nakshatra_lord: str
    sub_lord: str
    sub_sub_lord: str
    is_sub_sub_lord_change: bool
    change_type: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AstroCSV API",
        "version": "1.0.0",
        "endpoints": {
            "/calculate": "Calculate astrological data for a location and date",
            "/ascendant-changes": "Generate ascendant-based Sub Sub Lord changes",
            "/search-astrological": "Search astrological data by criteria",
            "/health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "AstroCSV API is running"}

@app.post("/calculate", response_model=AstroResponse)
async def calculate_astro_data(request: AstroRequest):
    """
    Calculate astrological data for a given location and date.
    """
    try:
        # Validate coordinates
        if not -90 <= request.latitude <= 90:
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        if not -180 <= request.longitude <= 180:
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        
        # Parse date string to datetime object (at sunrise time)
        target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        
        # Calculate sunrise times
        sunrise, next_sunrise = get_sunrise_times(request.latitude, request.longitude, target_date)
        
        # Calculate ascendant at sunrise time
        ascendant = get_ascendant_at_time(request.latitude, request.longitude, sunrise)
        
        # Get astrological details for ascendant
        sign, sign_lord = get_sign_and_lord(ascendant)
        nakshatra, nakshatra_lord = get_nakshatra_and_lord(ascendant)
        sub_lord, sub_sub_lord = get_kp_sub_lords(ascendant)
        
        # Generate ascendant-based Sub Sub Lord changes if requested
        degree_buckets = None
        if request.include_ascendant_changes:
            # Generate changes based on ascendant Sub Sub Lord transitions
            ascendant_changes = generate_ascendant_sub_sub_lord_changes()
            degree_buckets = []
            
            for change_data in ascendant_changes:
                # Calculate the time for this change point
                # Each degree represents 4 minutes of time (24 hours / 360 degrees)
                minutes_offset = change_data['degree'] * 4  # 4 minutes per degree
                change_time = sunrise + timedelta(minutes=minutes_offset)
                
                # Determine if this is a Sub Sub Lord change
                is_sub_sub_lord_change = 'Sub Sub Lord:' in change_data['change_type']
                
                degree_buckets.append({
                    "degree": change_data['degree'],
                    "date": change_time.strftime("%Y-%m-%d"),
                    "time": change_time.strftime("%H:%M:%S"),
                    "ascendant_degree": change_data['degree'],
                    "sign": change_data['sign'],
                    "sign_lord": change_data['sign_lord'],
                    "nakshatra": change_data['nakshatra'],
                    "nakshatra_lord": change_data['nakshatra_lord'],
                    "sub_lord": change_data['sub_lord'],
                    "sub_sub_lord": change_data['sub_sub_lord'],
                    "is_sub_sub_lord_change": is_sub_sub_lord_change,
                    "change_type": change_data['change_type']
                })
        
        return AstroResponse(
            date=request.date,
            latitude=request.latitude,
            longitude=request.longitude,
            sunrise=sunrise.isoformat(),
            next_sunrise=next_sunrise.isoformat(),
            ascendant=round(ascendant, 3),
            ascendant_sign=sign,
            ascendant_sign_lord=sign_lord,
            ascendant_nakshatra=nakshatra,
            ascendant_nakshatra_lord=nakshatra_lord,
            ascendant_sub_lord=sub_lord,
            ascendant_sub_sub_lord=sub_sub_lord,
            ascendant_changes=degree_buckets,
            message="Astrological calculations completed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/ascendant-changes")
async def get_ascendant_changes():
    """
    Generate ascendant-based Sub Sub Lord changes with astrological information.
    """
    try:
        # Use current date and time for standalone endpoint
        current_datetime = datetime.now()
        
        # Generate ascendant-based sub-sub lord changes
        ascendant_changes = generate_ascendant_sub_sub_lord_changes()
        
        result = []
        for change_data in ascendant_changes:
            # Calculate the time for this change point
            # Each degree represents 4 minutes of time (24 hours / 360 degrees)
            minutes_offset = change_data['degree'] * 4  # 4 minutes per degree
            change_time = current_datetime + timedelta(minutes=minutes_offset)
            
            # Determine if this is a Sub Sub Lord change
            is_sub_sub_lord_change = 'Sub Sub Lord:' in change_data['change_type']
            
            result.append({
                "degree": change_data['degree'],
                "date": change_time.strftime("%Y-%m-%d"),
                "time": change_time.strftime("%H:%M:%S"),
                "ascendant_degree": change_data['degree'],
                "sign": change_data['sign'],
                "sign_lord": change_data['sign_lord'],
                "nakshatra": change_data['nakshatra'],
                "nakshatra_lord": change_data['nakshatra_lord'],
                "sub_lord": change_data['sub_lord'],
                "sub_sub_lord": change_data['sub_sub_lord'],
                "is_sub_sub_lord_change": is_sub_sub_lord_change,
                "change_type": change_data['change_type']
            })
        
        return {
            "total_changes": len(result),
            "ascendant_changes": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ascendant changes: {str(e)}")

@app.get("/search-astrological")
async def search_astrological(
    nakshatra: Optional[str] = None,
    nakshatra_lord: Optional[str] = None,
    sub_lord: Optional[str] = None,
    sub_sub_lord: Optional[str] = None,
    sign: Optional[str] = None,
    sign_lord: Optional[str] = None
):
    """
    Search for astrological data by various criteria.
    """
    try:
        # Generate ascendant-based sub-sub lord changes
        ascendant_changes = generate_ascendant_sub_sub_lord_changes()
        
        # Filter results based on search criteria
        filtered_results = []
        for change_data in ascendant_changes:
            # Check if this entry matches all provided search criteria
            matches = True
            
            if nakshatra and nakshatra.lower() not in change_data['nakshatra'].lower():
                matches = False
            if nakshatra_lord and nakshatra_lord.lower() not in change_data['nakshatra_lord'].lower():
                matches = False
            if sub_lord and sub_lord.lower() not in change_data['sub_lord'].lower():
                matches = False
            if sub_sub_lord and sub_sub_lord.lower() not in change_data['sub_sub_lord'].lower():
                matches = False
            if sign and sign.lower() not in change_data['sign'].lower():
                matches = False
            if sign_lord and sign_lord.lower() not in change_data['sign_lord'].lower():
                matches = False
            
            if matches:
                # Calculate the time for this change point
                # Each degree represents 4 minutes of time (24 hours / 360 degrees)
                current_datetime = datetime.now()
                minutes_offset = change_data['degree'] * 4  # 4 minutes per degree
                change_time = current_datetime + timedelta(minutes=minutes_offset)
                
                filtered_results.append({
                    "degree": change_data['degree'],
                    "date": change_time.strftime("%Y-%m-%d"),
                    "time": change_time.strftime("%H:%M:%S"),
                    "ascendant_degree": change_data['degree'],
                    "sign": change_data['sign'],
                    "sign_lord": change_data['sign_lord'],
                    "nakshatra": change_data['nakshatra'],
                    "nakshatra_lord": change_data['nakshatra_lord'],
                    "sub_lord": change_data['sub_lord'],
                    "sub_sub_lord": change_data['sub_sub_lord'],
                    "change_type": change_data['change_type']
                })
        
        return {
            "search_criteria": {
                "nakshatra": nakshatra,
                "nakshatra_lord": nakshatra_lord,
                "sub_lord": sub_lord,
                "sub_sub_lord": sub_sub_lord,
                "sign": sign,
                "sign_lord": sign_lord
            },
            "total_results": len(filtered_results),
            "results": filtered_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching astrological data: {str(e)}")

@app.get("/signs")
async def get_zodiac_signs():
    """Get all zodiac signs and their lords."""
    signs = [
        {"name": "Aries", "lord": "Mars", "degrees": "0° - 30°"},
        {"name": "Taurus", "lord": "Venus", "degrees": "30° - 60°"},
        {"name": "Gemini", "lord": "Mercury", "degrees": "60° - 90°"},
        {"name": "Cancer", "lord": "Moon", "degrees": "90° - 120°"},
        {"name": "Leo", "lord": "Sun", "degrees": "120° - 150°"},
        {"name": "Virgo", "lord": "Mercury", "degrees": "150° - 180°"},
        {"name": "Libra", "lord": "Venus", "degrees": "180° - 210°"},
        {"name": "Scorpio", "lord": "Mars", "degrees": "210° - 240°"},
        {"name": "Sagittarius", "lord": "Jupiter", "degrees": "240° - 270°"},
        {"name": "Capricorn", "lord": "Saturn", "degrees": "270° - 300°"},
        {"name": "Aquarius", "lord": "Saturn", "degrees": "300° - 330°"},
        {"name": "Pisces", "lord": "Jupiter", "degrees": "330° - 360°"}
    ]
    return {"zodiac_signs": signs}

@app.get("/nakshatras")
async def get_nakshatras():
    """Get all nakshatras and their lords."""
    nakshatras = [
        {"name": "Ashwini", "lord": "Ketu", "degrees": "0° - 13°20'"},
        {"name": "Bharani", "lord": "Venus", "degrees": "13°20' - 26°40'"},
        {"name": "Krittika", "lord": "Sun", "degrees": "26°40' - 40°"},
        {"name": "Rohini", "lord": "Moon", "degrees": "40° - 53°20'"},
        {"name": "Mrigashira", "lord": "Mars", "degrees": "53°20' - 66°40'"},
        {"name": "Ardra", "lord": "Rahu", "degrees": "66°40' - 80°"},
        {"name": "Punarvasu", "lord": "Jupiter", "degrees": "80° - 93°20'"},
        {"name": "Pushya", "lord": "Saturn", "degrees": "93°20' - 106°40'"},
        {"name": "Ashlesha", "lord": "Mercury", "degrees": "106°40' - 120°"},
        {"name": "Magha", "lord": "Ketu", "degrees": "120° - 133°20'"},
        {"name": "Purva Phalguni", "lord": "Venus", "degrees": "133°20' - 146°40'"},
        {"name": "Uttara Phalguni", "lord": "Sun", "degrees": "146°40' - 160°"},
        {"name": "Hasta", "lord": "Moon", "degrees": "160° - 173°20'"},
        {"name": "Chitra", "lord": "Mars", "degrees": "173°20' - 186°40'"},
        {"name": "Swati", "lord": "Rahu", "degrees": "186°40' - 200°"},
        {"name": "Vishakha", "lord": "Jupiter", "degrees": "200° - 213°20'"},
        {"name": "Anuradha", "lord": "Saturn", "degrees": "213°20' - 226°40'"},
        {"name": "Jyeshtha", "lord": "Mercury", "degrees": "226°40' - 240°"},
        {"name": "Mula", "lord": "Ketu", "degrees": "240° - 253°20'"},
        {"name": "Purva Ashadha", "lord": "Venus", "degrees": "253°20' - 266°40'"},
        {"name": "Uttara Ashadha", "lord": "Sun", "degrees": "266°40' - 280°"},
        {"name": "Shravana", "lord": "Moon", "degrees": "280° - 293°20'"},
        {"name": "Dhanishta", "lord": "Mars", "degrees": "293°20' - 306°40'"},
        {"name": "Shatabhisha", "lord": "Rahu", "degrees": "306°40' - 320°"},
        {"name": "Purva Bhadrapada", "lord": "Jupiter", "degrees": "320° - 333°20'"},
        {"name": "Uttara Bhadrapada", "lord": "Saturn", "degrees": "333°20' - 346°40'"},
        {"name": "Revati", "lord": "Mercury", "degrees": "346°40' - 360°"}
    ]
    return {"nakshatras": nakshatras}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
