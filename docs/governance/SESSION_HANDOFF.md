# Session Handoff

Last updated: 2026-04-29

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
  - hand waving
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

1. Sweep the new sidecar lanes deliberately, not all at once.
2. Keep coherence primary when judging new slices.
3. Use repeated failure clusters to decide whether the baseline has earned a
   real change.
4. Keep the runtime contract steady unless the data justifies intervention.

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
