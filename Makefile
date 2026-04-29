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
SWEEP_COUNT ?= 1
SWEEP_LIST_LIMIT ?= 20

LIST_ARGS = $(if $(PROMPT),--prompt-type $(PROMPT),) --limit $(LIMIT)

.PHONY: install env venv doctor-env check package-check ask sample eval-init list judge pass fail clean
.PHONY: render-eval-chart-deps render-eval-chart
.PHONY: what when why where
.PHONY: eval-what-5 eval-when-5 eval-why-5 eval-where-5
.PHONY: sweep-gremlin sweep-rigorous
.PHONY: session-status day-start sod eod

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
	fi

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
	$(MAKE) --no-print-directory doctor-env; \
	$(MAKE) --no-print-directory session-status

sod: day-start

eod:
	@set -eu; \
	echo "== Probaboracle End-of-Day =="; \
	$(MAKE) --no-print-directory session-status; \
	echo ""; \
	echo "Recent outputs:"; \
	$(MAKE) --no-print-directory list LIMIT=5 || true

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
