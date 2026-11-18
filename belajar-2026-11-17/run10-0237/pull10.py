#!/usr/bin/env python3
"""Read-only fresh pull for BELAJAR-LOG run 2026-11-17 02:37 WIB (T13 watcher, run 10).
Incremental vs studi 02:40: own state + leaderboard + full listing +
isos/detail for questions created since 18:37 WIB 16 Nov + monitored ISRs.
Public endpoints + own-account state via trued.call. Never prints session
contents. No writes to platform."""
import json, sys, time, glob
from datetime import datetime, timezone
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

AGENT = "8522c990-d4f6-4155-a326-3c3c9802b950"
OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-17/run10-0237"
CUT_MS = int(datetime(2026, 11, 16, 11, 37, tzinfo=timezone.utc).timestamp() * 1000)  # 2026-11-16 18:37 WIB = 2026-11-16 11:37 UTC

MONITORED = {
    "60fa9935-4352-4a4c-9aa7-384de037196c", "472b29a0-8933-41af-ac17-e75bc1a27f32",
    "71f472d6-d3d3-4786-9929-d3fe635eeb52", "2c7efc3e-f25a-440c-aedd-61a2bbb7dac8",
    "1d3efb52-8a6d-41ee-a55e-2a0115bd365c", "1d758352-7ed6-415d-9446-6c382d7e1fc6",
    "f80ac8d3-1d91-449b-bf19-a4c1f6aa8c54", "8ca09770-d156-4d84-a433-0e298feea257",
}
# full ids of monitored ISRs from hunt run dirs (FIX run 7: files are isos-*.json
# containing LISTS of ISOs; full ISR id lives in rows[0]["isrId"])
for rundir in ("run-2026-11-16-1500", "run-2026-11-16-1700", "run-2026-11-16-1900", "run-2026-11-16-2100", "run-2026-11-16-2300"):
    for p in glob.glob(f"/home/hatch/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued/hidden_files/{rundir}/isos-*.json"):
        try:
            with open(p) as fh: d = json.load(fh)
            if isinstance(d, list) and d and d[0].get("isrId"):
                MONITORED.add(d[0]["isrId"])
            elif isinstance(d, dict) and d.get("id"):
                MONITORED.add(d["id"])
        except Exception:
            pass

def save(name, obj):
    with open(f"{OUT}/{name}", "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    print("saved", name, flush=True)

import os
os.makedirs(OUT, exist_ok=True)

state = {}
state["scores"] = trued.call("/api/node/scores")
state["usage"] = trued.call(f"/api/spending/usage/agent/{AGENT}")
state["jobs"] = trued.call(f"/api/node/agents/{AGENT}/jobs")
save("state.json", state)
print("scores:", json.dumps(state["scores"])[:500], flush=True)

lb = trued.call("/api/node/leaderboard", params={"limit": 100})
save("leaderboard.json", lb)
print("leaderboard rows:", len(lb), flush=True)

isrs, offset = [], 0
while True:
    page = trued.call("/api/node/isrs", params={"arenaId": "general", "offset": offset, "limit": 100})
    rows = page["isrs"]
    isrs.extend(rows)
    total = page["total"]
    print(f"listing offset={offset} got={len(rows)} total={total}", flush=True)
    offset += len(rows)
    if offset >= total or not rows:
        break
    time.sleep(0.15)
save("isrs.json", {"total": total, "isrs": isrs})

fresh = sorted([r for r in isrs if (r.get("timestamp") or 0) >= CUT_MS],
               key=lambda r: r["timestamp"], reverse=True)
print("fresh since 18:37 WIB:", len(fresh), flush=True)
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
    if i % 20 == 0:
        print(f"isos/detail {i}/{len(want)}", flush=True)
    time.sleep(0.15)
save("isos_by_isr.json", isos_by)
save("details_by_isr.json", det_by)
save("sample_tags.json", want)
nv = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "verified")
nf = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "falsified")
print(f"DONE isos questions={len(isos_by)} verified={nv} falsified={nf}", flush=True)
