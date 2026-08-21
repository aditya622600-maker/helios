# Three-day hackathon runbook

## Day 1 — make one candidate real

### Hours 0–3

- clone, install, run CI locally;
- choose one compact AOI and freeze CRS/reference date;
- register source manifests and agree on units;
- load the sample request and view API GeoJSON in GeoLibre.

### Hours 3–12

- Person 2 prepares footprints and source metadata;
- Person 3 produces physical/solar features for one real candidate;
- Person 4 persists and returns that candidate through the API;
- Person 1 verifies scoring/filtering/reranking;
- Person 5 validates the result and records demo evidence.

**Gate:** one real candidate completes the entire path before bulk processing begins.

## Day 2 — scale and prove

- scale to 1,000–5,000 candidates in the frozen AOI;
- add batch normalization, Pareto view and stability simulation;
- review/label a defensible sample and run baselines;
- style GeoLibre shortlist, confidence and exclusion layers;
- fix performance and data-quality failures before adding features.

**Gate:** stored metrics for at least one baseline comparison and a repeatable top-K map.

## Day 3 — harden and present

- freeze features by midday;
- run a clean environment setup and full test suite;
- capture source/provenance view, scenario rerank and candidate explanation;
- rehearse the same AOI and pre-cache permissible data;
- merge only demo-critical fixes after freeze.

## Demo sequence

1. Select AOI and balanced scenario.
2. Show sources, reference date and warnings.
3. Run analysis and display ranked roofs.
4. Open one candidate: raw metrics, five components, confidence, reasons and cautions.
5. Change scenario weights and show transparent reranking.
6. Compare Helios top-K with the manual or solar-only baseline.
7. State the screening boundary and required field/engineering checks.

## Failure fallbacks

- Keep one small sample request and GeoJSON in the repository.
- Cache only redistributable inputs.
- If a live data endpoint fails, demonstrate the recorded source version and manifest.
- If ML challenger fails, use the deterministic baseline; never hide the result.
