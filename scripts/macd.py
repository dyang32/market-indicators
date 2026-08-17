"""
MACD — Moving Average Convergence Divergence
Usage: python macd.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, ema_python


def calc_macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal:
        return None, None, None, None, None

    ema_fast = ema_python(closes, fast)
    ema_slow = ema_python(closes, slow)
    macd_line = ema_fast - ema_slow

    # Build macd line values for signal EMA
    macd_vals = []
    for i in range(slow - 1, len(closes)):
        ef = ema_python(closes[:i + 1], fast)
        es = ema_python(closes[:i + 1], slow)
        macd_vals.append(ef - es)

    signal_line = ema_python(macd_vals, signal)
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


def main():
    if len(sys.argv) < 3:
        print("Usage: python macd.py <TICKER> <TIMEFRAME>")
        print("Example: python macd.py NVDA daily")
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

    if len(closes) < 35:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    result = calc_macd(closes)

    if result[0] is None:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    macd_line, signal_line, histogram = result

    print(f"MACD — {symbol} ({tf.upper()})")
    print(f"Price:      ${price:.2f}")
    print(f"MACD Line:  {macd_line:.2f}")
    print(f"Signal:     {signal_line:.2f}")
    print(f"Histogram:  {histogram:+.2f}")

    if macd_line > signal_line and histogram > 0:
        signal = "Bullish crossover"
    elif macd_line < signal_line and histogram < 0:
        signal = "Bearish crossover"
    elif macd_line > signal_line:
        signal = "Bullish momentum"
    else:
        signal = "Bearish momentum"

    print(f"Signal:     {signal}")


if __name__ == "__main__":
    main()
