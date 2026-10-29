"""Verify the seven documented BSC withdrawal transactions via JSON-RPC.

Set BSC_RPC_URL to a BNB Smart Chain mainnet endpoint, then run this script.
Raw receipts are saved under data/rpc/ and ignored by git.
"""
from __future__ import annotations

import json
import os
import urllib.request
from decimal import Decimal
from pathlib import Path

from model import RECIPIENT, VAULT, decode_usdt_transfers, load_rows


def call(url: str, method: str, tx_hash: str) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": [tx_hash], "id": 1}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        reply = json.load(response)
    if reply.get("error") or not reply.get("result"):
        raise RuntimeError(f"{method} failed: {tx_hash}: {reply.get('error')}")
    return reply["result"]


def main() -> None:
    url = os.environ.get("BSC_RPC_URL")
    if not url:
        raise SystemExit("Set BSC_RPC_URL to a BNB Smart Chain mainnet JSON-RPC endpoint")
    out = Path(__file__).parent / "data" / "rpc"
    out.mkdir(exist_ok=True)
    for row in load_rows():
        tx = call(url, "eth_getTransactionByHash", row["tx_hash"])
        receipt = call(url, "eth_getTransactionReceipt", row["tx_hash"])
        if tx["hash"].lower() != row["tx_hash"].lower() or receipt["status"] != "0x1":
            raise RuntimeError(f"Hash/status mismatch for {row['id']}")
        transfers = decode_usdt_transfers(receipt)
        matching = [amount for sender, recipient, amount in transfers if sender == VAULT and recipient == RECIPIENT]
        if sum(matching, Decimal(0)) != Decimal(row["amount_usdt"]):
            raise RuntimeError(f"USDT transfer mismatch for {row['id']}: {matching}")
        (out / f"{row['id']}.json").write_text(json.dumps({"transaction": tx, "receipt": receipt}, indent=2), encoding="utf-8")
        print(f"{row['id']}: {row['amount_usdt']} USDT verified")


if __name__ == "__main__":
    main()
