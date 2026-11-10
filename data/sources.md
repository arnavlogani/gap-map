# Data sources

One row per dataset. The files themselves are never committed; this table is the record. Fill `Date pulled` and `Refresh cadence` from the source page the day you download.

Geography codes: ZCTA = ZIP Code Tabulation Area · tract = census tract · SD = school district · county.

## Need layer — ingested

| Dataset | Source | URL | Geography | Columns kept | Date pulled | Refresh cadence | Feeds |
|---|---|---|---|---|---|---|---|
| SNAP + poverty + income, Nassau | US Census, ACS (table S2201 / B22010 — confirm) | data.census.gov | ZCTA (24) | households, below/above poverty, median income, SNAP recipient est + MOE + pct, non-SNAP est + MOE + pct | | ACS 5-yr, annual | need |
| SNAP + poverty + income, Suffolk | US Census, ACS (same table) | data.census.gov | ZCTA (27) | same | | ACS 5-yr, annual | need |
| Food insecurity, SNAP, housing insecurity (+ ~35 other health measures) | CDC PLACES, 2025 release, ZCTA GIS-friendly format | https://data.cdc.gov/500-Cities-Places/PLACES-ZCTA-Data-GIS-Friendly-Format-2025-release/kee5-23sr | ZCTA (national, ~32.5k; 169 of 173 LI) | zcta5, foodinsecu_crudeprev (layer 1); crude 95% CIs and totalpop18plus planned for health checks | 2026-11-03 | annual | need |
| SNAP receipt | US Census, ACS 5-yr 2020–2024, S2201 | https://data.census.gov/table/ACSST5Y2024.S2201 | ZCTA (175 LI requested, 173 returned) | S2201_C01_001E, S2201_C03_001E | 2026-11-10 | annual | need (indirect) |
| Poverty: all, child, senior | US Census, ACS 5-yr 2020–2024, B17001 (S1701 not available for NY ZCTAs on data.census.gov) | https://data.census.gov/table/ACSDT5Y2024.B17001 | ZCTA (175 LI requested, 173 returned) | B17001_001E, _002E, under-18 and 65+ age groups | 2026-11-10 | annual | need (indirect) |
| Median household income | US Census, ACS 5-yr 2020–2024, B19013 | https://data.census.gov/table/ACSDT5Y2024.B19013 | ZCTA (175 LI requested, 173 returned) | B19013_001E | 2026-11-10 | annual | need (indirect) |
| Housing cost burden, renters | US Census, ACS 5-yr 2020–2024, B25070 | https://data.census.gov/table/ACSDT5Y2024.B25070 | ZCTA (175 LI requested, 173 returned) | B25070_001E, _010E | 2026-11-10 | annual | need (indirect) |
| Housing cost burden, owners | US Census, ACS 5-yr 2020–2024, B25091 | https://data.census.gov/table/ACSDT5Y2024.B25091 | ZCTA (175 LI requested, 173 returned) | B25091_001E, _011E, _022E | 2026-11-10 | annual | need (indirect) |
| Households with no vehicle | US Census, ACS 5-yr 2020–2024, B25044 | https://data.census.gov/table/ACSDT5Y2024.B25044 | ZCTA (175 LI requested, 173 returned) | B25044_001E, _003E, _010E | 2026-11-10 | annual | need (indirect) |

The six ACS tables are pulled from the Census API by `transforms/need/fetch_acs.py` (needs a free key in `CENSUS_API_KEY`). The URLs above are the same tables on data.census.gov.

**11717 (Brentwood) and 11798 (Wyandanch):** ACS 2019–2023 and 2020–2024 are suppressed by the Census Bureau for these areas and every smaller area inside them ([Errata #148](https://www.census.gov/programs-surveys/acs/technical-documentation/errata/148.html), a 2020 data collection error). The API omits them entirely, so their ACS indicators are null.

## Need layer — identified, not yet ingested

| Dataset | Source | URL | Geography | Notes | Feeds |
|---|---|---|---|---|---|
| Food insecurity rate + meal gap | Feeding America, Map the Meal Gap | | county | the headline number to reconcile: FA 5.2% / 4.4% vs NYS DOH 23.1% / 21.1% — recheck both against source before publishing | need |
| Food insecurity | USDA ERS | | national / state | ~40k sample nationwide; use for calibration, not LI estimates | need |
| 211 calls, food-related | 211 Long Island counts | https://longisland.211counts.org | ZIP / county | aggregate counts only; raw call records are never used | need |
| WIC enrollment | NYS DOH | https://health.data.ny.gov/Health/New-York-State-Monthly-WIC-Enrollment-and-Particip/5fre-5bds | county, monthly | | need |
| Free / reduced lunch | NYS Kids' Well-being Indicators (KWIC) | https://kwic.ny.gov/get_data/county_report_detail.cfm?countyid=36059&profileType=1 | county / SD | Nassau = 36059, Suffolk = 36103 | need |
| ALICE households | United for ALICE (United Way) | | county / place | | need |

## Geography

| Dataset | Source | URL | Notes |
|---|---|---|---|
| ZCTA boundaries | US Census TIGER/Line 2026, ZCTA5 (`tl_2026_us_zcta520`) | https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html | Shapefile, national. Filtered to LI and converted to GeoJSON by `transforms/geography/shapefile_to_geojson.py`. In use |
| ZCTA boundaries, Long Island | ArcGIS Hub | https://hub.arcgis.com/datasets/85769018b43a4d1a96a4175a1e97d163_0 | GeoJSON export. Not used; replaced by TIGER |
| ZCTA area + internal point lat/long | US Census | https://data.census.gov/table?q=latitude&g=860XX00US... | |
| ZCTA → tract crosswalk | HUD USPS Crosswalk | | needed before need layer joins at tract |

## Supply layer — identified

| Dataset | Source | Notes |
|---|---|---|
| Pantry locations and hours | Island Harvest + LI Cares public locators, OpenStreetMap | public pages only |
| Agency size | ProPublica Nonprofit Explorer (990s) | |
