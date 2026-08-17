"""FinViz stock news — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance

if len(sys.argv) < 2:
    print("Usage: python news.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
news = stock.ticker_news()

for _, row in news.iterrows():
    print(f"{row['Date']}\t{row['Source']}\t{row['Title'].strip()}\t{row['Link'].strip()}")
