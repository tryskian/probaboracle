# Research Beta 6.0: Fail-Pressure Pulse

## Status

Active method, first valid pulse failed.

`Research Beta 6.0` uses a bounded eval run as the binary unit:

- duration: `15` minutes
- prompt lane: one fixed prompt for the whole run
- default pacing: about one sample per minute
- run verdict: `PASS` or `FAIL`
- row product verdicts: not part of this beta
- row pulse labels: evidence only

## What This Beta Asks

Can Probaboracle hold its shape across a time-bounded run?

The unit of judgment is the eval run, not an individual row. Rows may be
labeled as evidence inside the run, but those labels are not product judgments
and do not touch `eval_outputs.current_verdict`.

## Eval Shape

The run protocol is:

1. Choose one prompt lane.
2. Run generation for `15` minutes.
3. Label each row as pulse evidence:
   - `anchor`
   - `counted_seam`
   - `excluded_noise`
4. Give each `excluded_noise` row one narrow reason:
   - `operator_artifact`
   - `off_target_failure`
5. Report the bounded run:
   - raw rows
   - anchors
   - counted seams
   - excluded noise by reason
   - counted total
   - pulse verdict
6. Assign one verdict to the run:
   - `PASS`
   - `FAIL`

Counted pulse rules:

- more anchors than counted seams: `PASS`
- more counted seams than anchors: `FAIL`
- tie: `FAIL`
- unlabeled rows: incomplete

## Current State

First valid `Research Beta 6.0` eval run:

- ids: `4850-4863`
- prompt lane: `why`
- duration: `15` minute paced pulse
- raw rows: `14`
- anchors: `1`
- counted seams: `13`
- excluded noise: `0`
- verdict: `FAIL`

Dominant counted seam:

- repeated soft abstraction built from:
  - quiet / soft / whisper
  - drift / edge
  - meaning / certainty
  - land / arrive / settle
- the run stayed answer-shaped, but the surface collapsed into one repeated
  vague motion family

Invalidated false starts:

- rows `4790-4804`
  - generated before the live prompt surface was clean
  - discarded from the active eval surface
- rows `4805-4819`
  - briefly received row-level product judgments by mistake
  - row product judgments were discarded as bad data
  - rows were discarded from the active eval surface
- rows `4820-4849`
  - interrupted before the full `15` minute pulse completed
  - rows were exported to the local undo lane before deletion
  - rows were discarded from the active eval surface

The next work is to decide the smallest correction that breaks the repeated
soft-drift family without returning to hard-coded phrase scaffolds.

Live reruns are paused until rate limits and prepaid credits are healthy again.

## Relationship To Beta 5.1

`Research Beta 5.1` remains the closed row-level baseline:

- row-level `PASS / FAIL`
- row-level `RETAIN / EVICT`
- hard-coded phrase scaffolds removed from the instruction surface

`Research Beta 6.0` changes the binary unit:

- one time-bounded eval run
- one prompt lane
- pulse evidence labels inside the run
- one run-level `PASS / FAIL`

That change is methodological. The row-level store may still hold generated
outputs as a transcript, but the beta verdict belongs to the run.
