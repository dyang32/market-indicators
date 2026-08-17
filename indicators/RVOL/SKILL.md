---
name: marketindicators-indicators-rvol
description: RVOL — Relative Volume. Current volume compared to the average volume over a lookback window. Shows label (High, Above Avg, Normal, Low) and ratio.
category: MySKILLS/marketindicators
---

# RVOL — Relative Volume

Current volume compared to the average volume over a lookback window.

**Script:** `scripts/rvol.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/rvol.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
RVOL — AAPL (DAILY)
Price:  $305.93
RVOL:   High (2.3x)
Window:  50 bars
Scale:   High ≥2.0x | Above Avg ≥1.2x | Normal ≥0.8x | Low <0.8x
```

---

## What It Means

| Label | Ratio | Meaning |
|-------|-------|---------|
| High | ≥2.0x | Volume is 2x the average — unusual activity |
| Above Avg | ≥1.2x | Volume slightly above average |
| Normal | ≥0.8x | Volume is average |
| Low | <0.8x | Volume is below average |

**Use cases:**
- High RVOL = institutional activity — worth investigating
- Low RVOL = low interest, range-bound or trending slowly
- Combine with Williams %R — RVOL High + %R Oversold = potential reversal setup

**Lookback windows:**
- Hourly: 50 bars
- Daily: 50 bars
- Weekly: 10 bars
- Monthly: 12 bars
