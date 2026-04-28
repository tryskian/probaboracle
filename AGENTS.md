# AGENTS.md

This repository uses normal docs as the main local instruction surface.

Read in this order before making non-trivial changes:

1. [README.md](./README.md)
2. [docs/governance/CHARTER.md](./docs/governance/CHARTER.md)
3. [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
4. [docs/runtime/ARCHITECTURE.md](./docs/runtime/ARCHITECTURE.md)
5. [docs/runtime/RUNBOOK.md](./docs/runtime/RUNBOOK.md)
6. [docs/governance/SESSION_HANDOFF.md](./docs/governance/SESSION_HANDOFF.md)

If the change touches product shape, docs drift, or repo conventions, also scan
[docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md).
If the change touches runtime or eval parameters, inspect
[src/probaboracle/config.py](./src/probaboracle/config.py).

Hard guards:

- Keep the project small.
- Keep the runtime local and CLI-first.
- Keep the runtime agent-backed.
- Use model generation through the OpenAI Agents SDK, not stitched fragment
  composition.
- Do not add a UI shell, backend API, auth, deployment scaffolding, or extra
  prompt input unless explicitly requested.
- Keep user-facing output in UK English.
- Keep prompt types limited to `what`, `when`, `why`, and `where`.
- Keep eval verdicts binary only: `pass` or `fail`.
- Do not add a `mixed` verdict state.
