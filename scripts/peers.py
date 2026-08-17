"""FinViz peer tickers — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance

if len(sys.argv) < 2:
    print("Usage: python peers.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
peers = stock.ticker_peer()

for p in peers:
    print(p)
