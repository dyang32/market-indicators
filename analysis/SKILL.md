---
name: marketindicators-technicals
description: Full technical analysis — all indicators computed at once. RSI, MACD, Bollinger Bands, SMA, EMA, ATR, ADX, crossover signals, volatility, Sharpe ratio.
category: MySKILLS/marketindicators
---

# marketindicators/technicals

Computes all technical indicators for a ticker in one call. Pure Python — no external TA library needed.

**Script:** `scripts/technicals/technicals.py`

## Single Ticker
```
hermes-venv/Scripts/python.exe skills/MySKILLS/marketindicators/scripts/technicals/technicals.py NVDA 3mo
```

## Multiple Tickers
```
hermes-venv/Scripts/python.exe -c "
from skills.MySKILLS.marketindicators.scripts.technicals.technicals import compute_multi
result = compute_multi(['NVDA','AAPL','MSFT','GOOGL'], '3mo')
for r in result['results']:
    print(r['symbol'], '|', r['price']['current'], '| RSI:', r['indicators'].get('rsi',{}).get('value'), '| ADX:', r['indicators'].get('adx',{}).get('adx'))
"
```

## All Indicators Output

```
SYMBOL: AAPL  |  PERIOD: 3mo  |  PRICE: $305.93
================================================================================
  RSI(14):         43.34
  MACD:            -2.56 | Signal: -0.02 | Hist: -2.54 | Crossover: bearish
  Bollinger:       Lower $292.22 | Mid $318.22 | Upper $344.22 | BW: 16.34%
  SMA:             20=$318.22 | 50=$308.95 | Cross: None
  EMA:             9=$308.74 | 12=$310.45 | 21=$312.83 | 26=$313.01 | Cross: None
  ATR(14):        $7.85 (2.56% of price)
  ADX:             21.90 | DMI+ 21.96 | DMI- 29.77 | Trend: bearish

  Vol (ann):       25.03%
  Sharpe:          1.26
  Return (ann):    31.58%

SIGNALS:
  - RSI oversold (43.34)
```

## Periods
`1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`

Add `--earnings` to show next earnings date.
