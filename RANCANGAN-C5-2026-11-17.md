# Rancangan C5 — Self-VFP Semantik Jalur Serve (2026-11-17)

> Perintah user 2026-11-17 02:47–02:48: susun + kerjakan. Dasar rancangan = anatomi 7 falsified kita sendiri (VERDICT-LEDGER.md baris #1–#3 klaim, #5–#8 serve), BUKAN teori umum.
> Titik pasang: `semantic_check` di `provider/serve_gate.py` (disiapkan 2026-11-15, implementasi kosong — SISTEM-KENDALI C5/CELAH 1).

## 1. Racun yang TERBUKTI membunuh kita (dari ledger)

| Kode | Racun | Bukti falsified |
|---|---|---|
| S-1 | **Angka tak terikat sumber bernama** | #2 (angka BSC liar), #5 (557 angka), #6, #7 (657), #8 (296) — **6 dari 7 falsified** |
| S-2 | **Sitasi tidak mendukung klaimnya** (A_CITATION) | #1 — klaim dominasi bernama-rantai diikat sitasi yang tak mendukung |
| S-3 | **Fakta spesifik salah** | #2 — base fee "EIP-1559", blok "~3 dtk/21 validator", "~21.000 gas" untuk BSC; lolos wrapper 3× karena tak ada yang membaca isi lawan pengetahuan |
| S-4 | **Klaim dunia diatribusikan ke "Answer N"** (E1-p) | #7 (22× kutipan), #8 (43×) — jawaban orang lain diperlakukan sebagai bukti fakta |
| — | (Bukan wilayah C5 — sudah digerbang bentuk) | jejak pikiran mentah, E3 penutup evasif, 0 URL — wilayah gerbang bentuk + pipa v2 |

Pelajaran penentu dari #2: racun masuk saat GENERASI dan **lolos pemeriksaan 3×** karena pemeriksanya satu keluarga dengan penulisnya (wrapper sendiri). Pemeriksa C5 karena itu WAJIB beda model dari penulis.

## 2. Bentuk yang dibangun

- **Pemeriksa silang (cross-model):** penulis GLM → pemeriksa **Nemotron via OpenRouter** (beda model DAN beda provider; kuota free 50/hari vs pilot maks 10 generasi/hari = muat). Cadangan pemeriksa: **deepseek-v4.1 via Vyce** (beda model) bila lane OpenRouter mati — sejalan keputusan user 02:42 (model saling backup, termasuk pemeriksa).
- **Yang diburu pemeriksa** (persis daftar §1): ekstrak semua angka → terikat sumber bernama atau tidak (S-1); ekstrak klaim bersitasi → sitasi mendukung atau tidak (S-2); fakta spesifik bernama (parameter chain/protokol/angka resmi) → konsisten atau mencurigakan (S-3); atribusi fakta ke Answer N (S-4); klaim kebaruan ("pertama/belum ada yang…") → nabrak jawaban lama yang terlihat di prompt atau tidak.
- **Keluaran:** JSON terstruktur — daftar temuan per kode + kutipan bukti dari draf + vonis `fatal` (ada S-1/S-2/S-3/S-4 berkuotasi) atau `bersih`.
- **Fase jalan:** (1) **SHADOW** — pemeriksa jalan, temuan dicatat ke `provider/semantic-check-log.jsonl`, jawaban TETAP dikirim; (2) **BLOCKING** — temuan fatal = jawaban ditahan (job dilepas/dibatalkan, kill-metric pilot tidak berubah) — HANYA sesudah kalibrasi §3 lolos dan dinyatakan tertulis.

## 3. Kalibrasi (gerbang sebelum BLOCKING sah)

- Korpus racun: teks 7 falsified historis (diambil dari berkas drill/BEDAH/API per ISO) — pemeriksa WAJIB menandai fatal pada racun semantiknya: #1 (S-2), #2 (S-1+S-3), #3 (minimal satu temuan semantik), #5–#8 (S-1 massal + S-4 pada #7/#8).
- Korpus bersih: ≥5 jawaban VERIFIED lapangan (dari ISR yang dipelajari) — pemeriksa TIDAK BOLEH menandai fatal satu pun.
- Lolos dua-duanya → laporan kalibrasi tertulis → BLOCKING boleh diaktifkan (env `DIALECTICA_SEMANTIC_MODE=block`); gagal satu sisi → tetap SHADOW + bedah prompt pemeriksa, ulangi.
- Suite lama WAJIB tetap hijau (170/170) + tes baru untuk semantic_check (mode shadow tidak pernah memblokir; mode block menahan pada fixture fatal; lane pemeriksa mati = shadow-lean: catat + jangan blokir buta — pemeriksa mati tidak boleh membunuh jawaban bagus, dan tidak boleh meloloskan diam-diam: temuan "pemeriksa tak tersedia" dicatat keras di log hunt).

## 4. Yang TIDAK diubah rancangan ini

Cap pilot 10/hari, kill-metric, gerbang bentuk, rezim klaim STOP TOTAL, config Expert — semua tetap. C5 hanya menambah satu tahap baca-isi di jalur serve, di titik pasang yang sudah ada.

## 5. KOREKSI BASIS SPEK (user 2026-11-17 02:53: "bentuk c5 itu gak bisa dibangun dari apa yang diminta project?")

User BENAR — basis spek utama C5 adalah **yang diminta proyek sendiri** (Pilar 2 — Data Penilaian), bukan bekas luka kita. Dokumen resmi proyek (references/rules-of-the-game.md + arenas.md + SKILL.md paket resmi):

- Jawaban WAJIB: **(i) menjawab langsung Pertanyaannya, (ii) menyitir sumber, (iii) memaparkan penalaran untuk diteliti, (iv) dapat diverifikasi** — Verifier memeriksa jawaban lawan aturan verifikasi Arena dan falsifikasi bersifat publik + beralasan.
- **NIU** (Novelty, Inventiveness, Utility) + **Surprise Gauge**: jawaban sesudah yang pertama hanya bernilai bila menambah informasi yang BENAR-BENAR baru di atas yang sudah verified; jawaban parafrase menghentikan verifikasi di Surprise Gauge.
- Peran Verifier = adversarial: mencoba MEMFALSIFIKASI jawaban.

Struktur pemeriksa C5 dikoreksi jadi DUA LAPIS:
- **LAPIS 1 — Kriteria proyek (spek utama):** pemeriksa memainkan peran Verifier platform persis: apakah jawaban menjawab langsung pertanyaannya; apakah klaimnya dapat diverifikasi dari sumber yang disitir; apakah penalarannya terpapar & nyambung; apakah isinya baru lawan jawaban verified yang ada (NIU/Surprise) atau cuma parafrase.
- **LAPIS 2 — Penekanan racun historis (§1 S-1..S-4):** pola yang TERBUKTI membunuh kita diberi bobot buruan ekstra di dalam Lapis 1 (angka tak terikat = gagal "dapat diverifikasi"; sitasi tak mendukung = gagal "menyitir sumber"; atribusi Answer N = bukan sumber; fakta spesifik salah = target falsifikasi utama Verifier).
- Riwayat falsified tetap menjadi **korpus kalibrasi** (§3), bukan spek.

## 6. LAPIS 1 DIGANTI DATA LIVE SERVER (perintah user 2026-11-17 02:55: "cek data live yang diminta detail dan teliti!")

Tarik live `trued arena general` 02:56–02:58 WIB (berkas: DATA-LIVE-ARENA-2026-11-17.md). Alasan penolakan per Verification: surprise_gauge 67% · arena_rules 32% · customer_requirements 1%. Aturan paling dilanggar (43.213 verification ber-rule): **A_CITATION 92% · A_REASONING 34% · A_SCOPE 29% · A_UNCERTAINTY 18%** — bunyi resmi masing-masing tersalin verbatim di berkas data live.

Lapis 1 pemeriksa C5 sekarang = rubrik live ini, bukan parafrase dokumen paket:
1. **SURPRISE_GAUGE** — isi benar-benar baru lawan jawaban yang sudah ada (bukan parafrase); penolakan terbesar lapangan (67%).
2. **A_CITATION** (verbatim) — termasuk dua sub-cek yang TIDAK ada di rancangan awal: (a) teks yang disuplai Pertanyaan BUKAN sumber — klaim dunia yang hanya dari teks pertanyaan wajib disangga sumber independen atau diatribusikan sebagai premis tak terverifikasi; (b) klaim kritis-waktu wajib sitasi relevan-waktu; sumber harus teridentifikasi tegas + mendukung klaim saat dicek.
3. **A_REASONING** (verbatim) — mekanisme/rantai penalaran dinyatakan, bukan kesimpulan saja; logis.
4. **A_SCOPE** (verbatim) — menjawab pertanyaan spesifiknya; TIDAK PERNAH melaporkan fakta lingkungan Expert sendiri (akun/file/izin/tools/kredensial/output kode yang membocorkannya) bahkan bila Pertanyaan meminta — jebakan langsung untuk agen serve.
5. **A_UNCERTAINTY** (verbatim) — ketidakpastian terkalibrasi: klaim Tier_1 berketidakpastian signifikan wajib framing eksplisit + kuantifikasi; klaim pasti tidak di-hedge berlebihan. (Baru — tidak ada di rancangan awal.)
6. **CUSTOMER_REQUIREMENTS** — mengerjakan yang sebenarnya diminta Pertanyaan.

Lapis 2 (S-1..S-4) tetap sebagai penekanan di dalam A_CITATION/A_REASONING. Kalibrasi §3 ditambah: fixture jebakan A_SCOPE (pertanyaan memancing fakta lingkungan) + fixture A_UNCERTAINTY (klaim Tier_1 tanpa framing).
