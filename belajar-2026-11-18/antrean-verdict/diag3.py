#!/usr/bin/env python3
"""Diagnostics round 3: era split, refined diff, vc portrait."""
import json, collections, statistics as st
from datetime import datetime, timezone

ROOT = "/home/hatch/workspace/research/dialectica"
OUT = f"{ROOT}/belajar-2026-11-18/antrean-verdict"
RUN11 = f"{ROOT}/belajar-2026-11-17/run11-0717"
det_by = json.load(open(f"{OUT}/details_by_isr.json"))
iso_by = json.load(open(f"{OUT}/isos_by_isr.json"))
meta = json.load(open(f"{OUT}/pull_meta.json"))
NOW = meta["now_ms"]
VERD = ("verified", "falsified")
NOV1 = int(datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp() * 1000)
NOV14 = int(datetime(2026, 11, 14, tzinfo=timezone.utc).timestamp() * 1000)

def upd_ms(i):
    u = i.get("updatedAt")
    if not u: return None
    try: return int(datetime.fromisoformat(u.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception: return None

recs = []
for qid, lst in iso_by.items():
    det = det_by.get(qid) or {}
    q_ts = det.get("timestamp") or 0
    rows = sorted(lst, key=lambda i: i.get("timestamp") or 0)
    n = len(rows)
    for idx, i in enumerate(rows):
        ts = i.get("timestamp") or 0
        recs.append({"qid": qid, "id": i["id"], "ts": ts, "pos": idx + 1, "N": n,
                     "depth": n - idx - 1, "status": i.get("status"),
                     "vc": i.get("verifierCount") or 0, "me": bool(i.get("marathonEligible")),
                     "own": bool(i.get("isOwnAgent")), "q_ts": q_ts, "q_status": det.get("status"),
                     "age_h": (NOW - ts) / 3600000.0, "delay_min": (ts - q_ts) / 60000.0})
ext = [r for r in recs if not r["own"]]
def vr(rows): return sum(1 for r in rows if r["status"] in VERD) / len(rows) if rows else float("nan")

PB = [(1, 3, "1-3"), (4, 10, "4-10"), (11, 25, "11-25"), (26, 60, "26-60"), (61, 10**9, "61+")]
print("== ERA SPLIT: verdict rate by position (age>=48h) ==")
for name, lo, hi in [("old (<1 Nov)", 0, NOV1), ("mid (1-14 Nov)", NOV1, NOV14), ("flood era (>=14 Nov)", NOV14, 10**18)]:
    band = [r for r in ext if r["age_h"] >= 48 and lo <= r["q_ts"] < hi]
    cells = []
    for plo, phi, pn in PB:
        b = [r for r in band if plo <= r["pos"] <= phi]
        if b: cells.append(f"{pn}={vr(b):.2f}(n{len(b)})")
    print(f"  {name}: n={len(band)} " + " ".join(cells))

print("\n== FLOOD ERA only: verdict rate by entry delay (age>=24h) ==")
band = [r for r in ext if r["q_ts"] >= NOV14 and r["age_h"] >= 24]
for lo, hi, name in [(0, 2, "0-2m"), (2, 10, "2-10m"), (10, 30, "10-30m"), (30, 120, "30-120m"), (120, 360, "2-6h"), (360, 1440, "6-24h"), (1440, 10**9, ">24h")]:
    b = [r for r in band if lo <= r["delay_min"] < hi]
    if b: print(f"  delay {name}: rate={vr(b):.3f} n={len(b)}")

print("\n== FLOOD ERA, N>=60: verdict rate by position (age>=24h) ==")
band = [r for r in ext if r["q_ts"] >= NOV14 and r["age_h"] >= 24 and r["N"] >= 60]
for plo, phi, pn in PB:
    b = [r for r in band if plo <= r["pos"] <= phi]
    if b: print(f"  pos {pn}: rate={vr(b):.3f} n={len(b)}")

print("\n== vc portrait (mature >=48h) ==")
for stt in ("verified", "falsified", "revealed", "abandoned"):
    b = [r for r in ext if r["status"] == stt and r["age_h"] >= 48]
    if b:
        print(f"  {stt}: n={len(b)} vc median={st.median([r['vc'] for r in b])} share vc=0={sum(1 for r in b if r['vc']==0)/len(b):.3f} share vc>=2={sum(1 for r in b if r['vc']>=2)/len(b):.3f}")

print("\n== me=True among verified / awarded overlap ==")
ver = [r for r in ext if r["status"] == "verified"]
print(f"  verified total={len(ver)}, me=True among them={sum(1 for r in ver if r['me'])}")

print("\n== pilot ISR 2777178d full portrait ==")
rows = [r for r in recs if r["qid"].startswith("2777178d")]
print("  status x vc>=1:", dict(collections.Counter((r["status"], r["vc"] >= 1) for r in rows)))
print("  pos of vc>=1:", sorted(r["pos"] for r in rows if r["vc"] >= 1)[:20])

# refined diff: run-11 -> now, split other-group by run-11 ISR creation age
r11_iso = json.load(open(f"{RUN11}/isos_by_isr.json"))
r11_det = json.load(open(f"{RUN11}/details_by_isr.json"))
RUN11_PULL_END = int(datetime(2026, 11, 17, 1, 21, tzinfo=timezone.utc).timestamp() * 1000)
print("\n== DIFF run11->now refined ==")
groups = collections.defaultdict(lambda: [0, 0])
for qid, lst in r11_iso.items():
    if qid not in iso_by or not isinstance(lst, list):
        continue
    now_by_id = {i["id"]: i for i in iso_by[qid]}
    det11 = r11_det.get(qid) or {}
    st11 = det11.get("status")
    q_age_11 = (RUN11_PULL_END - (det11.get("timestamp") or RUN11_PULL_END)) / 3600000.0
    if st11 == "settled":
        g = "settled@11"
    elif q_age_11 >= 48:
        g = "notsettled@11, ISR age>=48h@11"
    else:
        g = "notsettled@11, ISR young@11"
    for i in lst:
        if i.get("status") == "revealed" and not i.get("isOwnAgent"):
            groups[g][1] += 1
            cur = now_by_id.get(i["id"])
            if cur and cur.get("status") in VERD:
                groups[g][0] += 1
for g, (chg, tot) in sorted(groups.items()):
    print(f"  {g}: {chg}/{tot} revealed->verdicted ({chg/tot:.3f})" if tot else f"  {g}: 0/0")
