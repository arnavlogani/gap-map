# 2026-10-11 · Area-level rates, not households

## Found

The starting plan (10/7) was a household-grain master dataset: combine direct and indirect indicators, feed them to a model (random forest), and classify each household as food insecure or not. The assumption was that more granular is always better.

Thinking through what the map would actually show broke that assumption. A heatmap usually shows density: how often something happens in one area compared with the areas around it. That's right for counting events and wrong for food insecurity.

## Decided

### Map a rate per area, not flagged households

- **Options:**
  1. Household grain. Classify each household and map the flags.
  2. Area grain. Map food-insecure households ÷ all households, per area.
- **Choice:** area grain. Each household is a yes or no, but each area gets a value between 0 and 1, and the color shows that value.
- **Why:**
  - **A map of flags shows density, not rate.** Dense areas look "hot" even when only a small share of households is food insecure.
  - **Error tolerance.** Household classification has to be near perfect. Being 5% wrong produces a different map. At the area level, the same error moves a shade.
  - **Decisions are made on aggregates.** Five, or fifty, insecure households in a row don't tell you where to put a pantry. You need the area, then the organizations in that area.
  - **Feasibility.** Household-level data doesn't exist publicly. National surveys get about 40k responses.
  - **Privacy.** If household data did exist, it wouldn't be public, and it shouldn't be used here (see [data governance](../../data-governance.md)).
- **Consequences:** modeling moves from classification to combining area-level indicators.

## Outcome

A working definition of the target: **the smallest geographic unit where a food-insecurity rate can be estimated with a usable confidence interval.** Candidates: tract, ZIP code, school district.

Ingestion requirements, from the data engineering fundamentals reading:
- **Use case:** analytical. The data feeds a model that finds the gap.
- **Updates:** when a need source publishes new data, when supply facts change, and when operations write back.
- **Volume:** small. Optimize for low cost and infrequent ingestion.

## Open

- Which unit? See [2026-10-14](../2026-10-14-unit-storage-ingestion/).

Ideas from a mentor conversation, not yet scoped:
- Highlight food-insecure areas that border affluent ones.
- Show the nonprofit's outreach areas on the map itself, not just in tasks.
- Add a child focus: density of families with young children, possibly weighting WIC more heavily.
- Make giving low-effort, for example routing food that would otherwise spoil (before a vacation) to a nearby drop-off.
