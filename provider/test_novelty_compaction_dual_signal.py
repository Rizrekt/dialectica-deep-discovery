#!/usr/bin/env python3
"""Tests for the dual-signal compaction order
(PEMADATAN-DUA-SINYAL-2026-11-17): when the novelty block
exceeds BLOCK_CAP, the sacrifice order must protect BOTH
signals — (a) per-excerpt cap shrinks to its soft floor,
(b) weakest excerpts drop, (c) covered list trims from the
end but NEVER below COVER_FLOOR, (d) excerpt cap falls to
its hard floor. The R3 order trimmed the covered list first
and sacrificed the whole map (24 -> 0) on the live specimen.

Proves, WITHOUT network (pure build_block fixtures):
- a dense, R3-specimen-shaped block keeps the FULL covered
  map and all excerpts (stage (a) alone absorbs it);
- under a squeezed cap, excerpts drop BEFORE the covered
  list loses a single point;
- under deep pressure the covered list stops exactly at
  COVER_FLOOR and at least one excerpt survives whole;
- blocks that fit uncompacted are BYTE-IDENTICAL to the
  pre-change module (loaded from the .bak backup) — zero
  regression on the non-compaction path;
- the compaction is announced in the block + meta, as before.

Run: python3 test_novelty_compaction_dual_signal.py
(exit 0 = all pass).
"""
import importlib.util
import os
import sys
from importlib.machinery import SourceFileLoader
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import novelty_context as nc  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append(name)
        print(f"FAIL: {name} {detail}")


def iso(id_, supported=0, text=None, ts=0):
    sd = {}
    if text is not None:
        sd["answer"] = text
    return {"id": id_, "status": "verified",
            "supportedCount": supported, "refutationCount": 0,
            "isOwnAgent": False, "timestamp": ts,
            "reveal": {"data": {"structured_data": sd}}}


def dense_answer(i):
    """R3-specimen shape: several headings (covered points)
    over a long body (excerpt bulk)."""
    heads = "\n\n".join(
        f"## Angle {i}-{j} on custody and oracle design"
        for j in range(3))
    return heads + "\n\nbody " + "y" * 2000


DENSE = [iso(f"{i:08x}", supported=100 - i, text=dense_answer(i))
         for i in range(9)]


def dense_cases():
    with mock.patch.object(nc, "BLOCK_CAP", 10 ** 9):
        _fb, full_meta = nc.build_block(DENSE)
    check("prasyarat: blok padat memuat peta penuh",
          full_meta["covered_points"] == nc.MAX_COVER_POINTS,
          str(full_meta["covered_points"]))
    block, meta = nc.build_block(DENSE)
    check("blok padat terpadatkan dan muat",
          meta["compacted"] is True and len(block) <= nc.BLOCK_CAP,
          f"len={len(block)}")
    check("peta covered SELAMAT PENUH (tahap a menyerap)",
          meta["covered_points"] == nc.MAX_COVER_POINTS,
          str(meta["covered_points"]))
    check("semua kutipan selamat",
          meta["excerpted"] == nc.MAX_EXCERPTS,
          str(meta["excerpted"]))
    check("pemadatan dinyatakan di blok + meta",
          nc.COMPACTED_MARK in block and meta["compacted"] is True)


def excerpt_drop_before_covered_cases():
    # Squeeze the cap (4,500, probed on this deterministic
    # fixture) so stage (a) alone cannot fit the block:
    # excerpts must drop while the map stays untouched.
    with mock.patch.object(nc, "BLOCK_CAP", 4500):
        block2, meta2 = nc.build_block(DENSE)
    check("tekanan menengah: kutipan gugur lebih dulu",
          meta2["excerpted"] < nc.MAX_EXCERPTS,
          f"excerpted={meta2['excerpted']}")
    check("tekanan menengah: peta covered tak tersentuh",
          meta2["covered_points"] == nc.MAX_COVER_POINTS,
          str(meta2["covered_points"]))
    check("tekanan menengah: blok muat di cap sempit",
          len(block2) <= 4500, str(len(block2)))


def floor_cases():
    # Deep pressure (cap 1,600, probed on this fixture):
    # stages (b) and (c) run and the map must land exactly
    # on its floor — never below it.
    with mock.patch.object(nc, "BLOCK_CAP", 1600):
        block, meta = nc.build_block(DENSE)
    check("tekanan dalam: blok muat", len(block) <= 1600,
          str(len(block)))
    check("peta covered berhenti TEPAT di lantai",
          meta["covered_points"] == nc.COVER_FLOOR,
          str(meta["covered_points"]))
    check("minimal satu kutipan selamat",
          meta["excerpted"] >= 1, str(meta["excerpted"]))
    top_text = dense_answer(0)
    check("kutipan yang selamat utuh pada cap-nya "
          "(bukan potongan buta)",
          block.rstrip().endswith(top_text[:200])
          or block.rstrip().endswith(top_text[:500]),
          block.rstrip()[-60:])


def regression_cases():
    loader = SourceFileLoader(
        "novelty_context_pre_compact2",
        os.path.join(HERE,
                     "novelty_context.py.bak-20261117-compact2"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    old = importlib.util.module_from_spec(spec)
    loader.exec_module(old)
    small = [
        iso("aaaa0001", supported=5,
            text="## Custody split\n\nThe operator can freeze "
                 "withdrawals when the oracle stalls."),
        iso("bbbb0002", supported=3,
            text="A plain essay answer about rollup escape "
                 "hatches and their timing."),
    ]
    for label, fixture in (("kecil", small), ("kosong", []),
                           ("viso-0", [iso("cccc0003",
                                           supported=1,
                                           text=None)])):
        new_block, new_meta = nc.build_block(fixture)
        old_block, old_meta = old.build_block(fixture)
        check(f"regresi nol: blok {label} byte-identik",
              new_block == old_block and new_meta == old_meta)


if __name__ == "__main__":
    dense_cases()
    excerpt_drop_before_covered_cases()
    floor_cases()
    regression_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
