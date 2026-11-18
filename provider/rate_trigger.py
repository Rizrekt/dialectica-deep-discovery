#!/usr/bin/env python3
"""PEMICU LAJU — the Doctrine-A rate trigger observer
(2026-11-18, keputusan user 08:23 Opsi A). READ-ONLY / LAB: it
polls the same opportunity feed the picker uses, classifies each
new question's entry mode from the inflow of its first 2 minutes
of life, records classifications in the doctrine trigger store,
parks TELAT questions in the late queue, and re-decides TUNGGU
questions at +30 min. It never claims, never serves, never
submits.

HOW THE FIRST 2 MINUTES ARE MEASURED. Not by watching from
second 0 — our polling cannot promise that, and does not need
to: the count is reconstructed EXACTLY from the ISO list's own
timestamps (answers born in [birth, birth+120s)), the same
reconstruction the verdict-queue study used on the same fields.
Discovery lag therefore costs decision time, never accuracy;
this observer MEASURES that lag (first-seen minus birth, per
question) and reports its distribution, so the doctrine's
practical reach is stated from data, not assumed.

WHAT A CLASSIFICATION COSTS. One search call per poll (shared
with any picker run) + one ISO-list fetch per NEW question
(capped per poll, youngest first) + one per TUNGGU re-evaluation.
No other network behaviour; failures are data (a question whose
ISOs cannot be read stays unclassified and is retried next poll,
never guessed).

QUESTION BIRTH. The row's `timestamp` (ms epoch) when present;
else now − questionAgeMs. A row with neither cannot be timed
honestly and is skipped (counted, never classified).
"""
import argparse
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_serve_common as csc  # noqa: E402
import doctrine_a as da  # noqa: E402
import novelty_context  # noqa: E402
import serve_gate  # noqa: E402
import target_picker  # noqa: E402

# A question first observed older than this is past every doctrine
# window that a fresh classification could still steer (the late
# window closes at 6 h; beyond it a classification is archaeology).
MAX_CLASSIFY_AGE_S = 6 * 3600
# Per-poll ISO fetch budget: the API is slow (one call measured
# 5–17 s in picker runs); the youngest questions are classified
# first because their CEPAT window is the perishable one.
DEFAULT_ISO_BUDGET = 8


def row_birth_ts(row, now):
    """Question birth (epoch s) from the row's own fields, or
    None when the row cannot be timed honestly."""
    ts = (row or {}).get("timestamp")
    try:
        if ts is not None:
            v = float(ts)
            return v / 1000.0 if v > 1e12 else v
    except (TypeError, ValueError):
        pass
    age_ms = (row or {}).get("questionAgeMs")
    try:
        if age_ms is not None:
            return now - float(age_ms) / 1000.0
    except (TypeError, ValueError):
        pass
    return None


def iso_timestamps(isos):
    """ISO birth timestamps (epoch s) from the list payload —
    the study's own field (`timestamp`, ms epoch). Unparseable
    entries are skipped."""
    out = []
    for iso in isos or []:
        if not isinstance(iso, dict):
            continue
        ts = serve_gate.parse_ts(iso.get("timestamp"))
        if ts is not None:
            out.append(ts)
    return out


def classify_question(isr_id, birth_ts, isos, now, store_path=None):
    """Classify one question from its ISO timestamps and record
    it. Returns the classification record (also persisted)."""
    stamps = iso_timestamps(isos)
    first = da.count_in_window(stamps, birth_ts)
    mode = da.classify_inflow(first)
    return da.record_classification(
        isr_id, mode, first, birth_ts, now=now,
        discovery_lag_s=round(now - birth_ts, 1), path=store_path)


def observe_once(rows, now, isos_fetcher, store, store_path=None,
                 queue_path=None, iso_budget=DEFAULT_ISO_BUDGET):
    """One poll's worth of trigger work over opportunity `rows`.
    `store` is the in-memory trigger store (mutated + persisted
    per classification). Returns a facts dict for the run report:
    new classifications, TUNGGU re-evaluations, skips, and the
    discovery lags observed this poll. Pure orchestration — all
    network arrives through `isos_fetcher` (the fetch_isos
    contract: isr_id -> (isos, state))."""
    facts = {"classified": [], "reevaluated": [], "skipped_old": 0,
             "skipped_untimed": 0, "fetch_failed": 0, "budget_left": 0}
    # Youngest first: the CEPAT window is the perishable one.
    timed = []
    for row in rows or []:
        isr_id = csc.row_isr_id(row)
        if not isr_id or isr_id in store:
            continue
        birth = row_birth_ts(row, now)
        if birth is None:
            facts["skipped_untimed"] += 1
            continue
        if now - birth > MAX_CLASSIFY_AGE_S:
            facts["skipped_old"] += 1
            continue
        timed.append((birth, isr_id))
    timed.sort(reverse=True)
    budget = iso_budget
    for birth, isr_id in timed:
        if budget <= 0:
            break
        budget -= 1
        isos, state = isos_fetcher(isr_id)
        if state != "ok" or not isinstance(isos, list):
            facts["fetch_failed"] += 1
            continue
        rec = classify_question(isr_id, birth, isos, now,
                                store_path=store_path)
        store[isr_id] = rec
        facts["classified"].append(rec)
        if rec["mode"] == da.LANE_LATE:
            da.park(isr_id, birth, now=now, path=queue_path)
    facts["budget_left"] = budget
    # TUNGGU re-evaluations due at +30 min from classification.
    for isr_id, rec in list(store.items()):
        if rec.get("mode") != da.MODE_WAIT:
            continue
        if now - rec.get("classified_at", now) < da.WAIT_REEVAL_S:
            continue
        if budget <= 0:
            break
        budget -= 1
        isos, state = isos_fetcher(isr_id)
        if state != "ok" or not isinstance(isos, list):
            facts["fetch_failed"] += 1
            continue
        mode, wfacts = da.reevaluate_wait(
            iso_timestamps(isos), rec["birth_ts"], now)
        rec.update({"mode": mode, "reevaluated_at": now,
                    "wait_facts": wfacts})
        da._write_json(store_path or da.trigger_store_path(), store)
        facts["reevaluated"].append(rec)
        if mode == da.LANE_LATE:
            da.park(isr_id, rec["birth_ts"], now=now, path=queue_path)
    return facts


def _live_isos_fetcher(trued):
    """fetch_isos over the client's own call() — the caller seam
    bypasses the serve-gate arming env (this observer is its own
    launcher), the endpoint and payload shape are the client's."""
    def caller(isr_id):
        return trued.call(f"/api/node/isos/{isr_id}", timeout=30)
    return lambda isr_id: novelty_context.fetch_isos(
        isr_id, caller=caller)


def run_observer(duration_s=720, poll_s=45, max_age_ms=1800_000,
                 limit=100, iso_budget=DEFAULT_ISO_BUDGET,
                 store_path=None, queue_path=None, out=None):
    """The bounded live observation (dry-run): poll the picker
    feed, classify, and report the mode distribution + discovery
    lag at the end. Read-only throughout."""
    out = out or sys.stdout
    trued = target_picker._load_trued()
    fetcher = _live_isos_fetcher(trued)
    store = da.load_trigger_store(store_path)
    started = time.time()
    polls = 0
    all_lags = []
    modes = Counter()
    total_new = 0
    print(f"rate_trigger: observasi {duration_s:.0f} dtk, poll "
          f"{poll_s:.0f} dtk, maxAge {max_age_ms} ms — read-only",
          file=out, flush=True)
    while True:
        now = time.time()
        if polls and now - started >= duration_s:
            break
        polls += 1
        try:
            rows, notice = target_picker.pull_candidates(
                trued, limit, max_age_ms)
        except Exception as ex:  # noqa: BLE001 - a failed poll is
            # data for the report, never a crash of the observer
            print(f"  poll {polls}: pencarian gagal "
                  f"({type(ex).__name__}: {ex})", file=out, flush=True)
            rows = []
        facts = observe_once(rows, now, fetcher, store,
                             store_path=store_path,
                             queue_path=queue_path,
                             iso_budget=iso_budget)
        for rec in facts["classified"]:
            modes[rec["mode"]] += 1
            total_new += 1
            if rec.get("discovery_lag_s") is not None:
                all_lags.append(rec["discovery_lag_s"])
            print(f"  poll {polls}: {rec['isr_id'][:8]} mode="
                  f"{rec['mode']} first2min={rec['first2min']} "
                  f"lag={rec['discovery_lag_s']} dtk", file=out,
                  flush=True)
        for rec in facts["reevaluated"]:
            modes[rec["mode"]] += 1
            print(f"  poll {polls}: {rec['isr_id'][:8]} TUNGGU -> "
                  f"{rec['mode']} {rec['wait_facts']}", file=out,
                  flush=True)
        if time.time() - started >= duration_s:
            break
        time.sleep(poll_s)
    lags = sorted(all_lags)
    report = {
        "polls": polls, "duration_s": round(time.time() - started, 1),
        "new_classified": total_new, "modes": dict(modes),
        "discovery_lag_s": {
            "n": len(lags),
            "min": lags[0] if lags else None,
            "median": lags[len(lags) // 2] if lags else None,
            "max": lags[-1] if lags else None,
            "within_120s": sum(1 for x in lags if x <= 120),
        },
    }
    print("rate_trigger: LAPORAN "
          + json.dumps(report, ensure_ascii=False),
          file=out, flush=True)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Pemicu laju Doktrin A (observasi read-only — "
                    "tidak mengklaim apa pun)")
    ap.add_argument("--duration", type=float, default=720,
                    help="jendela observasi (detik)")
    ap.add_argument("--poll", type=float, default=45,
                    help="jeda antar poll (detik)")
    ap.add_argument("--max-age-ms", type=int, default=1800_000)
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--iso-budget", type=int,
                    default=DEFAULT_ISO_BUDGET)
    args = ap.parse_args(argv)
    run_observer(duration_s=args.duration, poll_s=args.poll,
                 max_age_ms=args.max_age_ms, limit=args.limit,
                 iso_budget=args.iso_budget)
    return 0


if __name__ == "__main__":
    sys.exit(main())
