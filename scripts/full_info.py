"""FinViz full info — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance

if len(sys.argv) < 2:
    print("Usage: python full_info.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
data = stock.ticker_full_info()

for key, val in data.items():
    print(f"{key}: {val}")
