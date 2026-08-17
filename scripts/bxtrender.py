"""
BX-Trender — multi-timeframe trend momentum indicator.
Shows color-coded momentum on monthly, weekly, and daily charts.

Usage: python bxtrender.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys


def ema_python(values, period):
    """Pure Python EMA."""
    alpha = 2.0 / (period + 1)
    ema = [values[0]]
    for v in values[1:]:
        ema.append(alpha * v + (1 - alpha) * ema[-1])
    return ema


def rma_python(values, period):
    """Pure Python RMA ( Wilder's smoothing )."""
    alpha = 1.0 / period
    rma = [sum(values[:period]) / period]
    for v in values[period:]:
        rma.append(alpha * v + (1 - alpha) * rma[-1])
    return rma


def rsi_python(gains, losses, period):
    """Pure Python RSI using RMA."""
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
    rsi = [100 - (100 / (1 + rs))]
    alpha = 1.0 / period
    for g, l in zip(gains[period:], losses[period:]):
        avg_gain = alpha * g + (1 - alpha) * avg_gain
        avg_loss = alpha * l + (1 - alpha) * avg_loss
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi.append(100 - (100 / (1 + rs)))
    return rsi


def color_long(val, prev):
    if val > 0:
        return "GREEN" if val > prev else "LIGHT GREEN"
    else:
        return "LIGHT RED" if val > prev else "RED"


def color_short(val, prev):
    if val > 0:
        return "G" if val > prev else "LG"
    else:
        return "LR" if val > prev else "R"


def calc_bxtrender(closes):
    short_l1, short_l2, short_l3 = 5, 20, 5

    ema_sl1 = ema_python(closes, short_l1)
    ema_sl2 = ema_python(closes, short_l2)
    diff_short = [e1 - e2 for e1, e2 in zip(ema_sl1, ema_sl2)]

    # RSI of diff_short minus 50
    gains = [max(diff_short[i] - diff_short[i-1], 0) for i in range(1, len(diff_short))]
    losses = [max(diff_short[i-1] - diff_short[i], 0) for i in range(1, len(diff_short))]

    if len(gains) < short_l3 + 2:
        return None, None, None

    stx = rsi_python(gains, losses, short_l3)
    stx = [v - 50 for v in stx]  # center at 0

    n = len(stx)
    cur_val = stx[-1]
    cur_prev = stx[-2]
    prev_val = stx[-2]
    prev_prev = stx[-3]

    return color_long(prev_val, prev_prev), color_short(prev_val, prev_prev), color_short(cur_val, cur_prev)


def fetch_data(ticker, interval, period):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    # Extract close column as plain list — avoid pandas scalar warnings
    close_series = data['Close'].values.flatten()
    return [float(v) for v in close_series]


def main():
    if len(sys.argv) < 3:
        print("Usage: python bxtrender.py <TICKER> <TIMEFRAME>")
        print("Example: python bxtrender.py NVDA daily")
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

    data = yf.download(symbol, period=period, interval=interval, progress=False)
    if data.empty or len(data) < 26:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    closes = fetch_data(symbol, interval, period)
    price = closes[-1]

    prev_long, prev_short, cur_short = calc_bxtrender(closes)

    print(f"BX-Trender — {symbol} ({tf.upper()})")
    print(f"Price:      ${price:.2f}")
    print(f"Prev bar:  {prev_long} ({prev_short})")
    print(f"Cur bar:   {cur_short}")


if __name__ == "__main__":
    main()
