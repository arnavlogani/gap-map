# 2026-11-04 · PLACES: need layer 1 (direct food insecurity)

## Found

CDC PLACES (2025 release, ZCTA, GIS-friendly GeoJSON): about 32.5k ZCTAs, about 40 measures each, modeled from CDC's BRFSS survey. Direct need measures:

- `foodinsecu`: food insecurity
- `foodstamp`: SNAP receipt
- `housinsecu`: housing insecurity

Each has a crude prevalence (`_crudeprev`) and 95% CI (`_crude95ci`).

- **Geometry is a point (ZCTA centroid).** It can't be shaded as an area.
- **Every value is a string**, e.g. `"16.7"`, `"( 9.8, 13.3)"`.

## Decided

### Two need layers: direct, then indirect

- **Options:** one composite of every indicator, or a direct layer with indirect indicators added on top.
- **Choice:**
  - **Layer 1:** PLACES `foodinsecu_crudeprev`, mapped as is.
  - **Layer 2:** indirect indicators (poverty, income, housing burden, others), z-scored across Long Island ZCTAs and combined.
- **Why:** PLACES gives a food-insecurity rate for every ZCTA before any weighting decision. A separate layer 2 can be checked against it; disagreements are data errors or findings.
- **Consequences:**
  - PLACES is modeled, not observed, and inherits BRFSS model assumptions.
  - Its food-insecurity, SNAP and housing measures share one model. Not independent indicators for layer 2.

### PLACES properties, TIGER geometry

- **Options:** filter PLACES by ZCTA code in pandas, or geo-join in Pipeline Builder (PLACES centroids within TIGER polygons).
- **Choice:** geo-join in Pipeline Builder.
- **Why:** both datasets were already in Foundry. Locally, a `zcta5` code match and a point-in-polygon join both returned the same **169** ZCTAs, no mismatches.
- **Consequences:** 4 Long Island ZCTAs have no PLACES row (`11042`, `11931`, `11947`, `11973`). Holes on the map for now.

### One object per ZCTA, indicators as properties

- **Options:** an object type per layer, or one ZCTA object type that gains properties.
- **Choice:** one object per ZCTA. Primary key `zcta5`, geometry as geoshape, `food_insecurity_crude` as the first property.
- **Why:** every layer has the same grain. No joins between object types later.

### Choropleth, not heatmap

- **Choice:** shade each ZCTA polygon by its rate, sequential scale, Long Island min to max.
- **Why:** follows [2026-10-11](../2026-10-11-area-rates-not-households/). Foundry's heatmap layer shows point density.

## Built

![Pipeline](pipeline.png)

1. **Inputs:** TIGER Long Island ZCTA GeoJSON ([2026-10-25](../2026-10-25-zcta-polygons/)) and PLACES ZCTA GeoJSON.
2. **Join:** PLACES points within TIGER polygons. `properties` from PLACES, `geometry` from TIGER.
3. **Get struct field:** `zcta5`, `foodinsecu_crudeprev` → `food_insecurity_crude`.
4. **Cast** `food_insecurity_crude` to double.
5. **Select columns:** `zcta5`, `food_insecurity_crude`, `geometry`.
6. **Output:** `food-insecurity-by-geo-zcta`, backing the ZCTA object type, mapped by `food_insecurity_crude`.

## Outcome

169 of 173 ZCTAs, each with a rate and its boundary. Darker = higher share of food-insecure adults.

![Need layer 1: food insecurity, crude prevalence](map-food-insecurity-crude.png)

Darkest around Hempstead, Brentwood and Riverhead. North Shore mostly light.

## Open

- Health checks not built: nulls, prevalence range (3–40%), CI width, ZCTAs under 500 adults, duplicate `zcta5`.
- ZCTA list missing `11549` (Hempstead/Hofstra) and `11709` (Bayville). Both are in TIGER and PLACES. Add them to the Long Island ZCTA list, then regenerate and re-upload the polygons.
- The 4 ZCTAs without PLACES data: left join from the ZCTA side to show "no data".
- Layer 2: ACS indicators, z-scored, signs flipped so higher = more need, correlation check for double counting.

## Links

- Sources: CDC PLACES and Census TIGER in [`data/sources.md`](../../../data/sources.md).
- Builds on: [2026-10-25 ZCTA polygons](../2026-10-25-zcta-polygons/).
