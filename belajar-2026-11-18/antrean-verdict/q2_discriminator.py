#!/usr/bin/env python3
"""UJI-PEMBEDA-Q2-2026-11-18: discriminating measurement for the Q2 dispute
(i) periodic marathon-channel selection timing vs (ii) early-flood quality
collapse / bot-noise filtering.

Reads ONLY the existing pull artifacts (isos_by_isr.json, details_by_isr.json,
pull_meta.json; pulled 2026-11-18 01:02-01:15 UTC). No new API calls.

M1: lag submit->verdict (updatedAt - timestamp) for verdicted answers,
    split by marathonEligible, flood era primary + older eras as control.
M2: panel assignment share (verifierCount>=2) among FLOOD-era EARLY answers
    (entry delay <=2h; sub-cut <=2min) by independent quality proxies
    (answer length quartile, URL/DOI citation presence, lexical novelty).
    Primary cut: revealed-only (assignment without verdict contamination).
"""
import json, re, statistics as st
from datetime import datetime, timezone

OUT = "/home/hatch/workspace/research/dialectica/belajar-2026-11-18/antrean-verdict"
iso_by = json.load(open(f"{OUT}/isos_by_isr.json"))
det_by = json.load(open(f"{OUT}/details_by_isr.json"))
NOW = json.load(open(f"{OUT}/pull_meta.json"))["now_ms"]

NOV1 = int(datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp() * 1000)
NOV14 = int(datetime(2026, 11, 14, tzinfo=timezone.utc).timestamp() * 1000)
VERD = ("verified", "falsified")

def upd_ms(i):
    u = i.get("updatedAt")
    if not u:
        return None
    try:
        return int(datetime.fromisoformat(u.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:
        return None

def answer_text(i):
    sd = ((i.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    t = sd.get("answer") if isinstance(sd, dict) else None
    return t if isinstance(t, str) else None

STOP = set("""the a an and or of to in is are was were be been being for on with as by at from
this that it its it's not no yes if then than so such can could should would may might must
we you they he she i our your their his her them us him one two also more most other others
which who whom what when where why how all any each per via into about between through during
before after above below under over out up down off again further once here there""".split())
TOK = re.compile(r"[a-z0-9]{3,}")
URLRE = re.compile(r"https?://|www\.|doi\.org|\bdoi:", re.I)

recs = []
for qid, lst in iso_by.items():
    if not isinstance(lst, list):
        continue
    det = det_by.get(qid) or {}
    q_ts = det.get("timestamp") or 0
    era = "banjir" if q_ts >= NOV14 else ("tengah" if q_ts >= NOV1 else "lama")
    rows = sorted(lst, key=lambda i: i.get("timestamp") or 0)
    seen_words = set()
    for idx, i in enumerate(rows):
        ts = i.get("timestamp") or 0
        um = upd_ms(i)
        txt = answer_text(i)
        words = set(TOK.findall(txt.lower())) - STOP if txt else set()
        novelty = (len(words - seen_words) / len(words)) if words else None
        seen_words |= words
        recs.append({
            "qid": qid, "id": i["id"], "era": era, "ts": ts, "pos": idx + 1,
            "delay_h": (ts - q_ts) / 3600000.0 if q_ts else None,
            "status": i.get("status"), "vc": i.get("verifierCount") or 0,
            "sup": i.get("supportedCount") or 0, "ref": i.get("refutationCount") or 0,
            "me": bool(i.get("marathonEligible")), "own": bool(i.get("isOwnAgent")),
            "age_h": (NOW - ts) / 3600000.0,
            "lag_h": ((um - ts) / 3600000.0) if (um and i.get("status") in VERD) else None,
            "len": len(txt) if txt else None,
            "cite": bool(URLRE.search(txt)) if txt else None,
            "novelty": novelty,
        })
ext = [r for r in recs if not r["own"]]
res = {}

def q(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    return s[min(len(s) - 1, int(p * len(s)))]

def lag_summary(rows):
    lags = [r["lag_h"] for r in rows if r["lag_h"] is not None and 0 <= r["lag_h"] <= 24 * 60]
    if not lags:
        return {"n": 0}
    return {"n": len(lags), "median_h": round(st.median(lags), 3),
            "p25_h": round(q(lags, 0.25), 3), "p75_h": round(q(lags, 0.75), 3),
            "p90_h": round(q(lags, 0.90), 3),
            "share_lt_1h": round(sum(1 for x in lags if x < 1) / len(lags), 3),
            "share_1_6h": round(sum(1 for x in lags if 1 <= x < 6) / len(lags), 3),
            "share_ge_6h": round(sum(1 for x in lags if x >= 6) / len(lags), 3)}

LAG_BUCKETS = [(0, 0.25, "<15mnt"), (0.25, 1, "15-60mnt"), (1, 2, "1-2j"),
               (2, 6, "2-6j"), (6, 24, "6-24j"), (24, 24 * 60, ">24j")]
def lag_hist(rows):
    lags = [r["lag_h"] for r in rows if r["lag_h"] is not None and 0 <= r["lag_h"] <= 24 * 60]
    out = {}
    for lo, hi, name in LAG_BUCKETS:
        c = sum(1 for x in lags if lo <= x < hi)
        out[name] = {"n": c, "share": round(c / len(lags), 3) if lags else None}
    return out

# ================= M1: lag by marathon membership =================
print("=" * 78)
print("M1 — LAG submit->verdict, split marathonEligible")
for era in ("banjir", "tengah", "lama"):
    for me in (True, False):
        rows = [r for r in ext if r["era"] == era and r["me"] == me and r["status"] in VERD]
        s = lag_summary(rows)
        nv = sum(1 for r in rows if r["status"] == "verified")
        print(f"  era={era:6s} me={me!s:5s}: verdicted={len(rows):4d} (V={nv}) lag={s}")
        res[f"m1_{era}_me{me}"] = {**s, "verdicted": len(rows), "verified": nv,
                                  "hist": lag_hist(rows)}
    rows = [r for r in ext if r["era"] == era and r["status"] in VERD]
    print(f"  era={era:6s} GABUNGAN: {lag_summary(rows)}  hist={lag_hist(rows)}")
    res[f"m1_{era}_all"] = {**lag_summary(rows), "hist": lag_hist(rows)}

# M1b: flood-era lag split ALSO by entry delay (does 'long lag' just mirror late entry?)
print("\nM1b — era banjir, lag menurut delay masuk (me=False saja, kanal panel):")
for lo, hi, name in [(0, 2/60, "<2mnt"), (2/60, 2, "2mnt-2j"), (2, 6, "2-6j"), (6, 24, "6-24j"), (24, 10**9, ">24j")]:
    rows = [r for r in ext if r["era"] == "banjir" and not r["me"] and r["status"] in VERD
            and r["delay_h"] is not None and lo <= r["delay_h"] < hi]
    print(f"  delay {name:8s}: verdicted={len(rows):4d} lag={lag_summary(rows)}")
    res[f"m1b_delay_{name}"] = lag_summary(rows)
print("M1b — era banjir, lag menurut delay masuk (me=True):")
for lo, hi, name in [(0, 2, "<2j"), (2, 6, "2-6j"), (6, 24, "6-24j"), (24, 10**9, ">24j")]:
    rows = [r for r in ext if r["era"] == "banjir" and r["me"] and r["status"] in VERD
            and r["delay_h"] is not None and lo <= r["delay_h"] < hi]
    print(f"  delay {name:8s}: verdicted={len(rows):4d} lag={lag_summary(rows)}")
    res[f"m1b_me_delay_{name}"] = lag_summary(rows)

# ================= M2: assignment by quality, flood-era early =================
def assign_share(rows):
    if not rows:
        return {"n": 0}
    return {"n": len(rows),
            "vc_ge2": round(sum(1 for r in rows if r["vc"] >= 2) / len(rows), 3),
            "vc_ge1": round(sum(1 for r in rows if r["vc"] >= 1) / len(rows), 3),
            "vc0": round(sum(1 for r in rows if r["vc"] == 0) / len(rows), 3)}

print("\n" + "=" * 78)
print("M2 — Penugasan panel (vc>=2) jawaban banjir AWAL menurut proksi mutu")
base = [r for r in ext if r["era"] == "banjir" and r["age_h"] >= 24
        and r["len"] is not None and r["delay_h"] is not None]
for dmax, dname in ((2/60, "delay<=2mnt"), (2, "delay<=2j")):
    early = [r for r in base if r["delay_h"] <= dmax]
    rev = [r for r in early if r["status"] == "revealed"]
    print(f"\n-- {dname}: n={len(early)} (revealed-only n={len(rev)})")
    print(f"   SEMUA status : {assign_share(early)}")
    print(f"   REVEALED saja: {assign_share(rev)}   <- uji utama (penugasan murni)")
    res[f"m2_{dname}_all"] = assign_share(early)
    res[f"m2_{dname}_revealed"] = assign_share(rev)
    # length quartiles (cut points from the revealed subset of this delay window)
    lens = sorted(r["len"] for r in rev)
    if len(lens) >= 40:
        cuts = [lens[int(p * (len(lens) - 1))] for p in (0.25, 0.5, 0.75)]
        print(f"   kuartil panjang (revealed): batas={cuts}")
        res[f"m2_{dname}_len_cuts"] = cuts
        for qi, (lo, hi) in enumerate([(0, cuts[0]), (cuts[0], cuts[1]), (cuts[1], cuts[2]), (cuts[2], 10**9)]):
            b = [r for r in rev if lo <= r["len"] < hi] if qi < 3 else [r for r in rev if r["len"] >= lo]
            print(f"     Q{qi+1} len [{lo}-{hi if hi<10**9 else 'inf'}): {assign_share(b)}")
            res[f"m2_{dname}_lenQ{qi+1}"] = assign_share(b)
    # citation
    for c in (True, False):
        b = [r for r in rev if r["cite"] == c]
        print(f"     sitasi URL/DOI={c}: {assign_share(b)}")
        res[f"m2_{dname}_cite_{c}"] = assign_share(b)
    # novelty buckets
    for lo, hi, name in [(0, 0.3, "<0.3"), (0.3, 0.5, "0.3-0.5"), (0.5, 0.7, "0.5-0.7"), (0.7, 1.01, ">=0.7")]:
        b = [r for r in rev if r["novelty"] is not None and lo <= r["novelty"] < hi]
        print(f"     novelty {name}: {assign_share(b)}")
        res[f"m2_{dname}_nov_{name}"] = assign_share(b)
    # combined: long AND cited AND novel vs short AND uncited AND unnovel
    hi_q = [r for r in rev if r["len"] >= (cuts[2] if len(lens) >= 40 else 10**9) and r["cite"] and (r["novelty"] or 0) >= 0.5]
    lo_q = [r for r in rev if r["len"] < (cuts[0] if len(lens) >= 40 else 0) and not r["cite"] and (r["novelty"] if r["novelty"] is not None else 1) < 0.5]
    print(f"     KOMBO mutu-tinggi (Q4+sita+nov>=0.5): {assign_share(hi_q)}")
    print(f"     KOMBO mutu-rendah (Q1+tanpa sita+nov<0.5): {assign_share(lo_q)}")
    res[f"m2_{dname}_combo_hi"] = assign_share(hi_q)
    res[f"m2_{dname}_combo_lo"] = assign_share(lo_q)

# background: assignment by delay (all quality) flood era, revealed-only
print("\n-- latar: pangsa vc>=2 (revealed-only, banjir, umur>=24j) menurut delay:")
for lo, hi, name in [(0, 2/60, "<2mnt"), (2/60, 2, "2mnt-2j"), (2, 6, "2-6j"), (6, 24, "6-24j"), (24, 10**9, ">24j")]:
    b = [r for r in base if r["status"] == "revealed" and lo <= r["delay_h"] < hi]
    print(f"   delay {name:8s}: {assign_share(b)}")
    res[f"m2_bg_delay_{name}"] = assign_share(b)

# control: older eras, early answers, revealed-only, by length quartile + citation
print("\n-- kontrol era lama+tengah (delay<=2j, revealed-only, umur>=24j):")
ctrl = [r for r in ext if r["era"] in ("lama", "tengah") and r["age_h"] >= 24
        and r["len"] is not None and r["delay_h"] is not None and r["delay_h"] <= 2
        and r["status"] == "revealed"]
print(f"   n={len(ctrl)} semua: {assign_share(ctrl)}")
res["m2_ctrl_all"] = assign_share(ctrl)
if len(ctrl) >= 40:
    lens = sorted(r["len"] for r in ctrl)
    cuts = [lens[int(p * (len(lens) - 1))] for p in (0.25, 0.5, 0.75)]
    for qi, (lo, hi) in enumerate([(0, cuts[0]), (cuts[0], cuts[1]), (cuts[1], cuts[2]), (cuts[2], 10**9)]):
        b = [r for r in ctrl if lo <= r["len"] < hi] if qi < 3 else [r for r in ctrl if r["len"] >= lo]
        print(f"     Q{qi+1} len: {assign_share(b)}")
        res[f"m2_ctrl_lenQ{qi+1}"] = assign_share(b)
    for c in (True, False):
        b = [r for r in ctrl if r["cite"] == c]
        print(f"     sitasi={c}: {assign_share(b)}")
        res[f"m2_ctrl_cite_{c}"] = assign_share(b)

with open(f"{OUT}/q2_discriminator.json", "w") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print("\nwrote q2_discriminator.json")
