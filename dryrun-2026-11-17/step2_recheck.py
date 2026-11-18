#!/usr/bin/env python3
"""Retry the C5 check on the stored gpt-oss draft (first attempt's
checker reply was non-JSON -> unavailable; checker variance is a
documented property, one retry is the honest measure)."""
import json
import os
import sys
import time

PROV = os.path.expanduser("~/workspace/research/dialectica/provider")
sys.path.insert(0, PROV)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

import serve_gate  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402

QUESTION = (
    "When an NFT contract blocks all transfers, how can a dedicated "
    "marketplace still enable trading of those tokens, and what "
    "trust assumptions around custody, operator honesty, or "
    "upgrade keys does that trading introduce for buyers and "
    "sellers?")
BASE = os.path.expanduser("~/workspace/research/dialectica/"
                          "dryrun-2026-11-17")


def vyce_first(prompt):
    errs = []
    for label, fn in (("vyce-nemotron", serve_gate._semantic_call_vyce),
                      ("openrouter-nemotron",
                       serve_gate._semantic_call_openrouter)):
        try:
            return fn(prompt), label
        except Exception as ex:  # noqa: BLE001
            errs.append(f"{label}: {type(ex).__name__}: {ex}")
    raise serve_gate.SemanticUnavailable(" || ".join(errs))


print("arm vyce:", cal.arm_vyce_fallback(), flush=True)
d = json.load(open(os.path.join(BASE, "step2-writers-results.json")))
text = d["gptoss"]["gate"]["final_text"]
t0 = time.time()
sem = serve_gate.semantic_check(
    text, question=QUESTION, isr_id="step2-gptoss-retry",
    model_call=vyce_first, mode="shadow",
    log_path=os.path.join(BASE, "step2-semantic-log.jsonl"))
out = {"verdict": sem["verdict"], "checker": sem["checker"],
       "codes": [f["code"] for f in sem["findings"]],
       "subs": [f["sub"] for f in sem["findings"] if f.get("sub")],
       "findings": sem["findings"],
       "dropped": sem["dropped_findings"],
       "error": (sem["error"] or "")[:300],
       "secs": round(time.time() - t0, 1)}
print(json.dumps({k: out[k] for k in ("verdict", "checker", "codes",
                                      "subs", "secs")}), flush=True)
with open(os.path.join(BASE, "step2-gptoss-semantic-retry.json"),
          "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
