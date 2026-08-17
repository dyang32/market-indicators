---
name: marketindicators-indicators-adx
description: Average Directional Index — measures trend strength. DMI+ and DMI- show trend direction.
category: MySKILLS/marketindicators
---

# ADX — Average Directional Index

Measures trend strength. DMI+ and DMI- show trend direction.

**Script:** `scripts/adx.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/adx.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
ADX — AAPL (DAILY)
Price:    $305.93
ADX:      21.33
DMI+:     22.29
DMI-:     29.67
Trend:    Weak bearish trend (ADX 21.3)
```

---

## What It Means

| ADX Value | Signal |
|-----------|--------|
| Above 25 | Strong trend |
| 20-25 | Weak trend / ranging |
| Below 20 | No trend |

**DMI+ vs DMI-:**
- DMI+ above DMI- = bullish trend
- DMI- above DMI+ = bearish trend

ADX only measures strength, not direction. Direction comes from DMI.
