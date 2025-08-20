# AstroCSV

Location-based astro transit CSV generator with KP nakshatra calculations.

## Overview

AstroCSV is a Python CLI tool that generates comprehensive astrological transit data for any location and date range. It calculates:

- **Sunrise times** in IST (Indian Standard Time)
- **Ascendant (Lagna)** at sunrise with precise degree values
- **Sign (Rāshi)** and **sign lord** mappings
- **Nakshatra** and **nakshatra lord** (Vimshottari system)
- **KP sub-lord** and **sub-sub-lord** calculations
- **0.5° degree grid** with sign and lord mappings for the entire zodiac

## Features

- **Well-Established Libraries**: Uses Swiss Ephemeris and standard astrological calculations
- **Multi-Location Support**: Generate CSV data for multiple cities/locations efficiently
- **IST Timezone**: Fixed to Asia/Kolkata timezone (no DST complications)
- **KP System**: Full Krishnamurti Paddhati sub-lord calculations using standard algorithms
- **Comprehensive Output**: Generates 721 rows per day (1 ascendant + 720 degree buckets)
- **Flexible Input**: Support for single dates or date ranges
- **CSV Output**: Standardized CSV format with exact schema compliance
- **Professional Grade**: Calculations used by professional astrologers worldwide

## Installation

### Prerequisites

- Python 3.11 or higher
- Swiss Ephemeris data files

### Install Package

```bash
# Clone the repository
git clone <repository-url>
cd astrocsv

# Install in development mode
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Swiss Ephemeris Setup

AstroCSV requires Swiss Ephemeris data files for accurate calculations.

### Download Ephemeris Files

1. Create the ephemeris directory:
   ```bash
   mkdir -p astrocsv/ephe
   ```

2. Download Swiss Ephemeris data files from:
   - **Official**: https://www.astro.com/ftp/swisseph/
   - **Alternative**: https://github.com/astrorigin/swisseph

3. Place the following files in `astrocsv/ephe/`:
   - `seas_18.se1` (Solar System ephemeris)
   - `semo_18.se1` (Moon ephemeris)
   - `sepl_18.se1` (Planets ephemeris)

### Minimum Required Files

For basic functionality, you need at least:
- `seas_18.se1` (Solar System)

## Usage

### Basic Syntax

```bash
astrocsv --lat <latitude> --lon <longitude> [--date <date> | --start-date <start> --end-date <end>] [--outfile <file>]
```

### Multiple Locations

For generating CSV data for multiple locations efficiently, use the example script:

```bash
python examples/multiple_locations.py
```

This will generate CSV files for 10 major Indian cities using well-established astrological libraries.

### Examples

#### Single Date (Pune)

```bash
astrocsv --date 2025-08-20 --lat 18.5204 --lon 73.8567 --outfile pune_2025-08-20.csv
```

This generates a CSV with 721 rows for August 20, 2025 in Pune.

#### Date Range (Pune)

```bash
astrocsv --start-date 2025-08-20 --end-date 2025-08-22 --lat 18.5204 --lon 73.8567 --outfile pune_aug20-22.csv
```

This generates a CSV with 2163 rows (3 days × 721 rows) for August 20-22, 2025.

#### Output to STDOUT

```bash
astrocsv --date 2025-08-20 --lat 18.5204 --lon 73.8567
```

Outputs CSV data directly to the terminal.

### Indian Cities Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Mumbai | 19.0760 | 72.8777 |
| Delhi | 28.7041 | 77.1025 |
| Kolkata | 22.5726 | 88.3639 |
| Chennai | 13.0827 | 80.2707 |
| Pune | 18.5204 | 73.8567 |
| Bangalore | 12.9716 | 77.5946 |
| Hyderabad | 17.3850 | 78.4867 |

## Output Schema

The CSV contains exactly these columns in order:

| Column | Description | Example |
|--------|-------------|---------|
| `row_type` | Row type identifier | "ascendant_at_sunrise" or "degree_bucket" |
| `date_ist` | Date in IST | "2025-08-20" |
| `sunrise_ist` | Sunrise time in IST | "2025-08-20T06:15:30+05:30" |
| `next_sunrise_ist` | Next sunrise time in IST | "2025-08-21T06:15:45+05:30" |
| `location_lat` | Latitude | 18.520400 |
| `location_lon` | Longitude | 73.856700 |
| `asc_abs_deg` | Ascendant degree (ascendant rows only) | 45.123 |
| `asc_sign` | Ascendant sign (ascendant rows only) | "Taurus" |
| `asc_sign_lord` | Ascendant sign lord (ascendant rows only) | "Venus" |
| `asc_nakshatra` | Ascendant nakshatra (ascendant rows only) | "Rohini" |
| `asc_nakshatra_lord` | Ascendant nakshatra lord (ascendant rows only) | "Moon" |
| `asc_sub_lord` | Ascendant KP sub-lord (ascendant rows only) | "Mars" |
| `asc_sub_sub_lord` | Ascendant KP sub-sub-lord (ascendant rows only) | "Rahu" |
| `bucket_start_deg` | Degree bucket start (bucket rows only) | 0.0, 0.5, 1.0, ... |
| `bucket_sign` | Bucket sign (bucket rows only) | "Aries", "Taurus", ... |
| `bucket_sign_lord` | Bucket sign lord (bucket rows only) | "Mars", "Venus", ... |

### Row Structure

For each date, the CSV contains:
- **1 row** with `row_type="ascendant_at_sunrise"` containing ascendant data
- **720 rows** with `row_type="degree_bucket"` covering the 0.5° grid (0.0° to 359.5°)

## Astrological Systems

### Signs (Rāshi)

- **Aries** (0°-30°): Mars
- **Taurus** (30°-60°): Venus
- **Gemini** (60°-90°): Mercury
- **Cancer** (90°-120°): Moon
- **Leo** (120°-150°): Sun
- **Virgo** (150°-180°): Mercury
- **Libra** (180°-210°): Venus
- **Scorpio** (210°-240°): Mars
- **Sagittarius** (240°-270°): Jupiter
- **Capricorn** (270°-300°): Saturn
- **Aquarius** (300°-330°): Saturn
- **Pisces** (330°-360°): Jupiter

### Nakshatras

27 nakshatras, each spanning 13°20' (13.333...°), starting from Ashwini at 0° Aries.

### KP System

Uses Vimshottari dasha system with proportional subdivisions:
- **Ketu**: 7 years
- **Venus**: 20 years
- **Sun**: 6 years
- **Moon**: 10 years
- **Mars**: 7 years
- **Rahu**: 18 years
- **Jupiter**: 16 years
- **Saturn**: 19 years
- **Mercury**: 17 years

## Testing

Run the test suite:

```bash
pytest tests/
```

### Test Categories

- **Mapping Tests**: Sign, nakshatra, and KP calculations
- **Sunrise Tests**: Astral and fallback calculations
- **Ascendant Tests**: Swiss Ephemeris integration
- **KP Tests**: Sub-lord calculations

## Technical Details

### Dependencies

- **pyswisseph**: Swiss Ephemeris Python bindings (industry standard)
- **astral**: Sunrise/sunset calculations (well-established library)
- **pandas**: CSV generation and manipulation (industry standard)
- **typer**: Command-line interface
- **zoneinfo**: Timezone handling
- **astrology**: Additional astrological functions

### Architecture

```
astrocsv/
├── __init__.py          # Package initialization
├── cli.py              # Command-line interface
├── ephem.py            # Ephemeris calculations
├── mapping.py          # Astrological mappings
├── csvout.py           # CSV output generation
└── ephe/               # Swiss Ephemeris data files
```

### Calculation Flow

1. **Input Validation**: Validate coordinates and dates
2. **Sunrise Calculation**: Compute sunrise times using astral (with Swiss Ephemeris fallback)
3. **Ascendant Calculation**: Use Swiss Ephemeris for precise ascendant at sunrise
4. **Astrological Mapping**: Determine signs, nakshatras, and KP sub-lords
5. **Degree Bucket Generation**: Create 0.5° grid with sign mappings
6. **CSV Output**: Generate properly formatted CSV with exact schema

## Error Handling

- **Invalid Coordinates**: Latitude must be -90 to 90, longitude -180 to 180
- **Date Conflicts**: Cannot specify both single date and date range
- **Missing Ephemeris**: Clear error message if Swiss Ephemeris files unavailable
- **Timezone Consistency**: All calculations use IST (Asia/Kolkata)

## Performance

- **Memory Efficient**: Streams data for large date ranges
- **Deterministic**: Same inputs always produce identical outputs
- **Fast**: Optimized calculations using Swiss Ephemeris

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the test suite for usage examples
2. Verify Swiss Ephemeris files are properly installed
3. Ensure coordinates are in valid ranges
4. Check timezone settings (fixed to IST)
