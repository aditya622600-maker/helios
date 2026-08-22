# Data and provenance policy

## Person 1 handoff status

The checked-in Kharghar fixture is a real, redistributable public-data sample:

- 15 Google Open Buildings v3 polygons from official S2 level-4 tile `3bf`;
- 2023 Open Buildings Temporal v1 height and uncalibrated presence sampled at polygon
  centroids—13 of 15 candidates have a positive height observation;
- Kharghar AOI, OSM roads and mapped power context;
- a window-clipped Copernicus DEM GLO-30 terrain raster; and
- five contract-valid source records plus SHA-256 checksums under `data/manifests/`.

This is a fallback-only run: no GOBS state file is present. The fixture contains no usable-roof,
shading, PV-yield, price, rent, score or rank fields because those belong to Persons 2–4.

## Reproduction commands

Install the declared geospatial dependencies:

```powershell
python -m pip install -e ".[geo,dev]"
```

Recreate the building fixture from the official `3bf_buildings.csv.gz` shard and the two
official 2023 Temporal v1 COGs covering the AOI:

```powershell
python scripts/ingestion/build_p1_fixture.py `
  --buildings C:\path\to\3bf_buildings.csv.gz `
  --source-tile 3bf `
  --temporal-raster https://storage.googleapis.com/open-buildings-temporal-data/v1/geotiffs/3be7c_2023_06_30/tile_dWbk5h9MBWQ.tif `
  --temporal-raster https://storage.googleapis.com/open-buildings-temporal-data/v1/geotiffs/3be7c_2023_06_30/tile_lLHJwXyOP0k.tif `
  --output data/sample/source_layers/candidate_buildings.geojson `
  --limit 15
```

The v3 shard is available from:

```text
https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/3bf_buildings.csv.gz
```

Recreate the terrain clip and validate the complete offline handoff:

```powershell
python scripts/ingestion/clip_copernicus_dem.py `
  --output data/sample/source_layers/kharghar_terrain.tif
python scripts/ingestion/validate_p1_handoff.py
```

Acquire a fresh full OSM context snapshot outside Git with:

```powershell
python scripts/ingestion/run_p1.py --output-dir data/processed
```

## Identity and missing-data rules

Google Open Buildings v3 publishes Plus Code, centroid, confidence, area and WKT, but no
upstream row identifier. Helios therefore labels `source_record_key` as a derived surrogate:
`sha256(tile|plus_code|normalized_source_wkt)`. `candidate_id` is derived from that digest and
does not depend on row order. The original Plus Code, source confidence, tile and geometry are
preserved.

Temporal v1 is a raster, not a table that can be joined by row number. The fixture samples the
2023 height and building-presence bands at the v3 polygon centroid and records the COG URI,
year, method and effective resolution. Height `0` or nodata becomes null. A legitimate sampled
height of `14.0 m` remains `14.0 m`; values are never deleted merely because they equal a
previously used synthetic constant.

The presence score is uncalibrated and must not be interpreted as a probability. Person 2 owns
height fusion and confidence calculation.

## Data-quality summary

| Check | Fixture result |
|---|---:|
| Google v3 candidate polygons | 15 |
| Unique stable candidate IDs | 15 |
| Valid source geometries | 15 |
| Positive Temporal v1 height observations | 13 |
| Missing Temporal v1 heights | 2 |
| Downstream feature or ranking fields | 0 |
| GeoLibre layers with relative paths and attribution | 5 |

## Minimum manifest

Every external dataset must have a `SourceManifest` before its features can enter a scored run.
`data/manifests/source_manifest.json` is a JSON array whose members each validate against
`helios.contracts.models.SourceManifest`. It records the provider, direct citation URL, license,
retrieval timestamp, version, temporal validity, spatial resolution and limitations.

## Storage zones

- `data/manifests/`: small, reviewable metadata committed to Git.
- `data/sample/`: tiny redistributable fixtures only.
- `data/raw/`: ignored; immutable downloads with checksums.
- `data/processed/`: ignored; reproducible derivatives.
- PostGIS: candidate geometries, feature tables and analysis runs.

## Rules

1. Never commit credentials, restricted imagery, personal data or bulk source rasters.
2. Keep original CRS and checksum metadata; use EPSG:4326 for exchange.
3. Missing observations remain missing and reduce confidence; they are not silently set to zero.
4. Record whether access is direct, request-only or credentialed.
5. Optional enrichment uses a documented spatial match and never joins by row order.
6. Do not commit requested GOBS bulk data until redistribution terms permit it.

The GOBS fallback and owner actions are defined in
[GOBS access finding and executable fallback](GOBS_ACCESS_AND_FALLBACK.md) and
[ADR 0004](../architecture/decisions/0004-gobs-is-optional-enrichment.md).
