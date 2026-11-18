#!/usr/bin/env python3
"""CrowLLM public-prompt checker lanes for Dialectica (2026-11-18).

Transport + verdict machinery for the BACKUP checker chain installed
in serve_gate (keputusan user 2026-11-18 07:16 "ydh pasang"; design:
RANTAI-PEMERIKSA-2026-11-18.md). The call pattern, the public prompt,
the retry policy and the quote-verification discipline are ported
verbatim from the calibration runner `calibrate_checker_crowllm.py`
(UJI-CROWLLM-PEMERIKSA-2026-11-17.md) — production must speak to the
relay in EXACTLY the regime the calibration scores certify.

RELAY FENCE (hard rule, user 2026-11-17): prompts visible to the
relay operator, so ONLY public-by-design material ever crosses it —
the question text and the draft (both published on the platform).
The internal C5 gate prompt / live rubric / finding codes are NEVER
sent. PUBLIC_PROMPT below is therefore deliberately generic, and the
scores that certify these lanes (qwen-3.8-max: poison 6/7 union,
false-fatal 2/6; gpt-5.6-sol: 5/7, 2/6) certify THIS prompt regime,
not the internal one. A verdict from this module is a FATAL/CLEAN
judgement at calibration semantics: FATAL survives only with >=1
finding whose quote re-verifies verbatim (whitespace-normalised)
against the draft; a FATAL whose findings all drop degrades to
CLEAN; an unparseable or transport-dead reply is UNAVAILABLE — a
lane failure, never a verdict.

Transport discipline (connector doc + calibration): >=13 s between
call starts (the account's 5 req/min free ceiling is SHARED by all
projects — this module never bursts), retries only on 429/500/503/
524 or transport failure, max 2, with growing pauses; a 524 retry
switches to streaming. Every production call is one subprocess run
of the registered connector client, prompt via a temp file (the
prompt never rides argv beyond the file path).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))

CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.crowllm/bin/client.py")

BACKUP_MODEL = os.environ.get(
    "DIALECTICA_CHAIN_BACKUP_MODEL", "qwen-3.8-max:free")
ARBITER_MODEL = os.environ.get(
    "DIALECTICA_CHAIN_ARBITER_MODEL", "gpt-5.6-sol:free")

# Byte-identical to calibrate_checker_crowllm.PUBLIC_PROMPT — the
# certified regime. Do not "improve" this text without a fresh
# calibration; a different prompt is a different, uncertified lane.
PUBLIC_PROMPT = """You are checking a draft answer for factual reliability before it is published on a public Q&A platform.

QUESTION:
{question}

DRAFT ANSWER:
{draft}

Check the draft for serious problems, such as:
- citations, references, DOIs, paper titles, URLs, statistics, dates or named sources that appear invented or wrong
- specific factual claims stated with confidence that are internally inconsistent or implausible
- content that does not actually answer the question that was asked
- leftover reasoning traces, working notes or meta-commentary inside the answer text

Reply with ONLY a JSON object in exactly this shape, and no other text:
{{"verdict": "FATAL" if at least one serious problem exists, otherwise "CLEAN", "findings": [{{"issue": "short description of the problem", "quote": "a short exact quote from the draft that shows the problem"}}]}}"""

PACE_S = 13.0
MAX_TOKENS = 4000
RETRY_STATUSES = (429, 500, 503, 524)

_last_call_start = [0.0]


# Clock seams: production uses the real clock; tests patch these
# two names to prove the pacing without sleeping.
def _monotonic():
    return time.monotonic()


def _sleep(seconds):
    time.sleep(seconds)


def _pace(extra=0.0):
    wait = PACE_S + extra - (_monotonic() - _last_call_start[0])
    if wait > 0:
        _sleep(wait)


def lane_label(model):
    """Short lane label for logs / the gate's checker field."""
    return "crowllm-" + (model or "").split(":")[0].split("/")[-1]


def _client_transport(model, prompt, stream=False):
    """One CrowLLM chat call via the connector client. Returns the
    client's parsed JSON dict. Raises RuntimeError on client
    failure (the caller classifies it as a lane failure)."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(prompt)
        cmd = [sys.executable, CLIENT, "chat", "--model", model,
               "--prompt-file", path, "--max-tokens", str(MAX_TOKENS)]
        if stream:
            cmd.append("--stream")
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=700)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(
            f"client rc={proc.returncode}: "
            f"{(proc.stderr or proc.stdout or '').strip()[:300]}")
    return json.loads(proc.stdout)


def _call_with_retries(model, prompt, transport):
    """Calibration retry policy: up to 3 attempts; retry only on
    429/500/503/524 or a transport exception, with growing extra
    pauses (429 waits longer); a 524 switches the next attempt to
    streaming. Returns (client_dict_or_None, attempts_log)."""
    attempts = []
    stream = False
    for attempt in range(3):
        _pace()
        _last_call_start[0] = _monotonic()
        try:
            res = transport(model, prompt, stream=stream)
        except Exception as exc:  # noqa: BLE001 - transport is data
            attempts.append({"attempt": attempt + 1, "ok": False,
                             "error": str(exc)[:300]})
            if attempt < 2:
                _pace(extra=30.0 * (attempt + 1))
                continue
            return None, attempts
        status = res.get("status")
        attempts.append({"attempt": attempt + 1,
                         "ok": status == 200,
                         "status": status,
                         "latency_s": res.get("latency_s"),
                         "model_returned": res.get("model_returned")})
        if status == 200:
            return res, attempts
        if status in RETRY_STATUSES and attempt < 2:
            if status == 524:
                stream = True
            _pace(extra=45.0 * (attempt + 1) if status == 429
                  else 30.0 * (attempt + 1))
            continue
        return None, attempts
    return None, attempts


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def parse_public_reply(text):
    """Extract the public-schema JSON verdict. Returns
    (verdict, findings, fmt_note) or (None, [], note) when the
    reply carries no usable verdict object."""
    if not text or not text.strip():
        return None, [], "empty"
    t = text.strip()
    t2 = re.sub(r"^```(?:json)?\s*", "", t)
    t2 = re.sub(r"\s*```$", "", t2)
    start, end = t2.find("{"), t2.rfind("}")
    if start < 0 or end <= start:
        return None, [], "no-json-object"
    try:
        obj = json.loads(t2[start:end + 1])
    except ValueError:
        return None, [], "json-parse-error"
    verdict = str(obj.get("verdict", "")).upper()
    if verdict not in ("FATAL", "CLEAN"):
        return None, [], f"bad-verdict:{verdict[:30]}"
    findings = obj.get("findings") or []
    if not isinstance(findings, list):
        findings = []
    extra = t2[:start].strip() or t2[end + 1:].strip()
    note = "prose-outside-json" if extra else "pure-json"
    return verdict, findings, note


def verify_public_findings(findings, draft):
    """Keep only findings whose quote verifies verbatim
    (whitespace-normalised) against the draft — the calibration
    discipline. Returns (kept, dropped); kept findings are shaped
    for the serve_gate result dict, with code=None ON PURPOSE: the
    public regime has no rubric codes, and inventing one would
    mislabel the evidence."""
    nd = _norm(draft)
    kept, dropped = [], 0
    for f in findings:
        if not isinstance(f, dict):
            dropped += 1
            continue
        q = _norm(f.get("quote", ""))
        if q and (q in nd or (len(q) > 60 and q[:60] in nd)):
            kept.append({"issue": str(f.get("issue", ""))[:200],
                         "quote": str(f.get("quote", ""))[:200]})
        else:
            dropped += 1
    return kept, dropped


def check_public(model, draft, question="", transport=None):
    """One public-prompt check of a draft on one CrowLLM lane.
    `transport` is the test seam: callable (model, prompt, stream)
    -> client dict; the default is the connector client. Always
    returns a structured dict and never raises for lane problems:

    {available, verdict, findings, dropped, error, attempts,
     latency_s, model, lane, prompt_chars}

    verdict is "fatal" (>=1 quote-verified finding), "clean", or
    "unavailable" (transport dead after retries, or the reply
    carried no usable verdict — a lane failure, NOT a judgement;
    the chain treats it exactly like the primary's unavailable)."""
    transport = transport or _client_transport
    label = lane_label(model)
    prompt = PUBLIC_PROMPT.format(
        question=question or "(no question text archived)",
        draft=draft or "")
    base = {"available": False, "verdict": "unavailable",
            "findings": [], "dropped": 0, "error": None,
            "attempts": [], "latency_s": None, "model": model,
            "lane": label, "prompt_chars": len(prompt)}
    res, attempts = _call_with_retries(model, prompt, transport)
    base["attempts"] = attempts
    if res is None:
        last = attempts[-1] if attempts else {}
        base["error"] = (
            f"transport gagal sesudah {len(attempts)} percobaan: "
            f"{last.get('error') or ('status ' + str(last.get('status')))}")
        return base
    base["latency_s"] = res.get("latency_s")
    verdict, findings, fmt = parse_public_reply(res.get("text"))
    if verdict is None:
        base["error"] = f"balasan tak terparse: {fmt}"
        return base
    kept, dropped = verify_public_findings(findings, draft or "")
    if verdict == "FATAL" and not kept:
        verdict = "CLEAN"
        fmt += "+fatal-all-dropped"
    shaped = [{"code": None, "sub": None,
               "quote": k["quote"], "claim": k["issue"], "why": "",
               "source": label} for k in kept]
    return {**base, "available": True,
            "verdict": "fatal" if verdict == "FATAL" else "clean",
            "findings": shaped, "dropped": dropped,
            "model_verdict": verdict, "fmt": fmt}
