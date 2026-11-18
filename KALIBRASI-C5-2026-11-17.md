# KALIBRASI C5 — Self-VFP Semantik Jalur Serve Dialectica

**Tanggal:** 2026-11-17 (bangun ±02:47–04:10 WIB) · **Kontrak:** RANCANGAN-C5-2026-11-17.md (§1–§6)
**Vonis akhir: SHADOW CUKUP — BELUM SIAP BLOCKING.** Pemeriksa menangkap 7/7 racun historis (lintas dua ronde) dan 3/3 fixture baru, tetapi menandai fatal 4/6 jawaban VERIFIED lapangan — terlalu ketat untuk menahan kiriman; sebagai peringatan bayangan ia persis yang dibutuhkan pilot.

---

## 1. Bentuk akhir yang terpasang

| Komponen | Isi |
|---|---|
| Fungsi | `serve_gate.semantic_check(draft, question, isr_id, model_call, mode, log_path)` → dict terstruktur `{performed, available, mode, checker, verdict: fatal/clean/unavailable, findings[{code, sub, quote, claim, why}], block, dropped_findings, model_verdict, error}`; selalu menulis 1 record ke log |
| Pemeriksa silang | Primer: **Nemotron** (`nvidia/nemotron-3-ultra-550b-a55b:free`) via klien connector OpenRouter, max-tokens 8000 + 1 retry bila balasan kosong (budget kecil → HTTP 200 berbadan kosong, terbukti di item kalibrasi pertama; sesudah perbaikan lane primer tidak pernah gagal lagi). Cadangan: **Nemotron via Vyce** (`nemotron-3.5-super-vl`, env `DIALECTICA_SEMANTIC_FALLBACK_MODEL`) |
| Perubahan lane cadangan | Rancangan awal menyebut deepseek-v4.1 via Vyce. **Probe live 2026-11-17: rute deepseek-v4.1 menjawab 403** dari runtime ini, sementara GLM dan Nemotron-Vyce menjawab normal — jadi deepseek tidak bisa jadi cadangan; diganti Nemotron-Vyce (tetap beda model dari penulis GLM, sifat cross-check utuh) |
| Mode | Env `DIALECTICA_SEMANTIC_MODE`: `block` = temuan fatal menahan; selain itu **shadow (default)** — catat ke `provider/semantic-check-log.jsonl`, TIDAK PERNAH memblokir |
| Pemeriksa tak tersedia | Kedua lane gagal / balasan tak terparse → verdict `unavailable`, performed=False, block=False, record log bertanda `"loud": true` + PERINGATAN KERAS ke stderr. Tidak diam, tidak memblokir, tidak menyamar jadi clean |
| Bukti temuan | Kutipan **diverifikasi ulang terhadap draf** (normalisasi whitespace + lipatan tipografi U+2011→`-`, NBSP→spasi, kutip lengkung→lurus). Kutipan yang tak cocok dibuang dan tidak bisa membuat fatal. Kode tak dikenal dibuang; kode warisan dipetakan (lihat §2) |
| Pemasangan | `vyce_serve_common.vyce_pipeline` meneruskan callable ke `gate_answer` (satu titik — melayani vyce_serve_prepare + fallback provider). Callable hanya hidup bila env `DIALECTICA_SEMANTIC_CHECK=1`, yang diset `run_serve.py` **hanya** di cabang serve Vyce tergating (bukan Cloudflare §39, bukan --answer) — pola arming yang sama dengan liveness fetch, supaya suite tetap hermetik |
| Cadangan berkas | `serve_gate.py.bak-20261117-c5`, `vyce_serve_common.py.bak-20261117-c5`, `run_serve.py.bak-20261117-c5` (dibuat sebelum edit pertama) |

Tidak ada yang dinyalakan: serve live tetap mati, config Expert tidak diubah, badan cron tidak diubah, cap/kill-metric tidak diubah. Mode produksi saat ini = shadow secara default env (tidak ada env yang diset).

## 2. Perubahan basis spek (dua koreksi user, keduanya diterapkan)

1. **§5 (user 02:53):** basis spek utama BUKAN daftar racun historis, melainkan kriteria proyek sendiri (Pilar 2) dari dokumen resmi paket — prompt sempat dibangun dua lapis P1..P5 + penekanan S-1..S-4.
2. **§6 (user 02:55, "cek data live yang diminta detail dan teliti"):** dokumen paket adalah snapshot; **rubrik final = DATA LIVE SERVER** (`trued arena general`, ditarik 2026-11-17 02:56 WIB, berkas DATA-LIVE-ARENA-2026-11-17.md). Lapis 1 kini enam rule live verbatim, dan P1..P5 **pensiun**:

| Kode live | Isi (ringkas) | Bobot lapangan |
|---|---|---|
| SURPRISE_GAUGE | Kebaruan lawan jawaban yang sudah ada; parafrase berhenti di sini | 67% penolakan |
| A_CITATION | Sumber teridentifikasi tegas + mendukung saat dicek; klaim kritis-waktu wajib sitasi relevan-waktu; **teks yang disuplai Pertanyaan BUKAN sumber** | 92% verifikasi ber-rule |
| A_REASONING | Mekanisme/rantai penalaran dinyatakan, logis | 34% |
| A_SCOPE | Menjawab pertanyaan spesifik; **TIDAK PERNAH melaporkan fakta lingkungan Expert sendiri** (akun/file/izin/tools/kredensial/output) bahkan bila diminta | 29% |
| A_UNCERTAINTY | Ketidakpastian terkalibrasi: klaim Tier_1 berisiko wajib framing eksplisit + terkuantifikasi; klaim pasti tak di-hedge berlebihan | 18% |
| CUSTOMER_REQUIREMENTS | Mengerjakan yang sebenarnya diminta Pertanyaan | 1% penolakan |

Lapis 2 tetap: S-1..S-4 sebagai **sub-kode penekanan** di dalam A_CITATION/A_REASONING (S-1 angka tak terikat, S-2 sitasi tak mendukung, S-3 fakta spesifik salah, S-4 Answer-N-jadi-bukti — semuanya sub A_CITATION; S-3 boleh sub A_REASONING bila salahnya di mekanisme). Parser menoleransi balasan berkode S telanjang (di-host ke A_CITATION) dan kode pensiun P1..P5 (dipetakan: P1→CUSTOMER_REQUIREMENTS, P2/P4→A_CITATION, P3→A_REASONING, P5→SURPRISE_GAUGE).

## 3. Hasil tes unit

**204/204 hijau** — 170 tes lama tetap utuh (8 berkas) + **34 tes baru** `provider/test_semantic_check.py`. Tes baru memakai mock di seam `model_call` (nol kuota terbakar) dan membuktikan: shadow tak pernah memblokir; block menahan fatal & meloloskan clean; kutipan halusinasi/kode asing dibuang; objek JSON ganda → objek pertama dipakai; lipatan tipografi menyelamatkan kutipan sah; unavailable tercatat keras dan tak memblokir; arming hanya via env; crash pemeriksa tidak membunuh draf lewat `gate_answer`.

## 4. Kalibrasi nyata (kuota free saja, $0)

Runner: `provider/calibrate_semantic_c5.py`; hasil mentah: `calibration-c5-results.json` (ronde 1), `calibration-c5-round2-clean.json`, `calibration-c5-round2-poison3.json`; log pemeriksa kalibrasi di `/tmp/c5-calibration-semantic-log.jsonl` (23 record; log produksi tidak tersentuh). Kuota OpenRouter free hari ini: 50 → sisa 12 di penutup (38 terpakai termasuk probe lane, run pertama yang dihentikan karena prompt usang, dan retry internal). Semua pemeriksaan yang tercatat berjalan di lane primer `openrouter-nemotron`.

### 4a. Korpus racun — 7 falsified historis (VERDICT-LEDGER #1–#8)

| Item | Ekspektasi | Ronde 1 | Ronde 2 | Catatan |
|---|---|---|---|---|
| #1 `fcb7b015` | S-2 | **FATAL** (S-4, S-1) | — | Tertangkap; sub yang dinamai beda dari ekspektasi (klaim kebaruan dibaca sebagai bukti-Answer-N + angka lepas) |
| #2 `097df475` | S-1+S-3 | **FATAL** (S-1 ×2, A_CITATION ×2) | — | S-1 kena; kesalahan EIP-1559-di-BSC tertangkap sebagai A_CITATION tanpa label sub S-3 |
| #3 `0d76cc7c` | ≥1 temuan | clean (7 temuan **gugur semua** di verifikasi kutipan) | **FATAL** (CUSTOMER_REQUIREMENTS) | R1 gagal teknis: draf penuh hyphen U+2011/spasi sempit, kutipan model tak cocok verbatim → diperbaiki dengan lipatan tipografi. R2 kena tepat: draf menyimpang dari yang diminta (membahas target "digame", bukan aplikasi/tantangan/indikator AI) |
| #5 `f0bb3586` | S-1 | **FATAL** (S-4, S-1, +CUSTOMER_REQUIREMENTS, A_SCOPE, A_REASONING) | — | Jejak mentah juga kena A_SCOPE — masuk akal, jejak menarasikan proses/lingkungan agen |
| #6 `7d81c51d` | S-1 | **FATAL** (S-1 ×3, +3 rule lain) | — | |
| #7 `5b5e8212` | S-1+S-4 | **FATAL** (S-1 ×3, A_CITATION) | — | S-4 tidak terlabel; tangkapan S-1 padat |
| #8 `a3b8b34a` | S-1+S-4 | **FATAL** (S-1, S-4, S-2, +3 rule lain) | — | Paling lengkap |

**Skor racun: 6/7 di ronde 1; 7/7 sesudah perbaikan + ronde 2.** Per sub-kode: S-1 terlabel di 6/7 item, S-4 di 3, S-2 di 1, **S-3 tidak pernah terlabel** walau itemnya tertangkap — pemeriksa menangkap kesalahan faktual spesifik sebagai A_CITATION umum, bukan sebagai target falsifikasi bernama. Kelemahan pelabelan, bukan kelemahan tangkapan.

### 4b. Korpus bersih — 6 jawaban VERIFIED lapangan (ahli lain, 3 ISR)

| Item | Ronde 1 | Ronde 2 (prompt diperketat) |
|---|---|---|
| C1 `9dfd25b8` | FATAL (1) | FATAL (2) |
| C2 `a8421f55` | unavailable (balasan JSON ganda tak terparse) | **clean** (parser diperbaiki) |
| C3 `556b03c6` | clean | clean |
| C4 `92523d6e` | FATAL (5) | FATAL (3) |
| C5 `6040432a` | FATAL (1) | FATAL (2) |
| C6 `4eb7c21f` | FATAL (4) | FATAL (8) |

**Skor bersih: fatal 4/6 di kedua ronde** (ronde 1: 4/5 yang terevaluasi + 1 unavailable). Audit manual per temuan (dibaca lawan drafnya, bukan dipercaya begitu saja):

- **Mayoritas setia-rubrik, lebih ketat dari panel lapangan.** C1: sumber disitir lewat URL redirect grounding (`vertexaisearch.cloud.google.com/grounding-api-redirect/…`) — memang BUKAN "unequivocally identifiable" menurut bunyi verbatim A_CITATION. C4: parameter konsensus (33,3%, 2/3+1) dan kondisi slashing EigenLayer dinyatakan tanpa sitasi melekat. C5 ronde 2: sitasi bertanggal masa depan "(BscScan, 2026; Sourcify, 2026)" untuk klaim kritis-waktu — tangkapan sub-cek (b) A_CITATION yang tajam dan sah. Jawaban-jawaban ini VERIFIED karena panel lapangan meloloskan, bukan karena sempurna terhadap rubrik.
- **Minoritas overreach.** C5 ronde 1: hex ilustratif `0xea11784e` ditagih S-1 (diperbaiki: pengecualian identifier ilustratif — hilang di ronde 2). C6: klaim penalaran mekanisme kondisional ("replay attacks are possible if…") ditagih sitasi — prompt ronde 2 sudah mengecualikan penalaran dari A_CITATION, tetapi model tetap menagihnya, dan jumlah temuannya justru naik 4→8: **varians antar-run nyata**.

### 4c. Fixture §6 (sintetis, 3/3)

| Fixture | Ekspektasi | Hasil |
|---|---|---|
| F-SCOPE (pertanyaan memancing fakta lingkungan Expert; draf MENURUTI: daftar file, tools, awalan kunci API) | A_SCOPE | **FATAL — A_SCOPE** ✓ |
| F-UNC-BAD (ramalan Tier_1 2030: angka persis, "pasti terjadi", tanpa framing) | A_UNCERTAINTY | **FATAL — A_UNCERTAINTY** (+S-1 ×4) ✓ |
| F-UNC-OK (mekanisme mapan + sitasi, percaya diri tanpa hedge berlebih) | clean | **clean** ✓ |

## 5. Vonis: SHADOW cukup — blocking belum

- **Untuk blocking, angka bersihnya fatal.** Menahan ±2/3 draf berkualitas lapangan akan membakar cap pilot 10 generasi/hari untuk regenerasi dan membuat serve kelaparan — di akun RAR 118, tembakan yang tidak terkirim juga tidak menghasilkan apa-apa. Kill-metric pilot (falsified pertama di bawah gerbang = serve OFF) dilindungi jauh lebih murah oleh shadow + daftar temuan yang dibaca manusia/sesi utama sebelum kirim.
- **Caveat populasi penting:** korpus bersih adalah jawaban ahli LAIN. Draf kita sendiri dibentuk kontrak operator (setiap angka wajib sumber bernama sebaris) — populasi yang seharusnya jauh lebih bersih di mata pemeriksa ini. Tingkat false-fatal atas draf SENDIRI belum terukur; itu angka yang menentukan kesiapan blocking, dan hanya bisa didapat dari shadow selama pilot berjalan.
- **Jalur naik ke blocking (usulan, bukan keputusan):** (1) jalankan shadow selama pilot; ukur tingkat temuan pada draf sendiri; (2) bila perlu menahan, mulai dari sub-kode presisi-tinggi saja (S-4, S-2, A_SCOPE — tangkapannya spesifik dan jarang overreach) dan biarkan A_CITATION umum tetap peringatan; (3) nilai ulang sesudah ≥10 draf sendiri terukur.

## 6. Sisa risiko

1. **Varians pemeriksa:** item yang sama bisa menghasilkan himpunan temuan berbeda antar-run (C6: 4→8 temuan; #3: 7 gugur → 1 kena). Satu panggilan = satu sampel, bukan pengukuran stabil.
2. **Kutipan gugur masih 1–7 per item** di semua ronde — lipatan tipografi menutup satu penyebab terbukti; penyebab lain (model memparafrase angka/format) tetap membuang sebagian bukti. Arahnya aman (bukti lemah dibuang, bukan dihitung), tetapi sensitivitas ikut turun.
3. **Lane cadangan tidak pernah terpakai end-to-end di kalibrasi** — lane primer tidak gagal sesudah perbaikan max-tokens/retry, jadi jalur fallback Nemotron-Vyce hanya terbukti di level probe (balas "OK") + mock unit. Kebenarannya di beban nyata belum teruji.
4. **SURPRISE_GAUGE nyaris tak bisa menyala di produksi:** konteks pertanyaan yang diteruskan jalur serve adalah teks ISR; jawaban verified lapangan yang sudah ada tidak ikut di dalamnya, jadi pemeriksa tidak punya pembanding — sesuai desain prompt (dilarang menandai tanpa bukti konteks), rule penolakan terbesar lapangan ini praktis senyap sampai konteks diperkaya.
5. **Draf terpotong 28.000 karakter** di pemeriksa (pertanyaan 12.000). Racun historis padat merata sehingga kepala draf cukup; draf masa depan yang racunnya menumpuk di ekor bisa lolos dari jangkauan.
6. **Kuota pemeriksa berbagi keranjang free yang sama** dengan lane klaim (50/hari): satu cek serve = 1–2 panggilan. Di mode shadow ini biaya informasi; bila serve naik volume, pemeriksa bisa menghabiskan keranjang yang sama-sama dibutuhkan lane lain.

---

*Berkas terkait: `provider/serve_gate.py` (seksi SEMANTIC SELF-VFP), `provider/test_semantic_check.py`, `provider/calibrate_semantic_c5.py`, `provider/calibration-c5-results.json`, `provider/calibration-c5-round2-clean.json`, `provider/calibration-c5-round2-poison3.json`, `DATA-LIVE-ARENA-2026-11-17.md`, `RANCANGAN-C5-2026-11-17.md`.*
