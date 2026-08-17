"""
Options — Black-Scholes Greeks and option spread analysis.
Builds TTM symbols automatically from ticker/strike/expiry.

Usage:
  python options.py NVDA chain 2026-09-18
  python options.py NVDA quote 2026-09-18 call 130
  python options.py NVDA vertical 2026-09-18 put 120 110
  python options.py NVDA straddle 2026-09-18 130
  python options.py NVDA strangle 2026-09-18 call 130 put 120
  python options.py NVDA condor 2026-09-18 120 125 135 140
  python options.py NVDA diagonal 2026-09-18 call 130 2026-10-17
Dependencies: yfinance only
"""

import sys
import math
import yfinance as yf
from datetime import datetime
from indicators_core import norm_pdf, norm_cdf


# ─── TTM SYMBOL BUILDER ───────────────────────────────────────────────────────

def build_ttm_symbol(ticker, expiry, option_type, strike):
    """
    Build a TTM (12-char) Yahoo Finance option symbol.
    ticker:   e.g. 'NVDA'
    expiry:   e.g. '2026-09-18'
    option_type: 'call' or 'put'
    strike:   float, e.g. 130.0
    Returns: TTM string like 'NVDA260918C00130000'
    """
    ticker = ticker.upper()
    date_obj = datetime.strptime(expiry, "%Y-%m-%d")
    date_part = date_obj.strftime("%y%m%d")   # 2026-09-18 -> 260918
    type_char = 'C' if option_type == 'call' else 'P'
    strike_int = int(float(strike) * 1000)          # 130.0 -> 130000
    strike_str = f"{strike_int:08d}"               # -> '00130000'
    return f"{ticker}{date_part}{type_char}{strike_str}"


def get_strike_from_ttm(ttm):
    """Extract strike price from a TTM symbol."""
    # Format: TICKYYMMDDC/DDDDDDDD
    strike_part = ttm[-8:]
    return int(strike_part) / 1000


# ─── BLACK-SCHOLES ─────────────────────────────────────────────────────────────

def black_scholes(spot, strike, T, r, sigma, option_type="call"):
    """Compute option price via Black-Scholes."""
    if T <= 0 or sigma <= 0:
        return None
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        price = spot * norm_cdf(d1) - strike * math.exp(-r * T) * norm_cdf(d2)
    else:
        price = strike * math.exp(-r * T) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    return price


def greeks(spot, strike, T, r, sigma, option_type="call"):
    """Compute all Greeks via Black-Scholes closed-form."""
    if T <= 0:
        return None
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    delta = norm_cdf(d1) if option_type == "call" else norm_cdf(d1) - 1
    gamma = norm_pdf(d1) / (spot * sigma * math.sqrt(T))
    theta = (-(spot * norm_pdf(d1) * sigma) / (2 * math.sqrt(T))
             - r * strike * math.exp(-r * T) * (norm_cdf(d2) if option_type == "call" else norm_cdf(-d2))) / 365
    vega = spot * norm_pdf(d1) * math.sqrt(T) / 100
    rho = (strike * T * math.exp(-r * T) *
           (norm_cdf(d2) if option_type == "call" else -norm_cdf(-d2))) / 100
    prob_itm = norm_cdf(d2) if option_type == "call" else norm_cdf(-d2)
    return {
        "delta": round(delta, 4),
        "gamma": round(gamma, 6),
        "theta": round(theta, 4),
        "vega": round(vega, 4),
        "rho": round(rho, 4),
        "prob_itm": round(prob_itm * 100, 1),
    }


def solve_iv(price, spot, strike, T, r, option_type="call"):
    """Newton-Raphson IV solver. Returns IV as a decimal (0.30 = 30%)."""
    iv = 0.30
    for _ in range(100):
        p = black_scholes(spot, strike, T, r, iv, option_type)
        if p is None:
            break
        d1 = (math.log(spot / strike) + (r + 0.5 * iv**2) * T) / (iv * math.sqrt(T))
        vega = spot * norm_pdf(d1) * math.sqrt(T) / 100
        diff = price - p
        if abs(diff) < 1e-6 or vega == 0:
            break
        iv += diff / vega
    return max(iv, 0.01)


# ─── OPTION CHAIN ──────────────────────────────────────────────────────────────

def fetch_chain(symbol, expiry):
    """Fetch option chain from yfinance. Returns (spot, calls_df, puts_df)."""
    ticker = yf.Ticker(symbol)
    try:
        chains = ticker.option_chain(expiry)
    except Exception as e:
        print(f"Error fetching chain: {e}")
        return None, None, None
    spot = ticker.info.get("regularMarketPrice")
    if spot is None:
        try:
            spot = ticker.history(period="1d")["Close"].iloc[-1]
        except:
            spot = 0
    return spot, chains.calls, chains.puts


def fetch_contract(symbol, expiry, option_type, strike):
    """
    Fetch a specific option contract by building its TTM symbol.
    Works even when the strike is outside the visible chain range.
    Returns dict with price, bid, ask, IV, and Greeks.
    """
    ttm = build_ttm_symbol(symbol, expiry, option_type, strike)
    ticker_ttm = yf.Ticker(ttm)
    info = ticker_ttm.info

    # Fallback: use spot from underlying
    under = yf.Ticker(symbol)
    spot = under.info.get("regularMarketPrice", 0)
    if spot == 0:
        try:
            spot = under.history(period="1d")["Close"].iloc[-1]
        except:
            pass

    strike_f = float(strike)
    exp_dt = datetime.strptime(expiry, "%Y-%m-%d")
    dte = max((exp_dt - datetime.now()).days, 1)
    T = dte / 365

    price = info.get("regularMarketPrice")
    bid = info.get("bid")
    ask = info.get("ask")
    iv_yf = info.get("impliedVolatility")

    # Use yfinance IV if available, otherwise solve from price
    if iv_yf and iv_yf > 0:
        sigma = iv_yf
    elif price and price > 0.01:
        sigma = solve_iv(price, spot, strike_f, T, 0.05, option_type)
        # Clamp insane IV from deep OTM/ITM contracts
        if sigma > 5.0:
            sigma = 0.30  # default to 30%
    else:
        sigma = 0.30

    g = greeks(spot, strike_f, T, 0.05, sigma, option_type)
    mid = ((bid or 0) + (ask or 0)) / 2 if bid and ask else price

    return {
        "ttm": ttm,
        "symbol": symbol.upper(),
        "expiry": expiry,
        "type": option_type.upper(),
        "strike": strike_f,
        "spot": spot,
        "price": price,
        "bid": bid,
        "ask": ask,
        "mid": mid,
        "iv": round(sigma * 100, 2),
        "dte": dte,
        "greeks": g,
    }


def print_contract(c):
    """Pretty-print a single contract."""
    g = c["greeks"] or {}
    moneyness = "ITM" if (c["spot"] > c["strike"] and c["type"] == "CALL") or (c["spot"] < c["strike"] and c["type"] == "PUT") else \
               "ATM" if abs(c["spot"] - c["strike"]) / c["spot"] < 0.02 else "OTM"
    print(f"  TTM:       {c['ttm']}")
    print(f"  Type:      {c['type']}  Strike: ${c['strike']}  Moneyness: {moneyness}")
    print(f"  Spot:     ${c['spot']:.2f}  DTE: {c['dte']} days  IV: {c['iv']}%")
    price_str = f"${c['price']:.2f}" if c['price'] else "N/A"
    bid_str = f"${c['bid']:.2f}" if c['bid'] else "N/A"
    ask_str = f"${c['ask']:.2f}" if c['ask'] else "N/A"
    mid_str = f"${c['mid']:.2f}" if c['mid'] else "N/A"
    print(f"  Price:    {price_str}  Bid: {bid_str}  Ask: {ask_str}  Mid: {mid_str}")
    if g:
        print(f"  Delta:    {g['delta']}  Gamma: {g['gamma']}  Theta: ${g['theta']}/day  Vega: ${g['vega']}/1%  Rho: ${g['rho']}/1%")


# ─── SPREADS ───────────────────────────────────────────────────────────────────

def calc_spread(c1, c2, spread_type):
    """Generic spread calculator between two contracts."""
    p1 = c1["mid"] or 0
    p2 = c2["mid"] or 0
    if spread_type == "vertical_call":
        # Bull call: buy lower strike, sell higher strike
        # c1 = long (lower strike), c2 = short (higher strike)
        debit = max(p1 - p2, 0)
        credit = debit
        max_loss = debit
        max_profit = (c2["strike"] - c1["strike"]) * 100 - max_loss
        breakeven = c1["strike"] + debit
    elif spread_type == "vertical_put":
        # Bear put: buy higher strike, sell lower strike
        debit = max(p1 - p2, 0)
        max_loss = debit
        max_profit = (c1["strike"] - c2["strike"]) * 100 - max_loss
        breakeven = c1["strike"] - debit
    elif spread_type == "straddle":
        # Long straddle: buy call + put at same strike
        total_cost = p1 + p2
        max_loss = total_cost * 100
        max_profit = float("inf")
        breakeven = [c1["strike"] - total_cost, c1["strike"] + total_cost]
    elif spread_type == "strangle":
        # Long strangle: buy OTM call + OTM put
        total_cost = p1 + p2
        max_loss = total_cost * 100
        max_profit = float("inf")
        breakeven = [c2["strike"] - total_cost, c1["strike"] + total_cost]
    elif spread_type == "condor":
        # Long condor: 4 legs
        # c1=buy lower, c2=sell lower-mid, c3=sell upper-mid, c4=buy upper
        total_cost = (p1 + p3) - (p2 + p2)  # simplified: buy wings, sell body
        max_loss = total_cost * 100
        max_profit = (c2["strike"] - c1["strike"] - total_cost) * 100
        breakeven = [c1["strike"] + total_cost, c4["strike"] - total_cost]
    else:
        return {}

    return {
        "spread_type": spread_type,
        "net_debit": round(p1 - p2, 2) if spread_type in ["vertical_call", "vertical_put"] else round(p1 + p2, 2),
        "max_profit": round(max_profit, 2) if max_profit != float("inf") else "Unlimited",
        "max_loss": round(max_loss * 100, 2) if not isinstance(max_loss, float) or max_loss != float("inf") else "Unlimited",
        "breakeven": breakeven,
    }


# ─── COMMANDS ─────────────────────────────────────────────────────────────────

def cmd_chain(symbol, expiry):
    print(f"Options Chain — {symbol.upper()}  Expiry: {expiry}")
    spot, calls, puts = fetch_chain(symbol, expiry)
    if spot is None:
        return
    print(f"Spot: ${spot:.2f}\n")

    print(f"{'Strike':<10} {'Type':<6} {'Mid':>8} {'IV%':>8} {'Delta':>7} {'Gamma':>8} {'Theta':>9} {'Vega':>8}")
    print("-" * 72)

    for df in [calls, puts]:
        if df is None or df.empty:
            continue
        for _, row in df.iterrows():
            s = float(row.get("strike", 0))
            t = "CALL" if "CALL" in str(row.get("contractSymbol", "")) else "PUT"
            mid = (float(row.get("bid", 0) or 0) + float(row.get("ask", 0) or 0)) / 2
            iv = float(row.get("impliedVolatility", 0) or 0) * 100
            g = greeks(spot, s, 30/365, 0.05, iv/100, t.lower()) or {}
            print(f"${s:<9.2f} {t:<6} ${mid:>7.2f} {iv:>7.1f}% {g.get('delta',0):>7.4f} {g.get('gamma',0):>8.6f} ${g.get('theta',0):>8.4f} ${g.get('vega',0):>7.4f}")


def cmd_quote(symbol, expiry, option_type, strike):
    print(f"Option Quote — {symbol.upper()} {expiry} {option_type.upper()} ${strike}")
    c = fetch_contract(symbol, expiry, option_type, float(strike))
    if c is None:
        print("Contract not found.")
        return
    print_contract(c)


def cmd_vertical(symbol, expiry, option_type, strike1, strike2):
    print(f"Vertical Spread — {symbol.upper()} {expiry} {option_type.upper()} ${strike1}/${strike2}")
    c1 = fetch_contract(symbol, expiry, option_type, float(strike1))
    c2 = fetch_contract(symbol, expiry, option_type, float(strike2))
    if c1 is None or c2 is None:
        return
    spread_type = f"vertical_{option_type}"
    result = calc_spread(c1, c2, spread_type)
    print(f"\n  [Long ${strike1} {option_type.upper()}]")
    print_contract(c1)
    print(f"\n  [Short ${strike2} {option_type.upper()}]")
    print_contract(c2)
    print(f"\n  Net Debit:   ${result['net_debit']:.2f}")
    print(f"  Max Profit:  ${result['max_profit']}")
    print(f"  Max Loss:    ${result['max_loss']}")
    be = result["breakeven"]
    print(f"  Breakeven:   ${be:.2f}")


def cmd_straddle(symbol, expiry, strike):
    print(f"Long Straddle — {symbol.upper()} {expiry} ATM ${strike}")
    c_call = fetch_contract(symbol, expiry, "call", float(strike))
    c_put = fetch_contract(symbol, expiry, "put", float(strike))
    if c_call is None or c_put is None:
        return
    result = calc_spread(c_call, c_put, "straddle")
    print_contract(c_call)
    print()
    print_contract(c_put)
    print(f"\n  Total Cost:  ${result['net_debit']:.2f} (${result['net_debit']*100:.2f} per spread)")
    print(f"  Max Loss:    ${result['max_loss']} (expires worthless)")
    print(f"  Breakevens:  ${result['breakeven'][0]:.2f} / ${result['breakeven'][1]:.2f}")


def cmd_strangle(symbol, expiry, call_strike, put_strike):
    print(f"Long Strangle — {symbol.upper()} {expiry} CALL ${call_strike} / PUT ${put_strike}")
    c_call = fetch_contract(symbol, expiry, "call", float(call_strike))
    c_put = fetch_contract(symbol, expiry, "put", float(put_strike))
    if c_call is None or c_put is None:
        return
    result = calc_spread(c_call, c_put, "strangle")
    print_contract(c_call)
    print()
    print_contract(c_put)
    print(f"\n  Total Cost:  ${result['net_debit']:.2f} (${result['net_debit']*100:.2f} per spread)")
    print(f"  Max Loss:    ${result['max_loss']} (expires worthless)")
    print(f"  Breakevens:  ${result['breakeven'][0]:.2f} / ${result['breakeven'][1]:.2f}")


def cmd_condor(symbol, expiry, s1, s2, s3, s4):
    print(f"Iron Condor — {symbol.upper()} {expiry} ${s1}/${s2}/${s3}/${s4}")
    legs = [
        fetch_contract(symbol, expiry, "put", float(s1)),
        fetch_contract(symbol, expiry, "put", float(s2)),
        fetch_contract(symbol, expiry, "call", float(s3)),
        fetch_contract(symbol, expiry, "call", float(s4)),
    ]
    for i, leg in enumerate(legs):
        if leg is None:
            return
        types = ["Long PUT", "Short PUT", "Short CALL", "Long CALL"]
        print(f"\n  [{types[i]} ${legs[i]['strike']}]")
        print_contract(leg)
    # Net credit
    credit = (legs[1]["mid"] + legs[2]["mid"]) - (legs[0]["mid"] + legs[3]["mid"])
    width = float(s3) - float(s2)
    max_profit = credit * 100
    max_loss = (width * 100) - max_profit
    print(f"\n  Net Credit:   ${credit:.2f} (${credit*100:.2f} per spread)")
    print(f"  Max Profit:  ${max_profit:.2f}")
    print(f"  Max Loss:    ${max_loss:.2f}")
    print(f"  Breakevens:  ${float(s2) - credit:.2f} / ${float(s3) + credit:.2f}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    symbol = sys.argv[1].upper()
    action = sys.argv[2].lower()
    args = sys.argv[3:]

    if action == "chain":
        if len(args) < 1:
            print("Usage: options.py <TICKER> chain <EXPIRY>")
            sys.exit(1)
        cmd_chain(symbol, args[0])

    elif action == "quote":
        # options.py NVDA quote 2026-09-18 call 130
        if len(args) < 3:
            print("Usage: options.py <TICKER> quote <EXPIRY> <call|put> <STRIKE>")
            sys.exit(1)
        cmd_quote(symbol, args[0], args[1], args[2])

    elif action == "vertical":
        # options.py NVDA vertical 2026-09-18 put 120 110
        if len(args) < 4:
            print("Usage: options.py <TICKER> vertical <EXPIRY> <call|put> <STRIKE_LONG> <STRIKE_SHORT>")
            sys.exit(1)
        cmd_vertical(symbol, args[0], args[1], args[2], args[3])

    elif action == "straddle":
        if len(args) < 2:
            print("Usage: options.py <TICKER> straddle <EXPIRY> <STRIKE>")
            sys.exit(1)
        cmd_straddle(symbol, args[0], args[1])

    elif action == "strangle":
        if len(args) < 3:
            print("Usage: options.py <TICKER> strangle <EXPIRY> <CALL_STRIKE> <PUT_STRIKE>")
            sys.exit(1)
        cmd_strangle(symbol, args[0], args[1], args[2])

    elif action == "condor":
        if len(args) < 5:
            print("Usage: options.py <TICKER> condor <EXPIRY> <S1> <S2> <S3> <S4>")
            sys.exit(1)
        cmd_condor(symbol, args[0], args[1], args[2], args[3], args[4])

    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
