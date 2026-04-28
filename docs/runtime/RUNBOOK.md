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
4. Check live runtime prerequisites:
   - `make doctor-env`

## Command Surface

- Install:
  - `make install`
- Environment sanity:
  - `make doctor-env`
- Run one oracle lane:
  - `make ask PROMPT=what`
- Create local eval storage:
  - `make eval-init`
- Generate local eval samples:
  - `make sample PROMPT=when COUNT=5`
- List recent outputs:
  - `make list PROMPT=when LIMIT=10`
- Judge an output:
  - `make pass ID=1 NOTE="deadpan and vague"`
  - `make fail ID=2 NOTE="too concrete"`
- Run local tests:
  - `make check`

## Command Ownership Rule

1. Human lead does not run terminal work as the normal workflow.
2. Engineer runs implementation, validation, and Git flow end to end.
3. Human control stays on objective, scope, acceptance, and theory.

## Validation Rule

1. Run `make check` for tracked logic changes.
2. Run one live `make ask PROMPT=<type>` smoke if `OPENAI_API_KEY` is present.
3. If eval persistence changes, run:
   - `make eval-init`
   - `make sample PROMPT=what COUNT=1`
   - `make list PROMPT=what LIMIT=5`
