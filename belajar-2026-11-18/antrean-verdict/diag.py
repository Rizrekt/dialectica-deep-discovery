#!/usr/bin/env python3
"""Diagnostics round 2 for STUDI-ANTREAN-VERDICT-2026-11-18."""
import json, os, statistics as st
from datetime import datetime, timezone

ROOT = "/home/hatch/workspace/research/dialectica"
OUT = f"{ROOT}/belajar-2026-11-18/antrean-verdict"
det_by = json.load(open(f"{OUT}/details_by_isr.json"))
iso_by = json.load(open(f"{OUT}/isos_by_isr.json"))
meta = json.load(open(f"{OUT}/pull_meta.json"))
NOW = meta["now_ms"]
VERD = ("verified", "falsified")

def upd_ms(i):
    u = i.get("updatedAt")
    if not u: return None
    try: return int(datetime.fromisoformat(u.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception: return None

def fmt(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%d %H:%M:%S")

recs = []
for qid, lst in iso_by.items():
    det = det_by.get(qid) or {}
    q_ts = det.get("timestamp") or 0
    rows = sorted(lst, key=lambda i: i.get("timestamp") or 0)
    n = len(rows)
    for idx, i in enumerate(rows):
        ts = i.get("timestamp") or 0
        um = upd_ms(i)
        recs.append({"qid": qid, "id": i["id"], "ts": ts, "pos": idx + 1, "N": n,
                     "depth": n - idx - 1, "status": i.get("status"),
                     "vc": i.get("verifierCount") or 0, "me": bool(i.get("marathonEligible")),
                     "own": bool(i.get("isOwnAgent")), "q_ts": q_ts, "q_status": det.get("status"),
                     "age_h": (NOW - ts) / 3600000.0,
                     "delay_min": (ts - q_ts) / 60000.0,
                     "lag_h": ((um - ts) / 3600000.0) if (um and i.get("status") in VERD) else None})
ext = [r for r in recs if not r["own"]]

# 1) pilot ISR raw check
print("== 1) PILOT ISR raw ==")
for qid in ["2777178d-2294-4303-9b94-e877fdac95d0", "5e905bef-7e0a-4b31-839c-d59a6688c70d"]:
    det = det_by[qid]
    print(f"{qid[:8]} created {fmt(det['timestamp'])} status={det['status']} isoCount={det.get('isoCount')}")
    rows = sorted(iso_by[qid], key=lambda i: i.get("timestamp") or 0)
    for idx, i in enumerate(rows):
        if i.get("isOwnAgent") or i.get("status") in VERD:
            print(f"   pos={idx+1:>3} ts={fmt(i['timestamp'])} status={i['status']:<10} own={i.get('isOwnAgent')} vc={i.get('verifierCount')} me={i.get('marathonEligible')}")
    early = [i for i in rows[:35]]
    print(f"   first-35 submit span: {fmt(early[0]['timestamp'])} .. {fmt(early[-1]['timestamp'])}")

# 2) marathonEligible x status
print("\n== 2) marathonEligible x status (external, all ages) ==")
for me in (True, False):
    b = [r for r in ext if r["me"] == me]
    import collections
    print(f"  me={me}: n={len(b)}", dict(collections.Counter(r["status"] for r in b)))

# 3) verdict rate by position within N bands (mature >=48h)
print("\n== 3) verdict rate by POSITION within N band (age>=48h) ==")
PB = [(1, 3, "1-3"), (4, 10, "4-10"), (11, 25, "11-25"), (26, 60, "26-60"), (61, 10**9, "61+")]
for nlo, nhi, nname in [(1, 24, "N<25"), (25, 60, "N25-60"), (61, 100, "N61-100"), (101, 10**9, "N>100")]:
    band = [r for r in ext if r["age_h"] >= 48 and nlo <= r["N"] <= nhi]
    if not band: continue
    cells = []
    for lo, hi, name in PB:
        b = [r for r in band if lo <= r["pos"] <= hi]
        if b:
            vr = sum(1 for r in b if r["status"] in VERD) / len(b)
            cells.append(f"pos{name}={vr:.2f}(n{len(b)})")
    print(f"  {nname}: " + " ".join(cells))

# 3b) verdict rate by DEPTH within N>=80 (mature)
print("\n== 3b) verdict rate by DEPTH, N>=80 only (age>=48h) ==")
band = [r for r in ext if r["age_h"] >= 48 and r["N"] >= 80]
for lo, hi, name in [(0, 5, "0-5"), (6, 20, "6-20"), (21, 50, "21-50"), (51, 10**9, "51+")]:
    b = [r for r in band if lo <= r["depth"] <= hi]
    if b:
        vr = sum(1 for r in b if r["status"] in VERD) / len(b)
        print(f"  depth {name}: rate={vr:.3f} n={len(b)}")

# 4) verdict rate by entry delay (minutes after question creation)
print("\n== 4) verdict rate by ENTRY DELAY ==")
DB2 = [(0, 2, "0-2m"), (2, 10, "2-10m"), (10, 30, "10-30m"), (30, 120, "30-120m"),
       (120, 360, "2-6h"), (360, 1440, "6-24h"), (1440, 10**9, ">24h")]
for minage in (24, 48):
    print(f" -- age>={minage}h")
    for lo, hi, name in DB2:
        b = [r for r in ext if r["age_h"] >= minage and lo <= r["delay_min"] < hi]
        if b:
            vr = sum(1 for r in b if r["status"] in VERD) / len(b)
            print(f"    delay {name}: rate={vr:.3f} n={len(b)}")

# 5) lag percentiles
lags = sorted(r["lag_h"] for r in ext if r["lag_h"] is not None and 0 <= r["lag_h"] <= 24 * 90)
if lags:
    q = lambda p: lags[int(p * (len(lags) - 1))]
    print(f"\n== 5) lag submit->verdict (n={len(lags)}): p10={q(.1):.2f}h p25={q(.25):.2f}h p50={q(.5):.2f}h p75={q(.75):.2f}h p90={q(.9):.2f}h p99={q(.99):.1f}h; share<1h={sum(1 for x in lags if x < 1)/len(lags):.3f} share<24h={sum(1 for x in lags if x < 24)/len(lags):.3f}")

# 6) revealed mature: verifierCount==0 share by ISR status
print("\n== 6) revealed age>=48h: share vc==0 (never touched) ==")
for qs in ("settled", "in_progress", "marathon"):
    b = [r for r in ext if r["status"] == "revealed" and r["age_h"] >= 48 and r["q_status"] == qs]
    if b:
        print(f"  ISR {qs}: n={len(b)} vc0={sum(1 for r in b if r['vc'] == 0) / len(b):.3f}")

# 7) verdict rate by ISR status x ISO age (all ISOs)
print("\n== 7) verdict rate by ISR status x ISO age ==")
for qs in ("settled", "in_progress", "marathon"):
    for lo, hi, name in [(0, 24, "<24h"), (24, 48, "24-48h"), (48, 96, "48-96h"), (96, 10**9, ">96h")]:
        b = [r for r in ext if r["q_status"] == qs and lo <= r["age_h"] < hi]
        if b:
            vr = sum(1 for r in b if r["status"] in VERD) / len(b)
            print(f"  ISR {qs} age {name}: rate={vr:.3f} n={len(b)}")

# 8) verdicted share by delay within pilot-like fresh giant ISRs (tag fresh/inprog, N>=60): pos of verdicted
print("\n== 8) verdicted positions in the 5 pilot ISRs (recheck) ==")
PILOT = {"2777178d", "d94d7e34", "635a010d", "d21135d5", "5e905bef"}
for r in sorted([r for r in recs if r["qid"][:8] in PILOT], key=lambda r: (r["qid"], r["pos"])):
    if r["own"] or r["status"] in VERD:
        print(f"  {r['qid'][:8]} pos={r['pos']:>3} N={r['N']} delay={r['delay_min']:.0f}m status={r['status']:<10} own={r['own']} lag={r['lag_h']}")
