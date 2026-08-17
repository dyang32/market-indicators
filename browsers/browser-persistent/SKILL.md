---
name: browser-persistent
description: Serve instant HTML pages from Hermes and access them via browser with full logged-in session cookies. For browser automation, dashboards, and trading tools.
category: MySKILLS
---

# Persistent Browser Webpages

Serve HTML pages from Hermes so browser can access them with your browser's full session — cookies, logins, auth tokens all work.

**Use this when you want to:** build a custom dashboard, interact with a logged-in site, serve dynamic HTML content, or create a UI for a script.

## Prerequisites

- Google Chrome installed
- browser CLI in Hermes venv (`hermes-venv/Scripts/browser.exe`)
- Python 3.11+

---

## Step 1 — Create the www folder

```bash
mkdir -p skills/MySKILLS/marketindicators/browsers/persistent/www
```

---

## Step 2 — Write your HTML page

Write any HTML file to `www/`. Example:

`www/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
  <title>My Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <h1>Dashboard</h1>
  <canvas id="chart"></canvas>
  <script>
    // Your JS here — has full browser session cookies
  </script>
</body>
</html>
```

---

## Step 3 — Start the HTTP server

From the `persistent/` directory:

```bash
cd skills/MySKILLS/marketindicators/browsers/persistent
python -m http.server 8787
```

**Use `background=true` on the terminal tool.** Save the `session_id` — you need it to stop the server later.

---

## Step 4 — Launch Chrome for browser

```bash
terminal(background=true, command="\"C:/Program Files/Google/Chrome/Application/chrome.exe\" --remote-debugging-port=9317 --user-data-dir=\"$HOME/.chrome-debug-profile\"")
```

Save the `session_id` — you need it to kill Chrome later.

---

## Step 5 — Verify Chrome is running

```bash
sleep 3 && curl -s http://127.0.0.1:9317/json/version
```

Look for JSON with Chrome version. If you get a connection error, wait 5 more seconds and try again.

---

## Step 6 — Start browser-harness daemon

```bash
terminal(background=true, command="\"C:/Users/user/Desktop/Hermes/hermes-venv/Scripts/browser-harness.exe\"")
```

Also save this `session_id`.

---

## Step 7 — Navigate to your page in browser

```bash
BU_CDP_URL="http://localhost:9317" PYTHONHOME="" PYTHONPATH="" browser <<'PY'
new_tab("http://localhost:8787/index.html")
wait_for_load()
print(page_info())
PY
```

Your page is now running inside the browser Chrome with full session cookies.

---

## Step 8 — Interact with your page

Use browser helpers inside the heredoc:

```bash
BU_CDP_URL="http://localhost:9317" PYTHONHOME="" PYTHONPATH="" browser <<'PY'
# Read page text
result = js("document.body.innerText")
print(repr(result))

# Click an element
result = js("var el = document.querySelector('#myButton'); if(el) { var r = el.getBoundingClientRect(); (r.x + r.width/2) + ',' + (r.y + r.height/2) } else { 'not found' }")
parts = result.split(',')
click_at_xy(float(parts[0]), float(parts[1]))

# Screenshot
capture_screenshot("output.png")
PY
```

**Available helpers:**

| Helper | What it does |
|--------|-------------|
| `new_tab(url)` | Opens a new tab |
| `goto_url(url)` | Navigate current tab to URL |
| `wait_for_load()` | Wait for page to finish loading |
| `page_info()` | Returns dict with url, title, viewport size |
| `capture_screenshot(path)` | Take a screenshot |
| `click_at_xy(x, y)` | Click at pixel coordinates |
| `type_text(text)` | Type text — use for tweet/text input |
| `fill_input(selector, text)` | Fill an input by CSS selector |
| `press_key(key)` | Press a keyboard key |
| `scroll(x, y)` | Scroll to pixel coordinates |
| `js(code)` | Run JavaScript — capture with `result = js("...")` |
| `list_tabs()` | List all open tabs |
| `switch_tab(n)` | Switch to tab number n |
| `close_tab(n)` | Close tab number n |
| `wait_for_element(selector)` | Wait for an element to appear |

---

## Step 9 — Cleanup

Stop everything in this order:

**1. Kill the HTTP server:**
```bash
process(action="kill", session_id="<http_server_session_id>")
```

**2. Kill Chrome:**
```bash
process(action="kill", session_id="<chrome_session_id>")
```

**3. Kill the browser-harness daemon:**
```bash
process(action="kill", session_id="<browser_harness_session_id>")
```

---

## Quick Reference — All Steps in Order

```
Step 1: mkdir www folder                    (one time)
Step 2: Write your HTML page               (one time)
Step 3: python -m http.server 8787        (background=true)
Step 4: Launch Chrome                      (background=true)
Step 5: curl verify Chrome is up          (sleep 3 first)
Step 6: browser-harness                   (background=true)
Step 7: browser navigate to page
Step 8: browser interact with page
Step 9: Kill server → Kill Chrome → Kill daemon
```

---

## Common Use Cases

### Stock dashboard
Write a dashboard in `www/index.html` using Chart.js. browser can fill in data from scripts and screenshot the result.

### Logged-in trading tool
browser has your Twitter/X session. Navigate to any logged-in page from your localhost HTML — it runs in the same Chrome with the same cookies.

### Options calculator
Build a calculator UI in HTML. browser fills in the inputs and reads the results from the DOM via `js()`.

---

## Port Note

Default port is `8787`. If it's in use, pick a different port and update the browser navigation URL to match.
