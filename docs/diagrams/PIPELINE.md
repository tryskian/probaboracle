# Pipeline

This is the canonical home for the Probaboracle pipeline diagram.

This is the active reasoning shape for the current runtime.

## Canonical Diagram

```mermaid
flowchart TD
  A["Prompt type"]

  B["Certainty words"]
  C["Indecision words"]
  D["Connective articles / hinges"]
  E["Soft conclusions"]

  F["Compose response logic"]
  G["Final line"]

  A --> B
  A --> C
  A --> D
  A --> E

  B --> F
  C --> F
  D --> F
  E --> F

  F --> G
```

## Reading Note

The prompt type does not map to one static phrase. It sets the reasoning lane,
and that lane composes a final line through certainty, indecision, connective,
and soft-conclusion choices.
