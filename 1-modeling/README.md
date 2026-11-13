# 1 · Modeling

How public data becomes one need score and one need class per Long Island ZCTA.

## The question

Where on Long Island is food need highest, at the smallest area where a food-insecurity rate can be estimated with usable confidence?

## Unit: a rate per area

- **Not households.** The first plan was to classify households with a model and map the flagged ones. That map shows density, not rate. It is also fragile: a 5% misclassification changes it. And no public household-level data exists.
- **ZCTA, not tract or school district.** CDC PLACES, Census ACS and TIGER boundaries all publish at ZCTA level, so no crosswalk is needed. People also know their ZIP codes.
- **175 ZCTAs.** The Long Island list was fixed before computing anything, because z-scores depend on the set. It includes 11549 (Hofstra) and 11709 (Bayville).

## Two kinds of evidence

| | Source | What it is | Coverage |
|---|---|---|---|
| **Direct** | CDC PLACES 2025, `foodinsecu_crudeprev` | Measures the right thing; modeled from BRFSS | 171 / 175 |
| **Indirect** | 7 ACS 5-year (2020–2024) indicators | Measured; proxies | 169 / 175 |

**Indirect indicators:** SNAP receipt, poverty, child poverty, senior poverty, median household income (flipped), severe housing cost burden, and households with no vehicle. All are rates at ZCTA level.

## Method

```
z_direct   = z(food insecurity rate)
z_indirect = z( mean of 7 indicator z-scores )        # re-standardized
need_score = z( 0.6 × z_direct + 0.4 × z_indirect )   # re-standardized
need_class = quintile(need_score)                      # 1 – 5
```

Z-scores put percentages and dollars on one scale: the distance from the Long Island average. Averaging the indicators keeps any one of them from deciding a ZCTA.

### Rules, set before computing

1. **The set:** 175 ZCTAs.
2. **Indicators:** the 7 above, equally weighted. Two alternatives were rejected:
   - Judgment weights: the data doesn't support them.
   - Weights fit to agree with PLACES: they would turn z_indirect into a copy of z_direct.
3. **Missing:** z_indirect needs at least 4 of the 7 indicators.
4. **Overlap:** drop one of any pair of indicators correlated above 0.85. No pair was, so all 7 stayed.
5. **Weight grid:** w from 0.5 to 0.8, leaning direct, because only PLACES measures food insecurity.
6. **Robustness target:** under 10% of ZCTAs change quintile across the grid.
7. **Nulls:**
   - Both sides present: the weighted sum.
   - One side null: the other side alone, flagged low confidence.
   - Both null: no score.
8. **Low confidence:** any of the following:
   - under 500 adults
   - one side missing
   - |z_direct − z_indirect| ≥ 1.5

### Weight: w = 0.6

The code picks the w where need_score's rank correlation with each source is most equal. That is 0.895 with direct and 0.904 with indirect, at w = 0.6.

**Rule 6 failed:** 26.6% of ZCTAs (46 of 173) change quintile somewhere in the grid. w = 0.6 was kept anyway: 45 of the 46 move by one class at a boundary, and only one moves more. The rank correlation between any two weights is ≥ 0.93. Leaving out any single indicator moves 12–20 ZCTAs, so no indicator drives the result.

## What came out

- **175 ZCTAs.** Classes hold 35 / 34 / 35 / 34 / 35 ZCTAs, and 2 have insufficient data (11042, 11973).
- **290,212 estimated food-insecure adults:** `fi_rate × adults`.
- **Direct vs. indirect:** Spearman ρ = 0.65 (0.74 for ZCTAs with 5,000+ adults). 8 of PLACES' top 10 are in the indirect top fifth.
- **20 low confidence:** 8 with one side missing, 3 under 500 adults, 9 where the sources disagree.

### The nulls, explained

| ZCTA | Why |
|---|---|
| 11717 Brentwood, 11798 Wyandanch | ACS 2019–23 and 2020–24 suppressed by the Census Bureau after a 2020 collection error ([Errata #148](https://www.census.gov/programs-surveys/acs/technical-documentation/errata/148.html)) |
| 11549 Hofstra, 11794 Stony Brook | College ZCTAs. Dorm residents are group quarters with no poverty status, so they fail the 4-of-7 rule |
| 11931, 11947 | No PLACES row |
| 11042, 11973 | Very small or non-residential; neither source |

### The disagreements

- **Indirect ≫ direct:** small or seasonal ZCTAs (11955, 11975, 11569, 11959, 11941, 11732). Likely causes are ACS sampling noise and second homes.
- **Direct ≫ indirect:** Roosevelt (11575), Copiague (11726), Uniondale (11553). Their incomes are below the Long Island median and their SNAP receipt is about 3× it. They are flagged for disagreement, not low need.

## Code

Run in order. The last three scripts assert health checks on their output: row count, unique `zcta5`, rate ranges, explained nulls.

| Script | Does |
|---|---|
| [`fetch_acs.py`](code/fetch_acs.py) | Pulls the 6 ACS tables from the Census API (needs `CENSUS_API_KEY`) |
| [`direct_food_insecurity.py`](code/direct_food_insecurity.py) | PLACES food-insecurity rate → `z_direct` |
| [`indirect_acs.py`](code/indirect_acs.py) | 7 ACS rates, correlation check → `z_indirect` |
| [`need_insecurity_model.py`](code/need_insecurity_model.py) | Combine, sensitivity across weights, final table → `need_final.csv`, `sensitivity.csv` |

## Sources

Public data only. The files are not committed.

| Dataset | Source | Geography | Pulled |
|---|---|---|---|
| Food insecurity | [CDC PLACES, ZCTA, 2025 release](https://data.cdc.gov/500-Cities-Places/PLACES-ZCTA-Data-GIS-Friendly-Format-2025-release/kee5-23sr) | ZCTA | 2026-11-03 |
| SNAP receipt | [ACS 5-yr 2024, S2201](https://data.census.gov/table/ACSST5Y2024.S2201) | ZCTA | 2026-11-10 |
| Poverty: all, child, senior | [ACS 5-yr 2024, B17001](https://data.census.gov/table/ACSDT5Y2024.B17001) | ZCTA | 2026-11-10 |
| Median household income | [ACS 5-yr 2024, B19013](https://data.census.gov/table/ACSDT5Y2024.B19013) | ZCTA | 2026-11-10 |
| Housing burden, renters / owners | [B25070](https://data.census.gov/table/ACSDT5Y2024.B25070), [B25091](https://data.census.gov/table/ACSDT5Y2024.B25091) | ZCTA | 2026-11-10 |
| No vehicle | [ACS 5-yr 2024, B25044](https://data.census.gov/table/ACSDT5Y2024.B25044) | ZCTA | 2026-11-10 |
| ZCTA boundaries | [Census TIGER/Line 2026, ZCTA5](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) | ZCTA | 2026-10 |
| Food pantries and meal sites | [map.thefoodpantries.org](https://map.thefoodpantries.org) | point | 2026-11 |
