# Session Handoff

Last updated: 2026-05-09

## Start Here

1. Read:
   - `README.md`
   - `docs/governance/CHARTER.md`
   - `docs/governance/DECISIONS.md`
   - `docs/runtime/ARCHITECTURE.md`
   - `docs/runtime/RUNBOOK.md`
   - this file
2. Confirm repo and branch:
   - `/Users/tryskian/Github/probaboracle`
   - feature branch for tracked changes
3. If the checkout is on `main`, cut a task branch before editing.
4. State the active kernel before changing files.

## Current State

Probaboracle is a local, CLI-first, agent-backed mini oracle.

The default app path is bare `probaboracle`:

- responsive startup header
- fixed selector for `where`, `what`, `why`, and `when`
- `enter` selects
- soft `hit esc to exit` hint exits cleanly
- inline spinner-only wait state
- collapsed selected prompt
- response on its own line
- immediate `another question [y/n]?`

Operator commands remain separate:

- `ask`
- `sample`
- `eval-list`
- `archive-pending`
- `judge`
- sidecar judgment commands

## Research Snapshot

Current tracked research beta:

- `Research Beta 5.0`
- `retain + evict`

Current long-run checkpoint:

- judged through row `4197`
- active product surface: `1704 pass / 1628 fail / 0 pending`
- active coherence surface: `1998 pass / 945 fail / 389 pending`
- active relevance surface: `1990 pass / 118 fail / 1224 pending`
- active absurdity surface: `5 pass / 8 fail / 3319 pending`
- archived out of the active surface:
  - `501` stale product-pending rows
  - `364` pre-sidecar rows with no live coherence lane

The active coherence rule is stricter than the early runs:

- one resolved sentence
- one dominant reasoning lane
- short lines with `2+` commas fail
- stacked fragment chains fail even when they look tidy

Useful current reads:

- the deciding Beta `5.0` `when` retain rerun used rows `3392-4097`
- fresh deciding surface: `317 pass / 389 fail / 0 pending`
- `when` has now earned `evict`:
  - `272` `stacked timing fragments`
  - `85` `semicolon pile and unresolved timing drift`
  - `32` `awkward temporal phrasing`
- the post-evict confirmation rerun used rows `4098-4197`
- confirmation surface: `97 pass / 3 fail / 0 pending`
- the old fail family collapsed:
  - `semicolon pile and unresolved timing drift`: `0`
  - `stacked timing fragments`: `1`
  - `awkward temporal phrasing`: `2`
- `where` is fully stable in the current surface:
  - `84 pass / 0 fail`
- `what` is close behind:
  - `81 pass / 3 fail`
- `why` now mostly passes when it stays plain:
  - `75 pass / 10 fail`
  - failures cluster around `stacked hinge accumulation`

## Next Kernel

Choose one lane at a time:

- app polish:
  - keep the wrapper small
  - do not widen the prompt surface
  - keep the user loop separate from operator commands
- research:
  - keep the tandem serial lane when product pending needs to stay at `0`
  - decide whether the remaining `when` misses deserve one more narrow cleanup
    or are already good enough to leave alone
  - if touching `when` again, keep it to one tiny phrasing fix only
  - do not widen the prompt surface or stack multiple runtime tweaks at once
- docs:
  - sweep tracked docs after every runtime, product-shape, or research-method change
  - keep `docs/peanut/` as the private scratch lane

## Guardrails

- Keep the app small.
- Keep the runtime local and CLI-first.
- Keep generation agent-backed through the OpenAI Agents SDK.
- Keep prompt types fixed to `what`, `when`, `why`, and `where`.
- Do not add freeform input while the constrained interaction theory is active.
- Keep eval verdicts binary only.
- Keep style signals as reasoning cues, not as a hard word bank.
- Prefer baseline-first tuning from repeated failures, not prompt accretion.
- Treat the loop as `pass / fail`, then on `fail` decide `retain / evict`,
  then rerun and judge `pass / fail` again.
- `when` has earned `evict`, and the first narrow fix is now confirmed.
- Do not widen the fix stack while the remaining misses are only narrow phrasing wobble.

## Close A Session

Follow `docs/runtime/RUNBOOK.md`.

At minimum:

- validate the active branch
- merge only after checks pass
- end on clean `main` when possible

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets: current state, risks, and next kernel. Confirm the repo path is /Users/tryskian/Github/probaboracle, confirm the active git branch, and say whether the thread is on clean main or a feature branch. Then execute the Next Slice with minimal drift and full validation.`
