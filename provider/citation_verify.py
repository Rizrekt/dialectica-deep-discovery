#!/usr/bin/env python3
"""Mechanical citation verification for Dialectica serve drafts —
the CITATION VERIFY layer (built 2026-11-17, user decision
2026-11-17 10:39 accepting the SPOTCHECK-PILOT-2026-11-17.md
proposal).

WHY THIS LAYER EXISTS. The first gated pilot (2026-11-17 09:35)
sent 5 Pioneer answers; the manual checklist-D spot-check of the
first 3 found ONE defect species in 3/3: the GLM writer fabricates
PRECISION POINTERS — identifiers that look exact but were generated
from plausibility, not retrieval:

- 2777178d: dead domain `proofofhumanity.site` (the live domain is
  `proofofhumanity.id`);
- d94d7e34: fabricated DOI 10.1145/2516651.2516734 (404; the real
  Meiklejohn DOI is 10.1145/2504730.2504747) and a no-TLD URL
  `https://whitepaper.worldcoin/`;
- 635a010d: pinpoint "Lindell, IACR ePrint 2020/940" — 2020/940 is
  Fei Meng's ABE-from-lattices paper, a different document.

The C5 semantic stage (serve_gate.semantic_check) structurally
CANNOT see this species: it is a pattern mimic judging text, not a
resolver — it returned "clean" on all 3. This layer closes the gap
MECHANICALLY: every pointer in the draft is extracted and actually
resolved against the live registry / host, and registry pinpoints
(DOI, IACR ePrint, arXiv) have their document title/authors compared
against the title/author the draft claims for them.

WHAT THIS LAYER DOES NOT DO (hard boundary, stated in the report):
it does NOT verify that a living source's CONTENT supports the
claim attached to it. The Hop Protocol species (source alive and
resolving, the claimed 50%/10% figures simply not in it) passes
this layer untouched — content entailment is a different layer
(C5/checklist-D territory), out of scope here.

POINTERS EXTRACTED: full URLs, DOIs (bare or as doi.org URLs),
IACR ePrint numbers (URL or textual "ePrint YYYY/NNN"), arXiv ids
(URL or "arXiv:NNNN.NNNNN"), and bare domains (galxe.com,
proofofhumanity.site, ...). A host whose final label is not a known
TLD (whitepaper.worldcoin) is a MALFORMED finding without any
fetch. For registry pinpoints the draft's claimed title (the last
quoted string before the pointer) and claimed author surname are
captured for the document comparison.

PIVOTAL vs PERIPHERAL (the withholding line, explicit):
a pointer is PIVOTAL when any of —
  P1  it is a registry pinpoint (DOI / ePrint / arXiv): a precision
      identifier exists only to anchor one specific document claim;
  P2  its sentence carries a specific figure (a percentage, a
      decimal, a thousands-grouped number): figures need their
      source alive;
  P3  its sentence carries a precedent/anchor marker ("precedent",
      "reference case", "canonical", "clearest", "landmark");
  P4  it sits in the closing "New in this answer" novelty section —
      the novelty anchor of the whole answer.
Everything else is PERIPHERAL.

WITHHOLD RULE (mode "block", the default for this layer when
armed): a draft is withheld when >=1 PIVOTAL pointer is dead
(HTTP 404/410, or unresolvable after retry), malformed, or a
WRONG DOCUMENT (registry title/author do not match the draft's
claimed title/author). Peripheral dead/wrong pointers are recorded
findings only — they never withhold on their own.

CHECKER-FAILURE RULE (mirrors the C5 doctrine — an unrun check must
never masquerade as a passed one, and a dead checker must not kill
a good draft):
- Bot-wall / rate-limit answers (401/403/429) and 5xx are
  UNVERIFIABLE, not dead: recorded openly, never a finding, never
  a withhold.
- A canary (Crossref + doi.org) runs first; if the egress itself
  is down, the whole run reports verdict "unverified"
  (available=False) and blocks nothing.
- If >=40% of fetches in a run die at connection level, the run is
  downgraded to "unverified" (mass egress failure is the checker's
  failure, not the draft's).
- If every PIVOTAL pointer is unverifiable while at least one
  exists, the verdict is "unverified" (loud in the log), still
  never a withhold.

ARMING (same pattern as C5): the stage runs only when the launcher
sets DIALECTICA_CITATION_CHECK=1 (run_serve does, for the gated
Vyce serve). Mode comes from DIALECTICA_CITATION_MODE: "shadow"
logs findings and NEVER withholds; anything else (including
unset) is "block" — for THIS layer the accepted pilot default is
withholding (user decision 2026-11-17 10:39), the opposite default
from C5, whose evidence base is still shadow-only.

Every run appends one record to citation-check-log.jsonl. Network
behaviour: one honest user-agent, per-run cache (each unique
pointer fetched once), >=0.34s pacing between requests, one retry
on connection errors and 5xx. The fetcher is the test seam: unit
tests inject a deterministic fake, calibration injects the real
one.
"""
import json
import os
import re
import sys
import time
import unicodedata
from urllib.parse import quote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CITATION_ARM_ENV = "DIALECTICA_CITATION_CHECK"
CITATION_MODE_ENV = "DIALECTICA_CITATION_MODE"
CITATION_LOG = os.path.join(HERE, "citation-check-log.jsonl")

USER_AGENT = ("DialecticaCitationVerify/1.0 (mechanical citation "
              "checker; operator research)")
FETCH_TIMEOUT_S = 20.0
PACE_S = 0.34
MASS_CONNECT_FAIL_RATIO = 0.40

# Final labels accepted as real TLDs for bare-domain / host
# classification. A host ending in anything else (and not a known
# file extension) is treated as malformed — the whitepaper.worldcoin
# species. Deliberately generous toward real-world ccTLD/gTLD use in
# this corpus (sh = attest.sh, id, io, xyz, site itself is real —
# proofofhumanity.site is syntactically valid and must be caught by
# RESOLUTION, not by this list).
#
# Two-letter final labels are NOT judged against this gTLD list:
# they are ccTLDs and are recognised against the ISO 3166-1
# alpha-2 assignments (CCTLD_ALPHA2 below). The whitelist-only
# doctrine misfired on real drafts (SPOTCHECK-SISA-PILOT-2026-11-17:
# eur-lex.europa.eu and docs.cow.fi flagged "malformed" — .eu/.fi
# simply missing here). An UNASSIGNED two-letter code (xq, zz, ...)
# is still not a TLD and stays malformed, exactly like a fabricated
# longer label.
KNOWN_TLDS = {
    "com", "org", "net", "edu", "gov", "mil", "int", "info", "biz",
    "name", "pro", "aero", "coop", "museum", "io", "ai", "co", "me",
    "tv", "cc", "sh", "gg", "xyz", "site", "online", "app", "dev",
    "id", "us", "uk", "de", "jp", "cn", "fr", "au", "ca", "in",
    "network", "finance", "exchange", "foundation", "institute",
    "technology", "systems", "protocol", "money", "cash", "wiki",
    "blog", "news", "press", "io", "so", "to", "fm", "am", "pm",
    "world", "global", "one", "live", "today", "zone", "page",
    "link", "click", "art", "eth", "crypto", "nft", "dao", "web3",
    "tech", "club", "store", "shop", "space", "life", "fun",
    "email", "group", "tools", "agency", "design", "solutions",
    "company",
}
# ISO 3166-1 alpha-2 country codes (officially assigned), plus
# the root-zone ccTLDs eu (European Union), uk (United Kingdom —
# gb is the assigned code, uk is the live root entry) and su
# (former USSR, still delegated). Lowercase.
CCTLD_ALPHA2 = set((
    "ac ad ae af ag ai al am ao aq ar as at au aw ax az "
    "ba bb bd be bf bg bh bi bj bl bm bn bo bq br bs bt bv bw by bz "
    "ca cc cd cf cg ch ci ck cl cm cn co cr cu cv cw cx cy cz "
    "de dj dk dm do dz "
    "ec ee eg eh er es et "
    "fi fj fk fm fo fr "
    "ga gb gd ge gf gg gh gi gl gm gn gp gq gr gs gt gu gw gy "
    "hk hm hn hr ht hu "
    "id ie il im in io iq ir is it "
    "je jm jo jp "
    "ke kg kh ki km kn kp kr kw ky kz "
    "la lb lc li lk lr ls lt lu lv ly "
    "ma mc md me mf mg mh mk ml mm mn mo mp mq mr ms mt mu mv mw mx my mz "
    "na nc ne nf ng ni nl no np nr nu nz "
    "om "
    "pa pe pf pg ph pk pl pm pn pr ps pt pw py "
    "qa "
    "re ro rs ru rw "
    "sa sb sc sd se sg sh si sj sk sl sm sn so sr ss st sv sx sy sz "
    "tc td tf tg th tj tk tl tm tn to tr tt tw tz "
    "ua ug um us uy uz "
    "va vc ve vg vi vn vu "
    "wf ws "
    "ye yt "
    "za zm zw "
    "eu uk su"
).split())


def _tld_recognized(label):
    """A final host label is a recognised TLD when it is a known
    gTLD (KNOWN_TLDS) or a real two-letter ccTLD (CCTLD_ALPHA2).
    Anything else — an unassigned two-letter code or a fabricated
    string like "worldcoin" — is NOT a TLD."""
    label = (label or "").lower()
    if len(label) == 2:
        return label in CCTLD_ALPHA2
    return label in KNOWN_TLDS
FILE_EXTS = {
    "py", "txt", "md", "json", "jsonl", "html", "htm", "xml",
    "csv", "png", "jpg", "jpeg", "gif", "svg", "pdf", "zip",
    "mediawiki", "rst", "yaml", "yml", "toml", "ini", "cfg",
}

_URL_RE = re.compile(r"https?://\S+")
_DOI_RE = re.compile(r"10\.\d{4,9}/\S+")
_EPRINT_URL_RE = re.compile(r"eprint\.iacr\.org/(\d{4})/(\d{1,4})",
                            re.IGNORECASE)
_EPRINT_TEXT_RE = re.compile(
    r"(?:IACR\s+)?ePrint\s+(?:Archive\s+)?(?:paper\s+)?(\d{4})/(\d{1,4})",
    re.IGNORECASE)
_ARXIV_URL_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
_ARXIV_TEXT_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})", re.IGNORECASE)
_BARE_DOMAIN_RE = re.compile(
    r"(?<![\w@./-])(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,24}(?:/[^\s\)\]\}\"'<>]*)?")
_QUOTED_RE = re.compile(r"[\"“]([^\"”\n]{6,220})[\"”]")
_AUTHOR_RE = re.compile(
    r"([A-Z][A-Za-zÀ-ÖØ-öø-ÿ\-']+)\s*(?:et\s+al\.?|,|&|\band\b)")
_FIGURE_RE = re.compile(
    r"(\d[\d.,]*\s?%|\$\s?\d|\b\d{1,3}(?:,\d{3})+\b|\b\d+\.\d+\b)")
_ANCHOR_MARKERS = ("precedent", "reference case", "canonical",
                   "clearest", "landmark", "the first ")
_STOPWORDS = {"the", "a", "an", "of", "on", "in", "for", "and",
              "to", "with", "from", "by", "at", "as", "is", "are",
              "via", "using", "based", "its", "it"}


def citation_mode():
    """DIALECTICA_CITATION_MODE: "shadow" = log-only, never
    withholds; anything else (including unset) is "block" — the
    accepted default for this layer (user 2026-11-17 10:39)."""
    return "shadow" if os.environ.get(
        CITATION_MODE_ENV, "").strip().lower() == "shadow" else "block"


# ------------------------------------------------------------ fetching

class FetchResult:
    """One HTTP fetch outcome. status=None means no HTTP response
    was received; error_kind then says why: "connect" (DNS/proxy/
    connection), "timeout", or "other"."""

    def __init__(self, url, status=None, final_url=None, text="",
                 error=None, error_kind=None):
        self.url = url
        self.status = status
        self.final_url = final_url or url
        self.text = text or ""
        self.error = error
        self.error_kind = error_kind

    def __repr__(self):
        return (f"FetchResult({self.url!r} status={self.status} "
                f"err={self.error_kind})")


class HttpFetcher:
    """Production fetcher: requests-based, per-run cache, pacing,
    one retry on connection errors / 5xx, honest user-agent, body
    capped so a giant page cannot flood the checker."""

    BODY_CAP = 300_000

    def __init__(self, pace_s=PACE_S, timeout_s=FETCH_TIMEOUT_S):
        import requests  # local import: tests never need it
        self._requests = requests
        self._pace_s = pace_s
        self._timeout_s = timeout_s
        self._cache = {}
        self._last_call = 0.0
        self.calls = 0
        self.connect_failures = 0

    def get(self, url):
        if url in self._cache:
            return self._cache[url]
        result = self._get_with_retry(url)
        self._cache[url] = result
        if result.error_kind == "connect":
            self.connect_failures += 1
        return result

    def _get_with_retry(self, url):
        last = None
        for attempt in range(2):
            last = self._get_once(url)
            retryable = (last.error_kind in ("connect", "timeout")
                         or (last.status is not None
                             and last.status >= 500))
            if not retryable or attempt == 1:
                return last
            time.sleep(1.0)
        return last

    def _get_once(self, url):
        wait = self._pace_s - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.monotonic()
        self.calls += 1
        try:
            resp = self._requests.get(
                url, headers={"User-Agent": USER_AGENT},
                timeout=(5, self._timeout_s), allow_redirects=True,
                stream=True)
            try:
                chunks = []
                size = 0
                for chunk in resp.iter_content(chunk_size=16384):
                    chunks.append(chunk)
                    size += len(chunk)
                    if size >= self.BODY_CAP:
                        break
                raw = b"".join(chunks)
            finally:
                resp.close()
            text = raw.decode("utf-8", errors="replace")
            return FetchResult(url, status=resp.status_code,
                               final_url=resp.url, text=text)
        except self._requests.exceptions.Timeout as ex:
            return FetchResult(url, error=f"Timeout: {ex}",
                               error_kind="timeout")
        except self._requests.exceptions.ConnectionError as ex:
            return FetchResult(url, error=f"ConnectionError: {ex}",
                               error_kind="connect")
        except Exception as ex:  # noqa: BLE001 - classified below
            return FetchResult(url, error=f"{type(ex).__name__}: {ex}",
                               error_kind="other")


# ------------------------------------------------------------ extraction

def _trim_pointer(raw):
    """Trim a loosely matched pointer: trailing sentence punctuation
    and UNBALANCED closing brackets/quotes/angular brackets. Real
    DOIs carry balanced parentheses and angle segments (AMS style:
    10.1175/1520-0469(1993)050<3625:MVATAS>2.0.CO;2) — those are
    kept whole; the wrapping paren of a citation is not."""
    s = raw
    changed = True
    while s and changed:
        changed = False
        while s and s[-1] in ".,;:\"'":
            s = s[:-1]
            changed = True
        for closer, opener in ((")", "("), ("]", "["),
                               (">", "<"), ("}", "{")):
            while s.endswith(closer) and s.count(closer) > s.count(opener):
                s = s[:-1]
                changed = True
    return s


class Pointer:
    def __init__(self, kind, value, raw, span):
        self.kind = kind            # url | doi | eprint | arxiv | domain
        self.value = value          # normalised identity for dedupe
        self.raw = raw              # as written in the draft
        self.span = span            # (start, end) of first occurrence
        self.spans = [span]
        self.claimed_title = None
        self.claimed_title_near = None
        self.claimed_author = None
        self.pivotal = False
        self.pivotal_reasons = []
        self.status = "pending"     # verified|dead|wrong_document|
        #                             malformed|unverifiable|pending
        self.detail = ""
        self.actual_title = None
        self.actual_authors = []

    def key(self):
        return (self.kind, self.value)

    def as_dict(self):
        return {"kind": self.kind, "pointer": self.raw,
                "value": self.value, "pivotal": self.pivotal,
                "pivotal_reasons": self.pivotal_reasons,
                "status": self.status, "detail": self.detail,
                "claimed_title": self.claimed_title,
                "claimed_title_near": self.claimed_title_near,
                "claimed_author": self.claimed_author,
                "actual_title": self.actual_title,
                "actual_authors": self.actual_authors,
                "occurrences": len(self.spans)}


def _sentence_bounds(text, start, end):
    lo = max(text.rfind(".", 0, start), text.rfind("!", 0, start),
             text.rfind("?", 0, start), text.rfind("\n", 0, start))
    hi_candidates = [i for i in (text.find(".", end),
                                 text.find("!", end),
                                 text.find("?", end),
                                 text.find("\n", end)) if i != -1]
    hi = min(hi_candidates) if hi_candidates else len(text)
    return lo + 1, hi


def _claimed_context(text, span):
    """Claimed title/author for a pointer: the last quoted string in
    the ~420 chars before it (citations here run Author, "Title,"
    venue — pointer), and the surname token attached to it. Also
    returns the NEAR title: the same quoted string, but only when
    it is structurally part of THIS pointer's citation apparatus —
    the gap between the closing quote and the pointer is short
    (<=80 chars, <=10 words, no sentence break). A quoted phrase
    from earlier prose ("at most N emails", another paper's title
    paragraphs away) is NOT a title claim about a plain URL and
    must never be compared against that URL's page title."""
    start = span[0]
    window = text[max(0, start - 420):start]
    title = None
    title_near = None
    author = None
    quoted = list(_QUOTED_RE.finditer(window))
    if quoted:
        m = quoted[-1]
        title = m.group(1).strip().rstrip(",").strip()
        before_title = window[:m.start()]
        authors = _AUTHOR_RE.findall(before_title[-200:])
        if authors:
            author = authors[-1]
        gap = window[m.end():]
        # NEAR additionally requires an author surname in the
        # apparatus: a quoted phrase inside running prose with a
        # short gap to a parenthetical link ("at most N emails"
        # ... (W3C — url)) is argument, not a citation title.
        if (author and len(gap) <= 80 and len(gap.split()) <= 10
                and not re.search(r"[.!?]", gap)):
            title_near = title
    return title, author, title_near


def _classify_pivotal(text, pointer, novelty_at):
    reasons = []
    if pointer.kind in ("doi", "eprint", "arxiv"):
        reasons.append("P1-registry-pinpoint")
    lo, hi = _sentence_bounds(text, pointer.span[0], pointer.span[1])
    sentence = text[lo:hi]
    if _FIGURE_RE.search(sentence):
        reasons.append("P2-figure-in-sentence")
    low = sentence.lower()
    if any(m in low for m in _ANCHOR_MARKERS):
        reasons.append("P3-precedent-marker")
    if novelty_at is not None and pointer.span[0] > novelty_at:
        reasons.append("P4-novelty-closing")
    pointer.pivotal = bool(reasons)
    pointer.pivotal_reasons = reasons


def _host_of(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def _host_malformed(host):
    """A host is malformed when it has no recognised TLD — the
    whitepaper.worldcoin species (no dot-TLD at all), an
    unassigned two-letter code, or a fabricated final label."""
    if not host:
        return True
    labels = host.split(".")
    if len(labels) < 2:
        return True
    return not _tld_recognized(labels[-1])


def extract_pointers(text):
    """All unique pointers in the draft, deduped by (kind, value),
    each with claimed context + pivotal classification."""
    text = text or ""
    found = {}

    def add(kind, value, raw, span):
        key = (kind, value)
        if key in found:
            found[key].spans.append(span)
            return found[key]
        p = Pointer(kind, value, raw, span)
        found[key] = p
        return p

    masked = list(text)

    def mask(span):
        for i in range(span[0], span[1]):
            masked[i] = " "

    # 1. URLs (a doi.org URL becomes a DOI pointer, not a URL one).
    # The loose match is trimmed of sentence punctuation and
    # unbalanced closers; the FULL loose span is masked so the
    # bare passes below never rescan its fragments.
    for m in _URL_RE.finditer(text):
        raw = _trim_pointer(m.group(0))
        span = (m.start(), m.start() + len(raw))
        host = _host_of(raw)
        doi_m = _DOI_RE.search(raw)
        if host == "doi.org" and doi_m:
            add("doi", _trim_pointer(doi_m.group(0)), raw, span)
        elif host == "eprint.iacr.org":
            em = _EPRINT_URL_RE.search(raw)
            if em:
                add("eprint", f"{em.group(1)}/{em.group(2)}", raw, span)
            else:
                add("url", raw, raw, span)
        elif host in ("arxiv.org", "www.arxiv.org"):
            am = _ARXIV_URL_RE.search(raw)
            if am:
                add("arxiv", am.group(1), raw, span)
            else:
                add("url", raw, raw, span)
        else:
            add("url", raw, raw, span)
        mask((m.start(), m.end()))

    # 2. Bare DOIs in the unmasked remainder.
    rest = "".join(masked)
    for m in _DOI_RE.finditer(rest):
        raw = _trim_pointer(m.group(0))
        add("doi", raw, raw, (m.start(), m.start() + len(raw)))
        mask((m.start(), m.end()))
    rest = "".join(masked)

    # 3. Textual ePrint / arXiv pinpoints.
    for m in _EPRINT_TEXT_RE.finditer(rest):
        add("eprint", f"{m.group(1)}/{m.group(2)}", m.group(0),
            (m.start(), m.end()))
    for m in _ARXIV_TEXT_RE.finditer(rest):
        add("arxiv", m.group(1), m.group(0), (m.start(), m.end()))

    # 4. Bare domains in what remains (URLs/DOIs already masked).
    for m in _BARE_DOMAIN_RE.finditer(rest):
        raw = m.group(0)
        host = raw.split("/")[0].lower()
        labels = host.split(".")
        if len(labels) < 2 or not any(c.isalpha() for c in labels[0]):
            continue
        last = labels[-1].lower()
        if last in FILE_EXTS:
            continue
        span = (m.start(), m.end())
        if _tld_recognized(last):
            # A bare domain that merely restates a URL pointer's
            # host (body text vs Sources line) is the same pointer.
            twin = None
            for p in found.values():
                if p.kind == "url" and _host_of(p.value) == host:
                    twin = p
                    break
            if twin is not None:
                twin.spans.append(span)
                continue
            add("domain", host, raw, span)
        else:
            add("domain", host, raw, span)

    novelty_at = text.rfind("New in this answer")
    if novelty_at == -1:
        novelty_at = None
    pointers = sorted(found.values(), key=lambda p: p.span[0])
    for p in pointers:
        title, author, title_near = _claimed_context(text, p.span)
        p.claimed_title = title
        p.claimed_title_near = title_near
        p.claimed_author = author
        _classify_pivotal(text, p, novelty_at)
    return pointers


# ------------------------------------------------------------ comparison

def _norm_tokens(title):
    if not title:
        return set()
    s = unicodedata.normalize("NFKD", str(title).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return {t for t in s.split() if t and t not in _STOPWORDS}


def _norm_name(name):
    if not name:
        return ""
    s = unicodedata.normalize("NFKD", str(name).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z\- ]", "", s).strip().split(" ")[-1]


def title_relation(claimed, actual):
    """("match"|"wrong"|"uncertain", containment) of two titles.
    Zero token overlap is a different document, full stop; the grey
    zone is reported as uncertain and never grounds a withhold."""
    a, b = _norm_tokens(claimed), _norm_tokens(actual)
    if not a or not b:
        return "uncertain", 0.0
    inter = len(a & b)
    containment = inter / min(len(a), len(b))
    if containment >= 0.6:
        return "match", containment
    if inter == 0 or containment < 0.2:
        return "wrong", containment
    return "uncertain", containment


def title_relation_strict(claimed, actual):
    """Strict relation for PAGE-title comparison (plain-URL
    pinpoints): a match requires one token set to contain the
    other (page titles routinely add site suffixes; drafts
    routinely give fuller titles). Anything in between — e.g. a
    one-word subtitle swap, containment 0.71 with neither set a
    subset — is "uncertain": the layer reports it unverifiable
    rather than passing it silently or calling it wrong on
    token arithmetic alone."""
    a, b = _norm_tokens(claimed), _norm_tokens(actual)
    if not a or not b:
        return "uncertain", 0.0
    inter = len(a & b)
    containment = inter / min(len(a), len(b))
    if a <= b or b <= a:
        return "match", containment
    if inter == 0 or containment < 0.2:
        return "wrong", containment
    return "uncertain", containment


def _page_title(html):
    if not html:
        return None
    m = re.search(r"<meta[^>]+property=[\"']og:title[\"'][^>]+"
                  r"content=[\"']([^\"']+)[\"']", html, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"<title[^>]*>([^<]{4,300})</title>", html, re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    return None


def _meta_content(html, name):
    if not html:
        return None
    m = re.search(r"<meta[^>]+name=[\"']" + re.escape(name) +
                  r"[\"'][^>]+content=[\"']([^\"']*)[\"']", html, re.I)
    return m.group(1).strip() if m else None


# ------------------------------------------------------------ verifiers

def _classify_http_failure(p, result, what):
    """Map a fetch outcome onto pointer status for non-registry
    fetches. Returns True when the outcome is decided here."""
    if result.status is not None:
        if 200 <= result.status < 400:
            return False  # alive — caller continues
        if result.status in (404, 410):
            p.status = "dead"
            p.detail = f"{what}: HTTP {result.status}"
            return True
        p.status = "unverifiable"
        p.detail = (f"{what}: HTTP {result.status} "
                    "(bot-wall/rate-limit/server — not proof of death)")
        return True
    if result.error_kind in ("connect", "timeout"):
        p.status = "dead"
        p.detail = f"{what}: tak ter-resolve ({result.error_kind})"
        return True
    p.status = "unverifiable"
    p.detail = f"{what}: fetch error {result.error}"
    return True


def _verify_doi(p, fetcher):
    doi = p.value
    res = fetcher.get("https://api.crossref.org/works/"
                      + quote(doi, safe="/"))
    if res.status == 404:
        # Not in Crossref is NOT proof of death — Crossref is one
        # registration agency among several. Fall through to the
        # doi.org check below: only a doi.org 404 as well convicts.
        pass
    elif res.status is not None and 200 <= res.status < 300:
        try:
            msg = json.loads(res.text)["message"]
        except (ValueError, KeyError):
            msg = None
        if msg:
            titles = msg.get("title") or []
            p.actual_title = titles[0] if titles else None
            p.actual_authors = [a.get("family", "") for a in
                                msg.get("author", []) if a.get("family")]
            _compare_document(p, "Crossref")
            return
    # Crossref unreachable/odd — fall back to doi.org resolution:
    # a redirect or any HTTP answer proves the DOI exists; a 404
    # there is death; a connection failure leaves it unverifiable.
    res2 = fetcher.get("https://doi.org/" + quote(doi, safe="/"))
    if res2.status == 404:
        p.status = "dead"
        p.detail = ("doi.org 404: DOI tidak terdaftar"
                    + (" (Crossref juga 404)"
                       if res.status == 404 else ""))
    elif res2.status is not None:
        p.status = "verified"
        p.detail = (f"doi.org menjawab HTTP {res2.status} "
                    "(Crossref tak terjangkau — judul tak terbanding)")
    else:
        p.status = "unverifiable"
        p.detail = f"Crossref + doi.org tak terjangkau ({res.error})"


def _verify_eprint(p, fetcher):
    year, num = p.value.split("/")
    res = fetcher.get(f"https://eprint.iacr.org/{year}/{num}")
    if _classify_http_failure(p, res, "IACR ePrint"):
        return
    p.actual_title = _meta_content(res.text, "citation_title")
    authors = re.findall(
        r"<meta[^>]+name=[\"']citation_author[\"'][^>]+"
        r"content=[\"']([^\"']*)[\"']", res.text, re.I)
    p.actual_authors = authors
    if p.actual_title:
        _compare_document(p, "IACR ePrint")
    else:
        p.status = "verified"
        p.detail = "ePrint hidup; metadata judul tak terbaca"


def _verify_arxiv(p, fetcher):
    res = fetcher.get("https://export.arxiv.org/api/query?id_list="
                      + quote(p.value, safe=""))
    if _classify_http_failure(p, res, "arXiv API"):
        return
    entry = re.search(r"<entry>(.*?)</entry>", res.text, re.S)
    if not entry:
        p.status = "dead"
        p.detail = "arXiv API: id tidak ditemukan"
        return
    t = re.search(r"<title>(.*?)</title>", entry.group(1), re.S)
    p.actual_title = (re.sub(r"\s+", " ", t.group(1)).strip()
                      if t else None)
    p.actual_authors = re.findall(r"<name>([^<]+)</name>",
                                  entry.group(1))
    if p.actual_title:
        _compare_document(p, "arXiv")
    else:
        p.status = "verified"
        p.detail = "arXiv hidup; judul tak terbaca"


def _compare_document(p, registry):
    """Title (+author corroboration) comparison for a registry
    pinpoint whose document metadata is known."""
    if not p.claimed_title:
        p.status = "verified"
        p.detail = f"{registry}: dokumen ada, draf tak mengklaim judul"
        return
    relation, containment = title_relation(p.claimed_title,
                                           p.actual_title)
    author_note = ""
    if p.claimed_author and p.actual_authors:
        claimed = _norm_name(p.claimed_author)
        actual = {_norm_name(a) for a in p.actual_authors}
        if claimed and claimed not in actual:
            author_note = (f"; penulis klaim '{p.claimed_author}' "
                           f"tidak ada di dokumen ({', '.join(p.actual_authors[:3])})")
    if relation == "match":
        p.status = "verified"
        p.detail = (f"{registry}: judul cocok "
                    f"(containment {containment:.2f}){author_note}")
    elif relation == "wrong":
        p.status = "wrong_document"
        p.detail = (f"{registry}: dokumen LAIN — klaim "
                    f"'{p.claimed_title}' vs aktual "
                    f"'{p.actual_title}' (containment "
                    f"{containment:.2f}){author_note}")
    else:
        p.status = "unverifiable"
        p.detail = (f"{registry}: judul abu-abu "
                    f"(containment {containment:.2f}) — tak cukup "
                    f"untuk vonis salah-dokumen{author_note}")


def _verify_url(p, fetcher):
    host = _host_of(p.value)
    if _host_malformed(host):
        p.status = "malformed"
        p.detail = f"host '{host}' tanpa TLD dikenal"
        return
    res = fetcher.get(p.value)
    if _classify_http_failure(p, res, "URL"):
        return
    p.status = "verified"
    p.detail = f"HTTP {res.status}"
    # A title claim riding on a plain URL is compared against the
    # fetched page title ONLY when the quoted title is structurally
    # part of this pointer's own citation (claimed_title_near —
    # SSRN-style pinpoints); a bot-walled page was already
    # classified unverifiable above.
    if p.claimed_title_near:
        page_title = _page_title(res.text)
        if page_title:
            p.actual_title = page_title
            relation, containment = title_relation_strict(
                p.claimed_title_near, page_title)
            if relation == "wrong":
                p.status = "wrong_document"
                p.detail = (f"judul halaman lain — klaim "
                            f"'{p.claimed_title_near}' vs halaman "
                            f"'{page_title}' (containment "
                            f"{containment:.2f})")
            elif relation == "match":
                p.detail += (f"; judul halaman cocok "
                             f"({containment:.2f})")
            else:
                p.status = "unverifiable"
                p.detail = (f"judul halaman abu-abu — klaim "
                            f"'{p.claimed_title_near}' vs halaman "
                            f"'{page_title}' (containment "
                            f"{containment:.2f}); tak cukup untuk "
                            "vonis, dilaporkan terbuka")


def _verify_domain(p, fetcher):
    """A bare domain claims only that the domain exists: ANY HTTP
    answer (even a 404 at the root — plenty of live projects serve
    nothing at the apex) proves the host is alive. Death requires
    connection-level failure on the apex AND on www.<host> (apex
    hosts that only serve under www are common)."""
    host = p.value
    if _host_malformed(host):
        p.status = "malformed"
        p.detail = f"domain '{host}' tanpa TLD dikenal"
        return
    res = fetcher.get("https://" + host + "/")
    if res.status is not None:
        p.status = "verified"
        p.detail = f"domain hidup (host menjawab HTTP {res.status})"
        return
    if res.error_kind == "other":
        p.status = "unverifiable"
        p.detail = f"domain: fetch error {res.error}"
        return
    if not host.startswith("www."):
        res2 = fetcher.get("https://www." + host + "/")
        if res2.status is not None:
            p.status = "verified"
            p.detail = (f"domain hidup via www "
                        f"(HTTP {res2.status}; apex tak menjawab)")
            return
    p.status = "dead"
    p.detail = ("domain: tak ter-resolve "
                f"({res.error_kind} di apex maupun www)")


_VERIFIERS = {"doi": _verify_doi, "eprint": _verify_eprint,
              "arxiv": _verify_arxiv, "url": _verify_url,
              "domain": _verify_domain}


# ------------------------------------------------------------ main entry

_LOG_DEFAULT = object()
_CANARY_URLS = ("https://api.crossref.org/works/10.1145/2504730.2504747",
                "https://doi.org/10.1145/2504730.2504747")


def _citation_log(record, log_path):
    if log_path is None:
        return
    try:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as ex:
        print(f"citation_verify: log write failed: {ex}",
              file=sys.stderr)


def verify_citations(draft, fetcher=None, mode=None, isr_id=None,
                     log_path=_LOG_DEFAULT):
    """Mechanically verify every citation pointer in one draft.
    `fetcher` is the test seam (an object with .get(url) ->
    FetchResult); the default is the production HttpFetcher.
    Always returns a structured dict and appends one record to the
    citation log (log_path default = CITATION_LOG; None disables):

    {performed, available, mode, verdict, block, findings,
     unverified, counts, pointers, error}

    verdict: "clean" (no findings), "findings" (recorded findings,
    none pivotal), "fatal" (>=1 pivotal dead/malformed/wrong —
    blocks ONLY in mode "block"), "unverified" (the checker could
    not run or could not judge the pivotal pointers — recorded
    loudly, NEVER blocks, NEVER reported as clean)."""
    if log_path is _LOG_DEFAULT:
        log_path = CITATION_LOG
    mode = mode or citation_mode()
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "isr": isr_id or None, "mode": mode,
              "draft_chars": len(draft or ""), "stage": "citation_verify"}
    result = {"performed": False, "available": False, "mode": mode,
              "verdict": "unverified", "block": False, "findings": [],
              "unverified": [], "counts": {}, "pointers": [],
              "error": None}
    fetcher = fetcher or HttpFetcher()
    pointers = extract_pointers(draft)

    # Canary: prove the egress works at all before judging pointers.
    canary_ok = False
    for canary in _CANARY_URLS:
        res = fetcher.get(canary)
        if res.status is not None:
            canary_ok = True
            break
    if not canary_ok:
        result["error"] = ("canary registry tak terjangkau — egress "
                           "pemeriksa mati; cek TIDAK berjalan")
        result["pointers"] = [p.as_dict() for p in pointers]
        record.update(result)
        record["loud"] = True
        _citation_log(record, log_path)
        print("citation_verify: PERINGATAN KERAS — canary Crossref/"
              "doi.org tak terjangkau; verifikasi sitasi TIDAK "
              "berjalan dan TIDAK memblokir", file=sys.stderr)
        return result

    fetches_before = fetcher.calls
    connect_before = fetcher.connect_failures
    for p in pointers:
        try:
            _VERIFIERS[p.kind](p, fetcher)
        except Exception as ex:  # noqa: BLE001 - per-pointer data
            p.status = "unverifiable"
            p.detail = f"verifier error: {type(ex).__name__}: {ex}"
    fetches = fetcher.calls - fetches_before
    connect_fails = fetcher.connect_failures - connect_before

    findings = [p for p in pointers
                if p.status in ("dead", "wrong_document", "malformed")]
    unverified = [p for p in pointers if p.status == "unverifiable"]
    pivotal_bad = [p for p in findings if p.pivotal]
    pivotal_unv = [p for p in unverified if p.pivotal]
    counts = {
        "pointers": len(pointers),
        "verified": sum(1 for p in pointers if p.status == "verified"),
        "findings": len(findings), "pivotal_findings": len(pivotal_bad),
        "unverified": len(unverified),
        "pivotal_unverified": len(pivotal_unv),
        "fetches": fetches,
    }
    result.update({"performed": True, "available": True,
                   "findings": [p.as_dict() for p in findings],
                   "unverified": [p.as_dict() for p in unverified],
                   "counts": counts,
                   "pointers": [p.as_dict() for p in pointers]})
    if (fetches >= 4 and connect_fails >= MASS_CONNECT_FAIL_RATIO
            * fetches):
        # Mass connection failure is the checker's egress dying,
        # not the draft's pointers: every connection-dead status is
        # re-marked unverifiable before the verdict is computed.
        for p in pointers:
            if p.status == "dead" and "tak ter-resolve" in p.detail:
                p.status = "unverifiable"
                p.detail += " [diturunkan: kegagalan egress massal]"
        findings = [p for p in pointers
                    if p.status in ("dead", "wrong_document",
                                    "malformed")]
        unverified = [p for p in pointers
                      if p.status == "unverifiable"]
        pivotal_bad = [p for p in findings if p.pivotal]
        result["findings"] = [p.as_dict() for p in findings]
        result["unverified"] = [p.as_dict() for p in unverified]
        result["pointers"] = [p.as_dict() for p in pointers]
        result["verdict"] = "unverified"
        result["error"] = (f"{connect_fails}/{fetches} fetch mati di "
                           "level koneksi — kegagalan egress massal, "
                           "bukan vonis atas draf")
    elif pivotal_bad:
        result["verdict"] = "fatal"
        result["block"] = bool(mode == "block")
    elif pivotal_unv and not any(
            p.pivotal and p.status == "verified" for p in pointers):
        result["verdict"] = "unverified"
        result["error"] = ("semua penunjuk poros tak terverifikasi "
                           "(bot-wall/jaringan) — dilaporkan terbuka, "
                           "tidak memblokir")
    elif findings:
        result["verdict"] = "findings"
    else:
        result["verdict"] = "clean"
    record.update({k: result[k] for k in
                   ("performed", "available", "verdict", "block",
                    "counts", "error")})
    record["findings"] = result["findings"]
    record["unverified"] = result["unverified"]
    _citation_log(record, log_path)
    return result
