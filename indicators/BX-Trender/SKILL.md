---
name: marketindicators-indicators-bxtrender
description: BX-Trender — multi-timeframe trend momentum indicator. Shows color-coded momentum (GREEN, LIGHT GREEN, LIGHT RED, RED) on monthly, weekly, and daily charts.
category: MySKILLS/marketindicators
---

# BX-Trender — Multi-Timeframe Trend Momentum Indicator

Shows color-coded momentum on monthly, weekly, and daily charts. Colors represent trend direction and strength.

**Script:** `scripts/bxtrender.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/bxtrender.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
BX-Trender — AAPL (DAILY)
Price:      $305.93
Prev bar:  LIGHT RED (LR)
Cur bar:   LR
```

---

## What It Means

| Color | Trend |
|-------|-------|
| GREEN | Bullish momentum strengthening |
| LIGHT GREEN | Bullish momentum weakening |
| LIGHT RED | Bearish momentum weakening |
| RED | Bearish momentum strengthening |

**Short codes:** G = GREEN, LG = LIGHT GREEN, LR = LIGHT RED, R = RED

**Prev bar** = last completed bar's color. **Cur bar** = current bar (may be incomplete).

Higher timeframes (monthly/weekly) carry more weight for directional bias.
