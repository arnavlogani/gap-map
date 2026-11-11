# Gap Map: technical docs

The technical side of the project. For the map itself, see the [project README](../README.md).

## What this is

A ZCTA-level map of food need vs. food supply on Long Island (Nassau and Suffolk counties), built for PanRelief, a 501(c)(3), so it can see where food is needed most and send it there.

**Question:** Where on Long Island does food need exceed food supply, at the smallest geographic unit where a food-insecurity rate can be estimated with a usable confidence interval?

**Model:** three layers, one value per ZIP Code Tabulation Area (ZCTA).

1. **Need.** A food-need score per ZCTA, mapped as quintiles (1–5).
   - **Direct:** CDC PLACES modeled food-insecurity rate → `z_direct`.
   - **Indirect:** 7 ACS indicators (SNAP receipt, poverty, child poverty, senior poverty, median income, severe housing burden, no vehicle), z-scored and averaged → `z_indirect`.
   - **Score:** `0.6 × z_direct + 0.4 × z_indirect`, tested across weights 0.5–0.8.
2. **Supply.** Food bank, pantry, and agency locations, with hours and capacity.
3. **Gap.** Need minus supply, ranked per ZCTA.

## Stack

| | |
|---|---|
| Platform | Palantir Foundry: datasets, Pipeline Builder, Ontology, Map, Workshop |
| Local processing | Python: pandas, geopandas, requests |
| Data | US Census ACS 5-year (via the Census API) and TIGER/Line, CDC PLACES. All public, listed in [`data/sources.md`](../data/sources.md) |
| Version control | Git and GitHub. Pipeline Builder graphs are recorded as screenshots and step lists in the journal |

## Journal

One folder per session in [`journal/`](journal/): what was found, what was decided and why, what was built (with pipeline screenshots), and what came out (with map screenshots).

The journal is chronological, so **the most recent entry is the current state**. A decision stands until a later entry changes it. To start a new entry, copy [`journal/TEMPLATE.md`](journal/TEMPLATE.md).

| Date | Entry | Decisions |
|---|---|---|
| 2026-10-11 | [Area-level rates, not households](journal/2026-10-11-area-rates-not-households/) | Map a rate per area, not flagged households |
| 2026-10-14 | [Unit of analysis, storage, and ingestion](journal/2026-10-14-unit-storage-ingestion/) | ZCTA as the first unit · Foundry datasets, not Iceberg · Manual upload, no Data Connection |
| 2026-10-18 | [SNAP by ZCTA](journal/2026-10-18-snap-by-zcta/) | Union the extracts, don't join them · *Superseded 2026-11-10 by the Census API fetch* |
| 2026-10-25 | [ZCTA polygons on a Foundry map](journal/2026-10-25-zcta-polygons/) | TIGER polygons, not lat/long points |
| 2026-11-04 | [PLACES: need layer 1](journal/2026-11-04-places-need-layer-1/) | Two need layers, direct then indirect · PLACES properties, TIGER geometry · One object per ZCTA · Choropleth, not heatmap |
| 2026-11-09 | [Modeling the need layer](journal/2026-11-09-need-modeling/) | Combine direct and indirect with z-scores · Rules set before computing |
| 2026-11-10 | [Need layer 2: indirect measures](journal/2026-11-10-need-layer-indirect/) | Seven ACS indicators, equal weights · Brentwood and Wyandanch null (Census suppression) |
| 2026-11-10 | [Need score: combine, test, finalize](journal/2026-11-10-need-score/) | One-sided rows use the other side, flagged · w = 0.6 kept though rule 6 failed · Large disagreements flagged |
| 2026-11-10 | [Need layer in Foundry](journal/2026-11-10-need-layer-foundry/) | Polygons left of the join · Map need class, not score · Low confidence marked, not hidden |

## Elsewhere in the repo

| Path | What's there |
|---|---|
| [`data-governance.md`](data-governance.md) | What data is and isn't used, and what's public |
| [`../data/sources.md`](../data/sources.md) | Every dataset: source, URL, geography, date pulled. The data itself is never committed |
| [`../ontology/`](../ontology/) | The object types that matter |
| [`../transforms/`](../transforms/) | Code that ran outside Foundry or was copied out of Code Repositories |
