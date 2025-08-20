
PROJECT NAME : location based astro transit

Here’s a single, in-depth **Cursor prompt** you can paste directly. It covers **date ranges**, **IST timezone**, **sunrise → next-day sunrise window**, **Ascendant (Lagna)**, **sign & lord**, **nakshatra + KP sub-lord + sub-sub-lord**, and a **0.5° grid**, returning one **CSV**. It also defines the exact CLI, schema, calculations, tests, and deliverables so the agent can implement without further questions.

---

# Cursor Prompt — AstroCSV (India-TZ Sunrise → Ascendant → KP Nakshatra CSV)

**Mission**
Build a Python 3.11+ CLI + library that, for any given **Indian location (lat, lon)** and **date or date range**, computes for each day:

* Local **sunrise** time (IST) at the given lat/lon
* The **Ascendant (Lagna)** at that sunrise instant (topocentric, true ecliptic longitude, 0–360°)
* **Ascendant sign (Rāshi)** and **sign lord**
* **Nakshatra** at that ascendant longitude + **nakshatra lord** (Vimshottari)
* **KP sub-lord** and **sub-sub-lord** at that ascendant longitude (Vimshottari proportional subdivisions)
* A **per-0.5° grid** from **0.0° → 359.5°**: for each half-degree bucket, compute which **sign** it falls in and the **sign lord**
* The “day window” is **\[sunrise at date D, sunrise at date D+1)** in **Asia/Kolkata** (IST).

All results for all days in the range are written into **one CSV file** (or STDOUT).

---

## Inputs & CLI

Support both single-day and multi-day runs:

```
astrocsv \
  --lat <decimal> \
  --lon <decimal> \
  [ --date YYYY-MM-DD | --start-date YYYY-MM-DD --end-date YYYY-MM-DD ] \
  [--outfile /path/to/output.csv]
```

Rules:

* If `--date` is present → compute that single day (D).
* If `--start-date` and `--end-date` are present → compute **inclusive** range \[start, end].
* Error if both `--date` and range flags are provided together, or if only one of `--start-date/--end-date` is given.
* **Timezone fixed** to `Asia/Kolkata` (IST). No DST.
* **Lat/Lon** are decimal degrees (lon positive east; lat positive north). You will receive Indian cities’ lat/lon from the user.

---

## Output: Single CSV (schema & ordering)

Write one CSV containing rows for each requested date. Sort by:

1. `date_ist` ascending,
2. `row_type` where `ascendant_at_sunrise` rows come before `degree_bucket`,
3. `bucket_start_deg` ascending (for bucket rows).

**Exact column order:**

```
row_type,            # "ascendant_at_sunrise" | "degree_bucket"
date_ist,            # YYYY-MM-DD (the sunrise date in IST)
sunrise_ist,         # ISO8601 IST time at date D sunrise
next_sunrise_ist,    # ISO8601 IST time at date D+1 sunrise (day window end)
location_lat,        # decimal
location_lon,        # decimal
asc_abs_deg,         # 0.000–359.999 (only for ascendant row; blank for buckets)
asc_sign,            # e.g., "Aries" (ascendant row only)
asc_sign_lord,       # e.g., "Mars" (ascendant row only)
asc_nakshatra,       # e.g., "Ashwini" (ascendant row only)
asc_nakshatra_lord,  # e.g., "Ketu" (ascendant row only)
asc_sub_lord,        # KP sub-lord at ascendant (ascendant row only)
asc_sub_sub_lord,    # KP sub-sub-lord at ascendant (ascendant row only)
bucket_start_deg,    # 0.0, 0.5, ..., 359.5 (bucket rows only)
bucket_sign,         # bucket’s sign (bucket rows only)
bucket_sign_lord     # bucket’s sign lord (bucket rows only)
```

For each **date D**:

* Exactly **1** row with `row_type=ascendant_at_sunrise`
* Exactly **720** rows with `row_type=degree_bucket` (0.5° grid)

So a range of N days → **N × 721** total rows.

CSV formatting:

* Degrees printed to **3 decimals** (round-half-away-from-zero or round-half-even; be consistent).
* Empty fields for not-applicable columns must be **blank**, not “null”.

---

## Core Calculations

### 1) Sunrise (IST)

* Use `astral` (v3+) or equivalent to compute sunrise for given lat/lon on date D in timezone `Asia/Kolkata`. Astral uses solar center at standard refraction; acceptable for this tool.
* Return **sunrise\_ist** (ISO8601 with `+05:30`).
* Compute **next\_sunrise\_ist** by running sunrise for date D+1 (same lat/lon).

Edge cases:

* If Astral fails (rare), provide fallback: compute solar altitude root near civil sunrise using Swiss Ephemeris solar RA/Dec and refraction (34′) + solar radius (16′).

### 2) Ascendant at sunrise (topocentric)

* Use **Swiss Ephemeris (`pyswisseph`)** with local topocentric observer:

  * Set observer: `swe.set_topo(lon, lat, 0)` (lon east+, lat north+; altitude 0m unless user provides).
  * Convert **sunrise\_ist** to UTC, then to Julian Day (UT).
  * Compute houses/ascendant: `swe.houses_ex(jd_ut, lat, lon, b'P', flags)` (system code may be 'P' Placidus; for **Asc** the house system choice does not affect the rising ecliptic point; still keep it explicit).
  * Recommended flags: `SEFLG_SWIEPH | SEFLG_SPEED | SEFLG_EQUATORIAL` not needed; for ascendant we need ecliptic long. A safe combo is `SEFLG_SWIEPH | SEFLG_TRUEPOS | SEFLG_TOPOCTR`.
  * Extract **Asc** (element 0 from the return tuple) in **degrees \[0,360)** → **asc\_abs\_deg**.

### 3) Sign (Rāshi) & Sign Lord

* 12 signs, **30° each**, lower bound inclusive, upper bound exclusive:

  * 0–30 **Aries** — **Mars**
  * 30–60 **Taurus** — **Venus**
  * 60–90 **Gemini** — **Mercury**
  * 90–120 **Cancer** — **Moon**
  * 120–150 **Leo** — **Sun**
  * 150–180 **Virgo** — **Mercury**
  * 180–210 **Libra** — **Venus**
  * 210–240 **Scorpio** — **Mars**
  * 240–270 **Sagittarius** — **Jupiter**
  * 270–300 **Capricorn** — **Saturn**
  * 300–330 **Aquarius** — **Saturn**
  * 330–360 **Pisces** — **Jupiter**
* Map **asc\_abs\_deg** to **asc\_sign** & **asc\_sign\_lord**.
* For the **0.5° grid**, compute:

  * `bucket_start_deg` ∈ {0.0, 0.5, 1.0, …, 359.5}
  * `bucket_sign`, `bucket_sign_lord` using the same 30° bins.

### 4) Nakshatra (27, each 13°20′) & Nakshatra Lord

* Total circle 360°; **nakshatra span = 13°20′ = 13.333333…° = 800 arcminutes**.

* Start at **0° Aries = Ashwini** and proceed in order:

  1 Ashwini—Ketu
  2 Bharani—Venus
  3 Krittika—Sun
  4 Rohini—Moon
  5 Mrigashira—Mars
  6 Ardra—Rahu
  7 Punarvasu—Jupiter
  8 Pushya—Saturn
  9 Ashlesha—Mercury
  10 Magha—Ketu
  11 Purva Phalguni—Venus
  12 Uttara Phalguni—Sun
  13 Hasta—Moon
  14 Chitra—Mars
  15 Swati—Rahu
  16 Vishakha—Jupiter
  17 Anuradha—Saturn
  18 Jyeshtha—Mercury
  19 Mula—Ketu
  20 Purva Ashadha—Venus
  21 Uttara Ashadha—Sun
  22 Shravana—Moon
  23 Dhanishta—Mars
  24 Shatabhisha—Rahu
  25 Purva Bhadrapada—Jupiter
  26 Uttara Bhadrapada—Saturn
  27 Revati—Mercury

* Find `nak_index = floor( asc_abs_deg / 13.333333… )` (with proper handling at 360 wrap) → **asc\_nakshatra**.

* **asc\_nakshatra\_lord** from the table above.

### 5) KP Sub-lord & Sub-sub-lord (Vimshottari proportional split)

* Vimshottari sequence & weights (years):
  **Ketu=7, Venus=20, Sun=6, Moon=10, Mars=7, Rahu=18, Jupiter=16, Saturn=19, Mercury=17** (sum = 120).
* Each **nakshatra = 800 arcminutes**.

  * **Sub-segment size (arcmin)** = `weight / 120 * 800`.
  * The **order** of sub-lords **starts from the nakshatra lord** and continues in the Vimshottari sequence cyclically.
    Example: if nakshatra lord = **Moon**, the sub order is `[Moon, Mars, Rahu, Jupiter, Saturn, Mercury, Ketu, Venus, Sun]` with corresponding lengths proportional to the same weights.
* Determine the **arcminute offset** of `asc_abs_deg` within its nakshatra; find which sub segment contains it → **asc\_sub\_lord**.
* For **sub-sub-lord**: subdivide the chosen sub segment into 9 parts **in the same order** starting from the **sub-lord**; pick the segment containing the point → **asc\_sub\_sub\_lord**.

Precision & boundaries:

* Treat **lower bound inclusive, upper bound exclusive** for all bins.
* Compute in arcminutes with high precision; convert to degrees for display.

---

## Non-Goals / Assumptions

* No external web calls. All offline ephemeris.
* Altitude = 0m unless user extends input; okay for now.
* Traditional sign lords (Mars for Scorpio, Saturn for Aquarius).
* We only compute ascendant at **sunrise instant** (not throughout the day). If later needed, we can add per-minute lagna tracking within \[sunrise, next\_sunrise).

---

## Tech Stack & Packaging

* **Python 3.11+**, `pyswisseph`, `astral`, `pandas`, `zoneinfo` (stdlib), `typer` or `argparse`.
* Keep ephemeris files in `./ephe/`; document how to download Swiss Ephemeris data.
* Project layout:

```
astrocsv/
  __init__.py
  cli.py
  ephem.py           # sunrise (IST), SwissEph setup, ascendant calc
  mapping.py         # signs/lords, nakshatra tables
  kp.py              # KP sub/sub-sub computations
  csvout.py          # writer + schema enforcement
tests/
  test_sunrise.py
  test_ascendant.py
  test_mapping.py
  test_kp.py
pyproject.toml
README.md
```

* Provide a **console script** entry point `astrocsv` in `pyproject.toml`.

---

## Acceptance Criteria (must pass)

1. **Single day example**

```
astrocsv --date 2025-08-20 --lat 18.5204 --lon 73.8567 --outfile pune_2025-08-20.csv
```

* Computes **sunrise\_ist** for Pune on 2025-08-20 and **next\_sunrise\_ist** (2025-08-21).
* Computes **asc\_abs\_deg**, **asc\_sign**, **asc\_sign\_lord**, **asc\_nakshatra**, **asc\_nakshatra\_lord**, **asc\_sub\_lord**, **asc\_sub\_sub\_lord** at sunrise.
* Adds **720 bucket rows** with correct sign & lord.
* CSV has **721 rows** with correct header and ordering.

2. **Date range example**

```
astrocsv --start-date 2025-08-20 --end-date 2025-08-22 --lat 18.5204 --lon 73.8567 --outfile pune_aug20-22.csv
```

* Produces **3 × 721 = 2163 rows** covering 2025-08-20, 21, 22.
* Each date has its own `sunrise_ist` and `next_sunrise_ist`.
* No row/column missing; numeric formats correct.

3. **Validation & errors**

* Invalid lat/lon → exit with non-zero code + clear message.
* Missing/ambiguous date flags → non-zero exit + help text.
* Timezone is strictly **Asia/Kolkata**; no DST artifacts.

4. **Determinism**

* Given same inputs and ephemeris files, outputs are byte-identical.

---

## Testing Requirements

* **Sunrise sanity**: known IST sunrises (Mumbai, Delhi, Kolkata, Chennai) within reasonable tolerance of authoritative values (±2–3 min).
* **Sign boundaries**: degrees `29.5, 30.0, 30.5, …` correctly map across Aries→Taurus, etc.
* **Nakshatra boundaries**: test near every `i * 13°20′`.
* **KP math**: for chosen nakshatras, verify sub and sub-sub segmentation totals (sum to 800′ and nested correctly).
* **CSV schema**: header exact; row ordering and row counts exact.

---

## Implementation Notes

* Normalize all longitudes to `[0, 360)`.
* Degree ↔ arcminute: `deg * 60 = arcmin`, `arcmin / 60 = deg`.
* Use `Decimal` or careful float math; keep internal calculations in arcminutes (integers where possible).
* Binning rule: **inclusive** at lower bound, **exclusive** at upper bound (`[start, end)`) for signs, nakshatras, subs, sub-subs, and 0.5° buckets.
* CSV writing via `pandas` or `csv` module; ensure **no extra index column**.
* Large ranges: stream writing (append) to keep memory stable.

---

## Deliverables

* Working CLI `astrocsv` with the behavior above.
* Source package as outlined, with **unit tests** and **README.md** (installation, ephemeris download, examples, schema).
* Example outputs for at least **Pune**, **Mumbai**, **Delhi** on the same date.

---

## Quick Hindi/Marathi alignment (for clarity)

* “**Ascendant Rāshi ghenār**” → compute lagna sign at sunrise.
* “**Pratek half degree-la sign konta & sign-lord kon**” → generate 0.5° buckets and map to sign + sign lord.
* “**End will be next day sunrise**” → include `next_sunrise_ist` per day to mark the window end.

---

**Build this exactly as specified. Ask for nothing else.**
