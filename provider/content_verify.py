#!/usr/bin/env python3
"""Content verification for Dialectica serve drafts — the
CONTENT VERIFY layer (built 2026-11-17, user decision 2026-11-17
21:52 "Opsi A — bangun lapis verifikasi isi dua tahap sekarang",
executing the strict-verification rule of 2026-11-17 10:50: claim
content must be verified against source content, not only judged
as a pattern).

WHY THIS LAYER EXISTS. Two earlier layers leave one species
untouched:

- citation_verify proves every pointer EXISTS and, for registry
  pinpoints, names the document the draft claims. It never reads
  whether the source's CONTENT supports the claim attached to it.
- C5 (serve_gate.semantic_check) is a pattern mimic: it judges
  text, it does not open sources.

The species that passes both is the Hop Protocol case in pilot
draft 2777178d (SPOTCHECK-PILOT-2026-11-17.md §1): the draft states
Hop's 2022 sybil scheme as "self-report to keep 50% of their
would-be allocation, while bounty hunters earned 10%", citing the
LIVE docs.hop.exchange. The documented figures are different (Hop
hunters were promised 25%; the self-report-keep scheme is
LayerZero's, at 15%). Source alive, pointer fine, figures simply
NOT IN the source — and this poison (calibration racun #1) escaped
every pattern checker in two calibrations. This layer closes the
gap by comparing CLAIM CONTENT against SOURCE CONTENT.

HOW IT WORKS — TWO STAGES.

Stage 1 (mechanical): the draft is split into sentences; a
PIVOTAL CLAIM is a sentence carrying >=1 PRECISION TOKEN (a
percentage, a decimal, a thousands-grouped number, a currency
amount, a full date, a spelled-out percent) — bare years and bare
integers are WEAK tokens, recorded but never the sole basis of a
conviction — paired with a citation pointer in the same sentence
or the same paragraph block (pointer extraction reuses
citation_verify.extract_pointers). For each pair the source text
is fetched through the SAME fetcher the citation layer uses and
every precision token is normalised (digit/word forms, thousand
separators, % variants) and searched in the source text. A STRONG
token that is absent is a STAGE-1 PIVOTAL FINDING (candidate
fatal). A source that cannot be fetched for a pivotal claim
(bot-wall 401/403/429, 5xx, connection failure, dead host — or an
HTTP-200 CAPTCHA/challenge/access-denial interstitial, a bot-wall
in disguise) puts the claim in the UNVERIFIABLE class of its
own — never silently treated as supported (the citation layer
separately owns dead pointers; this layer records the class and
moves on).

Stage 2 (entailment): pairs that are ambiguous — a stage-1 finding
that deserves an appeal (the source may state the figure in words,
in a table, or as an equivalent form the normaliser missed), or a
pivotal claim whose tokens are present but whose support is the
precedent/novelty anchor of the answer — are sent, claim +
relevant source excerpt, to Nemotron over OUR OWN checker
transport (serve_gate.default_semantic_model_call: OpenRouter
primary with its reserve guard, Vyce fallback). This layer NEVER
routes through CrowLLM or any third-party relay: the internal
gate prompt stays on our own lane. Verdicts: supported /
unsupported / unclear. A "supported" verdict is trusted ONLY with
an evidence quote that re-verifies verbatim against the fetched
source text (the C5 doctrine — the model's word alone is never
evidence); without a verifiable quote it degrades to "unclear".
"unsupported" on a pivotal claim is FATAL. "unclear" is a recorded
finding, never a withhold on its own. Stage 2 is budget-capped at
MAX_STAGE2_CALLS calls per draft (default 6: a serve draft carries
only a handful of pivotal precision claims; the cap binds the
runaway case, and every skipped pair is reported, not silent).

WITHHOLD RULE (mode "block", this layer's default — same doctrine
as citation_verify): the draft is withheld when >=1 pivotal claim
ends UNSUPPORTED (stage-1 strong-token absence not rescued by
stage 2, or a stage-2 unsupported verdict). Unverifiable claims,
unclear verdicts, unbound precision claims (a figure with no
pointer at all — C5's S-1 territory, recorded here, owned there)
and weak-token absences are recorded findings only.

CHECKER-FAILURE RULE (mirrors the house doctrine — an unrun check
never masquerades as a passed one, a dead checker never kills a
good draft): egress canary down -> verdict "unverified",
available=False, nothing blocked; every pivotal claim unverifiable
-> "unverified", loud, no block; stage-2 lane down -> stage-1
verdicts stand (recorded in `error`), the run is still performed.

HARD BOUNDARIES (stated in the build report): claims WITHOUT a
precision token (pure paraphrase / qualitative support) are out of
scope — this layer cannot see them; sources behind bot-walls are
unverifiable, not supported; the fetched text is the landing page
the pointer names (a docs homepage cited for a deep claim is
judged as what it is — that is the A_CITATION rule, applied
mechanically); stage 2 inherits the checker's own failure modes.

ARMING (same pattern as the other layers): the stage runs only
when the launcher sets DIALECTICA_CONTENT_CHECK=1 (run_serve does,
for the gated Vyce serve). Mode comes from
DIALECTICA_CONTENT_MODE: "shadow" logs and never withholds;
anything else (including unset) is "block".

Every run appends one record to content-check-log.jsonl. The
fetcher and the model call are the test seams: unit tests inject
deterministic fakes, calibration injects the real ones.
"""
import html as html_mod
import json
import os
import re
import sys
import time
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citation_verify as cv  # noqa: E402  (pointer parser + fetcher)

CONTENT_ARM_ENV = "DIALECTICA_CONTENT_CHECK"
CONTENT_MODE_ENV = "DIALECTICA_CONTENT_MODE"
CONTENT_LOG = os.path.join(HERE, "content-check-log.jsonl")

# Stage-2 budget per draft. A serve draft's pivotal precision
# claims are few (the pilot drafts carry 1-4); 6 covers the real
# distribution with headroom while bounding checker cost/latency
# on a pathological draft. Skips past the cap are reported.
MAX_STAGE2_CALLS = 6
_EXCERPT_CHARS = 6000
_EXCERPT_WINDOW = 700

_CANARY_URLS = cv._CANARY_URLS


def content_mode():
    """DIALECTICA_CONTENT_MODE: "shadow" = log-only, never
    withholds; anything else (including unset) is "block" — the
    accepted default for the mechanical layers (user 2026-11-17
    10:39 doctrine, extended to this layer by the 21:52 decision)."""
    return "shadow" if os.environ.get(
        CONTENT_MODE_ENV, "").strip().lower() == "shadow" else "block"


# ------------------------------------------------------------ tokens

_WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
    "ninety": 90,
}

_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5,
    "june": 6, "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12, "jan": 1, "feb": 2, "mar": 3,
    "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
}
_MONTH_FULL = ["january", "february", "march", "april", "may",
               "june", "july", "august", "september", "october",
               "november", "december"]

_PCT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s?%")
_PCT_WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(_WORD_NUMBERS, key=len, reverse=True))
    + r")\s+(?:percent|per\s?cent)\b", re.IGNORECASE)
_DECIMAL_RE = re.compile(r"(?<![\d.,])(\d+\.\d+)(?![\d])")
_GROUPED_RE = re.compile(r"\b(\d{1,3}(?:,\d{3})+)\b")
_CURRENCY_RE = re.compile(r"[$€£]\s?(\d[\d.,]*)")
_DATE_MDY_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+(\d{1,2}),?\s+"
    r"((?:19|20)\d{2})\b")
_DATE_DMY_RE = re.compile(
    r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|"
    r"August|September|October|November|December)\s+"
    r"((?:19|20)\d{2})\b")
_DATE_ISO_RE = re.compile(r"\b((?:19|20)\d{2})-(\d{2})-(\d{2})\b")
_YEAR_RE = re.compile(r"\b((?:19|20)\d{2})\b")
_BARE_INT_RE = re.compile(r"(?<![\d.,/])(\d{3,})(?![\d])")
# Identifiers that merely LOOK numeric (RFC 5233, BIP-32, EIP-1559,
# ePrint 2020/940, arXiv ids, section numbers) are pointers or
# labels, not figures: spans matching these are masked before the
# weak-token pass so they never become "claims".
_IDENT_MASK_RE = re.compile(
    r"(?:RFC|BIP|EIP|ERC|NIP|SLIP|ISO|IEEE|ANSI)[-\s]?\d+"
    r"|ePrint\s+\d{4}/\d{1,4}|arXiv:\s*\d{4}\.\d{4,5}"
    r"|10\.\d{4,9}/\S+|§\s?\d+", re.IGNORECASE)
_PRECEDENT_MARKERS = ("precedent", "reference case", "canonical",
                      "clearest", "landmark", "the first ")


class PrecisionToken:
    def __init__(self, raw, kind, canonical, strong, span):
        self.raw = raw
        self.kind = kind        # percent|decimal|grouped|currency|
        #                         date|year|integer
        self.canonical = canonical
        self.strong = strong
        self.span = span
        self.found = None       # True/False after the source check
        self.matched_as = None

    def as_dict(self):
        return {"raw": self.raw, "kind": self.kind,
                "canonical": self.canonical, "strong": self.strong,
                "found": self.found, "matched_as": self.matched_as}


def _num_variants(value_str):
    """Accepted surface forms of one numeric value in source text:
    the digit string as-is, the decimal-comma form, and the
    separator-stripped digit string."""
    forms = {value_str}
    if "." in value_str:
        forms.add(value_str.replace(".", ","))
    if "," in value_str:
        forms.add(value_str.replace(",", "."))
        forms.add(value_str.replace(",", ""))
    return forms


def extract_precision_tokens(sentence):
    """Precision tokens of one sentence, strong first. Spans are
    relative to the sentence. Overlapping weaker matches inside a
    stronger one are dropped."""
    found = []
    taken = []

    def free(span):
        return all(span[1] <= s or span[0] >= e for s, e in taken)

    def add(raw, kind, canonical, strong, span):
        if free(span):
            found.append(PrecisionToken(raw, kind, canonical, strong,
                                        span))
            taken.append(span)

    for m in _DATE_MDY_RE.finditer(sentence):
        iso = (f"{m.group(3)}-{_MONTHS[m.group(1).lower()]:02d}-"
               f"{int(m.group(2)):02d}")
        add(m.group(0), "date", iso, True, m.span())
    for m in _DATE_DMY_RE.finditer(sentence):
        iso = (f"{m.group(3)}-{_MONTHS[m.group(2).lower()]:02d}-"
               f"{int(m.group(1)):02d}")
        add(m.group(0), "date", iso, True, m.span())
    for m in _DATE_ISO_RE.finditer(sentence):
        add(m.group(0), "date", m.group(0), True, m.span())
    for m in _PCT_RE.finditer(sentence):
        value = m.group(1).replace(",", ".")
        add(m.group(0), "percent", value, True, m.span())
    for m in _PCT_WORD_RE.finditer(sentence):
        add(m.group(0), "percent",
            str(float(_WORD_NUMBERS[m.group(1).lower()])), True,
            m.span())
    for m in _CURRENCY_RE.finditer(sentence):
        add(m.group(0), "currency", m.group(1).replace(",", ""),
            True, m.span())
    for m in _GROUPED_RE.finditer(sentence):
        add(m.group(0), "grouped", m.group(1).replace(",", ""), True,
            m.span())
    for m in _DECIMAL_RE.finditer(sentence):
        add(m.group(0), "decimal", m.group(1), True, m.span())
    # Weak pass over an identifier-masked copy: bare years and bare
    # integers >=100. They are recorded and checked, but a weak
    # absence alone never convicts (years saturate bibliographies).
    masked = list(sentence)
    for m in _IDENT_MASK_RE.finditer(sentence):
        for i in range(m.start(), m.end()):
            masked[i] = " "
    rest = "".join(masked)
    for m in _YEAR_RE.finditer(rest):
        add(m.group(0), "year", m.group(1), False, m.span())
    for m in _BARE_INT_RE.finditer(rest):
        add(m.group(0), "integer", m.group(1), False, m.span())
    found.sort(key=lambda t: t.span[0])
    return found


# ------------------------------------------------------------ source text

def html_to_text(raw):
    """Crude but deterministic HTML -> text: drop script/style,
    tags become spaces, entities unescaped, whitespace collapsed.
    JSON registry payloads pass through nearly untouched."""
    if not raw:
        return ""
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ",
               raw)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html_mod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _fold(text):
    """Case/accent fold for matching: NFKD, strip combining marks,
    lowercase. Matching runs on folded text on both sides."""
    s = unicodedata.normalize("NFKD", text or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def _token_present(token, folded_source):
    """Is this claim token present in the folded source text?
    Returns the matched surface form or None. Percent tokens
    require a percent context in the source (a bare '50' proves
    nothing); grouped/integer tokens require a standalone digit
    run; dates accept MDY / DMY / ISO surface forms."""
    kind, canon = token.kind, token.canonical
    if kind == "percent":
        value = canon.rstrip("0").rstrip(".") if "." in canon \
            else canon
        for form in _num_variants(value):
            if re.search(re.escape(form) + r"\s?%", folded_source):
                return form + "%"
            if re.search(re.escape(form) +
                         r"\s+(?:percent|per cent)\b", folded_source):
                return form + " percent"
        for word, val in _WORD_NUMBERS.items():
            if str(float(val)) == canon or str(val) == canon:
                if re.search(r"\b" + word +
                             r"\s+(?:percent|per cent)\b",
                             folded_source):
                    return word + " percent"
        return None
    if kind == "date":
        year, month, day = canon.split("-")
        month_name = _MONTH_FULL[int(month) - 1]
        forms = [canon,
                 f"{month_name} {int(day)}, {year}",
                 f"{int(day)} {month_name} {year}"]
        for form in forms:
            if form in folded_source:
                return form
        return None
    if kind in ("decimal", "currency"):
        for form in _num_variants(canon):
            if re.search(r"(?<![\d.,])" + re.escape(form) +
                         r"(?![\d])", folded_source):
                return form
        return None
    if kind in ("grouped", "integer", "year"):
        digits = canon
        if re.search(r"(?<![\d])" + re.escape(digits) + r"(?![\d])",
                     folded_source):
            return digits
        if kind == "grouped":
            grouped = f"{int(digits):,}"
            if grouped in folded_source:
                return grouped
        return None
    return None


# ------------------------------------------------------------ claims

_SENT_SPLIT_RE = re.compile(
    r"(?<=[.!?])\s+(?=[A-Z0-9\"“(\[])|\n+")


def split_sentences(text):
    """Sentence spans of the draft. Deliberately simple (the house
    splitter style): terminal punctuation + whitespace + a capital
    opener, or a newline run. List markers and headings ride along
    with their sentence — harmless for token extraction."""
    spans = []
    start = 0
    for m in _SENT_SPLIT_RE.finditer(text or ""):
        end = m.start()
        if text[start:end].strip():
            spans.append((start, end))
        start = m.end()
    if (text or "")[start:].strip():
        spans.append((start, len(text)))
    return spans


class ContentClaim:
    def __init__(self, sentence, span, tokens, pointers, pivotal,
                 pivotal_reasons):
        self.sentence = sentence
        self.span = span
        self.tokens = tokens            # [PrecisionToken]
        self.pointers = pointers        # [cv.Pointer]
        self.pivotal = pivotal
        self.pivotal_reasons = pivotal_reasons
        self.key = None                 # dedupe identity
        # stage outcomes
        self.source_status = "pending"  # fetched|dead|unverifiable
        self.source_detail = ""
        self.stage1 = "pending"         # supported|finding|weak-only|
        #                                 unverifiable|no-source
        self.stage2 = None              # supported|unsupported|
        #                                 unclear|skipped-budget|None
        self.stage2_evidence = None
        self.stage2_why = None
        self.final = "pending"          # supported|unsupported|
        #                                 unverifiable|recorded
        self._source_text = ""
        self._folded_source = ""
        self._missing_strong = []

    def as_dict(self):
        return {"claim": self.sentence[:400],
                "pivotal": self.pivotal,
                "pivotal_reasons": self.pivotal_reasons,
                "tokens": [t.as_dict() for t in self.tokens],
                "pointers": [p.raw for p in self.pointers],
                "source_status": self.source_status,
                "source_detail": self.source_detail,
                "stage1": self.stage1, "stage2": self.stage2,
                "stage2_evidence": self.stage2_evidence,
                "stage2_why": self.stage2_why, "final": self.final}


def _claim_key(sentence, tokens):
    """Dedupe identity helper: the sorted canonical STRONG tokens
    plus the sentence's capitalised entity words. Two sentences are
    the same assertion when their strong-token tuples are equal AND
    their entity sets intersect — the Hop claim appears twice in
    2777178d (§2 with its pointer, and repeated in the 'New in this
    answer' closing without one) and must be checked once, with the
    union of both instances' pointers."""
    ents = {w.lower() for w in
            re.findall(r"\b[A-Z][A-Za-z]{2,}\b", sentence)}
    strong = tuple(sorted(t.canonical for t in tokens if t.strong))
    return strong, ents


def _pointer_in(p, lo, hi):
    """A pointer occurs at EVERY span in its spans list (the
    citation extractor's .span is only the first-processed
    occurrence — a bare domain in the body whose URL form lives in
    the Sources list carries the body occurrence in .spans[1:])."""
    return any(lo <= s < hi for s, _e in p.spans)


_SOURCES_HEAD_RE = re.compile(
    r"^#{0,3}\s*(sources|references|bibliography)\b",
    re.IGNORECASE | re.MULTILINE)


def extract_claims(draft):
    """Pivotal-claim candidates: sentences carrying precision
    tokens, paired with pointers in the same sentence, else the
    same paragraph block. Claims with tokens but NO pointer are
    returned too, flagged unbound (recorded; C5 owns S-1).
    Bibliography lines (the Sources/References section) generate
    no claims — they are apparatus, not assertions — and pointer
    spans are masked before token extraction so figures inside a
    URL/DOI (10.1007/..., .../jy0916) never become claim tokens."""
    text = draft or ""
    pointers = cv.extract_pointers(text)
    novelty_at = text.rfind("New in this answer")
    src_m = _SOURCES_HEAD_RE.search(text)
    biblio = None
    if src_m:
        biblio_end = novelty_at if novelty_at > src_m.start() \
            else len(text)
        biblio = (src_m.start(), biblio_end)
    blocks = []
    pos = 0
    for chunk in text.split("\n\n"):
        blocks.append((pos, pos + len(chunk)))
        pos += len(chunk) + 2

    def block_of(span):
        for lo, hi in blocks:
            if lo <= span[0] < hi:
                return (lo, hi)
        return (0, len(text))

    claims = []
    for lo, hi in split_sentences(text):
        if biblio and biblio[0] <= lo < biblio[1]:
            continue
        sentence = text[lo:hi]
        masked = list(sentence)
        for p in pointers:
            for s, e in p.spans:
                if lo <= s < hi:
                    for i in range(s - lo, min(e, hi) - lo):
                        masked[i] = " "
        tokens = extract_precision_tokens("".join(masked))
        if not tokens:
            continue
        # token spans are sentence-relative; pointers pair by
        # absolute span (any occurrence).
        in_sentence = [p for p in pointers if _pointer_in(p, lo, hi)]
        paired = in_sentence
        if not paired:
            blo, bhi = block_of((lo, hi))
            paired = [p for p in pointers
                      if _pointer_in(p, blo, bhi)]
        reasons = []
        if any(t.strong for t in tokens):
            reasons.append("T1-precision-figure")
        low = sentence.lower()
        if any(m in low for m in _PRECEDENT_MARKERS):
            reasons.append("T2-precedent-marker")
        if novelty_at != -1 and lo > novelty_at:
            reasons.append("T3-novelty-closing")
        pivotal = bool(reasons)
        claim = ContentClaim(sentence.strip(), (lo, hi), tokens,
                             paired, pivotal, reasons)
        strong_key, ents = _claim_key(sentence, tokens)
        claim.key = (strong_key, frozenset(ents))
        dupe = None
        for prev in claims:
            p_strong, p_ents = prev.key
            if strong_key and p_strong == strong_key \
                    and (p_ents & ents):
                dupe = prev
                break
            if not strong_key and prev.key == claim.key:
                dupe = prev
                break
        if dupe is not None:
            # A repetition of an assertion already extracted: merge
            # its pointers into the first instance (the closing
            # repetition inherits the §2 pointer) and drop the dupe.
            for p in paired:
                if p not in dupe.pointers:
                    dupe.pointers.append(p)
            continue
        claims.append(claim)
    return claims, pointers


# ------------------------------------------------------------ fetching

def _fetch_url_for_pointer(p):
    """The URL whose TEXT is the cited source's content."""
    if p.kind == "url":
        return p.value
    if p.kind == "domain":
        return "https://" + p.value + "/"
    if p.kind == "doi":
        return "https://doi.org/" + p.value
    if p.kind == "eprint":
        year, num = p.value.split("/")
        return f"https://eprint.iacr.org/{year}/{num}"
    if p.kind == "arxiv":
        return f"https://arxiv.org/abs/{p.value}"
    return None


# ------------------------------------------------- challenge pages

# A fetch can "succeed" (HTTP 200) while delivering no source
# content at all: a CAPTCHA / bot-challenge / access-denial
# interstitial. Proven false-positive species
# (SPOTCHECK-SISA-PILOT-2026-11-17): the Reg E claim in draft
# d21135d5 was judged stage-2 "unsupported" against an eCFR
# CAPTCHA page — the excerpt literally was the denial page, not
# Regulation E. Such a page is a bot-wall in disguise: the claim
# is UNVERIFIABLE, never evidence of unsupported; an "unsupported"
# verdict is only valid when the source text was actually
# retrieved and does not support the claim. STRONG markers are
# interstitial-only artefacts/phrases and convict at any length.
# WEAK markers convict only on a SHORT page (extracted text
# under _CHALLENGE_SHORT_TEXT): interstitials are short, while a
# genuine long article merely DISCUSSING captchas stays fetched.
_CHALLENGE_STRONG = (
    "g-recaptcha", "h-captcha", "cf-challenge", "cf-turnstile",
    "challenges.cloudflare.com", "px-captcha",
    "are you a robot", "verify you are not a robot",
    "verify that you are not a robot", "verify you are human",
    "unusual traffic from your computer",
    "checking your browser before accessing",
    "pardon our interruption", "complete the security check",
    "please complete the captcha", "solve the captcha",
    "access to this page has been denied",
)
_CHALLENGE_WEAK = (
    "captcha", "access denied", "bot detection",
    "human verification", "just a moment", "attention required",
    "security check", "not a robot",
)
_CHALLENGE_SHORT_TEXT = 3000


def _challenge_marker(raw_body, text):
    """The challenge marker when the fetched page is a CAPTCHA /
    challenge / access-denial interstitial, else None."""
    raw = (raw_body or "").lower()
    body = (text or "").lower()
    for marker in _CHALLENGE_STRONG:
        if marker in raw or marker in body:
            return marker
    if len(body) < _CHALLENGE_SHORT_TEXT:
        for marker in _CHALLENGE_WEAK:
            if marker in body:
                return marker + " (halaman pendek)"
    return None


def _fetch_source_text(p, fetcher):
    """(status, detail, text): status fetched|dead|unverifiable,
    mirroring the citation layer's failure doctrine (bot-wall /
    5xx / odd errors are unverifiable, never death; 404/410 and
    connection-level failure are dead — the citation layer owns
    the pointer verdict, this layer only needs the class). An
    HTTP-200 page whose body is a CAPTCHA/challenge/access-denial
    interstitial is unverifiable too: no source content was
    actually retrieved."""
    url = _fetch_url_for_pointer(p)
    if url is None:
        return "unverifiable", f"tak ada URL konten untuk {p.kind}", ""
    res = fetcher.get(url)
    if res.status is not None:
        if 200 <= res.status < 400:
            text = html_to_text(res.text)
            marker = _challenge_marker(res.text, text)
            if marker is not None:
                return ("unverifiable",
                        f"halaman CAPTCHA/challenge ('{marker}') "
                        "— bukan isi sumber", "")
            return "fetched", f"HTTP {res.status}", text
        if res.status in (404, 410):
            return "dead", f"HTTP {res.status}", ""
        return ("unverifiable",
                f"HTTP {res.status} (bot-wall/rate-limit/server)", "")
    if res.error_kind in ("connect", "timeout"):
        return "dead", f"tak ter-resolve ({res.error_kind})", ""
    return "unverifiable", f"fetch error {res.error}", ""


# ------------------------------------------------------------ stage 2

_ENTAILMENT_INSTRUCTIONS = """You are an independent content verifier. You are given ONE claim sentence from a draft answer and EXCERPTS from the source the draft cites for it. Decide ONLY whether the cited source's content supports the claim's specific figures and facts.

Rules:
- "supported": the excerpts contain the claim's specific figures/facts (in digits, words, or an equivalent stated form), or directly state what the claim states.
- "unsupported": the claim states a specific figure, date, or named fact that the excerpts do NOT contain, or the excerpts state a DIFFERENT figure/fact for the same thing. A source that never mentions the claimed scheme/figure at all does not support a specific claim about it.
- "unclear": the excerpts are too fragmentary to decide (navigation text, an index page with no relevant content either way, truncated mid-statement).
- For "supported" you MUST quote the exact supporting passage from the excerpts as "evidence" (verbatim, <=300 chars). No quote, no supported.
- Judge ONLY from the excerpts. Do not use outside knowledge. Do not rewrite the claim.

Reply with ONLY this JSON object, no other text:
{"verdict": "supported" or "unsupported" or "unclear", "evidence": "..." or "", "why": "one short sentence"}"""


def build_entailment_prompt(claim_sentence, excerpt):
    return (_ENTAILMENT_INSTRUCTIONS
            + "\n\nCLAIM:\n" + claim_sentence.strip()
            + "\n\nSOURCE EXCERPTS:\n" + excerpt)


def _excerpt_for(claim, source_text, folded_source):
    """Relevant source windows: around each FOUND token, around
    each MISSING token's subject words, and around the claim's
    capitalised entities — plus the head of the source when
    nothing anchors. Capped at _EXCERPT_CHARS."""
    if not source_text:
        return ""
    windows = []
    anchors = set()
    for t in claim.tokens:
        matched = _token_present(t, folded_source)
        if matched:
            anchors.add(matched.split("%")[0].split(" ")[0])
    for w in re.findall(r"\b[A-Z][A-Za-z]{3,}\b", claim.sentence):
        anchors.add(_fold(w))
    for anchor in sorted(anchors):
        if not anchor:
            continue
        idx = folded_source.find(anchor)
        while idx != -1 and len(windows) < 8:
            lo = max(0, idx - _EXCERPT_WINDOW // 2)
            hi = min(len(source_text), idx + _EXCERPT_WINDOW)
            windows.append(source_text[lo:hi])
            idx = folded_source.find(anchor, idx + len(anchor))
    if not windows:
        windows.append(source_text[:_EXCERPT_CHARS // 2])
    out, seen = [], set()
    total = 0
    for w in windows:
        key = w[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append(w)
        total += len(w)
        if total >= _EXCERPT_CHARS:
            break
    return "\n...\n".join(out)[:_EXCERPT_CHARS]


def default_entailment_call(prompt):
    """Stage-2 transport: Nemotron over OUR OWN checker lanes —
    serve_gate.default_semantic_model_call (OpenRouter primary,
    whose own probe guards the emergency reserve; Vyce fallback).
    Imported lazily so this module never cycles with serve_gate.
    NEVER a third-party relay (CrowLLM et al.): the gate prompt
    stays on our own lane by design (user rule, relay visibility).
    Returns (raw_text, lane_label)."""
    import serve_gate
    return serve_gate.default_semantic_model_call(prompt)


def _first_json_object(text):
    import serve_gate
    return serve_gate._first_json_object(text)


def run_entailment(claim, source_text, folded_source, model_call):
    """One stage-2 judgement. Returns (verdict, evidence, why):
    verdict supported|unsupported|unclear. A 'supported' without a
    verbatim-verifiable evidence quote degrades to 'unclear'."""
    excerpt = _excerpt_for(claim, source_text, folded_source)
    prompt = build_entailment_prompt(claim.sentence, excerpt)
    raw = model_call(prompt)
    if isinstance(raw, tuple):
        raw = raw[0]
    obj = _first_json_object(raw or "")
    if not isinstance(obj, dict):
        return "unclear", None, "balasan pemeriksa tak terurai"
    verdict = str(obj.get("verdict") or "").strip().lower()
    why = str(obj.get("why") or "")[:300]
    evidence = str(obj.get("evidence") or "").strip()
    if verdict not in ("supported", "unsupported", "unclear"):
        return "unclear", None, f"vonis tak dikenal: {verdict!r}"
    if verdict == "supported":
        folded_ev = _fold(re.sub(r"\s+", " ", evidence))
        if not evidence or folded_ev not in folded_source:
            return ("unclear", None,
                    "klaim 'supported' tanpa kutipan bukti yang "
                    "terverifikasi di teks sumber — diturunkan")
        return "supported", evidence[:300], why
    return verdict, None, why


# ------------------------------------------------------------ main entry

_LOG_DEFAULT = object()


def _content_log(record, log_path):
    if log_path is None:
        return
    try:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"content_verify: log write failed: {ex}",
              file=sys.stderr)


def verify_content(draft, fetcher=None, model_call=None, mode=None,
                   isr_id=None, log_path=_LOG_DEFAULT,
                   max_stage2=MAX_STAGE2_CALLS):
    """Two-stage content verification of one draft. `fetcher` and
    `model_call` are the test seams (fetcher: .get(url) ->
    citation_verify.FetchResult; model_call: prompt -> raw text
    or (text, lane)). Always returns a structured dict and
    appends one record to the content log (log_path default =
    CONTENT_LOG; None disables):

    {performed, available, mode, verdict, block, claims, findings,
     unverified, counts, stage2_calls, error}

    verdict: "clean" (no pivotal problem), "findings" (recorded
    findings only), "fatal" (>=1 pivotal claim unsupported —
    blocks ONLY in mode "block"), "unverified" (the checker could
    not run, or every pivotal claim is unverifiable — loud, never
    blocks, never reported as clean)."""
    if log_path is _LOG_DEFAULT:
        log_path = CONTENT_LOG
    mode = mode or content_mode()
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "isr": isr_id or None, "mode": mode,
              "draft_chars": len(draft or ""),
              "stage": "content_verify"}
    result = {"performed": False, "available": False, "mode": mode,
              "verdict": "unverified", "block": False, "claims": [],
              "findings": [], "unverified": [], "counts": {},
              "stage2_calls": 0, "error": None}
    fetcher = fetcher or cv.HttpFetcher()
    claims, _pointers = extract_claims(draft)
    paired = [c for c in claims if c.pointers]
    unbound = [c for c in claims if not c.pointers]

    # Canary: prove egress before judging any source.
    canary_ok = False
    for canary in _CANARY_URLS:
        res = fetcher.get(canary)
        if res.status is not None:
            canary_ok = True
            break
    if not canary_ok:
        result["error"] = ("canary registry tak terjangkau — egress "
                           "pemeriksa mati; cek isi TIDAK berjalan")
        result["claims"] = [c.as_dict() for c in claims]
        record.update(result)
        record["loud"] = True
        _content_log(record, log_path)
        print("content_verify: PERINGATAN KERAS — canary Crossref/"
              "doi.org tak terjangkau; verifikasi isi TIDAK "
              "berjalan dan TIDAK memblokir", file=sys.stderr)
        return result

    # ---- stage 1: fetch + token presence, per claim
    source_cache = {}
    for claim in paired:
        # A claim may carry several pointers; the FIRST that yields
        # text is its source (the rest are the citation layer's).
        best = None
        for p in claim.pointers:
            if p.key() not in source_cache:
                source_cache[p.key()] = _fetch_source_text(p, fetcher)
            status, detail, text = source_cache[p.key()]
            if status == "fetched":
                best = (status, detail, text)
                break
            if best is None:
                best = (status, detail, text)
        claim.source_status, claim.source_detail, src_text = best
        if claim.source_status != "fetched":
            claim.stage1 = "unverifiable" \
                if claim.source_status == "unverifiable" \
                else "no-source"
            claim.final = "unverifiable"
            continue
        folded = _fold(src_text)
        claim._source_text = src_text
        claim._folded_source = folded
        missing_strong, missing_weak = [], []
        for t in claim.tokens:
            matched = _token_present(t, folded)
            t.found = matched is not None
            t.matched_as = matched
            if not t.found:
                (missing_strong if t.strong
                 else missing_weak).append(t)
        claim._missing_strong = missing_strong
        if missing_strong:
            claim.stage1 = "finding"
        elif missing_weak:
            claim.stage1 = "weak-only"
        else:
            claim.stage1 = "supported"

    # ---- stage 2: entailment for the ambiguous, budget-capped.
    # Priority: (1) pivotal stage-1 findings (the appeal — a source
    # may state the figure in a form the normaliser missed);
    # (2) pivotal precedent/novelty claims whose tokens are present
    # (presence is not support); (3) other pivotal supported claims.
    def _priority(c):
        if c.stage1 == "finding" and c.pivotal:
            return 0
        if c.pivotal and ("T2-precedent-marker" in c.pivotal_reasons
                          or "T3-novelty-closing"
                          in c.pivotal_reasons):
            return 1
        if c.pivotal:
            return 2
        return 3

    candidates = [c for c in paired
                  if c.source_status == "fetched"
                  and c.stage1 in ("finding", "supported",
                                   "weak-only")]
    candidates.sort(key=_priority)
    caller = model_call or default_entailment_call
    stage2_errors = []
    calls = 0
    for claim in candidates:
        if _priority(claim) == 3 and claim.stage1 == "supported":
            continue  # non-pivotal + mechanically supported: done
        if calls >= max_stage2:
            claim.stage2 = "skipped-budget"
            continue
        try:
            verdict, evidence, why = run_entailment(
                claim, claim._source_text, claim._folded_source,
                caller)
            calls += 1
            claim.stage2 = verdict
            claim.stage2_evidence = evidence
            claim.stage2_why = why
        except Exception as ex:  # noqa: BLE001 - lane failure is data
            calls += 1
            claim.stage2 = None
            stage2_errors.append(
                f"{type(ex).__name__}: {ex}")
    result["stage2_calls"] = calls

    # ---- final per-claim verdicts
    for claim in paired:
        if claim.final == "unverifiable":
            continue
        if claim.stage2 == "unsupported":
            claim.final = "unsupported"
        elif claim.stage2 == "supported":
            claim.final = "supported"
        elif claim.stage1 == "finding":
            # Stage 2 did not rescue (unclear / skipped / lane
            # down): the mechanical absence stands as the verdict.
            claim.final = "unsupported" if claim.pivotal \
                else "recorded"
        elif claim.stage1 in ("supported", "weak-only"):
            claim.final = "supported" if claim.pivotal \
                else "recorded"
        else:
            claim.final = "recorded"
    for claim in unbound:
        claim.stage1 = "unbound"
        claim.final = "recorded"

    pivotal_bad = [c for c in claims
                   if c.final == "unsupported" and c.pivotal]
    pivotal_unv = [c for c in claims
                   if c.final == "unverifiable" and c.pivotal]
    findings = [c for c in claims
                if c.final == "unsupported"
                or (c.final == "recorded"
                    and c.stage1 in ("finding", "unbound"))]
    counts = {
        "claims": len(claims), "paired": len(paired),
        "unbound": len(unbound),
        "pivotal": sum(1 for c in claims if c.pivotal),
        "stage1_findings": sum(1 for c in claims
                               if c.stage1 == "finding"),
        "stage2_unsupported": sum(1 for c in claims
                                  if c.stage2 == "unsupported"),
        "unsupported": len(pivotal_bad),
        "unverifiable": len(pivotal_unv),
        "stage2_calls": calls,
    }
    result.update({"performed": True, "available": True,
                   "claims": [c.as_dict() for c in claims],
                   "findings": [c.as_dict() for c in findings],
                   "unverified": [c.as_dict() for c in pivotal_unv],
                   "counts": counts})
    if stage2_errors:
        result["error"] = ("tahap-2 (entailment) gagal di "
                           f"{len(stage2_errors)} klaim: "
                           + " || ".join(stage2_errors[:2]))
    if pivotal_bad:
        result["verdict"] = "fatal"
        result["block"] = bool(mode == "block")
    elif pivotal_unv and not any(
            c.pivotal and c.final == "supported" for c in claims):
        result["verdict"] = "unverified"
        result["error"] = (result["error"] or "") + (
            " semua klaim poros tak terverifikasi (sumber "
            "bot-wall/mati) — dilaporkan terbuka, tidak memblokir")
    elif findings:
        result["verdict"] = "findings"
    else:
        result["verdict"] = "clean"
    record.update({k: result[k] for k in
                   ("performed", "available", "verdict", "block",
                    "counts", "stage2_calls", "error")})
    record["findings"] = result["findings"]
    record["unverified"] = result["unverified"]
    _content_log(record, log_path)
    return result
