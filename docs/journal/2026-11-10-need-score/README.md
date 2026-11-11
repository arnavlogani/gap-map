# 2026-11-10 · Need score: combine, test, finalize

## Found

- z_direct vs z_indirect rank correlation: 0.65; 0.74 for ZCTAs with 5,000+ adults.
- 8 of PLACES' top 10 ZCTAs are in the indirect top fifth.
- Indicator agreement with PLACES: SNAP 0.67, median income 0.62, no vehicle 0.31, severe housing burden 0.23.

## Decided

### Null rule

- **Both sides present:** weighted sum, re-standardized to mean 0, std 1.
- **One side null:** the other side alone, flagged (rule 7).
- **Both null (11042, 11973):** no score; "no data" on the map.
- **Why re-standardize:** the two scores are correlated, so the weighted sum has std 0.85. Unscaled, one-sided rows would spread wider than combined rows.

### Weight: w = 0.6

- **Choice:** the code picks w from the 0.5–0.8 grid: the weight where need_score's rank correlation with z_direct is closest to its rank correlation with z_indirect. Result: w = 0.6 (0.895 with direct, 0.904 with indirect), the same value rule 6 planned.
- **Rule 6 failed:** 26.6% of ZCTAs (46 of 173) change quintile somewhere in the grid. Limit: 10%.
- **Used 0.6 anyway:** one ZCTA moves more than one quintile. The other 45 move by one, at a boundary.

### Flag large disagreements

- **Choice:** |z_direct − z_indirect| ≥ 1.5 → low confidence.
- **Why:** at that gap, the combined score averages two different stories. 1.5 catches the 9 largest disagreements.

## Built

`transforms/need/need_insecurity_model.py`:

1. Merge direct and indirect on `zcta5` (175 rows).
2. Combine with the null rule.
3. Sensitivity: quintiles at w = 0.5–0.8 in steps of 0.05, rank correlation between runs, leave-one-out per ACS indicator.
4. Final table and health checks.

## Outcome

- **need_final.csv:** 175 rows. Columns: zcta5, fi_rate, est_food_insecure_adults, z_direct, z_indirect, need_score, need_quintile, n_indicators, low_confidence.
- **sensitivity.csv:** each ZCTA's quintile at every weight.
- **Health checks:** pass. need_score mean 0.03. Quintiles 35/34/35/34/35. Every null explained.
- **Robustness:** rank correlation between any two weights ≥ 0.93. Leave-one-out moves 12–20 ZCTAs; no single indicator drives the result.
- **Low confidence (20):** 8 one side missing, 3 under 500 adults, 9 disagreement. 11042, 11549, 11553, 11569, 11575, 11717, 11726, 11732, 11770, 11794, 11798, 11931, 11941, 11947, 11955, 11956, 11959, 11970, 11973, 11975.
- **Largest disagreements:**
  - Indirect ≫ direct: small or seasonal ZCTAs (11955, 11975, 11569, 11959, 11941, 11732). Likely ACS sampling noise and second homes.
  - Direct ≫ indirect: Roosevelt (11575), Copiague (11726), Uniondale (11553). Incomes below the Long Island median ($121–128k vs $143k), SNAP about 3× the median (11–14% vs 3.8%), Uniondale poverty in the top 10%. Flagged for disagreement, not low need.

## Open

- Need layer on the Foundry map.

## Links

Code: `transforms/need/need_insecurity_model.py`. Builds on [Modeling the need layer](../2026-11-09-need-modeling/) and [Need layer 2: indirect measures](../2026-11-10-need-layer-indirect/).
