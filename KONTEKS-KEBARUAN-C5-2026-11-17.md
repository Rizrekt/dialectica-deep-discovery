# KONTEKS KEBARUAN C5 — Surprise Gauge Context untuk Pemeriksa Semantik

**Tanggal:** 2026-11-17 (item 2 dari 5, perintah user "gas satu-satu") · **Fase:** TESTING — SHADOW saja. Nol serve/submit/klaim; mode C5 tidak diubah (tetap shadow, keputusan user 06:12).
**Vonis: MEKANISME JALAN — SURPRISE_GAUGE menyala dengan konteks, senyap tanpa konteks, di semua sel A/B yang berhasil terbaca (2/2 vs 0/2).** Kontrol positif (draf parafrase yang sengaja mengulang jawaban eksisting) **tertangkap dengan konteks, tidak ditandai surprise tanpa konteks**. Kelemahan run ini bukan di mekanismenya: 10 dari 14 panggilan pemeriksa gugur *unavailable* karena lane pemeriksa sendiri kolaps stokastik (lihat §4).

---

## 1. Yang dibangun

| Komponen | Isi |
|---|---|
| Modul baru | `provider/novelty_context.py` — perakit konteks kebaruan (fetch + filter + blok), murni + seam injeksi untuk tes |
| Titik pasang | `serve_gate.armed_semantic_check` — titik yang sama dengan C5: sesudah arming `DIALECTICA_SEMANTIC_CHECK=1`, pertanyaan pemeriksa ditambah blok kebaruan lewat helper baru `_with_novelty_context` (diff lawan backup: 46 baris, hanya seksi ini). `vyce_serve_common.vyce_pipeline` tidak diubah — ia sudah meneruskan `isr_id` ke titik ini |
| Sub-flag | `DIALECTICA_SEMANTIC_NOVELTY` — bawaan ikut flag induk; `=0` mematikan konteks ini saja, C5 lain tetap jalan |
| Fetch | Menumpang arming fetch gerbang serve (`DIALECTICA_SERVE_GATE_FETCH=1`, diset run_serve bersamaan dengan flag semantik) — proses tak ter-arm tidak menyentuh jaringan sama sekali, pola yang sama dengan `fetch_isr_detail` |
| Kegagalan | `context_for_isr` tidak pernah raise: fetch gagal/payload sampah → blok kosong + state tercatat; di titik pasang, kegagalan dicetak keras ke stderr dan cek jalan TANPA konteks — konteks yang mati tidak pernah membunuh atau mengubah cek |
| Backup | `provider/serve_gate.py.bak-20261117-novelty` (dibuat sebelum edit) |
| Tes | `provider/test_novelty_context.py` — 33 tes baru; suite penuh provider **270/270 hijau** (basis 237 + 33) |
| Runner bukti | `provider/run_novelty_ab.py` (fase `select`/`run`) + `provider/run_novelty_control_retry.py` (satu ronde ulang terbatas khusus sel kontrol); artefak di `novelty-2026-11-17/` (pack.json, results.json, semantic-log.jsonl, control-paraphrase-a6148000.txt) |

## 2. Sumber data + bentuk blok

**Sumber (jalur klien sendiri, bukan karangan):** `GET /api/node/isos/{isr_id}` → `{"isos": [...]}` — endpoint yang sama dengan perintah `trued question` dan korpus bersih kalibrasi C5. Per ISO dipakai hanya field yang dibaca klien: `status` (filter `verified`), teks di `reveal.data.structured_data.answer` (skema klasik) atau `.reasoning` (jawaban forecasting), `supportedCount`, `refutationCount`, `timestamp`, `id`, `isOwnAgent`. Detail ISR (untuk teks pertanyaan) tetap dari jalur target_picker/`/api/node/isr/{id}` yang sudah ada — tidak ada jalur tarikan baru.

**Bentuk blok** (menempel di akhir string pertanyaan pemeriksa, di dalam cap pertanyaan 12 rb kar `build_semantic_prompt`):

1. Header `EXISTING VERIFIED ANSWERS — SURPRISE GAUGE CONTEXT` + jumlah verified total dan berapa yang dikutip + kalimat aturan (isi yang sudah ada di sini BUKAN hal baru; parafrase tanpa fakta/mekanisme/angka/sudut baru berhenti di Surprise Gauge).
2. **Daftar covered** — heading / lead tebal / kalimat pertama TIAP jawaban verified (diekstrak mekanis dari teksnya sendiri, tanpa parafrase oleh kita), maks 24 poin × 110 kar. Ini peta murah-penuh tentang "yang sudah dikatakan".
3. Catatan kejujuran (jawaban tak terkutip / verified tanpa teks reveal) — ditaruh SEBELUM kutipan supaya pemotongan cap memakan ekor kutipan, bukan angka.
4. **Kutipan** 5 jawaban verified dengan `supportedCount` tertinggi (seri: terbaru dulu), maks 1.100 kar per jawaban.

**Batas ukuran:** blok maks **6.000 kar** (dipotong dengan penanda eksplisit). Ukuran terukur di 3 ISR live run ini: 3.027 / 3.084 / 3.068 kar. **Viso 0 = blok kosong yang sah** (meta `verified_total: 0`, state `ok`) — bentuk Pioneer memang tidak punya pembanding.

## 3. Bukti kerja A/B (shadow, live)

Tiga ISR live viso 2 (satu-satunya bentuk viso ≥2 yang tersedia saat tarikan: 5 baris viso ≥2 dari 100 kandidat; ketiganya di luar topik inti — kelas bayar tidak relevan untuk uji mekanisme ini). Per draf: `semantic_check` dua kali — pertanyaan polos vs pertanyaan + blok — lane pemeriksa Vyce-dulu (preseden dry-run: jaga cadangan OpenRouter), mode shadow, log khusus run.

| Draf | Tanpa konteks | Dengan konteks |
|---|---|---|
| **Kontrol parafrase** — ISR `a6148000` (FOCIL/EIP-7805), 2.280 kar, ditulis tangan mengulang isi Verified Answer 1 (632c6439) dengan kata sendiri | 1 run terbaca: **fatal, 2× A_CITATION, 0 SURPRISE_GAUGE** (3 run unavailable) | 1 run terbaca (retry rep1): **fatal, 1× SURPRISE_GAUGE** (3 run unavailable) |
| GLM — ISR `67101f77` (penyimpanan co-location), 741 kar | **clean, 0 temuan** | **fatal, 1× SURPRISE_GAUGE** |
| GLM — ISR `a6148000`, 6.574 kar | unavailable | unavailable |
| GLM — ISR `206c07dc` (snapshot airdrop), 7.872 kar | unavailable | unavailable |

**Isi temuan SURPRISE_GAUGE (kutipan terverifikasi ulang ke draf oleh parser C5):**

- Kontrol: pemeriksa menunjuk kalimat pembuka draf dan menulis bahwa Verified Answer 1 dan 2 *sudah mencakup* penandatanganan header buta oleh proposer, sensor di lapisan builder, biaya menolak bid, komite 17 validator, inclusion list 8 KB, penegakan fork-choice/orphaning, dan mode gagal divergensi IL — persis tumpang-tindih yang ditanam. Tanpa konteks, draf yang sama hanya kena A_CITATION (angka tanpa sumber) — **surprise-nya lolos**.
- GLM `67101f77`: kalimat kesimpulan inti draf ditandai sebagai parafrase kesimpulan + mekanisme Verified Answer 2 (batas POI yang mengikat, menangkap energi yang ter-curtail, menghindari interkoneksi kedua). Tanpa konteks draf ini **clean total**.

**Bacaan:** SURPRISE_GAUGE menyala **2/2** run dengan-konteks yang terbaca dan **0/2** run tanpa-konteks yang terbaca. Kontrol positif **LOLOS uji** (tertangkap dengan konteks; tidak tertangkap surprise tanpa konteks). Ini bukti mekanisme pada sel yang terbaca — bukan pengukuran tingkat tangkapan populasi (lihat keterbatasan).

## 4. Kegagalan run (dilaporkan apa adanya)

- **Lane pemeriksa kolaps stokastik sepanjang run:** 10/14 invokasi `semantic_check` berakhir `unavailable`. Polanya sama dengan yang didokumentasikan PERBAIKAN-PENGHAMBAT: Nemotron-Vyce membakar budget di `reasoning_content` (±31–33 rb kar) lalu stream berakhir tanpa teks jawaban; satu run dengan-konteks menjawab non-JSON. Lane OpenRouter tidak pernah menyelesaikan satu pun panggilan: probe kuotanya melaporkan sisa **1 < 2**, jadi lane itu melewatkan dirinya sendiri sesuai aturan cadangannya (nol kuota terbakar — yang terpakai hanya panggilan `key` gratis).
- **Generasi GLM:** percobaan pertama ISR `a6148000` mati total (GLM kosong — reasoning 66–68 rb kar; fallback deepseek 403 permanen) lalu berhasil di percobaan kedua. Draf `67101f77` lahir hanya 741 kar (stub di bawah lantai serve — A/B-nya tetap sah sebagai spesimen teks, tapi bukan draf serve penuh). Dua draf penuh (6.574 + 7.872 kar) lahir sehat, tetapi keempat run pemeriksanya unavailable, jadi sel A/B mereka kosong.
- **Satu ronde ulang terbatas** dijalankan khusus untuk sel penentu kontrol (run_novelty_control_retry.py, tanpa generasi baru): di situlah tangkapan SURPRISE_GAUGE kontrol terbaca. Hasil retry dicatat sebagai blok terpisah di results.json, tidak menimpa run utama.

## 5. Panggilan per lane

| Lane | Panggilan | Hasil |
|---|---|---|
| Vyce GLM (generasi serve, tercatat cap) | cap **3 → 6 dari 10** (+3 tercatat: a6148000 percobaan-2, 67101f77, 206c07dc) | 3 draf lahir (741 / 6.574 / 7.872 kar); 2 percobaan gagal tanpa catatan generasi (GLM kosong + deepseek 403) |
| Vyce Nemotron (pemeriksa, lane pertama run ini) | 14 invokasi semantic_check | 4 terbaca (semua vonis di tabel §3), 10 unavailable (reasoning-overflow / non-JSON) |
| OpenRouter Nemotron (pemeriksa, cadangan run ini) | dipanggil hanya saat Vyce gagal | 0 selesai — terlewati aturan cadangan kuota (sisa 1 < 2); 0 kuota generasi terbakar |
| API klien `trued` (read-only) | fase select: 1 search peluang + 5 detail ISR + 5 fetch isos | 3 ISR terpaket; fase run memakai paket, nol tarikan ulang |

## 6. Keterbatasan

1. **Ketersediaan pemeriksa adalah batas bukti, bukan konteksnya.** Kesimpulan bertumpu pada 2 pasang sel terbaca (kontrol + draf GLM pendek). Dua draf panjang penuh tidak terbaca sama sekali. Mengulang A/B saat lane sehat akan menebalkan angka; mekanisme + kontrol positif sudah terbukti arahnya.
2. **Biaya token konteks:** blok menambah ±3 rb kar (±750–900 token) ke SETIAP panggilan pemeriksa di pertanyaan viso ≥1; di jalur tersegmentasi pertanyaan (termasuk blok) dikirim ulang per segmen — draf 3 segmen membayar konteks 3×.
3. **Risiko terpotong diam-diam di produksi:** blok menempel PALING AKHIR string pertanyaan, sedangkan `build_semantic_prompt` memotong pertanyaan di 12.000 kar. Di produksi "pertanyaan" yang diteruskan pipa adalah prompt serve utuh (pertanyaan + kontrak format + steering) — prompt panjang bisa mendorong blok melewati cap dan memotongnya habis tanpa sisa. Log semantik mencatat `question_chars`, jadi keterpotongan terlihat, tetapi mitigasinya (blok disisipkan sebelum kontrak, atau cap dinaikkan) belum dibangun — di luar cakupan item ini.
4. **Kelengkapan data API:** teks hanya tersedia untuk ISO yang sudah reveal; verified yang belum reveal terhitung di meta (`unrevealed`) tetapi tidak bisa dibandingkan — draf yang mengulang jawaban verified-belum-reveal akan lolos dari konteks ini. Di 3 ISR run ini unrevealed = 0.
5. **Urut dukungan ≠ kebenaran:** kutipan dipilih dari `supportedCount` tertinggi karena dukungan menandai cakupan yang paling mapan — untuk Surprise Gauge yang dibandingkan adalah *kehadiran isi*, bukan kebenarannya, jadi ini memang sumbu yang benar; tetapi jawaban verified yang dukungannya rendah dan isinya unik hanya muncul lewat daftar covered (heading), bukan kutipan penuh.
6. **Varians pemeriksa:** satu sampel per sel (kontrol 2 rep per kondisi, mayoritas unavailable). KALIBRASI-C5 sudah mengukur himpunan temuan bisa berubah antar-run; angka 2/2 vs 0/2 adalah arah yang konsisten di dua spesimen berbeda, bukan estimasi rate.
7. **Ketiga ISR uji viso 2 dan di luar topik inti** — perilaku blok pada viso tinggi (belasan verified, daftar covered + cap 6 rb kar bekerja penuh) teruji di unit saja, belum live; pool live saat tarikan memang hanya menyediakan 5 baris viso ≥2.

---

*Berkas: `provider/novelty_context.py`, `provider/serve_gate.py` (seksi arming; backup `.bak-20261117-novelty`), `provider/test_novelty_context.py`, `provider/run_novelty_ab.py`, `provider/run_novelty_control_retry.py`, `novelty-2026-11-17/` (pack.json, results.json, semantic-log.jsonl, control-paraphrase-a6148000.txt). Terkait: KALIBRASI-C5-2026-11-17.md §6 risiko 4 (celah yang ditutup berkas ini), DATA-LIVE-ARENA-2026-11-17.md (SURPRISE_GAUGE 67%), PEMILIH-TARGET-2026-11-17.md (sel Innovator).*

---

## Addendum 2026-11-17 (sore) — Ukur ulang draf GLM `3b5c0f0c`: utang TETAP TERBUKA

Sisa kecil 3 fase testing: draf GLM `3b5c0f0c` (ISR `3b5c0f0c-1637-4cba-a2eb-8429c0a9d910`, ZK-bridge vs optimistic fraud proofs; teks utuh 7.471 kar tersimpan di `dryrun-2026-11-17/step4-dryruns-results.json`, cocok dengan `final_chars` tercatat; saat lahir gate OK, sendable=True) diukur ulang dengan `semantic_check` lane **Nemotron-Vyce saja** (OpenRouter 0 panggilan — sisa kuota 1 tidak disentuh), mode shadow, konteks kebaruan jalur produksi pasca-R3 terlampir live: **27 verified, 4 dikutip, blok 5.361 kar (DIPADATKAN), utuh terverifikasi di prompt rakitan 19.524 kar**.

**Vonis: TETAP TAK TERUKUR.** 3/3 invokasi (plafon percobaan) gugur dengan spesies kegagalan yang sama persis: Nemotron-Vyce membakar budget di `reasoning_content` (31.076 / 29.968 / 32.298 kar) lalu stream berakhir dengan teks jawaban kosong. Percobaan 1 draf utuh; percobaan 2–3 tersegmentasi sah pola kalibrasi (potongan 3.164 + 4.307 kar) — segmentasi TIDAK menolong: luapan terjadi bahkan pada potongan ±3 rb kar, jadi penyebabnya perilaku lane pada prompt konteks-besar ini, bukan panjang draf. Utang ini bukan soal draf dan bukan soal konteks (konteks sampai utuh); ia soal ketersediaan lane pemeriksa Vyce — pola kolaps yang sama dengan §4 berkas ini dan PERBAIKAN-PENGHAMBAT. Berkas ringkas: `UKUR-ULANG-DRAF-3B5C0F0C-2026-11-17.md`.
