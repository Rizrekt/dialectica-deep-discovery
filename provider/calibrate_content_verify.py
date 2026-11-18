#!/usr/bin/env python3
"""Calibration runner for the content-verify layer (2026-11-17,
Opsi A). Runs content_verify.verify_content with the REAL
HttpFetcher and the REAL stage-2 transport (Nemotron over our own
checker lanes — serve_gate.default_semantic_model_call; the Vyce
key is injected into THIS process only, via dynamic_credentials,
exactly as run_serve injects it for serve; never printed).

ACCEPTANCE GATE (same shape as the citation calibration):
- The ORIGINAL Hop case (pilot draft 2777178d) MUST be caught —
  reported per stage: stage-1-alone (a second run with
  max_stage2=0) and stage-1+2.
- Controlled synthetics of the same species (same live source,
  figures/date swapped) MUST be caught.
- Healthy controls (claims whose figures the spot-check verified
  against their sources + the two verified-corpus drafts the
  citation calibration designated healthy) MUST NOT be withheld:
  false-fatal on a healthy control must be 0.
- Boundary case: the Meiklejohn fabricated DOI — the source is
  DEAD, which is the citation layer's conviction; the content
  layer must classify it no-source/unverifiable, NOT convict on
  content.

Writes calibration-content-results.json next to this script and
prints a per-case summary. Network: honest UA, fetcher pacing;
stage-2 calls are real checker-lane calls (budget-capped per
draft by the layer itself).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

from dynamic_credentials import dynamic_credential_entry  # noqa: E402

import content_verify as cnv  # noqa: E402

# Inject the Vyce checker-lane key into this process only (the
# OpenRouter lane self-guards its emergency reserve and will be
# skipped by its own probe while the reserve is low).
try:
    _entry = dynamic_credential_entry("custom.vyce", "access_token")
    os.environ["VYCE_API_KEY"] = str(_entry["surrogate"])
    print("calibrate_content: checker-lane credential injected "
          "(value not shown)")
except Exception as ex:  # noqa: BLE001
    print(f"calibrate_content: credential injection FAILED "
          f"({type(ex).__name__}) — stage 2 will report lane-down")

SPOTCHECK_DIR = os.path.join(HERE, "..", "PILOT-SPOTCHECK-2026-11-17")

with open(os.path.join(SPOTCHECK_DIR, "01-2777178d-jawaban.txt"),
          encoding="utf-8") as fh:
    DRAFT_2777 = fh.read()

HOP_SYNTHETIC = (
    "The clearest public precedent is Hop Protocol's 2022 "
    "airdrop: Hop let identified sybils self-report to keep 75% "
    "of their would-be allocation, while bounty hunters earned "
    "30% of the value of sybils they reported (Hop Protocol, "
    "docs.hop.exchange).")
TREASURY_TRUE = (
    "Its weaknesses: farms disperse funding through DEX swaps, "
    "bridges, P2P purchases, and mixers — Tornado Cash was "
    "sanctioned by the US Treasury on August 8, 2022 partly for "
    "this laundering role (https://home.treasury.gov/news/"
    "press-releases/jy0916) — and can rent aged wallets with "
    "clean funding histories.")
TREASURY_SWAPPED = TREASURY_TRUE.replace("August 8, 2022",
                                         "August 9, 2022")
BIP32_YEAR = (
    "Hierarchical deterministic wallets derive an unbounded "
    "number of addresses from a single seed (BIP-32, 2012 — "
    "https://github.com/bitcoin/bips/blob/master/"
    "bip-0032.mediawiki), and account-abstraction wallets make "
    "spinning up smart agent wallets a programmatic operation.")
MEIKLEJOHN_BOUNDARY = (
    "On UTXO chains, the common-input-ownership heuristic — "
    "inputs spent together are controlled by the same entity — "
    "is the backbone of wallet clustering (Meiklejohn et al., "
    "\"A Fistful of Bitcoins,\" ACM IMC 2013 — "
    "https://doi.org/10.1145/2516651.2516734).")

CASES = [
    ("hop-original-2777178d", DRAFT_2777, "must-catch"),
    ("hop-synthetic-figures", HOP_SYNTHETIC, "must-catch"),
    ("treasury-swapped-date", TREASURY_SWAPPED, "must-catch"),
    ("treasury-true", TREASURY_TRUE, "healthy"),
    ("bip32-year", BIP32_YEAR, "healthy"),
    ("ctrl-66bff0ce-Danis",
     open(os.path.join(HERE, "citation-calibration-controls",
                       "verified-66bff0ce-Danis.txt"),
          encoding="utf-8").read(), "healthy"),
    ("ctrl-3f3b1ffa-kasnapp",
     open(os.path.join(HERE, "citation-calibration-controls",
                       "verified-3f3b1ffa-kasnapp.txt"),
          encoding="utf-8").read(), "healthy"),
    ("meiklejohn-boundary", MEIKLEJOHN_BOUNDARY, "boundary"),
]


def _no_stage2(prompt):
    return json.dumps({"verdict": "unclear", "evidence": "",
                       "why": "stage-1-only run (budget 0)"})


def summarise(label, kind, out, out_s1):
    c = out["counts"]
    caught_full = out["verdict"] == "fatal"
    caught_s1 = out_s1["verdict"] == "fatal"
    print(f"\n== {label} [{kind}]")
    print(f"   tahap-1+2: verdict={out['verdict']} "
          f"block={out['block']} stage2_calls={out['stage2_calls']} "
          f"counts={c}")
    print(f"   tahap-1-saja: verdict={out_s1['verdict']} "
          f"block={out_s1['block']}")
    for cl in out["claims"]:
        if cl["pivotal"] or cl["stage1"] in ("finding", "unbound"):
            toks = ", ".join(
                f"{t['raw']}={'OK' if t['found'] else 'ABSENT'}"
                for t in cl["tokens"])
            print(f"   CLAIM pivotal={cl['pivotal']} "
                  f"s1={cl['stage1']} s2={cl['stage2']} "
                  f"final={cl['final']} src={cl['source_status']} "
                  f"[{toks}] :: {cl['claim'][:90]}")
            if cl["stage2_why"]:
                print(f"      stage2 why: {cl['stage2_why'][:160]}")
    if out["error"]:
        print(f"   ERROR: {out['error'][:200]}")
    return caught_full, caught_s1


def main():
    results = {}
    gate = {"must_catch_full": 0, "must_catch_s1": 0,
            "must_catch_total": 0, "healthy_fatal": 0,
            "healthy_total": 0}
    for label, draft, kind in CASES:
        started = time.time()
        out = cnv.verify_content(draft, mode="block")
        out_s1 = cnv.verify_content(draft, mode="block",
                                    model_call=_no_stage2,
                                    max_stage2=0)
        elapsed = time.time() - started
        caught_full, caught_s1 = summarise(label, kind, out, out_s1)
        results[label] = {"kind": kind, "elapsed_s": round(elapsed, 1),
                          "caught_full": caught_full,
                          "caught_stage1_only": caught_s1,
                          "full": out, "stage1_only": out_s1}
        if kind == "must-catch":
            gate["must_catch_total"] += 1
            gate["must_catch_full"] += int(caught_full)
            gate["must_catch_s1"] += int(caught_s1)
        elif kind == "healthy":
            gate["healthy_total"] += 1
            gate["healthy_fatal"] += int(caught_full)
    print("\n== ACCEPTANCE GATE ==")
    print(f"   must-catch tahap-1+2: {gate['must_catch_full']}/"
          f"{gate['must_catch_total']}")
    print(f"   must-catch tahap-1-saja: {gate['must_catch_s1']}/"
          f"{gate['must_catch_total']}")
    print(f"   healthy false-fatal: {gate['healthy_fatal']}/"
          f"{gate['healthy_total']} (wajib 0)")
    ok = (gate["must_catch_full"] == gate["must_catch_total"]
          and gate["healthy_fatal"] == 0)
    print(f"   GATE: {'LOLOS' if ok else 'GAGAL — laporkan apa adanya'}")
    out_path = os.path.join(HERE, "calibration-content-results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"gate": gate, "cases": results}, fh,
                  ensure_ascii=False, indent=1)
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
