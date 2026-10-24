# Gap Map

A ZCTA-level heatmap of food insecurity on Long Island (Nassau and Suffolk counties), built on Palantir Foundry for PanRelief.

## How it works

Three layers, each its own pipeline:

1. **Need** — public indicators of food insecurity (SNAP, WIC, free lunch, 211 calls, Feeding America / USDA estimates, ACS poverty and income), harmonized to a common geography and modeled into a per-area rate. 
2. **Supply** — pantry and agency locations, hours and capacity.
3. **Gap** — need versus supply, mapped.

Pipeline: raw uploads → Pipeline Builder (select, cast, union) → need dataset → ontology (six object types) → map. Decisions and rejected alternatives are logged in `docs/methodology.md`.

## Repo layout

| Path | What it holds |
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
