# 2026-10-18 · SNAP by ZCTA

*Superseded on 2026-11-10: ACS tables, including S2201, are now pulled from the Census API by `transforms/need/fetch_acs.py`. See [Need layer 2: indirect measures](../2026-11-10-need-layer-indirect/).*

## Found

ACS table S2201 (Food Stamps/SNAP) has SNAP receipt, poverty and income by ZCTA. data.census.gov limits geographies per export, so Long Island came down as 6 extracts by ZCTA range: 2 Nassau, 4 Suffolk. Same columns, one row per ZCTA.

## Decided

### Union the extracts, don't join them

- **Options:** join or union.
- **Choice:** union.
- **Why:** same grain and schema, different rows. A join on same-grain data gives many-to-many duplicates or side-by-side columns. A union appends rows and keeps one row per ZCTA.
- **Consequences:** ZCTA must be unique after the union.

## Built

Pipeline Builder, output to the L.I. SNAP dataset.

<!-- Screenshot: pipeline.png -->
*Pipeline screenshot to add.*

1. **Load** the 6 extracts.
2. **Select columns:** households, households below and above poverty, median income, ZCTA, SNAP and non-SNAP households (estimate, MOE, percent).
3. **Union** into one dataset.

## Outcome

One SNAP dataset for Long Island, one row per ZCTA.

## Open

- Row filtering not done.
- ZCTA uniqueness after the union not checked.
