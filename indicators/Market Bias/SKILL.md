---
name: marketindicators-indicators-marketbias
description: Market Bias — Heikin-Ashi based trend direction indicator. Shows GREEN, LIGHT GREEN, LIGHT RED, or RED. Used to filter trade direction.
category: MySKILLS/marketindicators
---

# Market Bias — Trend Direction Indicator

Heikin-Ashi based indicator showing overall trend direction. Used to filter which trades to take.

**Script:** `scripts/marketbias.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/marketbias.py NVDA monthly
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `monthly` with your timeframe: `monthly`, `weekly`, or `daily`.

---

## Output

```
Market Bias — AAPL (MONTHLY)
Price:   $305.93
Bias:    GREEN
Signal:  Bullish
```

---

## What It Means

| Bias | Meaning |
|------|---------|
| GREEN | Bullish — in an uptrend |
| LIGHT GREEN | Slight bullish momentum |
| LIGHT RED | Slight bearish momentum |
| RED | Bearish — in a downtrend |

**Trading rule:** If Market Bias is RED on the monthly, do not take long positions. Only take longs when bias is GREEN or LIGHT GREEN.

**Used in combination with BX-Trender** for the rating system:
- RED bias → always Bad
- GREEN/LIGHT GREEN bias → use monthly BX-Trender for rating
