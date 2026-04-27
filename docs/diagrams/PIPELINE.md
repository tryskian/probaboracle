# Pipeline Diagram

This is the canonical diagram for the Probaboracle response pipeline.

```mermaid
flowchart LR
    A["Prompt type"] --> B["Select body builder"]
    B --> C{"Type"}
    C --> D["what -> nominal(head)"]
    C --> E["when -> timing fragment"]
    C --> F["how -> method fragment"]
    C --> G["why -> reason fragment"]
    C --> H["where -> place fragment"]
    D --> I["Response parts"]
    E --> I
    F --> I
    G --> I
    H --> I
    J["Anchor classifier"] --> I
    K["Article modifiers"] --> D
    I --> L["Render line"]
    L --> M["Capitalise + full stop"]
    M --> N["Output text"]
```

## Shape

- The selected prompt type routes into one of five body builders.
- `what` is the only path that passes through article and nominal logic.
- The other prompt types resolve directly to timing, method, reason, or place fragments.
- An anchor classifier and the selected fragment merge into response parts.
- The renderer capitalises the line, adds a full stop, and emits the final text.
