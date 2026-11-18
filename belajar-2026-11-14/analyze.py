#!/usr/bin/env python3
"""Analysis for STUDI-KOHORT-2026-11-14. Methodology mirrors MEKANISME §30 +
STUDI-JUARA-VERDICT §1; citation metrics computed by the §45 wrapper itself
(openrouter_wrapper.mechanical_floor) for exact parity."""
import json, math, re, statistics as st, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/home/hatch/workspace/research/dialectica/provider")
from openrouter_wrapper import mechanical_floor  # noqa: E402

D = "/home/hatch/workspace/research/dialectica/belajar-2026-11-14"
WIB = timezone(timedelta(hours=7))
CUT = 1794294000000  # 2026-11-10T07:00Z

def load(n):
    with open(f"{D}/{n}") as fh: return json.load(fh)

def med(xs): return round(st.median(xs), 3) if xs else None
def q(xs, p):
    if not xs: return None
    s = sorted(xs); return round(s[min(len(s)-1, max(0, int(p*len(s))))], 3)
def cliffs_d(a, b):
    if not a or not b: return None
    gt = lt = 0
    for x in a:
        for y in b:
            if x > y: gt += 1
            elif x < y: lt += 1
    return round((gt - lt) / (len(a) * len(b)), 3)

state, lb = load("state.json"), load("leaderboard.json")
isrs = load("isrs.json")["isrs"]
isos_by, det_by, tags = load("isos_by_isr.json"), load("details_by_isr.json"), load("sample_tags.json")
out = {}

# ---------- own state ----------
out["own_scores"] = state["scores"]
out["own_usage"] = state["usage"]
jobs = (state["jobs"] or {}).get("jobs") or []
out["own_jobs"] = [{"id": j.get("id"), "status": j.get("jobStatus"), "isr": j.get("isrId") or j.get("questionId"),
                    "created": j.get("createdAt")} for j in jobs]

# ---------- leaderboard ----------
names = {r["userId"]: r.get("userName") or "" for r in lb}
house_ids = {r["userId"] for r in lb if (r.get("userName") or "").startswith("Dialectica")}
ext_lb = [r for r in lb if r["userId"] not in house_ids]
out["lb"] = {
    "rows": len(lb), "house_rows": len(house_ids),
    "house_names": sorted(names[i] for i in house_ids),
    "ext_coins_max": max(r["coins"] for r in ext_lb), "ext_coins_min_top100": min(r["coins"] for r in ext_lb),
    "top15_external": [{"name": r["userName"], "coins": round(r["coins"], 1),
                        "marathonWins": r.get("marathonWinsCount"), "rank": r.get("rank")} for r in ext_lb[:15]],
    "pioneer_house_coins": [round(r["coins"], 1) for r in lb if r.get("userName") == "Dialectica (Pioneer)"],
}
def who(uid): return names.get(uid) or uid[:8]

# ---------- listing-level ----------
def hour_wib(ms): return datetime.fromtimestamp(ms/1000, WIB).hour
all_hours = Counter(hour_wib(r["timestamp"]) for r in isrs if r.get("timestamp"))
fresh_rows = [r for r in isrs if (r.get("timestamp") or 0) >= CUT]
old_rows = [r for r in isrs if (r.get("timestamp") or 0) < CUT]
fresh_hours = Counter(hour_wib(r["timestamp"]) for r in fresh_rows)
span_days = (max(r["timestamp"] for r in isrs) - CUT) / 86400000
out["listing"] = {
    "total": len(isrs), "fresh_created_since_cut": len(fresh_rows), "old": len(old_rows),
    "fresh_span_days": round(span_days, 2), "fresh_per_day": round(len(fresh_rows)/span_days, 1) if span_days else None,
    "status_counts": dict(Counter(r.get("status") for r in isrs)),
    "top_hours_all": all_hours.most_common(6), "top_hours_fresh": fresh_hours.most_common(6),
    "hour_12_13_fresh_share": round((fresh_hours[12]+fresh_hours[13])/max(1, len(fresh_rows)), 3),
    "hour_17_fresh": fresh_hours[17], "tagged_share": round(sum(1 for r in isrs if r.get("domainTags"))/len(isrs), 3),
}

# ---------- sample isos ----------
OUR_ISO = {"fcb7b015", "097df475", "0d76cc7c"}
def is_ours(iso): return any(iso["id"].startswith(p) for p in OUR_ISO)
def answer_text(iso):
    sd = ((iso.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    return sd.get("answer")

records = []  # per-iso dict
for qid, lst in isos_by.items():
    if not isinstance(lst, list): continue
    qq = next((r for r in isrs if r["id"] == qid), {})
    for iso in lst:
        records.append({"qid": qid, "tag": tags.get(qid, ""), "q_ts": qq.get("timestamp"),
                        "fresh_q": (qq.get("timestamp") or 0) >= CUT, **iso})
out["sample"] = {"questions": len(isos_by),
                 "isos": len(records),
                 "status_counts": dict(Counter(r.get("status") for r in records))}

ext = [r for r in records if r["author"] not in house_ids and not is_ours(r)]
ours = [r for r in records if is_ours(r)]
house_isos = [r for r in records if r["author"] in house_ids]
out["sample"]["external_isos"] = len(ext); out["sample"]["house_isos"] = len(house_isos); out["sample"]["our_isos_found"] = len(ours)

# per-author verdict rates (external, all sampled)
by_auth = defaultdict(lambda: {"v": 0, "f": 0, "n": 0})
for r in ext:
    a = by_auth[r["author"]]; a["n"] += 1
    if r["status"] == "verified": a["v"] += 1
    elif r["status"] == "falsified": a["f"] += 1
rates = [a["v"]/(a["v"]+a["f"]) for a in by_auth.values() if a["v"]+a["f"] >= 5]
tv = sum(a["v"] for a in by_auth.values()); tf = sum(a["f"] for a in by_auth.values())
out["verdict_rates"] = {"agents_ge5_verdicts": len(rates), "median": med(rates), "q1": q(rates, .25), "q3": q(rates, .75),
                        "pooled": round(tv/(tv+tf), 3) if tv+tf else None, "pooled_v": tv, "pooled_f": tf,
                        "share_ge55": round(sum(1 for x in rates if x >= .55)/len(rates), 3) if rates else None}

# answer-hour histogram (external isos)
ans_hours = Counter(hour_wib(r["timestamp"]) for r in ext if r.get("timestamp"))
out["answer_hours_top"] = ans_hours.most_common(6)

# viso-at-entry + pioneer (per question, verified sorted by ts)
pion = {"external": 0, "house": 0, "ours": 0}
lat_ext, lat_house, viso_entry = [], [], []
fresh_pion = {"external": 0, "house": 0}
for qid in isos_by:
    lst = isos_by.get(qid)
    if not isinstance(lst, list): continue
    ver = sorted([i for i in lst if i.get("status") == "verified"], key=lambda i: i.get("timestamp") or 0)
    qq = next((r for r in isrs if r["id"] == qid), {})
    for rank, iso in enumerate(ver):
        if iso["author"] not in house_ids and not is_ours(iso): viso_entry.append(rank)
    if ver:
        first = ver[0]
        grp = "house" if first["author"] in house_ids else ("ours" if is_ours(first) else "external")
        pion[grp] += 1
        if (qq.get("timestamp") or 0) >= CUT and grp in fresh_pion: fresh_pion[grp] += 1
        if qq.get("timestamp") and first.get("timestamp"):
            lat = (first["timestamp"] - qq["timestamp"]) / 1000.0
            (lat_house if grp == "house" else lat_ext if grp == "external" else []).append(lat)
out["pioneer"] = {"sample_questions_with_verified": pion["external"]+pion["house"]+pion["ours"], **pion,
                  "fresh_questions": fresh_pion,
                  "latency_median_s_external": med(lat_ext), "latency_median_s_house": med(lat_house),
                  "latency_n_ext": len(lat_ext), "latency_n_house": len(lat_house)}
out["viso_entry"] = {"n": len(viso_entry), "median": med(viso_entry), "q1": q(viso_entry, .25), "q3": q(viso_entry, .75),
                     "share_rank0": round(sum(1 for x in viso_entry if x == 0)/len(viso_entry), 3) if viso_entry else None,
                     "share_rank_ge2": round(sum(1 for x in viso_entry if x >= 2)/len(viso_entry), 3) if viso_entry else None}

# marathon awarded (details)
iso_author = {r["id"]: r["author"] for r in records}
awarded = []
for qid, det in det_by.items():
    if not isinstance(det, dict): continue
    for e in det.get("marathonEligibleIsos") or []:
        if e.get("awarded"): awarded.append({"qid": qid, "iso": e["isoId"], "author": iso_author.get(e["isoId"])})
aw_ext = [a for a in awarded if a["author"] and a["author"] not in house_ids]
aw_house = [a for a in awarded if a["author"] in house_ids]
aw_by_q = Counter(a["qid"] for a in awarded)
win_auth = Counter(a["author"] for a in aw_ext)
out["marathon"] = {"sample_questions": len(det_by), "awarded_total": len(awarded),
                   "awarded_external": len(aw_ext), "awarded_house": len(aw_house),
                   "awarded_unknown_author": len(awarded)-len(aw_ext)-len(aw_house),
                   "per_question_mean": round(len(awarded)/max(1, len(det_by)), 2),
                   "questions_with_award_share": round(len(aw_by_q)/max(1, len(det_by)), 3),
                   "external_agents_with_win": len(win_auth),
                   "top_external_winners": [{"name": who(u), "wins": c} for u, c in win_auth.most_common(8)],
                   "rules_versions": dict(Counter(str(d.get("arenaRulesVersion")) for d in det_by.values() if isinstance(d, dict)))}

# ---------- style metrics: judge panels (verified vs falsified, external) ----------
HEDGE = re.compile(r"\b(may|might|could|suggests?|appears? to|likely|possibly|arguably)\b", re.I)
def style(txt):
    mf = mechanical_floor(txt)
    lines = txt.splitlines()
    return {"chars": len(txt), "density": mf["citation_density"], "ratio": mf["bound_ratio"],
            "url_count": mf["url_count"], "has_url": mf["url_count"] >= 1,
            "floor_pass": mf["passed"],
            "has_header": any(l.startswith("#") for l in lines),
            "num_tokens": mf["number_tokens"],
            "hedges_per_1k": round(len(HEDGE.findall(txt)) / (len(txt)/1000), 3) if txt else 0}
panels = [r for r in ext if "panel" in r["tag"] and r["status"] in ("verified", "falsified") and answer_text(r)]
sv = [style(answer_text(r)) for r in panels if r["status"] == "verified"]
sf = [style(answer_text(r)) for r in panels if r["status"] == "falsified"]
def summ(rows, key): return {"median": med([r[key] for r in rows]), "q1": q([r[key] for r in rows], .25), "q3": q([r[key] for r in rows], .75)}
out["style_panels"] = {"n_verified": len(sv), "n_falsified": len(sf),
    "chars": {"v": summ(sv, "chars"), "f": summ(sf, "chars"), "d": cliffs_d([r["chars"] for r in sv], [r["chars"] for r in sf])},
    "density": {"v": summ(sv, "density"), "f": summ(sf, "density"), "d": cliffs_d([r["density"] for r in sv], [r["density"] for r in sf])},
    "ratio": {"v": summ(sv, "ratio"), "f": summ(sf, "ratio"), "d": cliffs_d([r["ratio"] for r in sv], [r["ratio"] for r in sf])},
    "url_ge1_share": {"v": round(sum(r["has_url"] for r in sv)/len(sv), 3) if sv else None,
                      "f": round(sum(r["has_url"] for r in sf)/len(sf), 3) if sf else None},
    "header_share": {"v": round(sum(r["has_header"] for r in sv)/len(sv), 3) if sv else None,
                     "f": round(sum(r["has_header"] for r in sf)/len(sf), 3) if sf else None},
    "floor_pass_share": {"v": round(sum(r["floor_pass"] for r in sv)/len(sv), 3) if sv else None,
                         "f": round(sum(r["floor_pass"] for r in sf)/len(sf), 3) if sf else None},
    "hedges": {"v": summ(sv, "hedges_per_1k"), "f": summ(sf, "hedges_per_1k"),
               "d": cliffs_d([r["hedges_per_1k"] for r in sv], [r["hedges_per_1k"] for r in sf])}}

# winners' verified answers style (leaderboard coins>=400 external authors), all sampled questions
win_ids = {r["userId"] for r in ext_lb if r["coins"] >= 400}
wv = [r for r in ext if r["author"] in win_ids and r["status"] == "verified" and answer_text(r)]
per_agent_len = defaultdict(list)
for r in wv: per_agent_len[r["author"]].append(len(answer_text(r)))
out["winners_style"] = {"agents_on_lb_ge400": len(win_ids), "agents_in_sample": len(per_agent_len),
                        "verified_answers": len(wv),
                        "pooled_chars_median": med([len(answer_text(r)) for r in wv]),
                        "per_agent_median_chars_median": med([st.median(v) for v in per_agent_len.values()]),
                        "density_median": med([mechanical_floor(answer_text(r))["citation_density"] for r in wv]),
                        "ratio_median": med([mechanical_floor(answer_text(r))["bound_ratio"] for r in wv])}

# all-sample verified style for reference (pooled chars distribution)
allv = [len(answer_text(r)) for r in ext if r["status"] == "verified" and answer_text(r)]
out["all_verified_chars"] = {"n": len(allv), "median": med(allv), "q1": q(allv, .25), "q3": q(allv, .75),
                             "share_lt6000": round(sum(1 for x in allv if x < 6000)/len(allv), 3) if allv else None,
                             "share_6_12k": round(sum(1 for x in allv if 6000 <= x <= 12000)/len(allv), 3) if allv else None,
                             "share_gt12k": round(sum(1 for x in allv if x > 12000)/len(allv), 3) if allv else None}

print(json.dumps(out, ensure_ascii=False, indent=1))
with open(f"{D}/analysis.json", "w") as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
