# Probaboracle

Probaboracle is an unhelpful mini chatbot that's "probably" an "oracle", which is more or less how it responds.

At no point should it imply guidance, help, reassurance, or understanding. The user selects one of five prompt types, `what`, `when`, `how`, `why`, or `where`, and Probaboracle responds inside that narrow frame. That limit is deliberate and exists as a guardrail for safe human-AI interaction.

This is a local TypeScript oracle harness with a tiny SQLite eval loop. The important part is the simple node pipeline: a narrow prompt lane, a few semantic parts, and one short answer-shaped line. No public app shell. No helper-bot energy.

Current shape:

- CLI-first
- TypeScript
- local oracle/runtime harness
- local SQLite eval database
- UK English for user-facing copy
- prompt-type selection only: `what | when | how | why | where`

## Run

Install the dependencies, then ask it a question type.

```bash
npm install
npm run dev -- what
```

## Eval DB

```bash
npm run dev -- eval:init
npm run dev -- eval:prompt what
npm run dev -- eval:sample what 10
npm run dev -- eval:list what 20
npm run dev -- eval:judge 12 pass "deadpan and answer-shaped"
```

This creates a local SQLite database at:

`.probaboracle/evals.sqlite`

Current schema:

- `eval_runs`
- `eval_outputs`
- `eval_judgments`

Eval verdicts are binary only:

- `pass`
- `fail`

That binary gate is deliberate. It continues the strict eval semantics operationalised in Polinko Beta 2.0 and keeps the judgment surface explicit, auditable, and fail-closed.

Canonical eval parameters live in [src/config/index.ts](./src/config/index.ts) under `probaboracleConfig.eval`.

## Pipeline

The canonical pipeline diagram lives in [docs/diagrams/PIPELINE.md](./docs/diagrams/PIPELINE.md).

Pipeline shape:

- The selected prompt type chooses a narrow semantic lane.
- Inside that lane, the bot reasons through a few simple parts instead of a bank of canned full phrases.
- The line should feel generated, but still constrained by the node shape.
- `eval:prompt` records that output, then forces a human `pass` or `fail`.

## Archive Note

The agent/API experiment and its live eval database were archived locally on 2026-04-28 under:

`.probaboracle/archive/2026-04-28-agent-runtime-experiment/`
