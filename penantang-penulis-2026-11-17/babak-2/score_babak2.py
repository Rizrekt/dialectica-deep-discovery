#!/usr/bin/env python3
"""Penilai babak 2 + tabel tiga sisi.

Draf baru qwen-wajib-apparatus: citation_verify (mode block, fetcher
nyata) + mechanical_floor (K-1/K-2, fungsi gerbang persis) +
detect_thinking_trace + panjang vs pita PIONEER.

Enam draf lama (GLM asli + qwen babak 1): hasil sitasi diambil dari
scores.json babak 1 (fetcher nyata, sudah jalan); mechanical_floor +
trace dihitung lokal-deterministik di sini supaya vonis kirim
gabungan (sitasi + K-2) tiga sisi memakai penggaris yang sama."""
import json, pathlib, sys

PROV = pathlib.Path.home() / "workspace/research/dialectica/provider"
sys.path.insert(0, str(PROV))
import citation_verify as cv          # noqa: E402
import openrouter_wrapper as ow       # noqa: E402
import serve_gate as sg               # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
SPOT = ROOT.parent / "PILOT-SPOTCHECK-2026-11-17"
ITEMS = [(1, "2777178d"), (2, "d94d7e34"), (3, "635a010d")]
LOG = HERE / "citation-babak2-log.jsonl"
BAND = (3435, 7297)

def floor_and_trace(draft):
    fl = ow.mechanical_floor(draft)
    tr = sg.detect_thinking_trace(draft)
    return {
        "url_count": fl["url_count"],
        "citation_count": fl["citation_count"],
        "citation_density": fl["citation_density"],
        "number_tokens": fl["number_tokens"],
        "bound_numbers": fl["bound_numbers"],
        "bound_ratio": fl["bound_ratio"],
        "k2_passed": fl["checks"]["ratio"]["passed"],
        "floor_passed": fl["passed"],
        "floor_failures": fl["failures"],
        "trace_findings": len(tr),
    }

def cite_summary(draft, isr):
    out = cv.verify_citations(draft, mode="block", isr_id=isr,
                              log_path=str(LOG))
    findings = out.get("findings", [])
    return {
        "verdict": out.get("verdict"),
        "block": out.get("block"),
        "counts": out.get("counts", {}),
        "findings_pivotal": [{"value": f.get("value"),
                              "kind": f.get("kind"),
                              "status": f.get("status"),
                              "detail": (f.get("detail") or "")[:200]}
                             for f in findings if f.get("pivotal")],
        "findings_peripheral": [{"value": f.get("value"),
                                 "kind": f.get("kind"),
                                 "status": f.get("status"),
                                 "detail": (f.get("detail") or "")[:200]}
                                for f in findings
                                if not f.get("pivotal")],
        "unverified_n": len(out.get("unverified", [])),
        "error": out.get("error"),
    }

def send_verdict(cite_block, floor_passed, trace_n):
    reasons = []
    if cite_block:
        reasons.append("sitasi: TAHAN (fatal)")
    if not floor_passed:
        reasons.append("lantai mekanis K-1/K-2: GAGAL")
    if trace_n:
        reasons.append("jejak proses: ADA")
    return {"sendable": not reasons, "reasons": reasons}

def main():
    old = json.loads((ROOT / "scores.json").read_text())
    result = {}
    for n, tag in ITEMS:
        sides = {}
        # --- GLM asli (sitasi dari babak 1; lantai dihitung di sini)
        glm = (SPOT / f"{n:02d}-{tag}-jawaban.txt").read_text()
        g_cite = old[f"q{n}-glm"]
        g_ft = floor_and_trace(glm)
        sides["glm"] = {"chars": len(glm),
                        "cite": {k: g_cite[k] for k in
                                 ("verdict", "block", "counts",
                                  "findings_pivotal",
                                  "findings_peripheral", "unverified_n")},
                        **g_ft,
                        "send": send_verdict(g_cite["block"],
                                             g_ft["floor_passed"],
                                             g_ft["trace_findings"])}
        # --- qwen babak 1 tanpa apparatus
        q1 = (ROOT / f"q{n}-{tag}-jawaban-qwen.txt").read_text()
        q1_cite = old[f"q{n}-qwen"]
        q1_ft = floor_and_trace(q1)
        sides["qwen_babak1"] = {"chars": len(q1),
                                "cite": {k: q1_cite[k] for k in
                                         ("verdict", "block", "counts",
                                          "findings_pivotal",
                                          "findings_peripheral",
                                          "unverified_n")},
                                **q1_ft,
                                "send": send_verdict(
                                    q1_cite["block"],
                                    q1_ft["floor_passed"],
                                    q1_ft["trace_findings"])}
        # --- qwen babak 2 wajib apparatus (sitasi fetcher nyata, baru)
        q2f = HERE / f"q{n}-{tag}-jawaban-qwen2.txt"
        if q2f.exists():
            q2 = q2f.read_text()
            c2 = cite_summary(q2, tag)
            q2_ft = floor_and_trace(q2)
            sides["qwen_babak2"] = {
                "chars": len(q2),
                "in_band": BAND[0] <= len(q2) <= BAND[1],
                "cite": c2, **q2_ft,
                "send": send_verdict(c2["block"], q2_ft["floor_passed"],
                                     q2_ft["trace_findings"])}
            print("done", f"q{n}-qwen2", c2["verdict"], c2["counts"],
                  "ratio", q2_ft["bound_ratio"], flush=True)
        else:
            sides["qwen_babak2"] = None
            print("missing qwen2 draft", n, flush=True)
        result[f"q{n}-{tag}"] = sides
        (HERE / "scores-babak2.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1))
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    main()
