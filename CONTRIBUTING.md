# Contributing to Helios

## Branch workflow

Use short-lived branches from `integration`:

- `person1/ml-ranking-<task>`
- `person2/gis-geolibre-<task>`
- `person3/solar-geometry-<task>`
- `person4/backend-platform-<task>`
- `person5/product-validation-<task>`
- `fix/<task>`
- `docs/<task>`

`main` contains demonstrable checkpoints. `integration` is the shared merge branch during the hackathon.

## Before opening a pull request

1. Rebase or merge the latest `integration`.
2. Run `pytest`.
3. Run `ruff check .`.
4. Confirm the shared contracts still validate.
5. Add or update tests for changed behaviour.
6. Document inputs, outputs, failure behaviour and provenance.
7. Do not include credentials, large raw datasets or licensed imagery.

## Pull-request contract

A pull request must state:

- problem addressed;
- owner/workstream;
- inputs consumed;
- outputs produced;
- schema changes;
- validation performed;
- limitations or proxy assumptions;
- screenshots for GeoLibre/UI changes.

At least one teammate reviews changes before merge. Contract, scoring, database and temporal-alignment changes require review by the platform or ML lead.

## Commit format

Use imperative, scoped messages:

```text
feat(ranking): add balanced score calculation
fix(temporal): reject incompatible snapshots
docs(gis): record building source citation
test(api): cover invalid AOI request
```

## Data policy

- Commit only small, redistributable fixtures.
- Store source URLs and checksums in manifests.
- Keep downloaded rasters, imagery and large vectors outside Git.
- Never scrape sources against their terms.
- Do not commit personal field-survey information.

## Definition of done

A task is done when the consumer workstream can load and use the output without manual editing.
