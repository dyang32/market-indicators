"""
EMA — Exponential Moving Average
Usage: python ema.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, ema_python


def main():
    if len(sys.argv) < 3:
        print("Usage: python ema.py <TICKER> <TIMEFRAME>")
        print("Example: python ema.py NVDA daily")
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

    if len(closes) < 50:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    ema_9 = ema_python(closes, 9)
    ema_21 = ema_python(closes, 21)
    ema_50 = ema_python(closes, 50)
    ema_200 = ema_python(closes, 200) if len(closes) >= 200 else None

    print(f"EMA — {symbol} ({tf.upper()})")
    print(f"Price:   ${price:.2f}")
    print(f"EMA 9:   ${ema_9:.2f}")
    print(f"EMA 21:  ${ema_21:.2f}")
    print(f"EMA 50:  ${ema_50:.2f}")
    if ema_200:
        print(f"EMA 200: ${ema_200:.2f}")

    # EMA 9/21 crossover
    if ema_9 > ema_21:
        crossover = "bullish"
    else:
        crossover = "bearish"

    # Golden/death cross (50/200)
    if ema_50 and ema_200:
        if ema_50 > ema_200:
            cross = "golden cross"
        else:
            cross = "death cross"
        print(f"Cross:   {cross}")

    print(f"Crossover (9/21): {crossover}")


if __name__ == "__main__":
    main()
