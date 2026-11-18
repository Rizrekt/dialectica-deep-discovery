#!/usr/bin/env python3
"""KONTEKS KEBARUAN untuk pemeriksa C5 — Surprise Gauge context
(built 2026-11-17, KONTEKS-KEBARUAN-C5-2026-11-17.md).

THE GAP THIS CLOSES (KALIBRASI-C5 §6 risk 4): the C5 checker judges
a draft against the question context the serve pipeline hands it —
the ISR text alone. The verified answers already on the question
never ride along, so the checker has nothing to compare the draft
against and SURPRISE_GAUGE — the field's #1 rejection (67%,
DATA-LIVE-ARENA-2026-11-17) and the gate on the Innovator +10 cell
(novelty >= 15%) — is practically silent in production: the checker
prompt itself forbids flagging it without context evidence.

This module builds that missing context from the client's OWN read
path — the same endpoint `trued question` uses
(GET /api/node/isos/{isr_id} -> {"isos": [...]}; a verified answer's
text lives at reveal.data.structured_data.answer, forecasting
answers at .reasoning). No field is invented: filtering, sorting
and excerpting use only status / supportedCount / refutationCount /
timestamp / id / isOwnAgent, exactly as cmd_question and
calibrate_semantic_c5 read them.

BLOCK SHAPE (appended to the question string handed to
serve_gate.semantic_check; since R3 serve_gate splits it off and
re-attaches it as its own prompt section, EXEMPT from the 12k
question cap — MITIGASI-KONTEKS-TERPOTONG-2026-11-17):
  - a header naming the total verified count and how many are
    excerpted;
  - a COVERED list: each verified answer's own headings / bold
    lead-ins / first sentence — the cheap, dense map of what has
    already been said (collected from ALL verified answers, not
    just the excerpted ones);
  - EXCERPTS of the most-supported verified answers (per-answer
    cap, count cap, total block cap), so the checker can compare
    substance, not just titles.
When the assembled block exceeds its own total cap it is
COMPACTED in stages that protect BOTH signals — the per-excerpt
cap shrinks first, then the weakest excerpts drop, then the
covered list trims from the end but never below COVER_FLOOR,
and only as a last resort does the excerpt cap fall to its
hard floor — and a note inside the block says so
(COMPACTED_MARK); it is never blind-cut mid-text. (The R3 order
trimmed the covered list first and could sacrifice the whole
map on excerpt-dense ISRs — 24 -> 0 points on the live R3
specimen; PEMADATAN-DUA-SINYAL-2026-11-17.md.)
An ISR with no verified answers (viso 0, the Pioneer shape) yields
an EMPTY block — a legitimate state, stated in the meta, never an
error. Every failure (fetch down, malformed payload) is likewise
data: context_for_isr returns ("", meta) and never raises, so a
novelty outage can never break or block the semantic check itself.

ARMING: serve_gate.armed_semantic_check attaches the block only
when the C5 stage itself is armed (DIALECTICA_SEMANTIC_CHECK=1)
AND this module's sub-flag allows it — DIALECTICA_SEMANTIC_NOVELTY:
unset or any value but "0" = follow the parent flag; "0" = novelty
context OFF while the rest of C5 keeps running. The isos fetch
additionally rides the serve gate's own fetch arming
(DIALECTICA_SERVE_GATE_FETCH=1, set by run_serve for the gated
Vyce lane alongside the semantic flag): unarmed, no network is
touched and the state is reported "disabled", exactly like
serve_gate.fetch_isr_detail.
"""
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TRUED_DIR = os.path.expanduser(
    "~/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
FETCH_ENV = "DIALECTICA_SERVE_GATE_FETCH"
NOVELTY_ENV = "DIALECTICA_SEMANTIC_NOVELTY"

# Size budget. The block travels inside semantic_check's question
# argument, but since R3 build_semantic_prompt splits it off and
# re-attaches it whole as its own section — the 12_000-char cap
# binds the question text only. BLOCK_CAP is therefore the block's
# OWN budget, enforced by staged compaction in build_block.
BLOCK_CAP = 6000            # total block chars (header + lists)
ANSWER_EXCERPT_CAP = 1100   # per excerpted answer
MAX_EXCERPTS = 5            # most-supported answers excerpted
MAX_COVER_POINTS = 24       # covered-list entries across all answers
COVER_POINT_CAP = 110       # per covered-list entry
_EXCERPT_CAP_FLOOR = 200    # compaction never shrinks excerpts below
# Dual-signal compaction floors (PEMADATAN-DUA-SINYAL-2026-11-17).
# COVER_FLOOR: the covered map is never trimmed below this many
# points. 8 = MAX_COVER_POINTS / 3; worst-case cost 8 x
# (COVER_POINT_CAP + 3 render chars) = 904 chars, ~15% of
# BLOCK_CAP (on the live R3 specimen the 24 points averaged
# 65 chars, so the floor costs ~520 there) — cheap insurance for
# the breadth signal SURPRISE_GAUGE reads first.
COVER_FLOOR = 8             # covered points compaction keeps, minimum
# _EXCERPT_CAP_SOFT_FLOOR: stage (a) shrinks the per-excerpt cap
# (x0.7 steps from ANSWER_EXCERPT_CAP) only down to here; the
# fall from here to _EXCERPT_CAP_FLOOR is stage (d), the last
# resort after excerpt drops and the covered trim are spent.
_EXCERPT_CAP_SOFT_FLOOR = 500

BLOCK_HEADER = "EXISTING VERIFIED ANSWERS — SURPRISE GAUGE CONTEXT"
# First words of the in-block note that announces a compaction;
# serve_gate scans for it to log novelty_compacted (R3).
COMPACTED_MARK = "Novelty context compacted"


def novelty_enabled():
    """Sub-flag: default follows the parent C5 arming; only an
    explicit "0" switches the novelty context off on its own."""
    return os.environ.get(NOVELTY_ENV, "").strip() != "0"


# ------------------------------------------------------------ fetching

def fetch_isos(isr_id, caller=None):
    """(isos_or_None, state) — state "ok" / "failed" / "disabled".
    Read-only GET over the client's own call(); only touches the
    network when the serve gate's fetch is armed (FETCH_ENV=1),
    mirroring serve_gate.fetch_isr_detail. `caller` is the test
    seam: a callable isr_id -> the endpoint's decoded payload."""
    if caller is None and os.environ.get(FETCH_ENV) != "1":
        return None, "disabled"
    if not isr_id:
        return None, "failed"
    try:
        if caller is not None:
            data = caller(isr_id)
        else:
            if TRUED_DIR not in sys.path:
                sys.path.insert(0, TRUED_DIR)
            import trued
            data = trued.call(
                f"/api/node/isos/"
                f"{urllib.parse.quote(str(isr_id), safe='')}",
                timeout=30)
    except BaseException:  # noqa: BLE001 - includes SystemExit
        return None, "failed"
    if isinstance(data, dict):
        data = data.get("isos")
    if not isinstance(data, list):
        return None, "failed"
    return data, "ok"


# ------------------------------------------------------- pure assembly

def iso_answer_text(iso):
    """A verified answer's text, from the exact path the client
    prints: reveal.data.structured_data — `answer` for the classic
    schema, `reasoning` for forecasting answers. "" when the ISO
    carries no revealed text."""
    sd = ((iso.get("reveal") or {}).get("data") or {}).get(
        "structured_data") or {}
    return str(sd.get("answer") or sd.get("reasoning") or "")


def verified_answers(isos):
    """The verified answers among `isos`, as flat records sorted
    most-supported first (ties: newest first) — the most
    established coverage leads the block. Answers whose text is
    not revealed are counted in the total but cannot be excerpted;
    they are returned with text "" so the caller can say so."""
    out = []
    for iso in isos or []:
        if not isinstance(iso, dict) or iso.get("status") != "verified":
            continue
        try:
            supported = int(iso.get("supportedCount") or 0)
        except (TypeError, ValueError):
            supported = 0
        try:
            refuted = int(iso.get("refutationCount") or 0)
        except (TypeError, ValueError):
            refuted = 0
        out.append({
            "id": str(iso.get("id") or ""),
            "supported": supported,
            "refuted": refuted,
            "own": bool(iso.get("isOwnAgent")),
            "timestamp": iso.get("timestamp") or 0,
            "text": iso_answer_text(iso),
        })
    out.sort(key=lambda a: (-a["supported"], -_ts_key(a["timestamp"])))
    return out


def _ts_key(ts):
    try:
        return float(ts)
    except (TypeError, ValueError):
        return 0.0


_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
_BOLD_LEAD_RE = re.compile(r"\*\*([^*]{8,110})\*\*")


def coverage_points(text, limit=4):
    """What an existing answer already covers, in its own words:
    its markdown headings first, then bold lead-ins, then (when it
    has neither) its first sentence. Mechanical extraction only —
    nothing is paraphrased or summarised by us."""
    text = text or ""
    points = []
    for m in _HEADING_RE.finditer(text):
        p = m.group(1).strip().strip("*").strip()
        if p and p not in points:
            points.append(p[:COVER_POINT_CAP])
        if len(points) >= limit:
            return points
    for m in _BOLD_LEAD_RE.finditer(text):
        p = m.group(1).strip()
        if p and p not in points:
            points.append(p[:COVER_POINT_CAP])
        if len(points) >= limit:
            return points
    if not points:
        flat = " ".join(text.split())
        first = re.split(r"(?<=[.!?])\s+", flat, maxsplit=1)[0]
        if first:
            points.append(first[:COVER_POINT_CAP])
    return points


def _render_block(total, readable_count, unrevealed, covered,
                  excerpted, excerpt_cap, compacted):
    """Assemble the block text from explicit parts, so build_block
    can re-render it at each compaction stage with honest counts
    (the intro and the "+N further" note always describe the parts
    actually present)."""
    lines = [
        BLOCK_HEADER,
        f"This question already has {total} verified "
        f"answer(s). The {len(excerpted)} most-supported are "
        "excerpted below; the covered list spans all of them. "
        "Content already present here is NOT new: a draft that "
        "merely restates or paraphrases it — adding no new fact, "
        "mechanism, figure or angle — stops at the Surprise "
        "Gauge.",
        "Already covered (the existing answers' own headings / "
        "lead claims):",
    ]
    lines += [f"- {p}" for p in covered]
    if compacted:
        lines.append(
            f"({COMPACTED_MARK} to fit its {BLOCK_CAP}-char "
            f"budget: covered list at {len(covered)} "
            f"point(s), {len(excerpted)} excerpt(s) at "
            f"≤{excerpt_cap} chars each. The excerpts below are "
            "complete at that size — nothing here was cut "
            "mid-text.)")
    # The honesty notes ride BEFORE the excerpts: the excerpts are
    # the bulk, so any pressure lands on them, never the counts.
    if readable_count > len(excerpted):
        lines.append(
            f"(+{readable_count - len(excerpted)} further verified "
            "answers not excerpted — see the covered list above.)")
    if unrevealed:
        lines.append(
            f"({unrevealed} verified answer(s) carry no "
            "revealed text and could not be excerpted.)")
    for idx, a in enumerate(excerpted):
        lines.append(
            f"--- Verified Answer {idx + 1} (id {a['id'][:8]} · "
            f"supported {a['supported']} · refuted {a['refuted']}"
            f"{' · own earlier answer' if a['own'] else ''}) ---")
        lines.append(a["text"][:excerpt_cap])
    return "\n".join(lines)


def build_block(isos):
    """(block, meta) from a raw isos list. Pure. An empty block is
    the honest answer for viso 0 and for "verified exist but none
    revealed" — meta says which, and how much was left out. A block
    over BLOCK_CAP is compacted in stages that protect both
    signals, cheapest sacrifice first: (a) the per-excerpt cap
    shrinks in x0.7 steps, but only to _EXCERPT_CAP_SOFT_FLOOR;
    (b) the weakest excerpts drop (the list is most-supported
    first, so the tail is the weakest), down to one; (c) the
    covered list trims from the end, one point at a time, but
    never below COVER_FLOOR — the map is never sacrificed whole
    again; (d) last resort, the per-excerpt cap falls in x0.7
    steps to its hard floor _EXCERPT_CAP_FLOOR. The guaranteed
    minimum block (COVER_FLOOR points at full point cap + one
    excerpt at the hard floor + fixed overhead and notes,
    ~1,930 chars on the R3 specimen's sizes) sits far under
    BLOCK_CAP, so both floors are honourable before the defensive
    cut below ever matters. The block itself announces the
    compaction; meta["compacted"] mirrors it."""
    answers = verified_answers(isos)
    meta = {"verified_total": len(answers), "excerpted": 0,
            "covered_points": 0, "block_chars": 0, "compacted": False,
            "unrevealed": sum(1 for a in answers if not a["text"])}
    readable = [a for a in answers if a["text"]]
    if not readable:
        return "", meta
    covered, seen = [], set()
    for a in answers:
        for p in coverage_points(a["text"]):
            if p not in seen:
                seen.add(p)
                covered.append(p)
            if len(covered) >= MAX_COVER_POINTS:
                break
        if len(covered) >= MAX_COVER_POINTS:
            break
    covered = list(covered)
    excerpted = list(readable[:MAX_EXCERPTS])
    excerpt_cap = ANSWER_EXCERPT_CAP
    compacted = False
    block = _render_block(len(answers), len(readable),
                          meta["unrevealed"], covered, excerpted,
                          excerpt_cap, compacted)
    while len(block) > BLOCK_CAP:
        compacted = True
        if excerpt_cap > _EXCERPT_CAP_SOFT_FLOOR:
            # (a) excerpt depth first: the cap shrinks, both
            # signals stay whole.
            excerpt_cap = max(_EXCERPT_CAP_SOFT_FLOOR,
                              int(excerpt_cap * 0.7))
        elif len(excerpted) > 1:
            # (b) the weakest excerpt drops (tail = weakest).
            excerpted = excerpted[:-1]
        elif len(covered) > COVER_FLOOR:
            # (c) the map trims from the end, one point at a
            # time — and stops at COVER_FLOOR.
            covered = covered[:-1]
        elif excerpt_cap > _EXCERPT_CAP_FLOOR:
            # (d) last resort: the cap falls to its hard floor.
            excerpt_cap = max(_EXCERPT_CAP_FLOOR,
                              int(excerpt_cap * 0.7))
        else:
            break  # unreachable in practice (see the guaranteed
            # minimum in the docstring); the guard below still
            # honours the cap.
        block = _render_block(len(answers), len(readable),
                              meta["unrevealed"], covered, excerpted,
                              excerpt_cap, compacted)
    if len(block) > BLOCK_CAP:  # defensive: cap is a hard promise
        block = block[:BLOCK_CAP]
    meta.update({"excerpted": len(excerpted),
                 "covered_points": len(covered),
                 "block_chars": len(block),
                 "compacted": compacted})
    return block, meta


def context_for_isr(isr_id, isos_fetcher=None):
    """(block, meta) for one ISR — fetch + build, never raises.
    meta.state: "ok" (block built, possibly empty at viso 0),
    "disabled" (fetch not armed), "failed" (fetch or payload
    unusable). An empty block with state "ok" and verified_total
    0 is the legitimate Pioneer shape."""
    meta = {"state": "failed", "verified_total": 0, "excerpted": 0,
            "covered_points": 0, "block_chars": 0, "compacted": False,
            "unrevealed": 0}
    try:
        fetcher = isos_fetcher or fetch_isos
        isos, state = fetcher(isr_id)
        meta["state"] = state
        if state != "ok":
            return "", meta
        block, built = build_block(isos)
        meta.update(built)
        meta["state"] = "ok"
        return block, meta
    except Exception as ex:  # noqa: BLE001 - context is advisory
        meta["state"] = "failed"
        meta["error"] = f"{type(ex).__name__}: {ex}"
        return "", meta


def attach(question, block):
    """The question context with the novelty block appended, in
    the shape semantic_check's question argument carries."""
    if not block:
        return question or ""
    return ((question or "").rstrip() + "\n\n" + block).strip()
