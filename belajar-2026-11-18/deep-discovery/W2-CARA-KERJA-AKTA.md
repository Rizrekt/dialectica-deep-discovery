# W2 — CARA KERJA AKTUAL AGENT.AkTa DI DIALECTICA

**Lini:** Deep Discovery W2 (perintah user 18 Nov 23:38 WIB) — investigasi READ-ONLY: kode, log, dan laporan operasional ditelusuri; tidak ada konfigurasi diubah, tidak ada serve/answer/submit dijalankan, tidak ada API model dipanggil.
**Tanggal susun:** 2026-11-18 malam WIB.
**Disiplin bukti:** `[KODE: berkas:baris/fungsi]` = dibaca dari source sesi ini · `[LOG: berkas/tanggal]` = record log/notifikasi · `[LAPORAN: berkas]` = laporan operasional di disk · `[INFERENSI]` = simpulan penelusur, bukan bukti langsung.

---

## 0. PETA BESAR DALAM SATU PARAGRAF

AGENT.AkTa **tidak** menjawab pertanyaan lewat chat. Yang berjalan adalah rantai program lokal: **systemd unit → `run_serve.py` (launcher+supervisor kita) → `trued.py` v0.22.4 (klien resmi Dialectica, "stok") → tiga hook kita (`vyce_serve_prepare.py` / `vyce_serve_ready.py` / `vyce_serve_provider.py`) → `vyce_serve_common.vyce_pipeline` → penulis model (Vyce/GLM + rantai fallback) → gerbang berlapis (`serve_gate.py` dkk.) → cache di disk**. Klien stok yang melakukan polling pencarian, klaim (thread terpisah), dan pengiriman jawaban lewat gateway Matrix milik Expert. Muse (operator) **tidak berada di dalam loop per-pertanyaan**: peran Muse adalah pra-terbang, memasang/menyalakan unit, mengawasi log, menghentikan, memverifikasi keadaan akhir lewat API, dan melaporkan. Model AI hanya menyentuh dua hal: menulis draf (penulis) dan memeriksa draf (pemeriksa C5/rantai). Keputusan ambil/lewati sepenuhnya kode deterministik kita (doktrin + gerbang), bukan penilaian model dan bukan penilaian Muse saat runtime.

Tiga contoh nyata yang dipakai sebagai tulang bukti di seluruh dokumen:

- **Pilot 17 Nov** — 5 jawaban terkirim (semua Pioneer viso-0, penulis GLM), 3 draf tertahan K-2, 10 target gugur liveness [LAPORAN: NYALA-PILOT-2026-11-17.md]. Empat dari lima **dibayar +70** pada 18 Nov malam (Innovator +10 ×4, Marathon +10 ×3) [LOG: notifikasi `achievement_unlocked` dibaca live 18 Nov 23:23 WIB].
- **Mini-batch 18 Nov pagi** — 0 terkirim dari 3 izin: poller menyajikan 12 baris tak-terklasifikasi (kolam doktrin tidak pernah tersentuh), 9 generasi terbakar ditahan gerbang, 1 klaim gugur oleh veto kesegaran pasca-klaim, 1 klaim ditolak platform "at capacity", ekornya slash REL-005 [LAPORAN: NYALA-DOKTRIN-A-2026-11-18.md].
- **Uji asap 18 Nov malam** — sesudah perbaikan kolam: 48/48 baris tersaji = tiket terklasifikasi doktrin; 47 gugur liveness pra-generasi; 1 tiket (`b1a89a69`) menembus seluruh pipa sampai generasi lalu mati di bahan bakar penulis (Cloudflare 429 neuron habis); counter tetap 9/10, nol klaim [LAPORAN: UJI-1-TEMBAKAN-2026-11-18.md].

---

## LANGKAH 1 — KONEKSI KE DIALECTICA

**Yang benar-benar terjadi.** Ada dua kredensial berbeda yang tidak pernah tercampur:

1. **Sesi operator** — token sign-in disimpan di berkas `~/.dialectica/session`; klien membacanya dan mengirimnya sebagai header `X-Active-Session` ke basis `https://dialectica.xyz` pada setiap panggilan API node [KODE: trued.py:22–23, TOKEN_PATH :84, `token()` :122]. Isi berkas tidak pernah dicetak oleh alat mana pun dalam pipa kita; yang dibaca program hanyalah mekanismenya (baca berkas → header). Umur sesi ±7 hari; dua kode error tertentu berarti "sesi tidak bisa dipakai lagi" dan klien menjawab dengan petunjuk sign-in ulang [KODE: trued.py:410–414].
2. **Kredensial kerja Expert** — sesudah Expert terprovisioning, pekerjaan (cari/klaim/jawab) berjalan dengan kredensial Expert sendiri lewat gateway-nya; token sesi **tidak** dikirim pada panggilan kerja [KODE: trued.py:27, `credential_only_state()` — serve boleh lanjut tanpa sign-in yang masih hidup bila Expert tersimpan sudah `configured` dan kredensial kerjanya diterima deployment].
3. **Kunci provider model** — `run_serve.py` mengambil kunci Vyce sebagai *surrogate* vault (`dynamic_credential_entry("custom.vyce", "access_token")`) dan menyuntikkannya sebagai env `VYCE_API_KEY` ke proses anak; kunci asli ditukar saat egress dan tidak pernah menyentuh disk [KODE: run_serve.py docstring + `main()`]. Lane free-pool (OpenRouter/Cloudflare/DashScope/Z.ai) tidak disuntik kunci — klien konektor masing-masing mengambil surrogate-nya sendiri [KODE: run_serve.py `ANSWER_ONLY_LANES`].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Memverifikasi sesi hidup sebelum nyala (`trued.py status` + `agent show` dibaca saat pra-terbang) [LAPORAN: NYALA-PILOT §1; UJI-1 §1] |
| **CLI / sistem Dialectica** | `trued.py` membaca berkas sesi, memasang header, menolak basis URL non-https, membuang header sesi saat redirect lintas-origin [KODE: trued.py:87–114] |
| **Model AI** | Tidak ada peran di langkah ini |
| **Perlu tindakan user** | Sign-in awal dan sign-in ulang saat sesi kedaluwarsa (±7 hari) — token hanya bisa lahir dari alur connect-agent user; tidak bisa dibuat operator |
| **Mode gagal + penanganan** | Sesi mati di tengah masa tunggu: serve tidak start, nol tembakan tak disengaja; sesi di disk **selamat dari restart VM** (yang hilang hanya unit di /etc) — terbukti dua kali pada 18 Nov [LAPORAN: NYALA-DOKTRIN-A §3 insiden pra-start; UJI-1 §2]. Penanganan: pasang ulang unit dari salinan induk, baca ulang saldo sebagai bukti sesi utuh |

---

## LANGKAH 2 — INISIALISASI EXPERT

**Yang benar-benar terjadi.** Inisialisasi adalah fungsi klien stok `ensure_expert()`, idempoten: bila state lokal (`~/.dialectica/agent.json` — metadata + kredensial Expert, isinya tidak dicetak) cocok akun/host/kredensial, Expert lama dipakai ulang ("Reusing agent …") [LOG: serve-2026-11-17.log baris awal]. Bila belum ada: provisioning lewat `POST /api/node/agents/matrix {"type":"ISP"}` lalu `credential/reveal`, Expert baru lahir **pull-only** (tidak ada strategi pendorong), cap awal `DEFAULT_DAILY_ANSWER_CAP` dipasang segera, dan konfigurasi strategi ditunda ke serve/answer pertama karena server menolak mengonfigurasi agent yang belum pernah terhubung [KODE: trued.py `ensure_expert()` :4128, `_provision()` ±:4077–4085, `configure_new_expert()` :4237]. Satu serve per mesin dikunci (`_hold_serve_lock`) supaya dua salinan tidak berebut gateway [KODE: trued.py `cmd_serve()` :5187].

Expert kita sudah ada sejak lama dan tidak pernah dibuat ulang oleh nyala mana pun: **8522c990-d4f6-4155-a326-3c3c9802b950**, nama **AGENT.AkTa**, strategy **dynamic**, arena general, maxConcurrency **1**, contextWindowTokens 160.000, caps server unlimited [LAPORAN: NYALA-PILOT §1(a); UJI-1 §1].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Membaca identitas saat pra-terbang dan mencocokkannya dengan jangkar (id, nama, strategi, tidak suspended) — mismatch = berhenti [LAPORAN: UJI-1 §4 pemicu berhenti (c)] |
| **CLI / sistem Dialectica** | `ensure_expert` + provisioning + kunci serve tunggal; server menolak konfigurasi untuk agent yang belum pernah connect |
| **Model AI** | Tidak ada peran |
| **Perlu tindakan user** | Tidak ada dalam operasi normal. (Pembuatan Expert tambahan = wilayah keputusan user dan tidak pernah dilakukan pipa ini) |
| **Mode gagal + penanganan** | Expert hilang di server (`ExpertGone`) → satu kali percobaan ulang dengan registrasi baru, tidak loop [KODE: trued.py `cmd_serve()` :5187–5198]. Akun tanpa akses Expert → sesi read-only tetap jalan, bukan error [KODE: trued.py `ensure_expert()` docstring] |

---

## LANGKAH 3 — MENEMUKAN QUESTION

**Yang benar-benar terjadi.** Di bawah strategi **dynamic**, platform **tidak mengirim apa pun** — tidak ada push, tidak ada sweep, tidak ada notifikasi pekerjaan. Klien stok yang berputar mencari sendiri: `trued serve --every 1m` menjalankan pencarian berkala (lantai klien 30 detik; bawaan 300 detik; jendela pencarian wajib dibatasi kata kunci atau umur, bawaan 1 hari) [KODE: trued.py komentar :4400–4427, `DEFAULT_SEARCH_EVERY_MS`/`MIN_SEARCH_EVERY_MS`]. Filter pencarian datang dari argv unit systemd. **Sesudah perbaikan kolam 18 Nov**, ExecStart adalah `arenaIds=general questionMinAgeMs=7200000 questionMaxAgeMs=21600000` (pita umur 2–6 jam, **tanpa** `q=wallet`) — diselaraskan ke kolam doktrin [KODE: provider/dialectica-serve.service ExecStart + header rekonsiliasi]. Sebelum perbaikan, filter lama (`q=wallet`, maks 3 hari) menyajikan kolam yang irisannya dengan klasifikasi doktrin **nol** — akar kegagalan mini-batch [LAPORAN: NYALA-DOKTRIN-A §3; PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md].

Pendampingnya, **pengamat doktrin** (`rate_trigger.py`) berjalan sebagai proses terpisah read-only: polling peluang tiap 45 detik, mengambil daftar ISO pertanyaan muda, dan mengklasifikasikannya ke trigger store (lihat Langkah 4) [KODE: rate_trigger.py `run_observer()` :178, `observe_once()` :102]. Pengamat tidak mengklaim apa pun.

| Peran | Isi |
|---|---|
| **Muse sendiri** | Menjalankan pengamat lebih dulu sebelum serve start (supaya kolam terklasifikasi saat serve menyajikan) dan mengawasi log pencarian [LAPORAN: UJI-1 §1–§2] |
| **CLI / sistem Dialectica** | Polling pencarian `trued serve`; server menjawab daftar baris peluang; rate-limit platform dijawab klien dengan menunggu sesuai instruksi server |
| **Model AI** | Tidak ada peran — penemuan murni query indeks |
| **Perlu tindakan user** | Tidak ada |
| **Mode gagal + penanganan** | (a) HTTP 429 `M_LIMIT_EXCEEDED` dari platform → klien menunggu 5 detik sesuai perintah lambat server, bukan anomali [LOG: serve-2026-11-17.log; UJI-1 §3]. (b) Halaman habis dicoba → log "everything that matched has already been tried", serve masuk loop cari-ulang 60 detik [LAPORAN: NYALA-DOKTRIN-A §3]. (c) Pengamat mati karena restart VM → klasifikasi yang sudah tertulis di store selamat; pengamat dijalankan ulang di giliran yang sama [LAPORAN: UJI-1 §2] |

---

## LANGKAH 4 — KEPUTUSAN AMBIL / LEWATI (jantung sistem)

**Di sinilah keputusan benar-benar terjadi** — bukan di model, bukan di Muse, melainkan di hook `DIALECTICA_PREPARE_CMD` kita, `vyce_serve_prepare.prepare_row()`, yang dipanggil klien stok dengan baris pencarian sebagai JSON di stdin **sebelum klaim apa pun ada**. Exit 0 = boleh klaim; exit nonzero = lewati tanpa biaya [KODE: trued.py `_attempt()` :4640–4685; vyce_serve_prepare.py `prepare_row()`]. Urutan gerbang di dalam prepare:

1. **Kewarasan baris** — id + teks pertanyaan wajib ada.
2. **Liveness** (`serve_gate.liveness_gate_for_row`) — detail ISR di-fetch; filter tiga-field membuktikan ronde maraton masih hidup; fetch gagal = fail-closed (lewati, biayanya nol) [KODE: serve_gate.py `liveness_check()` :229, `liveness_gate_for_row()` :324].
3. **Keputusan lane Doktrin A** (`_doctrine_lane_decision`, hanya saat `DIALECTICA_DOCTRINE_A=1`) — membaca **ulang** trigger store pada setiap panggilan (keputusan tidak pernah di-cache di sisi kita) dan mencatat setiap keputusan ke log append-only `doctrine-decision-log.jsonl`: tak-terklasifikasi → **lewati fail-closed**; mode TUNGGU → lewati; TELAT belum due / jatah lane habis → lewati; CEPAT jatah habis → lewati [KODE: vyce_serve_prepare.py `_doctrine_lane_decision()`; doctrine_a.py `log_decision()` :393].
4. **Gerbang sekuensing klaim Q4** (`_job_sequence_block`) — daftar job Expert dibaca; ada job sebelumnya yang belum terminal (`completed/failed/cancelled/abandoned`) **atau** daftar tak terbaca → baris ditahan [KODE: vyce_serve_prepare.py `_job_sequence_block()`].
5. **Layar kesegaran pra-klaim Q3** (`_preclaim_freshness_screen`) — aturan kesegaran detik-kirim yang sama dijalankan atas payload saat-pilih, dicatat dengan `phase="pra-klaim"`; ruangan yang sudah mati saat dipilih dilewati sebelum generasi membakar jatah [KODE: vyce_serve_prepare.py `_preclaim_freshness_screen()`; freshness_gate.py `check_freshness()` :284].

Baru sesudah lima lapis itu generasi berjalan (Langkah 5–6) dan gerbang mutu menilai draf (Langkah 7). Hanya draf *sendable* yang menulis cache + mengambil token lane; kegagalan generasi tidak membakar jatah lane [KODE: vyce_serve_prepare.py `prepare_row()` ekor].

**Klasifikasinya sendiri** dibuat pengamat dari rekonstruksi timestamp ISO: hitungan jawaban dalam 120 detik pertama sejak lahir — ≤5 → **CEPAT**; ≥11 → **TELAT** (banjir); di antaranya → **TUNGGU**, diputus ulang pada +30 menit (laju lanjutan <2/menit DAN posisi ≤10 → CEPAT, selain itu TELAT) [KODE: doctrine_a.py :84–91, `classify_inflow()` :173, `reevaluate_wait()` :192]. Tiket TELAT diparkir di `late-queue.json` dengan jendela lepas lahir+2 s.d. +6 jam; jatah harian CEPAT 3 / TELAT 7 dari cap 10 [KODE: doctrine_a.py `park()` :269, `lane_remaining()` :363, `FAST_DAILY_CAP`/`LATE_DAILY_CAP` :94–95]. Veto zona terlarang (tunda 2–120 mnt + posisi 11–60 + terklasifikasi banjir) hidup di pemilih/kesegaran [KODE: doctrine_a.py `forbidden_zone()` :212].

Di sisi klien stok: baris yang dilewati prepare masuk skip sesi **6 jam** (`PREPARE_SKIP_TTL_S`) — jahitan ini **tidak bisa ditimpa bersih dari lapisan kita** dan tercatat sebagai keterbatasan terukur [KODE: trued.py :2988; PERBAIKAN-KOLAM-DOKTRIN §7]. Klaim sendiri berjalan di thread terpisah (`claim_opportunity` → `POST /api/node/agents/{id}/process-opportunity`), maks 3 percobaan per ronde, karena panggilan klaim bersifat blocking dan balasan offer-to-answer harus dijawab loop polling yang sama [KODE: trued.py :4404–4413, `claim_opportunity()` :4458, `MAX_CLAIM_ATTEMPTS_PER_ROUND`].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Tidak memutuskan per baris saat runtime. Peran Muse: merancang/memasang aturan (di bawah persetujuan user), membaca log keputusan sesudahnya, menghentikan nyala bila pola menyimpang dari izin |
| **CLI / sistem Dialectica** | Memanggil prepare hook per baris, menerapkan skip 6 jam, menjalankan thread klaim, menjawab assigned/declined/refused |
| **Model AI** | **Tidak ada peran dalam keputusan ambil/lewati.** Klasifikasi doktrin = aritmetika timestamp; gerbang = aturan deterministik |
| **Perlu tindakan user** | Mengubah ambang/aturan (K-2, CROWD_CAP, jatah lane, mode gerbang) = wilayah terkunci user; runtime tidak mengubahnya |
| **Mode gagal + penanganan** | (a) **Kolam tak beririsan** (mini-batch): 12/12 baris tak-terklasifikasi lewat alur warisan, 9 generasi terbakar, doktrin tak pernah terpicu → diperbaiki: fail-closed + filter serve diselaraskan; bukti perbaikan 48/48 [LAPORAN: NYALA-DOKTRIN-A §3; UJI-1 §3]. (b) **Liveness pola flag basi**: ronde sudah lewat tapi flag maraton basi — 10 pass-over di pilot, **47 dari 48** di uji asap; penanganan memang veto pra-generasi (nol generasi terbakar), tetapi konsekuensi strukturalnya: release TELAT +2 jam hampir selalu pasca-ronde → pertanyaan desain terbuka, bukan diubah dari dalam uji [LAPORAN: UJI-1 §6.2]. (c) **Klaim ditolak kapasitas**: lihat Langkah 8 |

---

## LANGKAH 5 — QUESTION DITERUSKAN KE MODEL

**Yang benar-benar terjadi.** Ada dua jalur prompt, dan serve tergating memakai yang pertama:

- **Jalur prepare (utama):** `csc.prompt_from_row(row)` merakit prompt dari baris pencarian, lalu `vyce_pipeline(prompt, isr_id)` [KODE: vyce_serve_prepare.py `prepare_row()`; cloudflare_serve_common.py]. Kontrak format serve (`SERVE_FORMAT_CONTRACT`, penanda `OPERATOR ANSWER CONTRACT`) ditempel tepat satu kali [KODE: vyce_serve_common.py `generate_vyce()`].
- **Jalur job (fallback/koreksi):** saat job tiba, klien stok merakit prompt resmi (`build_provider_prompt`: pertanyaan + aturan arena + jawaban terdahulu + konteks kebaruan) dan memanggil `DIALECTICA_PROVIDER_CMD` dengan prompt di **stdin** [KODE: trued.py `build_provider_prompt()` :1928, `run_provider()` :2897]. Prompt tidak pernah lewat argv — payload pertanyaan orang asing hanya di stdin [KODE: trued.py `run_hook()` docstring].

Di dalam `vyce_provider.py`, prompt ditambah **steering bertahap per-ISR** (dicocokkan lewat env `DIALECTICA_ISR_ID`) sebelum dikirim ke model [KODE: vyce_provider.py `main()` ±:200]. Konteks kebaruan (blok jawaban terdahulu yang tahan-potong, lantai cakupan COVER_FLOOR=8) disiapkan `novelty_context.py` dan dikonsumsi tahap semantik [KODE: serve_gate.py `_with_novelty_context()` :1160].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Tidak menyentuh prompt per pertanyaan saat runtime; kontrak format + steering adalah artefak yang dipasang sebelumnya |
| **CLI / sistem Dialectica** | Merakit prompt resmi di jalur job; memanggil provider sebagai subprocess stdin→stdout |
| **Model AI** | Menerima prompt; belum menghasilkan apa pun di langkah ini |
| **Perlu tindakan user** | Tidak ada |
| **Mode gagal + penanganan** | Prompt kosong tanpa cache siap → provider exit 2, job tidak dijawab paksa [KODE: vyce_serve_provider.py `main()`]. Generasi menggantung dibatasi `GEN_TIMEOUT_S=1200` dtk di lapisan kita (di bawah batas prepare klien 3600 dtk) → timeout menjadi pass-over, bukan hook macet [KODE: vyce_serve_common.py :GEN_TIMEOUT_S] |

---

## LANGKAH 6 — MODEL MENGHASILKAN ANSWER

**Yang benar-benar terjadi.** Generasi berjalan sebagai subprocess `vyce_provider.py` (prompt stdin, jawaban stdout, kunci dari env). Rantai kandidat penulis: **glm-5.3-flash utama** di Vyce (rantai bisa dipin persis lewat `VYCE_MODEL_CHAIN`); respons kosong sesudah reasoning overflow → kandidat berikut dicoba, bukan dikirim [KODE: vyce_provider.py `candidate_models()` :54, `call_vyce()` :115, `main()` :178–328]. Setiap generasi tercatat di `token-usage.jsonl` dengan label lane (`vyce-serve`) — catatan inilah yang dihitung cap [KODE: vyce_provider.py `_log_usage()` :79].

Di atasnya ada **rantai fallback penulis lintas-provider (R1)**: Vyce/GLM → gpt-oss-120b via Vyce (promo $0) → gpt-oss-120b via Cloudflare. Kegagalan total satu lane menyerahkan prompt yang sama ke lane berikut; rantai bersifat stateful (tetap di lane yang selamat); setiap perpindahan tercatat di stderr sebagai `fallback: <lane> gagal → <lane>` [KODE: vyce_serve_common.py `WriterFallback`, `default_writer_fallbacks()`]. Wrapper boleh meregenerasi **maks 1 kali** untuk panjang, lewat lane yang sama [KODE: vyce_serve_common.py `vyce_pipeline()`].

**Cap keras di kode:** `generate_vyce` menolak **sebelum membakar** bila `serve_generations_today() >= 10` (dihitung dari record lane `vyce-serve` hari UTC berjalan) [KODE: vyce_serve_common.py `serve_generations_today()`, `generate_vyce()`]. Supervisor `run_serve` untuk lane §39 melakukan hal setara lewat SIGINT di cap; untuk lane Vyce tergating, penegak cap-nya adalah penghitung ini + pengawasan operator [KODE: run_serve.py `supervise_serve()`; vyce_serve_common.py blok komentar audit S4].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Tidak menulis draf. Mengawasi counter generasi dari log saat nyala (dan watcher pengaman pada uji asap — Langkah 9) |
| **CLI / sistem Dialectica** | Tidak ada peran dalam generasi (klien hanya memanggil provider) |
| **Model AI** | GLM-5.3-flash menulis; gpt-oss-120b menulis bila rantai jatuh. Pemeriksa belum berjalan di langkah ini |
| **Perlu tindakan user** | Tidak ada |
| **Mode gagal + penanganan** | (a) **GLM kolaps stokastik** (konten kosong) → rantai fallback; bukti nyala: token-usage 18 Nov memuat vyce-serve glm ×7 + gpt-oss-120b ×2 [LOG: token-usage.jsonl 2026-11-18]. (b) **deepseek-v4.1 mati di Vyce (HTTP 403, lite tier)** → dikeluarkan dari rantai 17 Nov karena mengubah kolaps yang bisa pulih menjadi gagal total [KODE: vyce_provider.py :16–20]. (c) **Bahan bakar Cloudflare habis (429, alokasi 10.000 neuron/hari)** → error terminal rantai: mini-batch 03:20 UTC dan uji asap `b1a89a69` sama-sama mati di sini; generasi gagal **tidak** tercatat di token-usage dan counter tidak bergerak [LAPORAN: NYALA-DOKTRIN-A §3; UJI-1 §3] |

---

## LANGKAH 7 — PEMERIKSAAN ANSWER PRA-KIRIM

**Yang benar-benar terjadi.** Semua pemeriksaan berjalan di dalam `serve_gate.gate_answer()` atas draf yang baru lahir, **sebelum klaim** (jalur prepare) — draf yang ditahan tidak pernah menjadi job. Lapisan-lapisannya, sesuai urutan kode:

1. **Wrapper klaim** (`openrouter_wrapper.wrap_answer`): audit temuan, lantai panjang per kelas (Pioneer 1.717 / umum 3.000 / Marathon 4.500 karakter), **lantai K-2 = rasio token angka-terikat-sitasi ≥ 0,30**, gerbang format (g) harus LOLOS; status harus OK dan **nol temuan tak-ber-span** — konservatisme fail-closed yang disengaja [KODE: serve_gate.py `gate_answer()` :1556; vyce_serve_common.py `vyce_pipeline()` docstring].
2. **Detektor jejak berpikir + penutup sumber menghindar (E3)** — temuan digabung ke daftar audit; satu temuan tak-tertambal = tidak sendable [KODE: serve_gate.py `detect_thinking_trace()` :403, `detect_evasive_source_closing()` :510, `gate_answer()`].
3. **C5 semantik (self-VFP)** — pemeriksa utama **Nemotron** (lane OpenRouter kita) menilai draf melawan aturan arena server; mode berjalan saat ini **SHADOW** (keputusan user): vonis dicatat, tidak pernah menahan. Dalam mode block pun tahap ini hanya menahan lewat flag `block` miliknya [KODE: serve_gate.py `armed_semantic_check()` :1197, `semantic_check()` :1009, `semantic_mode()` :651].
4. **Rantai pemeriksa cadangan** (`chained_semantic_check`, ter-arm `DIALECTICA_CHECKER_CHAIN=1`): **qwen-3.8-max** (CrowLLM) menyala hanya bila utama *unavailable* atau utama *clean*; sengketa diputus **gpt-5.6-sol** (CrowLLM) 2-dari-3; penengah mati → vonis utama berdiri + `dispute_unresolved` tercatat; **semua lane mati = tak-terukur** (`performed=False, block=False` — tidak lolos sebagai clean, tidak pula menahan). Yang menyeberang relay hanya teks pertanyaan (blok kebaruan dilucuti) + draf — prompt publik kalibrasi, bukan rubrik internal [KODE: serve_gate.py `chained_semantic_check()` :1295; crowllm_checker.py].
5. **Verifikasi sitasi mekanis** (`citation_verify`, bawaan **block**): penunjuk presisi poros (DOI/URL/nomor dokumen) di-resolve ke registry/host hidup; penunjuk mati/format salah/dokumen salah pada klaim poros = tahan [KODE: serve_gate.py `armed_citation_check()` :1234; citation_verify.py].
6. **Verifikasi isi dua tahap** (`content_verify`, bawaan **block**): tahap 1 mekanis — token presisi klaim poros harus hadir di teks sumber ter-fetch (CAPTCHA/bot-wall = tak-terverifikasi); tahap 2 entailment Nemotron (maks 6 panggilan/draf); klaim poros *unsupported* = fatal [KODE: serve_gate.py `armed_content_check()` :1261; content_verify.py].

Setiap tahap menulis lognya sendiri: `semantic-check-log.jsonl` (20 record), `citation-check-log.jsonl` (26), `content-check-log.jsonl` (24), `freshness-check-log.jsonl` — dihitung dari berkas per 18 Nov malam [LOG: keempat berkas di provider/].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Tidak menilai draf saat runtime. Kalibrasi pemeriksa (drill berlabel) adalah pekerjaan sesi terpisah di bawah izin, bukan bagian nyala |
| **CLI / sistem Dialectica** | Tidak ada peran — gerbang seluruhnya lapisan kita di atas klien |
| **Model AI** | Nemotron (utama C5 + entailment isi), qwen-3.8-max (cadangan), gpt-5.6-sol (penengah) — ketiganya **memeriksa**, tidak menulis |
| **Perlu tindakan user** | Mode gerbang (shadow/block), nilai K-2, komposisi rantai = keputusan user; tercatat sebagai wilayah terkunci |
| **Mode gagal + penanganan** | (a) Pemeriksa crash → tahap melaporkan diri *unperformed*, `block=False` — crash pemeriksa tidak pernah membunuh draf bagus [KODE: serve_gate.py `gate_answer()` blok semantic/citation]. (b) **"C5 clean" bukan verifikasi sitasi** — terbukti di spot-check pilot: draf lolos C5-shadow clean tetap memuat apparatus sitasi karangan (DOI salah, pasal karangan); itulah alasan lapis 5–6 dipasang sebagai block terpisah [LAPORAN: SPOTCHECK-PILOT-2026-11-17.md; SPOTCHECK-SISA-PILOT-2026-11-17.md]. (c) Tahan gerbang = pass-over bersih: pilot menahan 3 draf di K-2 (rasio 0,000 / 0,048 / 0,111) [LAPORAN: NYALA-PILOT §3]; mini-batch menahan isi ×3, K-2 ×2, sitasi+isi ×1 [LAPORAN: NYALA-DOKTRIN-A hasil satu baris] |

---

## LANGKAH 8 — PENYERAHAN KE DIALECTICA

**Yang benar-benar terjadi.** Penyerahan punya tiga segmen yang terpisah tegas:

1. **Siap** — prepare exit 0 menulis teks lolos-gerbang ke cache bersama di disk (`csc.write_cache(isr_id, text)`) [KODE: vyce_serve_prepare.py `prepare_row()` ekor]. Pada langkah offer-to-answer, hook `DIALECTICA_READY_CMD` menjawab exit 0 **hanya** bila cache untuk pertanyaan itu ada — bid tanpa jawaban siap di-veto [KODE: vyce_serve_ready.py (identik §39); trued.py komentar :2958–2966].
2. **Klaim** — thread klaim memanggil `process-opportunity`; hasil dibedakan tiga: `assigned` / `declined` (kita menolak di langkah akhir) / `refused` (server menolak) [KODE: trued.py `claim_opportunity()` :4458].
3. **Kirim** — job tiba sebagai event gateway Matrix (`execute-job`); `handle_job` menjalankan provider: **cache-hit** → teks cache dicetak persis (tanpa generasi ulang, tanpa gerbang ulang), tetapi dua veto detik-kirim tetap berjalan di momen cetak — liveness terbukti-mati dan **gerbang kesegaran** (`freshness_gate.armed_freshness_veto`, bawaan block; keadaan tak terbaca = tahan). Veto/exit 1 stdout kosong = klien **men-drop job** tanpa mengirim apa pun. Teks lalu dikirim lewat gateway dengan kredensial Expert (`gw_send_threaded_text`) [KODE: vyce_serve_provider.py `main()`; trued.py `handle_job()` ±:5592–5650]. Server memvalidasi **sesudah** kirim dan bisa meminta koreksi skema (job `correction` menjalankan jalur provider live, bukan cache) [KODE: trued.py `report_outcomes()` docstring :4309]. Bukti kirim di log: `→ submitted for <jobId> (N chars) — awaiting validation` [LOG: serve-2026-11-17.log :16, :27, :43, :65, :86 — kelima job pilot].

Untuk jalur one-shot `trued answer`, hasil akhir dibaca dengan polling daftar job sampai terminal; kode keluar adalah bukti: **0** semua completed / **1** ada gagal / **3** `EXIT_UNKNOWN` / **4** `EXIT_DECLINED` (kita melewati) [KODE: trued.py :4289–4300, `report_outcomes()` :4309]. `run_serve.py` mencetak rc itu dengan lantang dan meneruskannya [KODE: run_serve.py `main()` ekor].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Mengawasi baris `submitted` di log serve dan menghitung kiriman lawan izin (kill-metric dihitung operator, bukan kode) |
| **CLI / sistem Dialectica** | Klaim, transport gateway, validasi pasca-kirim, koreksi skema — semua klien/server; lapisan kita hanya memasok teks lewat hook |
| **Model AI** | Tidak ada peran (teks sudah final dari cache) |
| **Perlu tindakan user** | Tidak ada per kiriman; jumlah tembakan per nyala adalah izin user yang dijaga operator |
| **Mode gagal + penanganan** | (a) **Veto pasca-klaim menahan kirim** (mini-batch, `a9408129`): draf lulus prepare, job `68be9cbe` ter-klaim, lalu gerbang kesegaran detik-kirim menahan (viso-0 tetapi kerumunan 79 ≥ garis 20) → job di-drop, **ISO intent `e3287902` tertinggal di server tanpa isi**, slot konkurensi tunggal terkunci ±30 menit [LAPORAN: NYALA-DOKTRIN-A §3]. (b) **Klaim berikutnya ditolak platform** "Agent at capacity (1/1)" untuk `556b8068` selagi slot masih diduduki job drop itu [LOG: serve-2026-11-18.log :94]. Mitigasi yang kemudian dipasang: layar pra-klaim Q3 + gerbang sekuensing Q4 (Langkah 4) memindahkan kedua kegagalan ini ke **sebelum** klaim. (c) **Ekor reliabilitas:** job ter-klaim yang ter-drop adalah spesies "pertanyaan menyerah" yang dihukum platform — notifikasi `user_suspended` "Slash from rule REL-005 (suspension #6)" tercatat 2026-11-18T03:31:51Z, ±3 menit sesudah unit mini-batch berhenti; reliability −5 → −6 [LOG: notifikasi API dibaca live 18 Nov 19:09/23:23 WIB; KODE: trued.py komentar :2950–2956 menamai biaya REL-005 untuk Question yang diserahkan] |

---

## LANGKAH 9 — PEMANTAUAN STATUS VERIFIKASI

**Yang benar-benar terjadi — dan ini temuan strukturalnya: TIDAK ADA watcher verdict otomatis.** Tidak ada cron Dialectica (dihapus user 17 Nov), tidak ada unit systemd pemantau verdict, dan klien stok sendiri hanya mem-poll status **job** sampai terminal pada saat exit one-shot — bukan verdict ISO [KODE: trued.py `report_outcomes()` :4309]. Pemantauan verdict selama ini adalah **tarikan read-only manual oleh operator/sesi utama** memakai `verifier/verifier_common.api_get()` — modul yang sengaja hanya punya GET, tanpa helper tulis [KODE: provider/verifier/verifier_common.py header + `api_get()`]. Endpoint yang dibaca: `/api/node/isos/{id}` (status + support/refutasi), `/api/node/isr/{id}`, `/api/node/agents/{id}/jobs`, `/api/node/notifications`, `/api/node/scores`.

Satu-satunya "watcher" yang pernah berjalan adalah `watcher_uji1.py` pada uji asap — pengaman counter generasi (poll 3 detik, bunuh unit bila counter mencapai 10), one-shot untuk satu nyala, **bukan** pemantau verdict [KODE: provider/watcher_uji1.py docstring].

Bukti cara kerja manualnya: VERDICT-WATCH-2026-11-17.md adalah satu kali cek bertanggal (10:10–10:16 WIB) yang menemukan kelima jawaban pilot masih `revealed`, panel 0 support / 0 refutasi / 0 intent — verdict belum mulai sama sekali ±7 jam sesudah submit terakhir [LAPORAN: VERDICT-WATCH-2026-11-17.md]. Latensi verdict nyata: jawaban pilot terkirim 17 Nov 02:37–03:02 UTC; pembayaran mendarat 18 Nov 15:10–16:18 UTC — **±36 jam** kemudian, dan hanya diketahui karena sesi utama membaca notifikasi malam itu [LOG: notifikasi `achievement_unlocked` 18 Nov 15:10–16:18 UTC].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Melakukan cek verdict secara manual saat sesi berjalan (tarikan API primer per item) dan melaporkannya; kill-metric (falsified pertama = serve OFF + JEDA + bedah) dieksekusi operator, bukan otomatisasi |
| **CLI / sistem Dialectica** | Menyediakan endpoint baca; tidak ada pemberitahuan verdict yang di-push ke klien serve |
| **Model AI** | Tidak ada peran |
| **Perlu tindakan user** | Tidak ada untuk membaca; keputusan reaksi atas verdict (jeda/lanjut) berada di rezim yang disetujui user |
| **Mode gagal + penanganan** | (a) **Verdict tak terpantau saat tidak ada sesi aktif** — konsekuensi langsung desain manual: 22 jawaban lama + 5 pilot pernah berada di kolam assigned-unconcluded tanpa pengamat berkelanjutan [INFERENSI dari struktur di atas + LAPORAN: NYALA-PILOT §5.6]. (b) Status job ≠ verdict: job `completed` hanya berarti kirim diterima mesin, bukan jawaban verified — mencampur keduanya adalah kesalahan baca yang dihindari dengan membaca detail ISO per item [KODE: trued.py `report_outcomes()` docstring: "Sending an answer is not acceptance"] |

---

## LANGKAH 10 — MENGETAHUI REWARD DITERIMA

**Yang benar-benar terjadi.** Reward tidak diumumkan oleh status ISO semata — verified biasa membayar **$0**. Sinyal reward yang otoritatif ada dua, keduanya dibaca manual:

1. **Notifikasi `achievement_unlocked`** — setiap pembayaran kanal membawa `delta`, `ruleId`, `isoId`, `isrId`. Pembayaran pilot terbaca persis begini: 7 event pada 18 Nov 15:10–16:18 UTC — `TRUED-002` "Innovator! You earned 10 $TRUED for a novel verified answer" ×4 dan `TRUED-014` "Marathon winner!" ×3, masing-masing delta **+10** [LOG: `/api/node/notifications` dibaca live sesi utama 18 Nov 23:23 WIB].
2. **Skor akun** — `GET /api/node/scores`: coins **−1,8788 → 68,1212**, lifetimeEarned **0 → 70**, expertise general **0 → 8** pada bacaan yang sama [LOG: `/api/node/scores` 18 Nov 23:23 WIB]. Perintah `trued status` membungkus hal yang sama sebagai "one-call session opener: reward balances + unread notifications digest" [KODE: trued.py `cmd_status()` :672].

Rekonsiliasi penuh sesudahnya (audit sesi utama 18 Nov 23:27 WIB): seluruh pergerakan koin seumur akun = 13 peristiwa notifikasi + pasangan netting kredit-bertanya/penalti; Jalur 1 **+70** adalah satu-satunya penghasil; Jalur 3 neto −1,8788; Jalur 2 = 0 (belum pernah dinyalakan) — jumlah akhir persis 68,1212 [LAPORAN: audit rekonsiliasi sesi utama 18 Nov 23:27 WIB, tercatat di log harian].

| Peran | Isi |
|---|---|
| **Muse sendiri** | Membaca notifikasi + skor, merekonsiliasi lawan riwayat, melaporkan angka terverifikasi ke user (bukan dari tangkapan layar) |
| **CLI / sistem Dialectica** | Server mencatat achievement, mengkreditkan koin, memperbarui skor; klien hanya membaca |
| **Model AI** | Tidak ada peran |
| **Perlu tindakan user** | Tidak ada — $TRUED saat ini belum bisa diekspor (paymentsEnabled false pada bacaan fitur terakhir); reward adalah posisi internal sampai platform membuka ekspor |
| **Mode gagal + penanganan** | (a) Membaca saldo saja tanpa notifikasi menyembunyikan *kanal* asal uang — rekonsiliasi mewajibkan keduanya dibaca [INFERENSI dari struktur event di atas]. (b) Kenaikan RAR/reputation bisa terjadi **tanpa** pembayaran (dinamika platform; RAR 125→127 pada malam uji asap dengan nol aksi kita) — RAR bukan bukti reward [LAPORAN: UJI-1 §5] |

---

## DAFTAR MODE GAGAL TERBUKTI (dengan kejadian nyatanya)

| # | Mode gagal | Kejadian nyata (bukti) | Penanganan yang berdiri |
|---|---|---|---|
| 1 | Jejak berpikir mentah terkirim verbatim → falsified | ISO `f0bb3586` (38.591 kar) pada serve Vyce tanpa hook, era pra-gerbang [KODE: run_serve.py docstring; vyce_serve_common.py docstring] | Arsitektur prepare/ready/provider tergating + detektor trace di `gate_answer` |
| 2 | Menjawab ronde yang sudah berakhir (jebakan §82) | 10 pass-over pilot; 47/48 baris uji asap [LAPORAN: NYALA-PILOT §3; UJI-1 §3] | Gerbang liveness fail-closed pra-generasi di prepare + re-cek saat cache-hit |
| 3 | Kolam serve ≠ kolam doktrin (diskoneksi struktural) | Mini-batch: 12/12 baris tak-terklasifikasi, 113 tiket parkir tak pernah tersaji, 9 generasi terbakar [LAPORAN: NYALA-DOKTRIN-A §3] | Jahitan kolam: filter ExecStart = pita 2–6 jam + prepare fail-closed; terbukti 48/48 [LAPORAN: UJI-1 §3; PERBAIKAN-KOLAM-DOKTRIN] |
| 4 | Veto kesegaran **pasca**-klaim menjatuhkan job | `a9408129` → intent `e3287902` yatim + slot terkunci ±30 mnt [LAPORAN: NYALA-DOKTRIN-A §3] | Layar pra-klaim Q3 + gerbang sekuensing Q4 memindahkan veto ke sebelum klaim [KODE: vyce_serve_prepare.py] |
| 5 | Penolakan kapasitas platform (1/1) | `556b8068`, log serve 18 Nov baris 94 [LOG: serve-2026-11-18.log :94] | Sama dengan #4; klaim tidak ditumpuk di atas job non-terminal |
| 6 | Slash reliabilitas REL-005 dari job ter-drop | Notifikasi suspensi #6, 18 Nov 03:31:51Z; reliability → −6 [LOG: notifikasi API 18 Nov] | Menghindari klaim yang berpotensi diserahkan: Q3/Q4 + veto detik-kirim tetap sebagai lapis terakhir |
| 7 | Bahan bakar penulis habis (neuron Cloudflare 429) | Mini-batch 03:20 UTC; uji asap `b1a89a69` 14:13 UTC [LAPORAN: NYALA-DOKTRIN-A §3; UJI-1 §3] | Belum ada penegak pra-terbang otomatis — tercatat sebagai butir pra-terbang menentukan untuk nyala berikutnya [LAPORAN: UJI-1 §6.3] |
| 8 | Penulis utama kolaps stokastik | GLM kosong → gpt-oss tercatat menulis 2 dari 9 generasi 18 Nov [LOG: token-usage.jsonl 2026-11-18] | Rantai fallback R1 lintas-provider, stateful [KODE: vyce_serve_common.py `WriterFallback`] |
| 9 | Lane penulis mati permanen (403) | deepseek-v4.1 di Vyce [KODE: vyce_provider.py :16–20] | Dikeluarkan dari rantai (17 Nov) |
| 10 | Draf ditahan gerbang mutu (K-2 / sitasi / isi) | Pilot 3 draf; mini-batch 6 tahan tercatat [LAPORAN: NYALA-PILOT §3; NYALA-DOKTRIN-A §3] | Memang desain: pass-over tanpa biaya klaim; angka poros harus terikat sumber |
| 11 | Restart VM menghapus unit /etc + membunuh pengamat | Dua kali pada 18 Nov (pra-start mini-batch ±02:15 UTC; pra-start uji asap ±12:44 UTC) [LAPORAN: NYALA-DOKTRIN-A §3; UJI-1 §2] | Unit dipasang ulang dari salinan induk workspace di giliran yang sama; sesi + store + counter selamat karena hidup di workspace/`~/.dialectica` |
| 12 | Rate-limit pencarian platform (429) | Berulang di kedua nyala 18 Nov [LOG: serve-2026-11-18.log; LAPORAN: UJI-1 §3] | Klien mematuhi perintah lambat server (tunggu 5 dtk) |
| 13 | Kolam relay pemeriksa mati (503 per-provider) | Sapuan 62 model CrowLLM 18 Nov malam: Gemini 12/12 mati, OpenAI arus utama mati — qwen-3.8-max + gpt-5.6-sol (cadangan + penengah rantai) ikut mati malam itu [LAPORAN: belajar-2026-11-18/frontier-transfer-direktif/CROWLLM-LIVENESS-2026-11-18.md] | Desain rantai: semua lane mati = tak-terukur, tidak memblokir, tercatat keras [KODE: serve_gate.py `chained_semantic_check()` aturan 4] |
| 14 | Skip prepare 6 jam klien stok menelan tiket | Keterbatasan terukur, belum terpicu merugikan pada uji asap [KODE: trued.py :2988; LAPORAN: UJI-1 §6.5] | Penghitung `count_lost_after_skip()` di doktrin untuk mengukur dari run nyata [KODE: doctrine_a.py :451] |
| 15 | Verdict datang sangat telat / tak terpantau | Pilot: ±36 jam submit→bayar; verdict-watch murni manual [LAPORAN: VERDICT-WATCH-2026-11-17.md; LOG: notifikasi 18 Nov] | Tidak ada otomatisasi — cek manual sesi utama; inilah celah operasional terbesar yang masih terbuka |

---

## CATATAN KEJUJURAN PENELUSURAN

- Angka "9 generasi terbakar" mini-batch dan rincian tahan-gerbangnya diambil dari laporan nyala (yang disusun dari log serve + token-usage pada hari itu), bukan dihitung ulang sesi ini; hitungan silang sesi ini atas `token-usage.jsonl` 18 Nov (vyce-serve glm ×7 + gpt-oss ×2 = 9) **cocok** dengannya [LOG: token-usage.jsonl].
- Record `doctrine-decision-log.jsonl` saat ini memuat tepat **1 baris** — `proceed/due` untuk `b1a89a69` — konsisten dengan klaim "record pertama" di laporan uji asap; keputusan pass mini-batch terjadi **sebelum** lipatan frontier Q2 memasang pencatatan keputusan, sehingga tidak ada di log ini [LOG: doctrine-decision-log.jsonl; KODE: vyce_serve_prepare.py header FRONTIER FOLD].
- Satu record `freshness-check-log.jsonl` fase `pra-klaim` (status `fresh`, `b1a89a69`) terverifikasi langsung dari berkas sesi ini, berdampingan dengan 26 record rezim detik-kirim/tak-berfase [LOG: freshness-check-log.jsonl].
- Isi `~/.dialectica/session` dan `agent.json` tidak dibuka untuk isi kredensialnya; hanya mekanisme baca dan nama berkasnya yang dirujuk, sesuai batasan tugas.
