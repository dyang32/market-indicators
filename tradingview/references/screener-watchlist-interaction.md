# Screener + Watchlist interaction — session detail (verified 08/01/26)

Verified against TradingView Desktop (debug port 42719), maximized 1920×1080 window.

## Screener

**Open:** right sidebar "Screeners" button at ~(1876, 665). Panel root class contains `screenerContainer-f56NdSlz`, ~944px wide, covers the right side of the window.

**Read rows:** `sc.querySelectorAll('[class*="row"]')` — the header row matches too, so filter with `width > 500 && children.length > 2`. Data rows look like:
`NVDA200.75 USD+2.93%139.95 M1.104.86 T USD30.746.53 USD+110.33%0.14%Electronic technologyStrong buy`

**Columns visible:** Symbol, Price, Chg %, Vol, Rel vol, Mkt cap, P/E, EPS dil TTM, EPS dil growth TTM YoY, Div yield % TTM, Sector, Analyst rating.

**Column filter buttons** (activeArea class) at y=112 / y=154 / y=196 rows:
- US (996,112), Watchlist (1105,112), Index (1238,112), Price (1327,112), Chg % (1413,112), Mkt cap (1504,112), P/E (1609,112), EPS dil growth (1685,112)
- Div yield % (996,154), Sector (1122,154), Analyst rating (1218,154), Perf % (1367,154), Revenue growth (1460,154), PEG (1625,154), ROE (1703,154), Beta (1782,154)
- Recent earnings date (996,196), Upcoming earnings date (1197,196)

**Price dropdown presets** (click Price → dropdown): "Above 100", "Fractional shares time 10 to 100", "Mid-priced 10 and below", "Not quoted". The popup contains a Search input (placeholder "Search", class `input-H0xdCnFS`, at ~(1336, 203)).

**Applying "Above 100"** (click at ~(1373, 257)): dropdown closes, filter goes live. Vision (OmniRoute gemini/gemini-3.5-flash) confirmed: "Price > 100 USD has been actively applied." The Price column button itself shows NO active indicator — the applied filter lives in the screener state, not the button style.

**PITFALL — portal rendering:** while the Price dropdown was open, scoped queries INSIDE the screener container found zero inputs/dropdowns. `document.querySelectorAll('input')` globally found the Search input. The popup is portal-rendered outside the screener root. Use global queries + vision confirmation.

**PITFALL — vision truncation:** the OmniRoute SSE response must be read by iterating `for raw in r:` (see vision skill Step 3). A one-shot `resp.read()` returns a truncated mid-sentence body ("Yes, there is a \"Price\" dropdown/" and stops). The stream iteration returns the full answer.

**Manual setup (custom value) — VERIFIED 08/01/26:**
After clicking a filter column (e.g. Price), the dropdown's last option is **"Manual setup"** (~(1501, 655) when open). Clicking it swaps the dropdown to an "Enter value" input PREFILLED with the current filter value (saw `100` after the "Above 100" preset). Type via React native setter:
```javascript
const input = [...document.querySelectorAll('input')].find(i => i.offsetParent !== null && i.placeholder === 'Enter value');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(input, '500');
input.dispatchEvent(new Event('input', {bubbles: true}));
input.dispatchEvent(new Event('change', {bubbles: true}));
```
Press Enter (`ui_keyboard` key "Enter") → filter applies. Verified: "Price > 500 USD" went live, table showed only stocks > $500 (META 556.71, LLY 1,148.84, BRK.A, MU 823.03, MA 573.10, COST 951.89, AMAT 507.67).

**Multi-select filters — VERIFIED 08/01/26:** Sector dropdown = multi-select list (Commercial services … Technology services + "Select all"). Clicking "Electronic technology" applied immediately; the column button then read "Electronic technology". Combined with Price > 500, table returned only MU, STX, WDC, SNDK, LMT — both filters compose.

**PITFALL — filter buttons SHIFT horizontally after filters apply:** after "Price > 500 USD" applied, the Price button label widened and pushed every button right. Cached coordinates from before (Analyst rating at (1218,154)) then hit a DIFFERENT column (opened Sector). Re-query positions by text before every click:
```javascript
(() => { const sc = document.querySelector('[class*="screenerContainer"]'); const btns = [...sc.querySelectorAll('button')].filter(b => b.offsetParent !== null && b.textContent.trim().length > 1).map(b => ({txt: b.textContent.trim().replace(/\s+/g, ' ').slice(0, 25), x: Math.round(b.getBoundingClientRect().left), y: Math.round(b.getBoundingClientRect().top)})); return JSON.stringify(btns.filter(b => b.y > 100 && b.y < 230)); })()
```
Post-shift positions observed (Price > 500 + Electronic technology active): US (996,112), Watchlist (1105,112), Index (1238,112), "Price 500 USD" (1327,112), Chg % (1518,112), Mkt cap (1609,112), P/E (1715,112); EPS dil growth (996,154), Div yield % (1149,154), Electronic technology (1275,154), Analyst rating (1505,154), Perf % (1654,154); Revenue growth (996,196), PEG (1161,196), ROE (1239,196), Beta (1318,196), Recent earnings date (1400,196), Upcoming earnings date (1601,196).

**Add filter column ("+" button) — VERIFIED 08/01/26:** the "+" icon button sits at the END of the filter row's second line (~(1013, 255) at test time; wraps/repositions as filters change). It opens the column/filter picker with categories: **Overview, Security info, Market data, Technicals, Financials, Valuation, Growth, Margins, Dividends** — click a category to expand its columns (e.g. Technicals has RSI, MACD), then click a column to add it as a filter row.

**More actions ("…" button) — VERIFIED 08/01/26:** next to "+" (~(1055, 255)) opens: **Reset all filters, Remove N inactive filters, Remove all filters.** Use "Reset all filters" to clear a screen to the default column set before building a new scan.

**Save / Load — FULLY VERIFIED 08/01/26 (round-trip proven):** header has the **screen-name button** ("All stocks", ~(992–1106, 62), class `screenNameButton-6G8gpYr4`) and a **Save** button (~(1106, 62), class `saveScreenButton-DMcxD0hG unsaved-DMcxD0hG`). Both open the SAME portal-rendered screen menu with: **Save screen, Autosave (toggle), Share screen (toggle), Make a copy…, Rename…, Download results as CSV, Create new screen…, Open screen…**

**Verified save flow:**
1. Click the screen-name button center (~(1049, 62)) — the menu opens (confirm with vision if in doubt; the menu is portal-rendered)
2. Click **"Save screen"** (~(1166, 118)) — opens the Save dialog CENTER-SCREEN with a "New screen name" input pre-filled "All stocks copy", Cancel (~(1055, 557)) / Save (~(1132, 557))
3. Set the name via the React native setter + input/change events (same pattern as the filter "Enter value" input), then click Save
4. Verify: `document.querySelector('[class*="screenNameButton"]').textContent` shows the new name

**Verified load flow (round-trip proven):**
1. Click the screen-name button → menu → **"Open screen…"** (~(1166, 437); position drifts between menu opens — re-query by text before clicking)
2. The dialog lists **"My screens"** (saved screens) + "All stocks", with a Search input — click the saved screen
3. Verify: screen name + filter buttons + table rows all restore. Test artifact: saved "Tech 500 Strong Buy" (Price > 500 + Electronic technology + Analyst rating Strong buy) → loaded "All stocks" cleared all filters (NVDA/AAPL back) → reloaded saved screen → MU, AXON back with all three filter chips intact.

**PITFALL — dialogs render CENTER-SCREEN, NOT inside the screener panel:** the Save dialog, Open-screen dialog, and the screen menu are portal-rendered; queries scoped to `[class*="screenerContainer"]` miss them entirely. Use GLOBAL queries: `document.querySelectorAll('input')` finds the name input; menu items are findable via leaf-text search (`[...document.querySelectorAll('div,span')].filter(e => e.children.length === 0 && /Open screen/.test(e.textContent))`). When a menu seems missing, verify with `capture_screenshot` + the vision skill before concluding — the screen-name button carries class `isPressed-*` while its menu is open (observed), which is a reliable DOM signal the menu IS up.

## Watchlist

**Add symbol flow:**
1. Click "Add symbol" at ~(1752, 47) (right panel header, near "Watchlist" label)
2. Search input appears with placeholder "Symbol, ISIN, or CUSIP". Type via React native setter:
```javascript
const input = [...document.querySelectorAll('input')].find(i => i.placeholder === 'Symbol, ISIN, or CUSIP' && i.offsetParent !== null);
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(input, 'SOFI');
input.dispatchEvent(new Event('input', {bubbles: true}));
input.dispatchEvent(new Event('change', {bubbles: true}));
```
3. Search results render; the stock result row contains "S SOFI". Click the first result row that includes SOFI.
4. Verify: `[...document.querySelectorAll('[class*="watchlist"]')].map(el => el.textContent).join('|')` contains SOFI.

**GOTCHA — chart navigates:** clicking the search result changes the main chart symbol to the searched ticker (chart went BATS:ENPH → BATS:SOFI). The watchlist row also becomes `active`/`selected` (class `symbol-ALH_8bJI active-ALH_8bJI`). This is expected TradingView behavior — the add-symbol search doubles as a symbol search.

**Remove attempts (all failed 08/01/26):**
- Right-click on the watchlist row (real mouse, button: right) opened a menu with: Flag/Unflag SOFI, Unflag all symbols, "Add SOFI to watchlist", Watchlist/Create new list…, Add SOFI to compare, Add note for SOFI, Financials…, Add section, Add symbol. NO "Remove from watchlist" item.
- Synthetic `contextmenu` dispatch on the row opened the same search-overlay menu.
- Delete key after selecting the row (click + Delete) — no removal.
- Hover-revealed remove button: a `removeButton-ALH_8bJI` span appears at the row's right edge ONLY during real hover. `getBoundingClientRect()` returns 0×0 when not hovered; synthetic mouseover/mouseenter do not render it. Clicking the revealed coordinates (~(1846, 819)) did not remove the row. Class observed: `button-uLhdDCrU removeButton-ALH_8bJI removeButton`.
- `ui_hover` by text "SOFI" after the chart navigated hit the chart's symbol label at (87, 19), not the watchlist row — the watchlist row span is at ~(1690, 823) with `symbolNameText-ALH_8bJI` class.

**Verdict:** watchlist add + read = reliable via MCP. Watchlist remove = NOT solved as of 08/01/26. The TradingView watchlist widget's internal API (`window.TradingViewApi._watchlistApiDeferredPromise`) was null/uninitialized in this session — no programmatic remove hook found. The user said "Stop, you've wasted enough time on it" — don't re-attempt removal loops; state plainly it's not working and let the user remove manually.

## Useful debug probes

- What's really at a click point (catches overlays/portals):
```javascript
(() => { const el = document.elementFromPoint(1704, 830); const chain = []; let cur = el; for (let i = 0; i < 6 && cur; i++) { chain.push({tag: cur.tagName, cls: (typeof cur.className === 'string' ? cur.className : '').slice(0, 60), txt: cur.textContent.trim().slice(0, 30)}); cur = cur.parentElement; } return JSON.stringify(chain); })()
```
- All visible inputs anywhere (catches portal inputs):
```javascript
(() => [...document.querySelectorAll('input')].filter(i => i.offsetParent !== null).map(i => ({ph: i.placeholder, x: Math.round(i.getBoundingClientRect().left), y: Math.round(i.getBoundingClientRect().top)})))()
```
- Visible menu boxes (context menus render as `[class*="menuBox"]`):
```javascript
(() => [...document.querySelectorAll('[class*="menuBox"]')].filter(el => el.offsetParent !== null && el.getBoundingClientRect().width > 100).map(m => m.textContent.trim().replace(/\s+/g, ' ').slice(0, 300)))()
```
