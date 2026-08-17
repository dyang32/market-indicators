---
name: marketindicators-options
description: Options spread analysis — Black-Scholes Greeks, option chains, verticals, straddles, strangles, iron condors, diagonal spreads. Builds TTM symbols automatically from ticker + expiry + strike.
category: MySKILLS/marketindicators
---

# Options — Spread Analysis and Greeks

Black-Scholes Greeks and option spread analysis. Automatically builds TTM symbols so you can query any strike, even deep ITM/OTM contracts not shown in standard chains.

**Script:** `scripts/options.py`
**Data source:** Yahoo Finance

---

## What It Gets

For any contract:

| Data | Available |
|------|-----------|
| Spot price | ✓ |
| Strike | ✓ |
| DTE (days to expiration) | ✓ |
| Bid | ✓ |
| Ask | ✓ |
| Last price | ✓ |
| Mid price | ✓ |
| IV (implied volatility) | ✓ |
| Delta | ✓ |
| Gamma | ✓ |
| Theta | ✓ |
| Vega | ✓ |
| Rho | ✓ |
| Probability ITM | ✓ |
| Moneyness (ITM/ATM/OTM) | ✓ |
| TTM symbol | ✓ (auto-built) |

---

## Step by Step

### Step 1 — Get an option chain

```
python options.py NVDA chain 2026-09-18
```
Shows all available strikes with mid price, IV, and Greeks.

### Step 2 — Get a specific contract quote

```
python options.py NVDA quote 2026-09-18 call 130
python options.py NVDA quote 2026-09-18 put 120
```
Can query any strike — deep ITM, deep OTM, or off-chain strikes.

### Step 3 — Analyze a vertical spread

```
python options.py NVDA vertical 2026-09-18 put 140 130
```
Shows both legs with full Greeks + net debit, max profit, max loss, breakeven.

### Step 4 — Analyze a long straddle

```
python options.py NVDA straddle 2026-09-18 130
```
Buys ATM call + put at the same strike. Shows total cost, max loss, breakevens.

### Step 5 — Analyze a long strangle

```
python options.py NVDA strangle 2026-09-18 135 125
```
Buys OTM call + OTM put at different strikes. Cheaper than straddle, wider breakevens.

### Step 6 — Analyze an iron condor

```
python options.py NVDA condor 2026-09-18 120 125 135 140
```
4-leg spread. Order: Long PUT $120 / Short PUT $125 / Short CALL $135 / Long CALL $140.
Shows net credit, max profit, max loss, breakevens.

### Step 7 — Diagonal spread (PMCC)

```
python options.py NVDA diagonal 2026-09-18 call 130 2026-10-17
```
Buy long-dated call + sell short-dated call at a higher strike.

---

## All Commands

| Command | Example |
|---------|---------|
| `chain` | `options.py NVDA chain 2026-09-18` |
| `quote` | `options.py SOXL quote 2026-09-18 put 50` |
| `vertical` | `options.py NVDA vertical 2026-09-18 call 130 140` |
| `straddle` | `options.py NVDA straddle 2026-09-18 130` |
| `strangle` | `options.py NVDA strangle 2026-09-18 135 125` |
| `condor` | `options.py NVDA condor 2026-09-18 120 125 135 140` |
| `diagonal` | `options.py NVDA diagonal 2026-09-18 call 130 2026-10-17` |

---

## What Each Spread Means

| Spread | Direction | Max Profit | Max Loss | Best For |
|--------|-----------|-----------|---------|---------|
| Bull Call Spread | Bullish | Limited | Limited | Ranged markets |
| Bear Put Spread | Bearish | Limited | Limited | Falling stock |
| Long Straddle | Volatility play | Unlimited | Limited | Earnings, events |
| Long Strangle | Volatility play | Unlimited | Limited | Wider range, cheaper |
| Iron Condor | Neutral | Limited | Limited | Range-bound stock |
| Diagonal (PMCC) | Bullish/leveraged | Large | Limited | Long-term calls |

---

## Greeks Explained

| Greek | What it means |
|-------|--------------|
| **Delta** | How much the option price moves per $1 move in the stock (0–1 for calls, -1–0 for puts) |
| **Gamma** | Rate of change of Delta — highest for ATM options near expiry |
| **Theta** | Time decay — how much value the option loses per day |
| **Vega** | Sensitivity to IV — how much the option gains/loses per 1% change in IV |
| **Rho** | Sensitivity to interest rates — minimal for short-dated options |
