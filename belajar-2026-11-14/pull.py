#!/usr/bin/env python3
"""Read-only fresh pull for STUDI-KOHORT-2026-11-14 (T13 learning loop).
Public node endpoints + own-account state via trued.call (same pattern as
hunt read_state.py). Never prints session contents. No writes to platform."""
import json, sys, time
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

AGENT = "8522c990-d4f6-4155-a326-3c3c9802b950"
OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-14"
FRESH_CUT_MS = 1794294000000  # 2026-11-10T07:00:00Z ~ §30 pull time (14:4x WIB = 07:4x UTC)

def save(name, obj):
    with open(f"{OUT}/{name}", "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    print("saved", name, flush=True)

# 1. own state
state = {}
state["scores"] = trued.call("/api/node/scores")
state["usage"] = trued.call(f"/api/spending/usage/agent/{AGENT}")
state["jobs"] = trued.call(f"/api/node/agents/{AGENT}/jobs")
state["agent_show_raw"] = None
save("state.json", state)
print("scores:", json.dumps(state["scores"])[:400], flush=True)

# 2. leaderboard
lb = trued.call("/api/node/leaderboard", params={"limit": 100})
save("leaderboard.json", lb)
print("leaderboard rows:", len(lb), flush=True)

# 3. full ISR listing
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

# 4. samples
# (a) judge panels: listing order (activity), settled, first 48
settled = [r for r in isrs if r.get("status") == "settled"]
panels = settled[:48]
# (b) fresh era: created >= cut, newest first, 70
fresh = sorted([r for r in isrs if (r.get("timestamp") or 0) >= FRESH_CUT_MS],
               key=lambda r: r["timestamp"], reverse=True)[:70]
want = {}
for r in panels: want[r["id"]] = "panel"
for r in fresh: want[r["id"]] = want.get(r["id"], "") + "+fresh" if r["id"] in want else "fresh"
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
