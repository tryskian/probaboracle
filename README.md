# Probaboracle

![Research Beta](https://img.shields.io/badge/research_beta-4.1%20coherent%20absurdity-E15759)

## probably a mini oracle. definitely a mini chatbot

Probaboracle is a small, local, agent-backed CLI oracle in the
**[Polinko research line](https://github.com/tryskian/polinko)**.

It only accepts four question lanes:

- `what`
- `when`
- `why`
- `where`

That narrow surface is the point. Probaboracle is not trying to be a general
chat tool. It is a small instrument for studying whether a model can stay
coherent, vague, answer-shaped, and product-specific inside tight interaction
guardrails.

Current tracked research beta:

- `Research Beta 4.1`
- `coherence + coherent absurdity`

In this repo, major betas are research architectures, and minor versions tighten
the active method without changing the whole eval shape.

## What This Repo Demonstrates

- constrained one-node generation through a fixed prompt surface
- coherence-first evaluation instead of one overloaded product verdict
- coherent absurdity as a small selective downstream class

## Run It

```sh
probaboracle
```

The app opens a compact terminal loop. Choose a question lane with the arrow
keys, press `enter`, or hit `esc` to exit.

The operator commands, eval workflow, and setup checks live in the
[runtime runbook](./docs/runtime/RUNBOOK.md).

## Read Next

- [docs/research/README.md](./docs/research/README.md)
  - beta map and research reading path
- [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
  - durable runtime and eval decisions

---

*Probaboracle is not a resource for advice, guidance, help, reassurance, or understanding.*
