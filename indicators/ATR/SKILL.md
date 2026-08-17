---
name: marketindicators-indicators-atr
description: Average True Range — measures volatility by calculating the average range of price movement over a period.
category: MySKILLS/marketindicators
---

# ATR — Average True Range

Measures volatility by calculating the average range of price movement.

**Script:** `scripts/atr.py`
**Dependencies:** `yfinance`
**Timeframes:** monthly, weekly, daily, hourly

---

## Step by Step

**Step 1:** Open terminal in the `marketindicators` folder.

**Step 2:** Run:
```
python scripts/atr.py NVDA daily
```

**Step 3:** Replace `NVDA` with any ticker symbol.

**Step 4:** Replace `daily` with your timeframe: `monthly`, `weekly`, `daily`, or `hourly`.

---

## Output

```
ATR — AAPL (DAILY)
Price:       $305.93
ATR(14):     $7.84
ATR %:       2.56% of price
1x ATR:      $7.84 move
2x ATR:      $15.68 move
```

---

## What It Means

| ATR Value | Meaning |
|---------|---------|
| High ATR | High volatility — larger daily moves |
| Low ATR | Low volatility — smaller daily moves |
| ATR % of price | Relative volatility — 3% on $100 stock = $3 avg move |

**Use cases:**
- Set stop losses — place stops 1.5-2x ATR below entry
- Position sizing — higher ATR = smaller position
- Confirm breakouts — breakout with high ATR = stronger signal
