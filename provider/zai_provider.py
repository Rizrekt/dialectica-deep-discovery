#!/usr/bin/env python3
"""Z.ai / glm-4.7-flash provider for Dialectica — claim lane, one-shot
--answer only (MEKANISME §40), same contract and same mandatory
wrapper as the OpenRouter/Nemotron lane (§34/§35) and the Cloudflare
lane (§37).

Wired into run_serve.py via `--zai` for `trued answer` ONLY;
background serve on this lane is refused by run_serve (exit 5) before
anything launches — serve stays on Vyce / Cloudflare §39. Bench
verdict (ZAI-BENCH-2026-11-10.md): LAYAK CADANGAN BERSYARAT — per-
successful-generation quality is competitive or better than the
existing lanes (natural in-band length, fastest success latency,
zero mojibake), but AVAILABILITY is the weakness: the free pool
saturates (HTTP 429 code 1305) and daily capacity is UNOBSERVED
(no published req/day figure, no rate-limit headers). Never the
only lane in any window until availability is proven across >=3
windows (bench condition 4).

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
(~/workspace/custom-connectors/custom.z-ai/bin/client.py); the vault
surrogate is swapped for the real API key on egress by Muse and
never touches this file or disk. Model is PINNED: glm-4.7-flash —
one of the two $0 models on Z.ai's official pricing (GLM-4.7-Flash
and GLM-4.5-Flash are $0 in every column); it does not appear in the
account's /models catalog (which lists paid models only) but is
callable, proven live 2026-11-10.

MANDATORY LANE CONDITIONS (from the bench verdict — embedded, do not
improvise):
1. THINKING DISABLED on every call (`--thinking disabled`): GLM
   Flash defaults thinking ON, and a thinking probe spent 256/256
   tokens on reasoning and returned ZERO content (the §31 disease).
2. 1305 RETRY: on HTTP 429 with error code 1305 (free-pool
   overload — not a key/billing/model error), wait ±60 s and retry
   EXACTLY ONCE per generation slot; a second 1305 (or any other
   failure) ends the slot — the lane gives up for that call. Bench
   evidence: both successful bench generations were preceded by
   exactly one 1305 + ±60 s wait; without the retry the window's
   effectiveness was ±29%.
3. STRICTLY SEQUENTIAL: this model's official concurrency limit is
   1 (user-supplied rate-limit table, 2026-11-10). Never invoke
   this provider in parallel; the one-shot pipeline is sequential
   by construction (first generation, then at most one wrapper
   regeneration).
4. Capacity accounting: every generation's success/1305 outcome is
   visible in token-usage.jsonl under lane `zai-glm47flash`; the
   success:1305 ratio per window is how this lane's effective
   capacity gets proven over time (no number is assumed).
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
    "~/workspace/custom-connectors/custom.z-ai/bin/client.py")
# PINNED (§40): the proven $0 claim-class model on this lane.
MODEL = "glm-4.7-flash"
MAX_TOKENS = 8000
# Verdict condition 2: exactly one retry after ±60 s on a 1305.
RETRY_1305_WAIT_S = 60
USAGE_LOG = os.path.join(HERE, "token-usage.jsonl")
LANE_LABEL = "zai-glm47flash"

# Same length instruction as the other lanes; this model's one
# completed bench run landed naturally in band (6,210 chars), and the
# wrapper's regeneration guard remains the second line of defence.
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
    """The client call failed (after the one allowed 1305 retry)
    or returned no usable answer."""


def _log_usage(usage, isr_id, answer_chars, retried_after_1305):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": LANE_LABEL,
        "model": MODEL,
        "isr": isr_id or None,
        "usage": usage,
        "answer_chars": answer_chars,
        "retried_after_1305": retried_after_1305,
    }
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"zai_provider: usage log write failed: {ex}",
              file=sys.stderr)


def _is_1305(result):
    """Free-pool overload: HTTP 429 + error code 1305 (the exact
    detection the bench driver used)."""
    if result.get("status") != 429:
        return False
    body = result.get("body") or {}
    return str((body.get("error") or {}).get("code", "")) == "1305"


def _client_chat(prompt_path):
    """One raw client call, thinking DISABLED (verdict condition 1).
    Returns the parsed client JSON (carries `status` even on API
    errors — the client exits 1 on non-200 but still prints it)."""
    proc = subprocess.run(
        [sys.executable, CLIENT, "chat", "--model", MODEL,
         "--prompt-file", prompt_path,
         "--max-tokens", str(MAX_TOKENS),
         "--thinking", "disabled"],
        capture_output=True, text=True, timeout=660)
    try:
        return json.loads(proc.stdout)
    except ValueError:
        raise GenerationError(
            f"client chat unparseable rc={proc.returncode}: "
            f"{proc.stderr.strip()[:200]} stdout={proc.stdout[:200]}")


def generate(prompt, isr_id=None):
    """One generation slot through the connector client: first
    attempt + EXACTLY ONE retry after ±60 s if the first attempt is
    a 1305 (verdict condition 2). Returns {text, usage, latency_s,
    finish_reason, reasoning_chars, retried_after_1305, attempts}.
    Sequential by construction (verdict condition 3)."""
    with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", dir=HERE, delete=False,
            encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    attempts = []
    retried = False
    try:
        result = _client_chat(prompt_path)
        attempts.append(result.get("status"))
        if _is_1305(result):
            print(f"zai_provider: 1305 (free pool overloaded) — "
                  f"waiting {RETRY_1305_WAIT_S}s, retrying exactly "
                  f"once", file=sys.stderr)
            time.sleep(RETRY_1305_WAIT_S)
            retried = True
            result = _client_chat(prompt_path)
            attempts.append(result.get("status"))
    finally:
        os.unlink(prompt_path)
    if result.get("status") != 200 or not (result.get("text") or "").strip():
        raise GenerationError(
            f"no usable answer after {len(attempts)} attempt(s) "
            f"(statuses={attempts}): status={result.get('status')} "
            f"chars={result.get('chars')} body={str(result.get('body'))[:200]}")
    _log_usage(result.get("usage"), isr_id, len(result["text"]), retried)
    return {"text": result["text"], "usage": result.get("usage"),
            "latency_s": result.get("latency_s"),
            "finish_reason": result.get("finish_reason"),
            "reasoning_chars": result.get("reasoning_chars"),
            "retried_after_1305": retried, "attempts": attempts}


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
        print(f"zai_provider: steering applied for {isr_id}",
              file=sys.stderr)
        return (prompt + "\n\n---\nOPERATOR STEERING (priority "
                "instruction):\n" + steer)
    return prompt


def run_pipeline(prompt, isr_id=None, **score_kwargs):
    """Generate + wrap. Returns the wrap result plus generation stats.
    Sendable semantics identical to §35/§37: status OK + no surviving
    audit finding + format gate (g) LOLOS. The wrapper report strips
    the finding `span` field, so ANY audit finding means not sendable
    (deliberate fail-closed conservatism, same as the other lanes).
    Note: each generation slot (first + any wrapper regeneration)
    carries its own single 1305 retry — the bench run that was cut
    at regeneration by a 1305 is exactly the failure this prevents
    from silently losing the draft."""
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
        print("zai_provider: empty prompt on stdin", file=sys.stderr)
        return 2
    isr_id = os.environ.get("DIALECTICA_ISR_ID", "").strip()
    prompt = apply_steering(prompt, isr_id) + LENGTH_SUFFIX
    try:
        result = run_pipeline(prompt, isr_id or None)
    except GenerationError as ex:
        print(f"zai_provider: {ex}", file=sys.stderr)
        return 1
    print(f"zai_provider: wrapped "
          f"status={result['status']} sendable={result['sendable']} "
          f"chars={result['report']['chars_final']} "
          f"audit_findings={len(result['report']['audit']['findings'])}",
          file=sys.stderr)
    if not result["sendable"]:
        print(f"zai_provider: "
              f"{format_withhold_breakdown(result['report'])}",
              file=sys.stderr)
        print("zai_provider: draft WITHHELD (sendable=false: an "
              "audit finding survived, the format gate failed, or the "
              "length guard ended GAGAL-LANJUT). Exiting 1 with empty "
              "stdout — trued treats a nonzero provider exit as "
              "'nothing submitted' and drops the job (MEKANISME §35/§40).",
              file=sys.stderr)
        return 1
    sys.stdout.write(result["text"] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
