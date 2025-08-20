"""
Ephemeris calculations for sunrise and ascendant using Swiss Ephemeris and astral.
"""

import swisseph as swe
from astral import LocationInfo
from astral.sun import sunrise
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from typing import Tuple
import math

# IST timezone
IST = ZoneInfo("Asia/Kolkata")

def setup_swiss_ephemeris():
    """
    Setup Swiss Ephemeris with topocentric observer.
    """
    # Set ephemeris path (default to ./ephe/ directory)
    swe.set_ephe_path("./ephe/")
    
    # Set topocentric observer (altitude 0m by default)
    # This will be set per calculation in get_ascendant_at_time

def get_sunrise_times(lat: float, lon: float, target_date: date) -> Tuple[datetime, datetime]:
    """
    Get sunrise times for a given date and location.
    
    Args:
        lat: Latitude in decimal degrees (positive north)
        lon: Longitude in decimal degrees (positive east)
        target_date: Date to calculate sunrise for
        
    Returns:
        Tuple of (sunrise_ist, next_sunrise_ist) as datetime objects in IST
    """
    # Create location info
    location = LocationInfo(
        latitude=lat,
        longitude=lon,
        timezone=IST,
        name="Location"
    )
    
    try:
        # Get sunrise for target date
        sunrise_time = sunrise(location.observer, date=target_date)
        sunrise_ist = sunrise_time.astimezone(IST)
        
        # Get sunrise for next day
        next_date = target_date + timedelta(days=1)
        next_sunrise_time = sunrise(location.observer, date=next_date)
        next_sunrise_ist = next_sunrise_time.astimezone(IST)
        
        return sunrise_ist, next_sunrise_ist
        
    except Exception as e:
        # Fallback calculation using Swiss Ephemeris
        return _fallback_sunrise_calculation(lat, lon, target_date)

def _fallback_sunrise_calculation(lat: float, lon: float, target_date: date) -> Tuple[datetime, datetime]:
    """
    Fallback sunrise calculation using Swiss Ephemeris.
    
    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        target_date: Date to calculate sunrise for
        
    Returns:
        Tuple of (sunrise_ist, next_sunrise_ist) as datetime objects in IST
    """
    # Convert date to Julian Day at 00:00 IST
    ist_midnight = datetime.combine(target_date, datetime.min.time(), tzinfo=IST)
    utc_midnight = ist_midnight.astimezone(ZoneInfo("UTC"))
    
    # Calculate Julian Day
    jd_utc = _datetime_to_julian_day(utc_midnight)
    
    # Search for sunrise (solar altitude = 0 with refraction)
    sunrise_jd = _find_solar_altitude_root(jd_utc, lat, lon, 0.0, search_forward=True)
    next_sunrise_jd = _find_solar_altitude_root(jd_utc + 1.0, lat, lon, 0.0, search_forward=True)
    
    # Convert back to datetime
    sunrise_utc = _julian_day_to_datetime(sunrise_jd)
    next_sunrise_utc = _julian_day_to_datetime(next_sunrise_jd)
    
    # Convert to IST
    sunrise_ist = sunrise_utc.astimezone(IST)
    next_sunrise_ist = next_sunrise_utc.astimezone(IST)
    
    return sunrise_ist, next_sunrise_ist

def _find_solar_altitude_root(jd_start: float, lat: float, lon: float, target_altitude: float, search_forward: bool = True) -> float:
    """
    Find the Julian Day when solar altitude equals target_altitude.
    
    Args:
        jd_start: Starting Julian Day
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        target_altitude: Target altitude in degrees
        search_forward: If True, search forward in time
        
    Returns:
        Julian Day when solar altitude equals target_altitude
    """
    # Use binary search to find the root
    jd_low = jd_start
    jd_high = jd_start + (1.0 if search_forward else -1.0)
    
    tolerance = 1e-6  # 1 second tolerance
    
    while abs(jd_high - jd_low) > tolerance:
        jd_mid = (jd_low + jd_high) / 2.0
        
        # Calculate solar altitude at jd_mid
        altitude = _calculate_solar_altitude(jd_mid, lat, lon)
        
        if abs(altitude - target_altitude) < 0.001:  # 0.001 degree tolerance
            return jd_mid
        elif altitude > target_altitude:
            if search_forward:
                jd_low = jd_mid
            else:
                jd_high = jd_mid
        else:
            if search_forward:
                jd_high = jd_mid
            else:
                jd_low = jd_mid
    
    return (jd_low + jd_high) / 2.0

def _calculate_solar_altitude(jd: float, lat: float, lon: float) -> float:
    """
    Calculate solar altitude at given Julian Day and location.
    
    Args:
        jd: Julian Day
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        
    Returns:
        Solar altitude in degrees
    """
    # Get solar position
    sun_pos = swe.calc_ut(jd, swe.SUN)
    sun_ra = sun_pos[0][0]  # Right Ascension
    sun_dec = sun_pos[0][1]  # Declination
    
    # Convert to altitude
    # This is a simplified calculation - for production use, consider using swe.azalt()
    lst = _julian_day_to_lst(jd, lon)
    hour_angle = lst - sun_ra
    
    # Convert to radians
    lat_rad = math.radians(lat)
    dec_rad = math.radians(sun_dec)
    ha_rad = math.radians(hour_angle * 15)  # Convert hours to degrees
    
    # Calculate altitude
    sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
               math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
    altitude = math.degrees(math.asin(sin_alt))
    
    # Apply refraction (simplified)
    if altitude > -0.833:  # Above horizon
        altitude += 0.1594 + 0.0196 * altitude + 0.00002 * altitude * altitude
    
    return altitude

def _julian_day_to_lst(jd: float, lon: float) -> float:
    """
    Convert Julian Day to Local Sidereal Time.
    
    Args:
        jd: Julian Day
        lon: Longitude in decimal degrees
        
    Returns:
        Local Sidereal Time in hours
    """
    # Calculate Greenwich Sidereal Time
    t = (jd - 2451545.0) / 36525.0
    gst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000.0
    
    # Convert to hours and normalize
    gst = (gst % 360) / 15.0
    
    # Add longitude correction
    lst = gst + lon / 15.0
    
    # Normalize to 0-24 range
    lst = lst % 24.0
    
    return lst

def _datetime_to_julian_day(dt: datetime) -> float:
    """
    Convert datetime to Julian Day.
    
    Args:
        dt: datetime object
        
    Returns:
        Julian Day as float
    """
    # Convert to UTC if not already
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    elif dt.tzinfo != ZoneInfo("UTC"):
        dt = dt.astimezone(ZoneInfo("UTC"))
    
    # Extract components
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    
    # Convert to Julian Day
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    
    # Add time component
    jd += hour / 24.0 + minute / 1440.0 + second / 86400.0
    
    return jd

def _julian_day_to_datetime(jd: float) -> datetime:
    """
    Convert Julian Day to datetime.
    
    Args:
        jd: Julian Day as float
        
    Returns:
        datetime object in UTC
    """
    # Extract date part
    jd_int = int(jd + 0.5)
    
    # Convert to Gregorian date
    f = jd_int + 1401 + (((4 * jd_int + 274277) // 146097) * 3) // 4 - 38
    e = 4 * f + 3
    g = (e % 1461) // 4
    h = 5 * g + 2
    day = (h % 153) // 5 + 1
    month = (h // 153 + 2) % 12 + 1
    year = e // 1461 - 4716 + (12 + 2 - month) // 12
    
    # Extract time part
    time_fraction = jd - jd_int + 0.5
    hour = int(time_fraction * 24)
    minute = int((time_fraction * 24 - hour) * 60)
    second = int(((time_fraction * 24 - hour) * 60 - minute) * 60)
    
    return datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo("UTC"))

def get_ascendant_at_time(lat: float, lon: float, dt: datetime) -> float:
    """
    Calculate the ascendant (Lagna) at a given time and location.
    
    Args:
        lat: Latitude in decimal degrees (positive north)
        lon: Longitude in decimal degrees (positive east)
        dt: datetime object (will be converted to IST if needed)
        
    Returns:
        Ascendant longitude in degrees (0-360)
    """
    # Convert to IST if not already
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    elif dt.tzinfo != IST:
        dt = dt.astimezone(IST)
    
    # Convert to UTC for Swiss Ephemeris
    utc_dt = dt.astimezone(ZoneInfo("UTC"))
    
    # Convert to Julian Day
    jd_ut = _datetime_to_julian_day(utc_dt)
    
    # Set topocentric observer
    swe.set_topo(lon, lat, 0)  # altitude 0m
    
    # Calculate houses (ascendant)
    # Use Placidus system, but for ascendant the system doesn't matter
    houses_result = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    
    # houses_ex returns (cusps, ascmc) where cusps is the first element
    cusps = houses_result[0]
    
    # Extract ascendant (element 0 of cusps)
    ascendant = cusps[0]
    
    # Normalize to 0-360 range
    ascendant = ascendant % 360.0
    
    return ascendant
