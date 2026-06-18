PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PY := $(BIN)/python
PROMPT ?= what
COUNT ?= 5
LIMIT ?= 20
ID ?=
NOTE ?=
VERDICT ?= pass
ARCHIVE_NOTE ?= stale pending archive
PULSE_LABEL ?= anchor
PULSE_REASON ?=
PULSE_START_ID ?=
PULSE_END_ID ?=
PULSE_MINUTES ?= 15
PULSE_INTERVAL_SECONDS ?= 60
SWEEP_COUNT ?= 1
SWEEP_LIST_LIMIT ?= 20
OPENAI_LIMITS_URL ?= https://platform.openai.com/settings/organization/limits
OPENAI_USAGE_URL ?= https://platform.openai.com/settings/organization/usage
OPENAI_BILLING_URL ?= https://platform.openai.com/settings/organization/billing/overview
CAFFEINATE_PID_FILE ?= /tmp/probaboracle-caffeinate.pid
CAFFEINATE_LOG ?= /tmp/probaboracle-caffeinate.log
CAFFEINATE_CMD ?= /usr/bin/caffeinate -d -i -m
PIP_AUDIT_ARGS ?=

LIST_ARGS = $(if $(PROMPT),--prompt-type $(PROMPT),) --limit $(LIMIT)

.PHONY: install refresh-deps env venv doctor-env path-leak-check path-leak-audit-local test lint format-check format typecheck precommit-install precommit-run prepush-run check package-check end-pending-check ask sample eval-init list archive-pending judge pass fail eval-pulse-start eval-pulse-label eval-pulse-report clean
.PHONY: lint-docs end-docs-check package-install-check python-security-check node-security-check security-checks
.PHONY: render-eval-chart-deps render-eval-chart
.PHONY: what when why where
.PHONY: eval-what-5 eval-when-5 eval-why-5 eval-where-5
.PHONY: sweep-gremlin sweep-rigorous
.PHONY: session-status
.PHONY: open-limits open-usage open-billing open-cost-console
.PHONY: caffeinate decaffeinate caffeinate-status decaffeinate-status
.PHONY: start end end-preflight end-git-check rituals

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

refresh-deps:
	@test -d "$(VENV)" || $(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade --upgrade-strategy eager -e ".[dev]"
	npm install --no-audit --no-fund

env venv:
	@test -d "$(VENV)" || (echo "Missing .venv. Run make install." && exit 1)
	@echo "Opening shell in $(VENV)"
	@. "$(BIN)/activate" && exec "$$SHELL" -i

doctor-env:
	@set -eu; \
	ACTIVE_VENV="$$(cd "$$(dirname "$(PY)")/.." && pwd)"; \
	VIRTUAL_ENV="$$ACTIVE_VENV" PATH="$$ACTIVE_VENV/bin:$$PATH" "$(PY)" -m probaboracle.doctor_env

path-leak-check:
	$(PY) ./scripts/path_leak_check.py --scope tracked

path-leak-audit-local:
	$(PY) ./scripts/path_leak_check.py --scope local

lint:
	$(PY) -m ruff check scripts src tests

format-check:
	$(PY) -m ruff format --check scripts src tests

format:
	$(PY) -m ruff format scripts src tests

test:
	$(PY) -m unittest discover -s tests -p 'test_*.py'

typecheck:
	PYTHONPATH=src $(PY) -m mypy src tests scripts

lint-docs:
	npm run lint:docs

precommit-install:
	$(PY) -m pre_commit install --install-hooks --hook-type pre-commit --hook-type pre-push

precommit-run:
	$(PY) -m pre_commit run --all-files

prepush-run:
	$(PY) -m pre_commit run --all-files --hook-stage pre-push

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
	fi

open-limits:
	@set -eu; \
	URL="$(OPENAI_LIMITS_URL)"; \
	if command -v open >/dev/null 2>&1; then \
		open "$$URL"; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open "$$URL" >/dev/null 2>&1 || true; \
	else \
		echo "Open this URL in your browser: $$URL"; \
	fi; \
	echo "OpenAI limits URL: $$URL"

open-usage:
	@set -eu; \
	URL="$(OPENAI_USAGE_URL)"; \
	if command -v open >/dev/null 2>&1; then \
		open "$$URL"; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open "$$URL" >/dev/null 2>&1 || true; \
	else \
		echo "Open this URL in your browser: $$URL"; \
	fi; \
	echo "OpenAI usage URL: $$URL"

open-billing:
	@set -eu; \
	URL="$(OPENAI_BILLING_URL)"; \
	if command -v open >/dev/null 2>&1; then \
		open "$$URL"; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open "$$URL" >/dev/null 2>&1 || true; \
	else \
		echo "Open this URL in your browser: $$URL"; \
	fi; \
	echo "OpenAI billing URL: $$URL"

open-cost-console:
	@set -eu; \
	$(MAKE) --no-print-directory open-limits; \
	$(MAKE) --no-print-directory open-usage; \
	$(MAKE) --no-print-directory open-billing

caffeinate:
	@set -eu; \
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
		echo "caffeinate started (PID $$PID)."; \
	else \
		rm -f "$(CAFFEINATE_PID_FILE)"; \
		echo "Failed to start caffeinate."; \
		exit 1; \
	fi

decaffeinate:
	@set -eu; \
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
		echo "caffeinate stopped (PID $$PID)."; \
	else \
		echo "Stale PID file found; cleaning up."; \
	fi; \
	rm -f "$(CAFFEINATE_PID_FILE)"

caffeinate-status:
	@set -eu; \
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
		EXISTING_PID=$$(pgrep -f "^/usr/bin/caffeinate -d -i -m( |$$)" | head -n 1 || true); \
		if [ -n "$$EXISTING_PID" ]; then \
			echo "Unmanaged caffeinate detected (PID $$EXISTING_PID); not owned by this repo."; \
		fi; \
	fi

decaffeinate-status: caffeinate-status

start:
	bash ./tools/start_of_day_routine.sh

end:
	bash ./tools/end_of_day_routine.sh

end-preflight:
	end_SKIP_GIT_CHECK=1 bash ./tools/end_of_day_routine.sh

end-pending-check:
	PYTHONPATH=src $(PY) ./scripts/check_end_pending.py

end-git-check:
	bash ./scripts/check_end_git_clean.sh

rituals:
	@cat docs/runtime/START_END_REFERENCE.md

check:
	$(MAKE) --no-print-directory format-check
	$(MAKE) --no-print-directory lint
	$(MAKE) --no-print-directory typecheck
	$(MAKE) --no-print-directory test

package-check:
	$(PY) -m build

package-install-check:
	$(PY) -m pip install --no-deps -e .
	$(PY) -c "import importlib; importlib.import_module('probaboracle'); importlib.import_module('probaboracle.main')"

python-security-check:
	$(PY) -m pip_audit $(PIP_AUDIT_ARGS)

node-security-check:
	npm audit --audit-level=moderate

security-checks: python-security-check node-security-check

end-docs-check:
	$(PY) ./scripts/check_end_docs.py

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

archive-pending:
	$(PY) -m probaboracle archive-pending --note "$(ARCHIVE_NOTE)"

judge:
	$(PY) -m probaboracle judge $(ID) $(VERDICT) --note "$(NOTE)"

pass:
	$(PY) -m probaboracle judge $(ID) pass --note "$(NOTE)"

fail:
	$(PY) -m probaboracle judge $(ID) fail --note "$(NOTE)"

eval-pulse-start:
	$(PY) -m probaboracle eval-pulse-start $(PROMPT) --minutes $(PULSE_MINUTES) --interval-seconds $(PULSE_INTERVAL_SECONDS)

eval-pulse-label:
	$(PY) -m probaboracle eval-pulse-label $(ID) $(PULSE_LABEL) $(if $(PULSE_REASON),--reason "$(PULSE_REASON)",)

eval-pulse-report:
	$(PY) -m probaboracle eval-pulse-report $(PULSE_START_ID) $(PULSE_END_ID)

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
