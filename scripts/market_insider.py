"""FinViz market-wide insider trading — run via hermes-venv Python."""
import sys

from finvizfinance.insider import Insider

option = sys.argv[1] if len(sys.argv) > 1 else 'latest'

df = Insider(option=option).get_insider()

for _, row in df.iterrows():
    print(f"{row['Ticker']}\t{row['Owner']}\t{row['Relationship']}\t{row['Date']}\t{row['Transaction']}\t{row['Cost']}\t{row['#Shares']}\t{row['Value ($)']}")
