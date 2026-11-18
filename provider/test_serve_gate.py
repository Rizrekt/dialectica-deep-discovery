#!/usr/bin/env python3
"""Tests for the shared SERVE quality gate (serve_gate.py, built
2026-11-15 after the falsified serve answer f0bb3586, MEKANISME §82).

Proves, WITHOUT launching any serve or taking any real job:
- LIVENESS: the three-field filter (KULIT-SISTEM edge #2) — the
  stale-flag pattern (concluded, every endsAt past) is DEAD; a new
  round with a future endsAt is LIVE even on a concluded question;
  a plain open question is LIVE; a settled one is DEAD; a marathon
  question with no provable future round is DEAD (fail-closed); a
  failed detail fetch closes the prepare gate; the row's own fields
  can still prove death when no fetch is armed.
- THINKING-TRACE: a reconstruction of the f0bb3586 pattern (reasoning
  preamble + uncertainty monologue + plan-not-answer closing) is
  detected; the proven claim fixture is not; a dominant raw code
  dump and a plan closing each fire on their own.
- GATE: the claim fixture passes sendable through gate_answer; the
  same fixture dressed as a thinking trace is WITHHELD by the trace
  layer alone (floor clean, format LOLOS); a 0-URL draft is withheld
  by floor K-1(a); the semantic self-VFP is reported NOT performed
  (mechanical gate only — the honest lab-facing declaration).
- E3 EVASIVE SOURCE CLOSING (ADOPTED, lab 2026-11-15): all four
  historical falsified serve texts are flagged by the E3 layer (their
  shared verbatim closing); the same closing on the clean fixture is
  withheld by the E3 layer ALONE (bare wrapper passes it); deferral
  language in the BODY and an explicit-phrase quote in the body do
  NOT fire (scan bounded to closing + source sections, LAB-E3 §1.6);
  a clean text with an explicit source section does NOT fire; an
  evasion inside a mid-text source section DOES fire.
- CLOUDFLARE §39 PREPARE (armed fetchers): stale target -> pass-over
  with ZERO generations; failed fetch -> pass-over, zero
  generations; live target -> prepared as before.
- VYCE SERVE (the previously ungated lane): prepare passes over a
  stale target without generating, withholds a trace draft without
  caching, and caches a clean draft; the provider serves the cache,
  blocks a proven-dead fallback target, withholds a trace fallback,
  and passes a clean fallback.
- RUN_SERVE: the Vyce serve dry-run shows the gated hook wiring;
  the Vyce --answer dry-run shows NO serve hooks (claim path
  untouched).

Generation and detail fetches are stubbed throughout; run_serve is
only ever run with --dry-run. Run: python3 test_serve_gate.py
(exit 0 = all pass).
"""
import contextlib
import io
import json
import os
import subprocess
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_provider as cp  # noqa: E402
import cloudflare_serve_common as csc  # noqa: E402
import cloudflare_serve_prepare as cf_prep  # noqa: E402
import cloudflare_serve_provider as cf_provider  # noqa: E402
import serve_gate  # noqa: E402
import test_cloudflare_serve as tcs  # noqa: E402  (fixtures only)
import vyce_serve_common as vsc  # noqa: E402
import vyce_serve_prepare as vyce_prep  # noqa: E402
import vyce_serve_provider as vyce_provider  # noqa: E402
from openrouter_wrapper import wrap_answer  # noqa: E402

RUN_SERVE = os.path.join(HERE, "run_serve.py")
ISR = tcs.ISR
GOOD_ROW = tcs.GOOD_ROW
FAILURES = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        FAILURES.append(name)


PAST = "2020-01-01T00:00:00Z"
FUTURE = "2999-01-01T00:00:00Z"

STALE_DETAIL = {"status": "settled", "marathonActive": True,
                "marathonConcluded": True,
                "marathonEligibleIsos": [
                    {"isoId": "old", "endsAt": PAST,
                     "isActive": False}]}
NEW_ROUND_DETAIL = {"status": "settled", "marathonActive": True,
                    "marathonConcluded": True,
                    "marathonEligibleIsos": [
                        {"isoId": "old", "endsAt": PAST},
                        {"isoId": "new", "endsAt": FUTURE,
                         "isActive": True}]}
OPEN_DETAIL = {"status": "in_progress", "marathonActive": False,
               "marathonConcluded": False, "marathonEligibleIsos": []}
SETTLED_DETAIL = {"status": "settled", "marathonActive": False,
                  "marathonConcluded": False,
                  "marathonEligibleIsos": []}
MARATHON_NO_ENDS = {"status": "in_progress", "marathonActive": True,
                    "marathonConcluded": False,
                    "marathonEligibleIsos": []}


def fetcher_ok(detail):
    return lambda isr_id: (detail, "ok")


def fetcher_failed(isr_id):
    return None, "failed"


def fetcher_disabled(isr_id):
    return None, "disabled"


# ------------------------------------------------------------ liveness

def liveness_cases():
    ok, reason = serve_gate.liveness_check(STALE_DETAIL)
    check("liveness: stale-flag (concluded + endsAt past) is DEAD",
          not ok, reason)
    ok, reason = serve_gate.liveness_check(NEW_ROUND_DETAIL)
    check("liveness: concluded + NEW round (future endsAt) is LIVE",
          ok, reason)
    ok, reason = serve_gate.liveness_check(OPEN_DETAIL)
    check("liveness: open question, no marathon dimension, is LIVE",
          ok, reason)
    ok, reason = serve_gate.liveness_check(SETTLED_DETAIL)
    check("liveness: settled, no live round, is DEAD", not ok, reason)
    ok, reason = serve_gate.liveness_check(MARATHON_NO_ENDS)
    check("liveness: marathon question, no provable future endsAt, "
          "is DEAD (fail-closed)", not ok, reason)
    ok, reason = serve_gate.liveness_check(None)
    check("liveness: missing detail is DEAD (fail-closed)",
          not ok, reason)

    ok, reason = serve_gate.liveness_gate_for_row(
        GOOD_ROW, detail_fetcher=fetcher_ok(STALE_DETAIL), isr_id=ISR)
    check("gate-for-row: armed stale detail -> closed", not ok, reason)
    ok, reason = serve_gate.liveness_gate_for_row(
        GOOD_ROW, detail_fetcher=fetcher_ok(OPEN_DETAIL), isr_id=ISR)
    check("gate-for-row: armed live detail -> open", ok, reason)
    ok, reason = serve_gate.liveness_gate_for_row(
        GOOD_ROW, detail_fetcher=fetcher_failed, isr_id=ISR)
    check("gate-for-row: failed fetch -> closed (fail-closed at "
          "prepare)", not ok, reason)
    dead_row = {**GOOD_ROW, "questionMarathonConcluded": True,
                "marathonEligibleIsos": [{"endsAt": PAST}]}
    ok, reason = serve_gate.liveness_gate_for_row(
        dead_row, detail_fetcher=fetcher_disabled, isr_id=ISR)
    check("gate-for-row: unarmed, row fields prove death -> closed",
          not ok, reason)
    ok, reason = serve_gate.liveness_gate_for_row(
        GOOD_ROW, detail_fetcher=fetcher_disabled, isr_id=ISR)
    check("gate-for-row: unarmed, plain open row -> open", ok, reason)

    reason = serve_gate.fallback_dead_reason(
        ISR, detail_fetcher=fetcher_ok(STALE_DETAIL))
    check("fallback: proven-dead detail yields a block reason",
          bool(reason), reason or "")
    reason = serve_gate.fallback_dead_reason(
        ISR, detail_fetcher=fetcher_ok(OPEN_DETAIL))
    check("fallback: live detail yields no block", reason is None)
    reason = serve_gate.fallback_dead_reason(
        ISR, detail_fetcher=fetcher_failed)
    check("fallback: failed fetch yields NO block (work already "
          "accepted is finished)", reason is None)


# -------------------------------------------------------- thinking trace

SPECIMEN = (
    "Let me think about this task carefully.\n\n"
    "Hmm, I genuinely don't remember the exact wording here. "
    "I don't recall the parameters, and I really can't reproduce "
    "it reliably. Fine.\n\n"
    "The honest position is that the mechanism is unclear from "
    "memory alone, so anything below is reconstruction.\n\n"
    "Decision: I will structure my novel contribution around the "
    "parts I can defend, and note the sources I could not verify.")

CODE_DUMP = "\n".join([
    "Berikut kode mentahnya:",
    "def compute_fee(x):",
    "    base = x * 2",
    "    return base",
    "import math",
    "for i in range(10):",
    "    print(i)",
    "value = compute_fee(3)",
    "if value > 5:",
    "    print('big')",
    "else:",
    "    print('small')",
    "while value:",
    "    value = value - 1",
    "try:",
    "    result = 1 / value",
    "except Exception:",
    "    result = 0",
    "class Solver:",
    "    pass",
    "data = [1, 2, 3]",
])

PLAN_ONLY = (
    "Jawaban ini membahas biaya klon untuk armada dompet.\n\n"
    "Isi pembahasan yang netral dan faktual.\n\n"
    "Decision: I will structure my novel contribution around the "
    "verifiable parts.")

# Regression fixtures for the dry-run false positive of 2026-11-17
# (DRY-RUN-TERPADU-2026-11-17.md §2): the closing below is the
# VERBATIM contract-mandated synthesis of dry-run draft 1 — the
# bare `decision\s*:` alternative withheld that C5-clean draft on
# the mid-sentence noun in "a single design decision: the same
# carve-out…". It must NOT fire; genuine plan closings must.
DRAFT1_SYNTHESIS = (
    "Sebuah pasar khusus tetap dapat memperdagangkan token yang "
    "kuncinya diblokir kontrak melalui pola kustodi berlapis.\n\n"
    "New in this answer: a three-pattern taxonomy — "
    "privileged-operator settlement, vault/wrapper, and custodial "
    "claim trading — that maps each way a dedicated marketplace "
    "trades locked NFTs to its specific custody failure mode. It "
    "frames the lock and the dedicated marketplace as a single "
    "design decision: the same carve-out that enables trading is "
    "what blocks third-party venues. Finally, it prices the "
    "upgrade key for both sides of the trade: \"locked\" is only "
    "as durable as the EIP-1967/EIP-173 admin key behind it, with "
    "buyers facing a silent unlock and sellers having sold at a "
    "locked discount before one.")

DECISION_PLAN_MID = (
    "Jawaban ini membahas kustodi token yang terkunci.\n\n"
    "Isi pembahasan yang netral dan faktual.\n\n"
    "Saya sudah menimbang opsi-opsi di atas. Decision: I shall "
    "organize the answer around the custody question.")

DECISION_LABEL_LOWER = (
    "Jawaban ini membahas kustodi token yang terkunci.\n\n"
    "Isi pembahasan yang netral dan faktual.\n\n"
    "decision: struktur jawaban disusun dari kustodi, lalu "
    "kejujuran operator.")


def trace_cases():
    found = serve_gate.detect_thinking_trace(SPECIMEN)
    check("trace: f0bb3586 reconstruction detected",
          len(found) == 1 and found[0]["severity"] == "THINKING-TRACE",
          found[0]["action"][:80] if found else "no finding")
    found = serve_gate.detect_thinking_trace(tcs.good_text())
    check("trace: proven claim fixture NOT flagged", found == [])
    found = serve_gate.detect_thinking_trace(CODE_DUMP)
    check("trace: dominant raw code dump detected", len(found) == 1)
    found = serve_gate.detect_thinking_trace(PLAN_ONLY)
    check("trace: plan-not-answer closing detected", len(found) == 1)
    found = serve_gate.detect_thinking_trace(DRAFT1_SYNTHESIS)
    check("trace: contract synthesis 'design decision:' NOT "
          "flagged (dry-run FP regression)", found == [],
          found[0]["action"][:80] if found else "clean")
    found = serve_gate.detect_thinking_trace(DECISION_PLAN_MID)
    check("trace: mid-paragraph 'Decision:' + plan still "
          "detected", len(found) == 1)
    found = serve_gate.detect_thinking_trace(DECISION_LABEL_LOWER)
    check("trace: line-start 'decision:' label still detected",
          len(found) == 1)


# ----------------------------------------------------------------- gate

def gate_cases():
    good = tcs.good_text()
    result = serve_gate.gate_answer(good)
    check("gate: clean claim fixture is sendable",
          result["sendable"] is True,
          f"status={result['status']} g={result['score']['g'][0]}")
    check("gate: semantic self-VFP honestly reported NOT performed",
          result["gate"]["semantic_vfp"]["performed"] is False
          and result["gate"]["thinking_trace"] is False)

    traced = ("Let me think about this task carefully.\n\n" + good
              + "\n\nDecision: I will structure my novel "
                "contribution around the parts I can defend.")
    plain = wrap_answer(traced)
    plain_sendable = (
        plain["status"] == "OK"
        and not plain["report"]["audit"]["findings"]
        and plain["score"]["g"][0] == "LOLOS")
    check("gate: traced fixture passes the BARE wrapper (control — "
          "the trace layer is what must stop it)", plain_sendable,
          f"status={plain['status']} findings="
          f"{len(plain['report']['audit']['findings'])}")
    result = serve_gate.gate_answer(traced)
    check("gate: thinking-trace draft WITHHELD by the trace layer",
          result["sendable"] is False
          and result["gate"]["thinking_trace"] is True
          and result["report"]["audit"]["thinking_trace"] == 1,
          "; ".join(result["gate"]["reasons"][:1])[:80])

    no_url = good.replace("https://eips.ethereum.org/EIPS/eip-2929",
                          "eip-2929").replace(
                              "https://eips.ethereum.org/EIPS/eip-3860",
                              "eip-3860")
    result = serve_gate.gate_answer(no_url)
    docs = [f.get("doc", "") for f in
            result["report"]["audit"]["findings"]]
    check("gate: 0-URL draft WITHHELD by floor K-1(a)",
          result["sendable"] is False
          and any("K-1(a)" in d for d in docs),
          f"docs={docs}")


# --------------------------------------- evasive source closing (E3)

E3_CLOSING = (
    "Note on sources: this answer relies on widely documented, "
    "independently checkable public records and scholarship rather "
    "than on any single citation, and it avoids pinpoint references "
    "that cannot be verified from the text alone.")

_HF = os.path.join(
    HERE, "..", "..", "goals",
    "dialectica-rutinitas-ringan-pemburu-slot-trued", "hidden_files")


def _historical_serve_text(iso):
    """Full submitted text of a falsified serve answer from the
    run artefacts; falls back to a neutral body + the verbatim
    closing (identical in all four) when the artefact is absent —
    the E3 behaviour under test lives in that closing."""
    paths = {
        "f0bb3586": os.path.join(
            _HF, "run-2026-11-14-0900", "answer-f0bb3586.txt"),
        "5b5e8212": os.path.join(
            _HF, "run-2026-11-15-0700", "sent-5b5e8212.txt"),
        "a3b8b34a": os.path.join(
            _HF, "run-2026-11-15-0700", "sent-a3b8b34a.txt"),
    }
    if iso in paths and os.path.exists(paths[iso]):
        with open(paths[iso], encoding="utf-8") as fh:
            return fh.read()
    if iso == "7d81c51d":
        jobs_path = os.path.join(
            _HF, "run-2026-11-14-0900", "jobs-0900.json")
        if os.path.exists(jobs_path):
            with open(jobs_path, encoding="utf-8") as fh:
                jobs = json.load(fh)
            found = []

            def _walk(obj):
                if isinstance(obj, dict):
                    if str(obj.get("id", "")).startswith("0a835ed7"):
                        ans = ((obj.get("output") or {})
                               .get("structuredData") or {}).get(
                                   "answer")
                        if ans:
                            found.append(ans)
                    for v in obj.values():
                        _walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        _walk(v)
            _walk(jobs)
            if found:
                return found[0]
    return ("Isi jawaban netral tentang mekanisme biaya klon.\n\n"
            + E3_CLOSING)


def e3_cases():
    for iso in ("f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"):
        found = serve_gate.detect_evasive_source_closing(
            _historical_serve_text(iso))
        check(f"e3: historical falsified serve {iso} flagged",
              len(found) == 1
              and found[0]["severity"] == "EVASIVE-SOURCE-CLOSING",
              found[0]["action"][:80] if found else "no finding")

    result = serve_gate.gate_answer(_historical_serve_text(
        "f0bb3586"))
    check("e3: gate withholds f0bb3586 with the E3 flag set",
          result["sendable"] is False
          and result["gate"]["evasive_source_closing"] is True
          and result["report"]["audit"]["evasive_source_closing"]
          == 1)

    good = tcs.good_text()
    dressed = good + "\n\n" + E3_CLOSING
    plain = wrap_answer(dressed)
    plain_sendable = (
        plain["status"] == "OK"
        and not plain["report"]["audit"]["findings"]
        and plain["score"]["g"][0] == "LOLOS")
    check("e3: clean fixture + evasive closing passes the BARE "
          "wrapper (control — the E3 layer is what must stop it)",
          plain_sendable,
          f"status={plain['status']} findings="
          f"{len(plain['report']['audit']['findings'])}")
    result = serve_gate.gate_answer(dressed)
    check("e3: evasive closing WITHHELD by the E3 layer alone",
          result["sendable"] is False
          and result["gate"]["evasive_source_closing"] is True
          and result["gate"]["thinking_trace"] is False,
          "; ".join(result["gate"]["reasons"][:1])[:80])

    body_defer = good.replace(
        "Mekanisme pada seksi ini menentukan angka akhirnya.",
        "Mekanisme pada seksi ini menentukan angka akhirnya. "
        "Pembaca sebaiknya verify exact current values in the live "
        "docs sebelum memakai angka ini.", 1)
    check("e3: deferral language in the BODY does NOT fire "
          "(verified 0006fe08 pattern)",
          serve_gate.detect_evasive_source_closing(body_defer) == [])

    body_quote = good.replace(
        "Mekanisme pada seksi ini menentukan angka akhirnya.",
        "Mekanisme pada seksi ini menentukan angka akhirnya. "
        "Sebuah jawaban lain menulis \"avoids pinpoint references\" "
        "di penutupnya dan gugur karenanya.", 1)
    check("e3: explicit phrase quoted in the BODY does NOT fire "
          "(scan bounded to closing + source sections)",
          serve_gate.detect_evasive_source_closing(body_quote) == [])

    clean_src = (good + "\n\n## Sumber\n"
                 "- EIP-2929: https://eips.ethereum.org/EIPS/eip-2929"
                 "\n- EIP-3860: "
                 "https://eips.ethereum.org/EIPS/eip-3860")
    check("e3: clean text with an explicit source section does "
          "NOT fire",
          serve_gate.detect_evasive_source_closing(clean_src) == [])

    mid_src = (good + "\n\n## Sumber\nCatatan: no live web access "
               "was available for this draft; I give no URLs.\n\n"
               "## 7. Penutup tambahan\nIsi penutup yang netral dan "
               "faktual.")
    found = serve_gate.detect_evasive_source_closing(mid_src)
    check("e3: evasion inside a mid-text SOURCE SECTION fires "
          "(not only in the closing block)",
          len(found) == 1, found[0]["action"][:80] if found else "")


# ------------------------------------------------- cloudflare prepare

def cf_prepare_cases():
    good = tcs.good_text()

    world = tcs.ServeWorld()
    try:
        calls = []
        with mock.patch.object(
                cp, "generate",
                tcs.fake_generate_factory([good], world, calls)):
            rc, line = cf_prep.prepare_row(
                GOOD_ROW, detail_fetcher=fetcher_ok(STALE_DETAIL))
        check("cf prepare: stale target -> pass-over, ZERO "
              "generations", rc == 1 and len(calls) == 0
              and "liveness" in line, f"rc={rc} line={line[:70]}")
    finally:
        world.close()

    world = tcs.ServeWorld()
    try:
        calls = []
        with mock.patch.object(
                cp, "generate",
                tcs.fake_generate_factory([good], world, calls)):
            rc, line = cf_prep.prepare_row(
                GOOD_ROW, detail_fetcher=fetcher_failed)
        check("cf prepare: failed detail fetch -> pass-over "
              "(fail-closed), zero generations",
              rc == 1 and len(calls) == 0 and "liveness" in line,
              f"rc={rc}")
    finally:
        world.close()

    world = tcs.ServeWorld()
    try:
        calls = []
        with mock.patch.object(
                cp, "generate",
                tcs.fake_generate_factory([good], world, calls)):
            rc, line = cf_prep.prepare_row(
                GOOD_ROW, detail_fetcher=fetcher_ok(OPEN_DETAIL))
        check("cf prepare: live target -> prepared + cached, exit 0",
              rc == 0 and csc.read_cache(ISR) is not None
              and len(calls) == 1, f"rc={rc} line={line[:70]}")
    finally:
        world.close()

    world = tcs.ServeWorld()
    try:
        calls = []
        with mock.patch.object(
                cp, "generate",
                tcs.fake_generate_factory([SPECIMEN * 30], world,
                                          calls)):
            rc, line = cf_prep.prepare_row(
                GOOD_ROW, detail_fetcher=fetcher_ok(OPEN_DETAIL))
        check("cf prepare: thinking-trace draft -> pass-over, "
              "nothing cached", rc == 1
              and csc.read_cache(ISR) is None, f"rc={rc}")
    finally:
        world.close()


# ------------------------------------------------------- vyce prepare

def vyce_gen_stub(text, calls):
    def _gen(prompt, isr_id=None):
        calls.append(prompt)
        return text
    return _gen


def vyce_prepare_cases():
    good = tcs.good_text()
    world = tcs.ServeWorld()
    try:
        calls = []
        rc, line = vyce_prep.prepare_row(
            GOOD_ROW, detail_fetcher=fetcher_ok(STALE_DETAIL),
            generate_fn=vyce_gen_stub(good, calls))
        check("vyce prepare: stale target -> pass-over, ZERO "
              "generations", rc == 1 and len(calls) == 0
              and "liveness" in line, f"rc={rc} line={line[:70]}")

        calls = []
        rc, line = vyce_prep.prepare_row(
            GOOD_ROW, detail_fetcher=fetcher_ok(OPEN_DETAIL),
            generate_fn=vyce_gen_stub(SPECIMEN * 30, calls))
        check("vyce prepare: thinking-trace draft -> pass-over, "
              "nothing cached", rc == 1
              and csc.read_cache(ISR) is None, f"rc={rc}")

        calls = []
        rc, line = vyce_prep.prepare_row(
            GOOD_ROW, detail_fetcher=fetcher_ok(OPEN_DETAIL),
            generate_fn=vyce_gen_stub(good, calls))
        check("vyce prepare: live target + clean draft -> exit 0, "
              "answer cached", rc == 0
              and csc.read_cache(ISR) is not None
              and len(calls) == 1, f"rc={rc} line={line[:70]}")
    finally:
        world.close()


# ------------------------------------------------------ provider mains

def run_main(main_fn, env_extra, prompt="Prompt pekerjaan uji."):
    out_buf, err_buf = io.StringIO(), io.StringIO()
    old_stdin, old_env = sys.stdin, dict(os.environ)
    sys.stdin = io.StringIO(prompt)
    os.environ.pop("DIALECTICA_ISR_ID", None)
    os.environ.pop("DIALECTICA_JOB_KIND", None)
    os.environ.update(env_extra)
    try:
        with contextlib.redirect_stdout(out_buf), \
                contextlib.redirect_stderr(err_buf):
            rc = main_fn()
    finally:
        sys.stdin = old_stdin
        os.environ.clear()
        os.environ.update(old_env)
    return rc, out_buf.getvalue(), err_buf.getvalue()


def provider_cases():
    good = tcs.good_text()
    miss_id = "11111111-2222-3333-4444-555555555555"

    # --- Vyce provider
    world = tcs.ServeWorld()
    try:
        csc.write_cache(ISR, "ISI CACHE VYCE")
        rc, out, _ = run_main(vyce_provider.main,
                              {"DIALECTICA_ISR_ID": ISR})
        check("vyce provider: cache hit -> cached text, exit 0",
              rc == 0 and out.strip() == "ISI CACHE VYCE", f"rc={rc}")

        calls = []
        with mock.patch.object(vsc, "generate_vyce",
                               vyce_gen_stub(good, calls)), \
                mock.patch.object(serve_gate, "fetch_isr_detail",
                                  fetcher_ok(STALE_DETAIL)):
            rc, out, _ = run_main(vyce_provider.main,
                                  {"DIALECTICA_ISR_ID": miss_id})
        check("vyce provider: fallback on proven-dead target -> "
              "exit 1, empty stdout, zero generations",
              rc == 1 and out == "" and len(calls) == 0, f"rc={rc}")

        calls = []
        with mock.patch.object(vsc, "generate_vyce",
                               vyce_gen_stub(good, calls)):
            rc, out, _ = run_main(vyce_provider.main,
                                  {"DIALECTICA_ISR_ID": miss_id})
        check("vyce provider: fallback clean draft -> exit 0",
              rc == 0 and len(out) >= 4500 and len(calls) == 1,
              f"rc={rc}")

        calls = []
        with mock.patch.object(vsc, "generate_vyce",
                               vyce_gen_stub(SPECIMEN * 30, calls)):
            rc, out, _ = run_main(vyce_provider.main,
                                  {"DIALECTICA_ISR_ID": miss_id})
        check("vyce provider: fallback thinking-trace -> exit 1, "
              "empty stdout", rc == 1 and out == "", f"rc={rc}")
    finally:
        world.close()

    # --- Cloudflare provider fallback, armed proven-dead
    world = tcs.ServeWorld()
    try:
        calls = []
        with mock.patch.object(
                cp, "generate",
                tcs.fake_generate_factory([good], world, calls)), \
                mock.patch.object(serve_gate, "fetch_isr_detail",
                                  fetcher_ok(STALE_DETAIL)):
            rc, out, _ = run_main(cf_provider.main,
                                  {"DIALECTICA_ISR_ID": miss_id})
        check("cf provider: fallback on proven-dead target -> "
              "exit 1, empty stdout, zero generations",
              rc == 1 and out == "" and len(calls) == 0, f"rc={rc}")
    finally:
        world.close()


# ------------------------------------------------------------- run_serve

def runserve(args):
    proc = subprocess.run([sys.executable, RUN_SERVE] + args,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout + proc.stderr


def runserve_cases():
    rc, out = runserve(["--dry-run", "arenaIds=general",
                        'q="wallet"'])
    check("run_serve vyce serve --dry-run: gated hook wiring shown",
          rc == 0 and "vyce_serve_prepare.py" in out
          and "vyce_serve_provider.py" in out
          and "vyce_serve_ready.py" in out
          and "DIALECTICA_SERVE_GATE_FETCH" in out
          and "DRY-RUN" in out and "launching" not in out, f"rc={rc}")
    rc, out = runserve(["--dry-run", "--answer", ISR])
    check("run_serve vyce --answer --dry-run: NO serve hooks (claim "
          "path untouched)", rc == 0 and "vyce_provider.py" in out
          and "vyce_serve_prepare" not in out
          and "DIALECTICA_SERVE_GATE_FETCH" not in out, f"rc={rc}")


if __name__ == "__main__":
    liveness_cases()
    trace_cases()
    gate_cases()
    e3_cases()
    cf_prepare_cases()
    vyce_prepare_cases()
    provider_cases()
    runserve_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
