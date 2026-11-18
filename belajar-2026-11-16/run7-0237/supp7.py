#!/usr/bin/env python3
"""Supplementary analysis for BELAJAR-LOG run 7 (2026-11-16 02:37 WIB).
Fresh-only pioneer latency, climbers run6->run7, korpus refresh 2B,
per-agent climber styles, fresh topic classification + 7-day table row,
attribution residuals. Read-only; uses run7 + run6 artefacts."""
import json, re, statistics as st, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/home/hatch/workspace/research/dialectica/provider")
from openrouter_wrapper import citation_spans, NUM_RE, BOUND_WINDOW  # noqa: E402

D6 = "/home/hatch/workspace/research/dialectica/belajar-2026-11-16/run7-0237"
D5 = "/home/hatch/workspace/research/dialectica/belajar-2026-11-15/run6-1837"
WIB = timezone(timedelta(hours=7))
CUT = int(datetime(2026, 11, 15, 11, 37, tzinfo=timezone.utc).timestamp() * 1000)  # 2026-11-15 18:37 WIB = 11:37 UTC

def load(b, n):
    with open(f"{b}/{n}") as fh: return json.load(fh)

lb6, lb5 = load(D6, "leaderboard.json"), load(D5, "leaderboard.json")
isrs = load(D6, "isrs.json")["isrs"]
isos_by, det_by, tags = load(D6, "isos_by_isr.json"), load(D6, "details_by_isr.json"), load(D6, "sample_tags.json")
a6 = load(D6, "analysis7.json")
out = {}

# --- climbers run6 -> run7 ---
by5 = {r["userId"]: r for r in lb5}
house5 = {r["userId"] for r in lb5 if (r.get("userName") or "").startswith("Dialectica")}
climbers, new_top100 = [], []
for r in lb6:
    if (r.get("userName") or "").startswith("Dialectica"):
        continue
    old = by5.get(r["userId"])
    if old is None:
        new_top100.append({"name": r["userName"], "coins": round(r["coins"], 1),
                           "wins": r.get("marathonWinsCount"), "rank": r.get("rank"), "note": "NEW top100"})
    else:
        dc = round(r["coins"] - old["coins"], 1)
        dw = (r.get("marathonWinsCount") or 0) - (old.get("marathonWinsCount") or 0)
        if dc >= 300:
            climbers.append({"name": r["userName"], "dcoins": dc, "dwins": dw,
                             "rank_old": old.get("rank"), "rank_new": r.get("rank"),
                             "coins": round(r["coins"], 1), "wins": r.get("marathonWinsCount")})
climbers.sort(key=lambda x: -x["dcoins"])
out["climbers"] = {"n_ge300": len(climbers), "new_top100": new_top100,
                   "top": climbers[:20], "floor_top100": min(r["coins"] for r in lb6 if not (r.get("userName") or "").startswith("Dialectica")),
                   "agents_ge400": sum(1 for r in lb6 if not (r.get("userName") or "").startswith("Dialectica") and r["coins"] >= 400)}
# flat agents era §30 still in top100 (names from run5 J9 list)
FLAT30 = ["DodolDuren", "Nawaz", "T04435", "Aaron Nev McLachlan", "Renato Oviedo", "Alison Haire",
          "Jeremy Cabral", "jan dev", "Tom", "Alpheon", "Makoto Nakae", "rizz", "Searchie", "CΞAZOR.eth", "GG", "Test"]
flat_now = []
for r in lb6:
    if r["userName"] in FLAT30:
        old = by5.get(r["userId"])
        flat_now.append({"name": r["userName"], "dcoins": round(r["coins"] - old["coins"], 1) if old else None,
                         "dwins": (r.get("marathonWinsCount") or 0) - (old.get("marathonWinsCount") or 0) if old else None})
out["flat30_now"] = flat_now

# --- attribution residual for top climbers ---
out["attribution"] = []
for c in climbers[:10]:
    resid = c["dcoins"] - 10 * c["dwins"]
    out["attribution"].append({"name": c["name"], "dcoins": c["dcoins"], "dwins": c["dwins"],
                               "residual": resid, "resid_share": round(resid / c["dcoins"], 3) if c["dcoins"] else None})

# --- fresh-only pioneer latency ---
names = {r["userId"]: r.get("userName") or "" for r in lb6}
house_ids = {r["userId"] for r in lb6 if (r.get("userName") or "").startswith("Dialectica")}
fresh_ids = {r["id"] for r in isrs if (r.get("timestamp") or 0) >= CUT}
lat_f_ext, lat_f_house = [], []
lat_all_ext = []
for qid, lst in isos_by.items():
    if not isinstance(lst, list):
        continue
    ver = sorted([i for i in lst if i.get("status") == "verified"], key=lambda i: i.get("timestamp") or 0)
    qq = next((r for r in isrs if r["id"] == qid), {})
    if not ver or not qq.get("timestamp") or not ver[0].get("timestamp"):
        continue
    lat = (ver[0]["timestamp"] - qq["timestamp"]) / 1000.0
    grp = "house" if ver[0]["author"] in house_ids else "external"
    if grp == "external":
        lat_all_ext.append(lat)
        if qid in fresh_ids:
            lat_f_ext.append(lat)
    elif qid in fresh_ids:
        lat_f_house.append(lat)
def med(xs): return round(st.median(xs), 1) if xs else None
def buckets(xs):
    return {"sub10s": sum(1 for x in xs if x < 10), "sub60s": sum(1 for x in xs if 10 <= x < 60),
            "1-10m": sum(1 for x in xs if 60 <= x < 600), "10-30m": sum(1 for x in xs if 600 <= x < 1800),
            "30-60m": sum(1 for x in xs if 1800 <= x < 3600), "gt60m": sum(1 for x in xs if x >= 3600)}
out["pioneer_latency"] = {"fresh_only_external": {"n": len(lat_f_ext), "median_s": med(lat_f_ext),
                                                   "min_s": round(min(lat_f_ext), 1) if lat_f_ext else None,
                                                   "buckets": buckets(lat_f_ext)},
                          "fresh_only_house": {"n": len(lat_f_house), "median_s": med(lat_f_house)},
                          "all_sample_external_median_s": med(lat_all_ext)}

# --- korpus refresh 2B: floor pass at 0.30 and 0.15, full + in-K1 ---
def metrics(txt):
    cites = citation_spans(txt)
    url_count = sum(1 for _, _, u in cites if u)
    density = len(cites) / (len(txt) / 1000.0) if txt else 0.0
    total = bound = 0
    for m in NUM_RE.finditer(txt):
        s, e = m.start(), m.end()
        if any(s < ce and cs < e for cs, ce, _ in cites):
            continue
        total += 1
        if any(max(cs - e, s - ce) <= BOUND_WINDOW for cs, ce, _ in cites):
            bound += 1
    ratio = bound / total if total else 0.0
    return url_count, density, ratio

def answer_text(iso):
    sd = ((iso.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    return sd.get("answer")

OUR_ISO = {"fcb7b015", "097df475", "0d76cc7c", "f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"}
panels = {"v": [], "f": []}
for qid, lst in isos_by.items():
    if not isinstance(lst, list):
        continue
    for iso in lst:
        if iso.get("status") not in ("verified", "falsified"):
            continue
        if iso["author"] in house_ids or any(iso["id"].startswith(p) for p in OUR_ISO):
            continue
        txt = answer_text(iso)
        if not txt:
            continue
        panels["v" if iso["status"] == "verified" else "f"].append(metrics(txt))
def floor_pass(rows, thr):
    if not rows:
        return None
    ok = sum(1 for u, d, r in rows if u >= 1 and d >= 0.5 and r >= thr)
    return round(100 * ok / len(rows), 1)
def in_k1(rows, thr):
    sub = [(u, d, r) for u, d, r in rows if u >= 1 and d >= 0.5]
    if not sub:
        return None
    ok = sum(1 for u, d, r in sub if r >= thr)
    return round(100 * ok / len(sub), 1)
ref = {"full_030": (32.5, 28.1), "full_015": (57.6, 32.8)}
kr = {"n": {"v": len(panels["v"]), "f": len(panels["f"])},
      "full_030": {"v": floor_pass(panels["v"], 0.30), "f": floor_pass(panels["f"], 0.30)},
      "full_015": {"v": floor_pass(panels["v"], 0.15), "f": floor_pass(panels["f"], 0.15)},
      "in_k1_030": {"v": in_k1(panels["v"], 0.30), "f": in_k1(panels["f"], 0.30)},
      "in_k1_015": {"v": in_k1(panels["v"], 0.15), "f": in_k1(panels["f"], 0.15)},
      "k1_only_gap_pp": None}
for k in ("full_030", "full_015", "in_k1_030", "in_k1_015"):
    kr[k]["gap_pp"] = round(kr[k]["v"] - kr[k]["f"], 1)
# K-1 alone gap
def k1_pass(rows):
    if not rows: return None
    return round(100 * sum(1 for u, d, r in rows if u >= 1 and d >= 0.5) / len(rows), 1)
kr["k1_only"] = {"v": k1_pass(panels["v"]), "f": k1_pass(panels["f"])}
kr["k1_only_gap_pp"] = round(kr["k1_only"]["v"] - kr["k1_only"]["f"], 1)
kr["ref"] = ref
kr["gap_vs_ref_pp"] = {"full_030": round(kr["full_030"]["gap_pp"] - (32.5 - 28.1), 1),
                       "full_015": round(kr["full_015"]["gap_pp"] - (57.6 - 32.8), 1)}
out["korpus_refresh"] = kr

# --- per-agent climber styles (verified answers in sample) ---
WATCH = ["Danis", "chirpy", "can-earn?", "Gufran The Legend", "zoya khan", "Febriyan", "Mauldrop",
         "Adam Reinhard", "Discord 1", "Md ripon Rana", "Rodeo", "GaBot", "neobros f", "Iqoo First",
         "coucung", "SyntaxZ", "DegenXBT", "megumii", "Hermawan Kwan", "HIMANSHU", "FlashX Bliz"]
by_name = defaultdict(list)
for qid, lst in isos_by.items():
    if not isinstance(lst, list):
        continue
    for iso in lst:
        if iso.get("status") == "verified" and answer_text(iso):
            by_name[names.get(iso["author"], "")].append(iso)
styles = {}
for nm in WATCH:
    rows = by_name.get(nm, [])
    if not rows:
        continue
    ms = [metrics(answer_text(r)) for r in rows]
    styles[nm] = {"n_verified": len(rows),
                  "chars_median": round(st.median([len(answer_text(r)) for r in rows])) if rows else None,
                  "density_median": round(st.median([m[1] for m in ms]), 3),
                  "ratio_median": round(st.median([m[2] for m in ms]), 3),
                  "floor030_pass_pct": round(100 * sum(1 for u, d, r in ms if u >= 1 and d >= 0.5 and r >= 0.30) / len(ms), 1),
                  "floor015_pass_pct": round(100 * sum(1 for u, d, r in ms if u >= 1 and d >= 0.5 and r >= 0.15) / len(ms), 1)}
out["climber_styles"] = styles

# --- fresh topic classification (KULIT §7 core topics) ---
CORE_KEYS = ["agent id", "agent identity", "wallet", "on-chain", "oracle", "rollup", "smart contract",
             "contract security", "token", "bridge", "mint", "eip-", "erc-", "consensus", "validator",
             "dialectica", "expert", "verifier", "pioneer", "marathon"]
def is_viking(q):
    t = ((q.get("content") or "") + " " + " ".join(q.get("domainTags") or [])).lower()
    return "viking" in t or "mars" in t
def is_core(q):
    t = ((q.get("content") or "") + " " + " ".join(q.get("domainTags") or [])).lower()
    return any(k in t for k in CORE_KEYS)
fresh_rows = [r for r in isrs if (r.get("timestamp") or 0) >= CUT]
hour_core = {}
for r in fresh_rows:
    h = datetime.fromtimestamp(r["timestamp"] / 1000, WIB).hour
    hour_core.setdefault(h, {"releases": 0, "viking": 0, "core_kw": 0, "core_new": []})
    hour_core[h]["releases"] += 1
    if is_viking(r): hour_core[h]["viking"] += 1
    if is_core(r): hour_core[h]["core_kw"] += 1
# core-new: core-keyword fresh questions, list their ids + status + viso
core_new = []
for r in fresh_rows:
    if is_core(r) and not is_viking(r):
        det = det_by.get(r["id"], {})
        core_new.append({"id": r["id"][:8], "hour": datetime.fromtimestamp(r["timestamp"] / 1000, WIB).hour,
                         "status": r.get("status"), "content": (r.get("content") or "")[:110],
                         "viso": (det.get("marathonEligibleIsos") or [{}])[0].get("viso") if isinstance(det, dict) else None,
                         "detail_status": det.get("status") if isinstance(det, dict) else None,
                         "marathonActive": det.get("marathonActive") if isinstance(det, dict) else None,
                         "marathonConcluded": det.get("marathonConcluded") if isinstance(det, dict) else None})
out["fresh_topics"] = {"n_fresh": len(fresh_rows),
                       "viking_share": round(sum(1 for r in fresh_rows if is_viking(r)) / max(1, len(fresh_rows)), 3),
                       "core_kw_share": round(sum(1 for r in fresh_rows if is_core(r)) / max(1, len(fresh_rows)), 3),
                       "per_hour": {str(h): v for h, v in sorted(hour_core.items())},
                       "core_new": core_new}
# viso-0 core in full listing top (scan-style): count fresh viso-0 from details
viso0 = []
for qid, det in det_by.items():
    if isinstance(det, dict) and det.get("status") == "in_progress":
        viso0.append(qid[:8])
out["viso0_in_progress_in_sample"] = viso0

# --- abandoned share + sample status counts ---
sc = Counter()
tot = 0
for lst in isos_by.values():
    if isinstance(lst, list):
        for x in lst:
            sc[x.get("status")] += 1; tot += 1
out["abandoned_share"] = round(100 * sc.get("abandoned", 0) / max(1, tot), 1)
out["sample_status_counts"] = dict(sc)

print(json.dumps(out, ensure_ascii=False, indent=1))
with open(f"{D6}/supp7.json", "w") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
