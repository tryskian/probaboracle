# Session Handoff

Last updated: 2026-05-02

## Startup

1. Read docs in this order:
   - `README.md`
   - `docs/governance/CHARTER.md`
   - `docs/governance/DECISIONS.md`
   - `docs/runtime/ARCHITECTURE.md`
   - `docs/runtime/RUNBOOK.md`
   - this file
2. Confirm execution location and branch:
   - canonical repo root
   - feature branch for active implementation
3. If on `main`, cut a task branch before editing.
4. State the active kernel before making changes.

## Current Snapshot

- Active runtime shape is local CLI plus local SQLite eval storage.
- Bare `probaboracle` now opens one persistent local app loop:
  - choose one of `where`, `what`, `why`, or `when` from the fixed selector
  - get one response
  - `continue? [y/n]`
- The local runtime now auto-loads the repo `.env` before live credential
  checks.
- Prompt surface is fixed to `what`, `when`, `why`, and `where`.
- Output is fully lowercase as part of the deadpan tone contract.
- Binary eval gates are active and remain strictly `pass` / `fail`.
- Layered eval sidecars now separate:
  - product fit
  - coherence
  - prompt relevance
  - coherent absurdity
- Prompt relevance is now complete across the full corpus:
  - `what`
  - `when`
  - `why`
  - `where`
- The meaningful coherent-absurdity pocket is also swept:
  - `coherence = pass`
  - `relevance = fail`
  - current pocket: `2 pass / 13 fail / 0 pending`
- Product fit is still intentionally behind the sidecars:
  - `116` pending rows
  - concentrated in `what` and `when`
- The current long-run serial checkpoint is judged through row `913`:
  - product: `398 pass / 399 fail / 116 pending`
  - coherence: `792 pass / 121 fail / 0 pending`
  - relevance: `778 pass / 135 fail / 0 pending`
  - absurdity: `5 pass / 14 fail / 894 pending`
- Public tracked docs now show:
  - the canonical generation pipeline
  - the high-level eval-shape diagram
- Current tracked research beta is:
  - `Research Beta 4.1`
  - `coherence + coherent absurdity`
- Tracked research findings now live under `docs/research/` by beta approach.
- The detailed stop/pass/fail eval flow stays in local/private `docs/peanut/`
  notes.
- The tone branch was pulled back to the simpler baseline after prompt
  accretion started fighting the Polinko method.
- A long baseline run generated a large new untagged backlog and made the main
  duplicate families obvious:
  - `why`: `reason / adjacent to one / perhaps not`
  - `what`: `curve / shape / becoming one`
  - `when`: `moment / not one you could schedule`
  - `where`: `unclaimed edge / not where you could keep it`
- Shared style signals are cues for synthesis, not a fixed word bank.
- The strongest current coherent-absurdity method is serial:
  - one product per run
  - immediate judgment
  - no pooled batch taste when isolating that gate
  - use `25+` rows as the default minimum useful chunk before summarizing
  - treat `50-100` rows, or about one hour, as the real long-run surface
  - keep extra `when` pressure in the mix
- Coherence is now being judged more strictly:
  - one resolved sentence
  - one dominant lane
  - fail stacked fragment chains and one-line-list shapes even if they look
    superficially tidy
  - for short lines, `2+` commas is now a hard fail heuristic
- The current long run also surfaced two strong in-lane `why` exceptions:
  - `896`: `apparently a reason, though not in any useful sense.`
  - `913`: `technically a reason, though not in any useful sense.`
- `when` is now splitting more clearly:
  - simple one-comma temporal lines can pass
  - stacked temporal blur fails fast

## Next Slice

1. Pick the final startup banner treatment for the local app loop.
2. Keep the app wrapper small:
   - local
   - CLI-first
   - one persistent session
   - no widened prompt surface
3. Smoke-test the installed `probaboracle` path after wrapper refinements.
4. Keep operator subcommands separate from the user-facing app loop.
5. Return to the Beta 4.1 serial run only when research becomes the active
   kernel again.

## Guardrails

- Keep the app small.
- Do not widen the prompt surface casually.
- Do not add freeform input while the constrained interaction theory is active.
- Keep eval verdicts binary only.
- Keep style signals as reasoning cues, not as a hard word bank.
- Prefer baseline-first tuning from repeated failures, not prompt accretion.

## Session Close

- Follow `docs/runtime/RUNBOOK.md`.
- Finish the branch validated and clean before merge.

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets: current state, risks, and next kernel. Confirm the repo path is /Users/tryskian/Github/probaboracle, confirm the active git branch, and say whether the thread is on clean main or a feature branch. Then execute the Next Slice with minimal drift and full validation.`
