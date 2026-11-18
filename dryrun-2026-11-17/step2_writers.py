#!/usr/bin/env python3
"""STEP 2 — backup-writer decision (PERBAIKAN-PENGHAMBAT).
Serve-shaped generation (the dry-run target question + the serve
format contract, exactly what generate_vyce appends) through:
  A) deepseek-v4.1 via vyce_provider.call_vyce (direct, no fallback
     contamination — the 403-vs-answers conflict decided here);
  B) @cf/openai/gpt-oss-120b via cloudflare_provider.generate.
Each draft then passes serve_gate.gate_answer (wrapper regen via
the same writer, mirroring vyce_pipeline) and semantic_check
shadow with the Vyce-first Nemotron checker. NO submit anywhere.
"""
import json
import os
import sys
import time
import urllib.error

PROV = os.path.expanduser("~/workspace/research/dialectica/provider")
sys.path.insert(0, PROV)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

import serve_gate  # noqa: E402
import vyce_provider  # noqa: E402
import cloudflare_provider as cfp  # noqa: E402
import calibrate_semantic_c5 as cal  # noqa: E402

OUT = os.path.expanduser(
    "~/workspace/research/dialectica/dryrun-2026-11-17/"
    "step2-writers-results.json")
QUESTION = (
    "When an NFT contract blocks all transfers, how can a dedicated "
    "marketplace still enable trading of those tokens, and what "
    "trust assumptions around custody, operator honesty, or "
    "upgrade keys does that trading introduce for buyers and "
    "sellers?")
PROMPT = QUESTION + serve_gate.SERVE_FORMAT_CONTRACT


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


def gate_and_check(text, regen_fn, label):
    res = serve_gate.gate_answer(text, regen_fn=regen_fn)
    final = res["text"]
    sem = serve_gate.semantic_check(
        final, question=QUESTION, isr_id="step2-" + label,
        model_call=vyce_first, mode="shadow",
        log_path=os.path.expanduser(
            "~/workspace/research/dialectica/dryrun-2026-11-17/"
            "step2-semantic-log.jsonl"))
    return {
        "gate_status": res["status"], "sendable": res["sendable"],
        "score_g": res["score"]["g"][0],
        "final_chars": len(final),
        "audit_findings": len(res["report"]["audit"]["findings"]),
        "thinking_trace": res["gate"]["thinking_trace"],
        "reasons": res["gate"]["reasons"][:4],
        "semantic": {"verdict": sem["verdict"],
                     "checker": sem["checker"],
                     "codes": [f["code"] for f in sem["findings"]],
                     "subs": [f["sub"] for f in sem["findings"]
                              if f.get("sub")],
                     "error": (sem["error"] or "")[:200]},
        "final_text": final,
    }


def main():
    print("arm vyce:", cal.arm_vyce_fallback(), flush=True)
    key_name = "VYCE" "_API" "_KEY"
    key = os.environ.get(key_name, "").strip()
    results = {}

    # ---- A) deepseek-v4.1 via Vyce, direct call
    rec = {"model": "deepseek-v4.1", "lane": "vyce"}
    t0 = time.time()
    try:
        text, usage = vyce_provider.call_vyce(
            "deepseek-v4.1", PROMPT, key)
        rec.update({"ok": True, "secs": round(time.time() - t0, 1),
                    "raw_chars": len(text), "usage": usage,
                    "raw_text": text})
        print(f"deepseek: OK chars={len(text)} "
              f"secs={rec['secs']}", flush=True)

        def ds_regen(instruction):
            t, _u = vyce_provider.call_vyce(
                "deepseek-v4.1", PROMPT + instruction, key)
            return t
        rec["gate"] = gate_and_check(text, ds_regen, "deepseek")
        print(f"deepseek gate: {rec['gate']['gate_status']} "
              f"sendable={rec['gate']['sendable']} "
              f"sem={rec['gate']['semantic']['verdict']}", flush=True)
    except urllib.error.HTTPError as ex:
        body = ""
        try:
            body = ex.read().decode("utf-8", "replace")[:300]
        except Exception:
            pass
        rec.update({"ok": False, "secs": round(time.time() - t0, 1),
                    "error": f"HTTPError {ex.code}: {body}"})
        print(f"deepseek: HTTP {ex.code} {body[:120]}", flush=True)
    except Exception as ex:  # noqa: BLE001
        rec.update({"ok": False, "secs": round(time.time() - t0, 1),
                    "error": f"{type(ex).__name__}: {ex}"[:400]})
        print(f"deepseek: {rec['error'][:160]}", flush=True)
    results["deepseek"] = rec
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)

    # ---- B) gpt-oss-120b via Cloudflare
    rec = {"model": "@cf/openai/gpt-oss-120b", "lane": "cloudflare"}
    t0 = time.time()
    try:
        gen = cfp.generate(PROMPT)
        rec.update({"ok": True, "secs": round(time.time() - t0, 1),
                    "raw_chars": len(gen["text"]),
                    "neurons_before": gen["neurons_before"],
                    "neurons_after": gen["neurons_after"],
                    "raw_text": gen["text"]})
        print(f"gpt-oss: OK chars={len(gen['text'])} "
              f"neurons={gen['neurons_before']}->"
              f"{gen['neurons_after']}", flush=True)

        def cf_regen(instruction):
            return cfp.generate(PROMPT + instruction)["text"]
        rec["gate"] = gate_and_check(gen["text"], cf_regen, "gptoss")
        print(f"gpt-oss gate: {rec['gate']['gate_status']} "
              f"sendable={rec['gate']['sendable']} "
              f"sem={rec['gate']['semantic']['verdict']}", flush=True)
    except Exception as ex:  # noqa: BLE001
        rec.update({"ok": False, "secs": round(time.time() - t0, 1),
                    "error": f"{type(ex).__name__}: {ex}"[:400]})
        print(f"gpt-oss: {rec['error'][:160]}", flush=True)
    results["gptoss"] = rec
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print("done ->", OUT, flush=True)


if __name__ == "__main__":
    main()
