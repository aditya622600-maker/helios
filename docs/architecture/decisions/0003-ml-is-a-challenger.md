# ADR 0003: Treat ML ranking as an optional challenger

- Status: accepted
- Date: 2026-08-21

## Context

Round-one feedback requires demonstrable improvement and defensible evaluation. A learned fusion model without enough reviewed sites risks overfitting and weak explanations.

## Decision

Ship deterministic MCDA first. Train a lightweight learned-to-rank or gradient-boosted challenger only after field/expert labels exist. Promote it only if it improves held-out Precision@K or nDCG and remains interpretable.

## Consequences

The MVP stays reliable if training fails. The ML lead still owns uncertainty, stability and challenger experiments, but the demo has no dependency on them.
