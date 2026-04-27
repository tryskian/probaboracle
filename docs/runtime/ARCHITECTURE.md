# Architecture

## Shape

Probaboracle is a small local TypeScript CLI.

It has three active parts:

- a prompt-type entrypoint
- a classifier-style response pipeline
- a local SQLite eval loop

There is no hosted model workflow, backend API, UI shell, auth layer, or deployment scaffold in the current architecture.

## Entrypoint

The CLI lives in [src/index.ts](../../src/index.ts).

It does two jobs:

- routes normal prompt invocations into the workflow
- exposes eval commands for init, sample, list, and judge

Prompt types are fixed:

- `what`
- `when`
- `how`
- `why`
- `where`

If no valid prompt type is supplied, the CLI falls back to `what`.

## Response Pipeline

The response pipeline lives in [src/workflow.ts](../../src/workflow.ts).

The canonical diagram lives in [docs/diagrams/PIPELINE.md](../diagrams/PIPELINE.md).

The flow is:

1. accept a selected prompt type
2. choose a body builder for that type
3. build a fragment
4. combine that fragment with an anchor
5. capitalise and punctuate the final line

The pipeline is compositional, not a bank of prewritten full sentences.

Current moving parts:

- anchor classifier:
  - `Certainly`, `Technically`, `Arguably`, `Probably`, `Definitely`, `Most likely`
- article modifier logic:
  - empty, `not quite`, `hardly`
- `what` path:
  - nominal head selection plus article logic
- `when`, `how`, `why`, `where` paths:
  - fragment selection for timing, method, reason, and place

Only the `what` path passes through article and nominal logic. The other prompt types resolve directly to their own fragment sets.

## Eval Loop

The eval database lives in [src/eval-db.ts](../../src/eval-db.ts).

The runtime and eval parameters live in [src/config/index.ts](../../src/config/index.ts).

Local storage path:

- `.probaboracle/evals.sqlite`

The eval loop records:

- sample runs
- generated outputs
- human verdicts

Current tables:

- `eval_runs`
- `eval_outputs`
- `eval_judgments`

Verdicts are binary only:

- `pass`
- `fail`

There is no `mixed` state in the schema or judging contract. That gate is deliberate and continues the strict binary eval semantics operationalised in Polinko Beta 2.0.

## Contract Surfaces

- Product framing lives in [README.md](../../README.md).
- Durable rules live in [docs/governance/CHARTER.md](../governance/CHARTER.md).
- Durable change history lives in [docs/governance/DECISIONS.md](../governance/DECISIONS.md).
- Near-term continuation lives in [docs/governance/SESSION_HANDOFF.md](../governance/SESSION_HANDOFF.md).
- Canonical diagrams live in `docs/diagrams/`.
- Operating procedure lives in [docs/runtime/RUNBOOK.md](./RUNBOOK.md).
- Canonical runtime and eval parameters live in [src/config/index.ts](../../src/config/index.ts).

## Change Bias

- Prefer small deltas over architecture churn.
- Preserve the classifier pipeline unless a deliberate rewrite is requested.
- Keep naming simple and consistent.
- Avoid speculative scaffolding.
