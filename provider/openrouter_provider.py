#!/usr/bin/env python3
"""OpenRouter/Nemotron provider for Dialectica — CLAIM LANE (one-shot
--answer only, MEKANISME §35) + shadow drill.

MEKANISME §34 (wrapper) + §35 (activation). Status: AKTIF untuk klaim
sejak persetujuan user 2026-11-10 16:56 ("Aktifkan Nemotron buat klaim
— one-shot, gerbang A8 penuh"). Wired into run_serve.py via
`--openrouter`, which points DIALECTICA_PROVIDER_CMD here for
`trued answer` ONLY; background serve on this lane is refused by
run_serve (exit 5) before anything launches. Until that activation the
§29.4 SCAN-ONLY regime governed this lane; it no longer does (the
Gemini revocation in §29.4 is separate and still in force). Two jobs:
(1) CLAIM one-shot — read the prompt on stdin, write ONLY the wrapped,
sendable answer on stdout; a draft the wrapper marks not-sendable is
withheld (exit 1, empty stdout), which trued treats as "nothing
submitted" (see §35 for the dropped-job consequence and the A8
discipline that governs it). (2) DRILL BAYANGAN drafts for staged
targets, archived under ~/workspace/research/dialectica/drills/ for
later comparison against what actually verifies (MODE DRILL 3A).

Contract (same shape as vyce_provider.py): read the prompt on stdin,
write ONLY the wrapped answer on stdout, diagnostics to stderr. Every
answer passes the mandatory wrapper (openrouter_wrapper.py): mojibake
normalisation, the 4,500-char length guard with one expansion
regeneration, the number/citation audit + citation_patch (dead gate d),
and the QUALITY.md rubric score. A draft that ends GAGAL-LANJUT, keeps
an unpatchable misattribution, or fails the format gate is NOT emitted
(exit 1, stderr explains) — in shadow mode that simply means no draft.

Generation goes through the registered connector client
(~/workspace/custom-connectors/custom.openrouter/bin/client.py); the
vault surrogate is swapped for the real key on egress by Muse and
never touches this file or disk. Model: nvidia/nemotron-3-ultra-550b-
a55b:free — the only model that completed claim-class answers in the
OpenRouter benchmark (5/5, BENCH-2026-11-10). Quota is checked via the
client's `key` command BEFORE every generation; remaining < 3 aborts
cleanly. Usage is appended to provider/token-usage.jsonl, the same log
the Vyce patch writes.

Drill usage:
  python3 openrouter_provider.py drill [--isr <uuid>] [--no-log]
"""
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from openrouter_wrapper import (  # noqa: E402
    format_withhold_breakdown, rubric_sheet, wrap_answer)

CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.openrouter/bin/client.py")
MODEL = os.environ.get("OPENROUTER_MODEL",
                       "nvidia/nemotron-3-ultra-550b-a55b:free")
MIN_QUOTA_REMAINING = 3
MAX_TOKENS = 8000
USAGE_LOG = os.path.join(HERE, "token-usage.jsonl")
DRILLS_DIR = os.path.expanduser("~/workspace/research/dialectica/drills")
DRILL_LOG = os.path.expanduser("~/workspace/research/dialectica/DRILL-LOG.md")
LANE_LABEL = "openrouter-nemotron"

# Nemotron's measured median is 3,846 chars against a 4,500 floor even
# when the prompt already demands 4,500-8,000, so this lane always
# carries an explicit overshoot instruction; the wrapper's regeneration
# guard is the second line of defence, not the first.
#
# §7.1 butir 5 (2026-11-11, utang §50.7): the 5,500–7,500 band below is
# the STANDARD band, aligned for the test targets (viso 4–5, pita
# baku). For MARATHON targets (busy band 10,000–12,000) this suffix
# band is ADVISORY, not binding — what actually gates sending is the
# §45 mechanical floor (4,500 chars) plus the dead gates (d)/(g), NOT
# band precision. The suffix text itself now says so, so the collision
# can no longer happen silently. Send behaviour is unchanged.
LENGTH_SUFFIX = (
    "\n\n---\nSYARAT PANJANG (wajib, diukur persis): jawaban akhir "
    "5.500–7.500 karakter. Di bawah 5.000 karakter = gagal. Tulis setiap "
    "seksi secara penuh — mekanisme, angka yang benar dari dokumen yang "
    "disebut namanya, dan contoh hitungan — jangan meringkas. "
    "Catatan pita: pita 5.500–7.500 ini pita baku (target viso 4–5); "
    "untuk target marathon yang mengikat BUKAN presisi pita ini, "
    "melainkan lantai 4.500 karakter + gerbang sitasi/format — jawaban "
    "marathon boleh lebih panjang dari pita ini."
)


class QuotaAbort(RuntimeError):
    """Free-tier daily quota too low; abort cleanly, spend nothing."""


class GenerationError(RuntimeError):
    """The client call failed or returned no usable answer."""


def quota_remaining():
    proc = subprocess.run([sys.executable, CLIENT, "key"],
                          capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise QuotaAbort(f"quota check failed: {proc.stderr.strip()[:200]}")
    data = json.loads(proc.stdout)
    counter = (data.get("body") or {}).get("data", {}).get(
        "free_model_daily_requests") or {}
    remaining = counter.get("remaining")
    if remaining is None:
        raise QuotaAbort(f"quota counter unreadable: {str(counter)[:120]}")
    return remaining


def _log_usage(usage, isr_id, answer_chars, quota_after):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": LANE_LABEL,
        "model": MODEL,
        "isr": isr_id or None,
        "usage": usage,
        "answer_chars": answer_chars,
        "quota_remaining_after": quota_after,
    }
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"openrouter_provider: usage log write failed: {ex}",
              file=sys.stderr)


def generate(prompt, isr_id=None):
    """One generation through the connector client, quota-gated.
    Returns {text, usage, latency_s, quota_before, quota_after}."""
    before = quota_remaining()
    if before < MIN_QUOTA_REMAINING:
        raise QuotaAbort(
            f"free quota remaining {before} < {MIN_QUOTA_REMAINING}; "
            "generation aborted before spending")
    with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", dir=HERE, delete=False,
            encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, CLIENT, "chat", "--model", MODEL,
             "--prompt-file", prompt_path,
             "--max-tokens", str(MAX_TOKENS)],
            capture_output=True, text=True, timeout=660)
    finally:
        os.unlink(prompt_path)
    if proc.returncode != 0:
        raise GenerationError(
            f"client chat failed rc={proc.returncode}: "
            f"{proc.stderr.strip()[:200]}")
    result = json.loads(proc.stdout)
    if result.get("status") != 200 or not (result.get("text") or "").strip():
        raise GenerationError(
            f"no usable answer: status={result.get('status')} "
            f"chars={result.get('chars')} body={str(result.get('body'))[:200]}")
    try:
        after = quota_remaining()
    except QuotaAbort:
        after = None
    _log_usage(result.get("usage"), isr_id, len(result["text"]), after)
    return {"text": result["text"], "usage": result.get("usage"),
            "latency_s": result.get("latency_s"),
            "quota_before": before, "quota_after": after}


def apply_steering(prompt, isr_id):
    if not isr_id:
        return prompt
    path = os.path.join(HERE, "steering", isr_id + ".txt")
    try:
        with open(path, encoding="utf-8") as fh:
            steer = fh.read().strip()
    except OSError:
        return prompt
    if steer:
        print(f"openrouter_provider: steering applied for {isr_id}",
              file=sys.stderr)
        return (prompt + "\n\n---\nOPERATOR STEERING (priority "
                "instruction):\n" + steer)
    return prompt


def run_pipeline(prompt, isr_id=None, **score_kwargs):
    """Generate + wrap. Returns the wrap result plus generation stats."""
    stats = {"generations": []}
    first = generate(prompt, isr_id)
    stats["generations"].append(first)

    def regen(instruction):
        again = generate(prompt + instruction, isr_id)
        stats["generations"].append(again)
        return again["text"]

    result = wrap_answer(first["text"], regen_fn=regen, **score_kwargs)
    result["generations"] = stats["generations"]
    unpatchable = [f for f in result["report"]["audit"]["findings"]
                   if not f.get("span")]
    result["sendable"] = (
        result["status"] == "OK" and not unpatchable
        and result["score"]["g"][0] == "LOLOS")
    return result


def main():
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("openrouter_provider: empty prompt on stdin", file=sys.stderr)
        return 2
    isr_id = os.environ.get("DIALECTICA_ISR_ID", "").strip()
    prompt = apply_steering(prompt, isr_id) + LENGTH_SUFFIX
    try:
        result = run_pipeline(prompt, isr_id or None)
    except (QuotaAbort, GenerationError) as ex:
        print(f"openrouter_provider: {ex}", file=sys.stderr)
        return 1
    print(f"openrouter_provider: wrapped "
          f"status={result['status']} sendable={result['sendable']} "
          f"chars={result['report']['chars_final']} "
          f"audit_findings={len(result['report']['audit']['findings'])}",
          file=sys.stderr)
    if not result["sendable"]:
        print("openrouter_provider: draft WITHHELD (sendable=false: an "
              "audit finding survived, the format gate failed, or the "
              "length guard ended GAGAL-LANJUT). Exiting 1 with empty "
              "stdout — trued treats a nonzero provider exit as "
              "'nothing submitted' and drops the job (MEKANISME §35).",
              file=sys.stderr)
        print(f"openrouter_provider: "
              f"{format_withhold_breakdown(result['report'])}",
              file=sys.stderr)
        return 1
    sys.stdout.write(result["text"] + "\n")
    return 0


# ------------------------------------------------------------------- drill

DRILL_QUESTION_60FA = (
    "For a token launch deploying a fleet of ERC-20 vaults on an L2: "
    "EIP-1167 minimal-proxy clones versus full standalone contracts — "
    "compare gas cost, upgradeability, and auditability. Which should "
    "the launch choose, and when does the answer flip?")
DRILL_FORBIDDEN_60FA = ("200(B", "N(S", "N* ≈ 2")


def drill(isr_id, write_log=True):
    steer_path = os.path.join(HERE, "steering", isr_id + ".txt")
    with open(steer_path, encoding="utf-8") as fh:
        steer = fh.read().strip()
    prompt = (DRILL_QUESTION_60FA + "\n\n---\nOPERATOR STEERING "
              "(priority instruction):\n" + steer + LENGTH_SUFFIX)
    started = time.strftime("%Y-%m-%d %H:%M WIB", time.localtime())
    result = run_pipeline(
        prompt, isr_id, expected_sections=6,
        forbidden_overlap=DRILL_FORBIDDEN_60FA if isr_id.startswith(
            "60fa9935") else ())
    rep = result["report"]
    stamp = time.strftime("%Y-%m-%d-%H%M", time.localtime())
    os.makedirs(DRILLS_DIR, exist_ok=True)
    fname = f"{isr_id}-{stamp}.md"
    gens = result["generations"]
    sheet = rubric_sheet(result["score"], isr=isr_id, model=MODEL,
                         kelas="DRILL BAYANGAN")
    audit_lines = "\n".join(
        f"- {f['severity']} {f['doc']} nilai={f['value']}: {f['action']}"
        f"\n  > {f['excerpt']}"
        for f in rep["audit"]["findings"]) or "- nol temuan"
    archive = f"""# DRILL BAYANGAN — lane={LANE_LABEL}

- Target: {isr_id} (EIP-1167 minimal proxy vs standalone, settled, viso 6)
- Waktu: {started}
- Model: {MODEL} via connector custom.openrouter (mode DRILL — TIDAK dikirim ke Dialectica; lane klaim aktif terpisah per §35, drill tetap bukan klaim)
- Generasi: {len(gens)} panggilan; latensi {[g['latency_s'] for g in gens]} dtk; kuota free {gens[0]['quota_before']} -> {gens[-1]['quota_after']} sisa
- Panjang: mentah {rep['chars_raw']} kar -> ternormalisasi {rep['chars_normalised']} -> final {rep['chars_final']} kar; regenerasi perluasan: {rep['regenerated']}
- Mojibake: penanda {rep['mojibake']['markers_before']} -> {rep['mojibake']['markers_after']}
- Status panjang: {result['status']}; sendable (seandainya klaim diizinkan): {result['sendable']}

## Skor rubrik

```
{sheet}
```

## Audit angka & sitasi (gerbang mati d)

{audit_lines}
- Angka dibuang oleh citation_patch: {rep['audit']['numbers_removed'] or 'tidak ada'}

## Draf final (sesudah wrapper)

{result['text']}

## Tindak lanjut (MODE DRILL 3A)

Perbandingan verdict: MENUNGGU — jendela berikutnya wajib memeriksa jawaban verified akhir pertanyaan ini dan menilai apakah draf ini akan menang dan di butir apa bedanya (DRILL-LOG.md).
"""
    with open(os.path.join(DRILLS_DIR, fname), "w", encoding="utf-8") as fh:
        fh.write(archive)
    log_entry = None
    if write_log:
        sc = result["score"]
        fmt = lambda i: {"LOLOS": "L", "GAGAL": "G"}.get(sc[i][0], "N-A")
        log_entry = (
            f"\n## {time.strftime('%Y-%m-%d')} — jendela "
            f"{time.strftime('%H:%M')} WIB — DRILL BAYANGAN\n"
            f"- Target: {isr_id} — EIP-1167 minimal proxy vs standalone "
            f"(settled, viso 6)\n"
            f"- Yang dinilai: draf kita, arsip drills/{fname} "
            f"(lane={LANE_LABEL})\n"
            f"- Skor rubrik v2: (a) {fmt('a')} · (b) {fmt('b')} · "
            f"(c) {fmt('c')} ({rep['chars_final']} karakter) · "
            f"(d) {fmt('d')} · (e) {fmt('e')} · (f) {fmt('f')} · "
            f"(g) {fmt('g')}\n"
            f"- Yang ditangkap rubrik: wrapper menangkap cacat terukur "
            f"lane ini — mojibake {rep['mojibake']['markers_before']}->"
            f"{rep['mojibake']['markers_after']} penanda, panjang "
            f"{rep['chars_raw']}->{rep['chars_final']} kar "
            f"(regenerasi: {rep['regenerated']}), audit angka "
            f"{len(rep['audit']['findings'])} temuan "
            f"({rep['audit']['wrong']} salah-atribusi).\n"
            f"- Celah rubrik: (f) tidak bisa dinilai mekanis di mode "
            f"bayangan (tidak ada pembanding verified di pipa) — cek "
            f"manual saat tindak lanjut verdict.\n"
            f"- Tindak lanjut: perbandingan verdict di entri arsip; pola "
            f"salah-atribusi angka = eksperimen E1 yang sudah tercatat "
            f"di QUALITY.md.\n"
            f"- Tindak lanjut verdict: MENUNGGU\n")
        with open(DRILL_LOG, "a", encoding="utf-8") as fh:
            fh.write(log_entry)
    summary = {
        "archive": fname, "status": result["status"],
        "sendable": result["sendable"],
        "chars_final": rep["chars_final"],
        "generations": len(gens),
        "quota_before": gens[0]["quota_before"],
        "quota_after": gens[-1]["quota_after"],
        "audit_findings": len(rep["audit"]["findings"]),
        "rubric": {k: v[0] for k, v in result["score"].items()},
        "drill_log_written": bool(log_entry),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "drill":
        isr = "60fa9935-4352-4a4c-9aa7-384de037196c"
        if "--isr" in sys.argv:
            isr = sys.argv[sys.argv.index("--isr") + 1]
        try:
            sys.exit(drill(isr, write_log="--no-log" not in sys.argv))
        except (QuotaAbort, GenerationError, OSError) as ex:
            print(f"openrouter_provider drill: {ex}", file=sys.stderr)
            sys.exit(1)
    sys.exit(main())
