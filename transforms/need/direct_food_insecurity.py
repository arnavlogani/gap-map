"""
Takes the CDC PLACES modeled food insecurity rate (check sources.md),
filters it to Nassau and Suffolk County Zip Code Tabulation Areas,
runs health checks, and computes z_direct.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
ZCTAS = (REPO_ROOT / "data" / "raw" / "long_island_zctas.txt").read_text().split()
PLACES_DIRECT = (
    REPO_ROOT
    / "data"
    / "raw"
    / "PLACES__ZCTA_Data_(GIS_Friendly_Format),_2025_release_20261103.geojson"
)
OUTPUT = REPO_ROOT / "data" / "processed"


def check_inputs(df):
    assert len(df) == 175, f"expected 175 rows, got {len(df)}"


def check_primary_key(df):
    assert df["zcta5"].is_unique, "duplicate zcta5 values"


def check_null_count(df):
    nulls = df["fi_rate"].isna().sum()
    assert nulls == 4, f"expected 4 null fi_rate values, got {nulls}"


def check_fi_rate_range(df):
    assert df["fi_rate"].min() >= 3 and df["fi_rate"].max() <= 40, (
        "Expect food insecurity rates to be between 3 and 40"
    )


def main():

    gdf = gpd.read_file(PLACES_DIRECT)

    gdf = gdf[["zcta5", "totalpop18plus", "foodinsecu_crudeprev"]]
    gdf = gdf.rename(
        columns={"totalpop18plus": "adults", "foodinsecu_crudeprev": "fi_rate"}
    )

    zcta_df = pd.DataFrame({"zcta5": ZCTAS})
    df = pd.merge(zcta_df, gdf, on="zcta5", how="left")

    df["fi_rate"] = pd.to_numeric(df["fi_rate"], errors="coerce")
    df["adults"] = pd.to_numeric(df["adults"], errors="coerce")

    check_inputs(df)
    check_null_count(df)
    check_primary_key(df)
    check_fi_rate_range(df)

    df["low_confidence"] = (df["adults"] < 500) | df["fi_rate"].isna()

    print(df["low_confidence"].sum())

    df["z_direct"] = (df["fi_rate"] - df["fi_rate"].mean()) / df["fi_rate"].std()

    df.to_csv(OUTPUT / "need_direct.csv", index=False)


if __name__ == "__main__":
    main()
