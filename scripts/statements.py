"""FinViz financial statements — run via hermes-venv Python."""
import sys

from finvizfinance.quote import Statements

if len(sys.argv) < 4:
    print("Usage: python statements.py TICKER TYPE PERIOD")
    print("  TICKER: stock symbol (e.g. NVDA)")
    print("  TYPE: I (Income), B (Balance), C (Cash Flow)")
    print("  PERIOD: Q (Quarterly), A (Annual)")
    exit(1)

ticker = sys.argv[1]
stmt_type = sys.argv[2]  # I, B, C
period = sys.argv[3]      # Q, A

s = Statements()
df = s.get_statements(ticker, stmt_type, period)

print(df.to_string())
