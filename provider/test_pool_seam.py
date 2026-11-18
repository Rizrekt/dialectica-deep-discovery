#!/usr/bin/env python3
"""Tests for the POOL SEAM fix (2026-11-18, PERBAIKAN-KOLAM-
DOKTRIN) in vyce_serve_prepare, built after mini-batch 3 proved
the serve-vs-picker pool disconnect (NYALA-DOKTRIN-A §6.1):

- FAIL-CLOSED POOL: while Doktrin A is armed, a row the rate
  observer never classified passes over at zero cost (before:
  it flowed into the legacy pipe and burned a generation —
  12/12 rows, 9 generations, 0 doctrine tickets released).
  With the doctrine OFF the same row flows exactly as before.
- PRE-CLAIM FRESHNESS SCREEN: the send-time freshness rules,
  run on the pick-time payloads BEFORE generation —
  * a CEPAT row picked at viso 0 whose crowd is ALREADY >= 20
    at pick (the a9408129 pattern: crowd 79 at pick, withheld
    in production only after its claim stranded the single
    concurrency slot ~30 min) passes over with the generator
    NEVER called;
  * the same CEPAT row with a quiet room prepares normally;
  * a DUE TELAT row in a big crowd is NOT withheld by the
    screen (TELAT lane semantics: the crowd is its entry
    condition) and prepares;
  * an unreadable pick-time state withholds (block mode) —
    at prepare a pass-over is free, so fail-closed costs
    nothing;
  * the sidecar records the SCREEN's pick state (one fetch,
    judged once), not a second fetch's.

No network (fake fetchers everywhere), no serve launched.
"""
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMP = tempfile.mkdtemp(prefix="pool-seam-test-")
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


def isos(revealed=0, verified=0):
    return ([{"status": "revealed"}] * revealed
            + [{"status": "verified"}] * verified)


def row(isr_id, viso=0):
    return {"id": isr_id, "title": "Wallet?",
            "content": "isi wallet", "questionVisoCount": viso}


prep.vsc.vyce_pipeline = counting_pipe
try:
    # ------------------------------------------ fail-closed pool
    rc, line = prep.prepare_row(
        row("isr-unclassified"), detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"), doctrine=True, now=NOWF)
    check("armed + tak terklasifikasi -> dilewati, generasi 0",
          rc == 1 and "TIDAK terklasifikasi" in line
          and called["pipe"] == 0, line)
    rc, line = prep.prepare_row(
        row("isr-unclassified"), detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: ([], "ok"), doctrine=False, now=NOWF)
    check("doktrin MATI + tak terklasifikasi -> alur lama persis",
          rc == 0 and called["pipe"] == 1, line)

    # --------------------------------- screen: crowded CEPAT pick
    da.record_classification("isr-fast-crowded", "CEPAT", 2,
                             NOWF - 300, now=NOWF)
    det79 = dict(LIVE_DET, isoCount=79)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-fast-crowded", viso=0),
        detail_fetcher=lambda _i: (det79, "ok"),
        isos_fetcher=lambda _i: (isos(revealed=79), "ok"),
        doctrine=True, now=NOWF)
    check("CEPAT viso 0 + kerumunan 79 saat pick -> layar PRA-KLAIM "
          "menahan, generasi 0 (pola a9408129)",
          rc == 1 and "PRA-KLAIM" in line and called["pipe"] == before,
          line)
    side = fg.read_pick_state("isr-fast-crowded")
    check("baris tertahan layar -> tidak ada sidecar/klaim",
          side is None, str(side))

    # ----------------------------------- screen: quiet CEPAT pick
    da.record_classification("isr-fast-quiet", "CEPAT", 2,
                             NOWF - 300, now=NOWF)
    rc, line = prep.prepare_row(
        row("isr-fast-quiet", viso=0),
        detail_fetcher=lambda _i: (LIVE_DET, "ok"),
        isos_fetcher=lambda _i: (isos(revealed=3), "ok"),
        doctrine=True, now=NOWF)
    check("CEPAT viso 0 + ruangan sepi -> disiapkan",
          rc == 0 and called["pipe"] == before + 1, line)
    side = fg.read_pick_state("isr-fast-quiet")
    check("sidecar = keadaan pick yang dinilai layar (answers 3)",
          side is not None and side.get("answers_at_pick") == 3
          and side.get("lane") == "CEPAT", str(side))

    # --------------------------- screen: TELAT due, crowded = lolos
    da.record_classification("isr-late-crowded", "TELAT", 40,
                             NOWF - 3 * 3600, now=NOWF - 3 * 3600)
    det40 = dict(LIVE_DET, visoCount=9, isoCount=49)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-late-crowded", viso=9),
        detail_fetcher=lambda _i: (det40, "ok"),
        isos_fetcher=lambda _i: (isos(revealed=40, verified=9), "ok"),
        doctrine=True, now=NOWF)
    check("TELAT due + kerumunan 49 -> layar TIDAK menahan "
          "(semantik lane), disiapkan",
          rc == 0 and called["pipe"] == before + 1, line)

    # ------------------------------ screen: unreadable state holds
    da.record_classification("isr-fast-unread", "CEPAT", 2,
                             NOWF - 300, now=NOWF)
    before = called["pipe"]
    rc, line = prep.prepare_row(
        row("isr-fast-unread", viso=0),
        detail_fetcher=lambda _i: (None, "failed"),
        isos_fetcher=lambda _i: (isos(revealed=1), "ok"),
        doctrine=True, now=NOWF)
    # NOTE: the liveness gate itself fails closed on a failed
    # detail fetch, so this row may be stopped there instead —
    # either way it must NOT reach generation.
    check("keadaan tak terbaca -> tidak sampai generasi",
          rc == 1 and called["pipe"] == before, line)
finally:
    prep.vsc.vyce_pipeline = _orig_pipe

print(f"\nALL PASS ({CHECKS[0]}/{CHECKS[0]})" if not FAILURES else
      f"\nFAILURES: {len(FAILURES)}/{CHECKS[0]}: {FAILURES}")
sys.exit(1 if FAILURES else 0)
