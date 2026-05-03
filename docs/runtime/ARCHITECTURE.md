# Architecture

This is the fast map of Probaboracle's stable shape.

Use it when you need to understand how the app, generation path, eval storage,
and docs surfaces fit together without rereading the whole repo.

## System Map

| Surface | Role |
| --- | --- |
| `pyproject.toml` | package metadata and dependency pins |
| `Makefile` | operator command surface |
| `src/probaboracle/config.py` | prompt constants, settings, and runtime contract |
| `src/probaboracle/agent.py` | OpenAI Agents SDK generation path |
| `src/probaboracle/main.py` | default app loop and explicit subcommands |
| `src/probaboracle/eval_db.py` | local SQLite eval storage |
| `tests/` | contract and persistence tests |
| `docs/` | charter, decisions, runbook, research notes, and diagrams |

## Default App Path

Bare `probaboracle` is the user-facing path.

It opens a persistent local CLI loop with:

- a responsive header:
  - boxed on wider terminals
  - simpler stacked forms on narrower terminals
- a fixed selector for:
  - `where`
  - `what`
  - `why`
  - `when`
- `enter` as the primary action
- `esc` as the explicit exit path
- an inline spinner wait state while generation runs
- a collapsed selected-question view after `enter`
- the response on its own line under the selected question
- an immediate `another question [y/n]?` follow-up

Explicit subcommands such as `ask`, `sample`, `eval-list`, and `judge` remain
available underneath the app path for operator work.

## Generation Path

1. The selector returns one fixed prompt type.
2. `config.py` validates that prompt type.
3. The prompt type sets the reasoning lane and matched scope.
4. The lane draws from shared style signals:
   - certainty
   - indecision
   - connective hinges
   - soft conclusions
5. `agent.py` runs one OpenAI Agents SDK generation node.
6. The model resolves the final sentence structure inside that node.
7. The CLI prints the final response.

The runtime is not stitched from static fragments. The shared style signals are
cues for synthesis, not a fixed word bank.

## Eval Path

Eval data lives in `.local/evals.sqlite`.

Generated rows are stored in `eval_outputs`. Human judgments are append-only
history, with the current verdict mirrored onto the output row for fast listing
and charting.

The active binary lenses are:

- product fit
- coherence
- prompt relevance
- coherent absurdity

Coherence is the primary experimental gate. It only passes when the line
resolves as one sentence with one dominant reasoning lane.

The public generation and eval-shape diagrams live in
`docs/diagrams/PIPELINE.md`. The more detailed stop/pass/fail operator flow
stays in local/private `docs/peanut/` notes.

## Contracts

- The runtime stays local and CLI-first.
- The runtime stays agent-backed through the OpenAI Agents SDK.
- The prompt surface stays fixed to `what`, `when`, `why`, and `where`.
- The default user path does not accept freeform input.
- Operator commands stay separate from the app loop.
- Eval verdicts stay binary:
  - `pass`
  - `fail`
- Runtime directions describe the target reasoning shape rather than
  accumulating long restriction lists.

## Docs Ownership

| Doc | Job |
| --- | --- |
| `README.md` | public framing and entrypoint |
| `docs/governance/CHARTER.md` | durable rules |
| `docs/governance/DECISIONS.md` | durable runtime and eval decisions |
| `docs/runtime/RUNBOOK.md` | operator procedure and commands |
| `docs/governance/SESSION_HANDOFF.md` | current checkpoint and next slice |
| `docs/research/` | tracked beta findings |
| `docs/diagrams/PIPELINE.md` | public generation and eval-shape diagrams |
