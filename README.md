# Probaboracle

[![Research Stage](https://img.shields.io/badge/research_stage-Research%20Beta%206.0%20fail--pressure%20pulse-E15759)](./docs/research/README.md) ![Polinko toy factory](https://img.shields.io/badge/polinko_toy_factory-active-4C956C)

## probably a mini oracle. definitely a mini chatbot

Probaboracle is a small, local, agent-backed CLI mini chatbot using the **[Polinko research model](https://github.com/tryskian/polinko)**.

It only accepts four question types:

- `what`
- `when`
- `why`
- `where`

That narrow surface is the point. Probaboracle is not trying to be a general chat tool. It is a small instrument for studying whether a model can stay coherent, vague, answer-shaped, and product-specific inside tight interaction guardrails.

Current research stage:

- `Research Beta 6.0`
- `fail-pressure pulse`
- first fixed-prompt pulse: `FAIL`
- result: `1` anchor / `13` counted seams / `0` excluded

Most recently closed beta:

- `Research Beta 5.1`
- `retain + evict`

In this repo, a new beta gets pinned when the method change alters what the
evidence means, not just when wording or procedure gets tidier. `Beta 6.0`
still follows the normal beta-test discipline: run the active eval method,
collect comparable evidence, and assign one binary verdict. Its active method
is `eval-pulse`: one fixed-prompt pulse receives rows as evidence, and the
pulse earns one `PASS` or `FAIL` verdict.

## What This Repo Demonstrates

- constrained one-node generation through a fixed prompt surface
- coherence-first evaluation instead of one overloaded product verdict
- beta-specific evidence gates:
  - row-level baselines use `PASS / FAIL`
  - closed `Beta 5.1` failures can then earn `RETAIN / EVICT`
  - active `Beta 6.0` judges one fixed-prompt pulse at a time
  - active `Beta 6.0` rows are only pulse evidence inside that pulse:
    - `anchor`
    - `counted_seam`
    - `excluded_noise`
  - active `Beta 6.0` assigns one `PASS / FAIL` verdict to the pulse

## Run It

```sh
make install
probaboracle
```

The app opens a compact terminal loop. Choose a question type with the arrow keys, press `enter`, or hit `esc` to exit.

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
