"""
Volatility — Annualized Volatility and Sharpe Ratio
Usage: python volatility.py NVDA daily
Timeframes: monthly, weekly, daily, hourly
Dependencies: yfinance
"""

import yfinance as yf
import sys
import math
from indicators_core import fetch_ohlc


def compute_volatility(closes):
    """Pure Python volatility and Sharpe."""
    if len(closes) < 30:
        return None, None, None

    # Log returns
    returns = []
    for i in range(1, len(closes)):
        if closes[i - 1] > 0:
            returns.append(math.log(closes[i] / closes[i - 1]))

    if len(returns) < 2:
        return None, None, None

    # Mean return
    mean_ret = sum(returns) / len(returns)

    # Std dev
    variance = sum((r - mean_ret) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)

    # Annualize based on daily bars
    annual_vol = std_dev * math.sqrt(252)
    annual_return = mean_ret * 252
    sharpe = (annual_return / annual_vol) if annual_vol > 0 else 0.0

    return annual_vol * 100, annual_return * 100, sharpe


def main():
    if len(sys.argv) < 3:
        print("Usage: python volatility.py <TICKER> <TIMEFRAME>")
        print("Example: python volatility.py NVDA daily")
        print("Timeframes: monthly, weekly, daily, hourly")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    tf = sys.argv[2].lower()

    if tf == 'monthly':
        period, interval = 'max', '1mo'
    elif tf == 'weekly':
        period, interval = 'max', '1wk'
    elif tf == 'hourly':
        period, interval = '730d', '1h'
    else:
        period, interval = '2y', '1d'

    _, _, _, closes, _ = fetch_ohlc(symbol, interval, period, yf)

    if len(closes) < 30:
        print(f"Error: insufficient data for {symbol} ({tf})")
        sys.exit(1)

    price = closes[-1]
    annual_vol, annual_return, sharpe = compute_volatility(closes)

    print(f"Volatility — {symbol} ({tf.upper()})")
    print(f"Price:           ${price:.2f}")
    print(f"Annual Vol:       {annual_vol:.2f}%")
    print(f"Annual Return:    {annual_return:.2f}%")
    print(f"Sharpe Ratio:    {sharpe:.2f}")


if __name__ == "__main__":
    main()
