#!/usr/bin/env python3
"""Supplementary STREAMING pass for the nemotron-VL candidate.

The main CrowLLM calibration run (calibrate_checker_crowllm.py,
non-streaming) returned HTTP 200 with EMPTY text for 10 of the
nemotron-VL items. The connector doc's remedy for empty/long
responses is streaming. This pass re-runs exactly those unresolved
items with --stream forced, same public prompt, same pacing, and
labels every result as a streaming supplement (the main table keeps
the non-streaming numbers untouched). Poison items that come back
CLEAN here get one more streaming sample (union convention).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calibrate_checker_crowllm as run  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402

MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b:free"
OUT = os.path.join(HERE, "calibration-crowllm-nemotron-stream.json")

_orig_call = run.call_model


def streaming_call(model, prompt, stream=False):
    return _orig_call(model, prompt, stream=True)


def main():
    run.call_model = streaming_call
    main_res = json.load(open(run.OUT, encoding="utf-8"))
    entry = main_res["candidates"][MODEL]
    unresolved = []
    for r in entry["poison_r1"]:
        if r["verdict"] == "UNPARSEABLE":
            unresolved.append(("poison", r["id"]))
    for r in entry["clean"]:
        if r["verdict"] == "UNPARSEABLE":
            unresolved.append(("clean", r["id"]))
    if entry["debt"] and entry["debt"]["verdict"] == "UNPARSEABLE":
        unresolved.append(("debt", "3b5c0f0c"))
    print(f"unresolved items: {unresolved}", flush=True)

    poison = {it["id"]: it for it in cal.build_poison()}
    clean = {it["id"]: it for it in cal.build_clean()}
    debt = run.load_debt_draft()
    pools = {"poison": poison, "clean": clean,
             "debt": {"3b5c0f0c": debt}}
    out = {"model": MODEL, "mode": "streaming-supplement",
           "items": []}
    for kind, iid in unresolved:
        item = pools[kind][iid]
        r = run.check_item(MODEL, item, f"{MODEL}|stream|{iid}")
        r["kind"] = kind
        out["items"].append(r)
        print(f"  {kind} {iid}: {r['verdict']} kept={len(r['kept'])} "
              f"fmt={r['fmt']}", flush=True)
        if kind == "poison" and r["verdict"] == "CLEAN":
            r2 = run.check_item(MODEL, item,
                                f"{MODEL}|stream2|{iid}")
            r2["kind"] = "poison-r2"
            out["items"].append(r2)
            print(f"  poison-r2 {iid}: {r2['verdict']}", flush=True)
    out["total_calls"] = run.CALL_COUNT[0]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"STREAM PASS DONE. calls={run.CALL_COUNT[0]}", flush=True)


if __name__ == "__main__":
    main()
