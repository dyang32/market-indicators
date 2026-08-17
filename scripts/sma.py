"""
SMA — Simple Moving Average
Usage: python sma.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, sma_python


def main():
    if len(sys.argv) < 3:
        print("Usage: python sma.py <TICKER> <TIMEFRAME>")
        print("Example: python sma.py NVDA daily")
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
    sma_20 = sma_python(closes, 20)
    sma_50 = sma_python(closes, 50)
    sma_200 = sma_python(closes, 200) if len(closes) >= 200 else None

    print(f"SMA — {symbol} ({tf.upper()})")
    print(f"Price:   ${price:.2f}")
    print(f"SMA 20:  ${sma_20:.2f}")
    print(f"SMA 50:  ${sma_50:.2f}")
    if sma_200:
        print(f"SMA 200: ${sma_200:.2f}")

    # Golden/death cross
    if sma_20 > sma_50:
        cross = "bullish (20 above 50)"
    else:
        cross = "bearish (20 below 50)"

    print(f"Signal:  {cross}")

    if sma_200:
        if sma_50 > sma_200:
            gdcross = "golden cross"
        else:
            gdcross = "death cross"
        print(f"Cross:   {gdcross} (50 vs 200)")


if __name__ == "__main__":
    main()
