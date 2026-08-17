# TradingView — Windows Configuration

## Install Path

TradingView for Windows ships as an MSIX package. The exact path varies by version. Use the launch script instead — it auto-detects the current install:

```bash
cd skills/MySKILLS/marketindicators/tradingview/scripts
./launch_tv_debug.bat
```

To find the install manually:
```bash
where /r "C:\Program Files" TradingView.exe 2>nul
```
Or: Task Manager → Details → TradingView.exe → Right-click → Open file location

## Debug Port Configuration

| Where | Key | Value |
|-------|-----|-------|
| `src/connection.js` | `CDP_PORT` default | `42719` |
| `config.yaml` | `mcp_servers.tradingview.env.TV_CDP_PORT` | `42719` |
| Launch script | `--remote-debugging-port` arg | `42719` |
| Env var override | `TV_CDP_PORT` or `CDP_PORT` | any port |

If the port changes, update all three places above.

## Launch Commands

**Using the batch script (recommended):**
```bash
cd skills/MySKILLS/marketindicators/tradingview/scripts
./launch_tv_debug.bat
```

**From cmd/PowerShell:**
```bash
"C:\Program Files\WindowsApps\TradingView.Desktop_VERSION_x64__n534cwy3pjxzj\TradingView.exe" --remote-debugging-port=42719
```

## Kill Command
```bash
taskkill -F -IM TradingView.exe
```

## CDP Wait Pattern
TradingView takes ~15 seconds after launch before the debug port is ready. Verify:
```bash
curl -s --max-time 5 "http://127.0.0.1:42719/json/version"
```
If it returns JSON with "Browser": "Chrome/...", the port is ready. Do NOT call MCP tools immediately after launch — wait for this response first.

## Multiple Processes
TradingView sometimes spawns multiple processes. `taskkill -F` closes all of them at once, which is the desired behavior when done.
