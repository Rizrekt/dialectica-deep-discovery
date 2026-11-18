#!/usr/bin/env python3
"""Tests for the mechanical citation-verify layer
(citation_verify.py, built 2026-11-17 per user decision 10:39).

Proves, WITHOUT any real network (a deterministic FakeFetcher is
injected everywhere) and WITHOUT launching any serve:

- EXTRACTION: URLs deduped; doi.org URLs and bare DOIs are one DOI
  pointer; ePrint URL + textual form dedupe; arXiv URL + textual
  dedupe; bare domains extracted once (a domain inside a URL is not
  double-counted); claimed title/author captured from the citation
  context; pivotal classification P1 (pinpoint) / P2 (figure in
  sentence) / P4 (novelty closing) vs peripheral.
- VERDICTS: a healthy DOI verifies clean; a Crossref-404 DOI is
  FATAL and blocks in block mode but never in shadow mode; a DOI
  resolving to a DIFFERENT document (title mismatch) blocks; an
  ePrint pinpoint naming the wrong paper blocks; a dead bare
  domain is a recorded PERIPHERAL finding (no block); a no-TLD host
  is malformed; a bot-wall 403 is UNVERIFIABLE (no finding, no
  block); a pivotal pointer behind a bot-wall makes the run
  "unverified", never a silent pass.
- CHECKER-FAILURE DOCTRINE: canary down -> available=False,
  verdict "unverified", nothing blocked; mass connection failure
  downgrades connection-dead pointers to unverifiable and the run
  to "unverified".
- TLD RECOGNITION (fix 2026-11-17, SPOTCHECK-SISA-PILOT): real
  two-letter ccTLDs (.eu EUR-Lex, .fi docs.cow.fi) verify — they
  are recognised against ISO 3166-1 alpha-2, not a hand-kept
  whitelist; an UNASSIGNED two-letter code (.xq) and the no-TLD
  host (whitepaper.worldcoin) stay malformed.
- GATE: gate_answer without the stage reports citation_verify NOT
  performed and the clean fixture stays sendable; a blocking
  citation verdict withholds the fixture; a clean verdict keeps
  it sendable; a crashing callable never withholds; the arming
  helper follows DIALECTICA_CITATION_CHECK; the layer's mode
  default is "block" (unlike C5), shadow only when set.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citation_verify as cv  # noqa: E402
import serve_gate  # noqa: E402
import test_cloudflare_serve as tcs  # noqa: E402  (fixtures only)

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}  {detail}")


CANARY_CR = "https://api.crossref.org/works/10.1145/2504730.2504747"
CANARY_DOI = "https://doi.org/10.1145/2504730.2504747"
CR_REAL_DOI = "https://api.crossref.org/works/10.1145/2504730.2504747"
CR_FAKE_DOI = "https://api.crossref.org/works/10.1145/2516651.2516734"
CR_WRONG_DOI = "https://api.crossref.org/works/10.1000/xyz123"


def _crossref_json(title, authors):
    return json.dumps({"message": {
        "title": [title],
        "author": [{"family": a} for a in authors]}})


CANARY_OK = {CANARY_CR: cv.FetchResult(
    CANARY_CR, status=200,
    text=_crossref_json("A fistful of bitcoins", ["Meiklejohn"]))}


class FakeFetcher:
    """Deterministic fetcher seam: routes map URL -> FetchResult
    (missing route = connection failure). Mirrors HttpFetcher's
    cache + counters contract."""

    def __init__(self, routes):
        self.routes = dict(routes)
        self.calls = 0
        self.connect_failures = 0
        self._cache = {}

    def get(self, url):
        if url in self._cache:
            return self._cache[url]
        self.calls += 1
        result = self.routes.get(url)
        if result is None:
            result = cv.FetchResult(url, error="no route",
                                    error_kind="connect")
        if result.error_kind == "connect":
            self.connect_failures += 1
        self._cache[url] = result
        return result


def run(draft, routes, mode="block"):
    fetcher = FakeFetcher({**CANARY_OK, **routes})
    return cv.verify_citations(draft, fetcher=fetcher, mode=mode,
                               log_path=None)


# ------------------------------------------------------------ extraction

def extraction_cases():
    print("== extraction ==")
    draft = ('Text with https://example.com/a and again '
             'https://example.com/a plus (galxe.com) notes.')
    ps = cv.extract_pointers(draft)
    urls = [p for p in ps if p.kind == "url"]
    doms = [p for p in ps if p.kind == "domain"]
    check("extract: URL deduped to one pointer, 2 occurrences",
          len(urls) == 1 and len(urls[0].spans) == 2,
          f"urls={[(p.value, len(p.spans)) for p in urls]}")
    check("extract: bare domain found once",
          len(doms) == 1 and doms[0].value == "galxe.com",
          f"doms={[p.value for p in doms]}")

    draft = ('(Meiklejohn et al., "A Fistful of Bitcoins," ACM IMC '
             '2013 — https://doi.org/10.1145/2516651.2516734) and '
             'bare 10.1145/2516651.2516734 again.')
    ps = cv.extract_pointers(draft)
    dois = [p for p in ps if p.kind == "doi"]
    check("extract: doi.org URL + bare DOI are ONE doi pointer",
          len(dois) == 1 and len(dois[0].spans) == 2,
          f"dois={[(p.value, len(p.spans)) for p in dois]}")
    check("extract: claimed title + author captured",
          dois and dois[0].claimed_title == "A Fistful of Bitcoins"
          and dois[0].claimed_author == "Meiklejohn",
          f"title={dois[0].claimed_title!r} "
          f"author={dois[0].claimed_author!r}" if dois else "none")
    check("extract: DOI is pivotal via P1",
          bool(dois) and dois[0].pivotal
          and "P1-registry-pinpoint" in dois[0].pivotal_reasons)

    draft = ('[Lindell, "Secure Multiparty Computation (MPC)," IACR '
             'eprint 2020/940 — https://eprint.iacr.org/2020/940]')
    ps = cv.extract_pointers(draft)
    eps = [p for p in ps if p.kind == "eprint"]
    check("extract: ePrint URL + textual form dedupe",
          len(eps) == 1 and eps[0].value == "2020/940"
          and len(eps[0].spans) == 2,
          f"eps={[(p.value, len(p.spans)) for p in eps]}")
    check("extract: ePrint claimed author Lindell captured",
          bool(eps) and eps[0].claimed_author == "Lindell",
          f"author={eps[0].claimed_author!r}" if eps else "none")

    draft = ('See arXiv:2101.00001 and '
             'https://arxiv.org/abs/2101.00001 for details.')
    ps = cv.extract_pointers(draft)
    axs = [p for p in ps if p.kind == "arxiv"]
    check("extract: arXiv textual + URL dedupe",
          len(axs) == 1 and axs[0].value == "2101.00001",
          f"axs={[p.value for p in axs]}")

    draft = ('The scheme kept 50% of the allocation '
             '(docs.example.org). A plain note (plain.example.net).'
             '\n\nNew in this answer: the anchor is '
             'https://anchor.example.io/x.')
    ps = {p.value: p for p in cv.extract_pointers(draft)}
    check("extract: figure sentence makes its pointer pivotal (P2)",
          ps["docs.example.org"].pivotal
          and "P2-figure-in-sentence"
          in ps["docs.example.org"].pivotal_reasons)
    check("extract: plain pointer stays peripheral",
          not ps["plain.example.net"].pivotal)
    check("extract: novelty-closing pointer pivotal (P4)",
          ps["https://anchor.example.io/x"].pivotal
          and "P4-novelty-closing"
          in ps["https://anchor.example.io/x"].pivotal_reasons)


def extraction_fix_cases():
    print("== extraction fixes (calibration round 1) ==")
    # AMS-style DOI with balanced parens + angle segment, cited via
    # a doi.org URL inside wrapping parens: must be captured WHOLE.
    draft = ('(see https://doi.org/10.1175/1520-0469(1993)050'
             '<3625:MVATAS>2.0.CO;2) for the result.')
    ps = cv.extract_pointers(draft)
    dois = [p for p in ps if p.kind == "doi"]
    check("extract: AMS DOI with parens/angles captured whole",
          len(dois) == 1 and dois[0].value
          == "10.1175/1520-0469(1993)050<3625:MVATAS>2.0.CO;2",
          f"dois={[p.value for p in dois]}")
    # Balanced-paren URL kept whole; prose wrapping paren trimmed.
    draft = ('Wiki (https://en.wikipedia.org/wiki/Foo_(bar)) and '
             'prose (https://example.com/page).')
    urls = [p.value for p in cv.extract_pointers(draft)
            if p.kind == "url"]
    check("extract: balanced-paren URL whole, prose paren trimmed",
          "https://en.wikipedia.org/wiki/Foo_(bar)" in urls
          and "https://example.com/page" in urls,
          f"urls={urls}")
    # Bare DOI at a sentence end: trailing period is not part of it.
    draft = 'Cite 10.1029/93JE00547. Next sentence.'
    dois = [p.value for p in cv.extract_pointers(draft)
            if p.kind == "doi"]
    check("extract: bare DOI sentence period trimmed",
          dois == ["10.1029/93JE00547"], f"dois={dois}")
    # Near-title rule: a distant quoted phrase is NOT a title claim
    # about a plain URL; an adjacent one IS.
    draft = ('He wrote "at most N emails" can be enforced, and much '
             'later prose follows with many more words in between '
             'before the link (BrightID — https://www.brightid.org/).')
    ps = [p for p in cv.extract_pointers(draft) if p.kind == "url"]
    check("extract: distant quote is not the URL's claimed title",
          bool(ps) and ps[0].claimed_title_near is None,
          f"near={ps[0].claimed_title_near!r}" if ps else "none")
    draft = ('Ohlhaver, Weyl & Buterin, "Decentralized Society: '
             'Finding Web3\'s Original Sybil," 2022 — '
             'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1)')
    ps = [p for p in cv.extract_pointers(draft) if p.kind == "url"]
    check("extract: adjacent quoted title IS the URL's claimed title",
          bool(ps) and ps[0].claimed_title_near
          == "Decentralized Society: Finding Web3's Original Sybil",
          f"near={ps[0].claimed_title_near!r}" if ps else "none")
    # Prose quote + short gap but NO author apparatus -> not near
    # (the webauthn false-positive species from calibration).
    draft = ('so "at most N emails" is not (W3C WebAuthn Level 2 — '
             'https://www.w3.org/TR/webauthn-2/) at all.')
    ps = [p for p in cv.extract_pointers(draft) if p.kind == "url"]
    check("extract: prose quote without author is not a title claim",
          bool(ps) and ps[0].claimed_title_near is None,
          f"near={ps[0].claimed_title_near!r}" if ps else "none")


# ------------------------------------------------------------ verdicts

_EPRINT_META = ('<html><head>'
                '<meta name="citation_title" content="{title}">'
                '<meta name="citation_author" content="{author}">'
                '</head></html>')


def verdict_cases():
    print("== verdicts ==")
    # Healthy DOI -> clean.
    draft = ('(Meiklejohn et al., "A Fistful of Bitcoins," ACM IMC '
             '2013 — https://doi.org/10.1145/2504730.2504747)')
    out = run(draft, {CR_REAL_DOI: cv.FetchResult(
        CR_REAL_DOI, status=200, text=_crossref_json(
            "A fistful of bitcoins",
            ["Meiklejohn", "Pomarole", "Jordan", "Levchenko"]))})
    check("verdict: healthy DOI verifies clean, no block",
          out["verdict"] == "clean" and out["block"] is False
          and out["counts"]["verified"] == 1,
          f"verdict={out['verdict']} counts={out['counts']}")

    # Fabricated DOI (Crossref 404 AND doi.org 404) -> fatal +
    # block; shadow: no block.
    draft = ('(Meiklejohn et al., "A Fistful of Bitcoins," ACM IMC '
             '2013 — https://doi.org/10.1145/2516651.2516734)')
    routes = {CR_FAKE_DOI: cv.FetchResult(CR_FAKE_DOI, status=404,
                                          text="Resource not found."),
              "https://doi.org/10.1145/2516651.2516734":
              cv.FetchResult(
                  "https://doi.org/10.1145/2516651.2516734",
                  status=404, text="DOI Not Found")}
    out = run(draft, routes, mode="block")
    check("verdict: Crossref+doi.org-404 DOI is FATAL, blocks (block)",
          out["verdict"] == "fatal" and out["block"] is True
          and out["findings"][0]["status"] == "dead",
          f"verdict={out['verdict']} block={out['block']}")
    out = run(draft, routes, mode="shadow")
    check("verdict: same DOI in shadow mode never blocks",
          out["verdict"] == "fatal" and out["block"] is False)

    # Legacy DOI: absent from Crossref but registered at doi.org
    # -> exists, verified, never blocks.
    draft = ('(Leovy & Zurek, "Thermal Tides," Icarus 1979 — '
             'https://doi.org/10.1016/0019-1035(79)90069-4)')
    from urllib.parse import quote as _q
    legacy_doi = "10.1016/0019-1035(79)90069-4"
    cr_legacy = "https://api.crossref.org/works/" + _q(legacy_doi,
                                                       safe="/")
    doiorg_legacy = "https://doi.org/" + _q(legacy_doi, safe="/")
    routes = {cr_legacy: cv.FetchResult(cr_legacy, status=404),
              doiorg_legacy: cv.FetchResult(
                  doiorg_legacy, status=200,
                  final_url="https://example.com/paper")}
    out = run(draft, routes, mode="block")
    check("verdict: Crossref-404 but doi.org-live DOI verifies",
          out["verdict"] == "clean" and out["block"] is False
          and out["counts"]["verified"] == 1,
          f"verdict={out['verdict']} counts={out['counts']}")

    # DOI exists but is a DIFFERENT document -> wrong_document block.
    draft = ('(Smith, "Quantum Widget Theory," 2020 — '
             'https://doi.org/10.1000/xyz123)')
    out = run(draft, {CR_WRONG_DOI: cv.FetchResult(
        CR_WRONG_DOI, status=200, text=_crossref_json(
            "Medieval Poetry of the Baltic", ["Jones"]))})
    check("verdict: DOI pointing at another document blocks",
          out["verdict"] == "fatal" and out["block"] is True
          and out["findings"][0]["status"] == "wrong_document",
          f"findings={out['findings']}")

    # ePrint wrong paper (the 635a010d species) -> block.
    draft = ('[Lindell, "Secure Multiparty Computation (MPC)," IACR '
             'eprint 2020/940 — https://eprint.iacr.org/2020/940]')
    url = "https://eprint.iacr.org/2020/940"
    out = run(draft, {url: cv.FetchResult(url, status=200, text=
        _EPRINT_META.format(
            title="Directly revocable ciphertext-policy "
                  "attribute-based encryption from lattices",
            author="Fei Meng"))})
    check("verdict: ePrint pinpoint naming the wrong paper blocks",
          out["verdict"] == "fatal" and out["block"] is True
          and out["findings"][0]["status"] == "wrong_document",
          f"findings={out['findings']}")
    # ePrint right paper -> verified.
    draft = ('[Meng, "Directly revocable ciphertext-policy '
             'attribute-based encryption from lattices," IACR '
             'eprint 2020/940 — https://eprint.iacr.org/2020/940]')
    out = run(draft, {url: cv.FetchResult(url, status=200, text=
        _EPRINT_META.format(
            title="Directly revocable ciphertext-policy "
                  "attribute-based encryption from lattices",
            author="Fei Meng"))})
    check("verdict: ePrint pinpoint naming the right paper verifies",
          out["verdict"] == "clean" and out["block"] is False,
          f"verdict={out['verdict']}")

    # arXiv healthy -> verified.
    draft = 'Preprint arXiv:2101.00001 covers the construction.'
    api = "https://export.arxiv.org/api/query?id_list=2101.00001"
    atom = ('<feed><entry><title>Some Construction</title>'
            '<author><name>Doe, Jane</name></author></entry></feed>')
    out = run(draft, {api: cv.FetchResult(api, status=200, text=atom)})
    check("verdict: healthy arXiv id verifies",
          out["verdict"] == "clean"
          and out["counts"]["verified"] == 1,
          f"verdict={out['verdict']} counts={out['counts']}")

    # Dead bare domain (peripheral) -> recorded finding, NO block.
    draft = ('Proof of Humanity uses video enrollment plus deposit '
             'and challenge (proofofhumanity.site).')
    out = run(draft, {})  # no route -> connection failure
    check("verdict: dead peripheral domain = finding, no block",
          out["verdict"] == "findings" and out["block"] is False
          and out["findings"][0]["status"] == "dead"
          and out["findings"][0]["pivotal"] is False,
          f"verdict={out['verdict']} findings={out['findings']}")

    # No-TLD URL -> malformed (peripheral here), no fetch needed.
    draft = ('biometric uniqueness (World ID — '
             'https://whitepaper.worldcoin/).')
    out = run(draft, {})
    check("verdict: no-TLD host is a malformed finding",
          out["verdict"] == "findings"
          and out["findings"][0]["status"] == "malformed",
          f"findings={out['findings']}")

    # Bare domain whose root answers 404: the host EXISTS -> alive.
    draft = 'Also listed at (hop.exchange).'
    url = "https://hop.exchange/"
    out = run(draft, {url: cv.FetchResult(url, status=404)})
    check("verdict: bare domain with HTTP 404 root is alive",
          out["verdict"] == "clean" and out["findings"] == [],
          f"verdict={out['verdict']} findings={out['findings']}")
    # Bare domain dead at apex but alive under www -> verified.
    draft = 'Also listed at (brightid.org).'
    out = run(draft, {
        "https://brightid.org/": cv.FetchResult(
            "https://brightid.org/", error="boom",
            error_kind="connect"),
        "https://www.brightid.org/": cv.FetchResult(
            "https://www.brightid.org/", status=200)})
    check("verdict: apex-dead but www-alive domain verifies",
          out["verdict"] == "clean"
          and out["counts"]["verified"] == 1,
          f"verdict={out['verdict']} counts={out['counts']}")
    # URL page-title comparison fires ONLY for a near claimed title:
    # a completely different page title is a wrong document...
    draft = ('Ohlhaver, Weyl & Buterin, "Decentralized Society: '
             'Finding Web3\'s Original Sybil," 2022 — '
             'https://papers.example.com/paper)')
    url = "https://papers.example.com/paper"
    page = ('<html><head><title>Quantum Widgets Quarterly</title>'
            '</head></html>')
    out = run(draft, {url: cv.FetchResult(url, status=200, text=page)})
    check("verdict: near title vs unrelated page title = wrong doc",
          out["findings"] and out["findings"][0]["status"]
          == "wrong_document",
          f"findings={out['findings']}")
    # ...while a one-word subtitle swap is honestly UNVERIFIABLE
    # (token arithmetic cannot convict it), never a silent pass.
    page = ('<html><head><title>Decentralized Society: Finding '
            'Web3\'s Soul</title></head></html>')
    out = run(draft, {url: cv.FetchResult(url, status=200, text=page)})
    check("verdict: subtitle swap = unverifiable, not passed silently",
          out["findings"] == [] and len(out["unverified"]) == 1
          and out["block"] is False,
          f"findings={out['findings']} unv={out['unverified']}")
    draft = ('He wrote "at most N emails" can be enforced, and much '
             'later prose follows with many more words in between '
             'before the link (BrightID — https://www.brightid.org/).')
    url = "https://www.brightid.org/"
    out = run(draft, {url: cv.FetchResult(
        url, status=200,
        text="<html><head><title>BrightID</title></head></html>")})
    check("verdict: distant quote never compared to page title",
          out["verdict"] == "clean" and out["findings"] == [],
          f"verdict={out['verdict']} findings={out['findings']}")

    # Bot-wall 403 on a peripheral URL -> unverifiable, clean-ish.
    draft = 'Docs at https://walled.example.com/guide explain it.'
    url = "https://walled.example.com/guide"
    out = run(draft, {url: cv.FetchResult(url, status=403,
                                          text="Just a moment...")})
    check("verdict: bot-wall 403 is unverifiable, not a finding",
          out["findings"] == [] and out["block"] is False
          and len(out["unverified"]) == 1,
          f"findings={out['findings']} unv={out['unverified']}")
    # Bot-wall on the ONLY pivotal pointer -> run is "unverified".
    draft = ('The scheme kept 50% of tokens '
             '(https://walled.example.com/guide).')
    out = run(draft, {url: cv.FetchResult(url, status=403,
                                          text="Just a moment...")})
    check("verdict: pivotal pointer behind bot-wall -> unverified run",
          out["verdict"] == "unverified" and out["block"] is False,
          f"verdict={out['verdict']}")


# ------------------------------------------------------------ failure doctrine

def failure_cases():
    print("== checker-failure doctrine ==")
    # Canary down: both canary URLs connection-fail.
    fetcher = FakeFetcher({})
    out = cv.verify_citations("Anything (example.com).",
                              fetcher=fetcher, mode="block",
                              log_path=None)
    check("failure: canary down -> unavailable, unverified, no block",
          out["performed"] is False and out["available"] is False
          and out["verdict"] == "unverified"
          and out["block"] is False,
          f"out={ {k: out[k] for k in ('performed', 'verdict', 'block')} }")

    # Mass connection failure: canary via doi.org OK, then >=40% of
    # pointer fetches die at connection level -> downgrade.
    routes = {CANARY_CR: cv.FetchResult(CANARY_CR,
                                        error="down",
                                        error_kind="connect"),
              CANARY_DOI: cv.FetchResult(CANARY_DOI, status=200)}
    draft = ("One (a-one.example.com). Two (b-two.example.net). "
             "Three (c-three.example.org). Four (d-four.example.io).")
    out = run(draft, routes)
    check("failure: mass connect failure downgrades run to unverified",
          out["verdict"] == "unverified" and out["block"] is False
          and all(u["status"] == "unverifiable"
                  for u in out["unverified"]),
          f"verdict={out['verdict']} unv={len(out['unverified'])}")


# ------------------------------------------------------------ gate wiring

def gate_cases():
    print("== gate wiring ==")
    good = tcs.good_text()
    os.environ.pop(cv.CITATION_ARM_ENV, None)
    result = serve_gate.gate_answer(good)
    check("gate: unarmed -> citation stage NOT performed, sendable",
          result["sendable"] is True
          and result["gate"]["citation_verify"]["performed"] is False,
          f"sendable={result['sendable']}")

    def fake_block(text):
        return {"performed": True, "mode": "block",
                "verdict": "fatal", "block": True,
                "findings": [{"pointer": "x"}], "unverified": [],
                "counts": {}, "error": None}

    result = serve_gate.gate_answer(good, citation_check=fake_block)
    check("gate: blocking citation verdict WITHHOLDS the fixture",
          result["sendable"] is False
          and any("sitasi" in r for r in result["gate"]["reasons"]),
          f"sendable={result['sendable']} "
          f"reasons={result['gate']['reasons']}")

    def fake_clean(text):
        return {"performed": True, "mode": "block",
                "verdict": "clean", "block": False, "findings": [],
                "unverified": [], "counts": {}, "error": None}

    result = serve_gate.gate_answer(good, citation_check=fake_clean)
    check("gate: clean citation verdict keeps the fixture sendable",
          result["sendable"] is True
          and result["gate"]["citation_verify"]["verdict"] == "clean")

    def fake_crash(text):
        raise RuntimeError("resolver exploded")

    result = serve_gate.gate_answer(good, citation_check=fake_crash)
    check("gate: crashing citation callable never withholds",
          result["sendable"] is True
          and result["gate"]["citation_verify"]["performed"] is False
          and result["gate"]["citation_verify"]["mode"]
          == "injected-check-error")

    check("arming: unarmed helper returns None",
          serve_gate.armed_citation_check() is None)
    os.environ[cv.CITATION_ARM_ENV] = "1"
    try:
        check("arming: DIALECTICA_CITATION_CHECK=1 yields a callable",
              callable(serve_gate.armed_citation_check()))
    finally:
        os.environ.pop(cv.CITATION_ARM_ENV, None)

    os.environ.pop(cv.CITATION_MODE_ENV, None)
    check("mode: layer default is block (not shadow)",
          cv.citation_mode() == "block")
    os.environ[cv.CITATION_MODE_ENV] = "shadow"
    try:
        check("mode: explicit shadow honoured",
              cv.citation_mode() == "shadow")
    finally:
        os.environ.pop(cv.CITATION_MODE_ENV, None)


# ------------------------------------------------------------ TLD fix

def tld_cases():
    print("== TLD recognition (ccTLD fix) ==")
    check("tld: .eu and .fi recognised as ccTLDs",
          cv._tld_recognized("eu") and cv._tld_recognized("fi"))
    check("tld: assigned ccTLDs recognised (de, jp, br, za)",
          all(cv._tld_recognized(t)
              for t in ("de", "jp", "br", "za")))
    check("tld: unassigned two-letter codes NOT recognised",
          not cv._tld_recognized("xq")
          and not cv._tld_recognized("zz"))
    check("tld: fabricated label NOT recognised",
          not cv._tld_recognized("worldcoin"))
    check("tld: eur-lex.europa.eu host not malformed",
          cv._host_malformed("eur-lex.europa.eu") is False)
    check("tld: docs.cow.fi host not malformed",
          cv._host_malformed("docs.cow.fi") is False)
    check("tld: no-TLD host still malformed",
          cv._host_malformed("whitepaper.worldcoin") is True)
    check("tld: unassigned-code host still malformed",
          cv._host_malformed("example.xq") is True)

    # EUR-Lex URL (the d21135d5 false positive) verifies end-to-end.
    draft = ('MiCA is Regulation (EU) 2023/1114 '
             '(https://eur-lex.europa.eu/eli/reg/2023/1114/oj).')
    url = "https://eur-lex.europa.eu/eli/reg/2023/1114/oj"
    out = run(draft, {url: cv.FetchResult(
        url, status=200,
        text="<html><body>Regulation (EU) 2023/1114</body></html>")})
    check("tld: EUR-Lex .eu URL verifies, no malformed finding",
          out["verdict"] == "clean"
          and out["counts"]["verified"] == 1
          and not any(f["status"] == "malformed"
                      for f in out["findings"]),
          f"verdict={out['verdict']} findings={out['findings']}")

    # Bare docs.cow.fi domain (the 5e905bef false positive) verifies.
    draft = 'Orders are signed off-chain with validity windows ' \
            '(docs.cow.fi).'
    url = "https://docs.cow.fi/"
    out = run(draft, {url: cv.FetchResult(
        url, status=200, text="<html><body>CoW Protocol</body>"
        "</html>")})
    check("tld: bare docs.cow.fi domain verifies",
          out["verdict"] == "clean"
          and out["counts"]["verified"] == 1,
          f"verdict={out['verdict']} findings={out['findings']}")

    # Fabricated two-letter TLD in a URL stays a malformed finding.
    draft = 'See https://example.xq/paper for the full text.'
    out = run(draft, {})
    check("tld: fabricated .xq URL is a malformed finding",
          out["findings"]
          and out["findings"][0]["status"] == "malformed",
          f"findings={out['findings']}")


if __name__ == "__main__":
    extraction_cases()
    extraction_fix_cases()
    verdict_cases()
    failure_cases()
    tld_cases()
    gate_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
