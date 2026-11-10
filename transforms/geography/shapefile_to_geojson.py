"""
Takes 2026 TIGER Shapefile by Zip Code Tabulation Area (ZCTA) Data.
Prefilters it to Nassau/Suffolk counties.
Reprojects NAD83 → WGS84
Converts it into a geoJSON format, for upload to Foundry.
"""

from pathlib import Path

import geopandas

REPO_ROOT = Path(__file__).resolve().parents[2]
ZCTAS = (REPO_ROOT / "data" / "raw" / "long_island_zctas.txt").read_text().split()
SHAPEFILE = REPO_ROOT / "data" / "raw" / "location-data" / "tl_2026_us_zcta520"
WGS84 = 4326


def main():

    cleaned_list = []
    for zcta in ZCTAS:
        cleaned_list.append(f"'{zcta}'")

    li_zcta_string = ",".join(cleaned_list)
    query = f"ZCTA5CE20 IN ({li_zcta_string})"
    gdf = geopandas.read_file(SHAPEFILE, where=query)

    gdf = gdf.to_crs(WGS84)

    gdf.to_file(REPO_ROOT / "data" / "processed" / "li-zcta.geojson", driver="GeoJSON")


if __name__ == "__main__":
    main()
