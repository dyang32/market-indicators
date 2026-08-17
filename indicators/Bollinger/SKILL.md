---
name: marketindicators-indicators-bollinger
description: Bollinger Bands — volatility bands placed above and below a moving average.
category: MySKILLS/marketindicators
---

# Bollinger Bands — Volatility Bands

Volatility bands placed above and below a moving average.

**Script:** `scripts/bollinger.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/bollinger.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
Bollinger Bands — AAPL (DAILY)
Price:          $305.93
Upper Band:     $344.22
Middle (SMA):   $318.22
Lower Band:     $292.22
Bandwidth:      16.34%
Position:       Below middle band (53% to lower)
```

---

## What It Means

| Position | Signal |
|---------|--------|
| Price above upper band | Extended — potential reversal or continuation |
| Price below lower band | Oversold — potential bounce |
| Bands contracting | Low volatility — squeeze — breakout coming |
| Bands expanding | High volatility |

**Bandwidth %** tells you how wide the bands are relative to the middle — narrow bandwidth = squeeze = volatility expansion coming.
