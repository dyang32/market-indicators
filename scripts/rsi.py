"""
RSI — Relative Strength Index
Usage: python rsi.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, rsi_python


def main():
    if len(sys.argv) < 3:
        print("Usage: python rsi.py <TICKER> <TIMEFRAME>")
        print("Example: python rsi.py NVDA daily")
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

    _, _, _, closes, _ = fetch_ohlc(symbol, interval, period, yf)

    if len(closes) < 15:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    rsi_val = rsi_python(closes)

    if rsi_val is None:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    prev_rsi = rsi_python(closes[:-1]) if len(closes) >= 15 else None
    change = round(rsi_val - prev_rsi, 2) if prev_rsi else 0.0

    if rsi_val >= 70:
        signal = "Overbought"
    elif rsi_val <= 30:
        signal = "Oversold"
    else:
        signal = "Neutral"

    print(f"RSI — {symbol} ({tf.upper()})")
    print(f"Price:     ${price:.2f}")
    print(f"RSI(14):   {rsi_val:.2f}")
    print(f"Signal:    {signal}")
    print(f"Prev RSI:  {prev_rsi:.2f} ({'+' if change >= 0 else ''}{change:.2f})")


if __name__ == "__main__":
    main()
