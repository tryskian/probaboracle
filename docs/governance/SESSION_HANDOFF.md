# Session Handoff

Last updated: 2026-05-01

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
- Coherence is now being judged more strictly:
  - one resolved sentence
  - one dominant lane
  - fail stacked fragment chains and one-line-list shapes even if they look
    superficially tidy
  - for short lines, `2+` commas is now a hard fail heuristic

## Next Slice

1. Define the first Probaboracle app-wrapper brief before building UI or shell
   behaviour.
2. Keep the wrapper small:
   - local
   - CLI-first
   - one clean command surface
3. Leave the current `116` pending product-fit rows alone unless product-fit
   closure becomes the explicit next kernel.
4. If returning to Beta 4 research work, prefer single-product flex runs with
   immediate coherence, relevance, and absurdity judgment.
5. Keep tracked research findings grouped by beta approach, not by raw run.

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
