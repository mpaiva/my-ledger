# Source data

These are the original, unedited account exports that everything on this site is built from.
They are included for reference and verification.

| File | Source | Rows | Notes |
|------|--------|------|-------|
| `coinbase-transactions-2026-06-03.csv` | Coinbase account export | 1,496 transactions | Buys, sells, conversions, rewards, and wallet transfers. Includes the original `User` and column headers. |
| `ledger-wallet-operations-2026-06-03.csv` | Ledger Live (hardware wallet) export | 19 operations (22 rows; some on-chain transfers are listed once per account) | On-chain Send/Receive operations for the BTC, ETH, and XRP wallets, each with its blockchain transaction hash. |
| `coinbase-wallet-tx-hashes.txt` | Coinbase Wallet (self-custody) | 9 transaction hashes | The Coinbase Wallet app offers no CSV export, so these Ethereum tx hashes were provided directly. They document the source of the ~8 ETH later moved into the Ledger. Verify each at `https://etherscan.io/tx/<hash>`. |

Both files were exported on **2026-06-03**.

## How the site uses them

`../build_ledger.py` reads these two files and generates `../ledger-data.js`
(`window.LEDGER_DATA`), which powers both `../ledger.html` (the full ledger) and
`../index.html` (the visual journey). To regenerate after updating a CSV:

```bash
python3 build_ledger.py
```

## Privacy note

Wallet addresses, public keys (`xpub…`), and transaction hashes in these files are
**public information** — they can be used to *view* activity on the blockchain but
**cannot** be used to access or move any funds. No private keys or seed phrases are
present in these exports.
