---
name: marketindicators-indicators-williamsr
description: Williams %R — momentum oscillator that measures overbought and oversold levels. Ranges from 0 (overbought) to -100 (oversold).
category: MySKILLS/marketindicators
---

# Williams %R — Momentum Oscillator

Momentum oscillator measuring overbought and oversold levels.

**Script:** `scripts/williamsr.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/williamsr.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
Williams %R — AAPL (DAILY)
Price:     $305.93
Value:     -86.10
Zone:      OVERSOLD
Scale:     0 (overbought) to -100 (oversold)
```

---

## What It Means

| Value | Zone | Meaning |
|-------|------|---------|
| 0 to -20 | OVERBOUGHT | Price near the top of the 21-bar range — may reverse down |
| -20 to -80 | NEUTRAL | No extreme reading |
| -80 to -100 | OVERSOLD | Price near the bottom of the 21-bar range — may bounce up |

**Note:** Williams %R is a leading indicator — it can stay overbought/oversold for long periods in strong trends. Use with trend indicators like BX-Trender or ADX.
