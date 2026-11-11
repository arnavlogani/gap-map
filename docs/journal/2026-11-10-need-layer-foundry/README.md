# 2026-11-10 · Need layer in Foundry

## Found

`need_final.csv` and `sensitivity.csv` from [the need score entry](../2026-11-10-need-score/): 175 rows, one per ZCTA.

## Decided

### Polygons on the left of the join

- **Choice:** left join, ZCTA polygons ← need scores, on `zcta5`.
- **Why:** all 175 ZCTAs stay on the map. 11042 and 11973 show as "Insufficient data", not holes. Closes the open item from [2026-11-04](../2026-11-04-places-need-layer-1/).

### Map need class, not need score

- **Choice:** color by `need_quintile`, 1 (lowest) to 5 (highest), 5-step sequential scale.
- **Why:** a class is easier to act on than a z-score. "Highest need" = top fifth of Long Island, 35 ZCTAs.

### Mark low confidence, don't hide it

- **Choice:** warning marker on the 20 low-confidence ZCTAs, plus a filter.
- **Why:** they keep their class. Users directing food there see that sources disagree or data is thin.

### Sensitivity as its own dataset

- **Choice:** `sensitivity` → `zcta_need_sensitivity`, separate from the map dataset.
- **Why:** it backs the weight choice. The map needs only the class.

## Built

![Pipeline](pipeline.png)

1. **Inputs:** `zcta-polygons` (TIGER, [2026-10-25](../2026-10-25-zcta-polygons/)), `need_final`, `sensitivity`.
2. **Clean ZCTA polygons:** `zcta5` and geometry into their own columns.
3. **Clean need scores:** cast types; add need class label ("1 – Lowest need" to "5 – Highest need", or "Insufficient data").
4. **Join:** polygons left, need right, on `zcta5`. Output `zcta_gap_map`, 14 columns, backing the ZCTA object type.
5. **Clean sensitivity:** output `zcta_need_sensitivity`.
6. **Workshop app:** Gap Map, with Need, Supply and Gap tabs. Need built.

## Outcome

![Need layer: need class by ZCTA](map-need-class.png)

- **175 ZCTAs:** 35 / 34 / 35 / 34 / 35 per class, 2 insufficient data.
- **290,212 estimated food-insecure adults.** Matches `need_final.csv`.
- **20 low confidence.** Matches the need score entry.

## Open

- Supply layer: pantry locations and hours.
- Gap layer: need minus supply.

## Links

Builds on [Need score: combine, test, finalize](../2026-11-10-need-score/) and [ZCTA polygons on a Foundry map](../2026-10-25-zcta-polygons/).
