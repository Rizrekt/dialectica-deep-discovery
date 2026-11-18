#!/usr/bin/env python3
"""Analysis for BELAJAR-LOG run 2026-11-15 02:37 WIB (incremental vs 02:40).
Mirrors belajar-2026-11-14/analyze.py methodology + §45 wrapper metrics."""
import json, re, statistics as st, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/home/hatch/workspace/research/dialectica/provider")
from openrouter_wrapper import mechanical_floor  # noqa: E402

D = "/home/hatch/workspace/research/dialectica/belajar-2026-11-15/run5-1037"
D0 = "/home/hatch/workspace/research/dialectica/belajar-2026-11-14/run4-0237"
WIB = timezone(timedelta(hours=7))
CUT = int(datetime(2026, 11, 14, 19, 37, tzinfo=timezone.utc).timestamp() * 1000)  # 02:37 WIB

def load(base, n):
    with open(f"{base}/{n}") as fh: return json.load(fh)

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

state, lb = load(D, "state.json"), load(D, "leaderboard.json")
isrs = load(D, "isrs.json")["isrs"]
isos_by, det_by, tags = load(D, "isos_by_isr.json"), load(D, "details_by_isr.json"), load(D, "sample_tags.json")
state0 = load(D0, "state.json")
out = {}

out["own_scores"] = state["scores"]
out["own_scores_0237"] = state0["scores"]
jobs = (state["jobs"] or {}).get("jobs") or []
out["own_jobs"] = [{"id": j.get("id"), "status": j.get("jobStatus"),
                    "isr": (j.get("input") or {}).get("isrId"),
                    "startedAt": j.get("startedAt")} for j in jobs]
out["own_jobs_new"] = [j for j in out["own_jobs"]
                       if j["startedAt"] and j["startedAt"] >= CUT // 1000]

names = {r["userId"]: r.get("userName") or "" for r in lb}
house_ids = {r["userId"] for r in lb if (r.get("userName") or "").startswith("Dialectica")}
ext_lb = [r for r in lb if r["userId"] not in house_ids]
out["lb"] = {
    "rows": len(lb), "house_rows": len(house_ids),
    "ext_coins_max": max(r["coins"] for r in ext_lb), "ext_coins_min_top100": min(r["coins"] for r in ext_lb),
    "agents_ge400": sum(1 for r in ext_lb if r["coins"] >= 400),
    "top15_external": [{"name": r["userName"], "coins": round(r["coins"], 1),
                        "marathonWins": r.get("marathonWinsCount"), "rank": r.get("rank")} for r in ext_lb[:15]],
}
def who(uid): return names.get(uid) or uid[:8]

def hour_wib(ms): return datetime.fromtimestamp(ms/1000, WIB).hour
fresh_rows = [r for r in isrs if (r.get("timestamp") or 0) >= CUT]
fresh_hours = Counter(hour_wib(r["timestamp"]) for r in fresh_rows)
span_h = (max(r["timestamp"] for r in isrs) - CUT) / 3600000
out["listing"] = {
    "total": len(isrs), "fresh_since_0237": len(fresh_rows),
    "fresh_span_hours": round(span_h, 2), "fresh_per_hour": round(len(fresh_rows)/span_h, 1) if span_h else None,
    "status_counts": dict(Counter(r.get("status") for r in isrs)),
    "fresh_status_counts": dict(Counter(r.get("status") for r in fresh_rows)),
    "top_hours_fresh": fresh_hours.most_common(8),
    "hour_22_fresh": fresh_hours[22],
    "hour_12_13_fresh_share": round((fresh_hours[12]+fresh_hours[13])/max(1, len(fresh_rows)), 3),
    "askers_fresh": len({r.get("author") for r in fresh_rows}),
}

OUR_ISO = {"fcb7b015", "097df475", "0d76cc7c", "f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"}
def is_ours(iso): return any(iso["id"].startswith(p) for p in OUR_ISO)
def answer_text(iso):
    sd = ((iso.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    return sd.get("answer")

records = []
for qid, lst in isos_by.items():
    if not isinstance(lst, list): continue
    qq = next((r for r in isrs if r["id"] == qid), {})
    for iso in lst:
        records.append({"qid": qid, "tag": tags.get(qid, ""), "q_ts": qq.get("timestamp"),
                        "fresh_q": (qq.get("timestamp") or 0) >= CUT, **iso})
out["sample"] = {"questions": len(isos_by), "isos": len(records),
                 "status_counts": dict(Counter(r.get("status") for r in records)),
                 "fresh_questions": sum(1 for q in isos_by if (next((r for r in isrs if r["id"] == q), {}) or {}).get("timestamp", 0) >= CUT)}

ext = [r for r in records if r["author"] not in house_ids and not is_ours(r)]
ours = [r for r in records if is_ours(r)]
house_isos = [r for r in records if r["author"] in house_ids]
out["sample"]["external_isos"] = len(ext); out["sample"]["house_isos"] = len(house_isos)
out["sample"]["our_isos_found"] = [{"id": r["id"][:8], "qid": r["qid"][:8], "status": r["status"],
                                    "support": r.get("support"), "refute": r.get("refute")} for r in ours]

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

pion = {"external": 0, "house": 0, "ours": 0}
lat_ext, lat_house = [], []
fresh_pion = {"external": 0, "house": 0}
for qid in isos_by:
    lst = isos_by.get(qid)
    if not isinstance(lst, list): continue
    ver = sorted([i for i in lst if i.get("status") == "verified"], key=lambda i: i.get("timestamp") or 0)
    qq = next((r for r in isrs if r["id"] == qid), {})
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
                   "per_question_mean": round(len(awarded)/max(1, len(det_by)), 2),
                   "questions_with_award_share": round(len(aw_by_q)/max(1, len(det_by)), 3),
                   "external_agents_with_win": len(win_auth),
                   "top_external_winners": [{"name": who(u), "wins": c} for u, c in win_auth.most_common(8)],
                   "rules_versions": dict(Counter(str(d.get("arenaRulesVersion")) for d in det_by.values() if isinstance(d, dict)))}

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
panels = [r for r in ext if r["status"] in ("verified", "falsified") and answer_text(r)]
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

# winners' verified answers style (leaderboard coins>=400 external authors)
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

# monitored questions: current status
MON = ["48c80dc6", "0dbd4532", "1287c2ae", "472b29a0", "71f472d6", "60fa9935", "970d09db",
       "1d758352", "2c7efc3e", "1d3efb52", "f80ac8d3", "8ca09770", "67635c30", "b1376a5e", "6f5820ff", "50e815cc"]
mon = {}
for qid, det in det_by.items():
    if not isinstance(det, dict): continue
    if qid[:8] in MON:
        lst = isos_by.get(qid, [])
        sc = Counter(x.get("status") for x in lst) if isinstance(lst, list) else {}
        ver = [x for x in lst if isinstance(lst, list) and x.get("status") == "verified"] if isinstance(lst, list) else []
        ver_new = [x for x in ver if (x.get("timestamp") or 0) >= CUT * 1 and (x.get("timestamp") or 0) >= CUT]
        mon[qid[:8]] = {"status": det.get("status"), "marathonActive": det.get("marathonActive"),
                        "marathonConcluded": det.get("marathonConcluded"),
                        "arenaRulesVersion": det.get("arenaRulesVersion"),
                        "isos": len(lst) if isinstance(lst, list) else lst,
                        "status_counts": dict(sc),
                        "verified_new_since_0237": len(ver_new),
                        "verified_new_authors": [who(x["author"]) for x in ver_new]}
out["monitored"] = mon

# fresh-era verified answers: who won pioneer in fresh questions + their style
fresh_ver = [r for r in ext if r["fresh_q"] and r["status"] == "verified" and answer_text(r)]
out["fresh_verified_style"] = {"n": len(fresh_ver),
    "chars_median": med([len(answer_text(r)) for r in fresh_ver]),
    "density_median": med([mechanical_floor(answer_text(r))["citation_density"] for r in fresh_ver]),
    "ratio_median": med([mechanical_floor(answer_text(r))["bound_ratio"] for r in fresh_ver]),
    "url_ge1_share": round(sum(1 for r in fresh_ver if mechanical_floor(answer_text(r))["url_count"] >= 1)/len(fresh_ver), 3) if fresh_ver else None}

print(json.dumps(out, ensure_ascii=False, indent=1))
with open(f"{D}/analysis5.json", "w") as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
