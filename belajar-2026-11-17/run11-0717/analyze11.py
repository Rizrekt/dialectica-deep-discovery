#!/usr/bin/env python3
"""Analysis for STUDI-KOHORT-2026-11-17 + KORPUS-JUARA-2026-11-17.
Mirrors 2026-11-14 methodology: citation metrics by provider wrapper's
mechanical_floor/citation_spans; old structural-pattern definitions from
KORPUS-JUARA-2026-11-14 §6. Read-only over local pull artefacts.
"""
import json, re, statistics as st, sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/home/hatch/workspace/research/dialectica/provider")
from openrouter_wrapper import mechanical_floor, citation_spans, NUM_RE, BOUND_WINDOW  # noqa: E402
try:
    from serve_gate import detect_evasive_source_closing  # noqa: E402
except Exception:
    detect_evasive_source_closing = None

ROOT = "/home/hatch/workspace/research/dialectica"
D = f"{ROOT}/belajar-2026-11-17/run11-0717"
RUN10 = f"{ROOT}/belajar-2026-11-17/run10-0237"
RUN9 = f"{ROOT}/belajar-2026-11-16/run9-1837"
BASE14 = f"{ROOT}/belajar-2026-11-14"
RUN2_14 = f"{BASE14}/run2-1037"
WIB = timezone(timedelta(hours=7))
CUT_RUN10 = int(datetime(2026, 11, 16, 19, 37, tzinfo=timezone.utc).timestamp() * 1000)
OLD_PANEL = ["chirpy", "Rodeo", "Febriyan", "Mauldrop", "Adam Reinhard", "megumii", "SyntaxZ", "GaBot",
             "HIMANSHU", "Gufran The Legend", "can-earn?", "Discord 1"]
HEDGE = re.compile(r"\b(may|might|could|suggests?|appears? to|likely|possibly|arguably)\b", re.I)
NOVELTY = re.compile(r"belum dibahas|belum ada|belum disentuh|belum dipertimbangkan|yang baru|kebaruan|novel|"
                     r"not (yet )?(covered|addressed|discussed)|belum pernah|missing|hilang dari|"
                     r"baru dalam jawaban ini|baru di jawaban ini|baru pada jawaban ini|baru dalam respons ini", re.I)
E3_FALLBACK = re.compile(r"avoids pinpoint references|cannot be verified from the text alone|no live web access|"
                         r"I give no URLs|relies on widely documented .* rather than on any single citation", re.I | re.S)
UNCERTAINTY_HEADING = re.compile(r"^#{1,6}\s.*(uncertaint|limitation|unknown|caveat|what would falsify|falsifier)", re.I | re.M)
SOURCE_HEADING = re.compile(r"(sources?|references?|bibliography|sumber|referensi)", re.I)

def load(base, name):
    with open(f"{base}/{name}") as fh: return json.load(fh)

def med(xs): return round(st.median(xs), 3) if xs else None
def quant(xs, p):
    if not xs: return None
    s = sorted(xs); return round(s[min(len(s)-1, max(0, int(p*len(s))))], 3)
def summ(xs): return {"median": med(xs), "q1": quant(xs, .25), "q3": quant(xs, .75)}
def cliffs_d(a, b):
    if not a or not b: return None
    bs = sorted(b); gt = lt = 0
    for x in a:
        gt += bisect_left(bs, x)          # count of b strictly below x -> P(a>b) mass
        lt += len(bs) - bisect_right(bs, x)  # count of b strictly above x -> P(a<b) mass
    return round((gt - lt) / (len(a) * len(b)), 3)
def pct(n, d): return round(100*n/d, 1) if d else None
def ts_ms(v):
    if v is None: return None
    if isinstance(v, (int, float)):
        return int(v*1000) if v < 10_000_000_000 else int(v)
    if isinstance(v, str):
        try:
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            return int(dt.timestamp()*1000)
        except Exception:
            return None
    return None
def answer_text(iso):
    sd = ((iso.get("reveal") or {}).get("data") or {}).get("structured_data") or {}
    return sd.get("answer")

# ---------------- snapshots / leaderboard ----------------
snaps = [("2026-11-14 02:40", BASE14), ("2026-11-14 10:37", RUN2_14), ("2026-11-16 18:37", RUN9),
         ("2026-11-17 02:37", RUN10), ("2026-11-17 07:17", D)]
lbs = {}
for label, base in snaps:
    try: lbs[label] = load(base, "leaderboard.json")
    except Exception: lbs[label] = []
def ext_map(lb):
    out = {}
    for i, r in enumerate(lb):
        if (r.get("userName") or "").startswith("Dialectica"): continue
        rr = dict(r); rr["_rank_calc"] = r.get("rank") or (i+1)
        out[r["userId"]] = rr
    return out
ext_snaps = {label: ext_map(lb) for label, lb in lbs.items()}
cur_label = snaps[-1][0]; cur_ext = ext_snaps[cur_label]
names = {uid: r.get("userName") or uid[:8] for uid, r in cur_ext.items()}
# names for agents no longer in current top100: fall back to older snapshots
for label, _ in snaps:
    for uid, r in ext_snaps[label].items(): names.setdefault(uid, r.get("userName") or uid[:8])
house_ids = set()
for lb in lbs.values():
    house_ids |= {r["userId"] for r in lb if (r.get("userName") or "").startswith("Dialectica")}

appear = Counter(); 
for label, _ in snaps:
    for uid in ext_snaps[label]: appear[uid] += 1

# ---------------- current pull records ----------------
state = load(D, "state.json"); isrs = load(D, "isrs.json")["isrs"]
isos_by = load(D, "isos_by_isr.json"); det_by = load(D, "details_by_isr.json"); tags = load(D, "sample_tags.json")
try: pull_errors = load(D, "errors.json")
except Exception: pull_errors = {}
qmap = {r["id"]: r for r in isrs}
OUR = {"fcb7b015", "097df475", "0d76cc7c", "f0bb3586", "7d81c51d", "5b5e8212", "a3b8b34a"}
def is_ours(iso): return any(iso["id"].startswith(p) for p in OUR)

records = []
for qid, lst in isos_by.items():
    if not isinstance(lst, list): continue
    qq = qmap.get(qid, {})
    for iso in lst:
        records.append({"qid": qid, "tag": tags.get(qid, ""), "q_ts": qq.get("timestamp"), **iso})
ext = [r for r in records if r.get("author") not in house_ids and not is_ours(r)]

# pioneer + marathon labels
pioneer_by_q = {}
for qid, lst in isos_by.items():
    if not isinstance(lst, list): continue
    ver = [i for i in lst if i.get("status") == "verified"]
    if ver:
        pioneer_by_q[qid] = sorted(ver, key=lambda i: ts_ms(i.get("timestamp")) or 0)[0]["id"]
awarded_ids = set(); awarded_rows = []
for qid, det in det_by.items():
    if not isinstance(det, dict): continue
    for e in det.get("marathonEligibleIsos") or []:
        if e.get("awarded"):
            awarded_ids.add(e.get("isoId")); awarded_rows.append({"qid": qid, "iso": e.get("isoId")})
def slot_label(r):
    p = pioneer_by_q.get(r["qid"]) == r["id"]; m = r["id"] in awarded_ids
    return ("P+M" if p and m else "P" if p else "M" if m else "—")

# ---------------- feature extraction ----------------
def features(txt):
    mf = mechanical_floor(txt)
    cites = citation_spans(txt)
    lines = txt.splitlines()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", txt) if b.strip()]
    closing = blocks[-1] if blocks else ""
    heads = [ln for ln in lines if re.match(r"^#{1,6}\s", ln)]
    bound_positions = []
    specific_counts = Counter(); specific_bound = set()
    for m in NUM_RE.finditer(txt):
        s, e = m.start(), m.end()
        if any(s < ce and cs < e for cs, ce, _ in cites): continue
        is_bound = any(max(cs - e, s - ce) <= BOUND_WINDOW for cs, ce, _ in cites)
        if is_bound: bound_positions.append(s)
        tok = m.group(0)
        numstr = tok.replace(",", "").replace("%", "")
        try: val = float(numstr)
        except Exception: val = None
        specific = ("%" in tok or "." in tok or (val is not None and val >= 100) or
                    (re.fullmatch(r"(19|20)\d{2}", tok or "") is not None))
        if specific:
            specific_counts[tok] += 1
            if is_bound: specific_bound.add(tok)
    pivot = any(specific_counts[t] >= 3 and t in specific_bound for t in specific_counts)
    last800 = txt[-800:] if len(txt) > 800 else txt
    if detect_evasive_source_closing is not None:
        e3 = bool(detect_evasive_source_closing(txt))
    else:
        e3 = bool(E3_FALLBACK.search(closing))
    last_head = heads[-1] if heads else ""
    return {
        "chars": len(txt), "url_count": mf["url_count"], "density": mf["citation_density"],
        "ratio": mf["bound_ratio"], "num_tokens": mf["number_tokens"],
        "k1": mf["url_count"] >= 1 and mf["citation_density"] >= 0.5,
        "floor030": mf["passed"], "floor015": (mf["url_count"] >= 1 and mf["citation_density"] >= 0.5 and mf["bound_ratio"] >= 0.15),
        "has_header": bool(heads), "numbered_header": any(re.match(r"^#{1,6}\s*\d+[\.\)]?\s", h) for h in heads),
        "n_sections": len(heads),
        "cite_first1000": any(cs < 1000 for cs, _, _ in cites),
        "cite_last_quartile": any(cs >= 0.75*len(txt) for cs, _, _ in cites) if txt else False,
        "cite_3_quartiles": len({min(3, int((cs/len(txt))*4)) for cs, _, _ in cites}) >= 3 if txt and cites else False,
        "bound_in_last800": any(s >= len(txt)-800 for s in bound_positions),
        "pivot_proxy": pivot,
        "novelty_naming_closing": bool(NOVELTY.search(closing)),
        "e3_evasive": e3,
        "closing_has_citation": any(cs >= len(txt)-len(closing) for cs, _, _ in cites) if closing else False,
        "closing_is_source_list": bool(SOURCE_HEADING.search(last_head)) and (len(txt)-txt.rfind(last_head) <= len(closing)+200 if last_head else False),
        "hedges_per_1k": round(len(HEDGE.findall(txt))/(len(txt)/1000), 3) if txt else 0,
        "has_hedge": bool(HEDGE.search(txt)), "hedge_in_closing": bool(HEDGE.search(closing)),
        "uncertainty_heading": bool(UNCERTAINTY_HEADING.search(txt)),
    }

feat_cache = {}
def F(r):
    if r["id"] not in feat_cache:
        feat_cache[r["id"]] = features(answer_text(r))
    return feat_cache[r["id"]]

def feature_summary(rows):
    if not rows: return {"n": 0}
    fs = [F(r) for r in rows]
    out = {"n": len(rows),
           "chars": summ([f["chars"] for f in fs]),
           "chars_bands_pct": {"<3000": pct(sum(1 for f in fs if f["chars"] < 3000), len(fs)),
                               "3000-4499": pct(sum(1 for f in fs if 3000 <= f["chars"] < 4500), len(fs)),
                               "4500-8000": pct(sum(1 for f in fs if 4500 <= f["chars"] <= 8000), len(fs)),
                               "8000-12000": pct(sum(1 for f in fs if 8000 < f["chars"] <= 12000), len(fs)),
                               ">12000": pct(sum(1 for f in fs if f["chars"] > 12000), len(fs))},
           "url_median": med([f["url_count"] for f in fs]),
           "density": summ([f["density"] for f in fs]), "ratio": summ([f["ratio"] for f in fs]),
           "k1_pct": pct(sum(1 for f in fs if f["k1"]), len(fs)),
           "floor030_pct": pct(sum(1 for f in fs if f["floor030"]), len(fs)),
           "floor015_pct": pct(sum(1 for f in fs if f["floor015"]), len(fs)),
           "sections_median": med([f["n_sections"] for f in fs])}
    for key in ["has_header", "numbered_header", "cite_first1000", "cite_last_quartile", "cite_3_quartiles",
                "bound_in_last800", "pivot_proxy", "novelty_naming_closing", "e3_evasive", "closing_has_citation",
                "closing_is_source_list", "has_hedge", "hedge_in_closing", "uncertainty_heading"]:
        out[key + "_pct"] = pct(sum(1 for f in fs if f[key]), len(fs))
    out["hedges_per_1k"] = summ([f["hedges_per_1k"] for f in fs])
    return out

def gate_table(vrows, frows):
    def rates(rows):
        if not rows: return {}
        fs = [F(r) for r in rows]
        k1 = [f for f in fs if f["k1"]]
        return {"n": len(fs),
                "k1_pct": pct(len(k1), len(fs)),
                "k2_030_pct": pct(sum(1 for f in fs if f["ratio"] >= 0.30), len(fs)),
                "k2_015_pct": pct(sum(1 for f in fs if f["ratio"] >= 0.15), len(fs)),
                "full_030_pct": pct(sum(1 for f in fs if f["floor030"]), len(fs)),
                "full_015_pct": pct(sum(1 for f in fs if f["floor015"]), len(fs)),
                "in_k1_030_pct": pct(sum(1 for f in k1 if f["ratio"] >= 0.30), len(k1)),
                "in_k1_015_pct": pct(sum(1 for f in k1 if f["ratio"] >= 0.15), len(k1)),
                "density_median": med([f["density"] for f in fs]), "ratio_median": med([f["ratio"] for f in fs]),
                "chars_median": med([f["chars"] for f in fs])}
    v, f = rates(vrows), rates(frows)
    gaps = {}
    for k in ["k1_pct", "k2_030_pct", "k2_015_pct", "full_030_pct", "full_015_pct", "in_k1_030_pct", "in_k1_015_pct"]:
        if v.get(k) is not None and f.get(k) is not None: gaps[k + "_gap_pp"] = round(v[k]-f[k], 1)
    ds = {}
    if vrows and frows:
        fv = [F(r) for r in vrows]; ff = [F(r) for r in frows]
        for key in ["chars", "density", "ratio", "hedges_per_1k"]:
            ds[key + "_d"] = cliffs_d([x[key] for x in fv], [x[key] for x in ff])
        ds["url_ge1_gap_pp"] = round(pct(sum(1 for x in fv if x["url_count"] >= 1), len(fv)) - pct(sum(1 for x in ff if x["url_count"] >= 1), len(ff)), 1)
        ds["header_gap_pp"] = round(pct(sum(1 for x in fv if x["has_header"]), len(fv)) - pct(sum(1 for x in ff if x["has_header"]), len(ff)), 1)
    return {"verified": v, "falsified": f, "gaps": gaps, "cliffs": ds}

out = {}
out["meta"] = {"pull_meta": load(D, "pull_meta.json"), "errors": pull_errors,
               "sample": {"questions": len(isos_by), "isos": len(records), "external_isos": len(ext),
                          "status_counts": dict(Counter(r.get("status") for r in records)),
                          "tag_counts": dict(Counter(tags.values()))}}
out["own_scores"] = state["scores"]
out["own_jobs_n"] = len((state["jobs"] or {}).get("jobs") or [])

# ---------------- listing / supply ----------------
old_isrs = load(BASE14, "isrs.json")["isrs"]; run10_isrs = load(RUN10, "isrs.json")["isrs"]
old_ids = {r["id"] for r in old_isrs}; run10_ids = {r["id"] for r in run10_isrs}; cur_ids = {r["id"] for r in isrs}
def growth(base_ids, base_rows):
    new = [r for r in isrs if r["id"] not in base_ids]
    span_d = (max(r["timestamp"] for r in isrs) - max(r["timestamp"] for r in base_rows)) / 86400000
    return {"new_questions": len(new), "span_days": round(span_d, 2),
            "per_day": round(len(new)/span_d, 1) if span_d else None,
            "askers_unique": len({r.get("author") for r in new}),
            "house_share_pct": pct(sum(1 for r in new if r.get("author") in house_ids), len(new)),
            "status_counts": dict(Counter(r.get("status") for r in new))}
out["listing"] = {"total_now": len(isrs), "total_2026_11_14": len(old_isrs), "total_run10": len(run10_isrs),
                  "status_counts_now": dict(Counter(r.get("status") for r in isrs)),
                  "growth_vs_2026_11_14": growth(old_ids, old_isrs),
                  "growth_vs_run10": growth(run10_ids, run10_isrs)}

# ---------------- cohort standing ----------------
lb_rows = []
for uid, r in cur_ext.items():
    row = {"userId": uid, "name": r.get("userName"), "rank": r.get("_rank_calc"), "coins": round(r.get("coins", 0), 1),
           "marathonWins": r.get("marathonWinsCount"), "appearances_of_5": appear[uid],
           "ranks": {label: (ext_snaps[label][uid].get("_rank_calc") if uid in ext_snaps[label] else None) for label, _ in snaps},
           "coins_by_snap": {label: (round(ext_snaps[label][uid].get("coins", 0), 1) if uid in ext_snaps[label] else None) for label, _ in snaps},
           "delta_vs_run10": (round(r.get("coins", 0) - ext_snaps["2026-11-17 02:37"][uid].get("coins", 0), 1) if uid in ext_snaps["2026-11-17 02:37"] else None),
           "delta_vs_2026_11_14_1037": (round(r.get("coins", 0) - ext_snaps["2026-11-14 10:37"][uid].get("coins", 0), 1) if uid in ext_snaps["2026-11-14 10:37"] else None)}
    lb_rows.append(row)
lb_rows.sort(key=lambda x: x["rank"])
out["leaderboard"] = {"floor_top100_external": min(r["coins"] for r in lb_rows) if lb_rows else None,
                      "floor_run10": 1819, "agents_ge400": sum(1 for r in lb_rows if r["coins"] >= 400),
                      "top20": lb_rows[:20], "climbers_vs_run10_ge300": [r for r in lb_rows if (r["delta_vs_run10"] or 0) >= 300]}
core_ids = [r["userId"] for r in lb_rows if r["appearances_of_5"] >= 4 and r["userId"] in ext_snaps["2026-11-17 02:37"]]
out["cohort_core_ids_ordered"] = core_ids
newcomer_consistent = [r for r in lb_rows if r["userId"] not in ext_snaps["2026-11-14 02:40"] and r["userId"] not in ext_snaps["2026-11-14 10:37"]
                       and r["userId"] in ext_snaps["2026-11-16 18:37"] and r["userId"] in ext_snaps["2026-11-17 02:37"]]
out["newcomers_consistent"] = newcomer_consistent
out["new_since_run10"] = [r for r in lb_rows if r["userId"] not in ext_snaps["2026-11-17 02:37"]]
# old guard: run2 top15 external + old panel status now
run2_top15 = sorted(ext_snaps["2026-11-14 10:37"].values(), key=lambda r: r["_rank_calc"])[:15]
out["old_top15_status"] = [{"name": r.get("userName"), "rank_2026_11_14": r.get("_rank_calc"), "coins_2026_11_14": round(r.get("coins", 0), 1),
                            "rank_now": (cur_ext[r["userId"]].get("_rank_calc") if r["userId"] in cur_ext else None),
                            "coins_now": (round(cur_ext[r["userId"]].get("coins", 0), 1) if r["userId"] in cur_ext else None)} for r in run2_top15]
name_to_uids = defaultdict(list)
for label, _ in snaps:
    for uid, r in ext_snaps[label].items():
        if r.get("userName") in OLD_PANEL and uid not in name_to_uids[r.get("userName")]: name_to_uids[r.get("userName")].append(uid)
out["old_panel_status"] = {}
for nm in OLD_PANEL:
    rows = []
    for uid in name_to_uids.get(nm, []):
        rows.append({"userId": uid, "rank_now": (cur_ext[uid].get("_rank_calc") if uid in cur_ext else None),
                     "coins_now": (round(cur_ext[uid].get("coins", 0), 1) if uid in cur_ext else None),
                     "appearances_of_5": appear[uid]})
    out["old_panel_status"][nm] = rows

# ---------------- verdict / discriminator frames ----------------
def readable(rows): return [r for r in rows if answer_text(r)]
panel_rows = readable([r for r in ext if "panel" in r["tag"]])
all_rows = readable(ext)
out["discriminator_panel48"] = gate_table([r for r in panel_rows if r["status"] == "verified"], [r for r in panel_rows if r["status"] == "falsified"])
out["discriminator_allframe"] = gate_table([r for r in all_rows if r["status"] == "verified"], [r for r in all_rows if r["status"] == "falsified"])

# verdict rates all-frame
by_auth = defaultdict(lambda: {"v": 0, "f": 0})
for r in ext:
    if r["status"] == "verified": by_auth[r["author"]]["v"] += 1
    elif r["status"] == "falsified": by_auth[r["author"]]["f"] += 1
rates = [a["v"]/(a["v"]+a["f"]) for a in by_auth.values() if a["v"]+a["f"] >= 5]
tv = sum(a["v"] for a in by_auth.values()); tf = sum(a["f"] for a in by_auth.values())
out["verdict_rates"] = {"agents_ge5": len(rates), "median": med(rates), "q1": quant(rates, .25), "q3": quant(rates, .75),
                        "pooled_pct": pct(tv, tv+tf), "pooled_v": tv, "pooled_f": tf}

# ---------------- cohort corpus ----------------
ver_by_author = Counter(r["author"] for r in ext if r["status"] == "verified" and answer_text(r))
chosen = []
for uid in core_ids:
    if ver_by_author.get(uid, 0) >= 10:
        chosen.append(uid)
    if len(chosen) >= 12: break
if len(chosen) < 12:
    for uid in core_ids:
        if uid not in chosen and ver_by_author.get(uid, 0) >= 5:
            chosen.append(uid)
        if len(chosen) >= 12: break
out["cohort_chosen"] = [{"userId": u, "name": names.get(u), "rank": cur_ext[u].get("_rank_calc"),
                         "coins": round(cur_ext[u].get("coins", 0), 1), "appearances_of_5": appear[u],
                         "verified_in_frame": ver_by_author.get(u, 0)} for u in chosen]
chosen_set = set(chosen)
cohort_v = [r for r in ext if r["author"] in chosen_set and r["status"] == "verified" and answer_text(r)]
cohort_f = [r for r in ext if r["author"] in chosen_set and r["status"] == "falsified" and answer_text(r)]
out["corpus_cohort"] = {"verified": feature_summary(cohort_v), "falsified": feature_summary(cohort_f),
                        "gates": gate_table(cohort_v, cohort_f)}
per_agent = {}
for uid in chosen:
    v = [r for r in cohort_v if r["author"] == uid]; f = [r for r in cohort_f if r["author"] == uid]
    sv = feature_summary(v); sf = feature_summary(f)
    per_agent[names.get(uid)] = {"n_v": len(v), "n_f": len(f), "verified": sv, "falsified": sf,
                                 "slots": dict(Counter(slot_label(r) for r in v))}
out["corpus_per_agent"] = per_agent
out["corpus_slots_cohort"] = {lab: feature_summary([r for r in cohort_v if slot_label(r) == lab]) for lab in ["P", "M", "P+M", "—"]}

# newly settled paid winners (updatedAt >= run10 start)
new_paid = []
for r in ext:
    if r["status"] != "verified" or not answer_text(r): continue
    if (ts_ms(r.get("updatedAt")) or 0) < CUT_RUN10: continue
    lab = slot_label(r)
    if lab != "—": new_paid.append(r)
out["new_paid_winners"] = {"n": len(new_paid), "by_slot": dict(Counter(slot_label(r) for r in new_paid)),
                           "by_agent": Counter((names.get(r["author"]) or ("uid:"+r["author"][:8])) for r in new_paid).most_common(15),
                           "features": feature_summary(new_paid),
                           "features_by_slot": {lab: feature_summary([r for r in new_paid if slot_label(r) == lab]) for lab in ["P", "M", "P+M"]}}
combined = {r["id"]: r for r in cohort_v}
for r in new_paid: combined[r["id"]] = r
out["corpus_combined_recipe"] = feature_summary(list(combined.values()))
out["combined_n_note"] = {"cohort_verified": len(cohort_v), "new_paid": len(new_paid), "combined_unique": len(combined)}

# marathon / pioneer headline stats
out["marathon_sample"] = {"questions_with_detail": len([d for d in det_by.values() if isinstance(d, dict)]),
                          "awarded_total": len(awarded_rows),
                          "awarded_external": sum(1 for a in awarded_rows if next((r["author"] for r in records if r["id"] == a["iso"]), None) not in house_ids),
                          "per_question_mean_all_sample": round(len(awarded_rows)/max(1, len(det_by)), 2),
                          "top_winners": Counter((names.get(next((r["author"] for r in records if r["id"] == a["iso"]), None)) or "author-not-in-sample") for a in awarded_rows).most_common(10),
                          "rules_versions": dict(Counter(str(d.get("arenaRulesVersion")) for d in det_by.values() if isinstance(d, dict)))}
lat_ext = []
for qid in isos_by:
    lst = isos_by.get(qid)
    if not isinstance(lst, list): continue
    ver = [i for i in lst if i.get("status") == "verified"]
    qq = qmap.get(qid, {})
    if not ver or not qq.get("timestamp"): continue
    first = sorted(ver, key=lambda i: ts_ms(i.get("timestamp")) or 0)[0]
    if first.get("author") in house_ids or is_ours(first): continue
    if (ts_ms(first.get("timestamp")) or 0) and qq.get("timestamp"):
        lat_ext.append(((ts_ms(first.get("timestamp")) - qq["timestamp"]) / 1000.0))
fresh_lat = []
for qid in isos_by:
    lst = isos_by.get(qid)
    if not isinstance(lst, list): continue
    qq = qmap.get(qid, {})
    if (qq.get("timestamp") or 0) < CUT_RUN10: continue
    ver = [i for i in lst if i.get("status") == "verified"]
    if not ver: continue
    first = sorted(ver, key=lambda i: ts_ms(i.get("timestamp")) or 0)[0]
    if first.get("author") in house_ids or is_ours(first): continue
    if ts_ms(first.get("timestamp")) and qq.get("timestamp"):
        fresh_lat.append(((ts_ms(first.get("timestamp")) - qq["timestamp"]) / 1000.0))
out["pioneer_latency"] = {"all_sample_external": {"n": len(lat_ext), "median_s": med(lat_ext)},
                           "fresh_since_run10_external": {"n": len(fresh_lat), "median_s": med(fresh_lat),
                                                          "sub10s": sum(1 for x in fresh_lat if x < 10), "gt10s": sum(1 for x in fresh_lat if x >= 10)}}
sc = Counter(r.get("status") for r in records)
out["abandoned_share_pct"] = pct(sc.get("abandoned", 0), len(records))

# row-level appendix data for KORPUS
def row_out(r):
    f = F(r)
    return {"agent": (names.get(r["author"]) or ("uid:"+r["author"][:8])), "iso": r["id"][:8], "isr": r["qid"][:8], "chars": f["chars"],
            "urls": f["url_count"], "density": f["density"], "ratio": f["ratio"], "slot": slot_label(r),
            "k1": "L" if f["k1"] else "G", "f030": "L" if f["floor030"] else "G", "f015": "L" if f["floor015"] else "G",
            "updatedAt": r.get("updatedAt")}
out["appendix_cohort_verified"] = [row_out(r) for r in sorted(cohort_v, key=lambda r: (names.get(r["author"]) or "", r["id"]))]
out["appendix_new_paid"] = [row_out(r) for r in sorted(new_paid, key=lambda r: (names.get(r["author"]) or "", r["id"]))]

print(json.dumps({"sample": out["meta"]["sample"], "listing": out["listing"], "chosen": out["cohort_chosen"],
                  "corpus_cohort_n": {"v": len(cohort_v), "f": len(cohort_f)}, "new_paid_n": len(new_paid)}, ensure_ascii=False, indent=1))
with open(f"{D}/analysis11.json", "w") as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
print("WROTE analysis11.json")
