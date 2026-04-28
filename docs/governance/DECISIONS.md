# Decisions Log

This file is the durable archive of Probaboracle's engineering, runtime, and
eval decisions. Keep entries short and operational.

## Taxonomy

- `runtime_engineering`
- `eval_quality`
- `collaboration_method`
- `workflow_environment`

## D-001: Local CLI first

- Category: `runtime_engineering`
- Tags: `local_first`, `cli`, `small_surface`
- Decision: Start with a local CLI runtime before any broader surface.
- Why: Keeps setup light and preserves tokens for actual product shaping.

## D-002: Fixed prompt surface

- Category: `runtime_engineering`
- Tags: `prompt_surface`, `safety_scope`, `constrained_input`
- Decision: Limit the active prompt types to `what`, `when`, `why`, and `where`.
- Why: The product is a constrained oracle instrument, not an open chat tool.

## D-003: Binary eval gates

- Category: `eval_quality`
- Tags: `pass_fail`, `polinko_lineage`, `strict_judgment`
- Decision: Keep human eval verdicts strictly binary: `pass` or `fail`.
- Why: This carries the same pass/fail discipline as the wider Polinko work.

## D-004: Agent-backed generation

- Category: `runtime_engineering`
- Tags: `agents_sdk`, `model_native`, `non_template_runtime`
- Decision: Use the OpenAI Agents SDK as the runtime generation path.
- Why: The app should generate through a real model path, not stitched fragment
  composition.

## D-005: Small doc stack

- Category: `workflow_environment`
- Tags: `docs_stack`, `runbook`, `architecture`
- Decision: Use a trimmed Polinko-style doc stack: charter, decisions,
  architecture, runbook, session handoff, and diagrams.
- Why: Keeps local instruction surfaces clear without dragging in unnecessary
  overhead.

## D-006: Python plus Makefile bootstrap

- Category: `workflow_environment`
- Tags: `python`, `make`, `venv`
- Decision: Bootstrap with Python, a local `.venv`, and one small Makefile
  command surface.
- Why: It is the lightest path that still matches the broader Polinko working
  model.
