# Decisions Log

This file is the durable archive of Probaboracle's engineering, runtime, and eval decisions.

## How To Use This File

- Need the current durable rules:
  - start with `docs/governance/CHARTER.md`
- Need the current system shape:
  - use `docs/runtime/ARCHITECTURE.md`
- Need the reasoning behind a repo choice:
  - use this file

Keep entries short, but informative enough to show what changed and why.

## Taxonomy

- `runtime_engineering`
- `eval_quality`
- `collaboration_method`
- `workflow_environment`

## Provenance Rule

Each decision should read as one of these:

- `human-led method decision`
  - the theory, bridge logic, or eval meaning came from the human lead
- `repo formalization`
  - the repo later encoded an already-active method or contract
- `implementation decision`
  - the engineering layer chose mechanics after the method was already set

If a decision crosses layers, say so plainly instead of flattening the method into implementation authorship.

## D-001: Local CLI first

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `local_first`, `cli`, `small_surface`
- Provenance: `repo formalization`
- Decision:
  - start with a local CLI runtime before any broader surface
  - keep the first execution path terminal-native and local
- Why: Keeps setup light and preserves tokens for actual product shaping.

## D-002: Fixed prompt surface

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `prompt_surface`, `safety_scope`, `constrained_input`
- Provenance: `human-led method decision`
- Decision:
  - limit the active prompt types to:
    - `what`
    - `when`
    - `why`
    - `where`
  - do not accept freeform prompt input in the active runtime path
- Why: The product is a constrained oracle instrument, not an open chat tool; the fixed prompts are a reasoning-scope boundary for the interaction, not a claim that the runtime itself is mechanically simple.

## D-003: Binary eval gates

- Date: `2026-04-28`
- Category: `eval_quality`
- Tags: `pass_fail`, `polinko_lineage`, `strict_judgment`
- Provenance: `human-led method decision`
- Decision:
  - keep human eval verdicts strictly binary:
    - `pass`
    - `fail`
  - do not add mixed or partial verdict states
- Why: This carries the same pass/fail discipline as the wider Polinko work.

## D-004: Agent-backed generation

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `agents_sdk`, `model_native`, `non_template_runtime`
- Provenance: `human-led method decision`
- Decision:
  - use the OpenAI Agents SDK as the runtime generation path
  - do not build the active oracle path out of stitched static fragments
- Why: The app should generate through a real model path, not stitched fragment composition.

## D-005: Small doc stack

- Date: `2026-04-28`
- Category: `workflow_environment`
- Tags: `docs_stack`, `runbook`, `architecture`
- Provenance: `implementation decision`
- Decision:
  - use a trimmed Polinko-style doc stack:
    - charter
    - decisions
    - architecture
    - runbook
    - session handoff
    - diagrams
- Why: Keeps local instruction surfaces clear without dragging in unnecessary overhead.

## D-006: Python plus Makefile bootstrap

- Date: `2026-04-28`
- Category: `workflow_environment`
- Tags: `python`, `make`, `venv`
- Provenance: `implementation decision`
- Decision:
  - bootstrap with Python
  - use a local `.venv`
  - expose one small Makefile command surface for operator actions
- Why: It is the lightest path that still matches the broader Polinko working model.

## D-007: Explicit Polinko lineage

- Date: `2026-04-28`
- Category: `collaboration_method`
- Tags: `polinko_lineage`, `scope_relation`, `shared_discipline`
- Provenance: `human-led method decision`
- Decision:
  - frame Probaboracle explicitly as a mini project within Polinko
  - do not present it as a disconnected side repo
- Why: The runtime is smaller, but the safety posture, eval discipline, and systems thinking are continuous with the wider research project.

## D-008: Shared style signals are cues, not a word bank

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `style_signals`, `human_direction`, `model_reasoning`, `non_template_runtime`
- Provenance: `human-led method decision`
- Decision:
  - use one shared style-signal resource across all prompt types
  - let prompt type control the reasoning lane, not the flavour pool
  - treat the style signals as compositional cues rather than as a fixed lexical pool
  - keep the model free to synthesize beyond the literal words provided
  - this shape was explicitly clarified through human direction during the tone pass
- Why: The prompt type should control the reasoning lane, while the model remains free to synthesize beyond the literal words provided.

## D-009: Hold the baseline and learn from failures

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `baseline`, `pass_fail`, `polinko_method`, `prompt_drift`
- Provenance: `human-led method decision`
- Decision:
  - keep the runtime baseline simple during long eval runs
  - prefer long sample streams plus hard `pass` / `fail` judgment sweeps over layering more prompt instructions
  - only change the runtime contract when repeated failures are strong enough to earn a real intervention
- Why: This keeps Probaboracle on the Polinko line. The model should reveal its real habits through data, then learn from what fails, rather than being smothered under prompt accretion.

## D-010: Matched prompt scope and one-node generation

- Date: `2026-04-29`
- Category: `runtime_engineering`
- Tags: `matched_scope`, `safe_interaction`, `minimal_config`, `one_node_generation`
- Provenance: `human-led method decision`
- Decision:
  - keep the fixed prompt surface matched to the intended reasoning scope
  - treat that matched scope as a material guardrail for safe interaction, drift control, and preserving the reasoning slope
  - keep runtime config minimal
  - express the target reasoning shape through concise directions rather than a long list of restrictions
  - generate words through one model node with shared vocabulary, while prompt type constrains the reasoning lane
- Why: Vocabulary is universal. The prompts should bound the kind of reasoning the oracle performs, while the model still resolves the actual sentence structure in one generation path.

## D-011: Coherence is the primary experimental gate

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `coherence`, `sidecar_eval`, `research_method`
- Provenance: `human-led method decision`
- Decision:
  - treat sentence coherence as the primary experimental binary gate
  - keep product fit separate from coherence
  - evaluate coherence with a dedicated sidecar verdict:
    - `pass`
    - `fail`
- Why: The research question is whether the model can maintain coherent sentence reasoning inside constrained guardrails. Product taste is a stricter downstream layer, not the core experiment.

## D-012: Downstream eval lenses stay separate

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `relevance`, `absurdity`, `layered_judgment`
- Provenance: `human-led method decision`
- Decision:
  - keep prompt relevance as its own binary sidecar
  - evaluate coherent absurdity separately from prompt relevance
  - treat coherent absurdity as a product-fit route for coherent but out-of-lane lines
  - do not collapse these lenses back into one overloaded verdict
- Why: Some responses are coherent but out-of-lane, and some out-of-lane responses are still valuable oracle behaviour. Separate binary lenses make those distinctions visible, and product fit can then distinguish between failed relevance and valuable coherent absurdity.

## D-013: Public eval shape stays high-level

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `diagram_surface`, `public_docs`, `internal_docs`
- Provenance: `human-led method decision`
- Decision:
  - keep the public diagram page high-level
  - show the generation pipeline and the eval-shape relationships together in tracked docs
  - keep the detailed stop/pass/fail judgment flow in local/private `docs/peanut/` notes while it remains an internal research surface
- Why: The public docs should show the system shape clearly without turning the repo-facing diagram page into an operator-only judgment chart.

## D-014: Distinct eval approaches are documented as betas

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `research_docs`, `beta_structure`, `method_tracking`
- Provenance: `human-led method decision`
- Decision:
  - treat each distinct eval architecture as a beta
  - document tracked findings by beta approach rather than by every sweep
  - keep raw runs, notebook poking, and private operator notes out of the tracked beta docs unless they are explicitly promoted
- Why: The research story needs method shifts, not a pile of batch logs. Distinct betas keep the findings legible while `docs/peanut/` remains the local lane for raw operator material.

## D-015: Runtime doc ownership stays split by job

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `docs_governance`, `runtime_changes`, `architecture`, `handoff`
- Provenance: `repo formalization`
- Decision:
  - record durable runtime or eval-method changes in `docs/governance/DECISIONS.md`
  - update `docs/runtime/ARCHITECTURE.md` when the stable system shape changes
  - use `docs/governance/SESSION_HANDOFF.md` for the current checkpoint and next slice only
  - use `docs/runtime/RUNBOOK.md` for operator procedure changes only
- Why: Runtime adjustments were too easy to smear across several docs. This split keeps durable changes, stable shape, live checkpoint, and procedure from collapsing into one blurred history lane.

## D-016: Research betas are method eras, not release versions

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `beta_structure`, `research_method`, `repo_framing`
- Provenance: `human-led method decision`
- Decision:
  - treat Probaboracle betas as named research architectures
  - do not present them as package or app release versions
  - use research-era numbering such as `Research Beta 1.0`, `2.0`, `3.0`, and `4.0` when the method shifts are distinct eras rather than software releases
  - keep the current research beta visible in public repo framing, but point beta interpretation back to `docs/research/README.md`
- Why: A plain `v4` label hides what actually changed. The important shift is methodological: what the verdict is asking and how the evidence should be interpreted.

## D-017: Final output stays one-line and lowercase

- Date: `2026-04-30`
- Category: `runtime_engineering`
- Tags: `output_contract`, `lowercase`, `tone_contract`
- Provenance: `repo formalization`
- Decision:
  - return one short final line only
  - normalise the final output to lowercase
  - keep the line tight, readable, and deadpan rather than fragmentary or overworked
- Why: Lowercase and one-line output are part of the oracle contract, not just incidental style. They keep the voice flat, comparable, and recognisably Probaboracle across lanes.

## D-018: Product fit remains the canonical top-level verdict

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `product_fit`, `sidecars`, `canonical_verdict`
- Provenance: `repo formalization`
- Decision:
  - keep product fit as the canonical top-level verdict stored in `eval_outputs.current_verdict`
  - keep coherence, prompt relevance, and coherent absurdity as separate binary sidecars rather than replacements for product fit
  - use the sidecars to clarify why a line passed or failed, not to collapse the eval surface back into one overloaded judgment
- Why: Product fit remains the strict oracle-quality gate, while the sidecars keep sentence quality, lane control, and valuable drift analytically separate.

## D-019: Eval storage keeps both history and current snapshot

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `eval_storage`, `sqlite`, `history`, `current_state`
- Provenance: `implementation decision`
- Decision:
  - keep generated rows in `eval_outputs`
  - keep append-only judgment history tables for:
    - product fit
    - coherence
    - prompt relevance
    - coherent absurdity
  - mirror the latest verdict and note for each lens onto the current snapshot columns in `eval_outputs`
- Why: The repo needs both an audit trail of judgments and a fast current-state surface for listing, charting, and operator review.

## D-020: Primary public eval chart stays lane-first and binary

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `eval_chart`, `public_surface`, `binary_signal`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep the primary public static chart as a prompt-lane stacked bar chart
  - derive that chart from `eval_outputs.current_verdict`
  - treat `NULL` canonical verdicts as `pending`
  - keep richer detail as a secondary surface rather than replacing the binary lane chart
- Why: The first visible research pulse should be fail pressure, pass pressure, and backlog by lane. That is the cleanest high-level evidence surface for this repo.

## D-021: Single-product eval isolates the strongest selective signal

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `single_product_eval`, `coherent_absurdity`, `strongest_signal`
- Provenance: `human-led method decision`
- Decision:
  - use broad sweeps when the goal is mapping a lane or clearing a sidecar backlog
  - switch to one product per run when the goal is isolating the strongest signal for a selective downstream gate
  - for coherent absurdity, judge each generated line in order:
    - coherence
    - relevance
    - absurdity only if it enters the coherence-pass relevance-fail pocket
- Why: Coherent absurdity is too sparse for pooled batch taste to be the main instrument. Single-product evaluation keeps attention on whether one line, by itself, earns coherence and absurdity at the same time.

## D-022: Local runtime auto-loads the repo `.env`

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `dotenv`, `local_runtime`, `operator_hygiene`
- Provenance: `implementation decision`
- Decision:
  - auto-load the repo `.env` from `src/probaboracle/config.py`
  - keep `override=False` so explicit shell exports still win
  - use the same credential bootstrap path for live CLI generation and local eval commands
- Why: The local operator path should not require manual shell sourcing every time a sample or ask command runs. Repo-local `.env` loading keeps the runtime small while reducing repeated environment grangle.

## D-023: Keep-awake control is not part of the canonical operator surface

- Date: `2026-05-01`
- Category: `workflow_environment`
- Tags: `operator_surface`, `makefile`, `local_runtime`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - remove the macOS `caffeinate` control targets from the canonical Makefile surface
  - keep session status focused on repo and eval state only
  - do not treat keep-awake management as a first-class Probaboracle operator concern
- Why: The keep-awake lane introduced more operator grangle than value. The repo should stay focused on the oracle runtime and eval workflow, not on background power-management helpers.

## D-024: Coherence requires one resolved sentence, not stacked fragments

- Date: `2026-05-01`
- Category: `eval_quality`
- Tags: `coherence`, `sentence_resolution`, `stricter_threshold`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - keep coherence as the primary experimental gate
  - tighten the coherence threshold so a `pass` means:
    - one resolved sentence
    - one dominant reasoning lane
    - punctuation supporting the line rather than propping it up
    - at most one comma in a short line
  - fail lines that read like:
    - stacked fragments
    - a one-line list or tiny poem
    - hinge accumulation held together by commas and connective residue
    - any short line with more than one comma
- Why: Some lines looked coherent at a glance but only because punctuation and stacked fragments were doing the reasoning work. The stricter threshold keeps coherence focused on genuine sentence resolution rather than dressed-up blur.

## D-025: Beta 4.1 serial lane work should use real chunks, not measly runs

- Date: `2026-05-01`
- Category: `eval_quality`
- Tags: `serial_lane`, `chunk_size`, `beta_4_1`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - keep Beta 4.1 serial lane work:
    - one product
    - immediate judgment
    - next product
  - but treat a longer serial chunk as the minimum useful surface for a live checkpoint
  - use `25+` rows as the default minimum useful chunk before summarizing progress
  - treat `50-100` rows, or about one hour of serial lane work, as the real long-run surface
  - keep extra `when` pressure in the mix because that lane is the most useful stress test for the current coherence rule
- Why: The value is in the data. Tiny taste-check runs make the method look cleaner than it really is and do not produce enough pressure to learn from the current coherence threshold.

## D-026: Bare `probaboracle` opens the local app loop

- Date: `2026-05-02`
- Category: `runtime_engineering`
- Tags: `app_wrapper`, `cli`, `local_runtime`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - make bare `probaboracle` open one persistent local app loop
  - keep that loop local, CLI-first, and agent-backed
  - keep prompt choice in that loop as a fixed selector, not typed input
  - keep explicit subcommands like `ask`, `sample`, `eval-list`, and `judge` underneath as the operator surface
  - do not widen the prompt surface or add a separate UI shell just to make it feel like an app
- Why: Probaboracle is ready to feel like a real small app, but the right wrapper is still the existing local CLI runtime. The app loop makes the research instrument runnable without creating a new surface area.

## D-027: The app loop keeps a small staged interaction rhythm

- Date: `2026-05-02`
- Category: `runtime_engineering`
- Tags: `app_loop`, `selector`, `header`, `interaction_rhythm`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep the app loop staged:
    - identity
    - selection
    - answer
    - another-question prompt
  - collapse the selector after `enter` so the chosen question and answer stay together
  - keep `esc` as the exit path in the selector flow
  - keep operator subcommands and research commands out of the user-facing loop
- Why: The app should feel shaped and legible without turning into a larger UI. The durable interaction contract is a tiny header-plus-selector oracle loop.

## D-028: The app opens with a real banner, with narrower fallbacks

- Date: `2026-05-02`
- Category: `runtime_engineering`
- Tags: `banner`, `header`, `cli_typography`, `responsive_fallback`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep a real Probaboracle banner at startup
  - use the banner as the app's identity block:
    - title
    - one-line oracle/chatbot strapline
    - repo pointer
  - use a boxed header when the terminal is wide enough
  - fall back to simpler stacked header forms as the terminal gets smaller, rather than forcing the box to wrap or squash
- Why: The app needs a stronger opening gesture than plain text alone, but the right answer is a compact CLI banner with width-aware fallbacks, not a bigger UI surface.

## D-029: The app loop uses staged CLI hierarchy and an inline wait state

- Date: `2026-05-02`
- Category: `runtime_engineering`
- Tags: `ux`, `layout`, `loader`, `selector`, `cli_hierarchy`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep the CLI interaction visually hierarchical:
    - identity block first
    - selector block second
    - selected prompt and answer block third
    - follow-up prompt after that
  - after `enter`, collapse the full selector to the chosen prompt rather than leaving the whole menu on screen
  - render the answer on its own line under the selected prompt so the question and answer stay contextually attached without turning the selector row into a crowded output line
  - keep `esc` as the explicit secondary action in the selector:
    - visible as a soft exit hint on the active row
    - exits cleanly from the selector and follow-up prompt
  - keep the wait state inline and minimal:
    - use the spinner by itself
    - do not add extra `loading` text
- Why: The app needs enough hierarchy to stay readable during generation. The wait state and answer layout should support the tiny loop without becoming a second interface.

## D-030: Runtime and method changes require a tracked docs sweep

- Date: `2026-05-03`
- Category: `workflow_environment`
- Tags: `docs_governance`, `docs_sweep`, `drift_control`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - sweep tracked docs before merging any change that touches:
    - runtime shape
    - app UX
    - product framing
    - research method
    - eval interpretation
  - keep the sweep scoped to the docs that own the changed surface
  - do not push every detail into every doc
- Why: Probaboracle's docs are part of the research instrument. Small runtime and method changes drift quickly if only the code moves, but copying every detail everywhere makes the docs heavy. The repo needs a docs sweep every time, with clear ownership for where each update belongs.

## D-031: Stale pending product rows are archived out of active eval surfaces

- Date: `2026-05-05`
- Category: `eval_quality`
- Tags: `archive`, `pending`, `active_surface`, `sqlite`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep `pass` and `fail` as the only live product verdict states
  - treat `pending` as temporary backlog state, not as a durable third bucket
  - when product-pending rows become stale, archive them instead of leaving them in the active counts forever
  - keep archived rows in `eval_outputs` with archive metadata
  - hide archived rows from default operator listings, session counts, and the public static chart
- Why: Old unresolved rows distort the live research pulse. Archiving preserves provenance without letting stale backlog masquerade as current eval pressure.

## D-032: Stale dependency PRs are auto-closed out of the active queue

- Date: `2026-05-05`
- Category: `workflow_environment`
- Tags: `github_automation`, `dependabot`, `stale_prs`, `queue_hygiene`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - apply the `dependencies` label to repo-managed dependency bump PRs
  - run a scheduled stale-PR workflow against dependency-labelled PRs only
  - mark dependency PRs stale after `14` idle days
  - close them after `7` more idle days
  - do not use this workflow to close general human work by default
- Why: Probaboracle is a small repo, and unattended dependency bumps can quickly dominate the open PR surface. Auto-closing stale dependency PRs keeps the queue legible without deleting the underlying history.

## D-033: The OpenAI Python SDK is pinned directly, not only through Agents

- Date: `2026-05-06`
- Category: `runtime_engineering`
- Tags: `openai_sdk`, `dependency_pin`, `runtime_contract`
- Provenance: `implementation decision`
- Decision:
  - pin the official `openai` Python SDK directly in `pyproject.toml`
  - do not leave the runtime depending on `openai` only as a transitive dependency of `openai-agents`
  - keep the direct SDK pin current alongside the Agents SDK pin
- Why: Probaboracle is agent-backed, but its OpenAI runtime dependency should still be explicit. A direct pin makes upgrades and compatibility checks legible instead of leaving the effective SDK version to transitively drift underneath the repo.

## D-034: Live eval work follows the token management protocol

- Date: `2026-05-07`
- Category: `runtime_engineering`
- Tags: `token_management`, `cost_console`, `live_eval`, `operator_posture`
- Provenance: `human-led runtime suggestion with implementation decision`
- Decision:
  - treat throughput limits and spend as separate operator control planes
  - keep one-off live checks small
  - treat extended serial runs as explicit batch work
  - add quick operator shortcuts for visibility:
    - `make open-limits`
    - `make open-usage`
    - `make open-billing`
    - `make open-cost-console`
- Why: Probaboracle's live lane is small, but the same drift applies here as in the wider research line: a quiet serial run can still consume budget or hit limits while looking harmless. The cost console keeps the live path visible without widening the app surface or turning the operator lane into an unbounded token sink.

## D-035: Extended serial reruns clear stale product backlog and judge in tandem

- Date: `2026-05-07`
- Category: `eval_quality`
- Tags: `serial_lane`, `tandem_judging`, `archive_reset`, `live_operator`
- Provenance: `human-led runtime correction`, later `implementation decision`
- Decision:
  - before relaunching an extended serial rerun, archive stale product-pending rows out of the active surface
  - for long serial reruns, pair one generator loop with one tandem product judge scoped to the fresh run ids
  - stamp coherence and prompt relevance alongside each product pass during that tandem pass
  - keep fresh product pending at `0` whenever the tandem judge can hold the edge
- Why: A long serial rerun becomes unreadable when stale backlog and fresh backlog share the same active surface. Clearing the old tail first, then stamping rows during generation, keeps the live signal honest and the end-of-run review legible.

## D-036: Hold the baseline and brute-force the failing lane before intervention

- Date: `2026-05-08`
- Category: `eval_quality`
- Tags: `when_lane`, `baseline_hold`, `brute_eval`, `sidecar_archive`
- Provenance: `human-led runtime correction`, later `implementation decision`
- Decision:
  - when one lane is still the clear failure cluster, keep the runtime baseline fixed and push longer single-lane eval pressure before changing the rule
  - do not treat one long run plus a repeated fail shape as enough reason to intervene if the active method is still brute-force characterization
  - if an older pre-sidecar judgment pocket is only historical residue and no longer a live queue, archive it out of the active surface instead of fabricating retrospective sidecar verdicts
- Why: The `when` lane still needed more pressure under the same rule before any runtime or prompt intervention could mean anything. Premature tweaking would blur the evidence instead of sharpening it. The older `914-1277` pre-sidecar rows were not a real active backlog anymore, so archiving them preserved a legible active surface without pretending late sidecar judgments were current research signal.

## D-037: Fail is evidence and evict is the later runtime correction

- Date: `2026-05-08`
- Category: `eval_quality`
- Tags: `fail_vs_evict`, `retain_vs_evict`, `when_lane`, `queue_discipline`, `runtime_correction`
- Provenance: `human-led method import`, later `repo formalization`
- Decision:
  - treat the eval loop as:
    - `pass / fail`
    - if `fail`, decide `retain / evict`
    - rerun under the resulting lane
    - judge `pass / fail` again
  - `retain` means the failure family stays in the active lane while the fixed
    rule keeps taking pressure
  - reserve `evict` for the later upstream runtime or boundary correction made
    because that evidence has stabilized into one known bad family
  - do not keep re-judging a family forever once it has clearly moved from
    active evidence into known residue
  - do not claim a `when` eviction fix yet while the current Beta `4.1` lane is
    still in brute-force characterization mode
- Why: Probaboracle needed the same distinction Hue formalized. `Fail` should
  tell us where the current lane breaks. `Retain` keeps us honest about when
  more baseline pressure is still the right move. `Evict` should only appear
  once the evidence is strong enough that the recurring family has earned
  removal or upstream correction. That keeps the queue honest and stops
  premature runtime meddling from masquerading as research progress.

## D-038: Beta 5.0 promotes retain versus evict as a tracked research layer

- Date: `2026-05-08`
- Category: `eval_quality`
- Tags: `beta_5`, `retain_vs_evict`, `when_lane`, `research_architecture`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - close Beta `4.1` after the dedicated `when` rerun rather than stretching
    coherent absurdity to cover a queue-posture question it does not answer
  - promote Beta `5.0` once the `when` fail family has been characterized under
    the fixed rule
  - track `retain / evict` as the new post-fail decision layer
  - open Beta `5.0` with `when` still in `retain`, not with a pre-claimed
    eviction fix
- Why: The closing Beta `4.1` `when` rerun stayed narrow and repetitive:
  `266` `stacked timing fragments`, `102` semicolon-led timing drift, and no
  coherent-absurdity pocket at all. That did not create a new coherent
  absurdity finding. It created a new architecture question about when repeated
  failure remains live evidence and when it has finally earned an upstream
  correction.

## D-039: The second long `when` retain rerun earns eviction

- Date: `2026-05-09`
- Category: `eval_quality`
- Tags: `when_lane`, `beta_5`, `retain_vs_evict`, `eviction_threshold`
- Provenance: `long-run evidence`, later `human-led decision`
- Decision:
  - treat the second long `when` retain rerun as the deciding Beta `5.0`
    evidence slice
  - mark `when` as `evict` after rows `3392-4097`
  - keep the runtime unchanged until the next slice implements one narrow
    eviction correction on a fresh branch
  - require a post-evict confirmation rerun before claiming improvement
- Why: The second long retain pass did not widen the failure story. It
  repeated the same narrow family at scale: `272` `stacked timing fragments`,
  `85` `semicolon pile and unresolved timing drift`, and `32` `awkward
  temporal phrasing`, with `317 pass / 389 fail / 0 pending`. That is no
  longer live ambiguity. It is a stable enough family to earn correction.

## D-040: The first `when` eviction fix should be one plain timing cue

- Date: `2026-05-09`
- Category: `runtime_shape`
- Tags: `when_lane`, `evict_fix`, `timing_cue`, `confirmation_rerun`
- Provenance: `human-led narrow-fix decision`, later `confirmed runtime change`
- Decision:
  - tighten the `when` lane guard to one plain timing cue only
  - prefer a single moment, arrival, or not-yet frame
  - avoid semicolons
  - keep the line as one resolved sentence that denies schedule usefulness once
  - confirm the change with a `100`-row `when` rerun before claiming improvement
- Why: The confirmation rerun (`4098-4197`) came back `97 pass / 3 fail / 0
  pending`. The old failure surface collapsed: `semicolon pile and unresolved
  timing drift` dropped to `0`, `stacked timing fragments` dropped to `1`, and
  only `2` `awkward temporal phrasing` misses remained. That is enough to
  confirm the narrow fix was pointed at the right family.

## D-041: The first long `why` retain rerun earns eviction

- Date: `2026-05-09`
- Category: `eval_quality`
- Tags: `why_lane`, `beta_5`, `retain_vs_evict`, `duplicate_fallback`
- Provenance: `long-run evidence`, later `human-led decision`
- Decision:
  - treat the first long `why` retain rerun as the deciding Beta `5.0`
    evidence slice for the `why` lane
  - mark `why` as `evict` after rows `4198-4642`
  - keep the runtime unchanged until the next slice implements one narrow
    `why` eviction correction on a fresh branch
  - target the product-level duplicate fallback family first, not a broad lane
    rewrite
- Why: The rerun closed at `77 pass / 368 fail / 0 pending`, with the fail
  surface dominated by `292` `duplicate why fallback` rows, then `65`
  `stacked hinge accumulation` and `11` `too fallback-bare for product pass`.
  The sidecar signal mostly held (`380` coherence passes, `380` relevance
  passes), so the main live problem is repetitive product fallback rather than
  lane loss. That is stable enough to earn correction.

## D-042: Saturated post-evict `why` residue should be archived before the next fix

- Date: `2026-05-09`
- Category: `eval_quality`
- Tags: `why_lane`, `archive_before_fix`, `bad_denominator`, `post_evict_residue`
- Provenance: `human-led cleanup decision`, later `repo formalization`
- Decision:
  - archive the current active `why` residue before the next narrow `why` fix
  - do not carry the `4198-4642` `why` surface forward as the live comparison
    denominator for the post-fix rerun
  - treat the next `why` slice as fresh evidence only
- Why: Once `why` had already earned `evict`, the continued active surface
  (`77 pass / 368 fail / 0 pending`) stopped being useful post-fix comparison
  data. It mostly records how much room the old duplicate-fallback family had
  to breed before correction, not how good the lane could be after a narrow
  fix. Keeping that residue active would poison the denominator and blur the
  next read.

## D-043: Dependency and security checks are first-class default-branch gates

- Date: `2026-05-12`
- Category: `workflow_environment`
- Tags: `github_actions`, `dependabot`, `dependency_review`, `security_gates`
- Provenance: `implementation decision`
- Decision:
  - keep the default-branch required checks to:
    - `markdownlint`
    - `test`
    - `dependency-review`
    - `python-security`
    - `node-security`
  - keep Dependabot version updates active for:
    - `github-actions`
    - `pip`
    - `npm`
  - treat GitHub secret scanning and Dependabot security updates as part of the
    repo baseline
- Why: Probaboracle now has both Python and Node dependency surfaces, so the
  repo should gate dependency changes explicitly instead of relying on a lighter
  CI-only posture or the retired stale-PR cleanup lane.

## D-044: Track repo-native pre-commit hooks and typecheck as baseline hygiene

- Date: `2026-05-13`
- Category: `workflow_environment`
- Tags: `pre_commit`, `pre_push`, `typecheck`, `repo_hygiene`
- Provenance: `human-led method decision with implementation decision`
- Decision:
  - treat this hook-surface addition as human-led:
    - the human lead set the direction for the standards pass
    - Codex executed, formalized, and validated the repo-facing update
  - add tracked `pre-commit` and `pre-push` hooks as part of the local repo
    baseline
  - expose first-class `make` targets for:
    - `typecheck`
    - `test`
    - `precommit-install`
    - `precommit-run`
    - `prepush-run`
  - keep hook execution routed through native repo commands instead of ad hoc
    editor or shell assumptions
- Why: Probaboracle already had the underlying lint, format, and unittest
  surfaces, plus a configured mypy toolchain in `pyproject.toml`. The missing
  piece was a tracked repo-native hook surface and a first-class typecheck
  command. Adding them closes the standards gap without changing the app or
  eval contract.

## D-045: Put the startup reading cue in the final `STOP` block

- Date: `2026-05-13`
- Category: `workflow_environment`
- Tags: `operator_surface`, `startup`, `session_ops`, `repo_hygiene`
- Provenance: `human-led operator decision with implementation decision`
- Decision:
  - treat this startup-ritual refinement as human-led:
    - the human lead set the operator expectation
    - Codex executed, formalized, and validated the repo-facing update
  - keep `make start` in two explicit phases:
    - machine context and startup safety checks first
    - docs read, startup read, and kernel declaration in the final `STOP`
      block
  - keep the canonical docs list inside the final `STOP` block instead of
    front-loading it before the machine checks
  - when the start routine changes, sync all three surfaces in the same kernel:
    - `tools/start_of_day_routine.sh`
    - `docs/runtime/START_END_REFERENCE.md`
    - `docs/runtime/RUNBOOK.md`
- Validation:
  - `make start`
  - `bash -n tools/start_of_day_routine.sh`
  - `git diff --check`
- Why: Probaboracle's startup ritual should end with the same explicit operator
  pause as the rest of the toy family. The docs list matters most at the final
  stop sign, where the next instance has to read, summarize, and name exactly
  one active kernel before doing repo work.

## D-046: Align the full start/end operator surface with the repo family

- Date: `2026-05-14`
- Category: `workflow_environment`
- Tags: `operator_surface`, `start_end`, `wake_lock`, `repo_family`
- Provenance: `human-led operator decision with implementation decision`
- Decision:
  - align Probaboracle with the shared repo-family operator target contract:
    - `make start`
    - `make end`
    - `make end-preflight`
    - `make end-git-check`
    - `make caffeinate`
    - `make caffeinate-status`
    - `make decaffeinate-status`
    - `make decaffeinate`
    - `make doctor-env`
    - `make session-status`
    - `make rituals`
  - keep `make end` as the strict clean-main closeout command
  - keep `make end-preflight` for branch-local validation before clean-main
    enforcement
  - make wake-lock ownership PID-scoped:
    - repo-managed PIDs may be stopped by the repo
    - unmanaged `caffeinate` processes are reported but not adopted or stopped
- Validation:
  - shared target matrix check
  - `bash -n tools/start_of_day_routine.sh tools/end_of_day_routine.sh`
  - `make doctor-env`
  - `npm run lint:docs`
  - `make check`
  - `make end-git-check` on synced `main`
- Why: Probaboracle had caught up to the toy-family closeout contract, but its
  docs still needed a durable current-truth entry for the full shared operator
  surface and safer wake-lock ownership model.

## D-047: Add path leak guards and replace the old startup STOP block with one canonical rehydrate prompt

- Date: `2026-05-15`
- Category: `workflow_environment`
- Tags: `operator_surface`, `rehydrate_prompt`, `path_hygiene`, `repo_hygiene`
- Provenance: `human-led operator decision with implementation decision`
- Decision:
  - add repo-native path leak checks:
    - tracked scope for CI and tracked repo truth
    - local scope for repo-owned private lanes such as `.history`, `.local`, and `docs/peanut`
  - fail the markdown/docs CI lane if tracked path leaks are present
  - add path leak checks to `make end` and `make end-preflight`
  - keep `make start` mechanical:
    - workspace context
    - `make doctor-env`
    - `make caffeinate`
    - `make caffeinate-status`
    - `make session-status`
  - replace the old final `STOP` block with one canonical rehydrate prompt
  - the rehydrate prompt must tell the agent to:
    - read `README.md`, `CHARTER`, `DECISIONS`, `ARCHITECTURE`, `RUNBOOK`, and `SESSION_HANDOFF`
    - return 5 bullets covering current state, risks, and next kernel
    - confirm repo path, host vs devcontainer mode, active branch, and whether the thread is on clean `main` or a feature branch
    - apply the no-guessing controls
    - run one active kernel at a time
    - execute the `Next Slice` from `SESSION_HANDOFF` with full validation
- Validation:
  - `bash -n tools/start_of_day_routine.sh tools/end_of_day_routine.sh`
  - `python ./scripts/path_leak_check.py --scope tracked`
  - `python ./scripts/path_leak_check.py --scope local`
  - `python -m unittest tests.test_path_leak_check`
  - `make start`
  - `make end-preflight`
- Why: the old startup STOP text had drifted into a weaker reminder while the
  repo still carried hardcoded local paths in tracked operator surfaces.
  Probaboracle needed the same fail-closed path hygiene and the same readable
  rehydrate contract that now exists in the stricter repo-family standard.

## D-048: Remove hard-coded phrase scaffolds from the runtime instruction surface

- Date: `2026-05-16`
- Category: `runtime_engineering`
- Tags: `instruction_surface`, `shape_first`, `drift_control`, `why_lane`
- Provenance: `human-led method decision with implementation decision`
- Decision:
  - treat this correction as a human-led method decision:
    - the human lead identified the drift through runtime audit
    - Codex formalized the repo-facing decision and will execute the cleanup
  - treat explicit phrase pools, stock opener lists, and hard-coded good-example
    lines in the active runtime instructions as drift from the durable contract
  - keep the instruction surface shape-first:
    - reasoning lane
    - tone contract
    - output constraints
    - lane guardrails
  - remove content-led scaffolds that oversteer the line toward repeated wording
    or stock closures
  - do not reintroduce a disguised word bank through examples, favourite
    closers, or preferred stock phrases
  - before the next promoted `why` fix, audit the live instruction path and
    strip any remaining hard-coded phrase scaffolds from:
    - `src/probaboracle/config.py`
    - `src/probaboracle/agent.py`
- Validation:
  - repo audit against:
    - `D-008`
    - `D-010`
    - `docs/governance/SESSION_HANDOFF.md`
  - confirm the live instruction path no longer hard-codes phrase examples as
    favored output content
- Why: The durable repo rules already say that style signals are cues, not a
  word bank, and that content-led cues invite repetition and drift. The live
  runtime surface had not fully caught up: it still carried explicit phrase
  pools, stock openers, and example lines that can collapse generation into
  repeated wording. Probaboracle needs the narrower shape-first contract before
  the next real `why` correction work, or the runtime will keep smuggling the
  same drift back in through the instruction layer.

## D-049: Beta 5.1 keeps the retain-evict architecture but tightens the instruction surface

- Date: `2026-05-16`
- Category: `eval_quality`
- Tags: `beta_5_1`, `retain_vs_evict`, `instruction_surface`, `shape_first`
- Provenance: `human-led method decision with implementation decision`
- Decision:
  - promote the current tracked beta from `5.0` to `5.1`
  - keep the beta question and architecture unchanged:
    - `retain / evict` remains the active post-fail research layer
  - use the `.1` bump to mark a method-tightening inside the same beta:
    - remove hard-coded phrase scaffolds
    - keep the live instruction path shape-first
    - preserve wording variation instead of steering the model through stock
      openers or closers
  - treat the next fresh `why` rerun as operating under the cleaned `5.1`
    instruction surface, not as one more `5.0` slice
- Why: This change does not ask a new architecture question, so it is not a
  full new beta. But it does materially tighten the live method by removing
  instruction-layer drift that was still feeding repeated wording back into the
  lane. `5.1` is the right label for "same retain-evict frame, cleaner
  instruction contract."

## D-050: Stage pre-Beta 6.0 fail-pressure pulse for non-OCR evals

- Date: `2026-05-16`
- Category: `eval_quality`
- Tags: `pre_beta_6`, `fail_pressure_pulse`, `non_ocr`, `pulse_judgment`
- Provenance: `human-led hypothesis import`, pending later `repo formalization`
- Decision:
  - stage fail-pressure pulse as `pre-Beta 6.0` after the closed `5.1` line
  - keep its scope broader than language-only:
    - non-OCR evals
    - language and logic-heavy pulses where fixed prompt shape matters more than
      isolated row replay
  - if later promoted, the binary unit would change from the row to the
    fixed-prompt pulse:
    - the pulse carries `PASS / FAIL`
    - rows become evidence inside that pulse
  - if later promoted, row evidence would be judged inside the pulse as:
    - `anchor`
    - `counted seam`
    - `excluded noise`
  - if later promoted, excluded-noise cleanup must stay auditable:
    - raw pulse count visible
    - counted pulse count visible
    - every exclusion gets a narrow reason
  - do not treat this as the active Probaboracle method yet
  - keep `Research Beta 5.1` as the most recently closed row-level baseline
    until the repo is explicitly updated to support pulse-level judgment
  - promote to `Beta 6.0` only when the first real fail-pressure pulse run
    starts
- Why: The upstream Polinko hypothesis is no longer just a small first-batch
  fail heuristic. It proposes a different binary unit for bounded non-OCR
  runs: the pulse passes or fails, while rows act as evidence inside that
  pulse. That is substantial enough to count as a real candidate next phase for
  Probaboracle, but it should not be smuggled in as if the repo already
  supports it. Pre-beta staging keeps the next phase explicit without claiming
  that `Beta 6.0` has already started.

## D-051: Closeout only finishes when active product pending is zero

- Date: `2026-05-17`
- Category: `workflow_environment`
- Tags: `closeout_gate`, `pending_zero`, `product_surface`
- Decision:
  - `make end` must fail while active product rows are still pending
  - use the product verdict surface in `eval_outputs.current_verdict` as the
    closeout pending gate
  - keep sidecar lens backlog out of this specific stop-state gate
- Why: Product fit is the canonical top-level oracle gate in this repo. Day
  close should not pass while that active product surface is still unresolved.

## D-052: Local tooling targets mirror closeout and CI gates

- Date: `2026-05-21`
- Category: `workflow_environment`
- Tags: `tooling_baseline`, `closeout`, `security_gates`, `operator_surface`
- Provenance: `human-led tooling hygiene decision with implementation decision`
- Decision:
  - keep `Makefile` as the operator command surface for local validation
  - expose first-class Make targets for:
    - `make lint-docs`
    - `make end-docs-check`
    - `make package-install-check`
    - `make security-checks`
  - keep package build and editable-install import checks separate:
    - `make package-check` proves the distribution can build
    - `make package-install-check` proves the local editable import surface is
      intact
  - make the active closeout script call Make targets instead of hidden npm
    commands or direct Python script paths
  - keep `scripts/end_of_day_routine.sh` only as a compatibility shim to the
    active `tools/end_of_day_routine.sh`
  - include `pip-audit` in the dev dependency surface so local security checks
    do not depend on ad hoc global tooling
- Validation:
  - `make check`
  - `make lint-docs`
  - `make package-check`
  - `make package-install-check`
  - `make security-checks`
  - `bash -n tools/end_of_day_routine.sh scripts/end_of_day_routine.sh`
- Why: Probaboracle already had CI security gates and closeout scripts, but the
  local operator surface hid some checks behind npm commands and carried a
  stale duplicate end routine. The repo family needs a compact, explicit
  tooling surface that can be mirrored by the other toys without widening
  runtime or eval behavior.

## D-053: Beta 6.0 judges one fixed-prompt pulse

- Date: `2026-05-21`
- Category: `eval_quality`
- Tags: `beta_6`, `fail_pressure_pulse`, `pulse_level_verdict`, `why_prompt`
- Provenance: `human-led method decision with implementation decision`
- Decision:
  - promote `pre-Beta 6.0` to active `Research Beta 6.0`
  - keep the normal beta-test cadence, using `eval-pulse` as the active method
  - use the fixed-prompt pulse, not the individual row, as
    the next binary evidence unit
  - open a separate fixed-prompt pulse for each prompt
  - run one fixed prompt for `15` minutes as one fixed-prompt pulse
  - default to one sample per minute inside that pulse
  - assign one `PASS / FAIL` verdict to the pulse
  - do not assign Beta `6.0` row-level product judgments
  - allow pulse evidence labels inside the pulse:
    - `anchor`
    - `counted_seam`
    - `excluded_noise`
  - keep pulse labels separate from `eval_outputs.current_verdict`
  - let pulse-labeled rows keep `current_verdict` empty without blocking
    closeout
  - keep `archive-pending` scoped to unlabeled product-pending rows
  - treat the earlier false-start batches as invalid protocol data, not Beta `6.0`
    evidence
  - keep `Research Beta 5.1` as the closed row-level comparison baseline
  - do not treat the first pulse as judged until a valid 15-minute pulse gets a
    pulse-level verdict
- Why: The staged fail-pressure hypothesis is now active, but the binary unit
  is one fixed-prompt pulse. Row-level product verdicts
  would collapse the method back into the `5.1` architecture, and a combined
  multi-prompt pulse would blur which fixed prompt actually held shape. Rows
  can only serve as pulse evidence, and each valid `6.0` result must be judged
  as one fixed-prompt pulse.

## D-054: First Beta 6.0 fail-pressure pulse failed on soft-drift collapse

- Date: `2026-05-21`
- Category: `eval_quality`
- Tags: `beta_6`, `fail_pressure_pulse`, `why_prompt`, `counted_seam`
- Provenance: `live eval result`
- Result:
  - first valid pulse ids: `4850-4863`
  - fixed prompt: `why`
  - duration: `15` minute paced pulse
  - raw rows: `14`
  - anchors: `1`
  - counted seams: `13`
  - excluded noise: `0`
  - pulse verdict: `FAIL`
- Decision:
  - keep rows `4850-4863` as pulse-labeled evidence
  - do not product-judge those rows through `eval_outputs.current_verdict`
  - treat the repeated soft-drift surface as the first active Beta `6.0`
    failure family
  - make the next correction shape-based, not phrase-bank-based
- Why: The pulse remained grammatically answer-shaped, but almost every row
  reused the same vague motion family: quiet / soft / whisper, drift / edge,
  meaning / certainty, and land / arrive / settle. That is exactly the
  pulse-level seam Beta `6.0` was created to catch.

## D-055: Pause live Beta 6.0 reruns on rate-limit and prepaid-credit boundary

- Date: `2026-05-21`
- Category: `operations`
- Tags: `beta_6`, `rate_limit`, `prepaid_credits`, `live_eval_pause`
- Provenance: `human operator stop condition`
- Decision:
  - pause additional live Beta `6.0` pulses for the day
  - do not start another live pulse until rate limits and prepaid credits are
    confirmed healthy
  - use the failed `4850-4863` pulse as the next planning surface
  - keep the next correction shape-based and avoid hard-coded phrase banks
- Why: The first valid pulse already produced enough evidence to plan the next
  method slice. More live generation would spend limited prepaid credits while
  adding pressure before the failure family has been digested.

## D-056: First Beta 6.0 correction adds grammatical-shape pressure

- Date: `2026-05-22`
- Category: `runtime_engineering`
- Tags: `beta_6`, `why_prompt`, `shape_first`, `soft_drift`
- Provenance: `failed pulse planning surface with implementation decision`
- Decision:
  - use failed pulse rows `4850-4863` as the correction surface
  - keep the prompt surface fixed and do not add a phrase bank
  - keep the correction grammatical and shape-first:
    - choose one plain sentence claim
    - make grammar carry the answer shape
    - prefer one clear subject and finite verb
    - keep imagery secondary to the sentence claim
    - vary sentence openings across samples
  - do not run another live pulse until the rate-limit / prepaid-credit boundary
    is cleared
- Validation:
  - `make lint-docs`
  - `git diff --check`
  - `make check`
- Why: The first valid `why` pulse did not fail because the prompt needed
  content examples. It failed because the model kept replacing the answer shape
  with repeated soft abstraction. The smallest correction is to make the
  sentence grammar carry more of the shape while still preserving the fixed
  prompt surface and non-concrete oracle contract.
