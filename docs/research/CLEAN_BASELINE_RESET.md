# Clean Baseline Reset

## Status

Active source reset before the next live pulse.

The failed Beta `6.0` fixed-prompt pulse remains useful as a diagnostic
snapshot, but it is not clean baseline proof. The next comparable line starts
from a proper-config candidate and uses the same fixed-prompt pulse method.

## What Changed

The reset keeps the lab bench and strips the contaminated prompt surface.

Kept:

- fixed prompt surface:
  - `what`
  - `when`
  - `why`
  - `where`
- binary verdict surface:
  - `pass`
  - `fail`
- local eval storage and pulse tooling
- tracked beta history

Reset:

- `config.py` now stays structural:
  - prompt types
  - verdicts
  - runtime settings
  - environment loading
- prompt phrase banks, style-signal lists, pipeline-step lists, and slot
  scaffolds are no longer config content
- `agent.py` owns one minimal routing prompt for the selected prompt type
- the CLI app banner no longer presents a research beta as an app version

## Eval Method

The eval gate is unchanged.

The next live evidence should use `eval-pulse`:

1. Choose one fixed prompt.
2. Run one `15` minute pulse.
3. Label every row as:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
4. Assign one pulse-level verdict:
  - `PASS`
  - `FAIL`

Rows are evidence inside the pulse. They are not Beta `6.0` row-level product
judgments.

## Comparison Boundary

Compare the next proper-config pulse against the Beta `6.0` snapshot as a
separate line:

- Beta `6.0` snapshot:
  - ids `4850-4863`
  - fixed prompt `why`
  - `1` anchor
  - `13` counted seams
  - `0` excluded
  - verdict `FAIL`
- clean baseline candidate:
  - structural config
  - minimal routing prompt
  - same fixed-prompt pulse method
  - fresh local eval store before live collection

Only after that comparison should the repo decide whether this is a reset
inside Beta `6.0` or a new beta boundary.
