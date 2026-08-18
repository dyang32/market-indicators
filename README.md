# Market Indicators

A lightweight Python toolkit for technical analysis and options research, designed as an agent skill for [Hermes Agent](https://github.com/NousResearch/Hermes) but compatible with any AI agent that can run Python scripts from the terminal.

**No API keys required** — all market data is sourced from Yahoo Finance (`yfinance`) and FinViz, both of which are free and require no authentication.

Built for traders and developers who want fast, scriptable market signals without a heavy charting platform, paid indicator package, or a large dependency stack. Each tool can run independently from the command line, making it easy to use in terminal workflows, automation scripts, spreadsheets, AI agents, or custom trading dashboards.

This project is for research and educational use only. It does not provide financial advice or automated trade execution.

## Why I Built This

I'm a technology enthusiast, AI builder, and amateur trader/investor with a strong interest in stocks, options, technical analysis, and data-driven decision-making.

I enjoy trading because it combines market psychology, probability, risk management, research, and continuous learning. I also love AI because it gives individual developers and traders new ways to organize information, automate repetitive research, test ideas, and build tools that were once limited to large institutions or expensive platforms.

This repository is my attempt to bring those interests together.

Over time, I found useful ideas, scripts, indicators, workflows, and approaches across many open-source repositories and trading tools. Rather than keeping those pieces scattered across separate projects, I wanted to build one practical collection of the tools and capabilities I personally use, learn from, and want to improve.

The goal is to create a flexible research toolkit that can be used from the terminal, integrated into Python scripts, connected to spreadsheets, incorporated into dashboards, or used as part of AI-assisted trading workflows.

If this project saves another trader time, helps someone learn how an indicator or options calculation works, or gives a developer a useful building block for their own market-research workflow, then it is giving something back to a community that has taught me a great deal.

## Why This Exists

Most platforms make it easy to *view* indicators, but harder to reuse them in your own workflows. This repo provides command-line tools for:

- Quickly evaluating momentum, trend, volatility, volume, and market bias
- Pulling option chains and pricing contracts by strike and expiration
- Calculating Black-Scholes Greeks for options analysis
- Evaluating common multi-leg options strategies
- Pulling fundamentals, news, insider trading, analyst ratings, and peer data
- Screening stocks by index, sector, market cap, and custom filters
- Integrating market data into scripts, spreadsheets, alerts, or AI-assisted trading workflows

The goal is not to replace a full trading platform. It is to provide reusable building blocks for independent research and decision support.

## Features

- Standalone Python scripts for common technical indicators
- Monthly, weekly, daily, and hourly analysis
- Yahoo Finance market data through `yfinance`
- Options-chain lookup and individual-contract quotes
- Automatic TTM option-symbol construction, including deep ITM and OTM contracts
- Black-Scholes Greeks and options-spread analysis
- FinViz financial data: fundamentals, news, insider trading, analyst ratings, peer tickers, financial statements, and custom screeners
- TradingView Desktop control via Chrome DevTools Protocol — charts, indicators, alerts, Pine Script, screenshots, replay trading
- Persistent browser webpages via browser-use — serve HTML dashboards from Hermes with full session cookies
- Minimal setup and a small dependency footprint
- Designed to be easy to modify, automate, and extend

## Indicators

| Indicator | Script | What It Helps Identify | Timeframes |
|-----------|--------|------------------------|------------|
| RSI | `scripts/rsi.py` | Overbought and oversold momentum conditions | Monthly, weekly, daily, hourly |
| MACD | `scripts/macd.py` | Trend direction, momentum shifts, and crossovers | Monthly, weekly, daily, hourly |
| Bollinger Bands | `scripts/bollinger.py` | Volatility expansion, compression, and price extremes | Monthly, weekly, daily, hourly |
| SMA | `scripts/sma.py` | Trend direction and support/resistance areas | Monthly, weekly, daily, hourly |
| EMA | `scripts/ema.py` | Faster-moving trend and momentum signals | Monthly, weekly, daily, hourly |
| ATR | `scripts/atr.py` | Average price movement and volatility-based risk sizing | Monthly, weekly, daily, hourly |
| ADX | `scripts/adx.py` | Trend strength, regardless of direction | Monthly, weekly, daily, hourly |
| Volatility | `scripts/volatility.py` | Historical price variability | Monthly, weekly, daily, hourly |
| BX-Trender | `scripts/bxtrender.py` | Trend and momentum conditions | Monthly, weekly, daily, hourly |
| Williams %R | `scripts/williamsr.py` | Momentum and potential reversal zones | Monthly, weekly, daily, hourly |
| RVOL | `scripts/rvol.py` | Relative volume versus normal trading activity | Monthly, weekly, daily, hourly |
| Market Bias | `scripts/marketbias.py` | Bullish, bearish, or neutral technical alignment | Monthly, weekly, daily, hourly |

## FinViz Financial Data

Financial data from FinViz.com. No API key needed.

| Tool | Script | What It Helps Identify |
|------|--------|------------------------|
| Fundamentals | `scripts/fundamentals.py` | P/E, EPS, ROE, margins, beta, 52W high/low, insider ownership, short float, analyst target |
| Stock news | `scripts/news.py` | Latest headlines with source and link |
| Market news | `scripts/market_news.py` | Broad market headlines + blogs |
| Insider trading | `scripts/insider.py` | Per-stock insider buys, sells, and 10b5-1 plans |
| Market insider | `scripts/market_insider.py` | Market-wide insider activity by category |
| Analyst ratings | `scripts/ratings.py` | Analyst rating history and price targets |
| Peer tickers | `scripts/peers.py` | Competitor and peer companies |
| Statements | `scripts/statements.py` | Income, Balance Sheet, Cash Flow (quarterly or annual) |
| Full info | `scripts/full_info.py` | Everything combined in one call |
| Screener | `scripts/screener.py` | Custom filter screeners by index, sector, market cap, and more |

## Options Toolkit

The options tools support contract lookup, chain analysis, Greeks, and common multi-leg strategies.

### Included capabilities

- Option-chain retrieval by ticker and expiration
- Quotes for calls and puts at a selected strike
- Black-Scholes Greeks, including delta, gamma, theta, vega, and rho
- Probability ITM
- Automatic TTM option-symbol generation
- Lookup support for contracts that are deep in-the-money or out-of-the-money
- Spread analysis for common long-premium and defined-risk structures

### Supported spread types

| Strategy | Command |
|----------|---------|
| Vertical spread | `vertical` |
| Long straddle | `straddle` |
| Long strangle | `strangle` |
| Iron condor | `condor` |
| Diagonal / PMCC | `diagonal` |

## TradingView Desktop

Control your TradingView Desktop app from Hermes via Chrome DevTools Protocol. Read charts, add indicators, create alerts, write Pine Script, take screenshots, and practice trading in replay mode.

### What it does

- **Chart control** — set symbol and timeframe, read OHLCV data
- **Indicators** — add built-in indicators, read indicator values
- **Screenshots** — capture chart images on demand
- **Alerts** — create, list, and delete price alerts
- **Pine Script** — compile code, pull/push scripts from Pine Editor
- **Replay** — practice trading in replay mode with step-through control
- **Watchlist** — read tickers from your TradingView watchlist

### Setup

**Prerequisites:** Node.js installed.

```bash
# 1. Install dependencies
cd market-indicators/tradingview
npm install

# 2. Add to your Hermes config.yaml:
# mcpServers:
#   tradingview:
#     command: node
#     args:
#       - path/to/market-indicators/tradingview/src/server.js
#     env:
#       TV_CDP_PORT: '42719'
#     enabled: true

# 3. Restart Hermes

# 4. Launch TradingView with debug port
cd market-indicators/tradingview/scripts
./launch_tv_debug.bat

# 5. Verify
# Use the tv_health_check MCP tool — you should see "cdp_connected": true
```

See `tradingview/SKILL.md` for full setup steps and `tradingview/SETUP_GUIDE.md` for detailed instructions.

## Browsers — Persistent Webpages

Serve instant HTML pages from Hermes and access them with browser-use using the same Chrome session with full session cookies. Great for dashboards, logged-in trading tools, and custom UIs.

### Setup

1. Write HTML files to `browsers/persistent/www/`
2. Start the HTTP server: `cd browsers/persistent && python -m http.server 8787`
3. Navigate with browser-use: `new_tab("http://localhost:8787/index.html")`
4. Kill the server when done

See `browsers/persistent/SKILL.md` for the full workflow.

## Quick Start

### Install

Requires Python 3.11+.

```bash
git clone https://github.com/your-username/market-indicators.git
cd market-indicators

pip install yfinance
```

### Run an indicator

```bash
python scripts/rsi.py NVDA daily
python scripts/macd.py AAPL weekly
python scripts/bxtrender.py TSLA monthly
```

### Get an option chain

```bash
python scripts/options.py NVDA chain 2026-09-18
```

### Quote a specific option contract

```bash
python scripts/options.py SOXL quote 2026-09-18 put 50
```

### Analyze common option spreads

```bash
# Put credit/debit vertical
python scripts/options.py NVDA vertical 2026-09-18 put 140 130

# Iron condor
python scripts/options.py NVDA condor 2026-09-18 120 125 135 140
```

### FinViz financial data

```bash
# Stock fundamentals
python scripts/fundamentals.py NVDA

# News and insider activity
python scripts/news.py NVDA
python scripts/insider.py NVDA
python scripts/market_news.py

# Analyst ratings
python scripts/ratings.py NVDA

# Competitors
python scripts/peers.py NVDA

# Financial statements
python scripts/statements.py NVDA I Q

# Everything at once
python scripts/full_info.py NVDA

# Custom screener
python scripts/screener.py Index="S&P 500" Sector=Technology

# Market insider activity
python scripts/market_insider.py latest
python scripts/market_insider.py "top week buys"
```

## Example Workflow

A simple research workflow might look like this:

1. Run `marketbias.py` on the weekly and daily timeframe to determine broader trend alignment.
2. Use RSI, MACD, ADX, and RVOL to check momentum, trend strength, and participation.
3. Review ATR and volatility to understand expected movement and help frame risk.
4. Pull the option chain for your preferred expiration.
5. Use the spread-analysis commands to compare strikes and risk/reward structures.

For example:

```bash
python scripts/marketbias.py NVDA weekly
python scripts/rsi.py NVDA daily
python scripts/adx.py NVDA daily
python scripts/rvol.py NVDA daily
python scripts/options.py NVDA chain 2026-09-18
```

## Project Structure

```text
market-indicators/
├── .gitignore
├── finviz/
│   └── SKILL.md              ← detailed FinViz documentation
├── indicators/               ← per-indicator documentation
│   ├── RSI/SKILL.md
│   ├── MACD/SKILL.md
│   ├── Bollinger/SKILL.md
│   ├── SMA/SKILL.md
│   ├── EMA/SKILL.md
│   ├── ATR/SKILL.md
│   ├── ADX/SKILL.md
│   ├── Volatility/SKILL.md
│   ├── BX-Trender/SKILL.md
│   ├── Williams%R/SKILL.md
│   ├── RVOL/SKILL.md
│   └── Market Bias/SKILL.md
├── options/
│   └── SKILL.md
├── scripts/
│   ├── indicators_core.py    ← shared utilities (do not run directly)
│   ├── rsi.py
│   ├── macd.py
│   ├── bollinger.py
│   ├── sma.py
│   ├── ema.py
│   ├── atr.py
│   ├── adx.py
│   ├── volatility.py
│   ├── bxtrender.py
│   ├── williamsr.py
│   ├── rvol.py
│   ├── marketbias.py
│   ├── options.py
│   ├── fundamentals.py         ← FinViz
│   ├── news.py                ← FinViz
│   ├── market_news.py         ← FinViz
│   ├── insider.py             ← FinViz
│   ├── market_insider.py      ← FinViz
│   ├── ratings.py             ← FinViz
│   ├── peers.py               ← FinViz
│   ├── statements.py          ← FinViz
│   ├── full_info.py           ← FinViz
│   └── screener.py            ← FinViz
├── tradingview/               ← TradingView MCP server
│   ├── SKILL.md
│   ├── SETUP_GUIDE.md
│   ├── README.md
│   ├── package.json
│   ├── src/
│   ├── scripts/
│   └── references/
├── browsers/
│   └── persistent/
│       ├── SKILL.md
│       └── www/             ← HTML files served here
├── SKILL.md                  ← main skill documentation
├── README.md
└── LICENSE
```

## Data and Limitations

Market data is retrieved through Yahoo Finance using `yfinance`. Data availability, prices, option-chain coverage, and contract metadata can vary by ticker, exchange, market session, and Yahoo Finance availability.

This project is intended for research, education, and workflow automation. Always verify market data independently before making trading decisions.

## Contributing

Issues, feature requests, bug reports, and pull requests are welcome.

Potential future additions include:

- Additional technical indicators
- Historical signal backtesting
- Trade journal and P/L tracking
- CSV or JSON output modes
- Alerting integrations
- More advanced options-risk and probability analysis
- Integration examples for Google Sheets, web dashboards, or AI agents

## License

Released under the [MIT License](LICENSE).

## Inspiration and Attribution

This project was built through hands-on experimentation and learning from the open-source trading, Python, automation, and AI communities.

Some implementation ideas, workflows, and approaches were inspired by other public projects, documentation, and educational resources. Where this repository directly uses, adapts, or includes third-party code, the original source and applicable license should be credited in the relevant file, documentation, or acknowledgments section.

Please review the licenses of any dependencies, code snippets, data sources, or external projects before using this toolkit in your own work.
