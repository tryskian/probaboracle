# Session Handoff

Last updated: 2026-04-27

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
   - current branch for this docs pass: `codex/bigbrain/runbook-pass`
3. If on `main`, branch before edits.
4. Re-state the current kernel before changing repo shape.

## Current Snapshot

- Probaboracle is a tiny local TypeScript CLI with a classifier-style response pipeline and local SQLite eval loop.
- The product framing in `README.md` is aligned to the current contract:
  - pseudo-mystical
  - deadpan
  - unhelpful
  - safe-human-AI-interaction guardrail
- The docs are being reshaped into a small governance/runtime stack:
  - `README.md`
  - `docs/governance/CHARTER.md`
  - `docs/governance/DECISIONS.md`
  - `docs/runtime/ARCHITECTURE.md`
  - `docs/runtime/RUNBOOK.md`
  - tiny `AGENTS.md` bootstrap
- Runtime and eval parameters now live in `src/config/`.
- `DECISIONS.md` is intentional here because it captures human-engineer shaping choices, including the compositional pipeline call.

## Next Slice

1. Review the doc stack as one set and trim any duplicated language.
2. Commit this docs pass on `codex/bigbrain/runbook-pass`.
3. Open a PR and merge when the wording feels settled.

## Guardrails

- Keep this file current-only.
- Keep `DECISIONS.md` for durable choices, not rolling status.
- Keep `AGENTS.md` tiny and doc-pointing only.
- Keep the repo small and avoid scaffolding drift.

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets, give the current repo shape, current doc stack, active branch, open risks, and next slice. Confirm the canonical repo path is /Users/tryskian/Github/probaboracle and say whether the thread is on main or a feature branch. Then continue in one active kernel without re-expanding the doc stack unless requested.`
