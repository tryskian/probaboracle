# Probaboracle Charter

## Mission

Build a small, local, agent-backed oracle runtime that explores constrained
human-AI interaction through deliberately vague, non-concrete responses and
strict binary evaluation.

## Durable Rules

- CLI-first runtime is canonical.
- The prompt surface is fixed:
  - `what`
  - `when`
  - `why`
  - `where`
- No freeform prompt input is accepted in the active runtime path.
- The runtime must stay agent-backed through the OpenAI Agents SDK.
- Responses must stay in UK English.
- Responses must stay vague, answer-shaped, and non-concrete.
- Responses must not imply guidance, help, reassurance, or understanding.
- Eval semantics remain strictly binary:
  - `pass`
  - `fail`
- Keep the project small and local-first.
- Archive before delete.

## Working Model

- Human lead owns:
  - objective
  - scope boundaries
  - acceptance criteria
  - theory-level interpretation
  - go/no-go decisions
- Engineer owns:
  - implementation
  - validation
  - branch and PR flow
  - runtime hygiene
  - execution recommendations
- Default execution model:
  - feature branch per change set
  - clean `main`
  - local-first iteration

## Documentation Governance

- `README.md`
  - public repo framing and command entrypoint
- `docs/governance/DECISIONS.md`
  - durable engineering, runtime, and eval decisions
- `docs/runtime/ARCHITECTURE.md`
  - stable system shape and contracts
- `docs/runtime/RUNBOOK.md`
  - operator procedure and command ownership
- `docs/governance/SESSION_HANDOFF.md`
  - current checkpoint and next slice
- `docs/diagrams/PIPELINE.md`
  - canonical home for the pipeline diagram

## Current Scope

- In scope:
  - local CLI runtime
  - fixed prompt selection
  - agent-backed generation
  - local SQLite eval storage
  - binary human judgment
  - diagram-backed runtime explanation
- Out of scope:
  - UI shell
  - backend API
  - auth
  - deployment scaffolding
  - freeform prompt input

## Security / Ops Baseline

- `OPENAI_API_KEY` is required for live generation.
- Localhost and local CLI execution are the trusted development boundary.
- Keep local eval data under `.local/`.
