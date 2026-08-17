---
name: finviz
description: Financial data from FinViz — individual stock fundamentals, news, insider trading, screener, and financial statements. Run via terminal with hermes-venv Python.
category: MySKILLS
---

# finviz

Financial data from FinViz.com via web scraping. Scripts live in the parent `scripts/` folder — run via hermes-venv Python.

## Scripts

| What | Script |
|---|---|---|
| Stock fundamentals | `scripts/fundamentals.py` |
| Stock news | `scripts/news.py` |
| Market news | `scripts/market_news.py` |
| Insider trading (per stock) | `scripts/insider.py` |
| Insider trading (market-wide) | `scripts/market_insider.py` |
| Analyst ratings | `scripts/ratings.py` |
| Peer tickers | `scripts/peers.py` |
| Financial statements | `scripts/statements.py` |
| Full info | `scripts/full_info.py` |
| Screener | `scripts/screener.py` |

Usage: `python scripts/SCRIPT_NAME.py [args]`

Example:
```
python scripts/fundamentals.py NVDA
python scripts/news.py NVDA
python scripts/market_news.py
python scripts/insider.py NVDA
python scripts/market_insider.py latest
python scripts/ratings.py NVDA
python scripts/peers.py NVDA
python scripts/statements.py NVDA I Q
python scripts/full_info.py NVDA
python scripts/screener.py Index="S&P 500"
```

All scripts run via hermes-venv Python from the `marketindicators/` root:
```
python scripts/fundamentals.py NVDA
python scripts/news.py NVDA
python scripts/screener.py Index="S&P 500"
python scripts/full_info.py NVDA
```

## Quick Reference

| What you want | Import | Method |
|---|---|---|
| Stock fundamentals | `finvizfinance.quote` | `ticker_fundament()` |
| Stock news | `finvizfinance.quote` | `ticker_news()` |
| Insider trading | `finvizfinance.quote` | `ticker_inside_trader()` |
| Analyst ratings | `finvizfinance.quote` | `ticker_outer_ratings()` |
| Peer tickers | `finvizfinance.quote` | `ticker_peer()` |
| ETF holders | `finvizfinance.quote` | `ticker_etf_holders()` |
| Chart pattern signals | `finvizfinance.quote` | `ticker_signal()` |
| All data at once | `finvizfinance.quote` | `ticker_full_info()` |
| Income Statement | `finvizfinance.quote` | `Statements().get_statements()` |
| Balance Sheet | `finvizfinance.quote` | `Statements().get_statements()` |
| Cash Flow | `finvizfinance.quote` | `Statements().get_statements()` |
| Market news | `finvizfinance.news` | `News().get_news()` |
| Market insider trading | `finvizfinance.insider` | `Insider(option=...)` |
| Screener table | `finvizfinance.screener.overview` | `Overview().screener_view()` |
| Screener tickers only | `finvizfinance.screener.ticker` | `Ticker().screener_view()` |
| Screener compare | `finvizfinance.screener.overview` | `Overview().compare()` |
| Chart image URL | `finvizfinance.quote` | `ticker_charts(urlonly=True)` |

---

## How to Call — Step by Step

### Every call uses this Python path:
```
python
```

### Pattern for single-ticker calls (quote module):
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('TICKER')
result = stock.METHOD_NAME()
print(result)
"
```

### Pattern for market-wide calls (news, insider):
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.news import News          # or insider, screener

instance = News()                           # or Insider(option='...')
result = instance.get_news()                # or get_insider()
print(result)
"
```

### Pattern for screener:
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(filters_dict={'Index': 'S&P 500'})
df = o.screener_view(order='Ticker', limit=20, sleep_sec=1, verbose=0)
print(df.head(10))
"
```

### Pattern for statements:
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()
df = s.get_statements('TICKER', 'I', 'Q')   # Income, Quarterly
print(df.head())
"
```

---

## ✅ TESTED & WORKING

### Methods — All 12 confirmed working (12/12 tests passed):

| # | Method | What it does |
|---|---|---|
| 1 | `ticker_fundament(raw=False)` | 80+ stats per stock |
| 2 | `ticker_news()` | 100 headlines with date/source/link |
| 3 | `ticker_inside_trader()` | Per-stock insider buys/sells |
| 4 | `ticker_outer_ratings()` | Analyst rating history |
| 5 | `ticker_peer()` | Peer tickers list |
| 6 | `ticker_etf_holders()` | ETF holders list |
| 7 | `ticker_full_info()` | All data combined |
| 8 | `ticker_charts(urlonly=True)` | Chart image URL |
| 9 | `Statements().get_statements(ticker, 'I'/'B'/'C', 'Q'/'A')` | Income, Balance, Cash Flow |
| 10 | `News().get_news()` | Market-wide news + blogs |
| 11 | `Insider(option=...).get_insider()` | Market insider trading |
| 12 | `Overview().screener_view()` | Screener table with filters |
| 13 | `Ticker().screener_view()` | Screener ticker list only |
| 14 | `Overview().compare()` | Sector/industry comparison |

### Fundamentals Metrics — All 75 confirmed working (from MAG7 live test):

**Identity**
- `Company` — full company name
- `Sector` — sector classification
- `Industry` — industry classification
- `Country` — country of HQ
- `Exchange` — exchange listing
- `Index` — indices the stock is in (e.g. S&P 500, NDX)

**Valuation**
- `P/E` — trailing P/E ratio
- `Forward P/E` — forward P/E
- `PEG` — PEG ratio
- `P/S` — price-to-sales
- `P/B` — price-to-book
- `P/C` — price-to-cash
- `P/FCF` — price-to-free cash flow
- `EV/EBITDA` — enterprise multiple
- `EV/Sales` — EV to sales
- `Market Cap` — market cap in raw dollars (use `raw=False` to get numeric)
- `Enterprise Value` — EV in raw dollars
- `Price` — current price
- `Prev Close` — previous close
- `Change %` — daily change percent
- `Target Price` — analyst consensus target

**Earnings**
- `EPS (ttm)` — trailing twelve month EPS
- `EPS next Y` — next year EPS estimate
- `EPS next Q` — next quarter EPS estimate
- `EPS this Y` — this year EPS growth %
- `EPS next Y Percentage` — next year growth % (second occurrence of EPS next Y)
- `EPS next 5Y` — 5-year EPS growth estimate
- `EPS past 3/5Y` — past 3yr and 5yr EPS growth %
- `EPS Y/Y TTM` — year-over-year EPS change
- `EPS Q/Q` — quarter-over-quarter EPS change
- `Sales past 3/5Y` — past sales growth %
- `Sales Y/Y TTM` — year-over-year sales change
- `Sales Q/Q` — quarter-over-quarter sales change
- `EPS/Sales Surpr.` — earnings/sales surprise %
- `Earnings` — next earnings date and time

**Profitability**
- `Gross Margin` — gross margin %
- `Oper. Margin` — operating margin %
- `Profit Margin` — net profit margin %
- `ROA` — return on assets
- `ROE` — return on equity
- `ROIC` — return on invested capital

**Financial Health**
- `Book/sh` — book value per share
- `Cash/sh` — cash per share
- `Debt/Eq` — debt to equity
- `LT Debt/Eq` — long-term debt to equity
- `Current Ratio` — current ratio
- `Quick Ratio` — quick ratio
- `Employees` — number of employees

**Dividends**
- `Dividend Est.` — estimated next dividend
- `Dividend TTM` — trailing twelve month dividend
- `Dividend Ex-Date` — ex-dividend date
- `Dividend Gr. 3/5Y` — 3yr and 5yr dividend growth %
- `Payout` — payout ratio

**Ownership**
- `Insider Own` — insider ownership %
- `Insider Trans` — insider transaction %
- `Inst Own` — institutional ownership %
- `Inst Trans` — institutional transaction %
- `Option/Short` — optionable and shortable status

**Price Action / Technicals**
- `SMA20` — price vs 20-day SMA %
- `SMA50` — price vs 50-day SMA %
- `SMA200` — price vs 200-day SMA %
- `RSI (14)` — 14-day RSI
- `Beta` — beta vs market
- `ATR (14)` — 14-day average true range
- `Volatility W` — weekly volatility
- `Volatility M` — monthly volatility
- `52W High` — 52-week high (includes current % below)
- `52W Low` — 52-week low (includes current % above)

**Performance**
- `Perf Week` — performance this week %
- `Perf Month` — performance this month %
- `Perf Quarter` — performance this quarter %
- `Perf Half Y` — performance last half year %
- `Perf YTD` — performance year to date %
- `Perf Year` — performance last 12 months %
- `Perf 3Y` — 3-year performance %
- `Perf 5Y` — 5-year performance %
- `Perf 10Y` — 10-year performance %

**Volume / Liquidity**
- `Volume` — today's volume
- `Avg Volume` — average daily volume
- `Rel Volume` — relative volume vs average
- `Short Float` — short interest as % of float
- `Short Ratio` — days to cover
- `Short Interest` — total shares sold short
- `Shs Outstand` — shares outstanding
- `Shs Float` — shares in float

**Analyst Sentiment**
- `Recom` — analyst recommendation (1=strong buy, 5=strong sell)

**Revenue / Income**
- `Income` — net income (raw dollars)
- `Sales` — total revenue (raw dollars)

---

## ❌ NOT TESTED

The following are part of the library but have NOT been confirmed working. Use at your own risk — Finviz HTML changes may have broken them.

### Fundamentals metrics not yet verified:
- `IPO` — IPO date field
- `Trades` — intraday trade count (returned empty in MAG7 test)

### Methods not yet tested:
- `ticker_signal()` — chart pattern scanner (fires 34+ requests, slow)
- Any `finvizfinance.screener.technical` module methods
- Any `finvizfinance.screener.forecast` module methods

---

## Step-by-Step: Every Capability

### 1. Stock Fundamentals — `ticker_fundament()`

**What it returns:** Dict of 75+ confirmed working stats.

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('NVDA')
fundament = stock.ticker_fundament(raw=False)

# raw=False  → numeric values (float/int)
# raw=True   → string values with K/M/B suffixes

for key in ['Company', 'Sector', 'Industry', 'Country', 'P/E', 'EPS (ttm)',
            'Forward P/E', 'Market Cap', 'Price', 'RSI (14)', 'Beta',
            'Volume', 'Perf Week', 'Perf YTD', 'ROE', 'Gross Margin',
            'Profit Margin', '52W High', '52W Low', 'Short Float', 'Recom']:
    print(f'{key}: {fundament.get(key, \"N/A\")}')
"
```

**Real output (NVDA):**
```
Company: NVIDIA Corp
Sector: Technology
Industry: Semiconductors
Country: USA
P/E: 34.48
EPS (ttm): 6.53
Forward P/E: 17.68
Market Cap: 5448870000000.0
Price: 225.16
RSI (14): 63.03
Beta: 2.22
Volume: 75680870.0
ROE: 1.1429
Gross Margin: 0.7415
```

---

### 2. Stock News — `ticker_news()`

**What it returns:** DataFrame. Columns: `Date`, `Title`, `Link`, `Source`. Up to 100 headlines.

**Columns:**
- `Date` — timestamp of the article (e.g. `2026-08-14 15:28:00`)
- `Title` — full article headline
- `Link` — **full clickable URL to the original article** on the source site
- `Source` — which outlet published it

**All links go to the actual article** — Finviz wraps external URLs through Yahoo Finance's redirect gateway (go.yahoo.com), so every link is a real working URL to the full story on the original publisher's site.

**Sources covered:** Reuters, Barrons, Stocktwits, Benzinga, Yahoo Finance, GuruFocus, Moneywise, MarketWatch, Bloomberg, CNBC, WSJ, Fortune, and more.

**What you CAN do with news:**
- ✅ Get up to 100 headlines for any ticker
- ✅ Get the full clickable link to each article
- ✅ Filter by ticker — news is tied to a specific stock
- ✅ Pull news from multiple tickers and combine into one feed
- ✅ Sort by date (newest first) and filter by source
- ✅ Build a news watchlist in Google Sheets with Date / Source / Title / Link

**What you CANNOT do with news:**
- ❌ **Topic/keyword search** — can't say "give me news about the Fed" or "oil prices" without knowing the ticker
- ❌ **Source filter in the library** — no way to pull only Reuters or exclude Stocktwits
- ❌ **Date range filter** — no way to get only the last 24 hours vs last 30 days
- ❌ **Broad subject search** — market-wide news without specifying tickers (use `News()` for that)
- ❌ **Sentiment scoring** — returns raw headlines only, no AI sentiment analysis

**Workaround for subject-based news (e.g. "AI news"):**
Since finvizfinance is a stock tool, not a news aggregator, the workaround is to pull per-ticker news from stocks in that space and aggregate:

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance
import pandas as pd

ai_tickers = ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMD', 'AVGO', 'PLTR']
rows = []
for t in ai_tickers:
    try:
        news = finvizfinance(t).ticker_news()
        for _, r in news.iterrows():
            r = r.to_dict()
            r['Ticker'] = t
            rows.append(r)
    except: pass

df = pd.DataFrame(rows)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date', ascending=False)
for _, r in df.head(10).iterrows():
    print(f\"{r['Date'].strftime('%Y-%m-%d')} | {r['Ticker']} | {r['Source']} | {r['Title'].strip()}\")
"
```

**Command — show headlines with links for a single ticker:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('PLTR')
news = stock.ticker_news()

print(f'Total headlines: {len(news)}')
print()
for _, row in news.head(10).iterrows():
    print(f\"{row['Date']} | {row['Source']}\")
    print(f\"  {row['Title'].strip()}\")
    print(f\"  {row['Link'].strip()}\")
    print()
"
```

**Command — tab-delimited for Google Sheets (Date / Source / Title / Link):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('PLTR')
news = stock.ticker_news()

for _, row in news.iterrows():
    print(f\"{row['Date']}\t{row['Source']}\t{row['Title'].strip()}\t{row['Link'].strip()}\")
"
```
Paste output into Google Sheets → Data → Split text to columns (Tab delimiter).

**Command — news from multiple tickers:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

tickers = ['PLTR', 'NVDA', 'TSLA']
for t in tickers:
    stock = finvizfinance(t)
    news = stock.ticker_news()
    print(f'=== {t} ({len(news)} headlines) ===')
    for _, row in news.head(3).iterrows():
        print(f\"  {row['Date']} | {row['Source']} | {row['Title'].strip()}\")
    print()
"
```

### 2b. Market News — `News().get_news()`

Returns two feeds from Finviz covering the broad market. Best for a morning briefing on what's moving the market right now.

**What it returns:** Dict with two DataFrames:
- `news` — 90 rows of market headlines
- `blogs` — 90 rows of blog posts

**Columns:** `Date`, `Title`, `Link`, `Source`

**What it covers:**
- Fed/rates commentary
- Earnings previews and results
- Sector moves (oil, defense, consumer, tech)
- Bond market news
- Geopolitics (Iran/Hormuz, China trade)
- Individual stock catalysts

**Sources:** Bloomberg, Reuters, WSJ, MarketWatch, Fox Business, BBC, Seeking Alpha, ZeroHedge, and more.

**What you CAN do:**
- ✅ Get broad market news in one call
- ✅ Morning briefing — what moved the market today
- ✅ Spot macro themes — rates, inflation, growth
- ✅ Blog feed for contrarian/alternative perspectives

**What you CANNOT do:**
- ❌ Filter by ticker, sector, or topic
- ❌ Search by keyword
- ❌ Filter by source (can't get only Reuters, for example)
- ❌ Date range filter — gets latest ~90 items only

**Command — market headlines:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.news import News

fnews = News()
all_news = fnews.get_news()

print(f'News: {len(all_news[\"news\"])} rows | Blogs: {len(all_news[\"blogs\"])} rows')
print()
for _, row in all_news['news'].head(10).iterrows():
    print(f\"{row['Date']} | {row['Source']}\")
    print(f\"  {row['Title'].strip()}\")
    print(f\"  {row['Link'].strip()}\")
    print()
"
```

**Command — blog posts only:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.news import News

fnews = News()
all_news = fnews.get_news()

for _, row in all_news['blogs'].head(10).iterrows():
    print(f\"{row['Date']} | {row['Source']}\")
    print(f\"  {row['Title'].strip()}\")
"
```

**Command — tab-delimited for Google Sheets:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.news import News

fnews = News()
all_news = fnews.get_news()

for _, row in all_news['news'].iterrows():
    print(f\"{row['Date']}\t{row['Source']}\t{row['Title'].strip()}\t{row['Link'].strip()}\")
"
```

### 2c. Deduplicated Subject Feed

To get clean news on a specific subject, pull per-ticker, combine, and dedupe:

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance
import pandas as pd

tickers = ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMD', 'AVGO', 'PLTR']
rows = []
for t in tickers:
    try:
        news = finvizfinance(t).ticker_news()
        for _, r in news.iterrows():
            d = r.to_dict()
            d['Ticker'] = t
            rows.append(d)
    except: pass

df = pd.DataFrame(rows)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date', ascending=False).drop_duplicates(subset=['Title'])
print(f'Unique headlines: {len(df)}')
for _, r in df.head(10).iterrows():
    print(f\"{r['Date'].strftime('%Y-%m-%d %H:%M')} | {r['Ticker']} | {r['Title'].strip()}\")
"
```

### 3. Insider Trading

**finvizfinance gives you insider data in 2 ways:**

---

#### 3a. Per-Stock Insider Trading — `ticker_inside_trader()`

Tied to one ticker. Returns up to 70 of the most recent insider transactions.

**Columns:**
- `Insider Trading` — insider name
- `Relationship` — their role (CEO, CFO, Officer, Director, 10% Owner, etc.)
- `Date` — transaction date
- `Transaction` — Buy, Sale, or Proposed Sale (10b5-1 scheduled sell)
- `Cost` — price per share
- `#Shares` — shares traded
- `Value ($)` — total dollar value
- `#Shares Total` — total shares owned after transaction
- `SEC Form 4 Link` — link to the actual SEC filing

**What you CAN do:**
- ✅ See who is buying vs selling at a company
- ✅ See insider sentiment — are executives buying or selling?
- ✅ Get SEC Form 4 links to verify the filing yourself
- ✅ Spot 10b5-1 planned sells (Proposed Sale) vs voluntary buys/sells
- ✅ See relationship/role to understand the insider's position

**What you CANNOT do:**
- ❌ Get historical insider data beyond ~70 recent rows
- ❌ Get aggregate insider buying ratio (sum it yourself)
- ❌ Filter by transaction size, role, or date range

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('SOFI')
insiders = stock.ticker_inside_trader()

print(f'Total rows: {len(insiders)}')
print(insiders[['Insider Trading', 'Relationship', 'Date', 'Transaction', 'Cost', '#Shares', 'Value (\$)']].head(15).to_string())
"
```

**Command — tab-delimited for Google Sheets:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('SOFI')
insiders = stock.ticker_inside_trader()

for _, r in insiders.iterrows():
    print(f\"{r['Date']}\t{r['Insider Trading']}\t{r['Relationship']}\t{r['Transaction']}\t{r['Cost']}\t{r['#Shares']}\t{r['Value (\$)']}\t{r['SEC Form 4 Link']}\")
"
```

---

#### 3b. Market-Wide Insider Trading — `Insider(option=...)`

Scans the entire market for insider activity. 9 modes:

| Option | What it does | Typical rows |
|--------|-------------|-------------|
| `latest` | Most recent trades (buys + sells) | 200 |
| `latest buys` | Most recent buys only | 200 |
| `latest sales` | Most recent sales only | 200 |
| `top week` | Biggest trades this week | 200 |
| `top week buys` | Biggest buys this week | 186 |
| `top week sales` | Biggest sales this week | 200 |
| `top owner trade` | Largest single-owner positions | 87 |
| `top owner buys` | Largest owner buys | 12 |
| `top owner sales` | Largest owner sales | 74 |

**Columns:** `Ticker`, `Owner`, `Relationship`, `Date`, `Transaction`, `Cost`, `#Shares`, `Value ($)`, `#Shares Total`, `SEC Form 4 Link`

**What you CAN do:**
- ✅ See what insiders across the whole market are doing right now
- ✅ Find the biggest insider buys of the week
- ✅ Track what major fund managers / 10% owners are buying
- ✅ Filter by buys-only or sells-only

**What you CANNOT do:**
- ❌ Filter by sector, market cap, or index
- ❌ Get historical data — only current/recent
- ❌ Aggregate insider sentiment by sector

**Command — top insider buys this week:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.insider import Insider

df = Insider(option='top owner buys').get_insider()
print(f'Top owner buys — {len(df)} transactions')
print(df[['Ticker', 'Owner', 'Relationship', 'Date', 'Transaction', '#Shares', 'Value (\$)']].head(15).to_string())
"
```

**Command — top insider sales this week:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.insider import Insider

df = Insider(option='top week sales').get_insider()
print(f'Top sales this week — {len(df)} transactions')
print(df[['Ticker', 'Owner', 'Relationship', 'Date', 'Transaction', '#Shares', 'Value (\$)']].head(15).to_string())
"
```

**Command — scan all modes and compare:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.insider import Insider

options = ['latest', 'latest buys', 'latest sales', 'top week', 'top week buys', 'top week sales', 'top owner trade', 'top owner buys', 'top owner sales']
for opt in options:
    try:
        df = Insider(option=opt).get_insider()
        buys = (df['Transaction'] == 'Buy').sum() if 'Transaction' in df.columns else 0
        sales = (df['Transaction'] == 'Sale').sum() if 'Transaction' in df.columns else 0
        tickers = df['Ticker'].unique()[:3] if 'Ticker' in df.columns else []
        print(f'{opt:<20} -> {len(df):3d} rows | buys: {buys:3d} | sales: {sales:3d} | sample: {tickers}')
    except Exception as e:
        print(f'{opt:<20} -> ERROR: {e}')
"
```

---

**Command — full latest output with breakdown:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.insider import Insider

df = Insider(option='latest').get_insider()
buys = df[df['Transaction'] == 'Buy']
sells = df[df['Transaction'] == 'Sale']

print(f'Total: {len(df)} | Buys: {len(buys)} | Sales: {len(sells)}')
print()
print('TOP 5 BUYS BY VALUE:')
for _, r in buys.sort_values('Value (\$)', ascending=False).head(5).iterrows():
    val = f'\${r[\"Value (\$)\"]:,.0f}' if r[\"Value (\$)\"] > 0 else 'N/A'
    print(f'{r[\"Ticker\"]:<8} {r[\"Owner\"]:<30} {r[\"Date\"]:<12} {r[\"#Shares\"]:>10,.0f}  {val}')
print()
print('TOP 5 SALES BY VALUE:')
for _, r in sells.sort_values('Value (\$)', ascending=False).head(5).iterrows():
    val = f'\${r[\"Value (\$)\"]:,.0f}' if r[\"Value (\$)\"] > 0 else 'N/A'
    print(f'{r[\"Ticker\"]:<8} {r[\"Owner\"]:<30} {r[\"Date\"]:<12} {r[\"#Shares\"]:>10,.0f}  {val}')
print()
print('BREAKDOWN:')
print(df['Transaction'].value_counts().to_string())
"
```

---

### 4. Analyst Ratings History — `ticker_outer_ratings()`
**What it returns:** DataFrame. Columns: Date, Status, Outer, Rating, Price Target.

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('NVDA')
ratings = stock.ticker_outer_ratings()

print(ratings.head(10).to_string())
"
```

---

### 5. Peer Tickers — `ticker_peer()`

Returns the 10 stocks Finviz considers competitors or closely related companies.

**What it returns:** List of ticker strings (e.g. `['AMD', 'AVGO', 'TSM', ...]`)

**What you CAN do:**
- ✅ Get 10 direct competitors for any stock
- ✅ Build a sector/similar-company watchlist in one call
- ✅ Cross-compare fundamentals — is this stock cheaper/more profitable than its peers?
- ✅ Combine with `ticker_fundament()` to get peers + fundamentals for all at once

**What you CANNOT do:**
- ❌ Know WHY they are peers (no explanation of the relationship)
- ❌ Filter by sector, market cap, or index membership
- ❌ Get historical peer data
- ❌ Know how "related" each peer is (equal weight — 10 equal peers)

**Example — OTLK peers (micro-cap biotech):**
```
OTLK: XLO, GLSI, INDP, TARA, PALI, PRLD, RNTX, RZLT, TELO, RADX
```
All micro-cap biotech/pharma companies.

**Example — AAPL peers (big tech):**
```
AAPL: MSFT, GOOG, META, AMZN, NVDA, AVGO, TSM, SONY, DELL, HPQ
```

**Example — SOFI peers (fintech):**
```
SOFI: SYF, AFRM, PYPL, COF, UPST, HOOD, AXP, NU, XYZ, CASH
```

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('NVDA')
peers = stock.ticker_peer()

print('NVDA peers:', peers)
"
```

**Command — peers + key fundamentals for comparison:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

ticker = 'NVDA'
stock = finvizfinance(ticker)
peers = stock.ticker_peer()

print(f'{ticker} peers: {peers}')
print()
print(f'{'Ticker':<8} {'Price':>8} {'P/E':>8} {'Mkt Cap':>10} {'RSI':>6}')
print('-' * 46)
all_tickers = [ticker] + peers
for t in all_tickers:
    try:
        s = finvizfinance(t)
        f = s.ticker_fundament(raw=False)
        price = f.get('Price', 'N/A')
        pe = f.get('P/E', 'N/A')
        mktcap = f.get('Market Cap', 'N/A')
        rsi = f.get('RSI (14)', 'N/A')
        if isinstance(mktcap, float):
            mktcap = f'\${mktcap/1e9:.1f}B'
        print(f'{t:<8} {str(price):>8} {str(pe):>8} {str(mktcap):>10} {str(rsi):>6}')
    except: pass
"
```

---

### 6. ETF Holders — `ticker_etf_holders()`

Returns the ETFs that hold this stock. Finviz caps it at 10 ETFs.

**What it returns:** List of ETF ticker strings (e.g. `['VTI', 'VOO', 'IVV', 'SPY', ...]`)

**What you CAN do:**
- ✅ See which ETFs own a stock (institutional support via index/sector funds)
- ✅ Identify if a stock is heavily indexed vs actively managed
- ✅ Track sector ETF exposure — e.g. NVDA in VGT/XLK/SMH = big tech chip exposure
- ✅ Cross-compare: is this stock in more ETFs than its peers?

**What you CANNOT do:**
- ❌ Know HOW MUCH of the ETF is that stock (weight %)
- ❌ See all ETFs — capped at 10 by Finviz
- ❌ Get historical holding changes
- ❌ See total shares/value held across all ETFs combined

**Example — NVDA ETF holders:**
```
['VTI', 'VOO', 'IVV', 'SPY', 'VUG', 'QQQ', 'VGT', 'IWF', 'XLK', 'SMH']
```
- Broad market: VTI, VOO, IVV, SPY, QQQ
- Sector: VGT, XLK, SMH (tech/chip focused)
- Other: VUG, IWF (growth)

**Example — SOFI ETF holders:**
```
['VTI', 'VB', 'VBK', 'VXF', 'IWR', 'SCHG', 'IWD', 'ARKE', 'ARKK', 'VFH']
```
All fintech/financial sector ETFs — SOFI has concentrated fintech index exposure.

**Example — OTLK ETF holders:**
```
['VTI', 'VXF']
```
Only 2 ETFs — micro-cap biotech has very limited index coverage.

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('NVDA')
etfs = stock.ticker_etf_holders()

print('NVDA held by:', len(etfs), 'ETFs')
for e in etfs:
    print(f'  {e}')
"
```

**Command — compare ETF exposure across tickers:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

tickers = ['NVDA', 'AAPL', 'SOFI', 'META']

for t in tickers:
    stock = finvizfinance(t)
    etfs = stock.ticker_etf_holders()
    broad = [e for e in etfs if e in ['VOO','SPY','IVV','VTI','QQQ','VUG','IWF']]
    sector = [e for e in etfs if e in ['VGT','XLK','SMH','XLV','XLF','ARKK','ARKE']]
    print(f'{t:<6} total:{len(etfs):2d} | broad:{broad} | sector:{sector}')
"
```




---

### 7. Full Info in One Call - `ticker_full_info()`

Returns fundamentals + ratings + news + insider trades all in one call.

**Python path:** `finvizfinance.quote.finvizfinance.ticker_full_info()`

**Returns a dict with 4 keys:**
| Key | Content | Rows |
|-----|---------|-----:|
| `fundament` | 75+ metrics | dict |
| `ratings_outer` | Analyst ratings history | 20 |
| `news` | Recent headlines | 100 |
| `inside trader` | Recent insider trades | 100 |

**What you CAN do:**
- Get everything at once - useful for a quick overview

**What you CANNOT do:**
- No peer tickers (separate `ticker_peer()`)
- No ETF holders (separate `ticker_etf_holders()`)
- No financial statements (separate `Statements()`)

**Output example:**

AAPL FULL INFO OUTPUT
================================================================================

FUNDAMENTALS
Price: 305.93
Market Cap: 4464.80B
P/E: 35.07
Forward P/E: 32.13
EPS TTM: 8.72
EPS Next Y: 9.52
PEG: 2.60
Gross Margin: 48.65%
Net Margin: 27.62%
ROE: 148.75%
ROIC: 72.08%
RSI: 43.67
Beta: 1.07
52W High: 344.57 (-11.21%)
52W Low: 223.78 (+36.71%)
Perf YTD: 12.53%
Perf Year: 31.42%
Perf 3Y: 70.47%
Avg Volume: 56.27M
Inst Own: 67.76%
Insider Own: 0.13%
Recom: 2.09
Earnings: Jul 30 AMC
Dividend: 1.06 (0.35%)

NEWS (top 5):
Aug 16 - Investing.com - Street Calls of the Week
Aug 16 - Money Digest - This Boring Stock Has Nearly Doubled The Nasdaq's Returns Over 5 Years
Aug 16 - Investing.com - 5 big analyst AI moves: Bullish on memory names; Apple and Cisco downgraded
Aug 15 - Bloomberg - AI Chipflation Washes Ashore in the UK Economy
Aug 15 - Fortune - Tariff refunds are juicing corporate profits and GDP as more tailwinds converge to propel growth to a blistering 4.3% pace

INSIDER TRADES (top 5):
Aug 11 - [Name] - Sale - $442,852 (SVP GC and Secretary)
Aug 11 - JENNIFER NEWSTEAD - Proposed Sale - $2,660,900 (Officer)
Jun 16 - Borders Ben - Sale - $34,236 (Principal Accounting Officer)
May 27 - LEVINSON ARTHUR D - Sale - $15,551,000 (Director)
May 27 - LEVINSON ARTHUR D - Proposed Sale - $15,551,085 (Director)

ANALYST RATINGS (all 20):
Aug 10 - Jefferies - Hold to Underperform - $263.66
Aug 04 - DZ Bank - Buy to Hold - $310
Aug 04 - China Renaissance - Buy to Hold - $280
Jul 31 - Wells Fargo - Overweight - $310 to $350
Jul 31 - TD Cowen - Buy - $350 to $400
Jul 31 - Morgan Stanley - Overweight - $364 to $360
Jul 31 - JP Morgan - Overweight - $345 to $340
Jul 31 - Goldman - Buy - $370 to $360
Jul 31 - Barclays - Underweight - $253 to $245
Jul 24 - Robert W. Baird - Outperform - $310 to $330
Jul 23 - Morgan Stanley - Overweight - $360 to $364
Jul 17 - HSBC Securities - Hold to Buy - $366
Jul 14 - KeyBanc Capital Markets - Sector Weight to Underweight - $250
Jul 13 - Citigroup - Buy - $315 to $365
May 26 - BofA Securities - Buy - $330 to $380
May 01 - Monness Crespi & Hardt - Buy - $315 to $335
Apr 28 - UBS - Neutral - $280 to $287
Apr 17 - BNP Paribas Exane - Neutral to Outperform
Apr 14 - BofA Securities - Buy - $320 to $325
Mar 23 - BofA Securities - Buy - $325 to $320

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance
d = finvizfinance('AAPL').ticker_full_info()
f = d['fundament']; n = d['news']; i = d['inside trader']; r = d['ratings_outer']
print('AAPL FULL INFO OUTPUT')
print('FUNDAMENTALS')
print('Price:', f['Price'], '| Market Cap:', f['Market Cap'], '| P/E:', f['P/E'], '| Fwd P/E:', f['Forward P/E'])
print('EPS TTM:', f['EPS (ttm)'], '| EPS Next Y:', f['EPS next Y'], '| PEG:', f['PEG'])
print('Gross Margin:', f['Gross Margin'], '| Net Margin:', f['Profit Margin'], '| ROE:', f['ROE'], '| ROIC:', f['ROIC'])
print('RSI:', f['RSI (14)'], '| Beta:', f['Beta'], '| 52W High:', f['52W High'], '| 52W Low:', f['52W Low'])
print('Perf YTD:', f['Perf YTD'], '| Perf Year:', f['Perf Year'], '| Perf 3Y:', f['Perf 3Y'])
print('Avg Vol:', f['Avg Volume'], '| Inst Own:', f['Inst Own'], '| Insider Own:', f['Insider Own'])
print('Recom:', f['Recom'], '| Earnings:', f['Earnings'], '| Dividend:', f['Dividend TTM'])
print()
print('NEWS (top 5):')
for _, row in n.head(5).iterrows():
    t = row['Title'].replace(chr(10),' ').strip()
    print(str(row['Date'])[:10], '-', row['Source'], '-', t[:80])
print()
print('INSIDER TRADES (top 5):')
for _, row in i.head(5).iterrows():
    val = row['Value ($)'] if row['Value ($)'] and row['Value ($)'] != 'N/A' else '0'
    print(str(row['Date'])[:10], '-', row['Insider Trading'], '-', row['Transaction'], '- $', float(val), '(', row['Relationship'], ')')
print()
print('ANALYST RATINGS (all 20):')
for _, row in r.iterrows():
    print(str(row['Date'])[:10], '-', row['Outer'], '-', row['Rating'], '-', row['Price'])
"
"
```

---

---

### 8. Chart Image URL — `ticker_charts()`

Downloads a stock chart as a JPG image and returns the finviz.com URL.

**Python path:** `finvizfinance.quote.finvizfinance.ticker_charts()`

**Important:** Output directory must already exist before calling.

**What it returns:** The finviz chart URL string. Side effect: saves a `.jpg` file to `out_dir`.

**URL structure:** `https://finviz.com/chart.ashx?t=NVDA&ty=c&ta=1&p=d`

**What you CAN do:**
- ✅ Download charts for any ticker as JPG (~20-30KB)
- ✅ Print the URL to view in browser
- ✅ Use the saved JPG with vision analysis tools

**What you CANNOT do:**
- ❌ No timeframe control — always daily chart
- ❌ No chart type options — always candlestick with default indicators
- ❌ No intraday charts

**Command — save to outputs folder:**
```
hermes-venv/Scripts/python.exe -c "
import os
os.makedirs('./outputs', exist_ok=True)

from finvizfinance.quote import finvizfinance

for ticker in ['NVDA', 'AAPL']:
    stock = finvizfinance(ticker)
    chart = stock.ticker_charts(out_dir='./outputs/')
    print(f'{ticker}: {chart}')
"
```

**Command — URL only (no download):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

stock = finvizfinance('NVDA')
url = stock.ticker_charts(urlonly=True)
print('Chart URL:', url)
"
```

---

### 9. Financial Statements — `Statements()`

Returns the full Income Statement, Balance Sheet, and Cash Flow — annual or quarterly.

**Python path:** `finvizfinance.quote.Statements`

**Method:**
```python
from finvizfinance.quote import Statements

s = Statements()
df = s.get_statements('NVDA', statement='I', timeframe='A')  # Annual Income
df = s.get_statements('NVDA', statement='B', timeframe='A')  # Annual Balance Sheet
df = s.get_statements('NVDA', statement='C', timeframe='Q')  # Quarterly Cash Flow
```

**Parameters:**
- `statement='I'` → Income Statement
- `statement='B'` → Balance Sheet
- `statement='C'` → Cash Flow
- `timeframe='Q'` → Quarterly (12 periods)
- `timeframe='A'` → Annual (9 periods + TTM where available)

---

**What it returns:**

| Statement | Rows | Periods | Key data |
|-----------|-----:|--------:|---------|
| Income | 31 | 9 annual + TTM, or 12 quarterly | Revenue, Gross Profit, R&D, SG&A, Operating Income, Net Income, EPS (3 types), EBITDA, Margins, P/E, P/S, P/B |
| Balance Sheet | 40 | 9 annual (no TTM) | Cash, Receivables, Inventories, PP&E, Investments, Intangibles, Total Assets, Debt, Payables, Equity, Book Value, Ratios |
| Cash Flow | 38 | 9 annual + TTM, or 12 quarterly | Net Income, D&A, Working Capital, Operating CF, CapEx, Acquisitions, Investing CF, Buybacks, Dividends, Financing CF, Free Cash Flow |

**Note:** Columns use numeric headers (0, 1, 2...) — row labels are the actual line items. Use `df.loc['Total Revenue']` to get a row.

---

**What you CAN do:**
- ✅ Full income statement, balance sheet, cash flow
- ✅ Annual (9 years) or quarterly (12 quarters)
- ✅ Derived metrics already calculated: Gross/Operating/Net Margin, ROA/ROE/ROIC, P/E, P/S, P/B, Free Cash Flow
- ✅ All three statements together give a complete financial picture
- ✅ Compare across time periods to spot trends

**What you CANNOT do:**
- ❌ Balance Sheet has no TTM — only annual data
- ❌ Quarterly Balance Sheet not available (only annual)
- ❌ Real-time data — web-scrape, same lag as finviz.com
- ❌ Cash Flow has no annual column headers for the first column — use row labels for row lookup

---

**Command — Income Statement (quarterly, key rows):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()
df = s.get_statements('NVDA', statement='I', timeframe='Q')

key_rows = ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EPS (Diluted)', 'Operating Margin', 'Net Margin']
available = [r for r in key_rows if r in df.index]
print(df.loc[available].to_string())
"
```

**Command — Balance Sheet (annual):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()
df = s.get_statements('NVDA', statement='B', timeframe='A')

key_rows = ['Total Assets', 'Total Current Assets', 'Cash & Short Term Investments',
            'Net Property, Plant & Equipment', 'Total Liabilities', 'Long Term Debt',
            'Total Shareholders Equity', 'Book Value Per Share', 'Current Ratio', 'Quick Ratio']
available = [r for r in key_rows if r in df.index]
print(df.loc[available].to_string())
"
```

**Command — Cash Flow (annual, key rows):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()
df = s.get_statements('NVDA', statement='C', timeframe='A')

key_rows = ['Net Income', 'Depreciation', 'Cash from Operating Activities',
            'Capital Expenditures', 'Free Cash Flow', 'Repurchase of Common Pref Stock',
            'Cash Dividends Paid', 'Net Change in Cash']
available = [r for r in key_rows if r in df.index]
print(df.loc[available].to_string())
"
```

**Command — All three statements at once:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()
for stmt, name in [('I', 'Income'), ('B', 'Balance Sheet'), ('C', 'Cash Flow')]:
    df = s.get_statements('NVDA', statement=stmt, timeframe='A')
    print(f'=== {name} === rows={len(df)} cols={len(df.columns)}')
"
```

---

### 10. Market News — `News()`

**What it returns:** Dict with `news` and `blogs` DataFrames. Columns: Date, Title, Source, Link.

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.news import News

fnews = News()
all_news = fnews.get_news()

print('News rows:', len(all_news['news']))
print('Blog rows:', len(all_news['blogs']))

for _, row in all_news['news'].head(5).iterrows():
    print(f\"{row['Date']} | {row['Source']} | {row['Title']}\")
"
```

---

### 11. Market Insider Trading — `Insider()`

**What it returns:** DataFrame of top insider trades across the whole market.

**Options for `option=`:**
- `latest` — most recent trades
- `latest buys` — only buys
- `latest sales` — only sales
- `top week` — biggest trades this week
- `top week buys` / `top week sales`
- `top owner trade` — largest single-owner positions
- `top owner buys` / `top owner sales`

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.insider import Insider

df = Insider(option='top owner buys').get_insider()
print('Top owner buys — shape:', df.shape)
print(df[['Ticker', 'Owner', 'Relationship', 'Date', 'Transaction', '#Shares', 'Value (\$)']].head(10).to_string())
"
```

---

### 12. Screener — Table View — `Overview()`

Returns a DataFrame of stocks matching your filters. 67 filter categories and 33 signal presets.

**What it returns:** DataFrame. Columns: `Ticker`, `Company`, `Sector`, `Industry`, `Country`, `Market Cap`, `P/E`, `Price`, `Change %`, `Volume`.

**Python path:** `finvizfinance.screener.overview.Overview`

---

**Method signature:**
```python
overview = Overview()
overview.set_filter(signal=None, filters_dict={}, ticker='')
df = overview.screener_view(order='Ticker', limit=100000, ascend=True, sleep_sec=1, verbose=1, columns=None)
```

---

**What you CAN do:**
- ✅ 67 filter categories — combine ALL at once, no hard limit
- ✅ 33 signal presets — technical patterns, performance, insider activity, earnings
- ✅ Sort by any column, ascending or descending
- ✅ Combine signals AND filters together
- ✅ Use all 67 filters in one screen
- ✅ Filter by chart pattern or candlestick formation
- ✅ All 67 filters tested — 65 PASS, 2 ZERO (no market match today)

**What you CANNOT do:**
- ❌ Save/load filter presets — no built-in save feature
- ❌ More than ~10 columns in the overview table (use specific table modules for more)
- ❌ Real-time data — still web-scraped, same rate limits as finviz.com

---

**67 FILTER CATEGORIES — ALL TESTED:**

*Identity:*
```
Exchange:        Any, AMEX, NASDAQ, NYSE
Index:           Any, S&P 500, NASDAQ 100, DJIA, RUSSELL 2000
Sector:          Basic Materials, Communication Services, Consumer Cyclical,
                 Consumer Defensive, Energy, Financial, Healthcare, Industrials,
                 Real Estate, Technology, Utilities
Industry:        151 options (Semiconductors, Software, Biotech, Airlines, etc.)
Country:         USA, Foreign (ex-USA), Asia, Europe, etc.
```

*Valuation:*
```
P/E:             Low (<15), Profitable (>0), High (>50), Under 5, Under 10,
                 Under 15, Under 20, Under 25, Under 30, Over 5, Over 10, etc.
Forward P/E:     Same options as P/E
PEG:             Low (<1), High (>2), Under 1, Under 2, etc.
P/S:             Low (<1), High (>10), Under 1, Under 2, Under 3, etc.
P/B:             Low (<1), High (>5), Under 1, Under 2, Under 3, etc.
Price/Cash:      Low (<3), High (>50), Under 1, Under 2, Under 3, etc.
Price/Free Cash Flow: Low (<15), High (>50), Under 5, Under 10, etc.
```

*Earnings Growth:*
```
EPS growththis year:    Negative (<0%), Positive (>0%), Positive Low (0-10%),
                        High (>25%), Under 5%, Under 10%, Over 5%, Over 10%, etc.
EPS growthnext year:    Same options
EPS growthpast 5 years: Same options
EPS growthnext 5 years: Same options
EPS growth ttm:         Same options
EPS growthqtr over qtr: Same options
Sales growthqtr over qtr: Same options
Sales growthpast 5 years: Same options
```

*Profitability:*
```
Return on Assets:  Positive (>0%), Negative (<0%), Very Positive (>15%), etc.
Return on Equity:  Positive (>0%), Very Positive (>30%), etc.
Return on Investment: Positive (>0%), Very Positive (>25%), etc.
Gross Margin:     Positive (>0%), Negative (<0%), High (>50%), Under 90%, etc.
Operating Margin: Same options
Net Profit Margin: Same options
```

*Financial Health:*
```
Current Ratio:     High (>3), Low (<1), Under 1, Under 0.5
Quick Ratio:      High (>3), Low (<0.5), Under 1, Under 0.5
LT Debt/Equity:   High (>0.5), Low (<0.1), Under 1, Under 0.9, etc.
Debt/Equity:      Same options
```

*Other:*
```
Dividend Yield:    None (0%), Positive (>0%), High (>5%), Very High (>10%), etc.
Payout Ratio:     None (0%), Positive (>0%), Low (<20%), High (>50%), etc.
Beta:             Under 0, Under 0.5, Under 1, Under 1.5, Over 1.5, etc.
Average True Range: Over 0.25, Over 0.5, Over 0.75, Over 1, etc.
IPO Date:         Today, Yesterday, In the last week, In the last month,
                  In the last year, etc.
Shares Outstanding: Under 1M, Under 5M, Under 10M, Over 100M, etc.
Float:             Same options
Net Expense Ratio: Under 0.1%, Under 0.2%, Under 0.3%, etc.
```

*Ownership:*
```
InsiderOwnership:        Low (<5%), High (>30%), Very High (>50%), etc.
InsiderTransactions:      Very Negative (<20%), Negative (<0%), Positive (>0%),
                          Very Positive (>20%), etc.
InstitutionalOwnership:  Low (<5%), High (>90%), Under 90%, etc.
InstitutionalTransactions: Same options
```

*Short Interest / Analyst:*
```
Float Short:       Low (<5%), High (>20%), Under 5%, Under 10%, Under 20%, etc.
Analyst Recom.:    Strong Buy (1), Buy or better, Buy, Hold or better,
                  Hold, Sell, Strong Sell (5)
Option/Short:      Any, Optionable, Shortable, Optionable and shortable
```

*Performance / Technicals:*
```
Performance:        Today Up, Today Down, Today -15%, Today -10%, etc.
Performance 2:      Week Up, Week Down, Month Up, Month Down, etc.
Volatility:         Week - Over 3%, Week - Over 4%, Week - Over 5%, etc.
RSI (14):          Overbought (90), Overbought (80), Overbought (70),
                   Oversold (40), Oversold (30), Oversold (20), etc.
Gap:               Up, Up 0%, Up 1%, Up 2%, Down, etc.
20-Day SMA:        Price above SMA20, Price below SMA20, Price 10% below SMA20, etc.
50-Day SMA:        Same options
200-Day SMA:       Same options
20-Day High/Low:   New High, New Low, 5% or more below High, etc.
50-Day High/Low:   Same options
52-Week High/Low:  New High, New Low, 5% or more below High, etc.
```

*Chart Patterns (Pattern):*
```
Horizontal S/R, Horizontal S/R (Strong), TL Resistance, TL Resistance (Strong),
TL Support, TL Support (Strong), Wedge Up, Wedge Down, Wedge,
Triangle Ascending, Triangle Descending, Channel Up, Channel Down, Channel,
Double Top, Double Bottom, Multiple Top, Multiple Bottom,
Head & Shoulders, Head & Shoulders Inverse
```

*Candlestick (Candlestick):*
```
Long Lower Shadow, Long Upper Shadow, Hammer, Inverted Hammer,
Doji, Dragonfly Doji, Gravestone Doji, Engulfing Bullish,
Engulfing Bearish, Morning Star, Evening Star
```

*Volume:*
```
Average Volume:    Under 50K, Under 100K, Under 500K, Over 5Mln, etc.
Relative Volume:   Over 10, Over 5, Over 3, Over 2, Over 1.5, etc.
Current Volume:    Same options as Average Volume
```

*Price / Target:*
```
Price:             Under $1, Under $2, Under $3, Over $20, Over $50, etc.
Target Price:      50% Above Price, 40% Above, 30% Above, 20% Above, etc.
Earnings Date:     Today, Today Before Market Open, Today After Market Close,
                  Tomorrow, This Week, Next Week, etc.
```

---

**33 SIGNAL PRESETS — ALL TESTED (31 PASS, 2 ZERO today — no earnings scheduled):**

Performance: `Top Gainers`, `Top Losers`, `New High`, `New Low`, `Most Volatile`, `Most Active`, `Unusual Volume`
RSI: `Overbought`, `Oversold`
Analyst: `Downgrades`, `Upgrades`
Earnings: `Earnings Before`, `Earnings After`
Insider: `Recent Insider Buying`, `Recent Insider Selling`
News: `Major News`
Patterns: `Horizontal S/R`, `TL Resistance`, `TL Support`, `Wedge Up`, `Wedge Down`, `Triangle Ascending`, `Triangle Descending`, `Wedge`, `Channel Up`, `Channel Down`, `Channel`, `Double Top`, `Double Bottom`, `Multiple Top`, `Multiple Bottom`, `Head & Shoulders`, `Head & Shoulders Inverse`

---

**Command — Top Gainers:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(signal='Top Gainers')
df = o.screener_view(order='Market Cap', limit=20, ascend=False, sleep_sec=1, verbose=0)
print(f'Results: {len(df)}')
print(df[['Ticker', 'Company', 'Sector', 'Price', 'Change %', 'Volume']].to_string())
"
```

**Command — S&P 500, strong EPS growth, high volume, low short interest:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(
    filters_dict={
        'Index': 'S&P 500',
        'EPS growthqtr over qtr': 'Over 20%',
        'EPS growththis year': 'Positive (>0%)',
        'Relative Volume': 'Over 1.5',
        'Float Short': 'Under 20%',
    }
)
df = o.screener_view(order='Market Cap', limit=20, ascend=False, sleep_sec=1, verbose=0)
print(f'Stocks: {len(df)}')
print(df[['Ticker', 'Company', 'Sector', 'Price', 'P/E', 'Change %']].to_string())
"
```

**Command — Short squeeze candidates:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(
    signal='Unusual Volume',
    filters_dict={
        'Float Short': 'Over 20%',
        'Price': 'Over \$5',
    }
)
df = o.screener_view(order='Volume', limit=20, ascend=False, sleep_sec=1, verbose=0)
print(f'Short squeeze candidates: {len(df)}')
print(df[['Ticker', 'Company', 'Sector', 'Price', 'Volume', 'Float Short']].to_string())
"
```

**Command — Chart patterns:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(
    signal='Double Bottom',
    filters_dict={'Sector': 'Technology'}
)
df = o.screener_view(order='Market Cap', limit=20, ascend=False, sleep_sec=1, verbose=0)
print(f'Double Bottom (Tech): {len(df)} stocks')
print(df[['Ticker', 'Company', 'Price', 'P/E', 'Change %']].to_string())
"
```

**Command — Test all 67 filters (quick):**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview
from finvizfinance.screener import base

fd = base.filter_dict
for cat, info in fd.items():
    opts = list(info['option'].keys())
    test_opt = opts[1] if len(opts) > 1 else opts[0]
    try:
        o = Overview()
        o.set_filter(filters_dict={cat: test_opt})
        df = o.screener_view(limit=1, verbose=0)
        status = 'OK' if df is not None and len(df) > 0 else 'ZERO'
    except Exception as e:
        status = 'ERR'
    print(f'{status}  {cat}')
"
```

---

### 13. Screener — Ticker List Only — `Ticker()`

**What it returns:** List of ticker symbols (no full table, faster).

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.ticker import Ticker

ft = Ticker()
ft.set_filter(
    signal='New High',
    filters_dict={'Sector': 'Technology'}
)
tickers = ft.screener_view(order='Ticker', limit=20, sleep_sec=1, verbose=0)
print('Tickers:', tickers)
"
```

---

### 14. Screener — Compare to Peers — `compare()`

**What it returns:** DataFrame comparing all stocks in the same sector/industry/country as a given ticker.

**Command:**
```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
df = o.compare(ticker='NVDA', compare_list=['Sector'], order='Market Cap')
print(df[['Ticker', 'Company', 'Market Cap', 'P/E', 'RSI (14)']].head(20).to_string())
"
```

---

## Practical Examples

### Example 1 — Get fundamentals for multiple tickers

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import finvizfinance

tickers = ['NVDA', 'AMD', 'AVGO', 'TSM']
for t in tickers:
    s = finvizfinance(t)
    f = s.ticker_fundament(raw=False)
    print(f\"{t}: P/E={f.get('P/E','N/A')}, EPS={f.get('EPS (ttm)','N/A')}, MktCap={f.get('Market Cap','N/A')}, RSI={f.get('RSI (14)','N/A')}\")
"
```

### Example 2 — Minervini-style growth screen (S&P 500, strong RS, positive EPS)

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(
    filters_dict={
        'Index': 'S&P 500',
        'Market Cap': 'Mega (\$200bln+)',
        'EPS': 'Positive',
        'RS (Rel Str)': 'A+ (90-100)',
        'Performance': 'Up 20% (4wk)',
        'Optionable': 'Yes',
    }
)
df = o.screener_view(order='Price', limit=30, ascend=True, sleep_sec=1, verbose=1)
print(df[['Ticker', 'Company', 'Price', 'Change %', 'Perf 4W', 'RSI']].to_string())
"
```

### Example 3 — Short squeeze candidates (unusual volume + shortable)

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.screener.overview import Overview

o = Overview()
o.set_filter(
    signal='Unusual Volume',
    filters_dict={'Shortable': 'Yes', 'Market Cap': 'Mid (\$2bln-\$10bln)'}
)
df = o.screener_view(order='Volume', limit=20, ascend=False, sleep_sec=1, verbose=1)
print(df[['Ticker', 'Price', 'Change %', 'Volume', 'Short Float']].to_string())
"
```

### Example 4 — Quarterly financials for a stock

```
hermes-venv/Scripts/python.exe -c "
from finvizfinance.quote import Statements

s = Statements()

df = s.get_statements('NVDA', 'I', 'Q')
print('NVDA Quarterly Income Statement')
print('Periods:', list(df.columns))
for idx in df.index:
    if 'Revenue' in idx or 'Net Income' in idx or 'EPS' in idx:
        print(f'{idx}: {dict(df.loc[idx])}')
"
```

---

## Library Patch Note (IMPORTANT)

Finviz changed their HTML layout in 2025. The installed finvizfinance v1.3.0 has two bugs:

**Bug 1:** `ticker_fundament()` crashes because the `quote-links` div no longer exists.
**Bug 2:** `_parse_column()` crashes on `IndexError` when `number_covert()` gets non-numeric text.

**Patches applied to:**
```
finvizfinance/quote.py
```

If you ever run `pip install --force-reinstall finvizfinance`, the patches are wiped.

**Verify patches are active:**
```
hermes-venv/Scripts/python.exe -c "from finvizfinance.quote import finvizfinance; f = finvizfinance('NVDA').ticker_fundament(raw=False); print('P/E:', f.get('P/E'), 'RSI:', f.get('RSI (14)'))"
```
Should print `P/E: 34.48 RSI: 63.03`. If it crashes, patches need re-applying.

---

## Pitfalls

1. **Rate limiting** — always use `sleep_sec=1` or higher on screener calls. Finviz free tier will soft-block on heavy scraping.
2. **Screener page limits** — Finviz returns max ~20 results per page. Set `limit` to cap rows.
3. **`ticker_signal()` is slow** — fires 34+ requests. Not yet tested.
4. **Signal + filter combo** — `set_filter(signal=..., filters_dict=...)` are AND conditions (both must match).
5. **No options data** — finvizfinance does not cover options chains or Greeks. Use `webull` or `alpaca` skills for that.
6. **`raw=True` vs `raw=False`** — `raw=True` returns string values with K/M/B suffixes. `raw=False` parses to numeric types. Default is `raw=True`.
7. **Key name gotchas:**
   - RSI is `RSI (14)` not `RSI`
   - 52W High contains both price and % below: `"236.54 -4.81%"`
   - 52W Low contains both price and % above: `"164.07 37.23%"`
   - `EPS next Y` appears twice — second occurrence is named `EPS next Y Percentage`
   - `EPS past 3/5Y` contains both 3yr and 5yr values
   - `Dividend Gr. 3/5Y` contains both values
   - `EPS Q/Q` and `EPS Y/Y TTM` contain both values
8. **Library patches** — Finviz periodically redesigns their site. If fundamentals or screener breaks, check the HTML structure first.
