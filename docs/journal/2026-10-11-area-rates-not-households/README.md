# 2026-10-11 · Area-level rates, not households

## Found

The starting plan (10/7): classify each household as food insecure with a model (random forest) and map the flagged households. Assumption: more granular is better.

A map of flagged households shows density, not rate. That's the wrong picture for food insecurity.

## Decided

### Map a rate per area, not flagged households

- **Options:** household grain (classify and map flags), or area grain (food-insecure households ÷ all households, per area).
- **Choice:** area grain. Each area gets a value from 0 to 1.
- **Why:**
  - **Density isn't rate.** Dense areas look high even when the share of insecure households is low.
  - **Error tolerance.** A 5% household misclassification changes the map. At area level it changes a shade.
  - **Decisions are made on aggregates.** A pantry is sited by area, not by household.
  - **Feasibility.** No public household-level data exists. National surveys get about 40k responses.
  - **Privacy.** Household data wouldn't be public, and isn't used here ([data governance](../../data-governance.md)).
- **Consequences:** modeling combines area-level indicators instead of classifying households.

## Outcome

Target: the smallest geographic unit where a food-insecurity rate can be estimated with a usable confidence interval. Candidates: tract, ZIP code, school district.

Ingestion requirements:
- **Use case:** analytical. The data feeds a model that finds the gap.
- **Updates:** on new source releases, supply changes, and operations writeback.
- **Volume:** small. Optimize for low cost and infrequent ingestion.

## Open

- Unit choice: [2026-10-14](../2026-10-14-unit-storage-ingestion/).
- Mentor ideas, not scoped:
  - Highlight food-insecure areas next to affluent ones.
  - Show the nonprofit's outreach areas on the map.
  - Child focus: density of families with young children; possibly weight WIC higher.
  - Low-effort giving, e.g. routing food that would spoil before a vacation to a nearby drop-off.
