#!/usr/bin/env python3
"""Resume of pull2.py detail phase after runtime restart (read-only GETs).
Reconstructs `want` from saved isrs.json + MONITORED, fetches isos/detail,
saves incrementally every 10 questions so a restart loses at most 10."""
import json, sys, time, glob, os
from datetime import datetime, timezone
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-14/run2-1037"
CUT_MS = int(datetime(2026, 11, 13, 19, 52, tzinfo=timezone.utc).timestamp() * 1000)

MONITORED = {
    "60fa9935-4352-4a4c-9aa7-384de037196c", "472b29a0-8933-41af-ac17-e75bc1a27f32",
    "71f472d6-d3d3-4786-9929-d3fe635eeb52", "2c7efc3e-f25a-440c-aedd-61a2bbb7dac8",
    "1d3efb52-8a6d-41ee-a55e-2a0115bd365c", "1d758352-7ed6-415d-9446-6c382d7e1fc6",
    "f80ac8d3-1d91-449b-bf19-a4c1f6aa8c54", "8ca09770-d156-4d84-a433-0e298feea257",
}
for p in glob.glob("/home/hatch/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued/hidden_files/run-2026-11-14-0900/isr-*.json"):
    try:
        with open(p) as fh: d = json.load(fh)
        if d.get("id"): MONITORED.add(d["id"])
    except Exception:
        pass

def save(name, obj):
    with open(f"{OUT}/{name}", "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    print("saved", name, flush=True)

with open(f"{OUT}/isrs.json") as fh: isrs = json.load(fh)["isrs"]
fresh = sorted([r for r in isrs if (r.get("timestamp") or 0) >= CUT_MS],
               key=lambda r: r["timestamp"], reverse=True)
want = {}
for r in fresh[:80]:
    want[r["id"]] = "fresh"
for qid in MONITORED:
    want[qid] = want.get(qid, "") + "+monitored" if qid in want else "monitored"
print("sample questions:", len(want), flush=True)

isos_by, det_by = {}, {}
for i, (qid, tag) in enumerate(want.items()):
    try:
        isos_by[qid] = trued.call(f"/api/node/isos/{qid}").get("isos", [])
    except Exception as ex:
        isos_by[qid] = {"error": str(ex)}
    try:
        det_by[qid] = trued.call(f"/api/node/isr/{qid}")
    except Exception as ex:
        det_by[qid] = {"error": str(ex)}
    if i % 10 == 0:
        save("isos_by_isr.json", isos_by); save("details_by_isr.json", det_by); save("sample_tags.json", want)
        print(f"isos/detail {i}/{len(want)}", flush=True)
    time.sleep(0.15)
save("isos_by_isr.json", isos_by)
save("details_by_isr.json", det_by)
save("sample_tags.json", want)
nv = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "verified")
nf = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "falsified")
print(f"DONE isos questions={len(isos_by)} verified={nv} falsified={nf}", flush=True)
