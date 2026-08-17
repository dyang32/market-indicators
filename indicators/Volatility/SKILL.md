---
name: marketindicators-indicators-volatility
description: Annualized volatility and Sharpe ratio — measures risk-adjusted returns.
category: MySKILLS/marketindicators
---

# Volatility — Annualized Volatility and Sharpe Ratio

Measures risk-adjusted returns based on historical price data.

**Script:** `scripts/volatility.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/volatility.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
Volatility — AAPL (DAILY)
Price:             $305.93
Annual Vol:        28.75%
Annual Return:     20.07%
Sharpe Ratio:      0.70
```

---

## What It Means

| Metric | What it means |
|--------|--------------|
| Annual Vol | How much the stock typically moves per year. 28% = volatile |
| Annual Return | Expected annual return based on the lookback period |
| Sharpe Ratio | Risk-adjusted return. Above 1 = good. Above 2 = excellent. Below 0 = bad |

**Sharpe Ratio guide:**
- 0.0 = no return for the risk taken
- 0.5 = below average
- 1.0 = acceptable
- 2.0+ = excellent risk-adjusted returns
- 3.0+ = exceptional

**Note:** Higher timeframe data gives more reliable Sharpe ratios but fewer data points.
