# 2026-11-09 · Modeling the need layer

## Found

Two kinds of need data. **Direct:** PLACES food insecurity, which measures the right thing but is modeled. **Indirect:** 7 ACS indicators, which are measured but are proxies. They're in different units, so they can't be combined as is.

## Decided

### Combine them with z-scores

- **Choice:** z-score every indicator across the 175 LI ZCTAs, average the indirect ones, then `need_score = w × z_direct + (1 − w) × z_indirect`.
- **Why:** z-scores put % and $ on one scale ("how far from the LI average"), and averaging keeps one number from deciding a ZCTA's color.
- **Output:** `need_score` ranks ZCTAs for the map. Counts come from `fi_rate × adults`.

### Rules (set before computing)

1. **175 ZCTAs.** Added 11549 and 11709. The list is fixed first, because z-scores depend on it.
2. **Indicators:** SNAP, poverty, child poverty, senior poverty, median income (flipped), severe housing burden, no vehicle. All rates, all at ZCTA level.
3. **Missing:** at least 4 of 7 indicators, otherwise z_indirect is null.
4. **Overlap:** if two indicators correlate above 0.85, drop one.
5. **Weights:** w from 0.5 to 0.8, leaning direct because only PLACES measures food insecurity itself.
6. **Robustness:** if under 10% of ZCTAs change quintile across the weights, use w = 0.6.
7. **Low confidence:** under 500 adults, or one side null (score uses the other side).
8. **Cut:** PLACES confidence intervals. The 500-adult rule covers it.
