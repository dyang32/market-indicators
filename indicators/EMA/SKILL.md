---
name: marketindicators-indicators-ema
description: Exponential Moving Averages — faster-moving averages that give more weight to recent prices. Includes EMA 9/21 crossover signal.
category: MySKILLS/marketindicators
---

# EMA — Exponential Moving Average

Faster-moving averages that give more weight to recent prices.

**Script:** `scripts/ema.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/ema.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
EMA — AAPL (DAILY)
Price:  $305.93
EMA 9:  $308.74  (below price)
EMA 12: $310.45  (below price)
EMA 21: $312.83  (below price)
EMA 26: $313.01  (below price)
Crossover (9/21): No crossover
```

---

## What It Means

| EMA | Use |
|-----|-----|
| 9 | Very short-term, fast |
| 12 | Short-term |
| 21 | Medium-term |
| 26 | Slow, confirms trend |

**Crossover signals:**
- EMA 9 crosses above EMA 21 = bullish short-term momentum
- EMA 9 crosses below EMA 21 = bearish short-term momentum

EMA reacts faster to price changes than SMA. Use for quicker signals.
