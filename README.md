# Probaboracle

Probaboracle is an unhelpful mini chatbot that's "probably" an "oracle", which is more or less how it responds.

At no point should it imply guidance, help, reassurance, or understanding. The user selects one of five prompt types, `what`, `when`, `how`, `why`, or `where`, and Probaboracle responds inside that narrow frame. That limit is deliberate and exists as a guardrail for safe human-AI interaction.

This is a local TypeScript agent harness with a tiny SQLite eval loop. It runs real model generation through the OpenAI Agents SDK, but the surface stays local, CLI-first, and tightly framed. No public app shell. No helper-bot energy.

Current shape:

- CLI-first
- TypeScript
- local OpenAI Agents SDK runtime
- local SQLite eval database
- UK English for user-facing copy
- prompt-type selection only: `what | when | how | why | where`

## Run

Install the dependencies, set an API key, then ask it a question type.

```bash
npm install
cp .env.example .env
# set OPENAI_API_KEY
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

- The selected prompt type resolves into a compact prompt frame.
- The local CLI sends that frame through a single Probaboracle agent.
- The agent generates one short response inside the selected lane.
- `eval:prompt` records that output, then forces a human `pass` or `fail`.
