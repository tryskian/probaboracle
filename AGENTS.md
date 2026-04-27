# AGENTS.md

This file applies to the whole repository.

## Repo Shape

- Keep this project small.
- Current baseline is CLI-first.
- Current generator is a local classifier pipeline, not a hosted model workflow.
- Do not add a UI shell, ChatKit, backend API, auth, or deployment scaffolding unless explicitly requested.

## Product Contract

- Probaboracle is a tiny useless oracle chatbot.
- User-facing output stays in UK English.
- Supported question types are:
  - `what`
  - `when`
  - `how`
  - `why`
  - `where`
- Responses should stay short, coherent, deadpan, confident, mysterious, and unhelpful.
- Avoid poetic drift, helper-bot drift, and over-explaining.

## Eval Contract

- Keep local eval storage in `.probaboracle/evals.sqlite`.
- Eval verdicts are binary only:
  - `pass`
  - `fail`
- Do not add a `mixed` state.
- Use the tracked eval judging contract in `EVAL_RULESET.md` when tuning outputs.

## Change Rules

- Prefer small deltas over architecture churn.
- Preserve the classifier pipeline unless a deliberate rewrite is requested.
- Keep naming simple and consistent.
- Avoid speculative scaffolding.

## Validation

Run the smallest relevant checks after changes:

- `npm run check`
- `npm run dev -- eval:init`
- `npm run dev -- eval:sample what 10`
- `npm run dev -- eval:list 10`
- `npm run dev -- eval:judge <id> pass "note"`
