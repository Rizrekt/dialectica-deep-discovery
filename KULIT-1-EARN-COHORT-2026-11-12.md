# KULIT-1 — Model Penghasilan Terverifikasi Ulang + Studi Kohort Pemenang SEGAR (2026-11-12)

Tugas: bedah Dialectica bagian A — model penghasilan $TRUED diverifikasi ulang dari data server live + studi kohort pemenang yang ditarik BARU (bukan snapshot §30). Read-only total: nol klaim, nol `trued answer`, nol perubahan serve/config. FREE-ONLY: tidak ada jalur berbayar yang dipakai atau diusulkan; lane Gemini tidak disentuh; dev.meta.ai tetap parkir; saldo Vyce tidak disentuh.

## 0. Metode, sumber, stempel waktu

- **Waktu tarik:** Kamis 2026-11-12 ±06:20–06:55 WIB (UTC 2026-11-11 23:20–23:55Z). Semua angka di bawah adalah bacaan pada jendela ini kecuali dinyatakan lain.
- **Klien:** `trued.py` 0.22.4 (whoami/agent show/status/arena) + API mentah `https://dialectica.xyz/api/node/*` (scores, leaderboard, isrs, isos) dengan kredensial akun sendiri (nilai kredensial tidak pernah dicetak/dicatat).
- **Korpus segar:** leaderboard limit=100 (100 baris); korpus PENUH arena General = **1.001 pertanyaan** (paginasi offset 0–1000, habis di 1.001 — cocok dengan angka analitik platform "questions: 1001"); payload ISO lengkap untuk **600 pertanyaan yang dibuat dalam 21 hari terakhir** (599 berhasil, 0 gagal; 1 pertanyaan tanpa ISO terbaca) = **19.354 record jawaban**.
- **Atribusi slot (metode sama dengan §30, dinyatakan ulang):** Pioneer = jawaban verified PERTAMA per pertanyaan (urut timestamp ISO); Marathon Winner = isoId muncul di `marathonEligibleIsos` pertanyaan itu dengan flag `awarded=true` pada saat tarik. Innovator TIDAK punya penanda publik per-jawaban (sama seperti temuan §26/§30) → perolehan Innovator per-agen tidak terukur dari luar; semua "penghasilan terukur" di studi ini = Pioneer×20 + Marathon×10 saja, yaitu LANTAI perolehan, bukan total.
- **Jendela kohort:** 21 hari terakhir dihitung dari timestamp pertanyaan/jawaban (bukan kalender): pertanyaan tertua di jendela ±22 Okt 2026, terbaru 12 Nov 06:02 WIB. Bias yang diakui: (a) pertanyaan yang dibuat >21 hari lalu tidak ditarik ISO-nya — agen yang menjawab pertanyaan tua di jendela ini kurang terhitung (kecil: hampir semua aksi terukur ada di pertanyaan segar); (b) flag `awarded` adalah keadaan saat tarik, bukan saat jawaban dikirim — untuk slot marathon, awardedAt berada ±500 detik dari timestamp jawaban pemenang, jadi atribusi per-hari akurat sampai ±1 jam; (c) `coins` di leaderboard = saldo bersih (sesudah fee bertanya/penalti), BUKAN lifetimeEarned — papan mengurutkan Lifetime Earned menurut §25, tetapi field yang terekspos publik adalah coins; keduanya dipakai apa adanya dengan label masing-masing.
- **Pembanding lama:** §24 (2026-11-10 ±13:45), §25 (2026-11-10 ±13:5x), §30 (2026-11-10 ±14:4x–15:0x), EVALUASI-STOP-2026-11-11 §6, VERDICT-LEDGER (3 baris, lengkap).

---

## 1. MODEL PENGHASILAN — diverifikasi ulang live hari ini

### 1.1 Tiga sel yang membayar penjawab (General) — TIDAK BERUBAH dari §25

| Sel | Bayaran | Syarat persis (diparafrase dari dokumen klien v0.22.4 + perilaku data live) | Verifikasi hari ini |
|---|---|---|---|
| **Pioneer** | **+20** | Jawaban pertama yang mencapai status verified pada sebuah pertanyaan; satu per pertanyaan selamanya; menurut dokumen aturan, slot tetap milik peraihnya walau jawaban itu belakangan difalsifikasi; di luar Forecasting | Struktur dikonfirmasi dokumen `references/rules-of-the-game.md` di paket klien saat ini (jawaban terverifikasi pertama = Pioneer, reward terbesar); atribusi data: 599 pertanyaan jendela 21 hari punya tepat 1 first-verified; total slot Pioneer yang teratribusi di jendela = 599 (387 eksternal / 212 rumah — lihat §2.4) |
| **Innovator** | **+10** | Jawaban verified yang lolos Surprise Gauge: konten baru ≥15% di atas yang sudah verified; di bawah itu gugur sebagai pengulangan | Dokumen yang sama: jawaban lanjutan hanya dibayar bila lolos Surprise Gauge dengan informasi yang sungguh baru; analitik arena hari ini (§1.4) menunjukkan surprise_gauge tetap penyebab penolakan terbesar (61% penolakan) — gerbangnya hidup dan aktif; ambang 15% sesuai §25 (dari tabel /earn + wiki saat itu); halaman /earn hari ini berupa SPA tanpa teks yang bisa diekstrak (fetch gagal, dicatat sebagai celah verifikasi — jumlah +10/15% bertumpu pada verifikasi §25 + konsistensi data, bukan bacaan /earn baru) |
| **Marathon Winner** | **+10** | Jawaban verified terakhir saat jendela marathon sebuah pertanyaan ditutup; dibayar saat marathon conclude; satu pertanyaan bisa membayar banyak marathon berurutan | Flag `awarded` + `awardedAt` terbaca live di payload pertanyaan hari ini; korpus penuh 1.001 pertanyaan memuat 8.258 slot marathon eligible, **3.613 awarded** (3,61 per pertanyaan; §30 membaca 2.262 awarded pada 858 pertanyaan — kenaikan konsisten dengan pertumbuhan korpus + gelombang 11–12 Nov) |
| Verified, tidak novel | **0** | Lolos verifikasi tapi tidak menambah informasi baru | Tetap: tidak ada kredit lain yang teramati; akun kita sendiri (§1.3) nol kredit masuk apa pun sejak 10 Nov |
| **Falsified** | **−1 saldo, −1 LifetimeEarned, −1 Expertise arena** | Verdict verified mensyaratkan dukungan tanpa bantahan; satu bantahan membunuh (aturan clean sheet, terverifikasi n=32 di T10 + 3 verdict kita sendiri) | **Terkonfirmasi dari jejak akun kita sendiri hari ini:** scores live 06:2x WIB — saldo 2,1212, lifetimeEarned 4, Expertise general 4, persis 5,1212/7/7 dikurangi 3× −1 untuk 3 falsified VERDICT-LEDGER; tidak ada gerakan lain |
| Abandoned (job diambil, tak selesai) | 0 + potong reliabilitas (REL-005): slash → suspensi → eksklusi naik → ban permanen | Pemicu: job diambil tidak mencapai completed (putus di tengah, timeout >15 menit generate, target runtimeContext yang tak bisa dilayani) | Jejak kita: reliability tetap **−3** beku sejak era 8 Nov (3 suspensi, suspensionCount 3, suspensionEndsAt 2026-11-08) — tidak ada abandoned baru sejak disiplin one-shot; 3 klaim rezim semuanya "completed" di jobs endpoint (§55/§56) |

- **Penumpukan slot (stacking)** pada satu jawaban: tetap **belum terbukti** — tidak dihitung di semua EV studi ini (sama seperti §25).
- **Kategori "differential verdict":** tetap tidak ada.
- **Pengali payout dari strategi/arena/RAR/Expertise:** tetap **tidak ada** yang terdokumentasi maupun teramati. Perbedaan penghasilan antar-strategi di analitik = efek seleksi pekerjaan (strategi menyaring pertanyaan apa yang sampai ke Expert), bukan pengali angka (§1.4).

### 1.2 Jalur bertanya — tetap tertutup oleh matematika

- Kredit pembuatan pertanyaan unik: **+1** (tetap di semua nomor); fee pertanyaan ke-n seumur hidup mengikuti rumus kubik resmi; pada n=8 fee 1,3504 → net **−0,3504** dan memburuk sesudahnya (n=11 tertahan saldo). Kita berhenti di n=7.
- Bonus asker NIU (+1 per jawaban yang lolos cek Novelty/Inventiveness/Utility): tetap **$0 teramati** — 7/7 pertanyaan kita settled dengan ≥23 jawaban verified dan nol kredit bonus (§24/§25); saldo kita hari ini tetap 2,1212 tanpa gerakan apa pun sejak 11 Nov 07:28, konsisten: tidak ada kredit NIU yang masuk.
- Marathon Winner di pertanyaan kita dibayar ke PENJAWAB, bukan asker (bukti historis Q1, §25) — tidak berubah.

### 1.3 Keadaan akun kita (live, 2026-11-12 ±06:2x WIB)

Dari `/api/node/scores` + `agent show` + `status`:

- Expert **8522c990-d4f6-4155-a326-3c3c9802b950**, strategyType **dynamic**, arenas **general**, maxConcurrency 1, caps maxIsrs24h **unlimited [used 1]** (used 1 = klaim #3 dalam jendela 24 jam bergeser; bacaan sebelum runonce retry 06:57 hari ini — runonce itu di luar tugas ini dan tidak disentuh).
- Saldo **2,1212 $TRUED**; lifetimeEarned **4**; Expertise general **4** (total 4).
- RAR **9** = reliability **−3** + availability **3** + reputation **9**. Komponen bergerak yang teramati dari jejak kita sendiri: availability naik +1 per job completed (0→3 untuk 3 klaim completed — termasuk yang falsified), reputation 7→9, reliability beku di −3. Artinya RAR di platform ini menghargai PENYELESAIAN job, bukan kualitas verdict — tiga falsified menaikkan RAR kita dari +4 ke 9 (EVALUASI §6.1 mencatat hal yang sama).
- suspensionCount **3** (semua era 8 Nov); tidak ada suspensi aktif.

### 1.4 Analitik arena General — dibaca live hari ini (panel `trued arena general`, jendela "all"/seumur platform)

| Strategi Expert | Verified rate | n settled | Earned ($TRUED) | Agen | EV per jawaban settled | Bacaan §24 (10 Nov) |
|---|---|---|---|---|---|---|
| marathon_tackler | 79% | 33 | 513 | 5 | 15,5 | tidak terdaftar |
| innovation_focus | **64%** | 2.354 | 22.985 | 89 | **9,76** | 59% (n 1.535), EV 8,96 |
| endgame | 57% | 838 | 6.819 | 59 | 8,14 | 56% (n 730), EV 8,44 |
| pioneer | 55% | 6.237 | 45.141 | 218 | 7,24 | 55% (n 4.837), EV 7,47 |
| **dynamic** | **52%** | 4.350 | 36.227 | 349 | **8,33** | 40% (n 1.789), EV 6,46 |
| early_follower | 48% | 884 | 6.017 | 49 | 6,81 | 48% (n 845), EV 5,92 |
| custom | 33% | 51 | 277 | 1 | 5,43 | 33% (n 51) |

- **Perubahan terukur vs §24:** rate dynamic naik **40% → 52%** dan EV-nya **6,46 → 8,33**; innovation_focus 59% → 64%, EV 8,96 → 9,76. Peringatan jendela: angka §24 dibaca dari panel yang sama tetapi n jauh lebih kecil (kemungkinan panel bergeser/tertimbang ulang oleh platform — trend panel hari ini menulis "verified rate rising: 24% → 63% over 66 buckets" untuk 90 hari terakhir, sedangkan §24 membaca "falling 76% → 45%" pada 10 Nov; kedua bacaan dicatat apa adanya — arah tren panel tidak konsisten antar-bacaan, jangan jadikan dasar keputusan sendirian).
- **Penolakan (seumur arena, per verifikasi):** surprise_gauge **61%** (19.693), arena_rules **37%** (11.835), customer_requirements 2% (523), inconclusive ~0% (75). Dari 9.279 verifikasi yang mencatat aturan: **A_CITATION 8.252 (89%)**, A_REASONING 3.179 (34%), A_SCOPE 2.695 (29%), A_UNCERTAINTY 1.507 (16%). Vs §24: surprise 59% → 61%, arena_rules 38% → 37%, A_CITATION 91% → 89% — komposisi nyaris diam; sitasi tetap pembunuh #1.
- **Waktu:** respons pertama <1 menit (n=1.001), verified ±2 menit (n=1.001) — identik dengan bacaan lama; lomba tidak melonggar.
- **Verifier (IVSP):** strategi economist — 52.754 verifikasi, 32.379 settled, agreed 92%, earned **42.577,959 $TRUED** → **±1,31 per verifikasi settled** (9 agen). §25 membaca 0,847/unit untuk sel General saja; angka hari ini adalah agregat panel arena (kemungkinan lintas arena/campuran) — dicatat sebagai bacaan baru dengan label agregatnya, bukan pengganti angka per-sel. Gerbangnya tetap sama: pembuatan Verifier **restricted to administrators**; tidak ada jalur resmi non-admin yang ditemukan di dokumen klien saat ini; akun kita tidak punya akses. Sel ini tetap terkaya dan tetap tertutup.
- **Forecasting:** tetap "not open for asking"; menjawabnya menahan reward di escrow sampai peristiwa settle (bulan) — di luar arenas kita (general) dan di luar cakupan maksimalisasi harian.
- **BARU vs §25 — arena ketiga muncul: `hle` ("Humanity's
...[truncated 20862 chars] Last Exam") kini terdaftar di daftar arena klien, tetapi keterangannya eksplisit: arena benchmark, **tidak terbuka untuk bertanya maupun partisipasi**. Payload-nya (100 pertanyaan pertama terbaca) semuanya berauthor "Dialectica" bertanggal Mei 2026 — arena pajangan benchmark internal, bukan jalur penghasilan. Akun rumah memuat Expertise `hle` ribuan (Pioneer 2.793, Innovator 3.277) — itu skor benchmark internal, bukan uang yang bisa dikejar akun luar. **Tidak ada tindakan untuk kita.**

### 1.5 Peran Expertise dan RAR (terverifikasi ulang)

- **Expertise:** skor per-arena; naik +1 per jawaban verified, turun −1 per falsified (terbukti di jejak kita: 7 → 4 untuk 3 falsified, tanpa gerakan lain). Fungsinya menurut dokumen: menggerbang badge (badge digerbang Lifetime Earned) dan menjadi bahan papan. **Tidak ada ambang Expertise yang membuka IVSP atau jalur bayar lain** yang ditemukan di dokumen klien saat ini, dan tidak ada pengali payout. Di kohort, Expertise general pemenang papan = 181–425 (kita: 4) — ia adalah AKIBAT volume verified, bukan tuas yang dibuka lebih dulu.
- **Lifetime Earned** menentukan posisi papan (bukan saldo); saldo (coins) adalah yang bisa dibelanjakan untuk fee bertanya.
- **RAR:** tiga komponen dengan peran berbeda — reliability adalah rem eksistensial (tangga REL-005: slash → suspensi → eksklusi → ban); availability naik dari penyelesaian job (+1/completed teramati); reputation bergerak dengan verdict compliant. RAR buruk berujung eksklusi = menghentikan SEMUA penghasilan; RAR tidak mengalikan payout per jawaban. Prioritas serve dari orkestrator (siapa ditawari job lebih dulu) tidak dipublikasikan sebagai rumus — tidak terukur dari luar; yang terukur hanyalah bahwa akun bervolume besar menoleransi reliability sangat negatif (pemenang papan: reliability −1 s/d −210) karena availability mereka ratusan–ribuan menenggelamkannya di RAR total (Adam RAR komponen: REL −173 / AV 784 / REP 1.747). Kita: REL −3 / AV 3 / REP 9 — bantalan availability kita 3, mereka 181–784.

### 1.6 Apakah penghasilan diskalakan hal lain? (jawaban terukur)

- **Verdict rate** — ya, paling curam: lihat gradien §2.2 (median kohort 35% vs pemenang 78–97%; EV/klaim berbalik negatif di bawah ±15% per EVALUASI §6.3).
- **Timing/viso saat masuk** — ya: di rezim hari ini marathon dibayar ke verified TERAKHIR; pemburu marathon papan atas masuk di viso median 5–12 (§2.3), bukan di 0. Pioneer adalah permainan latensi murni (respons pertama platform <1 menit; §30 mengukur latensi first-verified eksternal median 3,75 detik).
- **Kehadiran di jendela banjir** — ya, dan ini yang berubah paling besar: penghasilan terukur terkonsentrasi di hari-hari batch (§2.5, §3).
- **Arena** — General adalah satu-satunya arena terbuka untuk kita; Forecasting escrow bulanan; HLE tertutup.
- **Topik/tag** — sinyal lemah: tag domain tidak wajib (mayoritas pertanyaan tanpa tag informatif — §30: 584/858 tanpa tag); di jendela ini tag terbanyak pada jawaban pemenang = economics, public-policy, sports-science/football, finance, business, law — mencerminkan pasokan pertanyaan, bukan bukti keunggulan topik. Klaim "topik tertentu membayar lebih" TIDAK didukung data (konsisten dengan temuan §30 butir 6).

---

## 2. KOHORT SEGAR — ditarik 2026-11-12 ±06:20–06:55 WIB (BUKAN snapshot §30)

### 2.1 Leaderboard live (limit=100) — keadaan papan hari ini

- 100 baris = **9 akun rumah + 91 eksternal** (sama seperti §30). Rumah menempati #1–#7, #14, #16: Dialectica (Pioneer) 51.369 coins / 1.845 marathon wins; (Innovator) 34.298 / 1.808; Verifier B 32.334; (Late Entry) 31.954 / 1.613; Verifier A 30.544; (Endgame) 30.343 / 1.712; (Early Follower) 6.022 / 230; (Mixed) 2.750 (#14); Economist B 2.359 (#16).
- **Eksternal teratas (coins):** #8 Adam Reinhard **5.156** (marathon wins seumur 266; REL −173 / AV 784 / REP 1.747; Expertise general 425) — naik dari 4.459 pada bacaan §24 (10 Nov 13:55): **+697 dalam ±40 jam**; #9 Febriyan **4.884** (192 wins; REL −119 / AV 441 / REP 1.261; Exp 407); #10 Mauldrop **4.678** (215; REL −60 / AV 608 / REP 1.628; Exp 394); #11 Añoñi **3.698** (182; REL −210 / AV 505 / REP 1.143; Exp 316); #12 DodolDuren **3.331** (43; REL −4 / AV 290 / REP 906; Exp 297); #13 gisa **3.050** (161); #15 T04435 **2.407** (84); #17 Nawaz Ahmed **2.335** (54); #18 Nganjian Bebek **2.285** (150); #19 Katou Megumi **2.213** (100); #20 GaBot **2.202** (93).
- Ambang masuk top-100 eksternal: coins terendah eksternal di papan = **290**. Median coins 91 eksternal papan = **648**. Kita: **2,1212** — faktor ±137 di bawah ambang papan, ±2.431 di bawah eksternal #1.

### 2.2 Perilaku jendela 21 hari (19.354 jawaban pada 600 pertanyaan; 18.702 jawaban eksternal dari 373 agen)

Campuran status semua jawaban jendela: verified 5.292, falsified 4.317, revealed (menunggu verdict) 6.412, abandoned 3.320, intent 13. (Angka §30 untuk perbandingan: seumur platform saat itu 18.056 jawaban — **jendela 21 hari ini saja melampaui total seumur platform versi §30**, dan 10.095 dari jawaban eksternal jendela tiba dalam **48 jam terakhir**. Platform sedang dalam gelombang aktivitas yang tidak ada presedennya di data lama.)

Statistik kohort eksternal (agen dengan ≥5 jawaban di jendela, n=307):

- **Jawaban per hari-aktif: median 10** (q1 5,3 — q3 19,5). (§30: median 8, q1 5, q3 16 — volume naik.)
- **Verdict rate per-agen: median 35,3%** (q1 10,1% — q3 66,7%). (§30: median 32% — nyaris diam; yang berubah adalah desil atas, lihat di bawah.)
- **Penghasilan terukur per hari-aktif: median 4 $TRUED**; maksimum 703. Total penghasilan terukur jendela (semua eksternal): **30.120**; 191 dari 373 agen memperoleh >0; **10 agen teratas memegang 42,4%**-nya.
- **Viso saat masuk (semua jawaban eksternal jendela): median 5**; hanya **5,1% masuk di viso 0**. (§30: median 3, 13% di viso 0 — titik masuk bergeser jauh lebih lambat/akhir.)
- **Panjang jawaban verified eksternal: median 9.440 karakter** (q1 6.307 — q3 14.387); hanya 22,5% di bawah 6.000 karakter. (§30: median 6.200, 48% <6.000 — jawaban memanjang tajam di rezim banjir; dua peraih teratas jendela bahkan bermedian ±30.000 dan ±37.600 karakter — dibaca apa adanya dari teks reveal; ini menyimpang jauh dari pita template R3 4.500–8.000 dan dicatat sebagai fakta lapangan, bukan anjuran.)

### 2.3 Lima belas peraih teratas jendela 21 hari (penghasilan terukur = Pioneer×20 + Marathon×10)

| Agen | Terukur | P / M | Jawaban | Verified | Falsified | Verdict rate | Hari aktif | Jawab/hari | **$/hari-aktif** | Viso masuk median | Panjang median | Papan (coins / REL / AV / REP / Exp-general) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DodolDuren | **2.530** | 105 / 43 | 287 | 262 | 9 | **97%** | 5 | 57 | **506** | 1 | ±30.000 | #12 (3.331 / −4 / 290 / 906 / 297) |
| Mauldrop | **2.110** | 13 / 185 | 593 | 276 | 69 | 80% | 3 | 198 | **703** | 5 | 6.985 | #10 (4.678 / −60 / 608 / 1.628 / 394) |
| Febriyan | **1.830** | 3 / 177 | 525 | 294 | 85 | 78% | 5 | 105 | **366** | 5 | 10.673 | #9 (4.884 / −119 / 441 / 1.261 / 407) |
| Adam Reinhard | 1.410 | 12 / 117 | 553 | 259 | 33 | 89% | 21 | 26 | **67** | 3 | 12.576 | #8 (5.156 / −173 / 784 / 1.747 / 425) |
| T04435 | 1.180 | 25 / 68 | 127 | 101 | 25 | 80% | 9 | 14 | 131 | 2 | 9.914 | #15 (2.407 / −1 / 181 / 446 / 181) |
| Katou Megumi | 970 | 0 / 97 | 197 | 124 | 28 | 82% | 4 | 49 | 242 | 9 | 9.571 | #19 (2.213 / −15 / 185 / 596 / 197) |
| GaBot | 930 | 0 / 93 | 204 | 127 | 20 | 86% | 3 | 68 | 310 | 8 | 7.869 | #20 (2.202 / −5 / 204 / 609 / 204) |
| Añoñi ;-) | 640 | 0 / 64 | 143 | 65 | 10 | 87% | 17 | 8 | 38 | 4 | 11.184 | #11 (3.698 / −210 / 505 / 1.143 / 316) |
| Moden Gos | 600 | 16 / 28 | 290 | 112 | 111 | 50% | 5 | 58 | 120 | 3 | ±37.600 | #25 (1.767 / −8 / 398 / 869 / 68) |
| Federico Collarte | 580 | 0 / 58 | 164 | 70 | 16 | 81% | 12 | 14 | 48 | 3 | 5.398 | #22 (2.174 / −24 / 424 / 934 / 178) |
| gisa | 530 | 0 / 53 | 189 | 80 | 35 | 70% | 5 | 38 | 106 | 6 | 14.655 | #13 (3.050 / −62 / 289 / 795 / 268) |
| Soni Ajo | 500 | 13 / 24 | 97 | 68 | 9 | 88% | 4 | 24 | 125 | 2 | 7.766 | #43 (931 / −5 / 109 / 286 / 83) |
| Hermawan Kwan | 490 | 0 / 49 | 102 | 85 | 3 | **97%** | 2 | 51 | 245 | 12 | 9.796 | #85 (348 / −2 / 31 / 82 / 33) |
| kasnapp | 470 | 0 / 47 | 111 | 68 | 20 | 77% | 3 | 37 | 157 | 11 | 12.597 | #37 (1.190 / −7 / 108 / 324 / 101) |
| Nganjian Bebek | 410 | 0 / 41 | 234 | 55 | 49 | 53% | 5 | 47 | 82 | 6 | 14.284 | #18 (2.285 / −140 / 366 / 833 / 151) |

Pola yang terbaca dari tabel (semua angka dari tarikan yang sama):

- **Dua mesin berbeda di puncak:** (a) **Pioneer-latensi** — DodolDuren: 105 slot Pioneer dalam 5 hari aktif (83% penghasilan terukurnya dari Pioneer), verdict 97%, masuk di viso median 1, jam jawab terkonsentrasi 17:00–22:00 WIB; (b) **Marathon-volume** — Mauldrop/Febriyan/Katou/GaBot: 93–185 kemenangan marathon, masuk di viso median 5–9, volume 49–198 jawaban/hari-aktif, verdict 78–86%. Mauldrop menjawab paling pekat pada **00:00–05:00 WIB** (54+54+53+53+42 jawaban di jam 00–05 selama 3 hari) — kehadiran lintas-malam penuh.
- **Campuran kelas (dari penghasilan terukur):** marathon mendominasi hampir semua orang (Mauldrop 88%, Febriyan 97%, Katou/GaBot/Añoñi/Federico/gisa/Hermawan/kasnapp 100%); pioneer hanya dominan di DodolDuren (83%) dan berarti di T04435 (42%), Moden Gos (53%), Soni Ajo (52%). Innovator tidak terukur (tidak ada penanda publik) — pangsa sebenarnya dari total penghasilan para agen ini tidak diketahui; angka di atas adalah lantai.
- **Jam aktif pemenang (jawaban per jam WIB, jendela):** DodolDuren 17–22; Mauldrop 00–05; Febriyan 17–21 (64 jawaban jam 18); Adam menyebar 22, 02, 05, 08, 17; Katou 21–23 + 10–11; GaBot 14–15 + malam. Tidak ada satu jam ajaib — yang sama adalah kehadiran saat batch tiba (lihat §3).
- **Topik (tag terbanyak pada jawaban mereka):** economics, public-policy, sports-science/sports-economics/football, finance, business, law, technology — mencerminkan pasokan (lihat peringatan tag §1.6).

### 2.4 Pembagian slot jendela: rumah vs eksternal

- Pioneer (first-verified, 599 pertanyaan jendela): eksternal **387 (65%)** vs rumah **212 (35%)** — nyaris identik dengan temuan §30 (67% eksternal di korpus penuh). Pioneer BUKAN monopoli rumah; ia dimenangi minoritas cepat, dan di jendela ini DodolDuren sendirian mengambil 105.
- Marathon wins yang teratribusi ke jawaban di jendela: eksternal **2.238 dari 2.407 (93%)**. Marathon adalah kolam eksternal.
- Total slot marathon awarded seumur korpus penuh: 3.613 pada 1.001 pertanyaan = **3,61 slot/pertanyaan** (§30: 2,64 pada korpusnya) — pertanyaan sekarang membayar lebih banyak marathon per pertanyaan.

### 2.5 Seperti apa "sehari" bagi peraih #1 — tiga potret terukur

- **Hari burst terbesar yang terukur (Mauldrop, 12 Nov, hari BELUM selesai — dihitung s/d 06:11 WIB): 1.140 $TRUED terukur** (pioneer+marathon dari jawaban yang dikirim hari itu), sesudah 690 (11 Nov) dan 280 (10 Nov) — lajunya MENAIK mengikuti gelombang pertanyaan. Pada 11 Nov (hari penuh): 690. Sebagai pembanding laju: ini ±10–17× laju harian berkelanjutan Adam.
- **Hari burst Pioneer (DodolDuren):** 08 Nov 200 → **09 Nov 880** → 10 Nov 660 → 11 Nov 630 → 12 Nov 160 (parsial). Febriyan: 09 Nov 670, 10 Nov 730, 11 Nov 350.
- **Hari berkelanjutan (Adam Reinhard, 21 hari aktif):** seri harian terukur 02–12 Nov: 80, 130, 440, 110, 80, 110, 130, 160, 50, 10, 10 → median hari ±110 di pekan pertama jendela, **runtuh ke 10/hari pada 11–12 Nov** — di tengah gelombang, pangsa Adam justru disalip para burster; coins papannya tetap naik (+697/±40 jam) karena marathon dari jawaban-jawaban sebelumnya terus conclude. Añoñi: 640/17 hari aktif = 38/hari, pola long-form presisi (median 11.184 kar, verdict 87%) — arketipe berkelanjutan kedua.
- **Tier realistis $TRUED/hari (dari distribusi jendela, bukan janji):** puncak burst **650–1.140/hari** (Mauldrop, hari gelombang, volume ±190 jawaban/hari); burster menengah **240–510/hari** di hari aktifnya (DodolDuren 506, Febriyan 366, GaBot 310, Katou 242); berkelanjutan papan atas **38–131/hari** (Adam 67, T04435 131, Añoñi 38); **median agen aktif (≥5 jawaban): 4/hari-aktif**; median agen papan (91 eksternal) tidak terukur per-hari dari coins saja — tetapi ambang papannya (290) terhadap laju median 4/hari menyiratkan mayoritas agen tidak pernah mendekati papan.

---

## 3. POLA RILIS PERTANYAAN — dari timestamp 1.001 pertanyaan General (dibaca 2026-11-12 ±06:3x WIB)

### 3.1 Laju rilis: rezim berubah total

| Jendela | Pertanyaan baru | Per hari |
|---|---|---|
| 24 jam terakhir | **117** | **117,0** |
| 48 jam terakhir | 172 | 86,0 |
| 7 hari terakhir | 339 | 48,4 |
| 21 hari terakhir | 601 | 28,6 |
| Perkiraan §24/§25 (10 Nov) | — | ±15–25 |

Pasokan pertanyaan General sekarang **4–8× lipat** dari asumsi yang dipakai seluruh desain rezim (§24.4: "pasokanlah yang mengikat"). Hari-hari bersifat batch: dalam 21 hari, Rabu memuat 173 pertanyaan dan Senin 124, sedangkan Jumat hanya 36 dan Sabtu 45 (hitungan hari-dalam-jendela, bukan laju mingguan yang stabil — dicatat apa adanya). Umur slot viso-0 tetap pendek (respons pertama <1 menit, verified ±2 menit — analitik hari ini), tetapi dengan 86–117 pertanyaan/hari, jumlah slot Pioneer harian yang tersedia naik dari ±15–25 menjadi **86–117 slot/hari** secara aritmetika (satu per pertanyaan) — 65%-nya historis jatuh ke eksternal.

### 3.2 Distribusi jam rilis (WIB)

**48 jam terakhir (n=172):** 00:12 · 01:12 · 02:6 · 03:7 · 04:7 · 05:2 · 06:3 · **07:15** · 08:2 · 09:6 · 10:3 · 11:3 · 12:5 · 13:7 · 14:5 · 15:7 · 16:3 · 17:6 · 18:7 · 19:6 · **20:14 · 21:11 · 22:14** · 23:9. Tiga gugus: **pagi 07:00**, **malam 20:00–22:00**, **tengah malam 00:00–01:00**.

**7 hari terakhir (n=339):** puncak 17:00 (24), 22:00 (23), 20:00 (21), 07:00 (20), 19:00 (20), 18:00 (16), 13:00 (16), 00:00 (16), 01:00 (17), 02:00 (11), 23:00 (13); lembah 05:00 (6), 11:00 (6), 06:00 (8), 08:00 (9), 14:00 (9).

**21 hari terakhir (n=601):** puncak 13:00 (36), 17:00 (33), 22:00 (32), 01:00 (31), 07:00 (30), 18:00 (30), 19:00 (28), 00:00 (26), 23:00 (27), 04:00 (32), 02:00 (36→ termasuk batch), 21:00 (21); lembah 11:00 (12), 14:00 (14).

Perbandingan dengan §30 (korpus 858 saat itu): punuk dominan §30 adalah **12:00 (84) dan 13:00 (67)** lalu 07:00 (56) — punuk tengah hari itu **tidak dominan lagi** di 48 jam terakhir (12:00 = 5, 13:00 = 7 dari 172). Pola rilis bergeser ke **07:00 + 20:00–22:00 + 00:00–01:00** di rezim sekarang, dengan latar sore 17:00–19:00 yang tetap berarti di jendela 7–21 hari.

### 3.3 Jam menjawab kohort eksternal (jendela 21 hari, n=18.702)

Puncak: **18:00 (1.190), 22:00 (1.152), 17:00 (1.063), 19:00 (1.003), 20:00 (974), 00:00 (952)**, 21:00 (893), 15:00 (805), 07:00 (788), 03:00 (788), 23:00 (777), 01:00 (909), 02:00 (769). Lembah: 09:00 (479), 11:00 (481), 06:00 (525). Lapangan menjawab paling pekat **17:00–22:00 WIB** dan tetap hidup 00:00–05:00 (blok malam Mauldrop dkk).

### 3.4 Jendela tangkap nyata vs jendela hunt kita sekarang

Jadwal kita saat ini (badan slot-hunt): jendela kerja 07:00–21:00 WIB tiap ±2 jam (07, 09, 11, 13, 15, 17, 19, 21) + day-close 23:00; di luar itu hanya scan ringan; serve latar mati di malam hari.

| Gugus rilis nyata (48j–7h) | Tertangkap jadwal kita? |
|---|---|
| 07:00 (15/48j; 20/7h) | YA — jendela 07:00 persis di atasnya; serve-on ±06:55 (desain §25.7/R4) selaras |
| 17:00–19:00 (berarti di 7–21h) | SEBAGIAN — jendela 17:00 & 19:00 ada, tetapi batch yang tiba 17:30–18:30 menunggu s/d 19:00; slot Pioneer-nya (umur <1 menit untuk respons pertama) sudah lewat untuk one-shot terjadwal — hanya serve hidup yang menangkapnya |
| **20:00–22:00 (14+11+14/48j — gugus terbesar 48j)** | **SEBAGIAN BESAR TIDAK** — jendela terakhir 21:00, sesudah itu day-close 23:00 bersifat tutup-buku; tidak ada serve malam |
| **00:00–01:00 (12+12/48j)** | **TIDAK** — di luar jam kerja; justru di blok inilah Mauldrop memanen marathon (00–05) dan DodolDuren/Febriyan menutup hari burst mereka |
| Tengah hari 11:00–13:00 (dominan di §30) | Jadwal kita menaruh "jendela utama kedua" di sini (R4) — data 48j menunjukkan gugus ini sekarang LEMAH (3+5); di 21h ia masih berarti (11:00 adalah lembah 12, tetapi 13:00 = 36 tertinggi) — statusnya campuran: bukan lagi punuk yang bisa diandalkan harian |

Kesimpulan §3 (angka, bukan anjuran operasional — keputusan jadwal milik sesi utama): **pusat gravitasi rilis bergeser dari tengah hari ke malam (20:00–01:00) + pagi 07:00**, dan dua dari tiga gugus terbesar 48 jam terakhir berada di luar/di tepi jadwal kerja kita. Dengan laju 86–117 pertanyaan/hari, kendala pengikat bukan lagi pasokan (§24) melainkan **kehadiran pada jam batch + verdict rate**.

---

## 4. ANALISIS GAP — kita vs kohort (semua terkuantifikasi)

Keadaan kita (live 2026-11-12 ±06:2x + VERDICT-LEDGER): rizrekt, Expert 8522c990-d4f6-4155-a326-3c3c9802b950, dynamic/general, saldo **2,1212**, lifetimeEarned **4**, Expertise **4**, RAR **9** (REL −3 / AV 3 / REP 9), klaim rezim **3** (3 completed, **0 verified, 3 falsified**, 0 abandoned), slot dimenangi **0**, viso masuk klaim kita: 6, 5, 4 (median **5**).

| Dimensi | Kita | Median kohort eksternal (jendela) | Pemenang jendela / papan | Gap (angka) |
|---|---|---|---|---|
| Verdict rate | **0%** (0/3) | 35,3% (n=307 agen ≥5 verdict) | 78–97% (top-15 jendela); ambang impas ±15% (EVALUASI §6.3) | −35 pp vs median; −78 s/d −97 pp vs pemenang; di bawah impas → EV teramati **−1,00/klaim** |
| Volume | 3 klaim SEUMUR rezim (±2 hari) | 10 jawaban/hari-aktif | 49–198 jawaban/hari-aktif (burst); 8–26 (berkelanjutan) | Kita ≈ 1,5/hari kalender vs median 10/hari-aktif: **±7×**; vs burst: **±33–132×** |
| Penghasilan | −3 kumulatif rezim (saldo 5,1212 → 2,1212); 0 slot | +4/hari-aktif (terukur) | +38 s/d +703/hari-aktif; Adam +67/hari × 21 hari | Runway kita pada rate 0% = **2 klaim** (EVALUASI §6.2); saldo 2,1212 vs ambang papan 290 = **1 : 137** |
| Campuran kelas | 0 Pioneer / 0 Innovator / 0 Marathon | Marathon ≈ seluruh terukur agen tipikal (§30: pangsa median 100%) | Marathon 88–100% pada 13 dari 15 teratas; Pioneer dominan hanya DodolDuren (83%) | Kita belum masuk kelas mana pun; kelas yang paling terbuka untuk pendatang (marathon, 93% wins eksternal) justru yang belum pernah kita menangi |
| Viso saat masuk | median **5** (6, 5, 4) | median 5 (semua jawaban jendela) | Pemburu marathon: 5–12; DodolDuren (pioneer): 1 | **SELARAS** dengan kohort & kelas marathon — timing masuk BUKAN gap kita; yang gagal adalah verdict-nya |
| Jam kehadiran | One-shot siang–malam awal (07:26, ±19:03, ±21:24 WIB) + hunt 07–21 | Menjawab pekat 17–22 + blok 00–05 hidup | Mauldrop 00–05; DodolDuren/Febriyan 17–22; rilis terbesar 20:00–01:00 | Jendela tangkap kita menutup sebelum gugus rilis terbesar (20:00–01:00) — gap kehadiran terukur di §3.4 |
| Expertise general | **4** | — (tidak terukur per-agen di luar papan) | 181–425 (papan eksternal atas); 33 pun cukup untuk #85 (Hermawan, verdict 97%) | −177 s/d −421 vs papan atas; Expertise adalah akibat, bukan prasyarat (Hermawan: Exp 33, tetap 490 terukur dalam 2 hari) |
| RAR / bantalan reliabilitas | RAR 9 (REL −3 / AV 3 / REP 9); 3 suspensi historis | — | REL −1 s/d −210 dengan AV 181–784 (papan) | AV kita 3 vs 181–784: satu abandoned baru menelan kita (REL-005 tanpa bantalan); mereka menoleransi REL −210 karena AV 505 |
| Panjang jawaban | Klaim kita 6.580 kar (#2) dkk di pita R3 | Verified jendela median 9.440 kar | Pemenang bermedian 5.398–14.655 kar; dua burster ±30–37 rb | Pita kita berada di dalam sebaran lapangan; panjang BUKAN pembeda verdict kita (akar falsified kita = dukungan sitasi/scope, VERDICT-LEDGER) |
| Strategi (analitik platform) | dynamic (EV 8,33/settled, rate 52% — agregat platform) | — | innovation_focus EV 9,76, rate 64% (agregat) | Agregat platform BUKAN rate kita: rate kita di dynamic = 0/3; jangan membaca EV strategi sebagai EV agen |

**Pembacaan gap dalam satu paragraf angka:** dari semua dimensi di atas, hanya DUA yang menempatkan kita di bawah garis impas: **verdict rate (0% vs impas 15%)** dan **saldo/runway (2,1212 = 2 kegagalan lagi)**. Volume, viso, panjang, dan kelas target kita sudah berada di dalam sebaran lapangan; kehadiran malam adalah gap ketiga yang nyata tetapi sekunder (ia mengikat hanya sesudah verdict rate di atas impas). Kohort membuktikan lantainya rendah untuk masuk (Hermawan Kwan: 102 jawaban, 2 hari, verdict 97%, 490 terukur, papan #85 dari nol dalam jendela ini) — dan langit-langitnya ditentukan oleh verdict rate × kehadiran di hari batch, bukan oleh modal, config, atau akses: caps kita sudah unlimited, arena yang sama, pertanyaan yang sama.

---

## 5. Yang BERUBAH vs §25/§30 — daftar bendera (ringkasan penunjuk)

1. **Pasokan pertanyaan meledak:** 117/24 jam terakhir (86/hari di 48 jam) vs asumsi ±15–25/hari (§24/§25). Kendala pengikat berpindah dari pasokan ke kehadiran + verdict rate. (§3.1)
2. **Pusat rilis bergeser:** punuk 12:00–13:00 (§30) tidak dominan di 48 jam terakhir (5+7 dari 172); gugus nyata = 07:00, 20:00–22:00, 00:00–01:00. (§3.2)
3. **Volume lapangan meledak:** 10.095 jawaban eksternal dalam 48 jam vs 18.056 jawaban seumur platform pada bacaan §30; agen burst menjawab 105–198/hari-aktif (median kohort hanya naik 8 → 10). (§2.2)
4. **Titik masuk bergeser akhir:** viso median 3 → **5**; pangsa masuk viso-0 13% → **5,1%**. Marathon makin menjadi permainan verified-terakhir di pertanyaan yang sudah ramai. (§2.2)
5. **Jawaban memanjang:** median verified 6.200 → **9.440** karakter; pangsa <6.000 kar 48% → 22,5%. Pita R3 (4.500–8.000) kini berada di bawah median lapangan — dicatat sebagai fakta; konsekuensi template adalah keputusan sesi utama, bukan studi ini. (§2.2)
6. **Rate strategi platform bergeser:** dynamic 40% → 52% (EV 6,46 → 8,33); innovation_focus 59% → 64% (EV 8,96 → 9,76); panel tren menulis arah berlawanan antar-bacaan ("falling" 10 Nov vs "rising" hari ini) — jangan pakai tren panel sendirian. (§1.4)
7. **Arena ketiga `hle` muncul** — benchmark tertutup, bukan jalur uang. (§1.4)
8. **Verifier economist teragregat ±1,31/verifikasi settled** (panel arena) vs 0,847/unit sel General (§25) — agregat berbeda, gerbang admin tidak berubah. (§1.4)
9. **Yang TIDAK berubah:** tiga sel pembayar + jumlahnya (+20/+10/+10), falsified −1 rangkap tiga, abandoned/REL-005, bertanya tertutup (NIU $0 teramati), IVSP admin-only, Forecasting escrow + tertutup untuk bertanya, tidak ada pengali payout, stacking belum terbukti, Innovator tidak terukur dari luar.

## 6. Batas studi ini (dinyatakan, bukan disembunyikan)

- Halaman /earn tidak bisa dibaca sebagai teks hari ini (SPA) — jumlah +20/+10/+10 dan ambang 15% bertumpu pada: dokumen aturan di paket klien v0.22.4 (struktur + mekanisme), verifikasi §25 atas /earn+wiki saat itu, dan konsistensi atribusi data hari ini (slot×bayaran menjumlah ke pola coins papan tanpa kontradiksi yang teramati). Bila sesi utama butuh bacaan /earn segar, itu pekerjaan browser terpisah.
- Penghasilan "terukur" mengecualikan Innovator (tanpa penanda publik) dan kredit asker NIU — total penghasilan sebenarnya para agen ≥ angka studi ini.
- Atribusi marathon memakai flag awarded saat tarik; satu pertanyaan di jendela masih berstatus marathon berjalan (1 dari 1.001) — wins yang belum conclude tidak terhitung.
- Tiga klaim kita sendiri tidak masuk korpus ISO jendela (pertanyaannya dibuat >21 hari lalu) — angka kita diambil dari scores + VERDICT-LEDGER, bukan dari tarikan ISO.
