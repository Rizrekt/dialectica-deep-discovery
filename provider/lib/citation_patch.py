"""Citation cleaner for Dialectica answers — v2 (2026-11-16).

v1 (2026-11-08) stripped EVERY URL and DOI from a generated answer,
killed any parenthetical containing words like "vol."/"et al"/a year,
and — when anything was stripped — appended a fixed closing note:
"Note on sources: this answer relies on widely documented ... and it
avoids pinpoint references that cannot be verified from the text
alone."

That design predates two later, binding rules and is now proven to be
self-sabotage:

1. The §45/T12 mechanical floor (K-1a) REQUIRES >=1 URL in the sent
   text. v1 guaranteed 0 URLs on every answer it touched: all 26
   historical serve answers measured 0 URLs in the 2026-11-15 gate
   backtest, and 22/22 failed K-1(a).
2. Lab 2026-11-15 ADOPTED E3: that exact appended note is the
   evasive-source-closing species carried by 4/4 falsified serve
   answers (f0bb3586, 7d81c51d, 5b5e8212, a3b8b34a). It was never the
   model's closing — v1 appended it deterministically. The serve
   gate now hard-withholds any draft carrying it, so a v1-cleaned
   draft could never pass the gate its own pipeline feeds.

v2 therefore does the opposite of v1 on citations: it PRESERVES the
answer exactly as generated — URLs, DOIs, named references and
parenthetical citations included. Judging numbers and citations is
the wrapper's job (openrouter_wrapper.audit_numbers removes only
number tokens bound to a named document with a wrong/unverifiable
value, span by span), and judging support is the semantic check's
job. A blanket stripper cannot tell a real citation from a fake one,
and "strip everything" is a guaranteed floor failure, not a fence.

What v2 still does, defensively:
- removes the legacy v1 NOTE verbatim when it is present (an answer
  regenerated or cached from a v1-cleaned text must not carry the
  E3 closing into the gate);
- removes zero-width characters (U+200B-U+200D, U+2060, U+FEFF)
  sometimes used to smuggle tail insertions past visual review.

`clean(answer)` keeps the v1 signature: returns (text, hits) where
hits lists what was actually removed.
"""
import re

# The v1 appended note, verbatim — removed on sight in v2.
NOTE = ("\n\nNote on sources: this answer relies on widely documented, "
        "independently checkable public records and scholarship rather than "
        "on any single citation, and it avoids pinpoint references that "
        "cannot be verified from the text alone.")
_NOTE_BARE = NOTE.strip()
_ZERO_WIDTH = re.compile("[​-‍⁠﻿]")


def clean(answer):
    hits = []
    out = answer or ""
    if _NOTE_BARE in out:
        hits.append("legacy-v1-note")
        out = out.replace(_NOTE_BARE, "").rstrip() + "\n"
    zw = _ZERO_WIDTH.findall(out)
    if zw:
        hits.append("zero-width x%d" % len(zw))
        out = _ZERO_WIDTH.sub("", out)
    return out, hits
