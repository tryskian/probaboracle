# Probaboracle

Probaboracle is an unhelpful mini chatbot that's "probably" an "oracle", which
is more or less how it responds.

It is a local CLI mini app first: lightweight in surface area, but still a real
runtime. The prompt surface is fixed to `what`, `when`, `why`, and `where`.
There is no further prompt input. That limit is deliberate and exists as a
guardrail for safe human-AI interaction. It also keeps the interaction inside a
deliberate reasoning scope: the prompts bound what kind of answer-shape the
oracle is allowed to attempt, not because the engineering behind it is simple,
but because the interaction boundary is intentionally narrow.

At no point should it imply guidance, help, reassurance, or understanding.
Responses should stay vague, answer-shaped, and non-concrete.

Probaboracle is a mini project within Polinko, not separate from it. It carries
the same safety-minded way of working, the same binary eval discipline, and the
same systems thinking in a smaller local form.

This repo follows Polinko's systems discipline on a smaller scale:

- local runtime
- agent-backed generation
- minimal config
- binary eval gates only
- CLI-first operator surface

## Current Shape

- Python CLI runtime
- OpenAI Agents SDK
- local SQLite eval store
- tracked governance/runtime docs
- no UI shell, API, auth, or deployment scaffold in the initial slice

## Commands

1. Create the local environment and install the app:

```bash
make install
```

2. Run one oracle lane:

```bash
make ask PROMPT=what
```

Peanutbrain shortcuts:

```bash
make env
make what
make when
make why
make where
make eval-when-5
```

3. Initialise the eval database:

```bash
make eval-init
```

4. Generate local eval samples:

```bash
make sample PROMPT=when COUNT=5
```

5. List recent outputs:

```bash
make list PROMPT=when LIMIT=10
```

6. Judge outputs:

```bash
make judge ID=1 VERDICT=pass NOTE="deadpan and non-concrete"
make pass ID=1 NOTE="deadpan and non-concrete"
make fail ID=2 NOTE="too concrete"
```

## Docs

- [docs/governance/CHARTER.md](./docs/governance/CHARTER.md)
- [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
- [docs/runtime/ARCHITECTURE.md](./docs/runtime/ARCHITECTURE.md)
- [docs/runtime/RUNBOOK.md](./docs/runtime/RUNBOOK.md)
- [docs/governance/SESSION_HANDOFF.md](./docs/governance/SESSION_HANDOFF.md)
- [docs/diagrams/PIPELINE.md](./docs/diagrams/PIPELINE.md)

## Pipeline Diagram

The canonical Mermaid pipeline diagram lives in
[docs/diagrams/PIPELINE.md](./docs/diagrams/PIPELINE.md). The current runtime
reasons through certainty words, indecision words, connective articles or
hinges, and soft conclusions before resolving to one final line. All prompt
types draw from one shared style-signal resource, and those signals are cues
for synthesis rather than a fixed word bank.
