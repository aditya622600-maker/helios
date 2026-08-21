# ADR 0002: Keep GeoLibre as visualization and validation client

- Status: accepted
- Date: 2026-08-21

## Context

GeoLibre is valuable for GIS collection, layer inspection, styling and demonstration. Embedding core scoring logic in a desktop project would make automated tests, API reuse and reproducibility harder.

## Decision

The analytical pipeline owns standardized features and rankings. It exports GeoJSON/PostGIS layers. GeoLibre consumes those outputs, supports manual validation and returns corrections through defined field forms.

## Consequences

Map work and backend work can proceed independently. The integration contract must remain stable and GeoLibre project files must not contain machine-specific absolute paths.
