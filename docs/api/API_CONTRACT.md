# API contract v1

Interactive OpenAPI documentation is available at `/docs` when the service runs.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | service health |
| `POST` | `/analysis-runs` | validate a run request, apply filters and rank candidates |
| `GET` | `/analysis-runs/{run_id}` | retrieve the immutable analytical result |
| `POST` | `/analysis-runs/{run_id}/rerank` | recalculate scores using a new weight set |
| `GET` | `/analysis-runs/{run_id}/candidates.geojson` | GeoLibre-ready feature collection |

## Request boundary

The v1 baseline expects upstream experts to provide raw screening metrics and normalized `[0,1]` component inputs. Normalization must be fitted within the same AOI/candidate set and its method recorded by the ranking workstream. Weights must sum to 1.0.

## Response guarantees

- Excluded candidates have `total_score=null` and `rank=null`.
- Eligible rank starts at 1 and is deterministic for a fixed request.
- GeoJSON properties carry rank, score, confidence and concise reason lists.
- Source IDs and temporal warnings remain attached to the run.

## Evolution rule

Breaking field changes require a new contract version. Additive optional fields may remain in v1 with tests and documentation. The API should later persist the original request and normalization metadata to PostGIS for complete reproducibility.
