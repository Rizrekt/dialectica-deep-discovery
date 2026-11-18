"""Smoke test for the citation cleaner — v2 doctrine (2026-11-16).

v2 PRESERVES citations (the §45 floor K-1a requires >=1 URL; judging
numbers/citations belongs to the wrapper audit + semantic check) and
removes only the legacy v1 evasive note + zero-width characters.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from citation_patch import clean, NOTE

SAMPLE = """The Late Bronze Age collapse involved multiple stressors
(palynological evidence from the Sea of Galilee, Oren et al. 2020,
Journal of Archaeological Science, vol. 118, pp. 1-14). As documented at
https://example.org/fake-paper and doi:10.1234/abcd.2020.55, drought
played a role. The Ugarit letters describe invasions (see
https://en.wikipedia.org/wiki/Late_Bronze_Age_collapse for context)."""

out, hits = clean(SAMPLE)
print("REMOVED:", hits)
print("---CLEANED---")
print(out)
# Citations survive v2 — floor K-1(a) can now be met at all.
assert "https://example.org/fake-paper" in out and "10.1234" in out
assert "vol. 118" in out
# The evasive note is never appended by v2.
assert "avoids pinpoint references" not in out
# A legacy v1-cleaned text has its appended note removed on sight.
out3, hits3 = clean(SAMPLE + NOTE)
assert "avoids pinpoint references" not in out3 and "legacy-v1-note" in hits3
out2, hits2 = clean("A plain answer without any citations at all.")
assert hits2 == [] and "Note on sources" not in out2
print("CLEANER SMOKE OK")
