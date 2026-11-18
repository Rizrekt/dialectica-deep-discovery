#!/usr/bin/env python3
"""Genuine 5k-segment retry for f131675d: patches the splitter
itself (the module constant patch in run 2b did NOT take effect —
_split_draft_segments binds its default cap at definition time,
so run 2b silently repeated the 10k configuration)."""
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

_orig_split = serve_gate._split_draft_segments


def split5k(draft, cap=5000):
    return _orig_split(draft, 5000)


serve_gate._split_draft_segments = split5k
HF = os.path.expanduser(
    "~/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued"
    "/hidden_files")
OUT = os.path.expanduser(
    "~/workspace/research/dialectica/dryrun-2026-11-17/"
    "ramalan22-round2c-f131675d.json")


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
text = find_text("f131675d", "c7cc33a2")
q = find_question("c7cc33a2")
print("chars:", len(text), "segments at 5k:",
      len(split5k(text)), flush=True)
t0 = time.time()
res = serve_gate.semantic_check(
    text, question=q, isr_id="f131675d", model_call=vyce_first,
    mode="shadow",
    log_path=os.path.expanduser(
        "~/workspace/research/dialectica/dryrun-2026-11-17/"
        "ramalan22-r2c-semantic-log.jsonl"))
rec = {"id": "f131675d", "isr": "c7cc33a2", "chars": len(text),
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
