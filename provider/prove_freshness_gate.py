#!/usr/bin/env python3
"""Live proof for the send-time freshness gate (2026-11-17,
GERBANG-KESEGARAN). READ-ONLY: two client reads per check, no
serve, no submit, no generation. Run once by hand; every verdict
also lands in freshness-check-log.jsonl.

Proof obligations:
1. The 5 pilot questions of 2026-11-17 — picked at viso 0, since
   flooded to 23–59 answers — must ALL be WITHHELD in their
   current state (the gate catches exactly the pilot's failure
   shape).
2. Fresh candidates from the last picker sweep
   (picker-shadow-sisakecil1-2026-11-17.json, PIONEER viso 0) are
   checked in order until one PASSES or the trial budget (4) is
   spent — a candidate that has itself gone stale in the hours
   since the sweep is evidence FOR the gate, reported as such.

Pacing: 1.0 s between checks. The platform is preparing
maintenance (official banner 2026-11-17) — failures are recorded
openly, never retried in a loop.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["DIALECTICA_SERVE_GATE_FETCH"] = "1"  # arm the client reads

import freshness_gate as fg  # noqa: E402

PILOT = [
    ("2777178d-2294-4303-9b94-e877fdac95d0", "2026-11-17T02:37:00Z"),
    ("d94d7e34-01e1-44ef-9666-b0616980bc93", "2026-11-17T02:41:00Z"),
    ("635a010d-fa76-42a3-8ddf-c592e5189637", "2026-11-17T02:47:00Z"),
    ("d21135d5-5d4e-4a54-9da1-c54b4fc466f8", "2026-11-17T02:58:00Z"),
    ("5e905bef-7e0a-4b31-839c-d59a6688c70d", "2026-11-17T03:02:00Z"),
]
FRESH_TRIAL_BUDGET = 4
PACE_S = 1.0


def _pilot_pick(isr_id, submitted_z):
    import datetime
    ts = datetime.datetime.strptime(
        submitted_z, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc).timestamp()
    return {"isr_id": isr_id, "picked_at": ts,
            "target_class": "PIONEER", "viso_at_pick": 0,
            "verified_at_pick": 0, "answers_at_pick": 0,
            "source": "VERDICT-WATCH-2026-11-17 (pilot, viso 0)"}


def _line(v):
    live = v.get("live") or {}
    return (f"{v['isr_id'][:8]} kelas={v['class']} "
            f"status={v['status']} TAHAN={v['withhold']} "
            f"verified={live.get('verified_now')} "
            f"kerumunan={live.get('crowd_now')} "
            f"fetch={v['fetch']} "
            f"alasan={'; '.join(v['reasons'])[:220]}")


def main():
    results = {"pilot": [], "fresh_trials": []}
    print("== BUKTI 1: 5 pertanyaan pilot dalam keadaan SEKARANG ==")
    for isr_id, submitted in PILOT:
        v = fg.check_freshness(isr_id, pick_state=_pilot_pick(isr_id,
                                                              submitted))
        results["pilot"].append(v)
        print(" ", _line(v))
        time.sleep(PACE_S)
    print("== BUKTI 2: kandidat segar sapuan pemilih terakhir ==")
    with open(os.path.join(
            HERE, "picker-shadow-sisakecil1-2026-11-17.json"),
            encoding="utf-8") as fh:
        rows = json.load(fh)
    candidates = [r["isr_id"] for r in rows
                  if isinstance(r, dict) and r.get("cls") == "PIONEER"]
    passed = None
    for isr_id in candidates[:FRESH_TRIAL_BUDGET]:
        pick = {"isr_id": isr_id, "picked_at": None,
                "target_class": "PIONEER", "viso_at_pick": 0,
                "verified_at_pick": 0, "answers_at_pick": 0,
                "source": "SAPUAN-ULANG-PEMILIH-2026-11-17 (viso 0)"}
        v = fg.check_freshness(isr_id, pick_state=pick)
        results["fresh_trials"].append(v)
        print(" ", _line(v))
        if not v["withhold"] and v["status"] == "fresh":
            passed = isr_id
            break
        time.sleep(PACE_S)
    pilot_held = sum(1 for v in results["pilot"] if v["withhold"])
    print(f"\nRINGKASAN: pilot tertahan {pilot_held}/5 · kandidat "
          f"segar dicoba {len(results['fresh_trials'])} · lolos: "
          f"{passed[:8] if passed else 'TIDAK ADA dalam anggaran coba'}")
    out = os.path.join(HERE, "freshness-proof-2026-11-17.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"hasil mentah: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
