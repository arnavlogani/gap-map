"""
Takes 6 ACS 5-year 2020-2024 tables (check sources.md),
filters them to the 175 Long Island ZCTAs, computes 7 indirect
need rates, runs health checks, and computes z_indirect.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
ZCTAS = (REPO_ROOT / "data" / "raw" / "long_island_zctas.txt").read_text().split()
ACS_DIR = REPO_ROOT / "data" / "raw" / "acs"
OUTPUT = REPO_ROOT / "data" / "processed"

RATES = [
    "snap_rate",
    "poverty_rate",
    "child_poverty_rate",
    "senior_poverty_rate",
    "median_income",
    "severe_burden_rate",
    "no_vehicle_rate",
]

KIDS_BELOW = [
    "B17001_004E",
    "B17001_005E",
    "B17001_006E",
    "B17001_007E",
    "B17001_008E",
    "B17001_009E",
    "B17001_018E",
    "B17001_019E",
    "B17001_020E",
    "B17001_021E",
    "B17001_022E",
    "B17001_023E",
]
KIDS_ABOVE = [
    "B17001_033E",
    "B17001_034E",
    "B17001_035E",
    "B17001_036E",
    "B17001_037E",
    "B17001_038E",
    "B17001_047E",
    "B17001_048E",
    "B17001_049E",
    "B17001_050E",
    "B17001_051E",
    "B17001_052E",
]
SENIORS_BELOW = ["B17001_015E", "B17001_016E", "B17001_029E", "B17001_030E"]
SENIORS_ABOVE = ["B17001_044E", "B17001_045E", "B17001_058E", "B17001_059E"]


def load_acs(table):
    df = pd.read_csv(ACS_DIR / f"{table}-Data.csv", skiprows=[1])
    df["zcta5"] = df["GEO_ID"].str[-5:]
    df = df[df["zcta5"].isin(ZCTAS)].set_index("zcta5")
    # Census writes top/bottom-coded medians as text ("250,000+", "2,500-") and
    # missing estimates as "-" or "***". Keep the coded values, turn the rest to NaN.
    df = df.replace({"250,000+": "250000", "2,500-": "2500"})
    estimates = [c for c in df.columns if c.endswith("E") and c != "GEO_ID"]
    df[estimates] = df[estimates].apply(pd.to_numeric, errors="coerce")
    return df


def check_inputs(df):
    assert len(df) == 175, f"expected 175 rows, got {len(df)}"
    assert df.index.is_unique, "duplicate zcta5 values"


def check_suppressed(df):
    # Census Errata #148: no 2023/2024 ACS for Brentwood and Wyandanch
    assert df.loc[["11717", "11798"], RATES].isna().all().all(), (
        "11717/11798 should be null"
    )


def check_rate_range(df):
    rates = df[[c for c in RATES if c != "median_income"]]
    assert ((rates >= 0) & (rates <= 1) | rates.isna()).all().all(), (
        "rates must be between 0 and 1"
    )


def check_no_overlap(df):
    corr = df[[f"z_{c}" for c in RATES]].corr(method="spearman")
    pairs = (corr.abs() > 0.85).sum().sum() - len(RATES)  # minus the diagonal
    assert pairs == 0, "two indicators correlate above 0.85: drop one (rule 4)"


def main():

    pov = load_acs("ACSDT5Y2024.B17001")
    inc = load_acs("ACSDT5Y2024.B19013")
    veh = load_acs("ACSDT5Y2024.B25044")
    rent = load_acs("ACSDT5Y2024.B25070")
    own = load_acs("ACSDT5Y2024.B25091")
    snap = load_acs("ACSST5Y2024.S2201")

    kids_below = pov[KIDS_BELOW].sum(axis=1)
    kids_total = kids_below + pov[KIDS_ABOVE].sum(axis=1)
    seniors_below = pov[SENIORS_BELOW].sum(axis=1)
    seniors_total = seniors_below + pov[SENIORS_ABOVE].sum(axis=1)

    severe_burden = rent["B25070_010E"] + own["B25091_011E"] + own["B25091_022E"]
    all_households = rent["B25070_001E"] + own["B25091_001E"]

    no_vehicle = veh["B25044_003E"] + veh["B25044_010E"]

    income = inc["B19013_001E"]

    df = pd.DataFrame(index=pd.Index(ZCTAS, name="zcta5"))
    df["snap_rate"] = snap["S2201_C03_001E"] / snap["S2201_C01_001E"]
    df["poverty_rate"] = pov["B17001_002E"] / pov["B17001_001E"]
    df["child_poverty_rate"] = kids_below / kids_total
    df["senior_poverty_rate"] = seniors_below / seniors_total
    df["median_income"] = income
    df["severe_burden_rate"] = severe_burden / all_households
    df["no_vehicle_rate"] = no_vehicle / veh["B25044_001E"]

    check_inputs(df)
    check_suppressed(df)
    check_rate_range(df)

    for col in RATES:
        df[f"z_{col}"] = (df[col] - df[col].mean()) / df[col].std()
    df["z_median_income"] = -df["z_median_income"]  # higher income = less need

    check_no_overlap(df)

    z_cols = [f"z_{c}" for c in RATES]
    df["n_indicators"] = df[z_cols].notna().sum(axis=1)
    z_mean = df[z_cols].mean(axis=1)
    z_mean[df["n_indicators"] < 4] = None  # rule 3
    df["z_indirect"] = (z_mean - z_mean.mean()) / z_mean.std()

    print(df["z_indirect"].isna().sum(), "ZCTAs with null z_indirect")

    df.to_csv(OUTPUT / "need_indirect.csv")


if __name__ == "__main__":
    main()
