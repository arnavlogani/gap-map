# 2026-11-10 · Need layer 2: indirect measures (ACS)

## Found

PLACES, our direct measure, is a modeled estimate with gaps: it only covers adults 18 and over, it is built partly from census poverty data, and it is fixed to 2020 population counts. To cover what it misses, we added an indirect measure from the 2020–2024 American Community Survey: seven indicators at the ZCTA level (SNAP receipt, poverty, child poverty, senior poverty, median household income, severe housing burden and households without a vehicle). Each was turned into a rate, z-scored across the 175 Long Island ZCTAs (income flipped so higher always means more need), and averaged with equal weights into one score, z_indirect. We ran health checks on the data (row counts, rate ranges, missing values, and correlations between indicators) and kept all seven, since none overlapped enough to drop. The result is one indirect need score per ZCTA, ready to combine with the direct score.

## Decided

We used equal weights, as planned in the last entry. We tried weighting by judgment and by how closely each indicator tracks PLACES, but neither held up: the judgment weights weren't supported by the data, and matching PLACES would just make the indirect score a copy of the direct one. We also re-standardized z_indirect after averaging so it carries its intended share when combined with z_direct.

## Outcome

z_indirect is calculated for 169 of the 175 ZCTAs. The other 6 have too little data:

- **Brentwood (11717) and Wyandanch (11798):** the Census Bureau suppressed the 2019–2023 and 2020–2024 5-year estimates for these areas after a 2020 data collection error ([Errata #148](https://www.census.gov/programs-surveys/acs/technical-documentation/errata/148.html)).
- **Hofstra (11549) and Stony Brook (11794):** college ZCTAs. Most residents live in dorms, which the Census counts as group quarters: they aren't households, and their poverty status isn't determined. With almost no households or poverty population, too few indicators are published, so these fall under the 4-of-7 rule.
- **11042 and 11973:** very small or non-residential ZCTAs, also missing from PLACES.
 The indirect and direct outputs join on all 175 ZCTAs, and the two scores agree moderately (rank correlation 0.65). Four ZCTAs have only a direct score (11549, 11717, 11794, 11798), two have only an indirect score (11931, 11947), and two have neither (11042, 11973).

## Open

Children are only partly covered (through child poverty and household SNAP). School lunch and WIC data could fill that gap, but neither is available by ZCTA yet. The combined score needs a rule for the two ZCTAs with no data on either side; they should show as "no data" on the map.

## Links

Code: `transforms/need/indirect_acs.py`. Sources: `data/sources.md`. Builds on [2026-11-09 · Modeling the need layer](../2026-11-09-need-modeling/).
