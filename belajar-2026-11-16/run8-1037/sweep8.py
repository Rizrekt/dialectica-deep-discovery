#!/usr/bin/env python3
"""Live verdict sweep for BELAJAR-LOG run 8 (2026-11-16 10:37 WIB).
Re-reads the 29 ISRs that contain our ISOs + detail of 2d968d7e and df9cb696,
diffs our ISOs vs sweep7.json "now" (status/verifierCount/updatedAt only —
live ISO payload does not report support/refute, they come back null; the
support/refute cross-check uses verdicts-0900.json, 22:57) and diffs the two
monitored ISRs vs their 23:00 snapshots. All stamps computed from the
updatedAt/timestamp fields actually returned — NO hardcoded ms constants
(corrects the sweep6 defect (fixed run 7)). Read-only; never prints session."""
import json, sys, time
from collections import Counter
from datetime import datetime, timezone, timedelta
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-16/run8-1037"
RUN7 = "/home/hatch/workspace/research/dialectica/belajar-2026-11-16/run7-0237"
RUN0900 = "/home/hatch/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued/hidden_files/run-2026-11-16-0900"
CUT = datetime(2026, 11, 15, 19, 37, tzinfo=timezone.utc)  # 02:37 WIB 16 Nov
OUR = ["fcb7b015", "097df475", "0d76cc7c", "f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"]
WIB = timezone(timedelta(hours=7))

def wib(iso_ts):
    try:
        return datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone(WIB).strftime("%Y-%m-%d %H:%M WIB")
    except Exception:
        return iso_ts

# baseline: sweep7 "now" + verdicts-0900 (support/refute, 09:0x)
s6 = json.load(open(f"{RUN7}/sweep7.json"))["our_isos"]
base6 = {k: v["now"] for k, v in s6.items()}
base23 = {}
for v in json.load(open(f"{RUN0900}/verdicts-0900.json")):
    if any(v["iso"].startswith(o) for o in OUR):
        base23[v["iso"][:8]] = v

# 29 ISR full ids from verdicts-0900.json
ids = sorted({v["isr"] for v in json.load(open(f"{RUN0900}/verdicts-0900.json"))})
print("isr ids:", len(ids), flush=True)

changes = {}
for i, full in enumerate(ids):
    try:
        lst = trued.call(f"/api/node/isos/{full}").get("isos", [])
    except Exception as ex:
        print("ERR", full, ex, flush=True); continue
    for iso in lst:
        if any(iso["id"].startswith(o) for o in OUR):
            key = iso["id"][:8]
            prev6 = base6.get(key, {})
            prev23 = base23.get(key, {})
            cur = {"status": iso.get("status"), "support": iso.get("support"),
                   "refute": iso.get("refute"), "verifierCount": iso.get("verifierCount"),
                   "updatedAt": iso.get("updatedAt")}
            changes[key] = {"isr": full[:8], "prev_sweep6": prev6, "prev_2300": prev23,
                            "now": cur,
                            "status_changed_vs_sweep6": prev6.get("status") != cur["status"],
                            "verifier_changed_vs_sweep6": prev6.get("verifierCount") != cur["verifierCount"],
                            "updatedAt_changed_vs_sweep6": prev6.get("updatedAt") != cur["updatedAt"],
                            "support_refute_vs_2300": {"prev": (prev23.get("support"), prev23.get("refute")),
                                                       "note": "live payload reports support/refute as null; compare status/verifier/updatedAt only"}}
    if i % 10 == 0:
        print(f"sweep {i}/{len(ids)}", flush=True)
    time.sleep(0.15)

with open(f"{OUT}/sweep8.json", "w") as fh:
    json.dump({"our_isos": changes, "n_isr": len(ids),
               "baseline": "sweep7.json our_isos.now + verdicts-0900.json (support/refute)",
               "cut_wib": "2026-11-16 02:37 WIB"}, fh, ensure_ascii=False, indent=1)

# monitored ISRs: 2d968d7e + df9cb696, diff vs 23:00 snapshots
def monitored(short, full_id, snap_file):
    det = trued.call(f"/api/node/isr/{full_id}")
    isos = trued.call(f"/api/node/isos/{full_id}").get("isos", [])
    with open(f"{OUT}/detail-{short}.json", "w") as fh:
        json.dump(det, fh, ensure_ascii=False, indent=1)
    with open(f"{OUT}/isos-{short}.json", "w") as fh:
        json.dump(isos, fh, ensure_ascii=False, indent=1)
    snap = json.load(open(f"{RUN0900}/{snap_file}"))
    old_by_id = {x["id"]: x for x in snap}
    new_by_id = {x["id"]: x for x in isos}
    status_changes, new_isos = [], []
    for iid, cur in new_by_id.items():
        old = old_by_id.get(iid)
        if old is None:
            new_isos.append({"id": iid[:8], "status": cur.get("status"),
                             "support": cur.get("support"), "refute": cur.get("refute"),
                             "verifierCount": cur.get("verifierCount"),
                             "timestamp_wib": wib(cur.get("timestamp", "")) if cur.get("timestamp") else None,
                             "updatedAt_wib": wib(cur.get("updatedAt", "")) if cur.get("updatedAt") else None})
        elif old.get("status") != cur.get("status") or old.get("updatedAt") != cur.get("updatedAt"):
            status_changes.append({"id": iid[:8],
                                   "old": (old.get("status"), old.get("support"), old.get("refute"), old.get("verifierCount"), old.get("updatedAt")),
                                   "new": (cur.get("status"), cur.get("support"), cur.get("refute"), cur.get("verifierCount"), cur.get("updatedAt"))})
    # verdicts whose updatedAt is >= CUT (computed from the field, not hardcoded)
    cut_iso = CUT.isoformat()
    new_verdicts = [{"id": x["id"][:8], "status": x.get("status"),
                     "updatedAt_wib": wib(x.get("updatedAt", "")) if x.get("updatedAt") else None}
                    for x in isos
                    if x.get("status") in ("verified", "falsified") and x.get("updatedAt") and x["updatedAt"] >= cut_iso]
    return {"short": short, "status": det.get("status"),
            "viso": len(det.get("marathonEligibleIsos") or []),
            "awarded": sum(1 for e in det.get("marathonEligibleIsos") or [] if e.get("awarded")),
            "isos_status_counts": dict(Counter(x.get("status") for x in isos)),
            "n_isos_now": len(isos), "n_isos_0900": len(snap),
            "status_changes_vs_0900": status_changes,
            "new_isos_vs_0900": new_isos,
            "verdicts_updated_since_cut": new_verdicts}

m2 = monitored("2d968d7e", "2d968d7e-d6f2-450a-be81-99731b3029e7", "isos-2d968d7e.json")
time.sleep(0.15)
mdf = monitored("df9cb696", "df9cb696-e612-4b2d-be50-72be6ff47445", "isos-df9cb696.json")

with open(f"{OUT}/sweep8-monitored.json", "w") as fh:
    json.dump({"2d968d7e": m2, "df9cb696": mdf}, fh, ensure_ascii=False, indent=1)

print("OUR ISOS:")
print(json.dumps(changes, ensure_ascii=False, indent=1))
print("2d968d7e:", json.dumps(m2, ensure_ascii=False, indent=1))
print("df9cb696:", json.dumps(mdf, ensure_ascii=False, indent=1))
print("36492578 now:", [(x.get("status"), x.get("support"), x.get("refute"), x.get("verifierCount"), x.get("updatedAt"))
                        for x in json.load(open(f"{OUT}/isos-2d968d7e.json")) if x["id"].startswith("36492578")])
print("DONE")
