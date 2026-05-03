# Probaboracle Charter

## Mission

Probaboracle is a small, local, agent-backed oracle runtime.

It explores constrained human-AI interaction through deliberately vague,
non-concrete responses and strict binary evaluation.

Probaboracle is part of the Polinko research line. It is smaller, but it keeps
the same discipline: narrow surface, clear scope, hard evals, and careful docs.

## Durable Rules

These rules define the project shape.

Runtime:

- local and CLI-first
- agent-backed through the OpenAI Agents SDK
- one model generation path, not stitched fragment composition
- minimal config with an explicit reasoning target
- runtime directions that describe the target shape instead of accumulating
  restriction piles

Prompt surface:

- `what`
- `when`
- `why`
- `where`

The active runtime path does not accept freeform prompt input. The fixed prompt
types are the interaction boundary and the reasoning boundary.

Responses:

- UK English
- vague
- answer-shaped
- non-concrete
- not advice, guidance, help, reassurance, or understanding

Eval:

- binary verdicts only
- `pass`
- `fail`
- no `mixed` state

Project posture:

- keep it small
- keep it local-first
- keep it aligned with Polinko's safety and eval discipline
- archive before delete

## Working Model

Human lead owns:

- objective
- scope boundaries
- acceptance criteria
- theory-level interpretation
- go/no-go decisions

Engineer owns:

- implementation
- validation
- branch and PR flow
- runtime hygiene
- execution recommendations

Default execution model:

- feature branch per change set
- clean `main`
- local-first iteration

## Documentation Ownership

| Doc | Job |
| --- | --- |
| `README.md` | public framing and command entrypoint |
| `docs/governance/DECISIONS.md` | durable engineering, runtime, and eval decisions |
| `docs/research/README.md` | beta map and tracked findings |
| `docs/runtime/ARCHITECTURE.md` | stable system shape |
| `docs/runtime/RUNBOOK.md` | operator procedure and commands |
| `docs/governance/SESSION_HANDOFF.md` | current checkpoint and next slice |
| `docs/diagrams/PIPELINE.md` | public generation and eval-shape diagrams |

After runtime, product-shape, or research-method changes, sweep the tracked
docs before merging.

## Scope

In scope:

- local CLI runtime
- fixed prompt selection
- agent-backed generation
- one-node model generation with shared vocabulary
- local SQLite eval storage
- binary human judgment
- diagram-backed runtime explanation

Out of scope:

- UI shell
- backend API
- auth
- deployment scaffolding
- freeform prompt input

## Security And Ops

- `OPENAI_API_KEY` is required for live generation.
- The local runtime auto-loads the repo `.env`.
- Local CLI execution is the trusted development boundary.
- Local eval data stays under `.local/`.
