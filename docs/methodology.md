# Methodology

## Question

Where on Long Island does food need exceed food supply, at the smallest geographic unit where a food-insecurity rate can be estimated with a usable confidence interval?

## Unit of analysis

Target: ZCTA. School district and Census tract are still being considered.

### Why not household data?

Decision made Oct 2026, after starting from the assumption that more granular was better.

- A heatmap of flagged households shows density, not rate. Dense areas look "hot" even when the share of insecure households is low. The map needs a rate: insecure households ÷ all households per area.
- Household-level classification would need to be near-perfect; a 5% error rate changes the map. At the area level the same error moves a shade.
- Decisions (where to site a pantry, where to route food) are made on aggregates.
- Household-level data does not exist publicly and would not be published if it did.

## Need layer

Food insecurity, per area, estimated from:

- **Direct** — survey rates (Feeding America, USDA), observed demand (SNAP, WIC, free lunch, food-related 211 calls).
- **Indirect** — risk proxies: poverty, income, ALICE, housing cost burden > 50%, zero-vehicle households, children and seniors, disadvantaged students.

Open problems:
- Double counting across indicators (a SNAP household is also likely a free-lunch household). Weighting method TBD.
- Reconciling the county-level food-insecurity rate: Feeding America vs NYS DOH differ by ~4×.

## Storage

Foundry datasets, not Iceberg tables. Iceberg's advantages (schema evolution, hidden partitioning, time travel) matter for interoperability with an external Iceberg stack, which this project doesn't have. Data volume is small and ingestion infrequent.

## Ingestion

No Data Connection needed: all sources are public files downloaded and uploaded by hand. Logged per dataset in `data/sources.md`.

## Pipeline log

### 2026-10-25 · SNAP by ZCTA (Pipeline Builder)

*Graph screenshot: Coming Soon*
