# Eval Ruleset

This ruleset keeps local `pass` / `fail` judgements consistent while the classifier pipeline is still being tuned.

## Pass

Mark an output as `pass` if it is:

- coherent
- concise
- deadpan
- mysterious
- confident
- unhelpful

A passing line should read like a deliberate non-answer, not like a broken sentence or a normal assistant reply.

## Fail

Mark an output as `fail` if it is any of the following:

- poetic, florid, or soupy
- helpful, advisory, or instructional
- too long
- padded with unnecessary extenders
- too soft or wishy-washy
- too direct or conclusive
- off-type for the selected question kind

## Type Expectations

### `what`

Should feel like identity, category, or definition wobble.

Good:

- `Definitely a maybe.`
- `Arguably the thing.`

Bad:

- `It seems to be some kind of thing that...`

### `when`

Should feel like awkward, inconvenient, or misaligned timing.

Good:

- `Certainly too late.`
- `Probably not yet.`

Bad:

- `Likely around when you least expect it.`

### `how`

Should feel like method or process without becoming usable advice.

Good:

- `Technically in steps.`
- `Probably through a process.`

Bad:

- `Start by figuring out what you want.`

### `why`

Should feel like cause or explanation without providing real insight.

Good:

- `For reasons unclear.`
- `Because that seems to be the reason.`

Bad:

- `Because you need to trust yourself.`

### `where`

Should feel like place, direction, or location without becoming practical.

Good:

- `Definitely elsewhere.`
- `Probably nearby.`

Bad:

- `Two streets east of the station.`

## Tie-break Rule

If a line half-works but still feels wrong, mark it as `fail`.

This project does not use a `mixed` bucket. Short lines either land or they do not.
