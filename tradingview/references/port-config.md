# TradingView MCP — Port & Config Reference

## Port Override

The MCP server connects to TradingView via Chrome DevTools Protocol. Default port is hardcoded in `src/connection.js`:

```js
export const CDP_PORT = Number(process.env.TV_CDP_PORT || process.env.CDP_PORT) || 42719;
```

**To change the port**, update both:
1. `src/connection.js` — the default fallback value (last number in the `||` chain)
2. `config.yaml` → `mcp_servers.tradingview.env.TV_CDP_PORT` — the env var override

The env var in the MCP config takes priority over the hardcoded default. Set it in one place OR the other, not both.

## Hermes Config — YAML Array Gotcha

The `hermes config set` CLI does NOT handle YAML arrays cleanly. This produces wrong output:

```
hermes config set mcp_servers.tradingview.args '["path"]'
# Result: args: '[0]: path'  ← broken
```

**Fix:** Use Python to write the array directly:

```python
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
config['mcp_servers']['tradingview']['args'] = ['path/to/your/marketindicators/tradingview/src/server.js']
with open('config.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
```

## Launch Script Output Noise

`scripts/launch_tv_debug.bat` prints the `CLAUDE.md` file content to stdout — this is cosmetic, not an error. The CDP-ready JSON at the end confirms success.

## Starting TradingView from Agent

Do NOT use `scripts/launch_tv_debug.bat` directly in the terminal — it blocks with ping loops and outputs CLAUDE.md noise.

**Correct approach:** background=True with notify_on_complete=False (TradingView is long-lived), then verify separately:

```bash
# Step 1: start background
terminal(background=True, command='"path/to/TradingView.exe" --remote-debugging-port=42719', notify_on_complete=False)

# Step 2: wait separately
terminal(command='sleep 15 && curl http://127.0.0.1:42719/json/version')

# Step 3: test MCP
mcp_tradingview_tv_health_check
```

Or use the MCP tool `tv_launch` which handles all of this internally.

## TradingView Dies When Parent Exits

If you launch TradingView from a terminal that closes, TradingView may close too. TradingView should be launched independently (start menu, desktop shortcut, or double-clicked) so it persists.

## Verifying Connection

```bash
curl http://127.0.0.1:42719/json/version
# Should return JSON with "Browser": "...TradingView..."
```

Or use the MCP tool:
```
mcp_tradingview_tv_health_check
```

## File Locations

| File | Purpose |
|------|---------|
| `src/connection.js` | CDP host/port defaults (patch here to change default port) |
| `scripts/launch_tv_debug.bat` | Launch TradingView with debug port (Windows) |
| `src/tools/health.js` | `tv_launch` tool — reads port from `tv_launch({port})` arg |
| `src/core/health.js` | Launch logic — uses `CDP_PORT` from `connection.js` as fallback |

## Quick Port Change (summary)

1. Patch `src/connection.js` — change `42719` to your port in the fallback
2. Patch `config.yaml` — update `TV_CDP_PORT` under `mcp_servers.tradingview.env`
3. Restart Hermes
4. Launch/relaunch TradingView with `--remote-debugging-port=YOUR_PORT`
