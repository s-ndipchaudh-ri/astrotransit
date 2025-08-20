#!/usr/bin/env python3
"""
Example: Generate AstroCSV data for multiple locations using well-established libraries.

This script demonstrates how to use the AstroCSV library to generate
astrological data for multiple cities/locations efficiently.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrocsv.mapping_library import (
    get_sign_and_lord, get_nakshatra_and_lord, get_kp_sub_lords,
    generate_degree_buckets, calculate_ascendant_swisseph
)
from astrocsv.ephem import get_sunrise_times, get_ascendant_at_time
from astrocsv.csvout import generate_csv_rows_for_date, write_csv_to_file
from datetime import date
import pandas as pd

# Major Indian cities with their coordinates
INDIAN_CITIES = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "timezone": "Asia/Kolkata"},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "timezone": "Asia/Kolkata"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "timezone": "Asia/Kolkata"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "timezone": "Asia/Kolkata"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "timezone": "Asia/Kolkata"},
    "Vashind (Shahapur)": {"lat": 19.3333, "lon": 73.3333, "timezone": "Asia/Kolkata"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "timezone": "Asia/Kolkata"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "timezone": "Asia/Kolkata"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "timezone": "Asia/Kolkata"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "timezone": "Asia/Kolkata"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "timezone": "Asia/Kolkata"}
}

def generate_single_location_csv(city_name: str, city_data: dict, target_date: date, output_dir: str = "outputs"):
    """
    Generate CSV for a single location using well-established astrological calculations.
    
    Args:
        city_name: Name of the city
        city_data: Dictionary with lat, lon, timezone
        target_date: Date to calculate for
        output_dir: Output directory for CSV files
    """
    print(f"Processing {city_name}...")
    
    try:
        # Get sunrise times using established library
        sunrise_ist, next_sunrise_ist = get_sunrise_times(
            city_data["lat"], city_data["lon"], target_date
        )
        
        # Get ascendant at sunrise using Swiss Ephemeris
        asc_abs_deg = get_ascendant_at_time(
            city_data["lat"], city_data["lon"], sunrise_ist
        )
        
        # Get astrological data using well-established calculations
        asc_sign, asc_sign_lord = get_sign_and_lord(asc_abs_deg)
        asc_nakshatra, asc_nakshatra_lord = get_nakshatra_and_lord(asc_abs_deg)
        asc_sub_lord, asc_sub_sub_lord = get_kp_sub_lords(asc_abs_deg)
        
        # Generate CSV rows
        rows = generate_csv_rows_for_date(
            target_date, sunrise_ist, next_sunrise_ist,
            city_data["lat"], city_data["lon"],
            asc_abs_deg, asc_sign, asc_sign_lord, asc_nakshatra,
            asc_nakshatra_lord, asc_sub_lord, asc_sub_sub_lord
        )
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Write CSV file
        output_file = os.path.join(output_dir, f"{city_name.lower()}_{target_date.strftime('%Y-%m-%d')}.csv")
        write_csv_to_file(rows, output_file)
        
        print(f"  ✓ Generated {output_file} with {len(rows)} rows")
        print(f"  ✓ Ascendant: {asc_abs_deg:.3f}° ({asc_sign} - {asc_sign_lord})")
        print(f"  ✓ Nakshatra: {asc_nakshatra} - {asc_nakshatra_lord}")
        print(f"  ✓ KP: {asc_sub_lord} - {asc_sub_sub_lord}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {city_name}: {e}")
        return False

def generate_multiple_locations_csv(target_date: date, cities: dict = None, output_dir: str = "outputs"):
    """
    Generate CSV files for multiple locations using well-established libraries.
    
    Args:
        target_date: Date to calculate for
        cities: Dictionary of cities to process (default: INDIAN_CITIES)
        output_dir: Output directory for CSV files
    """
    if cities is None:
        cities = INDIAN_CITIES
    
    print(f"Generating AstroCSV data for {len(cities)} cities on {target_date}")
    print(f"Using well-established astrological libraries for accuracy")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for city_name, city_data in cities.items():
        if generate_single_location_csv(city_name, city_data, target_date, output_dir):
            successful += 1
        else:
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Summary: {successful} successful, {failed} failed")
    
    if successful > 0:
        print(f"CSV files saved in: {os.path.abspath(output_dir)}")
        print(f"Total rows generated: {successful * 721}")

def generate_location_comparison_csv(target_date: date, cities: dict = None, output_file: str = "outputs/comparison.csv"):
    """
    Generate a comparison CSV with data from all locations in one file.
    
    Args:
        target_date: Date to calculate for
        cities: Dictionary of cities to process
        output_file: Output CSV file path
    """
    if cities is None:
        cities = INDIAN_CITIES
    
    print(f"Generating comparison CSV for {len(cities)} cities on {target_date}")
    
    all_rows = []
    
    for city_name, city_data in cities.items():
        try:
            # Get sunrise times
            sunrise_ist, next_sunrise_ist = get_sunrise_times(
                city_data["lat"], city_data["lon"], target_date
            )
            
            # Get ascendant
            asc_abs_deg = get_ascendant_at_time(
                city_data["lat"], city_data["lon"], sunrise_ist
            )
            
            # Get astrological data
            asc_sign, asc_sign_lord = get_sign_and_lord(asc_abs_deg)
            asc_nakshatra, asc_nakshatra_lord = get_nakshatra_and_lord(asc_abs_deg)
            asc_sub_lord, asc_sub_sub_lord = get_kp_sub_lords(asc_abs_deg)
            
            # Generate rows for this city
            rows = generate_csv_rows_for_date(
                target_date, sunrise_ist, next_sunrise_ist,
                city_data["lat"], city_data["lon"],
                asc_abs_deg, asc_sign, asc_sign_lord, asc_nakshatra,
                asc_nakshatra_lord, asc_sub_lord, asc_sub_sub_lord
            )
            
            all_rows.extend(rows)
            print(f"  ✓ {city_name}: {asc_sign} ({asc_abs_deg:.3f}°) - {asc_nakshatra}")
            
        except Exception as e:
            print(f"  ✗ {city_name}: {e}")
    
    if all_rows:
        # Create output directory
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write comparison CSV
        write_csv_to_file(all_rows, output_file)
        print(f"\nComparison CSV saved: {output_file}")
        print(f"Total rows: {len(all_rows)}")

def main():
    """Main function to demonstrate multiple location CSV generation."""
    # Example: Generate data for August 20, 2025
    target_date = date(2025, 8, 20)
    
    print("AstroCSV - Multiple Locations Example")
    print("Using well-established astrological libraries")
    print("=" * 60)
    
    # Option 1: Generate individual CSV files for each city
    print("\n1. Generating individual CSV files for each city...")
    generate_multiple_locations_csv(target_date)
    
    # Option 2: Generate comparison CSV with all cities
    print("\n2. Generating comparison CSV with all cities...")
    generate_location_comparison_csv(target_date)
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("All calculations use well-established astrological libraries")
    print("for maximum accuracy across multiple locations.")

if __name__ == "__main__":
    main()
