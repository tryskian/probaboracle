# Probaboracle

[![Research Stage](https://img.shields.io/badge/research_stage-clean%20baseline%20reset-4C956C)](./docs/research/README.md) ![Polinko toy factory](https://img.shields.io/badge/polinko_toy_factory-active-4C956C)

## probably a mini oracle. definitely a mini chatbot

Probaboracle is a small, local, agent-backed CLI mini chatbot using the **[Polinko research model](https://github.com/tryskian/polinko)**.

It only accepts four question types:

- `what`
- `when`
- `why`
- `where`

That narrow surface is the point. Probaboracle is not trying to be a general chat tool. It is a small instrument for studying whether a model can stay coherent, vague, answer-shaped, and product-specific inside tight interaction guardrails.

Current research stage:

- `clean baseline reset`
- source state: proper-config candidate
- next eval gate: `eval-pulse`

Most recent diagnostic snapshot:

- `Research Beta 6.0`
- method: `fail-pressure pulse`
- first fixed-prompt pulse: `FAIL`
- result: `1` anchor / `13` counted seams / `0` excluded
- status: diagnostic snapshot, not a clean baseline

Most recently closed beta:

- `Research Beta 5.1`
- `retain + evict`

In this repo, a new beta gets pinned when the method change alters what the
evidence means, not just when wording or procedure gets tidier. The current
reset keeps the `eval-pulse` method but stops treating the first Beta `6.0`
line as live baseline proof.

The next baseline starts from structural config only: fixed prompt types,
binary verdicts, runtime settings, and a minimal routing prompt in the agent
path. Earlier prompt scaffolds and config-level word lists are kept out of the
fresh line. The next comparable evidence should be a new fixed-prompt pulse,
run one prompt at a time after the rate-limit / prepaid-credit boundary is
healthy.

## What This Repo Demonstrates

- constrained one-node generation through a fixed prompt surface
- structural config without prompt phrase banks
- coherence-first evaluation instead of one overloaded product verdict
- beta-specific evidence gates:
  - row-level baselines use `PASS / FAIL`
  - closed `Beta 5.1` failures can then earn `RETAIN / EVICT`
  - the Beta `6.0` snapshot judged one fixed-prompt pulse at a time
  - pulse rows are only evidence inside that pulse:
    - `anchor`
    - `counted_seam`
    - `excluded_noise`
  - the pulse receives one `PASS / FAIL` verdict
  - the clean-baseline candidate keeps the same pulse method before the next
    beta-boundary decision

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
- [docs/research/070_CB-CLEAN_BASELINE_RESET.md](./docs/research/070_CB-CLEAN_BASELINE_RESET.md)
  - current reset boundary, docs cleanup, and first local pulse plan
- [docs/runtime/templates/README.md](./docs/runtime/templates/README.md)
  - public templates for future research docs and pulse reports
- [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
  - durable runtime and eval decisions

## Licence

Apache-2.0. See [licence](LICENSE).

---

*Probaboracle is not a resource for yes, no, or maybe.*
