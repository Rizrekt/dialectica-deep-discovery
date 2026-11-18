# QUALITY PER-KELAS — Amendemen (c)-PK1 Diterapkan (2026-11-17)

> Eksekusi keputusan user **2026-11-17 08:59 WIB** ("yah gw terimalah!"): lantai + pita panjang jawaban dibedakan per kelas target — Pioneer pendek-padat, Marathon panjang-terstruktur. FASE TESTING: bedah dokumen + parameterisasi kode lantai saja. Nol serve/submit/klaim. K-1/K-2 tidak disentuh (K-2 tetap 0,30 — keputusan user 06:12).

## 1. Dasar angka (dari berkas primer, dihitung ulang sesi ini)

Sumber: `belajar-2026-11-17/run11-0717/analysis11.json` (`appendix_new_paid` = 71 jawaban sel bayar-baru; fungsi kuantil studi `analyze11.py`: `sorted[int(p*n)]`) + `KORPUS-JUARA-2026-11-17.md` §4–§5.

**Pioneer sel bayar-baru (n=35)** — panjang terurut: 1.237 · 1.416 · 1.484 · **1.717 (p10)** · 1.852 · 2.047 · 2.125 · 2.713 · **2.792 (p25/q1)** · 3.932 · … · **7.410 (median)** · … · 21.567.

- **p10 = 1.717** · p25 = 2.792 · median 7.410 · **9/35 (25,7%) di bawah 3.000**.
- Lantai dipilih di **p10 = 1.717**: di bawah p25 sesuai syarat tugas, dan 32/35 (91,4%) pemenang Pioneer berada pada/di atasnya — lantai 3.000 menggugurkan 25,7% bentuk yang terbukti dibayar; lantai p10 hanya menggugurkan 3/35 ekor terpendek (1.237–1.484, di bawah ambang substansi wajar mana pun).

**Catatan ketelitian — dua median Pioneer yang berbeda, jangan dicampur:**

- **4.094 kar** = median Pioneer **kohort inti n=7** (KORPUS §4; q1 3.435 — q3 7.297). Inilah sumber fenotipe "pendek-padat" dan dasar **pita anjuran** Pioneer.
- **7.410 kar** = median Pioneer **sel bayar-baru n=35** (KORPUS §5). Sampel ini yang memasok p10/p25 untuk **lantai**.

**Marathon:** kohort inti n=167 median **10.071** (KORPUS §4); sel bayar-baru n=30 median **10.499**, q1 5.806 — q3 14.719 (KORPUS §5). Pita patokan kelas 10.000–12.000 duduk di tengah kedua distribusi itu.

**Innovator:** tidak ada distribusi — Innovator tidak terukur publik per jawaban (KORPUS §5/§8). Dinyatakan **tidak cukup data**; diperlakukan ikut kelas umum.

## 2. Patokan lama → baru (dokumen QUALITY.md, Amendemen (c)-PK1)

| Kelas | Lama (v3) | Baru ((c)-PK1) |
|---|---|---|
| Pioneer | lantai 3.000; pita umum 4.500–8.000 | **lantai 1.717**; pita anjuran pendek-padat **3.435–7.297** (q1–q3 kohort inti, median 4.094) |
| Marathon | lantai 3.000; pita 10.000–12.000 sekadar anjuran (viso ≥5) | lantai mekanis minimum **3.000 tetap**; pita **10.000–12.000 naik status = PATOKAN KELAS** |
| Innovator | lantai 3.000; pita umum | **tidak berubah** (ikut umum — data per kelas tidak ada) |
| Umum / tak dikenal | lantai 3.000; pita 4.500–8.000 anjuran | **tidak berubah** (v3 utuh) |
| P+M | tidak diatur | diperlakukan sebagai **Marathon** (tidak dilonggarkan ke lantai Pioneer) |

Yang diubah di QUALITY.md: kepala amendemen (nomor **(c)-PK1** + tanggal + sitasi keputusan 08:59), butir (c) (tabel per kelas + cara cek per kelas + contoh GAGAL khas per kelas), baris (c) lembar skor, dan satu entri CHANGELOG. **Butir lain tidak disentuh.** Backup: `QUALITY.md.bak-v3-20261117-perkelas`.

## 3. Temuan kode — lantai yang benar-benar ditegakkan (identifikasi persis)

Lantai kode ternyata **tunggal dan BUKAN 3.000**: `provider/openrouter_wrapper.py` konstanta **`LENGTH_FLOOR = 4500`** — ditegakkan di `wrap_answer` (status OK/GAGAL-LANJUT + regenerasi satu kali) dan di `score_rubric` butir (c); `serve_gate.gate_answer` mewarisinya verbatim lewat `wrap_answer`. Adopsi QUALITY v3 pada 06:12 dulu adalah **bedah dokumen murni** (tertulis di entri SISTEM-KENDALI-nya sendiri: "nol kode disentuh"), jadi lantai dokumen 3.000 tidak pernah masuk kode — gerbang operatif tetap 4.500 untuk semua kelas sampai hari ini. Inilah lantai yang menggugurkan draf-draf pendek di dry-run.

Konsekuensi desain PK1 di kode (disengaja, dinyatakan terbuka):

- **Tanpa konteks kelas → 4.500 persis seperti lama.** Semua pemanggil lama (jalur klaim, audit, pipa tanpa kelas) mempertahankan perilaku operatifnya bit-for-bit; tidak ada pelonggaran diam-diam lintas lane.
- **Kelas eksplisit dari klasifikasi pemilih/konteks serve** → Pioneer **1.717**, GENERAL/INNOVATOR **3.000** (lantai dokumen v3), MARATHON **4.500** (kode mempertahankan lantai operatifnya yang lebih ketat dari minimum dokumen 3.000 — Marathon **tidak dilonggarkan ke bawah**; pita 10.000–12.000 adalah patokan bentuk, bukan pintu).

## 4. Perubahan kode

- `provider/openrouter_wrapper.py` (backup `.bak-20261117-perkelas`):
  - Konstanta per kelas: `PIONEER_LENGTH_FLOOR = 1717`, `GENERAL_LENGTH_FLOOR = 3000`, `MARATHON_LENGTH_FLOOR = LENGTH_FLOOR`, `PIONEER_BAND = (3435, 7297)`; helper `normalize_target_class` (alias pemilih: P/M/I, P+M → MARATHON, huruf bebas), `length_floor_for_class`, `length_band_for_class`.
  - `score_rubric(..., target_class=None)` dan `wrap_answer(..., target_class=None)`: lantai + pita per kelas; instruksi regenerasi menyebut lantai kelasnya sendiri; laporan wrapper kini mencatat `target_class` + `length_floor`. Legacy `marathon=True` memetakan ke MARATHON.
  - **K-1/K-2 utuh**: `FLOOR_MIN_URLS = 1`, `FLOOR_MIN_CITATION_DENSITY = 0.5`, `FLOOR_MIN_BOUND_RATIO = 0.30` — tidak berubah satu digit pun (dijaga tes).
- `provider/vyce_serve_common.py` + `provider/cloudflare_serve_common.py` (backup `.bak-20261117-perkelas`): `vyce_pipeline(..., target_class=None)` / `serve_pipeline(..., target_class=None)` meneruskan kelas ke `serve_gate.gate_answer`. `serve_gate.py` sendiri tidak perlu diubah — `**score_kwargs`-nya sudah meneruskan parameter ke wrapper.
- Tes baru: `provider/test_length_floors_perkelas.py` (**32 cek**): tabel lantai/pita, rubrik (c) per kelas, wrapper (Pioneer 2.500 OK tanpa regen; Pioneer 1.500 regen dengan instruksi lantai kelas; umum 2.500 GAGAL / 3.200 OK; Marathon 2.500 GAGAL), gerbang serve (Pioneer 2.500 SENDABLE; tanpa kelas ditahan), pipa Vyce dua arah, dan penjaga K-1/K-2.

**Sisa yang dinyatakan terbuka (di luar lingkup tugas ini):** suffix prompt generasi di provider (`LENGTH_SUFFIX`, "tulis 5.500–7.500 karakter") masih satu ukuran untuk semua kelas — itu instruksi menulis untuk model, bukan lantai gerbang; menyelaraskannya per kelas adalah pekerjaan terpisah bila sesi utama menghendaki.

## 5. Tes akhir — suite penuh provider HIJAU

14 berkas tes, **357/357 cek lolos** (basis pra-PK1 325 + 32 baru):

| Berkas | Cek |
|---|---:|
| test_cloudflare_claim_path | 8/8 |
| test_cloudflare_serve | 33/33 |
| test_dashscope_claim_path | 11/11 |
| test_improve_20261116 | 17/17 |
| **test_length_floors_perkelas (baru)** | **32/32** |
| test_novelty_context | 35/35 |
| test_novelty_truncation_r3 | 24/24 |
| test_openrouter_claim_path | 10/10 |
| test_openrouter_wrapper | 30/30 |
| test_semantic_check | 40/40 |
| test_serve_gate | 51/51 |
| test_target_picker | 42/42 |
| test_writer_fallback | 11/11 |
| test_zai_claim_path | 13/13 |

## 6. Usulan baris MEKANISME (untuk dilipat sesi utama)

> **§140 — QUALITY PER-KELAS (c)-PK1 (2026-11-17, keputusan user 08:59; berkas QUALITY-PER-KELAS-2026-11-17.md):** QUALITY butir (c) kini per kelas target — Pioneer lantai 1.717 (p10 pemenang Pioneer sel bayar-baru n=35 run-11; 25,7% pemenang <3.000) + pita anjuran 3.435–7.297 (q1–q3 kohort inti n=7, median 4.094); Marathon pita 10.000–12.000 naik jadi patokan kelas (lantai minimum umum 3.000 tetap); Innovator ikut umum (tak terukur publik); P+M diperlakukan sebagai Marathon. Temuan kode: lantai operatif wrapper ternyata tunggal 4.500 (`LENGTH_FLOOR`, openrouter_wrapper) — lantai dokumen v3 3.000 tidak pernah masuk kode (adopsi v3 = bedah dokumen murni). Parameterisasi: `wrap_answer`/`score_rubric` menerima `target_class` (pemilih/konteks serve; pipa Vyce + Cloudflare meneruskan) — Pioneer 1.717, GENERAL/INNOVATOR 3.000, MARATHON 4.500 (tidak dilonggarkan), tanpa konteks kelas = 4.500 persis seperti lama. K-1/K-2 utuh (K-2 tetap 0,30). Suite provider 357/357 (32 cek baru test_length_floors_perkelas).
