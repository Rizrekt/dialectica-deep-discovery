#!/usr/bin/env python3
"""Tests for the C5 novelty context (novelty_context.py, built
2026-11-17 per KONTEKS-KEBARUAN-C5-2026-11-17.md).

Proves, WITHOUT any network or model call (fetchers are injected
fixtures throughout):

- Only status="verified" ISOs enter the context; the answer text
  is read from reveal.data.structured_data.answer, forecasting
  answers from .reasoning — the client's own fields.
- Sorting is most-supported first (ties: newest first); the block
  carries the covered list (headings / bold lead-ins / first
  sentence) from ALL verified answers and excerpts of only the
  top MAX_EXCERPTS, under the per-answer and total caps, with the
  leftovers honestly counted.
- viso 0 (no verified answers) and "verified but unrevealed" both
  yield an EMPTY block with truthful meta — a legitimate state,
  not an error.
- context_for_isr never raises: fetch failure / disabled / junk
  payload all come back as ("", meta) with the state named.
- The isos fetch stays off the network unless the serve gate's
  fetch arming is on (DIALECTICA_SERVE_GATE_FETCH=1).
- The sub-flag DIALECTICA_SEMANTIC_NOVELTY=0 disables the context
  alone; the armed C5 stage attaches the block when an isr_id and
  verified answers are present, and leaves the question untouched
  when the sub-flag is off or the context is empty.

Run: python3 test_novelty_context.py (exit 0 = all pass).
"""
import os
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import novelty_context as nc  # noqa: E402
import serve_gate  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append(name)
        print(f"FAIL: {name} {detail}")


def iso(id_, status="verified", supported=0, text=None, own=False,
        ts=0, reasoning=None, refuted=0):
    sd = {}
    if text is not None:
        sd["answer"] = text
    if reasoning is not None:
        sd["reasoning"] = reasoning
    return {"id": id_, "status": status, "supportedCount": supported,
            "refutationCount": refuted, "isOwnAgent": own,
            "timestamp": ts,
            "reveal": {"data": {"structured_data": sd}}}


TEXT_A = ("## Custody split\n\nThe marketplace holds **settlement "
          "keys** while users keep withdrawal rights. " + "x" * 3000)
TEXT_B = ("A plain essay answer with no headings at all. It argues "
          "the operator can freeze withdrawals at will, and gives "
          "a worked example.")
TEXT_C = "## Timing\n\nReleases follow a **timelock schedule**."


def assembly_cases():
    isos = [
        iso("aaaa0001", supported=2, text=TEXT_A, ts=100),
        iso("bbbb0002", supported=9, text=TEXT_B, ts=50),
        iso("cccc0003", supported=9, text=TEXT_C, ts=200),
        iso("dddd0004", status="revealed", supported=99,
            text="## ShouldNotAppear\n\npending text"),
        iso("eeee0005", status="falsified", supported=99,
            text="## AlsoHidden\n\ndead text"),
        iso("ffff0006", supported=1, text=None),  # verified, no text
    ]
    answers = nc.verified_answers(isos)
    check("hanya verified yang masuk",
          [a["id"] for a in answers] ==
          ["cccc0003", "bbbb0002", "aaaa0001", "ffff0006"],
          str([a["id"] for a in answers]))
    check("urut: supported desc, seri -> terbaru dulu",
          answers[0]["supported"] == 9 and answers[1]["supported"] == 9)
    block, meta = nc.build_block(isos)
    check("blok terbangun", block.startswith(nc.BLOCK_HEADER))
    check("meta total verified = 4", meta["verified_total"] == 4)
    check("meta unrevealed = 1", meta["unrevealed"] == 1)
    check("daftar covered memuat heading jawaban A",
          "Custody split" in block)
    check("daftar covered memuat kalimat pertama jawaban B",
          "plain essay answer" in block)
    check("jawaban non-verified tidak bocor ke blok",
          "ShouldNotAppear" not in block and "AlsoHidden" not in block)
    check("kutipan jawaban B (supported tertinggi) ada",
          "operator can freeze withdrawals" in block)
    check("cap per-jawaban berlaku",
          TEXT_A[:nc.ANSWER_EXCERPT_CAP] in block
          and TEXT_A[:nc.ANSWER_EXCERPT_CAP + 1] not in block)
    check("cap total blok berlaku",
          len(block) <= nc.BLOCK_CAP + 40, str(len(block)))
    check("peringatan unrevealed dinyatakan",
          "no revealed text" in block)


def empty_cases():
    block, meta = nc.build_block([])
    check("viso 0: blok kosong sah", block == ""
          and meta["verified_total"] == 0 and meta["excerpted"] == 0)
    block, meta = nc.build_block(
        [iso("aaaa0001", supported=3, text=None)])
    check("verified tanpa teks: blok kosong, meta jujur",
          block == "" and meta["verified_total"] == 1
          and meta["unrevealed"] == 1)
    block, meta = nc.build_block(None)
    check("isos None: blok kosong", block == ""
          and meta["verified_total"] == 0)
    check("attach tanpa blok = pertanyaan utuh",
          nc.attach("q?", "") == "q?")
    check("attach dengan blok menempel rapi",
          nc.attach("q?", "BLOK") == "q?\n\nBLOK")


def cap_cases():
    many = [iso(f"{i:08x}", supported=100 - i,
                text=f"## Head {i}\n\nbody {i} " + "y" * 2000)
            for i in range(9)]
    block, meta = nc.build_block(many)
    # Kontrak R3 (MITIGASI-KONTEKS-TERPOTONG): blok raksasa
    # DIPADATKAN bertahap, bukan dipotong buta — jumlah kutipan
    # boleh turun di bawah MAX_EXCERPTS, blok berakhir pada
    # kutipan yang utuh, dan pemadatan dinyatakan di blok + meta.
    check("kutipan dibatasi MAX_EXCERPTS",
          meta["excerpted"] <= nc.MAX_EXCERPTS)
    check("sisa yang tak dikutip dihitung di blok",
          f"+{9 - meta['excerpted']} further verified" in block)
    check("poin covered dibatasi",
          meta["covered_points"] <= nc.MAX_COVER_POINTS)
    check("blok raksasa dipadatkan, bukan dipotong buta",
          meta.get("compacted") is True
          and nc.COMPACTED_MARK in block
          and "novelty context truncated" not in block)
    check("blok raksasa tetap di bawah cap",
          len(block) <= nc.BLOCK_CAP, str(len(block)))
    check("ekor blok = kutipan utuh (tak terpotong di tengah)",
          block.rstrip().endswith("yyyy"))


def fetch_cases():
    def junk(isr_id):
        return None, "failed"

    def boom(isr_id):
        raise RuntimeError("network down")

    def good(isr_id):
        return [iso("aaaa0001", supported=1, text=TEXT_C)], "ok"

    block, meta = nc.context_for_isr("isr-x", isos_fetcher=junk)
    check("fetch gagal -> failed, blok kosong",
          block == "" and meta["state"] == "failed")
    block, meta = nc.context_for_isr("isr-x", isos_fetcher=boom)
    check("fetch meledak -> failed, tidak raise",
          block == "" and meta["state"] == "failed")
    block, meta = nc.context_for_isr("isr-x", isos_fetcher=good)
    check("fetch ok -> blok terbangun",
          meta["state"] == "ok" and "Timing" in block)
    with mock.patch.dict(os.environ, {nc.FETCH_ENV: "1"}):
        isos, state = nc.fetch_isos(
            "isr-x", caller=lambda i: {"unexpected": True})
    check("payload tanpa field isos -> failed",
          isos is None and state == "failed")
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop(nc.FETCH_ENV, None)
        isos, state = nc.fetch_isos("isr-x")
    check("fetch tak ter-arm: disabled, nol jaringan",
          isos is None and state == "disabled")
    with mock.patch.dict(os.environ, {nc.FETCH_ENV: "1"}):
        isos, state = nc.fetch_isos(
            "isr-x", caller=lambda i: {"isos": []})
    check("fetch ter-arm via caller injeksi: ok",
          isos == [] and state == "ok")


def arming_cases():
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop(nc.NOVELTY_ENV, None)
        check("sub-flag bawaan: ikut induk (nyala)",
              nc.novelty_enabled())
    with mock.patch.dict(os.environ, {nc.NOVELTY_ENV: "0"}):
        check("sub-flag 0: konteks mati sendiri",
              not nc.novelty_enabled())
    with mock.patch.dict(os.environ, {nc.NOVELTY_ENV: "1"}):
        check("sub-flag 1: nyala", nc.novelty_enabled())

    fake = mock.Mock()
    fake.novelty_enabled.side_effect = lambda: nc.novelty_enabled()
    fake.context_for_isr.return_value = (
        "BLOK-KEBARUAN", {"verified_total": 3, "excerpted": 2,
                          "covered_points": 4, "block_chars": 13,
                          "state": "ok"})
    fake.attach.side_effect = lambda q, b: (q or "") + "\n\n" + b
    with mock.patch.dict(sys.modules, {"novelty_context": fake}):
        with mock.patch.dict(
                os.environ, {serve_gate.SEMANTIC_ARM_ENV: "1"}):
            os.environ.pop(nc.NOVELTY_ENV, None)
            captured = {}

            def recorder(text, question="", isr_id=None, **kw):
                captured["question"] = question
                return {"performed": True, "findings": [],
                        "block": False}

            with mock.patch.object(serve_gate, "semantic_check",
                                   recorder):
                stage = serve_gate.armed_semantic_check(
                    question="PERTANYAAN", isr_id="isr-123")
                check("stage ter-arm dengan konteks: callable",
                      callable(stage))
                stage("draf")
                check("konteks kebaruan menempel ke pertanyaan "
                      "pemeriksa",
                      captured.get("question") ==
                      "PERTANYAAN\n\nBLOK-KEBARUAN",
                      repr(captured.get("question")))
        with mock.patch.dict(
                os.environ, {serve_gate.SEMANTIC_ARM_ENV: "1",
                             nc.NOVELTY_ENV: "0"}):
            captured = {}

            def recorder2(text, question="", isr_id=None, **kw):
                captured["question"] = question
                return {"performed": True, "findings": [],
                        "block": False}

            with mock.patch.object(serve_gate, "semantic_check",
                                   recorder2):
                stage = serve_gate.armed_semantic_check(
                    question="PERTANYAAN", isr_id="isr-123")
                stage("draf")
                check("sub-flag 0: pertanyaan pemeriksa utuh",
                      captured.get("question") == "PERTANYAAN",
                      repr(captured.get("question")))


if __name__ == "__main__":
    assembly_cases()
    empty_cases()
    cap_cases()
    fetch_cases()
    arming_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
