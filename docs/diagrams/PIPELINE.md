# Pipeline

This is the canonical home for the public Probaboracle pipeline and eval-shape diagrams.

This is the shortest public explanation of how Probaboracle generates a line and how that line is judged.

## Canonical Diagram

```mermaid
flowchart TD
  A["Prompt type"]
  B["Reasoning lane"]
  C["Shared style signals"]
  D["Certainty signal"]
  E["Indecision signal"]
  F["Connective / hinge"]
  G["Soft conclusion"]
  H["Compose response logic"]
  I["Final line"]

  A --> B
  B --> D
  B --> E
  B --> F
  B --> G

  C --> D
  C --> E
  C --> F
  C --> G

  D --> H
  E --> H
  F --> H
  G --> H

  H --> I
```

## Reading Note

The prompt type does not map to one static phrase. It sets the reasoning lane, and that lane composes a final line through certainty, indecision, connective, and soft-conclusion choices.

All prompt types draw from one shared style-signal resource. Those signals are cues for synthesis and arrangement, not a fixed word bank.

## Eval Shape Diagram

```mermaid
flowchart TD
  I["Final line"]
  K["Coherence"]
  L["Prompt relevance"]
  M["Coherent absurdity"]
  J["Product fit"]

  I --> K
  K --> L
  K --> M
  L --> J
  M --> J
```

## Active Beta 6.0 Pulse Gate

```mermaid
flowchart LR
  A["Fixed prompt"] --> B["Fixed-prompt pulse"]
  B --> C["Row evidence labels"]
  C --> D["anchor"]
  C --> E["counted_seam"]
  C --> F["excluded_noise"]
  D --> G{"Pulse PASS / FAIL"}
  E --> G
  F --> G
  G -->|"PASS"| H["Keep confidence in prompt shape"]
  G -->|"FAIL"| I["Plan the smallest shape correction"]
  I --> J["Rerun one fixed-prompt pulse"]
```

## Clean-Baseline Comparison Plan

```mermaid
flowchart LR
  A["Beta 6.0 snapshot"]
  B["failed why pulse<br/>ids 4850-4863"]
  C["grammar-led correction<br/>not clean-baseline proof"]
  D["config-history contamination risk"]

  E["Clean baseline candidate"]
  F["proper cleaned config"]
  G["same fixed-prompt pulse method"]
  H["compare verdicts and seam families"]
  I["decide reset inside Beta 6.0<br/>or new beta boundary"]

  A --> B --> C --> D
  E --> F --> G --> H --> I
  D -. "reference line" .-> H
```

## Closed Row-Level Gate Stack

```mermaid
flowchart LR
  A["Generated line"] --> B{"PASS / FAIL"}
  B -->|"PASS"| C["Keep confidence in active lane"]
  B -->|"FAIL"| D["Failure evidence"]
  D --> E{"RETAIN / EVICT"}
  E -->|"RETAIN"| F["Keep family in active lane"]
  F --> G["Accumulate more judged signal"]
  G --> A
  E -->|"EVICT"| H["Upstream runtime or boundary correction"]
  H --> I["Rerun corrected lane"]
  I --> A
```

## Eval Shape Reading Note

The generation pipeline stays the same. This public diagram only shows the high-level relationship between the eval lenses that sit downstream of the generated line.

Coherence is the primary experimental gate. Prompt relevance and coherent absurdity are downstream binary lenses that sit on top of the generated line rather than changing the one-node runtime path.

The public claim is simple:

- one-node constrained generation
- then layered binary evaluation

Product fit sits downstream of those two lenses:

- coherent and in-lane lines can satisfy product fit directly
- coherent but out-of-lane lines can still satisfy product fit when they land as strong coherent absurdity

The closed row-level gate stack stays explicit for the `Beta 5.1` comparison
surface:

- `PASS / FAIL`
- if `FAIL`, then `RETAIN / EVICT`
- rerun
- `PASS / FAIL`

The active `Beta 6.0` gate is different:

- one fixed prompt feeds one fixed-prompt pulse
- different prompts get separate pulses
- rows become evidence inside that pulse
- pulse evidence is `anchor`, `counted_seam`, or `excluded_noise`
- the pulse receives one `PASS / FAIL` verdict

The clean-baseline comparison is not another eval gate yet. It is a planning
boundary that keeps the current Beta `6.0` snapshot separate from the next
proper-config baseline candidate.
