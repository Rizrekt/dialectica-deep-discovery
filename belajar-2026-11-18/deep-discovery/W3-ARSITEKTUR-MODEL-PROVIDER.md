# W3 — ARSITEKTUR MODEL & PROVIDER (Deep Discovery §3)

**Tanggal:** 2026-11-18 malam · **Sifat:** investigasi READ-ONLY — tidak ada config diubah, tidak ada API model dipanggil; semua klaim dari kode, doc connector, dan log yang sudah ada.
**Disiplin bukti:** `[KODE: file:fungsi]` = terbaca langsung di source · `[LOG]` = tercatat di log operasional · `[CONNECTOR-DOC]` = dokumen connector resmi workspace · `[TERVERIFIKASI]` = terbukti oleh kalibrasi/uji terdokumentasi · `[INFERENSI]` = simpulan penulis lini · `[HIPOTESIS]` = belum teruji.

---

## 1. Tabel kursi: model × fungsi × provider × jalur panggil × verifikasi

| # | Fungsi | Model aktif | Provider / transport | Jalur panggil persis | Status verifikasi |
|---|---|---|---|---|---|
| 1 | **Penulis utama (Answer)** | `glm-5.3-flash` (GLM, Zhipu) | Vyce (router OpenAI-compatible, `https://vyceai.com/v1`) | `trued serve` → prepare hook `vyce_serve_prepare.py` → `vyce_serve_common.generate_vyce()` → subprocess `vyce_provider.py` (prompt via stdin, jawaban via stdout) `[KODE: vyce_serve_common.py:generate_vyce; vyce_provider.py:main]` | [LOG] 19 record `lane=vyce-serve, model=glm-5.3-flash` di token-usage.jsonl; 5 jawaban pilot 17 Nov terkirim dari lane ini |
| 2 | **Penulis cadangan 1 (fallback rung 1)** | `gpt-oss-120b` | Vyce (provider sama, model dipin) | `WriterFallback` → `_generate_vyce_gptoss()` → `generate_vyce(model_chain="gpt-oss-120b")` → env `VYCE_MODEL_CHAIN` ke subprocess yang sama `[KODE: vyce_serve_common.py:_generate_vyce_gptoss, VYCE_GPTOSS_CHAIN]` | [LOG] 6 record `lane=vyce-serve, model=gpt-oss-120b` — rung ini **pernah benar-benar menyala di serve produksi**; [TERVERIFIKASI] probe live + draf lolos gerbang 2026-11-17 (R1) |
| 3 | **Penulis cadangan 2 (fallback rung 2)** | `@cf/openai/gpt-oss-120b` | Cloudflare Workers AI (connector client `run`) | `WriterFallback` → `_generate_cloudflare_gptoss()` → `cloudflare_provider.generate()` (budget neuron dicek SEBELUM bakar) `[KODE: vyce_serve_common.py:_generate_cloudflare_gptoss; cloudflare_provider.py:generate]` | [LOG] 51 record `lane=cloudflare-gptoss` (lane §39 historis); di rantai R1 terbukti lewat uji kering 17 Nov |
| 4 | **Pemeriksa utama (Review/Fact-check semantik, "C5")** | `nvidia/nemotron-3-ultra-550b-a55b:free` (Nemotron 3 Ultra) | OpenRouter (connector client `chat`) | `serve_gate.semantic_check()` → `default_semantic_model_call()` → `_semantic_call_openrouter()` (probe kuota `key` dulu; sisa <2 = lane dinyatakan unavailable) `[KODE: serve_gate.py:SEMANTIC_PRIMARY_MODEL, _semantic_call_openrouter, default_semantic_model_call]` | [TERVERIFIKASI] kalibrasi: racun **7/7**, salah-fatal 4/6 (KALIBRASI-C5-2026-11-17); [LOG] 17 record semantic-check-log `checker=openrouter-nemotron` |
| 5 | **Pemeriksa utama — lane cadangan internal** | `nemotron-3.5-super-vl` (Nemotron via Vyce) | Vyce (panggilan in-process `vyce_provider.call_vyce`) | `default_semantic_model_call()` lane ke-2: `_semantic_call_vyce()` `[KODE: serve_gate.py:SEMANTIC_FALLBACK_MODEL, _semantic_call_vyce]` | [LOG] 8+4 record token-usage `model=nemotron-3.5-super-vl`; dikenal cacat pada draf raksasa (reasoning overflow → content kosong) sehingga pemeriksa utama memakai **segmentasi** draf >10.000 kar `[KODE: serve_gate.py:_split_draft_segments]` |
| 6 | **Pemeriksa cadangan rantai (lapis 2)** | `qwen-3.8-max:free` (Qwen) | CrowLLM relay (connector client `chat`, prompt PUBLIK) | `serve_gate.chained_semantic_check()` → `crowllm_checker.check_public(BACKUP_MODEL)` — menyala HANYA bila utama unavailable ATAU utama clean `[KODE: crowllm_checker.py:BACKUP_MODEL, check_public; serve_gate.py:chained_semantic_check]` | [TERVERIFIKASI] kalibrasi prompt publik: racun **6/7**, salah-fatal **2/6** (UJI-CROWLLM-PEMERIKSA-2026-11-17) |
| 7 | **Penengah sengketa + cadangan kedua (lapis 3)** | `gpt-5.6-sol:free` | CrowLLM relay (prompt PUBLIK) | `chained_semantic_check()` → `check_public(ARBITER_MODEL)` — memutus sengketa utama-clean vs cadangan-FATAL (2-dari-3); juga bertugas sebagai cadangan kedua bila qwen mati `[KODE: crowllm_checker.py:ARBITER_MODEL; serve_gate.py:chained_semantic_check aturan 3–4]` | [TERVERIFIKASI] kalibrasi: racun **5/7**, salah-fatal **2/6** |
| 8 | **Fact-check isi tahap 2 (entailment)** | Nemotron (lane pemeriksa utama yang sama, #4/#5) | OpenRouter → Vyce | `content_verify.default_entailment_call()` → `serve_gate.default_semantic_model_call()` `[KODE: content_verify.py:default_entailment_call]` | [TERVERIFIKASI] tes content_verify 46/46; tahap 1-nya mekanis murni (token hadir di sumber ter-fetch), tanpa model |
| 9 | **Pemeriksa lapis 4 (gpt-oss Cloudflare) — BELUM TERPASANG** | `@cf/openai/gpt-oss-120b` sebagai pemeriksa | Cloudflare | **Tidak ada di kode rantai.** `chained_semantic_check` hanya mengenal utama + qwen + sol `[KODE: serve_gate.py:chained_semantic_check — tidak ada rujukan gpt-oss]` | [TERVERIFIKASI] kalibrasi pemeriksa: racun **7/7**, salah-fatal **4/6** (calibration-c5-gptoss-results.json) — tersertifikasi, menunggu keputusan pemasangan user |
| 10 | **Penulis penantang (pernah diuji, GUGUR sebagai penulis)** | qwen-3.8-max (via CrowLLM) | CrowLLM | Hanya pernah jalan di uji penentu penulis 17 Nov, bukan di pipa produksi | [TERVERIFIKASI] babak apparatus: 8/13 sitasi karangan (61,5%) → gugur sebagai penulis; kursinya dipindah ke pemeriksa (#6) |
| 11 | **Lane penantang/arsip (tidak aktif di serve)** | deepseek-v4-pro (DashScope), glm-4.7-flash (Z.ai), Nemotron (OpenRouter sbg penulis §35), gpt-oss (Cloudflare sbg penulis §39) | DashScope / Z.ai / OpenRouter / Cloudflare | `run_serve.py --dashscope / --zai / --openrouter / --cloudflare` — **answer one-shot saja**; serve latar di lane ini ditolak run_serve (exit 5) `[KODE: dashscope_provider.py & zai_provider.py header; run_serve.py]` | [LOG] token-usage: dashscope 3 record, zai 1 record (bench/claim historis); deepseek-v4.1 via Vyce **dihapus dari rantai 17 Nov** — route-nya 403 lite-tier `[KODE: vyce_provider.py:candidate_models]` |
| 12 | **Konsultasi frontier (di luar pipa serve)** | duck.ai (GPT-6 Luna) utama; gpt-5.6-sol co-advisor; gemini-3.1-pro penengah | Browser cloud (duck) / CrowLLM (sol, gemini) | Manual oleh sesi utama per paket konsultasi — BUKAN bagian pipa jawaban | [TERVERIFIKASI] beberapa paket konsultasi 18 Nov konvergen; malam 18 Nov kedua kursi CrowLLM mati (lihat §6) |
| 13 | **DILARANG / mati** | Gemini direct free-tier; Sonogami Router untuk Dialectica; deepseek-v4.1 via Vyce | — | Grounding Gemini di dalam `vyce_provider.py` **MATI secara bawaan** (env `DIALECTICA_GEMINI_GROUNDING=1` untuk menghidupkan, keputusan sesi utama) `[KODE: vyce_provider.py:main]`; Sonogami: "Never use it for Dialectica" `[CONNECTOR-DOC: custom.sonogami-router]` | [KODE]/[CONNECTOR-DOC] |

**Catatan kursi:** tidak ada fungsi "Research" bermodel tersendiri di pipa. Yang menyerupai riset bersifat deterministik: blok konteks kebaruan (jawaban verified yang sudah ada, ditarik dari API platform oleh `novelty_context.py`, tanpa model) + pengambilan isi sumber oleh fetcher `citation_verify/content_verify` (HTTP biasa). Model hanya muncul di tiga titik: **menulis**, **memeriksa semantik**, **menilai entailment isi**. `[KODE: novelty_context.py; content_verify.py]`

---

## 2. Bagaimana pemanggilan bekerja (per jalur)

- **Penulis (Vyce):** kontrak provider klien stok — prompt masuk lewat **stdin**, hanya jawaban keluar lewat **stdout**, diagnostik ke stderr. Streaming SSE, `max_tokens 12000`, timeout 240 dtk per panggilan, backoff 15/30/60 dtk hanya untuk HTTP 429/503, maks 4 percobaan per model. Kunci API tidak pernah ada di file/argv: launcher menyuntikkan env `VYCE_API_KEY` dari vault surrogate. `[KODE: vyce_provider.py:call_vyce, main]`
- **Pemeriksa utama (OpenRouter):** subprocess klien connector resmi; prompt ditulis ke **file sementara** (tidak lewat argv). Sebelum panggilan berbayar-kuota, klien `key` diprobe gratis: sisa kuota free harian **< 2 → lane menyerah sukarela** agar cadangan darurat tidak terbakar. `[KODE: serve_gate.py:_semantic_call_openrouter]`
- **Lane relay (CrowLLM):** subprocess klien connector, prompt via file temp, `--max-tokens 4000`; **pacing keras ≥13 detik antar awal panggilan** (anggaran 5 req/menit dibagi SEMUA proyek), retry maks 2 hanya pada 429/500/503/524, 524 → percobaan berikut streaming. `[KODE: crowllm_checker.py:_pace, _call_with_retries, _client_transport]`
- **Penulis Cloudflare:** klien connector `run --model @cf/openai/gpt-oss-120b`; total neuron hari-UTC dihitung dari token-usage.jsonl SEBELUM generasi; di atas 9.000 neuron generasi **dibatalkan sebelum bakar** (cap platform 10.000, cadangan aman 1.000). `[KODE: cloudflare_provider.py:generate, NEURON_ABORT_ABOVE]`

## 3. Routing model — ada atau tidak?

**Jawaban tegas: TIDAK ada routing per-pertanyaan/per-topik.** Setiap Question yang masuk pipa serve ditulis oleh model yang sama (GLM via Vyce), diperiksa oleh susunan pemeriksa yang sama. Yang ada adalah routing **per-fungsi** (penulis ≠ pemeriksa ≠ penengah — tabel §1) dan routing **per-kelas target** yang hanya mengubah *lantai panjang*, bukan model: kelas dari picker (PIONEER 1.717 kar / umum 3.000 / MARATHON 4.500, pita patokan s/d 10–12 rb) masuk ke wrapper sebagai `target_class`. `[KODE: openrouter_wrapper.py:length_floor_for_class; vyce_serve_common.py:vyce_pipeline(target_class)]`

Satu-satunya penyesuaian per-pekerjaan yang bersifat isi adalah **steering operator**: file `steering/<isr_id>.txt` yang disiapkan operator ditempel ke prompt untuk ISR itu (sudut pandang dipilih operator, bukan model). Itu routing *prompt*, bukan routing *model*. `[KODE: vyce_provider.py:main — blok STEERING]`

**Bisa-kah model berbeda untuk Research/Answer/Review/Fact-check?**
- **Sudah terpasang:** Answer (GLM) ≠ Review (Nemotron) ≠ Fact-check semantik (rantai qwen/sol) ≠ Fact-check isi (mekanis + Nemotron entailment). Empat fungsi, tiga keluarga model berbeda. `[KODE — tabel §1]`
- **Mungkin tapi BELUM terpasang:** Research bermodel (tidak ada komponennya sama sekali); pemilihan penulis per topik/kelas (tidak ada kode pemilih model per pertanyaan — `candidate_models()` hanya membaca env); pemeriksa lapis 4 gpt-oss-CF (tersertifikasi, tidak ter-wire). `[KODE: vyce_provider.py:candidate_models; serve_gate.py:chained_semantic_check]`
- Model pemeriksa rantai **bisa** diganti lewat env (`DIALECTICA_CHAIN_BACKUP_MODEL`, `DIALECTICA_CHAIN_ARBITER_MODEL`, `DIALECTICA_SEMANTIC_MODEL`, `DIALECTICA_SEMANTIC_FALLBACK_MODEL`, `VYCE_MODEL`, `VYCE_MODEL_CHAIN`, `CLOUDFLARE_MODEL`) — tetapi dokumen rantai menegaskan: mengganti model = mengganti lane tersertifikasi, **wajib kalibrasi ulang dulu**. `[KODE: crowllm_checker.py; serve_gate.py; RANTAI-PEMERIKSA-2026-11-18.md §1]`

## 4. Kerja paralel model — TIDAK ADA di pipa produksi

Tidak ada `ThreadPool/asyncio/concurrent/multiprocessing` di seluruh file provider non-tes `[KODE: grep menyeluruh provider/*.py — nol hasil]`. Semua rantai berjalan **sekuensial**: rantai penulis berjalan satu lane pada satu waktu; rantai pemeriksa memanggil utama → cadangan → penengah satu per satu (memang harus, karena aturan menyalanya bergantung pada vonis sebelumnya); serve sendiri dibatasi `maxConcurrency 1` di konfigurasi Expert server. Multi-model di sistem ini berarti **estafet**, bukan balapan. Konsekuensi terukur: satu cek rantai penuh bisa menambah ±15–40 detik per draf (latensi kalibrasi: qwen 2,5 dtk, sol 12,0 dtk, belum termasuk pacing 13 dtk antar panggilan relay). `[KODE; RANTAI-PEMERIKSA-2026-11-18.md §1]`

## 5. Bagaimana hasil multi-model digabungkan (rantai pemeriksa)

Penggabungan BUKAN rata-rata skor — ini mesin vonis beraturan, persisnya `[KODE: serve_gate.py:chained_semantic_check]`:

1. **Utama FATAL (tersedia) = FINAL.** Nol panggilan relay dibakar. (Veto satu arah: fatal yang berkuotasi terverifikasi adalah arah meyakinkan.)
2. **Cadangan (qwen) menyala hanya bila** utama *unavailable* (transport mati/luapan konteks) **atau** utama *clean* (satu clean = satu sampel, bukan pembebasan → wajib sampel kedua independen).
3. **Sengketa** (utama clean vs qwen FATAL) → **penengah (sol) memutus, 2-dari-3**: sol FATAL → rantai FATAL dengan temuan qwen yang berlaku; sol clean → clean utama pulih.
4. **Kaskade mati:** qwen mati → sol bertugas langsung sebagai cadangan kedua. Sol mati di tengah sengketa → vonis utama **berdiri**, sengketa dicatat `dispute_unresolved: true` + temuan yang disengketakan disimpan di record log, **tidak memblokir**.
5. **Semua lane mati:** hasil utama yang *unavailable* dikembalikan apa adanya — `performed=False, block=False` di semua mode. Draf **tidak** dinyatakan clean dan **tidak** ditahan oleh tahap ini; kegagalannya bersuara (peringatan stderr + record log menamai kegagalan tiap lane).

Disiplin bukti di dalam lane relay: vonis FATAL hanya sah bila ≥1 temuan yang **kutipannya terverifikasi verbatim** (normalisasi spasi) terhadap draf; FATAL yang semua temuannya gugur terdegradasi menjadi CLEAN; balasan tak terparse = *unavailable* (kegagalan lane, bukan vonis). `[KODE: crowllm_checker.py:verify_public_findings, check_public]`

Mode menggigitnya: rantai hanya menahan draf bila mode semantik `block` DAN vonis akhir fatal; mode bawaan warisan adalah `shadow` (catat saja). Pada nyala-nyala terakhir rantai berjalan di atas mode warisan shadow. `[KODE: serve_gate.py:semantic_mode; konteks nyala sesi utama]`

## 6. Bisakah hasil model diteruskan ke Dialectica TANPA diubah substansinya?

**Tidak — dan memang sengaja tidak.** Ada lapisan mekanis di antara model dan pengiriman, dengan bukti kode:

| Lapisan | Yang diubah | Bukti |
|---|---|---|
| `citation_patch.clean()` v2 (di dalam vyce_provider, semua jalur keluar) | Hampir tidak mengubah apa-apa secara desain: sitasi **dipertahankan**; hanya menghapus catatan warisan v1 (penutup evasif E3) + karakter zero-width | `[KODE: lib/citation_patch.py — docstring v2]` |
| `_format_gate()` (vyce_provider, hanya bila prompt menuntut JSON) | Mengekstrak objek JSON terluar, membuang prosa/fence pembungkus GLM, menormalisasi `confidence` 0–1 → persen | `[KODE: vyce_provider.py:_format_gate]` |
| `wrap_answer()` (wrapper wajib semua lane, dipanggil `gate_answer`) | (a) normalisasi mojibake; (b) **regenerasi panjang** — draf di bawah lantai kelas ditulis ulang oleh model dengan instruksi ekspansi (maks 1×); (c) **audit angka/sitasi: angka yang terikat dokumen bernama dengan nilai salah/tak terverifikasi DIHAPUS token-per-token — tidak pernah diganti nilai karangan**; (d) lantai mekanis K-1/K-2 (URL ≥1, densitas sitasi, rasio angka-terikat ≥0,30) — gagal = draf ditahan, bukan diedit lolos | `[KODE: openrouter_wrapper.py:wrap_answer, audit_numbers, mechanical_floor; serve_gate.py:gate_answer]` |
| Pagar keras di vyce_provider | Content kosong (model hanya mengeluarkan reasoning) = **kegagalan generasi**, reasoning_content dibuang — tidak pernah dikirim sebagai jawaban (spesies falsified f0bb3586) | `[KODE: vyce_provider.py:call_vyce]` |

Jadi yang dipertahankan utuh adalah **substansi argumen model**; yang dibuang/diedit adalah token angka yang terbukti salah ikat, cacat encoding, dan bungkus format. Tidak ada parafrase model-ke-model: tidak ada lane yang menulis ulang draf lane lain — pemeriksa hanya memvonis (FATAL/CLEAN + temuan), tidak pernah menyunting teks. `[KODE: serve_gate.py — semantic_check mengembalikan vonis+temuan, bukan teks]`

## 7. Verifiabilitas dari log — apa yang BISA dan TIDAK BISA dibuktikan

**`token-usage.jsonl`** (197 record s/d malam ini) — satu baris per panggilan model yang selesai, field: `ts` (UTC), `model` (**nama model yang DIMINTA**, string dari kode kita), `lane` (label jalur: `vyce-serve`, `vyce-direct`, `cloudflare-gptoss`, `openrouter-nemotron`, `dashscope-deepseekpro`, `zai-glm47flash`, …), `isr` (id pertanyaan, bisa null), `usage` (objek dari provider: `prompt_tokens`, `completion_tokens`, `total_tokens`; Cloudflare menambah `neurons`; OpenRouter menambah `cost` — tercatat **0** karena tier free), `answer_chars`; record Cloudflare juga `neurons_today_after`, record OpenRouter `quota_remaining_after`. `[LOG: token-usage.jsonl]`

**`semantic-check-log.jsonl`** — per cek: `checker` (label lane pemutus, mis. `openrouter-nemotron`, atau gabungan `utama+qwen+sol` bila rantai memutuskan), `verdict`, `model_verdict`, `findings` (dengan kutipan), `segments`, dan bila rantai aktif blok `chain{lanes[], dispute, dispute_unresolved, decided_by}`. `[LOG: semantic-check-log.jsonl — 17 record checker utama, 8 record berbungkus chain]`

**Yang BISA diverifikasi dari log:**
- Model apa yang *diminta* tiap panggilan, untuk ISR apa, berapa token/neuron, dan lane mana yang memutus tiap vonis pemeriksa — termasuk bukti fallback penulis pernah menyala (6 record gpt-oss di `vyce-serve`). `[LOG]`
- Kegagalan generasi yang tercatat: generasi yang gagal total **tidak menulis record** (kasus 18 Nov: token-usage tetap 197 baris sebelum/sesudah — kegagalan hanya terlihat di log serve/journal, bukan di log usage). `[LOG: UJI-1-TEMBAKAN-2026-11-18.md §timeline]`

**Yang TIDAK BISA diverifikasi dari log (klaim yang harus ditolak bila muncul):**
1. **Identitas model di balik router tidak teratestasi.** Untuk Vyce, yang tercatat adalah nama model yang kita kirim; potongan stream tidak menyimpan field model-balasan yang diverifikasi kode. Router *bisa* secara teknis menyajikan model lain dan log kita tidak akan tahu. `[KODE: vyce_provider.py:_log_usage — mencatat parameter `model` dari pemanggil]` — Untuk CrowLLM lebih baik: klien mengembalikan `model_returned` dan attempts-log rantai mencatatnya per percobaan `[KODE: crowllm_checker.py:_call_with_retries]`, tetapi attempts itu hidup di record rantai, bukan di token-usage.
2. **Biaya uang per panggilan tidak tercatat di mana pun** kecuali `cost: 0` bawaan usage OpenRouter. Tidak ada field biaya $ untuk Vyce/CrowLLM/Cloudflare (neuron ≠ dolar), dan runner verifier Jalur 2 juga belum punya field biaya per verdict (kekurangan tercatat di peta Jalur 2). Titik impas ekonomi per jawaban **tidak bisa dihitung dari log yang ada** — hanya bisa dari token × tarif eksternal. `[LOG: token-usage.jsonl — absennya field]`
3. **Alasan gugur tautan tengah rantai penulis tidak selalu tercatat di log serve** (lihat §8 kasus 18 Nov): transisi fallback dicetak ke **stderr proses prepare** (`fallback: <lane> gagal → <lane>`) — di jalan systemd ia masuk journal unit, bukan file serve-*.log; grep di serve-2026-11-17.log dan serve-2026-11-18.log menemukan **nol** baris `fallback:` padahal log uji kering R1 membuktikan formatnya bekerja. `[LOG: r1-fallback-drytest-2026-11-17.json memuat fallback_log; serve-2026-11-1{7,8}.log tidak]`

## 8. FALLBACK & RISIKO PERGANTIAN SENYAP (pertanyaan kunci user)

### 8.1 Rantai penulis R1 — persisnya

```
Vyce/GLM (glm-5.3-flash)  →  Vyce gpt-oss-120b (pin VYCE_MODEL_CHAIN)  →  Cloudflare gpt-oss-120b (@cf/openai/gpt-oss-120b)
```
- Stateful di dalam satu run pipa: generasi mulai dari lane terakhir yang berhasil; kegagalan TOTAL satu lane (kosong/error sesudah retry internal provider-nya sendiri) menyerahkan **prompt yang sama** ke lane berikut; draf yang selamat melewati gerbang yang identik. `[KODE: vyce_serve_common.py:WriterFallback.__call__, docstring R1]`
- Di dalam provider Vyce sendiri ada rantai mini: daftar kandidat `candidate_models()` — sejak 17 Nov hanya **satu** model bawaan (GLM); deepseek-v4.1 dibuang karena route 403. Jadi "fallback di dalam Vyce" praktis tidak ada lagi; semua fallback lintas-provider hidup di WriterFallback. `[KODE: vyce_provider.py:candidate_models]`
- Rantai bisa dimatikan total: `DIALECTICA_WRITER_FALLBACK=0` mengembalikan perilaku lama (kegagalan Vyce = target dilewati). Bawaan = menyala. `[KODE: vyce_serve_common.py:writer_fallback_enabled]`
- Rantai pemeriksa punya kaskade sendiri (§5 butir 4) dan pemeriksa utama punya fallback internal OpenRouter→Vyce (§1 #5): total **tiga** mekanisme fallback independen di sistem.

### 8.2 Apakah fallback bisa mengganti model TANPA sepengetahuan user?

**Ya — secara desain memang begitu cara kerjanya, dengan tiga pagar pencatatan dan satu celah nyata:**

- **Yang terjadi:** bila GLM runtuh (spesies nyatanya: content kosong sesudah reasoning overflow — stokastik, pernah membunuh generasi), pipa **otomatis** menulis jawaban dengan gpt-oss-120b (Vyce, lalu Cloudflare) dan jawaban itu **dikirim ke Dialectica sebagai jawaban AGENT.AkTa tanpa persetujuan per-kejadian dari user**. User menyetujui *mekanismenya* saat pemasangan R1 (17 Nov), bukan tiap pergantiannya. Tidak ada notifikasi real-time; pergantian terlihat sesudahnya dari (a) baris stderr `fallback: …` dan (b) record token-usage berlabel model pengganti. `[KODE: vyce_serve_common.py:WriterFallback; LOG: 6 record vyce-serve/gpt-oss-120b]`
- **Pagarnya:** (1) model pengganti bukan model acak — dua rung tetap, keduanya **diuji live + lolos gerbang sebelum dipasang** (aturan putus R1); (2) draf pengganti melewati **gerbang mutu yang sama persis** — yang berganti hanya penulisnya, bukan standarnya; (3) setiap generasi pengganti tercatat di token-usage dengan nama modelnya, jadi audit sesudah-kejadian selalu bisa membuktikan jawaban mana ditulis model mana. `[KODE; LOG]`
- **Celah nyata (wajib diakui):** pencatatan transisi di log serve tidak lengkap — kasus 18 Nov malam (§8.3) alasan gugur dua tautan pertama **tidak tercatat** di log serve; yang tersisa hanya error terminal. Dan di jalur klaim one-shot lama, provider langsung (`vyce_provider.py` tanpa lane) mencetak peringatan S1 bahwa stdout-nya terkirim **tanpa wrapper/gerbang** — jalur itu STOP total saat ini, tetapi pagarnya hanya peringatan stderr + disiplin operator, bukan kunci kode. `[KODE: vyce_provider.py — blok AUDIT S1 FENCE; LOG: UJI-1-TEMBAKAN-2026-11-18.md butir 3]`
- **Risiko senyap kedua — di dalam provider:** `_format_gate` dan `citation_patch` berjalan di dalam proses provider; keduanya tercatat hanya sebagai baris stderr. Tidak ada record terstruktur "draf ini diubah lapisan X sebanyak Y token" di token-usage. `[KODE: vyce_provider.py:main]`
- **Yang TIDAK pernah terjadi diam-diam:** penggantian model *pemeriksa* — model rantai memang bisa diganti lewat env, tetapi env hanya disetel launcher saat nyala (keputusan sesi utama/user), tidak pernah oleh kode di tengah jalan; dan prompt publik relay byte-identik dengan rezim kalibrasi — mengubahnya = lane tak tersertifikasi. `[KODE: crowllm_checker.py:PUBLIC_PROMPT; run_serve.py arming env]`

### 8.3 Kasus nyata: neuron habis, 18 Nov malam — kenapa rantai tidak menyelamatkan

Kronologi terbukti `[LOG: serve-2026-11-18.log baris ±450; UJI-1-TEMBAKAN-2026-11-18.md]`:

1. Tiket `b1a89a69` lolos semua gerbang pra-klaim; generasi dicoba ±2 menit.
2. Error terminal yang tercatat: lane Cloudflare **429 "you have used up your daily free allocation of 10,000 neurons"** — alokasi hari itu **sudah habis sejak pagi** (kalibrasi pemeriksa gpt-oss-CF ±4.786 neuron + fallback pagi; error terminal yang sama sudah muncul 03:20 pagi itu).
3. Karena error terminal berasal dari **rung terakhir**, rantai memang berjalan sampai ujung: dua tautan sebelumnya (GLM, gpt-oss-Vyce) tidak menghasilkan draf — **tetapi alasan gugurnya tidak tercatat di log serve** (celah §8.2). Yang pasti: tidak ada draf, tidak ada klaim, counter generasi tetap 9/10 (generasi gagal tidak tercatat di token-usage).

**Kenapa rantai secara struktural tidak bisa menyelamatkan kasus ini** `[INFERENSI dari KODE+LOG]`:
- Rung 1 dan 2 berbagi **satu provider** (Vyce) — kegagalan tingkat-provider (sesi/kuota/rute) menjatuhkan dua rung sekaligus; diversifikasi rantai sebenarnya hanya 2 provider, bukan 3.
- Rung 3 bergantung pada **anggaran harian bersama** (neuron Cloudflare) yang pada hari itu sudah dikonsumsi pekerjaan lain (kalibrasi) — rantai tidak punya anggaran cadangan yang dikunci untuk serve; pemeriksa `cloudflare_provider.generate` memang menolak SEBELUM bakar bila total >9.000, tetapi pada titik itu penolakan = kegagalan generasi juga.
- Rantai dirancang untuk kegagalan **model** (GLM runtuh stokastik), bukan kegagalan **bahan bakar bersama**. Obat yang tercatat di berkas uji: status neuron + kesehatan GLM menjadi butir pra-terbang menentukan sebelum nyala berikutnya — pencegahan, bukan fallback tambahan. `[LOG: UJI-1-TEMBAKAN-2026-11-18.md butir 3]`

## 9. Batasan teknis per lane

| Lane | Batasan keras | Bukti |
|---|---|---|
| Cloudflare Workers AI | **10.000 neuron/hari** (reset 00:00 UTC), bersama untuk semua pemakaian akun; kode berhenti di >9.000; ±128 neuron per generasi kelas-klaim terukur; kalibrasi satu hari bisa memakan ±4.786 | `[CONNECTOR-DOC: custom.cloudflare-workers-ai]` `[KODE: cloudflare_provider.py]` `[LOG: 18 Nov]` |
| CrowLLM | **5 req/menit per akun, DIBAGI semua proyek** → pacing kode 13 dtk; relay operator tunggal, bisa mati sewaktu-waktu; sapuan 18 Nov malam: **21 hidup / 41 mati dari 62 model** — Gemini mati total 12/12, OpenAI arus utama mati total (termasuk dua kursi kita: gpt-5.6-sol 503, gemini-3.1-pro mati), Nemotron hidup 5/5, qwen-3.8-max **503** (qwen kecil hidup) | `[KODE: crowllm_checker.py:PACE_S]` `[LOG: CROWLLM-LIVENESS-2026-11-18.md]` |
| OpenRouter (free) | Kuota request harian tier free; percobaan gagal ikut terhitung; sisa kuota diperlakukan sebagai **cadangan darurat**: pemeriksa utama menyerah sukarela pada sisa <2 agar tidak terbakar. Sisa live terakhir terbaca sesi utama = **1** → pada keadaan itu lane pemeriksa utama praktis selalu unavailable dan beban pindah ke lane Vyce-Nemotron | `[CONNECTOR-DOC: custom.openrouter]` `[KODE: serve_gate.py:_semantic_call_openrouter]` |
| Vyce | Router pihak ketiga; sesi/kunci lewat vault surrogate; model katalog bisa berubah status diam-diam (deepseek-v4.1 → 403 lite-tier); GLM runtuh stokastik (content kosong); timeout 240 dtk/panggilan, subprocess generasi dicap 1.200 dtk | `[KODE: vyce_provider.py; vyce_serve_common.py:GEN_TIMEOUT_S]` |
| Gemini | **Direct free-tier DILARANG** (aturan user); via CrowLLM boleh tetapi kolam Gemini mati total pada sapuan 18 Nov; grounding internal di vyce_provider mati secara bawaan (membakar ±20× kuota per panggilan + latensi s/d 300 dtk saat pernah aktif) | `[KODE: vyce_provider.py — blok grounding]` `[LOG: CROWLLM-LIVENESS-2026-11-18.md]` |
| NVIDIA NIM | Trial Terms: hanya prototyping/evaluasi, **bukan produksi**; prompt dapat dipakai NVIDIA — lane ini TIDAK dipakai pipa Dialectica (Nemotron kita datang via OpenRouter/Vyce/CrowLLM, bukan NIM langsung) | `[CONNECTOR-DOC: custom.nvidia-nim]` |
| Z.ai / DashScope | Lane cadangan bersyarat: pool free Z.ai jenuh (429/1305), kapasitas harian tak terpublikasi; DashScope tidak punya bacaan nol-biaya (setiap probe membakar stok kuota workspace) | `[KODE: zai_provider.py header]` `[CONNECTOR-DOC: custom.alibaba-dashscope]` |
| Serve (platform) | Cap generasi serve **10/hari-UTC terkunci di kode** (dihitung dari record `lane=vyce-serve`); `maxConcurrency 1`; satu pipa maks 2 generasi (1 + 1 regenerasi panjang) | `[KODE: vyce_serve_common.py:SERVE_GEN_CAP, PIPELINE_MAX_GENERATIONS]` |

## 10. Jawaban ringkas atas pertanyaan §3 user, satu per satu

1. **Model apa yang dipakai sekarang?** Penulis GLM-5.3-flash (Vyce); cadangan penulis gpt-oss-120b (Vyce → Cloudflare); pemeriksa utama Nemotron-3-Ultra (OpenRouter, cadangan internal Nemotron-3.5-super-vl via Vyce); pemeriksa rantai qwen-3.8-max + penengah gpt-5.6-sol (CrowLLM). Tabel §1.
2. **Bagaimana dipanggil?** Semua lewat klien connector resmi/provider lokal sebagai subprocess (prompt via stdin/file temp, tidak pernah argv), kunci dari vault surrogate via env. §2.
3. **Ada routing model?** Per-fungsi YA; per-pertanyaan/topik TIDAK; per-kelas hanya lantai panjang. §3.
4. **Setiap Question selalu model sama?** Ya untuk penulis (GLM), kecuali fallback R1 menyala — tercatat di log usage per record.
5. **Bisa model berbeda per Research/Answer/Review/Fact-check?** Answer/Review/Fact-check sudah berbeda model. Research bermodel tidak ada (konteks riset deterministik). Pemilihan penulis per pertanyaan: belum ada kodenya.
6. **Bisa paralel?** Tidak di pipa produksi — semua sekuensial; tidak ada primitif konkurensi di kode provider.
7. **Penggabungan multi-model?** Rantai pemeriksa: veto fatal utama, sampel kedua wajib untuk clean, arbitrase 2-dari-3 oleh penengah, `dispute_unresolved` tercatat bila penengah mati. §5.
8. **Hasil model spesialis diteruskan tanpa diubah?** Tidak — lapisan mekanis membuang angka salah-ikat, memperbaiki encoding/format, dan bisa memicu regenerasi; substansi argumen tidak diparafrase lane lain. §6.
9. **Provider eksternal?** Ya: Vyce, OpenRouter, Cloudflare, CrowLLM aktif; Z.ai/DashScope terpasang untuk klaim one-shot; NIM/Sonogami tidak dipakai untuk Dialectica.
10. **Terverifikasi dari log?** Sebagian: nama model yang diminta + lane + token/neuron per panggilan tercatat; identitas model di balik router TIDAK teratestasi; biaya $ tidak tercatat. §7.
11. **Fallback otomatis?** Ya, tiga mekanisme (penulis R1, pemeriksa utama, rantai pemeriksa). §8.1.
12. **Fallback mengganti model tanpa sepengetahuan user?** **Ya, per desain yang user setujui saat pemasangan** — tanpa persetujuan per-kejadian dan tanpa notifikasi real-time; tercatat sesudahnya di token-usage + stderr, dengan satu celah pencatatan transisi di log serve (kasus 18 Nov). §8.2–8.3.
13. **Batasan teknis yang membuat model tertentu tak bisa dipakai?** Kuota neuron Cloudflare, pacing + kematian kolam CrowLLM, cadangan darurat OpenRouter, larangan Gemini direct, route mati Vyce (deepseek), Trial Terms NIM. §9.

---

*Akhir lini W3. Temuan yang butuh keputusan user (bukan wewenang lini ini): pemasangan pemeriksa lapis 4 gpt-oss-CF; penutupan celah pencatatan transisi fallback di log serve; apakah diversifikasi rantai penulis perlu provider ketiga yang sungguh independen; penguncian anggaran neuron untuk serve vs kalibrasi.*
