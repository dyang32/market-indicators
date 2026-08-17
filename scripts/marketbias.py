"""
Market Bias — Heikin-Ashi based trend direction indicator.
Shows GREEN, LIGHT GREEN, LIGHT RED, or RED.

Usage: python marketbias.py NVDA monthly
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
from indicators_core import fetch_ohlc, ema_python


def get_bias_color(osc, sig):
    if osc > 0 and osc >= sig:
        return "GREEN"
    if osc > 0 and osc < sig:
        return "LIGHT GREEN"
    if osc < 0 and osc <= sig:
        return "RED"
    if osc < 0 and osc > sig:
        return "LIGHT RED"
    return "NEUTRAL"


def calc_market_bias(opens, highs, lows, closes):
    """
    Heikin-Ashi based Market Bias.
    1. EMA of O/H/L/C (period 20)
    2. HA close = (EMA_O + EMA_H + EMA_L + EMA_C) / 4
    3. HA open  = (prev HA open + prev HA close) / 2
    4. EMA of HA open/close (period 7) -> O2, C2
    5. osc = 100 * (C2 - O2), sig = EMA(osc, 7)
    """
    ha_len, ha_len2, osc_len = 20, 7, 7

    if len(opens) < ha_len + osc_len + 5:
        return None

    # Step 1: Build full EMA series for O, H, L, C
    def ema_series(vals, period):
        alpha = 2.0 / (period + 1)
        result = [sum(vals[:period]) / period]
        for v in vals[period:]:
            result.append(alpha * v + (1 - alpha) * result[-1])
        return result

    ema_o = ema_series(opens, ha_len)
    ema_h = ema_series(highs, ha_len)
    ema_l = ema_series(lows, ha_len)
    ema_c = ema_series(closes, ha_len)

    # Pad to full length
    n = len(opens)
    ema_o = [ema_o[0]] * (n - len(ema_o)) + ema_o
    ema_h = [ema_h[0]] * (n - len(ema_h)) + ema_h
    ema_l = [ema_l[0]] * (n - len(ema_l)) + ema_l
    ema_c = [ema_c[0]] * (n - len(ema_c)) + ema_c

    # Step 2: HA close = (EMA_O + EMA_H + EMA_L + EMA_C) / 4
    ha_close = [(ema_o[i] + ema_h[i] + ema_l[i] + ema_c[i]) / 4 for i in range(n)]

    # Step 3: HA open = (prev HA open + prev HA close) / 2
    ha_open = [(ema_o[0] + ema_c[0]) / 2]
    for i in range(1, n):
        ha_open.append((ha_open[-1] + ha_close[i - 1]) / 2)

    # Step 4: EMA of HA open and HA close (period 7)
    ha_open_ema = ema_series(ha_open, ha_len2)
    ha_close_ema = ema_series(ha_close, ha_len2)

    # Pad
    ha_open_ema = [ha_open_ema[0]] * (n - len(ha_open_ema)) + ha_open_ema
    ha_close_ema = [ha_close_ema[0]] * (n - len(ha_close_ema)) + ha_close_ema

    # Step 5: oscillator = 100 * (HA close EMA - HA open EMA)
    osc_vals = [100 * (ha_close_ema[i] - ha_open_ema[i]) for i in range(n)]

    # Signal = EMA of oscillator (period 7)
    alpha = 2.0 / (osc_len + 1)
    sig = sum(osc_vals[:osc_len]) / osc_len
    for i in range(osc_len, n):
        sig = alpha * osc_vals[i] + (1 - alpha) * sig

    cur_osc = osc_vals[-1]
    return get_bias_color(cur_osc, sig)


def main():
    if len(sys.argv) < 3:
        print("Usage: python marketbias.py <TICKER> <TIMEFRAME>")
        print("Example: python marketbias.py NVDA monthly")
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

    _, highs, lows, closes, _ = fetch_ohlc(symbol, interval, period, yf)

    # For market bias we need opens too
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    opens = [float(v) for v in data['Open'].values.flatten()]

    if len(opens) < 35:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    bias = calc_market_bias(opens, highs, lows, closes)

    print(f"Market Bias — {symbol} ({tf.upper()})")
    print(f"Price:   ${price:.2f}")
    print(f"Bias:    {bias}")

    if bias == "RED":
        print("Signal:  Bearish — do not buy")
    elif bias == "LIGHT RED":
        print("Signal:  Slight bearish")
    elif bias == "LIGHT GREEN":
        print("Signal:  Slight bullish")
    else:
        print("Signal:  Bullish")


if __name__ == "__main__":
    main()
