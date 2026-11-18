#!/usr/bin/env python3
"""Tests for Doktrin A (doctrine_a.py + rate_trigger.py + the
lane-aware seams in freshness_gate / target_picker /
vyce_serve_prepare), built 2026-11-18 per keputusan user 08:23
"Opsi A — Campuran 7:3 berpemicu".

Proves, WITHOUT any network (fake fetchers everywhere) and
WITHOUT launching any serve:

- TRIGGER: first-2-min inflow counts classify CEPAT (<=5) /
  TUNGGU (6-10) / TELAT (>=11); the count is reconstructed
  exactly from ISO timestamps at any observation time.
- TUNGGU re-evaluation at +30 min: slow continuation + position
  <= 10 -> CEPAT; fast continuation -> TELAT; position > 10 ->
  TELAT.
- LATE QUEUE: park releases at birth+2 h, expires at birth+6 h;
  release builds the novelty ticket with the 0.15
  differentiation target; a spent entry cannot re-release.
- LANE BUDGET: CEPAT 3/day, TELAT 7/day (UTC day), never forced.
- FORBIDDEN ZONE: delay 2-120 min + position 11-60 + measured
  flood -> veto; every boundary outside it, and any unmeasured
  flood flag, does NOT fire.
- FRESHNESS LANE AWARENESS (doctrine armed): the SAME crowded
  live state withholds a GENERAL pick but passes a TELAT pick;
  TELAT still withholds on unreadable state and on proven
  closure (settled without a live round; concluded marathon);
  settled WITH a provably open round passes; with the doctrine
  OFF a TELAT sidecar is judged by the old rules (env gating).
- PICKER VETO: classify() marks the forbidden zone NO-PAY only
  while the doctrine is on and the flood flag is measured True.
- PREPARE GLUE: TELAT not-yet-due passes over unparked-cost-free;
  TELAT due prepares under the TELAT lane (sidecar carries it,
  queue entry released, budget taken); a spent CEPAT lane
  passes over; unclassified questions pass over FAIL-CLOSED
  while the doctrine is armed (pool-seam fix 2026-11-18 — the
  original "flow exactly as before" behaviour was the
  serve-vs-picker disconnect proven by mini-batch 3; the
  pre-claim freshness screen itself is covered by
  test_pool_seam.py).
"""
import datetime
import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMP = tempfile.mkdtemp(prefix="doctrine-test-")
os.environ["DIALECTICA_TRIGGER_STORE"] = os.path.join(
    TMP, "trigger-store.json")
os.environ["DIALECTICA_LATE_QUEUE"] = os.path.join(
    TMP, "late-queue.json")
os.environ["DIALECTICA_LANE_BUDGET"] = os.path.join(
    TMP, "lane-budget.json")
os.environ["DIALECTICA_SERVE_CACHE_DIR"] = os.path.join(TMP, "cache")
os.environ["DIALECTICA_FRESHNESS_LOG"] = os.path.join(
    TMP, "freshness-log.jsonl")
os.environ["DIALECTICA_DOCTRINE_LOG"] = os.path.join(
    TMP, "doctrine-decision-log.jsonl")

import doctrine_a as da  # noqa: E402
import freshness_gate as fg  # noqa: E402
import rate_trigger as rt  # noqa: E402
import target_picker as tp  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}  {detail}")


T0 = 1_763_000_000.0  # a fixed birth epoch (s)


def iso_list(birth, offsets_s):
    """ISO payloads born at birth+offset (timestamp in ms, the
    study's own field shape)."""
    return [{"id": f"iso-{i}", "status": "revealed",
             "timestamp": int((birth + off) * 1000)}
            for i, off in enumerate(offsets_s)]


# ------------------------------------------------------------- trigger
check("klasifikasi <=5 -> CEPAT",
      da.classify_inflow(0) == "CEPAT"
      and da.classify_inflow(5) == "CEPAT")
check("klasifikasi 6..10 -> TUNGGU",
      da.classify_inflow(6) == "TUNGGU"
      and da.classify_inflow(10) == "TUNGGU")
check("klasifikasi >=11 -> TELAT",
      da.classify_inflow(11) == "TELAT"
      and da.classify_inflow(35) == "TELAT")
check("count_in_window: tepi jendela [birth, birth+120)",
      da.count_in_window([T0, T0 + 119.9, T0 + 120, T0 - 1], T0) == 2)
check("flood hanya dari ukuran (>=11)",
      da.flood_classified(11) is True
      and da.flood_classified(10) is False
      and da.flood_classified(None) is False)

# Synthetic inflow series through the observer (fake fetcher).
SERIES = {
    "isr-sepi": iso_list(T0, [5, 40, 90]),                       # 3
    "isr-banjir": iso_list(T0, [i * 3 for i in range(35)]),      # 35
    "isr-abu": iso_list(T0, [10, 25, 40, 55, 70, 95]),           # 6
}
FEED = dict(SERIES)


def fake_fetch(isr_id):
    return FEED.get(isr_id, []), "ok"


rows = [{"id": k, "timestamp": int(T0 * 1000)} for k in SERIES]
store = {}
facts = rt.observe_once(rows, T0 + 60, fake_fetch, store)
modes = {r["isr_id"]: r["mode"] for r in facts["classified"]}
check("observer: sepi -> CEPAT", modes.get("isr-sepi") == "CEPAT",
      str(modes))
check("observer: banjir -> TELAT", modes.get("isr-banjir") == "TELAT")
check("observer: abu -> TUNGGU", modes.get("isr-abu") == "TUNGGU")
check("observer: lag penemuan tercatat (60 dtk)",
      all(r["discovery_lag_s"] == 60 for r in facts["classified"]))
q = da._queue()
check("observer: banjir diparkir di antrean telat",
      any(e["isr_id"] == "isr-banjir" and e["state"] == "parked"
          for e in q), str(q))

# TUNGGU re-evaluations at +30 min (three grey fates).
FEED["isr-abu"] = iso_list(T0, [10, 25, 40, 55, 70, 95, 600, 1200])
facts2 = rt.observe_once([], T0 + 60 + 1800, fake_fetch, store)
reev = {r["isr_id"]: r for r in facts2["reevaluated"]}
check("TUNGGU + laju lambat + posisi <=10 -> CEPAT",
      reev.get("isr-abu", {}).get("mode") == "CEPAT", str(reev))
check("TUNGGU fakta: posisi tercatat 9",
      reev.get("isr-abu", {}).get("wait_facts", {})
      .get("position_if_enter") == 9, str(reev))

mode, wf = da.reevaluate_wait(
    [T0 + o for o in [10, 25, 40, 55, 70, 95] + [200 + 20 * i
                                                  for i in range(60)]],
    T0, T0 + 1860)
check("TUNGGU + laju lanjutan >=2/mnt -> TELAT",
      mode == "TELAT" and wf["continuation_per_min"] >= 2.0, str(wf))
mode, wf = da.reevaluate_wait(
    [T0 + o for o in [10, 25, 40, 55, 70, 85, 100, 115]
     + [600, 900, 1200, 1500, 1700]], T0, T0 + 1860)
check("TUNGGU + posisi >10 -> TELAT walau laju lambat",
      mode == "TELAT" and wf["position_if_enter"] == 14
      and wf["continuation_per_min"] < 2.0, str(wf))

# ----------------------------------------------------------- late queue
entry = da.park("isr-q", T0, now=T0 + 600)
check("parkir: release birth+2j, expiry birth+6j",
      entry["release_at"] == T0 + 7200
      and entry["expires_at"] == T0 + 21600)
check("antrean: belum due di +1 jam",
      da.due_entries(now=T0 + 3600) == [] or all(
          e["isr_id"] != "isr-q" for e in da.due_entries(now=T0 + 3600)))
check("antrean: due tepat di +2 jam",
      any(e["isr_id"] == "isr-q" for e in da.due_entries(now=T0 + 7200)))
check("release sebelum due -> None",
      da.release("isr-q", now=T0 + 3600) is None)


def fake_isos_ctx(isr_id):
    return ([{"id": "v1", "status": "verified",
              "supportedCount": 3, "refutationCount": 0,
              "reveal": {"data": {"structured_data":
                                   {"answer": "jawaban lama"}}}}], "ok")


ticket = da.release("isr-q", now=T0 + 7200, isos_fetcher=fake_isos_ctx)
check("release: tiket lane TELAT + target diferensiasi 0,15",
      ticket is not None and ticket["lane"] == "TELAT"
      and ticket["differentiation_target"] == 0.15
      and ticket["delay_at_release_s"] == 7200, str(ticket))
check("release: konteks kebaruan terbangun dari jawaban lama",
      ticket is not None and ticket["novelty_meta"]["state"] == "ok")
check("release dua kali -> None (entri terkonsumsi)",
      da.release("isr-q", now=T0 + 7300) is None)
da.park("isr-exp", T0, now=T0)
swept = da.sweep_expired(now=T0 + 21601)
check("antrean: lewat 6 jam -> expired, bukan released",
      "isr-exp" in swept
      and da.release("isr-exp", now=T0 + 21700) is None)

# ---------------------------------------------------------- lane budget
NOWD = T0
check("jatah CEPAT: 3 token lalu habis",
      all(da.lane_take("CEPAT", now=NOWD) for _ in range(3))
      and da.lane_take("CEPAT", now=NOWD) is False
      and da.lane_remaining("CEPAT", now=NOWD) == 0)
check("jatah TELAT: 7 token lalu habis",
      all(da.lane_take("TELAT", now=NOWD) for _ in range(7))
      and da.lane_take("TELAT", now=NOWD) is False)
check("jatah reset hari UTC berikutnya",
      da.lane_take("CEPAT", now=NOWD + 86400) is True)

# -------------------------------------------------------- forbidden zone
check("zona terlarang: 30 mnt + posisi 30 + banjir -> VETO",
      da.forbidden_zone(1800, 30, True) is True)
check("zona terlarang: tepi 2 mnt/posisi 11 & 120 mnt/posisi 60",
      da.forbidden_zone(120, 11, True) is True
      and da.forbidden_zone(7200, 60, True) is True)
check("zona terlarang: di luar zona -> lolos",
      da.forbidden_zone(119, 30, True) is False
      and da.forbidden_zone(7201, 30, True) is False
      and da.forbidden_zone(1800, 10, True) is False
      and da.forbidden_zone(1800, 61, True) is False)
check("zona terlarang: banjir tak terukur -> TIDAK menembak",
      da.forbidden_zone(1800, 30, None) is False
      and da.forbidden_zone(1800, 30, False) is False
      and da.forbidden_zone(None, 30, True) is False)

# ------------------------------------------------ freshness lane-aware
NOWF = time.time()


def detail(status="in_progress", viso=3, elig=None, active=False,
           concluded=False):
    return {"status": status, "visoCount": viso,
            "marathonActive": active, "marathonConcluded": concluded,
            "marathonEligibleIsos": elig or [], "isoCount": 45}


def isos_payload(verified=3, revealed=42):
    return ([{"status": "verified"}] * verified
            + [{"status": "revealed"}] * revealed)


def verdict_for(pick, det, isos_l, doctrine=True):
    return fg.check_freshness(
        "isr-fresh", pick_state=pick,
        detail_fetcher=lambda _i: (det, "ok"),
        isos_fetcher=lambda _i: (isos_l, "ok"),
        now=NOWF, log_path=None, doctrine=doctrine)


crowd_det, crowd_isos = detail(), isos_payload()
v = verdict_for({"target_class": "GENERAL"}, crowd_det, crowd_isos)
check("kesegaran: GENERAL di kerumunan 45 -> ditahan (aturan lama)",
      v["withhold"] is True and v["status"] == "stale", str(v["reasons"]))
v = verdict_for({"target_class": "GENERAL", "lane": "TELAT"},
                crowd_det, crowd_isos)
check("kesegaran: TELAT di keadaan SAMA -> lolos (kerumunan normal)",
      v["withhold"] is False and v["status"] == "fresh"
      and v["lane"] == "TELAT", str(v))
v = verdict_for({"target_class": "GENERAL", "lane": "TELAT"},
                crowd_det, crowd_isos, doctrine=False)
check("kesegaran: doktrin MATI -> sidecar TELAT diadili aturan lama",
      v["withhold"] is True, str(v["reasons"]))
v = verdict_for({"target_class": "PIONEER", "lane": "CEPAT"},
                crowd_det, crowd_isos)
check("kesegaran: CEPAT/PIONEER verified>=1 -> ditahan (persis lama)",
      v["withhold"] is True
      and any("PIONEER" in r for r in v["reasons"]), str(v["reasons"]))
v = verdict_for({"target_class": "GENERAL", "lane": "TELAT"},
                detail(status="settled", viso=0), isos_payload(0, 5))
check("kesegaran: TELAT + settled tanpa ronde live -> closed ditahan",
      v["withhold"] is True and v["status"] == "closed", str(v))
future = datetime.datetime.fromtimestamp(
    NOWF + 3600, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
v = verdict_for({"target_class": "GENERAL", "lane": "TELAT"},
                detail(status="settled", viso=1,
                       elig=[{"endsAt": future}]),
                isos_payload(1, 5))
check("kesegaran: TELAT + settled TAPI ronde maraton terbukti buka "
      "-> lolos (settled tidak membekukan)",
      v["withhold"] is False and v["status"] == "fresh", str(v))
past = datetime.datetime.fromtimestamp(
    NOWF - 3600, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
v = verdict_for({"target_class": "GENERAL", "lane": "TELAT"},
                detail(elig=[{"endsAt": past}], concluded=True),
                isos_payload(1, 5))
check("kesegaran: TELAT + maraton concluded tanpa ronde depan "
      "-> closed ditahan",
      v["withhold"] is True and v["status"] == "closed", str(v))
v = fg.check_freshness(
    "isr-fresh", pick_state={"target_class": "GENERAL",
                             "lane": "TELAT"},
    detail_fetcher=lambda _i: (None, "failed"),
    isos_fetcher=lambda _i: (None, "failed"),
    now=NOWF, log_path=None, doctrine=True)
check("kesegaran: TELAT + keadaan tak terbaca -> ditahan (kedua lane)",
      v["withhold"] is True and v["status"] == "unverified", str(v))

# ------------------------------------------------------------ picker veto
ROW = {"id": "isr-zona", "title": "Wallet identity question",
       "content": "tentang wallet dan smart contract",
       "questionVisoCount": 5, "questionAgeMs": 1800_000}
DET = {"status": "in_progress", "marathonActive": False,
       "marathonConcluded": False, "marathonEligibleIsos": [],
       "isoCount": 29}
rec = tp.classify(ROW, detail=DET, now=NOWF, doctrine_a_on=True,
                  flood=True)
check("picker: zona terlarang -> NO-PAY + tanda FORBIDDEN",
      rec["cls"] == "NO-PAY" and rec.get("doctrine_zone") == "FORBIDDEN"
      and "ZONA TERLARANG" in rec["reason"], str(rec))
rec = tp.classify(ROW, detail=DET, now=NOWF, doctrine_a_on=True,
                  flood=None)
check("picker: banjir tak terukur -> zona unknown, kelas normal",
      rec["cls"] == "INNOVATOR"
      and rec.get("doctrine_zone") == "unknown", str(rec))
rec = tp.classify(ROW, detail=DET, now=NOWF, doctrine_a_on=False,
                  flood=True)
check("picker: doktrin mati -> veto diam, kelas persis lama",
      rec["cls"] == "INNOVATOR" and "doctrine_zone" not in rec,
      str(rec))
rec = tp.classify(dict(ROW, questionAgeMs=10800_000), detail=DET,
                  now=NOWF, doctrine_a_on=True, flood=True)
check("picker: banjir tapi tunda 3 jam -> di luar zona, lolos",
      rec["cls"] == "INNOVATOR"
      and rec.get("doctrine_zone") == "clear", str(rec))

# ----------------------------------------------------------- prepare glue
import vyce_serve_prepare as prep  # noqa: E402

LIVE_DET = {"status": "in_progress", "visoCount": 0,
            "marathonActive": False, "marathonConcluded": False,
            "marathonEligibleIsos": []}
fake_result = {"sendable": True, "text": "jawaban siap",
               "report": {"chars_final": 12}, "gate": {"reasons": []}}
called = {"pipe": 0}
_orig_pipe = prep.vsc.vyce_pipeline


def counting_pipe(*a, **k):
    called["pipe"] += 1
    return fake_result


prep.vsc.vyce_pipeline = counting_pipe
try:
    # TELAT classified 10 minutes ago — parked, not due.
    da.record_classification("isr-late-wait", "TELAT", 30,
                             NOWF - 600, now=NOWF)
    rc, line = prep.prepare_row(
        {"id": "isr-late-wait", "title": "Wallet?",
         "content": "isi wallet", "questionVisoCount": 4},
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"),
        doctrine=True, now=NOWF)
    check("prepare: TELAT belum due -> dilewati, generasi 0",
          rc == 1 and "diparkir" in line and called["pipe"] == 0,
          line)
    # TELAT born 3 h ago — due (release was at +2 h).
    da.record_classification("isr-late-due", "TELAT", 30,
                             NOWF - 3 * 3600, now=NOWF - 3 * 3600)
    rc, line = prep.prepare_row(
        {"id": "isr-late-due", "title": "Wallet?",
         "content": "isi wallet", "questionVisoCount": 9},
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"),
        doctrine=True, now=NOWF)
    check("prepare: TELAT due -> disiapkan di lane TELAT",
          rc == 0 and called["pipe"] == 1, line)
    side = fg.read_pick_state("isr-late-due")
    check("prepare: sidecar membawa lane TELAT",
          side is not None and side.get("lane") == "TELAT", str(side))
    q = da._queue()
    check("prepare: entri antrean TELAT due -> released",
          any(e["isr_id"] == "isr-late-due"
              and e["state"] == "released" for e in q), str(q))
    # CEPAT with a spent lane passes over.
    da.record_classification("isr-fast", "CEPAT", 2, NOWF - 60,
                             now=NOWF)
    for _ in range(3):
        da.lane_take("CEPAT", now=NOWF)
    rc, line = prep.prepare_row(
        {"id": "isr-fast", "title": "Wallet?",
         "content": "isi wallet", "questionVisoCount": 0},
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"),
        doctrine=True, now=NOWF)
    check("prepare: jatah CEPAT habis -> dilewati (tidak dipaksa)",
          rc == 1 and "jatah lane CEPAT" in line, line)
    # Unclassified under an armed doctrine: FAIL-CLOSED since
    # the 2026-11-18 pool-seam fix (PERBAIKAN-KOLAM-DOKTRIN).
    # The original glue let it flow as before; mini-batch 3
    # proved that behaviour IS the disconnect (12 unclassified
    # serve rows, 9 generations burned, 0 doctrine tickets
    # released). While the doctrine is armed, the doctrine
    # pool is the only pool. (The pre-seam expectation is kept
    # in test_doctrine_a.py.bak-20261118-poolfix.)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        {"id": "isr-plain", "title": "Wallet?",
         "content": "isi wallet", "questionVisoCount": 0},
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"),
        doctrine=True, now=NOWF)
    check("prepare: tanpa klasifikasi -> FAIL-CLOSED (jahitan kolam)",
          rc == 1 and "TIDAK terklasifikasi" in line
          and called["pipe"] == before, line)
    # Doctrine OFF: a TELAT-classified question is NOT parked away.
    rc, line = prep.prepare_row(
        {"id": "isr-late-wait", "title": "Wallet?",
         "content": "isi wallet", "questionVisoCount": 4},
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"),
        doctrine=False, now=NOWF)
    check("prepare: doktrin MATI -> klasifikasi diabaikan total",
          rc == 0, line)
finally:
    prep.vsc.vyce_pipeline = _orig_pipe

# ------------------------------------------------------------- arming
os.environ.pop("DIALECTICA_DOCTRINE_A", None)
check("arming: env tak terpasang -> doktrin mati",
      da.doctrine_armed() is False)
os.environ["DIALECTICA_DOCTRINE_A"] = "1"
check("arming: env =1 -> doktrin menyala", da.doctrine_armed() is True)
os.environ.pop("DIALECTICA_DOCTRINE_A", None)

print(f"\nALL PASS ({CHECKS[0]}/{CHECKS[0]})" if not FAILURES else
      f"\nFAILURES: {len(FAILURES)}/{CHECKS[0]}: {FAILURES}")
sys.exit(1 if FAILURES else 0)
