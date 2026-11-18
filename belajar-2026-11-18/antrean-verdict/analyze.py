#!/usr/bin/env python3
"""Analysis for STUDI-ANTREAN-VERDICT-2026-11-18. Reads pull output (+ run-11
snapshot for the 1-day diff and a larger winner sample). Prints tables and
writes analysis.json."""
import json, os, statistics as st
from datetime import datetime, timezone

ROOT = "/home/hatch/workspace/research/dialectica"
OUT = f"{ROOT}/belajar-2026-11-18/antrean-verdict"
RUN11 = f"{ROOT}/belajar-2026-11-17/run11-0717"

def load(d, n, default=None):
    p = f"{d}/{n}"
    return json.load(open(p)) if os.path.exists(p) else default

meta = load(OUT, "pull_meta.json")
NOW = meta["now_ms"]
det_by = load(OUT, "details_by_isr.json", {})
iso_by = load(OUT, "isos_by_isr.json", {})
tags = load(OUT, "sample_tags.json", {})

def upd_ms(i):
    u = i.get("updatedAt")
    if not u:
        return None
    try:
        return int(datetime.fromisoformat(u.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:
        return None

def build(det_by, iso_by, now_ms, tags=None):
    recs = []
    isr_meta = {}
    for qid, lst in iso_by.items():
        if not isinstance(lst, list):
            continue
        det = det_by.get(qid) or {}
        awarded = {e.get("isoId") for e in (det.get("marathonEligibleIsos") or []) if e.get("awarded")}
        rows = sorted(lst, key=lambda i: i.get("timestamp") or 0)
        n = len(rows)
        ver = [i for i in rows if i.get("status") == "verified"]
        pioneer_id = ver[0]["id"] if ver else None
        isr_meta[qid] = {"status": det.get("status"), "q_ts": det.get("timestamp"),
                         "marathonActive": det.get("marathonActive"),
                         "marathonConcluded": det.get("marathonConcluded"),
                         "isoCount_detail": det.get("isoCount"), "n_pulled": n,
                         "tag": (tags or {}).get(qid, "")}
        for idx, i in enumerate(rows):
            ts = i.get("timestamp") or 0
            um = upd_ms(i)
            recs.append({
                "qid": qid, "id": i["id"], "ts": ts, "pos": idx + 1, "N": n,
                "depth": n - (idx + 1), "status": i.get("status"),
                "sup": i.get("supportedCount") or 0, "ref": i.get("refutationCount") or 0,
                "vc": i.get("verifierCount") or 0, "me": bool(i.get("marathonEligible")),
                "own": bool(i.get("isOwnAgent")), "author": i.get("author"),
                "age_h": (now_ms - ts) / 3600000.0,
                "lag_h": ((um - ts) / 3600000.0) if (um and i.get("status") in ("verified", "falsified")) else None,
                "pioneer": i["id"] == pioneer_id, "awarded": i["id"] in awarded,
                "q_status": det.get("status"),
            })
    return recs, isr_meta

recs, isr_meta = build(det_by, iso_by, NOW, tags)
ext = [r for r in recs if not r["own"]]
VERD = ("verified", "falsified")

def rate(rows):
    if not rows:
        return None
    return sum(1 for r in rows if r["status"] in VERD) / len(rows)

def bucket_table(rows, keyfn, buckets, label):
    out = []
    for lo, hi, name in buckets:
        b = [r for r in rows if lo <= keyfn(r) <= hi]
        if not b:
            continue
        v = sum(1 for r in b if r["status"] == "verified")
        f = sum(1 for r in b if r["status"] == "falsified")
        out.append({"bucket": name, "n": len(b), "verdict_rate": round(rate(b), 4),
                    "verified": v, "falsified": f,
                    "revealed": sum(1 for r in b if r["status"] == "revealed"),
                    "abandoned": sum(1 for r in b if r["status"] == "abandoned")})
    print(f"\n== {label} ==")
    for o in out:
        print(f"  {o['bucket']:>8}: n={o['n']:>5} verdict={o['verdict_rate']:.3f} "
              f"(V={o['verified']} F={o['falsified']} rev={o['revealed']} ab={o['abandoned']})")
    return out

res = {}
print(f"ISRs={len(isr_meta)} ISOs={len(recs)} external={len(ext)} own={len(recs)-len(ext)}")
import collections
print("status counts (ext):", dict(collections.Counter(r["status"] for r in ext)))
print("ISR status:", dict(collections.Counter(m["status"] for m in isr_meta.values())))
trunc = {q: (m["isoCount_detail"], m["n_pulled"]) for q, m in isr_meta.items()
         if m["isoCount_detail"] and m["isoCount_detail"] > m["n_pulled"]}
print(f"truncated ISO lists: {len(trunc)} ISRs (detail isoCount > pulled)")

# ---------- Q1: verdict rate vs depth / position (mature) ----------
DB = [(0, 0, "0"), (1, 2, "1-2"), (3, 5, "3-5"), (6, 10, "6-10"), (11, 20, "11-20"),
      (21, 40, "21-40"), (41, 80, "41-80"), (81, 10**9, "81+")]
PB = [(1, 1, "1"), (2, 3, "2-3"), (4, 5, "4-5"), (6, 10, "6-10"), (11, 20, "11-20"),
      (21, 50, "21-50"), (51, 10**9, "51+")]
for minage in (48, 72):
    mat = [r for r in ext if r["age_h"] >= minage]
    res[f"q1_depth_age{minage}"] = bucket_table(mat, lambda r: r["depth"], DB, f"Q1 verdict rate by DEPTH, age>={minage}h, n={len(mat)}")
    res[f"q1_pos_age{minage}"] = bucket_table(mat, lambda r: r["pos"], PB, f"Q1 verdict rate by POSITION, age>={minage}h")
# large ISRs only (depth signal without small-ISR dilution)
big = [r for r in ext if r["age_h"] >= 48 and r["N"] >= 40]
res["q1_depth_big"] = bucket_table(big, lambda r: r["depth"], DB, f"Q1 DEPTH, ISRs N>=40 only, n={len(big)}")
# mean depth verdicted vs not (mature, N>=10)
matN = [r for r in ext if r["age_h"] >= 48 and r["N"] >= 10]
dv = [r["depth"] for r in matN if r["status"] in VERD]
dn = [r["depth"] for r in matN if r["status"] not in VERD]
print(f"\nmean depth verdicted={st.mean(dv):.1f} (median {st.median(dv)}) vs non-verdicted={st.mean(dn):.1f} (median {st.median(dn)}), n_v={len(dv)} n_n={len(dn)}")
res["q1_meandepth"] = {"verdicted_mean": round(st.mean(dv), 1), "verdicted_median": st.median(dv),
                       "non_mean": round(st.mean(dn), 1), "non_median": st.median(dn),
                       "n_v": len(dv), "n_n": len(dn)}

# ---------- Q2: lag ----------
lagrows = [r for r in ext if r["lag_h"] is not None and 0 <= r["lag_h"] <= 24 * 60]
print(f"\nlag rows (verdicted, sane): {len(lagrows)}; median lag overall={st.median([r['lag_h'] for r in lagrows]):.2f}h")
res["q2_lag_depth"] = bucket_table(lagrows, lambda r: r["depth"],
    [(0, 0, "0"), (1, 5, "1-5"), (6, 20, "6-20"), (21, 50, "21-50"), (51, 10**9, "51+")],
    "Q2 (buckets show counts only; medians below)")
for lo, hi, name in [(0, 0, "0"), (1, 5, "1-5"), (6, 20, "6-20"), (21, 50, "21-50"), (51, 10**9, "51+")]:
    b = [r["lag_h"] for r in lagrows if lo <= r["depth"] <= hi]
    if b:
        print(f"  lag by depth {name}: median={st.median(b):.2f}h n={len(b)}")
for lo, hi, name in [(1, 15, "N<=15"), (16, 40, "N16-40"), (41, 80, "N41-80"), (81, 10**9, "N81+")]:
    b = [r["lag_h"] for r in lagrows if lo <= r["N"] <= hi]
    if b:
        print(f"  lag by crowd {name}: median={st.median(b):.2f}h n={len(b)}")

# ---------- Q3a: settled vs in_progress cross-section ----------
for lo, hi, name in [(48, 96, "48-96h"), (96, 10**9, ">96h")]:
    for qs in ("settled", "in_progress"):
        b = [r for r in ext if r["q_status"] == qs and lo <= r["age_h"] <= hi]
        if b:
            print(f"Q3 age {name} ISR={qs}: n={len(b)} verdict_rate={rate(b):.3f}")
            res[f"q3_{name}_{qs}"] = {"n": len(b), "verdict_rate": round(rate(b), 4)}

# ---------- Q3b: run-11 -> now diff ----------
r11_iso = load(RUN11, "isos_by_isr.json", {})
r11_det = load(RUN11, "details_by_isr.json", {})
r11_meta_time = load(RUN11, "pull_meta.json", {})
diff = {"settled_then": [0, 0], "other_then": [0, 0]}  # [changed_to_verdict, revealed_then_total]
diff_detail = []
for qid, lst in r11_iso.items():
    if qid not in iso_by or not isinstance(lst, list):
        continue
    now_by_id = {i["id"]: i for i in iso_by[qid]}
    then_status = (r11_det.get(qid) or {}).get("status")
    key = "settled_then" if then_status == "settled" else "other_then"
    for i in lst:
        if i.get("status") == "revealed" and not i.get("isOwnAgent"):
            diff[key][1] += 1
            cur = now_by_id.get(i["id"])
            if cur and cur.get("status") in VERD:
                diff[key][0] += 1
                diff_detail.append({"qid": qid[:8], "iso": i["id"][:8], "to": cur["status"], "then_isr": then_status})
print(f"\nQ3 diff run11->now (~30h): settled-then ISRs: {diff['settled_then'][0]}/{diff['settled_then'][1]} revealed->verdicted; "
      f"other: {diff['other_then'][0]}/{diff['other_then'][1]}")
res["q3_diff"] = {"settled_then": diff["settled_then"], "other_then": diff["other_then"], "detail": diff_detail[:40]}

# ---------- Q4: winners (fresh sample + run-11 big sample) ----------
def winner_stats(recs_, label):
    pio = [r for r in recs_ if r["pioneer"]]
    awd = [r for r in recs_ if r["awarded"]]
    def summ(rows):
        if not rows:
            return {}
        return {"n": len(rows),
                "pos_median": st.median([r["pos"] for r in rows]),
                "pos_p90": sorted([r["pos"] for r in rows])[int(0.9 * (len(rows) - 1))],
                "depth_median": st.median([r["depth"] for r in rows]),
                "N_median": st.median([r["N"] for r in rows]),
                "N_p90": sorted([r["N"] for r in rows])[int(0.9 * (len(rows) - 1))],
                "share_pos<=5": round(sum(1 for r in rows if r["pos"] <= 5) / len(rows), 3),
                "share_pos<=10": round(sum(1 for r in rows if r["pos"] <= 10) / len(rows), 3),
                "share_N<=25 among pos<=10": round(sum(1 for r in rows if r["pos"] <= 10 and r["N"] <= 25) / max(1, sum(1 for r in rows if r["pos"] <= 10)), 3)}
    print(f"\nQ4 {label}: pioneer={summ(pio)}")
    print(f"Q4 {label}: awarded={summ(awd)}")
    return {"pioneer": summ(pio), "awarded": summ(awd)}

res["q4_fresh"] = winner_stats([r for r in ext], "fresh sample")
NOW11 = int(datetime(2026, 11, 17, 1, 21, tzinfo=timezone.utc).timestamp() * 1000)
recs11, _ = build(r11_det, r11_iso, NOW11)
res["q4_run11"] = winner_stats([r for r in recs11 if not r["own"]], "run-11 sample")

# ---------- Q5: marathonEligible + deciles ----------
mat = [r for r in ext if r["age_h"] >= 48]
for me in (True, False):
    b = [r for r in mat if r["me"] == me]
    if b:
        print(f"Q5 marathonEligible={me}: n={len(b)} verdict_rate={rate(b):.3f}")
        res[f"q5_me_{me}"] = {"n": len(b), "verdict_rate": round(rate(b), 4)}
ds = sorted(r["depth"] for r in mat)
if ds:
    cuts = [ds[int(q * (len(ds) - 1))] for q in (0.25, 0.5, 0.75)]
    print("Q5 depth quartiles (mature):", cuts)

# ---------- pilot + ours ----------
print("\n== OUR ISOs (fresh pull) ==")
for r in recs:
    if r["own"]:
        print(f"  {r['qid'][:8]} iso={r['id'][:8]} pos={r['pos']} depth={r['depth']} N={r['N']} status={r['status']} sup={r['sup']} ref={r['ref']} vc={r['vc']} tag={isr_meta[r['qid']]['tag']}")
print("\n== verdicted in pilot ISRs ==")
for r in ext:
    if isr_meta[r["qid"]]["tag"].startswith("pilot") and r["status"] in VERD:
        print(f"  {r['qid'][:8]} iso={r['id'][:8]} pos={r['pos']} depth={r['depth']} status={r['status']} lag_h={r['lag_h']}")

with open(f"{OUT}/analysis.json", "w") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print("\nwrote analysis.json")
