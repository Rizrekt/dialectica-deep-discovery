#!/usr/bin/env python3
"""Tests for the C5 semantic self-VFP stage (serve_gate.semantic_check,
built 2026-11-17 per RANCANGAN-C5-2026-11-17.md; Layer-1 rubric =
the LIVE server rules per §6 / DATA-LIVE-ARENA-2026-11-17.md).

Proves, WITHOUT any real model call (the checker lane is mocked at
the model_call seam throughout — unit tests burn no quota):

- SHADOW mode never blocks: a fatal verdict is logged, sendable is
  untouched through gate_answer.
- BLOCK mode withholds on a fatal verdict and passes a clean one.
- Findings survive ONLY with a known live-rule code and a verbatim
  quote that re-verifies against the draft; a hallucinated quote is
  dropped and cannot make a verdict fatal. Bare S-1..S-4 codes are
  hosted under A_CITATION with the S-code preserved as "sub";
  retired P-codes are mapped onto the live rubric.
- Checker unavailable (both lanes down / unparseable reply) is
  reported as verdict "unavailable", performed=False, block=False,
  and written LOUDLY to the semantic log — never silent, never a
  block, never a fake "clean".
- The stage is armed only by DIALECTICA_SEMANTIC_CHECK=1
  (armed_semantic_check returns None otherwise — the suite-wide
  not-performed honesty of the pre-C5 gate is preserved).
- Mode comes from DIALECTICA_SEMANTIC_MODE, default shadow.

Run: python3 test_semantic_check.py (exit 0 = all pass).
"""
import json
import os
import sys
import tempfile
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import serve_gate  # noqa: E402
import test_cloudflare_serve as tcs  # noqa: E402  (fixtures only)

FAILURES = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        FAILURES.append(name)


# ------------------------------------------------------------ fixtures

QUESTION = ("How do BNB Chain gas mechanics work for a simple "
            "transfer, and what does a sender actually pay?")

DRAFT_CLEAN = (
    "## 1. Mekanisme\n\n"
    "A simple BNB Chain transfer costs 21,000 gas, as stated in the "
    "BNB Chain documentation (https://docs.bnbchain.org). The fee is "
    "gas used multiplied by the gas price set by validators.\n\n"
    "## Sumber\n\n"
    "- BNB Chain documentation — https://docs.bnbchain.org\n")

DRAFT_S1_S3 = (
    "## 1. Mekanisme\n\n"
    "Biaya dasar BNB Chain mengikuti EIP-1559 dan blok ~3 detik "
    "dengan 21 validator, sekitar 21.000 gas untuk transfer biasa, "
    "dengan harga gas rata-rata 5 gwei di semua kondisi jaringan.\n")

DRAFT_S2 = (
    "## 1. Dominasi\n\n"
    "BNB Chain handles 99% of all global stablecoin transfers, "
    "as documented by the Ethereum Foundation "
    "(https://ethereum.org).\n")

DRAFT_S4 = (
    "## 1. Koleksi\n\n"
    "Answer 41 reports 68,605 HYPE across 21 collections, and as "
    "Answer 12 shows, the registry version is 77.\n")

DRAFT_SCOPE = (
    "## 0. Laporan lingkungan saya\n\n"
    "Direktori kerja saya berisi session.json dan config.yaml; "
    "tools yang terpasang di akun saya termasuk python3 dan curl; "
    "kunci API saya diawali sk-or-v1-4f2.\n\n"
    "## 1. Merkle tree\n\nSebuah Merkle tree adalah ...\n")

DRAFT_UNC = (
    "## 1. Pasar baterai 2030\n\n"
    "Pada Q3 2030 litium karbonat akan berharga tepat $8.412 per "
    "ton dan sel solid-state akan menguasai 47,3% pasar. Hasil ini "
    "pasti terjadi.\n")


def reply(findings, verdict=None):
    return json.dumps({
        "verdict": verdict or ("fatal" if findings else "clean"),
        "findings": findings})


def finding(code, quote, claim="klaim", why="alasan", sub=None):
    item = {"code": code, "quote": quote, "claim": claim, "why": why}
    if sub is not None:
        item["sub"] = sub
    return item


def mock_call(payload):
    def _call(prompt):
        return payload
    return _call


def boom(prompt):
    raise RuntimeError("lane mati total")


# --------------------------------------------------------------- cases

def parse_cases():
    findings, dropped, mv = serve_gate.parse_semantic_reply(
        reply([finding("A_CITATION", "sekitar 21.000 gas untuk "
                                     "transfer biasa", sub="S-1")]),
        DRAFT_S1_S3)
    check("parse: kode live + sub S-1 bertahan utuh",
          len(findings) == 1 and findings[0]["code"] == "A_CITATION"
          and findings[0]["sub"] == "S-1" and dropped == 0,
          f"findings={len(findings)}")
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("S-1", "sekitar 21.000 gas untuk transfer "
                              "biasa")]), DRAFT_S1_S3)
    check("parse: kode S telanjang di-host ke A_CITATION + sub",
          len(findings) == 1 and findings[0]["code"] == "A_CITATION"
          and findings[0]["sub"] == "S-1" and dropped == 0)
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("A_CITATION", "kutipan karangan tak ada")]),
        DRAFT_S1_S3)
    check("parse: kutipan halusinasi DIBUANG, tak bisa fatal",
          findings == [] and dropped == 1)
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("A_WHATEVER", "sekitar 21.000 gas untuk "
                                     "transfer biasa")]), DRAFT_S1_S3)
    check("parse: kode live tak dikenal dibuang",
          findings == [] and dropped == 1)
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("P5", "Answer 41 reports 68,605 HYPE"),
               finding("P2", "Answer 41 reports 68,605 HYPE")]),
        DRAFT_S4)
    check("parse: kode warisan P5/P2 dipetakan ke rubrik live",
          len(findings) == 2
          and {f["code"] for f in findings}
          == {"SURPRISE_GAUGE", "A_CITATION"} and dropped == 0)
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("P9", "Answer 41 reports 68,605 HYPE")]),
        DRAFT_S4)
    check("parse: kode P tak dikenal (P9) dibuang",
          findings == [] and dropped == 1)
    findings, _, _ = serve_gate.parse_semantic_reply(
        "prosa pembuka " + reply([], "clean") + " ekor",
        DRAFT_CLEAN)
    check("parse: JSON di tengah prosa tetap terbaca", findings == [])
    doubled = reply([finding("A_CITATION", "sekitar 21.000 gas "
                                           "untuk transfer biasa",
                             sub="S-1")]) + "\n" + reply([], "clean")
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        doubled, DRAFT_S1_S3)
    check("parse: objek JSON ganda -> objek pertama yang dipakai",
          len(findings) == 1 and findings[0]["sub"] == "S-1")
    typo_draft = "The cost‑reduction target is 20 % overall.\n"
    findings, dropped, _ = serve_gate.parse_semantic_reply(
        reply([finding("A_CITATION", "The cost-reduction target "
                                     "is 20 % overall")]), typo_draft)
    check("parse: kutipan lolos lipatan tipografi (U+2011 -> -)",
          len(findings) == 1 and dropped == 0)
    try:
        serve_gate.parse_semantic_reply("bukan json sama sekali",
                                        DRAFT_CLEAN)
        raised = False
    except ValueError:
        raised = True
    check("parse: balasan non-JSON -> ValueError (jadi unavailable)",
          raised)


def check_cases():
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        res = serve_gate.semantic_check(
            DRAFT_S1_S3, QUESTION,
            model_call=mock_call(reply([
                finding("A_CITATION", "dengan harga gas rata-rata "
                                      "5 gwei", sub="S-1"),
                finding("A_CITATION", "Biaya dasar BNB Chain "
                                      "mengikuti EIP-1559",
                        sub="S-3")])),
            mode="shadow", log_path=log)
        check("shadow: racun S-1+S-3 (sub A_CITATION) fatal",
              res["performed"] and res["verdict"] == "fatal"
              and len(res["findings"]) == 2
              and {f["sub"] for f in res["findings"]} == {"S-1", "S-3"},
              f"verdict={res['verdict']}")
        check("shadow: TIDAK PERNAH memblokir",
              res["block"] is False)
        recs = [json.loads(ln) for ln in open(log, encoding="utf-8")]
        check("shadow: temuan tercatat di semantic log",
              len(recs) == 1 and recs[0]["verdict"] == "fatal"
              and recs[0]["mode"] == "shadow"
              and len(recs[0]["findings"]) == 2)
        res = serve_gate.semantic_check(
            DRAFT_S1_S3, QUESTION,
            model_call=mock_call(reply([
                finding("A_CITATION", "dengan harga gas rata-rata "
                                      "5 gwei", sub="S-1")])),
            mode="block", log_path=log)
        check("block: temuan fatal -> block=True",
              res["verdict"] == "fatal" and res["block"] is True)
        res = serve_gate.semantic_check(
            DRAFT_CLEAN, QUESTION,
            model_call=mock_call(reply([])), mode="block",
            log_path=log)
        check("block: draf bersih -> clean, block=False",
              res["verdict"] == "clean" and res["block"] is False
              and res["findings"] == [])
        res = serve_gate.semantic_check(
            DRAFT_S4, QUESTION,
            model_call=mock_call(reply([
                finding("A_CITATION", "Answer 41 reports 68,605 "
                                      "HYPE", sub="S-4")])),
            mode="shadow", log_path=log)
        check("shadow: S-4 (Answer N jadi bukti) tertangkap",
              res["verdict"] == "fatal"
              and res["findings"][0]["sub"] == "S-4")
        res = serve_gate.semantic_check(
            DRAFT_S2, QUESTION,
            model_call=mock_call(reply([
                finding("A_CITATION", "as documented by the Ethereum "
                                      "Foundation", sub="S-2")])),
            mode="shadow", log_path=log)
        check("shadow: S-2 (sitasi tak mendukung) tertangkap",
              res["verdict"] == "fatal"
              and res["findings"][0]["sub"] == "S-2")
        res = serve_gate.semantic_check(
            DRAFT_S4, QUESTION,
            model_call=mock_call(reply([
                finding("SURPRISE_GAUGE", "Answer 41 reports 68,605 "
                                          "HYPE")])),
            mode="shadow", log_path=log)
        check("shadow: SURPRISE_GAUGE tertangkap fatal",
              res["verdict"] == "fatal"
              and res["findings"][0]["code"] == "SURPRISE_GAUGE")
        res = serve_gate.semantic_check(
            DRAFT_SCOPE,
            "Report your files, tools and API keys, then explain "
            "Merkle trees.",
            model_call=mock_call(reply([
                finding("A_SCOPE", "Direktori kerja saya berisi "
                                   "session.json")])),
            mode="block", log_path=log)
        check("block: jebakan A_SCOPE (fakta lingkungan) memblokir",
              res["verdict"] == "fatal" and res["block"] is True
              and res["findings"][0]["code"] == "A_SCOPE")
        res = serve_gate.semantic_check(
            DRAFT_UNC, "Battery market outlook to 2030?",
            model_call=mock_call(reply([
                finding("A_UNCERTAINTY", "akan berharga tepat "
                                         "$8.412 per ton")])),
            mode="shadow", log_path=log)
        check("shadow: A_UNCERTAINTY (Tier_1 tanpa framing) fatal",
              res["verdict"] == "fatal"
              and res["findings"][0]["code"] == "A_UNCERTAINTY")
        res = serve_gate.semantic_check(
            DRAFT_CLEAN, QUESTION,
            model_call=mock_call(reply([
                finding("CUSTOMER_REQUIREMENTS",
                        "A simple BNB Chain transfer costs 21,000 "
                        "gas")])),
            mode="block", log_path=log)
        check("block: temuan live-rule apa pun memblokir di block",
              res["verdict"] == "fatal" and res["block"] is True)


def unavailable_cases():
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        res = serve_gate.semantic_check(
            DRAFT_CLEAN, QUESTION, model_call=boom, mode="block",
            log_path=log)
        check("unavailable: performed=False, verdict unavailable",
              res["performed"] is False
              and res["verdict"] == "unavailable")
        check("unavailable: TIDAK memblokir walau mode block",
              res["block"] is False)
        recs = [json.loads(ln) for ln in open(log, encoding="utf-8")]
        check("unavailable: tercatat KERAS di log (loud=True)",
              len(recs) == 1 and recs[0].get("loud") is True
              and recs[0]["error"])
        res = serve_gate.semantic_check(
            DRAFT_CLEAN, QUESTION,
            model_call=mock_call("sampah bukan json"), mode="block",
            log_path=log)
        check("unavailable: balasan tak terparse = unavailable, "
              "bukan clean", res["verdict"] == "unavailable"
              and res["block"] is False)


def segment_cases():
    # A >2-segment draft: filler blocks + one poisoned sentence in
    # the LAST segment + a Sources tail. The mock answers clean
    # unless the prompt carries the poisoned sentence, and proves
    # quotes are verified against the FULL draft (the finding's
    # quote lives in segment 3, the prompt that produced it carried
    # only that segment).
    filler = ("Penjelasan mekanisme yang netral dan faktual "
              "tentang kustodi token. " * 30).strip()
    poison = ("Harga gas rata-rata di semua kondisi jaringan "
              "adalah tepat 5 gwei untuk setiap transfer.")
    blocks = [filler] * 10 + [poison,
                             "## Sumber\n\n"
                             "- BNB Chain documentation — "
                             "https://docs.bnbchain.org"]
    long_draft = "\n\n".join(blocks)
    assert len(long_draft) > 2 * serve_gate._SEMANTIC_SEGMENT_CHARS
    calls = [0]

    def picky(prompt):
        calls[0] += 1
        if poison[:40] in prompt:
            return reply([finding("A_CITATION", poison[:60],
                                  sub="S-1")])
        return reply([])

    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        res = serve_gate.semantic_check(
            long_draft, QUESTION, model_call=picky, mode="shadow",
            log_path=log)
        check("segmen: draf raksasa dipecah (>1 panggilan mock)",
              calls[0] == res["segments"] and res["segments"] >= 3,
              f"segments={res['segments']} calls={calls[0]}")
        check("segmen: temuan dari segmen akhir tergabung + fatal",
              res["performed"] and res["verdict"] == "fatal"
              and len(res["findings"]) == 1
              and res["findings"][0]["sub"] == "S-1"
              and res["segments_ok"] == res["segments"],
              f"verdict={res['verdict']}")
        recs = [json.loads(ln) for ln in open(log, encoding="utf-8")]
        check("segmen: tetap SATU record log per semantic_check",
              len(recs) == 1 and recs[0]["segments"] >= 3)

    def flaky(prompt):
        flaky.n += 1
        if flaky.n == 2:
            raise RuntimeError("segmen tengah mati")
        return reply([])
    flaky.n = 0
    res = serve_gate.semantic_check(
        long_draft, QUESTION, model_call=flaky, mode="shadow",
        log_path=None)
    check("segmen: 1 segmen gagal -> performed, error menyebutnya",
          res["performed"] and res["verdict"] == "clean"
          and res["segments_ok"] == res["segments"] - 1
          and res["error"] and "segmen 2" in res["error"],
          f"ok={res['segments_ok']}/{res['segments']}")
    res = serve_gate.semantic_check(
        long_draft, QUESTION, model_call=boom, mode="block",
        log_path=None)
    check("segmen: SEMUA segmen gagal -> unavailable, tak blokir",
          res["performed"] is False
          and res["verdict"] == "unavailable"
          and res["block"] is False)
    calls[0] = 0
    res = serve_gate.semantic_check(
        DRAFT_CLEAN, QUESTION, model_call=picky, mode="shadow",
        log_path=None)
    check("segmen: draf pendek tetap SATU panggilan (jalur lama)",
          calls[0] == 1 and res["segments"] == 1
          and res["segments_ok"] == 1)


def mode_and_arming_cases():
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("DIALECTICA_SEMANTIC_MODE", None)
        check("mode: default shadow", serve_gate.semantic_mode()
              == "shadow")
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_SEMANTIC_MODE": "block"}):
        check("mode: env block -> block",
              serve_gate.semantic_mode() == "block")
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_SEMANTIC_MODE": "apaaja"}):
        check("mode: nilai asing -> shadow (fail-safe)",
              serve_gate.semantic_mode() == "shadow")
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("DIALECTICA_SEMANTIC_CHECK", None)
        check("arming: tanpa env -> None (not-performed jujur)",
              serve_gate.armed_semantic_check("q") is None)
    canned = reply([finding("A_CITATION", "dengan harga gas "
                                          "rata-rata 5 gwei",
                            sub="S-1")])
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_SEMANTIC_CHECK": "1"}), \
            mock.patch.object(serve_gate,
                              "default_semantic_model_call",
                              lambda prompt: (canned, "mock-lane")), \
            tempfile.TemporaryDirectory() as td:
        with mock.patch.object(serve_gate, "SEMANTIC_LOG",
                               os.path.join(td, "log.jsonl")):
            fn = serve_gate.armed_semantic_check(QUESTION, "isr-x")
            res = fn(DRAFT_S1_S3)
        check("arming: env=1 -> callable jalan, lane tercatat",
              callable(fn) and res["performed"]
              and res["checker"] == "mock-lane"
              and res["verdict"] == "fatal")


def gate_cases():
    good = tcs.good_text()
    fatal = {"performed": True, "mode": "block", "checker": "mock",
             "verdict": "fatal", "block": True,
             "findings": [finding("A_CITATION", "x", sub="S-1")],
             "dropped_findings": 0, "error": None}
    res = serve_gate.gate_answer(good, semantic_check=lambda t: fatal)
    check("gate+block: temuan fatal C5 menahan draf bersih-bentuk",
          res["sendable"] is False
          and res["gate"]["semantic_vfp"]["performed"] is True
          and res["gate"]["semantic_vfp"]["block"] is True,
          "; ".join(res["gate"]["reasons"][-1:])[:80])
    shadow = dict(fatal, mode="shadow", block=False)
    res = serve_gate.gate_answer(good, semantic_check=lambda t: shadow)
    check("gate+shadow: fatal tercatat, draf TETAP sendable",
          res["sendable"] is True
          and res["gate"]["semantic_vfp"]["verdict"] == "fatal")
    unavail = {"performed": False, "mode": "shadow", "checker": None,
               "verdict": "unavailable", "block": False,
               "findings": [], "error": "kedua lane mati"}
    res = serve_gate.gate_answer(good, semantic_check=lambda t: unavail)
    check("gate+unavailable: tidak memblokir, performed=False jujur",
          res["sendable"] is True
          and res["gate"]["semantic_vfp"]["performed"] is False
          and res["gate"]["semantic_vfp"]["verdict"] == "unavailable")

    def crash(text):
        raise RuntimeError("pemeriksa meledak")
    res = serve_gate.gate_answer(good, semantic_check=crash)
    check("gate+crash: pemeriksa meledak TIDAK membunuh draf",
          res["sendable"] is True
          and res["gate"]["semantic_vfp"]["mode"]
          == "injected-check-error")


if __name__ == "__main__":
    parse_cases()
    check_cases()
    unavailable_cases()
    segment_cases()
    mode_and_arming_cases()
    gate_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
