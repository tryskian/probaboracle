# Probaboracle Charter

## Mission

Build a mini oracle chatbot with constrained prompt lanes and local agent-backed generation that produces short pseudo-mystical non-answers without drifting into help, guidance, or advice.

## Durable Rules

- Keep the project small.
- CLI-first is the canonical execution surface.
- The runtime remains local and CLI-first, even when generation is model-backed.
- Generation runs through a single constrained agent, not a stitched fragment compositor.
- Do not add a UI shell, backend API, auth, deployment scaffolding, or ChatKit unless explicitly requested.
- User-facing output stays in UK English.
- Prompt types stay limited to:
  - `what`
  - `when`
  - `how`
  - `why`
  - `where`
- Responses should stay short, coherent, deadpan, confident, vaguely mystical, and unhelpful.
- At no point should the product imply guidance, help, reassurance, or understanding.
- The narrow prompt frame exists as a guardrail for safe human-AI interaction.
- Eval semantics remain binary:
  - `pass`
  - `fail`
- Do not add a `mixed` verdict state.
- The binary eval gate is by design. It continues the strict pass/fail semantics operationalised in Polinko Beta 2.0 as part of a broader human-AI safety and alignment stance.
- Prefer inspectable prompt framing over sentence-stitching or scaffolding-heavy abstractions.

## Working Model

- Human lead owns:
  - concept
  - scope boundaries
  - acceptance criteria
  - wording and product direction
- Engineer owns:
  - implementation
  - validation
  - Git and PR flow
  - documentation upkeep
  - proactive drift cleanup
- Default execution model:
  - feature branch per change set
  - merge back cleanly after validation

## Documentation Governance

- `docs/governance/CHARTER.md`
  - durable rules and scope
- `docs/governance/DECISIONS.md`
  - durable collaboration and implementation choices
- `docs/governance/SESSION_HANDOFF.md`
  - current snapshot and next slice for continuation
- `docs/runtime/ARCHITECTURE.md`
  - stable system shape and contracts
- `docs/runtime/RUNBOOK.md`
  - procedures, command ownership, and validation flow

## Current Scope

- In scope:
  - local CLI prompt generation
  - agent-backed response generation
  - local SQLite eval storage
  - README and docs that explain the product and system clearly
- Out of scope unless explicitly requested:
  - public app shell
  - web app or chat UI
  - backend service layer
  - auth or account systems
  - deployment automation
