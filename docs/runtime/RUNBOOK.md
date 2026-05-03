# Runbook

This is the operator guide for local setup, commands, validation, and eval work.

Use `docs/runtime/ARCHITECTURE.md` for system shape. Use this file when you
need to run or check something.

## Start A Session

1. Read the local instruction surface:
   - `README.md`
   - `docs/governance/CHARTER.md`
   - `docs/governance/DECISIONS.md`
   - `docs/runtime/ARCHITECTURE.md`
   - `docs/runtime/RUNBOOK.md`
   - `docs/governance/SESSION_HANDOFF.md`
2. Confirm branch state:
   - `git branch --show-current`
   - work from `codex/bigbrain/<task-name>` for tracked changes
3. Install or refresh the local environment:
   - `make install`
4. Add live runtime credentials:
   - put `OPENAI_API_KEY` in the repo `.env`
   - or export it in the shell
5. Check the environment:
   - `make doctor-env`

## Everyday Commands

| Task | Command |
| --- | --- |
| open the app loop | `probaboracle` |
| open the venv shell | `make env` |
| check the environment | `make doctor-env` |
| show session status | `make session-status` |
| run tests | `make check` |
| build the package | `make package-check` |
| lint tracked docs | `npm run lint:docs` |

The app loop is the default user-facing path. It opens the responsive header
and fixed selector, then generates one response at a time. `enter` selects, and
`esc` exits.

## Oracle Commands

Use these when you want the operator path instead of the app loop:

- `make ask PROMPT=what`
- `make what`
- `make when`
- `make why`
- `make where`

## Eval Commands

Storage:

- `make eval-init`
- `make list PROMPT=when LIMIT=10`

Sample generation:

- `make sample PROMPT=when COUNT=5`
- `make eval-what-5`
- `make eval-when-5`
- `make eval-why-5`
- `make eval-where-5`

Product verdicts:

- `make judge ID=1 VERDICT=pass NOTE="deadpan and vague"`
- `make pass ID=1 NOTE="deadpan and vague"`
- `make fail ID=2 NOTE="too concrete"`

Sidecar verdicts:

- `.venv/bin/python -m probaboracle judge-coherence 12 pass --note "one resolved sentence"`
- `.venv/bin/python -m probaboracle judge-relevance 12 pass --note "coherent and in-lane"`
- `.venv/bin/python -m probaboracle judge-absurdity 12 pass --note "coherent absurdity"`

## Eval Chart

The primary static chart is a prompt-lane stacked bar chart:

- x-axis: `what`, `when`, `why`, `where`
- segments: `fail`, `pass`, `pending`
- source: `eval_outputs.current_verdict` in `.local/evals.sqlite`

Commands:

- `make render-eval-chart-deps`
- `make render-eval-chart`

## Validation

Run the smallest check set that matches the change:

- tracked logic change:
  - `make check`
- docs change:
  - `npm run lint:docs`
  - `git diff --check`
- packaging or dependency metadata change:
  - `make package-check`
- eval persistence change:
  - `make eval-init`
  - `make sample PROMPT=what COUNT=1`
  - `make list PROMPT=what LIMIT=5`

If `OPENAI_API_KEY` is available and runtime generation changed, run one live
smoke:

- `make ask PROMPT=what`

## Long-Run Eval Loop

Use this when broad lane pressure matters.

1. Hold the current baseline steady.
2. Generate weighted batches when one lane is dragging.
3. Let rows accumulate as `untagged`.
4. Judge in sweeps.
5. Keep verdicts binary:
   - `pass`
   - `fail`
6. Treat repeated failure clusters as the signal for intervention.

Useful wrappers:

- `make sweep-gremlin`
- `make sweep-gremlin SWEEP_COUNT=3`
- `make sweep-rigorous`
- `make sweep-rigorous SWEEP_COUNT=3 SWEEP_LIST_LIMIT=10`

## Single-Product Signal Loop

Use this when isolating the strongest per-product signal for coherent
absurdity.

1. Generate one product:
   - `make sample PROMPT=what COUNT=1`
2. Judge it immediately:
   - coherence first
   - relevance second
   - coherent absurdity only if relevance fails after coherence passes
3. Repeat one product at a time.
4. Treat `25+` rows as the minimum useful checkpoint.
5. Treat `50-100` rows, or about one hour, as the real long-run surface.
6. Keep extra `when` pressure in the mix when testing the current coherence
   rule.

## Layered Eval Lenses

- Product fit is the strict oracle-quality gate.
- Coherence is the primary experimental gate:
  - `pass` = one resolved sentence with one dominant reasoning lane
  - `fail` = fragment stacking, one-line-list rhythm, hinge accumulation, or
    punctuation doing the reasoning work
  - for short lines, `2+` commas is a hard fail shortcut
- Prompt relevance asks whether a coherence-passing line stays in-lane.
- Coherent absurdity is only meaningful once coherence already passes.

## Command Ownership

- Human lead owns objective, scope, acceptance, and theory.
- Engineer owns implementation, validation, and Git flow.
- Keep bare `probaboracle` as the app path.
- Keep explicit subcommands as the operator path.
