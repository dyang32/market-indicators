"""
Bollinger Bands
Usage: python bollinger.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, sma_python


def main():
    if len(sys.argv) < 3:
        print("Usage: python bollinger.py <TICKER> <TIMEFRAME>")
        print("Example: python bollinger.py NVDA daily")
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

    if len(closes) < 20:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    mid = sma_python(closes, 20)

    # Rolling std dev
    n = 20
    mean = mid
    variance = sum((c - mean) ** 2 for c in closes[-n:]) / n
    std = variance ** 0.5

    upper = mid + (2 * std)
    lower = mid - (2 * std)
    bandwidth = round((upper - lower) / mid * 100, 2)

    print(f"Bollinger Bands — {symbol} ({tf.upper()})")
    print(f"Price:    ${price:.2f}")
    print(f"Upper:    ${upper:.2f}")
    print(f"Mid:      ${mid:.2f}")
    print(f"Lower:    ${lower:.2f}")
    print(f"Bandwidth: {bandwidth:.2f}%")

    if price > upper:
        zone = "Above upper band (extended)"
    elif price < lower:
        zone = "Below lower band (oversold)"
    elif price > mid:
        zone = "Above mid (bullish lean)"
    else:
        zone = "Below mid (bearish lean)"

    pct_b = round((price - lower) / (upper - lower) * 100, 2) if upper != lower else 50
    print(f"%B:       {pct_b:.2f}")
    print(f"Zone:     {zone}")


if __name__ == "__main__":
    main()
