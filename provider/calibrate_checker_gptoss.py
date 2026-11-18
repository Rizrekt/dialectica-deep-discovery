#!/usr/bin/env python3
"""Calibration runner: gpt-oss-120b (Cloudflare) as SECOND checker
for the C5 semantic stage — candidate backup checker lane.

Runs serve_gate.semantic_check (shadow mode, the PRODUCTION prompt
and parser, unmodified) over the SAME corpora as the Nemotron
calibration (calibrate_semantic_c5 builders: 7 historical falsified
+ 6 VERIFIED field answers + 3 fixtures), with the checker lane
swapped for @cf/openai/gpt-oss-120b via the registered Cloudflare
connector client. Plus the two C5-unmeasured drafts left over from
PERBAIKAN-PENGHAMBAT-2026-11-17 (the gpt-oss writer draft and the
GLM draft 3b5c0f0c).

Comparators (Nemotron, KALIBRASI-C5-2026-11-17.md): poison 7/7 over
two rounds; verified false-fatal 4/6. Method note: the Nemotron
numbers were produced pre-segmentation (single call, 28k cap);
this run uses the CURRENT production path (segmented at 10k) —
the path gpt-oss would actually serve in.

Budget discipline: cumulative Cloudflare neurons for THIS run are
metered per call from the API usage object; the run stops starting
new items once the cumulative total reaches NEURON_BUDGET (3,000,
per task brief) and marks the rest NOT-RUN. Every call's usage is
also appended to token-usage.jsonl (lane cloudflare-gptoss, isr
tag c5calib-*) so the account-wide daily accounting stays honest.
OpenRouter is never touched.

Usage: python3 calibrate_checker_gptoss.py [--ids fcb7b015,...]
       [--out path.json]
"""
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

import serve_gate  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402

CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.cloudflare-workers-ai/bin/"
    "client.py")
MODEL = "@cf/openai/gpt-oss-120b"
MAX_TOKENS = 8000  # same budget as the OpenRouter checker lane
NEURON_BUDGET = 3000.0
USAGE_LOG = os.path.join(HERE, "token-usage.jsonl")
SEM_LOG = os.path.join(HERE, "calibration-gptoss-semantic-log.jsonl")
BASE = os.path.expanduser("~/workspace/research/dialectica/"
                          "dryrun-2026-11-17")

CALLS = []  # per-call metering records for THIS run
# The probe call (poison #1, run separately ahead of the full run)
# already spent neurons on this calibration; seed the counter so
# the 3,000 cap covers ALL calibration spend, probe included.
CUM_NEURONS = float(os.environ.get("C5CALIB_START_NEURONS", "0"))


class BudgetStop(Exception):
    """Calibration neuron budget reached — not a lane failure."""


def _log_usage(usage, prompt_chars, content_chars):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": "cloudflare-gptoss",
        "model": MODEL,
        "isr": "c5calib-gptoss",
        "usage": usage,
        "answer_chars": content_chars,
        "prompt_chars": prompt_chars,
    }
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"calibrate-gptoss: usage log write failed: {ex}",
              file=sys.stderr)


def gptoss_call(prompt):
    """One checker call on the Cloudflare lane. Returns
    (raw_text, lane_label); raises on any unusable reply, mirroring
    the failure semantics of the other checker lanes (an empty or
    non-200 reply is a failed call, counted unavailable upstream).
    The client's extract_answer_text already separates the model's
    `reasoning` scratchpad from `content`; reasoning length is
    recorded as a diagnostic, never merged into the reply."""
    global CUM_NEURONS
    if CUM_NEURONS >= NEURON_BUDGET:
        raise BudgetStop(
            f"neuron budget {NEURON_BUDGET:.0f} reached "
            f"({CUM_NEURONS:.1f})")
    with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", dir=HERE, delete=False,
            encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, CLIENT, "run", "--model", MODEL,
             "--prompt-file", prompt_path,
             "--max-tokens", str(MAX_TOKENS)],
            capture_output=True, text=True, timeout=660)
    finally:
        os.unlink(prompt_path)
    if proc.returncode != 0:
        CALLS.append({"ok": False, "neurons": None,
                      "error": f"client rc={proc.returncode}: "
                               f"{proc.stderr.strip()[:200]}"})
        raise RuntimeError(CALLS[-1]["error"])
    result = json.loads(proc.stdout)
    usage = result.get("usage") or {}
    neurons = usage.get("neurons")
    if isinstance(neurons, (int, float)):
        CUM_NEURONS += neurons
    _log_usage(usage, len(prompt), result.get("chars") or 0)
    rec = {"ok": result.get("status") == 200
           and bool((result.get("text") or "").strip()),
           "neurons": neurons,
           "reasoning_chars": result.get("reasoning_chars"),
           "content_chars": result.get("chars"),
           "latency_s": result.get("latency_s"),
           "status": result.get("status"),
           "usage": usage}
    CALLS.append(rec)
    if not rec["ok"]:
        raise RuntimeError(
            f"jawaban pemeriksa tak terpakai: status="
            f"{result.get('status')} chars={result.get('chars')} "
            f"reasoning_chars={result.get('reasoning_chars')}")
    return result["text"], "cloudflare-gptoss"


def build_debt():
    """The two drafts whose C5 check stayed unmeasured in
    PERBAIKAN-PENGHAMBAT langkah 2/4 (checker lane unavailable)."""
    items = []
    d = json.load(open(os.path.join(BASE, "step2-writers-results.json"),
                       encoding="utf-8"))
    items.append({
        "label": "D-GPTOSS", "id": "step2-gptoss",
        "text": d["gptoss"]["gate"]["final_text"],
        "question": "When an NFT contract blocks all transfers, how "
                    "can a dedicated marketplace still enable trading "
                    "of those tokens, and what trust assumptions "
                    "around custody, operator honesty, or upgrade "
                    "keys does that trading introduce for buyers and "
                    "sellers?",
        "expected": []})
    s = json.load(open(os.path.join(BASE, "step4-dryruns-results.json"),
                       encoding="utf-8"))
    for row in s:
        if str(row.get("isr", "")).startswith("3b5c0f0c"):
            items.append({
                "label": "D-GLM", "id": "3b5c0f0c",
                "text": row.get("draft") or "",
                "question": row.get("question") or "",
                "expected": []})
    return items


def main():
    args = sys.argv[1:]
    out_path = os.path.join(HERE, "calibration-c5-gptoss-results.json")
    if "--out" in args:
        out_path = args[args.index("--out") + 1]
    ids = None
    if "--ids" in args:
        ids = {s.strip() for s in args[args.index("--ids") + 1]
               .split(",") if s.strip()}

    # Order chosen for budget-risk management. Measured probe cost
    # (poison #1): 221.7 neurons for ONE segment call (4,708 tokens;
    # reasoning ~1.8k of the 1,976 completion tokens) — the full
    # 34-call corpus cannot fit the 3,000 cap, so items are ordered
    # by decision value per neuron: short poisons, then the clean
    # corpus (single-segment items first), then the debt drafts,
    # then fixtures, then the giant serve traces. The runner stops
    # starting items once the cap is reached; the rest are NOT-RUN.
    poison = cal.build_poison()
    short = [it for it in poison if len(it["text"]) <= 10000]
    giant = [it for it in poison if len(it["text"]) > 10000]
    clean = sorted(
        cal.build_clean(),
        key=lambda it: len(serve_gate._split_draft_segments(
            it["text"])))
    corpus = [("poison", it) for it in short]
    corpus += [("clean", it) for it in clean]
    corpus += [("debt", it) for it in build_debt()]
    corpus += [("fixture", it) for it in cal.build_fixtures()]
    corpus += [("poison", it) for it in giant]
    if ids:
        corpus = [(k, it) for k, it in corpus if it["id"] in ids]

    results = []
    stopped = False
    for kind, item in corpus:
        if stopped or CUM_NEURONS >= NEURON_BUDGET:
            stopped = True
            results.append({**{k: item[k] for k in
                               ("label", "id", "expected")},
                            "kind": kind, "verdict": "NOT-RUN",
                            "codes": [], "findings": [],
                            "chars": len(item["text"])})
            print(f"{item['label']} {item['id']} [{kind}] NOT-RUN "
                  f"(budget {CUM_NEURONS:.1f}/{NEURON_BUDGET:.0f})",
                  flush=True)
            continue
        if not item["text"]:
            results.append({**{k: item[k] for k in
                               ("label", "id", "expected")},
                            "kind": kind, "verdict": "NO-TEXT",
                            "codes": [], "findings": [], "chars": 0})
            continue
        calls_before = len(CALLS)
        t0 = time.time()
        res = serve_gate.semantic_check(
            item["text"], question=item["question"],
            isr_id="c5calib-" + item["id"], mode="shadow",
            model_call=gptoss_call, log_path=SEM_LOG)
        new_calls = CALLS[calls_before:]
        codes = [f["code"] for f in res["findings"]]
        subs = [f["sub"] for f in res["findings"] if f.get("sub")]
        item_neurons = sum(c["neurons"] for c in new_calls
                           if isinstance(c.get("neurons"),
                                           (int, float)))
        print(f"{item['label']} {item['id']} [{kind}] "
              f"verdict={res['verdict']} codes={codes} subs={subs} "
              f"dropped={res['dropped_findings']} "
              f"segs={res.get('segments_ok')}/{res.get('segments')} "
              f"calls={len(new_calls)} neurons={item_neurons:.1f} "
              f"cum={CUM_NEURONS:.1f} "
              f"secs={time.time() - t0:.1f} err={res['error']}",
              flush=True)
        results.append({
            "label": item["label"], "id": item["id"], "kind": kind,
            "expected": item["expected"], "verdict": res["verdict"],
            "checker": res["checker"], "codes": codes, "subs": subs,
            "findings": res["findings"],
            "dropped_findings": res["dropped_findings"],
            "segments": res.get("segments"),
            "segments_ok": res.get("segments_ok"),
            "budget_truncated": "BudgetStop" in (res["error"] or ""),
            "error": res["error"], "chars": len(item["text"]),
            "calls": new_calls, "neurons": item_neurons})
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump({"results": results, "calls": CALLS,
                       "cum_neurons": CUM_NEURONS},
                      fh, ensure_ascii=False, indent=1)
    print(f"calibrate-gptoss: {len(CALLS)} calls, "
          f"{CUM_NEURONS:.1f} neurons total -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
