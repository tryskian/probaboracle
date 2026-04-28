# Session Handoff

Last updated: 2026-04-28

## Current Snapshot

- Repo has been re-initialised from a clean slate.
- Active runtime shape is local CLI plus local SQLite eval storage.
- Prompt surface is fixed to `what`, `when`, `why`, and `where`.
- Binary eval gates are part of the first slice, not a later add-on.
- The canonical Mermaid pipeline diagram is still waiting on the human-supplied
  version.

## Next Slice

1. Drop in the canonical Mermaid pipeline diagram.
2. Tune voice until outputs feel properly vague and unhelpful without becoming
   concrete.
3. Expand test coverage once the first real runtime behaviour settles.

## Guardrails

- Keep the app small.
- Do not widen the prompt surface casually.
- Do not add freeform input while the constrained interaction theory is active.
- Keep eval verdicts binary only.
