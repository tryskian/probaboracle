<!-- @format -->

# Research Legend

| Field | Value |
| --- | --- |
| Code | `000_LEGEND` |
| Category | `legend` |
| Status | `active` |
| Last evidence | `YYYY-MM-DD` |
| Owns | file map, code ranges, and shared status language for research docs. |

| Code | File | Meaning | Category | Status |
| --- | --- | --- | --- | --- |
| `CBR` | `030_CB-CLEAN_BASELINE_RESET.md` | clean-baseline reset boundary | `boundary` | `active` |
| `B60` | `060_B-FIXED_PROMPT_PULSE.md` | fixed-prompt pulse beta boundary | `boundary` | `snapshot` |
| `PULSE` | `120_PULSE_METHOD.md` | current pulse method lane | `lane` | `active` |
| `DRIFT` | `220_DRIFT_CASE.md` | bounded output drift case | `case` | `representative` |
| `AUDIT` | `310_PROMPT_SURFACE_AUDIT.md` | prompt-surface validation proof | `validation` | `staged` |

## Ordering

| Range | Role |
| ---: | --- |
| `000` | index and legend |
| `010-099` | closed, active, or reset beta boundaries |
| `100-199` | fixed-prompt pulse and evidence lane docs |
| `200-299` | bounded output, prompt, and drift case docs |
| `300-399` | pulse reports, prompt-surface audits, and validation docs |
| `400-499` | staged pre-beta boundaries, hypotheses, and backlog |

## Status Meanings

| Status | Meaning |
| --- | --- |
| `staged` | next boundary, prompt claim, or validation surface, not live evidence yet |
| `active` | current reset boundary, prompt surface, or pulse lane |
| `closed` | finished evidence surface held and moved into baseline |
| `paused` | lane intentionally stopped without promotion |
| `snapshot` | bounded read captured for reference |
| `representative` | case stands in for a wider seam cleanly |
| `running` | validation is in progress |
| `failed` | validation did not hold |
| `archived` | preserved but no longer active |

## Category Meanings

| Category | Owns |
| --- | --- |
| `legend` | file map, code ranges, and shared status language |
| `boundary` | beta or pre-beta method boundary |
| `lane` | active or closed prompt/pulse evidence lane and read |
| `case` | one representative output, pulse, run, or bounded slice |
| `validation` | fixed-prompt pulse, audit, gate, or closeout proof |
| `hypothesis` | staged claim before promotion or retirement |
| `backlog` | candidate pressure seams, source pools, and parked follow-up lanes |
