# Runbook

This is the operator guide for local setup, commands, validation, and eval work.

Use `docs/runtime/ARCHITECTURE.md` for system shape. Use this file when you need to run or check something.

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
5. For any live API work, keep the token monitoring dashboard available:
   - `make open-cost-console`
   - use `make open-limits` or `make open-usage` directly when a tighter check is enough
6. Check the environment:
   - `make doctor-env`

## Everyday Commands

| Task | Command |
| --- | --- |
| open the app loop | `probaboracle` |
| open the venv shell | `make env` |
| check the environment | `make doctor-env` |
| show session status | `make session-status` |
| lint Python files | `make lint` |
| check Python formatting | `make format-check` |
| run tests | `make check` |
| build the package | `make package-check` |
| lint tracked docs | `npm run lint:docs` |
| open the OpenAI limits page | `make open-limits` |
| open the OpenAI usage page | `make open-usage` |
| open the OpenAI billing page | `make open-billing` |
| open all three OpenAI cost pages | `make open-cost-console` |

The app loop is the default user-facing path. It opens the responsive header and fixed selector, then generates one response at a time. `enter` selects, and `esc` exits.

## Rate And Credit Operator Guardrails

1. Treat throughput and spend as separate control planes:
   - rate limits (`RPM`, `TPM`, queue limits)
   - usage/billing (token burn, budget, credits)
2. Cost posture:
   - keep one-off checks small
   - use short judged batches by default
   - treat extended serial runs as explicit batch work
3. Watch dashboards as part of normal operation:
   - `make open-limits`
   - `make open-usage`
   - `make open-billing`
   - or one-shot: `make open-cost-console`
4. Live API rule:
   - keep the token monitoring dashboard open or immediately reachable during live eval work
   - recheck it before widening a batch or starting an extended run
5. Efficiency defaults:
   - keep the prompt surface narrow
   - keep one response per command path
   - keep the live eval lens narrow before widening

## Repo Hygiene

- Dependabot-managed update PRs carry the `dependencies` label.
- `.github/workflows/stale-dependency-prs.yml` marks dependency PRs stale after `14` idle days and closes them after `7` more.
- The stale workflow is scoped to dependency-labelled PRs, not the normal human work queue.

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
- `.venv/bin/python -m probaboracle eval-list --prompt-type when --limit 10 --include-archived`
- `make archive-pending`
- `make archive-pending ARCHIVE_NOTE="stale pending archive before the next long run"`

Sample generation:

- `make sample PROMPT=when COUNT=5`
- `make eval-what-5`
- `make eval-when-5`
- `make eval-why-5`
- `make eval-where-5`

Local notebook operator lane:

- local path: `.local/notebooks/probaboracle-eval-viz.ipynb`
- use the built-in notebook helpers for:
  - recent active rows
  - pass/fail stamps
  - sidecar stamps
  - archived-surface inspection
  - stale pending archive operations

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
- source: active `eval_outputs.current_verdict` rows in `.local/evals.sqlite`

Commands:

- `make render-eval-chart-deps`
- `make render-eval-chart`

## Validation

Run the smallest check set that matches the change:

- tracked logic change:
  - `make check`
- Python-only style change:
  - `make format-check`
  - `make lint`
- docs change:
  - `npm run lint:docs`
  - `git diff --check`
- packaging or dependency metadata change:
  - `make package-check`
- eval persistence change:
  - `make eval-init`
  - `make sample PROMPT=what COUNT=1`
  - `make list PROMPT=what LIMIT=5`

If `OPENAI_API_KEY` is available and runtime generation changed, run one live smoke:

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
6. Treat the loop explicitly as:
   - `pass / fail`
   - if `fail`, decide `retain / evict`
   - rerun
   - `pass / fail`
7. If a row or family fails, decide the lane state:
   - `retain`
   - `evict`
8. `retain` means keep the current rule and keep taking pressure.
9. `evict` means the family has earned an upstream correction and should stop
   clogging the active queue.
10. Treat stale unresolved product rows as archive candidates, not as live
   backlog forever.
11. Treat repeated failure clusters as the evidence surface for the
    `retain / evict` decision, not as automatic intervention.

Useful wrappers:

- `make sweep-gremlin`
- `make sweep-gremlin SWEEP_COUNT=3`
- `make sweep-rigorous`
- `make sweep-rigorous SWEEP_COUNT=3 SWEEP_LIST_LIMIT=10`

## Single-Product Signal Loop

Use this when isolating the strongest per-product signal for coherent absurdity.

1. Generate one product:
   - `make sample PROMPT=what COUNT=1`
2. Judge it immediately:
   - coherence first
   - relevance second
   - coherent absurdity only if relevance fails after coherence passes
3. Repeat one product at a time.
4. Treat `25+` rows as the minimum useful checkpoint.
5. Treat `50-100` rows, or about one hour, as the real long-run surface.
6. Keep extra `when` pressure in the mix when testing the current coherence rule.
7. Before an extended rerun, archive stale product-pending rows out of the active surface:
   - `make archive-pending ARCHIVE_NOTE="stale pending archive before tandem rerun"`
8. For an extended rerun, pair one generator with one tandem judge:
   - generator creates fresh rows only
   - tandem judge stamps product immediately, plus coherence and relevance on passes
   - keep the tandem judge scoped to the fresh run ids
9. Let the tandem judge stop only after:
   - the generator is done
   - the fresh product queue is empty
10. After the run, decide whether the dominant fail family is still:
    - `retain`
    - `evict`
11. Only reroute or tighten the runtime after the family has actually earned
    `evict`.

## Layered Eval Lenses

- Product fit is the strict oracle-quality gate.
- Coherence is the primary experimental gate:
  - `pass` = one resolved sentence with one dominant reasoning lane
  - `fail` = fragment stacking, one-line-list rhythm, hinge accumulation, or punctuation doing the reasoning work
  - for short lines, `2+` commas is a hard fail shortcut
- Prompt relevance asks whether a coherence-passing line stays in-lane.
- Coherent absurdity is only meaningful once coherence already passes.

## Command Ownership

- Human lead owns objective, scope, acceptance, and theory.
- Engineer owns implementation, validation, and Git flow.
- Keep bare `probaboracle` as the app path.
- Keep explicit subcommands as the operator path.
