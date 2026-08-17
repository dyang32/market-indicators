"""FinViz insider trading — run via hermes-venv Python."""
import sys

from finvizfinance.quote import finvizfinance

if len(sys.argv) < 2:
    print("Usage: python insider.py TICKER")
    exit(1)

ticker = sys.argv[1]
stock = finvizfinance(ticker)
insiders = stock.ticker_inside_trader()

for _, r in insiders.iterrows():
    print(f"{r['Date']}\t{r['Insider Trading']}\t{r['Relationship']}\t{r['Transaction']}\t{r['Cost']}\t{r['#Shares']}\t{r['Value ($)']}\t{r['SEC Form 4 Link']}")
