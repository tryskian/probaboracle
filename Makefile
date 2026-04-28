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

LIST_ARGS = $(if $(PROMPT),--prompt-type $(PROMPT),) --limit $(LIMIT)

.PHONY: install doctor-env check ask sample eval-init list pass fail clean

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

doctor-env:
	@test -d "$(VENV)" || (echo "Missing .venv. Run make install." && exit 1)
	@test -n "$$OPENAI_API_KEY" || (echo "Missing OPENAI_API_KEY." && exit 1)
	@echo "Environment looks ready."

check:
	$(PY) -m unittest discover -s tests -p 'test_*.py'

ask:
	$(PY) -m probaboracle ask $(PROMPT)

sample:
	$(PY) -m probaboracle sample $(PROMPT) --count $(COUNT)

eval-init:
	$(PY) -m probaboracle eval-init

list:
	$(PY) -m probaboracle eval-list $(LIST_ARGS)

pass:
	$(PY) -m probaboracle eval-judge $(ID) pass --note "$(NOTE)"

fail:
	$(PY) -m probaboracle eval-judge $(ID) fail --note "$(NOTE)"

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache
