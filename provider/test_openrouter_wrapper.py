#!/usr/bin/env python3
"""Unit tests for openrouter_wrapper (MEKANISME §34). Offline: no API
calls — the wrapper is exercised over the raw Nemotron benchmark outputs
in ~/workspace/research/openrouter/runs/ plus synthetic regen callbacks.

Run: python3 test_openrouter_wrapper.py  (exit 0 = all pass)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openrouter_wrapper import (apply_citation_patch, audit_numbers,
                                mechanical_floor, normalize_mojibake,
                                score_rubric, wrap_answer)

RUNS = os.path.expanduser("~/workspace/research/openrouter/runs")
FAILURES = []


def check(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        FAILURES.append(name)


def load(run):
    with open(os.path.join(RUNS, f"nemotron-{run}.json"),
              encoding="utf-8") as fh:
        return json.load(fh)["text"]


def findings(run):
    text, _, _ = normalize_mojibake(load(run))
    return audit_numbers(text), text


# 1. Mojibake: every raw run is heavily marked, normalisation clears it
#    and never eats legitimate prose (length stays within 15%).
for run in ("r1", "r2", "r3", "r4", "r5"):
    raw = load(run)
    clean, before, after = normalize_mojibake(raw)
    check(f"mojibake {run}", before > 30 and after == 0
          and len(clean) > 0.85 * len(raw),
          f"markers {before}->{after}, chars {len(raw)}->{len(clean)}")
legit = "Harga naik ±5% — selesai ×2, “kutipan” utuh…"
clean, b, a = normalize_mojibake(legit)
check("mojibake teks sah utuh", clean == legit, repr(clean))

# 2. Audit catches the misattributions documented in BENCH-2026-11-10.
f1, _ = findings("r1")
check("audit r1 EIP-2929 cold=100",
      any(f["doc"] == "EIP-2929" and f["value"] == 100 for f in f1))
check("audit r1 EIP-2929 700",
      any(f["doc"] == "EIP-2929" and f["value"] == 700 for f in f1))
check("audit r1 EIP-3860 bukan DELEGATECALL/CALL",
      any(f["doc"] == "EIP-3860" and f["severity"] == "WRONG" for f in f1))
f2, _ = findings("r2")
check("audit r2 EIP-1167 10 byte",
      any(f["doc"] == "EIP-1167" and f["value"] == 10 for f in f2))
check("audit r2 EIP-2028 1 gas/byte",
      any(f["doc"] == "EIP-2028" for f in f2))
f4, _ = findings("r4")
check("audit r4 700 gas (EIP-2929)",
      any(f["doc"] == "EIP-2929" and f["value"] == 700 for f in f4))
f5, _ = findings("r5")
check("audit r5 EIP-3860 surcharge DELEGATECALL",
      sum(1 for f in f5 if f["doc"] == "EIP-3860") >= 2,
      f"{sum(1 for f in f5 if f['doc'] == 'EIP-3860')} temuan")
# Digits of the document names themselves must never be findings.
allf = f1 + f2 + f4 + f5
check("audit tidak menandai nomor dokumen",
      not any(f["value"] in (1167, 1967, 2028, 2929, 3860)
              for f in allf))

# 2b. Precision regressions from drill v1 (2026-11-10): a byte-range
#     offset and a CORRECT EIP-3860 initcode credit must not fire, and
#     the patch must never cut a document's own digits.
fp1 = ("Berbeda dengan stub EIP-1167 yang menyematkan target 20-byte "
       "di bytecode runtime (offset 10-29), beacon proxy membaca alamat "
       "dari kontrak beacon.")
fp2 = ("L2 execution gas sangat murah, membuat DELEGATECALL overhead "
       "(~100-200 gas tambahan per EIP-2929 access list + EIP-3860 "
       "initcode cost) dapat diabaikan.")
check("presisi: offset 10-29 bukan klaim ukuran",
      audit_numbers(fp1) == [])
check("presisi: kredit initcode EIP-3860 yang benar lolos",
      audit_numbers(fp2) == [])

# 3. Patch removes the wrong numbers and invents nothing.
_, t1 = findings("r1")
patched, removed = apply_citation_patch(t1, f1)
check("patch membuang angka salah r1",
      "700" in removed and "100" in removed and len(patched) < len(t1),
      f"dibuang: {removed}")

# 4. Length guard: short draft + one good regen -> OK; bad regen ->
#    GAGAL-LANJUT (must not be sent).
short_raw = load("r2")  # 3.220 kar mentah, di bawah lantai sesudah normalisasi
long_text = ("## 1\n**Lead.** " + "Analisis mekanisme yang diperluas. " * 140
             + "\n\n## 6\nPenutup: yang baru di sini adalah sintesisnya.")
res = wrap_answer(short_raw, regen_fn=lambda instr: long_text)
check("penjaga panjang: regenerasi menyelamatkan",
      res["status"] == "OK" and res["report"]["generations"] == 2
      and res["report"]["chars_final"] >= 4500,
      f"status={res['status']} gen={res['report']['generations']}")
res2 = wrap_answer(short_raw, regen_fn=lambda instr: "tetap pendek")
check("penjaga panjang: tetap pendek = GAGAL-LANJUT",
      res2["status"] == "GAGAL-LANJUT",
      f"status={res2['status']}")
res3 = wrap_answer(short_raw)
check("penjaga panjang: tanpa regen = GAGAL-LANJUT",
      res3["status"] == "GAGAL-LANJUT")

# 5. Rubric auto-score runs and the length item agrees with the floor.
score = score_rubric(res["text"])
check("rubrik (c) konsisten", score["c"][0] == "LOLOS", str(score["c"]))
score_short = score_rubric("pendek")
check("rubrik (c) menolak pendek", score_short["c"][0] == "GAGAL")

# 6. Mechanical floor §45 (K-1/K-2): the gate claim #2 slipped through.
# 6a. Distance semantics are exactly the study's ±150 chars.
_base = "https://example.com/a"  # ends at index 21
for _gap, _want in ((150, 1), (151, 0)):
    _t = _base + " " + "a" * (_gap - 1) + "12345 selesai di sini."
    _f = mechanical_floor(_t)
    check(f"lantai: jarak {_gap} kar -> bound={_want}",
          _f["bound_numbers"] == _want and _f["number_tokens"] == 1,
          f"bound={_f['bound_numbers']}")

# 6b. A citation-rich draft passes every floor; wrap_answer reports the
#     floor as passed, emits no FLOOR finding, and (d) stays LOLOS.
rich = ("Akses dingin 2.600 gas dan hangat 100 gas menurut "
        "https://eips.ethereum.org/EIPS/eip-2929 untuk pola ini. " * 50)
f_rich = mechanical_floor(rich)
check("lantai: draf kaya sitasi lolos semua",
      f_rich["passed"] and f_rich["url_count"] == 50
      and f_rich["bound_ratio"] == 1.0,
      f"url={f_rich['url_count']} dens={f_rich['citation_density']} "
      f"ratio={f_rich['bound_ratio']}")
res_rich = wrap_answer(rich)
check("lantai: wrap_answer kaya -> lantai lolos, (d) LOLOS",
      res_rich["report"]["floor"]["passed"]
      and res_rich["report"]["audit"]["floor_failures"] == 0
      and res_rich["score"]["d"][0] == "LOLOS",
      f"floor={res_rich['report']['floor']['passed']}")

# 6c. Zero-URL draft (the claim #2 species): K-1(a) fails by name, the
#     draft is withheld via FLOOR findings and (d) goes GAGAL.
no_url = ("Analisis panjang tanpa satu pun tautan: mekanisme "
          "dijelaskan dengan kata-kata saja, berulang-ulang tanpa "
          "angka dan tanpa rujukan. " * 45)
res_nu = wrap_answer(no_url)
fl_nu = res_nu["report"]["floor"]
check("lantai: 0 URL -> K-1(a) gagal bernama",
      not fl_nu["passed"] and not fl_nu["checks"]["url"]["passed"]
      and any("K-1(a)" in s and "aktual 0" in s
              for s in fl_nu["failures"]),
      f"failures={fl_nu['failures']}")
check("lantai: 0 URL -> temuan FLOOR menahan draf, (d) GAGAL",
      res_nu["report"]["audit"]["floor_failures"] >= 1
      and res_nu["score"]["d"][0] == "GAGAL",
      f"floor_failures={res_nu['report']['audit']['floor_failures']}")

# 6d. Low bound ratio: one URL, then a long tail of unbound numbers.
low_ratio = ("Sumber awal https://example.com/rujukan untuk konteks. "
             + "Klaim lepas menyebut 12345 dan 67890 tanpa ikatan. "
             * 100)
f_lr = mechanical_floor(low_ratio)
check("lantai: rasio rendah -> K-2 gagal bernama + angka aktual",
      not f_lr["checks"]["ratio"]["passed"]
      and f_lr["bound_ratio"] < 0.30
      and any("K-2" in s and f"{f_lr['bound_ratio']:.3f}" in s
              for s in f_lr["failures"]),
      f"ratio={f_lr['bound_ratio']} bound={f_lr['bound_numbers']}/"
      f"{f_lr['number_tokens']}")

# 6e. Thin citations only: URL present and numbers bound (K-1(a) + K-2
#     pass) but density below 0.5/1.000 -> only K-1(b) fails.
thin = ("Biaya 100 gas dan 200 gas menurut https://example.com/rujukan "
        "ini. " + "Kata pengisi tanpa angka apa pun mengalir terus "
        "menerus. " * 110)
f_thin = mechanical_floor(thin)
check("lantai: sitasi tipis -> hanya K-1(b) gagal",
      f_thin["checks"]["url"]["passed"]
      and f_thin["checks"]["ratio"]["passed"]
      and not f_thin["checks"]["density"]["passed"]
      and len(f_thin["failures"]) == 1
      and "K-1(b)" in f_thin["failures"][0],
      f"dens={f_thin['citation_density']} ratio={f_thin['bound_ratio']}")

print()
print("GAGAL:", FAILURES if FAILURES else "tidak ada")
sys.exit(1 if FAILURES else 0)
