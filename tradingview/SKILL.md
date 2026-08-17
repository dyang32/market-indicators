---
name: tradingview
description: Control TradingView Desktop via Chrome DevTools Protocol — charts, indicators, alerts, Pine Script, screenshots, replay trading.
category: MySKILLS
---

# TradingView

Control your TradingView Desktop app from Hermes via Chrome DevTools Protocol.

**Requires:** TradingView Desktop app running with debug port open.

---

## Setup

**Prerequisites:** Node.js installed.

### Step 1 — One-time npm install

After cloning, install dependencies in the tradingview folder:
```bash
cd marketindicators/tradingview
npm install
```

### Step 2 — Add to Hermes MCP config

Add to your Hermes `config.yaml`:
```yaml
mcpServers:
  tradingview:
    command: node
    args:
      - path/to/marketindicators/tradingview/src/server.js
    env:
      TV_CDP_PORT: '42719'
      CDP_HOST: 127.0.0.1
    enabled: true
```

Then restart Hermes.

### Step 3 — Open TradingView with debug port

```bash
cd marketindicators/tradingview/scripts
./launch_tv_debug.bat
```

TradingView will open. Log in if needed. Load a chart.

### Step 4 — Verify connection

Use the `tv_health_check` tool. You should see `"cdp_connected": true`.

---

## Available Tools

See `README.md` for the full list of 78 MCP tools and 30 CLI commands.

### Chart Control
- Set symbol and timeframe
- Add indicators
- Read indicator values
- Capture screenshots
- Draw lines and shapes

### Alerts
- Create, list, and delete price alerts
- Alerts fire in TradingView desktop app

### Pine Script
- Compile Pine Script code
- Pull/push scripts from Pine Editor

### Replay
- Practice trading in replay mode
- Step through price action

### Watchlist
- Read tickers from TradingView watchlist

---

## Sub-Skills

| Tool | Location |
|------|----------|
| Chart analysis | `skills/chart-analysis/SKILL.md` |
| Multi-symbol scan | `skills/multi-symbol-scan/SKILL.md` |
| Pine Script dev | `skills/pine-develop/SKILL.md` |
| Replay practice | `skills/replay-practice/SKILL.md` |
| Strategy reports | `skills/strategy-report/SKILL.md` |
