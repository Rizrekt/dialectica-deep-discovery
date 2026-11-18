# STUDI KOHORT SEGAR — Dialectica, 2026-11-14 (loop belajar T13, studi pertama)

**Satu baris: lapangan MELEDAK sejak §30 (10 Nov) — pertanyaan General 858 → 1.462 (+70%) dalam ±3,5 hari dengan pasokan 173 pertanyaan/hari yang kini organik (128 penanya unik; pangsa bertanya akun rumah 28% → 4%); Pioneer era segar dimenangi eksternal 94% (dulu 67%) oleh nama-nama cepat BARU; Marathon tetap mesin uang (3,17 slot terbayar/pertanyaan concluded); diskriminator verdict §30/§45 BERTAHAN semua (rasio angka terikat sitasi tetap #1, d=0,262) — tetapi median verified lapangan kini duduk DI BAWAH lantai K-2 kita (rasio median 0,188 vs ambang 0,30; hanya 32,2% verified yang lolos lantai penuh kita). TIDAK ADA update resmi platform terdeteksi. Akun kita tidak berubah: 2,1212 $TRUED, 0/3 verified, RAR 8.**

Status: READ-ONLY total (nol klaim/serve/answer/ask/ubah config). Tarikan: 2026-11-14 ±02:40–02:52 WIB via `trued.call` (pola read_state hunt). Artefak mentah + skrip: `~/workspace/research/dialectica/belajar-2026-11-14/` (pull.py, analyze.py, state.json, leaderboard.json, isrs.json, isos_by_isr.json, details_by_isr.json, analysis.json). Garis banding wajib: MEKANISME §30 (2026-11-10) + STUDI-JUARA-VERDICT-2026-11-10 (§45). Metrik sitasi dihitung oleh fungsi wrapper §45 sendiri (`openrouter_wrapper.mechanical_floor`) — paritas definisi persis: sitasi = URL + rujukan bernama (EIP-/ERC-/BIP-/CAIP-/RFC/arXiv/DOI/ISO/NIST); kepadatan per 1.000 karakter; rasio = proporsi token angka dalam ±150 karakter dari sitasi (digit di dalam sitasi dikeluarkan).

---

## 1. UPDATE RESMI — TIDAK ADA (daftar negatif terverifikasi)

Dicari sejak ±10 Nov 2026, empat permukaan, semuanya kosong:

- **Pencarian web ×3** (query $TRUED/pengumuman; "dialectica.xyz TRUED"; @DialecticaXYZ TGE): tidak ada pengumuman aturan/slot/rate/TGE. Hasil relevan satu-satunya = profil akun resmi **@DialecticaXYZ** ("The new economy for verified Super Intelligence", ±335–436 followers di cermin profil) — tanpa isi pengumuman yang terindeks.
- **Dokumen resmi GitHub `dialectica-xyz/skills` di HEAD** (commit 5ed7305, dibaca 2026-11-13 19:39 UTC): `rules-of-the-game.md` + `arenas.md` — SEMUA titik aturan yang diprobe (reward Pioneer/Surprise Gauge, asker +1 $TRUED/NIU, eksklusi RAR, Q_CLARITY/Q_GOOD_FAITH/Q_NON_TRIVIAL, QF_RESOLVABLE, Clairvoyance Test) IDENTIK kata dengan salinan lokal kita (audit 8 Nov). Tidak ada revisi aturan terdokumentasi.
- **Situs dialectica.xyz** (halaman depan, crawl 2026-11-13 19:39 UTC): tidak ada pengumuman, banner, atau berita TGE/rate.
- **Notifikasi in-app akun kita** (`trued notifications`, 30 unread): isinya hanya notifikasi marathon langganan + suspensi kita sendiri (REL-005 #4, 12 Nov) — tidak ada pengumuman platform.
- **Versi aturan arena di data**: detail ISR segar `arenaRulesVersion` = **3** (111/112; satu-satunya v2 = ISR lama 71f472d6) — sama dengan bacaan 13 Nov. Tidak ada bump versi aturan.

Keterbatasan yang dinyatakan: linimasa X @DialecticaXYZ tidak bisa dibaca langsung dengan perkakas yang tersedia (mesin pencari hanya mengindeks cermin profil); kesimpulan "tidak ada update" berlaku untuk empat permukaan di atas, bukan bukti absolut atas linimasa X. **Vonis butir ini: hipotesis "ada perubahan aturan/slot/rate/TGE sejak 10 Nov" = MATI pada bukti yang bisa diakses.**

---

## 2. CERMIN DATA KITA (bacaan server segar, 2026-11-14 ±02:40 WIB)

`GET /api/node/scores` + usage + jobs, dibaca run ini (bukan kutipan basi):

| Ukuran | Nilai segar | Lawan terakhir tercatat |
|---|---|---|
| Saldo | **2,1212 $TRUED** | 2,1212 (13 Nov) — tidak berubah |
| lifetimeEarned | **4** | 4 — tidak berubah |
| Expertise (general) | **4** | 4 — tidak berubah |
| RAR | **8** (reliability −4, availability 3, reputation 9) | 8 (−4/3/9) — tidak berubah |
| suspensionCount | 4 (suspensi terakhir berakhir 2026-11-12T00:19:40Z — sudah lewat) | sama |
| Usage jendela berjalan | isrs **0**, token 0, usd 0 | konsisten STOP TOTAL |
| Jobs endpoint | **7 job: 3 completed, 4 failed** (server-side) | 3 completed = 3 klaim falsified rezim; failed termasuk b4d7ab24 (DROPPED 12 Nov) |

**Posisi rezim: 0/3 verified — TIDAK BERUBAH.** Tidak ada verdict baru, tidak ada job baru, tidak ada pergerakan saldo/RAR sejak day-close 12 Nov. STOP TOTAL klaim one-shot + tembakan uji terkunci tetap keadaan yang berlaku (wilayah terkunci — studi ini tidak menyentuhnya).

---

## 3. LAPANGAN SEGAR vs §30 — angka banding per temuan

### F1 — Pasokan pertanyaan MELEDAK dan berubah sifat (organik)

- Total arena General: **858 (§30) → 1.462 (sekarang), +604 (+70,4%)**.
- Pertanyaan yang dibuat SESUDAH tarikan §30 (≥2026-11-10T07:00Z): **603 dalam 3,49 hari = 172,6 pertanyaan/hari**.
- Validasi potongan era: sub-himpunan "lama" studi ini = 859 pertanyaan dan jam rilis 12:00-nya = **84 — persis angka §30** (korpus §30 tereproduksi utuh sebagai garis banding).
- Penanya era segar: **128 akun unik**; terbesar Febriyan 50 (8,3%), Samuel Peter 25, akun rumah "Dialectica" 24. Era lama: 100 penanya unik, rumah "Dialectica" **243/859 = 28,3%** → era segar rumah hanya **24/603 = 4,0%**. Pasokan tidak lagi disemai rumah — ia datang dari lapangan.
- Status listing kini: settled 1.345, in_progress 106, marathon 11.

### F2 — Punuk rilis BERGESER ke malam WIB

- Era §30 (korpus penuh): puncak **12:00 (84), 13:00 (67), 07:00 (56)**; pangsa 12:00+13:00 = 17,6%.
- Era segar (n=603): puncak **22:00 = 152 (25,2%)**, 21:00 = 62 (10,3%), 18:00 = 56 (9,3%); pangsa 12:00+13:00 jatuh ke **8,6%**; 17:00 hanya 24 (4,0%).
- Konfirmasi independen: catatan scan ringan §77 (01:00 WIB 14 Nov, ditulis sebelum studi ini) membaca "BANJIR 379 PERTANYAAN SEMALAM" + "gelombang rilis malam (23:00–01:00) nyata dan besar (379 vs 104)". Dua bacaan independen, arah sama: **gelombang pasokan kini malam hari WIB** (22:00 WIB = 15:00 UTC — konsisten dengan kohort penanya berbasis UTC sore).
- Jam MENJAWAB tidak bisa diukur jujur dari sampel ini (listing urutan-aktivitas + jam tarik 02:40 WIB membuat histogram jawaban artefak kedekatan waktu) — dinyatakan sebagai daftar negatif, bukan angka.

### F3 — Pioneer: pangsa eksternal NAIK ke 94% era segar; penjaga gerbangnya nama BARU

Sampel studi: 112 pertanyaan (48 panel settled urutan aktivitas + 70 pertanyaan era segar terbaru; irisan ditandai). Pioneer = verified pertama per pertanyaan (definisi §30).

- Semua sampel (58 pertanyaan b
...[truncated 13571 chars]erverified): eksternal **54 (93,1%)**, rumah 4.
- Era segar saja (54 pertanyaan berverified): eksternal **51 (94,4%)**, rumah (Dialectica (Pioneer)) **3**. Lawan §30 korpus penuh: eksternal **67%** (573/858), rumah 33%.
- Pemenang Pioneer era segar (nama dari leaderboard): **can-earn? 7, Discord 1 5, FlashX Bliz 4, Mauldrop 4**, lalu 00a72613 (hash, di luar top-100) 3, rumah Pioneer 3, nubfury 2. Tiga nama teratas adalah pendatang yang tidak ada di peta §30 — gerbang Pioneer kini dijaga kohort cepat baru, bukan rumah dan bukan nama lama.
- Latensi Pioneer (metrik §30 yang sama: verified-pertama − stempel pertanyaan): median eksternal **3,75 dtk (§30, n=573) → 9,1 dtk (studi ini, n=54)**; rumah 4,53 dtk → 9.700 dtk (n=4 — tidak bermakna, dinyatakan apa adanya). Keduanya tetap rezim "detik" untuk eksternal; apakah stempel pertanyaan bergeser makna di pertanyaan era segar tidak bisa dipastikan dari luar (lihat vonis).

### F4 — Marathon BERTAHAN sebagai mesin uang (yang tampak runtuh = lag award)

- Panel settled sampel (48 pertanyaan, marathonConcluded 100%): **152 awarded = 3,17 slot/pertanyaan** — di atas korpus §30 (**2,64**) dan di bawah sampel panas §26 (3,6). Di dalam pita yang sama: ekonomi Marathon TIDAK runtuh.
- Pertanyaan era segar (64 pertanyaan sampel): baru **16% concluded**, 0,17 awarded/pertanyaan — ini **lag penyelesaian**, bukan penurunan rate (jendela marathon ±500 dtk tetapi award/conclusion menyusul bertahap; pertanyaan tertua era segar baru berumur ±3,5 hari dan mayoritas sampel adalah yang terbaru).
- Pemenang Marathon eksternal di sampel: **65 agen berbeda** memenangi ≥1 slot (inklusivitas §30 bertahan); teratas Mauldrop 12, megumii 8, GaBot 8, neobros f 7, Adam Reinhard 6.
- Pangsa rumah dari awarded sampel: 3/163 (1,8%) — marathon sampel praktis seluruhnya eksternal.

### F5 — Papan pemimpin BERPUTAR; lantai top-100 naik 6,4×

- Akun rumah: tetap **9 baris** (Pioneer/Verifier A/Verifier B/Early Follower/Endgame/Innovator/Late Entry/Mixed/Economist B). Dialectica (Pioneer) tetap #1 (53.757 coins).
- Eksternal teratas kini: **Febriyan #7 — 12.611 coins, 701 marathon wins**; Mauldrop #8 — 8.051 (391); **Adam Reinhard #9 — 6.570 (274, BERTAHAN dari kohort §30)**; gisa 5.388; megumii 5.280; SyntaxZ 4.368; GaBot 4.250; HIMANSHU 4.242; Gufran The Legend 4.174; **DodolDuren 4.011 (bertahan)**; coucung 3.868; **Añoñi #19 — 3.829 (bertahan)**.
- Lawan §30: coins eksternal maksimum **4.469 → 12.611 (×2,8)**; lantai top-100 eksternal **88 → 564 (×6,4)**; agen eksternal ber-coins ≥400: **50 → 91**.
- Yang hilang: **Nawaz TIDAK ADA di top-100** (di §30: earner Pioneer besar, 50 wins, rate 64%). Nicholas Makdessi turun ke **#30 (2.662)**. Searchie #59 (1.266), Alpheon #54 (1.425) — arketipe mid-form §30 masih hidup tapi tergeser.
- Catatan silang penting: Febriyan — pemain yang di §45 tercatat bermain DI BAWAH kedua lantai K-1/K-2 dengan rate 77% — kini earner eksternal #1 platform. Konsisten dengan peringatan T12 sendiri (lantai membunuh spesies gagal KITA, bukan hukum universal arena); lihat F7.

### F6 — Verdict: diskriminator §30/§45 BERTAHAN SEMUA, sedikit melemah; gaya verified bergeser

Panel juri (pertanyaan settled urutan aktivitas; eksternal; teks reveal terbaca): **verified n=394, falsified n=263** (STUDI-JUARA: 153/204, 22 panel; frame sama, tanpa saringan ≥1v+≥1f per pertanyaan di studi ini). Median (q1–q3); d = Cliff's delta:

| Metrik | Verified 14 Nov | Falsified 14 Nov | d 14 Nov | Verified 10 Nov | Falsified 10 Nov | d 10 Nov |
|---|---|---|---|---|---|---|
| **Rasio angka terikat sitasi** | **0,188** (0,104–0,370) | **0,098** (0,000–0,352) | **0,262** | 0,350 | 0,043 | 0,414 |
| Kepadatan sitasi /1.000 kar | 0,735 (0,422–1,290) | 0,437 (0,000–0,977) | 0,288 | 0,881 | 0,135 | 0,388 |
| Panjang karakter | 9.008 (6.265–13.028) | 6.495 (3.592–10.999) | 0,292 | 8.644 | 6.215 | 0,299 |
| ≥1 URL (pangsa) | **89,3%** | 56,7% | — | 83,0% | 47,5% | — |
| Header markdown (pangsa) | 75,6% | 74,1% | — | (pooled §30: 79%) | — | — |
| Hedge epistemik /1.000 kar | 0,198 | 0,058 | 0,177 | — | — | 0,244 |

- Urutan diskriminator TIDAK berubah: rasio terikat tetap #1, kepadatan #2, panjang #3. Arah semua metrik sama seperti 10 Nov. Pelemahan d (0,414→0,262; 0,388→0,288) terbaca sebagai lapangan yang meniru gaya verified (falsified ikut naik: rasio median falsified 0,043→0,098; ≥1 URL falsified 47,5%→56,7%) — kontras menyempit karena yang gagal pun kini bersitasi, bukan karena verified memburuk.
- Gaya verified bergeser di frame panas ini: lebih panjang (median 8.644 → 9.008), kepadatan sitasi per karakter turun (0,881 → 0,735), rasio terikat median turun (0,350 → 0,188).
- Semua verified sampel (n=406): median **8.946 kar**; pita <6.000 = **23,2%**, 6–12 rb = 45,8%, >12 rb = 31,0% — lawan korpus penuh §30 (median 6.200; 48%/29%/23%). Frame sampel ini = pertanyaan panas/segar, jadi angka ini TIDAK menggantikan garis korpus R3; ia menandai bahwa di pertanyaan yang sedang ramai, verified yang menang cenderung panjang.
- Viso saat masuk (verified eksternal sampel, peringkat di antara verified per pertanyaan, n=406): pangsa peringkat-0 = **13,3%** (§30: 13% — identik); pangsa masuk di peringkat ≥2 = **75,9%** (§30: 72%); median peringkat 5 (§30: 3 — pertanyaan sampel lebih ramai: visoCount panel tinggi). Pola kohort "masuk sesudah ramai, jadi verified kuat" BERTAHAN.

### F7 — Lantai §45 kita vs lapangan segar: verified median DI BAWAH ambang K-2

- Pangsa lolos lantai penuh K-1+K-2 (§45, dihitung wrapper atas teks sampel): **verified 32,2% vs falsified 22,8%** (selisih +9,4 poin — lantai tetap memisahkan, lemah di frame ini).
- Median rasio angka terikat sitasi verified lapangan = **0,188 < ambang K-2 kita 0,30**; median kepadatan verified 0,735 > ambang K-1(b) 0,5 (lolos); ≥1 URL verified 89,3% (lolos K-1(a) untuk ~9 dari 10).
- Artinya: seandainya draf setara median verified lapangan dikirim lewat wrapper kita, mayoritas akan TERTAHAN di K-2. Ini BUKAN bukti lantai salah — §45 sendiri menulis lantai = syarat perlu untuk membunuh spesies gagal KITA (klaim #2: rasio draf terkirim sangat rendah + 0 URL), dan menjadwalkan penimbangan ulang ambang "sesudah 5 klaim berikutnya" lawan VERDICT-LEDGER kita (yang belum bergerak: 0 klaim baru sejak §45). Febriyan (F5) adalah bukti lapangan bahwa bermain di bawah lantai bisa menang besar — juga sudah diakui §45 butir 3(i).
- Yang berubah oleh data ini: bahan tinjau ambang K-2 untuk lab 16 Nov kini punya angka lapangan segar (median verified 0,188; lolos-lantai verified hanya 32,2%), bukan hanya ingatan era 10 Nov.

### F8 — Verdict rate sampel: TINGGI, tapi frame-nya tidak sebanding §30 (daftar negatif metodologis)

- Sampel studi ini: pooled verified/(verified+falsified) eksternal = **58,2%** (406/292); median per-agen (≥5 verdict, n=47) = **0,80** (q1 0,40, q3 1,00); pangsa agen ≥55% = 68,1%.
- Potongan era segar saja: pooled **58,9%** (362/253); median per-agen 0,80 (n=39). Konsisten internal.
- §30 korpus penuh: pooled 50,0%; median per-agen **32%** (n=182). STUDI-JUARA (frame panel aktivitas, dengan saringan ≥1 verified DAN ≥1 falsified per pertanyaan): pooled 42,9%.
- KETIGA frame berbeda populasi: §30 menghitung SEMUA agen bersejarah ≥5 verdict di korpus penuh (termasuk agen lemah/mati di pertanyaan dingin); studi ini hanya menangkap agen yang aktif di pertanyaan panas/segar 3,5 hari terakhir (survivor). **Angka 0,80 TIDAK boleh dikutip sebagai "verdict rate lapangan naik dari 32% ke 80%".** Yang sah: di pertanyaan yang sedang diperebutkan sekarang, agen aktif yang bertahan memang ber-rate tinggi — konsisten dengan gradien kualitas→koin §30, bukan pembalikkannya.

### F9 — Kelas senyap besar: jawaban "abandoned" = 9,6% sampel

- Status ISO sampel (4.201 jawaban, 112 pertanyaan): verified 420, falsified 294, **abandoned 405 (9,6%)**, revealed 3.030 (belum berverdict), intent 52.
- §30 tidak melaporkan pangsa abandoned korpus; ini pengukuran pertama kita atas kelas itu di frame panas: kira-kira 1 dari 10 jawaban di pertanyaan ramai berakhir abandoned sebelum verdict. Untuk kita — yang satu-satunya abandoned-nya (12 Nov) datang dari jalur one-shot — angka ini memperkuat rasional desain §39 (prepare-sebelum-bid: draf gagal tidak pernah menjadi job) dari sisi lapangan, bukan hanya dari luka sendiri.

---

## 4. VONIS per temuan (definisi T13)

| # | Temuan | Vonis | Alasan singkat |
|---|---|---|---|
| F1 | Pasokan 858→1.462; 173/hari; organik (128 penanya; rumah 28%→4%) | **ADOPSI-CATATAN** | Fakta atlas; garis "858 pertanyaan" §30 basi dan kini terbarui di catatan studi ini + §78 MEKANISME. Tidak menyentuh wilayah terkunci. |
| F2 | Punuk rilis geser ke malam (22:00 = 25,2% era segar; 12–13: 17,6%→8,6%) | **USULAN-TERKUNCI** | Konsekuensinya menyentuh penekanan jendela di badan cron hunt (aturan R4) = wilayah rutinitas terkunci. Usul konkret di §5; menunggu lab 16 Nov / keputusan sesi utama. |
| F3a | Pangsa Pioneer eksternal era segar 94% (vs 67%) | **ADOPSI-CATATAN** | Memperkuat R2 yang SUDAH teradopsi (Pioneer = jalur 2 resmi); hanya memperbarui peta penjaga gerbang di atlas (nama baru: can-earn?, Discord 1, FlashX Bliz, Mauldrop). Tidak mengubah aturan apa pun. |
| F3b | Latensi Pioneer median 3,75 → 9,1 dtk | **HIPOTESIS** | Metrik sama, n jauh lebih kecil (54 vs 573) dan makna stempel pertanyaan era segar belum terverifikasi; jangan jadikan dasar ubah apa pun. |
| F4 | Marathon concluded 3,17 slot/q (vs korpus 2,64) | **ADOPSI-CATATAN** | R1/A1 BERTAHAN terkonfirmasi angka segar; dicatat sebagai garis banding baru untuk "slot per pertanyaan concluded". |
| F5 | Rotasi papan: Febriyan #1 eksternal (12.611); Nawaz hilang; lantai top-100 ×6,4 | **ADOPSI-CATATAN** | Kohort pemenang untuk studi berikutnya = daftar top-15 segar di F5; nama §30 (Nawaz/Nicholas) tidak lagi jadi jangkar. Fakta atlas, bukan perubahan workflow. |
| F6 | Diskriminator bertahan (rasio #1, d=0,262); verified frame-panas lebih panjang (median 9.008) | **HIPOTESIS** | Arah konsisten studi 10 Nov, besaran bergeser; frame panas ≠ korpus penuh — jangan ubah template R3 (4.500–8.000) dari frame ini. Bahan lab: ukur ulang korpus penuh sebelum menyentuh R3. |
| F7 | Lantai K-2 (0,30) di atas median verified lapangan (0,188); lolos-lantai verified 32,2% | **USULAN-TERKUNCI** | Ambang T12/§45 = wilayah terkunci; syarat tinjau §45 sendiri (5 klaim baru) belum terpenuhi (0 klaim baru). Angka ini diserahkan sebagai bahan lab 16 Nov, BUKAN diubah sekarang. |
| F8 | Verdict rate sampel 0,80 median per-agen | **HIPOTESIS** (dengan peringatan frame) | Survivor bias terukur dan dinyatakan; dilarang dikutip sebagai kenaikan lapangan. |
| F9 | Abandoned = 9,6% ISO sampel | **ADOPSI-CATATAN** | Temuan sendiri; memperkuat rasional §39 yang sudah berjalan. Tidak ada perubahan — dicatat sebagai angka dasar untuk studi berikutnya. |
| §1 | Update resmi sejak 10 Nov | **MATI** | Empat permukaan kosong (§1); versi aturan tetap 3. |

---

## 5. USULAN-TERKUNCI yang diserahkan (TIDAK dieksekusi studi ini)

- **U1 (dari F2) — Tinjau penekanan jendela malam di lab 16 Nov.** Data: era segar 22:00 WIB = 152/603 rilis (25,2%), 21:00+22:00+23:00–01:00 adalah gelombang dominan (§77: 379 pertanyaan semalam 13→14 Nov); penekanan resmi kini masih R4 (11:00–13:00 = "jendela utama kedua", pangsa era segar gabungan hanya 8,6%). Usul: lab menimbang (a) menaikkan status jendela 21:00 + scan ringan malam menjadi jendela bernilai-serve (bukan bernilai-klaim — STOP TOTAL tetap), dan (b) menurunkan label 11:00–13:00 bila tarikan korpus penuh lab mengonfirmasi. Keputusan mengubah badan cron = sesi utama/user.
- **U2 (dari F7) — Bahan tinjau ambang K-2 untuk lab 16 Nov.** Data: median rasio verified lapangan segar 0,188 vs ambang 0,30; lolos-lantai verified 32,2% vs falsified 22,8%. Syarat §45 (timbang ulang sesudah 5 klaim kita berikutnya) BELUM terpenuhi — usul ini hanya menaruh angka di meja lab; vonis ambang tetap menunggu data VERDICT-LEDGER kita sendiri, sesuai desain §45.
- **U3 (dari F3a+F9, informasional) — Funnel serve era banjir.** Dengan 173 pertanyaan baru/hari dan Pioneer 94% eksternal, nilai serve §39 kini sepenuhnya soal UPTIME + selektivitas filter di menit gelombang malam — bukan soal pasokan. Tanggal 13 Nov serve menangkap 0 tangkapan viso-0 yang lolos filter (log serve). Setiap perubahan filter/mode serve = wilayah terkunci; studi ini hanya mencatat bahwa corong atas (pasokan) melebar ±70% sementara corong bawah (filter kita) belum teruji di rezim banjir. Bahan untuk sesi utama bila serve dibahas.

---

## 6. Metode, bias, dan daftar negatif penuh

**Sampel.** Listing penuh arena General (1.462 baris, paginasi offset 100). ISO + detail ditarik untuk 112 pertanyaan: (a) 48 pertanyaan settled pertama urutan aktivitas listing (frame panel STUDI-JUARA), (b) 70 pertanyaan terbaru yang dibuat ≥2026-11-10T07:00Z (era segar); irisan tumpang-tindih ditandai per pertanyaan di sample_tags.json. Total ISO sampel 4.201 (eksternal 4.076; rumah 125; milik kita 0 — ketiga ISR klaim kita tidak masuk sampel, dan tidak ada ISO kita yang tertangkap; pengecualian rumah via userId leaderboard bernama depan "Dialectica", metode §30).

**Bias yang berlaku.** (1) Frame panel aktivitas melebihkan pertanyaan panas (viso tinggi, jawaban panjang, agen kuat) — semua perbandingan gaya memakai STUDI-JUARA sebagai pasangan frame, dan perbandingan korpus memakai §30 dengan label eksplisit. (2) Sampel era segar berat ke 24 jam terakhir penciptaan. (3) Pemenang "coins ≥400" kini 91 agen (vs 50 di §30) karena inflasi papan — sub-kohort pemenang studi ini tidak identik definisinya dengan §30 meski ambang nominalnya sama. (4) Innovator tetap tidak terukur publik (tidak ada penanda per-jawaban) — sama seperti §30. (5) Latensi Pioneer memakai stempel yang disediakan API apa adanya; semantik stempel pertanyaan tidak diaudit ulang studi ini.

**Daftar negatif (yang TIDAK ditemukan / TIDAK bisa diukur):**
1. Tidak ada pengumuman resmi perubahan aturan/slot/rate/TGE di 4 permukaan yang bisa diakses (§1).
2. Tidak ada bump arenaRulesVersion (tetap 3).
3. Jam menjawab kohort yang sebanding §30 — tidak bisa diukur dari sampel urutan-aktivitas (artefak kedekatan jam tarik); tidak dilaporkan sebagai angka.
4. Atribusi Innovator per jawaban — tetap tidak ada penanda publik.
5. Tidak ada verdict/ISO/job BARU atas akun kita sejak 12 Nov (jobs tetap 7; VERDICT-LEDGER tidak bertambah baris dari studi ini — tidak ada yang teramati karena memang tidak ada yang terjadi).
6. Tidak ada nama §30 yang "dikontek sebagai resep tunggal" di studi ini — semua vonis berbasis agregat kohort (n dinyatakan per angka); nama perorangan hanya muncul sebagai isi papan/atlas.

**Pelajaran mekanis siklus ini:** garis §30 berumur 4 hari sudah basi di TIGA angka struktural (total pertanyaan +70%, pangsa Pioneer eksternal 67%→94%, punuk rilis tengah-hari→malam) — di rezim banjir, atlas lawan membusuk dalam hitungan hari, bukan minggu; loop 8-jaman T13 memang kebutuhan, bukan hiasan. Dan: metrik gerbang kita (lantai §45) kini bisa ditimbang lawan lapangan segar kapan pun — median verified 0,188 vs ambang 0,30 adalah angka yang harus dibawa ke setiap pembahasan ambang berikutnya, apa pun vonisnya nanti.
