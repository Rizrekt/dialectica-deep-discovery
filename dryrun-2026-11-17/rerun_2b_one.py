#!/usr/bin/env python3
"""Single-item round-2b retry: f8801972 at 5k segments (the first
2b run was killed by a service restart before writing results)."""
import glob
import json
import os
import sys
import time

PROV = os.path.expanduser("~/workspace/research/dialectica/provider")
sys.path.insert(0, PROV)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

import serve_gate  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402

serve_gate._SEMANTIC_SEGMENT_CHARS = 5000
HF = os.path.expanduser(
    "~/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued"
    "/hidden_files")
OUT = os.path.expanduser(
    "~/workspace/research/dialectica/dryrun-2026-11-17/"
    "ramalan22-round2b-f8801972.json")


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def find_text(iso_id, isr):
    for path in sorted(glob.glob(os.path.join(HF, "run-*",
                                              f"isos-{isr}.json"))):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        for iso in walk(data):
            if str(iso.get("id", "")).startswith(iso_id):
                try:
                    return iso["reveal"]["data"]["structured_data"][
                        "answer"]
                except (KeyError, TypeError):
                    continue
    return ""


def find_question(isr):
    for path in sorted(glob.glob(os.path.join(HF, "run-*",
                                              f"isr-{isr}.json"))):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        q = str(data.get("content") or data.get("title") or "")
        if q:
            return q
    return ""


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
text = find_text("f8801972", "c6b0eadc")
q = find_question("c6b0eadc")
print("chars:", len(text), "qchars:", len(q), flush=True)
t0 = time.time()
res = serve_gate.semantic_check(
    text, question=q, isr_id="f8801972", model_call=vyce_first,
    mode="shadow",
    log_path=os.path.expanduser(
        "~/workspace/research/dialectica/dryrun-2026-11-17/"
        "ramalan22-r2b-semantic-log.jsonl"))
rec = {"id": "f8801972", "isr": "c6b0eadc", "chars": len(text),
       "segment_chars": 5000, "verdict": res["verdict"],
       "checker": res["checker"],
       "codes": [f["code"] for f in res["findings"]],
       "subs": [f["sub"] for f in res["findings"] if f.get("sub")],
       "findings": res["findings"],
       "dropped": res["dropped_findings"],
       "segments": res.get("segments"),
       "segments_ok": res.get("segments_ok"),
       "error": (res["error"] or "")[:600],
       "secs": round(time.time() - t0, 1)}
print(json.dumps({k: rec[k] for k in ("verdict", "segments_ok",
                                      "segments", "codes", "secs")}),
      flush=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=1)
print("done ->", OUT, flush=True)
