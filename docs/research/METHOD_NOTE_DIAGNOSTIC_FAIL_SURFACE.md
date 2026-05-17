# Method Note: Diagnostic Fail Surface

## What This Is

This is a small Polinko-line method rule for the first short run in a new lane
or under a newly tightened runtime surface.

The first short run is not asked to prove health.

It is asked to expose the live failure family.

## Core Rule

Treat the first short run as a diagnostic fail surface:

- keep it short
- hold the runtime baseline steady
- fail the batch at the product layer by default
- use the batch to name the dominant failure family, not to rescue a few early
  passes

This keeps the first read honest.

## Why It Exists

Tiny early batches are good at one thing:

- showing what is wrong right now

They are bad at pretending to prove:

- healthy lane shape
- durable pass rates
- successful runtime correction

If the first short run is judged like a balanced final surface, it invites two
 bad habits:

- early false optimism from a few salvageable lines
- premature intervention before the failure family is actually clear

The diagnostic fail surface prevents that.

## Working Shape

Use the opening sequence like this:

1. Run one short batch.
2. Fail the batch at the product layer by default.
3. Name the dominant failure family.
4. Hold the baseline and gather more pressure if the family is still
   stabilizing.
5. Only then decide:
   - `retain`
   - `evict`
6. After correction, return to real `pass / fail` pressure on the fresh rerun.

## What It Is Not

This is not:

- a claim that every row is equally bad in a final sense
- a substitute for coherence, relevance, or other sidecar reads
- a way to skip the later retain-evict decision

It is a deliberate first-pass posture:

- failure discovery first
- health claims later

## Why It Fits This Line

This method matches the broader Polinko discipline:

- binary judgment stays strict
- the baseline stays steady long enough to learn from failure
- recurring failure earns characterization before intervention
- later passes have to be earned on a fresh surface, not assumed from one
  hopeful mini run
