PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PY := $(BIN)/python
CAFFEINATE_SLOT ?= $(shell sh -c 'TTY=$$(tty 2>/dev/null || true); case "$$TTY" in /dev/*) SLOT="$${TTY#/dev/}" ;; *) SLOT="default" ;; esac; printf "%s" "$$SLOT" | tr -c "A-Za-z0-9_.-" "-"')
CAFFEINATE_PID_FILE ?= /tmp/probaboracle-caffeinate.$(CAFFEINATE_SLOT).pid
CAFFEINATE_LOG ?= /tmp/probaboracle-caffeinate.$(CAFFEINATE_SLOT).log
CAFFEINATE_CMD ?= /usr/bin/caffeinate -d -i -m
PROMPT ?= what
COUNT ?= 5
LIMIT ?= 20
ID ?=
NOTE ?=
VERDICT ?= pass
SWEEP_COUNT ?= 1
SWEEP_LIST_LIMIT ?= 20

LIST_ARGS = $(if $(PROMPT),--prompt-type $(PROMPT),) --limit $(LIMIT)

.PHONY: install env venv doctor-env check package-check ask sample eval-init list judge pass fail clean
.PHONY: caffeinate-on caffeinate-off caffeinate-off-all caffeinate-status decaffeinate caf decaf
.PHONY: render-eval-chart-deps render-eval-chart
.PHONY: what when why where
.PHONY: eval-what-5 eval-when-5 eval-why-5 eval-where-5
.PHONY: sweep-gremlin sweep-rigorous
.PHONY: session-status day-start sod eod eod-preflight eod-docs-check eod-git-check eod-stop

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

env venv:
	@test -d "$(VENV)" || (echo "Missing .venv. Run make install." && exit 1)
	@echo "Opening shell in $(VENV)"
	@. "$(BIN)/activate" && exec "$$SHELL" -i

doctor-env:
	@set -eu; \
	ACTIVE_VENV="$$(cd "$$(dirname "$(PY)")/.." && pwd)"; \
	VIRTUAL_ENV="$$ACTIVE_VENV" PATH="$$ACTIVE_VENV/bin:$$PATH" "$(PY)" -m probaboracle.doctor_env

session-status:
	@set -eu; \
	ACTIVE_VENV="$$(cd "$$(dirname "$(PY)")/.." && pwd)"; \
	echo "== Probaboracle Session Status =="; \
	echo "repo: $$(pwd)"; \
	echo "branch: $$(git branch --show-current)"; \
	if git diff --quiet --ignore-submodules HEAD -- && [ -z "$$(git ls-files --others --exclude-standard)" ]; then \
		echo "worktree: clean"; \
	else \
		echo "worktree: dirty"; \
	fi; \
	if [ -f ".local/evals.sqlite" ]; then \
		echo "eval db: .local/evals.sqlite"; \
		VIRTUAL_ENV="$$ACTIVE_VENV" PATH="$$ACTIVE_VENV/bin:$$PATH" "$(PY)" -c "from probaboracle.config import load_settings; from probaboracle.eval_db import counts; s=load_settings(); c=counts(s.eval_db_path); print(f\"evals: total={c['total']} pass={c['pass']} fail={c['fail']} pending={c['pending']}\")"; \
	else \
		echo "eval db: missing"; \
	fi; \
	echo ""; \
	echo "== Keep-awake =="; \
	$(MAKE) --no-print-directory caffeinate-status || true

caffeinate-on:
	@set -eu; \
	echo "slot: $(CAFFEINATE_SLOT)"; \
	if [ "$$(uname -s)" != "Darwin" ]; then \
		echo "caffeinate is macOS-only; skipping."; \
		exit 0; \
	fi; \
	if [ -f "$(CAFFEINATE_PID_FILE)" ]; then \
		PID=$$(cat "$(CAFFEINATE_PID_FILE)" 2>/dev/null || true); \
		if [ -n "$$PID" ] && kill -0 "$$PID" 2>/dev/null; then \
			echo "caffeinate already running (PID $$PID)."; \
			exit 0; \
		fi; \
		rm -f "$(CAFFEINATE_PID_FILE)"; \
	fi; \
	nohup $(CAFFEINATE_CMD) >"$(CAFFEINATE_LOG)" 2>&1 & \
	PID=$$!; \
	echo "$$PID" >"$(CAFFEINATE_PID_FILE)"; \
	sleep 0.1; \
	if kill -0 "$$PID" 2>/dev/null; then \
		echo "caffeinate started for slot $(CAFFEINATE_SLOT) (PID $$PID)."; \
	else \
		rm -f "$(CAFFEINATE_PID_FILE)"; \
		echo "Failed to start caffeinate."; \
		exit 1; \
	fi

caffeinate-off:
	@set -eu; \
	echo "slot: $(CAFFEINATE_SLOT)"; \
	if [ "$$(uname -s)" != "Darwin" ]; then \
		echo "caffeinate is macOS-only; skipping."; \
		exit 0; \
	fi; \
	if [ ! -f "$(CAFFEINATE_PID_FILE)" ]; then \
		echo "No managed caffeinate PID file found."; \
		exit 0; \
	fi; \
	PID=$$(cat "$(CAFFEINATE_PID_FILE)" 2>/dev/null || true); \
	if [ -n "$$PID" ] && kill -0 "$$PID" 2>/dev/null; then \
		kill "$$PID"; \
		sleep 0.1; \
		echo "caffeinate stopped for slot $(CAFFEINATE_SLOT) (PID $$PID)."; \
	else \
		echo "Stale PID file found; cleaning up."; \
	fi; \
	rm -f "$(CAFFEINATE_PID_FILE)"

caffeinate-off-all:
	@set -eu; \
	if [ "$$(uname -s)" != "Darwin" ]; then \
		echo "caffeinate is macOS-only; skipping."; \
		exit 0; \
	fi; \
	$(MAKE) --no-print-directory caffeinate-off || true; \
	PIDS=$$(pgrep -x caffeinate || true); \
	if [ -n "$$PIDS" ]; then \
		for PID in $$PIDS; do \
			kill "$$PID" 2>/dev/null || true; \
		done; \
		sleep 0.1; \
		echo "Stopped matching caffeinate processes: $$PIDS"; \
	else \
		echo "No matching caffeinate processes running."; \
	fi; \
	rm -f /tmp/probaboracle-caffeinate.*.pid

caffeinate-status:
	@set -eu; \
	echo "slot: $(CAFFEINATE_SLOT)"; \
	if [ "$$(uname -s)" != "Darwin" ]; then \
		echo "caffeinate status is only available on macOS."; \
		exit 0; \
	fi; \
	if [ -f "$(CAFFEINATE_PID_FILE)" ]; then \
		PID=$$(cat "$(CAFFEINATE_PID_FILE)" 2>/dev/null || true); \
		if [ -n "$$PID" ] && kill -0 "$$PID" 2>/dev/null; then \
			echo "Managed caffeinate: RUNNING (PID $$PID)."; \
		else \
			echo "Managed caffeinate: STALE PID file."; \
		fi; \
	else \
		echo "Managed caffeinate: OFF."; \
	fi; \
	ALL_PIDS=$$(pgrep -x caffeinate | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $$//' || true); \
	if [ -n "$$ALL_PIDS" ]; then \
		echo "Active caffeinate PIDs: $$ALL_PIDS"; \
	fi; \
	if command -v rg >/dev/null 2>&1; then \
		/usr/bin/pmset -g assertions | rg -n "PreventUserIdleDisplaySleep|PreventUserIdleSystemSleep|PreventDiskIdle|caffeinate" || true; \
	else \
		/usr/bin/pmset -g assertions | grep -nE "PreventUserIdleDisplaySleep|PreventUserIdleSystemSleep|PreventDiskIdle|caffeinate" || true; \
	fi

decaffeinate: caffeinate-off
caf: caffeinate-on
decaf: decaffeinate

day-start:
	@set -eu; \
	echo "== Probaboracle Start-of-Day =="; \
	CURRENT_BRANCH="$$(git branch --show-current)"; \
	if [ "$$CURRENT_BRANCH" = "main" ]; then \
		BRANCH_NAME="codex/bigbrain/sod-$$(date +%Y%m%d-%H%M%S)"; \
		echo "Creating feature branch: $$BRANCH_NAME"; \
		git checkout -b "$$BRANCH_NAME"; \
	fi; \
	echo "Read in order:"; \
	echo "  - README.md"; \
	echo "  - docs/governance/CHARTER.md"; \
	echo "  - docs/governance/DECISIONS.md"; \
	echo "  - docs/runtime/ARCHITECTURE.md"; \
	echo "  - docs/runtime/RUNBOOK.md"; \
	if [ -f "docs/governance/SESSION_HANDOFF.md" ]; then \
		echo "  - docs/governance/SESSION_HANDOFF.md"; \
	fi; \
	echo ""; \
	$(MAKE) --no-print-directory caffeinate-on; \
	$(MAKE) --no-print-directory doctor-env; \
	$(MAKE) --no-print-directory session-status

sod: day-start

eod:
	./scripts/end_of_day_routine.sh

eod-preflight:
	EOD_SKIP_GIT_CHECK=1 ./scripts/end_of_day_routine.sh

eod-docs-check:
	$(PY) ./scripts/check_eod_docs.py

eod-git-check:
	bash ./scripts/check_eod_git_clean.sh

eod-stop:
	@set -eu; \
	$(MAKE) --no-print-directory decaf || true; \
	$(MAKE) --no-print-directory session-status || true

check:
	$(PY) -m unittest discover -s tests -p 'test_*.py'

package-check:
	$(PY) -m build

render-eval-chart-deps:
	npm install

render-eval-chart:
	@test -d "node_modules" || (echo "Missing node_modules. Run make render-eval-chart-deps." && exit 1)
	$(PY) scripts/render_eval_chart.py

ask:
	$(PY) -m probaboracle ask $(PROMPT)

what:
	$(PY) -m probaboracle ask what

when:
	$(PY) -m probaboracle ask when

why:
	$(PY) -m probaboracle ask why

where:
	$(PY) -m probaboracle ask where

sample:
	$(PY) -m probaboracle sample $(PROMPT) --count $(COUNT)

eval-what-5:
	$(PY) -m probaboracle sample what --count 5

eval-when-5:
	$(PY) -m probaboracle sample when --count 5

eval-why-5:
	$(PY) -m probaboracle sample why --count 5

eval-where-5:
	$(PY) -m probaboracle sample where --count 5

eval-init:
	$(PY) -m probaboracle eval-init

list:
	$(PY) -m probaboracle eval-list $(LIST_ARGS)

judge:
	$(PY) -m probaboracle judge $(ID) $(VERDICT) --note "$(NOTE)"

pass:
	$(PY) -m probaboracle judge $(ID) pass --note "$(NOTE)"

fail:
	$(PY) -m probaboracle judge $(ID) fail --note "$(NOTE)"

sweep-gremlin:
	@set -eu; \
	i=0; \
	while [ "$$i" -lt "$(SWEEP_COUNT)" ]; do \
		echo "gremlin sweep $$((i + 1))/$(SWEEP_COUNT)"; \
		$(PY) -m probaboracle sample why --count 3; \
		$(PY) -m probaboracle sample what --count 1; \
		$(PY) -m probaboracle sample when --count 1; \
		$(PY) -m probaboracle sample where --count 1; \
		i=$$((i + 1)); \
	done

sweep-rigorous:
	@set -eu; \
	$(MAKE) --no-print-directory doctor-env; \
	$(MAKE) --no-print-directory eval-init; \
	$(MAKE) --no-print-directory sweep-gremlin SWEEP_COUNT="$(SWEEP_COUNT)"; \
	$(MAKE) --no-print-directory list LIMIT="$(SWEEP_LIST_LIMIT)"

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache build dist src/*.egg-info
