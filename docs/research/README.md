# Research

Probaboracle keeps the tracked research lane small on purpose.

Each beta or staged note is a distinct eval approach. This folder preserves the
method shifts that changed what the evidence means.

Raw run notes, operator poking, and private scratch material stay in the local `docs/peanut/` lane.

## Current Stage

Current research stage:

- `clean baseline reset`
- source state: proper-config candidate
- next eval gate: `eval-pulse`

Most recent diagnostic snapshot:

- `Research Beta 6.0`
- `fail-pressure pulse`
- first pulse verdict: `FAIL`
- snapshot held for comparison only

Most recently closed beta:

- `Research Beta 5.1`
- `retain + evict`

Clean-baseline question:

Can Probaboracle produce a comparable fixed-prompt pulse from structural config
alone, without carrying forward prompt phrase banks or slot scaffolds?

Current finding:

- `Research Beta 5.1` proved the row-level retain-evict architecture under the
  cleaned instruction surface
- `when` earned `evict`, and the first narrow post-evict correction held:
  - deciding rerun: `317 pass / 389 fail / 0 pending`
  - confirmation rerun: `97 pass / 3 fail / 0 pending`
  - old dominant failures collapsed to:
    - `semicolon pile and unresolved timing drift`: `0`
    - `stacked timing fragments`: `1`
    - `awkward temporal phrasing`: `2`
- `why` also earned `evict`, but the first post-evict fix overcollapsed:
  - deciding rerun: `77 pass / 368 fail / 0 pending`
  - dominant fail mix:
    - `duplicate why fallback`: `292`
    - `stacked hinge accumulation`: `65`
    - `too fallback-bare for product pass`: `11`
  - first post-evict rerun: `81 pass / 0 fail / 0 pending`
  - new pass rut:
    - `good useless reason`: `66`
    - `strong why lane`: `15`
- the next method question is no longer whether `retain / evict` belongs in
  the active line
- `Research Beta 6.0` produced the current diagnostic snapshot:
  - pulse duration: `15` minutes
  - each pulse uses one fixed prompt
  - the method used `eval-pulse`
  - default pacing: about one sample per minute
  - row labels are pulse evidence only
  - one `PASS / FAIL` verdict for the pulse
  - first valid pulse failed:
    - ids: `4850-4863`
    - `1` anchor
    - `13` counted seams
    - `0` excluded
- live reruns are paused until rate limits and prepaid credits are healthy
  again
- the current Beta `6.0` line should be treated as diagnostic rather than clean
  comparison evidence until a proper-config baseline is defined

Current reset method:

- `Research Beta 5.1` is closed as the row-level `retain / evict` baseline
- `Research Beta 6.0` is the latest pulse-level diagnostic snapshot
- the clean-baseline candidate keeps the same pulse-level method
- one fixed-prompt pulse is judged at a time
- label rows as `anchor`, `counted_seam`, or `excluded_noise`
- first pulse verdict: `FAIL`
- next work is validating the clean baseline source reset before another live
  run
- keep row-level `5.1` as the comparison surface, not the active method

## Beta Map

| Beta | Question | What Changed |
| --- | --- | --- |
| `Research Beta 1.0` | Does it feel like good Probaboracle? | Product fit shaped the voice, but overloaded one verdict. |
| `Research Beta 2.0` | Is the sentence coherent? | Coherence became the primary experimental gate. |
| `Research Beta 3.0` | Is a coherent line in-lane? | Prompt relevance separated lane control from sentence quality. |
| `Research Beta 4.1` | Can coherent drift still be valuable? | Coherent absurdity became a small selective class. |
| `Research Beta 5.1` | When does a fail family stay active evidence versus earn eviction? | `retain / evict` stays active, with the instruction surface tightened to preserve shape-first lane control. |
| `Research Beta 6.0` | Can Probaboracle hold shape across a bounded fixed-prompt pulse? | The fixed-prompt pulse became the binary unit, but the first line is now a diagnostic snapshot. |

Current reset:

- [Clean Baseline Reset](./CLEAN_BASELINE_RESET.md)
- proper-config candidate
- same fixed-prompt pulse method before the next boundary decision

Pulse method reference:

- `Research Beta 6.0`
- [Fail-Pressure Pulse](./BETA_6_FAIL_PRESSURE_PULSE.md)
- staging note: [Pre-Beta 6.0](./PRE_BETA_6_FAIL_PRESSURE_PULSE.md)

Read in order:

1. [Research Beta 1.0: Product Fit Only](./BETA_1_PRODUCT_FIT.md)
2. [Research Beta 2.0: Coherence First](./BETA_2_COHERENCE_FIRST.md)
3. [Research Beta 3.0: Coherence + Prompt Relevance](./BETA_3_PROMPT_RELEVANCE.md)
4. [Research Beta 4.1: Coherence + Coherent Absurdity](./BETA_4_COHERENT_ABSURDITY.md)
5. [Research Beta 5.1: Retain + Evict](./BETA_5_RETAIN_OR_EVICT.md)
6. [Research Beta 6.0: Fail-Pressure Pulse](./BETA_6_FAIL_PRESSURE_PULSE.md)
7. [Clean Baseline Reset](./CLEAN_BASELINE_RESET.md)

## How To Read The Betas And Stages

These betas and staged notes are research architectures. They are not app
release versions, package versions, branch names, or one more sweep.

Each beta marks a real change in what the evaluation is asking:

- `Research Beta 1.0` shaped the product voice
- `Research Beta 2.0` established the core experimental gate
- `Research Beta 3.0` separated lane control from sentence coherence
- `Research Beta 4.1` preserves the selective value of coherent drift while holding coherence to a stricter sentence-resolution bar
- `Research Beta 5.1` separates failure evidence from later runtime correction while keeping the live instruction path shape-first
- `Research Beta 6.0` moves bounded non-OCR work from row-level product
  verdicts to pulse evidence plus one pulse-level verdict
- the clean baseline reset is not a new beta yet; it resets the source surface
  before the next pulse decides whether the beta boundary moves

Later betas do not erase earlier ones. They narrow what each verdict is allowed to mean.

## Cross-Beta Flow

```mermaid
flowchart LR
  B1["Research Beta 1.0<br/>product fit only"]
  B2["Research Beta 2.0<br/>coherence first"]
  B3["Research Beta 3.0<br/>coherence + prompt relevance"]
  B4["Research Beta 4.1<br/>coherence + coherent absurdity"]
  B5["Research Beta 5.1<br/>retain + evict"]
  B6["Research Beta 6.0<br/>bounded fail-pressure pulse"]
  C1["Clean baseline reset<br/>proper-config candidate"]

  S1["one verdict overloaded tone,<br/>sentence quality, and lane control"]
  S2["coherence pulled out as the<br/>primary experimental gate"]
  S3["lane control separated from<br/>sentence coherence"]
  S4["valuable coherent drift preserved<br/>as a selective class"]
  S5["failure evidence separated from<br/>later runtime correction"]
  S6["row evidence labels feed<br/>one pulse verdict"]
  S7["source surface reset before<br/>the next comparable pulse"]

  B1 --> S1 --> B2 --> S2 --> B3 --> S3 --> B4 --> S4 --> B5 --> S5 --> B6 --> S6 --> C1 --> S7
```

## Plans

Plans are useful, but they are not evidence. They do not become active method until the repo earns them.

Active reset lane:

- clean baseline reset:
  - keep `config.py` structural
  - keep prompt phrase banks and slot scaffolds out of the source surface
  - compare the Beta `6.0` snapshot against the next proper-config pulse
  - keep the comparison diagram explicit before deciding whether this becomes
    a new beta boundary or a reset inside Beta `6.0`

Planning lanes:
- provider portability:
  - keep OpenAI-native behaviour stable if the runtime surface later widens
  - leave room for an Azure-compatible path if it becomes necessary
- research visuals:
  - keep per-beta diagrams in tracked docs
  - only add a polished cross-beta Sankey if the era-to-era story needs it
- future betas:
  - promote a new beta only when the eval architecture changes materially
  - do not turn one more sweep into a fake beta

## Polinko Contrast

Probaboracle is part of the same line of work as Polinko, but it is a smaller instrument.

```mermaid
flowchart LR
  P["Polinko"]
  P1["broader research system"]
  P2["many runtime and eval surfaces"]
  P3["binary fail pressure across products"]

  Q["Probaboracle"]
  Q1["mini oracle instrument"]
  Q2["one-node constrained generation"]
  Q3["coherence-first layered sidecars"]

  S["shared line\\nhuman-led research\\nbinary eval discipline\\nrepo-native docs and diagrams"]

  P --> P1
  P --> P2
  P --> P3

  Q --> Q1
  Q --> Q2
  Q --> Q3

  P --- S
  Q --- S
```
