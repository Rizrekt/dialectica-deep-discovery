#!/usr/bin/env python3
"""Offline audit of a SENT draft (the reveal text) — §7.1 butir 3.

MEKANISME §50/EVALUASI §7.1(3): the regime's structural defect was
that gates scored the PROBE draft while the one-shot path re-rolled
inside `trued answer`, so the SENT text was never the gated text.
This tool is the verdict-watch half of the fix: given the revealed
text of a submitted answer (fetched from the ISO after submit), it
re-scores that exact text against QUALITY.md **v2**:

- (a)–(g): the wrapper's mechanical rubric (openrouter_wrapper),
  with (d) recomputed from the number audit + §45 floor over the
  sent text itself (no patching — this tool never modifies text);
- (h) BARU (pintu mati): sub-question coverage. Needs the question's
  sub-questions, one per line, in a --subquestions file (a phrase or
  keyword set per line). A sub-question counts as covered when
  >=60% of its significant words appear in the sent text AND at
  least one of them appears inside a numbered ## section body.
  Without the file, (h) is N-A (manual) — never silently LOLOS.
  Caveat: matching is literal word overlap, so write the
  sub-question keywords in the ANSWER's language (verified
  2026-11-11: an English keyword list against an Indonesian answer
  scored 0/3 on a fully-covering text; the same list in Indonesian
  scored 3/3, and a definitions-only species-C text failed (h)+(i)).
- (i) BARU: empirical-evidence standard. Mechanical proxy: at least
  one world number BOUND to a citation (within ±150 chars, the §45
  K-2 definition). Definitions alone (Goodhart/Campbell/MAPE/HACCP
  with no bound world fact) score bound=0 -> GAGAL. The proxy does
  NOT replace the manual open-and-read entailment check (E1): a
  bound number whose citation does not state it still fails (d)
  on manual review.

Read-only and offline: no generation, no network, no submit.
Usage:
  python3 audit_sent_draft.py <sent-text-file> \
      [--subquestions <file>] [--expected-sections N] [--json]

Exit: 0 = (h) and (i) not GAGAL; 1 = (h) or (i) GAGAL (per §7.1(3)
the NEXT claim is blocked until steering is fixed); 2 = usage error.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from openrouter_wrapper import (  # noqa: E402
    RUBRIC_LABELS, audit_numbers, mechanical_floor, score_rubric)

STOPWORDS = {
    "yang", "dan", "atau", "dari", "dengan", "untuk", "pada", "dalam",
    "adalah", "bagaimana", "mengapa", "apakah", "sebutkan", "jelaskan",
    "the", "and", "or", "of", "to", "in", "on", "for", "with", "what",
    "how", "why", "which", "does", "do", "is", "are", "a", "an",
}


def significant_words(phrase):
    words = re.findall(r"[a-z0-9][a-z0-9\-]*", phrase.lower())
    return [w for w in words if len(w) > 3 and w not in STOPWORDS]


def section_bodies(text):
    """Split text into (header, body) per numbered ## section, plus
    the pre-header preamble as header ''."""
    parts = re.split(r"(?m)^(##\s+\d+[^\n]*)$", text)
    out = [("", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i], parts[i + 1] if i + 1 < len(parts) else ""))
    return out


def score_coverage(text, subquestions):
    """(h): per-sub-question coverage detail + verdict."""
    low = text.lower()
    bodies = [(h, b.lower()) for h, b in section_bodies(text)]
    details = []
    for sub in subquestions:
        words = significant_words(sub)
        if not words:
            details.append({"sub": sub, "covered": False,
                            "reason": "tanpa kata signifikan"})
            continue
        present = [w for w in words if w in low]
        frac = len(present) / len(words)
        in_section = any(
            any(w in body for w in present)
            for header, body in bodies if header)
        covered = frac >= 0.6 and in_section
        details.append({
            "sub": sub, "covered": covered,
            "words": f"{len(present)}/{len(words)}",
            "in_numbered_section": in_section,
        })
    if not subquestions:
        return ("N-A", "tidak ada daftar sub-pertanyaan — cek manual "
                "wajib (jangan anggap lolos)"), details
    fails = [d for d in details if not d["covered"]]
    status = "GAGAL" if fails else "LOLOS"
    note = (f"{len(details) - len(fails)}/{len(details)} sub-pertanyaan "
            f"tercakup dalam seksi bernomor"
            + (f"; GAGAL: {[d['sub'][:60] for d in fails]}" if fails
               else ""))
    return (status, note), details


def score_evidence(text):
    """(i): empirical-evidence proxy from the §45 floor metrics."""
    floor = mechanical_floor(text)
    bound = floor["bound_numbers"]
    status = "LOLOS" if bound >= 1 else "GAGAL"
    note = (f"{bound} angka dunia terikat sitasi (±150 kar, K-2); "
            f"URL {floor['url_count']}, rasio terikat "
            f"{floor['bound_ratio']}"
            + ("" if bound >= 1 else
               " — definisi konsep saja TIDAK cukup (v2 (i))")
            + "; entailment sitasi→angka tetap cek manual buka-dan-baca "
              "(E1)")
    return (status, note), floor


def audit_sent(text, subquestions=(), expected_sections=6,
               needs_json=False):
    score = score_rubric(text, expected_sections=expected_sections,
                         needs_json=needs_json)
    findings = audit_numbers(text)
    floor = mechanical_floor(text)
    score["d"] = (
        "LOLOS" if not findings and floor["passed"] else "GAGAL",
        f"{len(findings)} temuan audit angka atas teks terkirim, "
        f"lantai §45 {'lolos' if floor['passed'] else 'GAGAL: ' + '; '.join(floor['failures'])}")
    score["h"], cov_details = score_coverage(text, list(subquestions))
    score["i"], _ = score_evidence(text)
    return {"score": score, "floor": floor,
            "audit_findings": [{k: v for k, v in f.items() if k != "span"}
                               for f in findings],
            "coverage": cov_details, "chars": len(text)}


def main(argv):
    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else None
    optvals = {opt(n) for n in ("--subquestions", "--expected-sections")
               if opt(n)}
    args = [a for a in argv
            if not a.startswith("--") and a not in optvals]
    if len(args) != 1:
        print(__doc__)
        return 2
    with open(args[0], encoding="utf-8") as fh:
        text = fh.read()
    subquestions = []
    if opt("--subquestions"):
        with open(opt("--subquestions"), encoding="utf-8") as fh:
            subquestions = [ln.strip() for ln in fh if ln.strip()]
    expected = int(opt("--expected-sections") or 6)
    res = audit_sent(text, subquestions, expected_sections=expected)
    if "--json" in argv:
        print(json.dumps(
            {"chars": res["chars"], "floor": res["floor"],
             "audit_findings": res["audit_findings"],
             "coverage": res["coverage"],
             "rubric": {k: list(v) for k, v in res["score"].items()}},
            ensure_ascii=False, indent=2))
    else:
        print(f"AUDIT DRAF TERKIRIM — RUBRIK v2 — {args[0]} "
              f"({res['chars']} karakter)")
        for item in "abcdefghi":
            status, note = res["score"][item]
            print(f"({item}) {RUBRIC_LABELS[item]}: {status} — {note}")
        blocked = any(res["score"][i][0] == "GAGAL" for i in ("h", "i"))
        print("VONIS (h)/(i): " + (
            "BLOKIR klaim berikutnya sampai steering diperbaiki "
            "(§7.1 butir 3)" if blocked else
            "tidak ada blokir (h)/(i) — (h) N-A tetap butuh cek manual "
            "bila tanpa daftar sub-pertanyaan"))
    return 1 if any(res["score"][i][0] == "GAGAL"
                    for i in ("h", "i")) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
