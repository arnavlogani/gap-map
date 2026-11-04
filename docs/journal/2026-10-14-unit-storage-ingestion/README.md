# 2026-10-14 · Unit of analysis, storage, and ingestion

## Found

[2026-10-11](../2026-10-11-area-rates-not-households/) left three candidate units: census tract, ZIP Code Tabulation Area (ZCTA), and school district. With the need indicators listed, the next questions were where the data lives in Foundry and how it gets there.

## Decided

### ZCTA as the first unit

- **Options:**
  - **Tract.** Smallest standard census unit and widely published, but tracts mean nothing to the people using the map.
  - **ZCTA.** Close to ZIP codes, which people already know. ACS, CDC PLACES, and TIGER boundaries are all published at ZCTA level.
  - **School district.** Free and reduced lunch data is strong here, but the boundaries don't line up with census units.
- **Choice:** ZCTA for v1. Tract and school district are still open.
- **Why:**
  - The core sources and the boundaries are all at ZCTA level, so v1 needs no crosswalk.
  - Users think in ZIP codes.
  - Mentor guidance: ship a simple, imperfect baseline instead of designing the perfect one forever.
- **Consequences:**
  - County-only and school-district sources (WIC, free lunch, Feeding America) need a crosswalk or must stay as calibration checks.
  - ZCTAs aren't ZIP codes. Some ZIPs (PO boxes, single buildings) have no ZCTA, and some ZCTAs have almost no population.

### Foundry datasets, not Iceberg tables

- **Options:** Apache Iceberg tables (open table format with schema evolution, hidden partitioning, partition layout evolution, and time travel) or native Foundry datasets.
- **Choice:** Foundry datasets.
- **Why:** Iceberg's advantages matter most for interoperability with an external Iceberg stack, which this project doesn't have. Volume is small and ingestion infrequent. Datasets work directly with Pipeline Builder, the Ontology, and Map.
- **Consequences:** revisit if data needs to be shared outside Foundry or volume grows a lot (for example, streaming supply data).

### Manual upload, no Data Connection

- **Options:** Data Connection (scheduled syncs from source systems) or manual upload of downloaded files.
- **Choice:** manual upload. Every file is logged in [`data/sources.md`](../../../data/sources.md) with its URL and the date it was pulled.
- **Why:** every source is a public file with an annual or slower refresh cycle (ACS 5-year, PLACES, TIGER). There's no live system to connect to.
- **Consequences:**
  - Refreshes are manual, and `sources.md` is the only record of what was pulled and when.
  - Revisit for the supply layer, where pantry hours change often.

## Open

- USDA's survey sample (about 40k nationwide) is too small for Long Island estimates. Use it for calibration only.
- The county-level food-insecurity rate differs by about 4× between Feeding America and NYS DOH. Reconcile against the sources before publishing.
- Double counting across indicators (a SNAP household is also likely a free-lunch household). Weighting method TBD.
