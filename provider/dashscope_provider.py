#!/usr/bin/env python3
"""Alibaba DashScope / deepseek-v4-pro-0813 provider for Dialectica —
claim lane, one-shot --answer only (MEKANISME §40), same contract and
same mandatory wrapper as the OpenRouter/Nemotron lane (§34/§35) and
the Cloudflare lane (§37).

Wired into run_serve.py via `--dashscope` for `trued answer` ONLY;
background serve on this lane is refused by run_serve (exit 5) before
anything launches — serve stays on Vyce / Cloudflare §39. Whether the
hunt cron may fire claims on this lane, and on which targets, is a
main-session decision (§40); this file is the wiring + its fences.

Contract (same shape as openrouter_provider.py / cloudflare_provider.py):
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
(~/workspace/custom-connectors/custom.alibaba-dashscope/bin/client.py)
on the USER'S WORKSPACE host; the vault surrogate is swapped for the
real workspace key on egress by Muse and never touches this file or
disk. Model is PINNED: deepseek-v4-pro-0813 — the only model in the
DashScope free-quota tank whose reasoning control is PROVEN (bench
2026-11-10, DASHSCOPE-BENCH-2026-11-10.md).

LOCKED CONFIG A (bench-proven, do not improvise):
  enable_thinking=false, max_tokens=8000, streaming.
CFG-A is what makes this model usable at all: the parameter the
flagship qwen3.8-2.4t-a95b REJECTS (HTTP 400) is accepted here and
thinking really turns off (reasoning:content = 0:100% in all 4 bench
calls; latencies 74–102 s, 3/3 completions, 0 mojibake).

KNOWN DISEASES — read before firing (both are §40 conditions):
1. Gate (d): raw-model (d) FAILED 3/3, every finding bound to
   EIP-2929 (the E1 disease: 700 gas as an EIP-2929 figure, cold
   SLOAD 2,100 "per EIP-2929", etc.) — the same disease as
   gpt-oss-120b (§37). The wrapper caught and removed every number
   mechanically (sendable fail-closed 0/3 raw). The hunt body's
   steering hardening §37 point 4(viii) — the explicit ban on
   binding figures to EIP-2929 — is a CONDITION of using this lane;
   it is written for exactly this pattern.
2. Length discipline NOT yet in the standard band: raw lengths
   overshot systematically (11,792 / 16,188 / 13,626 chars against
   the 4,500–8,000 band; median ±13.6k) — the model treats the
   length requirement as a FLOOR, not a band. Until a hard-ceiling
   steering test proves otherwise, interim claims on this lane are
   legitimate ONLY for targets that allow 10–12k chars (the §30
   template's busy-marathon zone). The LENGTH_SUFFIX below stays
   identical to the other lanes for cross-lane comparability; the
   wrapper is the measuring instrument, not a truncator.

STOCK: this lane burns the user's per-model free-quota stock
(1,000,000 tokens for this model; ±987,129 remained after the bench).
The stock EXPIRES 2026-11-12 — unused stock is gone, not deferred.
Stop-on-Exhaust ("Free Quota Only") is enabled in the user's console
and the API is documented to answer 403 AllocationQuota.FreeTierOnly
instead of billing, BUT that refusal has NEVER been observed live:
quota consumption by successful calls is proven, the protective
refusal is not (§40 keeps this as an open verification item). Usage
from every API response is appended to provider/token-usage.jsonl
under lane `dashscope-deepseekpro` — the response usage figures are
the only stock ledger the API exposes.
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
    "~/workspace/custom-connectors/custom.alibaba-dashscope/bin/client.py")
# PINNED (§40): the only DashScope tank model with proven reasoning
# control; its free-quota stock expires 2026-11-12.
MODEL = "deepseek-v4-pro-0813"
MAX_TOKENS = 8000
# LOCKED CONFIG A: thinking off (accepted by this model; rejected by
# the 2.4T flagship). Streaming is the client default — never pass
# --no-stream on this lane.
EXTRA_BODY = {"enable_thinking": False}
USAGE_LOG = os.path.join(HERE, "token-usage.jsonl")
LANE_LABEL = "dashscope-deepseekpro"

# Same overshoot instruction as the other lanes (see header note 2:
# this model treats it as a floor — measured, documented, and the
# reason interim claims are restricted to 10–12k-char targets).
#
# §7.1 butir 5 (2026-11-11, utang §50.7): the 5,500–7,500 band is the
# STANDARD band (test targets viso 4–5); for marathon targets it is
# ADVISORY — what binds is the §45 floor (4,500) + gates (d)/(g), not
# band precision. The suffix text now says so explicitly. Send
# behaviour unchanged.
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


class GenerationError(RuntimeError):
    """The client call failed or returned no usable answer."""


def _log_usage(usage, isr_id, answer_chars):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": LANE_LABEL,
        "model": MODEL,
        "isr": isr_id or None,
        "usage": usage,
        "answer_chars": answer_chars,
    }
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"dashscope_provider: usage log write failed: {ex}",
              file=sys.stderr)


def _client_chat(prompt_path):
    """One raw client call under LOCKED CONFIG A. Returns the parsed
    client JSON (which carries `status` even on API errors — the
    client exits 1 on non-200 but still prints the summary)."""
    proc = subprocess.run(
        [sys.executable, CLIENT, "chat", "--model", MODEL,
         "--prompt-file", prompt_path,
         "--max-tokens", str(MAX_TOKENS),
         "--extra-json", json.dumps(EXTRA_BODY)],
        capture_output=True, text=True, timeout=660)
    try:
        return json.loads(proc.stdout)
    except ValueError:
        raise GenerationError(
            f"client chat unparseable rc={proc.returncode}: "
            f"{proc.stderr.strip()[:200]} stdout={proc.stdout[:200]}")


def generate(prompt, isr_id=None):
    """One generation through the connector client, LOCKED CONFIG A.
    Returns {text, usage, latency_s, finish_reason, reasoning_chars}.
    Every call burns per-model free-quota stock (see header); the
    response usage is logged to token-usage.jsonl."""
    with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", dir=HERE, delete=False,
            encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    try:
        result = _client_chat(prompt_path)
    finally:
        os.unlink(prompt_path)
    if result.get("status") != 200 or not (result.get("text") or "").strip():
        raise GenerationError(
            f"no usable answer: status={result.get('status')} "
            f"chars={result.get('chars')} body={str(result.get('body'))[:200]}")
    _log_usage(result.get("usage"), isr_id, len(result["text"]))
    return {"text": result["text"], "usage": result.get("usage"),
            "latency_s": result.get("latency_s"),
            "finish_reason": result.get("finish_reason"),
            "reasoning_chars": result.get("reasoning_chars")}


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
        print(f"dashscope_provider: steering applied for {isr_id}",
              file=sys.stderr)
        return (prompt + "\n\n---\nOPERATOR STEERING (priority "
                "instruction):\n" + steer)
    return prompt


def run_pipeline(prompt, isr_id=None, **score_kwargs):
    """Generate + wrap. Returns the wrap result plus generation stats.
    Sendable semantics identical to §35/§37: status OK + no surviving
    audit finding + format gate (g) LOLOS. The wrapper report strips
    the finding `span` field, so ANY audit finding means not sendable
    (deliberate fail-closed conservatism, same as the other lanes)."""
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
        print("dashscope_provider: empty prompt on stdin", file=sys.stderr)
        return 2
    isr_id = os.environ.get("DIALECTICA_ISR_ID", "").strip()
    prompt = apply_steering(prompt, isr_id) + LENGTH_SUFFIX
    try:
        result = run_pipeline(prompt, isr_id or None)
    except GenerationError as ex:
        print(f"dashscope_provider: {ex}", file=sys.stderr)
        return 1
    print(f"dashscope_provider: wrapped "
          f"status={result['status']} sendable={result['sendable']} "
          f"chars={result['report']['chars_final']} "
          f"audit_findings={len(result['report']['audit']['findings'])}",
          file=sys.stderr)
    if not result["sendable"]:
        print("dashscope_provider: draft WITHHELD (sendable=false: an "
              "audit finding survived, the format gate failed, or the "
              "length guard ended GAGAL-LANJUT). Exiting 1 with empty "
              "stdout — trued treats a nonzero provider exit as "
              "'nothing submitted' and drops the job (MEKANISME §35/§40).",
              file=sys.stderr)
        print(f"dashscope_provider: "
              f"{format_withhold_breakdown(result['report'])}",
              file=sys.stderr)
        return 1
    sys.stdout.write(result["text"] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
