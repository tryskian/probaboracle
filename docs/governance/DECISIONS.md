# Decisions Log

This file is the durable archive of Probaboracle's engineering, runtime, and
eval decisions.

## How To Use This File

- Need the current durable rules:
  - start with `docs/governance/CHARTER.md`
- Need the current system shape:
  - use `docs/runtime/ARCHITECTURE.md`
- Need the reasoning behind a repo choice:
  - use this file

Keep entries short, but informative enough to show what changed and why.

## Taxonomy

- `runtime_engineering`
- `eval_quality`
- `collaboration_method`
- `workflow_environment`

## D-001: Local CLI first

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `local_first`, `cli`, `small_surface`
- Decision:
  - start with a local CLI runtime before any broader surface
  - keep the first execution path terminal-native and local
- Why: Keeps setup light and preserves tokens for actual product shaping.

## D-002: Fixed prompt surface

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `prompt_surface`, `safety_scope`, `constrained_input`
- Decision:
  - limit the active prompt types to:
    - `what`
    - `when`
    - `why`
    - `where`
  - do not accept freeform prompt input in the active runtime path
- Why: The product is a constrained oracle instrument, not an open chat tool;
  the fixed prompts are a reasoning-scope boundary for the interaction, not a
  claim that the runtime itself is mechanically simple.

## D-003: Binary eval gates

- Date: `2026-04-28`
- Category: `eval_quality`
- Tags: `pass_fail`, `polinko_lineage`, `strict_judgment`
- Decision:
  - keep human eval verdicts strictly binary:
    - `pass`
    - `fail`
  - do not add mixed or partial verdict states
- Why: This carries the same pass/fail discipline as the wider Polinko work.

## D-004: Agent-backed generation

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `agents_sdk`, `model_native`, `non_template_runtime`
- Decision:
  - use the OpenAI Agents SDK as the runtime generation path
  - do not build the active oracle path out of stitched static fragments
- Why: The app should generate through a real model path, not stitched fragment
  composition.

## D-005: Small doc stack

- Date: `2026-04-28`
- Category: `workflow_environment`
- Tags: `docs_stack`, `runbook`, `architecture`
- Decision:
  - use a trimmed Polinko-style doc stack:
    - charter
    - decisions
    - architecture
    - runbook
    - session handoff
    - diagrams
- Why: Keeps local instruction surfaces clear without dragging in unnecessary
  overhead.

## D-006: Python plus Makefile bootstrap

- Date: `2026-04-28`
- Category: `workflow_environment`
- Tags: `python`, `make`, `venv`
- Decision:
  - bootstrap with Python
  - use a local `.venv`
  - expose one small Makefile command surface for operator actions
- Why: It is the lightest path that still matches the broader Polinko working
  model.

## D-007: Explicit Polinko lineage

- Date: `2026-04-28`
- Category: `collaboration_method`
- Tags: `polinko_lineage`, `scope_relation`, `shared_discipline`
- Decision:
  - frame Probaboracle explicitly as a mini project within Polinko
  - do not present it as a disconnected side repo
- Why: The runtime is smaller, but the safety posture, eval discipline, and
  systems thinking are continuous with the wider research project.

## D-008: Shared style signals are cues, not a word bank

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `style_signals`, `human_direction`, `model_reasoning`, `non_template_runtime`
- Decision:
  - use one shared style-signal resource across all prompt types
  - let prompt type control the reasoning lane, not the flavour pool
  - treat the style signals as compositional cues rather than as a fixed
    lexical pool
  - keep the model free to synthesize beyond the literal words provided
  - this shape was explicitly clarified through human direction during the tone
    pass
- Why: The prompt type should control the reasoning lane, while the model
  remains free to synthesize beyond the literal words provided.

## D-009: Hold the baseline and learn from failures

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `baseline`, `pass_fail`, `polinko_method`, `prompt_drift`
- Decision:
  - keep the runtime baseline simple during long eval runs
  - prefer long sample streams plus hard `pass` / `fail` judgment sweeps over
    layering more prompt instructions
  - only change the runtime contract when repeated failures are strong enough
    to earn a real intervention
- Why: This keeps Probaboracle on the Polinko line. The model should reveal its
  real habits through data, then learn from what fails, rather than being
  smothered under prompt accretion.

## D-010: Matched prompt scope and one-node generation

- Date: `2026-04-29`
- Category: `runtime_engineering`
- Tags: `matched_scope`, `safe_interaction`, `minimal_config`, `one_node_generation`
- Decision:
  - keep the fixed prompt surface matched to the intended reasoning scope
  - treat that matched scope as a material guardrail for safe interaction,
    drift control, and preserving the reasoning slope
  - keep runtime config minimal
  - express the target reasoning shape through concise directions rather than a
    long list of restrictions
  - generate words through one model node with shared vocabulary, while prompt
    type constrains the reasoning lane
- Why: Vocabulary is universal. The prompts should bound the kind of reasoning
  the oracle performs, while the model still resolves the actual sentence
  structure in one generation path.

## D-011: Coherence is the primary experimental gate

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `coherence`, `sidecar_eval`, `research_method`
- Decision:
  - treat sentence coherence as the primary experimental binary gate
  - keep product fit separate from coherence
  - evaluate coherence with a dedicated sidecar verdict:
    - `pass`
    - `fail`
- Why: The research question is whether the model can maintain coherent
  sentence reasoning inside constrained guardrails. Product taste is a
  stricter downstream layer, not the core experiment.

## D-012: Downstream eval lenses stay separate

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `relevance`, `absurdity`, `handwaving`, `layered_judgment`
- Decision:
  - keep prompt relevance as its own binary sidecar
  - evaluate coherent absurdity separately from prompt relevance
  - evaluate answer-shaped hand waving separately from both
  - do not collapse these lenses back into one overloaded verdict
- Why: Some responses are coherent but out-of-lane, and some out-of-lane
  responses are still valuable oracle behaviour. Separate binary lenses make
  those distinctions visible instead of flattening them.
