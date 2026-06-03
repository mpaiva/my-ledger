# My Crypto Journey 🪙

An interactive, plain-language tracker showing how my cryptocurrency moved between
**Coinbase** (an online exchange) and my **Ledger hardware wallet** (a physical
vault for crypto) — from 2022 to 2026. Every transfer links to its public record
on the blockchain so anyone can verify it.

👉 **Live page:** `https://mpaiva.github.io/my-ledger/` (after enabling Pages — see below)

## What's inside

- **The big picture** — a visual map of the round trip: Coinbase → Ledger → Coinbase → bank.
- **Every move, step by step** — a filterable timeline (Bitcoin / Ethereum / XRP), each
  card written in everyday language with value-then vs. value-today and a one-click
  **"View on blockchain"** link.
- **Plain-English glossary** of crypto terms.

It's a single, self-contained `index.html` — no build step, no dependencies.

## The money trail

| Coin | Bought & moved to Ledger | Cashed back out |
|------|--------------------------|-----------------|
| ₿ Bitcoin | ~1.20 BTC (2022 & 2024) | ~1.19 BTC sent back to Coinbase (2026) → converted to USD → bank |
| Ξ Ethereum | ~13.6 ETH (2022 & 2024) | still held in Ledger |
| ✕ XRP | ~4,328 XRP (2025) | still held in Ledger |

Blockchain explorers used: [mempool.space](https://mempool.space) (BTC),
[Etherscan](https://etherscan.io) (ETH), [XRPScan](https://xrpscan.com) (XRP).

## How to publish on GitHub Pages

1. Push this branch (or merge it to `main`).
2. On GitHub: **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Pick the branch and the **/ (root)** folder, then **Save**.
5. Wait ~1 minute — your page will be live at `https://mpaiva.github.io/my-ledger/`.

## Notes

- Wallet addresses shown are **public** and safe to share — they cannot move any funds.
- Tiny spam/dust tokens were filtered out for clarity.
- "Value then" = price on the transfer date; "value today" = a later snapshot from the export.
