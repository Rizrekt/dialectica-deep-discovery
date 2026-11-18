#!/usr/bin/env python3
"""Read-only pull for STUDI-ANTREAN-VERDICT-2026-11-18.

Frame (dedup by ISR id):
- PILOT: 5 pilot ISRs of 2026-11-17 (our answers entered at position ~1).
- OLDSERVE: 14-Nov-era monitored ISRs holding our 22 still-revealed answers
  (prefix-resolved from today's listing, fallback run-11 listing).
- RUN11: overlap sample from run-11 (17 Nov) data -> 1-day status diff
  (settled-freeze test), 12 settled-panel + 12 fresh/monitored with >=8 ISOs.
- SETTLED: fresh stratified settled ISRs from today's listing by crowd
  bucket (small <=15, mid 16-40, large 41-80, giant >80), age >= 48h.
- INPROG: in_progress age 24-96h. FRESH: in_progress age < 24h.
Only trued.call GET endpoints. No platform writes; never prints session.
"""
import json, os, sys, time
from datetime import datetime, timezone
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

ROOT = "/home/hatch/workspace/research/dialectica"
OUT = f"{ROOT}/belajar-2026-11-18/antrean-verdict"
RUN11 = f"{ROOT}/belajar-2026-11-17/run11-0717"
os.makedirs(OUT, exist_ok=True)
NOW_MS = int(datetime.now(timezone.utc).timestamp() * 1000)

def call(path, params=None, tries=4):
    last = None
    for attempt in range(tries):
        try:
            return trued.call(path, params=params) if params is not None else trued.call(path)
        except (Exception, SystemExit) as ex:
            last = ex
            print(f"retry {attempt+1}/{tries} {path}: {ex}", flush=True)
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"API call failed after {tries} tries: {path}: {last}")

def save(name, obj):
    tmp = f"{OUT}/{name}.tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    os.replace(tmp, f"{OUT}/{name}")

save("pull_meta.json", {"started_at_utc": datetime.now(timezone.utc).isoformat(),
                        "now_ms": NOW_MS})

# ---------- listing ----------
isrs, offset = [], 0
while True:
    page = call("/api/node/isrs", params={"arenaId": "general", "offset": offset, "limit": 100})
    rows = page["isrs"]
    isrs.extend(rows)
    total = page["total"]
    if offset == 0:
        print("listing row keys:", sorted(rows[0].keys()) if rows else [], flush=True)
    offset += len(rows)
    print(f"listing offset={offset}/{total}", flush=True)
    if offset >= total or not rows:
        break
    time.sleep(0.15)
save("listing.json", {"total": total, "isrs": isrs})
by_id = {r["id"]: r for r in isrs}

def resolve_prefix(pfx):
    for r in isrs:
        if r["id"].startswith(pfx):
            return r["id"]
    return None

want = {}  # id -> tag
def add(qid, tag):
    if not qid:
        return
    want[qid] = (want[qid] + "+" + tag) if qid in want else tag

PILOT = ["2777178d-2294-4303-9b94-e877fdac95d0", "d94d7e34-01e1-44ef-9666-b0616980bc93",
         "635a010d-fa76-42a3-8ddf-c592e5189637", "d21135d5-5d4e-4a54-9da1-c54b4fc466f8",
         "5e905bef-7e0a-4b31-839c-d59a6688c70d"]
for q in PILOT:
    add(q, "pilot")

for pfx in ["60fa9935", "472b29a0", "71f472d6", "1287c2ae", "30fe9eea", "a361a16b", "3884b6c3"]:
    add(resolve_prefix(pfx), "oldserve")

# run-11 overlap
r11_isos = json.load(open(f"{RUN11}/isos_by_isr.json"))
r11_tags = json.load(open(f"{RUN11}/sample_tags.json"))
r11_det = json.load(open(f"{RUN11}/details_by_isr.json"))
settled11, other11 = [], []
for qid, tag in r11_tags.items():
    lst = r11_isos.get(qid)
    if not isinstance(lst, list) or len(lst) < 8:
        continue
    st = (r11_det.get(qid) or {}).get("status")
    (settled11 if st == "settled" else other11).append(qid)
for q in sorted(settled11)[:12]:
    add(q, "run11settled")
for q in sorted(other11)[:12]:
    add(q, "run11other")

def age_h(r):
    return (NOW_MS - (r.get("timestamp") or NOW_MS)) / 3600000.0

def crowd(r):
    return r.get("isoCount") or 0

settled = [r for r in isrs if r.get("status") == "settled" and age_h(r) >= 48]
buckets = {"small": [], "mid": [], "large": [], "giant": []}
for r in settled:
    c = crowd(r)
    if c <= 15: buckets["small"].append(r)
    elif c <= 40: buckets["mid"].append(r)
    elif c <= 80: buckets["large"].append(r)
    else: buckets["giant"].append(r)
for name, rows in buckets.items():
    rows_sorted = sorted(rows, key=lambda r: r.get("timestamp") or 0)
    # spread across ages: take evenly spaced
    picks = rows_sorted[:: max(1, len(rows_sorted) // 5)][:5] if rows_sorted else []
    for r in picks:
        add(r["id"], f"settled-{name}")
    print(f"bucket {name}: avail={len(rows)} picked={len(picks)}", flush=True)

inprog_mid = [r for r in isrs if r.get("status") == "in_progress" and 24 <= age_h(r) <= 96]
for r in sorted(inprog_mid, key=lambda r: r.get("timestamp") or 0)[:: max(1, len(inprog_mid) // 8)][:8]:
    add(r["id"], "inprog")
fresh = [r for r in isrs if r.get("status") == "in_progress" and age_h(r) < 24]
for r in sorted(fresh, key=lambda r: -(r.get("timestamp") or 0))[:8]:
    add(r["id"], "fresh")
print(f"sample size: {len(want)}", flush=True)
save("sample_tags.json", want)

# ---------- per-ISR detail + isos (incremental) ----------
det_path, iso_path = f"{OUT}/details_by_isr.json", f"{OUT}/isos_by_isr.json"
det_by = json.load(open(det_path)) if os.path.exists(det_path) else {}
iso_by = json.load(open(iso_path)) if os.path.exists(iso_path) else {}
errors = {}
for i, (qid, tag) in enumerate(sorted(want.items())):
    if qid in det_by and qid in iso_by:
        continue
    try:
        det_by[qid] = call(f"/api/node/isr/{qid}")
        time.sleep(0.3)
        iso_by[qid] = call(f"/api/node/isos/{qid}")["isos"]
    except Exception as ex:
        errors[qid] = str(ex)
        print(f"ERROR {qid}: {ex}", flush=True)
    save("details_by_isr.json", det_by)
    save("isos_by_isr.json", iso_by)
    print(f"[{i+1}/{len(want)}] {qid[:8]} tag={tag} isos={len(iso_by.get(qid) or [])}", flush=True)
    time.sleep(0.3)
save("errors.json", errors)
tot_iso = sum(len(v or []) for v in iso_by.values())
print(f"DONE isrs={len(iso_by)} isos={tot_iso} errors={len(errors)}", flush=True)
