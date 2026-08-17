"""FinViz screener — run via hermes-venv Python."""
import sys

from finvizfinance.screener.overview import Overview

# Optional: pass filters as command line args
# Usage: python screener.py Index=S&P 500 Sector=Technology
filters = {}
for arg in sys.argv[1:]:
    if '=' in arg:
        k, v = arg.split('=', 1)
        filters[k.strip()] = v.strip()

if not filters:
    filters = {'Index': 'S&P 500'}

o = Overview()
o.set_filter(filters_dict=filters)
df = o.screener_view(order='Ticker', limit=20, sleep_sec=1, verbose=0)

for col in df.columns:
    print('\t'.join(df.columns), file=sys.stderr)
    break

for _, row in df.iterrows():
    print('\t'.join(str(v) for v in row.values))
