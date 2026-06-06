# Clean Baseline Reset

## Status

Clean-baseline source reset before the next local pulse.

The failed Beta `6.0` fixed-prompt pulse remains useful as a diagnostic
snapshot, but it is not clean baseline proof. The next comparable line starts
from a proper-config candidate, uses the same fixed-prompt pulse method, and
is collected locally before tracked docs receive result claims.

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
- `agent.py` owns one minimal positive routing prompt for the selected prompt
  type
- the CLI app banner no longer presents a research beta as an app version

## Cleanup Before Eval

Tracked docs stay aligned before local evidence collection:

- keep tracked docs aligned on the reset boundary
- keep Beta `6.0` as a diagnostic snapshot, not the active baseline
- keep the first clean-baseline pulse plan explicit
- use [runtime research templates](../runtime/templates/README.md) for any
  promoted pulse report or seam case
- do not add result claims until a local pulse has been run, labeled, and
  reported

Public research docs should stay split by evidence type:

| Doc Shape | Use When | Template |
| --- | --- | --- |
| pulse report | the clean-baseline pulse has a complete range and verdict | [validation](../runtime/templates/validation.md) |
| representative case | one output cleanly explains a repeated seam | [case](../runtime/templates/case.md) |
| new beta boundary | the comparison changes what the eval means | [boundary](../runtime/templates/boundary.md) |

## Eval Method

The eval gate is unchanged.

The next local evidence collection should use `eval-pulse`:

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
  - minimal positive routing prompt
  - same fixed-prompt pulse method
  - fresh local eval store before collection

Only after that comparison should the repo decide whether this is a reset
inside Beta `6.0` or a new beta boundary.

## First Clean-Baseline Pulse Plan

First target:

- fixed prompt: `why`
- reason: the Beta `6.0` diagnostic snapshot was also a `why` pulse, so this
  gives the cleanest first comparison
- duration: `15` minutes
- pacing: default one sample per minute
- run condition: rate limits and prepaid credits are healthy

Fresh local DB boundary:

1. Start from no live local eval store in this checkout.
2. Initialise a fresh store only when ready to run:
  - `make eval-init`
3. Run the first pulse:
  - `make eval-pulse-start PROMPT=why PULSE_MINUTES=15`
4. Record the printed id range before labeling.
5. Label every row in that range as:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
6. Give each `excluded_noise` row one narrow reason:
  - `operator_artifact`
  - `off_target_failure`
7. Report the pulse:
  - `make eval-pulse-report PULSE_START_ID=<start> PULSE_END_ID=<end>`

Comparison shape:

| Line | Prompt | Config State | Method | Verdict |
| --- | --- | --- | --- | --- |
| Beta `6.0` snapshot | `why` | prior contaminated line | fixed-prompt pulse | `FAIL` |
| clean baseline candidate | `why` | structural config + positive routing prompt | fixed-prompt pulse | pending |

The comparison should focus on pulse-level seam density:

- anchors
- counted seams
- excluded noise
- repeated seam family, if any
- one pulse-level verdict

Use clean-baseline rows as evidence inside the fixed-prompt pulse. Apply
product-row judgment to row-level baseline runs.
