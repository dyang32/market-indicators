"""FinViz fundamentals — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance
import json

if len(sys.argv) < 2:
    print("Usage: python fundamentals.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
data = stock.ticker_fundament(raw=False)

# Print all key fields
for key, val in data.items():
    print(f"{key}: {val}")
