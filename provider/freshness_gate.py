#!/usr/bin/env python3
"""Send-time freshness re-check for the gated Vyce serve lane
(built 2026-11-17 — ATURAN KETAT user 2026-11-17 10:50 as clarified
10:52, SISTEM-KENDALI: "VERIFIKASI TUGAS").

THE GAP THIS CLOSES. The picker (target_picker.py) classifies the
paying cell and serve_gate's liveness gate proves the round alive —
both at PICK time. Generation then takes minutes, and until now
NOTHING re-read the question before the answer left for the server.
The 2026-11-17 pilot fired 5 answers picked at viso 0 whose
questions flooded to 23–59 answers behind them, unchecked. Two
measured losses follow from submitting into a filled room (user
10:52): (1) falsified exposure — the novelty space the answer was
written for is already closed by earlier answers; (2) wasted work —
even a verified answer pays $0 once the paying slot (Pioneer
verified-first, +20) has been taken by someone else.

WHAT THE GATE DOES. Installed in vyce_serve_provider.py at BOTH
points where an answer is about to be printed for submission
(prepared-cache hit and live fallback), it re-reads the question's
LIVE state — ISR detail + ISO list, through the client's own
endpoints (serve_gate.fetch_isr_detail / novelty_context.fetch_isos,
the same seams the liveness gate and the novelty context already
use) — and applies per-class withhold rules:

- state unreadable (fetch failed / disabled / malformed)
    -> "unverified": WITHHOLD in block mode. The strict rule is
       explicit: unverified is NOT a pass (this deliberately
       differs from fallback_dead_reason, whose job-time semantics
       spare an accepted job on an unverifiable fetch — freshness
       is a pre-submit veto, and the user's rule overrides).
- question proven closed on the fresh detail (serve_gate
  .liveness_check MATI: settled, stale-flag marathon, concluded)
    -> "closed": WITHHOLD.
- PIONEER (picked at viso 0 — verified-first slot, +20):
    verified_now >= 1  -> slot dead, WITHHOLD.
    crowd_now >= CROWD_CAP -> novelty room closed, WITHHOLD.
- MARATHON (paid slots are plural; measured mean 5.85 awarded
  slots per concluded panel question, STUDI-KOHORT-2026-11-17 F4):
    verified_now >= VERIFIED_FULL_CAP (6) -> the question already
    carries at least the average paid-slot complement, WITHHOLD.
    (Crowding alone does NOT withhold a Marathon: cohort winners
    enter crowded rounds, median entry rank ~5, prime band up to
    15 — the binding constraints are the slot count and the round
    still being open, which the closed rule above covers.)
- INNOVATOR / GENERAL / unknown class (conservative, per the
  user's rule): verified_now >= VERIFIED_FULL_CAP -> WITHHOLD
  (verified-full); crowd_now >= CROWD_CAP -> WITHHOLD.

THRESHOLD GROUNDS (from our own field data — see
GERBANG-KESEGARAN-2026-11-17.md):
- CROWD_CAP = 20 competing answers (revealed + verified).
  Initial calibration was 10: the picker's own novelty model,
  novelty_room(viso) = 0.95 − 0.08·viso, reaches its NO-PAY floor
  (ROOM_FLOOR 0.15) at viso 10. RAISED 10 -> 20 by USER DECISION
  2026-11-17 11:57 ("AMBIL RESIKO" — take the risk): 20 is the
  upper band of the cohort winners' entry positions, and the
  novelty risk below this line is now consciously accepted by
  the user rather than withheld against.
- VERIFIED_FULL_CAP = 6 = ceil(5.85), the measured mean number of
  paid Marathon slots per concluded panel question (46 questions,
  STUDI-KOHORT F4).

DEFINITIONS. verified_now = max(detail visoCount, ISO-list count
of status "verified") — the detail counter and the list are both
read; the larger wins (conservative, and the ISO list is known to
truncate on giant questions, STUDI-KOHORT F4). crowd_now = ISO-list
count of status "revealed" + "verified" (live competitors; intent
is not an answer yet, abandoned is withdrawn, falsified is settled
— all three are logged in the status counts for audit).

PICK STATE. Class and baselines come from pick time, not send
time: vyce_serve_prepare records a sidecar
(serve-cache/<isr_id>.fresh.json: target_class, viso_at_pick,
answers_at_pick, picked_at) next to the prepared answer. Without
a sidecar (fallback arrivals) the class is GENERAL — the
conservative rule set — and no baseline is claimed.

ARMING + MODE (same pattern as C5 / citation verify): the stage
exists only when the launcher sets DIALECTICA_FRESHNESS_CHECK=1
(run_serve does, gated Vyce serve). Mode from
DIALECTICA_FRESHNESS_MODE: "shadow" logs and NEVER withholds;
anything else (including unset) is "block" — the default for this
layer, per the strict rule. A crash of the check callable itself
never withholds but is logged as a "crash" record (mirrors the
serve_gate doctrine for checker stages); that is distinct from an
unreadable question state, which is data and DOES withhold.

Every check appends one record to freshness-check-log.jsonl
(DIALECTICA_FRESHNESS_LOG overrides the path — the test seam).
Network behaviour: exactly two client reads per check, no retries
of its own (the client's call() has its own discipline), no loops.
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_serve_common as csc  # noqa: E402  (serve cache dir)
import doctrine_a  # noqa: E402  (Doktrin A lane awareness, 2026-11-18)
import novelty_context  # noqa: E402  (fetch_isos seam)
import serve_gate  # noqa: E402  (fetch_isr_detail, liveness_check)

FRESHNESS_ARM_ENV = "DIALECTICA_FRESHNESS_CHECK"
FRESHNESS_MODE_ENV = "DIALECTICA_FRESHNESS_MODE"
FRESHNESS_LOG_ENV = "DIALECTICA_FRESHNESS_LOG"
FRESHNESS_LOG = os.path.join(HERE, "freshness-check-log.jsonl")
SIDECAR_SUFFIX = ".fresh.json"

# ------------------------------------------------------- thresholds
PIONEER_VERIFIED_DEAD = 1     # the verified-first slot itself
VERIFIED_FULL_CAP = 6         # ceil(5.85) — STUDI-KOHORT-2026-11-17 F4
CROWD_CAP = 20                # user decision 2026-11-17 11:57 "AMBIL
                              # RESIKO" (was 10, picker novelty_room
                              # floor line 0.15); 20 = upper band of
                              # cohort winners' entry positions

_LOG_DEFAULT = object()


def freshness_mode():
    """DIALECTICA_FRESHNESS_MODE: "shadow" = log-only, never
    withholds; anything else (including unset) is "block" — the
    accepted default for this layer (aturan ketat 2026-11-17)."""
    return "shadow" if os.environ.get(
        FRESHNESS_MODE_ENV, "").strip().lower() == "shadow" else "block"


def _log_path():
    return os.environ.get(FRESHNESS_LOG_ENV) or FRESHNESS_LOG


def _freshness_log(record, log_path):
    path = _log_path() if log_path is _LOG_DEFAULT else log_path
    if path is None:
        return
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass  # the log is evidence, never a reason to break a send


# --------------------------------------------------------- pick state

def sidecar_path(isr_id):
    return os.path.join(csc.cache_dir(), f"{isr_id}{SIDECAR_SUFFIX}")


def record_pick_state(isr_id, state):
    """Persist the pick-time state next to the prepared answer.
    Best-effort by design: a failed write degrades the send-time
    check to the conservative GENERAL rules, never breaks prepare.
    Returns True when written."""
    if not isr_id or not isinstance(state, dict):
        return False
    try:
        os.makedirs(csc.cache_dir(), exist_ok=True)
        with open(sidecar_path(isr_id), "w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False)
        return True
    except OSError:
        return False


def read_pick_state(isr_id):
    """The recorded pick state, or None (missing/corrupt). Never
    raises — an unreadable sidecar is a missing baseline, and the
    check falls back to the conservative class rules."""
    if not isr_id:
        return None
    try:
        with open(sidecar_path(isr_id), encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        return None
    return state if isinstance(state, dict) else None


def _marathon_open(detail, now=None):
    """A marathon round provably open on this detail (an eligible
    endsAt in the future) — target_picker.marathon_open semantics
    over the same fields, kept local so this module's import graph
    stays on the serve seams it already uses."""
    now = time.time() if now is None else now
    ends = []
    for entry in (detail or {}).get("marathonEligibleIsos") or []:
        if isinstance(entry, dict):
            ts = serve_gate.parse_ts(entry.get("endsAt"))
            if ts is not None:
                ends.append(ts)
    return bool(ends) and max(ends) > now


def derive_class(viso_at_pick, marathon_open):
    """The picker's cell logic without its value/topic layers:
    viso 0 is the Pioneer cell; a provably open marathon round on
    a non-empty question is the Marathon cell; everything else is
    GENERAL (the conservative rule set — an Innovator pick is
    judged by these rules too, since the serve pipe carries no
    novelty measurement to distinguish it)."""
    if viso_at_pick == 0:
        return "PIONEER"
    if marathon_open:
        return "MARATHON"
    return "GENERAL"


def pick_state_from_row(row, isos=None, now=None, lane=None):
    """Build the pick-state record from a prepare-time search row
    (+ the pick-time ISO list when the caller fetched one).
    Pure assembly; every field that cannot be known is None, never
    invented. `lane` (Doktrin A, 2026-11-18) records the entry lane
    the trigger assigned — CEPAT / TELAT — when the caller knows
    it; the send-time check only honours it while the doctrine is
    armed (see check_freshness)."""
    row = row or {}
    viso = row.get("questionVisoCount", row.get("visoCount"))
    try:
        viso = int(viso) if viso is not None else None
    except (TypeError, ValueError):
        viso = None
    detail = serve_gate.row_liveness_detail(row)
    answers = None
    verified = None
    if isinstance(isos, list):
        counts = Counter(
            str(iso.get("status") or "") for iso in isos
            if isinstance(iso, dict))
        answers = counts.get("revealed", 0) + counts.get("verified", 0)
        verified = counts.get("verified", 0)
    return {
        "isr_id": csc.row_isr_id(row),
        "picked_at": time.time() if now is None else now,
        "target_class": derive_class(viso, _marathon_open(detail, now)),
        "viso_at_pick": viso,
        "verified_at_pick": verified,
        "answers_at_pick": answers,
        "lane": lane,
    }


# --------------------------------------------------------- live state

def state_from_payloads(detail, isos):
    """Flat live-state counts from the two payloads. verified_now
    takes the LARGER of the detail counter and the ISO-list count
    (the list truncates on giant questions — conservative wins);
    crowd_now counts live competitors on the list."""
    counts = Counter(
        str(iso.get("status") or "") for iso in (isos or [])
        if isinstance(iso, dict))
    verified_list = counts.get("verified", 0)
    verified_detail = (detail or {}).get("visoCount")
    try:
        verified_detail = int(verified_detail) \
            if verified_detail is not None else None
    except (TypeError, ValueError):
        verified_detail = None
    verified_now = max(verified_list, verified_detail or 0)
    iso_total = (detail or {}).get("isoCount")
    try:
        iso_total = int(iso_total) if iso_total is not None else None
    except (TypeError, ValueError):
        iso_total = None
    return {
        "verified_now": verified_now,
        "verified_list": verified_list,
        "verified_detail": verified_detail,
        "crowd_now": counts.get("revealed", 0) + verified_list,
        "iso_list_len": len(isos or []),
        "iso_total_detail": iso_total,
        "status_counts": dict(counts),
        "question_status": str((detail or {}).get("status") or ""),
    }


# ------------------------------------------------------------- the check

def check_freshness(isr_id, pick_state=None, detail_fetcher=None,
                    isos_fetcher=None, now=None, mode=None,
                    log_path=_LOG_DEFAULT, doctrine=None, phase=None):
    """One send-time freshness verdict for `isr_id`. Returns the
    verdict dict (also appended to the freshness log):

    {isr_id, ts, class, lane, mode, phase, status, withhold,
     reasons, pick, live, fetch} — status is "fresh" (no rule fired),
    "stale" (a withhold rule fired), "closed" (the question is
    proven closed on the fresh detail), or "unverified" (the live
    state could not be read). `withhold` already has the mode
    applied: shadow mode never withholds.

    DOKTRIN A LANE AWARENESS (2026-11-18, keputusan user 08:23
    Opsi A; only while DIALECTICA_DOCTRINE_A=1 — `doctrine`
    overrides for tests): the per-class vetoes below are PIONEER
    logic — they judge a room by whether the verified-first slot
    and the novelty space survive. A TELAT-lane entry (parked
    2–6 h, written against the answers already there, aimed at
    the marathon selection + Innovator cells) enters a crowded
    room BY DESIGN: existing verified and a crowd of 26–60+ are
    its normal state (the marathon tail), never a withhold. What
    still withholds a TELAT send is exactly what withholds every
    lane and comes BEFORE the class rules below: an unreadable
    state ("unverified") and a question proven closed on the
    fresh detail ("closed"). The closed rule is liveness_check
    semantics, which is precisely the study's line: settled does
    NOT freeze a question (its revealed pool keeps converting
    ±7%/30 h through the periodic channel — STUDI-ANTREAN-
    VERDICT Q3), so a settled question whose marathon round is
    provably still open (a future endsAt) is LIVE and sendable;
    a settled/concluded question with no future round
    (marathonConcluded, no endsAt ahead) has no channel left for
    a NEW late entrant — the tail conversion belongs to answers
    already in the pool — and withholds as closed. A CEPAT-lane
    pick (and any pick without a lane) is judged by the class
    rules exactly as before this layer existed.

    Fetchers are the test seam: callables isr_id -> (payload,
    state) with state "ok"/"failed"/"disabled", exactly the
    serve_gate.fetch_isr_detail / novelty_context.fetch_isos
    contract.

    `phase` (FRONTIER FOLD 2026-11-18, Q3 tata cara): the same
    rule code is evaluated TWICE per sendable row — once at
    pick time as the pre-claim screen (phase "pra-klaim",
    vyce_serve_prepare) and once at send time as the veto
    (phase "detik-kirim", armed_freshness_veto below). Both
    verdicts land in THIS log, told apart by `phase`, each
    carrying its own reasons — a divergence between the two
    records of one ISR is a normal race over a changing room
    (the room filled during generation), readable from the log
    itself, never a silent disagreement."""
    now = time.time() if now is None else now
    mode = mode or freshness_mode()
    det_fetcher = detail_fetcher or serve_gate.fetch_isr_detail
    iso_fetcher = isos_fetcher or novelty_context.fetch_isos
    pick = pick_state if isinstance(pick_state, dict) else None
    cls = str((pick or {}).get("target_class") or "GENERAL").upper()
    if cls not in ("PIONEER", "MARATHON", "INNOVATOR", "GENERAL"):
        cls = "GENERAL"
    if doctrine is None:
        doctrine = doctrine_a.doctrine_armed()
    lane = str((pick or {}).get("lane") or "").upper() or None
    if lane not in (doctrine_a.LANE_FAST, doctrine_a.LANE_LATE):
        lane = None
    late_lane = bool(doctrine) and lane == doctrine_a.LANE_LATE
    verdict = {
        "isr_id": isr_id, "ts": now, "class": cls, "lane": lane,
        "doctrine": bool(doctrine), "mode": mode, "phase": phase,
        "status": "unverified", "withhold": False, "reasons": [],
        "pick": pick, "live": None,
        "fetch": {"detail": None, "isos": None},
    }
    detail, d_state = det_fetcher(isr_id)
    isos, i_state = iso_fetcher(isr_id)
    verdict["fetch"] = {"detail": d_state, "isos": i_state}
    if d_state != "ok" or i_state != "ok" or not isinstance(detail, dict) \
            or not isinstance(isos, list):
        verdict["reasons"].append(
            f"keadaan live pertanyaan tidak terbaca (detail={d_state}, "
            f"isos={i_state}) — kesegaran TAK terverifikasi; aturan "
            f"ketat: tak terverifikasi bukan lolos")
        verdict["withhold"] = mode == "block"
        _freshness_log(verdict, log_path)
        return verdict
    live = state_from_payloads(detail, isos)
    verdict["live"] = live
    ok, live_reason = serve_gate.liveness_check(detail, now=now)
    live["liveness_ok"] = ok
    live["liveness_reason"] = live_reason
    if not ok:
        verdict["status"] = "closed"
        verdict["reasons"].append(
            f"pertanyaan terbukti TUTUP pada bacaan segar: {live_reason}")
        verdict["withhold"] = mode == "block"
        _freshness_log(verdict, log_path)
        return verdict
    verified = live["verified_now"]
    crowd = live["crowd_now"]
    if late_lane:
        # TELAT lane (Doktrin A): the room being full IS the entry
        # condition — verified >= 1 and crowd 26–60+ are the
        # marathon tail this lane was parked for, so NO per-class
        # veto applies. Unreadable state and proven closure have
        # already withheld above, exactly as for every lane.
        verdict["status"] = "fresh"
        verdict["reasons"] = []
        verdict["withhold"] = False
        _freshness_log(verdict, log_path)
        return verdict
    if cls == "PIONEER":
        if verified >= PIONEER_VERIFIED_DEAD:
            verdict["reasons"].append(
                f"PIONEER: verified sudah ada {verified} — slot "
                f"verified-pertama (+20) sudah direbut; verified kita "
                f"pun bayar $0 (slot mati)")
        if crowd >= CROWD_CAP:
            verdict["reasons"].append(
                f"PIONEER: kerumunan {crowd} jawaban hidup "
                f"(>= garis {CROWD_CAP} = pita atas posisi masuk "
                f"pemenang kohort; garis risiko keputusan user "
                f"2026-11-17 11:57) — ruang kebaruan yang dipilih "
                f"saat viso 0 sudah tertutup")
    elif cls == "MARATHON":
        if verified >= VERIFIED_FULL_CAP:
            verdict["reasons"].append(
                f"MARATHON: verified sudah {verified} — memenuhi/"
                f"melewati jatah slot wajar {VERIFIED_FULL_CAP} "
                f"(rerata terukur 5,85 slot/pertanyaan, STUDI-KOHORT "
                f"F4); slot bayar realistis habis")
    else:  # INNOVATOR / GENERAL — conservative shared rules
        if verified >= VERIFIED_FULL_CAP:
            verdict["reasons"].append(
                f"{cls}: verified sudah {verified} — pertanyaan "
                f"verified-penuh (garis konservatif {VERIFIED_FULL_CAP}"
                f" = jatah slot wajar terukur); verified biasa $0")
        if crowd >= CROWD_CAP:
            verdict["reasons"].append(
                f"{cls}: kerumunan {crowd} jawaban hidup "
                f"(>= garis {CROWD_CAP} = pita atas posisi masuk "
                f"pemenang kohort; garis risiko keputusan user "
                f"2026-11-17 11:57) — ruang kebaruan tertutup")
    verdict["status"] = "stale" if verdict["reasons"] else "fresh"
    verdict["withhold"] = bool(verdict["reasons"]) and mode == "block"
    _freshness_log(verdict, log_path)
    return verdict


def armed_freshness_veto(isr_id):
    """The provider-hook seam, or None when the launcher has not
    armed the gate (DIALECTICA_FRESHNESS_CHECK=1 — run_serve sets
    this for the gated Vyce serve). The returned callable takes no
    arguments and returns (withhold, reason): it reads the pick
    sidecar and runs the check. A crash of the check itself is
    logged as a "crash" record and does NOT withhold (checker
    doctrine, mirroring serve_gate's stages) — an unreadable
    question state is not a crash and withholds inside the check."""
    if os.environ.get(FRESHNESS_ARM_ENV) != "1":
        return None

    def _veto():
        try:
            verdict = check_freshness(
                isr_id, pick_state=read_pick_state(isr_id),
                phase="detik-kirim")
        except Exception as ex:  # noqa: BLE001 - a crashed checker
            # must never kill a good send; it reports itself loudly.
            _freshness_log({
                "isr_id": isr_id, "ts": time.time(), "class": None,
                "mode": freshness_mode(), "phase": "detik-kirim",
                "status": "crash",
                "withhold": False,
                "reasons": [f"gerbang kesegaran crash: "
                            f"{type(ex).__name__}: {ex}"],
                "pick": None, "live": None, "fetch": None},
                _LOG_DEFAULT)
            return False, (f"gerbang kesegaran crash "
                           f"({type(ex).__name__}: {ex}) — tercatat, "
                           f"tidak menahan")
        if verdict["withhold"]:
            return True, "; ".join(verdict["reasons"])
        return False, (f"kesegaran {verdict['status']} "
                       f"(kelas {verdict['class']}, mode "
                       f"{verdict['mode']})")
    return _veto
