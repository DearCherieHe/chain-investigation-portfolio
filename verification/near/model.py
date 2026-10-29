"""Evidence model for the bounded NEAR Intents BNB Chain case study."""
from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).parent / "data" / "withdrawals.csv"
VAULT = "0x233c5370ccfb3cd7409d9a3fb98ab94de94cb4cd"
RECIPIENT = "0x09fd1f5d9f185067a92493e43aa259ea4ab3ad37"
USDT_BSC = "0x55d398326f99059ff775485246999027b3197955"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def load_rows(path: Path = DATA) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len({r["tx_hash"].lower() for r in rows}) != len(rows):
        raise ValueError("Duplicate transaction hash")
    for row in rows:
        if len(row["tx_hash"]) != 66 or not row["tx_hash"].startswith("0x"):
            raise ValueError(f"Invalid hash: {row['id']}")
        if Decimal(row["amount_usdt"]) <= 0:
            raise ValueError(f"Invalid amount: {row['id']}")
    return rows


def total(rows: list[dict[str, str]], phase: str) -> Decimal:
    return sum((Decimal(r["amount_usdt"]) for r in rows if r["phase"] == phase), Decimal(0))


def decode_usdt_transfers(receipt: dict) -> list[tuple[str, str, Decimal]]:
    """Decode BEP-20 Transfer logs for BSC USDT from a transaction receipt."""
    result = []
    for log in receipt.get("logs", []):
        topics = log.get("topics", [])
        if (log.get("address", "").lower() != USDT_BSC or len(topics) != 3
                or topics[0].lower() != TRANSFER_TOPIC):
            continue
        sender = "0x" + topics[1][-40:].lower()
        recipient = "0x" + topics[2][-40:].lower()
        amount = Decimal(int(log["data"], 16)) / Decimal(10**18)
        result.append((sender, recipient, amount))
    return result
