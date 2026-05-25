<!-- @format -->

# Lane Template

Use this for current prompt or pulse evidence lanes where the method boundary is
already known and the doc's job is to show the active surface cleanly.

## Metadata

| Field | Value |
| --- | --- |
| Code | `NNN_LANE` |
| Category | `lane` |
| Status | `active`, `paused`, `closed`, or `snapshot` |
| Last evidence | `YYYY-MM-DD` |
| Owns | one sentence naming the active prompt or pulse lane this doc tracks |

## Headline Shape

- `Lane: Name`
- or `Pulse Lane: Name`
- or `Prompt Surface: Name`

## Section Order

1. metadata table
2. `Question`
3. `Current Shape`
4. `Evidence Table`
5. `Diagram`
6. `Read`
7. `Why It Matters`
8. `Next Move`

## Required Lane Moves

- name the exact prompt or pulse lane being tracked
- state the judged object explicitly: one fixed-prompt eval pulse/run
- state whether the lane is active, paused, closed, or a snapshot
- keep the current evidence in a table
- state the next move without turning the doc into a backlog dump

## Default Evidence Table

| Pulse | Prompt surface | Result | Notes |
| --- | --- | --- | --- |
| `pulse-id` | fixed prompt or prompt surface | `pass` or `fail` | one compact note |

## Default Diagram Shape

```mermaid
flowchart LR
  A["Bounded prompt surface"]
  B["Fixed-prompt pulse"]
  C["Evidence table"]
  D["Current read"]
  E["Next move"]

  A --> B --> C --> D --> E
```

## Lane Questions To Answer

- what exact lane is open?
- what prompt surface and pulse currently define it?
- what does the lane read show right now?
- what remains unresolved?
- what is the immediate next move?

## Style Rules

- lead with the metadata table
- keep the evidence in tables, not long inventories
- use prose only for interpretation
- prefer one compact diagram over multiple mini-diagrams
- keep `Next Move` concrete and near-term
