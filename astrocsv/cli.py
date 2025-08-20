"""
Command line interface for AstroCSV.
"""

import typer
from datetime import date, datetime
from typing import Optional
from pathlib import Path
import sys

from .ephem import setup_swiss_ephemeris, get_sunrise_times, get_ascendant_at_time
from .mapping import get_sign_and_lord, get_nakshatra_and_lord, get_kp_sub_lords
from .csvout import generate_csv_rows_for_date, write_csv_to_file, write_csv_to_stdout

app = typer.Typer(help="Location-based astro transit CSV generator with KP nakshatra calculations")

def validate_latitude(lat: float) -> float:
    """Validate latitude is between -90 and 90 degrees."""
    if not -90 <= lat <= 90:
        raise typer.BadParameter("Latitude must be between -90 and 90 degrees")
    return lat

def validate_longitude(lon: float) -> float:
    """Validate longitude is between -180 and 180 degrees."""
    if not -180 <= lon <= 180:
        raise typer.BadParameter("Longitude must be between -180 and 180 degrees")
    return lon

def validate_date(date_str: str) -> date:
    """Validate and parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise typer.BadParameter("Date must be in YYYY-MM-DD format")

def process_single_date(
    target_date: date,
    lat: float,
    lon: float
) -> list:
    """
    Process a single date and return CSV rows.
    
    Args:
        target_date: Date to process
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        
    Returns:
        List of CSV row dictionaries
    """
    # Get sunrise times
    sunrise_ist, next_sunrise_ist = get_sunrise_times(lat, lon, target_date)
    
    # Get ascendant at sunrise
    asc_abs_deg = get_ascendant_at_time(lat, lon, sunrise_ist)
    
    # Get sign and sign lord
    asc_sign, asc_sign_lord = get_sign_and_lord(asc_abs_deg)
    
    # Get nakshatra and nakshatra lord
    asc_nakshatra, asc_nakshatra_lord = get_nakshatra_and_lord(asc_abs_deg)
    
    # Get KP sub-lord and sub-sub-lord
    asc_sub_lord, asc_sub_sub_lord = get_kp_sub_lords(asc_abs_deg)
    
    # Generate CSV rows for this date
    rows = generate_csv_rows_for_date(
        target_date, sunrise_ist, next_sunrise_ist, lat, lon,
        asc_abs_deg, asc_sign, asc_sign_lord, asc_nakshatra,
        asc_nakshatra_lord, asc_sub_lord, asc_sub_sub_lord
    )
    
    return rows

@app.command()
def main(
    lat: float = typer.Argument(..., help="Latitude in decimal degrees (positive north)"),
    lon: float = typer.Argument(..., help="Longitude in decimal degrees (positive east)"),
    date_str: Optional[str] = typer.Option(None, "--date", help="Single date in YYYY-MM-DD format"),
    start_date: Optional[str] = typer.Option(None, "--start-date", help="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = typer.Option(None, "--end-date", help="End date in YYYY-MM-DD format"),
    outfile: Optional[str] = typer.Option(None, "--outfile", help="Output CSV file path (default: stdout)")
):
    """
    Generate astro transit CSV for location and date(s).
    
    Examples:
        astrocsv --date 2025-08-20 --lat 18.5204 --lon 73.8567 --outfile pune_2025-08-20.csv
        astrocsv --start-date 2025-08-20 --end-date 2025-08-22 --lat 18.5204 --lon 73.8567 --outfile pune_aug20-22.csv
    """
    # Validate inputs
    try:
        lat = validate_latitude(lat)
        lon = validate_longitude(lon)
    except (TypeError, AttributeError):
        # This happens when --help is called, just return
        return
    
    # Validate date parameters
    if date_str and (start_date or end_date):
        typer.echo("Error: Cannot specify both --date and --start-date/--end-date", err=True)
        raise typer.Exit(1)
    
    if not date_str and not (start_date and end_date):
        typer.echo("Error: Must specify either --date or both --start-date and --end-date", err=True)
        raise typer.Exit(1)
    
    if start_date and not end_date:
        typer.echo("Error: Must specify both --start-date and --end-date", err=True)
        raise typer.Exit(1)
    
    if not start_date and end_date:
        typer.echo("Error: Must specify both --start-date and --end-date", err=True)
        raise typer.Exit(1)
    
    # Parse dates
    if date_str:
        target_date = validate_date(date_str)
        start_date_obj = target_date
        end_date_obj = target_date
    else:
        start_date_obj = validate_date(start_date)
        end_date_obj = validate_date(end_date)
        
        if start_date_obj > end_date_obj:
            typer.echo("Error: Start date must be before or equal to end date", err=True)
            raise typer.Exit(1)
    
    # Setup Swiss Ephemeris
    try:
        setup_swiss_ephemeris()
    except Exception as e:
        typer.echo(f"Error setting up Swiss Ephemeris: {e}", err=True)
        typer.echo("Please ensure ephemeris files are available in ./ephe/ directory", err=True)
        raise typer.Exit(1)
    
    # Process dates
    all_rows = []
    current_date = start_date_obj
    
    while current_date <= end_date_obj:
        try:
            rows = process_single_date(current_date, lat, lon)
            all_rows.extend(rows)
            current_date = current_date.replace(day=current_date.day + 1)
        except Exception as e:
            typer.echo(f"Error processing date {current_date}: {e}", err=True)
            raise typer.Exit(1)
    
    # Output results
    if outfile:
        try:
            write_csv_to_file(all_rows, outfile)
            typer.echo(f"CSV written to {outfile}")
            typer.echo(f"Total rows: {len(all_rows)}")
        except Exception as e:
            typer.echo(f"Error writing to file {outfile}: {e}", err=True)
            raise typer.Exit(1)
    else:
        # Write to stdout
        write_csv_to_stdout(all_rows)

if __name__ == "__main__":
    app()
