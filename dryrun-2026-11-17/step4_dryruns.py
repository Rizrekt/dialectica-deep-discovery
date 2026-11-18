#!/usr/bin/env python3
"""STEP 4 — two more GLM dry-runs on two DIFFERENT live targets
(PERBAIKAN-PENGHAMBAT). Target selection mirrors the dry-run of
03:48: explore-search over core-topic queries -> core-topic
keyword filter -> serve_gate.liveness_gate_for_row (armed fetch,
three-field) -> Pioneer viso-0 preferred. Generation + form gate
through the REAL pipe (vyce_serve_common.vyce_pipeline; serve cap
counted in code), then semantic_check shadow with the Vyce-first
Nemotron checker. STOPS before submit — nothing is sent anywhere.
"""
import json
import os
import re
import sys
import time

PROV = os.path.expanduser("~/workspace/research/dialectica/provider")
sys.path.insert(0, PROV)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser(
    "~/workspace/research/dialectica/skill-audit/pkg/dialectica/"
    "scripts"))

os.environ["DIALECTICA_SERVE_GATE_FETCH"] = "1"

import serve_gate  # noqa: E402
import vyce_serve_common as vsc  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402
import trued  # noqa: E402

BASE = os.path.expanduser("~/workspace/research/dialectica/"
                          "dryrun-2026-11-17")
OUT = os.path.join(BASE, "step4-dryruns-results.json")
QUERIES = ["ethereum gas fees", "smart contract security",
           "token staking validator", "cross-chain bridge",
           "NFT marketplace", "DeFi lending protocol",
           "layer 2 rollup", "wallet custody keys",
           "MEV frontrunning", "stablecoin peg",
           "oracle price feed", "DAO governance token"]
TOPIC_KW = ["token", "ethereum", "bitcoin", "blockchain", "defi",
            "nft", "staking", "validator", "bridge", "rollup",
            "wallet", "smart contract", "gas", "mev", "stablecoin",
            "oracle", "dao", "custody", "on-chain", "onchain",
            "solana", "bnb", "eip-", "erc-", "layer 2", "l2 "]
EXCLUDE = {"8a4e9623"}


def vyce_first(prompt):
    errs = []
    for label, fn in (("vyce-nemotron", serve_gate._semantic_call_vyce),
                      ("openrouter-nemotron",
                       serve_gate._semantic_call_openrouter)):
        try:
            return fn(prompt), label
        except Exception as ex:  # noqa: BLE001
            errs.append(f"{label}: {type(ex).__name__}: {ex}")
    raise serve_gate.SemanticUnavailable(" || ".join(errs))


def viso_of(row):
    for k in ("verifiedIsoCount", "viso", "verifiedCount",
              "verifiedAnswers"):
        v = row.get(k)
        if isinstance(v, int):
            return v
    return None


def main():
    print("arm vyce:", cal.arm_vyce_fallback(), flush=True)
    print("serve cap before:", vsc.serve_generations_today(),
          "/", vsc.SERVE_GEN_CAP, flush=True)
    rows = {}
    for q in QUERIES:
        try:
            data = trued.call("/api/node/explore-search",
                              {"q": q, "limit": 10})
        except BaseException as ex:  # noqa: BLE001 - client exits
            print(f"search {q!r} gagal: {ex}", flush=True)
            continue
        for row in data.get("questions", []):
            rid = str(row.get("isrId") or row.get("id") or "")
            if rid and rid not in rows:
                rows[rid] = row
    print(f"baris unik: {len(rows)}", flush=True)
    cands = []
    for rid, row in rows.items():
        if rid[:8] in EXCLUDE:
            continue
        content = str(row.get("content") or "")
        low = content.lower()
        hits = [k for k in TOPIC_KW if k in low]
        if not hits:
            continue
        cands.append((viso_of(row), rid, row, hits))
    cands.sort(key=lambda t: (t[0] is None, t[0] or 0))
    print(f"kandidat topik inti: {len(cands)}", flush=True)
    targets = []
    for viso, rid, row, hits in cands:
        if len(targets) >= 2:
            break
        ok, reason = serve_gate.liveness_gate_for_row(row)
        print(f"  {rid[:8]} viso={viso} liveness={ok} "
              f"({reason[:70]})", flush=True)
        if ok:
            targets.append({"isr": rid, "viso": viso, "hits": hits,
                            "liveness": reason,
                            "question": str(row.get("content") or "")})
    print(f"target terpilih: {[t['isr'][:8] for t in targets]}",
          flush=True)
    results = []
    for t in targets:
        rec = dict(t)
        t0 = time.time()
        try:
            res = vsc.vyce_pipeline(t["question"], isr_id=t["isr"])
            rec.update({
                "gen_ok": True,
                "gen_secs": round(time.time() - t0, 1),
                "gate_status": res["status"],
                "sendable": res["sendable"],
                "score_g": res["score"]["g"][0],
                "final_chars": len(res["text"]),
                "audit_findings": len(
                    res["report"]["audit"]["findings"]),
                "thinking_trace": res["gate"]["thinking_trace"],
                "reasons": res["gate"]["reasons"][:4],
                "draft": res["text"]})
            print(f"{t['isr'][:8]}: lahir {len(res['text'])} kar, "
                  f"status={res['status']} sendable="
                  f"{res['sendable']}", flush=True)
        except Exception as ex:  # noqa: BLE001
            rec.update({"gen_ok": False,
                        "gen_secs": round(time.time() - t0, 1),
                        "error": f"{type(ex).__name__}: {ex}"[:300]})
            print(f"{t['isr'][:8]}: GENERASI GAGAL {rec['error']}",
                  flush=True)
            results.append(rec)
            continue
        sem = serve_gate.semantic_check(
            rec["draft"], question=t["question"], isr_id=t["isr"],
            model_call=vyce_first, mode="shadow",
            log_path=os.path.join(BASE, "step4-semantic-log.jsonl"))
        rec["semantic"] = {
            "verdict": sem["verdict"], "checker": sem["checker"],
            "codes": [f["code"] for f in sem["findings"]],
            "subs": [f["sub"] for f in sem["findings"]
                     if f.get("sub")],
            "findings": sem["findings"],
            "dropped": sem["dropped_findings"],
            "error": (sem["error"] or "")[:200]}
        print(f"{t['isr'][:8]}: C5={sem['verdict']} "
              f"codes={rec['semantic']['codes']}", flush=True)
        results.append(rec)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=1)
    print("serve cap after:", vsc.serve_generations_today(),
          "/", vsc.SERVE_GEN_CAP, flush=True)
    print("done ->", OUT, flush=True)


if __name__ == "__main__":
    main()
