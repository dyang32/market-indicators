"""
ATR — Average True Range
Usage: python atr.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, true_range, rma_python


def main():
    if len(sys.argv) < 3:
        print("Usage: python atr.py <TICKER> <TIMEFRAME>")
        print("Example: python atr.py NVDA daily")
        print("Timeframes: monthly, weekly, daily, hourly")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    tf = sys.argv[2].lower()

    if tf == 'monthly':
        period, interval = '5y', '1mo'
    elif tf == 'weekly':
        period, interval = '2y', '1wk'
    elif tf == 'hourly':
        period, interval = '730d', '1h'
    else:
        period, interval = '6mo', '1d'

    _, highs, lows, closes, _ = fetch_ohlc(symbol, interval, period, yf)

    if len(closes) < 15:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    trs = true_range(highs, lows, closes)
    atr_val = rma_python(trs, 14)

    atr_pct = round(atr_val / price * 100, 2)

    print(f"ATR — {symbol} ({tf.upper()})")
    print(f"Price:   ${price:.2f}")
    print(f"ATR(14): ${atr_val:.2f}")
    print(f"ATR %:   {atr_pct:.2f}% of price")


if __name__ == "__main__":
    main()
