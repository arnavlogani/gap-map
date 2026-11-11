# 2026-11-09 · Modeling the need layer

## Found

Two kinds of need data:
- **Direct:** PLACES food insecurity. Measures the right thing; modeled.
- **Indirect:** 7 ACS indicators. Measured; proxies.

Different units. Can't be combined as is.

## Decided

### Combine with z-scores

- **Choice:** z-score every indicator across the 175 Long Island ZCTAs, average the indirect ones, then `need_score = w × z_direct + (1 − w) × z_indirect`.
- **Why:** z-scores put % and $ on one scale (distance from the Long Island average). Averaging keeps one indicator from deciding a ZCTA.
- **Output:** `need_score` ranks ZCTAs for the map. Counts come from `fi_rate × adults`.

### Rules, set before computing

1. **175 ZCTAs.** Added 11549 and 11709. Fixed first, because z-scores depend on the set.
2. **Indicators:** SNAP, poverty, child poverty, senior poverty, median income (flipped), severe housing burden, no vehicle. All rates, all at ZCTA level.
3. **Missing:** at least 4 of 7 indicators, else z_indirect is null.
4. **Overlap:** two indicators correlating above 0.85 → drop one.
5. **Weights:** w from 0.5 to 0.8. Leans direct: only PLACES measures food insecurity.
6. **Robustness:** under 10% of ZCTAs change quintile across the weights → use w = 0.6.
7. **Low confidence:** under 500 adults, or one side null (score uses the other side).
8. **Cut:** PLACES confidence intervals. The 500-adult rule covers it.
