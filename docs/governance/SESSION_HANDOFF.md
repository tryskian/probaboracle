# Session Handoff

Last updated: 2026-05-03

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
- `judge`
- sidecar judgment commands

## Research Snapshot

Current tracked research beta:

- `Research Beta 4.1`
- `coherence + coherent absurdity`

Current long-run checkpoint:

- judged through row `913`
- product: `398 pass / 399 fail / 116 pending`
- coherence: `792 pass / 121 fail / 0 pending`
- relevance: `778 pass / 135 fail / 0 pending`
- absurdity: `5 pass / 14 fail / 894 pending`

The active coherence rule is stricter than the early runs:

- one resolved sentence
- one dominant reasoning lane
- short lines with `2+` commas fail
- stacked fragment chains fail even when they look tidy

Useful current reads:

- `when` splits between simple one-comma temporal passes and stacked temporal
  fails
- `why` is still the weakest product lane, but has rare strong passes:
  - `896`: `apparently a reason, though not in any useful sense.`
  - `913`: `technically a reason, though not in any useful sense.`

## Next Kernel

Choose one lane at a time:

- app polish:
  - keep the wrapper small
  - do not widen the prompt surface
  - keep the user loop separate from operator commands
- research:
  - continue the Beta 4.1 serial run
  - use `25+` rows as a minimum checkpoint
  - treat `50-100` rows, or about one hour, as the real long-run surface
- docs:
  - sweep tracked docs after every runtime, product-shape, or research-method
    change
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

## Close A Session

Follow `docs/runtime/RUNBOOK.md`.

At minimum:

- validate the active branch
- merge only after checks pass
- end on clean `main` when possible

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets: current state, risks, and next kernel. Confirm the repo path is /Users/tryskian/Github/probaboracle, confirm the active git branch, and say whether the thread is on clean main or a feature branch. Then execute the Next Slice with minimal drift and full validation.`
