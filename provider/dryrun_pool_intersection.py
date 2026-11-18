#!/usr/bin/env python3
"""DRY-RUN IRISAN KOLAM — bukti read-only untuk perbaikan diskoneksi
kolam serve-vs-picker (PERBAIKAN-KOLAM-DOKTRIN-2026-11-18).

Menarik TIGA query peluang lewat jahitan klien yang persis sama
dengan produksi, lalu mengiriskan hasilnya lawan store doktrin
yang hidup di disk (trigger store + antrean telat):

  A. Query serve SAAT INI (argv unit): arenaIds=general,
     questionMaxAgeMs=259200000 (3 hari), q=wallet — tanpa limit,
     persis resolve_claim_plan di trued.py.
  B. Query pengamat/picker: arenaIds=general,
     questionMaxAgeMs=1800000 (30 mnt), limit=100.
  C. Query PITA SELARAS (kandidat perbaikan): arenaIds=general,
     questionMinAgeMs=7200000 (2 jam), questionMaxAgeMs=21600000
     (6 jam) — pita umur yang sama dengan jendela lepas TELAT.

Read-only total: hanya pencarian peluang (GET) + baca store lokal.
Tidak ada klaim, tidak ada prepare, tidak ada submit.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import doctrine_a as da  # noqa: E402
import target_picker  # noqa: E402


def _ids(rows):
    out = []
    for row in rows or []:
        rid = row.get("isrId") or row.get("id")
        if rid:
            out.append(str(rid))
    return out


def _query(trued, agent_id, caps, pairs, limit=None):
    query = trued.build_opportunity_query(pairs, caps, limit=limit)
    query = trued.ensure_search_bound(query, announce=False)
    rows, degraded, err = trued.search_opportunities(agent_id, query)
    if err is not None:
        raise RuntimeError(f"pencarian gagal: {err}")
    return rows


def main():
    now = time.time()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    trued = target_picker._load_trued()
    agent_id = trued.resolve_agent_id(None)
    caps = trued.opportunity_capabilities(agent_id)
    cap_ids = sorted(c.get("id") for c in caps if isinstance(c, dict))
    print(f"dryrun_pool_intersection — {stamp} (read-only)")
    print(f"filter teriklan server: {cap_ids}")
    print(f"questionMinAgeMs teriklan: "
          f"{'questionMinAgeMs' in cap_ids}")

    store = da.load_trigger_store()
    classified = set(store)
    parked = {e["isr_id"] for e in da._queue()
              if e.get("state") == "parked"}
    due = {e["isr_id"] for e in da.due_entries(now)}
    print(f"store doktrin: terklasifikasi={len(classified)} "
          f"parked={len(parked)} due-sekarang={len(due)}")

    queries = [
        ("A serve-saat-ini (q=wallet, <=3 hari)",
         [("arenaIds", "general"),
          ("questionMaxAgeMs", "259200000"),
          ("q", "wallet")], None),
        ("B pengamat/picker (<=30 mnt, limit 100)",
         [("arenaIds", "general"),
          ("questionMaxAgeMs", "1800000")], 100),
        ("C pita-selaras (2-6 jam, tanpa limit)",
         [("arenaIds", "general"),
          ("questionMinAgeMs", "7200000"),
          ("questionMaxAgeMs", "21600000")], None),
        ("C2 pita-selaras (2-6 jam, limit 100)",
         [("arenaIds", "general"),
          ("questionMinAgeMs", "7200000"),
          ("questionMaxAgeMs", "21600000")], 100),
    ]
    results = {}
    for name, pairs, limit in queries:
        t0 = time.time()
        rows = _query(trued, agent_id, caps, pairs, limit=limit)
        ids = _ids(rows)
        idset = set(ids)
        rec = {
            "rows": len(ids),
            "int_classified": len(idset & classified),
            "int_parked": len(idset & parked),
            "int_due": len(idset & due),
            "due_ids": sorted(idset & due),
            "secs": round(time.time() - t0, 1),
        }
        results[name] = rec
        print(f"[{name}] baris={rec['rows']} "
              f"iris-terklasifikasi={rec['int_classified']} "
              f"iris-parked={rec['int_parked']} "
              f"iris-DUE={rec['int_due']} ({rec['secs']} dtk)")
        for did in rec["due_ids"]:
            print(f"    DUE: {did}")
    print("RINGKASAN " + json.dumps(
        {k: {kk: vv for kk, vv in v.items() if kk != "due_ids"}
         for k, v in results.items()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
