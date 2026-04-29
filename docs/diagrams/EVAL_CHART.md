# Eval Chart

This is the canonical home for Probaboracle's primary static D3 chart.

## Contract

The chart answers one question first:

How much `fail`, `pass`, and `pending` pressure is accumulating in each prompt
lane?

It reads only the live eval SQLite store:

- source table: `eval_outputs`
- verdict field: `current_verdict`
- lane field: `prompt_type`

`pending` is derived from rows where `current_verdict IS NULL`.

## Output

- render target: `docs/diagrams/probaboracle-pass-fail.svg`
- command:

```bash
make render-eval-chart-deps
make render-eval-chart
```

## Visual Notes

- `FAIL` uses the Polinko fail red.
- `PASS` uses the Polinko pass green.
- `PENDING` uses the Polinko source blue.

This is the primary static evidence surface for Probaboracle. If richer detail
is added later, it should sit below or beside this chart rather than replace
the binary lane view.
