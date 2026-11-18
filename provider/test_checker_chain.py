#!/usr/bin/env python3
"""Tests for the CrowLLM backup checker chain (serve_gate.
chained_semantic_check + crowllm_checker, built 2026-11-18 per
user decision 07:16 "ydh pasang"; RANTAI-PEMERIKSA-2026-11-18.md).

Proves, WITHOUT any real model or relay call (every lane is mocked
at its seam — the primary at primary_check / default_semantic_
model_call, the relay at public_check / transport):

- Firing rules: an available primary FATAL is final and spends NO
  relay call; the backup fires only on primary-unavailable or
  primary-clean; a backup FATAL against a primary clean is a
  dispute settled by the arbiter; lane outages cascade (backup
  down -> arbiter lane as second backup).
- Unresolved disputes and a fully dead chain follow the primary's
  unavailable doctrine exactly: never a block (even in block mode),
  never a fake clean, the primary's verdict stands and the gap is
  recorded in the result's chain detail.
- The chain writes exactly ONE record to the semantic log, whose
  checker field names the lane that actually decided.
- The relay lanes receive the question TEXT ONLY (novelty block
  stripped — the calibration regime carried question + draft).
- Arming: DIALECTICA_CHECKER_CHAIN=1 engages the chain only on top
  of DIALECTICA_SEMANTIC_CHECK=1; without it, armed_semantic_check
  behaves byte-identically to before the chain existed.
- crowllm_checker itself: the public prompt is the calibration
  text; verdicts survive only with verbatim-verified quotes (a
  FATAL whose findings all drop degrades to CLEAN); unparseable /
  transport-dead replies are "unavailable"; retries follow the
  calibration policy; pacing keeps >=13 s between call starts.

Run: python3 test_checker_chain.py (exit 0 = all pass).
"""
import json
import os
import sys
import tempfile
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import crowllm_checker  # noqa: E402
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
QUOTE = ("BNB Chain charges exactly 5 gwei for every transfer "
         "in all conditions")
DRAFT = ("## Jawaban\n\n" + QUOTE + ", as proven by the 2019 "
         "Nakamoto-Buterin paper on gas pricing.\n")
QWEN = crowllm_checker.BACKUP_MODEL
SOL = crowllm_checker.ARBITER_MODEL
QWEN_LANE = crowllm_checker.lane_label(QWEN)
SOL_LANE = crowllm_checker.lane_label(SOL)


def primary_dict(verdict, available=True, mode="shadow"):
    return {"performed": available, "available": available,
            "mode": mode,
            "checker": "openrouter-nemotron" if available else None,
            "verdict": verdict,
            "findings": ([{"code": "A_CITATION", "sub": "S-1",
                           "quote": QUOTE, "claim": "c", "why": "w"}]
                         if verdict == "fatal" else []),
            "block": bool(mode == "block" and verdict == "fatal"),
            "dropped_findings": 0,
            "model_verdict": verdict,
            "error": None if available else "kedua lane utama mati",
            "segments": 1, "segments_ok": 1 if available else 0,
            "prompt_chars": 1000}


def public_dict(verdict, model, with_finding=True):
    lane = crowllm_checker.lane_label(model)
    findings = ([{"code": None, "sub": None, "quote": QUOTE,
                  "claim": "angka karangan", "why": "",
                  "source": lane}]
                if verdict == "fatal" and with_finding else [])
    return {"available": verdict != "unavailable",
            "verdict": verdict, "findings": findings, "dropped": 0,
            "error": (None if verdict != "unavailable"
                      else "transport gagal sesudah 3 percobaan"),
            "attempts": [], "latency_s": 1.0, "model": model,
            "lane": lane, "prompt_chars": 500,
            "model_verdict": {"fatal": "FATAL",
                              "clean": "CLEAN"}.get(verdict)}


def make_primary(verdict, available=True, mode="shadow"):
    def _p(d, q, i):
        return primary_dict(verdict, available=available, mode=mode)
    return _p


def make_public(responses, calls, questions=None):
    def _pub(model, draft, question):
        calls.append(model)
        if questions is not None:
            questions.append(question)
        r = responses[model]
        if isinstance(r, Exception):
            raise r
        return r
    return _pub


def run_chain(primary, responses, mode="shadow", question=QUESTION):
    calls = []
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        res = serve_gate.chained_semantic_check(
            DRAFT, question=question, isr_id="isr-test", mode=mode,
            log_path=log, primary_check=primary,
            public_check=make_public(responses, calls))
        lines = []
        if os.path.exists(log):
            lines = [json.loads(x) for x in open(log)]
    return res, calls, lines


# ------------------------------------------------------------ firing rules

def firing_cases():
    # 1. primary FATAL is final — no relay call spent.
    res, calls, _ = run_chain(
        make_primary("fatal"), {QWEN: public_dict("clean", QWEN)})
    check("rantai: utama FATAL final, cadangan TIDAK dipanggil",
          res["verdict"] == "fatal" and calls == []
          and res["checker"] == "openrouter-nemotron"
          and res["chain"]["decided_by"] == "openrouter-nemotron")

    # 2. primary clean + backup clean = agreement.
    res, calls, _ = run_chain(
        make_primary("clean"), {QWEN: public_dict("clean", QWEN)})
    check("rantai: utama clean + cadangan clean = sepakat clean",
          res["verdict"] == "clean" and calls == [QWEN]
          and QWEN_LANE in (res["checker"] or "")
          and "openrouter-nemotron" in (res["checker"] or ""))

    # 3. dispute, arbiter fatal -> chain fatal (block mode blocks).
    resp = {QWEN: public_dict("fatal", QWEN),
            SOL: public_dict("fatal", SOL)}
    res, calls, _ = run_chain(make_primary("clean", mode="block"),
                              resp, mode="block")
    check("rantai: sengketa + penengah FATAL = fatal + block",
          res["verdict"] == "fatal" and res["block"] is True
          and calls == [QWEN, SOL] and res["checker"] == SOL_LANE
          and len(res["findings"]) == 1
          and res["chain"]["dispute"] is True)
    res, calls, _ = run_chain(make_primary("clean"), resp)
    check("rantai: sengketa yang sama di shadow TIDAK memblokir",
          res["verdict"] == "fatal" and res["block"] is False)

    # 4. dispute, arbiter clean -> primary clean restored (2-of-3).
    resp = {QWEN: public_dict("fatal", QWEN),
            SOL: public_dict("clean", SOL)}
    res, calls, _ = run_chain(make_primary("clean"), resp)
    check("rantai: sengketa + penengah clean = clean (2-dari-3)",
          res["verdict"] == "clean" and res["findings"] == []
          and res["chain"]["decided_by"] == SOL_LANE)

    # 5. dispute, arbiter down -> primary clean stands, unresolved,
    #    never blocks even in block mode.
    resp = {QWEN: public_dict("fatal", QWEN),
            SOL: public_dict("unavailable", SOL)}
    res, calls, _ = run_chain(make_primary("clean", mode="block"),
                              resp, mode="block")
    check("rantai: sengketa + penengah mati = clean utama berdiri, "
          "tak-terselesaikan tercatat, TIDAK block",
          res["verdict"] == "clean" and res["block"] is False
          and res["chain"]["dispute_unresolved"] is True
          and len(res["chain"]["disputed_findings"]) == 1)

    # 6. primary down -> backup verdict IS the chain verdict.
    res, calls, _ = run_chain(
        make_primary("unavailable", available=False),
        {QWEN: public_dict("fatal", QWEN)})
    check("rantai: utama mati -> vonis cadangan berlaku penuh",
          res["verdict"] == "fatal" and res["performed"] is True
          and res["checker"] == QWEN_LANE and calls == [QWEN])

    # 7. primary down + backup down -> arbiter lane as backup2.
    resp = {QWEN: public_dict("unavailable", QWEN),
            SOL: public_dict("clean", SOL)}
    res, calls, _ = run_chain(
        make_primary("unavailable", available=False), resp)
    check("rantai: utama+cadangan mati -> cadangan kedua memutuskan",
          res["verdict"] == "clean" and res["checker"] == SOL_LANE
          and calls == [QWEN, SOL])

    # 8. ALL lanes down -> tak-terukur: unavailable verbatim,
    #    performed False, block False even in block mode.
    resp = {QWEN: public_dict("unavailable", QWEN),
            SOL: public_dict("unavailable", SOL)}
    res, calls, _ = run_chain(
        make_primary("unavailable", available=False, mode="block"),
        resp, mode="block")
    check("rantai: semua lane mati = tak-terukur (unavailable, "
          "performed=False, block=False walau mode block)",
          res["verdict"] == "unavailable"
          and res["performed"] is False and res["block"] is False
          and res["chain"]["decided_by"] is None
          and len(res["chain"]["lanes"]) == 3)

    # 9. primary clean + both relay lanes down -> clean stands,
    #    outage recorded (backup_outage), no fake second sample.
    res, calls, _ = run_chain(make_primary("clean"), resp)
    check("rantai: utama clean + relay mati total = clean utama, "
          "outage tercatat",
          res["verdict"] == "clean"
          and res["chain"].get("backup_outage") is True
          and calls == [QWEN, SOL])

    # 10. primary clean + backup1 down + backup2 fatal = dispute
    #     with no arbiter left: clean stands, unresolved.
    resp = {QWEN: public_dict("unavailable", QWEN),
            SOL: public_dict("fatal", SOL)}
    res, calls, _ = run_chain(make_primary("clean", mode="block"),
                              resp, mode="block")
    check("rantai: cadangan-2 FATAL tanpa penengah tersisa = "
          "sengketa tak-terselesaikan, clean berdiri, TIDAK block",
          res["verdict"] == "clean" and res["block"] is False
          and res["chain"]["dispute_unresolved"] is True)

    # 11. a CRASHING public seam is a lane failure, not an exception.
    resp = {QWEN: RuntimeError("relay meledak"),
            SOL: public_dict("clean", SOL)}
    res, calls, _ = run_chain(
        make_primary("unavailable", available=False), resp)
    check("rantai: seam relay crash = lane gagal, rantai lanjut",
          res["verdict"] == "clean" and res["checker"] == SOL_LANE)


def log_and_question_cases():
    # Exactly ONE log record; checker names the deciding lane.
    resp = {QWEN: public_dict("fatal", QWEN),
            SOL: public_dict("fatal", SOL)}
    res, calls, lines = run_chain(make_primary("clean"), resp)
    check("rantai: tepat SATU record log, checker = lane pemutus",
          len(lines) == 1 and lines[0]["checker"] == SOL_LANE
          and lines[0]["verdict"] == "fatal"
          and len(lines[0]["chain"]["lanes"]) == 3)

    # Relay lanes get the question TEXT ONLY (novelty stripped).
    header, _mark = serve_gate._novelty_markers()
    q_with_block = (QUESTION + "\n" + header +
                    "\nVERIFIED ANSWER LAIN ...\n")
    questions = []
    calls = []
    with tempfile.TemporaryDirectory() as td:
        serve_gate.chained_semantic_check(
            DRAFT, question=q_with_block, isr_id="isr-test",
            mode="shadow", log_path=os.path.join(td, "log.jsonl"),
            primary_check=make_primary("clean"),
            public_check=make_public(
                {QWEN: public_dict("clean", QWEN)}, calls,
                questions=questions))
    check("rantai: lane relay menerima teks pertanyaan SAJA "
          "(blok kebaruan dilucuti)",
          len(questions) == 1 and header not in questions[0]
          and questions[0].startswith("How do BNB Chain"))


def arming_cases():
    canned_primary = mock.Mock(
        return_value=primary_dict("clean"))
    canned_chain = mock.Mock(
        return_value=primary_dict("clean"))
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("DIALECTICA_SEMANTIC_CHECK", None)
        os.environ.pop("DIALECTICA_CHECKER_CHAIN", None)
    # semantic unarmed -> None even with chain env set
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_CHECKER_CHAIN": "1"}):
        check("arming rantai: tanpa arming semantik -> None",
              serve_gate.armed_semantic_check("q") is None)
    # semantic armed, chain OFF -> plain semantic path only
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_SEMANTIC_CHECK": "1"}), \
            mock.patch.dict(os.environ, {}, clear=False), \
            mock.patch.object(serve_gate, "semantic_check",
                              canned_primary), \
            mock.patch.object(serve_gate, "chained_semantic_check",
                              canned_chain):
        os.environ.pop("DIALECTICA_CHECKER_CHAIN", None)
        fn = serve_gate.armed_semantic_check(QUESTION)
        fn(DRAFT)
    check("arming rantai: env rantai OFF -> jalur utama persis "
          "seperti sebelum rantai ada",
          canned_primary.called and not canned_chain.called)
    canned_primary.reset_mock()
    # semantic armed + chain ON -> chain path
    with mock.patch.dict(os.environ,
                         {"DIALECTICA_SEMANTIC_CHECK": "1",
                          "DIALECTICA_CHECKER_CHAIN": "1"}), \
            mock.patch.object(serve_gate, "semantic_check",
                              canned_primary), \
            mock.patch.object(serve_gate, "chained_semantic_check",
                              canned_chain):
        fn = serve_gate.armed_semantic_check(QUESTION)
        fn(DRAFT)
    check("arming rantai: env rantai ON -> rantai yang jalan",
          canned_chain.called and not canned_primary.called)


def gate_end_to_end_case():
    # Real primary machinery (mocked lane) + stubbed relay seams,
    # through armed_semantic_check + gate_answer in block mode:
    # primary clean, qwen FATAL, arbiter FATAL -> gate withholds.
    clean_reply = json.dumps({"verdict": "clean", "findings": []})
    resp = {QWEN: public_dict("fatal", QWEN),
            SOL: public_dict("fatal", SOL)}
    calls = []
    env = {"DIALECTICA_SEMANTIC_CHECK": "1",
           "DIALECTICA_CHECKER_CHAIN": "1",
           "DIALECTICA_SEMANTIC_MODE": "block"}
    with mock.patch.dict(os.environ, env), \
            mock.patch.object(
                serve_gate, "default_semantic_model_call",
                lambda prompt: (clean_reply, "openrouter-nemotron")), \
            mock.patch.object(crowllm_checker, "check_public",
                              make_public(resp, calls)), \
            tempfile.TemporaryDirectory() as td:
        with mock.patch.object(serve_gate, "SEMANTIC_LOG",
                               os.path.join(td, "log.jsonl")):
            fn = serve_gate.armed_semantic_check(QUESTION)
            res = serve_gate.gate_answer(tcs.good_text(),
                                         semantic_check=fn)
    sem = res["gate"]["semantic_vfp"]
    check("rantai e2e: sengketa FATAL yang diputus penengah "
          "menahan draf lewat gate (mode block)",
          res["sendable"] is False and sem["verdict"] == "fatal"
          and sem["block"] is True and sem["checker"] == SOL_LANE
          and calls == [QWEN, SOL])


# ------------------------------------------------------------ crowllm_checker

class FakeClock:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


def crowllm_cases():
    # The prompt that crosses the relay is the calibration text.
    check("crowllm: prompt publik = teks kalibrasi persis",
          crowllm_checker.PUBLIC_PROMPT.startswith(
              "You are checking a draft answer for factual "
              "reliability")
          and "{question}" in crowllm_checker.PUBLIC_PROMPT
          and "A_CITATION" not in crowllm_checker.PUBLIC_PROMPT
          and "SURPRISE_GAUGE" not in crowllm_checker.PUBLIC_PROMPT)

    fatal_json = json.dumps({
        "verdict": "FATAL",
        "findings": [{"issue": "angka karangan", "quote": QUOTE}]})

    def ok_transport(model, prompt, stream=False):
        return {"status": 200, "text": fatal_json,
                "latency_s": 1.5, "model_returned": model}

    with mock.patch.object(crowllm_checker, "_monotonic",
                           FakeClock().monotonic), \
            mock.patch.object(crowllm_checker, "_sleep",
                              lambda s: None):
        crowllm_checker._last_call_start[0] = 0.0
        r = crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                         transport=ok_transport)
    check("crowllm: FATAL + kutipan terverifikasi = fatal",
          r["available"] and r["verdict"] == "fatal"
          and len(r["findings"]) == 1
          and r["findings"][0]["code"] is None
          and r["findings"][0]["source"] == QWEN_LANE)

    def bad_quote_transport(model, prompt, stream=False):
        return {"status": 200,
                "text": json.dumps({
                    "verdict": "FATAL",
                    "findings": [{"issue": "x",
                                  "quote": "kalimat yang tidak "
                                           "pernah ada di draf"}]}),
                "latency_s": 1.0, "model_returned": model}

    with mock.patch.object(crowllm_checker, "_sleep", lambda s: None):
        crowllm_checker._last_call_start[0] = 0.0
        r = crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                         transport=bad_quote_transport)
    check("crowllm: FATAL yang kutipannya gugur semua -> CLEAN",
          r["available"] and r["verdict"] == "clean"
          and r["dropped"] == 1 and r["findings"] == [])

    def garbage_transport(model, prompt, stream=False):
        return {"status": 200, "text": "maaf saya tidak bisa",
                "latency_s": 1.0, "model_returned": model}

    with mock.patch.object(crowllm_checker, "_sleep", lambda s: None):
        crowllm_checker._last_call_start[0] = 0.0
        r = crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                         transport=garbage_transport)
    check("crowllm: balasan tak terparse = unavailable (bukan vonis)",
          not r["available"] and r["verdict"] == "unavailable"
          and "tak terparse" in (r["error"] or ""))

    # Retry: 503 then 200 — verdict comes from the second attempt.
    state = {"n": 0}

    def flaky_transport(model, prompt, stream=False):
        state["n"] += 1
        if state["n"] == 1:
            return {"status": 503, "text": None}
        return {"status": 200, "text": fatal_json,
                "latency_s": 2.0, "model_returned": model}

    with mock.patch.object(crowllm_checker, "_sleep", lambda s: None):
        crowllm_checker._last_call_start[0] = 0.0
        r = crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                         transport=flaky_transport)
    check("crowllm: 503 -> retry -> vonis dari percobaan kedua",
          r["available"] and r["verdict"] == "fatal"
          and len(r["attempts"]) == 2
          and r["attempts"][0]["status"] == 503)

    # Dead lane: 3 attempts, then unavailable.
    def dead_transport(model, prompt, stream=False):
        return {"status": 524, "text": None}

    with mock.patch.object(crowllm_checker, "_sleep", lambda s: None):
        crowllm_checker._last_call_start[0] = 0.0
        r = crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                         transport=dead_transport)
    check("crowllm: lane mati 524 x3 = unavailable sesudah 3 "
          "percobaan (kelas gagal transport, bukan vonis)",
          not r["available"] and len(r["attempts"]) == 3)

    # Pacing: two consecutive call starts are >=13 s apart.
    clock = FakeClock()
    starts = []

    def timed_transport(model, prompt, stream=False):
        starts.append(clock.now)
        return {"status": 200,
                "text": json.dumps({"verdict": "CLEAN",
                                    "findings": []}),
                "latency_s": 0.5, "model_returned": model}

    with mock.patch.object(crowllm_checker, "_monotonic",
                           clock.monotonic), \
            mock.patch.object(crowllm_checker, "_sleep", clock.sleep):
        crowllm_checker._last_call_start[0] = 0.0
        crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                     transport=timed_transport)
        crowllm_checker.check_public(QWEN, DRAFT, QUESTION,
                                     transport=timed_transport)
    check("crowllm: jeda antar awal panggilan >= 13 detik (pacing)",
          len(starts) == 2 and starts[1] - starts[0] >= 13.0,
          f"starts={starts}")


if __name__ == "__main__":
    firing_cases()
    log_and_question_cases()
    arming_cases()
    gate_end_to_end_case()
    crowllm_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
