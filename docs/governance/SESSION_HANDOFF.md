# Session Handoff

Last updated: 2026-04-28

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

- Repo has been re-initialised from a clean slate.
- Active runtime shape is local CLI plus local SQLite eval storage.
- Prompt surface is fixed to `what`, `when`, `why`, and `where`.
- Binary eval gates are part of the first slice, not a later add-on.
- The canonical Mermaid pipeline diagram now lives in
  `docs/diagrams/PIPELINE.md`.
- The active tone pass clarified that prompt type selects the reasoning lane,
  while all lanes draw from one shared style-signal pool.
- Shared style signals are cues for synthesis, not a fixed word bank.

## Next Slice

1. Run live tone samples across `what`, `when`, `why`, and `where`.
2. Judge the outputs with strict binary `pass` / `fail` verdicts.
3. Tune voice until outputs feel properly vague and unhelpful without becoming
   concrete.
4. Expand test coverage once the first real runtime behaviour settles.

## Guardrails

- Keep the app small.
- Do not widen the prompt surface casually.
- Do not add freeform input while the constrained interaction theory is active.
- Keep eval verdicts binary only.
- Keep style signals as reasoning cues, not as a hard word bank.

## Session Close

- Follow `docs/runtime/RUNBOOK.md`.
- Finish the branch validated and clean before merge.

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets: current state, risks, and next kernel. Confirm the repo path is /Users/tryskian/Github/probaboracle, confirm the active git branch, and say whether the thread is on clean main or a feature branch. Then execute the Next Slice with minimal drift and full validation.`
