"""
RVOL — Relative Volume. Current volume compared to the average volume over a lookback window.
Shows label (High, Above Avg, Normal, Low) and ratio on monthly, weekly, and daily.

Usage: python rvol.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys


def calc_rvol(volume, window):
    """Pure Python RVOL."""
    cur_vol = volume[-1]
    avg_vol = sum(volume[-window:]) / window
    if avg_vol == 0:
        return None, None
    rvol = round(cur_vol / avg_vol, 1)
    if rvol >= 2.0:
        label = "High"
    elif rvol >= 1.2:
        label = "Above Avg"
    elif rvol >= 0.8:
        label = "Normal"
    else:
        label = "Low"
    return label, rvol


def fetch_volume(ticker, interval, period):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    vol = data['Volume'].values.flatten()
    return [float(v) for v in vol]


def main():
    if len(sys.argv) < 3:
        print("Usage: python rvol.py <TICKER> <TIMEFRAME>")
        print("Example: python rvol.py NVDA daily")
        print("Timeframes: monthly, weekly, daily, hourly")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    tf = sys.argv[2].lower()

    if tf == 'monthly':
        period, interval, window = '5y', '1mo', 12
    elif tf == 'weekly':
        period, interval, window = '2y', '1wk', 10
    elif tf == 'hourly':
        period, interval, window = '730d', '1h', 50
    else:
        period, interval, window = '6mo', '1d', 50

    volume = fetch_volume(symbol, interval, period)

    if len(volume) < window:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price_data = yf.download(symbol, period='6mo', interval='1d', progress=False)
    price = float(price_data['Close'].values.flatten()[-1])
    label, rvol = calc_rvol(volume, window)

    print(f"RVOL — {symbol} ({tf.upper()})")
    print(f"Price:  ${price:.2f}")
    print(f"RVOL:   {label} ({rvol}x)")
    print(f"Window:  {window} bars")
    print(f"Scale:   High >=2.0x | Above Avg >=1.2x | Normal >=0.8x | Low <0.8x")


if __name__ == "__main__":
    main()
