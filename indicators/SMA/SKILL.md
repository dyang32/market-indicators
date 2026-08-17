---
name: marketindicators-indicators-sma
description: Simple Moving Averages — trend lines that smooth price data. Detects golden cross and death cross.
category: MySKILLS/marketindicators
---

# SMA — Simple Moving Average

Simple trend lines that smooth price data over a set period.

**Script:** `scripts/sma.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/sma.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
SMA — AAPL (DAILY)
Price:   $305.93
SMA 20:  $318.22  (below price)
SMA 50:  $308.95  (below price)
SMA 200: $279.99  (above price)
Cross:   No cross
```

---

## What It Means

| Signal | What it means |
|--------|--------------|
| Golden cross | SMA 20 crosses above SMA 50 = bullish |
| Death cross | SMA 20 crosses below SMA 50 = bearish |
| Price above SMA | Bullish trend |
| Price below SMA | Bearish trend |

**Note:** Golden/death cross is a lagging signal — it confirms trends after they have already started.
