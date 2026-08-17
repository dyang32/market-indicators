"""
ADX — Average Directional Index + DMI
Usage: python adx.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, true_range, rma_python


def calc_adx(highs, lows, closes, period=14):
    """Returns (adx, plus_di, minus_di)."""
    if len(closes) < period * 2 + 1:
        return None, None, None

    trs = true_range(highs, lows, closes)
    atr = rma_python(trs, period)

    plus_dm = [0.0]
    minus_dm = [0.0]
    for i in range(1, len(highs)):
        hd = highs[i] - highs[i - 1]
        ld = lows[i - 1] - lows[i]
        pd = hd if hd > ld and hd > 0 else 0.0
        md = ld if ld > hd and ld > 0 else 0.0
        plus_dm.append(pd)
        minus_dm.append(md)

    plus_di_vals = [100 * rma_python(plus_dm[:period], period) / rma_python(trs[:period], period)]
    minus_di_vals = [100 * rma_python(minus_dm[:period], period) / rma_python(trs[:period], period)]

    for i in range(period, len(trs)):
        pdi = 100 * rma_python(plus_dm[i - period + 1:i + 1], period) / rma_python(trs[i - period + 1:i + 1], period)
        mdi = 100 * rma_python(minus_dm[i - period + 1:i + 1], period) / rma_python(trs[i - period + 1:i + 1], period)
        plus_di_vals.append(pdi)
        minus_di_vals.append(mdi)

    dx_vals = [100 * abs(p - m) / (p + m) if (p + m) > 0 else 0 for p, m in zip(plus_di_vals, minus_di_vals)]
    adx_vals = [rma_python(dx_vals[:period], period)]

    for i in range(period, len(dx_vals)):
        adx_vals.append(rma_python(dx_vals[i - period + 1:i + 1], period))

    return adx_vals[-1], plus_di_vals[-1], minus_di_vals[-1]


def main():
    if len(sys.argv) < 3:
        print("Usage: python adx.py <TICKER> <TIMEFRAME>")
        print("Example: python adx.py NVDA daily")
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

    if len(closes) < 30:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    adx, plus_di, minus_di = calc_adx(highs, lows, closes)

    print(f"ADX — {symbol} ({tf.upper()})")
    print(f"Price:    ${price:.2f}")
    print(f"ADX(14):  {adx:.2f}")
    print(f"DMI+:     {plus_di:.2f}")
    print(f"DMI-:     {minus_di:.2f}")

    if adx < 20:
        trend = "No trend / ranging"
    elif adx < 40:
        trend = "Weak trend"
    elif adx < 60:
        trend = "Strong trend"
    else:
        trend = "Very strong trend"

    direction = "bullish" if plus_di > minus_di else "bearish"
    print(f"Signal:   {trend} ({direction})")


if __name__ == "__main__":
    main()
