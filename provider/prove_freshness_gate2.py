#!/usr/bin/env python3
"""Live proof, part 2b (2026-11-17): the PASS side of the
freshness gate. Part 2 of prove_freshness_gate.py showed the
09:27-sweep "fresh" candidates had ALL flooded within ±1.5 hours
(33–71 answers) — correct withholds, but no live PASS. This run
pulls a small, tight-recency batch through the picker's own pull
(max age 15 minutes), takes viso-0 rows youngest-first, and runs
the gate on them immediately. READ-ONLY; pacing 1.0 s; at most 3
gate checks after the single search pull.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["DIALECTICA_SERVE_GATE_FETCH"] = "1"

import freshness_gate as fg  # noqa: E402
import target_picker as tp  # noqa: E402

MAX_AGE_MS = 900_000          # 15 minutes
LIMIT = 40
MAX_CHECKS = 3
PACE_S = 1.0


def main():
    trued = tp._load_trued()
    rows, notice = tp.pull_candidates(trued, LIMIT, MAX_AGE_MS)
    print(f"tarikan: {len(rows)} baris (maxAge {MAX_AGE_MS} ms)"
          + (f" · {notice}" if notice else ""))
    fresh_rows = []
    for row in rows:
        viso = tp.row_viso(row)
        age = tp.row_age_s(row)
        if viso == 0 and tp.core_topic(row):
            fresh_rows.append((age if age is not None else 1e18,
                               tp.csc.row_isr_id(row), row))
    fresh_rows.sort()
    print(f"baris viso-0 topik-inti: {len(fresh_rows)} "
          f"(termuda dulu)")
    results = []
    passed = None
    for age_s, isr_id, _row in fresh_rows[:MAX_CHECKS]:
        pick = {"isr_id": isr_id, "picked_at": time.time() - (age_s or 0),
                "target_class": "PIONEER", "viso_at_pick": 0,
                "verified_at_pick": 0, "answers_at_pick": 0,
                "source": "tarikan segar prove2 (viso 0, umur "
                          f"{age_s:.0f} dtk)"}
        v = fg.check_freshness(isr_id, pick_state=pick)
        results.append(v)
        live = v.get("live") or {}
        print(f"  {isr_id[:8]} umur={age_s:.0f}dtk status={v['status']} "
              f"TAHAN={v['withhold']} verified={live.get('verified_now')} "
              f"kerumunan={live.get('crowd_now')} fetch={v['fetch']} "
              f"alasan={'; '.join(v['reasons'])[:160]}")
        if not v["withhold"] and v["status"] == "fresh":
            passed = isr_id
            break
        time.sleep(PACE_S)
    print(f"\nRINGKASAN 2b: dicek {len(results)} · LOLOS: "
          f"{passed[:8] if passed else 'tidak ada dalam anggaran'}")
    out = os.path.join(HERE, "freshness-proof2-2026-11-17.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"pulled_rows": len(rows),
                   "viso0_core_rows": len(fresh_rows),
                   "checks": results}, fh, ensure_ascii=False, indent=1)
    print(f"hasil mentah: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
