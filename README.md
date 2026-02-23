# GMX V2 Short Funding Scanner

A funding-rate scanner for **GMX V2** (Arbitrum) focused on **basis trade** and **delta-neutral** strategies. It ranks markets by net short funding so you can spot the best opportunities to run a short on GMX while holding the asset long elsewhere and earning funding.

## What it does

- Fetches live market data from the [GMX V2 Arbitrum API](https://arbitrum-api.gmxinfra.io/markets/info).
- Shows **Net Short APR** (using the API’s `netRateShort`), plus **Gross Funding** and **Borrow Fee**, with 30-decimal precision (1e30).
- Filters to **GM markets only** (V2), with **USDC** as short collateral.
- Sorts from **highest to lowest** net short APR so the best funding opportunities appear first.

**Basis trade / delta-neutral use case:** You are long the asset (e.g. in a wallet or CEX) and short the same asset on GMX. You earn when the short leg **receives** positive funding; the scanner helps you find where that funding is highest.

## Requirements

- Python 3.8+
- `requests`, `pandas`

## How to run

**1. Clone the repo and go to the project folder**

```bash
git clone https://github.com/pnideck/gmx-funding-scanner.git
cd gmx-funding-scanner
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the scanner**

```bash
python3 gmx_funding_tracker.py
```

## Output

The script prints a table with:

| Column | Description |
|--------|-------------|
| **Market** | GM market name (e.g. `ETH/USD [ETH-USDC]`). |
| **Net Short APR (%)** | Net funding for shorts (positive = short receives funding). |
| **Gross Funding (%)** | Funding rate component (1e30). |
| **Borrow Fee (%)** | Borrow fee component (1e30). |

Rows are sorted by **Net Short APR** descending (best opportunities at the top).

## Project status

**This project is under active development.** Features, data sources, and output format may change. Use at your own risk and always verify numbers against [GMX](https://gmx.io) before trading.

## License

See the repository for license information.
