# Pipeline Diagram

This is the canonical diagram for the Probaboracle response pipeline.

```mermaid
flowchart TD
    A["User selects prompt type"]

    A --> W["what<br/>identity / category / designation"]
    A --> H["how<br/>manner / method / process"]
    A --> Y["why<br/>cause / reason / rationale"]
    A --> N["when<br/>timing / sequence / moment"]
    A --> R["where<br/>place / direction / position"]

    W --> B
    H --> B
    Y --> B
    N --> B
    R --> B

    B["Reason through semantic parts<br/>certainty words<br/>indecision words<br/>connective articles / hinges<br/>soft conclusions"]
    B --> C["Core oracle voice<br/>deadpan<br/>confident<br/>unhelpful<br/>flat<br/>UK English"]
    C --> D["Generate one short line"]
    D --> E["Output cleanup<br/>trim, de-quote, collapse whitespace"]

    E --> G{"eval:prompt?"}
    G -->|no| P["Print response"]
    G -->|yes| S["Store output in SQLite"]
    S --> J["Human judges pass or fail"]
    J --> K["Save verdict"]
```

## Shape

- The prompt type selects a reasoning lane, not a fragment bank.
- Each lane narrows the kind of thing the answer is about.
- The live part comes from a few semantic nodes working together, not from static full phrases and not from totally loose freeform drift.
- Manual eval stays local and binary: `pass` or `fail`.
