---
name: marketindicators-indicators-rsi
description: Relative Strength Index — momentum oscillator that measures overbought and oversold conditions.
category: MySKILLS/marketindicators
---

# RSI — Relative Strength Index

Momentum oscillator measuring the speed and change of price movements.

**Script:** `scripts/rsi.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/rsi.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
RSI — AAPL (DAILY)
Price:     $305.93
RSI(14):   43.82
Signal:    Neutral
Prev RSI:  43.18 (up 0.64)
```

---

## What It Means

| RSI Value | Signal | Meaning |
|-----------|--------|---------|
| Above 70 | Overbought | Price may be too high, reversal possible |
| 30-70 | Neutral | No extreme reading |
| Below 30 | Oversold | Price may be too low, bounce possible |

**Note:** Overbought does not mean sell. Oversold does not mean buy. Use with trend indicators.
