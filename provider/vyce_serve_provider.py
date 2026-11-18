#!/usr/bin/env python3
"""DIALECTICA_PROVIDER_CMD at job time for the gated Vyce serve lane
(2026-11-15).

Primary path: the answer was prepared BEFORE the claim by
vyce_serve_prepare.py and sits in the shared serve cache under
DIALECTICA_ISR_ID — print it and exit 0. No generation, no gate
re-run: the cached text is exactly the text the gate passed.

Fallback (live pipeline on the real job prompt): schema-correction
jobs — the cached text is the very thing being corrected — and
arrivals with no prepared cache entry. The fallback is gated the
same way prepare is, plus a proven-dead liveness block: when the
fetched ISR detail PROVES the target dead (serve_gate
.fallback_dead_reason), it exits 1 with empty stdout rather than
submit a post-round answer; an unverifiable fetch does not block
finishing work already accepted. A withheld fallback draft likewise
exits 1 with empty stdout — trued treats that as "nothing
submitted" and drops the job (the §35 consequence), reachable only
off the primary path.

FRESHNESS RE-CHECK (2026-11-17, aturan ketat user 10:50/10:52):
both paths pass the send-time freshness veto (freshness_gate) at
the last moment before the answer text is printed — the pick-time
screens cannot see a room that filled during generation (the
2026-11-17 pilot: 5 answers picked at viso 0, questions flooded to
23–59 answers unchecked). Armed by run_serve
(DIALECTICA_FRESHNESS_CHECK=1); a withholding verdict exits 1 with
empty stdout exactly like the proven-dead block, and an unreadable
question state withholds too (tak terverifikasi bukan lolos). A
crash of the check itself never withholds (logged instead).
"""
import os
import sys

import cloudflare_serve_common as csc
import freshness_gate
import serve_gate
import vyce_serve_common as vsc
from openrouter_wrapper import format_withhold_breakdown


def _freshness_block_reason(isr_id):
    """The withhold reason when the armed freshness veto stops
    this send, else None. Unarmed -> None (the pipe behaves exactly
    as before this layer). A non-withholding outcome (fresh, or a
    logged crash) is noted on stderr and the send proceeds."""
    veto = freshness_gate.armed_freshness_veto(isr_id)
    if veto is None:
        return None
    withhold, reason = veto()
    if withhold:
        return reason
    print(f"vyce_serve_provider: gerbang kesegaran — {reason}",
          file=sys.stderr)
    return None


def main():
    prompt = sys.stdin.read()
    isr_id = os.environ.get("DIALECTICA_ISR_ID", "").strip()
    job_kind = os.environ.get("DIALECTICA_JOB_KIND", "").strip()
    if job_kind != "correction":
        cached = csc.read_cache(isr_id)
        if cached is not None:
            # Liveness re-check on cache hit (2026-11-16, audit S5):
            # a prepared answer could otherwise be submitted after
            # its round ended when a job arrives late. Only a PROVEN
            # death blocks (fallback semantics: an unverifiable or
            # unarmed fetch proves nothing and never drops the job).
            if isr_id:
                dead = serve_gate.fallback_dead_reason(isr_id)
                if dead:
                    print(f"vyce_serve_provider: gerbang liveness "
                          f"(cache-hit) — target terbukti MATI "
                          f"({dead}). Exiting 1 with empty stdout; "
                          f"trued drops the job.", file=sys.stderr)
                    return 1
                stale = _freshness_block_reason(isr_id)
                if stale:
                    print(f"vyce_serve_provider: gerbang kesegaran "
                          f"(cache-hit) — kiriman DITAHAN ({stale}). "
                          f"Exiting 1 with empty stdout; trued "
                          f"drops the job.", file=sys.stderr)
                    return 1
            print(f"vyce_serve_provider: serving prepared answer "
                  f"for {isr_id} ({len(cached)} chars)",
                  file=sys.stderr)
            sys.stdout.write(cached + "\n")
            return 0
    if not prompt.strip():
        print("vyce_serve_provider: empty prompt and no prepared "
              "answer", file=sys.stderr)
        return 2
    if isr_id:
        dead = serve_gate.fallback_dead_reason(isr_id)
        if dead:
            print(f"vyce_serve_provider: gerbang liveness — target "
                  f"terbukti MATI ({dead}). Exiting 1 with empty "
                  f"stdout; trued drops the job rather than submit "
                  f"a post-round answer.", file=sys.stderr)
            return 1
    try:
        result = vsc.vyce_pipeline(prompt, isr_id or None)
    except Exception as ex:  # noqa: BLE001 - provider failure path
        print(f"vyce_serve_provider: {type(ex).__name__}: {ex}",
              file=sys.stderr)
        return 1
    print(f"vyce_serve_provider: fallback pipeline "
          f"status={result['status']} sendable={result['sendable']} "
          f"chars={result['report']['chars_final']}", file=sys.stderr)
    if not result["sendable"]:
        print("vyce_serve_provider: fallback draft WITHHELD by the "
              "serve gate (sendable=false). Exiting 1 with empty "
              "stdout — trued drops the job (MEKANISME §35).",
              file=sys.stderr)
        print(f"vyce_serve_provider: "
              f"{format_withhold_breakdown(result['report'])}; "
              f"alasan: {'; '.join(result['gate']['reasons'][:3])}",
              file=sys.stderr)
        return 1
    if isr_id:
        stale = _freshness_block_reason(isr_id)
        if stale:
            print(f"vyce_serve_provider: gerbang kesegaran "
                  f"(fallback) — kiriman DITAHAN ({stale}). "
                  f"Exiting 1 with empty stdout; trued drops "
                  f"the job.", file=sys.stderr)
            return 1
    sys.stdout.write(result["text"] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
