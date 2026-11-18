import json, sys
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

lst = trued.call("/api/node/isrs", params={"arenaId": "general", "offset": 0, "limit": 1})
isr = lst["isrs"][0]
print("TOTAL ISRS:", lst["total"])
iid = isr["id"]
isos = trued.call(f"/api/node/isos/{iid}")
print("ISOS type:", type(isos), (list(isos.keys()) if isinstance(isos, dict) else len(isos)))
if isinstance(isos, dict):
    for k, v in isos.items():
        print(" key:", k, type(v), (len(v) if isinstance(v, list) else str(v)[:120]))
det = trued.call(f"/api/node/isrs/{iid}")
print("DETAIL keys:", list(det.keys()) if isinstance(det, dict) else type(det))
for k in ("marathonEligibleIsos","marathonActive","concluded","visoCount","status"):
    if isinstance(det, dict) and k in det:
        print(" ", k, "=", json.dumps(det[k])[:300])
