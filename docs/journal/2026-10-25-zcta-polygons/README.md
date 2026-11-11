# 2026-10-25 · ZCTA polygons on a Foundry map

## Found

First attempt: one geopoint per ZCTA from its Census GEOINFO internal lat/long. ZCTAs are irregular areas, so a point can't be shaded as one.

## Decided

### ZCTA polygons from TIGER, not lat/long points

- **Options:** a geopoint per ZCTA, or a polygon per ZCTA from the Census TIGER/Line shapefile.
- **Choice:** polygons, pre-processed locally in Python and uploaded as GeoJSON.
- **Why:** a rate per area ([2026-10-11](../2026-10-11-area-rates-not-households/)) needs the real boundary.
- **Consequences:**
  - The only step outside Foundry. Pipeline Builder doesn't read shapefiles.
  - Filtering before upload keeps the Foundry dataset small.
  - The hand-maintained Long Island ZCTA list decides what's on the map.

## Built

[`transforms/geography/shapefile_to_geojson.py`](../../../transforms/geography/shapefile_to_geojson.py):

1. Read the 2026 TIGER ZCTA shapefile, filtered to the Long Island ZCTA list (kept locally, not in the repo).
2. Reproject NAD83 → WGS84 (EPSG:4326).
3. Write `data/processed/li-zcta.geojson`; upload to Foundry.

Also learned: terminal navigation, file paths, Git. This repo started here.

## Outcome

173 Long Island ZCTA polygons in Foundry.

<!-- Screenshot: map.png -->
*Map screenshot to add.*
