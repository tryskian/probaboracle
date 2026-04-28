# Architecture

This page is the fast structural map of the repo: start here when you need the
runtime shape without rereading every file.

## Top-Level Map

- `pyproject.toml`
  - package metadata and dependency pin
- `Makefile`
  - canonical operator command surface
- `src/probaboracle/config.py`
  - runtime contract and prompt/eval constants
- `src/probaboracle/agent.py`
  - OpenAI Agents SDK wiring
- `src/probaboracle/eval_db.py`
  - local SQLite eval storage and judgment writes
- `src/probaboracle/main.py`
  - CLI entrypoint
- `tests/`
  - local contract and persistence tests
- `docs/`
  - charter, decisions, runbook, handoff, and diagrams

## Runtime Flow

1. CLI receives a fixed prompt selection.
2. `config.py` validates the selected prompt type.
3. The selected prompt type defines the reasoning lane.
4. That lane reasons through certainty words, indecision words, connective
   articles or hinges, and soft conclusions.
5. `agent.py` builds the oracle agent and runs that constrained reasoning task
   through the OpenAI Agents SDK.
6. The CLI prints the final response.
7. Optional sample generation stores outputs in `.local/evals.sqlite`.
8. Human evaluation records a binary `pass` or `fail`.

## Data Surfaces

- Live runtime config:
  - environment variables
  - tracked constants in `src/probaboracle/config.py`
- Eval state:
  - `.local/evals.sqlite`
  - `eval_outputs` stores generated outputs
  - `eval_judgments` stores human `pass` / `fail` decisions

## Placement Rules

- Runtime contract and constants: `src/probaboracle/config.py`
- Model generation wiring: `src/probaboracle/agent.py`
- Local persistence: `src/probaboracle/eval_db.py`
- Operator procedure: `docs/runtime/RUNBOOK.md`
- Durable decisions: `docs/governance/DECISIONS.md`
- Pipeline diagram: `docs/diagrams/PIPELINE.md`

## Governance Flow

- `README.md` frames the repo and command entrypoint.
- `docs/governance/CHARTER.md` holds durable rules.
- `docs/governance/DECISIONS.md` holds durable decisions.
- `docs/runtime/RUNBOOK.md` holds procedures and command ownership.
- `docs/governance/SESSION_HANDOFF.md` holds the current checkpoint.
- `docs/diagrams/PIPELINE.md` is the diagram home.
