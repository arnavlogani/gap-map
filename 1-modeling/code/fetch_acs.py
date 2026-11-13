"""
Downloads the 6 ACS 5-year 2020-2024 tables used by indirect_acs.py from the
Census API, for the 175 Long Island ZCTAs, into data/raw/acs/.

Files are written in the same layout as a data.census.gov download
(code header row, then a label row, then one row per ZCTA), so indirect_acs.py
reads them unchanged.

Needs a free Census API key: https://api.census.gov/data/key_signup.html
    export CENSUS_API_KEY=your_key
"""

import os
from pathlib import Path
from urllib.parse import quote, urlencode

import pandas as pd
import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
ZCTAS = (REPO_ROOT / "data" / "raw" / "long_island_zctas.txt").read_text().split()
ACS_DIR = REPO_ROOT / "data" / "raw" / "acs"
API = "https://api.census.gov/data/2024/acs/acs5"

# (file prefix, API path, table)
TABLES = [
    ("ACSDT5Y2024", "", "B17001"),
    ("ACSDT5Y2024", "", "B19013"),
    ("ACSDT5Y2024", "", "B25044"),
    ("ACSDT5Y2024", "", "B25070"),
    ("ACSDT5Y2024", "", "B25091"),
    ("ACSST5Y2024", "/subject", "S2201"),
]


def get_json(url, params):
    # quote, not quote_plus: the API wants %20 for the space in "zip code ..."
    response = requests.get(f"{url}?{urlencode(params, quote_via=quote)}", timeout=60)
    response.raise_for_status()
    if "json" not in response.headers.get("Content-Type", ""):
        raise RuntimeError(f"Census API did not return data. Check your key.\n{url}")
    return response.json()


def fetch_table(path, table, key):
    rows = get_json(
        f"{API}{path}",
        {
            "get": f"group({table})",
            "for": f"zip code tabulation area:{','.join(ZCTAS)}",
            "key": key,
        },
    )
    df = pd.DataFrame(rows[1:], columns=rows[0])

    # Keep what a data.census.gov download has: GEO_ID, NAME, estimates, MOEs.
    keep = [c for c in df.columns if c.endswith(("E", "M")) and c[:1] in "BS"]
    df = df[["GEO_ID", "NAME", *keep]]

    # The API marks missing or suppressed values with large negative codes
    # (e.g. -666666666). data.census.gov shows these as "-".
    for col in keep:
        values = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].where(~(values < 0), "-")
    return df


def fetch_labels(path, table, key):
    variables = get_json(f"{API}{path}/groups/{table}.json", {"key": key})
    labels = {name: v["label"] for name, v in variables["variables"].items()}
    labels.update({"GEO_ID": "Geography", "NAME": "Geographic Area Name"})
    return labels


def main():
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise SystemExit("Set CENSUS_API_KEY first (see the docstring).")

    ACS_DIR.mkdir(parents=True, exist_ok=True)
    for prefix, path, table in TABLES:
        df = fetch_table(path, table, key)
        labels = fetch_labels(path, table, key)
        label_row = pd.DataFrame([{c: labels.get(c, c) for c in df.columns}])

        out = ACS_DIR / f"{prefix}.{table}-Data.csv"
        pd.concat([label_row, df]).to_csv(out, index=False)
        print(f"{table}: {len(df)} ZCTAs -> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
