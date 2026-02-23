#!/usr/bin/env python3
"""
GMX V2 Short Funding Scanner (Arbitrum)

Simple list of the best opportunities to open a short and receive funding.
Data source: GMX V2 markets API (arbitrum-api.gmxinfra.io).
Net Short APR: uses API netRateShort (authoritative) with sign inverted to match GMX (positive = short receives).
Gross Funding and Borrow Fee in 1e30 precision.
"""

import requests
import pandas as pd

API_URL = "https://arbitrum-api.gmxinfra.io/markets/info"
PRECISION = 1e30  # 30 decimals GMX V2

ZERO = "0x0000000000000000000000000000000000000000"
USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"


def fetch_markets():
    r = requests.get(API_URL, timeout=30)
    r.raise_for_status()
    return r.json().get("markets", [])


def to_apr_pct(raw):
    if raw is None:
        return 0.0
    return (int(raw) / PRECISION) * 100


def is_ok(m):
    if not m.get("isListed"):
        return False
    n = m.get("name", "")
    if "SWAP-ONLY" in n or "deprecated" in n.lower():
        return False
    idx = (m.get("indexToken") or "").strip().lower()
    if idx == ZERO.lower():
        return False
    short = (m.get("shortToken") or "").strip().lower()
    if short != USDC.lower():
        return False
    return True


def main():
    print("GMX V2 Short Funding Scanner (Arbitrum)\n")
    markets = fetch_markets()

    rows = []
    for m in markets:
        if not is_ok(m):
            continue
        market = m.get("name", "")
        raw_funding = m.get("fundingRateShort")
        raw_borrow = m.get("borrowingRateShort")
        raw_net = m.get("netRateShort")
        funding_apr = to_apr_pct(raw_funding)
        borrow_apr = to_apr_pct(raw_borrow)
        net_from_api = to_apr_pct(raw_net)
        # Use netRateShort from API (authoritative). API sign: positive = short pays; invert so positive = short receives (matches GMX)
        net_apr = -net_from_api
        rows.append({
            "Market": market,
            "Net Short APR (%)": round(net_apr, 2),
            "Gross Funding (%)": round(funding_apr, 2),
            "Borrow Fee (%)": round(borrow_apr, 2),
        })

    if not rows:
        print("No markets found.")
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("Net Short APR (%)", ascending=False).reset_index(drop=True)

    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 50)
    print(df.to_string(index=False))
    print("\nSorted: highest profit (Net Short APR) to lowest. Positive = short receives funding.")


if __name__ == "__main__":
    main()
