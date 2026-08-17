"""
Williams %R — momentum oscillator measuring overbought/oversold levels.
Shows value and zone on monthly, weekly, and daily charts.

Usage: python williamsr.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys


def rolling_max(highs, period):
    result = []
    for i in range(len(highs)):
        if i < period - 1:
            result.append(max(highs[:i+1]))
        else:
            result.append(max(highs[i-period+1:i+1]))
    return result


def rolling_min(lows, period):
    result = []
    for i in range(len(lows)):
        if i < period - 1:
            result.append(min(lows[:i+1]))
        else:
            result.append(min(lows[i-period+1:i+1]))
    return result


def calc_willy(highs, lows, closes, period=21):
    hh = rolling_max(highs, period)
    ll = rolling_min(lows, period)
    last_close = closes[-1]
    last_hh = hh[-1]
    last_ll = ll[-1]
    if last_hh == last_ll:
        return -50.0
    return 100 * (last_close - last_hh) / (last_hh - last_ll)


def fetch_ohlc(ticker, interval, period):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    h = data['High'].values.flatten()
    l = data['Low'].values.flatten()
    c = data['Close'].values.flatten()
    return [float(v) for v in h], [float(v) for v in l], [float(v) for v in c]


def main():
    if len(sys.argv) < 3:
        print("Usage: python williamsr.py <TICKER> <TIMEFRAME>")
        print("Example: python williamsr.py NVDA daily")
        print("Timeframes: monthly, weekly, daily")
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

    highs, lows, closes = fetch_ohlc(symbol, interval, period)

    if len(closes) < 21:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    wr = calc_willy(highs, lows, closes)

    if wr >= -20:
        zone = "OVERBOUGHT"
    elif wr <= -80:
        zone = "OVERSOLD"
    else:
        zone = "NEUTRAL"

    print(f"Williams %R — {symbol} ({tf.upper()})")
    print(f"Price:     ${price:.2f}")
    print(f"Value:     {wr:.2f}")
    print(f"Zone:      {zone}")
    print(f"Scale:     0 (overbought) to -100 (oversold)")


if __name__ == "__main__":
    main()
