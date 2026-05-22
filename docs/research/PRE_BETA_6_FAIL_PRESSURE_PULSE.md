# Pre-Beta 6.0: Fail-Pressure Pulse

> Historical staging note. The active contract now lives in
> [Research Beta 6.0: Fail-Pressure Pulse](./BETA_6_FAIL_PRESSURE_PULSE.md).

## What This Pre-Beta Asked

Should Probaboracle treat a bounded eval run as the real binary unit once
run-level shape matters more than single-row replay?

## Status

Promoted into active `Research Beta 6.0`.

The staging question was valid, but its first draft was too row-shaped. The
active method now separates evidence labels from the verdict:

- one prompt lane
- one `15` minute eval run
- row labels as pulse evidence only:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
- one `PASS / FAIL` verdict for the whole run
- no row-level product judgments for Beta `6.0`

## What Changed

`Research Beta 5.1` keeps the row-level baseline:

- row-level `PASS / FAIL`
- row-level `RETAIN / EVICT`

`Research Beta 6.0` changes the evidence unit:

- the eval run is the binary unit
- generated rows are the transcript of that run
- row labels explain the transcript without judging rows as products
- the whole run passes or fails once

## Promotion Boundary

This became active once Probaboracle accepted the run-level contract as the
next method:

1. choose one prompt lane
2. run for `15` minutes
3. label rows as pulse evidence
4. judge the whole run `PASS` or `FAIL`

The first valid run is still pending.
