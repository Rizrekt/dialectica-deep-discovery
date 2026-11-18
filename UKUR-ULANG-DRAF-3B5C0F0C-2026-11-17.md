# UKUR ULANG DRAF GLM `3b5c0f0c` — C5 (sisa kecil 3 fase testing)

**Tanggal:** 2026-11-17 · **Fase:** TESTING — SHADOW. Nol serve/submit/klaim; mode C5 tidak diubah (shadow). Nol kode produksi diubah (pengukuran lewat seam injeksi `model_call` milik `semantic_check` sendiri).

**Vonis: TETAP TAK TERUKUR** — 3/3 invokasi pemeriksa gugur *unavailable* (reasoning-overflow Nemotron-Vyce), persis spesies kegagalan dua percobaan aslinya. Bukan CLEAN, bukan FATAL — tidak ada vonis isi yang sah dari run ini.

---

## 1. Draf — ketemu utuh (bukti)

- Sumber: `dryrun-2026-11-17/step4-dryruns-results.json`, baris ISR `3b5c0f0c-1637-4cba-a2eb-8429c0a9d910`.
- Teks field `draft` = **7.471 kar**, cocok persis dengan `final_chars: 7471` tercatat di baris yang sama (PERBAIKAN-PENGHAMBAT-2026-11-17.md baris 146: GLM final 7.471 kar, audit 0, trace bersih, gate OK, **sendable=True**).
- Pertanyaan pasangan: *"How do zero-knowledge proofs reduce the cost of verifying cross-chain bridge transactions compared with optimistic fraud proofs?"*
- Konteks kebaruan pasangan dibangun live lewat jalur produksi pasca-R3 (`serve_gate._with_novelty_context` → `novelty_context.context_for_isr`, fetch armed): **27 verified** di ISR ini sekarang (ronde maratonnya sudah settle sejak draf lahir), **4 dikutip**, blok **5.361 kar, DIPADATKAN** (jalur pemadatan R3). Blok terverifikasi **utuh di prompt rakitan** `build_semantic_prompt` (19.524 kar) — jalur tahan-potong R3 yang dipakai, bukan jalur lama.

## 2. Tiga invokasi (plafon percobaan habis)

| # | Bentuk | Lane | Hasil |
|---|---|---|---|
| 1 | Draf utuh 7.471 kar (1 segmen) | vyce-nemotron | unavailable — `empty answer text (stream ended); reasoning_content held 31076 chars` |
| 2 | Potongan 1/2 — 3.164 kar | vyce-nemotron | unavailable — reasoning_content 29.968 kar, jawaban kosong |
| 3 | Potongan 2/2 — 4.307 kar | vyce-nemotron | unavailable — reasoning_content 32.298 kar, jawaban kosong |

Segmentasi sah pola kalibrasi (potong di batas paragraf + konteks sama per potongan) **tidak menolong**: luapan reasoning terjadi bahkan pada potongan ±3 rb kar. Bacaan: pemicunya perilaku lane Nemotron-Vyce pada prompt berkonteks-besar ini (prompt rakitan ±19,5 rb kar termasuk blok kebaruan 5.361 kar), bukan panjang draf — konsisten dengan kolaps stokastik lane yang didokumentasikan di KONTEKS-KEBARUAN-C5 §4 (10/14 unavailable) dan dua percobaan asli draf ini (31.207 / 29.015 kar, PERBAIKAN-PENGHAMBAT).

Catatan ketelitian: pesan "PERINGATAN KERAS … di kedua lane" yang dicetak `semantic_check` adalah teks generik tahap itu; run ini menginjeksi caller **Vyce-only**, jadi satu-satunya lane yang benar-benar dipanggil adalah vyce-nemotron (penghitung panggilan di runner: 3). OpenRouter **0 panggilan** — tidak disentuh sesuai aturan keras (sisa kuota 1 = cadangan darurat).

## 3. Kesimpulan + sisa utang

- Draf `3b5c0f0c` tetap **satu-satunya draf sendiri yang C5-nya tak terukur**; utang ukurnya kini terkonfirmasi BUKAN utang artefak (teks + konteks lengkap dan sampai utuh ke prompt) melainkan **utang ketersediaan lane pemeriksa Vyce**.
- Penuntas yang sah di luar plafon run ini: ukur ulang saat lane Nemotron-Vyce sehat (pola run-11: lane kolaps bersifat stokastik per-jendela), atau lewat lane pemeriksa cadangan ketiga (gpt-oss Cloudflare) sesudah sertifikasi racun #5–#8 tuntas — keduanya utang terjadwal yang sudah tercatat, bukan tebakan baru.
- Addendum juga dicatat di `KONTEKS-KEBARUAN-C5-2026-11-17.md` (seksi Addendum 2026-11-17 sore).

*Artefak run: runner `/tmp/ukur_ulang_3b5c0f0c.py`, hasil `/tmp/ukur_ulang_3b5c0f0c_result.json`; 3 record run ini masuk log produksi `provider/semantic-check-log.jsonl` (mode shadow, isr 3b5c0f0c).*
