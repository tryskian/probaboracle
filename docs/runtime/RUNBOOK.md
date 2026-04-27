# Runbook

## When to Read This

- Use this when you need the repo's operating contract instead of guessing from memory.
- Use this before non-trivial code or docs changes.
- Use this when runtime behaviour, eval output, or local state looks wrong.

## Read Order

1. Read [README.md](../../README.md) for product framing.
2. Read [docs/governance/CHARTER.md](../governance/CHARTER.md) for durable rules.
3. Read [docs/governance/DECISIONS.md](../governance/DECISIONS.md) for shaping history.
4. Read [docs/runtime/ARCHITECTURE.md](./ARCHITECTURE.md) for system shape.
5. Use this runbook for procedure and command ownership.
6. Read [docs/governance/SESSION_HANDOFF.md](../governance/SESSION_HANDOFF.md) for the current snapshot and next slice.
7. If the change touches runtime or eval parameters, inspect [src/config/index.ts](../../src/config/index.ts).

## Branch and PR Flow

1. Start from the canonical local repo:
   - `/Users/tryskian/Github/probaboracle`
2. Work from a task branch, not `main`:
   - `git switch -c codex/bigbrain/<task-name>`
3. Keep one logical change set per branch.
4. Push the branch and merge through a PR before returning to `main`.
5. After merge, sync local `main`:
   - `git switch main`
   - `git pull --ff-only`

## Command Ownership

1. The human sets objective, scope, and acceptance.
2. The engineer executes commands, validation, and Git flow end-to-end.
3. Do the work directly instead of bouncing terminal steps back to the user.

## Repo Shape

- Keep the project small.
- Current shape is CLI-first.
- Current generator is a local classifier pipeline, not a hosted model workflow.
- Do not add a UI shell, backend API, auth, deployment scaffolding, or ChatKit unless explicitly requested.

## Product Contract

- Probaboracle is a tiny unhelpful oracle chatbot that routes pseudo-mystical reasoning through a hollow, answer-shaped node.
- User-facing output stays in UK English.
- Prompt types are limited to:
  - `what`
  - `when`
  - `how`
  - `why`
  - `where`
- Responses stay short, coherent, deadpan, confident, vaguely mystical, and unhelpful.
- Avoid poetic drift, helper-bot drift, and over-explaining.
- At no point should the product imply guidance, help, reassurance, or understanding.
- The narrow prompt frame exists as a guardrail for safe human-AI interaction.

## Eval Contract

- Keep local eval storage in `.probaboracle/evals.sqlite`.
- Eval verdicts are binary only:
  - `pass`
  - `fail`
- Do not add a `mixed` state.
- Use `src/config/index.ts` as the eval source of truth when tuning outputs.

## Change Rules

- Prefer small deltas over architecture churn.
- Preserve the classifier pipeline unless a deliberate rewrite is requested.
- Keep naming simple and consistent.
- Avoid speculative scaffolding.

## Command Surface

- Main prompt path:
  - `npm run dev -- what`
- Eval setup:
  - `npm run dev -- eval:init`
- Eval sampling:
  - `npm run dev -- eval:sample what 10`
- Eval listing:
  - `npm run dev -- eval:list what 20`
- Eval judging:
  - `npm run dev -- eval:judge 12 pass "clean and deadpan"`

## Validation

Run the smallest relevant checks after changes:

- `npm run check`
- `npm run dev -- eval:init`
- `npm run dev -- eval:sample what 10`
- `npm run dev -- eval:list what 20`
- `npm run dev -- eval:judge <id> pass "note"`
