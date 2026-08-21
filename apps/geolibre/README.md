# GeoLibre workspace contract

GeoLibre is the collection, inspection and visualization surface for Helios. The API remains the source of ranking logic.

## MVP setup

1. Start the API and create a run from `data/sample/analysis-request.json`.
2. Add `http://localhost:8000/analysis-runs/{run_id}/candidates.geojson` as a GeoJSON/HTTP layer, or save the response locally.
3. Style eligible candidates by `rank` or `total_score` and excluded candidates separately.
4. Configure popups for component confidence, positive reasons and cautions.
5. Keep source layers read-only; use a separate validation layer/form for reviewer labels.

## Required visual layers

- AOI boundary;
- source building footprints;
- eligible candidates graduated by score;
- excluded candidates with reason codes;
- grid asset/proximity context labelled as proxy;
- optional elevation/shading proxy;
- field/expert validation points.

## Portability

Store relative paths, project CRS and attribution in the project. Do not commit local caches, credentials or restricted layers. A future checked-in `.qgz`/GeoLibre project must open after cloning into a different directory.
