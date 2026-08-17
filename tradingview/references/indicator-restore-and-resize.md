# Indicator restore — input-key pitfall (verified 08/01/26)

Findings from ENPH daily chart (BATS:ENPH, 1D) while building the indicator library.
indicator library. Pane-resize internals live in `pane-resize-internals.md`
— this file covers the SETTINGS-RESTORE side only.

## 1. Remove → add resets settings to defaults

TradingView does NOT remember an indicator's custom settings across a
remove/re-add cycle. A re-added study comes back with factory defaults.
Always re-apply saved settings after any remove+add.

## 2. Input-key pitfall: `in_X` vs named keys

`data_get_study_values` reports study inputs as `in_0`, `in_1`, … for an
indicator that has been configured. But a RE-ADDED study can expose NAMED
keys instead:

- Original RSI (VeuZJv): inputs `in_0`–`in_7` (length/source/MA type/MA len/stdev)
- Re-added RSI (S3BvWt): inputs were only `length` + `source`

Calling `indicator_set_inputs` with `in_X` keys on the re-added instance
silently returned `updated_inputs: {}` — NOTHING applied, and the RSI-based
MA / stdev settings were silently dropped (RSI value 38.87 survived only
because length 14 + source close are the RSI defaults).

**Fix:** after any add, run `mcp_tradingview_data_get_indicator` on the NEW
entity_id FIRST. It returns the actual input IDs that instance accepts. Set
those keys, then verify with `data_get_study_values` that every saved
setting shows up in the values (e.g. RSI must show BOTH "RSI" and
"RSI-based MA" values; MACD must show Histogram; RGV must show Volume +
Volume MA). Don't trust `updated_inputs` in the set response — verify via
the values.

## 3. Overshoot when batching pane drags (resize cross-ref)

The pixel→stretch factor is computed per drag from the CURRENT pane pair,
so a batch of pre-computed deltas drifts. Observed: after dragging sep[1]
75px (MACD 155→80, THT 155→230), dragging sep[0] by a pre-computed 150px
left THT at 65px — not 80px. A corrective −15px drag on sep[0] fixed it.

**Correct pattern:** resize ONE pane (bottom first) → re-measure all
`.chart-markup-table.pane` heights → compute the next delta from the FRESH
measurement → correct with small follow-up drags if off target.

See `pane-resize-internals.md` for the drag-handler mechanics.
