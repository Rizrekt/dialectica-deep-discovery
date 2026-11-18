#!/usr/bin/env python3
"""Verifier runner — Jalur 2 (2026-11-18). DRY-RUN BY DEFAULT;
THE SEND PATH IS LOCKED in this build.

WHAT A LIVE RUN WILL LOOK LIKE (post-registration, post-user-kata):
an IVSP credential in ~/.dialectica-ivsp/agent.json connects to the
agent gateway exactly as the Expert does (Matrix room; system user
sends evaluate-request / execute-job / schema-correction events —
see verifier_common.parse_gateway_event); verification jobs name
the Answer in the opportunity's targetIsoId; the verdict goes back
as the threaded reply text in the job's room, in the output format
the server's job prompt dictates; the jobs endpoint
(GET /api/node/agents/{id}/jobs) reconciles outcomes afterwards.

WHAT THIS BUILD DOES (all that is possible and permitted today —
no IVSP exists on the account, and creating one is the user's
decision):
  --dry-run (default): builds the work list from PUBLIC reads —
  recent General questions and their revealed Answers — runs the
  self-dealing gate on every candidate, drafts verdicts with the
  local mechanical drafter (and, with --lanes, the Nemotron + qwen
  model lanes), appends every draft to verdict-drafts.jsonl, and
  prints a summary. It sends NOTHING, ever, in this mode.
  --send: LOCKED. Refuses unconditionally in this build (exit 5):
  there is no IVSP credential to send with, and arming a send path
  is part of the go-live act, not of this kit's delivery.

Usage:
  python3 run_verifier.py [--dry-run] [--limit-questions 3]
                          [--per-question 3] [--lanes]
                          [--samples <dryrun-samples.json>]
  python3 run_verifier.py --send        # refuses; documents the lock
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import self_dealing_gate  # noqa: E402
import verdict_drafter  # noqa: E402
import verifier_common as vc  # noqa: E402

DRAFT_LOG = os.path.join(HERE, "verdict-drafts.jsonl")


def log_draft(entry):
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **entry}
    with open(DRAFT_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def fetch_candidates(limit_questions, per_question):
    """Public-read work list: recent General questions, their
    revealed Answers as candidates. Read-only."""
    data = vc.api_get("/api/node/isrs", params={"limit": 40})
    out = []
    for question in data.get("isrs") or []:
        if len(out) >= limit_questions:
            break
        if question.get("arenaId") not in (None, "general"):
            continue
        isos = vc.api_get(f"/api/node/isos/{question['id']}").get("isos") or []
        revealed = [i for i in isos if i.get("status") == "revealed"]
        if not revealed:
            continue
        cands = [vc.parse_iso_row(i, question)
                 for i in revealed[:per_question]]
        out.append((question, cands))
    return out


def load_sample_candidates(path):
    """Offline work list from a saved samples file (the 2026-11-18
    dry-run evidence shape: {questions: [{question, isos}]})."""
    with open(path) as fh:
        data = json.load(fh)
    return [(item["question"],
             [vc.parse_iso_row(i, item["question"])
              for i in item["isos"]])
            for item in data.get("questions") or []]


def run_dry(candidates, identity, use_lanes=False, lane_answers=0):
    """Gate -> draft -> log, for every candidate. Returns a summary
    dict. `lane_answers` caps how many gate-passing candidates also
    go to the model lanes (relay budget is shared; default 0 =
    local only unless --lanes raises it)."""
    summary = {"candidates": 0, "gate_refused": 0, "drafted": 0,
               "verdicts": {}, "lane_drafts": 0}
    laned = 0
    for _question, cands in candidates:
        for cand in cands:
            summary["candidates"] += 1
            gate = self_dealing_gate.check_candidate(cand, identity)
            if not gate["allowed"]:
                summary["gate_refused"] += 1
                log_draft({"mode": "dry-run", "stage": "gate-refused",
                           "isrId": cand["isrId"], "isoId": cand["isoId"],
                           "reasons": gate["reasons"]})
                continue
            draft = verdict_drafter.draft_verdict(
                cand["question"], cand["answer"])
            summary["drafted"] += 1
            summary["verdicts"][draft["verdict"]] = \
                summary["verdicts"].get(draft["verdict"], 0) + 1
            entry = {"mode": "dry-run", "stage": "draft",
                     "isrId": cand["isrId"], "isoId": cand["isoId"],
                     "ownerName": cand["answerOwnerName"],
                     "local_draft": draft}
            if use_lanes and laned < lane_answers:
                import lane_drafter
                lanes = [lane_drafter.draft_with_lane(name, model,
                                                      cand["question"],
                                                      cand["answer"])
                         for name, model in lane_drafter.LANES]
                entry["lane_drafts"] = lanes
                entry["agreement"] = lane_drafter.compare_drafts(
                    [draft] + lanes)
                summary["lane_drafts"] += 1
                laned += 1
            log_draft(entry)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verifier runner (dry-run build)")
    ap.add_argument("--dry-run", action="store_true",
                    help="explicit dry-run (this is also the default)")
    ap.add_argument("--send", action="store_true",
                    help="LOCKED in this build — always refuses")
    ap.add_argument("--limit-questions", type=int, default=3)
    ap.add_argument("--per-question", type=int, default=3)
    ap.add_argument("--lanes", action="store_true",
                    help="also draft with the Nemotron + qwen lanes "
                         "(shared relay budget; paced >=13 s/call)")
    ap.add_argument("--lane-answers", type=int, default=3)
    ap.add_argument("--samples", default=None,
                    help="offline samples JSON instead of live reads")
    args = ap.parse_args(argv)

    if args.send:
        print("SEND LOCKED — this build cannot submit verifications: "
              "no IVSP credential exists on this account, and arming "
              "the send path is part of the go-live act (user kata "
              "jalan + registration via register_ivsp.py + a wired, "
              "reviewed send path). Nothing was sent.")
        return 5

    identity = self_dealing_gate.load_identity()
    if not identity["user_ids"]:
        print("WARNING: ours.json carries no user id — the gate is "
              "running on the API's isOwnAgent signal alone.")
    if os.path.exists(vc.IVSP_STATE_PATH):
        print("NOTE: an IVSP state file exists — live polling is a "
              "go-live step; this build still dry-runs from reads.")
    else:
        print("No IVSP credential home yet (~/.dialectica-ivsp) — "
              "dry-run from public reads, as designed.")

    if args.samples:
        candidates = load_sample_candidates(args.samples)
    else:
        candidates = fetch_candidates(args.limit_questions,
                                      args.per_question)
    summary = run_dry(candidates, identity, use_lanes=args.lanes,
                      lane_answers=args.lane_answers if args.lanes else 0)
    print(f"DRY-RUN DONE: {json.dumps(summary)}")
    print(f"Drafts appended to {DRAFT_LOG}. Nothing was sent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
