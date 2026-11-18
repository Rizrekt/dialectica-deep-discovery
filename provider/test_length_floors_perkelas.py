#!/usr/bin/env python3
"""Tests for the per-class length floor — QUALITY (c)-PK1
(keputusan user 2026-11-17 08:59; laporan QUALITY-PER-KELAS-2026-11-17.md).

Proves, offline:
- the floor table itself: PIONEER 1.717 (= p10 of the run-11
  newly-paid Pioneer winners, n=35), MARATHON keeps the operative
  4.500 (never loosened downward), explicit GENERAL/INNOVATOR use
  the QUALITY v3 document floor 3.000, and NO/unknown class context
  keeps the exact pre-PK1 operative behaviour (4.500);
- a Pioneer draft between the new floor and 3.000 chars now passes
  the length gate end-to-end (wrapper status OK, serve gate
  sendable, Vyce pipeline pass-through) where it previously failed;
- a general draft below 3.000 still fails; a Marathon draft is not
  loosened; K-1/K-2 constants are untouched (K-2 stays 0.30).

Run: python3 test_length_floors_perkelas.py  (exit 0 = all pass)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import serve_gate  # noqa: E402
import vyce_serve_common as vsc  # noqa: E402
from openrouter_wrapper import (FLOOR_MIN_BOUND_RATIO,
                                FLOOR_MIN_CITATION_DENSITY,
                                FLOOR_MIN_URLS, length_band_for_class,
                                length_floor_for_class, score_rubric,
                                wrap_answer)

FAILURES = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        FAILURES.append(name)


_BASE = ("Akses dingin 2.600 gas dan hangat 100 gas menurut "
         "https://eips.ethereum.org/EIPS/eip-2929 untuk pola ini. ")
_FILLER = "Analisis mekanisme lanjutan tanpa angka baru. "


def draft_of(chars):
    """Citation-rich draft of exactly `chars` characters: the bound
    EIP-2929 numbers repeat in the head; the tail is number-free
    filler, so the §45 K-1/K-2 floor passes on its own merits."""
    text = _BASE * 12
    while len(text) < chars:
        text += _FILLER
    return text[:chars]


# ------------------------------------------------------------- the table

def table_cases():
    check("lantai PIONEER = 1.717 (p10 bayar-baru n=35)",
          length_floor_for_class("PIONEER") == (1717, "PIONEER"))
    check("lantai 'pioneer' (huruf kecil) sama",
          length_floor_for_class("pioneer") == (1717, "PIONEER"))
    check("lantai MARATHON = 4.500 operatif (tidak dilonggarkan)",
          length_floor_for_class("MARATHON") == (4500, "MARATHON"))
    check("lantai P+M diperlakukan sebagai MARATHON",
          length_floor_for_class("P+M") == (4500, "MARATHON"))
    check("marathon=True warisan -> MARATHON 4.500",
          length_floor_for_class(marathon=True) == (4500, "MARATHON"))
    check("lantai GENERAL eksplisit = 3.000 (dokumen v3)",
          length_floor_for_class("GENERAL") == (3000, "GENERAL"))
    check("lantai INNOVATOR = 3.000 (ikut umum — tak ada data sendiri)",
          length_floor_for_class("INNOVATOR") == (3000, "INNOVATOR"))
    check("tanpa konteks kelas = perilaku lama persis (4.500)",
          length_floor_for_class() == (4500, None))
    check("kelas tak dikenal = perilaku lama persis (4.500)",
          length_floor_for_class("NO-PAY") == (4500, None))
    check("pita PIONEER = 3.435–7.297 (q1–q3 kohort inti, median 4.094)",
          length_band_for_class("PIONEER") == (3435, 7297))
    check("pita MARATHON = 10.000–12.000",
          length_band_for_class("MARATHON") == (10000, 12000))
    check("pita bawaan = 4.500–8.000",
          length_band_for_class() == (4500, 8000))
    check("K-1/K-2 TIDAK disentuh (K-2 tetap 0,30)",
          FLOOR_MIN_URLS == 1 and FLOOR_MIN_CITATION_DENSITY == 0.5
          and FLOOR_MIN_BOUND_RATIO == 0.30,
          f"url={FLOOR_MIN_URLS} dens={FLOOR_MIN_CITATION_DENSITY} "
          f"rasio={FLOOR_MIN_BOUND_RATIO}")


# ------------------------------------------------------------- rubric (c)

def rubric_cases():
    s = score_rubric("x" * 2500, target_class="PIONEER")
    check("rubrik (c): Pioneer 2.500 kar LOLOS (dulu GAGAL)",
          s["c"][0] == "LOLOS" and "1717" in s["c"][1], s["c"][1])
    s = score_rubric("x" * 1716, target_class="PIONEER")
    check("rubrik (c): Pioneer 1.716 kar GAGAL (di bawah p10)",
          s["c"][0] == "GAGAL", s["c"][1])
    s = score_rubric("x" * 2500, target_class="GENERAL")
    check("rubrik (c): umum 2.500 kar GAGAL (di bawah 3.000)",
          s["c"][0] == "GAGAL", s["c"][1])
    s = score_rubric("x" * 3000, target_class="GENERAL")
    check("rubrik (c): umum 3.000 kar LOLOS",
          s["c"][0] == "LOLOS", s["c"][1])
    s = score_rubric("x" * 2500)
    check("rubrik (c): tanpa kelas 2.500 kar GAGAL (perilaku lama)",
          s["c"][0] == "GAGAL", s["c"][1])
    s = score_rubric("x" * 2500, target_class="MARATHON")
    check("rubrik (c): Marathon 2.500 kar GAGAL (tidak dilonggarkan)",
          s["c"][0] == "GAGAL", s["c"][1])
    s = score_rubric("x" * 4600, target_class="MARATHON")
    check("rubrik (c): Marathon 4.600 kar LOLOS lantai (pita kelas "
          "10–12 rb = patokan, bukan pintu)",
          s["c"][0] == "LOLOS" and "10000" in s["c"][1], s["c"][1])


# ------------------------------------------------------------- wrapper

def wrapper_cases():
    pioneer = draft_of(2500)
    check("fixture Pioneer tepat 2.500 kar", len(pioneer) == 2500)

    calls = []
    res = wrap_answer(pioneer, target_class="PIONEER",
                      regen_fn=lambda instr: calls.append(instr)
                      or draft_of(6000))
    check("wrapper: Pioneer 2.500 -> OK, TANPA regenerasi",
          res["status"] == "OK" and res["report"]["generations"] == 1
          and not calls,
          f"status={res['status']} gen={res['report']['generations']}")
    check("wrapper: laporan mencatat kelas + lantai Pioneer",
          res["report"]["target_class"] == "PIONEER"
          and res["report"]["length_floor"] == 1717,
          f"{res['report']['target_class']}/"
          f"{res['report']['length_floor']}")

    seen = []
    res = wrap_answer(draft_of(1500), target_class="PIONEER",
                      regen_fn=lambda instr: seen.append(instr)
                      or pioneer)
    check("wrapper: Pioneer 1.500 -> regen 1x dgn instruksi lantai "
          "kelas -> OK",
          res["status"] == "OK" and res["report"]["generations"] == 2
          and seen and "1.717" in seen[0],
          f"status={res['status']} gen={res['report']['generations']}")

    res = wrap_answer(pioneer)
    check("wrapper: tanpa kelas 2.500 -> GAGAL-LANJUT (perilaku lama)",
          res["status"] == "GAGAL-LANJUT"
          and res["report"]["length_floor"] == 4500,
          f"status={res['status']}")
    res = wrap_answer(pioneer, target_class="GENERAL")
    check("wrapper: umum 2.500 -> GAGAL-LANJUT (di bawah 3.000)",
          res["status"] == "GAGAL-LANJUT", f"status={res['status']}")
    res = wrap_answer(draft_of(3200), target_class="GENERAL")
    check("wrapper: umum 3.200 -> OK",
          res["status"] == "OK", f"status={res['status']}")
    res = wrap_answer(pioneer, target_class="MARATHON")
    check("wrapper: Marathon 2.500 -> GAGAL-LANJUT (tidak dilonggarkan)",
          res["status"] == "GAGAL-LANJUT", f"status={res['status']}")


# ------------------------------------------------------------- serve gate

def gate_cases():
    pioneer = draft_of(2500)
    res = serve_gate.gate_answer(pioneer, target_class="PIONEER")
    check("gerbang serve: Pioneer 2.500 -> SENDABLE",
          res["sendable"] is True,
          f"status={res['status']} alasan="
          f"{res['gate']['reasons'][:1]}")
    res = serve_gate.gate_answer(pioneer)
    check("gerbang serve: tanpa kelas 2.500 -> ditahan (perilaku lama)",
          res["sendable"] is False and res["status"] == "GAGAL-LANJUT",
          f"status={res['status']}")

    res = vsc.vyce_pipeline(
        "Pertanyaan tentang wallet dan klon proxy.",
        "00000000-0000-0000-0000-000000000000",
        generate_fn=lambda prompt, isr_id=None: pioneer,
        target_class="PIONEER")
    check("pipa Vyce: target_class PIONEER diteruskan ke gerbang "
          "-> SENDABLE",
          res["sendable"] is True, f"status={res['status']}")
    res = vsc.vyce_pipeline(
        "Pertanyaan tentang wallet dan klon proxy.",
        "00000000-0000-0000-0000-000000000000",
        generate_fn=lambda prompt, isr_id=None: pioneer)
    check("pipa Vyce: tanpa kelas -> ditahan seperti lama",
          res["sendable"] is False, f"status={res['status']}")


def main():
    table_cases()
    rubric_cases()
    wrapper_cases()
    gate_cases()
    print()
    print(f"HASIL: {CHECKS[0] - len(FAILURES)}/{CHECKS[0]} lolos")
    print("GAGAL:", FAILURES if FAILURES else "tidak ada")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
