#!/usr/bin/env python3
"""Satu ronde ulang TERBATAS untuk pasangan kontrol positif A/B
konteks kebaruan (2026-11-17): di run utama, kedua run
dengan-konteks untuk draf kontrol gugur di lane pemeriksa
(reasoning-overflow Nemotron-Vyce + balasan non-JSON), jadi sel
penentu kontrol tidak pernah terbaca. Ronde ini hanya menjalankan
ulang draf kontrol ISR pertama (2 rep x 2 kondisi, lane Vyce-dulu
yang sama), tanpa generasi baru (nol cap terbakar), dan menulis
hasilnya sebagai blok terpisah di results.json ("control_retry").
Apa pun hasilnya = final untuk A/B ini.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_novelty_ab as ab  # noqa: E402

CONTROL = os.path.join(ab.OUT_DIR, "control-paraphrase-a6148000.txt")


def main():
    with open(ab.PACK, encoding="utf-8") as fh:
        pack = json.load(fh)
    entry = pack[0]
    print("arm vyce:", ab.cal.arm_vyce_fallback(), flush=True)
    with open(CONTROL, encoding="utf-8") as fh:
        control = fh.read()
    rec = ab.run_checks("kontrol-parafrase-retry", control, entry,
                        reps=2)
    with open(ab.RESULTS, encoding="utf-8") as fh:
        results = json.load(fh)
    results["control_retry"] = rec
    with open(ab.RESULTS, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print(f"retry tercatat -> {ab.RESULTS}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
