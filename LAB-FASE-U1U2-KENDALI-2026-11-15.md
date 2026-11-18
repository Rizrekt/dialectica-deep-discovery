# LAB LINI C — SUB-CEK ARITMETIKA FASE + U1/U2 + AUDIT SISTEM-KENDALI

**Konteks:** lab Dialectica dimajukan dari Senin 2026-11-16 ke malam Minggu 2026-11-15 (±19:10 WIB). File ini = keluaran lini C. Ditulis dari FILE + keadaan live terverifikasi sesi kolom malam ini; lini ini tidak mengeksekusi apa pun (nol klaim/serve/ubah config/cron/dokumen kendali).

**Keadaan live yang dipakai (verifikasi sesi kolom, malam ini):** Expert `8522c990-d4f6-4155-a326-3c3c9802b950`, akun rizrekt, strategyType=dynamic, arenas=general; saldo **−1,8788 $TRUED**; RAR **118** (reliability −5 / availability 29 / reputation 94); Expertise **0**; lifetimeEarned **0**; falsified rezim **7** (3 klaim one-shot + 4 serve); **22** jawaban serve masih revealed; suspensionCount 5.

**Sumber:** VERDICT-LEDGER.md (8 baris), MEKANISME-DAN-LAPANGAN.md (§26 A5, §45, §46, §51, §97–§105), operator prompt (paket b.13, T10.4, T12, T13.3, T16-A/B), INVENTARIS-PANEN.md, SISTEM-KENDALI.md, STUDI-KOHORT-2026-11-14.md, LAB-PREP-U1U2-2026-11-14.md, KORPUS-JUARA-2026-11-14.md, BELAJAR-LOG.md (run 2/4/5/6), SHADOW-AWARD-TIMING-2026-11-15.md.

---

## 1. SUB-CEK ARITMETIKA FASE KLAIM

### 1.1 Hitung ulang dari ledger

| Klaim disiplin | ISR | Lane | Verdict | ΔSaldo | ΔLE | ΔExpertise |
|---|---|---|---|---|---|---|
| #1 (10 Nov 19:07) | 60fa9935 | Nemotron one-shot | FALSIFIED (2 supp / 2 ref, panel 4) | −1 (→4,1212) | −1 (7→6) | −1 (7→6) |
| #2 (10 Nov ±21:29) | 472b29a0 | Nemotron one-shot (uji gerbang pasca-JEDA) | FALSIFIED (0/4, panel 4) | −1 (→3,1212) | −1 (6→5) | −1 (6→5) |
| #3 (11 Nov 07:28) | 71f472d6 | Cloudflare/gpt-oss one-shot (uji JEDA #2) | FALSIFIED (0/1, panel 2) | −1 (→2,1212) | −1 (5→4) | −1 (5→4) |

- **Klaim one-shot: 3 tembakan, 0 verified, 3 falsified (0/3).** Baris ledger #4 (2c7efc3e, 12 Nov) = ABANDONED/DROPPED dengan **0 submitted** — bukan klaim disiplin ke-4; cacah klaim disiplin tetap **3** (konsisten §97: "3 klaim disiplin, semua settled — falsified").
- Baris #5–#8 = falsified SERVE (f0bb3586, 7d81c51d, 5b5e8212, a3b8b34a — semua jawaban serve Vyce pagi 14 Nov, spesies thinking-trace yang sama): masing-masing −1 saldo/−1 LE/−1 Expertise.
- **Rekonsiliasi saldo penuh:** 5,1212 (awal rezim caps-20) − 7 × 1 (tujuh falsified) = **−1,8788** ✓ cocok dengan bacaan live. LE 7 → 0 ✓. Expertise 7 → 0 ✓. Tidak ada gerakan saldo lain yang belum terjelaskan (NIU $0, bertanya tertutup — §25.2/INVENTARIS #8/#9).

### 1.2 Keadaan fase dalam angka (§97, bacaan terakhir yang menyatakan kill-metric lengkap)

- **Fase tangga: RAMP** — total klaim disiplin 3 < 10 (A5, MEKANISME §26: RAMP = klaim disiplin pertama s/d total 10 klaim, anggaran 4–10 kontes/hari; anggaran tidak dieksekusi karena kunci di bawah).
- **Kill-metric (i)** klaim disiplin tanpa settle: **0/10 — TIDAK terpicu** (ketiga klaim settled, semuanya falsified).
- **Kill-metric (ii)** 1 falsified → jeda + bedah: **JEDA AKTIF** — falsified sejak klaim terakhir terus bertambah dari jalur serve (terakhir #8, 15 Nov 06:43).
- **Kill-metric (iii)** RAR < −5: RAR **118 — tidak terpicu**.
- **Kill-metric (iv)** abandoned baru: **0 — tidak terpicu**.
- **STOP TOTAL formal klaim one-shot: BERLAKU** sejak 11 Nov ±07:28 (§51/§56; asal: janji day-close §46 — falsified klaim uji → sesi utama memanggil STOP operasi untuk evaluasi total; §51 memvonis LANJUT BERSYARAT dengan uji maks 2 klaim + stop otomatis; uji klaim 1 jalan lewat verifikasi sesi utama §54 lalu **DROPPED** 12 Nov → uji GAGAL per §7.3; sejak itu STOP TOTAL tertulis mengunci di semua catatan jendela §67–§105).
- **Benchmark RAMP (R8):** verdict rate berjalan **0/3 = 0%** lawan ambang pemenang kohort **≥55%**; viso median saat masuk klaim kita **10** (12/10/9) lawan patokan **±3** — di luar pita di kedua sumbu (§97 butir 3).

### 1.3 Aritmetika naik fase — syarat PENUH sudah gugur permanen untuk batch ini

Syarat naik RAMP → PENUH (A5, §26): **10 klaim pertama menghasilkan ≥3 verified DAN 0 abandoned DAN 0 falsified.**

- Klaim 1–3 sudah memuat **3 falsified**. Syarat "0 falsified pada 10 klaim pertama" **tidak bisa lagi dipenuhi oleh kombinasi hasil klaim 4–10 mana pun** — bahkan 7/7 verified berikutnya (total 7 verified, 3 falsified) tetap gagal di komponen 0-falsified.
- Konsekuensi aritmetika murni: di bawah definisi A5 yang berlaku, fase akun ini **terkunci di RAMP (atau di bawahnya) secara permanen untuk batch 10 pertama**. Satu-satunya jalan mengubah itu = merumuskan ulang definisi batch/fase — dan tangga volume adalah **wilayah terkunci T13.3** (hanya USULAN; keputusan sesi utama/user). Lab tidak bisa membukanya dari dalam.

### 1.4 Aritmetika saldo & runway

- Saldo **−1,8788** = runway **negatif**. Tidak ada "sisa tembakan yang terjangkau": setiap falsified tambahan = −1 lagi (→ −2,8788), dan perilaku LE/Expertise di bawah 0 **belum terpetakan** (keduanya sudah di 0; saldo terbukti bisa negatif per T16-B, LE/Exp belum teramati negatif — tidak dikarang di sini).
- Yang bisa menaikkan saldo hanya 3 sel berbayar (T11.5): **Pioneer +20, Innovator +10 (novelty ≥15%), Marathon Winner +10**. Verified biasa = **$0** — verified sebanyak apa pun di slot biasa tidak menggerakkan saldo.
- Untuk kembali ke ≥ 0 dari −1,8788 perlu bersih **+1,8788**, artinya minimal: **1× Pioneer (+20 → +18,1212)**, ATAU **2× slot +10** (1× +10 saja → −0,8788, masih negatif) — dengan **nol falsified di antaranya** (tiap falsified menaikkan kebutuhan +1).
- EV per klaim (model §51.5, era korpus §30): EV = v·s·P − (1−v), s≈0,5, P≈12,7 → **impas ≈15%** (rentang 9–19%). Pada rate teramati kita 0% → **−1,00/klaim**. Pada median kohort 32% → +1,16/klaim; pemenang 55% → +2,72/klaim. Kejujuran statistik §51.5 tetap berlaku: P(0/3 | v=0,15) ≈ 0,61 — n=3 **tidak membuktikan** rate sejati kita <15%; vonis kunci bersandar pada mekanisme (tiga spesies gagal berbeda + gerbang fase gugur + runway negatif), bukan pada n=3 saja.
- Syarat tinjau ambang dari data sendiri (§45): evaluasi K-1/K-2 "sesudah 5 klaim berikutnya" — klaim berikutnya sejak 11 Nov = **0**, jadi syarat itu **belum terpenuhi**; keputusan U2 (butir 3) bersandar pada data korpus eksternal, bukan verdict klaim kita.

### 1.5 Siapa yang bisa mencabut — verifikasi teks (klaim brief diuji lawan dokumen)

Brief lini ini menyebut "STOP TOTAL hanya bisa dicabut user tertulis". **Hasil verifikasi: frasa itu TIDAK ada verbatim di dokumen untuk STOP TOTAL klaim.** Teks yang benar-benar tertulis:

1. **T12 (KEADAAN):** "JEDA tetap berlaku sampai **sesi utama** memverifikasi implementasi gerbang ini (wrapper §45 + addendum ini) dan **mencabutnya tertulis**."
2. **T10.4:** "JEDA klaim sampai **sesi utama mencabutnya** sesudah bedah."
3. **INVENTARIS-PANEN (a) #1:** syarat buka klaim Kelas 1 = "**Sesi utama mencabut JEDA + STOP TOTAL tertulis** sesudah bedah (mekanisme T12); bahan kalibrasi (U2, (e), sub-cek aritmetika) diputuskan lab 16 Nov." Pemilik keputusan tertulis di sana: **Sesi utama (pencabutan); lab (bahan kalibrasi)**.
4. Satu-satunya teks "sampai user memutuskan" = **kill-metric (a) paket b.13**: "10 klaim disiplin tanpa settle → STOP TOTAL serve sampai user memutuskan" — itu metrik (a), hitungannya **0/10 = tidak terpicu**, dan objeknya serve, bukan STOP TOTAL klaim formal yang sedang berlaku.
5. **T13.3 / klausul C12:** status STOP TOTAL klaim + tembakan uji = **wilayah terkunci** — run/cron/lab hanya boleh melaporkannya sebagai USULAN; eksekusi perubahan menunggu keputusan sesi utama/user.
6. Catatan sejarah yang relevan: §52 mencatat keputusan user atas vonis evaluasi §51 (lanjut-bersyarat vs tutup-total) **belum diberikan** per 11 Nov 09:00; uji sesudahnya berjalan lewat verifikasi + penjadwalan sesi utama (§54). Tidak ada di file yang dibaca lini ini pencabutan STOP TOTAL oleh siapa pun sesudah itu — semua §67–§105 menulisnya tetap berlaku.

**Rumusan akurat untuk lab:** pencabutan JEDA + STOP TOTAL = **keputusan sesi utama, tertulis, sesudah bedah**, dengan bahan kalibrasi diputuskan lab; bukan wewenang run/lab sendiri (wilayah terkunci), dan bukan pula tertulis sebagai "hanya user" untuk kunci yang sedang berlaku ini.

### 1.6 VONIS SUB-CEK

**TERKUNCI-MATEMATIS** — untuk rezim fase/volume: (a) syarat naik fase A5 gugur permanen di batch ini (3 falsified dalam 10 klaim pertama); (b) runway negatif (−1,8788) dengan EV teramati −1,00/klaim; (c) syarat tinjau ambang dari data sendiri (5 klaim berikutnya) belum terpenuhi dan tidak bisa terpenuhi tanpa membuka kunci.

**Satu-satunya pintu non-aritmetika (BISA-BUKA-BERSYARAT, bukan hak lab):** satu tembakan uji tunggal hanya sah bila SEMUA syarat angka/keputusan ini terpenuhi bersamaan —
1. pencabutan JEDA + STOP TOTAL **tertulis oleh sesi utama** sesudah bedah (T12), sesudah bahan kalibrasi lab (U2 + sub-cek ini) diputuskan;
2. target = satu-satunya kelas yang bisa mengangkat saldo dari negatif dalam satu tembakan: **Kelas 2 Pioneer viso-0 topik inti (+20)**, atau Kelas 1 Marathon dengan edge award-timing terbukti (shadow M1 97,9%, lihat butir 4.2 #6) — target selain itu tidak mengubah aritmetika saldo walau verified;
3. risiko dinyatakan telanjang sebelumnya: 1 falsified lagi = saldo **−2,8788**, LE/Exp menabrak wilayah belum terpetakan di bawah 0;
4. gerbang penuh T12 (lantai + self-VFP + sensus) lolos tercatat per klaim — dengan catatan jujur bahwa klaim #3 lolos semua gerbang itu dan tetap falsified (lantai perlu, bukan cukup).

---

## 2. U1 — JENDELA MALAM (VONIS: PARSIAL)

### 2.1 Usul + basis angkanya (STUDI-KOHORT-2026-11-14 F2 + LAB-PREP-U1U2-2026-11-14)

- Basis = era segar studi (603 rilis / 3,49 hari): jam **22:00 WIB = 152/603 (25,2%)**; blok **21:00–22:59 = 35,5%**; blok gelombang malam inti **21:00–01:59 = 45,1%**; blok tanpa serve 23:00–06:59 = 14,4% (±87 pertanyaan lolos tanpa peluang Pioneer).
- Opsi terkuat LAB-PREP = **O3+O1**: pindah label "jendela utama kedua" R4 dari 11:00–13:00 (pangsa era segar 8,6–11,4%) ke **21:00–23:00**, DAN perpanjang hidup serve dari stop-23:00 ke **stop-01:00** → cakupan serve atas pasokan **±85,6% → ±92,7%** (+7,1pp dari jam 23:00+00:00). Manfaat yang diklaim LAB-PREP untuk hari ini (di bawah STOP TOTAL): tangkapan Pioneer oleh serve + kesiapan staging — bukan klaim.

### 2.2 Lawan data segar 15 Nov

| Data | Angka | Bacaan lawan U1 |
|---|---|---|
| Run belajar 4 (malam 14→15 Nov, 278 rilis segar) | Jam: 19:00=54, 21:00=53, 20:00=52, 23:00=45, **22:00=43 (15,5%)** | Gelombang malam **lebar 19:00–23:00**, bukan punuk tunggal 22:00. Vonis run 4 (X7): "punuk 22:00 sebagai jam dominan" = **MATI / tidak tereplikasi**. |
| Run belajar 5 (02:37–10:37) | Gelombang **pagi 05:00–06:59 = 97/117 (82,9%)** pasokan jendela; laju 14,7/jam | Di hari banjir melambat, punuk bergeser ke **pagi buta** — distribusi jam tidak stabil antar-hari; 22:00 di luar rentang tarikan (tidak teruji, bukan terbantah). |
| Run belajar 6 (10:37–18:37) | Banjir Viking **berakhir** (0/53); 53 rilis: 11:00=20, 15:00=15; laju **6,8/jam** | Pasokan siang beragam kembali; malam 15 Nov belum tertarik sama sekali. |
| Tangkapan gelombang 21:00, 14 Nov (§90 via tabel 7 hari I11) | **98 rilis, 0 topik inti** | Gelombang malam terbesar yang tertangkap penuh berisi nol pasokan yang bisa kita klaim. |
| Tabel 7 hari jam × topik-inti (I11 + J11 + K10) | Pasokan inti ≈ **0 di SEMUA jam** terukur 2 hari (median harian inti = 0; viso-0 inti sejati = 0 di run 5 dan run 6) | Ambang naik status KULIT (≥1,5× median harian inti di ≥3 hari terpisah) **tidak dipenuhi jam mana pun** — termasuk 21:00–23:00. |

**Titik kritis pengukuran:** angka cakupan 85,6% → 92,7% dihitung atas **pasokan total** era banjir (didominasi Viking/Mars). Untuk tujuan kita, cakupan yang relevan adalah **pasokan topik inti** — dan itu ≈ 0 di semua jam yang terukur, siang maupun malam. U1 benar secara aritmetika pasokan-total, tetapi belum mengukur peluang yang benar-benar bisa dipanen akun ini.

**Titik kritis kedua:** komponen serve U1 (O1, perpanjangan s/d 01:00) saat ini **moot** — serve OFF total (hold T16-A/T16-B) sampai lab memutuskan gerbang serve + sesi utama menyalakan tertulis. U1 tidak bisa dieksekusi mendahului keputusan serve itu; yang bisa dinilai sekarang hanya komponen staging/label (O2/O3).

### 2.3 Data yang kurang (kenapa PARSIAL)

1. **Tangkapan gelombang 21:00 malam ini (15 Nov) belum ada** — hunt 21:00 belum jalan saat lab mulai 19:10. Ini tangkapan pertama gelombang malam **sesudah banjir Viking berakhir** — justru sampel yang paling menentukan.
2. **Replikasi malam non-banjir:** belum ada satu pun malam tanpa Viking yang tertarik penuh (run 4/5 keduanya malam banjir).
3. **Distribusi jam pasokan topik inti > 0:** belum pernah ada hari dengan pasokan inti terukur > 0 sebagai pembanding; tabel 7 hari baru berumur 2 hari dari 7.
4. **Latensi Pioneer per jam malam non-banjir** (data kurang K3 run 6): snipe detik terbukti hidup lagi di siang (median 2,9 dtk); apakah hidup juga di malam tanpa banjir — belum terukur.

### 2.4 VONIS SEMENTARA U1

**TUNDA (parsial).** Bukan TOLAK — basis era segar 14 Nov nyata (45,1% pasokan di 21:00–01:59 era itu; §77 independen membaca 379 pertanyaan semalam). Bukan LAYAK-UJI penuh sekarang — tiga dari empat data penentu belum ada dan komponen serve-nya terkunci di belakang keputusan gerbang serve.

- **LAYAK-UJI (sebagai pengumpulan data, bukan perubahan rezim):** komponen staging O2/O3 — perlakukan run 21:00 + tangkapan gelombangnya sebagai sumber data prioritas dan akumulasi tabel 7 hari sampai ≥3 hari terpisah, termasuk malam non-banjir.
- **Syarat uji ulang di lab berikutnya:** tangkapan 21:00 malam ini terbaca + ≥1 malam non-banjir tertarik + cakupan dihitung ulang **terpisah untuk pasokan inti** (bukan hanya total). Bila pasokan inti tetap 0 di 21:00–23:00 pada sampel itu, U1 gugur oleh datanya sendiri; bila inti muncul pekat di malam, U1 naik dengan angka inti, bukan angka banjir.

---

## 3. U2 — AMBANG K-2 (DRAF KEPUTUSAN LAB)

### 3.1 Deret data (semua dari file; metode wrapper §45 yang sama)

**Korpus acuan (KORPUS-JUARA-2026-11-14, n = 203 verified / 64 falsified, 12 agen juara):**

| Gerbang | Verified lolos | Falsified lolos | Gap |
|---|---|---|---|
| K-1 saja | 72,4% | 43,8% | **+28,7pp** |
| Lantai penuh @0,30 | 32,5% | 28,1% | +4,4pp |
| Lantai penuh @0,15 | 57,6% | 32,8% | **+24,8pp** |
| Di dalam K-1: @0,30 | 44,9% | 64,3% | **−19,4pp (terbalik)** |
| Di dalam K-1: @0,15 | 79,6% | 75,0% | +4,6pp |

**Refresh korpus (BELAJAR-LOG, frame fresh+monitored):**

| Frame | @0,30 V / F (gap) | @0,15 V / F (gap) | In-K1 @0,15 | K-1 saja (gap) |
|---|---|---|---|---|
| Run 2 (n 210/184) | lantai penuh +5,6pp | +16,0pp | −0,6pp | +20,8pp |
| Run 4 (n 241/195) | 28,6% / 23,6% (**+5,0pp**) | 56,8% / 35,9% (+20,9pp) | −5,6pp | +37,4pp |
| Run 5 (n 323/240) | 29,4% / 20,8% (**+8,6pp**) | 60,4% / 38,8% (+21,6pp) | +0,8pp | +27,1pp |
| Run 6 (n 555/495) | 31,7% / 19,0% (**+12,7pp**) | 57,8% / 31,5% (+26,3pp) | +4,6pp | **+30,2pp** |

- **Deret gap penuh @0,30: +4,4 → +5,0 → +8,6 → +12,7pp** — naik monoton; run 6 = **selisih MATERIAL pertama** lawan acuan (+12,7 vs +4,4 = **+8,3pp**, ambang material ≥5pp). Pendorongnya (K6): falsified makin jarang lolos (19,0% vs acuan 28,1%) sementara verified **datar** (31,7% vs 32,5%) — lantai @0,30 makin memfilter falsified di frame siang, bukan makin meloloskan verified.
- **Deret gap penuh @0,15:** +24,8 (korpus) → +20,9 → +21,6 → +26,3pp — besar dan stabil; selisih run 6 lawan acuan hanya **+1,5pp (tidak material)**.
- **Deret in-K1 @0,15 (lengkap, semua frame):** +4,2 (LAB-PREP) → −0,6 (run 2) → +4,6 (korpus) → −5,6 (run 4) → +0,8 (run 5) → +4,6 (run 6). Berayun di kedua sisi nol; rata-rata ≈ +1,4pp. **Kesimpulan yang didukung deret penuh: K-2 tidak terbukti menambah diskriminasi di atas K-1 pada ambang mana pun** — nilai @0,15 ≈ nol, nilai @0,30 konsisten negatif (in-K1 @0,30: −19,4 korpus; −13,4 run 4; −3,5 run 5; −1,7 run 6 — tidak pernah positif).
- **K-1 saja = diskriminator terkuat di setiap frame** (+28,7 korpus; +30,2 run 6; gap URL≥1 run 6 = 38,4pp).

### 3.2 Catatan penyeimbang: K-2 lawan falsified KITA sendiri

Rasio angka terikat ketiga klaim falsified kita: #1 = **0,647**, #2 = **0,318**, #3 = **0,60** (T12/§51.1). Ketiganya **lolos K-2 di @0,30 maupun @0,15** — K-2 tidak menangkap satu pun falsified kita di ambang mana pun; yang menangkap #2 adalah K-1 (0 URL + kepadatan 0,456 < 0,5), dan #1/#3 hanya tertangkap gerbang semantik/cakupan. Argumen sisa K-2 = fungsi desain §45 sebagai rem spesies draf (draf rasio-rendah ala spesies B), bukan diskriminator terukur. Ini menimbang ke opsi (ii) — dan ditimbang balik di 3.4.

### 3.3 Tiga opsi

**Opsi (i) — K-2 turun 0,30 → 0,15.**
- Konsekuensi terukur (korpus): laju lolos verified **32,5% → 57,6% (+25,1pp)**; falsified **28,1% → 32,8% (+4,7pp)**; gap **+4,4 → +24,8pp**. Frame run 6: verified 31,7% → 57,8%; falsified 19,0% → 31,5%; gap +12,7 → +26,3pp.
- Risiko: in-K1 tetap ≈ nol → K-2@0,15 hampir dekoratif di atas K-1 (pemisahan diwarisi K-1); keputusan bersandar data eksternal saja (syarat tinjau §45 dari 5 klaim kita belum terpenuhi); menurunkan K-2 ikut mengubah **gerbang serve** (serve_gate memakai wrapper verbatim dengan K-2 0,30 — klausul C6/C13) tepat saat lab juga memutuskan tahap semantik serve (C5) — dua perubahan gerbang dalam satu lab harus dicatat sebagai satu paket, bukan dua kebetulan.

**Opsi (ii) — K-2 dihapus, K-1 saja.**
- Konsekuensi terukur: gap terbesar di korpus (**+28,7pp**) dan run 6 (**+30,2pp**); laju lolos = laju K-1: korpus verified 72,4% / falsified **43,8%**; run 6 falsified lolos 41,2%.
- Risiko: laju lolos falsified **tertinggi dari tiga opsi** (43,8% korpus) — gerbang jadi paling longgar persis di sisi yang membunuh kita; menghapus komponen lantai = perubahan wilayah terkunci yang lebih dalam daripada menggeser angka; fungsi rem-spesies §45 hilang formal (walau data 3.2 menunjukkan rem itu tidak pernah menangkap falsified kita, ia tetap satu-satunya rem rasio untuk draf masa depan); bertabrakan dengan desain gerbang serve yang baru dibangun di atas wrapper verbatim (C6) — serve akan hidup (bila dibuka) tanpa komponen yang jadi bagian dari alasan gerbang itu lolos uji 142/142.

**Opsi (iii) — Tetap 0,30.**
- Konsekuensi terukur: false-rejection verified tertinggi — **67,5% verified korpus tertahan** (run 6: 68,3%); arketipe pemenang mayoritas tertahan (chirpy lolos 25,0–33,3%; megumii 0,0% — K9/J10); in-K1 @0,30 **negatif di semua frame** → di dalam subset yang lolos K-1, K-2@0,30 secara aktif memilih falsified lebih sering daripada verified.
- Risiko: bila serve dibuka di bawah gerbang ini, ±2/3 draf setara-verified tertahan → volume serve tercekik dan cap serve tidak pernah terpakai produktif; argumen "tunggu" memang menguat sebagian dari run 6 (gap @0,30 naik ke +12,7pp), tetapi kenaikannya digerakkan falsified yang menyusut di frame siang — bukan bukti @0,30 memisahkan lebih baik di dalam K-1 (tetap −1,7pp).

### 3.4 DRAF REKOMENDASI LAB (keputusan final tetap user/sesi utama)

**Opsi (i): turunkan K-2 dari 0,30 ke 0,15.** Alasan berangka:
1. Gap penuh @0,15 besar dan **stabil di dua frame independen** (+24,8pp korpus n=267; +26,3pp run 6 n=1.050) — bukan artefak satu frame.
2. False-rejection verified turun **25,1pp** (korpus) — perbaikan terbesar yang tersedia untuk jalur serve/klaim tanpa menyentuh K-1.
3. Berbeda dengan @0,30, @0,15 **tidak pernah terbalik di dalam K-1 secara material** (deretnya berayun di sekitar nol, bukan negatif konsisten) — ia berhenti merusak diskriminasi K-1.
4. K-2 dipertahankan sebagai rem spesies di atas kertas (desain §45) — menghapusnya (opsi ii) menaikkan laju lolos falsified ke 43,8% dan mengubah dua hal sekaligus di lab yang sama dengan keputusan semantik serve (C5); prinsip satu perubahan terukur menolak itu.
5. Dicatat jujur di draf ini: yang dibeli opsi (i) adalah **kelonggaran false-rejection**, bukan diskriminasi tambahan — K-1 tetap satu-satunya diskriminator terukur (+28,7/+30,2pp), dan gerbang penentu tetap semantik (self-VFP T10.2/T12.5).

---

## 4. AUDIT SISTEM-KENDALI vs KEADAAN LIVE MALAM INI

### 4.1 Verifikasi hitungan dokumen (grep per baris klausul, malam ini)

| Hitungan dokumen | Klaim dokumen | Hasil grep | Vonis |
|---|---|---|---|
| Total klausul | 65 | 65 baris klausul (A15+B7+C16+D7+E5+F13+G2) | ✓ cocok |
| TERKAIT | 51 | 51 baris berstatus `TERKAIT` murni | ✓ cocok |
| TERKAIT-BELUM-TERBUKTI | 13 | 13 baris | ✓ cocok |
| CELAH | 1 (C5) | 1 baris berstatus `CELAH` | ✓ cocok |

**Hitungan SISTEM-KENDALI.md TERVERIFIKASI: 65 / 51 / 13 / 1.**

Catatan basi (bukan kesalahan hitung): bagian "CATATAN KEADAAN" di SISTEM-KENDALI.md masih menulis saldo −0,8788 / RAR 109 (keadaan saat audit dokumen ditulis, 15 Nov pagi) — keadaan live kini −1,8788 / RAR 118. Hal yang sama di INVENTARIS-PANEN.md: jangkar runway masih "1,1212 (bacaan §95, 02:56 WIB)" dan risiko dihitung lawan runway itu ("1 gagal lagi → sisa 0,1212") — **sudah tertimpa live**: tiga falsified serve berikutnya sudah terjadi (ledger #6–#8) dan saldo kini negatif. Angka-angka tertahan di bawah memakai keadaan live, bukan jangkar basi itu.

### 4.2 Tujuh sumber TERTAHAN (INVENTARIS-PANEN (a)) — syarat buka + efek lab malam ini

| # | Sumber | Syarat buka tertulis | Lab malam ini mengubah status? |
|---|---|---|---|
| 1 | Klaim one-shot Kelas 1 Marathon | Sesi utama mencabut JEDA + STOP TOTAL **tertulis** sesudah bedah; bahan kalibrasi diputuskan lab | **TIDAK.** Lab memasok bahan kalibrasi (butir 1+3 file ini); pencabutan tertulis belum ada. Sub-cek 1.6: fase TERKUNCI-MATEMATIS; pintu bersyarat menuntut pencabutan itu + target Pioneer/award. |
| 2 | Klaim one-shot Kelas 2 Pioneer viso-0 | Pencabutan tertulis yang sama dengan #1 **DAN** target viso-0 topik inti muncul di scan | **TIDAK.** Dua syarat belum terpenuhi: pencabutan belum ada; viso-0 inti sejati = **0** di run belajar 5 dan 6 (J11/K10). |
| 3 | Serve Vyce | Lab memutuskan **gerbang serve** (eligibility `endsAt` + gerbang mutu pra-kirim + pemisah skor verdict/award) **DAN** sesi utama menyalakan ulang tertulis | **TIDAK (dari dokumen).** Gerbang teknisnya sudah jadi (serve_gate.py, 142/142 — GERBANG-SERVE-2026-11-15.md); keputusan lab atas tahap semantik (C5) + penyalaan tertulis belum tertulis di file mana pun yang bisa dibaca lini ini. Status tetap TERTAHAN + hold T16-A/T16-B. |
| 4 | Serve §39 Cloudflare | (i) Pasang ulang unit systemd dari salinan provider (kesiapan — dalam mandat T14), (ii) keputusan gerbang serve yang sama dengan #3, (iii) relevan penuh bila Vyce mati | **TIDAK.** Syarat (ii) sama dengan #3 — belum diputuskan tertulis; (i) kesiapan tidak mengubah status sumber. |
| 5 | Innovator | Salah satu jalur jawab buka (#1 atau #3) + target ramai dengan sudut novelty ≥15% terbukti grep | **TIDAK.** Menempel jalur induk; kedua induknya tertahan. |
| 6 | Edge award-timing (eksekusi) | Jalur jawab buka; shadow-test 20 ronde boleh mendahului sebagai analisis | **TIDAK untuk eksekusi.** Catatan koreksi atas inventaris: teks inventaris menyebut shadow-test "belum pernah dijalankan sebagai program bernama" — **sudah tertimpa**: SHADOW-AWARD-TIMING-2026-11-15.md mencatat shadow-test **selesai** (624 peristiwa awarded dari 264 ISR; model M1 survival-jendela-500-dtk akurat **97,9%**, 1.636/1.671). Yang tertahan tinggal eksekusinya, menempel #1/#3. |
| 7 | Forecast Arena | Keputusan mengubah config arenas + menerima horizon escrow (wilayah terkunci T13) | **TIDAK.** Config live tetap arenas=general (bacaan malam ini); tidak ada keputusan config. |

**Ringkasan 4.2: nol dari tujuh sumber tertahan berubah status oleh lab malam ini.** Yang berubah = kelengkapan bahan keputusannya: sub-cek fase (butir 1), draf U2 (butir 3), dan vonis parsial U1 (butir 2) kini tertulis; status baru lahir hanya dari keputusan tertulis sesi utama/user sesudah lab, bukan dari lab itu sendiri.

### 4.3 Klausul CELAH + TERKAIT-BELUM-TERBUKTI (SISTEM-KENDALI.md)

**CELAH (1):**

| ID | Isi | Syarat buka tertulis | Lab malam ini mengubah? |
|---|---|---|---|
| C5 | Self-VFP semantik jalur serve belum terpasang di serve_gate.py (titik pasang `semantic_check` disiapkan) | Lab memutuskan bentuknya (weekly-revision butir 11(4) — gerbang serve); P4 DAFTAR PERBAIKAN: implementasi hanya sesudah keputusan itu; serve tetap OFF sampai saat itu | **BELUM.** Keputusan bentuk semantik adalah item lab malam ini (lini gerbang serve), tetapi sampai keputusan + implementasinya tertulis, status dokumen tetap CELAH. Lini C tidak bisa menutupnya dari file. |

**TERKAIT-BELUM-TERBUKTI (13) — syarat bukti + efek lab:**

| ID | Klausul | Bukti/syarat yang ditunggu dokumen | Lab malam ini mengubah? |
|---|---|---|---|
| A9 | Lab kualitas mingguan + anti-stagnasi | Run weekly pertama di bawah badan revisi 2026-11-14 ("bukti pertama = lab Senin 2026-11-16") | **Belum di dokumen.** Lab yang dimajukan malam ini ADALAH run itu — bukti sedang diproduksi; status resmi berubah hanya bila lab menutup dengan bump QUALITY.md beralasan angka atau pernyataan "tanpa perubahan" + alasan, tertulis di entri revisi. |
| A11 | Langkah COCOK VERDICT (D/L §43) | Artefak run yang membuktikan pencocokan per verdict; bukti pertama = lab ini | **Belum di dokumen** — alasan sama dengan A9; lini C tidak menjalankan langkah itu. |
| A15 | Tabel 7 hari jam × topik-inti | Bukti artefak eksplisit di entri BELAJAR-LOG | **Siap naik — bukti kini ADA:** run 5 (J11) dan run 6 (K10) memuat tabel eksplisit (menutup kekurangan P7). Status tertulis di dokumen masih BELUM-TERBUKTI; penaikan status = wewenang audit weekly/sesi utama, bukan lini ini. |
| B2 | Rujukan INVENTARIS-PANEN di badan cron | Tambalan badan hunt/day-close (P5) dieksekusi sesi utama | **TIDAK.** P5 belum dieksekusi (dokumen kendali sendiri mencatatnya sebagai daftar perbaikan). |
| B7 | Progres terus | Bukti pertama = lab ini (pola mati → pengganti di hari yang sama) | **Belum di dokumen** — bukti bergantung hasil lab malam ini secara keseluruhan, belum tertulis saat lini ini selesai. |
| C4 | Self-VFP jalur klaim | Artefak klaim one-shot pasca-T12 | **TIDAK.** Nol klaim sejak T12 terbit (STOP TOTAL/JEDA) — dorman oleh rezim, bukan oleh lab. |
| C7 | Sensus angka per klaim | Catatan sensus per klaim | **TIDAK.** Dorman, alasan sama dengan C4. |
| C8 | Penamaan kebaruan opsional (tambalan 2026-11-15) | Bukti run pertama weekly = lab ini | **Belum di dokumen** — tambalan teksnya sudah masuk; bukti run-nya menunggu entri lab tertulis. |
| C9 | Clean sheet sebagai pagar steering | Bedah verdict diukur lawan aturan pada klaim baru | **TIDAK.** Dorman selama tidak ada klaim baru. |
| D4 | Revisi mingguan badan baru | Run weekly pertama berbadan baru = lab ini | **Belum di dokumen** — lab malam ini adalah run-nya; status menunggu entri revisi tertulis. |
| E3 | Kesesuaian penuh aturan kolom (delivery dua lapis) | Keputusan sesi utama atas ambiguitas delivery (P6) | **TIDAK.** P6 belum diputuskan di dokumen. |
| F10 | Jendela ukur push innovation_focus | Run weekly yang membuktikan pengelolaan jendela ukur | **TIDAK** dari lini ini — tidak ada artefak pengelolaan jendela ukur di file yang dibaca; strategi live tetap dynamic. |
| G2 | Rujukan SISTEM-KENDALI di kelima badan + audit weekly butir 12 | Audit klausul per klausul pertama = lab ini | **Belum di dokumen.** Audit lini C ini (butir 4 file ini) adalah bukti parsial pemeriksaan lawan dokumen kendali, tetapi audit resmi per klausul + pembaruan status adalah keluaran weekly-revision — belum tertulis saat lini ini selesai. |

**Ringkasan 4.3:** CELAH tetap **1 (C5)**. Dari 13 BELUM-TERBUKTI: **1 siap naik berbasis bukti artefak (A15)**; **5 menunggu bukti yang sedang diproduksi lab malam ini** (A9, A11, B7, C8, D4 — plus G2 sebagai auditnya); **4 dorman oleh rezim STOP TOTAL/JEDA** (C4, C7, C9 — dan F10 tanpa artefak); **2 menunggu tambalan/keputusan sesi utama** (B2/P5, E3/P6). Tidak satu pun berubah status *di dalam dokumen* oleh lini ini — dokumen kendali memang tidak boleh diubah dari tugas audit (aturan tugas lini C + cara pakai SISTEM-KENDALI butir 4).

---

## 5. RINGKASAN VONIS LINI C

1. **Sub-cek fase: TERKUNCI-MATEMATIS.** Klaim 0/3 verified; syarat naik fase A5 (0 falsified di 10 klaim pertama) gugur permanen; saldo −1,8788 (runway negatif, EV teramati −1,00/klaim, impas ±15%); kembali ke ≥0 butuh ≥1 Pioneer atau ≥2 slot +10 tanpa falsified di antaranya. Verifikasi teks: pencabutan JEDA + STOP TOTAL = **sesi utama tertulis sesudah bedah** (T10.4/T12/INVENTARIS) dengan bahan kalibrasi dari lab — frasa "hanya user tertulis" tidak ada verbatim untuk kunci ini; kill-metric (a) "sampai user memutuskan" tidak terpicu (0/10). Pintu bersyarat satu tembakan uji ada, syaratnya tertulis di 1.6 — bukan wewenang lab.
2. **U1: TUNDA (PARSIAL).** Basis malam era banjir nyata (45,1% di 21:00–01:59), tetapi punuk 22:00 tidak tereplikasi (run 4: malam lebar 19:00–23:00, 22:00 hanya 15,5%), gelombang bergeser ke pagi di run 5 (82,9% di 05:00–06:59), dan pasokan **inti** ≈ 0 di semua jam (tabel 7 hari) sehingga cakupan 85,6% → 92,7% mengukur banjir, bukan peluang kita. Kurang: tangkapan 21:00 malam ini + ≥1 malam non-banjir + cakupan versi pasokan-inti. Komponen staging LAYAK-UJI sebagai pengumpulan data; komponen serve terkunci di belakang keputusan gerbang serve.
3. **U2: draf rekomendasi = opsi (i), K-2 0,30 → 0,15.** Gap @0,15 stabil +24,8/+26,3pp di dua frame; false-rejection verified turun 25,1pp; @0,30 terbalik di dalam K-1 di semua frame; K-1 saja tetap terkuat (+28,7/+30,2pp) dan K-2 tidak terbukti menambah diskriminasi di atasnya pada ambang mana pun (in-K1 @0,15 berayun ≈ nol) — yang dibeli opsi (i) adalah kelonggaran, bukan diskriminasi. Opsi (ii) ditolak di draf ini: laju lolos falsified tertinggi (43,8%) + menghapus rem di lab yang sama dengan keputusan semantik serve. Keputusan final: user/sesi utama.
4. **Audit kendali: hitungan dokumen TERVERIFIKASI 65/51/13/1.** Nol dari 7 sumber tertahan berubah status malam ini; CELAH tetap C5; A15 siap naik (bukti tabel 7 hari kini ada di J11/K10); 5 klausul menunggu bukti lab malam ini sendiri; koreksi basi tercatat: jangkar runway INVENTARIS (1,1212) dan status shadow-test di inventaris sudah tertimpa live/file baru.
