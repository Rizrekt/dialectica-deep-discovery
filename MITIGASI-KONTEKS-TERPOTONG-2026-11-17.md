# MITIGASI KONTEKS TERPOTONG (R3) — 2026-11-17

**Status: SELESAI, terverifikasi.** Revisi persiapan R3 (persetujuan user 2026-11-17 08:36), dikerjakan fase testing, mode C5 tetap **shadow**, nol serve/submit/klaim. Backup: `provider/serve_gate.py.bak-20261117-r3`, `provider/novelty_context.py.bak-20261117-r3`, `provider/test_novelty_context.py.bak-20261117-r3`.

## 1. Cacat yang ditutup

`build_semantic_prompt` memotong string pertanyaan gabungan (pertanyaan + blok kebaruan yang ditempel `novelty_context.attach` di ekornya) pada `_SEMANTIC_QUESTION_CAP = 12000`. Pada prompt serve panjang, blok kebaruan — satu-satunya bahan penilai SURPRISE_GAUGE — terpotong diam-diam, di tengah teks, tanpa sinyal apa pun di log. Cek kebaruan buta persis di kasus berat (KONTEKS-KEBARUAN-C5-2026-11-17 §keterbatasan).

## 2. Mekanisme: sebelum → sesudah

**Sebelum.** Satu string gabungan dipotong di 12.000 kar; blok di ekor jadi korban pertama. Blok yang sendirinya melebihi `BLOCK_CAP` dipotong buta oleh `build_block` (`block[:BLOCK_CAP] + "…[novelty context truncated]"`), walau metanya tetap mengaku mengutip 5 jawaban. Log semantic-check tidak mencatat pemotongan apa pun.

**Sesudah — dua lapis.**

1. **Saluran terpisah di perakitan prompt** (`serve_gate._split_novelty_block` + `build_semantic_prompt`): blok dipisah dari string gabungan lewat header-nya (`novelty_context.BLOCK_HEADER`, dibaca dari modulnya dengan fallback literal), teks pertanyaan dipotong ke cap seperti biasa, lalu blok ditempel kembali **utuh sebagai seksi prompt tersendiri** sesudah konteks pertanyaan. Cap kini mengikat teks pertanyaan saja. Tanpa blok, prompt **byte-identik** dengan bentuk pra-R3 (dibuktikan tes regresi). Blok tetap menumpang setiap panggilan segmen pada jalur tersegmentasi, seperti sebelumnya.
2. **Pemadatan bertahap di sumbernya** (`novelty_context.build_block`): blok yang melebihi `BLOCK_CAP = 6000` tidak lagi dipotong buta, melainkan dirender ulang bertahap — (a) daftar *covered* dipangkas dari ekor dulu, (b) lalu kutipan terlemah dibuang, (c) lalu cap per-kutipan menyusut (1100 → ×0,7, lantai 200) — sampai muat. Blok memuat catatan pemadatannya sendiri (`COMPACTED_MARK = "Novelty context compacted"`, termasuk hitungan akhir), dan `meta["compacted"]` mencerminkannya. Rumus cadangan ruang: pertanyaan ≤ 12.000 + blok ≤ 6.000, keduanya dijamin terpisah — total konteks yang dijamin sampai = 18.000 kar + draf.

**Sinyal terbuka (tidak ada lagi pemotongan diam).** Setiap record log semantic-check kini memuat: `question_text_chars`, `question_truncated` (teks pertanyaan menyentuh cap), `novelty_chars`, `novelty_compacted` (dari catatan di dalam blok), dan `prompt_chars` (panjang prompt terbesar yang benar-benar terkirim, dari jalur segmen). Baris stderr arming juga menandai `DIPADATKAN` saat blok terpadatkan.

## 3. Bukti

**Tes unit baru** — `provider/test_novelty_truncation_r3.py`, **24/24**:

- Pertanyaan 15 rb kar + blok: ekor blok (sentinel) sampai utuh di prompt; ekor pertanyaan terpotong; porsi pertanyaan ≤ 12.000.
- Regresi nol: tanpa blok, prompt byte-identik pra-R3 untuk pertanyaan pendek, panjang (20 rb), dan kosong.
- Log: record mock-call memuat `question_truncated=true`, `novelty_chars` = panjang blok persis, `novelty_compacted=false`, `prompt_chars` = panjang prompt yang tertangkap mock.
- Blok terpadatkan: `novelty_compacted=true` tercatat; markah pemadatan + ekor blok utuh di prompt.
- Jalur tersegmentasi (draf 17 rb kar, 2 segmen): blok utuh di **kedua** prompt segmen.
- Urutan pemadatan: dengan cap dimonkeypatch longgar sebagai pembanding, versi terpadatkan mengorbankan poin *covered* (20 → lebih sedikit) sementara kutipan tetap 5/5 — covered dulu, kutipan terakhir, sesuai rancangan.

**Kontrak tes lama yang berubah (1 berkas):** `test_novelty_context.py` kasus cap — ekspektasi lama ("5 kutipan DAN blok ≤ cap" — hanya bisa dipenuhi potong buta) diganti kontrak pemadatan: kutipan ≤ `MAX_EXCERPTS`, blok ≤ `BLOCK_CAP` ketat (tanpa kelonggaran +40), blok berakhir pada kutipan utuh, markah + meta pemadatan wajib ada. 33 → **35/35**.

**Uji nyata shadow (1 panggilan pemeriksa asli, lane Vyce saja — OpenRouter 0 panggilan):** ISR `e20d251f-b761-43c6-85e8-6936988a9ba2` (spesimen serve 14 Nov, prompt serve terukur 141.901 token; 61 ISO, **25 verified** terbaca live).

- Blok dibangun jalur produksi (`context_for_isr` atas fetch live): **5.361 kar, terpadatkan di data nyata** (covered 24 → 0 poin, kutipan 5 → 4 — lihat sisa risiko).
- Pertanyaan uji 331.334 kar disusun dari teks nyata ISR yang sama (konten + teks penuh jawaban verified-nya; prompt serve verbatim tidak tersimpan, jadi regim panjangnya direproduksi dari bahan nyata ISR itu dan dinyatakan apa adanya). Draf uji = 900 kar kepala Verified Answer 1 sendiri.
- **Kontrafaktual pra-R3: blok yang terlihat di prompt = 0 dari 5.361 kar** (pertanyaan sendiri 27× cap). **Pasca-R3: 5.361 dari 5.361 kar** — header + ekor kutipan terakhir terverifikasi byte-wise di prompt yang benar-benar terkirim (24.825 kar, tersimpan di artefak uji).
- Log record: `question_truncated=true`, `novelty_chars=5361`, `novelty_compacted=true`, `prompt_chars=24825`, `segments=1/1`.
- Konteksnya bukan cuma sampai — **bekerja**: pemeriksa (Nemotron via Vyce, percobaan pertama) membalas **fatal, 1× SURPRISE_GAUGE**, menandai draf sebagai pengulangan Verified Answer 1 (d1387fc0) "visible in the context". Di regim pra-R3 temuan ini mustahil: bahan pembandingnya tidak pernah meninggalkan mesin.

**Suite penuh provider: hijau semua** — per berkas: cloudflare claim 8/8, cloudflare serve 33/33, dashscope 11/11, improve 17/17, novelty 35/35, **r3 24/24 (baru)**, openrouter claim 10/10, openrouter wrapper bersih, semantic 40/40, serve_gate 51/51, target_picker 42/42, writer_fallback 11/11, zai 13/13.

## 4. Sisa risiko

- **Urutan pemadatan mengorbankan peta covered secara total pada ISR padat-kutipan.** Di uji nyata, 25 verified menghasilkan blok yang kelebihan muatan didominasi kutipan (5 × 1.100), sehingga daftar covered (peta murah semua jawaban) terpangkas 24 → 0 sebelum kutipan dikorbankan. Sesuai urutan yang dirancang (covered dulu), tapi akibatnya: pada ISR seperti ini pemeriksa menerima 4 kutipan dalam dan kehilangan peta 25 jawaban. Bila nanti dianggap merugikan, kandidat revisi = cadangkan jatah minimum covered sebelum pemadatan mulai (keputusan terpisah, bukan bagian R3).
- **Pemisahan blok bergantung pada teks header.** Bila `novelty_context.BLOCK_HEADER` suatu hari diganti tanpa menyelaraskan fallback literal di `serve_gate`, pemisahan gagal dan perilaku kembali ke pra-R3 (blok di dalam string tercap) — menurun secara aman (cek tetap jalan), tapi mitigasi hilang diam-diam di level prompt; log akan menunjukkannya sebagai `novelty_chars=0` pada ISR berviso > 0, jadi terbaca di record.
- **Prompt membengkak terukur:** konteks terjamin kini 18 rb kar (12 rb pertanyaan + 6 rb blok) di SETIAP segmen — pada draf tersegmentasi banyak, biaya per panggilan pemeriksa naik sebanding; itu harga yang dinyatakan, bukan kebocoran.
- Uji nyata memakai pertanyaan reproduksi dari teks nyata ISR yang sama (bukan prompt serve verbatim — tidak tersimpan di artefak mana pun); jalur fetch, blok, pemeriksa, dan log-nya adalah jalur produksi persis.

*Berkas: `provider/serve_gate.py` (penanda + `_split_novelty_block` + `build_semantic_prompt` + field log R3), `provider/novelty_context.py` (`_render_block` + pemadatan bertahap + `COMPACTED_MARK`), `provider/test_novelty_truncation_r3.py` (baru), `provider/test_novelty_context.py` (kontrak cap diperbarui). Terkait: KONTEKS-KEBARUAN-C5-2026-11-17.md (item 2 yang keterbatasannya ditutup berkas ini), KALIBRASI-C5-2026-11-17.md §6 risiko 4.*
