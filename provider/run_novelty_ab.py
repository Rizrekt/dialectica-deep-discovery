#!/usr/bin/env python3
"""A/B bukti kerja konteks kebaruan C5 (2026-11-17,
KONTEKS-KEBARUAN-C5-2026-11-17.md). SHADOW ONLY — tidak ada
serve/submit/klaim: yang dipanggil hanya search/detail/isos
read-only, generasi GLM jalur dry-run (cap serve tercatat), dan
semantic_check mode shadow dengan log khusus run ini.

Fase `select`: tarik kandidat live (jalur target_picker), saring
viso >= 2, ambil isos, bangun paket (pertanyaan + jawaban verified
+ blok kebaruan) ke novelty-2026-11-17/pack.json.
Fase `run`: muat paket; per ISR buat draf GLM (generate_vyce —
pipa asli, kontrak serve ditempel generate sendiri), plus draf
kontrol parafrase dari --control-file untuk ISR pertama bila
diberikan; jalankan semantic_check DUA kali per draf (pertanyaan
polos vs pertanyaan + blok kebaruan; kontrol diulang 2x per kondisi
karena varians pemeriksa terukur di kalibrasi). Lane pemeriksa
Vyce-dulu (preseden dry-run 2026-11-17: jaga cadangan OpenRouter).
Hasil: novelty-2026-11-17/results.json.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT_DIR = os.path.expanduser(
    "~/workspace/research/dialectica/novelty-2026-11-17")
PACK = os.path.join(OUT_DIR, "pack.json")
RESULTS = os.path.join(OUT_DIR, "results.json")
SEM_LOG = os.path.join(OUT_DIR, "semantic-log.jsonl")

os.environ.setdefault("DIALECTICA_SERVE_GATE_FETCH", "1")

import calibrate_semantic_c5 as cal  # noqa: E402
import novelty_context as nc  # noqa: E402
import serve_gate  # noqa: E402
import target_picker as tp  # noqa: E402
import vyce_serve_common as vsc  # noqa: E402


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


def question_text(detail):
    return str((detail or {}).get("content")
               or (detail or {}).get("title") or "")


def do_select(limit_isr):
    trued = tp._load_trued()
    rows, notice = tp.pull_candidates(trued, 100,
                                      tp.DEFAULT_MAX_AGE_MS)
    if notice:
        print(notice, flush=True)
    cand = [r for r in rows if (tp.row_viso(r) or 0) >= 2]
    cand.sort(key=lambda r: (-(tp.row_viso(r) or 0),
                             0 if tp.core_topic(r) else 1))
    print(f"baris viso>=2: {len(cand)} — ambil isos untuk "
          f"{min(limit_isr * 2, len(cand))} teratas", flush=True)
    pack = []
    for row in cand[:limit_isr * 2]:
        if len(pack) >= limit_isr:
            break
        isr_id = row.get("id") or row.get("isrId")
        detail, dstate = tp.fetch_detail(trued, isr_id)
        isos, istate = nc.fetch_isos(isr_id)
        if istate != "ok":
            print(f"  {str(isr_id)[:8]}: isos {istate} — lewati",
                  flush=True)
            continue
        answers = nc.verified_answers(isos)
        readable = [a for a in answers if len(a["text"]) >= 400]
        block, meta = nc.build_block(isos)
        print(f"  {str(isr_id)[:8]}: viso baris={tp.row_viso(row)} "
              f"verified={len(answers)} terbaca(>=400)={len(readable)} "
              f"blok={meta['block_chars']} kar", flush=True)
        if len(readable) < 2 or not block:
            continue
        pack.append({
            "isr_id": isr_id,
            "viso_row": tp.row_viso(row),
            "core_topic": tp.core_topic(row),
            "question": question_text(detail),
            "block": block,
            "block_meta": meta,
            "answers": [{"id": a["id"], "supported": a["supported"],
                         "text": a["text"]} for a in readable],
        })
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(PACK, "w", encoding="utf-8") as fh:
        json.dump(pack, fh, indent=1, ensure_ascii=False)
    print(f"\npaket: {len(pack)} ISR -> {PACK}", flush=True)
    for p in pack:
        print(f"- {p['isr_id'][:8]} viso={p['viso_row']} "
              f"inti={p['core_topic']} verified={len(p['answers'])} "
              f"blok={p['block_meta']['block_chars']} kar")
        print(f"  Q: {p['question'][:140]!r}")
    if pack:
        a1 = pack[0]["answers"][0]
        print(f"\nJawaban verified #1 ISR pertama "
              f"({a1['id'][:8]}, supported {a1['supported']}) — "
              f"bahan draf kontrol:\n{a1['text'][:2500]}")
    return 0


def summarise(res):
    by_code = {}
    for f in res.get("findings", []):
        by_code[f["code"]] = by_code.get(f["code"], 0) + 1
    return {
        "verdict": res.get("verdict"),
        "checker": res.get("checker"),
        "findings_total": len(res.get("findings", [])),
        "by_code": by_code,
        "surprise_findings": [
            {"quote": f["quote"], "why": f["why"]}
            for f in res.get("findings", [])
            if f["code"] == "SURPRISE_GAUGE"],
        "dropped": res.get("dropped_findings"),
        "error": res.get("error"),
    }


def run_checks(label, draft, entry, reps):
    out = {"label": label, "draft_chars": len(draft), "runs": []}
    q_plain = entry["question"]
    q_ctx = nc.attach(entry["question"], entry["block"])
    for rep in range(reps):
        for cond, q in (("tanpa-konteks", q_plain),
                        ("dengan-konteks", q_ctx)):
            res = serve_gate.semantic_check(
                draft, question=q, isr_id=entry["isr_id"],
                model_call=vyce_first, mode="shadow",
                log_path=SEM_LOG)
            s = summarise(res)
            s.update({"rep": rep + 1, "condition": cond})
            out["runs"].append(s)
            print(f"  [{label}] rep{rep + 1} {cond}: "
                  f"verdict={s['verdict']} temuan={s['findings_total']} "
                  f"per-kode={s['by_code']} lane={s['checker']}",
                  flush=True)
    return out


def do_run(control_file):
    with open(PACK, encoding="utf-8") as fh:
        pack = json.load(fh)
    print("arm vyce:", cal.arm_vyce_fallback(), flush=True)
    print(f"cap serve sebelum: {vsc.serve_generations_today()}/"
          f"{vsc.SERVE_GEN_CAP}", flush=True)
    results = {"cap_before": vsc.serve_generations_today(),
               "isrs": []}
    for idx, entry in enumerate(pack):
        print(f"\n== ISR {entry['isr_id'][:8]} "
              f"(viso {entry['viso_row']}) ==", flush=True)
        rec = {"isr_id": entry["isr_id"], "drafts": [],
               "glm_error": None}
        draft, last_err = None, None
        for attempt in range(2):
            try:
                draft = vsc.generate_vyce(entry["question"],
                                          isr_id=entry["isr_id"])
                break
            except Exception as ex:  # noqa: BLE001 - generation is data
                last_err = f"{type(ex).__name__}: {ex}"
                print(f"  generasi GLM percobaan {attempt + 1} GAGAL: "
                      f"{last_err}", flush=True)
        if draft:
            print(f"  draf GLM lahir: {len(draft)} kar", flush=True)
            rec["drafts"].append(
                run_checks("glm", draft, entry, reps=1))
        else:
            rec["glm_error"] = last_err
            print("  draf GLM TIDAK lahir sesudah 2 percobaan — "
                  "dicatat, lanjut", flush=True)
        if idx == 0 and control_file:
            with open(control_file, encoding="utf-8") as fh:
                control = fh.read()
            print(f"  draf kontrol dimuat: {len(control)} kar",
                  flush=True)
            rec["drafts"].append(
                run_checks("kontrol-parafrase", control, entry,
                           reps=2))
        results["isrs"].append(rec)
    results["cap_after"] = vsc.serve_generations_today()
    print(f"\ncap serve sesudah: {results['cap_after']}/"
          f"{vsc.SERVE_GEN_CAP}", flush=True)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print(f"hasil -> {RESULTS}", flush=True)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("select", "run"))
    ap.add_argument("--limit-isr", type=int, default=3)
    ap.add_argument("--control-file", default="")
    args = ap.parse_args()
    if args.phase == "select":
        sys.exit(do_select(args.limit_isr))
    sys.exit(do_run(args.control_file or None))
