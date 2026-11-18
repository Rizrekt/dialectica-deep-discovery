# LAB KUALITAS — REVISI MINGGUAN DIALECTICA, SENIN 2026-11-16

**Jendela lab:** 10 Nov 00:00 – 16 Nov 11:42 WIB (minggu ini).
**Rubrik yang berlaku:** QUALITY.md **v2** (11 Nov 2026). **QUALITY.md TIDAK diedit lab ini** — semua perubahan di bawah adalah DRAF usul bernomor + draf entri CHANGELOG (§9) untuk diputuskan sesi utama.
**Status akun (jangkar §106 / LAB-FASE 15 Nov):** saldo **−1,8788 $TRUED**, RAR 118, Expertise 0, lifetimeEarned 0. Klaim STOP TOTAL + JEDA (ii) aktif; serve pilot tergating nyala 07:00 16 Nov, 0 generasi tercatat s/d 11:00 WIB (token-usage baris terakhir 04:00:46Z).
**Catatan slot:** lab 15 Nov malam (§106 MEKANISME) sudah memakai slot lab Senin untuk 8 butir (backtest gerbang serve, E3, sensus E1, pintu (e), sub-cek fase, U1, U2, audit kendali). Lab ini (11:42) adalah lab butir 10 yang ditugaskan — ia menambah drill 15 Nov 21:00 + 16 Nov 07:00/09:00/11:00, sampel lapangan segar n=670, dan putusan paket butir 11.

---

# 0. BEDAH STAGNASI — TEMUAN UTAMA (pemicu anti-stagnasi §33/butir 10(e))

**Vonis: STAGNASI RUBRIK NYATA — v2 beku sejak 11 Nov sementara bukti menumpuk 6 hari.**

Dua lab sebelumnya sama-sama berakhir tanpa bump versi:

| Lab | Penutup | Entri CHANGELOG? |
|---|---|---|
| §20, 9 Nov | "tanpa perubahan" + alasan (penutup sah) | Ya ("tanpa perubahan") |
| §106, 15 Nov (lab dimajukan, perintah user 19:10) | 8 butir diputus sebagai DRAF (E3 adopsi, U2 draf 0,15, U1 tunda) | **TIDAK ADA** — tidak ada entri changelog v2.1/v3 maupun "tanpa perubahan" di QUALITY.md. Ini celah penutup: lab yang berakhir tanpa bump DAN tanpa entri = pelanggaran aturan penutup (§33). |

Bedah penyebab, masing-masing dengan bukti angka:

1. **Pasokan verdict kita nol? YA untuk verified — tapi BUKAN penghalang belajar.** Minggu ini 7 falsified + 1 abandoned, **0 verified** (0/7). Namun pasokan belajar eksternal melimpah: sensus clean-sheet **465 iso ber-verdict, 0 penyimpangan**; sampel segar lab ini **670 verified / 156 agen**; 27 entri drill 13–16 Nov. Stagnasi bukan karena tidak ada data.
2. **Sampel lapangan tidak bergerak? BENAR — tapi bukan alasan diam.** Median panjang lapangan vs KORPUS-JUARA hanya +4,9% (10.016 vs 9.549 kar, §3). Yang bergerak bukan lapangan, melainkan BUKTI DISKRIMINASI rubrik: celah (b) ×31, (a) ×27, (h) ×17, anomali (e) 27/38 — semuanya menuntut putusan, bukan menunggu pergeseran lapangan.
3. **Rubrik sudah jenuh untuk kelas target? TIDAK — rubrik aktif salah di 3 butir.** (e) v2 gagal di 27/38 verified (71%); (b) v2 tidak membedakan di 31/31 kemunculan; (h) v2 false-positive pada 2 verified (07e5e10f, V1 db20e091). Rubrik yang salah bukan rubrik yang jenuh.
4. **Celah drill menumpuk tanpa putusan? YA — ini akar stagnasinya.** Sejak 12 Nov setiap entri drill menutup dengan "calon usul revisi lab mingguan" — (b) ke-13 (12 Nov 21:00) → ke-31 (16 Nov 11:00) tanpa satu pun putusan lab di antaranya. Mekanisme "celah ≥2 kali wajib naik usul ATAU ditolak beralasan" tidak pernah dieksekusi sampai lab ini.

**Tindakan pemecah (diusulkan ke sesi utama):** adopsi DRAF BUMP v3 di §9 lab ini (U-LAB-01…U-LAB-08) + tulis entri CHANGELOG-nya di giliran yang sama; dan mulai lab berikutnya, tiap celah yang mencapai kemunculan ke-2 WAJIB diputus di drill itu juga (usul bernomor atau tolak beralasan) tanpa menunggu lab mingguan.

---

# 1. (a) SKOR MINGGUAN — jawaban kita yang settle minggu ini

## 1.1 Ringkasan

| | Angka |
|---|---|
| Jawaban kita settle minggu ini (verdict-bearing) | **7 — SEMUA falsified, 0 verified** |
| Abandoned (bukan verdict, disiplin) | **1** (b4d7ab24, 12 Nov) |
| **Rate verified kita minggu ini** | **0/7 = 0%** (benchmark §30: median pemenang ≥55%, median kohort 32%, n=182) |
| Saldo minggu ini | 5,1212 → **−1,8788** (7 × −1, rekonsiliasi ✓) |

Definisi minggu: 10 Nov 00:00 – 16 Nov 11:42 WIB. Sumber: VERDICT-LEDGER.md baris #1–#8 + MEKANISME §82/§96/§97.

## 1.2 Tabel settle (nilai ulang lawan QUALITY.md v2 — versi saat dikirim: klaim #1–#3 di bawah v1; serve tanpa rubrik)

| # | ISO kita | Jalur / model | Verdict (panel) | Skor v2 (reskor) | Akar (kelas §1.4) |
|---|---|---|---|---|---|
| 1 | fcb7b015 (60fa9935) | Klaim one-shot / Nemotron | FALSIFIED 2/2/4, 263 dtk | (d) G — tidak di-reskor penuh v2 (pra-v2; bedah BEDAH-TOTAL-2026-11-10) | (d) sitasi |
| 2 | 097df475 (472b29a0) | Klaim one-shot / Nemotron | FALSIFIED 0/4/4, ±5 mnt | (d) G — bedah BEDAH-KLAIM2-2026-11-10 | (d) sitasi |
| 3 | 0d76cc7c (71f472d6) | Klaim one-shot / Cloudflare gpt-oss-120b | FALSIFIED 0/1→0/2, panel 2, ±135 dtk | **6/9** — (a)L (b)G (c)L (d)L-borderline (e)L (f)L (g)L **(h)G (pintu mati)** **(i)G**; T12 3/3 (7 URL, densitas 1,36, rasio 0,58) — drill 14 Nov 19:00 | (b) struktur / (h) scope-miss + (i) |
| 4 | — (b4d7ab24) | Klaim uji / Vyce deepseek-v4.1 (draf) | **ABANDONED (DROPPED)** 12 Nov 07:19 | N/A — 0 submitted; draf probe lolos semua gerbang, draf di `trued answer` tertahan wrapper (sendable=false) | Operasional (bukan kelas rubrik) — cacat §1.5 |
| 5 | f0bb3586 (1287c2ae) | Serve / Vyce GLM 5.3 Flash | FALSIFIED 0/1→0/2, panel 1→2, ±85 dtk | **3/9** (c,f,g) — gagal (d)+(h)+(i) pintu mati; T12 0/3; 38.591 kar, 0 URL, 557 angka, 0 sitasi | (d) sitasi + (e) E3 |
| 6 | 7d81c51d (30fe9eea) | Serve / Vyce GLM 5.3 Flash | FALSIFIED 0/4/5, ±20 jam 43 mnt | Tidak di-drill-skor (spesies sama #5; backtest: T12 0/3, 0 URL) | (d) sitasi + (e) E3 |
| 7 | 5b5e8212 (a361a16b) | Serve / Vyce GLM 5.3 Flash | FALSIFIED 0/4/6, ±21 jam 32 mnt | **3/9**; T12 0/3; 37.098 kar, 0 URL, 657 angka | (d) sitasi + E1-p + (e) E3 |
| 8 | a3b8b34a (3884b6c3) | Serve / Vyce GLM 5.3 Flash | FALSIFIED 0/6/6, ±22 jam 01 mnt | **3/9**; T12 0/3; 43.623 kar, 0 URL, 296 angka | (d) sitasi + E1-p + (e) E3 |

**Skor gerbang kualitas 4A dari catatan jendela minggu ini: TIDAK ADA.** 0 klaim dieksekusi 12–16 Nov (STOP TOTAL + JEDA mengunci); MEKANISME §97 butir 8 dan §98 butir 8 menulis verbatim "Tidak ada klaim dieksekusi → tidak ada skor 4A per klaim." Skor di tabel di atas adalah reskor drill/lab atas teks terkirim (butir 3A), bukan skor pra-kirim 4A. Steering staged 60fa9935/472b29a0/71f472d6 tetap BUANG dan tidak diubah minggu ini.

## 1.3 Rate verified per MODEL (butir 5 — data token-usage.jsonl + log serve)

Token-usage minggu ini: **126 baris, biaya $0,00 semua** (promo/free).

| Model | Eksekusi minggu ini | Completed | Verified | Falsified / Abandoned | Token total | Vonis |
|---|---|---|---|---|---|---|
| Nemotron-3-ultra (OpenRouter) | 2 klaim (#1, #2) + 41 baris drill/probe | 2 | **0/2 = 0%** | 2 falsified | 218.464 | 0% — konsisten era pra-disiplin |
| Cloudflare gpt-oss-120b | 1 klaim (#3) + 14 baris drill | 1 | **0/1 = 0%** | 1 falsified | 237.268 | 0% (n=1) |
| **GLM 5.3 Flash (Vyce serve)** | **26 serve** (14 Nov 00:07–02:01 UTC, ±143–166 rb token/generasi, 35–45 rb kar jawaban) | 26 | **0/4 settle = 0%** (22 revealed menunggu verdict) | 4 falsified | 3.921.366 (55 baris) | 0% atas yang settle; 22 paparan terbuka |
| **deepseek-v4.1 (Vyce, klaim A6)** | **0 eksekusi** — hanya 4 baris probe (12–13 Nov, 1.232 token, jawaban 2 kar) | 0 | **n=0 — tidak terukur** | — | 4.930 | **A6 BELUM TERUJI** |
| deepseek-v4-pro (DashScope) | 0 klaim (3 baris probe 10–11 Nov) | 0 | n=0 | — | 7.949 | — |
| glm-4.7-flash (Z.ai) | 1 baris probe | 0 | n=0 | — | 8.133 | — |

**Vonis routing A6 (klaim=v4.1, serve/scan=GLM): PERLU DATA LAGI.** Tidak satu pun klaim minggu ini memakai v4.1 — rate verified v4.1 tidak bisa dihitung dari n=0. GLM sebagai serve terbukti MEMPRODUKSI jawaban (26/26 berkonten) tapi 0/4 atas yang settle, semuanya spesies serve-mentah pra-gerbang (0 URL; penutup E3 ternyata artefak `citation_patch` v1 — lihat §2.5). Routing dipertahankan sebagai spekulasi terukur (§30.5 R7) sampai ada klaim v4.1 yang settle; klaim uji berikutnya (bila STOP dicabut) WAJIB memakai v4.1 + 4A penuh + lane-probe, agar A6 akhirnya terukur.

## 1.4 Rate verified per VERSI TEMPLATE/RUBRIK

| Versi | Jawaban settle | Verified | Keterangan |
|---|---|---|---|
| v1 (era steering v1, klaim #1–#3, 10–11 Nov) | 3 | **0/3 = 0%** | Semua mati di (d)/E1 atau (h)/(i) — persis yang v2 dirancang menangkap |
| Serve mentah (tanpa rubrik sama sekali) | 4 | **0/4 = 0%** | Rubrik tidak pernah diterapkan di jalur serve — celah cakupan gerbang, bukan isi rubrik (§4.3) |
| **v2 (11 Nov – kini)** | **0** | **n=0 — TIDAK TERUKUR** | Tidak ada jawaban yang dikirim di bawah v2 dan mencapai verdict. Rate v2 tidak bisa dinilai minggu ini; klaim pertama v2 adalah ujian sesungguhnya |
| Abandoned (disiplin) | 1 | — | Bukan verdict; dihitung di REL, bukan di rate |

**n=0 untuk v2 adalah temuan, bukan kekosongan laporan.** Lab minggu depan WAJIB menilai v2 dari klaim/serve pertama yang settle di bawahnya; sampai saat itu semua klaim tentang v2 ("lebih baik dari v1") adalah hipotesis, bukan hasil.

---

# 2. (b) BEDAH KEGAGALAN — tiap jawaban falsified/gagal-aturan sampai akar

Kelas akar: (a) pembuka / (b) struktur / (c) panjang / (d) sitasi / (e) kebaruan / (f) parafrase / (g) format. Tiap akar → satu USUL REVISI bernomor (U-LAB-nn, §8).

## 2.1 Klaim #1 — fcb7b015 (Nemotron, 10 Nov) — akar (d) SITASI

Klaim dominasi bernama-rantai ("700 gas DELEGATECALL", "3 MB standalone", "+1.500 gas/tx") diikat ke sitasi yang tidak mendukungnya (A_CITATION; BEDAH-TOTAL-2026-11-10). Lolos semua ambang mekanis pra-§45, mati di dukungan semantik. **Usul: TIDAK ADA yang baru** — akar ini SUDAH diadopsi sebagai sub-cek E1 di (d) v2. Dicatat sebagai validasi adopsi (kasus E1 ke-1 dalam rantai).

## 2.2 Klaim #2 — 097df475 (Nemotron, 10 Nov) — akar (d) SITASI

Racun masuk saat GENERASI: parameter BSC salah faktual tanpa sitasi (base fee "EIP-1559", blok "~3 dtk / 21 validator", "~21.000 gas"); lolos wrapper 3× karena tabel kanonis tak memuat parameter BSC + angka tak terikat lolos audit (BEDAH-KLAIM2-2026-11-10). Parameter basi yang sama membunuh 0be4bf85 + 755b3f19 (drill 12 Nov 09:00). **Usul: TIDAK ADA yang baru** — akar ini sudah ditutup v2 (E1 + sensus tanggal-berlaku parameter di steering 1d758352). Validasi: larangan angka BSC basi di steering TERBUKTI benar.

## 2.3 Klaim #3 — 0d76cc7c (GPT-OSS, 11 Nov) — akar (b) STRUKTUR + (i)

Reskor v2 (drill 14 Nov 19:00): **6/9**. (d) LOLOS borderline (Goodhart/Campbell/MAPE/HACCP ke Wikipedia nyata; sintesis Tier-0, tanpa angka poros karangan), (e) LOLOS (penutup menamai spine anti-gaming yang BENAR per grep), T12 3/3 — tetapi **(h) GAGAL pintu mati** (0 aplikasi AI dinamai dari sub-pertanyaan eksplisit (a); customer experience tidak dijawab) dan **(i) GAGAL** (definisi konsep saja, 0 fakta/angka dunia). Falsified 0/1→0/2, panel 2. **Pelajaran:** (h)/(i) v2 MENANGKAP KEMBALI jawaban yang melahirkannya — gerbang v2 bekerja atas spesies ini. **Usul → U-LAB-03** (turunkan (b) jadi catatan; (h) tetap pintu mati) **+ U-LAB-08** (gradasi (h): miss total vs parsial).

## 2.4 Abandoned #4 — b4d7ab24 (Vyce v4.1, 12 Nov) — akar OPERASIONAL, bukan rubrik

Job DROPPED: draf segar di `trued answer` (5.860 kar) tertahan wrapper (sendable=false, floor=1, wrong=0, bound-unverified=0), 0 submitted; server menutup job FAILED ("Agent transport disconnected…"). Draf probe (7.187 kar) LOLOS semua gerbang — **draf yang digerbang ≠ draf yang dikirim** (cacat §1.5 EVALUASI). REL −1 (reliability −3→−4), suspensionCount 3→4. **Usul → U-LAB-10** (proses, bukan rubrik): draf yang digerbang WAJIB identik byte-dengan-byte dengan draf yang dikirim; audit draf-terkirim (`audit_sent_draft.py`) wajib sebelum klaim berikutnya; wrapper menahan = JANGAN kirim ulang tanpa regenerasi + gerbang ulang.

## 2.5 Serve #5–#8 — f0bb3586, 7d81c51d, 5b5e8212, a3b8b34a (Vyce GLM, 14 Nov) — akar (d) SITASI + (e) E3

Spesies sama, 4/4: teks terkirim 36.679–43.623 kar, **0 URL**, 0 header ##, jejak pikiran mentah ("Let me…" 8–21×), 296–657 angka tanpa sitasi, penutup evasif sumber verbatim. Skor v2 3/9 (c,f,g); T12 0/3; marathonEligible=FALSE (upside $0); panel 1→6; latensi verdict 85 dtk – 22 jam 01 mnt. E1-p: 5b5e8212 22× "Answer 41", a3b8b34a 43× "Answer N" sebagai sumber angka poros.

**KOREKSI ATRIBUSI (temuan IMPROVE-2026-11-16, wajib dicatat):** penutup evasif E3 itu **ditulis oleh kode kita sendiri** — `citation_patch.py` v1 membuang SEMUA URL/DOI lalu menempel note evasif verbatim di ekor jawaban. Jadi 0-URL + E3 pada 4/4 serve ini SEBAGIAN artefak pipa, bukan perilaku model. Backtest 26/26 serve 0-URL ikut tercemar artefak yang sama. Implikasi: (i) E3 sebagai sinyal tetap sah (frasa itu tidak boleh muncul — kini dicegah patch v2 + gerbang), tapi (ii) vonis "model GLM evasif" DICABUT — yang evasif adalah cleaner v1; (iii) argumen "lantai K-2 terlalu kasar" (U2) harus dibaca ulang — sebagian false-rejection historis adalah artefak cleaner, meski bukti korpus-juara (independen dari pipa kita) tetap mendukung turun ke 0,15 (§7).

**Usul → U-LAB-01** (adopsi E3 sebagai sinyal tahan gerbang + cek negatif (e)/(d)) **+ U-LAB-06** (E1-p: "Answer N" sebagai sumber angka poros = (d) gagal; sudah di kontrak serve P-3 IMPROVE — lab mengesahkan).

## 2.6 Ringkasan akar minggu ini

| Akar | n | ISO |
|---|---|---|
| (d) sitasi / E1 | 6 dari 7 falsified | #1, #2, #5, #6, #7, #8 |
| (b) struktur / (h)+(i) | 1 dari 7 | #3 |
| Operasional (abandoned) | 1 | #4 |
| (a)/(c)/(e)-murni/(f)/(g) | 0 | — |

**Tidak satu pun falsified minggu ini berakar (a), (c), (f), atau (g) sebagai penyebab utama.** (e) muncul hanya sebagai pendamping (E3) pada spesies serve. Kesimpulan bedah: (d) tetap pembunuh tunggal kita (6/7) — dan (d) v2 + E1 + gerbang serve adalah jawaban yang sudah dibangun; yang belum teruji adalah apakah jawaban yang LOLOS (d) v2 bisa verified (n=0, §1.4).

---

# 3. (c) SAMPEL LAPANGAN SEGAR — jawaban verified kohort General

**Metode:** sweep `run-2026-11-16-1100/isos-*.json` (32 ISR panel, tarikan 11:00 WIB 16 Nov) — semua ISO status verified dengan `updatedAt` 10–16 Nov 2026 dan teks reveal ≥100 kar. BUKAN satu teladan. Teks diekstrak dari `reveal.data.structured_data.answer`.

## 3.1 Angka sampel

| Ukuran | Hasil (n=670) |
|---|---|
| Jawaban verified | **670** dari 156 agen berbeda, 32 ISR |
| Panjang | median **10.016 kar** (q1 6.894, q3 14.136; mean 11.530; min 438; max 55.047) |
| Pita panjang | <4.500: **57 (8,5%)** · 4.500–8.000: 178 (26,6%) · 8.000–12.000: 189 (28,2%) · >12.000: **246 (36,7%)** |
| Header ##/### | **501/670 = 74,8%**; bernomor 398/670 = 59,4% |
| URL sitasi | ≥1 URL: **598/670 = 89,3%**; median 6,0 URL/jawaban; mean 10,0 |
| Kepadatan sitasi (URL+bracket per 1.000 kar) | median **0,64**; mean 1,09 |
| Pola pembuka (kalimat pertama) | tesis/panjang (≥40 kar, non-generik): 485 (72,4%) · generik (regex sempit): 0 · lain (judul/pendek): 185 (27,6%) |
| Penutup menamai kebaruan (regex longgar, 1.200 kar terakhir) | **54/670 = 8,1%** |

Agen terbanyak: Hermawan Kwan 23, Dialectica (Pioneer) 20, megumii 20, Mauldrop 18, Febriyan 18, Adam Reinhard 17, kasnapp 17. (Dialectica (Pioneer) adalah akun rumah — mengeluarkannya tidak mengubah kesimpulan: tetap ≥150 agen eksternal.)

## 3.2 Banding (i) lawan rubrik kita saat ini

- **(c) panjang: rubrik KALAH telak di plafon, lantai pun tidak mengikat.** Median lapangan 10.016 kar; 36,7% verified >12.000 kar (plafon anjuran v2 sudah benar bukan pintu). Lebih tajam: **8,5% verified di bawah lantai 4.500** — dan drill mencatat 5 verified+awarded di bawah lantai (3.009, 3.238, 3.755, 4.053, 4.326 kar). Lantai 4.500 sebagai pintu gagal menolak pemenang. → **U-LAB-05** (lantai → 3.000).
- **(b) struktur: header 74,8% — dekat asumsi rubrik (79% R3), tapi bentuknya longgar.** Header bernomor hanya 59,4%; 25,2% verified TANPA header ##/### sama sekali (termasuk awarded: 6b7267f2 3.009 kar, bfd1ca7a). → **U-LAB-03**.
- **(d) sitasi: URL 89,3% (naik dari 77% R3); kepadatan median 0,64.** Median lapangan LOLOS K-1(b) 0,5 — tapi tipis; korpus-juara median 0,842. K-1(b) bukan pemisah kuat di lapangan kini; (d)/E1 (entailment) yang memisahkan. → mendukung U-LAB-06 (operasionalisasi E1), bukan menaikkan ambang K-1.
- **(e) kebaruan: rubrik v2 BERTENTANGAN dengan lapangan.** Penamaan eksplisit ketat di korpus-juara hanya **1/203 = 0,5%**; regex longgar lab ini 8,1%. Sementara drill: **27/38 verified (71%) GAGAL (e) v2**. (e) sebagai syarat penutup = menuntut sesuatu yang 92–99,5% pemenang tidak lakukan. → **U-LAB-02** (reformulasi total (e)).
- **(a) pembuka: 72,4% kalimat pertama tesis/panjang** — (a) sebagai ARAH benar, tapi sebagai hitungan ≤3 kalimat ia false-positive (844f4a1d: tesis tajam 4 kalimat, verified). → **U-LAB-04**.

## 3.3 Banding (ii) lawan sampel lab minggu lalu

**Tidak ada sampel lab minggu lalu** — lab mingguan sebelumnya (§20, 9 Nov) tidak menarik sampel lapangan; CHANGELOG QUALITY.md menyatakan lab 16 Nov ini lab mingguan pertama yang wajib menulis entri. Pembanding yang sah:

| Pembanding | Median panjang | Header | URL ≥1 | Kepadatan |
|---|---|---|---|---|
| R3/§30 (n=4.440 verified, 165 agen) | 6.200 | 79% | 77% | — |
| KORPUS-JUARA (n=203 verified, 12 agen juara) | 9.549 | 78,8% | URL median 6,0 | 0,842 |
| **Lab ini (n=670)** | **10.016 (+4,9% vs juara; +61,6% vs R3)** | **74,8% (−4,0pp vs juara)** | **89,3% (+12,3pp vs R3)** | **0,64 (−24% vs juara)** |

**Selisih material: TIDAK ADA vs korpus-juara.** Gap +61,6% vs R3 adalah KOMPOSISI panel (ISR pantau marathon-ramai, jawaban panjang), bukan pergeseran lapangan — dibuktikan selisih hanya +4,9% lawan korpus-juara yang metodenya sama (juara, teks penuh). Kepadatan −24% vs juara adalah satu-satunya selisih yang patut dipantau (median 0,64 vs 0,842) — belum material (masih di atas lantai K-1(b) 0,5), dicatat sebagai pantau lab berikutnya, bukan pemicu revisi.

---

# 4. (d) GERBANG REVISI TEMPLATE — putusan

**Putusan: BUMP v3 (DRAF) — 8 usul bernomor di §8, semuanya didukung angka** (rate verified kita §1 + pergeseran/diskriminasi lapangan §3 + hitungan drill §5). Bukan "tanpa perubahan": tiga butir rubrik terbukti aktif salah ((e), (b), lantai (c)) dan dua butir butuh tafsir operatif ((a), (h)). Draf entri CHANGELOG v3 di §9; adopsi oleh sesi utama.

# 5. (e) TINJAUAN DRILL + ANTI-STAGNASI

## 5.1 Cakupan drill minggu ini

**27 entri drill 13–16 Nov** (8 + 8 + 8 + 3), semuanya BEDAH (0 bayangan baru sejak 13:00 11 Nov — tidak ada kandidat hidup + STOP TOTAL + hemat pool promo di jendela pilot). Cek bayangan menunggu: **TIDAK ADA yang tertunda** (1d3efb52-1126 TERISI 13:00 11 Nov; 02:11 DIBATALKAN cacat alat).

## 5.2 DAFTAR CELAH RUBRIK KUMULATIF (keadaan s/d drill 11:00 16 Nov)

| Celah | Hitungan | Arah | Putusan lab ini |
|---|---|---|---|
| (b) tidak membedakan (falsified lolos (b) v2) | **ke-31** | Falsified lolos; verified gagal (b) ×2 (07e5e10f, V2 71f472d6) + false-positive (b) ×2 (V5 2d968d7e tanpa header, bfd1ca7a) | **U-LAB-03** — turun jadi catatan |
| (a) tidak membedakan (falsified lolos (a)) | **ke-27** | + false-positive (a) ke-1 (844f4a1d, tesis tajam 4 kalimat) | **U-LAB-04** — tafsir 3-kalimat-tesis |
| (h) tidak membedakan (falsified lolos (h)) | **ke-17** (vs 3 tangkapan) | + verified-gagal-(h) ×2 (07e5e10f, V1 db20e091) | **U-LAB-08** — gradasi miss total vs parsial |
| Plafon (c) tidak mengikat | **ke-26** | Verified >12 rb kar berulang (terpanjang 47.978 kar) | **DITOLAK sebagai usul baru** — sudah anjuran di v2; terkonfirmasi benar, bukan celah terbuka |
| Lantai (c) tidak mengikat | **observasi ke-5** | 5 verified+awarded <4.500 kar | **U-LAB-05** — lantai → 3.000 |
| Proksi (i) vs manual | **ke-11 disagreement** | Proksi hitung proksimitas, bukan entailment | **U-LAB-07** — label proksi + cek manual wajib |
| (e) anomali | **27/38 verified gagal (e)** (71%; ketat 28/38) | Mati total/terbalik di sebagian besar ISR; ISR-spesifik (df9cb696: 7/10 LOLOS (e); 2d968d7e: 24/27 gagal) | **U-LAB-02** — reformulasi (e) |
| E1 (angka tanpa sitasi pendukung) | **ke-43** | 3 di antaranya jawaban kita (ke-30, ke-40, ke-41); ke-42 pada verified+awarded (kalibrasi (d)) | Validasi adopsi v2; **U-LAB-06** konsolidasi sub-pola |
| E1-p "pinjam angka dari Answer N" | **4 instance** | Melemah ×4 (verified dengan "Answer N" konseptual: f557911e "Answer 52", 33787163 "Answer 25", 1a833948, c202875b) | **U-LAB-06** — persempit ke angka poros |
| E1-c label bertabrakan | 2 makna, 1 nama | Kausal-salah (2 kemunculan) vs klaim-korpus-salah-baca (1) | **U-LAB-06** — pecah E1-c1/E1-c2 |
| E1-a / E1-b | **TIDAK TERDEFINISI** | Grep seluruh folder kosong; seri bernama mulai di E1-c | **U-LAB-06** — nyatakan seri dimulai E1-c; jangan retro-namai |
| Spesies "jawaban terpotong" | **ke-21** (+kandidat pra-penutup ke-17–21) | Terpotong di tengah sitasi/rencana | **DITOLAK sebagai usul rubrik baru** — sudah tertutup lantai (c)+K-1/K-2 (vonis drill sendiri); kandidat pra-penutup = varian yang sama, klasifikasi selesai |
| Spesies baru "dump tool-call mentah" | ke-1 (F1 2d968d7e 11:00 15 Nov) | Jejak pemanggilan tool terkirim sebagai jawaban | **DITOLAK sebagai usul rubrik** — sudah ditangkap lapis trace gerbang serve (LAB-BACKTEST); bukan celah rubrik klaim |
| Kalibrasi T12 | **observasi ke-13** | Verified lolos K-2 tapi gagal K-1 (densitas 0,37/0,40) berulang; K-1 gagal ≠ verdict gagal | Bahan U2 (§7) — bukan usul rubrik |
| Falsified-dengan-support | seri ke-13 | ≥1 refutasi = falsified, support tidak menyelamatkan (termasuk panel terbelah 2–2) | Model §43 bertahan; bukan celah rubrik |
| Sensus clean-sheet | **465 iso, 0 penyimpangan** | verified ⟺ ≥2 support DAN 0 refutasi; 1 refutasi membunuh (panel 1–6) | Model bertahan; L-02 TERJAWAB sebagian (36492578 verified+awarded, panel 2 — sisi verified panel-1 masih belum teramati) |

**Tidak ada celah ≥2 kali yang dibiarkan menggantung tanpa putusan di lab ini** — tiap baris di atas berakhir di usul bernomor §8 atau penolakan beralasan di atas.

## 5.3 ANTRIAN EKSPERIMEN — status tiap hipotesis

| Hipotesis | Status minggu ini | Bukti |
|---|---|---|
| **E1** — sitasi harus mengikat angkanya | **DIADOPSI di v2 — TERVALIDASI** | Ke-43 (LAB-E3 sensus cocok Δ0); sub-pola baru minggu ini: E1-h, E1-i, E1-j, E1-k, E1-l, E1-m, E1-n, E1-o, E1-p, E1-c (makna ke-2), E1-f, E1-g (12–15 Nov). E1 kini keluarga sub-pola, bukan satu cek → U-LAB-06 |
| **E2** — gerbang lane mendahului gerbang jawaban | **MENUJU AMBANG (parsial)** | GLM: 26/26 generasi serve berkonten >0 (kriteria konten terpenuhi). v4.1: 4 probe, jawaban 2 kar — BELUM lolos probe kelas-klaim. Ambang (≥1 model lolos penuh) terpenuhi untuk GLM saja; formalisasi gerbang lane menunggu klaim v4.1 pertama |
| **E3** — penutup evasif sumber = gagal (e) + bendera (d) | **AMBANG TERCAPAI → USUL ADOPSI (U-LAB-01)** | 4/4 falsified serve kita (×4 ambang); false-positive 0/203 verified + 0/64 falsified korpus-juara; 0× di semua drill publik 13–16 Nov. **Koreksi atribusi:** frasa ditulis `citation_patch` v1 (IMPROVE) — adopsi sebagai tripwire pipa + cek negatif, bukan vonis perilaku model |

---

# 6. PAKET KEPUTUSAN LAB (butir 11 badan weekly-revision — tiap item diputuskan ATAU ditunda beralasan)

| # | Item | Putusan lab ini | Dasar angka |
|---|---|---|---|
| (1) | U1 JENDELA MALAM | **TUNDA** (parsial, sesuai LAB-FASE) | Punuk 22:00 MATI di data segar: run 4 43/278 (15,5%) vs era segar 152/603 (25,2%); tangkapan 21:00 14 Nov 98 rilis, 0 topik inti; pasokan inti ≈0 di semua jam. Syarat uji ulang: tangkapan 21:00 15 Nov + ≥1 malam non-banjir + cakupan versi pasokan-inti |
| (2) | U2 AMBANG K-2 | **PUTUSKAN dari data lapangan → opsi (i) turun 0,30 → 0,15** (keputusan final user/sesi utama) | Korpus n=203/64: lantai penuh @0,30 gap +4,4pp vs @0,15 +24,8pp; run 6 gap @0,30 +12,7pp vs @0,15 +26,3pp; false-rejection verified 67,5%→42,4% (−25,1pp). Dalam-K-1 @0,30 terbalik di semua frame (−19,4pp korpus). Penyeimbang: 3/3 falsified kita lolos K-2 di kedua ambang (K-2 bukan penangkap spesies kita); IMPROVE: sebagian kekasaran historis adalah artefak cleaner v1 — tapi bukti korpus independen dari pipa kita, rekomendasi berdiri |
| (3) | E3 ADOPSI | **PUTUSKAN ADOPSI** (U-LAB-01) | Ambang ×4; FP 0,0% (0/203). Bentuk: sinyal TAHAN gerbang + cek negatif (e)/(d); cek dibatasi frasa eksplisit di penutup/seksi sumber |
| (4) | GERBANG SERVE | **PUTUSKAN: syarat hidup TERPENUHI bersyarat** | Backtest n=29: 4/4 falsified serve tertahan (3 lapis mandiri); 22/22 revealed tertahan; 0/26 lolos isi. Pilot 07:00 16 Nov nyala, 0 generasi s/d 11:00 WIB. C5 permanen (semantic_check) MASIH UTANG — jembatan: spot-check manual 3 jawaban pertama (CHECKLIST D). Serve tetap DITAHAN MATI di luar pilot; restart penuh BUKAN keputusan lab ini |
| (5) | FILTER LIVENESS TIGA-FIELD | **DINILAI: BEKERJA, dipertahankan** | Backtest: 25/26 target serve MATI benar; 4/4 falsified MATI; 0 draf terkirim ke target mati. Catatan jendela minggu ini konsisten (flag basi = MATI). Tidak ada perubahan |
| (6) | SUB-CEK ARITMETIKA | **PUTUSKAN ADOPSI** (bagian U-LAB-06) | E1-f (kontradiksi-internal, 8539092c "1.3 B of 1 B") + pemenang dengan aritmetika dicek-di-teks (e5abc76e, 15084f8d, 42aea0e2). Sub-cek: (i) konsistensi-internal angka poros (jumlah komponen = total); (ii) turunan ditandai hitungan + dicek benar di teks |
| (7) | TAKSONOMI E1-p / E1-c | **PUTUSKAN** (U-LAB-06) | E1-p dipersempit → hanya angka poros yang disitasi ke "Answer N" (melemah ×4 oleh verified konseptual). E1-c dipecah → E1-c1 kausal-salah, E1-c2 klaim-korpus-salah-baca |
| (8) | ANOMALI PINTU (e) | **PUTUSKAN** (U-LAB-02) | (e) v2 gagal 27/38 verified; penamaan eksplisit ketat 0,5% korpus-juara. (e) direformulasi: kebaruan substantif di posisi mana pun (pembuka/sintesis/penutup); penamaan eksplisit jadi anjuran; cek kebenaran (v2) dipertahankan. Tafsir operatif diputus: 01d43336 + 59bed01d (borderline) = LOLOS di bawah tafsir baru |
| (9) | UNIT SYSTEMD SERVE VYCE | **TETAP PARKIR** | Hilang 7× tercatat; pilot jalan via jendela hunt, bukan systemd. Nilai ulang HANYA bila serve hidup penuh — bukan sekarang |
| (10) | 3 EDGE-SAH KULIT-SISTEM | **DINILAI: ketiganya TERKONFIRMASI** | (i) award≠verdict: award diputus (f)+timing (36492578 awarded dengan (e) gagal; V10/V11 (f)L tidak awarded — pola (f) terkoreksi, bukan mati); pisahkan Skor Verdict vs Skor Award. (ii) flag basi→liveness: bekerja (butir 5). (iii) triase gelombang jam: metode sah, hasilnya menunda U1 (butir 1) |

---

# 7. USUL REVISI BERNOMOR (gerbang §4 — adopsi hanya lewat sesi utama)

**U-LAB-01 — Adopsi E3 (penutup evasif sumber).** (e) tambah cek negatif eksplisit + gerbang serve: draf yang penutup/seksi sumbernya memuat frasa keluarga ("avoids pinpoint references", "cannot be verified from the text alone", "no live web access", "I give no URLs", "relies on widely documented … rather than on any single citation") = TAHAN (serve: tidak dikirim; klaim: sendable=false) + (e) GAGAL + bendera (d). Dasar: ambang ×4 (4/4 falsified serve kita); FP 0/203 verified korpus-juara + 0 di semua drill 13–16 Nov. Batas: cek hanya frasa eksplisit di penutup/seksi sumber (bukan bahasa penundaan di badan — 0006fe08 verified). Koreksi atribusi: frasa pada jawaban kita ditulis `citation_patch` v1 — tripwire pipa, bukan vonis model. → **v3 (e) + gerbang serve.**

**U-LAB-02 — Reformulasi (e): kebaruan substantif, bukan penamaan di penutup.** (e) v2 ("penutup 2–3 kalimat MENYEBUT apa yang baru") diganti: (e) LOLOS bila jawaban memuat kebaruan substantif yang BENAR (lolos (d) atas dasarnya + absen dari verified yang ada) di posisi mana pun — pembuka, seksi "What this adds", sintesis penutup, atau "Verdict: … factors". Penamaan eksplisit "Baru dalam jawaban ini:" jadi ANJURAN, bukan syarat. Dasar: 27/38 verified gagal (e) v2 (71%); penamaan ketat 1/203 (0,5%) korpus-juara, 8,1% regex longgar sampel n=670; 4 bentuk penamaan diterima verifier (pembuka d20b7bda/91c01d0f, §7 "What this adds", daftar eksplisit 15084f8d, sintesis penutup f4b4e157). → **v3 (e).**

**U-LAB-03 — (b) turun dari gerbang skor jadi catatan cakupan.** (b) v2 (cakupan sub-pertanyaan) tidak membedakan di 31/31 kemunculan drill; verified gagal (b) ×2; false-positive (b) ×2 (verified tanpa header). (b) dicatat sebagai checklist (daftar sub-pertanyaan → seksi), bukan LOLOS/GAGAL. (h) tetap pintu mati cakupan. Dasar: celah (b) ke-31; skor total tidak memisah tanpa (d). → **v3 (b).**

**U-LAB-04 — Tafsir operatif (a): hitung 3 kalimat TESIS.** (a) ≤3 kalimat dinilai atas 3 kalimat tesis pertama; kalimat ke-4+ yang berupa catatan metode/hasil ("verify exact current values…", enumerasi) tidak menggagalkan. Dasar: 10 kasus drill diputus dengan tafsir ini (15084f8d 5 kalimat, 91c01d0f 4 kalimat, 11f4031f, dst.); false-positive (a) ke-1 (844f4a1d, tesis tajam 4 kalimat). (a) tetap butir skor, bukan gerbang. → **v3 (a) — klarifikasi.**

**U-LAB-05 — Lantai (c) 4.500 → 3.000 kar.** Dasar: 5 observasi verified+awarded di bawah lantai (3.009, 3.238, 3.755, 4.053, 4.326 kar); verified terpendek seri 3.009 kar; 8,5% sampel n=670 verified <4.500. Plafon tetap anjuran. Falsified pendek tetap tertangkap (d)/(h). → **v3 (c).**

**U-LAB-06 — Konsolidasi keluarga E1 di (d) v3 (operasionalisasi buka-dan-baca).** (d) dilengkapi daftar periksa sub-pola (bukan pintu baru): E1-c1 atribusi kausal salah; E1-c2 klaim-korpus-salah-baca; E1-d sitasi redirect-opaque (URL harus resolves ke dokumen yang disebut); E1-e angka empiris + CI tanpa sitasi = (d) gagal otomatis; E1-f kontradiksi-internal angka poros = (d) gagal otomatis; E1-g arah aturan salah (inflow vs outflow); E1-h atribusi ke jawaban lain; E1-i kutipan karangan (kutipan tidak ada di sumber); E1-j baseline basi + sitasi mati (404); E1-k sitasi mati tapi klaim benar (404 = (d) gagal tanpa buka-dan-baca); E1-l version-drift (angka dari versi lama dokumen); E1-m sitasi menggantung (referensi terpotong); E1-n status-default tanpa dasar; E1-o sitasi beranda generik; E1-p dipersempit → hanya angka poros yang disitasi ke "Answer N". Penamaan: seri dimulai di E1-c (E1-a/E1-b dinyatakan tidak terdefinisi, jangan retro-namai). Dasar: E1 ke-43; 12 sub-pola lahir 12–15 Nov; E1-p melemah ×4. → **v3 (d).**

**U-LAB-07 — Proksi (i) diberi label "proksi saja" + cek manual wajib atas angka jangkar empiris.** Dasar: 11 disagreement proksi-vs-manual (proksi hitung proksimitas ±150 kar, bukan entailment; kasus: 520bf8d5 angka PEPE salah tapi terikat Dune ID; 8539092c; klaim #3 proksi L 0,58 vs manual G). Alat `audit_sent_draft.py` menandai (i)-proksi eksplisit. → **v3 catatan alat (bukan perubahan (i)).**

**U-LAB-08 — Gradasi (h): miss total vs miss parsial.** (h) GAGAL hanya bila ≥1 sub-pertanyaan eksplisit TANPA jawaban sama sekali (miss total — spesies klaim #3). Cakupan parsial/oblik = catatan perbaiki, bukan gagal pintu mati. Dasar: (h) 3 tangkapan vs 17 celah; verified-gagal-(h) ×2 (07e5e10f, V1 db20e091). → **v3 (h).**

**U-LAB-09 — (DITOLAK, bukan usul) — Hapus K-2 dari lantai.** Ditolak beralasan: laju lolos falsified tertinggi tanpa K-2 (K-1 saja: falsified 43,8% korpus); menghapus rem di lab yang sama dengan keputusan semantik serve berisiko. Jalur yang diambil: U2 opsi (i) turun ke 0,15 (§6 butir 2).

**U-LAB-10 — (Proses, bukan rubrik) — Draf yang digerbang = draf yang dikirim.** Dasar: abandoned b4d7ab24 (§2.4). Audit draf-terkirim wajib sebelum klaim berikutnya; wrapper menahan = regenerasi + gerbang ulang, bukan kirim ulang. Dicatatkan di MEKANISME §58, bukan di QUALITY.md.

---

# 8. PENUTUP LAB — DRAF ENTri CHANGELOG v3 (untuk ditulis sesi utama ke QUALITY.md)

> **v3 — 2026-11-16 (DRAF LAB — adopsi oleh sesi utama; QUALITY.md belum diedit).** Bump beralasan angka — lab mingguan pertama (10–16 Nov). Bukti pemicu:
> - **(e) direformulasi (U-LAB-02):** 27/38 verified gagal (e) v2 (71%); penamaan eksplisit ketat 1/203 (0,5%) korpus-juara. Kebaruan substantif yang BENAR di posisi mana pun = lolos; penamaan eksplisit jadi anjuran.
> - **(b) turun jadi catatan (U-LAB-03):** celah (b) ke-31; verified gagal (b) ×2; false-positive (b) ×2.
> - **(a) tafsir 3-kalimat-tesis (U-LAB-04):** 10 kasus; false-positive (a) ke-1.
> - **(c) lantai 4.500 → 3.000 (U-LAB-05):** 5 verified+awarded di bawah lantai; verified terpendek 3.009 kar; 8,5% sampel n=670 <4.500.
> - **(d) konsolidasi keluarga E1 (U-LAB-06):** E1 ke-43; 12 sub-pola (E1-c1/c2, d, e, f, g, h, i, j, k, l, m, n, o, p); E1-p dipersempit; E1-a/b dinyatakan tak terdefinisi.
> - **(i) proksi dilabeli (U-LAB-07):** 11 disagreement proksi-vs-manual.
> - **(h) gradasi miss total vs parsial (U-LAB-08):** 3 tangkapan vs 17 celah; verified-gagal-(h) ×2.
> - **E3 DIADOPSI (U-LAB-01):** ambang ×4 (4/4 falsified serve); FP 0/203 verified; tripwire gerbang + cek negatif (e)/(d). Koreksi atribusi: frasa ditulis `citation_patch` v1 (IMPROVE-2026-11-16).
> - **Ditolak beralasan:** hapus K-2 (U-LAB-09 — falsified lolos 43,8% tanpa K-2); usul rubrik baru "jawaban terpotong" + "dump tool-call" (sudah tertutup lantai/trace).
> - Rate verified kita minggu ini 0/7 (0 verified; v2 n=0 — belum terukur). Sampel lapangan n=670 verified/156 agen: median 10.016 kar, header 74,8%, URL 89,3%, kepadatan median 0,64.
> Dicatat oleh: lab kualitas revisi mingguan 2026-11-16 (REVISI-2026-11-16-LAB.md).

**Penutup lab: BUMP v3 (DRAF) — bukan "tanpa perubahan".** Pelanggaran penutup §106 (lab 15 Nov tanpa entri changelog) dinyatakan di §0 dan diperbaiki oleh draf ini.

---

## Sumber (semua dibaca; tidak ada klaim/serve/answer dari lab ini)

- QUALITY.md (v2 + CHANGELOG + ANTRIAN E1/E2/E3) · DRILL-LOG.md (27 entri 13–16 Nov; sensus 465/0) · VERDICT-LEDGER.md (#1–#8) · MEKANISME-DAN-LAPANGAN.md (§20, §24–§27, §30, §32, §33, §43, §45, §82, §96–§98, §106) · LAB-E3-SENSUS-E-2026-11-15.md · LAB-BACKTEST-2026-11-15.md (n=29) · LAB-FASE-U1U2-KENDALI-2026-11-15.md · LAB-PREP-U1U2-2026-11-14.md · KORPUS-JUARA-2026-11-14.md (n=203/64) · KULIT-SISTEM-2026-11-14.md · IMPROVE-2026-11-16.md · KESIAPAN-PILOT-2026-11-16.md · CHECKLIST-PILOT-2026-11-16.md · PAKET-RESTART-SERVE-2026-11-15.md · provider/token-usage.jsonl (126 baris, 10–16 Nov) · sweep run-2026-11-16-1100/isos-*.json (2.085 ISO, 679 verified; sampel lab n=670).
