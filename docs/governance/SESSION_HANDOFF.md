# Session Handoff

Last updated: 2026-05-25

## Start Here

1. Read:
  - `README.md`
  - `docs/governance/CHARTER.md`
  - `docs/governance/DECISIONS.md`
  - `docs/runtime/ARCHITECTURE.md`
  - `docs/runtime/RUNBOOK.md`
  - `docs/runtime/START_END_REFERENCE.md`
  - this file
2. Confirm repo and branch:
  - `/abs/path/to/probaboracle`
  - feature branch for tracked changes
3. If the checkout is on `main`, cut a task branch before editing.
4. State the active kernel before changing files.

## Current State

Probaboracle is a local, CLI-first, agent-backed mini oracle.

The default app path is bare `probaboracle`:

- responsive startup header
- fixed selector for `where`, `what`, `why`, and `when`
- `enter` selects
- soft `hit esc to exit` hint exits cleanly
- inline spinner-only wait state
- collapsed selected prompt
- response on its own line
- immediate `another question [y/n]?`

Operator commands remain separate:

- `make start`
- `make end-preflight`
- `make end-git-check`
- `make lint-docs`
- `make package-check`
- `make package-install-check`
- `make security-checks`
- `make caffeinate`
- `make caffeinate-status`
- `make decaffeinate-status`
- `make decaffeinate`
- `make rituals`
- `ask`
- `sample`
- `eval-list`
- `archive-pending`
- `judge`
- sidecar judgment commands

Current maintenance surface:

- public licence presentation follows Polinko style:
  - README heading and link text use `Licence`
  - package metadata declares `license = "Apache-2.0"`
  - the Apache `LICENSE` legal text is unchanged
- Ruff owns Python linting, formatting checks, and import sorting:
  - no separate isort dependency
  - no `[tool.isort]` block
  - no doctor-env isort import check
- clean baseline source reset:
  - `config.py` is structural only
  - prompt phrase banks, style-signal lists, pipeline-step lists, and slot
    scaffolds are out of config
  - the app banner says `PROBABORACLE`, not a research beta label

## Research Snapshot

Most recently closed beta:

- `Research Beta 5.1`
- `retain + evict`

Current reset state:

- `clean baseline reset`
- source state:
  - proper-config candidate
  - structural config only
  - minimal routing prompt in `agent.py`
- current kernel:
  - docs cleanup before local evidence collection
- next eval gate:
  - `eval-pulse`
  - one fixed prompt per pulse
  - one pulse-level `PASS / FAIL`
- first clean-baseline pulse plan:
  - fixed prompt `why`
  - fresh local eval DB boundary
  - compare against the Beta `6.0` `why` snapshot
- status:
  - first valid Beta `6.0` fixed-prompt pulse failed
  - that line is now a diagnostic snapshot
  - live eval work remains paused on the rate-limit / prepaid-credit boundary
  - invalid false starts were discarded

Historical eval checkpoint before the local fresh-start strip:

- product-judged through row `4723`
- pulse-labeled through row `4863`
- active product surface: `1543 pass / 1459 fail / 14 pulse-labeled pending`
- active coherence surface: `1670 pass / 923 fail / 389 pending`
- active relevance surface: `1663 pass / 113 fail / 1206 pending`
- active absurdity surface: `4 pass / 8 fail / 2970 pending`
- archived out of the active surface:
  - `501` stale product-pending rows
  - `364` pre-sidecar rows with no live coherence lane
- this checkout's local `.local/evals.sqlite` was removed for the fresh start
- historical counts above are tracked documentation context, not live DB state

The active coherence rule is stricter than the early runs:

- one resolved sentence
- one dominant reasoning lane
- short lines with `2+` commas fail
- stacked fragment chains fail even when they look tidy

Useful current reads:

- the deciding Beta `5.0` `when` retain rerun used rows `3392-4097`
- fresh deciding surface: `317 pass / 389 fail / 0 pending`
- `when` has now earned `evict`:
  - `272` `stacked timing fragments`
  - `85` `semicolon pile and unresolved timing drift`
  - `32` `awkward temporal phrasing`
- the post-evict confirmation rerun used rows `4098-4197`
- confirmation surface: `97 pass / 3 fail / 0 pending`
- the old fail family collapsed:
  - `semicolon pile and unresolved timing drift`: `0`
  - `stacked timing fragments`: `1`
  - `awkward temporal phrasing`: `2`
- the first long `why` retain rerun used rows `4198-4642`
- fresh `why` surface: `77 pass / 368 fail / 0 pending`
- `why` has now earned `evict`:
  - `292` `duplicate why fallback`
  - `65` `stacked hinge accumulation`
  - `11` `too fallback-bare for product pass`
- the `why` sidecar surface mostly held:
  - coherence: `380 pass / 65 fail`
  - relevance: `380 pass / 0 fail`
- that active `why` surface is now saturated enough to count as bad post-fix
  comparison data
- the first narrow `why` fix attempt then used rows `4643-4723`
- fresh `why` post-fix surface: `81 pass / 0 fail / 0 pending`
- the old fail family disappeared, but the pass surface overcollapsed:
  - `66` `good useless reason`
  - `15` `strong why lane`
- that first `why` fix was not promoted
- Beta `5.1` is now the most recently closed row-level baseline:
  - retain-evict stays closed there
  - hard-coded phrase scaffolds are removed
- Beta `6.0` produced the latest pulse-level diagnostic snapshot:
  - each pulse uses one fixed prompt
  - pulse duration: `15` minutes
  - default pacing: about one sample per minute
  - row labels are pulse evidence only:
    - `anchor`
    - `counted_seam`
    - `excluded_noise`
  - one `PASS / FAIL` verdict for the pulse
  - no row-level product judgments inside that pulse
  - first valid pulse failed:
    - ids: `4850-4863`
    - fixed prompt: `why`
    - anchors: `1`
    - counted seams: `13`
    - excluded noise: `0`
  - false-start batches `4790-4804`, `4805-4819`, and `4820-4849` were
    discarded from the active eval surface
- first correction after the failed pulse is shape-first and grammar-led:
  - choose one plain sentence claim
  - make grammar carry the answer shape
  - prefer one clear subject and finite verb
  - keep imagery secondary to the sentence claim
  - vary sentence openings across samples
- baseline reset note:
  - do not treat that first correction as a clean comparable baseline
  - prior hard-coded prompt scaffolds may have contaminated the current logic
    line even after removal
  - the clean baseline source reset now defines the next proper-config
    candidate before spending more live API calls
  - compare the Beta `6.0` snapshot against that clean baseline as a
    separate line, preferably with a diagram
- Stop condition for the next session:
  - do not start another live pulse until rate limits and prepaid credits are
    confirmed healthy
  - use the existing failed pulse and first correction as planning surfaces only
- `where` is fully stable in the current surface:
  - `84 pass / 0 fail`
- `what` is close behind:
  - `81 pass / 3 fail`

## Next Kernel

Choose one lane at a time:

- app polish:
  - keep the wrapper small
  - do not widen the prompt surface
  - keep the user loop separate from operator commands
- research:
  - keep `Beta 5.1` frozen as the most recently closed row-level beta
  - treat `Beta 6.0` as the latest pulse-level diagnostic snapshot
  - finish docs cleanup and validate the clean baseline reset before running
    local evals
  - preserve the explicit comparison boundary:
    - row-level `5.1`
    - pulse-level `6.0` snapshot
    - clean baseline candidate
  - first clean-baseline pulse target is `why` because it directly compares
    against the Beta `6.0` diagnostic `why` pulse
  - start from a fresh local eval store:
    - `make eval-init`
    - `make eval-pulse-start PROMPT=why PULSE_MINUTES=15`
  - diagram the comparison:
    - Beta `6.0` snapshot
    - clean baseline candidate
    - shared fixed-prompt pulse method
  - once the baseline question is settled, run one fixed-prompt pulse for `15`
    minutes
  - keep each fixed prompt in its own pulse
  - use the one-sample-per-minute pulse default unless the method changes
  - label rows as pulse evidence only
  - treat the first valid pulse verdict as `FAIL`
  - do not validate the first grammar-led correction as if it were already a
    clean baseline
  - do not start another live pulse until the rate-limit / prepaid-credit boundary
    is cleared
- docs:
  - sweep tracked docs after every runtime, product-shape, or research-method change
  - current cleanup should remove stale "active Beta `6.0`" framing from
    stable docs while preserving historical decision entries
  - use `docs/runtime/templates/` for new public research docs and pulse
    reports
  - keep `docs/peanut/` as the private scratch lane

## Guardrails

- Keep the app small.
- Keep the runtime local and CLI-first.
- Keep generation agent-backed through the OpenAI Agents SDK.
- Keep prompt types fixed to `what`, `when`, `why`, and `where`.
- Do not add freeform input while the constrained interaction theory is active.
- Keep eval verdicts binary only.
- Keep the current verdict unit explicit:
  - row-level `5.1`
  - pulse-level `6.0` snapshot
  - clean-baseline pulse candidate
- Keep config structural; prompt phrase banks do not belong there.
- Keep prompt routing minimal; content-led cues invite repetition and drift.
- Prefer baseline-first tuning from repeated failures, not prompt accretion.
- Treat `retain / evict` as the closed row-level failure-family layer, not as
  the pulse-level row gate.
- `when` has earned `evict`, and the first narrow fix is now confirmed.
- `why` has now earned `evict`, but the first fix attempt overcollapsed and
was not promoted.
- Do not use the saturated pre-fix `why` residue as the live post-fix
denominator.
- Do not count one repeated pass family as a healthy `why` lane.
- Do not stack a new `why` fix with unrelated `when` or `where` tinkering.

## Close A Session

Follow `docs/runtime/RUNBOOK.md`.

Compact operator path:

- `make end-preflight` before merge while still on the feature branch
- after merge, sync clean `main`
- `make end` on clean synced `main`
- quick operator sheet: `docs/runtime/START_END_REFERENCE.md`

At minimum:

- validate the active branch
- merge only after checks pass
- end on clean `main` when possible

## Copy/Paste Refresh Prompt

`Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md. In 5 bullets: current state, risks, and next kernel. Before starting implementation, confirm environment/workspace context: canonical repo path is /abs/path/to/probaboracle, confirm host vs devcontainer mode, confirm active git branch, and say whether the thread is on clean main or a feature branch. Apply no-guessing controls: prefer repo-scoped edits and do not modify user shell profile file or global VS Code settings unless explicitly approved in-chat. Run in one active kernel at a time. Then execute the Next Slice from SESSION_HANDOFF with minimal behavior drift and full validation.`
