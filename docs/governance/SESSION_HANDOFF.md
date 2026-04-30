# Session Handoff

Last updated: 2026-04-30

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
- Public tracked docs now show:
  - the canonical generation pipeline
  - the high-level eval-shape diagram
- Current tracked research beta is:
  - `Research Beta 4.0`
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

## Next Slice

1. Decide whether to close the last `48` pending product-fit rows from the
   focused `when` run, or leave them as an intentionally separate product
   pocket.
2. Keep coherence primary when judging any new slices.
3. Use repeated failure clusters to decide whether the baseline has earned a
   real change.
4. Keep the public eval shape and the private detailed flow aligned if either
   changes.
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
