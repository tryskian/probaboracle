<!-- @format -->

# Probaboracle Research Doc Templates

Tracked template set for shaping Probaboracle research docs before they land in
`docs/research/`.

Use these when a new beta boundary, clean-baseline note, pulse report, case, or
staged hypothesis needs the same public structure as the existing research
lane.

## Kernel

| Rule | Choice |
| --- | --- |
| Target folder | `docs/research/` |
| Entry file | `README.md` |
| Legend file | `000_LEGEND.md` |
| Filename shape | `NNN_CODE.md` or `NNN_CODE-QUALIFIER.md` |
| Boundary code rule | `B` for beta boundaries, `CB` for clean-baseline boundaries, `PB` for staged pre-beta boundaries |
| Dates | inside docs, not filenames |
| Default style | concise, table-first, and pulse-explicit |
| First content surface | table or diagram |

## Template Files

| Template | Use For |
| --- | --- |
| [legend.md](legend.md) | `000_LEGEND.md` |
| [boundary.md](boundary.md) | beta or method boundary docs |
| [lane.md](lane.md) | current prompt or pulse evidence lane docs |
| [case.md](case.md) | representative pulse, run, or case docs |
| [validation.md](validation.md) | fixed-prompt pulse, gate, or closeout proof docs |
| [hypothesis.md](hypothesis.md) | staged hypothesis docs |
| [backlog.md](backlog.md) | source pool and candidate pressure docs |

## Code Ranges

| Range | Role |
| ---: | --- |
| `000` | index and legend |
| `010-099` | closed, active, or reset beta boundaries |
| `100-199` | fixed-prompt pulse and evidence lane docs |
| `200-299` | bounded output, prompt, and drift case docs |
| `300-399` | pulse reports, prompt-surface audits, and validation docs |
| `400-499` | staged pre-beta boundaries, hypotheses, and backlog |

## Boundary Filename Shape

Use boundary files like this in Probaboracle:

- `NNN_B-NAME.md`
  - active or closed beta boundary
- `NNN_CB-NAME.md`
  - clean-baseline or reset boundary
- `NNN_PB-NAME.md`
  - staged pre-beta boundary

Examples:

- `010_B-PRODUCT_FIT.md`
- `051_B-RETAIN_OR_EVICT.md`
- `060_B-FAIL_PRESSURE_PULSE.md`
- `070_CB-CLEAN_BASELINE_RESET.md`
- `410_PB-FAIL_PRESSURE_PULSE.md`

## Shared Metadata

Every category template starts with this table shape.

| Field | Value |
| --- | --- |
| Code | short doc code |
| Category | `legend`, `boundary`, `lane`, `case`, `validation`, `hypothesis`, or `backlog` |
| Status | current state |
| Last evidence | `YYYY-MM-DD` |
| Owns | one sentence naming the doc's job |

## Probaboracle Defaults

| Surface | Default |
| --- | --- |
| Judged unit | one fixed-prompt eval pulse or run |
| Verdict shape | pass or fail for the whole pulse |
| Prompt shape | configuration-neutral and explicitly bounded |
| Evidence shape | pulse report, prompt-surface audit, or bounded output case |
| Baseline shape | clean snapshot before the next beta claim |

## Style Rules

- Lead with a table or diagram.
- Use prose only for interpretation.
- Keep inventories in tables.
- Use one or two bullets per prose section.
- Prefer one compact Mermaid diagram when a contrast or eval flow is the point.
- Name the pulse/run before interpreting the result.
