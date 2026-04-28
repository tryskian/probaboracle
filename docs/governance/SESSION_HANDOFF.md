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
2. Confirm working location and branch:
   - canonical repo: `/Users/tryskian/Github/probaboracle`
   - current branch for this slice: `codex/bigbrain/model-generation-eval-hook`
3. If on `main`, branch before edits.
4. Re-state the current kernel before changing repo shape.

## Current Snapshot

- Probaboracle is a local TypeScript CLI with a manual eval loop and an in-progress runtime rethink.
- The product framing in `README.md` is aligned to the current contract:
  - unhelpful
  - flat
  - deadpan
  - safe-human-AI-interaction guardrail
- The docs are being reshaped into a small governance/runtime stack:
  - `README.md`
  - `docs/governance/CHARTER.md`
  - `docs/governance/DECISIONS.md`
  - `docs/runtime/ARCHITECTURE.md`
  - `docs/runtime/RUNBOOK.md`
  - tiny `AGENTS.md` bootstrap
- Runtime and eval parameters live in `src/config/`.
- Current theory shift:
  - the best shape is not loose oracle generation
  - and not stitched full-phrase templates
  - it is a simple semantic node pipeline:
    - certainty words
    - indecision words
    - connective hinges / articles
    - soft conclusions
- The current uncommitted branch has:
  - docs updated toward that node-pipeline theory
  - local node-generator restoration in `src/workflow.ts`
  - archived agent/API experiment and eval DB under `.probaboracle/archive/2026-04-28-agent-runtime-experiment/`
- `DECISIONS.md` is intentional here because it captures the recovered shaping choice: simplicity plus semantic nodes.

## Next Slice

1. Decide the runtime direction cleanly:
   - active path is now the local semantic-node generator
   - archived path is recoverable if needed
2. Continue prompt-type tuning, especially `what`, so it refers to a thing/category rather than literally echoing `what`.
3. Keep testing through `eval:prompt` with forced `pass` / `fail`.
4. Only after the tone settles:
   - commit
   - PR
   - merge

## Guardrails

- Keep this file current-only.
- Keep `DECISIONS.md` for durable choices, not rolling status.
- Keep `AGENTS.md` tiny and doc-pointing only.
- Keep the repo small and avoid scaffolding drift.
- Prefer the recovered simple node theory over overbuilt abstractions.

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets, give the current repo shape, active branch, current theory of the runtime, open risks, and next slice. Confirm the canonical repo path is /Users/tryskian/Github/probaboracle and say whether the thread is on main or a feature branch. Then continue in one active kernel without re-expanding the doc stack unless requested.`
