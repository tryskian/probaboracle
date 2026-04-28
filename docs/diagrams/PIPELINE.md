# Pipeline

This is the canonical home for the Probaboracle pipeline diagram.

This is the active reasoning shape for the current runtime.

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

The prompt type does not map to one static phrase. It sets the reasoning lane,
and that lane composes a final line through certainty, indecision, connective,
and soft-conclusion choices.

All prompt types draw from one shared style-signal resource. Those signals are
cues for synthesis and arrangement, not a fixed word bank.
