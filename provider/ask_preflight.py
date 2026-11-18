#!/usr/bin/env python3
"""Preflight READ-ONLY jalur bertanya (asker) — Dialectica.

Menjawab satu pertanyaan sebelum user memutuskan apa pun soal bertanya:
"BISAKAH kita bertanya lagi hari ini, dan berapa harga persisnya?"

Yang dilakukan (SEMUA read-only, nol create, nol assist, nol charge):
  1. Tarik GET /api/node/scores        -> coins (Wallet/spendable), lifetimeEarned.
  2. Tarik GET /api/node/notifications -> notifikasi ask_fee_charged:
     feeIndex terbesar = n terpakai; jumlah amount = total fee terbayar.
     Setiap amount diverifikasi lawan tangga rumus resmi (self-audit).
  3. Hitung fee pertanyaan berikutnya dari rumus resmi api.md:
         Fee = 10*(n-1)^3 / ((n-1)^3 + 13^3), dibulatkan 4 desimal.
  4. Gerbang affordable: fee berikutnya vs coins.
  5. CETAK VONIS: BISA / TIDAK + alasannya (saldo dan/atau ekonomi).

Exit: 0 = BISA (affordable DAN net >= 0 atau user-override tidak dinilai di sini;
      vonis ekonomi dinyatakan terpisah), 1 = TIDAK, 2 = error tarikan.

Usage:
  python3 ask_preflight.py [--json]
"""
import argparse
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.expanduser(
    "~/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts"))

import trued  # noqa: E402


def fee_for(n: int) -> Decimal:
    """Rumus resmi api.md SS Fee for asking. n=1 persis 0."""
    if n <= 1:
        return Decimal("0")
    x = (n - 1) ** 3
    raw = Decimal(10 * x) / Decimal(x + 13 ** 3)
    return raw.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        scores = trued.call("/api/node/scores")
        notif = trued.call("/api/node/notifications", params={"limit": 200})
    except Exception as e:  # tarikan gagal = jangan menebak
        print(f"PREFLIGHT ERROR: tarikan live gagal: {e}")
        return 2

    coins = Decimal(str(scores.get("coins")))
    lifetime_earned = Decimal(str(scores.get("lifetimeEarned")))
    items = notif.get("notifications") or []
    fee_notes = [n for n in items if n.get("type") == "ask_fee_charged"]

    indices = []
    total_fees = Decimal("0")
    audit_ok = True
    for n in fee_notes:
        c = n.get("content") or {}
        idx = c.get("feeIndex")
        amt = Decimal(str(c.get("amount")))
        indices.append(idx)
        total_fees += amt
        if fee_for(idx) != amt:  # self-audit: amount server vs rumus
            audit_ok = False

    n_used = max(indices) if indices else 0
    next_n = n_used + 1
    next_fee = fee_for(next_n)
    next_net = Decimal("1") - next_fee
    affordable = coins >= next_fee
    shortfall = (next_fee - coins) if not affordable else Decimal("0")
    bisa = affordable  # gerbang server; ekonomi dilaporkan terpisah

    out = {
        "coins": str(coins),
        "lifetimeEarned": str(lifetime_earned),
        "n_used": n_used,
        "fee_notifications": len(fee_notes),
        "total_fees_paid": str(total_fees),
        "fee_audit_ok": audit_ok,
        "next_n": next_n,
        "next_fee": str(next_fee),
        "next_net_without_niu": str(next_net),
        "affordable": affordable,
        "shortfall": str(shortfall),
        "verdict": "BISA" if bisa else "TIDAK",
    }
    if args.json:
        print(json.dumps(out, indent=1))
        return 0 if bisa else 1

    print("=== PREFLIGHT JALUR BERTANYA (read-only) ===")
    print(f"Saldo Wallet (coins)      : {coins} $TRUED")
    print(f"Lifetime Earned           : {lifetime_earned} $TRUED")
    print(f"n terpakai (feeIndex maks): {n_used}  "
          f"({len(fee_notes)} notifikasi fee, total fee terbayar {total_fees})")
    print(f"Self-audit fee vs rumus   : {'COCOK' if audit_ok else 'SELISIH!'}")
    print(f"Pertanyaan berikutnya     : n={next_n}, fee {next_fee}, "
          f"net tanpa NIU {next_net:+}")
    print(f"Gerbang affordable        : "
          f"{'LOLOS' if affordable else 'GAGAL'} "
          f"(fee {next_fee} vs saldo {coins})")
    if not affordable:
        print(f"Kekurangan saldo          : {shortfall} $TRUED harus masuk dulu")
    print(f"VONIS                     : {'BISA' if bisa else 'TIDAK'}")
    if not bisa:
        print("Alasan: saldo di bawah fee pertanyaan berikutnya — create akan "
              "ditolak server (VALIDATION_FAILED) sebelum apa pun ditulis, dan "
              "curiosityToken tidak akan diterbitkan di fase ready.")
    if next_net < 0:
        print("Catatan ekonomi: TANPA bonus NIU (terbukti $0 di akun ini), "
              "tembakan ini bernilai net negatif walau saldo cukup.")
    return 0 if bisa else 1


if __name__ == "__main__":
    sys.exit(main())
