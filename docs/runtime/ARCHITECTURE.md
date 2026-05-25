# Architecture

This is the fast map of Probaboracle's stable shape.

Use it when you need to understand how the app, generation path, eval storage, and docs surfaces fit together without rereading the whole repo.

## System Map

| Surface | Role |
| --- | --- |
| `pyproject.toml` | package metadata and dependency pins |
| `Makefile` | operator command surface |
| `src/probaboracle/config.py` | structural constants, settings, and runtime validation |
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

Explicit subcommands such as `ask`, `sample`, `eval-list`, and `judge` remain available underneath the app path for operator work.

## Generation Path

1. The selector returns one fixed prompt type.
2. `config.py` validates that prompt type.
3. `agent.py` builds one minimal routing prompt from the selected prompt type.
4. The routing prompt treats the prompt type as private context, not answer text.
5. `ORACLE_INSTRUCTIONS` carries the stable output contract:
   - UK English
   - one short lowercase line
   - answer-like but not useful
   - vague and non-concrete
   - no concrete external facts
6. `agent.py` runs one OpenAI Agents SDK generation node.
7. The model resolves the final sentence structure inside that node.
8. The CLI prints the final response.

The runtime is not stitched from static fragments. `config.py` does not hold
prompt phrase banks, style-signal lists, pipeline-step lists, or hidden slot
scaffolds.

## Eval Path

Eval data lives in `.local/evals.sqlite`.

Generated rows are stored in `eval_outputs`. Human judgments are append-only
history, with the current verdict mirrored onto the output row for fast listing
and charting.

Archived rows stay in the same SQLite store with archive metadata, but the default operator surfaces treat them as inactive:

- `eval-list` hides them unless explicitly asked for
- counts and session status exclude them
- the public static eval chart excludes them

The row-level binary lenses are:

- product fit
- coherence
- prompt relevance
- coherent absurdity

Coherence is the primary experimental gate. It only passes when the line resolves as one sentence with one dominant reasoning lane.

The active Beta `6.0` gate is pulse-level:

- each pulse uses one fixed prompt
- one fixed-prompt pulse
- row labels as evidence only:
  - `anchor`
  - `counted_seam`
  - `excluded_noise`
- one pulse-level `pass` or `fail`

Beta `6.0` pulse labels do not update `eval_outputs.current_verdict`.
Row-level product verdicts remain the `Beta 5.1` comparison surface and the
operator chart source, not the active Beta `6.0` verdict unit.

The public generation and eval-shape diagrams live in `docs/diagrams/PIPELINE.md`. The more detailed stop/pass/fail operator flow stays in local/private `docs/peanut/` notes.

## Contracts

- The runtime stays local and CLI-first.
- The runtime stays agent-backed through the OpenAI Agents SDK.
- The prompt surface stays fixed to `what`, `when`, `why`, and `where`.
- The default user path does not accept freeform input.
- Operator commands stay separate from the app loop.
- Runtime config stays structural; prompt phrase banks do not belong there.
- Eval verdicts stay binary, but the active beta owns the unit:
  - `pass`
  - `fail`
- Row-level baselines may decide `retain / evict` after a failure family
  stabilises.
- Beta `6.0` rows are not product-judged; they feed one fixed-prompt pulse
  verdict.
- Runtime directions describe the target reasoning shape rather than accumulating long restriction lists.

## Operator Surface

- Startup ritual: `make start`
- Day-close routine: `make end`
- Branch-local closeout validation: `make end-preflight`
- Clean-main closeout gate: `make end-git-check`
- Managed wake lock:
  - `make caffeinate`
  - `make caffeinate-status`
  - `make decaffeinate-status`
  - `make decaffeinate`
- Baseline validation: `make check`
- Environment sanity: `make doctor-env`
- Compact operator sheet: `make rituals`

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
