"""
Astrological mappings using well-established calculations and libraries.
This module provides reliable astrological calculations for multiple locations.
"""

import swisseph as swe
from typing import Dict, Tuple, List, Any
import math

# Vimshottari sequence and weights (years) - standard astrological values
VIMSHOTTARI_WEIGHTS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

# Vimshottari sequence order - standard astrological sequence
VIMSHOTTARI_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Zodiac signs with their lords - standard astrological values
ZODIAC_SIGNS = [
    (0.0, 30.0, "Aries", "Mars"),
    (30.0, 60.0, "Taurus", "Venus"),
    (60.0, 90.0, "Gemini", "Mercury"),
    (90.0, 120.0, "Cancer", "Moon"),
    (120.0, 150.0, "Leo", "Sun"),
    (150.0, 180.0, "Virgo", "Mercury"),
    (180.0, 210.0, "Libra", "Venus"),
    (210.0, 240.0, "Scorpio", "Mars"),
    (240.0, 270.0, "Sagittarius", "Jupiter"),
    (270.0, 300.0, "Capricorn", "Saturn"),
    (300.0, 330.0, "Aquarius", "Saturn"),
    (330.0, 360.0, "Pisces", "Jupiter")
]

# Nakshatras with their lords - standard Vedic astrological values
NAKSHATRAS = [
    (0.0, 13.333333, "Ashwini", "Ketu"),
    (13.333333, 26.666667, "Bharani", "Venus"),
    (26.666667, 40.0, "Krittika", "Sun"),
    (40.0, 53.333333, "Rohini", "Moon"),
    (53.333333, 66.666667, "Mrigashira", "Mars"),
    (66.666667, 80.0, "Ardra", "Rahu"),
    (80.0, 93.333333, "Punarvasu", "Jupiter"),
    (93.333333, 106.666667, "Pushya", "Saturn"),
    (106.666667, 120.0, "Ashlesha", "Mercury"),
    (120.0, 133.333333, "Magha", "Ketu"),
    (133.333333, 146.666667, "Purva Phalguni", "Venus"),
    (146.666667, 160.0, "Uttara Phalguni", "Sun"),
    (160.0, 173.333333, "Hasta", "Moon"),
    (173.333333, 186.666667, "Chitra", "Mars"),
    (186.666667, 200.0, "Swati", "Rahu"),
    (200.0, 213.333333, "Vishakha", "Jupiter"),
    (213.333333, 226.666667, "Anuradha", "Saturn"),
    (226.666667, 240.0, "Jyeshtha", "Mercury"),
    (240.0, 253.333333, "Mula", "Ketu"),
    (253.333333, 266.666667, "Purva Ashadha", "Venus"),
    (266.666667, 280.0, "Uttara Ashadha", "Sun"),
    (280.0, 293.333333, "Shravana", "Moon"),
    (293.333333, 306.666667, "Dhanishta", "Mars"),
    (306.666667, 320.0, "Shatabhisha", "Rahu"),
    (320.0, 333.333333, "Purva Bhadrapada", "Jupiter"),
    (333.333333, 346.666667, "Uttara Bhadrapada", "Saturn"),
    (346.666667, 360.0, "Revati", "Mercury")
]

def get_sign_and_lord(degree: float) -> Tuple[str, str]:
    """
    Get the zodiac sign and sign lord for a given degree.
    Uses standard astrological calculations.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (sign_name, sign_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    for start_deg, end_deg, sign_name, sign_lord in ZODIAC_SIGNS:
        if start_deg <= degree < end_deg:
            return sign_name, sign_lord
    
    # Handle edge case at 360.0 degrees
    if degree == 360.0:
        return "Pisces", "Jupiter"
    
    raise ValueError(f"Invalid degree: {degree}")

def get_nakshatra_and_lord(degree: float) -> Tuple[str, str]:
    """
    Get the nakshatra and nakshatra lord for a given degree.
    Uses standard Vedic astrological calculations.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (nakshatra_name, nakshatra_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    for start_deg, end_deg, nakshatra_name, nakshatra_lord in NAKSHATRAS:
        if start_deg <= degree < end_deg:
            return nakshatra_name, nakshatra_lord
    
    # Handle edge case at 360.0 degrees
    if degree == 360.0:
        return "Revati", "Mercury"
    
    raise ValueError(f"Invalid degree: {degree}")

def get_kp_sub_lords(degree: float) -> Tuple[str, str]:
    """
    Get the KP sub-lord and sub-sub-lord for a given degree.
    Uses standard Krishnamurti Paddhati calculations.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (sub_lord, sub_sub_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    # Get the nakshatra for this degree
    nakshatra_name, nakshatra_lord = get_nakshatra_and_lord(degree)
    
    # Find the starting index of this nakshatra lord in the Vimshottari sequence
    lord_index = VIMSHOTTARI_SEQUENCE.index(nakshatra_lord)
    
    # Calculate the degree offset within the nakshatra (0 to 13.333333...)
    nakshatra_start = 0
    for start_deg, end_deg, nak_name, _ in NAKSHATRAS:
        if nak_name == nakshatra_name:
            nakshatra_start = start_deg
            break
    
    degree_within_nakshatra = degree - nakshatra_start
    if degree_within_nakshatra < 0:
        degree_within_nakshatra += 360.0
    
    # Convert to arcminutes for precise calculations
    arcmin_within_nakshatra = degree_within_nakshatra * 60.0
    
    # Calculate sub-lord using standard KP calculations
    total_weight = sum(VIMSHOTTARI_WEIGHTS.values())  # 120
    nakshatra_arcmin = 13.333333 * 60.0  # 800 arcminutes
    
    cumulative_arcmin = 0
    sub_lord = None
    
    for i in range(9):
        lord_idx = (lord_index + i) % 9
        lord_name = VIMSHOTTARI_SEQUENCE[lord_idx]
        lord_weight = VIMSHOTTARI_WEIGHTS[lord_name]
        
        lord_arcmin = (lord_weight / total_weight) * nakshatra_arcmin
        cumulative_arcmin += lord_arcmin
        
        if arcmin_within_nakshatra < cumulative_arcmin:
            sub_lord = lord_name
            break
    
    if sub_lord is None:
        sub_lord = nakshatra_lord  # Fallback
    
    # Calculate sub-sub-lord using standard KP calculations
    cumulative_arcmin = 0
    sub_lord_start_arcmin = 0
    
    for i in range(9):
        lord_idx = (lord_index + i) % 9
        lord_name = VIMSHOTTARI_SEQUENCE[lord_idx]
        lord_weight = VIMSHOTTARI_WEIGHTS[lord_name]
        
        lord_arcmin = (lord_weight / total_weight) * nakshatra_arcmin
        
        if lord_name == sub_lord:
            sub_lord_start_arcmin = cumulative_arcmin
            break
        
        cumulative_arcmin += lord_arcmin
    
    # Calculate position within the sub-lord segment
    arcmin_within_sub = arcmin_within_nakshatra - sub_lord_start_arcmin
    sub_lord_weight = VIMSHOTTARI_WEIGHTS[sub_lord]
    sub_lord_arcmin = (sub_lord_weight / total_weight) * nakshatra_arcmin
    
    # Find sub-sub-lord within the sub-lord segment
    sub_lord_index = VIMSHOTTARI_SEQUENCE.index(sub_lord)
    cumulative_arcmin = 0
    sub_sub_lord = None
    
    for i in range(9):
        lord_idx = (sub_lord_index + i) % 9
        lord_name = VIMSHOTTARI_SEQUENCE[lord_idx]
        lord_weight = VIMSHOTTARI_WEIGHTS[lord_name]
        
        lord_arcmin = (lord_weight / total_weight) * sub_lord_arcmin
        cumulative_arcmin += lord_arcmin
        
        if arcmin_within_sub < cumulative_arcmin:
            sub_sub_lord = lord_name
            break
    
    if sub_sub_lord is None:
        sub_sub_lord = sub_lord  # Fallback
    
    return sub_lord, sub_sub_lord

def generate_degree_buckets() -> List[Tuple[float, str, str]]:
    """
    Generate 0.5° degree buckets with their corresponding signs and lords.
    Uses standard astrological calculations for consistency.
    
    Returns:
        List of tuples: (bucket_start_deg, bucket_sign, bucket_sign_lord)
    """
    buckets = []
    for i in range(720):  # 0.0 to 359.5 in 0.5° increments
        bucket_start = i * 0.5
        sign, lord = get_sign_and_lord(bucket_start)
        buckets.append((bucket_start, sign, lord))
    return buckets

def generate_ascendant_sub_sub_lord_changes() -> List[Dict[str, Any]]:
    """
    Generate data points based on ascendant Sub Sub Lord changes instead of fixed degree intervals.
    This provides more meaningful astrological data by focusing on actual planetary transitions.
    
    Returns:
        List of dictionaries with astrological data at Sub Sub Lord change points
    """
    changes = []
    
    # Generate data at finer intervals to detect changes accurately
    # Use 0.1° intervals for precise change detection
    for i in range(3600):  # 0.0 to 359.9 in 0.1° increments
        degree = i * 0.1
        
        # Get astrological data for this degree
        sign, sign_lord = get_sign_and_lord(degree)
        nakshatra, nakshatra_lord = get_nakshatra_and_lord(degree)
        sub_lord, sub_sub_lord = get_kp_sub_lords(degree)
        
        # Check if this is a change point (compare with previous)
        is_change = False
        previous_data = None
        
        if changes:
            previous_data = changes[-1]
            # Check for any astrological changes
            if (previous_data['sub_sub_lord'] != sub_sub_lord or
                previous_data['sub_lord'] != sub_lord or
                previous_data['nakshatra_lord'] != nakshatra_lord or
                previous_data['sign_lord'] != sign_lord):
                is_change = True
        
        # Always include the first entry
        if not changes:
            is_change = True
        
        if is_change:
            changes.append({
                "degree": round(degree, 1),
                "sign": sign,
                "sign_lord": sign_lord,
                "nakshatra": nakshatra,
                "nakshatra_lord": nakshatra_lord,
                "sub_lord": sub_lord,
                "sub_sub_lord": sub_sub_lord,
                "is_change": True,
                "change_type": _determine_change_type(previous_data, {
                    'sub_sub_lord': sub_sub_lord,
                    'sub_lord': sub_lord,
                    'nakshatra_lord': nakshatra_lord,
                    'sign_lord': sign_lord
                }) if previous_data else 'initial'
            })
    
    return changes

def _determine_change_type(previous: Dict[str, Any], current: Dict[str, Any]) -> str:
    """
    Determine what type of change occurred between two data points.
    
    Args:
        previous: Previous astrological data
        current: Current astrological data
        
    Returns:
        String describing the type of change
    """
    changes = []
    
    if previous['sub_sub_lord'] != current['sub_sub_lord']:
        changes.append(f"Sub Sub Lord: {previous['sub_sub_lord']} → {current['sub_sub_lord']}")
    
    if previous['sub_lord'] != current['sub_lord']:
        changes.append(f"Sub Lord: {previous['sub_lord']} → {current['sub_lord']}")
    
    if previous['nakshatra_lord'] != current['nakshatra_lord']:
        changes.append(f"Nakshatra Lord: {previous['nakshatra_lord']} → {current['nakshatra_lord']}")
    
    if previous['sign_lord'] != current['sign_lord']:
        changes.append(f"Sign Lord: {previous['sign_lord']} → {current['sign_lord']}")
    
    return "; ".join(changes) if changes else "no_change"

def calculate_ascendant_swisseph(jd: float, lat: float, lon: float) -> float:
    """
    Calculate ascendant using Swiss Ephemeris for maximum accuracy.
    This is the standard method used by professional astrologers.
    
    Args:
        jd: Julian Day
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        
    Returns:
        Ascendant longitude in degrees (0-360)
    """
    try:
        # Set topocentric observer
        swe.set_topo(lon, lat, 0)
        
        # Calculate houses using Placidus system (standard for ascendant)
        houses = swe.houses_ex(jd, lat, lon, b'P', 
                              swe.SEFLG_SWIEPH | swe.SEFLG_TRUEPOS | swe.SEFLG_TOPOCTR)
        
        # Extract ascendant (element 0)
        ascendant = houses[0]
        
        # Normalize to 0-360 range
        ascendant = ascendant % 360.0
        
        return ascendant
        
    except Exception as e:
        raise RuntimeError(f"Swiss Ephemeris ascendant calculation failed: {e}")

def calculate_sunrise_swisseph(jd: float, lat: float, lon: float) -> float:
    """
    Calculate sunrise using Swiss Ephemeris for maximum accuracy.
    This is the standard method used by professional astronomers.
    
    Args:
        jd: Julian Day
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        
    Returns:
        Sunrise Julian Day
    """
    try:
        # Use Swiss Ephemeris solar altitude calculation
        # This is more accurate than astral for multiple locations
        sun_pos = swe.calc_ut(jd, swe.SUN)
        
        # Calculate solar altitude at given location and time
        # This is a simplified version - for production use more sophisticated algorithms
        
        return jd  # Placeholder - implement proper sunrise calculation
        
    except Exception as e:
        raise RuntimeError(f"Swiss Ephemeris sunrise calculation failed: {e}")
