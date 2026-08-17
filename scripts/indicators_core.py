"""
indicators_core.py — Pure Python technical indicator calculations.
No pandas. No external dependencies beyond the standard library + yfinance.
Used by all indicator scripts in this folder.
"""

import math
import yfinance as yf


# ─── NORMAL DISTRIBUTION (Black-Scholes) ──────────────────────────────────────

def norm_pdf(x):
    """Standard normal PDF — pure Python, no scipy."""
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def norm_cdf(x):
    """
    Cumulative distribution function for standard normal — pure Python.
    Abramowitz & Stegun approximation (formula 26.2.17).
    """
    if x < 0:
        return 1 - norm_cdf(-x)
    if x > 37:
        return 1.0
    t = 1.0 / (1.0 + 0.2316419 * x)
    poly = t * (0.319381530
                + t * (-0.356563782
                + t * (1.781477937
                + t * (-1.821255978
                + t * 1.330274429))))
    return 1.0 - norm_pdf(x) * poly


# ─── MOVING AVERAGES ──────────────────────────────────────────────────────────

def sma_python(values, period):
    """Simple moving average."""
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def ema_python(values, period):
    """Exponential moving average."""
    if len(values) < period:
        return None
    alpha = 2.0 / (period + 1)
    ema = sum(values[:period]) / period
    for v in values[period:]:
        ema = alpha * v + (1 - alpha) * ema
    return ema


def rma_python(values, period):
    """Wilder's RMA (smoothed moving average)."""
    if len(values) < period:
        return None
    alpha = 1.0 / period
    rma = sum(values[:period]) / period
    for v in values[period:]:
        rma = alpha * v + (1 - alpha) * rma
    return rma


# ─── RSI ───────────────────────────────────────────────────────────────────────

def rsi_python(values, period=14):
    """RSI using Wilder's RMA."""
    if len(values) < period + 1:
        return None
    deltas = [values[i] - values[i - 1] for i in range(1, len(values))]
    gains = [max(d, 0) for d in deltas]
    losses = [abs(min(d, 0)) for d in deltas]
    avg_gain = rma_python(gains, period)
    avg_loss = rma_python(losses, period)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


# ─── ROLLING HELPERS ─────────────────────────────────────────────────────────

def rolling_max(values, period):
    if len(values) < period:
        return None
    return max(values[-period:])


def rolling_min(values, period):
    if len(values) < period:
        return None
    return min(values[-period:])


def rolling_avg(values, period):
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


# ─── TRUE RANGE ────────────────────────────────────────────────────────────────

def true_range(highs, lows, closes):
    """True Range: max of (H-L, |H-C_prev|, |L-C_prev|)."""
    trs = []
    for i in range(len(highs)):
        if i == 0:
            trs.append(highs[0] - lows[0])
        else:
            h_l = highs[i] - lows[i]
            h_c = abs(highs[i] - closes[i - 1])
            l_c = abs(lows[i] - closes[i - 1])
            trs.append(max(h_l, h_c, l_c))
    return trs


# ─── DATA FETCHING ─────────────────────────────────────────────────────────────

def fetch_ohlc(ticker, interval, period,YF):
    """Fetch OHLCV as plain Python lists. Pass yfinance as YF argument."""
    data = YF.download(ticker, period=period, interval=interval, progress=False)
    highs = [float(v) for v in data['High'].values.flatten()]
    lows = [float(v) for v in data['Low'].values.flatten()]
    closes = [float(v) for v in data['Close'].values.flatten()]
    opens = [float(v) for v in data['Open'].values.flatten()]
    volumes = [float(v) for v in data['Volume'].values.flatten()]
    return opens, highs, lows, closes, volumes
