# Probaboracle

Probaboracle is a tiny oracle chatbot named for "probably" and "oracle", built as a satirical take on confident LLM hallucination.
The current prototype is local-first, with future OpenAI API and Agents SDK integration in mind.

Current baseline:

- Node-first
- TypeScript
- local classifier pipeline
- local SQLite eval database
- no app shell yet
- no ChatKit yet
- UK English for user-facing copy
- question-type selection only: `what | when | how | why | where`

## Run

Install the dependencies, then ask it a question type.

```bash
npm install
npm run dev -- what
```

## Eval DB

```bash
npm run dev -- eval:init
npm run dev -- eval:sample what 10
npm run dev -- eval:list what 20
npm run dev -- eval:judge 12 pass "clean and deadpan"
```

This creates a local SQLite database at:

`/Users/tryskian/Github/probaboracle/.probaboracle/evals.sqlite`

Current schema:

- `eval_runs`
- `eval_outputs`
- `eval_judgments`

Judgements are binary only:

- `pass`
- `fail`

The tracked judging contract lives in [EVAL_RULESET.md](./EVAL_RULESET.md).

## Pipeline

```mermaid
flowchart LR
    A["Question type"] --> B["Select body builder"]
    B --> C{"Type"}
    C --> D["what -> nominal(head)"]
    C --> E["when -> timing fragment"]
    C --> F["how -> method fragment"]
    C --> G["why -> reason fragment"]
    C --> H["where -> place fragment"]
    D --> I["Response parts"]
    E --> I
    F --> I
    G --> I
    H --> I
    J["Anchor classifier"] --> I
    K["Article modifiers"] --> D
    I --> L["Render line"]
    L --> M["Capitalise + full stop"]
    M --> N["Output text"]
```

Current shape:

- `anchors` supply the opening verdict tone.
- `what` is the only branch that uses article/modifier logic.
- the other question types map directly to their own classifier fragments.
- the final renderer joins the selected anchor and body into one short line.
