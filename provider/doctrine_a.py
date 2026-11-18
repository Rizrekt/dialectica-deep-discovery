#!/usr/bin/env python3
"""DOKTRIN MASUK A — campuran 7:3 berpemicu (keputusan user
2026-11-18 08:23 "Opsi A", SISTEM-KENDALI entri "DOKTRIN MASUK
BARU DIADOPSI"). LAB implementation: this module is pure decision
machinery + small JSON state stores. It never claims, never
serves, never submits; serve stays STOP. Everything here is inert
unless the operator arms DIALECTICA_DOCTRINE_A=1.

THE DOCTRINE (measured grounds: STUDI-ANTREAN-VERDICT-2026-11-18,
66 ISR / 6.188 ISO; frontier consultation KONSULTASI-FRONTIER-
ANTREAN-2026-11-18, duck (c) + sol (b) convergent, gemini arbiter):

- The verdict probability of an answer is decided by the CROWD AT
  ENTRY and the question's era, not by depth or final size. In
  flood questions the first ~2 hours are a measured dead zone
  (delay 2–120 min + position 11–60 -> verdict chance 0.14–0.25);
  entering at delay 2–6 h recovers to ~0.50 via the marathon
  selection channel. In quiet questions, entering at position 1–3
  is the richest cell in the system (0.88–0.93, Pioneer +20).
- So the entry mode is decided PER QUESTION from the inflow rate
  of its first 2 minutes of life (answers with timestamp in
  [birth, birth+120s)):
      count <= 5   -> CEPAT  (fast lane, Pioneer; max 3/day)
      count 6..10  -> TUNGGU (grey zone; re-decided at +30 min)
      count >= 11  -> TELAT  (late lane; parked until delay 2–6 h,
                              entered with the novelty context of
                              the answers already there and a
                              differentiation target >= 15%;
                              7/day)
- TUNGGU re-evaluation at +30 min: continuation inflow after the
  first window < 2 answers/min AND our would-be position <= 10
  -> CEPAT; anything else -> TELAT.
- FORBIDDEN ZONE (hard veto, both lanes): delay 2–120 min AND
  position 11–60 in a flood-classified question — the exact cell
  the 2026-11-17 pilot died in. A question is "flood-classified"
  only by measurement (its first-2-min count >= 11, recorded by
  the rate trigger), never by guesswork: unknown classification
  means the veto cannot fire and the record says so.

DISCOVERY-LAG HONESTY. The trigger does NOT need to watch a
question from second 0: the first-2-minutes count is reconstructed
EXACTLY from the ISO list's own timestamps whenever the question
is first observed (the study measured floods from those same
timestamps). What discovery lag costs is decision TIME, not
classification accuracy — and the doctrine absorbs it: a CEPAT
verdict is still actionable while crowd-at-entry <= 10 (the
binding adopted constraint, SISTEM-KENDALI point 5), and a TELAT
verdict is parked for hours anyway. rate_trigger.py measures the
actual discovery lag of our polling feed and reports it.

STATE STORES (JSON files, paths overridable by env — test seams):
- trigger store  DIALECTICA_TRIGGER_STORE  (default HERE/
  trigger-store.json): isr_id -> classification record written by
  the rate trigger; read by the picker (flood flag) and prepare
  (lane lookup).
- late queue     DIALECTICA_LATE_QUEUE    (default HERE/
  late-queue.json): parked TELAT questions with release/expiry.
- lane budget    DIALECTICA_LANE_BUDGET   (default HERE/
  lane-budget.json): per-UTC-day lane token counts (the serve
  cap's own day boundary: UTC day = reset 07:00 WIB).

All store writes are best-effort atomic (tmp + rename); a corrupt
store reads as empty, never raises into a caller's path.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DOCTRINE_ENV = "DIALECTICA_DOCTRINE_A"
TRIGGER_STORE_ENV = "DIALECTICA_TRIGGER_STORE"
LATE_QUEUE_ENV = "DIALECTICA_LATE_QUEUE"
LANE_BUDGET_ENV = "DIALECTICA_LANE_BUDGET"
DECISION_LOG_ENV = "DIALECTICA_DOCTRINE_LOG"

LANE_FAST = "CEPAT"
LANE_LATE = "TELAT"
MODE_WAIT = "TUNGGU"

# ------------------------------------------------------- thresholds
FIRST_WINDOW_S = 120          # the doctrine's measurement window:
                              # answers in [birth, birth+120s)
FAST_MAX_FIRST = 5            # <=5 in the window -> CEPAT
FLOOD_MIN_FIRST = 11          # >=11 (>10) in the window -> TELAT /
                              # flood-classified; 6..10 -> TUNGGU
WAIT_REEVAL_S = 1800          # TUNGGU re-decided at +30 min
WAIT_MAX_CONT_PER_MIN = 2.0   # continuation rate must be < 2/min
WAIT_MAX_POSITION = 10        # ... and would-be position <= 10
LATE_MIN_DELAY_S = 7200       # late window opens at delay 2 h
LATE_MAX_DELAY_S = 21600      # ... and closes at delay 6 h
FAST_DAILY_CAP = 3            # lane allotments of the 10/day cap
LATE_DAILY_CAP = 7
FAST_MAX_CROWD_AT_ENTRY = 10  # binding CEPAT constraint (adopted
                              # doctrine point 5: crowd-at-entry
                              # <= 10 replaces the old viso rule)
DIFFERENTIATION_TARGET = 0.15  # Innovator novelty floor the late
                              # lane's entry is written against
FORBIDDEN_DELAY_MIN_S = 120   # hard-veto zone: delay 2–120 min ...
FORBIDDEN_DELAY_MAX_S = 7200
FORBIDDEN_POS_MIN = 11        # ... at position 11–60 ...
FORBIDDEN_POS_MAX = 60        # ... in a flood question


def doctrine_armed():
    """The whole doctrine layer exists only under the operator's
    explicit arming env; unset/other -> every consumer behaves
    exactly as before this module existed."""
    return os.environ.get(DOCTRINE_ENV) == "1"


# ------------------------------------------------------------ stores

def _store_path(env_name, default_name):
    return os.environ.get(env_name) or os.path.join(HERE, default_name)


def trigger_store_path():
    return _store_path(TRIGGER_STORE_ENV, "trigger-store.json")


def late_queue_path():
    return _store_path(LATE_QUEUE_ENV, "late-queue.json")


def lane_budget_path():
    return _store_path(LANE_BUDGET_ENV, "lane-budget.json")


def _read_json(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return default
    return data if isinstance(data, type(default)) else default


def _write_json(path, data):
    """Best-effort atomic write; returns True when written. A
    failed write never raises — doctrine state is advisory to the
    callers that gate on it, and they fail closed on absence."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        tmp = f"{path}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


# ------------------------------------------------- inflow measurement

def count_in_window(timestamps, birth_ts, window_s=FIRST_WINDOW_S):
    """Answers born in [birth, birth+window) — the doctrine's
    inflow count, reconstructed from the ISO list's own
    timestamps (exact at any observation time; see module
    docstring). Unparseable timestamps are skipped, never
    invented."""
    n = 0
    for ts in timestamps or []:
        if ts is None:
            continue
        if birth_ts <= ts < birth_ts + window_s:
            n += 1
    return n


def classify_inflow(first_count):
    """The trigger's three-way verdict on a first-window count."""
    if first_count is None:
        return None
    if first_count <= FAST_MAX_FIRST:
        return LANE_FAST
    if first_count >= FLOOD_MIN_FIRST:
        return LANE_LATE
    return MODE_WAIT


def flood_classified(first_count):
    """A question is flood-classified ONLY by this measurement
    (first-window count >= 11). Anything else — including an
    unmeasured question — is not flood, and the forbidden-zone
    veto must not pretend otherwise."""
    return first_count is not None and first_count >= FLOOD_MIN_FIRST


def reevaluate_wait(timestamps, birth_ts, now):
    """The +30-minute TUNGGU decision. Returns (mode, facts):
    CEPAT only when BOTH the continuation inflow after the first
    window ran < 2/min AND our would-be position (answers so far
    + 1) is <= 10; otherwise TELAT. `timestamps` are the ISO
    timestamps observed at re-evaluation time."""
    stamps = sorted(ts for ts in (timestamps or []) if ts is not None)
    after = [ts for ts in stamps
             if birth_ts + FIRST_WINDOW_S <= ts <= now]
    span_min = max((now - (birth_ts + FIRST_WINDOW_S)) / 60.0, 1e-9)
    cont_rate = len(after) / span_min
    position = len([ts for ts in stamps if ts <= now]) + 1
    facts = {"continuation_per_min": round(cont_rate, 3),
             "continuation_count": len(after),
             "position_if_enter": position}
    if cont_rate < WAIT_MAX_CONT_PER_MIN and position <= WAIT_MAX_POSITION:
        return LANE_FAST, facts
    return LANE_LATE, facts


def forbidden_zone(delay_s, position, flood):
    """The hard veto: delay 2–120 min AND position 11–60 AND the
    question flood-classified by measurement. `flood` must be
    True (a measured classification) — False/None never fires."""
    if flood is not True:
        return False
    if delay_s is None or position is None:
        return False
    return (FORBIDDEN_DELAY_MIN_S <= delay_s <= FORBIDDEN_DELAY_MAX_S
            and FORBIDDEN_POS_MIN <= position <= FORBIDDEN_POS_MAX)


# --------------------------------------------------- trigger store

def record_classification(isr_id, mode, first_count, birth_ts,
                          now=None, discovery_lag_s=None,
                          path=None):
    """Persist one trigger classification. Returns the record."""
    now = time.time() if now is None else now
    path = path or trigger_store_path()
    store = _read_json(path, {})
    rec = {
        "isr_id": isr_id, "mode": mode, "first2min": first_count,
        "flood": flood_classified(first_count),
        "birth_ts": birth_ts, "classified_at": now,
        "discovery_lag_s": discovery_lag_s,
    }
    store[isr_id] = rec
    _write_json(path, store)
    return rec


def load_trigger_store(path=None):
    return _read_json(path or trigger_store_path(), {})


def trigger_record(store, isr_id):
    rec = (store or {}).get(isr_id)
    return rec if isinstance(rec, dict) else None


def flood_flag(store, isr_id):
    """True / False from a measured classification, None when the
    question was never classified — the picker must distinguish
    'measured not-flood' from 'unknown' (veto honesty)."""
    rec = trigger_record(store, isr_id)
    if rec is None:
        return None
    return bool(rec.get("flood"))


# ------------------------------------------------------ late queue

def _queue(path=None):
    return _read_json(path or late_queue_path(), [])


def park(isr_id, birth_ts, now=None, path=None):
    """Park a TELAT question until its late window. Release is
    scheduled at birth + 2 h (the window's opening edge — the
    measured recovery band starts there); expiry at birth + 6 h
    (the adopted window's closing edge). Idempotent per ISR:
    re-parking an already-parked question returns the existing
    entry unchanged. Returns the entry."""
    now = time.time() if now is None else now
    path = path or late_queue_path()
    entries = _queue(path)
    for entry in entries:
        if entry.get("isr_id") == isr_id and \
                entry.get("state") == "parked":
            return entry
    entry = {
        "isr_id": isr_id, "birth_ts": birth_ts, "parked_at": now,
        "release_at": birth_ts + LATE_MIN_DELAY_S,
        "expires_at": birth_ts + LATE_MAX_DELAY_S,
        "state": "parked",
    }
    entries.append(entry)
    _write_json(path, entries)
    return entry


def due_entries(now=None, path=None):
    """Parked entries whose release time has arrived and whose
    window has not closed. Pure read — releasing is release()."""
    now = time.time() if now is None else now
    return [e for e in _queue(path)
            if e.get("state") == "parked"
            and e["release_at"] <= now <= e["expires_at"]]


def sweep_expired(now=None, path=None):
    """Mark parked entries past their window as expired (they are
    never silently released late). Returns the swept ids."""
    now = time.time() if now is None else now
    path = path or late_queue_path()
    entries = _queue(path)
    swept = []
    for entry in entries:
        if entry.get("state") == "parked" and now > entry["expires_at"]:
            entry["state"] = "expired"
            swept.append(entry["isr_id"])
    if swept:
        _write_json(path, entries)
    return swept


def release(isr_id, now=None, path=None, isos_fetcher=None):
    """Release one due parked question into a late-entry ticket:
    the novelty context built from the answers already there
    (novelty_context.context_for_isr — the existing machinery the
    C5 stage already consumes) plus the differentiation target
    the entry is written against. Returns the ticket, or None
    when the entry is not due. The ticket is a LAB artefact: it
    prepares an entry decision; nothing here submits."""
    import novelty_context  # lazy: keeps this module's import
    # graph free of the serve seams at import time
    now = time.time() if now is None else now
    path = path or late_queue_path()
    entries = _queue(path)
    entry = next((e for e in entries if e.get("isr_id") == isr_id
                  and e.get("state") == "parked"), None)
    if entry is None or not (entry["release_at"] <= now
                             <= entry["expires_at"]):
        return None
    block, meta = novelty_context.context_for_isr(
        isr_id, isos_fetcher=isos_fetcher)
    entry["state"] = "released"
    entry["released_at"] = now
    _write_json(path, entries)
    return {
        "isr_id": isr_id, "lane": LANE_LATE,
        "birth_ts": entry["birth_ts"], "parked_at": entry["parked_at"],
        "released_at": now,
        "delay_at_release_s": now - entry["birth_ts"],
        "differentiation_target": DIFFERENTIATION_TARGET,
        "novelty_block": block, "novelty_meta": meta,
    }


# ------------------------------------------------------ lane budget

def _day_key(now):
    return time.strftime("%Y-%m-%d", time.gmtime(now))


def lane_counts(day=None, path=None):
    budget = _read_json(path or lane_budget_path(), {})
    return dict(budget.get(day or _day_key(time.time()), {}))


def lane_remaining(lane, now=None, path=None):
    now = time.time() if now is None else now
    cap = FAST_DAILY_CAP if lane == LANE_FAST else LATE_DAILY_CAP
    used = lane_counts(_day_key(now), path).get(lane, 0)
    return max(0, cap - used)


def lane_take(lane, now=None, path=None):
    """Consume one lane token for today (UTC day — the serve
    cap's own boundary). False when the lane's allotment is
    spent: a fast slot that finds no quiet question is NEVER
    forced, and a spent lane simply stops for the day."""
    now = time.time() if now is None else now
    path = path or lane_budget_path()
    if lane_remaining(lane, now, path) <= 0:
        return False
    budget = _read_json(path, {})
    day = _day_key(now)
    budget.setdefault(day, {})[lane] = \
        budget.get(day, {}).get(lane, 0) + 1
    _write_json(path, budget)
    return True


# --------------------------------------- decision log (Q2/Q4 fold)

def decision_log_path():
    return _store_path(DECISION_LOG_ENV, "doctrine-decision-log.jsonl")


def log_decision(isr_id, decision, reason_class, lane=None,
                 mode=None, now=None, path=None):
    """Append one doctrine decision record (JSONL, best-effort —
    a failed write never raises into the caller's path).

    Written by vyce_serve_prepare for every doctrine-armed
    decision it takes: "pass" (the row was passed over;
    reason_class says which doctrine branch did it),
    "proceed" (the lane decision let the row through toward
    generation/claim), and "hold" (the Q4 claim-sequencing
    gate stopped it). This log is what makes the Q2
    reconsideration question MEASURABLE (see
    count_lost_after_skip): without a timestamped record of
    first passes, "tickets lost after their skip" is a story,
    not a number. FRONTIER FOLD 2026-11-18 (Q2/Q4)."""
    now = time.time() if now is None else now
    rec = {"ts": now, "isr_id": isr_id, "decision": decision,
           "reason_class": reason_class, "lane": lane, "mode": mode}
    try:
        path = path or decision_log_path()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def load_decisions(path=None):
    """All decision records, oldest first. A missing/corrupt
    log reads as empty; malformed lines are skipped, never
    invented."""
    path = path or decision_log_path()
    out = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if isinstance(rec, dict):
                    out.append(rec)
    except OSError:
        return []
    return out


# Reason classes that mean "this row may become actionable
# later" — the passes the Q2 reconsideration question is about.
# (lane_spent passes are final for the day by doctrine design
# and are not skip losses.)
_RECONSIDERABLE_PASS_CLASSES = ("unclassified", "wait", "not_due")


def count_lost_after_skip(decisions=None, entries=None,
                          decision_path=None, queue_path=None):
    """THE Q2 DECIDING MEASUREMENT (frontier fold 2026-11-18;
    duck's overturn evidence, operationalised): how many parked
    tickets were lost to the classification-lag race — i.e.
    tickets that (1) prepare passed over at least once while
    they were not yet actionable (unclassified / TUNGGU /
    TELAT-not-yet-due), (2) later sat in the late queue, and
    (3) EXPIRED there without prepare ever proceeding on them
    inside their release window [release_at, expires_at].

    A ticket that was proceeded on inside its window is not
    lost to the skip (whatever happened next is generation /
    gate business, recorded elsewhere). A ticket still parked
    is not lost YET. Pure function over the three stores;
    reads them from disk when not given. Returns
    {"count": n, "ids": [...]}."""
    if decisions is None:
        decisions = load_decisions(decision_path)
    if entries is None:
        entries = _queue(queue_path)
    first_pass = {}
    proceeded = {}
    for rec in decisions or []:
        isr = rec.get("isr_id")
        ts = rec.get("ts")
        if not isr or not isinstance(ts, (int, float)):
            continue
        if rec.get("decision") == "pass" and \
                rec.get("reason_class") in _RECONSIDERABLE_PASS_CLASSES:
            if isr not in first_pass or ts < first_pass[isr]:
                first_pass[isr] = ts
        elif rec.get("decision") == "proceed":
            proceeded.setdefault(isr, []).append(ts)
    lost = []
    for entry in entries or []:
        isr = entry.get("isr_id")
        if isr not in first_pass or entry.get("state") != "expired":
            continue
        rel, exp = entry.get("release_at"), entry.get("expires_at")
        if rel is None or exp is None:
            continue
        if not any(rel <= ts <= exp for ts in proceeded.get(isr, [])):
            lost.append(isr)
    return {"count": len(lost), "ids": sorted(lost)}
