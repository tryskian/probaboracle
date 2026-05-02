# Runbook

## When to Read This

- Startup and environment checks
- Procedure lookup
- Local eval workflow

## Branch Policy

1. Work from a feature branch, not `main`.
2. Default branch prefix:
   - `codex/bigbrain/<task-name>`
3. Keep one logical change set per branch.

## Startup

1. Read in this order:
   - `README.md`
   - `docs/governance/CHARTER.md`
   - `docs/governance/DECISIONS.md`
   - `docs/runtime/ARCHITECTURE.md`
   - `docs/runtime/RUNBOOK.md`
   - `docs/governance/SESSION_HANDOFF.md`
2. Confirm active branch:
   - `git branch --show-current`
3. Create the local environment:
   - `make install`
4. Add live runtime credentials:
   - put `OPENAI_API_KEY` in the repo `.env` or export it in the shell
   - the local runtime auto-loads the repo `.env`
5. Check live runtime prerequisites:
   - `make doctor-env`

## Doc Map

- Repo framing:
  - [README.md](../../README.md)
- Durable rules:
  - [docs/governance/CHARTER.md](../governance/CHARTER.md)
- Durable decisions:
  - [docs/governance/DECISIONS.md](../governance/DECISIONS.md)
- Tracked beta findings:
  - [docs/research/README.md](../research/README.md)
- Runtime shape:
  - [docs/runtime/ARCHITECTURE.md](./ARCHITECTURE.md)
- Current checkpoint:
  - [docs/governance/SESSION_HANDOFF.md](../governance/SESSION_HANDOFF.md)
- Public diagrams:
  - [docs/diagrams/PIPELINE.md](../diagrams/PIPELINE.md)
  - [docs/diagrams/EVAL_CHART.md](../diagrams/EVAL_CHART.md)

## Command Surface

- Install:
  - `make install`
- Codex cloud environment setup:
  - `./scripts/cloud-setup.sh`
  - creates a feature branch automatically when the environment starts on
    `main`
- Codex cloud environment maintenance:
  - `./scripts/cloud-maintenance.sh`
- Open the local venv shell:
  - `make env`
  - alias: `make venv`
- Environment sanity:
  - `make doctor-env`
- Session snapshot:
  - `make session-status`
- Run one oracle lane:
  - `make ask PROMPT=what`
  - shortcuts:
    - `make what`
    - `make when`
    - `make why`
    - `make where`
- Generate a five-sample eval batch quickly:
  - `make eval-what-5`
  - `make eval-when-5`
  - `make eval-why-5`
  - `make eval-where-5`
- Create local eval storage:
  - `make eval-init`
- Generate local eval samples:
  - `make sample PROMPT=when COUNT=5`
  - reads the repo `.env` automatically when present
- Weighted gremlin sweep:
  - `make sweep-gremlin`
  - optional:
    - `make sweep-gremlin SWEEP_COUNT=3`
- Rigorous sweep wrapper:
  - `make sweep-rigorous`
  - optional:
    - `make sweep-rigorous SWEEP_COUNT=3 SWEEP_LIST_LIMIT=10`
- List recent outputs:
  - `make list PROMPT=when LIMIT=10`
- Record a verdict:
  - `make judge ID=1 VERDICT=pass NOTE="deadpan and vague"`
- Record a coherence verdict:
  - `.venv/bin/python -m probaboracle judge-coherence 12 pass --note "one resolved sentence"`
- Record a prompt relevance verdict:
  - `.venv/bin/python -m probaboracle judge-relevance 12 pass --note "coherent and in-lane"`
- Record a coherent absurdity verdict:
  - `.venv/bin/python -m probaboracle judge-absurdity 12 pass --note "coherent absurdity"`
- Shortcut verdict targets:
  - `make pass ID=1 NOTE="deadpan and vague"`
  - `make fail ID=2 NOTE="too concrete"`
- Run local tests:
  - `make check`
- Build the package locally:
  - `make package-check`
  - build the Python package and verify metadata still resolves.
- Lint tracked docs:
  - `npm run lint:docs`
- `make render-eval-chart-deps`
  - install the explicit Node dependencies for the static D3 renderer.
- `make render-eval-chart`
  - render the current PASS/FAIL/PENDING lane chart from `.local/evals.sqlite`
    into `docs/diagrams/probaboracle-pass-fail.svg`.

## Eval Chart

Probaboracle's primary static chart is a strict stacked bar chart:

- x-axis: prompt lane (`what`, `when`, `why`, `where`)
- segments: `fail`, `pass`, `pending`
- source of truth: `eval_outputs.current_verdict` in `.local/evals.sqlite`

This chart is intentionally simple. It is the binary pulse surface first, not a
failure-taxonomy dashboard.

## Command Ownership Rule

1. Human lead does not run terminal work as the normal workflow.
2. Engineer runs implementation, validation, and Git flow end to end.
3. Human control stays on objective, scope, acceptance, and theory.

## Validation Rule

1. Run `make check` for tracked logic changes.
2. Run `make package-check` when packaging or dependency metadata changes.
3. Run one live `make ask PROMPT=<type>` smoke if `OPENAI_API_KEY` is present.
4. If eval persistence changes, run:
   - `make eval-init`
   - `make sample PROMPT=what COUNT=1`
   - `make list PROMPT=what LIMIT=5`

## Long-Run Eval Loop

1. Hold the current baseline steady during the run.
2. Generate samples in weighted batches when one lane is dragging:
   - for example:
     - `why x3`
     - `what x1`
     - `when x1`
     - `where x1`
3. Let new rows accumulate as `untagged`.
4. Judge in sweeps, not one row at a time.
5. Keep verdicts hard binary:
   - `pass`
   - `fail`
6. Treat repeated failure clusters as the intervention signal.
7. Do not add new prompt layers unless the failures are strong enough to earn
   a real runtime change.

## Single-Product Signal Loop

1. Use this loop when the goal is isolating the strongest per-product signal
   for a selective downstream gate.
2. Generate one product at a time:
   - for example:
     - `make sample PROMPT=what COUNT=1`
3. Judge that one product immediately:
   - coherence first
   - relevance second
   - coherent absurdity only if relevance fails after coherence passes
4. Repeat one product at a time instead of pooling a larger batch.
5. Prefer this loop over broader sweeps when testing coherent absurdity.

## Layered Eval Lenses

1. Product fit stays the stricter oracle-quality gate.
2. Coherence is the primary experimental gate:
   - `pass` = one resolved sentence with one dominant reasoning lane
   - `fail` = fragment stacking, one-line-list rhythm, hinge accumulation, or
     punctuation doing the reasoning work
3. Prompt relevance asks whether a coherence-passing line stays in-lane for the
   selected prompt type.
4. Coherent absurdity is only meaningful once coherence is already passing.
