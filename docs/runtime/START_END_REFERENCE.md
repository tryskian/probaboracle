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
  - print the canonical docs to read:
    - `README.md`
    - `docs/governance/CHARTER.md`
    - `docs/governance/DECISIONS.md`
    - `docs/runtime/ARCHITECTURE.md`
    - `docs/runtime/RUNBOOK.md`
    - `docs/governance/SESSION_HANDOFF.md`
  - give the startup read
  - name exactly one active kernel
  - do not branch, search, or edit until that is stated

Source of truth:

- [tools/start_of_day_routine.sh](../../tools/start_of_day_routine.sh)

## End

Command:

```bash
make end
```

Sequence:

1. Run the generic closeout safety path:
  - `make doctor-env`
  - `npm run lint:docs`
  - `make check`
  - `git diff --check`
2. Print the final repo state:
  - `make session-status`

Probaboracle does not keep a long-lived local daemon or caffeinate process, so
the final stop path is intentionally small.

Source of truth:

- [tools/end_of_day_routine.sh](../../tools/end_of_day_routine.sh)
- [Makefile](../../Makefile)
