#!/usr/bin/env python3
"""Cloudflare Workers AI / gpt-oss-120b provider for Dialectica —
claim lane, one-shot --answer only (MEKANISME §37), same contract and
same mandatory wrapper as the OpenRouter/Nemotron lane (§34/§35).

Status: WIRING + BENCHMARK tugas ini; whether the hunt cron may fire
claims on this lane is a main-session decision taken on the §37 bench
verdict. run_serve.py wires this file behind `--cloudflare` for
`trued answer` ONLY; background serve on this lane is refused by
run_serve (exit 5) before anything launches — identical fence to §35.

Contract (same shape as vyce_provider.py / openrouter_provider.py):
read the prompt on stdin, write ONLY the wrapped, sendable answer on
stdout, diagnostics to stderr. Every answer passes the mandatory
wrapper (openrouter_wrapper.py, imported unchanged): mojibake
normalisation, the 4,500-char length guard with one expansion
regeneration, the number/citation audit + citation_patch (dead gate
d), and the QUALITY.md rubric score. A draft the wrapper marks
not-sendable is withheld (exit 1, empty stdout) — trued treats a
nonzero provider exit as "nothing submitted" and drops the job (see
§35 for the dropped-job consequence and the A8 discipline).

Generation goes through the registered connector client
(~/workspace/custom-connectors/custom.cloudflare-workers-ai/bin/
client.py); the vault surrogate is swapped for the real API token on
egress by Muse and never touches this file or disk. Model:
@cf/openai/gpt-oss-120b — the strongest model PROVEN to run on the
Workers Free plan (ELIGIBILITY-2026-11-10; GLM 5.3 Flash and DeepSeek
V4.1 Flash on this platform are PAID-ONLY, HTTP 403 code 5035 — never
route them here).

Budget: the free allocation is 10,000 neurons/day (reset 00:00 UTC),
metered per generation in usage.neurons. The running UTC-day total is
rebuilt from provider/token-usage.jsonl (this lane's records only)
BEFORE every generation; a total above 9,000 neurons aborts cleanly
before anything is spent (1,000-neuron safety reserve). One measured
claim-class generation cost 128.56 neurons (ELIGIBILITY), so the abort
line is a runaway fence, not an operating limit.
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
    format_withhold_breakdown, wrap_answer)

CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.cloudflare-workers-ai/bin/client.py")
MODEL = os.environ.get("CLOUDFLARE_MODEL", "@cf/openai/gpt-oss-120b")
NEURON_DAILY_CAP = 10000
NEURON_ABORT_ABOVE = 9000
MAX_TOKENS = 8000
USAGE_LOG = os.path.join(HERE, "token-usage.jsonl")
LANE_LABEL = "cloudflare-gptoss"

# Same overshoot instruction as the Nemotron lane: the wrapper's
# regeneration guard is the second line of defence, not the first.
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


class NeuronBudgetAbort(RuntimeError):
    """UTC-day neuron spend already above the safety line; spend 0."""


class GenerationError(RuntimeError):
    """The client call failed or returned no usable answer."""


def neurons_spent_today_utc(lanes=None):
    """Sum usage.neurons over today's (UTC) records in token-usage.jsonl
    for the given lane labels (default: THIS lane only). Other platforms
    meter other currencies (OpenRouter requests, Vyce tokens) and are
    never mixed in. The serve lane (§39) passes BOTH Cloudflare lane
    labels: the platform's 10,000-neuron day is account-wide, so its
    budget check must see claim + serve spend together."""
    wanted = (LANE_LABEL,) if lanes is None else tuple(lanes)
    today = time.strftime("%Y-%m-%d", time.gmtime())
    total = 0.0
    try:
        with open(USAGE_LOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if rec.get("lane") not in wanted:
                    continue
                if not str(rec.get("ts", "")).startswith(today):
                    continue
                neurons = (rec.get("usage") or {}).get("neurons")
                if isinstance(neurons, (int, float)):
                    total += neurons
    except OSError:
        pass
    return total


def _log_usage(usage, isr_id, answer_chars, neurons_today_after,
               lane=LANE_LABEL):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": lane,
        "model": MODEL,
        "isr": isr_id or None,
        "usage": usage,
        "answer_chars": answer_chars,
        "neurons_today_after": neurons_today_after,
    }
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"cloudflare_provider: usage log write failed: {ex}",
              file=sys.stderr)


def generate(prompt, isr_id=None, lane=LANE_LABEL, budget_lanes=None):
    """One generation through the connector client, budget-gated.
    Returns {text, usage, latency_s, neurons_before, neurons_after}.

    `lane` is the token-usage.jsonl label the generation is recorded
    under (claim lane by default; the §39 serve lane passes its own).
    `budget_lanes` selects which labels the pre-generation neuron total
    sums over; None keeps the claim lane's original semantics (its own
    label, via a no-argument call)."""
    if budget_lanes is None:
        before = neurons_spent_today_utc()
    else:
        before = neurons_spent_today_utc(budget_lanes)
    if before > NEURON_ABORT_ABOVE:
        raise NeuronBudgetAbort(
            f"neuron spend today (UTC) {before:.1f} > "
            f"{NEURON_ABORT_ABOVE} safety line (daily cap "
            f"{NEURON_DAILY_CAP}); generation aborted before spending")
    with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", dir=HERE, delete=False,
            encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, CLIENT, "run", "--model", MODEL,
             "--prompt-file", prompt_path,
             "--max-tokens", str(MAX_TOKENS)],
            capture_output=True, text=True, timeout=660)
    finally:
        os.unlink(prompt_path)
    if proc.returncode != 0:
        raise GenerationError(
            f"client run failed rc={proc.returncode}: "
            f"{proc.stderr.strip()[:200]} stdout={proc.stdout[:200]}")
    result = json.loads(proc.stdout)
    if result.get("status") != 200 or not (result.get("text") or "").strip():
        raise GenerationError(
            f"no usable answer: status={result.get('status')} "
            f"chars={result.get('chars')} body={str(result.get('body'))[:200]}")
    usage = result.get("usage") or {}
    neurons = usage.get("neurons")
    after = before + neurons if isinstance(neurons, (int, float)) else None
    _log_usage(usage, isr_id, len(result["text"]), after, lane=lane)
    return {"text": result["text"], "usage": usage,
            "latency_s": result.get("latency_s"),
            "neurons_before": before, "neurons_after": after}


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
        print(f"cloudflare_provider: steering applied for {isr_id}",
              file=sys.stderr)
        return (prompt + "\n\n---\nOPERATOR STEERING (priority "
                "instruction):\n" + steer)
    return prompt


def run_pipeline(prompt, isr_id=None, **score_kwargs):
    """Generate + wrap. Returns the wrap result plus generation stats.
    Sendable semantics identical to §35: status OK + no surviving audit
    finding + format gate (g) LOLOS. The wrapper report strips the
    finding `span` field, so patchable vs unpatchable cannot be told
    apart downstream — ANY audit finding therefore means not sendable
    (deliberate fail-closed conservatism, same as the Nemotron lane)."""
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
        print("cloudflare_provider: empty prompt on stdin", file=sys.stderr)
        return 2
    isr_id = os.environ.get("DIALECTICA_ISR_ID", "").strip()
    prompt = apply_steering(prompt, isr_id) + LENGTH_SUFFIX
    try:
        result = run_pipeline(prompt, isr_id or None)
    except (NeuronBudgetAbort, GenerationError) as ex:
        print(f"cloudflare_provider: {ex}", file=sys.stderr)
        return 1
    print(f"cloudflare_provider: wrapped "
          f"status={result['status']} sendable={result['sendable']} "
          f"chars={result['report']['chars_final']} "
          f"audit_findings={len(result['report']['audit']['findings'])}",
          file=sys.stderr)
    if not result["sendable"]:
        print("cloudflare_provider: draft WITHHELD (sendable=false: an "
              "audit finding survived, the format gate failed, or the "
              "length guard ended GAGAL-LANJUT). Exiting 1 with empty "
              "stdout — trued treats a nonzero provider exit as "
              "'nothing submitted' and drops the job (MEKANISME §35/§37).",
              file=sys.stderr)
        print(f"cloudflare_provider: "
              f"{format_withhold_breakdown(result['report'])}",
              file=sys.stderr)
        return 1
    sys.stdout.write(result["text"] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
