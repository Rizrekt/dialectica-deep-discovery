#!/usr/bin/env python3
"""DIALECTICA_READY_CMD for the temporary Cloudflare serve lane
(MEKANISME §39).

trued runs this at the offer-to-answer (bid) step with the
opportunity as JSON on stdin, inside a ~10 s window. Exit 0 only
when a prepared answer for that Question is in the serve cache —
anything else vetoes the bid (score 0), so this Expert can never win
work it has not already prepared an answer for. Pure file lookup:
no network, no generation, far inside the time window.

An EMPTY or whitespace-only cache file does NOT count as a prepared
answer (SOLUSI-39 fix B): ids are filtered through
cloudflare_serve_common.read_cache, whose semantics are exactly
that — otherwise READY would pass a bid the provider can only serve
via the live fallback.
"""
import json
import sys

import cloudflare_serve_common as csc


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    ids = {isr_id for isr_id in csc.cached_ids()
           if csc.read_cache(isr_id) is not None}
    hit = next((s for s in _strings(payload) if s in ids), None)
    if hit:
        print(f"jawaban siap untuk {hit}")
        return 0
    print("tidak ada jawaban siap untuk pertanyaan ini")
    return 1


if __name__ == "__main__":
    sys.exit(main())
