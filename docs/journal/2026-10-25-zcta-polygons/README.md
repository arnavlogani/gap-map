# 2026-10-25 · ZCTA polygons on a Foundry map

## Found

Before more transformation, the first priority was getting a real map into Foundry. The first attempt used each ZCTA's internal point (latitude and longitude from Census GEOINFO) as a geopoint. But ZCTAs are irregular areas, not points or circles around a radius, so that approach can't shade an area.

## Decided

### ZCTA polygons from TIGER, not lat/long points

- **Options:**
  1. A geopoint per ZCTA from its internal lat/long.
  2. A polygon per ZCTA from the Census TIGER/Line shapefile.
- **Choice:** polygons, pre-processed locally in Python and uploaded to Foundry as GeoJSON.
- **Why:** a rate per area ([2026-10-11](../2026-10-11-area-rates-not-households/)) has to be drawn as a filled area, which needs the real boundary.
- **Consequences:**
  - This is the one step done outside Foundry, because Pipeline Builder doesn't read shapefiles directly.
  - The national shapefile is large, so filtering before upload keeps the Foundry dataset small.
  - The Long Island ZCTA list is a hand-maintained input, and it decides what's on the map.

## Built

[`transforms/geography/shapefile_to_geojson.py`](../../../transforms/geography/shapefile_to_geojson.py):

1. Read the 2026 TIGER ZCTA shapefile, filtered to the Long Island ZCTA list (kept locally, not in the repo).
2. Reproject from NAD83 to WGS84 (EPSG:4326), which web maps expect.
3. Write `data/processed/li-zcta.geojson` and upload it to Foundry.

Learned along the way: terminal navigation, file paths, and Git (init vs. clone, add vs. commit, push vs. pull). This repo started here.

## Outcome

173 Long Island ZCTA polygons in Foundry.

<!-- Screenshot: map.png -->
*Map screenshot to add.*
