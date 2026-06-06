# Probaboracle Charter

## Mission

Probaboracle is a small, local, agent-backed oracle runtime.

It explores constrained human-AI interaction through deliberately vague, non-concrete responses and strict binary evaluation.

Probaboracle is part of the Polinko research line. It is smaller, but it keeps the same discipline: narrow surface, clear scope, hard evals, and careful docs.

## Durable Rules

These rules define the project shape.

Runtime:

- local and CLI-first
- agent-backed through the OpenAI Agents SDK
- one model generation path with model-owned final wording
- minimal structural config
- config limited to prompt types, verdicts, runtime settings, and local paths
- runtime directions that describe the target shape instead of accumulating restriction piles

Prompt surface:

- `what`
- `when`
- `why`
- `where`

The active runtime path uses fixed prompt types as the interaction boundary and
the reasoning boundary.

Responses:

- UK English
- vague
- answer-shaped
- non-concrete
- low-utility oracle text

Eval:

- binary verdicts only
- `pass`
- `fail`
- verdict state set stays binary
- the research method defines the unit of judgment:
  - row-level baselines judge rows
  - pulse-level baselines judge fixed-prompt pulses
- pulse-level work runs one fixed-prompt pulse at a time:
  - different prompts get separate pulses
- pulse rows are evidence only inside that pulse:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
- after a row-level baseline `fail`, decide:
  - `retain`
  - `evict`
- `retain` means keep the family in the active lane and keep gathering baseline
  evidence under the current rule
- `evict` means make the later upstream runtime correction because the failure
  family has stabilised enough to earn removal
- eviction ends repeated judgment of the known bad family
- one eval focus at a time
- treat small evals as smoke checks only
- treat long-run consistency as the real evidence surface

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
| `docs/runtime/START_END_REFERENCE.md` | compact day-open/day-close operator sheet |
| `docs/runtime/templates/` | public templates for research docs and pulse reports |
| `docs/governance/SESSION_HANDOFF.md` | current checkpoint and next slice |
| `docs/diagrams/PIPELINE.md` | public generation and eval-shape diagrams |

After runtime, product-shape, or research-method changes, sweep the tracked docs before merging.

## Scope

In scope:

- local CLI runtime
- fixed prompt selection
- agent-backed generation
- one-node model generation without configured phrase banks
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
- default branch changes land through PRs with required checks:
  - `markdownlint`
  - `test`
  - `dependency-review`
  - `python-security`
  - `node-security`
- Local validation should expose matching Make targets for docs linting,
  package checks, and dependency security checks.
- Dependabot and GitHub secret scanning are part of the tracked repo baseline.
