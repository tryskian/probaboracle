# Probaboracle

[![Research Stage](https://img.shields.io/badge/research_stage-pre--Beta%206.0%20fail--pressure%20pulse-E15759)](./docs/research/README.md) ![Polinko toy factory](https://img.shields.io/badge/polinko_toy_factory-active-4C956C)
![Maintenance](https://img.shields.io/badge/maintenance-in%20progress-F28E2B)

> **Maintenance in progress.** Documentation and research surfaces are being
> standardised before this repo is shared as a stable reference.

## probably a mini oracle. definitely a mini chatbot

Probaboracle is a small, local, agent-backed CLI mini chatbot using the **[Polinko research model](https://github.com/tryskian/polinko)**.

It only accepts four question lanes:

- `what`
- `when`
- `why`
- `where`

That narrow surface is the point. Probaboracle is not trying to be a general chat tool. It is a small instrument for studying whether a model can stay coherent, vague, answer-shaped, and product-specific inside tight interaction guardrails.

Current staged research lane:

- `pre-Beta 6.0`
- `fail-pressure pulse`

Most recently closed beta:

- `Research Beta 5.1`
- `retain + evict`

In this repo, a new beta gets pinned when the method change alters what the
evidence means, not just when wording or procedure gets tidier. Pre-beta
staging notes can hold the next method boundary before the first real evidence
run starts.

`Beta 6.0` does not begin until the first real fail-pressure pulse run starts.

## What This Repo Demonstrates

- constrained one-node generation through a fixed prompt surface
- coherence-first evaluation instead of one overloaded product verdict
- recurring failure as evidence before it earns runtime correction
- explicit post-fail gate stack:
  - `PASS / FAIL`
  - if `FAIL`, then `RETAIN / EVICT`
  - rerun
  - `PASS / FAIL`

## Run It

```sh
make install
probaboracle
```

The app opens a compact terminal loop. Choose a question lane with the arrow keys, press `enter`, or hit `esc` to exit.

The operator commands, eval workflow, and setup checks live in the [runtime runbook](./docs/runtime/RUNBOOK.md).

Core operator commands:

```sh
make start
make end-preflight
make end-git-check
make caffeinate-status
make decaffeinate
make check
```

## Read Next

- [docs/research/README.md](./docs/research/README.md)
  - beta map and research reading path
- [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
  - durable runtime and eval decisions

## License

Apache-2.0. See [LICENSE](LICENSE).

---

*Probaboracle is not a resource for yes, no, or maybe.*
