# PROOF RUN 5 PILAR Dialectica — 2026-11-17 02:12–02:14 WIB (BACA-SAJA TOTAL)

> Tujuan: membuktikan protokol cek 5 pilar (disahkan user 2026-11-17 02:08; AUDIT-5-PILAR §3 + ADDENDUM SISTEM-KENDALI 2026-11-17) benar-benar jalan dan menangkap keadaan nyata.
> Sifat run: **nol klaim, nol serve, nol ubah config/cron** — hanya GET lewat klien resmi `trued.py` + `liveness_check` asli dari `provider/serve_gate.py`.
> Jangkar pembanding: keadaan tercatat tutup 16 Nov 23:00 WIB (MEKANISME §127).
> Waktu jalan: baca murni ±44 detik (2 pass: 15,3 + 28,6 dtk); ujung-ke-ujung 02:12:49–02:14:24 WIB (±1 mnt 35 dtk, termasuk koreksi pass-2 di §6).

## 1. PILAR 4 — KEADAAN AKUN (baca live 2026-11-16T19:13:21–19:13:27Z = 02:13 WIB)

| Butir | Tercatat 16 Nov 23:00 | LIVE malam ini | Selisih |
|---|---|---|---|
| Saldo $TRUED | −1,8788 | **−1,8788** | 0 |
| LifetimeEarned | 0 | **0** | 0 |
| Expertise (general) | 0 | **0** | 0 |
| RAR total | 118 | **118** | 0 |
| — Reliability | −5 | **−5** | 0 |
| — Availability | 29 | **29** | 0 |
| — Reputation | 94 | **94** | 0 |
| suspensionCount | 5 | **5** | 0 |
| Caps (limits API) | unlimited | **semua null, isActive=true, warning 80%** | cocok |
| Usage jendela bergulir | 0 | **0 ISR / 0 token / $0** (window 15 Nov 19:13:24Z → 16 Nov 19:13:24Z, costComplete=true) | 0 |
| strategyType | dynamic | **dynamic** (nodeConfig; maxConcurrency 1; arenas [general]; enabled) | cocok |
| Jobs | 34 (29 completed / 5 failed) | **34 (29 / 5)**; totalJobsCompleted 29, totalJobsFailed 5 di profil agen | 0 |
| connectionStatus | offline di luar serve | **offline** | wajar (tak ada serve di luar jendela) |

**Tangkapan utama Pilar 4: TIDAK ADA verdict baru yang mendarat sejak tutup 16 Nov.** Dari **22 jawaban serve yang masih revealed**: seandainya satu saja falsified, saldo/LE/Expertise wajib turun −1 per buah; seandainya ada yang verified-menang, LE wajib naik. Semua angka identik sampai 4 desimal → **22 revealed itu masih revealed semua** (paparan −22 potensial BELUM tertutup, tapi juga belum memburuk). Inilah persis tangkapan yang dirancang Pilar 4: verdict falsified itu senyap — tanpa baca scores, keadaan ini tidak terlihat dari mana pun.
Kill-metric: (a) 0/10 tetap; (b) JEDA + STOP TOTAL klaim tetap mengikat (rezim internal, konsisten dengan usage 0 + jobs 0 baru); (c) RAR total 118 aman, REL tetap tepat −5; (d) jalur ask tetap tertutup.

## 2. PILAR 5 — WAKTU & LIVENESS (baca live 19:13:56–19:14:24Z)

**Verdict di 4 permukaan (semua dibaca malam ini):**
1. Status ISO kita — klaim #1 `fcb7b015` di ISR 60fa9935…: **falsified, support 2 / refute 2, panel 4** (persis catatan lama; tidak berubah). Di ISR 64bd68ac… kita tidak punya ISO (ISR korpus studi, bukan klaim kita).
2. `/api/node/scores` — identik jangkar (§1): tidak ada gerakan verdict.
3. Endpoint jobs — 34, 0 baru, 0 in-flight.
4. Endpoint usage — 0/0/0.
Permukaan pendamping — notifikasi: 50 terakhir = **48× subscribed_isr_marathon + 2× user_suspended (lama)**, 40 belum terbaca, **0 notifikasi verdict** — membuktikan lagi falsified/verified tidak pernah datang sebagai alarm; hanya 4 permukaan di atas yang melihatnya.

**Scan lapangan:** `opportunities --limit 100` → **100 baris dari total 201** (19:13:30Z). Komposisi questionStatus: **96 settled, 3 marathon, 1 in_progress**; questionMarathonActive **59 true / 41 false**; viso: 0→1 baris, 1→28, 2→37, 3→12, 4→8, 5→8, 6→5, 7→1.
Kandidat serius (settled/marathon viso 0 atau 2–9, in_progress viso-0): **72 baris** — listing-nya saja terlihat subur. Di sinilah filter bekerja:

**Filter liveness 3-field atas detail ISR — 10 kandidat teratas diperiksa, dibaca 19:14:14–19:14:24Z: 5 LIVE, 5 MATI.**

LIVE:
- `9b16a5bb` — in_progress, viso 0, tanpa dimensi maraton → LIVE (terbuka). Satu-satunya viso-0 malam ini; topik off-core (kompetisi skor).
- `05a4e7f5` — status marathon, viso listing 3, endsAt maks **19:16:50Z** → LIVE.
- `103408f7` — status marathon, viso listing 6, endsAt maks **19:19:17Z** → LIVE.
- `5936174b` — status marathon, viso listing 5, endsAt maks **19:15:24Z** → LIVE (sisa ±65 detik saat dibaca — contoh nilai membusuk dalam menit).
- `c8aeca05` — settled, marathonConcluded=**true** TAPI ada endsAt ronde baru **19:20:23Z** → **LIVE** (kasus "ronde baru di atas pertanyaan concluded" — flag listing akan membuangnya, filter detail menyelamatkannya).

MATI (semua pola flag basi — marathonActive=true di listing, semua endsAt sudah lewat):
- `6327070e` (maks 19:10:46Z), `9255cb44` (19:10:45Z), `49752147` (19:04:25Z), `519ad929` (19:07:55Z), `f3a9d1d5` (18:57:09Z) → upside $0, persis celah serve 14 Nov.

**Temuan waktu:** run ini berjalan **02:12–02:14 WIB — DI LUAR jendela hunt (07:00–21:00)** — dan lapangan tetap hidup (ronde maraton berakhir 19:15–19:20Z). Pilar 5 menangkap bahwa arena tidak tidur mengikuti jadwal kita; yang menahan serve di jam ini adalah rezim jendela kita sendiri, bukan ketiadaan target.

## 3. PILAR 1–2 — KONFIRMASI REZIM (tanpa perubahan apa pun)

- Strategi live **dynamic** + caps **unlimited** + arena **general** — cocok dokumen terbaru (dan membuktikan sekali lagi teks basi K1/K2 di operator prompt: yang hidup di server adalah dynamic/unlimited).
- STOP TOTAL klaim + JEDA (kill-metric ii) — status rezim internal, tidak terbaca dari server; bacaan live **konsisten** dengannya (0 usage, 0 job baru, 0 klaim sejak jangkar). Tidak ada bukti live yang membukanya.
- Gerbang turunan Pilar 2 yang terpakai malam ini = liveness fail-closed (jalan, §2). Ambang K-2 tetap **0,30** (belum ada keputusan final 0,15). C5 tidak teruji malam ini (tidak ada serve/generasi — memang bukan wilayah proof baca-saja).

## 4. PILAR 3 — LATIHAN PENILAIAN LAWAN BIDIK BOOSTER (bukan rekomendasi tembak)

Dari 5 kandidat LIVE: **4/5 adalah ronde Marathon** → selaras bidik **Marathon-first**. Viso listing-nya: 3, 6, 5, 2 (median 4) — di dalam pita bidik kohort (masuk ramai, median viso ±3, pita klaim 2–9); yang viso-0 (`9b16a5bb`) adalah jalur Pioneer = jalur kedua menurut booster, dan topiknya off-core. Latihan selesai: angka bidik bisa diterapkan ke kandidat live dalam hitungan detik. **Klaim tetap terkunci STOP TOTAL — tidak ada rekomendasi tembak dari run ini.**

## 5. VONIS PROOF — PER PILAR

| Pilar | Vonis | Alasan satu baris |
|---|---|---|
| 1 Tugas | **LULUS** | Konfirmasi rezim dari bacaan live cocok; teks basi dokumen justru tertangkap kontrasnya. |
| 2 Penilaian | **LULUS (sebagian wilayah)** | Permukaan verdict + gerbang liveness terbukti bekerja; wilayah isi (K-2/C5) memang di luar jangkauan proof baca-saja. |
| 3 Booster | **LULUS** | Angka bidik (Marathon-first, viso) terapan langsung ke kandidat live malam ini. |
| 4 Keadaan Akun | **LULUS — tangkapan nyata** | Membuktikan 22 revealed belum ber-verdict satu pun (semua angka identik) — fakta yang tak terlihat dari notifikasi mana pun. |
| 5 Waktu & Liveness | **LULUS — tangkapan nyata** | 5/10 kandidat "subur" di listing ternyata MATI; 1 kandidat concluded justru LIVE oleh ronde baru; 1 LIVE tersisa 65 detik. Tanpa cek ini, separuh daftar target adalah peta mati. |

**Vonis keseluruhan: PROTOKOL JALAN.** Kelima cek bisa dieksekusi dari bacaan live dalam ±44 detik baca murni, dan dua pilar barunya (4 & 5) masing-masing menangkap sesuatu yang pasti terlewat tanpa mereka.

## 6. CATATAN KEJUJURAN PROOF (kelemahan yang ditemukan run ini sendiri)

1. **Pass-1 filter kandidat sempat salah bidang**: baris opportunities membawa `status` (open/verified) yang BUKAN status pertanyaan — bidang yang benar `questionStatus` + `questionVisoCount`. Hasil pass-1 (0 kandidat) terlihat mustahil lawan bukti bidang lain, dikoreksi di pass-2. Pelajaran tertulis: skrip scan masa depan WAJIB membaca field `question*`; kegagalan ini tertangkap justru karena protokol menuntut angka lintas permukaan.
2. **Detail ISR tidak membawa questionVisoCount** (null di payload detail) — viso hanya sah dari baris listing; endsAt hanya sah dari detail. Dua sumber itu memang harus dibaca berpasangan, sesuai desain filter.
3. ID pendek 8-karakter ditolak endpoint ISO ("Invalid UUID format") — permukaan ISO wajib UUID penuh.
4. Proof berjalan di luar jendela hunt — disengaja untuk uji protokol, dan Pilar 5 mencatatnya sebagai temuan (§2), bukan pelanggaran: tidak ada serve/klaim yang dinyalakan.

Sumber mentah run: skrip baca `/tmp/proof5.py` + `/tmp/proof5b.py`, keluaran `/tmp/proof5-out.json` + `/tmp/proof5b-out.json` (sementara, di /tmp).
