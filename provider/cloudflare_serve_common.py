#!/usr/bin/env python3
"""Shared machinery for the TEMPORARY Cloudflare serve lane
(MEKANISME §39) — the Pioneer-coverage replacement for the Vyce serve
while Vyce is in official downtime (user decision 2026-11-10 17:34:
the two prepared lanes must REPLACE Vyce in full, serve included, so
progress never waits on Vyce).

Design, taken from how `trued serve` itself works (all three seams are
the client's own, not inventions):

- DIALECTICA_PREPARE_CMD runs BEFORE any claim with the search row as
  JSON on stdin; no job exists yet, and a nonzero exit passes the
  Question over at zero cost. Generation therefore happens in the
  prepare hook (cloudflare_serve_prepare.py): a draft the wrapper
  withholds is a pass-over, never a dropped job.
- DIALECTICA_READY_CMD runs at the offer-to-answer (bid) step and
  vetoes any bid we hold no prepared answer for
  (cloudflare_serve_ready.py).
- At job time the provider (cloudflare_serve_provider.py) serves the
  prepared answer from the on-disk cache keyed by isrId; only schema
  corrections and unprepared arrivals fall back to a live pipeline.

CAP (hard): at most SERVE_CAP client generations per UTC day are ever
STARTED for serve, counted as records under lane `cloudflare-serve`
in token-usage.jsonl (the claim lane keeps its own label,
`cloudflare-gptoss`). Enforcement is BEFORE acceptance, never by
provider failure after a job exists:

- the prepare hook refuses (pass-over) when the remaining generation
  budget cannot cover a full pipeline (1 generation + at most 1
  wrapper regeneration), and runs the last pipeline with regeneration
  disabled when only one generation remains — so the count can never
  exceed the cap;
- the run_serve supervisor SIGINTs the serve process when the count
  reaches the cap (trued stops claiming and drains in-flight work —
  its own graceful shutdown) and never relaunches it;
- run_serve refuses to START serve at all when the day's cap is
  already reached, so a keyword rotation later the same day cannot
  resurrect it.

The account-wide neuron budget still applies on top: generations abort
pre-spend above 9,000 neurons summed over BOTH Cloudflare lanes (the
10,000/day platform allocation is account-wide).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_provider as cp  # noqa: E402
import serve_gate  # noqa: E402

SERVE_LANE = "cloudflare-serve"
CLAIM_LANE = cp.LANE_LABEL  # "cloudflare-gptoss"
BUDGET_LANES = (CLAIM_LANE, SERVE_LANE)
SERVE_CAP = 10
PIPELINE_MAX_GENERATIONS = 2  # 1 generation + at most 1 wrapper regen

# Core topics of the Class-2 (Pioneer) screen — the same rotation the
# Vyce serve used (agent identity -> wallet -> on-chain -> oracle ->
# rollup -> smart contract security -> token), as match keywords.
CORE_TOPIC_KEYWORDS = (
    "agent identity", "identitas agen", "identity", "wallet", "dompet",
    "on-chain", "onchain", "oracle", "rollup", "smart contract",
    "kontrak pintar", "keamanan kontrak", "token",
)


def usage_log_path():
    """token-usage.jsonl location. DIALECTICA_TOKEN_USAGE_LOG is a
    test hook for the supervisor counter; production uses the default
    (the same file cloudflare_provider writes)."""
    return os.environ.get("DIALECTICA_TOKEN_USAGE_LOG") or cp.USAGE_LOG


def iter_records(path=None):
    path = path or usage_log_path()
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def _today_utc():
    return time.strftime("%Y-%m-%d", time.gmtime())


def serve_generations_today(path=None):
    """Client generations started for serve today (UTC): one usage-log
    record per generation under the serve lane label."""
    today = _today_utc()
    return sum(
        1 for rec in iter_records(path)
        if rec.get("lane") == SERVE_LANE
        and str(rec.get("ts", "")).startswith(today))


def cache_dir():
    return os.environ.get("DIALECTICA_SERVE_CACHE_DIR") or os.path.join(
        HERE, "serve-cache")


def cache_path(isr_id):
    return os.path.join(cache_dir(), f"{isr_id}.txt")


def write_cache(isr_id, text):
    os.makedirs(cache_dir(), exist_ok=True)
    with open(cache_path(isr_id), "w", encoding="utf-8") as fh:
        fh.write(text)


def read_cache(isr_id):
    if not isr_id:
        return None
    try:
        with open(cache_path(isr_id), encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    return text if text.strip() else None


def cached_ids():
    try:
        return {name[:-4] for name in os.listdir(cache_dir())
                if name.endswith(".txt")}
    except OSError:
        return set()


def row_isr_id(row):
    return str((row or {}).get("id") or (row or {}).get("isrId") or "")


def screen_row(row):
    """Class-2 (Pioneer) screen over a search row, as far as the row
    supports it. Returns (ok, reason); reason names the failing gate.

    Supported by the row: viso count, marathon state, question text
    for the core-topic match. NOT carried by search rows (proven from
    trued.py: the client never reads one): a runtimeContext field —
    if a row ever carries one, a truthy value fails the screen; its
    absence cannot be screened here (limitation documented in §39).
    """
    row = row or {}
    if not row_isr_id(row):
        return False, "baris tanpa id/isrId"
    viso = row.get("questionVisoCount", row.get("visoCount"))
    if viso is not None and viso != 0:
        return False, f"viso {viso} — bukan pertanyaan viso-0 (Pioneer)"
    if row.get("questionMarathonActive"):
        return False, "marathonActive — di luar cakupan Pioneer serve"
    for key in ("runtimeContext", "runtime", "requiresRuntime"):
        if row.get(key):
            return False, f"{key} terisi — menuntut runtime, dilewati"
    text = (str(row.get("title") or "") + "\n"
            + str(row.get("content") or "")).strip()
    if not text:
        return False, "baris tanpa judul/konten pertanyaan"
    low = text.lower()
    if not any(kw in low for kw in CORE_TOPIC_KEYWORDS):
        return False, "di luar topik inti (identitas/wallet/on-chain/" \
                      "oracle/rollup/keamanan kontrak/token)"
    return True, "lolos saringan Kelas 2"


def prompt_from_row(row):
    title = str((row or {}).get("title") or "").strip()
    content = str((row or {}).get("content") or "").strip()
    parts = ["Pertanyaan Dialectica (arena general, diajukan pengguna "
             "lain):"]
    if title:
        parts.append(title)
    if content and content != title:
        parts.append(content)
    return "\n\n".join(parts)


def serve_pipeline(prompt, isr_id=None, allow_regen=True,
                   target_class=None):
    """Generate + gate for serve, recorded under the serve lane.

    Since 2026-11-15 the wrap step is the SHARED serve gate
    (serve_gate.gate_answer): the claim wrapper's sendable semantics
    of §35/§37 (status OK + no surviving audit finding + format gate
    (g) LOLOS) PLUS the thinking-trace layer, so a raw reasoning
    monologue can never be cached or submitted by this lane (the
    f0bb3586 species, §82). The claim pipeline is untouched. The
    liveness layer of the gate lives in the prepare hook (before any
    claim) and in the provider fallback — see serve_gate.py.

    `target_class` ((c)-PK1, 2026-11-17): the picker's class when
    the caller has one; selects the gate's per-class length floor.
    None keeps the operative default floor exactly as before.
    """
    first = cp.generate(prompt, isr_id, lane=SERVE_LANE,
                        budget_lanes=BUDGET_LANES)
    generations = [first]

    def regen(instruction):
        again = cp.generate(prompt + instruction, isr_id,
                            lane=SERVE_LANE, budget_lanes=BUDGET_LANES)
        generations.append(again)
        return again["text"]

    result = serve_gate.gate_answer(
        first["text"], regen_fn=regen if allow_regen else None,
        target_class=target_class)
    result["generations"] = generations
    return result
