# 2026-11-10 · Need layer 2: indirect measures (ACS)

## Found

PLACES gaps:
- Adults 18+ only.
- Built partly from census poverty data.
- Fixed to 2020 population counts.

## Decided

### Seven ACS indicators, equal weights

- **Indicators (ACS 5-year 2020–2024, ZCTA):** SNAP receipt, poverty, child poverty, senior poverty, median household income, severe housing burden, households without a vehicle.
- **Method:** each a rate, z-scored across the 175 ZCTAs, income flipped so higher = more need, averaged into z_indirect.
- **Weights:** equal, as planned. Rejected:
  - Judgment weights: not supported by the data.
  - Weights by agreement with PLACES: would make z_indirect a copy of z_direct.
- **Re-standardized** z_indirect after averaging, so it carries its intended share when combined with z_direct.
- **Overlap check:** no pair above 0.85. All seven kept.

## Built

- `transforms/need/fetch_acs.py`: pulls the 6 ACS tables from the Census API.
- `transforms/need/indirect_acs.py`: rates, health checks (row count, unique `zcta5`, rate range, missing values, correlation), z_indirect.

## Outcome

z_indirect for 169 of 175 ZCTAs. The other 6:

- **Brentwood (11717), Wyandanch (11798):** Census suppressed the 2019–2023 and 2020–2024 5-year estimates after a 2020 data collection error ([Errata #148](https://www.census.gov/programs-surveys/acs/technical-documentation/errata/148.html)).
- **Hofstra (11549), Stony Brook (11794):** college ZCTAs. Dorm residents are group quarters: not households, no poverty status. Too few indicators published; fail the 4-of-7 rule.
- **11042, 11973:** very small or non-residential. Also missing from PLACES.

Direct and indirect join on all 175 ZCTAs. Rank correlation 0.65.
- Direct only: 11549, 11717, 11794, 11798.
- Indirect only: 11931, 11947.
- Neither: 11042, 11973.

## Open

- Children partly covered (child poverty, household SNAP). School lunch and WIC aren't available by ZCTA.
- Rule needed for the 2 ZCTAs with no data on either side. Show as "no data".

## Links

Sources: [`data/sources.md`](../../../data/sources.md). Builds on [2026-11-09 · Modeling the need layer](../2026-11-09-need-modeling/).
