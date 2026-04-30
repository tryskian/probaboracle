# Beta 3: Coherence + Prompt Relevance

## What This Beta Asked

Once a line is coherent, does it stay in-lane for the selected prompt?

## Eval Shape

- coherence first
- prompt relevance second
- both stay binary

## Main Finding

Prompt relevance is narrower than product fit and different from coherence.

It is not just a word-spotting exercise. The real question is which reasoning
lane is actually leading the sentence.

## Current Signal

Current snapshot:

- relevance: `396 pass / 71 fail / 271 pending`

A useful early result came from the `when` lane:

- many apparent misses were actually boundary cases
- temporal signal could still outrank a small spatial leak
- coherent lines were often still recognisably in-lane

## Why It Matters

This beta separates:

- broken sentence logic
- prompt-lane drift

That makes the research cleaner and keeps coherence as the primary question.

## What Changed Next

Coherent absurdity emerged as a separate class rather than being flattened into
relevance failure.
