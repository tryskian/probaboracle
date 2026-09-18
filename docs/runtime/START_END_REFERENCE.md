# Start / End Reference

This is the compact operator sheet for the canonical day-open/day-close
commands.

## Start

Command:

```bash
make start
```

Sequence:

1. Print workspace context:
  - repo root
  - active branch
  - `git status --short --branch`
2. Run the generic startup safety path:
  - `make doctor-env`
  - `make session-status`
3. Stop before repo action:
  - print the canonical rehydrate prompt
  - the prompt tells the agent to:
    - read `README.md`, `CHARTER`, `DECISIONS`, `ARCHITECTURE`, `RUNBOOK`, and `SESSION_HANDOFF`
    - return 5 bullets covering current state, risks, and next kernel
    - confirm repo path, host vs devcontainer mode, active branch, and whether the thread is on clean `main` or a feature branch
    - apply the no-guessing controls
    - run one active kernel at a time
    - execute the `Next Slice` from `SESSION_HANDOFF` with full validation

Source of truth:

- [tools/start_of_day_routine.sh](../../tools/start_of_day_routine.sh)

Shared power-control boundary:

- the external Coffee Codex plugin owns the one shared Mac-wide keep-awake
  session for Polinko and the toys
- Probaboracle start, preflight, and closeout leave that session unchanged
- the repository owns no power-control PID, process state, or Make target

## End

Command:

```bash
make end
```

Sequence:

1. Run the generic closeout safety path:
  - `make end-docs-check`
  - `make doctor-env`
  - tracked path leak check
  - local path leak audit
  - `make lint-docs`
  - `make scripts-check`
  - `make check`
  - `make package-check`
  - `make package-install-check`
  - `git diff --check`
  - `make end-pending-check`
  - `make security-checks`
2. Print the final repo state:
  - `make session-status`
3. Enforce the final git state:
  - `make end-git-check`

Preflight:

- `make end-preflight`
- runs the validation path without requiring clean synced `main`

Dependency maintenance:

- `make refresh-deps`
- run it after merged Dependabot or dependency metadata work, then run
  `make security-checks`

Source of truth:

- [tools/end_of_day_routine.sh](../../tools/end_of_day_routine.sh)
- [Makefile](../../Makefile)
