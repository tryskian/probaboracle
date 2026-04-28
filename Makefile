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

LIST_ARGS = $(if $(PROMPT),--prompt-type $(PROMPT),) --limit $(LIMIT)

.PHONY: install env venv doctor-env check ask sample eval-init list judge pass fail clean
.PHONY: what when why where
.PHONY: eval-what-5 eval-when-5 eval-why-5 eval-where-5

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

env venv:
	@test -d "$(VENV)" || (echo "Missing .venv. Run make install." && exit 1)
	@echo "Opening shell in $(VENV)"
	@. "$(BIN)/activate" && exec "$$SHELL" -i

doctor-env:
	@test -d "$(VENV)" || (echo "Missing .venv. Run make install." && exit 1)
	@test -n "$$OPENAI_API_KEY" || (echo "Missing OPENAI_API_KEY." && exit 1)
	@echo "Environment looks ready."

check:
	$(PY) -m unittest discover -s tests -p 'test_*.py'

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

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache
