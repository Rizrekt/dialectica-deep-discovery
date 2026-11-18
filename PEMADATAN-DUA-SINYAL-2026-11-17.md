# PEMADATAN DUA SINYAL — 2026-11-17

**Status: SELESAI, terverifikasi.** Sisa kecil 2 fase testing (sesudah R3), dikerjakan fase testing, mode C5 tetap **shadow**, nol serve/submit/klaim, OpenRouter **0 panggilan**, plafon prompt 12 rb R3 tidak disentuh. Backup: `provider/novelty_context.py.bak-20261117-compact2`, `provider/test_novelty_truncation_r3.py.bak-20261117-compact2`.

## 1. Cacat yang ditutup

Urutan pemadatan R3 di `novelty_context.build_block` mengorbankan daftar *covered* lebih dulu — sampai habis — sebelum menyentuh kutipan. Pada uji nyata R3 (ISR `e20d251f…`, 25 verified) hasilnya: peta covered **24 → 0 poin**, kutipan 5 → 4. Pemeriksa menerima kutipan dalam tapi kehilangan peta semua jawaban verified yang sudah ada — padahal peta covered adalah sinyal murah pertama untuk deteksi pengulangan (SURPRISE_GAUGE): judul/klaim utama tiap jawaban, ±65 kar per poin, melawan 1.100 kar per kutipan. Tukar yang salah di ISR padat.

## 2. Rumus pemadatan: lama → baru

**Lama (R3).** Ulangi sampai muat: (1) pangkas covered dari ekor — tanpa lantai, bisa sampai 0; (2) buang kutipan terlemah; (3) cap per-kutipan menyusut ×0,7 ke lantai 200.

**Baru (dua sinyal).** Setiap iterasi mengambil pengorbanan pertama yang masih tersedia dalam urutan ini:

| Tahap | Pengorbanan | Batasnya |
|---|---|---|
| (a) | Cap per-kutipan menyusut ×0,7: 1.100 → 770 → 539 → 500 | berhenti di lantai lunak `_EXCERPT_CAP_SOFT_FLOOR = 500` |
| (b) | Kutipan terlemah dibuang (daftar urut dukungan terbanyak, ekor = terlemah) | sampai tersisa 1 kutipan |
| (c) | Poin covered dipangkas dari ekor, satu per satu | **berhenti di `COVER_FLOOR = 8`** — peta tidak pernah habis |
| (d) | Cap per-kutipan jatuh ×0,7: 500 → 350 → 245 → 200 | lantai keras `_EXCERPT_CAP_FLOOR = 200` (tetap) |

**Angka lantai dan dasarnya** (dari ukuran nyata blok uji R3: total tanpa pemadatan 7.947 kar; 24 poin covered = 1.552 kar teks poin, rata-rata 65 kar, maks 110 = `COVER_POINT_CAP`; 5 kutipan × 1.100 = 5.500 kar):

- `COVER_FLOOR = 8` = `MAX_COVER_POINTS / 3`. Biaya kasus-terburuk 8 × (110 + 3 kar render) = **904 kar ≈ 15% `BLOCK_CAP`**; pada spesimen nyata ±520 kar. Poin dikumpulkan dari jawaban dukungan-terbanyak lebih dulu, jadi 8 poin yang dilindungi adalah peta jawaban paling mapan.
- `_EXCERPT_CAP_SOFT_FLOOR = 500`: tahap (a) menyerap kelebihan muatan spesimen (±1.947 kar di atas cap) dalam dua langkah saja (lihat §3) tanpa satu pun sinyal kehilangan anggota; penurunan di bawah 500 dicadangkan sebagai tahap terakhir (d) supaya kedalaman kutipan tidak dikorbankan dua kali sebelum peta ikut menanggung.
- Blok minimum yang dijamin: peta lantai pada cap poin penuh (904) + 1 kutipan di lantai keras (200) + header kutipan (±85) + teks tetap header/intro/catatan (±740) ≈ **1.930 kar**, jauh di bawah `BLOCK_CAP = 6.000` — kedua lantai selalu bisa ditepati sebelum potongan defensif `block[:BLOCK_CAP]` (yang dipertahankan sebagai pengaman terakhir) berperan.

Perbaikan redaksi kecil yang ikut: catatan pemadatan di dalam blok kini berbunyi "covered list **at** N point(s)" (sebelumnya "trimmed to N") — pada hasil baru covered tidak selalu terpangkas, dan catatan harus menggambarkan yang benar-benar terjadi. Hitungan di catatan dan `meta["compacted"]` tetap cermin jujur keadaan akhir, seperti sebelumnya.

## 3. Bukti

**Uji nyata ulang — ISR yang sama dengan uji R3** (`e20d251f-b761-43c6-85e8-6936988a9ba2`, fetch live jalur produksi `context_for_isr`, 61 ISO, 25 verified; tanpa panggilan pemeriksa — yang dibuktikan komposisi bloknya). Hasil live dan hasil hitung-ulang atas snapshot payload yang sama identik:

| Versi | Poin covered | Kutipan | Cap kutipan | Total blok |
|---|---|---|---|---|
| Tanpa pemadatan | 24 | 5 | 1.100 | 7.947 kar |
| Urutan R3 (lama) | **0** | 4 | 1.100 | 5.361 kar |
| Urutan dua-sinyal (baru) | **24** | **5** | 539 | **5.339 kar** |

Tahap (a) saja menyerap seluruh kelebihan muatan (1.100 → 770 → 539); peta selamat **penuh**, kutipan selamat **semua**, dan blok akhir bahkan 22 kar lebih kecil dari hasil urutan lama. Catatan di blok: *"covered list at 24 point(s), 5 excerpt(s) at ≤539 chars each"*.

**Tes unit baru** — `provider/test_novelty_compaction_dual_signal.py`, **15/15**:

- Blok padat sintetis berbentuk spesimen (24 poin, 5 kutipan panjang): peta selamat penuh + semua kutipan selamat; pemadatan dinyatakan di blok + meta.
- Tekanan menengah (cap diperas ke 4.500): kutipan gugur lebih dulu (5 → 4), peta covered **tidak tersentuh** (24).
- Tekanan dalam (cap 1.600): peta berhenti **tepat** di `COVER_FLOOR = 8`, ≥1 kutipan selamat dan utuh pada cap-nya (ekor blok = teks sumber pada cap, bukan potongan buta).
- Regresi nol: blok yang muat tanpa pemadatan **byte-identik** (blok + meta) dengan modul pra-perubahan yang dimuat dari backup `.bak-20261117-compact2` — untuk fixture kecil, kosong, dan viso-0.

**Kontrak tes lama yang berubah (1 berkas):** `test_novelty_truncation_r3.py` kasus urutan pemadatan — ekspektasi lama ("covered dipangkas DULU") diganti kontrak urutan baru ("cap menyusut DULU, kedua sinyal utuh"), dengan penanda di docstring berkas bahwa urutannya kini dikunci oleh berkas tes dua-sinyal. 24/24 tetap hijau. `test_novelty_context.py` (35/35) tidak berubah dan tetap hijau — kasus cap-nya lolos di bawah kedua urutan.

**Suite penuh provider: 372/372 hijau** (15 berkas; basis 357 + 15 tes baru). Per berkas: cloudflare claim 8/8, cloudflare serve 33/33, dashscope 11/11, improve 17/17, length floors 32/32, **compaction dual-signal 15/15 (baru)**, novelty 35/35, r3 24/24, openrouter claim 10/10, openrouter wrapper 30/30 (0 gagal), semantic 40/40, serve_gate 51/51, target_picker 42/42, writer_fallback 11/11, zai 13/13.

## 4. Sisa risiko

- **Kedalaman kutipan kini pengorbanan pertama.** Di ISR padat-kutipan pemeriksa menerima peta penuh + kutipan lebih dangkal (spesimen: 539 vs 1.100 kar). Itu arah tukar yang dimandatkan perbaikan ini; bila suatu hari data panel menunjukkan kedalaman kutipan lebih menentukan daripada keluasan peta, urutannya bisa ditinjau — datanya belum ada.
- **Langkah tahap (a) kasar (×0,7).** Blok bisa berakhir jauh di bawah cap (fixture sintetis: 4.711 kar pada cap 5.500) — aman (tidak pernah melanggar cap), tapi kedalaman kutipan dilepas dalam lompatan, bukan sehalus mungkin.
- **Yang dilindungi lantai adalah KEPALA peta.** Poin dikumpulkan dari jawaban dukungan-terbanyak lebih dulu; di bawah tahap (c) yang terpangkas tetap ekor peta (jawaban paling lemah cakupannya) — disengaja, tapi berarti keluasan dari jawaban dukungan-rendah adalah bagian peta pertama yang hilang di tekanan dalam.
- **Jalur baca tetap bisa goyah.** Satu fetch live selama verifikasi sempat timeout; modul berperilaku fail-soft seperti dirancang (state "failed", blok kosong, tanpa pengecualian) dan fetch ulang berhasil identik. Bukan urusan pemadatan, dicatat apa adanya.

*Berkas: `provider/novelty_context.py` (konstanta `COVER_FLOOR` + `_EXCERPT_CAP_SOFT_FLOOR`, loop pemadatan dua-sinyal di `build_block`, redaksi catatan), `provider/test_novelty_compaction_dual_signal.py` (baru), `provider/test_novelty_truncation_r3.py` (kontrak urutan diperbarui). Terkait: MITIGASI-KONTEKS-TERPOTONG-2026-11-17.md §4 (sisa risiko pertama yang ditutup berkas ini), KONTEKS-KEBARUAN-C5-2026-11-17.md.*
