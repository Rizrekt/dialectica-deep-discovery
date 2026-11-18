#!/usr/bin/env python3
"""STEP 4b — complete the sample: (1) one C5 retry on the stored
3b5c0f0c draft; (2) one more live core-topic target through the
real pipe (the first step-4 target's generation failed). Read-only
question fetches record each chosen target's served fields. Stops
before submit."""
import json
import os
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
EXCLUDE = {"8a4e9623", "3dd05619", "3b5c0f0c"}


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


def question_fields(isr):
    try:
        d = trued.call("/api/node/question", {"isrId": isr})
    except BaseException as ex:  # noqa: BLE001
        return {"error": str(ex)[:120]}
    keep = {}
    for k in ("status", "phase", "answerCount", "answersCount",
              "verifiedIsoCount", "verifiedCount"):
        if k in d:
            keep[k] = d[k]
    iso = d.get("isolatedAnswers")
    if isinstance(iso, list):
        keep["isolatedAnswers_len"] = len(iso)
        keep["isolated_verified"] = sum(
            1 for a in iso if isinstance(a, dict)
            and a.get("verdict") == "verified")
    return keep


def main():
    print("arm vyce:", cal.arm_vyce_fallback(), flush=True)
    out = {}
    prev = json.load(open(os.path.join(
        BASE, "step4-dryruns-results.json")))
    # (1) C5 retry on 3b5c0f0c
    for rec in prev:
        if rec["isr"].startswith("3b5c0f0c") and rec.get("gen_ok"):
            sem = serve_gate.semantic_check(
                rec["draft"], question=rec["question"],
                isr_id=rec["isr"], model_call=vyce_first,
                mode="shadow",
                log_path=os.path.join(BASE,
                                      "step4-semantic-log.jsonl"))
            out["c5_retry_3b5c0f0c"] = {
                "verdict": sem["verdict"], "checker": sem["checker"],
                "codes": [f["code"] for f in sem["findings"]],
                "subs": [f["sub"] for f in sem["findings"]
                         if f.get("sub")],
                "error": (sem["error"] or "")[:200]}
            print("C5 retry 3b5c0f0c:", sem["verdict"],
                  out["c5_retry_3b5c0f0c"]["codes"], flush=True)
    # served fields for both step-4 targets
    out["fields"] = {rec["isr"][:8]: question_fields(rec["isr"])
                     for rec in prev}
    print("fields:", json.dumps(out["fields"])[:300], flush=True)
    # (2) one more target
    rows = {}
    for q in QUERIES:
        try:
            data = trued.call("/api/node/explore-search",
                              {"q": q, "limit": 10})
        except BaseException:
            continue
        for row in data.get("questions", []):
            rid = str(row.get("isrId") or row.get("id") or "")
            if rid and rid not in rows:
                rows[rid] = row
    target = None
    for rid, row in rows.items():
        if rid[:8] in EXCLUDE:
            continue
        content = str(row.get("content") or "")
        low = content.lower()
        if not any(k in low for k in TOPIC_KW):
            continue
        ok, reason = serve_gate.liveness_gate_for_row(row)
        print(f"  {rid[:8]} liveness={ok} ({reason[:60]})",
              flush=True)
        if ok:
            target = {"isr": rid, "liveness": reason,
                      "question": content}
            break
    if target is None:
        out["extra"] = {"error": "tidak ada target live lain"}
        print("tidak ada target live lain", flush=True)
    else:
        rec = dict(target)
        t0 = time.time()
        try:
            res = vsc.vyce_pipeline(target["question"],
                                    isr_id=target["isr"])
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
            print(f"{target['isr'][:8]}: lahir {len(res['text'])} "
                  f"kar status={res['status']} sendable="
                  f"{res['sendable']}", flush=True)
            sem = serve_gate.semantic_check(
                res["text"], question=target["question"],
                isr_id=target["isr"], model_call=vyce_first,
                mode="shadow",
                log_path=os.path.join(BASE,
                                      "step4-semantic-log.jsonl"))
            rec["semantic"] = {
                "verdict": sem["verdict"],
                "checker": sem["checker"],
                "codes": [f["code"] for f in sem["findings"]],
                "subs": [f["sub"] for f in sem["findings"]
                         if f.get("sub")],
                "findings": sem["findings"],
                "dropped": sem["dropped_findings"],
                "error": (sem["error"] or "")[:200]}
            print(f"{target['isr'][:8]}: C5={sem['verdict']} "
                  f"codes={rec['semantic']['codes']}", flush=True)
        except Exception as ex:  # noqa: BLE001
            rec.update({"gen_ok": False,
                        "gen_secs": round(time.time() - t0, 1),
                        "error": f"{type(ex).__name__}: {ex}"[:300]})
            print(f"{target['isr'][:8]}: GAGAL {rec['error']}",
                  flush=True)
        rec["fields"] = question_fields(target["isr"])
        out["extra"] = rec
    print("serve cap after:", vsc.serve_generations_today(),
          "/", vsc.SERVE_GEN_CAP, flush=True)
    with open(os.path.join(BASE, "step4b-results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
