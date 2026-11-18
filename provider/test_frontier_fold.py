#!/usr/bin/env python3
"""Tests for the FRONTIER FOLD (2026-11-18, F-31D;
SINTESIS-FRONTIER-PERBAIKAN-JALUR1 — duck + gpt-5.6-sol
convergent 4/4) applied to vyce_serve_prepare / freshness_gate /
doctrine_a:

Q2 RECONSIDERATION (the part this layer owns): a row passed over
while unclassified / TUNGGU / not-yet-due is decided FRESH from
its current classification when presented again — this layer
never caches a pass. Proven by: pass-while-unclassified ->
classify TELAT (already due) -> re-present -> prepared;
TUNGGU pass -> +30 min re-decision lands TELAT due -> prepared.
Every decision lands in the doctrine decision log with its
reason class, and doctrine_a.count_lost_after_skip counts
exactly the tickets that expired un-proceeded in their window.

Q3 TATA CARA: the pre-claim screen's verdict and the send-time
veto's verdict land in the SAME freshness log, told apart by
phase ("pra-klaim" vs "detik-kirim"), each carrying its reasons
— a divergence between them is readable from the log itself.

Q4 CLAIM SEQUENCING: while a previous job of this Expert is not
in a terminal state, prepare holds the row BEFORE generation
(generator never called) and records the hold; an unreadable
job list holds too; all-terminal proceeds; "disabled" (launcher
never armed fetching) leaves the gate inactive.

No network (fake fetchers everywhere), no serve launched.
"""
import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMP = tempfile.mkdtemp(prefix="frontier-fold-test-")
os.environ["DIALECTICA_TRIGGER_STORE"] = os.path.join(
    TMP, "trigger-store.json")
os.environ["DIALECTICA_LATE_QUEUE"] = os.path.join(
    TMP, "late-queue.json")
os.environ["DIALECTICA_LANE_BUDGET"] = os.path.join(
    TMP, "lane-budget.json")
os.environ["DIALECTICA_DOCTRINE_LOG"] = os.path.join(
    TMP, "doctrine-decision-log.jsonl")
os.environ["DIALECTICA_SERVE_CACHE_DIR"] = os.path.join(TMP, "cache")
os.environ["DIALECTICA_FRESHNESS_LOG"] = os.path.join(
    TMP, "freshness-log.jsonl")
os.environ.pop("DIALECTICA_FRESHNESS_MODE", None)  # block default

import doctrine_a as da  # noqa: E402
import freshness_gate as fg  # noqa: E402
import vyce_serve_prepare as prep  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name} :: {detail}")


NOWF = time.time()
LIVE_DET = {"status": "in_progress", "visoCount": 0, "isoCount": 0,
            "marathonActive": False, "marathonConcluded": False,
            "marathonEligibleIsos": []}
fake_result = {"sendable": True, "text": "jawaban siap",
               "report": {"chars_final": 12}, "gate": {"reasons": []}}
called = {"pipe": 0}
_orig_pipe = prep.vsc.vyce_pipeline


def counting_pipe(*a, **k):
    called["pipe"] += 1
    return fake_result


def row(isr_id, viso=0):
    return {"id": isr_id, "title": "Wallet?",
            "content": "isi wallet", "questionVisoCount": viso}


def no_jobs():
    return [], "ok"


def det_ok(_i):
    return LIVE_DET, "ok"


def isos_ok(_i):
    return [{"status": "revealed"}] * 3, "ok"


prep.vsc.vyce_pipeline = counting_pipe
try:
    # ============================ Q2: reconsideration =========
    # (1) passed while UNCLASSIFIED, classified TELAT (due) in
    # the meantime -> re-presentation is decided from the NEW
    # classification and prepares. This layer cached nothing.
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-recon"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=no_jobs)
    check("Q2: tak terklasifikasi -> dilewati (fail-closed)",
          rc == 1 and "TIDAK terklasifikasi" in line
          and called["pipe"] == before, line)
    da.record_classification("isr-recon", "TELAT", 40,
                             NOWF - 3 * 3600, now=NOWF)
    rc, line = prep.prepare_row(
        row("isr-recon"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=no_jobs)
    check("Q2: sesudah terklasifikasi TELAT + jatuh tempo, "
          "penyajian ulang DIPUTUS ULANG -> disiapkan",
          rc == 0 and called["pipe"] == before + 1, line)

    # (2) TUNGGU pass -> the +30 min re-decision rewrites the
    # record to TELAT -> prepare proceeds. (The observer's own
    # re-decision machinery is what rewrites it in production;
    # here the record rewrite itself is the seam under test.)
    da.record_classification("isr-wait", "TUNGGU", 8,
                             NOWF - 3 * 3600, now=NOWF - 1800)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-wait"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=no_jobs)
    check("Q2: mode TUNGGU -> dilewati",
          rc == 1 and "TUNGGU" in line and called["pipe"] == before,
          line)
    da.record_classification("isr-wait", "TELAT", 8,
                             NOWF - 3 * 3600, now=NOWF)
    rc, line = prep.prepare_row(
        row("isr-wait"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=no_jobs)
    check("Q2: TUNGGU yang diputus ulang jadi TELAT due -> "
          "disiapkan pada penyajian berikut",
          rc == 0 and called["pipe"] == before + 1, line)

    # (3) the decision log carries both passes + the proceeds,
    # with reason classes — the raw material of the Q2 measure.
    decisions = da.load_decisions()
    seq = [(d["isr_id"], d["decision"], d["reason_class"])
           for d in decisions if d["isr_id"] in
           ("isr-recon", "isr-wait")]
    check("Q2: log keputusan memuat pass(unclassified) -> "
          "proceed(due) dan pass(wait) -> proceed(due)",
          ("isr-recon", "pass", "unclassified") in seq
          and ("isr-recon", "proceed", "due") in seq
          and ("isr-wait", "pass", "wait") in seq
          and ("isr-wait", "proceed", "due") in seq, str(seq))

    # (4) count_lost_after_skip: fixture join — one ticket
    # passed while unclassified, parked, expired, never
    # proceeded in-window = lost; the proceeded one is not;
    # a still-parked one is not lost YET.
    fix_decisions = [
        {"ts": 1000, "isr_id": "lost-1", "decision": "pass",
         "reason_class": "unclassified"},
        {"ts": 1000, "isr_id": "won-1", "decision": "pass",
         "reason_class": "not_due"},
        {"ts": 9000, "isr_id": "won-1", "decision": "proceed",
         "reason_class": "due"},
        {"ts": 1000, "isr_id": "parked-1", "decision": "pass",
         "reason_class": "wait"},
    ]
    fix_entries = [
        {"isr_id": "lost-1", "state": "expired",
         "release_at": 8000, "expires_at": 22000},
        {"isr_id": "won-1", "state": "expired",
         "release_at": 8000, "expires_at": 22000},
        {"isr_id": "parked-1", "state": "parked",
         "release_at": 8000, "expires_at": 22000},
    ]
    lost = da.count_lost_after_skip(decisions=fix_decisions,
                                    entries=fix_entries)
    check("Q2: hitungan tiket hilang pasca-skip = tepat 1 "
          "(lost-1; won-1 ter-proceed, parked-1 belum hilang)",
          lost == {"count": 1, "ids": ["lost-1"]}, str(lost))

    # ============================ Q3: phase-tagged log ========
    log_path = os.environ["DIALECTICA_FRESHNESS_LOG"]
    with open(log_path, encoding="utf-8") as fh:
        records = [json.loads(x) for x in fh if x.strip()]
    screen_recs = [r for r in records
                   if r.get("phase") == "pra-klaim"]
    check("Q3: vonis layar pra-klaim tercatat di log kesegaran "
          "dengan phase=pra-klaim + alasan",
          len(screen_recs) >= 1
          and all("reasons" in r for r in screen_recs),
          str([r.get("phase") for r in records]))
    # The send-time veto over the SAME prepared question: quiet
    # at pick, crowded by send time — the divergence the log
    # must be able to tell. Direct check with the veto's phase.
    pick = fg.pick_state_from_row(row("isr-diverge", viso=0),
                                  isos=[{"status": "revealed"}] * 3,
                                  now=NOWF, lane="CEPAT")
    det79 = dict(LIVE_DET, isoCount=79)
    v = fg.check_freshness(
        "isr-diverge", pick_state=pick,
        detail_fetcher=lambda _i: (det79, "ok"),
        isos_fetcher=lambda _i: ([{"status": "revealed"}] * 79, "ok"),
        now=NOWF + 600, doctrine=True, phase="detik-kirim")
    with open(log_path, encoding="utf-8") as fh:
        records = [json.loads(x) for x in fh if x.strip()]
    send_recs = [r for r in records
                 if r.get("isr_id") == "isr-diverge"
                 and r.get("phase") == "detik-kirim"]
    check("Q3: vonis detik-kirim tercatat di log yang sama, "
          "phase=detik-kirim, menahan dengan alasannya sendiri "
          "(divergensi terbaca dari log)",
          v["withhold"] and len(send_recs) == 1
          and bool(send_recs[0]["reasons"])
          and send_recs[0]["status"] == "stale",
          str(send_recs))

    # ============================ Q4: sequencing gate =========
    da.record_classification("isr-seq", "CEPAT", 2,
                             NOWF - 300, now=NOWF)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-seq"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=lambda: ([{"id": "job-1",
                                "jobStatus": "assigned"}], "ok"))
    check("Q4: job sebelumnya 'assigned' (belum terminal) -> "
          "klaim DITAHAN sebelum generasi",
          rc == 1 and "sekuensing" in line
          and called["pipe"] == before, line)
    decisions = da.load_decisions()
    check("Q4: tahan sekuensing tercatat di log keputusan",
          any(d["isr_id"] == "isr-seq" and d["decision"] == "hold"
              and d["reason_class"] == "job_sequence"
              for d in decisions), str(decisions[-3:]))
    rc, line = prep.prepare_row(
        row("isr-seq"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=lambda: (None, "failed"))
    check("Q4: daftar jobs tak terbaca -> DITAHAN juga "
          "(belum terminal-pasti)",
          rc == 1 and "sekuensing" in line
          and called["pipe"] == before, line)
    rc, line = prep.prepare_row(
        row("isr-seq"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=lambda: ([{"id": "job-0",
                                "jobStatus": "completed"},
                               {"id": "job-9",
                                "jobStatus": "abandoned"}], "ok"))
    check("Q4: semua job terminal -> jalan terus, disiapkan",
          rc == 0 and called["pipe"] == before + 1, line)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-seq"), detail_fetcher=det_ok,
        isos_fetcher=isos_ok, doctrine=True, now=NOWF,
        jobs_fetcher=lambda: (None, "disabled"))
    check("Q4: fetching tak ter-arm (disabled) -> gerbang "
          "nonaktif, disiapkan seperti biasa",
          rc == 0 and called["pipe"] == before + 1, line)
finally:
    prep.vsc.vyce_pipeline = _orig_pipe

print(f"\nALL PASS ({CHECKS[0]}/{CHECKS[0]})" if not FAILURES else
      f"\nFAILURES: {len(FAILURES)}/{CHECKS[0]}: {FAILURES}")
sys.exit(1 if FAILURES else 0)
