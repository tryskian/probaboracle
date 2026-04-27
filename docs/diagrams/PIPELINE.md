# Pipeline Diagram

This is the canonical diagram for the Probaboracle response pipeline.

```mermaid
flowchart LR
    A["Prompt type"] --> B["Prompt frame"]
    B --> C["Build local run input"]
    C --> D["Probaboracle agent"]
    D --> E["Model-backed generation"]
    E --> F["Output text"]
    F --> G{"Eval mode?"}
    G -->|no| H["Print and exit"]
    G -->|yes| I["Store run + output"]
    I --> J["Human verdict"]
    J --> K["Persist pass or fail"]
```

## Shape

- The selected prompt type resolves into a compact prompt frame.
- The local CLI turns that frame into one run input for the agent.
- The agent generates the response instead of stitching fragments together.
- Manual eval stays local and binary: `pass` or `fail`.
