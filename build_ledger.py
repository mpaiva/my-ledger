#!/usr/bin/env python3
"""Parse Coinbase + Ledger CSV exports into a single unified ledger dataset
embedded as a JS file for the static GitHub Pages site."""
import csv, json, re, os

UP = "/root/.claude/uploads/4a2304f7-4c80-481c-a148-df39f4b77076"
COINBASE = os.path.join(UP, "9c73985d-coinbasealltransactions2026.06.03.csv")
LEDGER   = os.path.join(UP, "f7691392-ledgerwalletoperations2026.06.03.csv")
OUT      = "/home/user/my-ledger/ledger-data.js"

def money(s):
    """'$1,234.56' -> 1234.56 ; '' -> None"""
    if s is None: return None
    s = s.strip().replace("$", "").replace(",", "")
    if s in ("", "-"): return None
    try: return float(s)
    except ValueError: return None

def num(s):
    if s is None: return None
    s = s.strip().replace(",", "")
    if s == "": return None
    try: return float(s)
    except ValueError: return None

# ---- address explorer mapping ----
def addr_explorer(asset, addr):
    """Return an explorer URL for a wallet address, or None if not linkable."""
    if not addr: return None
    a = addr.strip()
    # Coinbase placeholders / contact names / internal tags -> not linkable
    if a == "" or " " in a or a.lower().startswith("coinbase") or ":::ucl:::" in a and a.startswith("coinbasebase"):
        # but stellar memo form "G...:::ucl:::123" should be stripped, handled below
        if ":::ucl:::" not in a:
            return None
    base = a.split(":::")[0]  # strip stellar/eos memo tags
    # decide by address shape, then asset
    if re.fullmatch(r"(bc1|[13])[a-zA-HJ-NP-Z0-9]{20,}", base):
        return "https://mempool.space/address/" + base
    if base.startswith("0x") and len(base) == 42:
        return "https://etherscan.io/address/" + base
    if re.fullmatch(r"r[1-9A-HJ-NP-Za-km-z]{24,34}", base):
        return "https://xrpscan.com/account/" + base
    if re.fullmatch(r"G[A-Z2-7]{55}", base):
        return "https://stellar.expert/explorer/public/account/" + base
    if base.startswith("ltc1") or (base.startswith("L") and len(base) > 25) or base.startswith("M"):
        return "https://litecoinspace.org/address/" + base
    # fall back by asset for anything we don't recognize as a real chain address
    return None

# ---- tx hash explorer mapping (Ledger ops have real hashes) ----
def tx_explorer(asset, h):
    if not h: return None
    h = h.strip()
    a = asset.upper()
    if a == "BTC": return "https://mempool.space/tx/" + h
    if a in ("ETH", "WETH", "HEX", "USDC", "USDT", "MATIC", "MANA", "SHIB", "GRT", "SKL"):
        return "https://etherscan.io/tx/" + h
    if a == "XRP": return "https://xrpscan.com/tx/" + h
    if a == "XLM": return "https://stellar.expert/explorer/public/tx/" + h
    if a == "SOL": return "https://solscan.io/tx/" + h
    if a == "LTC": return "https://litecoinspace.org/tx/" + h
    return None

rows = []

# ---------------- Coinbase ----------------
with open(COINBASE, newline="") as f:
    reader = csv.reader(f)
    header_seen = False
    for r in reader:
        if not r or len(r) < 5:
            continue
        if r[0] == "ID" or r[0] == "Transactions" or r[0] == "User":
            header_seen = True
            continue
        if not header_seen:
            continue
        (txid, ts, ttype, asset, qty, pcur, price, subtotal, total, fees,
         notes, sender, recip) = (r + [""]*13)[:13]
        qtyf = num(qty)
        usd  = money(total) if money(total) is not None else money(subtotal)
        feef = money(fees)
        # direction: negative qty = outflow from Coinbase
        is_out = (qtyf is not None and qtyf < 0)
        link = None
        if ttype in ("Send",):
            link = addr_explorer(asset, recip)
        elif ttype in ("Receive",):
            link = addr_explorer(asset, recip) or addr_explorer(asset, sender)
        rows.append({
            "date": ts.replace(" UTC", "").strip(),
            "venue": "Coinbase",
            "type": ttype,
            "asset": asset,
            "qty": qtyf,
            "usd": usd,
            "fee": feef,
            "note": notes.strip(),
            "link": link,
            "onchain": link is not None,
        })

# ---------------- Ledger ----------------
seen = set()
with open(LEDGER, newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
        h = (r.get("Operation Hash") or "").strip()
        asset = (r.get("Currency Ticker") or "").strip()
        op = (r.get("Operation Type") or "").strip()  # IN / OUT
        key = (h, op, r.get("Operation Amount"))
        if key in seen:
            continue
        seen.add(key)
        amt = num(r.get("Operation Amount"))
        usd = money(r.get("Countervalue at Operation Date"))
        usd_now = money(r.get("Countervalue at CSV Export"))
        fee = num(r.get("Operation Fees"))
        ts = (r.get("Operation Date") or "").replace("T", " ").replace(".000Z", "").strip()
        qty = amt if op == "IN" else (-(amt) if amt is not None else None)
        rows.append({
            "date": ts,
            "venue": "Ledger wallet",
            "type": "Receive" if op == "IN" else "Send",
            "asset": asset,
            "qty": qty,
            "usd": usd,
            "usd_now": usd_now,
            "fee": fee,
            "note": (r.get("Account Name") or "").strip(),
            "link": tx_explorer(asset, h),
            "onchain": True,
            "hash": h,
        })

# sort newest first
def keyf(x):
    return x["date"]
rows.sort(key=keyf, reverse=True)

with open(OUT, "w") as f:
    f.write("window.LEDGER_DATA = ")
    json.dump(rows, f, ensure_ascii=False)
    f.write(";\n")

# quick stats
print("total rows:", len(rows))
from collections import Counter
print("by venue:", Counter(x["venue"] for x in rows))
print("with links:", sum(1 for x in rows if x["link"]))
print("date range:", min(x["date"] for x in rows), "->", max(x["date"] for x in rows))
print("file bytes:", os.path.getsize(OUT))
