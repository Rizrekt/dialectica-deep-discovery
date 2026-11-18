#!/usr/bin/env python3
"""CrowLLM checker-candidate calibration for Dialectica (2026-11-17).

Runs the SAME corpus as KALIBRASI-C5 (Nemotron) and
KALIBRASI-PEMERIKSA-KEDUA (gpt-oss Cloudflare) -- poison x7 from
calibrate_semantic_c5.build_poison(), clean controls x6 from
build_clean(), plus the GLM debt draft 3b5c0f0c -- against checker
candidates reached through the CrowLLM relay.

DELIBERATE DEVIATION from the two earlier calibrations (user fence,
2026-11-17): the checker prompt sent to the relay is the PUBLIC SHORT
version below (question + draft + generic instruction only). The
internal C5 gate prompt / rubric / finding codes are NEVER sent to
the relay (prompts are visible to the relay operator). Scoring stays
comparable at the FATAL/CLEAN level: a poison item is "caught" when
the verdict is FATAL with >=1 finding whose quote verifies verbatim
against the draft (the same quote-verification discipline the
production parser applies; unverifiable findings are dropped, and a
FATAL whose findings all drop degrades to CLEAN). Poison items that
come back CLEAN get a second sample; the union of the two samples is
the headline score (the convention that produced Nemotron's 7/7).

Transport discipline (connector doc): >=13 s between call starts
(5 req/min free ceiling), retries only on 503/524/429/transport
failure, max 2, with longer pauses. Every call is logged. No serve
code is touched; this is a lab runner only.
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calibrate_semantic_c5 as cal  # noqa: E402

CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.crowllm/bin/client.py")
DRYRUN = os.path.expanduser(
    "~/workspace/research/dialectica/dryrun-2026-11-17")
OUT = os.path.join(HERE, "calibration-crowllm-results.json")
LOG = os.path.join(HERE, "calibration-crowllm-calls.jsonl")

CANDIDATES = [
    "gpt-5.6-sol:free",
    "qwen-3.8-max:free",
    "gemini-3-pro:free",
    "nvidia/nemotron-3.5-super-vl-120b-a12b:free",
]
PROBE_MODEL = "deepseek-v4-flash-0731:free"

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

FORMAT_PROBE_QUESTION = "What is a Merkle tree and what is it used for?"
FORMAT_PROBE_DRAFT = (
    "A Merkle tree is a hash tree invented by Ralph Merkle in 1979. "
    "As conclusively proven by Nakamoto and Buterin in their 2019 paper "
    "\"Merkle Trees Revisited\" (Journal of Cryptographic Engineering, "
    "DOI 10.1234/fake.999), a Merkle tree can verify data integrity in "
    "exactly O(1) time regardless of dataset size, which is why every "
    "blockchain uses them for transaction inclusion proofs.")

PACE_S = 13.0
MAX_TOKENS = 4000
_last_call_start = [0.0]
CALL_COUNT = [0]


def _pace(extra=0.0):
    wait = PACE_S + extra - (time.monotonic() - _last_call_start[0])
    if wait > 0:
        time.sleep(wait)


def call_model(model, prompt, stream=False):
    """One CrowLLM chat call via the connector client. Returns the
    client's parsed JSON dict. Raises RuntimeError on client failure."""
    _pace()
    _last_call_start[0] = time.monotonic()
    CALL_COUNT[0] += 1
    fd, path = __import__("tempfile").mkstemp(suffix=".txt")
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


def call_with_retries(model, prompt, tag):
    """Retry policy: 503/524/429/transport -> up to 2 retries with
    longer pauses; second retry of a 524 switches to streaming.
    Returns (result_dict_or_None, attempts_log)."""
    attempts = []
    stream = False
    for attempt in range(3):
        try:
            res = call_model(model, prompt, stream=stream)
        except Exception as exc:  # transport / client failure
            attempts.append({"attempt": attempt + 1, "ok": False,
                             "error": str(exc)[:300]})
            _log({"tag": tag, "model": model, **attempts[-1]})
            if attempt < 2:
                _pace(extra=30.0 * (attempt + 1))
                continue
            return None, attempts
        status = res.get("status")
        rec = {"attempt": attempt + 1, "ok": status == 200,
               "status": status,
               "latency_s": res.get("latency_s"),
               "usage": res.get("usage"),
               "model_returned": res.get("model_returned")}
        attempts.append(rec)
        _log({"tag": tag, "model": model, **rec})
        if status == 200:
            return res, attempts
        if status in (429, 500, 503, 524) and attempt < 2:
            if status == 524:
                stream = True
            _pace(extra=45.0 * (attempt + 1) if status == 429
                  else 30.0 * (attempt + 1))
            continue
        return None, attempts
    return None, attempts


def _log(rec):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           **rec}
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def parse_verdict(text):
    """Extract the JSON verdict. Returns (verdict, findings, fmt_note)
    or (None, [], note) when unparseable."""
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


def verify_findings(findings, draft):
    """Keep only findings whose quote verifies verbatim (whitespace-
    normalised) against the draft. Returns (kept, dropped)."""
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


def check_item(model, item, tag):
    prompt = PUBLIC_PROMPT.format(
        question=item["question"] or "(no question text archived)",
        draft=item["text"])
    res, attempts = call_with_retries(model, prompt, tag)
    base = {"label": item["label"], "id": item["id"],
            "chars": len(item["text"]), "attempts": attempts,
            "calls": len(attempts)}
    if res is None:
        return {**base, "verdict": "UNAVAILABLE", "kept": [],
                "dropped": 0, "fmt": "transport-failed",
                "latency_s": None}
    verdict, findings, fmt = parse_verdict(res.get("text"))
    if verdict is None:
        return {**base, "verdict": "UNPARSEABLE", "kept": [],
                "dropped": 0, "fmt": fmt,
                "latency_s": res.get("latency_s"),
                "raw_head": (res.get("text") or "")[:200]}
    kept, dropped = verify_findings(findings, item["text"])
    if verdict == "FATAL" and not kept:
        verdict = "CLEAN"
        fmt += "+fatal-all-dropped"
    return {**base, "verdict": verdict, "kept": kept,
            "dropped": dropped, "fmt": fmt,
            "latency_s": res.get("latency_s")}


def load_debt_draft():
    s = json.load(open(os.path.join(
        DRYRUN, "step4-dryruns-results.json"), encoding="utf-8"))
    for row in s:
        if str(row.get("isr", "")).startswith("3b5c0f0c"):
            return {"label": "D-GLM", "id": "3b5c0f0c",
                    "text": row.get("draft") or "",
                    "question": row.get("question") or "",
                    "expected": []}
    return None


def save(state):
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)


def main():
    state = {"prompt": PUBLIC_PROMPT, "candidates": {},
             "probe": None, "total_calls": 0}
    poison = cal.build_poison()
    clean = cal.build_clean()
    debt = load_debt_draft()
    short = [it for it in poison if len(it["text"]) <= 10000]
    giant = [it for it in poison if len(it["text"]) > 10000]
    print(f"corpus: poison={len(poison)} (short {len(short)}, "
          f"giant {len(giant)}), clean={len(clean)}, "
          f"debt={'yes' if debt else 'MISSING'}", flush=True)

    # --- deepseek successor probe: one short call ---
    res, attempts = call_with_retries(
        PROBE_MODEL, "Reply with exactly one word: alive",
        "probe-deepseek")
    state["probe"] = {
        "model": PROBE_MODEL, "attempts": attempts,
        "alive": bool(res and res.get("status") == 200
                      and (res.get("text") or "").strip()),
        "text_head": (res.get("text") or "")[:100] if res else ""}
    state["total_calls"] = CALL_COUNT[0]
    save(state)
    print(f"probe {PROBE_MODEL}: alive={state['probe']['alive']} "
          f"attempts={len(attempts)}", flush=True)

    for model in CANDIDATES:
        print(f"\n=== {model} ===", flush=True)
        entry = {"format": None, "poison_r1": [], "poison_r2": [],
                 "clean": [], "debt": None}
        state["candidates"][model] = entry

        # format probe
        probe_item = {"label": "FMT", "id": "fmt-probe",
                      "text": FORMAT_PROBE_DRAFT,
                      "question": FORMAT_PROBE_QUESTION,
                      "expected": []}
        r = check_item(model, probe_item, f"{model}|fmt")
        entry["format"] = r
        fmt_ok = r["verdict"] in ("FATAL", "CLEAN")
        print(f"  fmt: verdict={r['verdict']} fmt={r['fmt']} "
              f"kept={len(r['kept'])}", flush=True)
        state["total_calls"] = CALL_COUNT[0]
        save(state)

        # poison round 1: short first, then clean controls, then
        # debt draft, then giants (decision value per call first,
        # mirroring the gpt-oss runner's ordering logic)
        for it in short:
            r = check_item(model, it, f"{model}|poison1|{it['id']}")
            entry["poison_r1"].append(r)
            print(f"  poison {it['label']}: {r['verdict']} "
                  f"kept={len(r['kept'])} dropped={r['dropped']}",
                  flush=True)
            state["total_calls"] = CALL_COUNT[0]
            save(state)
        for it in clean:
            r = check_item(model, it, f"{model}|clean|{it['id']}")
            entry["clean"].append(r)
            print(f"  clean {it['label']}: {r['verdict']} "
                  f"kept={len(r['kept'])}", flush=True)
            state["total_calls"] = CALL_COUNT[0]
            save(state)
        if fmt_ok and debt:
            r = check_item(model, debt, f"{model}|debt|3b5c0f0c")
            entry["debt"] = r
            print(f"  debt 3b5c0f0c: {r['verdict']} "
                  f"kept={len(r['kept'])} dropped={r['dropped']}",
                  flush=True)
            state["total_calls"] = CALL_COUNT[0]
            save(state)
        for it in giant:
            r = check_item(model, it, f"{model}|poison1|{it['id']}")
            entry["poison_r1"].append(r)
            print(f"  poison {it['label']}: {r['verdict']} "
                  f"kept={len(r['kept'])} dropped={r['dropped']}",
                  flush=True)
            state["total_calls"] = CALL_COUNT[0]
            save(state)

        # poison round 2 (union convention): only items still CLEAN
        by_id = {it["id"]: it for it in poison}
        for r1 in list(entry["poison_r1"]):
            if r1["verdict"] == "CLEAN":
                r2 = check_item(model, by_id[r1["id"]],
                                f"{model}|poison2|{r1['id']}")
                entry["poison_r2"].append(r2)
                print(f"  poison R2 {r1['label']}: {r2['verdict']}",
                      flush=True)
                state["total_calls"] = CALL_COUNT[0]
                save(state)
        print(f"=== done {model}: total calls so far "
              f"{CALL_COUNT[0]} ===", flush=True)

    state["total_calls"] = CALL_COUNT[0]
    save(state)
    print(f"\nALL DONE. total calls={CALL_COUNT[0]}", flush=True)


if __name__ == "__main__":
    main()
