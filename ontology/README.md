# Ontology

Six object types and their links. Drafted at milestone 2 (Nov 1).

| Object type | Grain | Source dataset | Key properties |
|---|---|---|---|
| Area | ZCTA → tract | geography | geoid, name, county, geometry, centroid |
| NeedEstimate | Area × period | need layer | rate, CI, indicators used |
| Agency | one per org | supply layer | name, location, hours, size |
| SupplyEstimate | Area × period | supply layer | |
| Gap | Area × period | gap layer | need − supply, rank |
| Task | one per action | writeback | agency, area, status |

Links: Area ↔ NeedEstimate, Area ↔ SupplyEstimate, Area ↔ Gap, Agency → Area, Task → Gap.

Open question: whether ZCTA geometry comes in as a dataset with a geo column or directly as an object type with a geopoint/geoshape property.
