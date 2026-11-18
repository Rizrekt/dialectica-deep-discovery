# W1 — MEKANIK PLATFORM + STRATEGI EARNING (Deep Discovery, 2026-11-18 malam)

Lini investigasi W1 untuk perintah user 18 Nov 23:38. READ-ONLY mutlak: tidak ada config/model/strategi diubah, tidak ada serve/answer/submit/create, tidak ada panggilan API model. Sumber: ledger `MEKANISME-DAN-LAPANGAN.md` (disebut "MEKANISME §n"), dokumen resmi klien v0.22.4 (`SKILL.md`, `references/rules-of-the-game.md`, `references/arenas.md`, `references/api.md` di `skill-audit/pkg/dialectica/`), `PETA-EARN-LIVE-2026-11-18.md`, `PETA-DIALECTICA-2026-11-17.md`, `BREAKDOWN.md`, `BREAKDOWN-TUJUAN.md`, `QUALITY.md`, dan tarikan live read-only 2026-11-18 ±23:4x WIB (leaderboard, analytics general+forecasting, scores).

Konvensi tag: **[LIVE tgl]** terverifikasi dari API primer · **[RESMI: file §]** dokumentasi resmi proyek · **[OPERASIONAL]** pengalaman operasi akun ini · **[INFERENSI]** turunan/penafsiran berlabel · **[HIPOTESIS]** belum teruji.

---

# BLOK §1 — DIALECTICA SECARA MENYELURUH

## 1.1 Apa platform ini, dan apa tujuannya

Dialectica adalah marketplace pengetahuan terverifikasi adversarial: Customer mengajukan **Question**, **Expert** bersaing memberi **Answer**, **Verifier** independen mencoba **memfalsifikasi** Answer itu; Answer yang selamat menjadi **Verified Answer** dan bentuk awetnya adalah halaman **Wiki** publik yang bisa disitasi. Seluruh proses (siapa menjawab, siapa mencoba membantah, kenapa gagal) tercatat di ledger yang bisa diaudit — nilai jualnya adalah Answer yang lolos pengawasan independen, bukan sekadar hasil pencarian atau opini satu model. [RESMI: rules-of-the-game.md "What is Dialectica"]

Mata uang internalnya **$TRUED**: poin kontribusi yang menentukan posisi leaderboard (leaderboard mengurutkan **Lifetime Earned**, bukan saldo) dan menggerbang badge. [RESMI: SKILL.md Workflow 2; MEKANISME §25.1] Status nilai riilnya per hari ini: ekspor on-chain **belum tersedia**, tidak ada harga pasar, kontrak token, rate konversi, atau tanggal TGE yang dipublikasikan; proyek menyebut dirinya pre-seed, MVP live. [OPERASIONAL: BREAKDOWN-TUJUAN §10; MEKANISME §20.4b, §23.5] Feature flag live pagi ini: `paymentsEnabled=false` — $TRUED yang terkumpul **belum bisa dicairkan**; earning ≠ withdraw. [LIVE 2026-11-18 pagi: PETA-EARN "Jalur mati/bukan jalur"]

## 1.2 Hubungan antar-entitas

- **Customer** = penanya. Lewat skill ini user biasanya Customer (search/read/ask), dan bisa sekaligus menjadi Expert. [RESMI: rules-of-the-game.md "What this skill's user is"]
- **Question (ISR)** = milik tepat satu Arena; harus lolos Aturan Question arena itu + cek kebaruan (duplikat ditolak dan diarahkan ke Answer yang sudah ada). [RESMI: rules-of-the-game.md "The playing field"; arenas.md]
- **Expert (ISP)** = agent bermodel milik user yang menjawab Question orang lain untuk $TRUED. Satu mesin = satu Expert (dibuat server-side saat `signin`); satu akun bisa punya >1 Expert, tapi dompet + level RAR adalah milik **user**, dibagi semua agent-nya. [RESMI: SKILL.md Workflow 3; OPERASIONAL: MEKANISME §13.1 untuk dinding 1-mesin-1-Expert; AUDIT-5-PILAR 17 Nov untuk dompet/RAR per-user]
- **Answer (ISO)** = jawaban yang diserahkan Expert atas sebuah Question; wajib menjawab langsung, menyitasi sumber, membuka penalaran untuk diperiksa, dan bisa diverifikasi. [RESMI: rules-of-the-game.md]
- **Verifier (IVSP)** = penilai independen; verifikasinya (VFP) adalah verdict mendukung/membantah atas Answer lawan Aturan Verifikasi arena. [RESMI: rules-of-the-game.md]
- **Verified Answer (VISO)** = Answer dengan verdict verified; bentuk sitabelnya = halaman Wiki. Lawannya **FISO** = Answer terfalsifikasi — falsifikasi bersifat publik dan menjelaskan alasannya. [RESMI: rules-of-the-game.md tabel terminologi]
- **Aturan konflik kepentingan (keras):** user tidak boleh menjawab Question-nya sendiri dan tidak boleh memverifikasi Answer-nya sendiri; cek berjalan di level **user pemilik**, bukan agent/klien yang dipakai. [RESMI: rules-of-the-game.md "Conflict-of-interest rules"]

## 1.3 Bagaimana Question masuk ke marketplace

1. Customer menulis draf; pembuatan digerbang **Question Assistant** percakapan yang memoles draf sampai lolos Aturan Question arena (General: Q_CLARITY, Q_GOOD_FAITH, Q_NON_TRIVIAL, Q_PROHIBITED; Forecasting: QF_RESOLVABLE dengan Clairvoyance Test, QF_TIME_BOUND, QF_FALSIFIABLE, QF_PROHIBITED). Draf yang dinilai duplikat dari Question yang ada **ditolak**, bukan ditanya ulang. [RESMI: SKILL.md Workflow 2; arenas.md]
2. Saat draf `ready`, Question dibuat dalam run yang sama, **Fee** dipotong dari Wallet, dan URL Question terbit. Fee adalah harga pekerjaan adversarial yang digerakkan Question itu — dibayar ke platform, **bukan** ke Expert; Fee tidak pernah mengurangi Lifetime Earned. [RESMI: SKILL.md Workflow 2]
3. Question unik memberi penanya **+1 $TRUED** saat dibuat, dan +1 lagi per Answer di Question itu yang lolos cek **NIU** (Novelty, Inventiveness, Utility) — di Forecasting hanya sesudah Question resolve, hanya untuk Answer yang terbukti benar dan masih Verified. [RESMI: rules-of-the-game.md "Rewards"]
4. Sesudah terbit, Question terbuka untuk dijawab Expert mana pun yang eligible di arenanya (lihat 1.4); "settled" di luar Forecasting **bukan** berarti tertutup — Marathon baru masih bisa berjalan dan dimenangkan di atasnya. [RESMI: SKILL.md "What the row means"]

## 1.4 Bagaimana Expert mendapatkan pekerjaan

Ada dua bentuk kedatangan kerja, ditentukan strategi Expert [RESMI: SKILL.md Workflow 3]:

- **Pushed work** (semua strategi kecuali `dynamic`): platform mencocokkan Question ke Expert dan **mengirimkannya**; `serve` tinggal menjawab yang diberikan. Mekanik transportnya: Expert dibuat via `POST /api/node/agents/matrix {type: ISP}` → credential bootstrap satu kali → koneksi Matrix; orchestrator mengirim event bid di room, klien membalas skor fitness, lalu event penugasan berisi prompt; jawaban dikirim sebagai pesan thread. [OPERASIONAL: MEKANISME §1.1–1.2, dari pembacaan kode klien v0.22.4]
- **Dynamic work** (`dynamic`): platform **tidak mengirim pekerjaan apa pun**. Sesi `serve` yang berjalan harus **mencari sendiri** lewat `opportunities` (filter server-side: kata kunci `q`, umur Question, viso/fiso, status marathon, arena, dll), memilih kandidat, dan **meminta** untuk diberi Question itu. Sesi dynamic yang berhenti mencari = berhenti menghasilkan, diam-diam, tampak persis seperti sesi idle. [RESMI: SKILL.md Workflow 3 + api.md "Agent operations"]
- **Klaim satu pertanyaan** (`trued answer <isrId>`): mengambil satu Question pilihan, menjawab, putus — end-by-itself. Hasil klaim berakhir salah satu dari: *taken on* (dikerjakan), *passed on* (Expert menolak di cek akhir karena format arena tidak bisa diproduksi klien — aman, tidak menghabiskan apa pun), *not given* (platform menolak: kapasitas penuh, cap harian tercapai, Expert lain lebih dulu, atau Question terlalu panjang untuk context window yang dideklarasikan). [RESMI: SKILL.md "Answer one Question"]
- **Fakta mekanis yang membatalkan teks skill:** klaim satu-pertanyaan hanya bekerja di bawah `dynamic`; di bawah strategi pushed, server menolak dengan pesan bahwa Expert "receives work automatically and cannot request work itself" — bertentangan dengan kalimat SKILL.md "Any strategy can do this"; server yang menang. [OPERASIONAL: MEKANISME §9.2]
- **Caps adalah config Expert, bukan kuota platform:** Expert yang dibuat skill mulai dengan plafon 20 jawaban/24 jam dan bisa diset `none` (tanpa batas); platform menegakkan angka yang dipasang pemilik. Cap menghitung ISR yang **disentuh** dalam jendela geser 24 jam — termasuk serve yang gagal — bukan jawaban yang settle. [RESMI: SKILL.md "Answer one Question"; OPERASIONAL: MEKANISME §10, §24.3]
- Pekerjaan dibatasi juga oleh **maxConcurrency** (kita: 1) dan jendela hidup job: satu Answer punya **15 menit** untuk digenerate sebelum dianggap abandoned. [RESMI: SKILL.md Workflow 3 "Time limit"]

## 1.5 Bagaimana Answer diproses dan diverifikasi

1. **Penyerahan.** Jawaban dikirim sebagai pesan thread di room job; klien lalu mem-poll endpoint jobs resmi (`GET /api/node/agents/{id}/jobs`, otorisasi = work credential agent itu sendiri) — status terminal server: `completed / failed / cancelled / abandoned`. Satu-satunya pembaca resmi status itu adalah `report_outcomes()` di dalam serve; tidak ada subcommand CLI untuk jobs. [OPERASIONAL: MEKANISME §1.3]
2. **Saringan pertama — Surprise Gauge.** Answer yang mengulang yang sudah ada gugur di sini **sebelum** isi diperiksa: baris `para:N` di opportunities = Answer yang ditandai paraphrasing; verifikasi berhenti di Gauge untuk mereka, jadi status paraphrasing tidak mengatakan apa-apa tentang benar/salah isinya. [RESMI: SKILL.md "What the row means"]
3. **Panel verifikasi.** Answer yang lolos Gauge ditugaskan ke panel Verifier independen yang memeriksanya lawan Aturan Answer arena (General: keluarga A_* — sitasi, penalaran, cakupan, ketidakpastian). Ambang verdict dari esai resmi platform: **Verified = 2 verifikasi mendukung; 1 verifikasi membantah = falsified.** [RESMI: BREAKDOWN-TUJUAN §10, dari esai resmi + /why + /earn; konsisten dengan rules-of-the-game.md]
4. **Dua tahap yang menentukan nasib (temuan studi kita):** verdict bukan antrean satu tahap melainkan corong dua tahap — *panel ditugaskan* → *panel menyimpulkan*. Di era banjir hanya **32,6%** jawaban yang pernah dipegang ≥2 verifier (vs 85,9% pra-banjir); jawaban yang tidak pernah ditugaskan tidak akan pernah ber-verdict, berapa pun mutunya. Penugasan panel era banjir **tidak menyaring mutu** — terbalik: jawaban panjang/bersitasi/novel justru lebih jarang ditugaskan; satu-satunya saringan yang terlihat adalah volume author. Mekanik penyimpulan yang terkonfirmasi = **sapuan berkala lintas kanal**: entrant awal era banjir menyimpulkan median 4,22 jam, entrant telat ≥6 jam menyimpulkan median 0,03 jam di kanal panel yang sama — fase masuk terhadap sapuan yang menentukan, bukan keanggotaan marathon. [OPERASIONAL: STUDI-ANTREAN-VERDICT-2026-11-18 Q1–Q3; IMPLEMENTASI-DOKTRIN-A §3]
5. **Marathon.** Verifikasi berjalan sampai Question settle ("the marathon"); di pertanyaan settled, ronde Marathon berkala memilih Answer verified **terakhir** saat jendela ditutup sebagai Marathon Winner — jendela marathon terukur persis **500 detik** di sampel juara; satu Question bisa membayar Marathon berkali-kali (751 slot awarded di 210 pertanyaan sampel; ±3,6 per pertanyaan). [RESMI: rules-of-the-game.md "Rewards"; OPERASIONAL: MEKANISME §26.3]
6. **Waktu khas lapangan:** jawaban pertama ±2,8 detik; verified ±85 detik; marathon ±8,4 menit; rata-rata 6 Answer masuk sebelum ada yang verified; 3 verifikasi per Verified Answer (bacaan awal platform). [OPERASIONAL: BREAKDOWN-TUJUAN §2] Di era banjir angka ini tidak berlaku untuk jawaban yang tidak ditugaskan panel (lihat butir 4).

## 1.6 Bagaimana reward dihitung dan diberikan

Prinsip resmi: Expert dibayar hanya untuk Answer **Verified**, proporsional ke **isi informasi** Answer itu. [RESMI: rules-of-the-game.md] Bentuk terukurnya — hanya **tiga slot pemenang** yang membayar di jalur Expert [OPERASIONAL: MEKANISME §25.1, terverifikasi dari tabel /earn live + wiki token-economics + esai resmi]:

| Slot | Nilai | Syarat persis |
|---|---|---|
| **Pioneer** | **+20** | Answer terverifikasi **pertama** pada sebuah Question; hanya 1 per Question selamanya; **tetap milik walau Answer itu belakangan difalsifikasi**; tidak berlaku di Forecasting |
| **Innovator** | **+10** | Answer verified yang lolos Surprise Gauge/NIU: konten baru **≥15%** di atas yang sudah verified |
| **Marathon Winner** | **+10** | Answer verified terakhir saat jendela Marathon sebuah Question ditutup; dibayar saat marathon conclude |
| Verified, tidak novel | **0** | Lolos verifikasi tapi tidak menambah informasi baru |
| Falsified | **−1 saldo** + potong Expertise arena itu | Lihat 1.8 |

- **Penumpukan slot** (satu Answer memanen Pioneer+Innovator+Marathon sekaligus): **belum terbukti** — tidak ada dokumen yang menyatakannya; jangan dihitung dalam EV apa pun. [OPERASIONAL: MEKANISME §25.1] Fakta penutup hari ini menunjukkan dua achievement berbeda (Innovator dan Marathon) bisa mendarat untuk Answer yang sama pada menit berbeda — lihat 1.10 — tapi apakah itu "penumpukan slot" dalam arti desain payout atau dua kanal independen, tidak dinyatakan dokumen mana pun. [INFERENSI dari notifikasi 18 Nov]
- **Tidak ada pengali strategi/arena atas payout.** Perbedaan $/unit antar strategi di analitik adalah efek **seleksi pekerjaan** (strategi menentukan pekerjaan apa yang sampai ke Expert), bukan pengali angka. RAR & Expertise juga **tidak mengalikan** payout — fungsinya gerbang (lihat 1.7). [OPERASIONAL: MEKANISME §25.1]
- **Reward Verifier** menurun menurut urutan kedatangan: formula esai resmi `max(0,1, sqrt(2^(1−x)))` dengan x = urutan kedatangan verdict — verifier pertama paling mahal per unit; dibayar untuk verdict yang **selaras dengan hasil akhir**. [OPERASIONAL: MEKANISME §25.4, dari esai resmi platform]
- **Reward penanya:** +1 per Question unik saat dibuat; +1 per Answer lolos NIU di Question itu (aturan di 1.3). Fee bertanya = `10(n−1)³/((n−1)³+13³)`, n = Question berbayar **seumur hidup**, tidak pernah reset, plafon mendekati 10. [RESMI: SKILL.md Workflow 2 + api.md §Fee]
- **Forecasting = escrow:** reward di arena itu ditahan sampai Question resolve terhadap hasil dunia-nyata; analitiknya sendiri menyatakan "$TRUED figures read low until Questions resolve" (`rewardsDeferredToSettlement=true`). [LIVE 2026-11-18 malam: analytics forecasting, coverage notes]
- Pemberian reward terbaca sebagai notifikasi `achievement_unlocked` (Innovator/Marathon) dan `ask_fee_charged` (fee), dan terrekonsiliasi persis di saldo — lihat audit 1.10.

## 1.7 Expertise, Arena, RAR, reputasi — hubungannya

- **Expertise** = skor per-arena milik user (akun kita: general). Naik dari pekerjaan terverifikasi dan dari membuat Question (+1 per Question terukur di akun kita); **turun dipotong setiap Answer falsified** di arena itu. [RESMI: rules-of-the-game.md "Falsified Answers cost the Expert Expertise score in that Arena"; OPERASIONAL: MEKANISME §22 — 7 Question memberi Expertise general 0→7; §97 — falsified serve memotongnya kembali ke 0]
- **Arena** = ruang domain yang menetapkan aturan Question/Answer/Verifikasi dan eligibility per peran; angka strategi **hanya bisa dibandingkan di dalam satu Arena** — beda Arena = beda permainan. [RESMI: api.md "Arena analytics"; arenas.md]
- **RAR** = skor gabungan **Reliability, Availability, Reputation** milik user. Bad-faith engagement dan reliabilitas buruk menurunkannya, memicu **eksklusi bertingkat sampai ban permanen**. [RESMI: rules-of-the-game.md] **Formula numerik RAR dan ambang suspensi tidak dipublikasikan di mana pun** — yang terbaca dari API hanya tiga komponennya. [OPERASIONAL: BREAKDOWN-TUJUAN §10] Bacaan live akun kita malam ini: reliability **−6**, availability **34**, reputation **107** → RAR **135**. [LIVE 2026-11-18 malam: /api/node/scores]
- **Rank leaderboard ditentukan Lifetime Earned**, bukan RAR dan bukan saldo; reliability negatif ada di **semua** baris papan atas (live malam ini: −7 s.d. −731) — reliabilitas bukan mata uang rank, tapi untuk akun baru tanpa bantalan volume completed, reliabilitas negatif + suspensi adalah risiko eksklusi nyata. [LIVE 2026-11-18 malam: /api/node/leaderboard; OPERASIONAL: MEKANISME §3]
- **Fungsi gerbang, diringkas:** RAR buruk → eksklusi (menghentikan SEMUA penghasilan); Expertise → menggerbang badge; Lifetime Earned → rank + badge (badge digerbang Lifetime Earned, bukan Expertise). [OPERASIONAL: MEKANISME §25.1; RESMI: SKILL.md Workflow 2]

## 1.8 Aturan yang membuat Expert kehilangan reputasi / terkena penalti

1. **Job diambil tapi tidak selesai = pelanggaran reliabilitas termahal.** Pemicu terdokumentasi di SKILL.md: early stop, DROPPED, REJECT (model menolak), abandon 15 menit (generate melewati batas), kegagalan berulang. Panduan Earn resmi: "Reliability drops if an Answer is started and never delivered." [RESMI: SKILL.md Workflow 3; OPERASIONAL: BREAKDOWN-TUJUAN §10]
2. **REL-005** = kode slash reliabilitas server-side untuk job yang diambil tapi tidak pernah mencapai status terminal `completed` tepat waktu (abandoned adalah pemicu yang terbukti). Ia **tidak terdokumentasi** di notifikasi/changelog/blog/kode klien — definisi di atas adalah satu-satunya yang konsisten dengan data. Tangga sanksinya: slash reliabilitas → suspensi sementara → eksklusi naik → ban permanen. [OPERASIONAL: MEKANISME §1.5, §25.6]
3. **Bukti di akun kita:** 6/6 job era pra-disiplin (8 Nov) berakhir abandoned (koneksi mati di tengah siklus sebelum `report_outcomes` membaca status) → REL turun, 3 suspensi hari itu juga; total suspensionCount akun kini **6**, termasuk slash REL-005 baru 18 Nov 10:31:51 WIB (suspensi #6, 4 detik, reliabilitas −5→−6) yang hampir pasti biaya ekor satu job ter-drop dari veto pasca-klaim mini-batch pagi itu. [OPERASIONAL: MEKANISME §2; LIVE 2026-11-18: notifikasi user_suspended 03:31:51Z]
4. **Falsified:** −1 $TRUED dari saldo + potongan Expertise arena itu, per kejadian. (Klaim "−50" yang beredar di kanal pihak ketiga = palsu, direfutasi trail platform + fetch /earn langsung.) [OPERASIONAL: MEKANISME §25.1]
5. **Menolak Question (REJECT/declined)** juga memberi pekerjaan itu kembali dan **mengurangi reliabilitas** — jalan keluar resmi dari Question yang tidak bisa dijawab tetap berbiaya; *passed on* di cek format (sebelum klaim) yang tidak berbiaya. [RESMI: SKILL.md Workflow 3 "Declining a Question" + "Answer one Question"]
6. **Self-dealing** (jawab Question sendiri / nilai Answer sendiri) dilarang di level pemilik akun — pelanggaran konflik kepentingan, risiko eksklusi. [RESMI: rules-of-the-game.md]
7. Yang **tidak** menghukum: klaim yang *not given* (ditolak platform sebelum pekerjaan diambil) tidak menghabiskan apa pun; Answer yang tidak pernah ditugaskan panel tidak memberi penalti — ia hanya tidak menghasilkan. [RESMI: SKILL.md; OPERASIONAL: §1.5 butir 4 di atas]

## 1.9 Answer berkualitas vs Answer biasa — pembeda terukur

Dari analitik arena + studi korpus juara (bukan selera) [OPERASIONAL: MEKANISME §26.4; QUALITY.md pendahuluan]:

- **Lolos Surprise Gauge dulu, baru dinilai.** Penolakan platform terbesar adalah `surprise_gauge` — live malam ini **68,5%** dari semua penolakan general (112.979 kejadian), disusul `arena_rules` 30,8%. Answer "benar tapi mengulang" mati sebelum isinya dibaca. [LIVE 2026-11-18 malam: analytics general rejectionReasons]
- **Sitasi yang bisa diverifikasi pembaca.** Di dalam kegagalan arena_rules, **A_CITATION = 92,2%** dari aturan yang gagal (44.461 kejadian, live malam ini); berikutnya A_REASONING 36,7%, A_SCOPE 31,2%, A_UNCERTAINTY 19,3% (satu penolakan bisa gagal di beberapa aturan). Aturan resminya: klaim reportase wajib sitasi sumber yang bisa diidentifikasi jelas dan mendukung klaim saat dicek; gaya APA + URL diutamakan; **teks dari Question BUKAN sumber**. [LIVE 2026-11-18 malam: analytics general failedRules; OPERASIONAL: BREAKDOWN-TUJUAN §5]
- **Bentuk korpus juara:** jawaban verified eksternal (n=4.440, 165 agen): header markdown 79%, URL sitasi 77–100%, median panjang pemenang 4,7–11,7 ribu karakter; pembuka = tesis/distingsi tajam atau koreksi premis (≤3 kalimat), badan ##/### bernomor, penutup menyebut apa yang baru. [OPERASIONAL: MEKANISME §26.4; QUALITY.md (a)–(c)]
- **Kalibrasi ketidakpastian dinyatakan** (A_UNCERTAINTY adalah aturan gagal resmi) dan cakupan menjawab **semua** sub-pertanyaan (A_SCOPE). [RESMI: arenas.md melalui ruleChecklist; OPERASIONAL: QUALITY.md (h)]
- **Angka poros harus ter-entail sitasinya** — sitasi harus *menyatakan* angka spesifik yang diklaim, bukan sekadar ada di dekatnya (sub-cek E1 rubrik kita; lahir dari 3–4 kasus falsified kita sendiri yang berakar persis di sini). [OPERASIONAL: QUALITY.md (d)/E1]
- Sebaliknya, Answer biasa yang mati: parafrase verified yang ada (gugur Gauge), sitasi karangan/tidak mendukung (gugur A_CITATION), atau tidak pernah ditugaskan panel sama sekali (mati diam — lihat 1.5.4).

## 1.10 Bagaimana sistem menilai informasi baru, kontribusi orisinal, dan jawaban yang sudah ada

- **Surprise Gauge / NIU** adalah pengukur kebaruan resmi: minting $TRUED digerbang Surprise Gauge `I(x) = −log2 P(x)` (esai scarcity resmi); Answer sesudah Pioneer hanya dibayar bila lolos Gauge — ambang terukurnya **≥15% konten baru** di atas yang sudah verified; di bawah itu diklasifikasikan **Paraphrasing** dan gugur (parameter strategi `maxParaphrasing` menyaring di sisi Expert). [OPERASIONAL: BREAKDOWN-TUJUAN §10; MEKANISME §25.1; RESMI: SKILL.md "What the row means" untuk para:N]
- **Yang dibandingkan adalah yang sudah VERIFIED**, bukan semua jawaban: `viso:N` pada sebuah Question = berapa Verified Answer yang harus dilampaui kebaruan Answer baru; `fiso:N` tinggi menandai Question yang sulit dijawab benar, bukan Question kosong. [RESMI: SKILL.md "What the row means"]
- **Kebaruan dinilai relatif terhadap keadaan saat masuk, dan verdict-nya relatif terhadap fase sapuan** — studi antrean kita: penentu verdict = kerumunan-saat-masuk (≈ posisi masuk), era Question, dan penugasan panel; **kedalaman akhir (berapa jawaban masuk sesudah kita) TIDAK menentukan apa-apa**. [OPERASIONAL: STUDI-ANTREAN-VERDICT-2026-11-18 Q1/Q4]
- **Duplikat di sisi Question** dicegah di gerbang pembuatan (cek kebaruan asisten; duplikat diarahkan ke Answer yang ada). [RESMI: SKILL.md Workflow 2 "Duplicate handling"]
- **FAKTA PENUTUP HARI INI (bukti sistem bekerja persis seperti di atas):** 4 Answer pilot 17 Nov dibayar total **+70** pada 18 Nov 22:10–23:18 WIB — Innovator +10 ×4 (edc2bf0a, d0c2b089, 7b00324a, 8eece8ab) dan Marathon +10 ×3 (tiga yang pertama); Answer ke-5 (8300bcbe, fabrikasi sitasi terberat versi spot-check kita) tidak dibayar. Audit notifikasi seumur akun: **88 notifikasi = 13 peristiwa koin** (7 achievement +10, 6 fee bertanya −1,8788 total) + kredit pembuatan +7 dan penalti falsified −7 yang saling meniadakan di luar notifikasi — rekonsiliasi **persis** ke saldo 68,1212 dan lifetimeEarned 70 pada cek 23:24 WIB. [LIVE 2026-11-18: /api/node/scores + /api/node/notifications, audit sesi utama 23:23–23:24]
- **Gerak sesudahnya (dicatat apa adanya):** tarikan lini ini ±23:4x WIB membaca coins **78,1212**, lifetimeEarned **80**, Expertise general **9** — ada **satu peristiwa +10 lagi** sesudah audit 23:24. Atribusi persisnya (Answer dan slot mana) **tidak terverifikasi** dalam himpunan endpoint yang diizinkan lini ini. [LIVE 2026-11-18 malam: /api/node/scores; INFERENSI: satu achievement +10 tambahan, konsisten dengan pola Innovator/Marathon]

---

# BLOK §5 — ANALISIS STRATEGI EARNING (tanpa rekomendasi)

## 5.1 Arena yang tersedia + karakteristiknya

Eligibility per peran [LIVE 2026-11-18 pagi: PETA-EARN tabel arena; feature flags + katalog arena]:

| Arena | Bertanya | Expert | Verifier | Karakter |
|---|---|---|---|---|
| **general** | anyone | anyone | **anyone** | standard; arena pengetahuan "why/how", aturan Q_* dan A_* |
| **forecasting** | **admin** | anyone | **anyone** | prediksi resolusi dunia-nyata; marathonTurns 1000, consensus 2; reward **escrow** sampai resolve |
| **hle** | admin | admin | admin | benchmark internal (Humanity's Last Exam) — tertutup untuk akun non-admin di semua peran |

Ukuran lapangan live malam ini [LIVE 2026-11-18 malam: analytics pulse]:

- **general:** 4.417 Question (0 tanpa Verified Answer), 325.491 Answer, 64.714 verified, 32.635 falsified, 353.705 verifikasi.
- **forecasting:** 455 Question, 14.268 Answer, 3.929 verified, 3.274 falsified, 21.213 verifikasi.
- **hle:** tidak ditarik lini ini (tertutup); per-unit Expert-nya 16,05–23,01 — tertinggi di platform tapi subsidi arena admin. [LIVE 2026-11-18 pagi: PETA-EARN]

## 5.2 Bagaimana Expert memilih Arena

Arena Expert adalah **config di platform** (`trued agent set arenas=general`), bukan pilihan per-job: nilai `arenas` membatasi tawaran/pencarian ke arena itu saja; membiarkannya `(all)` membiarkan semua arena masuk — termasuk jebakan skema Forecasting (format jawaban prediksi terstruktur: answerType/outcomeType/prediction/confidence; esai markdown gagal validasi → koreksi berulang → jendela hidup habis → abandoned). [RESMI: SKILL.md Workflow 3; OPERASIONAL: MEKANISME §4, §9/§12 BREAKDOWN-TUJUAN] Konfigurasi akun kita saat ini: arenas=general, strategy dynamic, caps server unlimited, maxConcurrency 1. [OPERASIONAL: keadaan akun 18 Nov]

## 5.3 Strategi entry — apa saja dan bagaimana kerjanya

Strategi menentukan **bagaimana pekerjaan tiba dan pekerjaan mana yang disaring**; parameter bimbingannya diterbitkan server per strategi (`trued agent strategies`) dan harus dikutip dari server, bukan disintesis — dilarang mengarang "skor kelayakan" sendiri dari baris opportunities. [RESMI: SKILL.md "What the row means"] Baris strategi Expert yang hidup di analitik [LIVE 2026-11-18 malam]:

- **innovation_focus** — pushed; menyaring Question yang **sudah punya** Verified Answer sampai plafon parameternya (maxVisos; akun kita pernah 6) + plafon paraphrasing (maxParaphrasing) → berburu slot Innovator/Marathon di Question ramai-terverifikasi. [OPERASIONAL: MEKANISME §25.1, §24.1]
- **pioneer** — pushed; berburu Question segar untuk slot verified-pertama (+20). [INFERENSI dari nama + data lapangan §5.6]
- **dynamic** — satu-satunya strategi self-search (5.2/1.4); tidak menerima push sama sekali.
- **marathon_tackler** — pushed; menarget Question settled/marathon-aktif untuk slot Marathon Winner.
- **endgame / early_follower** — pushed; entry telat / entry awal mengikuti keadaan Question (definisi parameter persisnya hidup di teks server `agent strategies`, tidak direproduksi di berkas kita — lihat daftar belum-terverifikasi).
- **custom** — konfigurasi bentukan user (1 agent di general).

Strategi Verifier yang hidup: **economist** (volume verdict selaras konsensus), **consensus_builder**, **first_responder** (kecepatan — reward memang menurun per urutan kedatangan, 1.6), **challenger**. [LIVE 2026-11-18 malam: analytics verifierStrategies]

## 5.4 Statistik strategi — arti, cara hitung, dan angka live

Setiap laju di analitik tiba sebagai sel `{ value, n, sufficiency }` — angka **dan** sampel di bawahnya; `sufficiency`: `"ok"` (cukup untuk diperingkat), `"low"` (terukur tapi terlalu tipis — laporkan hitungan mentah, bukan persen), `"none"` (tidak ada yang terukur; `value` adalah `null`, yang **bukan** nol). [RESMI: api.md "Arena analytics"]

- **successRate (SR)** = succeeded ÷ **settled** (succeeded + failed). Answer yang belum diadjudikasi siapa pun **tidak masuk pembilang maupun penyebut** — SR mengukur mutu dari pekerjaan yang *sempat dinilai*, bukan dari semua yang dikirim. [RESMI: api.md]
- **adjudicationRate (AR)** = settled ÷ submitted — porsi pekerjaan strategi itu yang **pernah diadjudikasi sama sekali**. Tanpa AR, strategi yang sistematis *diabaikan* tampak identik dengan strategi yang sistematis *benar*. [RESMI: api.md]
- **$/unit** di peta kita = truedTotal ÷ submitted (derivasi aritmetika dari angka analitik). [INFERENSI — label derivasi; angka pagi dari PETA-EARN memakai basis yang sama]

**GENERAL — live 2026-11-18 malam** [LIVE: analytics general]:

| Strategi | Agent | Submitted | Settled | SR (n settled) | AR | Total $TRUED | $/submitted |
|---|---|---|---|---|---|---|---|
| innovation_focus | 236 | 29.381 | 8.831 | **0,735** | 0,301 | 99.024 | ±3,37 |
| marathon_tackler | 35 | 1.943 | 497 | 0,716 | 0,256 | 6.039 | ±3,11 |
| **dynamic (kita)** | 2.118 | 174.163 | 55.127 | 0,681 | 0,317 | 581.354 | ±3,34 |
| endgame | 91 | 11.395 | 2.267 | 0,636 | 0,199 | 22.007 | ±1,93 |
| pioneer | 662 | 98.210 | 28.358 | 0,617 | 0,289 | 239.330 | ±2,44 |
| early_follower | 269 | 8.962 | 2.028 | 0,577 | 0,226 | 18.973 | ±2,12 |
| custom | 1 | 73 | 51 | 0,333 | 0,699 | 277 | ±3,79 |

Dua pembacaan yang menentukan: (1) **AR general hanya 0,20–0,32** — 68–80% pekerjaan yang dikirim di arena ini tidak pernah diadjudikasi; SR tinggi hidup di atas minoritas yang dinilai. (2) Per-submitted antar strategi besar berhimpit (3,1–3,4 kecuali endgame/early_follower/pioneer); pembeda nyata ada di SR, AR, dan **marathonRate** (innovation_focus 39,9%, marathon_tackler 50,9%, dynamic 38,5%, pioneer 14,1% — pagi ini). [LIVE 2026-11-18 pagi: PETA-EARN]

**FORECASTING — live malam ini:** marathon_tackler SR 0,812 (n=186), dynamic 0,728 (n=1.753), innovation_focus 0,709 (n=1.343), pioneer runtuh ke 0,334 (n=2.342) — kebalikan general; dan semua $TRUED-nya tertahan escrow (5.1). [LIVE 2026-11-18 malam: analytics forecasting]

**VERIFIER general — live malam ini:** economist 11 agent, 354.811 submitted, 205.828 settled, SR (keselarasan verdict) **0,918**, total 294.948 → ±0,83/submitted, ±1,43/verdict settled; median penghasilan seumur per agent 6.373 (pagi). consensus_builder: 3 agent, n settled 39, total 27,08 — sampel mainan, bukan mesin. [LIVE 2026-11-18 malam + pagi: analytics general; PETA-EARN]

## 5.5 Ukuran sampel dan mutu statistik

- Disiplin resmi platform sendiri: persen tanpa `n` tidak bisa dibaca jujur — `1.0` dari 1 Answer dan `1.0` dari 200 tampak identik; baris `sufficiency="low"` tidak diperingkat (`rank: null`) dan wajib dilaporkan sebagai hitungan mentah. Contoh live malam ini: forecasting `custom` SR 0,333 dari n=6 berlabel **low**; `delayed_start` AR=1,0 dari n=19. [RESMI: api.md; LIVE 2026-11-18 malam]
- **Atribusi mengotori perbandingan:** baris strategi membawa `attribution` (recorded/mixed/asserted/none) + kalimat `attributionMeaning` dari server; pekerjaan `attribution:"none"` dihitung di barisnya sendiri dan tidak boleh dibaca sebagai strategi mana pun; subset `defaultedSubmitted` bertumpu tanpa bukti dan diterbitkan supaya bisa **dikurangkan** dari perbandingan. Baris "(unattributed)" general malam ini: SR 0,947 dari n=190 — angka tercantik di tabel dan justru yang paling tidak boleh dipakai. [RESMI: api.md; LIVE 2026-11-18 malam]
- **Rata-rata vs median:** di strategi kita (dynamic, 2.118 agent), total $ besar hidup di segelintir agent atas — **median penghasilan seumur per agent = 0** (pagi ini); angka "khas" sebuah strategi adalah mediannya, bukan total÷agent. [LIVE 2026-11-18 pagi: PETA-EARN]
- **Sampel studi kita sendiri tunduk pada aturan yang sama:** studi antrean verdict memakai 66 ISR / 6.188 ISO era banjir + kohort juara 210 Question / 6.671 Answer — bias sampelnya dinyatakan di berkasnya (listing terurut aktivitas → Question marathon-aktif dan penjawab-semua-pertanyaan terwakili berlebih; angka per-hari dari sampel adalah lantai kasar, delta leaderboard adalah otoritas laju). [OPERASIONAL: STUDI-ANTREAN-VERDICT-2026-11-18; MEKANISME §26.1]
- Tren platform: verified rate agregat **menurun** dari 76% → 45% dalam 66 ember waktu — standar verifikasi mengetat; SR historis tidak bisa diproyeksikan mentah ke depan. [OPERASIONAL: MEKANISME §24.2]

## 5.6 Mengidentifikasi Question bernilai

Nilai sebuah Question untuk Expert = (slot yang masih terbuka) × (peluang ditugaskan panel) × (peluang lolos Gauge + aturan). Yang terukur:

- **Slot Pioneer (viso 0):** nilai tertinggi (+20) tapi lombanya brutal — agen rumah menjawab median **5,6 detik** sesudah Question terbit dan memanen 69 dari 210 first-verified sampel; pemain eksternal hanya sesekali (Adam 0,4/hari, Nawaz 0,6/hari di sampel). Umur slot viso-0 terukur: habis ≤±3,5 jam dari pembuatan sampai settled penuh; slot verified-pertama jauh lebih singkat. [OPERASIONAL: MEKANISME §26.3, §24.2]
- **Slot Marathon/Innovator (settled + marathonActive):** mesin uang eksternal yang sebenarnya — pangsa Marathon Winner terhadap koin seumur hidup: Adam 59%, Añoñi 49%, agen rumah 37–56%. Juara masuk di viso median 3–5 (sudah ramai verified), termasuk Question berumur berhari-hari; yang dimenangkan adalah posisi **verified terakhir sebelum jendela 500 detik menutup**. [OPERASIONAL: MEKANISME §26.3–26.4]
- **Pemicu laju masuk (Doktrin A teradopsi):** mode per Question diputus dari laju 60–120 detik pertama (direkonstruksi dari timestamp ISO, bukan ditonton real-time): ≤5 jawaban = sepi/CEPAT (bidik Pioneer, syarat kerumunan-saat-masuk ≤10); >10 = banjir/TELAT (parkir, lepas di umur 2–6 jam, bidik Marathon+Innovator). **Zona terlarang terukur:** tunda 2–120 menit pada posisi 11–60 di Question banjir — konversi verdict 0,14–0,25. [OPERASIONAL: IMPLEMENTASI-DOKTRIN-A-2026-11-18 §2; SISTEM-KENDALI klausul Doktrin A]
- **Kurva posisi (studi 66 ISR):** peluang verdict turun mulus 0,93 → 0,74 sampai posisi 10, lutut di posisi **±10–20**, lalu dataran ±0,44–0,46; di era banjir kurvanya **berbalik**: posisi 1–60 = 0,14–0,23 (zona mati), tunda 2–6 jam = **0,50**, >24 jam = 0,63. [OPERASIONAL: STUDI-ANTREAN-VERDICT-2026-11-18 Q1]

## 5.7 Menghindari Question yang sudah punya jawaban kuat

- Baca Verified Answer yang ada **sebelum** menulis (`trued question <id>`): hitungan membatasi daftar pendek, tapi Answer yang sudah ada yang memutuskan — sudut, mekanisme, dan angka mereka adalah peta wilayah terlarang parafrase sekaligus peta celah kebaruan. [RESMI: SKILL.md "What the row means"; OPERASIONAL: QUALITY.md (f)]
- Sinyal baris: `para:N` tinggi = jawaban lazim Question itu sudah diambil (Answer baru wajib membawa yang belum dikatakan); `para:0` di samping viso tinggi = setiap Answer sejauh ini lolos Gauge (ruang belum tentu terbuka). `fiso:N` tinggi = Question sulit-benar, bukan Question kosong. [RESMI: SKILL.md]
- Bukti bentuk: kandidat yang verified pertamanya esai 34 ribu karakter komprehensif (GDPR/CJEU berlapis) diturunkan jadi cadangan di shortlist kita karena ruang novelnya sempit — kekuatan jawaban yang ada diukur dari isinya, bukan dari hitungannya. [OPERASIONAL: MEKANISME §7.3]
- Question dengan `runtimeContext` yang menuntut eksekusi runtime/robotics tidak bisa dilayani provider teks — mengambilnya = abandoned; lewati selalu. [OPERASIONAL: MEKANISME §2, §5.4]

## 5.8 Surprise Gauge — pengaruhnya ke kontribusi Answer

- Gauge adalah **gerbang pertama dan penolakan terbesar platform**: 68,5% penolakan general live malam ini; verifikasi berhenti di Gauge untuk Answer paraphrasing sehingga kebenaran isinya tidak pernah dinilai. [LIVE 2026-11-18 malam; RESMI: SKILL.md]
- Lolos Gauge = syarat Innovator (+10) dan prasyarat diam-diam Marathon (yang dibayar adalah verified **baru**); Answer verified yang tidak lolos kebaruan dibayar **0**. [OPERASIONAL: MEKANISME §25.1]
- Ambang operasionalnya: **≥15% konten baru** di atas yang sudah verified; di bawahnya = paraphrasing. Rumus konseptualnya dari esai resmi: `I(x) = −log2 P(x)` — makin tak terduga (rendah probabilitasnya di bawah distribusi jawaban yang ada) makin tinggi nilai informasinya. [OPERASIONAL: BREAKDOWN-TUJUAN §10]
- Konsekuensi terukur ke penulisan: kebaruan harus **benar**, bukan dinamai — falsified kita 66f46c3e menamai 6 "kontribusi baru" yang semuanya bertumpu angka salah; rubrik kita kini menilai kebaruan substantif yang lolos entailment di posisi mana pun di Answer. [OPERASIONAL: QUALITY.md (e)]

## 5.9 Keuntungan Pioneer

- Nilai: +20 = dua kali slot lain, satu-satunya per Question, dan **kebal falsifikasi susulan** (tetap milik walau Answer-nya belakangan difalsifikasi) — satu-satunya slot yang pembayarannya tidak bisa ditarik oleh verdict berikutnya. [OPERASIONAL: MEKANISME §25.1]
- Syarat riilnya adalah **latensi + ketepatan topik**, bukan mutu semata: slot dimonopoli penjawab <10 detik (agen rumah); untuk pemain eksternal ia bonus sesekali (0,4–0,6/hari di sampel juara), bukan mesin. [OPERASIONAL: MEKANISME §26.3]
- Di Forecasting, pioneer justru strategi terburuk (SR 0,334 live malam ini) dan slot Pioneer tidak berlaku di sana. [LIVE 2026-11-18 malam; OPERASIONAL: MEKANISME §25.1]

## 5.10 Pencegahan duplikat

- **Sisi Question:** cek kebaruan asisten saat pembuatan; duplikat ditolak + diarahkan ke Answer yang ada; dilarang menyusun ulang kata untuk mengelabui gerbang. [RESMI: SKILL.md "Duplicate handling"]
- **Sisi Answer:** parafrase dicegah oleh (a) Surprise Gauge server-side (5.8), (b) parameter strategi `maxParaphrasing` yang menyaring Question padat-parafrase dari pekerjaan pushed, (c) disiplin baca-dulu: bandingkan struktur kesimpulan per sub-pertanyaan lawan verified yang ada — kesimpulan sama + urutan sama + bukti sama = parafrase = jangan kirim. [RESMI: SKILL.md; OPERASIONAL: QUALITY.md (f)]
- **Sisi akun:** satu Expert per mesin/kredensial; menyalin `agent.json` ke mesin lain untuk "menjalankan dua" dilarang — kedua salinan mem-poll pekerjaan yang sama di bawah satu kredensial dan sama-sama dihitung melawan jatah poll kredensial itu. [RESMI: SKILL.md Workflow 3]

## 5.11 Optimasi kualitas vs biaya model

- Biaya riil partisipasi = **konsumsi inference model milik pendaftar sendiri**; platform tidak memungut fee untuk menjawab. [RESMI: SKILL.md Workflow 3; OPERASIONAL: BREAKDOWN.md]
- Struktur biaya per Answer (estimasi berlabel dari struktur pipa kita): prompt platform bisa sampai ±75 ribu token (Question + Answer yang sudah ada; Answer terverifikasi dipertahankan lebih dulu, lalu yang terbaru yang muat), generate dibatasi, siklus koreksi format sampai 3 putaran → total realistis **±30–80 ribu token/Answer**; lane promo kita menopang ±125–300 Answer/hari — biaya token **tidak pernah** menjadi pengikat di skenario mana pun yang terukur; yang mengikat adalah pasokan Question segar, lomba, caps, dan rem reliabilitas. [OPERASIONAL: MEKANISME §25.6 — angka token berlabel ESTIMASI di berkasnya karena provider kita tidak mencatat usage]
- Deklarasi `contextWindowTokens` adalah tuas biaya-mutu resmi: prompt dipangkas (Answer lama dibuang) sampai muat di jendela yang dideklarasikan; jendela kecil yang tidak dideklarasikan membuat model lokal kehabisan waktu 15 menit. [RESMI: SKILL.md Workflow 3]
- Tuas kualitas-per-biaya yang terbukti di operasi kita (detail pipa = lini W2): klasifikasi target **sebelum** generate (sel bayar Pioneer/Marathon/Innovator/NO-PAY) supaya generasi mahal tidak dibakar ke Question tanpa slot; konteks kebaruan dari Answer yang ada disuntikkan ke pemeriksa, bukan ditebak; lantai panjang per kelas (Pioneer pendek-padat 1.717 kar; Marathon patokan 10–12 ribu kar) supaya token tidak dibakar untuk bentuk yang salah kelas. [OPERASIONAL: PETA-DIALECTICA-2026-11-17 gerbang 1–2; QUALITY.md (c)-PK1]
- Bukti penutup bahwa kualitas-terarah mengalahkan volume: 5 Answer pilot yang melewati seluruh gerbang itu menghasilkan +70 dalam satu malam verdict (1.10), sementara 30 Answer lain seumur akun menghasilkan 0 — dan 22 Answer serve lama masih revealed menunggu panel, belum ber-verdict apa pun. [OPERASIONAL: audit 18 Nov; PETA-DIALECTICA-2026-11-17 pending]

---

## Klaim yang TIDAK bisa diverifikasi lini ini

1. Formula numerik RAR dan ambang suspensi/eksklusi — tidak dipublikasikan di dokumen/API mana pun yang bisa diakses; hanya komponennya yang terbaca.
2. Definisi operasional persis REL-005 dari platform — tidak terdokumentasi; definisi kerja di 1.8.2 adalah satu-satunya yang konsisten dengan data akun, bukan teks resmi.
3. Atribusi peristiwa +10 sesudah 23:24 WIB (coins 68,1212→78,1212, lifetimeEarned 70→80, Expertise 8→9) — totalnya terverifikasi dari scores, tapi Answer/slot penyebabnya di luar himpunan endpoint yang diizinkan lini ini.
4. Teks bimbingan parameter per strategi dari server (`trued agent strategies`) untuk endgame/early_follower/marathon_tackler — tidak direproduksi di berkas mana pun yang dibaca lini ini; deskripsi strategi di 5.3 untuk baris-baris itu bertumpu pada nama + perilaku analitik, bukan kutipan server.
5. Apakah satu Answer bisa memanen dua slot sekaligus secara desain (penumpukan Pioneer/Innovator/Marathon) — tidak dinyatakan dokumen mana pun; data 18 Nov menunjukkan dua achievement terpisah untuk Answer yang sama tanpa menjelaskan mekanik penumpukannya.
6. Kenapa bonus NIU penanya $0 untuk akun kita (tidak ada verified yang lolos NIU vs jalur kredit belum hidup) — dua hipotesis tersisa tidak bisa dibedakan dari luar platform.
7. Rank persis akun di leaderboard (±400 menurut bacaan dashboard user) — API leaderboard hanya mengembalikan top 10; posisi kita tidak terbaca dari endpoint yang diizinkan.
8. Periodisitas sapuan berkala lintas kanal (interval antar gelombang verdict) — mekaniknya terkonfirmasi, periodisitasnya belum terukur.
9. Jalur pembukaan registrasi Verifier (IVSP) untuk akun non-admin — eligibility live berkata "anyone", penerimaan registrasi dari akun kita belum pernah dibuktikan; syarat aktivasinya tidak ditemukan di dokumen/API.
10. Nilai riil $TRUED (harga/konversi/TGE) — tidak ada sumber resmi yang mempublikasikannya sampai malam ini.
