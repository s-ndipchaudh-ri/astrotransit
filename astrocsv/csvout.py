"""
CSV output generation with schema enforcement and proper ordering.
"""

import pandas as pd
from datetime import datetime, date
from typing import List, Dict, Any
from .mapping import generate_degree_buckets

# CSV column order as specified in requirements
CSV_COLUMNS = [
    "row_type",
    "date_ist",
    "sunrise_ist",
    "next_sunrise_ist",
    "location_lat",
    "location_lon",
    "asc_abs_deg",
    "asc_sign",
    "asc_sign_lord",
    "asc_nakshatra",
    "asc_nakshatra_lord",
    "asc_sub_lord",
    "asc_sub_sub_lord",
    "bucket_start_deg",
    "bucket_sign",
    "bucket_sign_lord"
]

def create_ascendant_row(
    date_ist: date,
    sunrise_ist: datetime,
    next_sunrise_ist: datetime,
    lat: float,
    lon: float,
    asc_abs_deg: float,
    asc_sign: str,
    asc_sign_lord: str,
    asc_nakshatra: str,
    asc_nakshatra_lord: str,
    asc_sub_lord: str,
    asc_sub_sub_lord: str
) -> Dict[str, Any]:
    """
    Create a row for ascendant at sunrise.
    
    Args:
        date_ist: Date in IST
        sunrise_ist: Sunrise time in IST
        next_sunrise_ist: Next sunrise time in IST
        lat: Latitude
        lon: Longitude
        asc_abs_deg: Ascendant absolute degree
        asc_sign: Ascendant sign
        asc_sign_lord: Ascendant sign lord
        asc_nakshatra: Ascendant nakshatra
        asc_nakshatra_lord: Ascendant nakshatra lord
        asc_sub_lord: Ascendant KP sub-lord
        asc_sub_sub_lord: Ascendant KP sub-sub-lord
        
    Returns:
        Dictionary representing the row
    """
    return {
        "row_type": "ascendant_at_sunrise",
        "date_ist": date_ist.strftime("%Y-%m-%d"),
        "sunrise_ist": sunrise_ist.isoformat(),
        "next_sunrise_ist": next_sunrise_ist.isoformat(),
        "location_lat": round(lat, 6),
        "location_lon": round(lon, 6),
        "asc_abs_deg": round(asc_abs_deg, 3),
        "asc_sign": asc_sign,
        "asc_sign_lord": asc_sign_lord,
        "asc_nakshatra": asc_nakshatra,
        "asc_nakshatra_lord": asc_nakshatra_lord,
        "asc_sub_lord": asc_sub_lord,
        "asc_sub_sub_lord": asc_sub_sub_lord,
        "bucket_start_deg": "",
        "bucket_sign": "",
        "bucket_sign_lord": ""
    }

def create_bucket_row(
    date_ist: date,
    sunrise_ist: datetime,
    next_sunrise_ist: datetime,
    lat: float,
    lon: float,
    bucket_start_deg: float,
    bucket_sign: str,
    bucket_sign_lord: str
) -> Dict[str, Any]:
    """
    Create a row for a degree bucket.
    
    Args:
        date_ist: Date in IST
        sunrise_ist: Sunrise time in IST
        next_sunrise_ist: Next sunrise time in IST
        lat: Latitude
        lon: Longitude
        bucket_start_deg: Bucket start degree
        bucket_sign: Bucket sign
        bucket_sign_lord: Bucket sign lord
        
    Returns:
        Dictionary representing the row
    """
    return {
        "row_type": "degree_bucket",
        "date_ist": date_ist.strftime("%Y-%m-%d"),
        "sunrise_ist": sunrise_ist.isoformat(),
        "next_sunrise_ist": next_sunrise_ist.isoformat(),
        "location_lat": round(lat, 6),
        "location_lon": round(lon, 6),
        "asc_abs_deg": "",
        "asc_sign": "",
        "asc_sign_lord": "",
        "asc_nakshatra": "",
        "asc_nakshatra_lord": "",
        "asc_sub_lord": "",
        "asc_sub_sub_lord": "",
        "bucket_start_deg": round(bucket_start_deg, 1),
        "bucket_sign": bucket_sign,
        "bucket_sign_lord": bucket_sign_lord
    }

def generate_csv_rows_for_date(
    date_ist: date,
    sunrise_ist: datetime,
    next_sunrise_ist: datetime,
    lat: float,
    lon: float,
    asc_abs_deg: float,
    asc_sign: str,
    asc_sign_lord: str,
    asc_nakshatra: str,
    asc_nakshatra_lord: str,
    asc_sub_lord: str,
    asc_sub_sub_lord: str
) -> List[Dict[str, Any]]:
    """
    Generate all CSV rows for a single date.
    
    Args:
        date_ist: Date in IST
        sunrise_ist: Sunrise time in IST
        next_sunrise_ist: Next sunrise time in IST
        lat: Latitude
        lon: Longitude
        asc_abs_deg: Ascendant absolute degree
        asc_sign: Ascendant sign
        asc_sign_lord: Ascendant sign lord
        asc_nakshatra: Ascendant nakshatra
        asc_nakshatra_lord: Ascendant nakshatra lord
        asc_sub_lord: Ascendant KP sub-lord
        asc_sub_sub_lord: Ascendant KP sub-sub-lord
        
    Returns:
        List of dictionaries representing all rows for the date
    """
    rows = []
    
    # Add ascendant row
    ascendant_row = create_ascendant_row(
        date_ist, sunrise_ist, next_sunrise_ist, lat, lon,
        asc_abs_deg, asc_sign, asc_sign_lord, asc_nakshatra,
        asc_nakshatra_lord, asc_sub_lord, asc_sub_sub_lord
    )
    rows.append(ascendant_row)
    
    # Add 720 bucket rows (0.5° grid)
    degree_buckets = generate_degree_buckets()
    for bucket_start_deg, bucket_sign, bucket_sign_lord in degree_buckets:
        bucket_row = create_bucket_row(
            date_ist, sunrise_ist, next_sunrise_ist, lat, lon,
            bucket_start_deg, bucket_sign, bucket_sign_lord
        )
        rows.append(bucket_row)
    
    return rows

def write_csv_to_file(rows: List[Dict[str, Any]], output_file: str) -> None:
    """
    Write rows to CSV file with proper schema enforcement.
    
    Args:
        rows: List of row dictionaries
        output_file: Path to output CSV file
    """
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Ensure columns are in correct order
    df = df[CSV_COLUMNS]
    
    # Write to CSV without index
    df.to_csv(output_file, index=False, float_format='%.3f')

def write_csv_to_stdout(rows: List[Dict[str, Any]]) -> None:
    """
    Write rows to stdout with proper schema enforcement.
    
    Args:
        rows: List of row dictionaries
    """
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Ensure columns are in correct order
    df = df[CSV_COLUMNS]
    
    # Write to stdout without index
    df.to_csv('-', index=False, float_format='%.3f')
