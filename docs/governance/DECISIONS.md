# Decisions Log

This file is the durable archive of Probaboracle's engineering, runtime, and
eval decisions.

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

If a decision crosses layers, say so plainly instead of flattening the method
into implementation authorship.

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
- Why: The product is a constrained oracle instrument, not an open chat tool;
  the fixed prompts are a reasoning-scope boundary for the interaction, not a
  claim that the runtime itself is mechanically simple.

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
- Why: The app should generate through a real model path, not stitched fragment
  composition.

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
- Why: Keeps local instruction surfaces clear without dragging in unnecessary
  overhead.

## D-006: Python plus Makefile bootstrap

- Date: `2026-04-28`
- Category: `workflow_environment`
- Tags: `python`, `make`, `venv`
- Provenance: `implementation decision`
- Decision:
  - bootstrap with Python
  - use a local `.venv`
  - expose one small Makefile command surface for operator actions
- Why: It is the lightest path that still matches the broader Polinko working
  model.

## D-007: Explicit Polinko lineage

- Date: `2026-04-28`
- Category: `collaboration_method`
- Tags: `polinko_lineage`, `scope_relation`, `shared_discipline`
- Provenance: `human-led method decision`
- Decision:
  - frame Probaboracle explicitly as a mini project within Polinko
  - do not present it as a disconnected side repo
- Why: The runtime is smaller, but the safety posture, eval discipline, and
  systems thinking are continuous with the wider research project.

## D-008: Shared style signals are cues, not a word bank

- Date: `2026-04-28`
- Category: `runtime_engineering`
- Tags: `style_signals`, `human_direction`, `model_reasoning`, `non_template_runtime`
- Provenance: `human-led method decision`
- Decision:
  - use one shared style-signal resource across all prompt types
  - let prompt type control the reasoning lane, not the flavour pool
  - treat the style signals as compositional cues rather than as a fixed
    lexical pool
  - keep the model free to synthesize beyond the literal words provided
  - this shape was explicitly clarified through human direction during the tone
    pass
- Why: The prompt type should control the reasoning lane, while the model
  remains free to synthesize beyond the literal words provided.

## D-009: Hold the baseline and learn from failures

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `baseline`, `pass_fail`, `polinko_method`, `prompt_drift`
- Provenance: `human-led method decision`
- Decision:
  - keep the runtime baseline simple during long eval runs
  - prefer long sample streams plus hard `pass` / `fail` judgment sweeps over
    layering more prompt instructions
  - only change the runtime contract when repeated failures are strong enough
    to earn a real intervention
- Why: This keeps Probaboracle on the Polinko line. The model should reveal its
  real habits through data, then learn from what fails, rather than being
  smothered under prompt accretion.

## D-010: Matched prompt scope and one-node generation

- Date: `2026-04-29`
- Category: `runtime_engineering`
- Tags: `matched_scope`, `safe_interaction`, `minimal_config`, `one_node_generation`
- Provenance: `human-led method decision`
- Decision:
  - keep the fixed prompt surface matched to the intended reasoning scope
  - treat that matched scope as a material guardrail for safe interaction,
    drift control, and preserving the reasoning slope
  - keep runtime config minimal
  - express the target reasoning shape through concise directions rather than a
    long list of restrictions
  - generate words through one model node with shared vocabulary, while prompt
    type constrains the reasoning lane
- Why: Vocabulary is universal. The prompts should bound the kind of reasoning
  the oracle performs, while the model still resolves the actual sentence
  structure in one generation path.

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
- Why: The research question is whether the model can maintain coherent
  sentence reasoning inside constrained guardrails. Product taste is a
  stricter downstream layer, not the core experiment.

## D-012: Downstream eval lenses stay separate

- Date: `2026-04-29`
- Category: `eval_quality`
- Tags: `relevance`, `absurdity`, `layered_judgment`
- Provenance: `human-led method decision`
- Decision:
  - keep prompt relevance as its own binary sidecar
  - evaluate coherent absurdity separately from prompt relevance
  - treat coherent absurdity as a product-fit route for coherent but out-of-lane
    lines
  - do not collapse these lenses back into one overloaded verdict
- Why: Some responses are coherent but out-of-lane, and some out-of-lane
  responses are still valuable oracle behaviour. Separate binary lenses make
  those distinctions visible, and product fit can then distinguish between
  failed relevance and valuable coherent absurdity.

## D-013: Public eval shape stays high-level

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `diagram_surface`, `public_docs`, `internal_docs`
- Provenance: `human-led method decision`
- Decision:
  - keep the public diagram page high-level
  - show the generation pipeline and the eval-shape relationships together in
    tracked docs
  - keep the detailed stop/pass/fail judgment flow in local/private
    `docs/peanut/` notes while it remains an internal research surface
- Why: The public docs should show the system shape clearly without turning the
  repo-facing diagram page into an operator-only judgment chart.

## D-014: Distinct eval approaches are documented as betas

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `research_docs`, `beta_structure`, `method_tracking`
- Provenance: `human-led method decision`
- Decision:
  - treat each distinct eval architecture as a beta
  - document tracked findings by beta approach rather than by every sweep
  - keep raw runs, notebook poking, and private operator notes out of the
    tracked beta docs unless they are explicitly promoted
- Why: The research story needs method shifts, not a pile of batch logs.
  Distinct betas keep the findings legible while `docs/peanut/` remains the
  local lane for raw operator material.

## D-015: Runtime doc ownership stays split by job

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `docs_governance`, `runtime_changes`, `architecture`, `handoff`
- Provenance: `repo formalization`
- Decision:
  - record durable runtime or eval-method changes in `docs/governance/DECISIONS.md`
  - update `docs/runtime/ARCHITECTURE.md` when the stable system shape changes
  - use `docs/governance/SESSION_HANDOFF.md` for the current checkpoint and
    next slice only
  - use `docs/runtime/RUNBOOK.md` for operator procedure changes only
- Why: Runtime adjustments were too easy to smear across several docs. This
  split keeps durable changes, stable shape, live checkpoint, and procedure
  from collapsing into one blurred history lane.

## D-016: Research betas are method eras, not release versions

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `beta_structure`, `research_method`, `repo_framing`
- Provenance: `human-led method decision`
- Decision:
  - treat Probaboracle betas as named research architectures
  - do not present them as package or app release versions
  - use research-era numbering such as `Research Beta 1.0`, `2.0`, `3.0`, and
    `4.0` when the method shifts are distinct eras rather than software
    releases
  - keep the current research beta visible in public repo framing, but point
    beta interpretation back to `docs/research/README.md`
- Why: A plain `v4` label hides what actually changed. The important shift is
  methodological: what the verdict is asking and how the evidence should be
  interpreted.

## D-017: Final output stays one-line and lowercase

- Date: `2026-04-30`
- Category: `runtime_engineering`
- Tags: `output_contract`, `lowercase`, `tone_contract`
- Provenance: `repo formalization`
- Decision:
  - return one short final line only
  - normalise the final output to lowercase
  - keep the line tight, readable, and deadpan rather than fragmentary or
    overworked
- Why: Lowercase and one-line output are part of the oracle contract, not just
  incidental style. They keep the voice flat, comparable, and recognisably
  Probaboracle across lanes.

## D-018: Product fit remains the canonical top-level verdict

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `product_fit`, `sidecars`, `canonical_verdict`
- Provenance: `repo formalization`
- Decision:
  - keep product fit as the canonical top-level verdict stored in
    `eval_outputs.current_verdict`
  - keep coherence, prompt relevance, and coherent absurdity as separate binary
    sidecars rather than replacements for product fit
  - use the sidecars to clarify why a line passed or failed, not to collapse
    the eval surface back into one overloaded judgment
- Why: Product fit remains the strict oracle-quality gate, while the sidecars
  keep sentence quality, lane control, and valuable drift analytically
  separate.

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
  - mirror the latest verdict and note for each lens onto the current snapshot
    columns in `eval_outputs`
- Why: The repo needs both an audit trail of judgments and a fast current-state
  surface for listing, charting, and operator review.

## D-020: Primary public eval chart stays lane-first and binary

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `eval_chart`, `public_surface`, `binary_signal`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - keep the primary public static chart as a prompt-lane stacked bar chart
  - derive that chart from `eval_outputs.current_verdict`
  - treat `NULL` canonical verdicts as `pending`
  - keep richer detail as a secondary surface rather than replacing the binary
    lane chart
- Why: The first visible research pulse should be fail pressure, pass pressure,
  and backlog by lane. That is the cleanest high-level evidence surface for
  this repo.

## D-021: Single-product eval isolates the strongest selective signal

- Date: `2026-04-30`
- Category: `eval_quality`
- Tags: `single_product_eval`, `coherent_absurdity`, `strongest_signal`
- Provenance: `human-led method decision`
- Decision:
  - use broad sweeps when the goal is mapping a lane or clearing a sidecar
    backlog
  - switch to one product per run when the goal is isolating the strongest
    signal for a selective downstream gate
  - for coherent absurdity, judge each generated line in order:
    - coherence
    - relevance
    - absurdity only if it enters the coherence-pass relevance-fail pocket
- Why: Coherent absurdity is too sparse for pooled batch taste to be the main
  instrument. Single-product evaluation keeps attention on whether one line, by
  itself, earns coherence and absurdity at the same time.

## D-022: Local runtime auto-loads the repo `.env`

- Date: `2026-04-30`
- Category: `workflow_environment`
- Tags: `dotenv`, `local_runtime`, `operator_hygiene`
- Provenance: `implementation decision`
- Decision:
  - auto-load the repo `.env` from `src/probaboracle/config.py`
  - keep `override=False` so explicit shell exports still win
  - use the same credential bootstrap path for live CLI generation and local
    eval commands
- Why: The local operator path should not require manual shell sourcing every
  time a sample or ask command runs. Repo-local `.env` loading keeps the
  runtime small while reducing repeated environment grangle.

## D-023: Keep-awake control is not part of the canonical operator surface

- Date: `2026-05-01`
- Category: `workflow_environment`
- Tags: `operator_surface`, `makefile`, `local_runtime`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - remove the macOS `caffeinate` control targets from the canonical Makefile
    surface
  - keep session status focused on repo and eval state only
  - do not treat keep-awake management as a first-class Probaboracle operator
    concern
- Why: The keep-awake lane introduced more operator grangle than value. The
  repo should stay focused on the oracle runtime and eval workflow, not on
  background power-management helpers.

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
- Why: Some lines looked coherent at a glance but only because punctuation and
  stacked fragments were doing the reasoning work. The stricter threshold keeps
  coherence focused on genuine sentence resolution rather than dressed-up blur.

## D-025: Beta 4.1 serial probing should use real chunks, not measly runs

- Date: `2026-05-01`
- Category: `eval_quality`
- Tags: `serial_probe`, `chunk_size`, `beta_4_1`
- Provenance: `human-led method decision`, later `repo formalization`
- Decision:
  - keep Beta 4.1 probing serial:
    - one product
    - immediate judgment
    - next product
  - but treat a longer serial chunk as the minimum useful surface for a live
    checkpoint
  - use `25+` rows as the default minimum useful chunk before summarizing
    progress
  - treat `50-100` rows, or about one hour of serial probing, as the real
    long-run surface
  - keep extra `when` pressure in the mix because that lane is the most useful
    stress test for the current coherence rule
- Why: The value is in the data. Tiny taste-check runs make the method look
  cleaner than it really is and do not produce enough pressure to learn from
  the current coherence threshold.

## D-026: Bare `probaboracle` opens the local app loop

- Date: `2026-05-02`
- Category: `runtime_engineering`
- Tags: `app_wrapper`, `cli`, `local_runtime`
- Provenance: `human-led method decision`, later `implementation decision`
- Decision:
  - make bare `probaboracle` open one persistent local app loop
  - keep that loop local, CLI-first, and agent-backed
  - keep prompt choice in that loop as a fixed selector, not typed input
  - keep explicit subcommands like `ask`, `sample`, `eval-list`, and `judge`
    underneath as the operator surface
  - do not widen the prompt surface or add a separate UI shell just to make it
    feel like an app
- Why: Probaboracle is ready to feel like a real small app, but the right
  wrapper is still the existing local CLI runtime. A persistent session loop
  makes the research instrument runnable without turning the project into a new
  surface area.

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
  - collapse the selector after `enter` so the chosen question and answer stay
    together
  - keep `esc` as the exit path in the selector flow
  - keep operator subcommands and research commands out of the user-facing loop
- Why: The app should feel shaped and legible without turning into a larger UI.
  The durable interaction contract is a tiny header-plus-selector oracle loop,
  not a relaunch-per-question CLI and not a broadened chat surface.

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
  - fall back to simpler stacked header forms as the terminal gets smaller,
    rather than forcing the box to wrap or squash
- Why: The app needs a stronger opening gesture than plain text alone, but the
  right answer is a compact CLI banner with width-aware fallbacks, not a bigger
  UI surface.

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
  - after `enter`, collapse the full selector to the chosen prompt rather than
    leaving the whole menu on screen
  - render the answer on its own line under the selected prompt so the question
    and answer stay contextually attached without turning the selector row into
    a crowded output line
  - keep `esc` as the explicit secondary action in the selector:
    - visible as a soft exit hint on the active row
    - exits cleanly from the selector and follow-up prompt
  - keep the wait state inline and minimal:
    - use the spinner by itself
    - do not add extra `loading` text
- Why: Probaboracle needs enough CLI hierarchy to feel shaped and legible, but
  the interaction still has to stay tiny. The durable UX contract is a
  question-first selector that collapses cleanly, waits in place, and then
  reveals a response without crowding the layout.

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
- Why: Probaboracle's docs are part of the research instrument. Small runtime
  and method changes drift quickly if only the code moves, but copying every
  detail everywhere makes the docs heavy. The repo needs a docs sweep every
  time, with clear ownership for where each update belongs.
