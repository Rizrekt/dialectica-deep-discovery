#!/usr/bin/env python3
"""Live verdict sweep for BELAJAR-LOG run 6 (2026-11-15 18:37 WIB).
Re-reads the 29 ISRs that contain our ISOs (ids from run-2026-11-15-1700
isos-*.json filenames) + detail of 2d968d7e (drill focus), and diffs our
ISOs' statuses vs verdicts-1700.json. Read-only; never prints session."""
import json, sys, glob, os, time
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-15/run6-1837"
RUN1700 = "/home/hatch/workspace/goals/dialectica-rutinitas-ringan-pemburu-slot-trued/hidden_files/run-2026-11-15-1700"
OUR = ["fcb7b015", "097df475", "0d76cc7c", "f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"]

ids = []
old = {}
for v in json.load(open(f"{RUN1700}/verdicts-1700.json")):
    ids.append(v["isr"])
    old[v["iso"][:8]] = {"status": v.get("status"), "support": v.get("support"),
                         "refute": v.get("refute"), "verifierCount": v.get("verifier"),
                         "updatedAt": v.get("updatedAt")}
ids = sorted(set(ids))
print("isr ids:", len(ids), flush=True)

now, changes = {}, {}
for i, p in enumerate(ids):
    full = None
    # full id: from the isos file itself (first iso's isrId) or from details file
    try:
        rows = json.load(open(f"{RUN1700}/isos-{p[:8]}.json"))
        if rows and isinstance(rows, list) and rows[0].get("isrId"):
            full = rows[0]["isrId"]
    except Exception:
        pass
    if not full:
        # fall back: detail file
        try:
            d = json.load(open(f"{RUN1700}/detail-{p}.json"))
            full = d.get("id")
        except Exception:
            pass
    if not full:
        print("skip (no full id):", p, flush=True); continue
    try:
        lst = trued.call(f"/api/node/isos/{full}").get("isos", [])
    except Exception as ex:
        print("ERR", p, ex, flush=True); continue
    now[p] = lst
    for iso in lst:
        if any(iso["id"].startswith(o) for o in OUR):
            key = iso["id"][:8]
            prev = old.get(key, {})
            cur = {"status": iso.get("status"), "support": iso.get("support"),
                   "refute": iso.get("refute"), "verifierCount": iso.get("verifierCount"),
                   "updatedAt": iso.get("updatedAt")}
            changes[key] = {"prev": prev, "now": cur,
                            "changed": (prev.get("status") != cur["status"] or
                                        prev.get("support") != cur["support"] or
                                        prev.get("refute") != cur["refute"])}
    if i % 10 == 0:
        print(f"sweep {i}/{len(ids)}", flush=True)
    time.sleep(0.15)

with open(f"{OUT}/sweep6.json", "w") as fh:
    json.dump({"our_isos": changes, "n_isr": len(now)}, fh, ensure_ascii=False, indent=1)

# 2d968d7e detail (drill focus): new verdicts/awards since 17:00
det = trued.call("/api/node/isr/2d968d7e-0000-0000-0000-000000000000") if False else None
# resolve full id from run-1700 detail file
d1700 = json.load(open(f"{RUN1700}/detail-2d968d7e.json"))
full2 = d1700.get("id")
det2 = trued.call(f"/api/node/isr/{full2}")
isos2 = trued.call(f"/api/node/isos/{full2}").get("isos", [])
with open(f"{OUT}/detail-2d968d7e.json", "w") as fh:
    json.dump(det2, fh, ensure_ascii=False, indent=1)
with open(f"{OUT}/isos-2d968d7e.json", "w") as fh:
    json.dump(isos2, fh, ensure_ascii=False, indent=1)
from collections import Counter
print("OUR ISOS:")
print(json.dumps(changes, ensure_ascii=False, indent=1))
print("2d968d7e status:", det2.get("status"), "viso:", len(det2.get("marathonEligibleIsos") or []),
      "awarded:", sum(1 for e in det2.get("marathonEligibleIsos") or [] if e.get("awarded")))
print("2d968d7e isos status counts:", dict(Counter(x.get("status") for x in isos2)))
print("2d968d7e verified since 17:00 (ts>=1763288400000):",
      [x["id"][:8] for x in isos2 if x.get("status") == "verified" and (x.get("timestamp") or 0) >= 1763200800000])
print("2d968d7e falsified since 17:00:",
      [x["id"][:8] for x in isos2 if x.get("status") == "falsified" and (x.get("timestamp") or 0) >= 1763200800000])
print("36492578 now:", [ (x.get("status"), x.get("support"), x.get("refute")) for x in isos2 if x["id"].startswith("36492578")])
print("DONE")
