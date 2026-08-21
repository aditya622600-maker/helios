# Five-person delivery workflow

## Shared integration rule

All work enters through the contracts in `helios/contracts/models.py`. Each owner works on a short-lived branch, opens a pull request to `integration`, and attaches a fixture or reproducible output. `main` is the demo-stable branch. One real candidate must pass end to end before any team member scales a module.

| Person | Primary responsibility | Must deliver | Definition of done |
|---|---|---|---|
| 1 — ML/ranking lead (includes project lead) | normalization, MCDA, uncertainty, rank stability, optional challenger | scoring package, scenario weights, evaluation notebook/script, recorded metrics | excluded sites cannot rank; reranking is reproducible; Precision@K/nDCG evaluation runs on reviewed labels |
| 2 — GIS/GeoLibre lead | AOI, public-data acquisition, CRS, provenance, GeoLibre project | source manifests, cleaned layers, repeatable import notes, styled shortlist map | all layers share documented CRS; citations/licenses exist; no machine-specific paths; map consumes API GeoJSON |
| 3 — geometry/solar lead | rooftop geometry, height/shading proxy, solar-yield physics | candidate feature table with units/confidence, assumptions, validation fixture | outputs match contract; proxy limitations are visible; sample sites pass sanity checks |
| 4 — platform/integration lead | FastAPI, PostGIS, pipeline orchestration, CI | API endpoints, persistence adapter, migrations, integration tests, deploy instructions | one request returns ranked GeoJSON; CI passes; errors preserve run/source context |
| 5 — product/validation lead | baseline scouting comparison, field/expert labels, demo UX, narrative | validation rubric/form, reviewed top-K set, demo script, screenshots/evidence | manual baseline and Helios use same AOI/time budget; claims trace to measured results |

## Contract handoffs

1. GIS lead publishes `SourceManifest` records and candidate geometry IDs.
2. Geometry/solar lead joins features by `candidate_id` and records `provenance_ids`.
3. Platform lead validates contracts and persists a versioned run.
4. Ranking lead produces eligibility, component scores, ranks and stability evidence.
5. Platform emits GeoJSON; GIS lead styles it; product lead records validation outcomes.

## Branch and pull-request convention

- `main`: demo-stable releases only.
- `integration`: daily integration target.
- `feature/p1-ranking-stability`, `feature/p2-geolibre-aoi`, etc.
- Keep pull requests under one workstream when possible.
- Rebase or merge `integration` before the scheduled integration window, not during the demo freeze.
- Any contract change requires API documentation and at least one compatibility test.

## Ownership placeholders

Replace Person 1–5 with GitHub usernames in `docs/OWNERSHIP.md`, then add CODEOWNERS. Until usernames are known, review ownership follows the table above.
