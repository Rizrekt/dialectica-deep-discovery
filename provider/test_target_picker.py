#!/usr/bin/env python3
"""Tests for the pay-cell target picker (target_picker.py, built
2026-11-17, PEMILIH-TARGET-2026-11-17.md). Pure classification only
— no network, no serve, no claim:

- viso 0 live -> PIONEER (+20 x age feasibility x priority weight);
- marathon round provably open + viso in the A1 band -> MARATHON;
- viso mid without a marathon -> INNOVATOR (novelty room estimate);
- viso high without a marathon -> NO-PAY (room below the floor);
- stale-flag detail (concluded, every endsAt past) -> NO-PAY dead;
- marathon detail with no provable future round -> NO-PAY dead
  (fail-closed, inherited from serve_gate.liveness_check);
- off-core-topic demotes under the pilot rule (default) and passes
  with require_core_topic=False;
- the class-priority profile is a parameter: pioneer profile swaps
  the PIONEER/MARATHON weights;
- feasibility pieces: Pioneer age bands, Marathon viso band +
  timing factors, novelty room clamp.
"""
import sys

import target_picker as tp

CHECKS = [0]
FAILURES = []

NOW = 1_800_000_000  # fixed epoch — fixtures are relative to this


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append(name)
        print(f"FAIL: {name} {detail}")


def iso(epoch):
    import datetime
    return datetime.datetime.fromtimestamp(
        epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def row(isr="aaaa0001", viso=0, age_ms=60_000, text="wallet security",
        **kw):
    base = {"id": isr, "title": text, "content": text,
            "questionVisoCount": viso, "questionAgeMs": age_ms,
            "status": "in_progress"}
    base.update(kw)
    return base


def open_detail():
    return {"status": "in_progress", "marathonActive": False,
            "marathonConcluded": False, "marathonEligibleIsos": []}


def marathon_detail(ends_in_s=3600, viso_note=None):
    return {"status": "in_progress", "marathonActive": True,
            "marathonConcluded": False,
            "marathonEligibleIsos": [{"endsAt": iso(NOW + ends_in_s)}]}


def stale_detail():
    return {"status": "in_progress", "marathonActive": True,
            "marathonConcluded": True,
            "marathonEligibleIsos": [{"endsAt": iso(NOW - 3600)}]}


def classify_cases():
    rec = tp.classify(row(), detail=open_detail(), now=NOW)
    check("viso 0 live -> PIONEER", rec["cls"] == "PIONEER",
          rec["reason"])
    check("PIONEER score = 20 x 0.60 (age 60 s) x 0.9 (marathon "
          "profile)", abs(rec["score"] - 20 * 0.60 * 0.9) < 1e-9,
          str(rec["score"]))

    rec = tp.classify(row(viso=6), detail=marathon_detail(), now=NOW)
    check("viso 6 + ronde terbuka -> MARATHON",
          rec["cls"] == "MARATHON", rec["reason"])
    check("MARATHON feasibility band 2-9, timing normal = 0.50",
          abs(rec["feasibility"] - 0.50) < 1e-9,
          str(rec["feasibility"]))

    rec = tp.classify(row(viso=5), detail=open_detail(), now=NOW)
    check("viso 5 tanpa maraton -> INNOVATOR",
          rec["cls"] == "INNOVATOR", rec["reason"])
    check("INNOVATOR feasibility = 0.6 x room(5)=0.55",
          abs(rec["feasibility"] - 0.6 * 0.55) < 1e-9,
          str(rec["feasibility"]))

    rec = tp.classify(row(viso=14), detail=open_detail(), now=NOW)
    check("viso 14 tanpa maraton -> NO-PAY (ruang di bawah lantai)",
          rec["cls"] == "NO-PAY" and rec["score"] == 0.0,
          rec["reason"])

    rec = tp.classify(row(viso=3), detail=stale_detail(), now=NOW)
    check("detail basi (concluded, endsAt lewat) -> NO-PAY mati",
          rec["cls"] == "NO-PAY" and not rec["live"], rec["reason"])

    rec = tp.classify(row(viso=3), detail={
        "status": "in_progress", "marathonActive": True,
        "marathonConcluded": False, "marathonEligibleIsos": []},
        now=NOW)
    check("maraton tanpa endsAt terbukti -> NO-PAY (fail-closed)",
          rec["cls"] == "NO-PAY" and not rec["live"], rec["reason"])

    rec = tp.classify(row(viso=0), detail=None, now=NOW)
    check("detail None + baris terbuka -> PIONEER (baris membuktikan "
          "hidup)", rec["cls"] == "PIONEER", rec["reason"])

    rec = tp.classify(row(viso=2, questionMarathonConcluded=True),
                      detail=None, now=NOW)
    check("detail None + baris maraton mati -> NO-PAY",
          rec["cls"] == "NO-PAY", rec["reason"])

    rec = tp.classify(row(text="best pasta sauce recipe"),
                      detail=open_detail(), now=NOW)
    check("viso 0 di luar topik inti -> gugur (aturan pilot)",
          rec["cls"] == "NO-PAY" and "topik inti" in rec["reason"],
          rec["reason"])
    rec = tp.classify(row(text="best pasta sauce recipe"),
                      detail=open_detail(), now=NOW,
                      require_core_topic=False)
    check("require_core_topic=False -> PIONEER lolos",
          rec["cls"] == "PIONEER", rec["reason"])

    rec = tp.classify(row(), detail=open_detail(), now=NOW,
                      priority="pioneer")
    check("profil pioneer: bobot PIONEER 1.0",
          abs(rec["score"] - 20 * 0.60 * 1.0) < 1e-9,
          str(rec["score"]))

    rec = tp.classify(row(viso=None), detail=open_detail(), now=NOW)
    check("viso tak terbaca -> NO-PAY jujur",
          rec["cls"] == "NO-PAY" and "tidak terbaca" in rec["reason"],
          rec["reason"])


def feasibility_cases():
    check("room(0)=0.95", abs(tp.novelty_room(0) - 0.95) < 1e-9)
    check("room(20) terjepit 0.05",
          abs(tp.novelty_room(20) - 0.05) < 1e-9)
    check("PIONEER umur 3 jam -> 0.08",
          tp.feasibility("PIONEER", 0, 3 * 3600, None) == 0.08)
    check("PIONEER umur tak diketahui -> 0.20",
          tp.feasibility("PIONEER", 0, None, None) == 0.20)
    check("MARATHON viso 12 -> pita 0.35",
          abs(tp.feasibility("MARATHON", 12, None, 3600) - 0.35)
          < 1e-9)
    check("MARATHON berakhir <900 dtk -> faktor 0.6",
          abs(tp.feasibility("MARATHON", 5, None, 600) - 0.50 * 0.6)
          < 1e-9)
    check("MARATHON berakhir >48 jam -> faktor 0.8",
          abs(tp.feasibility("MARATHON", 5, None, 200_000)
              - 0.50 * 0.8) < 1e-9)
    check("MARATHON endsAt tak diketahui -> faktor 0.7",
          abs(tp.feasibility("MARATHON", 5, None, None) - 0.50 * 0.7)
          < 1e-9)
    ranked = tp.rank([{"isr_id": "b", "score": 1.0},
                      {"isr_id": "a", "score": 2.0}])
    check("rank: skor tertinggi dulu", ranked[0]["isr_id"] == "a")


def _pre(rows, **kw):
    kw.setdefault("now", NOW)
    return [tp.classify(r, **kw) for r in rows]


def _bands(order):
    return [band for _isr, band, _viso in order]


def hunt_cases():
    # --- jatah: rumus eksplisit per profil
    j = tp.detail_jatah(30, "marathon")
    check("jatah marathon cap30 = M15/I8/P7/S0",
          j == {"MARATHON": 15, "INNOVATOR": 8, "PIONEER": 7,
                "SISA": 0}, str(j))
    j = tp.detail_jatah(30, "pioneer")
    check("jatah pioneer cap30 = P15/M8/I7/S0",
          j == {"PIONEER": 15, "MARATHON": 8, "INNOVATOR": 7,
                "SISA": 0}, str(j))
    j = tp.detail_jatah(6, "marathon")
    check("jatah marathon cap6 = M3/I2/P1",
          (j["MARATHON"], j["INNOVATOR"], j["PIONEER"]) == (3, 2, 1),
          str(j))

    # --- pita per kandidat
    def band_of(r, **kw):
        pre = tp.classify(r, now=NOW)
        return tp.hunt_band(r, pre, **kw)

    check("viso 0 -> pita PIONEER", band_of(row()) == "PIONEER")
    check("viso 5 + flag maraton -> pita MARATHON",
          band_of(row(viso=5, questionMarathonActive=True))
          == "MARATHON")
    check("viso 12 + flag maraton -> pita MARATHON (kelas maraton "
          "tak berplafon viso)",
          band_of(row(viso=12, questionMarathonActive=True))
          == "MARATHON")
    check("viso 5 tanpa dimensi maraton -> pita INNOVATOR",
          band_of(row(viso=5)) == "INNOVATOR")
    check("viso 12 tanpa dimensi -> pita SISA",
          band_of(row(viso=12)) == "SISA")
    check("viso tak terbaca -> tanpa detail",
          band_of(row(viso=None)) is None)
    check("luar topik inti (wajib) -> tanpa detail",
          band_of(row(text="best pasta sauce recipe")) is None)
    check("luar topik inti (parameter mati) -> pita PIONEER",
          band_of(row(text="best pasta sauce recipe"),
                  require_core_topic=False) == "PIONEER")
    check("settled tanpa dimensi maraton -> tanpa detail",
          band_of(row(viso=3, status="settled")) is None)

    # --- urutan: profil marathon membaca pita maraton lebih dulu,
    # jatah dipatuhi, sisa anggaran mengalir searah profil
    m_rows = [row(isr="m0000001", viso=5, questionMarathonActive=True),
              row(isr="m0000002", viso=3, questionMarathonActive=True)]
    i_rows = [row(isr="i0000001", viso=5), row(isr="i0000002", viso=2)]
    p_rows = [row(isr=f"p000000{k}", viso=0) for k in range(1, 5)]
    rows = p_rows + i_rows + m_rows  # sengaja diacak urutan masuknya
    order = tp.hunt_order(rows, _pre(rows), priority="marathon",
                          detail_cap=6, now=NOW)
    check("marathon cap6: urutan pita M,M,I,I,P,P (jatah + sisa)",
          _bands(order) == ["MARATHON", "MARATHON", "INNOVATOR",
                            "INNOVATOR", "PIONEER", "PIONEER"],
          str(_bands(order)))
    check("marathon cap6: dua detail pertama = kandidat maraton",
          [o[0] for o in order[:2]] == ["m0000001", "m0000002"],
          str(order))
    check("cap dihormati + tanpa duplikat",
          len(order) == 6 and len({o[0] for o in order}) == 6)

    # --- urutan: profil pioneer mempertahankan viso-0 lebih dulu
    order = tp.hunt_order(rows, _pre(rows), priority="pioneer",
                          detail_cap=6, now=NOW)
    check("pioneer cap6: urutan pita P,P,P,M,M,I",
          _bands(order) == ["PIONEER", "PIONEER", "PIONEER",
                            "MARATHON", "MARATHON", "INNOVATOR"],
          str(_bands(order)))

    # --- di dalam pita MARATHON: kelompok viso utama dulu; di
    # dalamnya yang terbukti terbuka > belum terbukti > basi
    def mrow(isr, viso, **kw):
        return row(isr=isr, viso=viso, questionMarathonActive=True,
                   **kw)
    mm = [mrow("mm0000st", 5,
               marathonEligibleIsos=[{"endsAt": iso(NOW - 3600)}]),
          mrow("mm0000ad", 12),
          mrow("mm0000un", 5),
          mrow("mm0000op", 4,
               marathonEligibleIsos=[{"endsAt": iso(NOW + 3600)}])]
    order = tp.hunt_order(mm, _pre(mm), priority="marathon",
                          detail_cap=10, now=NOW)
    check("pita MARATHON: terbuka > belum-terbukti > basi > "
          "kelompok viso sebelah",
          [o[0] for o in order] == ["mm0000op", "mm0000un",
                                    "mm0000st", "mm0000ad"],
          str(order))

    # --- SISA hanya dari sisa anggaran
    s_rows = [row(isr="s0000001", viso=12)]
    order = tp.hunt_order(s_rows + p_rows, _pre(s_rows + p_rows),
                          priority="marathon", detail_cap=10, now=NOW)
    check("SISA terbaca sesudah pita berbobot habis",
          _bands(order)[-1] == "SISA" and len(order) == 5,
          str(_bands(order)))


if __name__ == "__main__":
    classify_cases()
    feasibility_cases()
    hunt_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
