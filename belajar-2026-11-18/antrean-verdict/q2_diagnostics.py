#!/usr/bin/env python3
"""Diagnostics for UJI-PEMBEDA-Q2-2026-11-18 (companion to q2_discriminator.py):
(1) confounder checks for M2 — ISR size, novelty x N>=41, position/author
    concentration behind the novelty & length gradients;
(2) pooled lag figures for M1 — flood-era panel-channel early vs late entrants,
    marathon pool, and marathonEligible share of flood verdicts.
Reads only the existing pull artifacts. No API calls."""
import json, re, statistics as st, collections
from datetime import datetime, timezone

OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-18/antrean-verdict"
iso_by = json.load(open(f"{OUT}/isos_by_isr.json"))
det_by = json.load(open(f"{OUT}/details_by_isr.json"))
NOW = json.load(open(f"{OUT}/pull_meta.json"))["now_ms"]
NOV14 = int(datetime(2026, 11, 14, tzinfo=timezone.utc).timestamp() * 1000)
STOP = set("""the a an and or of to in is are was were be been being for on with as by at from
this that it its not no yes if then than so such can could should would may might must
we you they he she i our your their his her them us him one two also more most other others
which who whom what when where why how all any each per via into about between through during
before after above below under over out up down off again further once here there""".split())
TOK = re.compile(r"[a-z0-9]{3,}")

def txt(i):
    sd = ((i.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    t = sd.get("answer") if isinstance(sd, dict) else None
    return t if isinstance(t, str) else None

def upd(i):
    u = i.get("updatedAt")
    if not u:
        return None
    try:
        return int(datetime.fromisoformat(u.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:
        return None

recs = []
for qid, lst in iso_by.items():
    det = det_by.get(qid) or {}
    q_ts = det.get("timestamp") or 0
    if q_ts < NOV14:
        continue
    rows = sorted(lst, key=lambda i: i.get("timestamp") or 0)
    seen = set()
    for idx, i in enumerate(rows):
        ts = i.get("timestamp") or 0
        t = txt(i)
        w = set(TOK.findall(t.lower())) - STOP if t else set()
        nov = (len(w - seen) / len(w)) if w else None
        seen |= w
        um = upd(i)
        recs.append({"qid": qid, "author": i.get("author"), "pos": idx + 1, "N": len(rows),
                     "delay_h": (ts - q_ts) / 3600000.0, "status": i.get("status"),
                     "vc": i.get("verifierCount") or 0, "own": bool(i.get("isOwnAgent")),
                     "age_h": (NOW - ts) / 3600000.0, "len": len(t) if t else None,
                     "nov": nov, "me": bool(i.get("marathonEligible")),
                     "lag_h": ((um - ts) / 3600000.0) if (um and i.get("status") in ("verified", "falsified")) else None})

def sh(rows):
    if not rows:
        return "n=0"
    return (f"n={len(rows):4d} vc>=2={sum(1 for r in rows if r['vc'] >= 2) / len(rows):.3f} "
            f"vc0={sum(1 for r in rows if r['vc'] == 0) / len(rows):.3f}")

base = [r for r in recs if not r["own"] and r["age_h"] >= 24 and r["len"] is not None
        and r["delay_h"] <= 2 and r["status"] == "revealed"]
print("populasi revealed banjir delay<=2j:", len(base))
print("\n-- menurut ukuran ISR (N):")
for lo, hi, name in [(1, 15, "N<=15"), (16, 40, "N16-40"), (41, 80, "N41-80"), (81, 10**9, "N81+")]:
    print(f"  {name:8s}: {sh([r for r in base if lo <= r['N'] <= hi])}")
big = [r for r in base if r["N"] >= 41]
print("\n-- novelty x N>=41:")
for lo, hi, name in [(0, 0.3, "nov<0.3"), (0.3, 0.5, "0.3-0.5"), (0.5, 1.01, "nov>=0.5")]:
    print(f"  {name:9s}: {sh([r for r in big if r['nov'] is not None and lo <= r['nov'] < hi])}")
print("\n-- panjang x N>=41:")
lens = sorted(r["len"] for r in big)
if lens:
    c = [lens[int(p * (len(lens) - 1))] for p in (0.25, 0.5, 0.75)]
    print("   batas kuartil:", c)
    for qi, (lo, hi) in enumerate([(0, c[0]), (c[0], c[1]), (c[1], c[2]), (c[2], 10**9)]):
        b = [r for r in big if lo <= r["len"] < hi] if qi < 3 else [r for r in big if r["len"] >= lo]
        print(f"  Q{qi + 1}: {sh(b)}")
print("\n-- posisi/N/delay median per ember novelty:")
for lo, hi, name in [(0, 0.3, "nov<0.3"), (0.3, 0.5, "0.3-0.5"), (0.5, 0.7, "0.5-0.7"), (0.7, 1.01, "nov>=0.7")]:
    b = [r for r in base if r["nov"] is not None and lo <= r["nov"] < hi]
    if b:
        print(f"  {name:9s}: n={len(b):4d} pos median={st.median([r['pos'] for r in b]):.0f} "
              f"N median={st.median([r['N'] for r in b]):.0f} delay median={st.median([r['delay_h'] for r in b]) * 60:.1f} mnt")
print("\n-- konsentrasi author:")
cnt = collections.Counter(r["author"] for r in base)
top = [a for a, _ in cnt.most_common(10)]
print("   author unik:", len(cnt), "| top10 mencakup:", sum(cnt[a] for a in top), "dari", len(base))
print("   top10    :", sh([r for r in base if r["author"] in top]))
print("   non-top10:", sh([r for r in base if r["author"] not in top]))

print("\n-- lag pooled era banjir (verdicted, 0<=lag<=60 hari):")
pools = {"panel_awal (me=F, delay<2j)": [], "panel_telat (me=F, delay>=6j)": [],
         "marathon (me=T)": [], "semua": []}
for r in recs:
    if r["own"] or r["lag_h"] is None or not (0 <= r["lag_h"] <= 24 * 60):
        continue
    pools["semua"].append(r["lag_h"])
    if r["me"]:
        pools["marathon (me=T)"].append(r["lag_h"])
    elif r["delay_h"] < 2:
        pools["panel_awal (me=F, delay<2j)"].append(r["lag_h"])
    elif r["delay_h"] >= 6:
        pools["panel_telat (me=F, delay>=6j)"].append(r["lag_h"])
for k, v in pools.items():
    if v:
        print(f"  {k:32s} n={len(v):4d} median={st.median(v):.3f}j <1j={sum(1 for x in v if x < 1) / len(v):.3f} "
              f"2-6j={sum(1 for x in v if 2 <= x < 6) / len(v):.3f} >=6j={sum(1 for x in v if x >= 6) / len(v):.3f}")
tot = sum(1 for r in recs if not r["own"] and r["status"] in ("verified", "falsified"))
me = sum(1 for r in recs if not r["own"] and r["status"] in ("verified", "falsified") and r["me"])
ver = sum(1 for r in recs if not r["own"] and r["status"] == "verified")
mev = sum(1 for r in recs if not r["own"] and r["status"] == "verified" and r["me"])
print(f"\nverdict banjir: total={tot}, me=True={me} ({me / tot:.1%}); verified={ver}, me=True={mev} ({mev / ver:.1%})")
