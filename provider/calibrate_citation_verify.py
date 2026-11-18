#!/usr/bin/env python3
"""Calibration runner for the citation-verify layer (2026-11-17).

Runs citation_verify.verify_citations with the REAL HttpFetcher
over the exact texts the manual checklist-D spot-check judged:

POSITIVE cases (must be CAUGHT — SPOTCHECK-PILOT-2026-11-17.md):
- 2777178d: dead domain proofofhumanity.site must appear as a
  finding (peripheral — this layer records it; the draft's fatal
  defect, the Hop figures, is content-level and OUT OF SCOPE for
  this layer by design);
- d94d7e34: fabricated DOI (Crossref 404) is pivotal -> WITHHELD,
  plus the no-TLD whitepaper.worldcoin URL as a malformed finding;
- 635a010d: ePrint 2020/940 names Fei Meng's paper, not Lindell's
  -> wrong-document pinpoint -> WITHHELD.

NEGATIVE controls (must NOT be withheld): verified field answers
from the run-11 corpus extract (belajar-2026-11-17/run11-0717
isos_by_isr.json, status "verified"), stored under
citation-calibration-controls/. Candidates are screened by this
same run; the report designates as controls the ones whose
pinpoints verify healthy.

Writes calibration-citation-results.json next to this script and
prints a per-case summary. Network: honest UA, >=0.34s pacing,
per-answer cache — a full run is ~100 fetches.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citation_verify as cv  # noqa: E402

SPOTCHECK_DIR = os.path.join(
    HERE, "..", "PILOT-SPOTCHECK-2026-11-17")
CASES = [
    ("2777178d", os.path.join(SPOTCHECK_DIR, "01-2777178d-jawaban.txt"),
     "positive-domain"),
    ("d94d7e34", os.path.join(SPOTCHECK_DIR, "02-d94d7e34-jawaban.txt"),
     "positive-doi"),
    ("635a010d", os.path.join(SPOTCHECK_DIR, "03-635a010d-jawaban.txt"),
     "positive-eprint"),
    ("ctrl-829b8dd2-Sushil",
     os.path.join(HERE, "citation-calibration-controls",
                  "verified-829b8dd2-Sushil.txt"), "control-candidate"),
    ("ctrl-66bff0ce-Danis",
     os.path.join(HERE, "citation-calibration-controls",
                  "verified-66bff0ce-Danis.txt"), "control-candidate"),
    ("ctrl-3f3b1ffa-kasnapp",
     os.path.join(HERE, "citation-calibration-controls",
                  "verified-3f3b1ffa-kasnapp.txt"), "control-candidate"),
]


def main():
    results = {}
    for label, path, kind in CASES:
        with open(path, encoding="utf-8") as fh:
            draft = fh.read()
        started = time.time()
        out = cv.verify_citations(draft, mode="block")
        elapsed = time.time() - started
        results[label] = {"kind": kind, "path": path,
                          "elapsed_s": round(elapsed, 1), **out}
        c = out["counts"]
        print(f"\n== {label} [{kind}] verdict={out['verdict']} "
              f"block={out['block']} ({elapsed:.0f}s) counts={c}")
        for f in out["findings"]:
            print(f"   FINDING [{'POROS' if f['pivotal'] else 'pinggir'}] "
                  f"{f['kind']} {f['pointer'][:70]} -> {f['status']}: "
                  f"{f['detail'][:130]}")
        for u in out["unverified"]:
            print(f"   UNVERIFIED {u['kind']} {u['pointer'][:70]}: "
                  f"{u['detail'][:110]}")
        if out["error"]:
            print(f"   ERROR: {out['error']}")
    out_path = os.path.join(HERE, "calibration-citation-results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
