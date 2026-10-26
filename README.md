# Gap Map

A ZCTA-level heatmap of food insecurity on Long Island (Nassau and Suffolk counties), built on Palantir Foundry. For PanRelief 501(c)(3).

## How it works

Three layers:

1. **Need**:  Existing measurements of food insecuirty (Feeding America / USDA) + Direct and Indirect indicators of food insecurity (SNAP, WIC, free lunch, 211 calls, ACS poverty, Income, Seniors etc...). Modeled into a conclusion about Food Insecurity per Zip Code Tablulation Area (ZCTA).

2. **Supply**: Food bank, pantry and agency locations + their hours and capacity.

3. **Gap**: Need versus supply. Geo-Pointed and put on a Heatmap.

## Repo layout
| Path | Description |
|---|---|
| `transforms/` | Code copied out of Foundry at the end of each session (`need/`, `supply/`, `gap/`). Pipeline Builder graphs are documented in `docs/` as screenshots + step lists. |
| `ontology/` | The object types and links. |
| `docs/` | Methodology, decision log, data governance, map images. |
| `data/sources.md` | Every dataset: source, URL, geography, date pulled. The datasets themselves are never committed. |

## Data sources

See [`data/sources.md`](data/sources.md).

## Status

| Milestone | Date | Status |
|---|---|---|
| 1. Need map | Oct 26 | in progress |
| 2. Gap map | Nov 1 | |
| 3. Hot zones | Nov 8 | |
| 4. Docs | Nov 11 | |
| 5. Ship | Nov 14 | |

Every line in this repo is written by hand.
