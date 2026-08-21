# Ranking and scouting validation

## Research question

Does Helios find more genuinely promising rooftops near the top of the list, and reduce analyst scouting effort, compared with traditional map/manual scouting under the same time and AOI constraints?

## Labels

The product/validation lead creates a blinded review sheet for a sample of candidate roofs. Two reviewers label each as `inspect`, `uncertain` or `reject`, record reason codes, and resolve disagreements. Field validation is preferred; expert orthophoto review is the documented fallback.

## Baselines

1. manual scouting using the team's prior/default process;
2. solar-resource-only ranking;
3. equal-weight MCDA;
4. proposed balanced MCDA;
5. learned challenger, only if enough labels exist.

## Primary metrics

- **Precision@K:** fraction of the first K results labelled `inspect`.
- **Recall@K:** fraction of all labelled `inspect` candidates captured in the first K.
- **nDCG@K:** rank quality when `inspect`, `uncertain`, `reject` are graded 2, 1, 0.
- **time to shortlist:** minutes to produce K reviewed candidates.
- **inspection yield:** confirmed promising candidates per inspection.

Report the number of labelled sites and confidence intervals; do not present a small convenience sample as general proof.

## Robustness

Perturb normalized inputs within their uncertainty ranges and scenario weights within a declared tolerance. Record top-K overlap and rank intervals. A candidate with a high mean score but unstable rank must be labelled accordingly.

## Demonstration claim rule

Use “improved” only when a stored evaluation run beats the named baseline on a named metric. Otherwise say “designed to improve” and demonstrate traceability, speed and scenario sensitivity without fabricating an effect size.
