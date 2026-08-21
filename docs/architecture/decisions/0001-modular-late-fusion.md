# ADR 0001: Use modular experts with late feature fusion

- Status: accepted
- Date: 2026-08-21

## Context

The inputs are heterogeneous: polygons, rasters, time series, network proximity and monetary proxies. Training one end-to-end model would require aligned labels and a volume of validated site decisions unavailable during the hackathon.

## Decision

Build independent GIS/physics feature modules that emit one versioned candidate contract. Apply hard filters, then explicit MCDA ranking. Keep a learned ranker behind the same contract as an optional challenger.

## Consequences

The result is auditable, parallelizable and demonstrable with little labelled data. It may not capture every nonlinear interaction, so ranking validation and a future challenger remain necessary.
