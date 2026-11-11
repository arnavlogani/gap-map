# 2026-11-10 · Need score: combine, test, finalize

## Found

z_direct and z_indirect agree moderately: rank correlation 0.65, or 0.74 for ZCTAs with at least 5,000 adults. 8 of PLACES' top 10 ZCTAs are also in the indirect top fifth. SNAP (0.67) and median income (0.62) track PLACES most closely. Severe housing burden (0.23) and no vehicle (0.31) track it least.

## Decided

### Null rule

- **Both sides present:** weighted sum, re-standardized so it has mean 0 and std 1.
- **One side null:** use the other side alone and flag the row (rule 7).
- **Both null (11042, 11973):** no score, shown as "no data" on the map.
- **Why re-standardize:** the two scores are correlated, so their weighted sum has a std of 0.85. Without rescaling, rows scored from one side alone would spread wider than combined rows.

### Weight: w = 0.6

- **Choice:** the code picks w from the 0.5–0.8 grid: the weight where need_score's rank correlation with z_direct is closest to its rank correlation with z_indirect, so the score agrees about equally with both sources. That gives w = 0.6 (0.895 with direct, 0.904 with indirect), the same value rule 6 planned.
- **Rule 6 failed:** 26.6% of ZCTAs (46 of 173) change quintile somewhere in the grid, above the 10% limit.
- **Used 0.6 anyway:** only one ZCTA moves more than one quintile. The other 45 move by one, at a quintile boundary.

### Flag large disagreements

- **Choice:** ZCTAs where z_direct and z_indirect are 1.5 or more apart are flagged low confidence.
- **Why:** when the two sources disagree that much, the combined score is an average of two different stories. 1.5 catches exactly the 9 largest disagreements below.

## Built

`transforms/need/need_insecurity_model.py`:

1. Merge direct and indirect on zcta5 (175 rows).
2. Combine with the null rule above.
3. Sensitivity: quintiles at each w from 0.5 to 0.8 in steps of 0.05, rank correlation between runs, and leave-one-out for each ACS indicator.
4. Final table and health checks.

## Outcome

- **need_final.csv:** 175 rows, one per ZCTA. Columns: zcta5, fi_rate, est_food_insecure_adults, z_direct, z_indirect, need_score, need_quintile, n_indicators, low_confidence.
- **sensitivity.csv:** each ZCTA's quintile at every weight.
- **Health checks:** all pass. need_score mean is 0.03. Quintile sizes are 35, 34, 35, 34, 35. Every null is explained.
- **Robustness:** any two weights rank ZCTAs similarly (rank correlation 0.93 or higher). Dropping any one indicator moves 12–20 ZCTAs, so no single indicator drives the result.
- **Flagged low confidence (20):** 8 with a side missing, 3 with under 500 adults, 9 for disagreement. 11042, 11549, 11553, 11569, 11575, 11717, 11726, 11732, 11770, 11794, 11798, 11931, 11941, 11947, 11955, 11956, 11959, 11970, 11973, 11975.
- **Largest disagreements:** two groups.
  - Indirect much higher than direct: small or seasonal ZCTAs (11955, 11975, 11569, 11959, 11941, 11732). Likely ACS sampling noise and second homes.
  - Direct much higher than indirect: Roosevelt (11575), Copiague (11726), Uniondale (11553). High need: incomes below the LI median ($121–128k vs $143k), SNAP use about 3× the LI median (11–14% vs 3.8%), and Uniondale's poverty rate in the top 10%. The ACS indicators average out near typical while PLACES ranks them near the top, so they're flagged for disagreement, not for low need.

## Open

- The need layer on the Foundry map.

## Links

Code: `transforms/need/need_insecurity_model.py`. Builds on [Modeling the need layer](../2026-11-09-need-modeling/) and [Need layer 2: indirect measures](../2026-11-10-need-layer-indirect/).
