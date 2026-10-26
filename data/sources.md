# Data sources

One row per dataset. The files themselves are never committed; this table is the record. Fill `Date pulled` and `Refresh cadence` from the source page the day you download.

Geography codes: ZCTA = ZIP Code Tabulation Area · tract = census tract · SD = school district · county.

## Need layer — ingested

| Dataset | Source | URL | Geography | Columns kept | Date pulled | Refresh cadence | Feeds |
|---|---|---|---|---|---|---|---|
| SNAP + poverty + income, Nassau | US Census, ACS (table S2201 / B22010 — confirm) | data.census.gov | ZCTA (24) | households, below/above poverty, median income, SNAP recipient est + MOE + pct, non-SNAP est + MOE + pct | | ACS 5-yr, annual | need |
| SNAP + poverty + income, Suffolk | US Census, ACS (same table) | data.census.gov | ZCTA (27) | same | | ACS 5-yr, annual | need |

## Need layer — identified, not yet ingested

| Dataset | Source | URL | Geography | Notes | Feeds |
|---|---|---|---|---|---|
| Food insecurity rate + meal gap | Feeding America, Map the Meal Gap | | county | the headline number to reconcile: FA 5.2% / 4.4% vs NYS DOH 23.1% / 21.1% — recheck both against source before publishing | need |
| Food insecurity | USDA ERS | | national / state | ~40k sample nationwide; use for calibration, not LI estimates | need |
| 211 calls, food-related | 211 Long Island counts | https://longisland.211counts.org | ZIP / county | aggregate counts only; raw call records are never used | need |
| WIC enrollment | NYS DOH | https://health.data.ny.gov/Health/New-York-State-Monthly-WIC-Enrollment-and-Particip/5fre-5bds | county, monthly | | need |
| Free / reduced lunch | NYS Kids' Well-being Indicators (KWIC) | https://kwic.ny.gov/get_data/county_report_detail.cfm?countyid=36059&profileType=1 | county / SD | Nassau = 36059, Suffolk = 36103 | need |
| ALICE households | United for ALICE (United Way) | | county / place | | need |
| Housing cost burden, zero-vehicle households, children/seniors | US Census, ACS | data.census.gov | tract | | need |

## Geography

| Dataset | Source | URL | Notes |
|---|---|---|---|
| ZCTA boundaries, Long Island | ArcGIS Hub | https://hub.arcgis.com/datasets/85769018b43a4d1a96a4175a1e97d163_0 | GeoJSON export |
| ZCTA area + internal point lat/long | US Census | https://data.census.gov/table?q=latitude&g=860XX00US... | |
| ZCTA → tract crosswalk | HUD USPS Crosswalk | | needed before need layer joins at tract |

## Supply layer — identified

| Dataset | Source | Notes |
|---|---|---|
| Pantry locations and hours | Island Harvest + LI Cares public locators, OpenStreetMap | public pages only |
| Agency size | ProPublica Nonprofit Explorer (990s) | |
