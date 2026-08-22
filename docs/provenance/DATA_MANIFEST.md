# HELIOS DATA PROVENANCE & QUALITY REPORT

**Generated:** 2026-08-22T10:16:02.098619+00:00

## 1. Layers & Provenance
### Google Open Buildings v3 & OpenStreetMap (`buildings`)
- **URL:** https://sites.research.google/open-buildings/ / https://www.openstreetmap.org
- **License:** ODbL 1.0 / CC-BY 4.0
- **Temporal Coverage:** 2023 - 2026
- **Known Limitations:** Direct building heights are sparse; missing heights are represented as null to avoid synthetic bias.

### OpenStreetMap Overpass API (Highways) (`roads`)
- **URL:** https://overpass-api.de/api/interpreter
- **License:** ODbL 1.0
- **Temporal Coverage:** 2026
- **Known Limitations:** Secondary and service roads mapped; informal access pathways may be unindexed.

### OpenStreetMap Power Infrastructure (`power`)
- **URL:** https://overpass-api.de/api/interpreter
- **License:** ODbL 1.0
- **Temporal Coverage:** 2026
- **Known Limitations:** Includes public substations and lines; low-voltage local distribution transformers may require on-site validation.

### Copernicus GLO-30 DEM (`terrain_elevation`)
- **URL:** https://spacedata.copernicus.eu/
- **License:** Open Data Policy
- **Temporal Coverage:** 2020
- **Known Limitations:** 30-meter ground spatial resolution.

## 2. SHA-256 Checksums
- `data/processed/kharghar_aoi.geojson`: `20db85540460bbc540949409c6002fb88ee7e7c75094f16409b4ecb15582b8b1`
- `data/processed/kharghar_buildings_clean.geojson`: `370a8a6833fedd74e95ff71c9f5d9cc6f91e75d719fb68b5ebd80c4e2136241b`
- `data/processed/kharghar_power.geojson`: `5a7c8949f895510ad15369ba7b9025d5e637ea57eb192d395bb51da1a0850d8c`
- `data/processed/kharghar_roads.geojson`: `f263e7c6c43b270e6322f56bd725840925664fef4dbc111f600618bb9dae41bc`
- `data/processed/solar_economic_inputs.json`: `2acea1dea2e871b640ad62ecc48e20e9b88f1dae1e257a726eeeaac5b66ad4b5`
- `data/sample/source_layers/kharghar_aoi.geojson`: `20db85540460bbc540949409c6002fb88ee7e7c75094f16409b4ecb15582b8b1`
- `data/sample/source_layers/kharghar_power.geojson`: `5a7c8949f895510ad15369ba7b9025d5e637ea57eb192d395bb51da1a0850d8c`
- `data/sample/source_layers/kharghar_roads.geojson`: `f263e7c6c43b270e6322f56bd725840925664fef4dbc111f600618bb9dae41bc`
- `data/sample/source_layers/sample_kharghar_buildings.geojson`: `c7738ae55b3d840b7f90e50178034d7d4946bd18b608da5acdf68e57a2922fbf`
- `data/sample/source_layers/solar_economic_inputs.json`: `2acea1dea2e871b640ad62ecc48e20e9b88f1dae1e257a726eeeaac5b66ad4b5`
