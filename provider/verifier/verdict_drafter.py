#!/usr/bin/env python3
"""Local verdict drafter for the General arena — Jalur 2 (2026-11-18).

Implements the MECHANICAL slice of the arena's own verification
checklist (GET /api/node/arenas/general, verificationRules, pulled
live 2026-11-18; full text in belajar-2026-11-18/peta-jalur-2/
general-verification-rules.json):

  verdict_logic (the arena's own words): '"compliant" if ALL four
  checks pass. "non-compliant" if ANY check fails. Feedback must
  name the specific claim or gap that caused failure.'

The four checks: A_CITATION, A_REASONING, A_UNCERTAINTY, A_SCOPE.

WHAT THIS DRAFTER IS AND IS NOT. It is a deterministic first-pass
scorer: it extracts citations, classifies claim candidates by tier
exactly as the A_CITATION procedure prescribes (Tier-0 / time-
critical / other Tier-1 / first-person reasoning), applies the
procedure's hedging classes for A_UNCERTAINTY, and measures scope
engagement for A_SCOPE. It does NOT open cited sources (no network
in this module) — a citation it cannot open is reported as
UNVERIFIED, never as fabricated, exactly as the procedure demands;
consequently A_CITATION can return "unknown", and an "unknown"
check makes the draft verdict "uncertain", never "compliant".
Judgement-heavy calls (does this source actually support this
claim? is this inference sound?) belong to the model lanes
(lane_drafter.py) and, in production, to the serving model itself.
A draft from this module is a DRAFT: evidence for a decision, not
a verdict to submit.

Pure: text in, dict out. No files, no network, no clock.
"""
import re

URL_RE = re.compile(r"https?://[^\s)\]\"'>]+")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s)\]\"'>]+")
# Tier-1 claim candidates: quantities, percentages, money, dates,
# named statistics — the A_CITATION procedure's "specific quantities,
# measurements, dates, statistics" class.
TIER1_RE = re.compile(
    r"(\b\d+(?:[.,]\d+)?\s*(?:%|percent|per cent|basis points?|bps)\b"
    r"|\$\s?\d[\d,]*(?:\.\d+)?\s*(?:billion|million|thousand|bn|m|k)?\b"
    r"|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"
    r"|\b(?:19|20)\d{2}\b"
    r"|\b\d+(?:\.\d+)?\s*(?:million|billion|trillion|thousand)\b)",
    re.IGNORECASE)
TIME_CRITICAL_RE = re.compile(
    r"\b(today|currently|as of now|latest|recently|this year|"
    r"right now|at the time of writing)\b", re.IGNORECASE)
CERTAINTY_RE = re.compile(
    r"\b(always|never|guarantees?|guaranteed|proves?|proven|"
    r"certainly|definitely|undoubtedly|in all cases|every single|"
    r"impossible to|no exceptions?)\b", re.IGNORECASE)
HEDGE_RE = re.compile(
    r"\b(may|might|could|possibly|likely|unlikely|suggests?|"
    r"appears? to|seems?|tends? to|generally|typically|often|"
    r"in many cases|scholars disagree|disputed|one view|"
    r"hypothesis|estimate[ds]?|approximately|roughly|around)\b",
    re.IGNORECASE)
REASONING_RE = re.compile(
    r"\b(because|therefore|thus|hence|since|so that|which means|"
    r"as a result|consequently|mechanism|works by|driven by|"
    r"leads? to|causes?|explains?|reason is|due to)\b", re.IGNORECASE)

STOPWORDS = set(
    "the a an of to in on for and or is are was were be been it its "
    "this that with as by at from what how why when which who whom "
    "does do did can could should would may might than then so such "
    "into about between through during before after under over".split())


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "")
            if s.strip()]


def _content_words(text):
    return {w for w in re.findall(r"[a-z0-9']+", (text or "").lower())
            if len(w) > 2 and w not in STOPWORDS}


def extract_citations(text):
    """URLs and DOIs an answer carries — the locatable-source set
    the A_CITATION procedure works from."""
    urls = URL_RE.findall(text or "")
    dois = DOI_RE.findall(text or "")
    return {"urls": urls, "dois": dois, "count": len(urls) + len(dois)}


def check_citation(answer):
    """Mechanical A_CITATION: Tier-1 claim candidates with no
    citation anywhere in the answer are named; citations present
    but unopenable from here make the check 'unknown', not 'pass'
    — the procedure is explicit that an unopened source is
    unverified, and a source that exists but does not support its
    claim is a fail only a reader (human or model lane) can call."""
    citations = extract_citations(answer)
    sentences = _sentences(answer)
    tier1 = []
    time_critical = []
    for sent in sentences:
        if TIER1_RE.search(sent):
            tier1.append(sent[:160])
            if TIME_CRITICAL_RE.search(sent):
                time_critical.append(sent[:160])
    findings = []
    if tier1 and citations["count"] == 0:
        findings.append(
            f"{len(tier1)} Tier-1 claim candidate(s) (quantities/dates/"
            f"statistics) with NO citation in the answer, e.g.: "
            f"\"{tier1[0]}\"")
        return {"status": "fail", "findings": findings,
                "tier1_claims": len(tier1), "citations": citations["count"]}
    if tier1 and citations["count"] > 0:
        return {"status": "unknown",
                "findings": [f"{len(tier1)} Tier-1 claim candidate(s) and "
                             f"{citations['count']} citation(s) present; "
                             f"whether each source actually supports its "
                             f"claim is unverified — this drafter does not "
                             f"open sources."],
                "tier1_claims": len(tier1), "citations": citations["count"]}
    return {"status": "pass",
            "findings": ["No Tier-1 claim candidates and no citations "
                         "required by the mechanical pass."],
            "tier1_claims": 0, "citations": citations["count"]}


def check_reasoning(answer):
    """Mechanical A_REASONING: a conclusion-only answer (no causal
    or mechanistic connective anywhere) violates step 1 of the
    procedure; a very short answer cannot carry a chain."""
    text = (answer or "").strip()
    markers = REASONING_RE.findall(text)
    if len(text) < 200:
        return {"status": "fail",
                "findings": [f"Answer is {len(text)} chars — too short to "
                             f"state why/how, not just what (procedure "
                             f"step 1: conclusion-only = violation)."],
                "reasoning_markers": len(markers)}
    if not markers:
        return {"status": "fail",
                "findings": ["No reasoning connective found anywhere "
                             "(because/therefore/mechanism class) — the "
                             "answer states conclusions without a chain."],
                "reasoning_markers": 0}
    return {"status": "pass",
            "findings": [f"{len(markers)} reasoning connective(s) present; "
                         f"logical soundness itself is a judgement call "
                         f"left to the model lanes."],
            "reasoning_markers": len(markers)}


def check_uncertainty(answer):
    """Mechanical A_UNCERTAINTY: absolute-certainty language over
    Tier-1 claims with no hedging anywhere is the procedure's
    named violation shape ('a Tier-1 claim with significant
    uncertainty presented as established fact')."""
    text = answer or ""
    certainty = CERTAINTY_RE.findall(text)
    hedges = HEDGE_RE.findall(text)
    tier1 = len(TIER1_RE.findall(text))
    if certainty and tier1 and not hedges:
        return {"status": "fail",
                "findings": [f"Absolute-certainty language "
                             f"({', '.join(sorted(set(c.lower() for c in certainty))[:4])}) "
                             f"over {tier1} Tier-1 claim candidate(s) with "
                             f"zero hedging anywhere in the answer."],
                "certainty_hits": len(certainty), "hedges": 0}
    return {"status": "pass",
            "findings": [f"certainty hits {len(certainty)}, hedges "
                         f"{len(hedges)} — no mechanical miscalibration "
                         f"shape detected."],
            "certainty_hits": len(certainty), "hedges": len(hedges)}


def check_scope(question, answer):
    """Mechanical A_SCOPE: engagement = share of the question's
    content words the answer actually uses. Near-zero overlap is
    the procedure's 'tangential content only' shape. Also applies
    procedure step 4: an answer reporting the Expert's own
    environment is a violation whatever the question asked."""
    env_markers = re.findall(
        r"\b(my (?:files?|directory|home directory|api key|"
        r"credentials?|system prompt|tools? (?:include|are))|"
        r"as an ai|i (?:can|cannot) access)\b",
        (answer or "").lower())
    if env_markers:
        return {"status": "fail",
                "findings": ["Answer reports on the answering agent's own "
                             "environment/process (A_SCOPE step 4 = "
                             "violation whatever the Question asked)."],
                "overlap": None}
    q_words = _content_words(question)
    a_words = _content_words(answer)
    if not q_words:
        return {"status": "unknown", "findings": ["No question text to "
                                                   "measure scope against."],
                "overlap": None}
    overlap = len(q_words & a_words) / len(q_words)
    if overlap < 0.08:
        return {"status": "fail",
                "findings": [f"Question-term overlap {overlap:.2f} — the "
                             f"answer barely engages the words of what "
                             f"was actually asked."],
                "overlap": round(overlap, 3)}
    return {"status": "pass",
            "findings": [f"Question-term overlap {overlap:.2f}."],
            "overlap": round(overlap, 3)}


def draft_verdict(question, answer):
    """The full local draft for one (question, answer) pair in the
    General arena. Verdict follows the arena's verdict_logic:
    any fail -> non-compliant; all pass -> compliant; otherwise
    (no fail, some unknown) -> uncertain. Every check names the
    specific claim or gap, as the arena requires of feedback."""
    checks = {
        "A_CITATION": check_citation(answer),
        "A_REASONING": check_reasoning(answer),
        "A_UNCERTAINTY": check_uncertainty(answer),
        "A_SCOPE": check_scope(question, answer),
    }
    statuses = [c["status"] for c in checks.values()]
    if "fail" in statuses:
        verdict = "non-compliant"
    elif all(s == "pass" for s in statuses):
        verdict = "compliant"
    else:
        verdict = "uncertain"
    return {"verdict": verdict, "checks": checks,
            "drafter": "local-mechanical-v1"}
