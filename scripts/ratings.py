"""FinViz analyst ratings — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance

if len(sys.argv) < 2:
    print("Usage: python ratings.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
ratings = stock.ticker_outer_ratings()

for _, row in ratings.iterrows():
    print(f"{row['Date']}\t{row['Status']}\t{row['Outer']}\t{row['Rating']}\t{row['Price']}")
