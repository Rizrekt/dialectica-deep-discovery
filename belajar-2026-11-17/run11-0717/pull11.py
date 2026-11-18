#!/usr/bin/env python3
"""Read-only fresh pull for STUDI-KOHORT-2026-11-17.

Frame:
- first 48 settled ISRs in listing/activity order (mirror 2026-11-14 panels);
- newest 80 ISRs created since run-10 began (2026-11-17 02:37 WIB);
- 48 monitored ISRs carried from run-10 (tag contains 'monitored').
Uses only existing trued.call endpoints. No platform writes; never prints
session contents.
"""
import json, os, sys, time
from datetime import datetime, timezone
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

AGENT = "8522c990-d4f6-4155-a326-3c3c9802b950"
ROOT = "/home/hatch/workspace/research/dialectica"
OUT = f"{ROOT}/belajar-2026-11-17/run11-0717"
RUN10 = f"{ROOT}/belajar-2026-11-17/run10-0237"
CUT_MS = int(datetime(2026, 11, 16, 19, 37, tzinfo=timezone.utc).timestamp() * 1000)
os.makedirs(OUT, exist_ok=True)
STARTED = datetime.now(timezone.utc).isoformat()

def call(path, params=None, tries=4):
    last = None
    for attempt in range(tries):
        try:
            return trued.call(path, params=params) if params is not None else trued.call(path)
        except (Exception, SystemExit) as ex:
            last = ex
            print(f"retry {attempt+1}/{tries} {path}: {ex}", flush=True)
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"API call failed after {tries} tries: {path}: {last}")

def save(name, obj):
    tmp = f"{OUT}/{name}.tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    os.replace(tmp, f"{OUT}/{name}")
    print("saved", name, flush=True)

meta = {"started_at_utc": STARTED, "cut_fresh_utc": datetime.fromtimestamp(CUT_MS/1000, timezone.utc).isoformat(),
        "frame": {"panels": "first 48 settled in listing order", "fresh": "newest 80 since cut", "monitored": "run10 tags containing monitored"}}
save("pull_meta.json", meta)

state = {}
state["scores"] = call("/api/node/scores")
state["usage"] = call(f"/api/spending/usage/agent/{AGENT}")
state["jobs"] = call(f"/api/node/agents/{AGENT}/jobs")
save("state.json", state)
print("state saved (scores/usage/jobs)", flush=True)

lb = call("/api/node/leaderboard", params={"limit": 100})
save("leaderboard.json", lb)
print("leaderboard rows:", len(lb), flush=True)

isrs, offset = [], 0
while True:
    page = call("/api/node/isrs", params={"arenaId": "general", "offset": offset, "limit": 100})
    rows = page["isrs"]
    isrs.extend(rows)
    total = page["total"]
    print(f"listing offset={offset} got={len(rows)} total={total}", flush=True)
    offset += len(rows)
    if offset >= total or not rows:
        break
    time.sleep(0.15)
save("isrs.json", {"total": total, "isrs": isrs})

panels = [r for r in isrs if r.get("status") == "settled"][:48]
fresh = sorted([r for r in isrs if (r.get("timestamp") or 0) >= CUT_MS], key=lambda r: r["timestamp"], reverse=True)[:80]
with open(f"{RUN10}/sample_tags.json") as fh:
    tags10 = json.load(fh)
monitored = [qid for qid, tag in tags10.items() if "monitored" in tag]

want = {}
for r in panels: want[r["id"]] = "panel"
for r in fresh: want[r["id"]] = (want.get(r["id"], "") + "+fresh") if r["id"] in want else "fresh"
for qid in monitored: want[qid] = (want.get(qid, "") + "+monitored") if qid in want else "monitored"
print(f"sample questions: panels={len(panels)} fresh={len(fresh)} monitored={len(monitored)} union={len(want)}", flush=True)
save("sample_tags.json", want)

isos_by, det_by, errors = {}, {}, {}
for i, (qid, tag) in enumerate(want.items()):
    try:
        isos_by[qid] = call(f"/api/node/isos/{qid}").get("isos", [])
    except Exception as ex:
        isos_by[qid] = {"error": str(ex)}; errors[qid + ":isos"] = str(ex)
    time.sleep(0.15)
    try:
        det_by[qid] = call(f"/api/node/isr/{qid}")
    except Exception as ex:
        det_by[qid] = {"error": str(ex)}; errors[qid + ":detail"] = str(ex)
    if i % 10 == 0:
        print(f"isos/detail {i}/{len(want)} errors={len(errors)}", flush=True)
        save("isos_by_isr.json", isos_by); save("details_by_isr.json", det_by); save("errors.json", errors)
    time.sleep(0.15)

save("isos_by_isr.json", isos_by); save("details_by_isr.json", det_by); save("sample_tags.json", want); save("errors.json", errors)
meta["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
meta["sample_union"] = len(want); meta["errors"] = errors
save("pull_meta.json", meta)
nv = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "verified")
nf = sum(1 for v in isos_by.values() if isinstance(v, list) for x in v if x.get("status") == "falsified")
print(f"DONE questions={len(isos_by)} verified={nv} falsified={nf} errors={len(errors)}", flush=True)
