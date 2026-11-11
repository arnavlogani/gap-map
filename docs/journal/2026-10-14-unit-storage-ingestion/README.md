# 2026-10-14 · Unit of analysis, storage, and ingestion

## Found

Three candidate units from [2026-10-11](../2026-10-11-area-rates-not-households/): census tract, ZIP Code Tabulation Area (ZCTA), school district. Next: where the data lives in Foundry and how it gets there.

## Decided

### ZCTA as the first unit

- **Options:**
  - **Tract:** smallest standard census unit. Means nothing to map users.
  - **ZCTA:** close to ZIP codes. ACS, CDC PLACES and TIGER boundaries all publish at ZCTA level.
  - **School district:** strong free-lunch data. Boundaries don't match census units.
- **Choice:** ZCTA for v1. Tract and school district stay open.
- **Why:** core sources and boundaries are all at ZCTA level, so no crosswalk for v1. Users know ZIP codes. Mentor guidance: ship a simple baseline first.
- **Consequences:**
  - County and school-district sources (WIC, free lunch, Feeding America) need a crosswalk or serve as calibration only.
  - ZCTAs aren't ZIP codes. PO-box ZIPs have no ZCTA; some ZCTAs have almost no population.

### Foundry datasets, not Iceberg tables

- **Options:** Apache Iceberg tables (schema evolution, hidden partitioning, time travel) or native Foundry datasets.
- **Choice:** Foundry datasets.
- **Why:** Iceberg pays off for interoperability with an external Iceberg stack. There isn't one. Volume is small, ingestion infrequent. Datasets work directly with Pipeline Builder, the Ontology and Map.
- **Consequences:** revisit if data is shared outside Foundry or volume grows (e.g. streaming supply data).

### Manual upload, no Data Connection

- **Options:** Data Connection (scheduled syncs) or manual upload.
- **Choice:** manual upload, logged in [`data/sources.md`](../../../data/sources.md) with URL and date pulled.
- **Why:** every source is a public file refreshed annually or less (ACS 5-year, PLACES, TIGER). No live system to connect to.
- **Consequences:** refreshes are manual. Revisit for the supply layer, where pantry hours change often.

## Open

- USDA's sample (about 40k nationwide) is too small for Long Island. Calibration only.
- County food-insecurity rates differ about 4× between Feeding America and NYS DOH. Reconcile before publishing.
- Double counting across indicators (SNAP households are likely free-lunch households). Weighting TBD.
