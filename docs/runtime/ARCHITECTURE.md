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
3. The selected prompt type defines the reasoning lane and matched scope.
4. That lane reasons through certainty words, indecision words, connective
   articles or hinges, and soft conclusions using one shared style-signal pool.
5. `agent.py` builds the oracle agent and runs that constrained reasoning task
   through the OpenAI Agents SDK in one model generation node.
6. The CLI prints the final response.
7. Optional sample generation stores outputs in `.local/evals.sqlite`.
8. Human evaluation records layered binary judgments:
   - product fit
   - coherence
   - prompt relevance
   - coherent absurdity
   - hand waving

The generation diagram and the eval-layer diagram now live together in
`docs/diagrams/PIPELINE.md`.

## Data Surfaces

- Live runtime config:
  - environment variables
  - tracked constants in `src/probaboracle/config.py`
  - shared style signals are cues for model reasoning, not a fixed word bank
  - runtime directions should describe the target reasoning shape, not become a
    large restriction pile
- Eval state:
  - `.local/evals.sqlite`
  - `eval_outputs` stores generated outputs
  - `eval_judgments` stores human `pass` / `fail` decisions
  - sidecar judgment tables store separate binary lenses for:
    - coherence
    - prompt relevance
    - coherent absurdity
    - hand waving

## Reasoning Contract

- Prompt type matches the reasoning scope.
- The matched scope is a real guardrail:
  - it helps avoid drift
  - it preserves the intended reasoning slope
- Vocabulary is shared across lanes.
- Words are generated in one node, not stitched from per-prompt fragments.
- The model resolves the final logical sentence structure inside that one
  generation path.

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
