#!/usr/bin/env python3
"""Model-lane verdict drafting for the Verifier kit — Jalur 2
(2026-11-18; F-31D: the drafter must not rest on one lane).

Two lanes, both through the registered CrowLLM connector client —
the same transport, pacing (>=13 s between call starts, shared
5 req/min account ceiling) and retry discipline the production
checker chain uses (provider/crowllm_checker.py, imported, not
re-implemented):

  NEMOTRON  nvidia/nemotron-3.5-super-vl-120b-a12b:free
            (the lane the checker calibration ran via CrowLLM
            streaming; the chain's primary checker family)
  QWEN      qwen-3.8-max:free
            (the chain's backup checker, calibration 6/7 poison)

RELAY FENCE (hard rule, user 2026-11-17 — same fence as
crowllm_checker): only public-by-design material crosses the
relay. What crosses here is exactly: a PUBLIC Question text and a
PUBLIC Answer text (both published on the platform), plus the
prompt below — a plain-language restatement of the arena's four
published verification checks. The platform itself serves those
procedures to any reader via GET /api/node/arenas/general. Our
internal gate logic, rubrics, thresholds and this kit's heuristics
are NEVER in the prompt.

The lane's verdict is never taken on trust: the reply's per-check
pass/fail is parsed and the verdict RECOMPUTED under the arena's
verdict_logic (all four pass = compliant; any fail =
non-compliant). A reply with no usable JSON is a lane failure
("unavailable"), not a judgement.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROVIDER_DIR = os.path.dirname(HERE)
if PROVIDER_DIR not in sys.path:
    sys.path.insert(0, PROVIDER_DIR)

import crowllm_checker as cc  # noqa: E402  (transport + pacing + retries)

NEMOTRON_MODEL = os.environ.get(
    "DIALECTICA_VERIFIER_LANE_NEMOTRON",
    "nvidia/nemotron-3.5-super-vl-120b-a12b:free")
QWEN_MODEL = os.environ.get(
    "DIALECTICA_VERIFIER_LANE_QWEN", "qwen-3.8-max:free")
LANES = (("nemotron", NEMOTRON_MODEL), ("qwen", QWEN_MODEL))

CHECKS = ("A_CITATION", "A_REASONING", "A_UNCERTAINTY", "A_SCOPE")

VERDICT_PROMPT = """You are a verifier on a public Q&A platform. A Question and one Answer to it are below. Judge the Answer against the platform's four published verification checks:

- A_CITATION: every specific factual claim (quantities, dates, statistics, named findings) needs a citation to a real source that actually supports the claim it is attached to. Widely accepted foundational principles need no citation. A citation that cannot be located or does not support its claim fails this check.
- A_REASONING: the Answer must state why/how, not just what. Conclusion-only answers, self-contradictory steps, or conclusions that do not follow from their premises fail this check.
- A_UNCERTAINTY: contested, speculative or probabilistic claims must be framed with suitable qualifiers (for example "may", "suggests", "scholars disagree"). A claim with significant uncertainty presented as established fact fails this check.
- A_SCOPE: the Answer must respond to the actual Question asked, not just the topic area. Tangential content with no engagement with what was asked fails this check.

QUESTION:
{question}

ANSWER:
{answer}

Reply with ONLY a JSON object in exactly this shape, and no other text:
{{"checks": {{"A_CITATION": {{"pass": true or false, "reason": "the specific claim or gap, in one sentence"}}, "A_REASONING": {{"pass": true or false, "reason": "..."}}, "A_UNCERTAINTY": {{"pass": true or false, "reason": "..."}}, "A_SCOPE": {{"pass": true or false, "reason": "..."}}}}}}"""


def parse_lane_reply(text):
    """Parse one lane reply into {checks, verdict} with the
    verdict RECOMPUTED from the checks. Returns (parsed, note);
    parsed is None when the reply carries no usable object."""
    if not text or not text.strip():
        return None, "empty"
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    start, end = t.find("{"), t.rfind("}")
    if start < 0 or end <= start:
        return None, "no-json-object"
    try:
        obj = json.loads(t[start:end + 1])
    except ValueError:
        return None, "json-parse-error"
    raw_checks = obj.get("checks") or {}
    checks = {}
    for name in CHECKS:
        cell = raw_checks.get(name) or {}
        if not isinstance(cell, dict) or "pass" not in cell:
            return None, f"missing-check:{name}"
        checks[name] = {"pass": bool(cell.get("pass")),
                        "reason": str(cell.get("reason", ""))[:300]}
    verdict = ("compliant" if all(c["pass"] for c in checks.values())
               else "non-compliant")
    return {"checks": checks, "verdict": verdict}, "ok"


def draft_with_lane(lane_name, model, question, answer, transport=None):
    """One lane's verdict draft. Always returns a dict; a dead or
    unparseable lane is {available: False, verdict: 'unavailable'},
    never an exception and never a judgement."""
    transport = transport or cc._client_transport
    prompt = VERDICT_PROMPT.format(question=question or "",
                                   answer=answer or "")
    base = {"lane": lane_name, "model": model, "available": False,
            "verdict": "unavailable", "checks": None, "error": None,
            "attempts": [], "prompt_chars": len(prompt)}
    res, attempts = cc._call_with_retries(model, prompt, transport)
    base["attempts"] = attempts
    if res is None:
        last = attempts[-1] if attempts else {}
        base["error"] = (f"transport gagal sesudah {len(attempts)} "
                         f"percobaan: {last.get('error') or ('status ' + str(last.get('status')))}")
        return base
    parsed, note = parse_lane_reply(res.get("text"))
    if parsed is None:
        base["error"] = f"balasan tak terparse: {note}"
        return base
    return {**base, "available": True, "verdict": parsed["verdict"],
            "checks": parsed["checks"], "latency_s": res.get("latency_s")}


def compare_drafts(drafts):
    """Agreement table over a list of draft dicts (local + lanes).
    Pure. Per check: the set of pass/fail/unknown verdicts each
    drafter gave; overall: whether every AVAILABLE drafter agrees
    on the verdict."""
    per_check = {}
    names = []
    for d in drafts:
        label = d.get("drafter") or d.get("lane") or "?"
        names.append(label)
        checks = d.get("checks") or {}
        for name in CHECKS:
            cell = checks.get(name) or {}
            if "status" in cell:  # local drafter shape
                value = {"pass": "pass", "fail": "fail"}.get(
                    cell["status"], "unknown")
            elif "pass" in cell:  # lane shape
                value = "pass" if cell["pass"] else "fail"
            else:
                value = "unknown"
            per_check.setdefault(name, {})[label] = value
    verdicts = {}
    for d in drafts:
        label = d.get("drafter") or d.get("lane") or "?"
        verdicts[label] = d.get("verdict")
    usable = [v for v in verdicts.values() if v and v != "unavailable"]
    return {
        "drafters": names,
        "verdicts": verdicts,
        "per_check": per_check,
        "all_agree": len(set(usable)) == 1 and len(usable) == len(verdicts),
        "check_disagreements": [
            name for name, votes in per_check.items()
            if len({v for v in votes.values() if v != "unknown"}) > 1],
    }
