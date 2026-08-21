# Temporal alignment

## Why it matters

A current rent estimate, an old roof footprint, climatological irradiance and a one-day weather snapshot do not describe the same state. Combining them without disclosure can move a candidate's rank for reasons unrelated to actual suitability.

## Reference-window protocol

1. Every run declares `reference_date`.
2. Each source is classified as static, snapshot, range or climatology.
3. Snapshot/range data outside its validity interval is flagged.
4. Building and grid layers older than the chosen freshness threshold require review.
5. Long-term yield uses climatology; short weather windows cannot be presented as annual potential.
6. Economic data records currency, nominal date and collection method.

## MVP policy

The API currently returns temporal warnings. Before production, define severity by source type and reject high-severity incompatibilities. The UI must never hide warnings for a top-ranked candidate.
