#!/usr/bin/env python3
"""DIALECTICA_READY_CMD for the gated Vyce serve lane (2026-11-15).

Identical semantics to the §39 ready hook — exit 0 only when a
prepared answer for the Question sits in the shared serve cache —
so it IS that hook: both serve lanes share the one on-disk cache
(they never run simultaneously; the §39 pension rule swaps one for
the other), and a second implementation would only be a second
place for the semantics to drift.
"""
import sys

from cloudflare_serve_ready import main

if __name__ == "__main__":
    sys.exit(main())
