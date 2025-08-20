# Swiss Ephemeris Data Files

This directory should contain Swiss Ephemeris data files for accurate astronomical calculations.

## Required Files

For basic functionality, you need at least one of these files:

- `seas_18.se1` - Solar System ephemeris (recommended)
- `semo_18.se1` - Moon ephemeris
- `sepl_18.se1` - Planets ephemeris

## Download Sources

### Official Swiss Ephemeris
- **Website**: https://www.astro.com/ftp/swisseph/
- **Files**: Look for files ending in `.se1`

### Alternative Sources
- **GitHub**: https://github.com/astrorigin/swisseph
- **Direct Download**: Various astrological software repositories

## File Descriptions

- **`seas_18.se1`**: Contains positions of Sun, Moon, and planets (most comprehensive)
- **`semo_18.se1`**: Moon-specific ephemeris (high precision for lunar calculations)
- **`sepl_18.se1`**: Planetary ephemeris (Sun, Mercury, Venus, Mars, Jupiter, Saturn)

## Installation

1. Download the required `.se1` files
2. Place them in this directory (`astrocsv/ephe/`)
3. Ensure the files are readable by your Python process

## Verification

After placing the files, you can verify they're working by running:

```bash
python -c "import swisseph as swe; swe.set_ephe_path('./astrocsv/ephe/'); print('Ephemeris files loaded successfully')"
```

## Troubleshooting

- **File not found errors**: Ensure files are in the correct directory
- **Permission errors**: Check file permissions (should be readable)
- **Corrupted files**: Re-download if files appear corrupted
- **Missing files**: At minimum, you need `seas_18.se1` for basic functionality

## Note

Swiss Ephemeris data files are large (several MB each) and contain precise astronomical data. They are essential for accurate astrological calculations.
