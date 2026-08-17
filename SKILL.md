---
name: marketindicators
description: Technical analysis indicators, options trading analysis, and FinViz financial data — RSI, MACD, Bollinger Bands, SMA, EMA, ATR, ADX, BX-Trender, Williams %R, RVOL, Market Bias, option spreads, Greeks, fundamentals, news, insider trading, screener. Plus TradingView Desktop control (MCP server).
category: MySKILLS
---

# marketindicators — Technical Analysis + Options Toolkit

Technical analysis indicators and options trading analysis.

**Script location:** `scripts/`
**Data source:** Yahoo Finance

---

## Available Scripts

All indicator scripts accept: `<TICKER> <TIMEFRAME>`
Timeframes: `monthly`, `weekly`, `daily`, `hourly`

### Indicators

| Script | What it does |
|--------|-------------|
| `scripts/rsi.py` | Relative Strength Index |
| `scripts/macd.py` | Moving Average Convergence Divergence |
| `scripts/bollinger.py` | Bollinger Bands |
| `scripts/sma.py` | Simple Moving Averages (SMA 20/50/200) |
| `scripts/ema.py` | Exponential Moving Averages (EMA 9/12/21/26) |
| `scripts/atr.py` | Average True Range |
| `scripts/adx.py` | Average Directional Index + DMI |
| `scripts/volatility.py` | Annualized volatility + Sharpe ratio |
| `scripts/bxtrender.py` | BX-Trender multi-timeframe momentum |
| `scripts/williamsr.py` | Williams %R oscillator |
| `scripts/rvol.py` | Relative Volume |
| `scripts/marketbias.py` | Market Bias (Heikin-Ashi trend) |
| `scripts/indicators_core.py` | Shared utilities (do not run directly) |

### Options

| Script | What it does |
|--------|-------------|
| `scripts/options.py` | Option chains, quotes, spreads, Greeks, TTM symbol builder |

### FinViz

Financial data from FinViz.com. All scripts accept a ticker as an argument.

| Script | What it does |
|--------|-------------|
| `scripts/fundamentals.py` | Full fundamentals — P/E, EPS, ROE, margins, RSI, beta, 52W high/low, etc. |
| `scripts/news.py` | Per-stock news headlines with date, source, and link |
| `scripts/market_news.py` | Market-wide news + blogs (no ticker needed) |
| `scripts/insider.py` | Per-stock insider trading (buys/sells/10b5-1 plans) |
| `scripts/market_insider.py` | Market-wide insider activity — pass option: `latest`, `latest buys`, `latest sales`, `top week`, `top week buys`, `top week sales`, `top owner trade`, `top owner buys`, `top owner sales` |
| `scripts/ratings.py` | Analyst ratings history with price targets |
| `scripts/peers.py` | Competitor/peer tickers |
| `scripts/statements.py` | Income, Balance Sheet, or Cash Flow statements |
| `scripts/full_info.py` | Everything combined — fundamentals + news + ratings + insiders |
| `scripts/screener.py` | Custom filter screener — pass filters as `Key=Value` args |

### TradingView

Control TradingView Desktop via Chrome DevTools Protocol. MCP server — requires Node.js, npm install, and Hermes MCP config. See `tradingview/SKILL.md` for full setup steps.

| Script | What it does |
|--------|-------------|
| `tradingview/SKILL.md` | Setup and usage guide |
| `tradingview/scripts/launch_tv_debug.bat` | Launch TradingView with debug port |
| `tradingview/src/server.js` | MCP server (loads through Hermes MCP system) |

---

## Quick Start

### Run an indicator
```
python scripts/rsi.py NVDA daily
python scripts/macd.py NVDA weekly
python scripts/bollinger.py NVDA monthly
python scripts/bxtrender.py NVDA hourly
```

### Run options analysis
```
python scripts/options.py NVDA chain 2026-09-18
python scripts/options.py NVDA quote 2026-09-18 call 130
python scripts/options.py NVDA quote 2026-09-18 put 120
python scripts/options.py NVDA vertical 2026-09-18 put 140 130
python scripts/options.py NVDA straddle 2026-09-18 130
python scripts/options.py NVDA condor 2026-09-18 120 125 135 140
```

### Run FinViz analysis
```
python scripts/fundamentals.py NVDA
python scripts/news.py NVDA
python scripts/market_news.py
python scripts/insider.py NVDA
python scripts/market_insider.py latest
python scripts/market_insider.py "top week buys"
python scripts/ratings.py NVDA
python scripts/peers.py NVDA
python scripts/statements.py NVDA I Q
python scripts/full_info.py NVDA
python scripts/screener.py Index="S&P 500" Sector=Technology
```

---

## Per-Indicator Documentation

Each indicator has its own detailed SKILL.md:

| Indicator | Location |
|-----------|----------|
| RSI | `indicators/RSI/SKILL.md` |
| MACD | `indicators/MACD/SKILL.md` |
| Bollinger Bands | `indicators/Bollinger/SKILL.md` |
| SMA | `indicators/SMA/SKILL.md` |
| EMA | `indicators/EMA/SKILL.md` |
| ATR | `indicators/ATR/SKILL.md` |
| ADX | `indicators/ADX/SKILL.md` |
| Volatility | `indicators/Volatility/SKILL.md` |
| BX-Trender | `indicators/BX-Trender/SKILL.md` |
| Williams %R | `indicators/Williams%R/SKILL.md` |
| RVOL | `indicators/RVOL/SKILL.md` |
| Market Bias | `indicators/Market Bias/SKILL.md` |
| Options | `options/SKILL.md` |

---

## Options Strategies

| Strategy | Command | Best For |
|---------|---------|---------|
| Vertical spread | `vertical <EXPIRY> <call\|put> <LOW> <HIGH>` | Ranged markets, defined risk |
| Long straddle | `straddle <EXPIRY> <STRIKE>` | Earnings, volatility plays |
| Long strangle | `strangle <EXPIRY> <CALL_STRIKE> <PUT_STRIKE>` | Wider range, cheaper than straddle |
| Iron condor | `condor <EXPIRY> <S1> <S2> <S3> <S4>` | Range-bound stocks |
| Diagonal spread | `diagonal <EXPIRY> <STRIKE> <EXPIRY2>` | Long-term calls (PMCC) |

---

## Folder Structure

```
marketindicators/
├── .gitignore
├── SKILL.md              ← you are here
├── README.md
├── finviz/
│   └── SKILL.md          ← detailed FinViz usage
├── scripts/
│   ├── indicators_core.py  ← shared utilities (do not run)
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
│   ├── fundamentals.py      ← FinViz
│   ├── news.py              ← FinViz
│   ├── market_news.py       ← FinViz
│   ├── insider.py           ← FinViz
│   ├── market_insider.py    ← FinViz
│   ├── ratings.py           ← FinViz
│   ├── peers.py             ← FinViz
│   ├── statements.py        ← FinViz
│   ├── full_info.py         ← FinViz
│   └── screener.py          ← FinViz
├── indicators/
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
└── options/
    └── SKILL.md
└── tradingview/
    └── SKILL.md          ← TradingView Desktop control (MCP server)
```

---

## Limitations

- No real-time data (~15min delay on US stocks via yfinance)
- Read-only analysis only — no order placement
- No portfolio tracking
- Iron condor and diagonal spread calculations are estimates

---

## Pushing to GitHub

`git push` does NOT work from this environment. Use the GitHub API uploader script instead.

1. Put your GitHub token in `keys/push_github.env` inside this skill directory (gitignored — never pushed):

```
GITHUB_TOKEN=your_token_here
```

2. Run from the `marketindicators/` root:
```
python scripts/push_github.py
```

This uploads every file in this skill folder to your GitHub repo.
