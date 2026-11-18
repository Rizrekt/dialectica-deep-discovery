#!/usr/bin/env python3
"""Tests for the send-time freshness gate (freshness_gate.py,
built 2026-11-17 per ATURAN KETAT user 10:50/10:52).

Proves, WITHOUT any real network (deterministic fake fetchers are
injected everywhere) and WITHOUT launching any serve:

- FRESH PASSES: a Pioneer pick still at verified 0 / small crowd
  passes; a Marathon pick with slots open and the round open
  passes (crowding alone does not withhold a Marathon).
- SLOT DEATH: Pioneer with verified >= 1 withholds (the +20
  verified-first slot is taken); the detail visoCount wins over a
  truncated ISO list (conservative max).
- CROWD: Pioneer / GENERAL at >= CROWD_CAP live answers withholds.
- VERIFIED-FULL: Marathon and GENERAL at >= VERIFIED_FULL_CAP
  verified withhold.
- CLOSED: a question proven closed on the fresh detail (stale-flag
  marathon, settled) withholds with status "closed".
- UNREADABLE STATE: a failed detail or isos fetch withholds in
  block mode with status "unverified" (tak terverifikasi bukan
  lolos); in shadow mode nothing ever withholds.
- CRASH DOCTRINE: a crashing check callable never withholds
  through the armed veto, and the crash is logged.
- ARMING: the veto exists only under DIALECTICA_FRESHNESS_CHECK=1;
  the layer's mode default is "block", shadow only when set.
- PICK STATE: sidecar round-trip; class derivation (viso 0 ->
  PIONEER, open marathon -> MARATHON, else GENERAL); prepare_row
  records a sidecar next to a sendable cache entry.
- PROVIDER WIRING: with the veto armed and withholding, the Vyce
  provider's cache-hit path exits 1 with EMPTY stdout; with a
  passing veto it serves the cached answer exactly as before.
"""
import io
import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import freshness_gate as fg  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}  {detail}")


TMP = tempfile.mkdtemp(prefix="freshgate-test-")
LOG = os.path.join(TMP, "freshness-log.jsonl")
os.environ["DIALECTICA_FRESHNESS_LOG"] = LOG
os.environ["DIALECTICA_SERVE_CACHE_DIR"] = os.path.join(TMP, "cache")

FUTURE = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600))
PAST = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3600))


def detail(status="in_progress", viso=0, iso_count=None, marathon=False,
           ends=None):
    return {
        "status": status, "visoCount": viso, "isoCount": iso_count,
        "marathonActive": marathon, "marathonConcluded": False,
        "marathonEligibleIsos": [{"endsAt": e} for e in (ends or [])],
    }


def isos(**status_counts):
    out = []
    for status, n in status_counts.items():
        out.extend({"status": status} for _ in range(n))
    return out


def fetchers(det, iso_list):
    return (lambda _id: (det, "ok")), (lambda _id: (iso_list, "ok"))


def run(isr, pick, det, iso_list, mode="block"):
    df, isf = fetchers(det, iso_list)
    return fg.check_freshness(isr, pick_state=pick, detail_fetcher=df,
                              isos_fetcher=isf, mode=mode)


PIONEER_PICK = {"target_class": "PIONEER", "viso_at_pick": 0,
                "answers_at_pick": 0, "verified_at_pick": 0}
MARATHON_PICK = {"target_class": "MARATHON", "viso_at_pick": 2,
                 "answers_at_pick": 4, "verified_at_pick": 2}
GENERAL_PICK = {"target_class": "GENERAL", "viso_at_pick": 3,
                "answers_at_pick": 5, "verified_at_pick": 3}

# ---------------------------------------------------------- fresh passes
v = run("isr-fresh-p", PIONEER_PICK, detail(viso=0), isos(revealed=3))
check("pioneer segar lolos", v["status"] == "fresh" and not v["withhold"],
      str(v["reasons"]))
v = run("isr-fresh-m", MARATHON_PICK,
        detail(viso=3, marathon=True, ends=[FUTURE]),
        isos(revealed=17, verified=3))
check("marathon rame tapi slot terbuka lolos",
      v["status"] == "fresh" and not v["withhold"], str(v["reasons"]))
v = run("isr-fresh-g", GENERAL_PICK, detail(viso=2), isos(revealed=4,
                                                          verified=2))
check("general segar lolos", v["status"] == "fresh" and not v["withhold"],
      str(v["reasons"]))

# ---------------------------------------------------------- slot death
v = run("isr-slotdead", PIONEER_PICK, detail(viso=1),
        isos(revealed=2, verified=1))
check("pioneer verified>=1 DITAHAN (slot mati)",
      v["withhold"] and v["status"] == "stale"
      and any("slot" in r for r in v["reasons"]), str(v["reasons"]))
v = run("isr-slotdead2", PIONEER_PICK, detail(viso=1),
        isos(revealed=5))
check("pioneer: penghitung detail menang atas daftar terpotong",
      v["withhold"] and v["live"]["verified_now"] == 1,
      str(v["live"]))

# ---------------------------------------------------------- crowd
# Garis kerumunan = 20 sejak keputusan user 2026-11-17 11:57
# ("AMBIL RESIKO"; sebelumnya 10). Semantik >= garis: 19 lolos,
# 20 tahan, 21 tahan.
v = run("isr-crowd-p", PIONEER_PICK, detail(viso=0), isos(revealed=23))
check("pioneer kerumunan 23 DITAHAN", v["withhold"]
      and any("kerumunan" in r for r in v["reasons"]), str(v["reasons"]))
v = run("isr-crowd-edge-lo", PIONEER_PICK, detail(viso=0),
        isos(revealed=19))
check("pioneer kerumunan 19 (di bawah garis 20) lolos",
      not v["withhold"] and v["status"] == "fresh", str(v["reasons"]))
v = run("isr-crowd-edge-at", PIONEER_PICK, detail(viso=0),
        isos(revealed=20))
check("pioneer kerumunan 20 (persis garis) DITAHAN",
      v["withhold"] and any("kerumunan" in r for r in v["reasons"]),
      str(v["reasons"]))
v = run("isr-crowd-edge-hi", PIONEER_PICK, detail(viso=0),
        isos(revealed=21))
check("pioneer kerumunan 21 (di atas garis) DITAHAN",
      v["withhold"] and any("kerumunan" in r for r in v["reasons"]),
      str(v["reasons"]))
v = run("isr-crowd-g", GENERAL_PICK, detail(viso=2),
        isos(revealed=18, verified=2))
check("general kerumunan 20 DITAHAN", v["withhold"], str(v["reasons"]))
v = run("isr-crowd-g-lo", GENERAL_PICK, detail(viso=2),
        isos(revealed=10, verified=2))
check("general kerumunan 12 lolos di garis risiko baru",
      not v["withhold"] and v["status"] == "fresh", str(v["reasons"]))

# ---------------------------------------------------------- verified-full
v = run("isr-full-m", MARATHON_PICK,
        detail(viso=6, marathon=True, ends=[FUTURE]),
        isos(revealed=9, verified=6))
check("marathon verified 6 DITAHAN (jatah slot penuh)",
      v["withhold"] and any("jatah slot" in r for r in v["reasons"]),
      str(v["reasons"]))
v = run("isr-full-g", GENERAL_PICK, detail(viso=7),
        isos(revealed=3, verified=7))
check("general verified 7 DITAHAN (verified-penuh)",
      v["withhold"], str(v["reasons"]))
v = run("isr-full-edge", MARATHON_PICK,
        detail(viso=5, marathon=True, ends=[FUTURE]),
        isos(revealed=8, verified=5))
check("marathon verified 5 (di bawah garis) lolos",
      not v["withhold"], str(v["reasons"]))

# ---------------------------------------------------------- closed
v = run("isr-closed-stale", MARATHON_PICK,
        detail(viso=2, marathon=True, ends=[PAST]),
        isos(revealed=4, verified=2))
check("ronde terbukti tutup (flag basi) DITAHAN status closed",
      v["withhold"] and v["status"] == "closed", str(v["reasons"]))
v = run("isr-closed-settled", PIONEER_PICK, detail(status="settled"),
        isos(revealed=1))
check("pertanyaan settled DITAHAN status closed",
      v["withhold"] and v["status"] == "closed", str(v["reasons"]))

# ---------------------------------------------------------- unreadable
df_fail = lambda _id: (None, "failed")  # noqa: E731
_, isf_ok = fetchers(detail(), isos(revealed=1))
v = fg.check_freshness("isr-unread-det", pick_state=PIONEER_PICK,
                       detail_fetcher=df_fail, isos_fetcher=isf_ok,
                       mode="block")
check("detail gagal dibaca -> unverified + DITAHAN (block)",
      v["status"] == "unverified" and v["withhold"], str(v["reasons"]))
v = fg.check_freshness("isr-unread-det", pick_state=PIONEER_PICK,
                       detail_fetcher=df_fail, isos_fetcher=isf_ok,
                       mode="shadow")
check("detail gagal dibaca -> unverified, shadow TIDAK menahan",
      v["status"] == "unverified" and not v["withhold"], str(v["reasons"]))
df_ok, _ = fetchers(detail(), isos())
isf_fail = lambda _id: (None, "failed")  # noqa: E731
v = fg.check_freshness("isr-unread-iso", pick_state=PIONEER_PICK,
                       detail_fetcher=df_ok, isos_fetcher=isf_fail,
                       mode="block")
check("isos gagal dibaca -> unverified + DITAHAN (block)",
      v["status"] == "unverified" and v["withhold"], str(v["reasons"]))
v = run("isr-shadow-stale", PIONEER_PICK, detail(viso=1),
        isos(verified=1), mode="shadow")
check("shadow: stale tercatat tapi TIDAK menahan",
      v["status"] == "stale" and not v["withhold"], str(v["reasons"]))

# ---------------------------------------------------------- mode + arming
os.environ.pop("DIALECTICA_FRESHNESS_MODE", None)
check("mode bawaan = block", fg.freshness_mode() == "block")
os.environ["DIALECTICA_FRESHNESS_MODE"] = "shadow"
check("mode shadow terbaca", fg.freshness_mode() == "shadow")
os.environ.pop("DIALECTICA_FRESHNESS_MODE", None)
os.environ.pop("DIALECTICA_FRESHNESS_CHECK", None)
check("veto None saat tidak di-arm", fg.armed_freshness_veto("x") is None)
os.environ["DIALECTICA_FRESHNESS_CHECK"] = "1"
check("veto ada saat di-arm", fg.armed_freshness_veto("x") is not None)

# ---------------------------------------------------------- crash doctrine
_orig_check = fg.check_freshness


def _boom(*_a, **_k):
    raise RuntimeError("ledakan uji")


fg.check_freshness = _boom
try:
    veto = fg.armed_freshness_veto("isr-crash")
    w, why = veto()
finally:
    fg.check_freshness = _orig_check
check("crash callable TIDAK menahan", w is False and "crash" in why, why)
with open(LOG, encoding="utf-8") as fh:
    records = [json.loads(line) for line in fh if line.strip()]
check("crash tercatat di log",
      any(r.get("status") == "crash" for r in records))
check("setiap cek tercatat di log",
      any(r.get("isr_id") == "isr-fresh-p" for r in records)
      and any(r.get("isr_id") == "isr-slotdead" for r in records))

# ---------------------------------------------------------- pick state
check("derive_class viso 0 -> PIONEER",
      fg.derive_class(0, False) == "PIONEER")
check("derive_class maraton terbuka -> MARATHON",
      fg.derive_class(2, True) == "MARATHON")
check("derive_class lain -> GENERAL", fg.derive_class(3, False) == "GENERAL")
state = fg.pick_state_from_row(
    {"id": "isr-pick", "questionVisoCount": 0}, isos=isos(revealed=1))
check("pick_state_from_row: kelas+baseline",
      state["target_class"] == "PIONEER" and state["viso_at_pick"] == 0
      and state["answers_at_pick"] == 1, str(state))
check("record_pick_state menulis", fg.record_pick_state("isr-pick", state))
back = fg.read_pick_state("isr-pick")
check("sidecar round-trip", back is not None
      and back["target_class"] == "PIONEER", str(back))
check("sidecar hilang -> None (jujur)",
      fg.read_pick_state("isr-tidak-ada") is None)

# ------------------------------------------- prepare records the sidecar
import vyce_serve_prepare as prep  # noqa: E402

row = {"id": "isr-prep", "title": "Tentang wallet dan oracle?",
       "content": "Pertanyaan uji", "questionVisoCount": 0}
fake_result = {"sendable": True, "text": "jawaban siap",
               "report": {"chars_final": 12}, "gate": {"reasons": []}}
_orig_pipe = prep.vsc.vyce_pipeline
prep.vsc.vyce_pipeline = lambda *a, **k: fake_result
try:
    rc, _line = prep.prepare_row(
        row,
        detail_fetcher=lambda _id: (detail(viso=0), "ok"),
        isos_fetcher=lambda _id: (isos(revealed=0), "ok"))
finally:
    prep.vsc.vyce_pipeline = _orig_pipe
check("prepare_row lolos dengan pipeline palsu", rc == 0, _line)
side = fg.read_pick_state("isr-prep")
check("prepare_row mencatat sidecar kesegaran",
      side is not None and side["target_class"] == "PIONEER"
      and side["answers_at_pick"] == 0, str(side))

# ---------------------------------------------------------- provider wiring
import vyce_serve_provider as vsp  # noqa: E402
import cloudflare_serve_common as csc  # noqa: E402

csc.write_cache("isr-wire", "JAWABAN TERSIAP")
_orig_veto = fg.armed_freshness_veto
_orig_stdin, _orig_stdout = sys.stdin, sys.stdout
os.environ["DIALECTICA_ISR_ID"] = "isr-wire"
os.environ.pop("DIALECTICA_JOB_KIND", None)
try:
    fg.armed_freshness_veto = lambda _id: (lambda: (True, "slot mati uji"))
    sys.stdin, sys.stdout = io.StringIO(""), io.StringIO()
    rc = vsp.main()
    out = sys.stdout.getvalue()
    check("provider: veto menahan -> rc 1 + stdout KOSONG",
          rc == 1 and out == "", f"rc={rc} out={out!r}")
    fg.armed_freshness_veto = lambda _id: (lambda: (False, "segar uji"))
    sys.stdin, sys.stdout = io.StringIO(""), io.StringIO()
    rc = vsp.main()
    out = sys.stdout.getvalue()
    check("provider: veto lolos -> jawaban cache terkirim persis",
          rc == 0 and out == "JAWABAN TERSIAP\n", f"rc={rc} out={out!r}")
    fg.armed_freshness_veto = lambda _id: None
    sys.stdin, sys.stdout = io.StringIO(""), io.StringIO()
    rc = vsp.main()
    out = sys.stdout.getvalue()
    check("provider: tidak di-arm -> perilaku lama persis",
          rc == 0 and out == "JAWABAN TERSIAP\n", f"rc={rc} out={out!r}")
finally:
    fg.armed_freshness_veto = _orig_veto
    sys.stdin, sys.stdout = _orig_stdin, _orig_stdout
    os.environ.pop("DIALECTICA_ISR_ID", None)

print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)} "
      f"({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
sys.exit(1 if FAILURES else 0)
