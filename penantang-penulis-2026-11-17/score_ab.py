#!/usr/bin/env python3
"""Skor A/B penantang penulis: jalankan citation_verify (mode block,
fetcher nyata — pola calibrate_citation_verify.py) ke 6 draf dan
ringkas per draf: penunjuk total, findings dipisah poros/pinggiran,
vonis, panjang. Simpan JSON hasil."""
import json, pathlib, sys

PROV = pathlib.Path.home() / "workspace/research/dialectica/provider"
sys.path.insert(0, str(PROV))
import citation_verify as cv  # noqa: E402

HERE = pathlib.Path(__file__).parent
SPOT = HERE.parent / "PILOT-SPOTCHECK-2026-11-17"
ITEMS = [(1, "2777178d"), (2, "d94d7e34"), (3, "635a010d")]
LOG = HERE / "citation-ab-log.jsonl"

def summarize(tag_side, draft, isr):
    out = cv.verify_citations(draft, mode="block", isr_id=isr,
                              log_path=str(LOG))
    findings = out.get("findings", [])
    piv = [f for f in findings if f.get("pivotal")]
    per = [f for f in findings if not f.get("pivotal")]
    return {
        "side": tag_side,
        "chars": len(draft),
        "verdict": out.get("verdict"),
        "block": out.get("block"),
        "counts": out.get("counts", {}),
        "findings_pivotal": [{"value": f.get("value"), "kind": f.get("kind"),
                              "status": f.get("status"),
                              "detail": (f.get("detail") or "")[:160]}
                             for f in piv],
        "findings_peripheral": [{"value": f.get("value"),
                                 "kind": f.get("kind"),
                                 "status": f.get("status"),
                                 "detail": (f.get("detail") or "")[:160]}
                                for f in per],
        "unverified_n": len(out.get("unverified", [])),
        "error": out.get("error"),
    }

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"  # glm|qwen|all
    results = {}
    out_path = HERE / "scores.json"
    if out_path.exists():
        results = json.loads(out_path.read_text())
    for n, tag in ITEMS:
        if only in ("glm", "all"):
            draft = (SPOT / f"{n:02d}-{tag}-jawaban.txt").read_text()
            results[f"q{n}-glm"] = summarize("glm", draft, tag)
            print("done", f"q{n}-glm", results[f"q{n}-glm"]["verdict"],
                  results[f"q{n}-glm"]["counts"], flush=True)
        if only in ("qwen", "all"):
            qf = HERE / f"q{n}-{tag}-jawaban-qwen.txt"
            if qf.exists():
                draft = qf.read_text()
                results[f"q{n}-qwen"] = summarize("qwen", draft, tag)
                print("done", f"q{n}-qwen",
                      results[f"q{n}-qwen"]["verdict"],
                      results[f"q{n}-qwen"]["counts"], flush=True)
            else:
                print("missing qwen draft", n, flush=True)
        out_path.write_text(json.dumps(results, ensure_ascii=False,
                                       indent=1))

if __name__ == "__main__":
    main()
