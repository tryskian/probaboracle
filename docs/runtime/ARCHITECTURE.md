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
  - CLI entrypoint for the default app loop and operator subcommands
- `tests/`
  - local contract and persistence tests
- `docs/`
  - charter, decisions, runbook, handoff, and diagrams

## Runtime Flow

1. Bare `probaboracle` opens one persistent local app loop with a small
   responsive header:
   - boxed when the terminal is wide enough
   - stacked fallbacks when it is not
2. The user selects one fixed prompt type per turn from the selector:
   - `enter` is the primary action
   - `esc` is the explicit secondary exit path
3. `config.py` validates the selected prompt type.
4. The selected prompt type defines the reasoning lane and matched scope.
5. That lane reasons through certainty words, indecision words, connective
   articles or hinges, and soft conclusions using one shared style-signal pool.
6. `agent.py` builds the oracle agent and runs that constrained reasoning task
   through the OpenAI Agents SDK in one model generation node while the app
   shows a minimal inline spinner wait state in the selected prompt area.
7. After `enter`, the CLI collapses to the selected question, renders the
   response on its own line, and then offers the immediate continue prompt.
8. Operator subcommands remain available for explicit repo work like `ask`,
   `sample`, `eval-list`, and `judge`.
9. Optional sample generation stores outputs in `.local/evals.sqlite`.
10. Human evaluation records layered binary judgments:

    - product fit
    - coherence
    - prompt relevance
    - coherent absurdity
    - coherence only passes when the line resolves as one sentence rather than
      a stacked fragment chain

The public generation diagram and the high-level public eval-shape diagram now
live together in `docs/diagrams/PIPELINE.md`. The detailed judgment flow lives
in local/private `docs/peanut/` notes. Incoherent lines terminate at the
coherence gate, and coherent out-of-lane lines only continue if they pass as
coherent absurdity before the final product-fit judgment.

## Data Surfaces

- Live runtime config:
  - environment variables
  - repo `.env` auto-loaded by `load_settings()`
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

## Reasoning Contract

- Prompt type matches the reasoning scope.
- The matched scope is a real guardrail:
  - it helps avoid drift
  - it preserves the intended reasoning slope
- Vocabulary is shared across lanes.
- Words are generated in one node, not stitched from per-prompt fragments.
- The model resolves the final logical sentence structure inside that one
  generation path.
- The default user path is a persistent session loop, not a relaunch for each
  question.
- The default user path keeps the question and answer visually attached:
  - selector first
  - collapsed selected prompt second
  - response line underneath
  - follow-up prompt after that
- Human coherence judgment checks whether that structure resolves cleanly:
  - one dominant lane
  - one resolved sentence
  - punctuation supporting the line rather than carrying it

## Placement Rules

- Runtime contract and constants: `src/probaboracle/config.py`
- Model generation wiring: `src/probaboracle/agent.py`
- Local persistence: `src/probaboracle/eval_db.py`
- Operator procedure: `docs/runtime/RUNBOOK.md`
- Durable decisions: `docs/governance/DECISIONS.md`
- Tracked beta findings: `docs/research/`
- Public pipeline and eval-shape diagrams: `docs/diagrams/PIPELINE.md`
- Local/private detailed eval flow: `docs/peanut/`

## Governance Flow

- `README.md` frames the repo and command entrypoint.
- `docs/governance/CHARTER.md` holds durable rules.
- `docs/governance/DECISIONS.md` holds durable decisions.
- `docs/runtime/RUNBOOK.md` holds procedures and command ownership.
- `docs/governance/SESSION_HANDOFF.md` holds the current checkpoint.
- `docs/diagrams/PIPELINE.md` is the diagram home.
