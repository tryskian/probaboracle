<!-- @format -->

# Validation Template

Use this for tracked or staged fixed-prompt pulse, prompt-surface audit, or gate
proof docs where the job is to show whether a bounded evidence surface actually
held.

## Metadata

| Field | Value |
| --- | --- |
| Code | `NNN_VALIDATION` |
| Category | `validation` |
| Status | `staged`, `running`, `closed`, `failed`, or `snapshot` |
| Last evidence | `YYYY-MM-DD` |
| Owns | one sentence naming the pulse, audit, gate, or proof surface this doc covers |

## Headline Shape

- `Validation: Name`
- or `Pulse Report: Name`
- or `Prompt Surface Audit: Name`
- or `Gate Proof: Name`
- or `Closeout Proof: Name`

## Section Order

1. metadata table
2. `Question`
3. `Run`
4. `Decision`
5. `Residual Risk`
6. `Next Move`

## Required Validation Moves

- state the exact fixed-prompt pulse, prompt audit, gate, or closeout surface being proved
- state the bounded run, pulse id, or command surface explicitly
- keep the proof in a compact table
- state the decision plainly:
  - `pass`
  - `hold`
  - `rerun`
  - `fail`
- state what the validation still does not prove

## Default Run Table

| Check | Result | Read |
| --- | ---: | --- |
| prompt surface | `pass` | fixed prompt is explicit and bounded |
| pulse report | `pass` | whole-pulse verdict is recorded |
| docs gate | `pass` | claim matches current research wording |
| repo validation | `pass` | relevant command or check held |
| residual failures | `0` | compact note |

## Default Decision Table

| Decision | Reason |
| --- | --- |
| `pass`, `hold`, `rerun`, or `fail` | one sentence |

## Validation Questions To Answer

- what exact surface is being proved?
- what bounded run, pulse, or command sequence produced the evidence?
- did the gate or closeout actually hold?
- what still remains outside the proof?
- what is the immediate next move?

## Style Rules

- lead with the metadata table
- keep the run proof in tables
- keep the decision short and operational
- keep residual risk to one or two bullets
- do not let the doc drift into a broader lane recap
