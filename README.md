# GMX V2 Basis Trade / Funding Arbitrage Tool (Arbitrum)

For **basis trades**: you are **long** the asset (in your wallet or elsewhere) and **short** on GMX. You earn when the GMX short leg **receives** positive funding.

This tool uses the **GMX V2 Arbitrum API** (`arbitrum-api.gmxinfra.io/markets/info`), **GM markets only** (V2, not V1 GLP). Only markets where **short collateral is USDC** (native USDC on Arbitrum). Rates use **30-decimal precision (1e30)**. **Net Short APR** = (Funding APR for Shorts) − (Borrow Fee for Short Token). The **top of the list** = best basis-trade candidates (short receives the most).

## Setup (first time)

```bash
python3 -m venv .venv
```

## Run

```bash
# 1. Activate your virtual environment
source .venv/bin/activate

# 2. Install the necessary libraries
pip install requests pandas

# 3. Run your tool
python3 gmx_funding_tracker.py
```

## Output

- **Market**: GM market name (e.g. ETH/USD [ETH-USDC]).
- **Net Short APR (%)**: From API netRateShort (positive = short receives funding, you earn).
- **Gross Funding (%)** and **Borrow Fee (%)**: Funding and borrow components (1e30 precision). USDC collateral, GM only (V2).
- Sorted: highest profit to lowest.
