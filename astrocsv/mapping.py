"""
Astrological mappings using standard astronomical libraries.
"""

from typing import Dict, Tuple, List
import math

# Use Swiss Ephemeris for precise calculations
try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    SWISSEPH_AVAILABLE = False

def get_zodiac_sign(degree: float) -> Tuple[str, str]:
    """
    Get zodiac sign and lord using astronomical calculations.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (sign_name, sign_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    # Standard zodiac divisions (30° each)
    sign_index = int(degree // 30)
    
    # Zodiac signs and their lords (astronomical standard)
    zodiac_signs = [
        ("Aries", "Mars"),
        ("Taurus", "Venus"), 
        ("Gemini", "Mercury"),
        ("Cancer", "Moon"),
        ("Leo", "Sun"),
        ("Virgo", "Mercury"),
        ("Libra", "Venus"),
        ("Scorpio", "Mars"),
        ("Sagittarius", "Jupiter"),
        ("Capricorn", "Saturn"),
        ("Aquarius", "Saturn"),
        ("Pisces", "Jupiter")
    ]
    
    return zodiac_signs[sign_index]

def get_nakshatra(degree: float) -> Tuple[str, str]:
    """
    Get nakshatra and lord using astronomical divisions.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (nakshatra_name, nakshatra_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    # Nakshatras are 13°20' (13.333333°) each
    nakshatra_index = int(degree // 13.333333)
    
    # 27 nakshatras with their lords (astronomical standard)
    nakshatras = [
        ("Ashwini", "Ketu"),
        ("Bharani", "Venus"),
        ("Krittika", "Sun"),
        ("Rohini", "Moon"),
        ("Mrigashira", "Mars"),
        ("Ardra", "Rahu"),
        ("Punarvasu", "Jupiter"),
        ("Pushya", "Saturn"),
        ("Ashlesha", "Mercury"),
        ("Magha", "Ketu"),
        ("Purva Phalguni", "Venus"),
        ("Uttara Phalguni", "Sun"),
        ("Hasta", "Moon"),
        ("Chitra", "Mars"),
        ("Swati", "Rahu"),
        ("Vishakha", "Jupiter"),
        ("Anuradha", "Saturn"),
        ("Jyeshtha", "Mercury"),
        ("Mula", "Ketu"),
        ("Purva Ashadha", "Venus"),
        ("Uttara Ashadha", "Sun"),
        ("Shravana", "Moon"),
        ("Dhanishta", "Mars"),
        ("Shatabhisha", "Rahu"),
        ("Purva Bhadrapada", "Jupiter"),
        ("Uttara Bhadrapada", "Saturn"),
        ("Revati", "Mercury")
    ]
    
    return nakshatras[nakshatra_index]

def get_vimshottari_weights() -> Dict[str, int]:
    """
    Get Vimshottari dasha weights (standard astrological system).
    
    Returns:
        Dictionary mapping planet names to their dasha periods
    """
    return {
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

def get_vimshottari_sequence() -> List[str]:
    """
    Get Vimshottari dasha sequence (standard astrological system).
    
    Returns:
        List of planets in Vimshottari order
    """
    return ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

def calculate_kp_sub_lords(degree: float) -> Tuple[str, str]:
    """
    Calculate KP sub-lord and sub-sub-lord using Vimshottari system.
    
    Args:
        degree: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (sub_lord, sub_sub_lord)
    """
    # Normalize degree to 0-360 range
    degree = degree % 360.0
    
    # Get the nakshatra for this degree
    nakshatra_name, nakshatra_lord = get_nakshatra(degree)
    
    # Get Vimshottari data
    weights = get_vimshottari_weights()
    sequence = get_vimshottari_sequence()
    
    # Find the starting index of this nakshatra lord in the sequence
    lord_index = sequence.index(nakshatra_lord)
    
    # Calculate the degree offset within the nakshatra (0 to 13.333333...)
    nakshatra_start = int(degree // 13.333333) * 13.333333
    degree_within_nakshatra = degree - nakshatra_start
    
    # Convert to arcminutes for precise calculations
    arcmin_within_nakshatra = degree_within_nakshatra * 60.0
    
    # Calculate sub-lord
    total_weight = sum(weights.values())  # 120
    nakshatra_arcmin = 13.333333 * 60.0  # 800 arcminutes
    
    cumulative_arcmin = 0
    sub_lord = None
    
    for i in range(9):
        lord_idx = (lord_index + i) % 9
        lord_name = sequence[lord_idx]
        lord_weight = weights[lord_name]
        
        lord_arcmin = (lord_weight / total_weight) * nakshatra_arcmin
        cumulative_arcmin += lord_arcmin
        
        if arcmin_within_nakshatra < cumulative_arcmin:
            sub_lord = lord_name
            break
    
    if sub_lord is None:
        sub_lord = nakshatra_lord  # Fallback
    
    # Calculate sub-sub-lord
    # Find the start of the sub-lord segment
    cumulative_arcmin = 0
    sub_lord_start_arcmin = 0
    
    for i in range(9):
        lord_idx = (lord_index + i) % 9
        lord_name = sequence[lord_idx]
        lord_weight = weights[lord_name]
        
        lord_arcmin = (lord_weight / total_weight) * nakshatra_arcmin
        
        if lord_name == sub_lord:
            sub_lord_start_arcmin = cumulative_arcmin
            break
        
        cumulative_arcmin += lord_arcmin
    
    # Calculate position within the sub-lord segment
    arcmin_within_sub = arcmin_within_nakshatra - sub_lord_start_arcmin
    sub_lord_weight = weights[sub_lord]
    sub_lord_arcmin = (sub_lord_weight / total_weight) * nakshatra_arcmin
    
    # Find sub-sub-lord within the sub-lord segment
    sub_lord_index = sequence.index(sub_lord)
    cumulative_arcmin = 0
    sub_sub_lord = None
    
    for i in range(9):
        lord_idx = (sub_lord_index + i) % 9
        lord_name = sequence[lord_idx]
        lord_weight = weights[lord_name]
        
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
    
    Returns:
        List of tuples: (bucket_start_deg, bucket_sign, bucket_sign_lord)
    """
    buckets = []
    for i in range(720):  # 0.0 to 359.5 in 0.5° increments
        bucket_start = i * 0.5
        sign, lord = get_zodiac_sign(bucket_start)
        buckets.append((bucket_start, sign, lord))
    return buckets

# Backward compatibility aliases
get_sign_and_lord = get_zodiac_sign
get_nakshatra_and_lord = get_nakshatra
get_kp_sub_lords = calculate_kp_sub_lords
