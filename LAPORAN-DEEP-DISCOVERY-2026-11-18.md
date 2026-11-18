# LAPORAN DEEP DISCOVERY — SISTEM OPERASI AGENT.AkTa DI DIALECTICA

**Tanggal:** 18 November 2026 (investigasi 23:38–23:5x WIB) · **Perintah:** user, eksplisit — investigasi mendalam TANPA implementasi.
**Batasan yang dipatuhi:** read-only mutlak. Tidak ada konfigurasi diubah, tidak ada model diganti, tidak ada strategi diubah, tidak ada Question dibuat, tidak ada pekerjaan earning baru, tidak ada kredit dibeli, tidak ada Expert tambahan, tidak ada pengujian berbayar, tidak ada Answer dikirim, tidak ada submission. Temuan yang perlu perbaikan hanya dilaporkan.
**Metode:** 5 lini bedah paralel atas source code, konfigurasi, log operasional, dan berkas pengalaman proyek + 1 kursi frontier independen (duck.ai, peran AUDITOR — bukan pemeta) + verifikasi live read-only oleh sesi utama. Klaim diberi label: **[TERVERIFIKASI]** terbukti dari kode/log/API primer · **[DOKUMENTASI RESMI]** dari SKILL.md/dokumen platform · **[PENGALAMAN]** kejadian operasional nyata · **[INFERENSI]** simpulan beralasan dari bukti · **[HIPOTESIS]** belum teruji.
**Lampiran bukti (pendamping laporan ini, folder `belajar-2026-11-18/deep-discovery/`):** `W1-MEKANIK-PLATFORM-DAN-STRATEGI.md` · `W2-CARA-KERJA-AKTA.md` · `W3-ARSITEKTUR-MODEL-PROVIDER.md` · `W4-SKILL-DAN-CLI.md` · `W5-ORKESTRASI-PELUANG-KELEMAHAN.md` · `FRONTIER-DUCK-AUDITOR-2026-11-18.md` · `CROWLLM-LIVENESS-2026-11-18.md` (di folder frontier-transfer-direktif).

**PETA ASAL-USUL — bagian mana ditulis siapa (ditambahkan 23:48 atas permintaan user):**
Label bukti ([TERVERIFIKASI] dll.) menyatakan JENIS buktinya; tabel ini menyatakan PENULISNYA. Tiga penulis berbeda terlibat dan tidak boleh tercampur:
- **[PEKERJA W1–W5]** = lima agen bedah yang bekerja paralel atas perintah sesi utama — mereka membaca kode/log/berkas dan menulis lampiran. Isi laporan utama yang bersumber dari mereka adalah RINGKASAN SETIA lampirannya (kata kunci + angka dipertahankan; versi utuh di berkas W).
- **[FRONTIER — DUCK]** = model frontier duck.ai (GPT-6 Luna) dalam peran auditor independen; teksnya utuh di berkas FRONTIER dan dikutip setia.
- **[SESI UTAMA — MUSE]** = tulisan/rakitan/verifikasi operator: tarikan API live malam ini, rekonsiliasi angka, executive summary, diagram, dan penutup. Catatan penilaian sesi utama selalu berlabel "catatan operator".

| Bagian laporan | Penulis utama | Peran sesi utama |
|---|---|---|
| §1 Executive Summary | [SESI UTAMA] | Ditulis sesi utama dari seluruh lampiran + tarikan live |
| §2 Cara Kerja Dialectica | [PEKERJA W1] | Ringkasan setia W1; angka akun akhir dari tarikan live sesi utama |
| §3 Cara Kerja AGENT.AkTa | [PEKERJA W2] | Ringkasan setia W2 |
| §4 Arsitektur Model dan Provider | [PEKERJA W3] | Ringkasan setia W3 |
| §5 Agent Skill dan CLI | [PEKERJA W4] | Ringkasan setia W4 |
| §6 Mekanisme Expert dan Arena | [PEKERJA W1 + W4] | Rakitan sesi utama dari dua lampiran |
| §7 Strategi Earning | [PEKERJA W1] | Ringkasan setia W1 Blok §5 |
| §8 Kemampuan Orkestrasi | [PEKERJA W5] | Tabel W5 dipertahankan utuh |
| §9 Fitur yang Belum Dimanfaatkan | [PEKERJA W4 + W5] | Rakitan sesi utama dari dua lampiran |
| §10 Kelemahan dan Risiko | [PEKERJA W5] (+ W3 untuk celah fallback) | Pilihan butir menentukan oleh sesi utama; isi dari lampiran |
| §11 Arsitektur Aktual | [SESI UTAMA] | Diagram digambar sesi utama dari W2/W3/W4 |
| §12 Arsitektur Ideal | [FRONTIER — DUCK] | Dikutip setia; tambahan sesi utama berlabel "catatan operator" di dalam seksi |
| §13 Rekomendasi Pengembangan | [SESI UTAMA] dari usulan [W5] + [FRONTIER] | Urutan daya angkat = rakitan operator; sumber tiap butir tercantum di §9/§12 |
| §14 Hal yang Membutuhkan Keputusan User | [SESI UTAMA] | Kompilasi operator dari butir-butir terkunci di semua lampiran |

Model frontier LAIN (gpt-5.6-sol, gemini-3.1-pro) TIDAK menulis bagian mana pun dari laporan ini — kolam CrowLLM mereka mati malam ini (bukti: CROWLLM-LIVENESS); konsultasi mereka tetap utang tercatat. Model-model di dalam pipa produksi (GLM, Nemotron, qwen) adalah OBJEK yang dibedah laporan ini, bukan penulisnya.

---

## 1. EXECUTIVE SUMMARY

1. **Sistem ini nyata, bekerja, dan sudah menghasilkan.** Pipa lengkap — poller serve klien vendor → lapisan doktrin kita → penulis GLM → empat gerbang pemeriksa → submission via gateway Matrix → verdict panel — telah mengirim 5 jawaban pilot (17 Nov) yang 4 di antaranya dibayar **+80 $TRUED** pada 18 Nov malam (Innovator +10 ×4, Marathon +10 ×4; verifikasi API primer sesi utama 23:24–23:44: coins **78,1212**, lifetimeEarned **80**, expertise general **9**). **[TERVERIFIKASI]**
2. **Yang membayar di platform ini sangat sempit:** hanya tiga slot — Pioneer +20, Innovator +10 (kebaruan ≥15%), Marathon Winner +10. Verified biasa = **0**. Seluruh arsitektur kita yang benar adalah arsitektur berburu dua slot yang bisa dijangkau (Innovator + Marathon); Pioneer praktis tertutup oleh ekonomi kerumunan. **[TERVERIFIKASI — analitik live + pembayaran sendiri]**
3. **Corong verdict adalah pembunuh utama, bukan mutu:** adjudicationRate general live hanya **0,20–0,32** — 68–80% jawaban terkirim tidak pernah dipegang panel sampai selesai. Penugasan panel era banjir tidak menyaring mutu. **[TERVERIFIKASI-LIVE 18 Nov]**
4. **Keputusan ambil/lewati TIDAK dibuat model AI dan TIDAK dibuat Muse saat runtime** — ia aritmetika deterministik di hook prepare kita sendiri (klasifikasi laju 120 detik + gerbang fail-closed). Model hanya menulis dan menilai draf. **[TERVERIFIKASI — W2 §4]**
5. **Fallback penulis berganti model secara OTOMATIS tanpa persetujuan per kejadian** (desain yang user setujui 17 Nov) — dan transisinya hanya tercatat ke stderr proses; pada kegagalan nyata 18 Nov malam, alasan gugur dua tautan pertama rantai **tidak tercatat di mana pun**. Biaya $ per panggilan model juga **tidak tercatat di log mana pun** — titik impas per jawaban tidak dapat dihitung dari data yang ada. **[TERVERIFIKASI — W3]**
6. **Tidak ada pengamat verdict otomatis.** Verdict-watch adalah tarikan API manual operator. Bukti paling telanjang: penghasilan pertama akun (+70) pertama kali terlihat dari **screenshot user**, bukan dari pantauan sistem. Latensi submit→bayar pilot ±36 jam. **[TERVERIFIKASI — W2 §9, W5 K11]**
7. **CLI stok terbukti secara kode TIDAK bisa menjadi Verifier** (provision dikode-keras ISP di tiga titik) — Jalur 2 (menilai) hanya mungkin lewat API mentah, yang memang jalur kit kita. Gerbang urutan frontier untuk menyalakan Jalur 2 ("Expert terbukti dibayar") **terpenuhi malam ini**. **[TERVERIFIKASI — W4]**
8. **Titik rapuh teratas (audit frontier, dikonfirmasi bukti kami):** (a) slot eksekusi tunggal — satu job ter-drop mengunci ±30 menit tanpa API pelepas, dan slash REL-005 adalah harga nyatanya; (b) gerbang mengukur resolusi sitasi, bukan dukungan sumber→klaim — dua jawaban berfabrikasi lolos gerbang pilot dan DIBAYAR panel, jadi bayaran ≠ kebenaran; (c) bahan bakar fallback (kuota neuron gratis bersama) bisa terbakar kalibrasi dan membunuh generasi produksi — sudah terjadi. **[FRONTIER + TERVERIFIKASI]**
9. **Klasifikasi orkestrasi jujur:** dari 12 kemampuan yang ditanya user — **8 A** (pernah dipakai, berbukti), **3 B** (didukung, belum pernah dipakai penuh), **1 C** (memilih model per karakteristik pertanyaan — belum ada; penulis tetap untuk semua pertanyaan), **0 D**. **[W5 §6]**
10. **Satu-satunya tembakan live sesudah perbaikan kolam** membuktikan jahitan doktrin bekerja (48/48 baris sesuai doktrin; satu tiket menembus seluruh pipa baru) tetapi menabrak dua tembok: liveness lama mem-veto 47/48 tiket marathon yang sudah pasca-ronde, dan generasi satu-satunya mati di kuota neuron habis. Keduanya tercatat sebagai keputusan desain untuk user, bukan diperbaiki diam-diam. **[TERVERIFIKASI — UJI-1-TEMBAKAN]**

---

## 2. CARA KERJA DIALECTICA

*(Ringkasan setia dari W1; mekanisme lengkap + kutipan sumber di lampiran W1.)*

**Platformnya.** Dialectica adalah marketplace pengetahuan terverifikasi: penanya (Customer) mengajukan Question (ISR) ke sebuah Arena; Expert (agen ISP) menjawab (Answer/ISO); panel Verifier (agen IVSP) menilai jawaban; jawaban yang lolos menjadi Verified Answer dan masuk wiki publik. $TRUED adalah poin kontribusi internal — **ekspor on-chain belum tersedia** per FAQ resmi /why; yang menentukan peringkat leaderboard adalah **Lifetime Earned**, bukan saldo. **[DOKUMENTASI RESMI + TERVERIFIKASI]**

**Alur sebuah Question.** Question dibuat (fee bertingkat seumur akun penanya: fee(n) = 10(n−1)³/((n−1)³+13³); pertanyaan pertama gratis) → masuk kolam arena → Expert mengambilnya lewat dua pola: *pushed work* (platform menugaskan) atau *dynamic work* (Expert menarik sendiri dari kolam; strategi akun kita `dynamic` = pull-only) → Answer dikomit (commit) lalu diungkap (reveal) → panel Verifier ditugaskan → panel menyimpulkan (≥2 support DAN 0 refutasi = verified; ada refutasi yang bertahan = falsified) → reward achievement diproses. **[TERVERIFIKASI + DOKUMENTASI]**

**Reward — hanya tiga slot yang membayar di jalur Expert [TERVERIFIKASI, MEKANISME §25.1 + pembayaran sendiri]:**
- **Pioneer +20** — jawaban verified PERTAMA pada sebuah Question; kebal falsifikasi susulan.
- **Innovator +10** — jawaban verified dengan konten baru ≥15% (lolos **Surprise Gauge**, pengukur kebaruan platform).
- **Marathon Winner +10** — jawaban verified yang menutup jendela marathon (500 detik) sebuah Question.
- Verified tidak-novel = **0**. Tidak ada pengali strategi, RAR, atau Expertise atas payout — strategi hanya menyeleksi pekerjaan apa yang sampai ke Expert; RAR buruk berfungsi sebagai gerbang eksklusi (menghentikan semua penghasilan), Expertise menggerbang badge. **[TERVERIFIKASI — ledger §24/§25]**

**Corong verdict dua tahap [TERVERIFIKASI-LIVE]:** jawaban harus (1) DITUGASKAN ke panel dan (2) panel MENYIMPULKAN. Di era banjir hanya ±32,6% jawaban pernah dipegang ≥2 verifier; adjudicationRate general live 18 Nov = 0,20–0,32. Kurva peluang dari studi 6.188 ISO: posisi masuk 1–60 = 0,14–0,25 (zona mati); tunda 2–6 jam = 0,50; >24 jam = 0,63; lutut posisi ±10–20; kedalaman akhir tidak menentukan. Penolakan platform: surprise_gauge **68,5%** dari semua penolakan general; di dalam arena_rules, pelanggaran sitasi **A_CITATION = 92,2%**. **[TERVERIFIKASI-LIVE 18 Nov malam]**

**Skor dan risiko akun.** Expertise per arena tumbuh dari jawaban verified; Reputation/RAR adalah komposit (formula numerik + ambang suspensi **tidak dipublikasikan** — [BELUM-TERBUKTI]). Reliability turun lewat slash aturan REL (definisi resmi REL-005 tidak terpublikasi; definisi kerja kami dari data: job yang diklaim lalu ter-drop tanpa jawaban). Suspensi bertingkat (akun kita: 6 kali, reliability −6). Falsified Answer berbiaya −1 poin pada sisi bertanya dan kerusakan reputasi/suspensi pada sisi menjawab — bukan potongan koin langsung. **[TERVERIFIKASI sebagian; formula = BELUM-TERBUKTI]**

**Pembeda Answer berkualitas [TERVERIFIKASI dari analitik + hasil sendiri]:** (1) lolos Surprise Gauge — membawa informasi yang belum ada di kolam jawaban Question itu (kebaruan diukur lawan jawaban yang sudah ada, bukan lawan dunia); (2) sitasi yang benar-benar menyatakan klaimnya (A_CITATION); (3) masuk pada posisi/waktu yang membuatnya sempat ditugaskan panel (mekanik §2 di atas). Panjang dan kedalaman sendiri BUKAN penentu terbukti.

**Posisi akun saat laporan ditulis [TERVERIFIKASI 23:44]:** coins **78,1212** · lifetimeEarned **80** · expertise general **9** · reputation **107** · RAR **135** · reliability **−6** · suspensionCount **6** · rank ±400 (angka dashboard user; API leaderboard hanya mempublikasikan top 10 — #10 = ±28.762 lifetime, #1 = ±98.826). Rekonsiliasi koin seumur akun: 14 peristiwa notifikasi (8 achievement +70→+80, 6 fee −1,8788) + kredit pembuatan +7 − penalti falsified −7 = **78,1212 persis**.

---

## 3. CARA KERJA AGENT.AkTa

*(Ringkasan setia dari W2 — 10 langkah user, per langkah: Muse / CLI-sistem / model / user / mode gagal. Tabel peran lengkap di lampiran W2.)*

**Langkah 1 — Koneksi.** Dua kredensial terpisah tegas **[TERVERIFIKASI-KODE]**: (a) sesi operator `~/.dialectica/session` → header `X-Active-Session` untuk REST read/write akun; (b) kredensial kerja Expert via gateway Matrix untuk pekerjaan. Kunci provider disuntik `run_serve.py` sebagai *surrogate vault* (env proses, tidak menyentuh disk). Satu-satunya tindakan user yang tersisa di langkah ini: sign-in ulang berkala (±7 hari) lewat alur aman. Mode gagal terbukti: file unit systemd di /etc hilang saat VM replacement (2× dalam sehari, 18 Nov) — state `~/.dialectica/` selalu selamat; pemulihan = pasang ulang unit dari salinan induk provider.

**Langkah 2 — Inisialisasi Expert.** `ensure_expert()` klien stok, idempoten: Expert kita (`8522c990…`, strategy dynamic, arena general, maxConcurrency 1, contextWindowTokens 160.000, caps server unlimited) selalu dipakai ulang; tidak pernah dibuat ulang oleh nyala mana pun. **[TERVERIFIKASI]**

**Langkah 3 — Menemukan Question.** Strategy dynamic = platform TIDAK mendorong apa pun; `trued serve --every 1m` melakukan polling sendiri ke kolam. Sesudah perbaikan kolam 18 Nov: pita usia **2–6 jam, tanpa query wallet** (sebelumnya: query `q=wallet` jendela 3 hari — akar kegagalan mini-batch: kolam serve dan kolam doktrin nol irisan). Pengamat terpisah `rate_trigger.py` (siklus 45 detik, read-only) mengklasifikasi pertanyaan dari rekonstruksi timestamp ISO. **[TERVERIFIKASI — PERBAIKAN-KOLAM + UJI-1-TEMBAKAN]**

**Langkah 4 — Keputusan ambil/lewati.** Terjadi **seluruhnya di hook kita** `vyce_serve_prepare.prepare_row()`, SEBELUM klaim, berurutan: liveness fail-closed → keputusan lane Doktrin A (klasifikasi laju 120 detik pertama: ≤5 CEPAT; ≥11 TELAT; antaranya TUNGGU; baris tak-terklasifikasi = TAHAN fail-closed; keputusan dibaca ulang dari store tiap panggilan — reconsideration Q2) → gerbang sekuensing klaim Q4 (job sebelumnya belum terminal = tahan) → layar kesegaran pra-klaim Q3 → generasi. **Model AI dan Muse tidak punya peran runtime di keputusan ini** — ia aritmetika + gerbang deterministik. **[TERVERIFIKASI-KODE — W2 §4]** Keterbatasan tercatat: skip prepare 6 jam klien stok hidup di memori proses klien dan tidak bisa ditimpa bersih dari lapisan kita.

**Langkah 5 — Penerusan ke model.** Prompt dirakit dari baris (jalur prepare) atau `build_provider_prompt` klien (jalur job), selalu lewat stdin; kontrak format ditempel satu kali; steering per-ISR tercatat di `vyce_provider`. Konteks kebaruan (jawaban yang sudah ada di Question itu) disuntikkan dengan lantai cakupan COVER_FLOOR=8 dan tahan-potong. **[TERVERIFIKASI-KODE]**

**Langkah 6 — Model menghasilkan Answer.** Penulis utama GLM-5.3-flash via Vyce; rantai cadangan R1: gpt-oss-120b via Vyce → gpt-oss via Cloudflare (stateful, tercatat per lane). Cap keras **10 generasi/hari-UTC ditegakkan di kode SEBELUM membakar**, dihitung dari `token-usage.jsonl` berlabel lane (reset 07:00 WIB). Lantai panjang per kelas tertanam di kode: Pioneer 1.717 · umum 3.000 · Marathon 4.500 kata-token dengan pita patokan 10.000–12.000. **[TERVERIFIKASI-KODE + LOG]**

**Langkah 7 — Pemeriksaan pra-kirim.** `gate_answer` berlapis: (a) wrapper mutu — lantai panjang per kelas, K-2 kemiripan konteks 0,30 (ambang keputusan user), format; (b) detektor trace/E3 fail-closed; (c) rantai pemeriksa semantik — Nemotron utama (fatal = final) → qwen-3.8-max cadangan via CrowLLM → gpt-5.6-sol penengah sengketa (2-dari-3; penengah mati = vonis utama berdiri + flag `dispute_unresolved`); mode C5 warisan berjalan SHADOW; semua lane mati = tak-terukur, tidak memblokir; (d) verifikasi sitasi mekanis (55 tes) mode block; (e) verifikasi isi dua tahap (mekanis + entailment Nemotron, 46 tes) mode block; (f) gerbang kesegaran (CROWD_CAP 20, keputusan user) yang dinilai ulang di detik kirim. **Bukti jujur yang tercatat di berkas kami sendiri: label "C5 clean" pada pilot terbukti BUKAN verifikasi sitasi** — spot-check manual menemukan fabrikasi pada 3 dari 5 jawaban pilot yang lolos semua gerbang versi saat itu. **[TERVERIFIKASI — W2 §7, SPOTCHECK 17 Nov]**

**Langkah 8 — Penyerahan.** Cache draf → veto READY → klaim di thread terpisah (klaim di loop utama membuat Question ditolak, bukan dilewati — [KODE W4]) → kirim via gateway. Veto detik-kirim masih bisa men-drop job SESUDAH klaim. Rantai kejadian terbukti 18 Nov pagi: veto pasca-klaim → intent yatim `e3287902` tanpa isi → slot terkunci ±30 menit → tembakan berikutnya ditolak "Agent at capacity (1/1)" → **slash REL-005** (notifikasi 03:31:51Z, reliability −5). Mitigasi Q3/Q4 yang dibangun sesudahnya memindahkan kegagalan itu ke SEBELUM klaim — terbukti bekerja di uji asap (layar pra-klaim menilai `fresh`, sekuensing lolos, nol klaim yatim). **[PENGALAMAN + TERVERIFIKASI]**

**Langkah 9 — Pemantauan verifikasi.** **Tidak ada watcher otomatis — temuan struktural.** Yang ada: tarikan GET manual operator (`verifier_common.api_get`, modul yang sengaja tidak punya helper tulis) saat sesi aktif. Satu-satunya "watcher" yang pernah hidup adalah pengaman counter one-shot milik uji asap. Latensi nyata pilot: submit 17 Nov → bayar 18 Nov malam (±36 jam), dan kabar pertamanya sampai ke operator lewat screenshot user. **[TERVERIFIKASI — W2 §9]**

**Langkah 10 — Mengetahui reward.** Sinyal otoritatif = notifikasi `achievement_unlocked` (delta +10 per event; 8 event pilot) dibaca silang dengan `/api/node/scores`. Status ISO "verified" saja BUKAN bukti bayaran (verified biasa = $0). Audit penuh 18 Nov 23:24–23:44: 89 notifikasi seumur akun, 14 peristiwa koin, rekonsiliasi persis ke saldo. **[TERVERIFIKASI]**

---

## 4. ARSITEKTUR MODEL DAN PROVIDER

*(Ringkasan setia dari W3 — tabel 13 kursi lengkap di lampiran.)*

**Kursi yang benar-benar terpasang [TERVERIFIKASI-KODE+LOG]:**
| Fungsi | Model | Provider/jalur | Catatan |
|---|---|---|---|
| Penulis utama | GLM-5.3-flash | Vyce (relay) | semua Question, tanpa kecuali |
| Penulis cadangan 1 | gpt-oss-120b | Vyce | fallback otomatis R1 |
| Penulis cadangan 2 | gpt-oss | Cloudflare Workers AI | kuota neuron ±10.000/hari bersama |
| Pemeriksa utama (C5/rantai) | Nemotron-3-Ultra | OpenRouter (lane sendiri) | tangkapan fatal 7/7 kalibrasi |
| Pemeriksa cadangan internal | Nemotron-3.5-super-vl | Vyce | di dalam lane pemeriksa |
| Pemeriksa cadangan rantai | qwen-3.8-max | CrowLLM (relay bersama) | 6/7; **503 malam ini** |
| Penengah sengketa | gpt-5.6-sol | CrowLLM | 5/7; **503 malam ini** |
| Entailment isi tahap 2 | Nemotron (lane sama) | OpenRouter | maks 6 panggilan/draf |
| Lapis 4 (tersertifikasi) | gpt-oss | Cloudflare | 7/7 — **belum ter-wire di kode** |
| Research | — | deterministik, tanpa model | konteks kebaruan dirakit kode, bukan model |

**Routing.** Per-fungsi: YA (tabel di atas). Per-pertanyaan/topik: **TIDAK ADA** — setiap Question ditulis model yang sama; karakteristik Question hanya mengubah lantai panjang dan konteks, bukan pilihan model. Kerja paralel model: **nol** — tidak ada primitif konkurensi di seluruh provider; semua estafet sekuensial. **[TERVERIFIKASI-KODE — W3]**

**Apakah hasil model diteruskan mentah ke Dialectica?** Substansi argumen: ya — pemeriksa hanya memvonis, tidak memparafrase. Tetapi ada lapisan mekanis yang terbukti dari kode: audit wrapper membuang token angka yang salah-ikat (tidak pernah menggantinya dengan karangan), regenerasi panjang maks 1×, dan gerbang format JSON. Jadi "tanpa mengubah substansi" = benar untuk isi, dengan penyuntingan mekanis terbatas yang tercatat. **[TERVERIFIKASI-KODE]**

**Fallback — jawaban langsung atas pertanyaan user.** YA, rantai penulis R1 mengganti model **otomatis tanpa persetujuan per kejadian**; ini desain yang user setujui saat pemasangan (17 Nov), bukan penyimpangan. Pergantian tercatat sesudahnya di `token-usage.jsonl` (terbukti 6 record gpt-oss di lane vyce-serve). **Celahnya:** transisi fallback hanya ditulis ke stderr proses prepare — grep log serve 17/18 Nov menemukan **nol** baris `fallback:`; pada kegagalan neuron 18 Nov malam, alasan gugur tautan 1–2 rantai tidak tercatat, yang tersisa hanya error terminal 429 tautan 3. Rantai gagal menyelamatkan karena tautan 1–2 berbagi satu provider (Vyce) dan tautan 3 bergantung pada anggaran neuron bersama yang sudah habis sejak pagi oleh kalibrasi — rantai ini dirancang untuk kegagalan MODEL, bukan kegagalan BAHAN BAKAR BERSAMA. **[TERVERIFIKASI — W3]**

**Verifiabilitas dari log — yang bisa dan tidak bisa dibuktikan.** `token-usage.jsonl` mencatat model yang *diminta*, lane, token/neuron terpakai. TIDAK tercatat: identitas model di balik router Vyce (tidak teratestasi), dan **biaya $ per panggilan di mana pun** (selain `cost: 0` bawaan OpenRouter). Konsekuensi: titik impas per jawaban tidak dapat dihitung dari log yang ada. **[TERVERIFIKASI — W3]**

**Batasan teknis per lane [TERVERIFIKASI]:** neuron Cloudflare berhenti-kode di >9.000/hari; CrowLLM = anggaran bersama 5 req/menit semua proyek (pacing kami 13 detik) dan kesehatan per-kolam-upstream (sapuan 18 Nov malam: 21 hidup/41 mati — Gemini 12/12 mati, OpenAI arus utama mati, Nemotron 5/5 hidup); OpenRouter diperlakukan cadangan darurat (lane pemeriksa menyerah sukarela pada sisa kredit <2 — sisa saat ini 1, terkunci keputusan user); Gemini direct free-tier dilarang (keputusan user; via CrowLLM boleh); route deepseek Vyce mati 403.

---

## 5. AGENT SKILL DAN CLI

*(Ringkasan setia dari W4 — semua angka dikutip [KODE: trued.py:baris] di lampiran.)*

**Arsitektur transport ganda [TERVERIFIKASI-KODE].** Klien `trued` v0.22.4 berbicara dua bahasa: (a) **REST** untuk baca/tulis akun — header `X-Active-Session` dari `~/.dialectica/session`, atau *work credential* `Authorization: Bearer` yang MENGGANTIKAN token sesi hanya untuk 3 panggilan penghasilan, digerbang flag server `agentWorkCredentialEnabled` yang diprobe sekali per proses; (b) **protokol Matrix** untuk pekerjaan Expert — login gateway, long-poll `/sync` 10 detik, event diterima fail-closed hanya dari system user.

**Peta command.** 19 command + 5 subcommand `agent` terpetakan penuh di W4 beserta endpointnya. Yang dipakai operasi kami sehari-hari hanya sebagian (serve, answer, scores, notifications, agents, isrs, isos). Provision Expert dikode-keras `{"type": "ISP"}` (trued.py:4082); cap bawaan klien 20 jawaban/24 jam (cap operasi kami 10 ditegakkan lapisan kami sendiri, lebih ketat); strategi awal `dynamic` pull-only terpasang pada serve/answer pertama.

**Serve [TERVERIFIKASI-KODE].** Kunci proses tunggal `serve.lock`; klaim dynamic berjalan di thread terpisah (klaim di loop utama = Question DITOLAK, bukan dilewati — jebakan yang pernah membakar kami); offer-to-answer dijawab inline ±30 detik dengan aritmetika lokal (skor 100/0, tanpa model); **`PREPARE_SKIP_TTL_S = 6 × 3600` (trued.py:2988) disimpan di memori proses** — restart mengosongkannya; timeout provider bawaan 900.000 ms (15 menit); konkurensi ditegakkan server — klien membuat thread per job tanpa gerbang lokal.

**Answer [TERVERIFIKASI].** Pola resmi satu jawaban = `trued answer <isrId>` yang end-by-itself dengan exit code — bukan serve open-ended. Serve adalah mode massal yang kami pakai; answer langsung adalah jalur bedah yang belum pernah dipakai operasi (lihat §9).

**Kematian proses — titik buta terverifikasi kode.** Klien **tidak memiliki panggilan pelepas/abandon job sama sekali**. Job Expert yang prosesnya mati hanya berakhir dari sisi server sebagai `abandoned` (keluarga REL-005). Ini menjelaskan persis kunci "Agent at capacity (1/1)" ±30 menit pada 18 Nov: maxConcurrency=1 + nol API pelepas. Kredensial dikelola sebagai file sesi di `~/.dialectica/` (mekanisme saja yang dilaporkan di sini; isinya tidak pernah dibuka lini investigasi).

**Verifier di luar jangkauan CLI stok — terbukti di tiga titik kode:** provision ISP-only, resolusi agent menyaring `type=="ISP"`, gerbang evaluate menolak non-ISR. Bangunan Jalur 2 lewat API mentah (kit `provider/verifier/`) adalah keharusan teknis, bukan pilihan gaya. **[TERVERIFIKASI-KODE — W4]**

---

## 6. MEKANISME EXPERT DAN ARENA

**Arena [TERVERIFIKASI-LIVE 18 Nov].** Tiga arena terdaftar: **general** (semua peran — postISR/ISP/IVSP — terbuka `anyone`), **forecasting** (postISR `admin`, ISP `anyone`, IVSP `anyone`; marathonTurns 1000, consensus 2; reward verdict masuk escrow), **hle** (semua peran `admin` — tertutup total untuk kami). Expert kita terdaftar di general saja. Ekonomi per arena dari analitik live: general per-unit Expert 3,33–3,46 pada strategi yang tepat dengan median/agent rendah (0–10) kecuali strategi marathon; forecasting per-unit 0,5–1,7; HLE per-unit 16–23 tetapi admin-only.

**Strategi Expert [TERVERIFIKASI].** Strategi adalah pemilih pekerjaan server-side: ia menentukan Question apa yang ditawarkan ke Expert (mis. innovation_focus menyaring lewat maxVisos 6 → menyasar pertanyaan yang belum ramai verified; dynamic berburu bebas termasuk viso-0 → satu-satunya akses Pioneer). Statistik strategi di analitik = successRate (verified dari yang diadjudikasi) dan adjudicationRate (yang mencapai panel) dihitung per kohort strategi — **bukan** pengali payout. Akun kita: strategy `dynamic` (1.984 agen sekohort, SR 66,0%, 3,40/unit, median/agent 0 — median nol berarti mayoritas agen dynamic tidak pernah dibayar; penghasilan terkonsentrasi di ekor atas). **[TERVERIFIKASI — PETA-EARN-LIVE]**

**Hubungan skor [TERVERIFIKASI sebagian].** Expertise (per arena) ← jawaban verified; Reputation & RAR ← komposit perilaku (reliability, availability, expertise); Lifetime Earned ← total reward achievement (yang menentukan leaderboard + gerbang badge); saldo coins ← lifetime dikurangi fee/penalti sisi bertanya. Formula persis RAR dan ambang suspensi: **[BELUM-TERBUKTI — tidak dipublikasikan platform]**.

---

## 7. STRATEGI EARNING

*(Analisis mekanisme — BUKAN rekomendasi; keputusan strategi tetap milik user. Dari W1 Blok §5.)*

**Faktor yang terbukti menentukan hasil, berurutan daya:**
1. **Ditugaskan panel atau tidak** (adjudicationRate 0,20–0,32) — corong pertama; diatur oleh posisi + waktu masuk (kurva §2), bukan mutu.
2. **Lolos Surprise Gauge** (68,5% penolakan) — kebaruan ≥15% lawan kolam jawaban yang ada; diatur oleh seleksi Question (yang kolamnya belum memuat substansi kita) + konteks kebaruan yang disuntikkan ke penulis.
3. **Menutup marathon** — verified terakhir saat jendela 500 detik menutup; diatur oleh timing masuk telat (basis Doktrin A: parkir 2–6 jam).
4. **Tidak falsified** — ≥2 support DAN 0 refutasi; risiko terkonsentrasi di dukungan sitasi (A_CITATION 92,2% dari kegagalan aturan).
5. **Menghindari zona mati** — tunda 2–120 menit × posisi 11–60 pada Question banjir (konversi 0,14–0,25).

**Statistik strategi dibaca dengan ukuran sampel:** successRate tanpa adjudicationRate adalah angka yatim — SR 66% atas 30% yang diadjudikasi berarti laju bayar efektif per submission jauh lebih rendah; perbandingan antar-strategi sah hanya pada kohort + jendela yang sama, dan median/agent 0 pada dynamic membuktikan distribusi sangat miring (rata-rata ditopang ekor). **[INFERENSI terukur dari analitik live]**

**Pioneer** menguntungkan karena +20 dan kebal falsifikasi susulan, tetapi mensyaratkan verified PERTAMA — di Question yang terlihat publik, jendela itu dimenangi laju masuk detik-pertama; jalur kami (viso-0 via dynamic) pernah mengirim 5 jawaban Pioneer-era pilot dan tidak satu pun memanen Pioneer — yang memanen justru Innovator+Marathon dari posisi telat. **[PENGALAMAN]**

**Duplikat dicegah** oleh Surprise Gauge itu sendiri (jawaban yang mengulang kolam gugur kebaruan) + konteks kebaruan kita (COVER_FLOOR=8) yang memaksa penulis membawa sudut baru. **Biaya model** ditekan oleh urutan gerbang murah→mahal (mekanis sebelum juri) dan cap generasi harian; kebocoran biaya terbukti justru di luar pipa: kalibrasi memakan kuota fallback bersama (lihat §10-K8).

---

## 8. KEMAMPUAN ORKESTRASI

*(Klasifikasi W5 §6 — A = sudah bisa + pernah digunakan (berbukti) · B = didukung teknis, belum pernah digunakan penuh · C = butuh integrasi/pengembangan · D = tidak didukung. Bukti per butir di lampiran W5.)*

| # | Kemampuan | Kelas | Bukti ringkas |
|---|---|---|---|
| 1 | Membaca Question + menentukan spesialisasi | **B** | Klasifikasi kelas/lane nyata (doktrin); spesialisasi domain per pertanyaan tidak ada |
| 2 | Memilih model berdasar karakteristik Question | **C** | Penulis tetap GLM untuk semua; hanya lantai panjang per kelas yang berubah |
| 3 | Menyiapkan konteks + prompt yang tepat | **A** | Konteks kebaruan tahan-potong, steering per-ISR, kontrak format |
| 4 | Mengatur urutan Research→Answer→Review→Fact-check | **A** | Pipa terpasang: konteks deterministik → GLM → gerbang berlapis → entailment |
| 5 | Meminta model memperbaiki hasil saat ada kesalahan | **B** | Terbukti manual (revisi terdokumentasi); loop revisi otomatis di pipa tidak ada |
| 6 | Menyelesaikan konflik antar-model | **B** | Rantai 2-dari-3 terpasang; belum ada sengketa live yang terputus olehnya |
| 7 | Mengukur kualitas jawaban pra-submission | **A** | Empat gerbang + kalibrasi terukur (7/7, 6/7, 5/7) |
| 8 | Mengelola deadline & pekerjaan yang diterima | **A** | Cap kode, gerbang sekuensing, veto detik-kirim, kill-metric |
| 9 | Memantau biaya API & penggunaan token | **A−** | Token/neuron tercatat per lane; **biaya $ tidak tercatat**; biaya per verdict Jalur 2 belum dibangun |
| 10 | Menyimpan riwayat pekerjaan untuk pembelajaran | **A** | Jurnal per nyala, ledger mekanisme, log keputusan append-only |
| 11 | Menganalisis hasil Verified & Falsified | **A** | Audit notifikasi penuh + rekonsiliasi; spot-check pasca-verdict pilot |
| 12 | Memakai hasil sebelumnya untuk keputusan berikutnya | **A** | Doktrin A lahir dari studi 6.188 ISO; perbaikan kolam dari bedah mini-batch — di siklus yang sama |

**Total: 8 A · 3 B · 1 C · 0 D.** Tidak ada kemampuan yang mustahil; dua lubang terbesar adalah #2 (routing per pertanyaan) dan #9 (biaya $ tak terlihat).

---

## 9. FITUR YANG BELUM DIMANFAATKAN

*(Inventaris W4 — 18 butir, manfaat+risiko per butir di lampiran — + peluang berbasis bukti W5 §7. Yang berlabel [HIPOTESIS] belum teruji.)*

**Dari CLI/API resmi yang sudah ada [TERVERIFIKASI-KODE]:**
- `opportunities --list-filters` — jalur baca resmi untuk memanen Question sesuai filter; belum pernah dipakai (kita memanen via serve).
- Command `arena` dengan alasan penolakan server — diagnostik kelayakan per arena tanpa menebak.
- `agent strategies` — daftar strategi resmi + parameter servernya (endgame/early_follower/marathon_tackler belum pernah dibaca parameter resminya dari jalur ini).
- `notes` server-side — catatan yang menempel di server, bukan hanya berkas lokal.
- Ritual `signin` resmi — jalur penyegaran sesi terdokumentasi.
- `trued answer <isrId>` langsung — jalur bedah satu jawaban end-by-itself (untuk tembakan tertarget tanpa serve massal).
- Paling berisiko bila disentuh: `DIALECTICA_PROVIDER_TOOLS` + `Bash`/`Read` — memberi provider akses alat; **tidak direkomendasikan tanpa keputusan user eksplisit**.

**Dari bangunan kita sendiri [BUKTI]:**
- **Registrasi IVSP (Jalur 2)** — kit selesai, gerbang urutan frontier terpenuhi malam ini (+80); belum teregistrasi. Median agen economist general 6.373 lifetime — daya angkat terbesar yang belum dinyalakan.
- **IVSP Forecasting** — eligibility anyone; reward escrow; belum disentuh.
- **Liveness sadar-lane** — penyesuaian desain yang dituntut bukti uji asap (47/48 tiket terveto aturan liveness warisan).
- **Pencatatan biaya per verdict** di runner verifier — prasyarat uji 14 hari yang jujur; belum dibangun.
- **Pra-terbang bahan bakar** — cek kuota neuron + kesehatan lane penulis sebagai gerbang nyala (pelajaran kegagalan 18 Nov malam).
- **Verifikasi pinpoint** (pasal/angka persis di dalam sumber) — celah yang dibuktikan spot-check MiCA (Article 62 karangan vs 75 benar) yang lolos verifikasi isi dua tahap.
- **Kursi penengah dari kolam CrowLLM yang hidup** (Nemotron-ultra/Grok/k2-horizon hidup malam ini; kursi resmi sol/gemini di kolam mati) — penggantian kursi = wilayah keputusan user.
- **Otomatisasi verdict-watch** — polling terjadwal + buku besar hasil per jawaban (perubahan daya-angkat tertinggi menurut auditor frontier).
- **[HIPOTESIS]** Expert paralel kedua (platform membolehkan >1 Expert per akun; dompet + RAR dibagi), loop revisi otomatis penulis, tata ulang rantai penulis ke provider ketiga independen.

---

## 10. KELEMAHAN DAN RISIKO

*(18 kelemahan bernomor di W5 §8; di sini yang menentukan, dengan bukti. Penomoran K merujuk lampiran W5.)*

- **K1/K3 — Fabrikasi penunjuk presisi GLM bersifat struktural.** Tanpa retrieval yang mengikat, penulis mengarang penunjuk non-kanonis: preseden Hop karangan, DOI Meiklejohn salah, Article 62 (benar: 75). Pengenal kanonis terkenal (nomor EIP) aman. Gerbang sitasi mekanis memverifikasi resolusi, **bukan** dukungan sumber→klaim per pinpoint. **[PENGALAMAN + TERVERIFIKASI]**
- **K2 — Paradoks panel (dibaca dua arah, jujur).** Dua pemenang +20 justru yang spot-check sitasinya GAGAL; yang lolos bersih dibayar paling kecil (+10, sebelum Marathon-nya menyusul +10 lagi). Data ini melemahkan "sitasi menentukan bayaran" — tetapi falsified historis kita mati persis di dukungan sitasi, jadi sitasi tetap menentukan **risiko**, bukan **bayaran**. Mengoptimalkan gerbang untuk bayaran dengan melonggarkan sitasi akan menukar risiko akun (reliability −6, suspensi 6, ambang ban tak terpublikasi) demi slot +10. **[PENGALAMAN — dua arah]**
- **K8 — Fallback berganti model tanpa sinyal real-time + bahan bakar bersama.** Lihat §4: transisi hanya ke stderr; neuron fallback terbakar kalibrasi pagi, membunuh generasi malam. **[TERVERIFIKASI]**
- **K11 — Verdict dipantau manual.** +70 pertama terlihat dari screenshot user. Tidak ada watcher; tidak ada buku besar hasil per jawaban yang menggabungkan lane/provider/alasan gerbang/verdict/reward. **[TERVERIFIKASI]**
- **K13 — Tembok liveness-vs-marathon.** Ronde marathon pertanyaan berumur 0,4–1,5 jam; release TELAT doktrin +2 jam → hampir semua tiket due sudah pasca-ronde saat tersaji dan aturan liveness warisan mem-veto (47/48 di uji asap). **[TERVERIFIKASI — UJI-1-TEMBAKAN §6]**
- **K15 — Infrastruktur ephemeral.** Unit systemd di /etc hilang 2× sehari (VM replacement); kesiapan nyala bergantung pada langkah pasang-ulang manual menit-terakhir. **[PENGALAMAN]**
- **Slot tunggal + nol API pelepas** (W4): satu job yatim = ±30 menit mati + paparan slash REL. Mitigasi Q3/Q4 mengurangi sebabnya, tidak menghapus strukturnya. **[TERVERIFIKASI-KODE]**
- **Konsentrasi provider.** Tautan penulis 1–2 satu provider (Vyce); juri cadangan + penengah satu relay bersama (CrowLLM) yang kolamnya bisa mati per-upstream (malam ini: dua-duanya). Suara 2-dari-3 dari relay yang sama **bukan** bukti independen — ditegaskan auditor frontier. **[TERVERIFIKASI + FRONTIER]**
- **Biaya tak terlihat.** Tanpa catatan biaya $ per panggilan, efisiensi hanya bisa diukur dalam token/neuron dan generasi — bukan uang. **[TERVERIFIKASI]**
- **Risiko yang belum terantisipasi penuh:** ambang ban permanen tidak terpublikasi sementara reliability sudah −6/suspensi 6; 22 jawaban lama masih revealed di kolam assigned-unconcluded yang hidup (paparan verdict negatif kolektif); $TRUED belum bisa diekspor — seluruh nilai saat ini adalah posisi, bukan kas. **[TERVERIFIKASI + BELUM-TERBUKTI untuk ambang ban]**

---

## 11. ARSITEKTUR AKTUAL

```
USER (Sara — operator-1: arah, konsep, keputusan berbayar/berisiko/ireversibel)
  │  kata jalan / izin per nyala / keputusan wilayah terkunci
  ▼
MUSE / AGENT.AkTa (operator-2: orkestrasi, routing model, verifikasi, laporan)
  │  menyiapkan unit + drop-in, arming env gerbang, memantau, membunuh unit di batas
  ▼
LAPISAN KITA (provider/, di atas klien stok)
  ├─ Pengamat rate_trigger (45 dtk, read-only) → klasifikasi lane → store doktrin
  ├─ Hook prepare_row: liveness → keputusan lane (fail-closed) → sekuensing Q4
  │    → layar pra-klaim Q3 → panggil penulis → gate_answer → cache READY
  └─ Gerbang: wrapper mutu (K-2 0,30, lantai per kelas) · detektor trace
       · rantai pemeriksa (Nemotron → qwen → sol penengah) · sitasi (block)
       · isi dua tahap (block) · kesegaran (pra-klaim + veto detik-kirim)
  ▼
DIALECTICA SKILL / CLI trued v0.22.4 (stok, tak dimodifikasi)
  ├─ REST (X-Active-Session / work credential) — akun, scores, notifications
  └─ Matrix gateway — serve poller (pita 2–6 jam) → klaim (thread) → kirim Answer
  ▼
EXPERT AGENT.AkTa (ISP, dynamic, general, concurrency 1)
  ▼
MODEL PROVIDER (semua sekuensial, nol paralel)
  Penulis: GLM-5.3-flash (Vyce) → fallback gpt-oss (Vyce) → gpt-oss (Cloudflare)
  Pemeriksa: Nemotron (OpenRouter) · qwen + sol (CrowLLM, relay bersama)
  ▼
SUBMISSION → kolam Answer (commit/reveal) → panel Verifier (pihak lain)
  ▼
VERDICT (jam–hari kemudian) → achievement Pioneer/Innovator/Marathon
  ▼
REWARD & ANALYTICS — dibaca MANUAL oleh operator (API poll saat sesi aktif);
  TIDAK ada watcher otomatis; pembelajaran masuk ledger berkas secara manual.
```

Yang TIDAK ada di diagram karena memang tidak ada: routing model per pertanyaan, watcher verdict, buku besar hasil per jawaban, pencatatan biaya $, jalur Verifier (kit ada, registrasi belum), Expert kedua.

---

## 12. ARSITEKTUR IDEAL

*(Usulan auditor frontier duck — disampaikan setia dari lampiran FRONTIER; komponennya hanya yang sudah ada. Catatan operator di akhir seksi, berlabel.)*

1. **Sebelum seleksi:** cek status slot akun + ketersediaan provider penulis termasuk kuota fallback. Slot terkunci atau tak ada rute penulis → jangan pilih pekerjaan.
2. **Seleksi berdasar nilai-harapan:** klasifikasi cepat/telat doktrin menjadi MASUKAN, bukan aturan keputusan; prioritas = peluang Innovator/Marathon × kelayakan dukungan sumber.
3. **Generate sekali, gerbang berurutan murah→mahal,** dengan uji sitasi inti digeser dari "pengenal ter-resolve" ke **"sumber mendukung klaim"**.
4. **Voting tidak menciptakan kepercayaan palsu:** juri utama dipertahankan; suara relay-bersama diperlakukan sebagai pendeteksi ketidaksepakatan, bukan konfirmasi independen; temuan fatal tidak dibatalkan mayoritas — ketidaksepakatan naik ke jalur persetujuan manusia.
5. **Tutup lingkaran otomatis:** polling verdict terotomatisasi; tiap verdict dikaitkan ke pertanyaan/jawaban/jalur provider/alasan gerbang; catatan seleksi + prompting diperbarui darinya. Persetujuan manusia tetap untuk berbayar/berisiko/ireversibel.
6. **Verifier sebagai lane terpisah** dengan evaluasi nilai-harapannya sendiri; registrasi hanya lewat persetujuan user.
7. **Perubahan daya-angkat tertinggi menurut auditor:** buku besar hasil per jawaban + pengamat verdict otomatis. **Ilusi paling berbahaya menurut auditor:** menganggap "sitasi ter-resolve + mayoritas juri + bayaran panel" = jawaban bisa dipercaya.

**Catatan operator (Muse, bukan vonis model):** usulan #3 (uji dukungan sumber→klaim sebagai inti) sejalan dengan celah pinpoint yang dibuktikan spot-check kami sendiri (K1) — dua jalur bukti independen bertemu di titik yang sama. Usulan #1 (pra-terbang bahan bakar) sudah menjadi pelajaran tercatat kami dari kegagalan 18 Nov malam (W5-P5) sebelum audit ini tiba. Tidak ada usulan di seksi ini yang dieksekusi oleh laporan ini.

---

## 13. REKOMENDASI PENGEMBANGAN

*(Usulan untuk dianalisis user — bukan keputusan, bukan implementasi. Berurutan daya angkat menurut gabungan bukti W1–W5 + auditor.)*

1. **Bangun buku besar hasil per jawaban + verdict-watch terotomatisasi** (menutup K11; prasyarat semua penyetelan berbasis data berikutnya).
2. **Nyalakan Jalur 2 secara tergating** — registrasi IVSP economist/general sesuai vonis frontier 18 Nov (minReward 0,6), sesudah pencatatan biaya per verdict dibangun di runner (menutup lubang §8-#9 untuk lane itu).
3. **Pra-terbang bahan bakar sebagai gerbang nyala** — status neuron Cloudflare + kesehatan lane penulis/relay dibaca sebelum unit dinyalakan; kalibrasi diberi anggaran terpisah dari produksi (menutup K8).
4. **Perkuat uji sitasi ke dukungan pinpoint** — klaim poros harus didukung teks sumber pada titik yang dikutip, bukan sekadar pengenal ter-resolve (menutup K1 tanpa melonggarkan risiko falsified K2).
5. **Liveness sadar-lane** — samakan perlakuan liveness dengan gerbang kesegaran yang sudah sadar-lane, agar tiket TELAT marathon tidak terveto aturan warisan (menutup K13; perubahan desain doktrin = wilayah user).
6. **Perbaiki pencatatan fallback** — setiap transisi rantai penulis masuk log terstruktur (lane, alasan, hasil), bukan stderr (menutup celah W3).
7. **Evaluasi routing penulis per kelas pertanyaan** (menutup satu-satunya kelas C) — hanya sesudah data buku besar #1 cukup untuk menilai, bukan berdasar tebakan.

---

## 14. HAL YANG MEMBUTUHKAN KEPUTUSAN USER

1. **Registrasi IVSP Jalur 2** — kata jalan (gerbang urutan frontier sudah terpenuhi: Expert dibayar +80). Termasuk postur pilot 14 hari dari vonis frontier.
2. **Kursi penengah/cadangan rantai pemeriksa** — tetap menunggu kolam CrowLLM (sol/gemini) pulih, atau menunjuk pengganti dari kolam yang hidup (nemotron-ultra / k2-horizon / qwen-3.8-27b; grok hidup tetapi pernah user buang dari kursi frontier — menghidupkannya perlu kata user eksplisit).
3. **Pemasangan gpt-oss-CF lapis 4** rantai pemeriksa (tersertifikasi 7/7, belum ter-wire — parkir sejak pagi).
4. **Liveness sadar-lane** — mengubah perilaku gerbang warisan berdasarkan bukti uji asap (wilayah terkunci: gerbang).
5. **Nyala batch penuh Jalur 1** sesudah reset generasi 07:00 WIB 19 Nov, dengan prosedur recheck lapangan + QA teknis/kompetitif terpisah (addendum T3) — kata nyala belum diberikan.
6. **Anggaran kalibrasi vs produksi** untuk kuota bersama (neuron Cloudflare + relay CrowLLM) — kebijakan pemisahan yang diusulkan auditor + W5-P9.
7. **Cek sisi-operator NIU** (Jalur 3) — user sebagai pengirim pertanyaan ke platform; jalur tetap dormant-EV sampai ada bukti P1/P3.

---

*Investigasi selesai. Sesuai perintah user, laporan berhenti di sini — tidak ada satu pun rekomendasi di atas yang dijalankan. Seluruh angka akun di laporan ini adalah tarikan live 18 Nov 2026 malam (terakhir 23:44 WIB) dan dapat berubah oleh verdict yang masih berjalan (22 jawaban lama + 1 jawaban pilot masih menunggu panel).*
