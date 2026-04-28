# Decisions Log

This file records the durable shaping choices behind Probaboracle.

It is the place for human-engineer decisions that explain why the repo looks the way it does, not a changelog of every edit.

## How To Use This File

- Need the current contract:
  - start with [CHARTER.md](./CHARTER.md) and [docs/runtime/ARCHITECTURE.md](../runtime/ARCHITECTURE.md)
- Need procedure:
  - use [docs/runtime/RUNBOOK.md](../runtime/RUNBOOK.md)
- Need the why behind a weird or deliberate choice:
  - scan this file

## Entry Style

- Keep entries short.
- `Human input` captures the product or workflow push from the imagineer.
- `Engineer choice` captures the implementation or repo-shape decision.
- `Why` captures the durable rationale.

## D-001: Local oracle harness

- Human input: Keep the app tiny and inspectable.
- Engineer choice: Keep the surface as a local CLI and keep the active runtime small enough to inspect end-to-end.
- Why: The product works better as a small constrained machine than as an app shell or orchestration stack.

## D-002: Prompt-type guardrail

- Human input: The user selects the prompt shape directly.
- Engineer choice: Limit prompt types to `what`, `when`, `how`, `why`, and `where`.
- Why: The narrow frame is the product boundary and a guardrail for safe human-AI interaction.

## D-003: Binary eval semantics

- Human input: The eval call should be clear, not mushy.
- Engineer choice: Keep local SQLite verdicts binary only: `pass` or `fail`.
- Why: Forcing the judge to land or reject is better than inventing a soft middle bucket.

## D-004: Local node generation

- Human input: The output should think like a real LLM inside hard tone and purpose guardrails, not just arrange fragments into a sentence.
- Engineer choice: Route each prompt type into a small semantic node pipeline and let the composition produce the line.
- Why: The right live shape is neither rigid canned phrases nor loose oracle soup.

## D-011: Simple semantic node pipeline

- Human input: What mattered in the earlier local version was not canned phrasing but the simple shape: certainty words, indecision words, connective hinges, and soft conclusions.
- Engineer choice: Treat the pipeline as a small semantic node system rather than either a bank of full phrases or a giant freeform oracle prompt.
- Why: The product gets more life from a little structure than from either brittle templates or loose poetic soup.

## D-012: Archive the API experiment, keep the evals

- Human input: The local node generator was working better than the API build for the current goal, but the experiment and eval evidence should stay recoverable.
- Engineer choice: Archive the agent/API runtime snapshot and the live SQLite DB locally under `.probaboracle/archive/2026-04-28-agent-runtime-experiment/`, then return the active repo to the local node path.
- Why: It keeps the experiment recoverable without forcing the active runtime down the wrong path.

## D-005: README product framing

- Human input: Frame Probaboracle as a tiny unhelpful oracle chatbot and keep the policy language straight where it matters.
- Engineer choice: Put the product contract up top in the README, including the pseudo-mystical node line and the safe human-AI interaction guardrail.
- Why: The repo should explain the product clearly before it explains the implementation.

## D-006: Small doc stack with agent shim

- Human input: Prefer normal project docs over a giant agent-only policy file.
- Engineer choice: Keep the real contract in README, Charter, Architecture, Runbook, and this Decisions log, with `AGENTS.md` reduced to a tiny bootstrap pointer.
- Why: Normal docs are easier to live with, while the small shim preserves repo-local auto-read behaviour for future agents.

## D-007: Canonical pipeline diagram

- Human input: Have a diagrams folder so the pipeline does not only exist in the README.
- Engineer choice: Add `docs/diagrams/PIPELINE.md` as the canonical diagram surface and point README and Architecture to it.
- Why: The pipeline is part of the product shape and should have a real home outside the top-level overview doc.

## D-008: Binary gate lineage

- Human input: Make it explicit that the binary eval gate is by design and continues the Polinko Beta 2.0 line of thinking.
- Engineer choice: Keep `probaboracle` eval verdicts strict `pass` or `fail` and document that lineage in the README, Charter, Architecture, and config-backed eval contract.
- Why: The binary gate is part of the safety and alignment theory, not a missing feature or an arbitrary simplification.

## D-009: Config-backed eval contract

- Human input: The eval rules should not live as a prose slab; all of the parameters should be in config.
- Engineer choice: Move workflow, CLI, storage, and eval parameters into the `src/config/` module and stop using a separate markdown ruleset as a contract surface.
- Why: Tunable behavior should be inspectable and versionable as code, not hidden across hardcoded values and markdown prose.

## D-010: Local manual eval prompt

- Human input: Manual eval should stay human-friendly, but the browser workbench was cursed.
- Engineer choice: Keep evaluation in the CLI and add a post-response `pass` / `fail` prompt with no skip path.
- Why: The repo still needs immediate human judgement, but not a separate UI surface.
