# 2026-10-18 · SNAP by ZCTA

## Found

ACS table S2201 (Food Stamps/SNAP) has SNAP receipt, poverty, and income by ZCTA, which makes it the first direct need source to ingest. data.census.gov limits how many geographies one export can hold, so Long Island came down as separate extracts by ZCTA range: 2 for Nassau and 4 for Suffolk. Each extract has the same columns, one row per ZCTA.

## Decided

### Union the extracts, don't join them

- **Options:** join the extracts, or union them.
- **Choice:** union.
- **Why:** the extracts have the same grain and schema but different rows. Joining datasets at the same grain gives either many-to-many duplicates or columns stacked side by side. A union appends rows and keeps the grain: one row per ZCTA.
- **Consequences:** ZCTA must be unique after the union. Check for duplicates where extract ranges overlap.

## Built

Pipeline Builder, output to the L.I. SNAP dataset in the need layer folder.

<!-- Screenshot: pipeline.png -->
*Pipeline screenshot to add.*

1. **Load** the six extracts.
2. **Select columns.** S2201 has hundreds of columns. Keep the ones that feed the need layer:
   - number of households
   - households below and above the poverty line
   - median income
   - ZCTA
   - households receiving SNAP (estimate, margin of error, percent)
   - households not receiving SNAP (estimate, margin of error, percent)
3. **Union** into one dataset.

## Outcome

One SNAP dataset for Long Island, one row per ZCTA.

## Open

- Filter rows to the values needed. Not done yet.
- Check that ZCTA is unique after the union.
- Remaining direct sources: Feeding America and USDA food insecurity and meal gap, 211 calls, WIC, free lunch.
