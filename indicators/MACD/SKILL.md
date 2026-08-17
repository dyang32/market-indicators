---
name: marketindicators-indicators-macd
description: Moving Average Convergence Divergence — trend and momentum indicator with crossover signals.
category: MySKILLS/marketindicators
---

# MACD — Moving Average Convergence Divergence

Trend and momentum indicator showing the relationship between two moving averages.

**Script:** `scripts/macd.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/macd.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
MACD — AAPL (DAILY)
Price:       $305.93
MACD Line:   -2.39
Signal:      0.22
Histogram:   -2.62
Crossover:   No crossover
Direction:   Bearish (MACD below signal)
```

---

## What It Means

| Component | Description |
|-----------|-------------|
| MACD Line | 12-period EMA minus 26-period EMA |
| Signal Line | 9-period EMA of MACD line |
| Histogram | MACD minus Signal — shows momentum |

**Crossover signals:**
- MACD crosses above Signal = bullish
- MACD crosses below Signal = bearish
- Histogram crosses zero = momentum shift
