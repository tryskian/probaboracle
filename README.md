# Probaboracle

[![Research Stage](https://img.shields.io/badge/research_stage-polinko%20research%20model%20refactor-4C956C)](./docs/research/README.md)
[![Polinko Model](https://img.shields.io/badge/polinko_model-staged_next_beta-4C956C)](https://github.com/tryskian/polinko)
![Polinko Toy Factory](https://img.shields.io/badge/polinko_toy_factory-active-4C956C)
![Model Refactor](https://img.shields.io/badge/model_refactor-active-F28E2B)

## probably a mini oracle. definitely a mini chatbot

> [!NOTE]
> **Current status:** The Polinko research model is being staged for the next
> beta.
>
> This is an active refactor window for the model contract, evidence snapshots,
> docs, and supporting tools. Current builds are kept stable while the repo
> surfaces are simplified, tested, and aligned for the next release.

Probaboracle is a small, local, agent-backed CLI mini chatbot using the **[Polinko research model](https://github.com/tryskian/polinko)**.

It only accepts four question types:

- `what`
- `when`
- `why`
- `where`

That narrow surface is the point. Probaboracle is not trying to be a general chat tool. It is a small instrument for studying whether a model can stay coherent, vague, answer-shaped, and product-specific inside tight interaction guardrails.

Current research stage:

- `Polinko research model refactor`
- source state: under audit against the Polinko-family governance contract
- live eval gate: paused
- next step: reconstruct the instruction/config blueprint before any runtime
  or beta claim

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
evidence means, not just when wording or procedure gets tidier. The previous
clean-baseline reset frame is now under quarantine until the family governance
contract is reconstructed and checked against the established Polinko method.

The next baseline is not a live eval run. It is a method-contract repair pass:
separate structural config from runtime instruction language, identify
patched-in instruction drift, and require human approval before any instruction
change becomes a research or beta claim.

## What This Repo Demonstrates

- constrained one-node generation through a fixed prompt surface
- structural config plus positive agent-owned routing/output targets
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

## Data Viz Direction

Probsie charts follow the eval shape first. Shared chart families are useful
only when the data shape naturally matches.

The initial visualisation set is:

- pulse charts:
  - stacked horizontal bars for `anchor`, `counted_seam`, and `excluded_noise`
  - grouped or faceted pulse comparison for snapshot versus clean baseline
- detail table:
  - row id, prompt, output, pulse label, reason, and seam note below the chart
- row and lens charts:
  - row-level `pass / fail / pending` stack by prompt type
  - prompt-by-lens table heatmap
  - fail-family horizontal bars
  - correction slope only when true before/after pairs exist

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
  - current reset boundary and first local pulse plan
- [docs/diagrams/EVAL_CHART.md](./docs/diagrams/EVAL_CHART.md)
  - current static eval chart contract
- [docs/diagrams/PIPELINE.md](./docs/diagrams/PIPELINE.md)
  - public generation and eval-shape diagrams
- [docs/runtime/templates/README.md](./docs/runtime/templates/README.md)
  - public templates for future research docs and pulse reports
- [docs/governance/DECISIONS.md](./docs/governance/DECISIONS.md)
  - durable runtime and eval decisions

## Licence

Apache-2.0. See [licence](LICENSE).

---

*Probaboracle is not a resource for yes, no, or maybe.*
