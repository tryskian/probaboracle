# Research Beta 6.0: Fail-Pressure Pulse

## Status

Diagnostic snapshot. The first valid pulse failed, and the current line is held
for clean-baseline comparison rather than treated as live baseline proof.

This page owns the public evidence record for the Beta `6.0` pulse. New
proper-config results belong in [Clean Baseline Reset](./070_CB-CLEAN_BASELINE_RESET.md)
or a promoted pulse report, not as another result claim on this snapshot page.

`Research Beta 6.0` uses a fixed-prompt pulse as the binary unit:

- duration: `15` minutes
- fixed prompt: one prompt type
- default pacing: about one sample per minute
- pulse verdict: `PASS` or `FAIL`
- row product verdicts: not part of this beta
- row pulse labels: evidence only

This beta was run like the earlier beta tests: use the active eval method,
collect comparable evidence, and assign one binary verdict. The method changed
to `eval-pulse`; the pulse became the tested object.

## What This Beta Asks

Can Probaboracle hold its shape across a time-bounded fixed-prompt pulse?

The unit of judgment is the fixed-prompt pulse, not an individual row. Each
pulse uses one fixed prompt. Different prompts get separate pulses. Rows may be
labeled as evidence inside that pulse, but those labels are not product
judgments and do not touch `eval_outputs.current_verdict`.

## Eval Shape

The `eval-pulse` protocol is:

1. Choose one fixed prompt.
2. Run generation for that prompt for `15` minutes.
3. Label each row as pulse evidence:
   - `anchor`
   - `counted_seam`
   - `excluded_noise`
4. Give each `excluded_noise` row one narrow reason:
   - `operator_artifact`
   - `off_target_failure`
5. Report the fixed-prompt pulse:
   - raw rows
   - anchors
   - counted seams
   - excluded noise by reason
   - counted total
   - pulse verdict
6. Assign one verdict to the pulse:
   - `PASS`
   - `FAIL`

Counted pulse rules:

- more anchors than counted seams: `PASS`
- more counted seams than anchors: `FAIL`
- tie: `FAIL`
- unlabeled rows: incomplete

## Current State

First valid `Research Beta 6.0` fixed-prompt pulse:

- ids: `4850-4863`
- fixed prompt: `why`
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
- the pulse stayed answer-shaped, but the surface collapsed into one repeated
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

The next work is no longer another small correction on this same line. It is a
clean-baseline reset that starts from structural config and compares the next
proper-config pulse against this snapshot.

Live reruns are paused until rate limits and prepaid credits are healthy again.

## First Correction Surface

The first correction was shape-first and grammar-led. It did not add prompt
examples or a phrase bank.

Runtime pressure now asks each response to:

- choose one plain sentence claim
- make grammar carry the answer shape
- prefer one clear subject and finite verb
- keep imagery secondary to the sentence claim
- vary sentence openings across samples

That correction targeted the repeated soft-drift family while keeping the
fixed-prompt pulse method unchanged. It is now part of the diagnostic snapshot,
not the clean comparable baseline.

## Clean-Baseline Reset Question

The first correction is not a clean comparable baseline.

Earlier hard-coded prompt scaffolds were removed from the runtime surface, but
the current Beta `6.0` evidence may still be shaped by that prior config
history. Treat the failed pulse and the grammar-led correction as diagnostic
surfaces. Do not fold the next run into the same line until the baseline
question is settled.

The active reset note is [Clean Baseline Reset](./070_CB-CLEAN_BASELINE_RESET.md).

Next research slice:

- define a clean baseline candidate from the proper cleaned config
- keep the fixed-prompt pulse method unchanged
- compare the Beta `6.0` snapshot against the clean baseline line
- use the public runtime templates for any promoted pulse report or seam case
- use a diagram to make the comparison boundary explicit
- only then decide whether the clean baseline is a new beta boundary or a
  reset inside Beta `6.0`

## Relationship To Beta 5.1

`Research Beta 5.1` remains the closed row-level baseline:

- row-level `PASS / FAIL`
- row-level `RETAIN / EVICT`
- hard-coded phrase scaffolds removed from the instruction surface

`Research Beta 6.0` changes the binary unit:

- one fixed-prompt pulse at a time
- pulse evidence labels inside that pulse
- one pulse-level `PASS / FAIL`

That change is methodological. The row-level store may still hold generated
outputs as a transcript, but the beta verdict belongs to the pulse.
