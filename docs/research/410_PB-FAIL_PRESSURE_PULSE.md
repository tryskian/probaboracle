# Pre-Beta 6.0: Fail-Pressure Pulse

> Historical staging note. The active contract now lives in
> [Research Beta 6.0: Fail-Pressure Pulse](./060_B-FAIL_PRESSURE_PULSE.md).

## What This Pre-Beta Asked

Should Probaboracle treat a fixed-prompt pulse as the real binary unit
once fixed prompt shape matters more than single-row replay?

## Status

Promoted into active `Research Beta 6.0`.

The staging question was valid, but its first draft was too row-shaped. The
active method now separates evidence labels from the verdict:

- one fixed prompt
- one `15` minute fixed-prompt pulse
- row labels as pulse evidence only:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
- one `PASS / FAIL` verdict for the pulse
- no row-level product judgments for Beta `6.0`

## What Changed

`Research Beta 5.1` keeps the row-level baseline:

- row-level `PASS / FAIL`
- row-level `RETAIN / EVICT`

`Research Beta 6.0` changes the evidence unit:

- the fixed-prompt pulse is the binary unit
- generated rows are the transcript of that pulse
- row labels explain the transcript without judging rows as products
- the pulse passes or fails once

## Promotion Boundary

This became active once Probaboracle accepted the pulse-level contract as the
next method:

1. choose one fixed prompt
2. run that fixed-prompt pulse for `15` minutes
3. label rows as pulse evidence
4. judge the pulse `PASS` or `FAIL`

The first valid pulse later failed on the active `Research Beta 6.0`
surface.
