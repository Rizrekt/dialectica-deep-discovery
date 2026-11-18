# KORPUS JUARA — Dialectica (2026-11-14)

**Satu baris: korpus 12 agen menghasilkan 203 jawaban VERIFIED dan 64 FALSIFIED yang terbaca penuh; lantai penuh kita hanya meloloskan 32,5% verified pada K-2 0,30 versus 57,6% pada 0,15 — hipotesis chirpy TERUJI SEBAGIAN: chirpy memang long-form ekstrem dan phenotype long-form/rasio-rendah juga hidup pada Febriyan, SyntaxZ, dan can-earn?, tetapi penolakan lantai @0,30 adalah fenomena kohort juara secara luas, bukan pengecualian chirpy.**

Status: **READ-ONLY total** — tidak ada klaim, serve, answer, perubahan config, ambang, atau aturan yang dilakukan oleh korpus ini. Semua angka adalah bahan keputusan lab Senin 2026-11-16.

## 1. Frame, seleksi agen, dan metode

- **Sumber yang dipakai ulang:** artefak belajar 2026-11-14 tarikan 02:40 (`belajar-2026-11-14/`) dan run ke-2 10:37 (`belajar-2026-11-14/run2-1037/`), dengan fungsi metrik yang sama persis: `openrouter_wrapper.mechanical_floor` dari wrapper §45.
- **Pertanyaan unik:** 212 (108 hanya/baca-terakhir dari frame 02:40; 104 dari frame 10:37). Bila pertanyaan yang sama muncul di dua tarikan, daftar ISO dan detail dari run 10:37 menggantikan snapshot 02:40 karena status verdict dapat berubah. Detail marathon tersedia untuk 212/212 pertanyaan.
- **Panel agen (12):** wajib dari celah run ke-2 = chirpy dan Rodeo (pendaki +1.477/+50 dan +1.007/+38 dalam ±8 jam) + Febriyan (earner eksternal #1). Jangkar aktif lain dipilih dari papan run ke-2/studi F5 dan syarat minimal 10 verified terbaca di frame gabungan: Mauldrop, Adam Reinhard, megumii, SyntaxZ, GaBot, HIMANSHU, Gufran The Legend, can-earn?, dan Discord 1.
- **Korpus terukur:** **203 verified** dan **64 falsified** milik panel yang sama, semuanya mempunyai teks reveal terbaca. Jawaban panel berstatus revealed/intent/abandoned tidak masuk korpus verdict ini.
- **Definisi metrik (persis studi §30/§45):** sitasi = URL + rujukan bernama yang dikenali wrapper (EIP-/ERC-/BIP-/CAIP-/RFC/arXiv/DOI/ISO/NIST); kepadatan = jumlah span sitasi per 1.000 karakter; rasio angka terikat = proporsi token angka yang berada dalam ±150 karakter dari sitasi, dengan digit di dalam sitasi dikeluarkan.
- **Gerbang kita:** K-1 = URL ≥1 **dan** kepadatan ≥0,5/1.000 kar. Lantai penuh @0,30 = K-1 + rasio ≥0,30. Lantai penuh @0,15 = K-1 + rasio ≥0,15. Ini skor mekanik saja; entailment semantik T12.5 tidak dinilai per jawaban di korpus ini.
- **Slot:** Pioneer = verified pertama berdasarkan stempel ISO pada daftar terbaru pertanyaan itu. Marathon Winner = ISO ada di `marathonEligibleIsos` detail dan `awarded=true`. Innovator tidak mempunyai penanda publik per jawaban; label 'tidak terbaca' di bawah berarti bukan Pioneer/Marathon yang terbaca, **bukan** bukti bukan Innovator.
- **Batas frame yang penting:** ini adalah *semua jawaban panel yang bisa ditarik dari 212 pertanyaan sampel dua tarikan belajar*, bukan sensus seumur hidup per agen. API publik yang tersedia tidak menyediakan indeks jawaban per-penulis; leaderboard chirpy misalnya mencatat 78 marathon wins pada 10:37, sedangkan hanya 6 dari 18 verified chirpy di frame ini yang terbaca sebagai Marathon Winner. Karena itu korpus ini menutup celah n=3 menjadi n=18 untuk chirpy dan n=203 gabungan, tetapi tidak boleh disebut korpus lifetime lengkap chirpy.

## 2. Agregat korpus dan angka keputusan U2

| Kelompok | n | Karakter median (q1–q3) | URL median | Kepadatan median (q1–q3) | Rasio median (q1–q3) | K-1 lolos | Lantai penuh @0,30 | Lantai penuh @0,15 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Verified juara | 203 | 9.549 (6.772–12.683) | 6,0 | 0,842 (0,476–1,439) | 0,212 (0,108–0,394) | 72,4% | 32,5% | 57,6% |
| Falsified agen sama | 64 | 9.626 (5.553–13.235) | 5,0 | 0,454 (0,264–0,970) | 0,119 (0,049–0,327) | 43,8% | 28,1% | 32,8% |

Kontras verified−falsified (Cliff's d; positif = verified lebih besar): karakter **0,048**, URL **0,223**, kepadatan **0,377**, rasio **0,268**, token angka **-0,006**, angka terikat **0,182**. Di panel juara ini kepadatan adalah pemisah mekanik terkuat; panjang hampir tidak memisahkan (d=0,048).

### 2.1 Pemisahan gerbang

| Gerbang | Verified lolos | Falsified lolos | Pemisahan | Verified tertahan | Falsified tertahan |
|---|---:|---:|---:|---:|---:|
| K-1 saja | 147/203 (72,4%) | 28/64 (43,8%) | **+28,7 pp** | 56 | 36 |
| K-2 saja @0,30 | 70/203 (34,5%) | 19/64 (29,7%) | **+4,8 pp** | 133 | 45 |
| K-2 saja @0,15 | 135/203 (66,5%) | 28/64 (43,8%) | **+22,8 pp** | 68 | 36 |
| Lantai penuh @0,30 | 66/203 (32,5%) | 18/64 (28,1%) | **+4,4 pp** | 137 | 46 |
| Lantai penuh @0,15 | 117/203 (57,6%) | 21/64 (32,8%) | **+24,8 pp** | 86 | 43 |

Bacaan yang mengikat untuk U2:

- **@0,30 hampir menghapus nilai K-1.** Di dalam subset yang sudah lolos K-1, verified lolos @0,30 hanya 66/147 (44,9%) sedangkan falsified 18/28 (64,3%): pemisahan **−19,4 pp (terbalik)**. Inilah sebabnya pemisahan lantai penuh @0,30 tinggal +4,4 pp walaupun K-1 sendiri +28,7 pp.
- **@0,15 tidak terbalik di dalam K-1.** Verified 117/147 (79,6%) versus falsified 21/28 (75,0%): pemisahan **+4,6 pp**. Pemisahan lantai penuh menjadi +24,8 pp, terutama diwarisi K-1, tetapi @0,15 jauh lebih sedikit merusak K-1 daripada @0,30.
- **K-1 sendiri tetap pemisah terkuat di panel ini (+28,7 pp).** Jadi data korpus juara mendukung @0,15 *mengalahkan* @0,30, tetapi tidak membuktikan K-2 menambah daya pisah di atas K-1. Fungsi K-2 sebagai pembunuh spesies draf kita tetap argumen terpisah dari desain §45, bukan hasil diskriminasi panel ini.
- **Biaya false-rejection juara:** @0,30 menahan 137/203 verified (67,5%); @0,15 menahan 86/203 (42,4%). Perbedaan 51 jawaban verified juara berpindah dari tertahan menjadi lolos hanya dengan mengganti angka K-2.

## 3. Distribusi per agen — verified

Median (q1–q3). Slot dihitung per jawaban dan dapat tumpang tindih Pioneer+Marathon; kolom terakhir adalah sisa verified yang slot terbayarnya tidak terbaca publik.

| Agen | n V / n F | Karakter | URL median | Kepadatan | Rasio | K-1 | @0,30 | @0,15 | Slot terbaca P / M / tak terbaca |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chirpy | 18 / 11 | 14.892 (11.947–18.192) | 8,0 | 0,614 (0,452–0,760) | 0,172 (0,093–0,317) | 72,2% | 33,3% | 61,1% | 2 / 6 / 12 |
| Rodeo | 14 / 3 | 9.403 (7.449–11.667) | 7,5 | 0,730 (0,611–1,017) | 0,136 (0,093–0,209) | 78,6% | 14,3% | 50,0% | 2 / 2 / 10 |
| Febriyan | 24 / 7 | 11.816 (10.545–15.014) | 7,0 | 0,893 (0,448–1,216) | 0,159 (0,101–0,235) | 70,8% | 20,8% | 50,0% | 3 / 10 / 14 |
| Mauldrop | 19 / 3 | 4.890 (3.835–7.587) | 5,0 | 1,181 (0,856–1,951) | 0,494 (0,254–0,611) | 94,7% | 63,2% | 94,7% | 4 / 14 / 4 |
| Adam Reinhard | 16 / 1 | 11.499 (7.946–17.026) | 46,0 | 4,425 (3,227–5,051) | 0,790 (0,633–0,844) | 100,0% | 100,0% | 100,0% | 0 / 10 / 6 |
| megumii | 22 / 4 | 9.544 (8.770–10.540) | 4,0 | 0,641 (0,295–1,287) | 0,229 (0,082–0,318) | 54,5% | 22,7% | 50,0% | 0 / 12 / 10 |
| SyntaxZ | 10 / 1 | 12.079 (10.444–12.404) | 10,0 | 1,014 (0,830–1,157) | 0,222 (0,149–0,317) | 80,0% | 20,0% | 50,0% | 0 / 10 / 0 |
| GaBot | 17 / 2 | 8.223 (7.319–9.267) | 10,0 | 1,500 (1,153–1,920) | 0,416 (0,250–0,564) | 88,2% | 58,8% | 76,5% | 1 / 12 / 5 |
| HIMANSHU | 13 / 11 | 6.253 (5.551–6.622) | 5,0 | 1,065 (0,757–1,439) | 0,203 (0,157–0,263) | 84,6% | 15,4% | 61,5% | 2 / 10 / 1 |
| Gufran The Legend | 17 / 5 | 4.357 (4.054–5.070) | 2,0 | 0,519 (0,443–0,742) | 0,140 (0,088–0,179) | 52,9% | 11,8% | 29,4% | 2 / 10 / 6 |
| can-earn? | 20 / 10 | 13.688 (12.894–14.889) | 6,0 | 0,524 (0,431–1,039) | 0,211 (0,188–0,361) | 50,0% | 20,0% | 50,0% | 10 / 4 / 8 |
| Discord 1 | 13 / 6 | 8.650 (7.496–10.663) | 4,0 | 0,523 (0,231–0,876) | 0,071 (0,047–0,112) | 53,8% | 0,0% | 7,7% | 6 / 3 / 6 |

Rentang agen memperlihatkan lebih dari satu arketipe yang sah:

- **Presisi padat:** Adam Reinhard (median rasio 0,790; kepadatan 4,425; 100% lolos kedua lantai) dan Mauldrop (4.890 kar; rasio 0,494; 94,7% lolos @0,15) — dua bentuk berbeda dari jawaban yang mudah lolos gerbang kita.
- **Long-form rasio-rendah:** chirpy, Febriyan, SyntaxZ, dan can-earn? — dibedah di §4.
- **Rasio-rendah bukan long-form saja:** Discord 1 (median rasio 0,071; 100% jawaban <0,30), Gufran The Legend (0,140), Rodeo (0,136), dan HIMANSHU (0,203) membuktikan K-2 menyaring gaya di banyak panjang, bukan hanya arketipe panjang.
- **Pengecualian format:** Mauldrop hanya 5,3% ber-header dan Discord 1 0% ber-header, tetapi keduanya memenangi slot terbaca. Header adalah pola mayoritas kohort, bukan syarat universal bentuk jawaban (lihat §6).

## 4. Uji hipotesis chirpy — TERUJI SEBAGIAN

Hipotesis run ke-2 berasal dari n=3: chirpy median 18.192 kar, kepadatan 0,440, rasio 0,109, dan dinyatakan gagal lantai. Korpus frame gabungan menaikkan chirpy menjadi **n=18 verified + 11 falsified**.

| Kelompok | n verified | Karakter median (q1–q3) | ≥12.000 kar | Kepadatan median | Rasio median | Long-form + rasio <0,30 | K-1 | @0,30 | @0,15 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chirpy | 18 | 14.892 (11.947–18.192) | 72,2% | 0,614 | 0,172 | 50,0% | 72,2% | 33,3% | 61,1% |
| 11 agen lain | 185 | 9.244 (6.588–12.154) | 28,1% | 0,876 | 0,219 | 20,0% | 72,4% | 32,4% | 57,3% |
| Rodeo | 14 | 9.403 (7.449–11.667) | 14,3% | 0,730 | 0,136 | 14,3% | 78,6% | 14,3% | 50,0% |
| Febriyan | 24 | 11.816 (10.545–15.014) | 50,0% | 0,893 | 0,159 | 41,7% | 70,8% | 20,8% | 50,0% |

Kontras chirpy versus 11 agen lain: Cliff's d karakter **0,567** (kuat), kepadatan **-0,310**, rasio **-0,167**, URL **0,160**. Jadi komponen yang paling khas dari chirpy adalah **panjang**, bukan ketiadaan URL.

### 4.1 Phenotype long-form/rasio-rendah per agen

Definisi phenotype: karakter ≥12.000 **dan** rasio <0,30.

| Agen | n | Median karakter | Median rasio | Phenotype n | Phenotype % |
|---|---:|---:|---:|---:|---:|
| chirpy | 18 | 14.892 | 0,172 | 9 | 50,0% |
| Rodeo | 14 | 9.403 | 0,136 | 2 | 14,3% |
| Febriyan | 24 | 11.816 | 0,159 | 10 | 41,7% |
| Mauldrop | 19 | 4.890 | 0,494 | 1 | 5,3% |
| Adam Reinhard | 16 | 11.499 | 0,790 | 0 | 0,0% |
| megumii | 22 | 9.544 | 0,229 | 2 | 9,1% |
| SyntaxZ | 10 | 12.079 | 0,222 | 5 | 50,0% |
| GaBot | 17 | 8.223 | 0,416 | 2 | 11,8% |
| HIMANSHU | 13 | 6.253 | 0,203 | 0 | 0,0% |
| Gufran The Legend | 17 | 4.357 | 0,140 | 0 | 0,0% |
| can-earn? | 20 | 13.688 | 0,211 | 13 | 65,0% |
| Discord 1 | 13 | 8.650 | 0,071 | 2 | 15,4% |

Vonis mekaniknya:

1. **Long-form chirpy = nyata.** Median 14.892 kar, 72,2% ≥12.000 kar, dan 27,8% ≥18.000 kar — jauh di atas 11 agen lain (median 9.244; 28,1% ≥12.000).
2. **Rasio-rendah chirpy = nyata tetapi bukan unik.** Median chirpy 0,172; sembilan dari 12 agen bermedian rasio <0,30. Phenotype gabungan panjang+rendah terkonsentrasi pada can-earn? 65,0%, chirpy 50,0%, SyntaxZ 50,0%, dan Febriyan 41,7% — ini **sub-arketipe kohort (4 agen)**, bukan pola satu orang.
3. **Klaim 'lantai secara khusus memblokir chirpy' = tidak terbukti.** Chirpy lolos lantai penuh @0,30 sebesar 33,3%, hampir sama dengan gabungan 32,5% dan 11 agen lain 32,4%. Yang diblokir adalah mayoritas verified juara dari hampir semua agen. Pada @0,15 chirpy naik ke 61,1%, juga sejajar gabungan 57,6%.
4. **Yang benar dari hipotesis awal:** bila workflow kita mengharuskan draf menyerupai median chirpy, K-2 @0,30 akan menolak dua pertiga output semacam itu; tetapi alasan lab mengubah ambang—bila diputuskan—harus ditulis sebagai *false-rejection kohort juara yang luas*, bukan pengecualian untuk chirpy.

## 5. Slot yang dimenangi dan implikasi gerbang serve

| Slot terbaca | n jawaban | Karakter median | Kepadatan median | Rasio median | K-1 | @0,30 | @0,15 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pioneer | 32 | 9.496 | 0,746 | 0,191 | 68,8% | 18,8% | 50,0% |
| Marathon Winner | 103 | 8.770 | 1,052 | 0,250 | 80,6% | 37,9% | 67,0% |
| tidak terbaca (Innovator tak berpenanda publik) | 82 | 10.188 | 0,700 | 0,178 | 65,9% | 31,7% | 50,0% |

Catatan slot: 14 jawaban adalah Pioneer sekaligus Marathon Winner, jadi total label slot melebihi 203. Pioneer adalah kelompok yang paling keras ditahan @0,30 (hanya 18,8% lolos) dan naik ke 50,0% pada @0,15. Marathon Winner naik dari 37,9% ke 67,0%.

**Implikasi untuk gerbang serve (bahan lab, bukan keputusan):** menyalin lantai penuh klaim secara membabi buta ke serve akan menahan sebagian besar jawaban yang akhirnya memenangi slot. Sebaliknya, falsified serve kita yang menjadi pemicu perdebatan gerbang adalah teks jejak-penalaran dengan 0 URL/0 sitasi dan target basi — kegagalan itu sudah tertangkap oleh cek yang lebih dasar: target masih eligible/live, keluaran adalah jawaban final (bukan thinking trace), K-1, format/schema, cakupan sub-pertanyaan, bukti empiris, dan audit semantik angka poros. Korpus ini mendukung kesimpulan sempit: **bila K-2 ikut dipasang di serve, @0,15 jauh lebih tidak merusak daripada @0,30; korpus tidak mendukung @0,30 sebagai pintu mati serve.**

## 6. Pola struktural lintas agen

Ambang pembacaan yang dipakai di bagian ini: pola disebut bersama bila prevalensi pooled tinggi dan mayoritas jawaban pada banyak agen; pengecualian per agen selalu ditampilkan agar pola tidak berubah menjadi resep tunggal.

| Pola terukur | Verified pooled | Agen dengan prevalensi ≥50% | Pembacaan |
|---|---:|---:|---|
| Ada header markdown | 78,8% | 10/12 | Pola bersama kuat; pengecualian Mauldrop 5,3% dan Discord 1 0% membuktikan bukan satu-satunya bentuk. |
| Header bernomor | 57,6% | 9/12 | Mayoritas, tetapi lebih lemah daripada keberadaan header; jangan disamakan dengan cakupan sub-pertanyaan. |
| Sitasi muncul di kuartil terakhir teks | 89,7% | 12/12 | Pola bersama terkuat: sumber tetap hadir sampai bagian akhir pada semua agen. |
| Ada angka terikat sitasi dalam 800 karakter terakhir | 84,2% | 12/12 | Penutup juara umumnya substantif/terikat angka, bukan sekadar label kebaruan. |
| Ada angka spesifik terikat yang berulang ≥3 kali (proksi pivot) | 76,8% | 11/12 | Umum pada 11/12 agen, tetapi juga 65,6% pada falsified — ciri gaya, bukan diskriminator verdict. |
| Sitasi tersebar di ≥3 kuartil | 39,9% | 4/12 | Bukan pola universal; hanya 4 agen mayoritas. |
| Sitasi sudah muncul dalam 1.000 karakter pertama | 34,5% | 5/12 | Bukan pola universal; hanya 5 agen mayoritas — ada arketipe front-loaded dan back-loaded. |
| Penutup menamai kebaruan secara eksplisit | 0,5% | 0/12 | Nyaris absen pada verified juara (1/203); konsisten dengan T12.4 bahwa label kebaruan bukan kewajiban. |
| Penutup evasif sumber (regex frasa eksplisit) | 0,0% | 0/12 | 0/203 verified dan 0/64 falsified pada panel ini; lihat keputusan E3 di §8. |

### Kandidat ADOPSI-CATATAN dari pola bersama

- **Struktur ber-header tetap dicatat sebagai ciri juara mayoritas** (78,8%; ≥50% pada 10/12 agen), dengan catatan pengecualian eksplisit Mauldrop/Discord 1. Ini mengonfirmasi arah QUALITY v2, bukan dasar untuk memperketat format menjadi satu templat.
- **Audit penutup sebaiknya mencari isi terikat, bukan frasa kebaruan.** Sitasi mencapai kuartil terakhir pada 89,7% verified dan angka terikat muncul di 800 karakter terakhir pada 84,2%, dengan prevalensi ≥50% di 12/12 agen untuk kedua pola; penanda kebaruan eksplisit hanya 0,5%. Ini adalah penguatan catatan T12.4 yang sudah berlaku: penutup memuat isi baru yang terikat, labelnya bebas.
- **Penempatan sitasi awal tidak boleh dijadikan resep.** Hanya 34,5% verified mempunyai sitasi dalam 1.000 karakter pertama dan hanya 39,9% tersebar ke ≥3 kuartil. Rodeo/Mauldrop/Adam cenderung front-loaded; chirpy/Febriyan/can-earn?/Discord 1 cenderung tidak. Perbedaan ini tetap **HIPOTESIS arketipe**, bukan aturan adopsi.
- **Pengulangan angka spesifik terikat adalah ciri deskriptif, bukan gerbang.** Proksi pivot spesifik muncul pada 76,8% verified dan ≥50% pada 11/12 agen, tetapi juga 65,6% falsified agen yang sama. Ia boleh dicatat sebagai gaya kohort; menjadikannya syarat lolos tidak didukung kontras verdict.

## 7. Kontras falsified dari agen yang sama

| Agen | n F | Karakter median (q1–q3) | Kepadatan median | Rasio median | K-1 | @0,30 | @0,15 |
|---|---:|---:|---:|---:|---:|---:|---:|
| chirpy | 11 | 16.940 (14.293–22.331) | 0,531 | 0,206 | 54,5% | 27,3% | 45,5% |
| Rodeo | 3 | 8.476 (6.372–9.791) | 0,472 | 0,024 | 33,3% | 33,3% | 33,3% |
| Febriyan | 7 | 10.389 (9.934–12.395) | 0,970 | 0,314 | 100,0% | 71,4% | 71,4% |
| Mauldrop | 3 | 6.245 (3.086–7.357) | 1,296 | 0,400 | 100,0% | 66,7% | 66,7% |
| Adam Reinhard | 1 | 6.191 (6.191–6.191) | 1,938 | 0,462 | 100,0% | 100,0% | 100,0% |
| megumii | 4 | 10.040 (9.460–11.436) | 0,349 | 0,083 | 0,0% | 0,0% | 0,0% |
| SyntaxZ | 1 | 10.121 (10.121–10.121) | 1,087 | 0,091 | 100,0% | 0,0% | 0,0% |
| GaBot | 2 | 9.066 (7.993–10.138) | 2,416 | 0,476 | 100,0% | 100,0% | 100,0% |
| HIMANSHU | 11 | 3.480 (2.542–5.625) | 0,000 | 0,000 | 27,3% | 18,2% | 27,3% |
| Gufran The Legend | 5 | 7.056 (4.821–7.565) | 0,207 | 0,033 | 20,0% | 0,0% | 0,0% |
| can-earn? | 10 | 12.606 (12.203–13.752) | 0,445 | 0,141 | 30,0% | 20,0% | 20,0% |
| Discord 1 | 6 | 5.235 (4.778–5.553) | 0,214 | 0,070 | 0,0% | 0,0% | 0,0% |

Kontras ini adalah pembanding wajib, bukan pasangan matched per pertanyaan/topik. Beberapa n falsified sangat kecil (Adam Reinhard 1, SyntaxZ 1, GaBot 2, Mauldrop 3, Rodeo 3), jadi angka per agen tidak boleh dibaca sebagai rate agen. Pada level pooled, falsified panel hampir sama panjangnya dengan verified (median 9.626 vs 9.549) tetapi lebih jarang URL (median 5 vs 6), lebih rendah kepadatan (0,454 vs 0,842), dan lebih rendah rasio (0,119 vs 0,212).

Anomali yang mencegah pembacaan naif: falsified Febriyan (n=7) lolos lantai penuh 71,4% pada kedua ambang — lebih tinggi daripada verified Febriyan sendiri (20,8% @0,30; 50,0% @0,15). Ini menegaskan lagi bahwa lantai mekanik adalah saringan spesies gagal tertentu, bukan penjamin atau prediktor verdict individual.

## 8. KEPUTUSAN YANG DIMINTA DARI LAB

### U2 — angka final korpus ini

Lab diminta memilih dengan angka panel juara berikut di atas meja: lantai penuh @0,30 meloloskan **32,5% verified / 28,1% falsified (+4,4 pp)**; @0,15 meloloskan **57,6% verified / 32,8% falsified (+24,8 pp)**; di dalam K-1, @0,30 terbalik **−19,4 pp**, @0,15 **+4,6 pp**. Korpus ini menempatkan @0,15 jelas di atas @0,30. Lab tetap harus menimbang dua caveat: (i) K-1 saja memisahkan +28,7 pp, jadi K-2 tidak terbukti menambah diskriminasi; (ii) syarat desain §45 tentang verdict klaim kita sendiri belum terpenuhi. Keputusan yang diminta: **tetap 0,30, turun ke 0,15, atau tunda menurut §45 — dengan alasan yang merujuk angka ini.** Korpus tidak mengubah ambang.

### Gerbang serve — apakah juara lolos gerbang yang akan dipasang

Lab diminta memutuskan tumpukan gerbang serve secara eksplisit, bukan menyalin lantai klaim utuh. Data penentu: jawaban pemenang Pioneer hanya 18,8% lolos @0,30 dan 50,0% @0,15; Marathon Winner 37,9% dan 67,0%. Bila gerbang serve memakai K-2 sebagai pintu mati, @0,30 adalah pilihan yang paling merusak menurut korpus. Minimum yang didukung data untuk dibahas lab: kelayakan/live target, jawaban final bukan thinking trace, K-1, format/schema, cakupan sub-pertanyaan, bukti empiris, dan audit semantik angka poros; keputusan apakah K-2 @0,15 ikut menjadi pintu serve harus dinyatakan terpisah.

### E3 — penutup evasif sumber

Regex frasa eksplisit menemukan **0/203 verified dan 0/64 falsified** dengan penutup evasif sumber di panel juara ini. Jadi korpus eksternal **tidak menambah maupun membantah** bukti E3; ambang adopsi E3 yang sudah terpenuhi bertumpu pada jawaban kita sendiri yang falsified, sesuai rumusan eksperimen di QUALITY.md. Keputusan yang diminta dari lab: adopsi E3 sebagai cek negatif berdasarkan bukti internal itu, atau tunda — tetapi jangan mencatat korpus juara sebagai koroborasi eksternal E3. Regex ini juga hanya menangkap frasa eksplisit, bukan penghindaran yang diparafrasekan.

### Format header/penomoran

Lab boleh menimbang apakah catatan workflow perlu membedakan lebih tajam antara *cakupan berstruktur* dan *penomoran literal*: header ada pada 78,8% verified, header bernomor 57,6%; Mauldrop dan Discord 1 menang dengan hampir/tanpa header. Korpus tidak meminta perubahan QUALITY.md di sini; ia hanya mencegah angka 78,8% dibaca sebagai kewajiban templat tunggal.

## 9. Daftar negatif dan keterbatasan

1. **Tidak ada indeks publik per-penulis** yang ditemukan di jalur tarikan yang dipakai; jawaban panel di luar 212 pertanyaan sampel tidak bisa ditarik secara terarah dari artefak/API yang dipakai. Karena itu 'korpus penuh' di file ini selalu berarti penuh *di dalam frame dua tarikan belajar*, bukan lifetime platform.
2. **Tidak ada jawaban panel verified/falsified tanpa teks** di frame terpilih: daftar negatif teks kosong = 0 dari 267 jawaban verdict panel.
3. **Innovator tidak terukur.** 82 verified berlabel 'tidak terbaca' hanya berarti bukan Pioneer pertama dan tidak ada flag Marathon awarded pada detail snapshot; mereka bisa saja termasuk pembayaran Innovator atau slot lain yang tidak diterbitkan per jawaban.
4. **Status dibekukan oleh snapshot.** Untuk pertanyaan tumpang tindih dipakai status run 10:37; untuk pertanyaan lain status 02:40. Verdict yang berubah sesudah tarikan masing-masing tidak masuk.
5. **Tidak ada audit entailment semantik per jawaban.** Rasio ±150 karakter adalah proksi mekanik persis wrapper; jawaban yang 'lolos' di file ini belum tentu sitasi-sitasinya mendukung klaimnya, dan jawaban yang 'gagal' belum tentu salah secara semantik.
6. **Proksi angka poros bukan identifikasi tesis.** Definisi proksi: nilai desimal/persen/tahun/≥100 yang muncul ≥3 kali dan setidaknya sekali terikat sitasi. Ia menangkap pengulangan terikat, bukan membuktikan angka itu menopang kesimpulan.
7. **E3 diukur dengan regex frasa eksplisit.** Nol temuan berarti nol frasa yang cocok, bukan bukti tidak ada penghindaran sumber dalam bentuk bahasa lain.
8. **Kontras falsified tidak matched.** Verified dan falsified berasal dari agen serta frame yang sama, tetapi tidak dipasangkan per pertanyaan, topik, viso, atau waktu; n falsified per agen timpang.
9. **Pioneer bergantung pada kelengkapan daftar ISO snapshot dan stempel yang diterbitkan API.** Metode ini sama dengan §30, tetapi tidak diaudit ke sumber kedua.

## Lampiran A — Semua jawaban VERIFIED panel (203)

Kolom: Kar = karakter; Sit = total span sitasi; Terikat = angka terikat/total token angka; Slot P=Pioneer, M=Marathon Winner, —=tidak terbaca; L=lolos, G=gagal.

| Agen | ISO | ISR | Kar | URL | Sit | Kepadatan | Terikat | Rasio | Slot | K-1 | @0,30 | @0,15 |
|---|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|
| Adam Reinhard | 93df4e56 | 71f472d6 | 19.062 | 62 | 64 | 3,357 | 73/130 | 0,562 | M | L | L | L |
| Adam Reinhard | 8e09eba3 | 472b29a0 | 8.848 | 35 | 39 | 4,408 | 40/48 | 0,833 | M | L | L | L |
| Adam Reinhard | 9a62a8ea | 5869b52e | 9.181 | 37 | 40 | 4,357 | 38/45 | 0,844 | — | L | L | L |
| Adam Reinhard | 7af747e2 | 8c9c01f2 | 5.060 | 8 | 15 | 2,964 | 19/30 | 0,633 | M | L | L | L |
| Adam Reinhard | 324a3042 | 60fa9935 | 7.765 | 13 | 24 | 3,091 | 36/43 | 0,837 | M | L | L | L |
| Adam Reinhard | f02c779d | f7e02fc3 | 11.533 | 55 | 55 | 4,769 | 61/72 | 0,847 | — | L | L | L |
| Adam Reinhard | fa3582fb | e20d251f | 11.465 | 35 | 37 | 3,227 | 28/32 | 0,875 | — | L | L | L |
| Adam Reinhard | b45b9c8e | d854b19a | 15.658 | 97 | 98 | 6,259 | 102/128 | 0,797 | — | L | L | L |
| Adam Reinhard | e6971f70 | 21ef1f75 | 12.898 | 68 | 68 | 5,272 | 81/119 | 0,681 | — | L | L | L |
| Adam Reinhard | 2e4b922c | 97274fcc | 17.026 | 86 | 86 | 5,051 | 85/98 | 0,867 | M | L | L | L |
| Adam Reinhard | b843e9c8 | bf7cc34f | 5.090 | 8 | 9 | 1,768 | 10/16 | 0,625 | M | L | L | L |
| Adam Reinhard | 642051a7 | 80aa63c0 | 7.946 | 10 | 10 | 1,258 | 17/54 | 0,315 | M | L | L | L |
| Adam Reinhard | fcc60d2d | 98b011f3 | 23.191 | 115 | 115 | 4,959 | 132/196 | 0,673 | M | L | L | L |
| Adam Reinhard | 472ca24d | f6940d0d | 21.375 | 111 | 112 | 5,240 | 137/175 | 0,783 | M | L | L | L |
| Adam Reinhard | 1e16b615 | 9d93f7fe | 15.607 | 76 | 76 | 4,870 | 76/92 | 0,826 | — | L | L | L |
| Adam Reinhard | bbf496a6 | a1265b87 | 5.404 | 24 | 24 | 4,441 | 28/46 | 0,609 | M | L | L | L |
| Discord 1 | d5ecdefd | d854b19a | 17.954 | 13 | 13 | 0,724 | 25/224 | 0,112 | — | L | G | G |
| Discord 1 | 664b2461 | 21ef1f75 | 10.663 | 4 | 4 | 0,375 | 10/94 | 0,106 | — | G | G | G |
| Discord 1 | ed3c96ef | 37dce0fa | 6.523 | 1 | 1 | 0,153 | 1/38 | 0,026 | — | G | G | G |
| Discord 1 | dd67266f | 5b219615 | 8.792 | 2 | 2 | 0,227 | 2/57 | 0,035 | — | G | G | G |
| Discord 1 | 454fc505 | 0e901710 | 7.496 | 1 | 1 | 0,133 | 2/48 | 0,042 | P | G | G | G |
| Discord 1 | a79d5df1 | bb77f86f | 8.650 | 2 | 2 | 0,231 | 5/106 | 0,047 | — | G | G | G |
| Discord 1 | d443bba8 | bd33b747 | 10.270 | 9 | 9 | 0,876 | 6/92 | 0,065 | P+M | L | G | G |
| Discord 1 | 56ba3267 | e9509814 | 7.724 | 5 | 5 | 0,647 | 12/82 | 0,146 | P | L | G | G |
| Discord 1 | 65002a67 | 9f6a21c9 | 5.561 | 2 | 2 | 0,360 | 5/96 | 0,052 | M | G | G | G |
| Discord 1 | 7c2b30f3 | 9d93f7fe | 7.652 | 4 | 4 | 0,523 | 1/14 | 0,071 | — | L | G | G |
| Discord 1 | 66cf660c | 94ee459e | 5.062 | 5 | 5 | 0,988 | 7/65 | 0,108 | P | L | G | G |
| Discord 1 | 23f2e010 | 385a54ba | 17.330 | 18 | 18 | 1,039 | 59/236 | 0,250 | P | L | G | L |
| Discord 1 | 47b35a21 | 2d05b2a5 | 10.954 | 12 | 14 | 1,278 | 35/241 | 0,145 | P+M | L | G | G |
| Febriyan | a28f77ee | 71f472d6 | 12.413 | 2 | 2 | 0,161 | 8/37 | 0,216 | — | G | G | G |
| Febriyan | 188c2e40 | 8aacc7f8 | 12.343 | 3 | 3 | 0,243 | 11/185 | 0,059 | — | G | G | G |
| Febriyan | 2652d7b1 | 8c9c01f2 | 10.675 | 2 | 19 | 1,780 | 10/21 | 0,476 | M | L | L | L |
| Febriyan | cfb6bcb9 | 60fa9935 | 10.500 | 8 | 32 | 3,048 | 84/139 | 0,604 | M | L | L | L |
| Febriyan | 0006fe08 | 1d758352 | 15.519 | 13 | 15 | 0,967 | 10/64 | 0,156 | M | L | G | L |
| Febriyan | 14aa07c8 | 5869b52e | 19.334 | 11 | 36 | 1,862 | 46/95 | 0,484 | M | L | L | L |
| Febriyan | 526e9ecb | 7cc5c1d5 | 12.319 | 10 | 10 | 0,812 | 27/154 | 0,175 | — | L | G | L |
| Febriyan | 4cc167ea | f7e02fc3 | 6.506 | 2 | 2 | 0,307 | 2/24 | 0,083 | — | G | G | G |
| Febriyan | 95ce600d | 79437a33 | 9.062 | 4 | 4 | 0,441 | 12/115 | 0,104 | — | G | G | G |
| Febriyan | c179abe9 | e20d251f | 13.505 | 15 | 26 | 1,925 | 35/99 | 0,354 | — | L | L | L |
| Febriyan | 6f974942 | d854b19a | 19.396 | 8 | 8 | 0,412 | 15/297 | 0,051 | — | G | G | G |
| Febriyan | 50aff436 | 21ef1f75 | 11.155 | 5 | 5 | 0,448 | 5/85 | 0,059 | — | G | G | G |
| Febriyan | d6fcf5fc | 314024e4 | 9.745 | 9 | 9 | 0,924 | 4/118 | 0,034 | — | L | G | G |
| Febriyan | bc187d91 | 37dce0fa | 17.272 | 16 | 16 | 0,926 | 16/141 | 0,113 | — | L | G | G |
| Febriyan | 997414a6 | 5b219615 | 10.631 | 7 | 7 | 0,658 | 23/98 | 0,235 | — | L | G | L |
| Febriyan | 35971775 | 38f7d21f | 10.545 | 5 | 21 | 1,991 | 17/54 | 0,315 | — | L | L | L |
| Febriyan | 6908d7c1 | 31072e67 | 10.083 | 7 | 10 | 0,992 | 19/128 | 0,148 | — | L | G | G |
| Febriyan | 7de10843 | dbd4f6b9 | 12.145 | 2 | 8 | 0,659 | 9/78 | 0,115 | — | L | G | G |
| Febriyan | 818d365b | bb77f86f | 15.751 | 16 | 16 | 1,016 | 45/201 | 0,224 | M | L | G | L |
| Febriyan | 9b0aa769 | 48c80dc6 | 15.014 | 13 | 16 | 1,066 | 30/128 | 0,234 | M | L | G | L |
| Febriyan | fe271830 | 80aa63c0 | 14.806 | 11 | 18 | 1,216 | 25/148 | 0,169 | P+M | L | G | L |
| Febriyan | 34b6f480 | bc49f758 | 11.486 | 7 | 7 | 0,609 | 23/250 | 0,092 | P+M | L | G | G |
| Febriyan | c727edd8 | aa1a533d | 11.168 | 4 | 4 | 0,358 | 16/158 | 0,101 | M | G | G | G |
| Febriyan | 2c4324c5 | d2e190b5 | 5.799 | 5 | 5 | 0,862 | 23/142 | 0,162 | P+M | L | G | L |
| GaBot | dc5dec01 | 60fa9935 | 7.319 | 5 | 31 | 4,236 | 67/86 | 0,779 | M | L | L | L |
| GaBot | f4b4e157 | 1d3efb52 | 5.988 | 8 | 8 | 1,336 | 13/32 | 0,406 | M | L | L | L |
| GaBot | 2e137057 | 8c9c01f2 | 8.223 | 13 | 22 | 2,675 | 21/42 | 0,500 | M | L | L | L |
| GaBot | f7601f2a | 1d758352 | 6.299 | 10 | 10 | 1,588 | 21/46 | 0,457 | M | L | L | L |
| GaBot | 3fd502c9 | 8aacc7f8 | 6.588 | 4 | 5 | 0,759 | 35/140 | 0,250 | M | L | G | L |
| GaBot | ac743f63 | 5869b52e | 11.336 | 16 | 17 | 1,500 | 26/88 | 0,295 | M | L | G | L |
| GaBot | 7ef3950b | 79437a33 | 7.828 | 17 | 17 | 2,172 | 66/117 | 0,564 | — | L | L | L |
| GaBot | 3a45969c | e20d251f | 7.290 | 13 | 14 | 1,920 | 11/16 | 0,688 | M | L | L | L |
| GaBot | c2c43753 | f7e02fc3 | 8.671 | 10 | 10 | 1,153 | 16/133 | 0,120 | M | L | G | G |
| GaBot | a0675780 | c6d213c0 | 7.458 | 12 | 12 | 1,609 | 18/30 | 0,600 | — | L | L | L |
| GaBot | a01330ce | dbd4f6b9 | 10.089 | 10 | 12 | 1,189 | 24/54 | 0,444 | — | L | L | L |
| GaBot | bbd51ca6 | e46c0387 | 8.536 | 10 | 11 | 1,289 | 47/113 | 0,416 | M | L | L | L |
| GaBot | b145234a | d91de605 | 12.152 | 20 | 20 | 1,646 | 15/55 | 0,273 | — | L | G | L |
| GaBot | c10bd5c9 | 693c0d6b | 9.267 | 5 | 6 | 0,647 | 19/151 | 0,126 | — | L | G | G |
| GaBot | 1ad86ff6 | 1c5f15d2 | 8.576 | 4 | 4 | 0,466 | 14/64 | 0,219 | M | G | G | G |
| GaBot | af228b0a | 356c90fc | 12.154 | 4 | 5 | 0,411 | 14/96 | 0,146 | M | G | G | G |
| GaBot | 98395171 | 886afcd0 | 7.698 | 15 | 15 | 1,949 | 39/56 | 0,696 | P+M | L | L | L |
| Gufran The Legend | 71a5d6e6 | e20d251f | 5.070 | 0 | 0 | 0,000 | 0/18 | 0,000 | M | G | G | G |
| Gufran The Legend | 715381a5 | 1d3efb52 | 6.162 | 5 | 6 | 0,974 | 6/66 | 0,091 | M | L | G | G |
| Gufran The Legend | 89725756 | 8c9c01f2 | 6.053 | 5 | 24 | 3,965 | 26/39 | 0,667 | M | L | L | L |
| Gufran The Legend | d7175b8a | 472b29a0 | 5.970 | 4 | 6 | 1,005 | 10/56 | 0,179 | M | L | G | L |
| Gufran The Legend | f74819ec | 71f472d6 | 4.624 | 3 | 3 | 0,649 | 7/24 | 0,292 | M | L | G | L |
| Gufran The Legend | 22bdf9c4 | bb77f86f | 3.802 | 2 | 2 | 0,526 | 2/28 | 0,071 | — | L | G | G |
| Gufran The Legend | 057e0967 | bf7cc34f | 3.580 | 2 | 3 | 0,838 | 5/13 | 0,385 | — | L | L | L |
| Gufran The Legend | 16ec70ad | 1782ccf2 | 4.080 | 2 | 2 | 0,490 | 3/18 | 0,167 | P | G | G | G |
| Gufran The Legend | 0909b297 | 693c0d6b | 4.357 | 2 | 3 | 0,689 | 8/57 | 0,140 | — | L | G | G |
| Gufran The Legend | 6fc32bd1 | e25d35d6 | 4.517 | 2 | 2 | 0,443 | 11/64 | 0,172 | — | G | G | G |
| Gufran The Legend | ff45200b | a1389f56 | 3.851 | 2 | 2 | 0,519 | 4/23 | 0,174 | — | L | G | L |
| Gufran The Legend | 5e0950db | e46c0387 | 4.241 | 1 | 1 | 0,236 | 2/30 | 0,067 | M | G | G | G |
| Gufran The Legend | 8c5ac7de | d91de605 | 5.837 | 2 | 2 | 0,343 | 3/34 | 0,088 | M | G | G | G |
| Gufran The Legend | a3f4e800 | dbd4f6b9 | 4.054 | 2 | 2 | 0,493 | 2/24 | 0,083 | M | G | G | G |
| Gufran The Legend | e951ebf1 | 966e3512 | 4.545 | 2 | 2 | 0,440 | 5/28 | 0,179 | — | G | G | G |
| Gufran The Legend | 7f85aa9b | 94ee459e | 2.695 | 2 | 2 | 0,742 | 6/49 | 0,122 | M | L | G | G |
| Gufran The Legend | 7a8ccff2 | dd8b2ff9 | 4.284 | 2 | 2 | 0,467 | 6/59 | 0,102 | P+M | G | G | G |
| HIMANSHU | f62a0dd5 | f7e02fc3 | 6.527 | 2 | 2 | 0,306 | 10/55 | 0,182 | M | G | G | G |
| HIMANSHU | 959b3b73 | 79437a33 | 5.635 | 6 | 6 | 1,065 | 30/148 | 0,203 | M | L | G | L |
| HIMANSHU | 20b03685 | f80ac8d3 | 6.609 | 5 | 5 | 0,757 | 5/87 | 0,057 | M | L | G | G |
| HIMANSHU | efff6821 | 1f58031d | 5.551 | 3 | 6 | 1,081 | 3/12 | 0,250 | — | L | G | L |
| HIMANSHU | b3b11746 | 60fa9935 | 6.230 | 6 | 13 | 2,087 | 9/33 | 0,273 | M | L | G | L |
| HIMANSHU | db8d82c8 | 2c7efc3e | 6.914 | 4 | 10 | 1,446 | 11/22 | 0,500 | M | L | L | L |
| HIMANSHU | 1c89f21b | 1d3efb52 | 8.856 | 7 | 7 | 0,790 | 5/84 | 0,060 | M | L | G | G |
| HIMANSHU | bee0856d | 1d758352 | 6.253 | 5 | 9 | 1,439 | 3/27 | 0,111 | M | L | G | G |
| HIMANSHU | 225d8928 | 8aacc7f8 | 10.481 | 9 | 9 | 0,859 | 18/97 | 0,186 | M | L | G | L |
| HIMANSHU | 8913f3c5 | 5869b52e | 6.622 | 8 | 10 | 1,510 | 2/8 | 0,250 | M | L | G | L |
| HIMANSHU | d8a6fb6a | 472b29a0 | 4.326 | 2 | 2 | 0,462 | 8/51 | 0,157 | M | G | G | G |
| HIMANSHU | 2b14bb91 | cef6bcea | 4.148 | 3 | 3 | 0,723 | 21/64 | 0,328 | P | L | L | L |
| HIMANSHU | 8f7ddb39 | 355aa793 | 1.870 | 2 | 2 | 1,070 | 10/38 | 0,263 | P | L | G | L |
| Mauldrop | 079f2eaf | 5869b52e | 12.473 | 8 | 9 | 0,722 | 28/95 | 0,295 | M | L | G | L |
| Mauldrop | e937bc31 | 472b29a0 | 6.772 | 7 | 8 | 1,181 | 33/54 | 0,611 | M | L | L | L |
| Mauldrop | bddd4151 | f7e02fc3 | 4.336 | 7 | 7 | 1,614 | 26/49 | 0,531 | M | L | L | L |
| Mauldrop | d20b7bda | 8c9c01f2 | 4.890 | 3 | 10 | 2,045 | 18/31 | 0,581 | M | L | L | L |
| Mauldrop | 3d30286d | 71f472d6 | 7.472 | 4 | 4 | 0,535 | 12/62 | 0,194 | M | L | G | L |
| Mauldrop | 9256f123 | aa59f63f | 9.314 | 8 | 8 | 0,859 | 17/67 | 0,254 | M | L | G | L |
| Mauldrop | f5174758 | 1f58031d | 4.660 | 9 | 12 | 2,575 | 43/45 | 0,956 | — | L | L | L |
| Mauldrop | 9ba9729a | d854b19a | 3.912 | 5 | 5 | 1,278 | 25/42 | 0,595 | — | L | L | L |
| Mauldrop | 334f6287 | 314024e4 | 3.053 | 5 | 5 | 1,638 | 42/85 | 0,494 | P+M | L | L | L |
| Mauldrop | 469ce737 | 37dce0fa | 3.110 | 4 | 4 | 1,286 | 15/29 | 0,517 | P+M | L | L | L |
| Mauldrop | 394253f0 | 5b219615 | 3.511 | 4 | 4 | 1,139 | 10/41 | 0,244 | P | L | G | L |
| Mauldrop | 91a3be56 | 38f7d21f | 3.651 | 4 | 11 | 3,013 | 10/15 | 0,667 | M | L | L | L |
| Mauldrop | 97cbdc4e | dbd4f6b9 | 7.587 | 14 | 18 | 2,372 | 36/53 | 0,679 | M | L | L | L |
| Mauldrop | 57055732 | 59279b57 | 3.835 | 2 | 2 | 0,522 | 8/25 | 0,320 | M | L | L | L |
| Mauldrop | 3c86bef1 | 693c0d6b | 9.653 | 7 | 9 | 0,932 | 24/139 | 0,173 | — | L | G | L |
| Mauldrop | 55e80721 | 1782ccf2 | 10.798 | 12 | 12 | 1,111 | 30/82 | 0,366 | M | L | L | L |
| Mauldrop | d27f4d31 | e9509814 | 5.043 | 2 | 2 | 0,397 | 9/35 | 0,257 | — | G | G | G |
| Mauldrop | 76844248 | a2aeccd2 | 7.175 | 14 | 14 | 1,951 | 29/42 | 0,690 | P+M | L | L | L |
| Mauldrop | 0e18c585 | 966e3512 | 4.675 | 4 | 4 | 0,856 | 8/38 | 0,211 | M | L | G | L |
| Rodeo | 271203f5 | 21ef1f75 | 9.549 | 7 | 7 | 0,733 | 10/48 | 0,208 | — | L | G | L |
| Rodeo | 027cf098 | 38f7d21f | 9.457 | 13 | 24 | 2,538 | 10/19 | 0,526 | — | L | L | L |
| Rodeo | 16d66c19 | dbd4f6b9 | 9.349 | 3 | 4 | 0,428 | 0/13 | 0,000 | — | G | G | G |
| Rodeo | 174eb448 | e46c0387 | 6.883 | 8 | 12 | 1,743 | 5/54 | 0,093 | — | L | G | G |
| Rodeo | a1939e8c | 59279b57 | 14.738 | 9 | 9 | 0,611 | 23/114 | 0,202 | M | L | G | L |
| Rodeo | d2dc965e | 356c90fc | 6.881 | 4 | 7 | 1,017 | 1/46 | 0,022 | M | L | G | G |
| Rodeo | 41f76734 | bb77f86f | 11.667 | 4 | 4 | 0,343 | 8/71 | 0,113 | — | G | G | G |
| Rodeo | c107aa21 | bf7cc34f | 7.449 | 10 | 11 | 1,477 | 5/15 | 0,333 | — | L | L | L |
| Rodeo | fb6d61a6 | cd871256 | 9.639 | 6 | 7 | 0,726 | 5/32 | 0,156 | — | L | G | L |
| Rodeo | 558fe53a | 1782ccf2 | 7.044 | 3 | 3 | 0,426 | 3/31 | 0,097 | — | G | G | G |
| Rodeo | dd3119b3 | 693c0d6b | 8.659 | 5 | 6 | 0,693 | 0/42 | 0,000 | P | L | G | G |
| Rodeo | 4edcbd01 | a1389f56 | 11.874 | 8 | 10 | 0,842 | 19/73 | 0,260 | — | L | G | L |
| Rodeo | 9a6ca8b3 | e25d35d6 | 8.721 | 8 | 8 | 0,917 | 19/91 | 0,209 | P | L | G | L |
| Rodeo | 9920d83b | e9509814 | 12.684 | 9 | 9 | 0,710 | 11/95 | 0,116 | — | L | G | G |
| SyntaxZ | 38640560 | 2c7efc3e | 7.972 | 7 | 15 | 1,882 | 20/46 | 0,435 | M | L | L | L |
| SyntaxZ | 9c117021 | 1d3efb52 | 12.311 | 12 | 12 | 0,975 | 25/160 | 0,156 | M | L | G | L |
| SyntaxZ | 72df93ab | 8ca09770 | 17.251 | 13 | 16 | 0,927 | 43/151 | 0,285 | M | L | G | L |
| SyntaxZ | d0c8f319 | f80ac8d3 | 19.529 | 10 | 10 | 0,512 | 25/231 | 0,108 | M | L | G | G |
| SyntaxZ | fb7c5bf7 | d854b19a | 9.507 | 10 | 10 | 1,052 | 26/174 | 0,149 | M | L | G | G |
| SyntaxZ | d2383c96 | c6d213c0 | 10.444 | 12 | 12 | 1,149 | 17/96 | 0,177 | M | L | G | L |
| SyntaxZ | 482b1a79 | 38f7d21f | 12.054 | 16 | 19 | 1,576 | 35/46 | 0,761 | M | L | L | L |
| SyntaxZ | b029adab | 5b219615 | 12.046 | 0 | 10 | 0,830 | 46/145 | 0,317 | M | G | G | G |
| SyntaxZ | 678f76eb | 31072e67 | 12.104 | 8 | 14 | 1,157 | 10/150 | 0,067 | M | L | G | G |
| SyntaxZ | 793317aa | 37dce0fa | 12.404 | 3 | 3 | 0,242 | 21/79 | 0,266 | M | G | G | G |
| can-earn? | c904f9cb | e20d251f | 14.889 | 15 | 20 | 1,343 | 18/85 | 0,212 | M | L | G | L |
| can-earn? | 177e428d | 21ef1f75 | 13.931 | 6 | 6 | 0,431 | 4/160 | 0,025 | — | G | G | G |
| can-earn? | b379498b | 38f7d21f | 12.833 | 4 | 25 | 1,948 | 26/132 | 0,197 | — | L | G | L |
| can-earn? | 2b1f2c4f | dbd4f6b9 | 12.894 | 7 | 16 | 1,241 | 26/53 | 0,491 | — | L | L | L |
| can-earn? | d6b7539f | 0e901710 | 14.871 | 16 | 17 | 1,143 | 81/152 | 0,533 | — | L | L | L |
| can-earn? | 44ba5c41 | 59279b57 | 15.377 | 4 | 4 | 0,260 | 8/81 | 0,099 | P | G | G | G |
| can-earn? | 63e76d3b | bb77f86f | 13.446 | 6 | 6 | 0,446 | 13/36 | 0,361 | P | G | G | G |
| can-earn? | bbcea12e | bf7cc34f | 13.944 | 5 | 5 | 0,359 | 11/119 | 0,092 | P | G | G | G |
| can-earn? | a0ee1486 | cd871256 | 18.039 | 9 | 9 | 0,499 | 47/224 | 0,210 | — | G | G | G |
| can-earn? | d7c0a947 | 1782ccf2 | 13.299 | 8 | 8 | 0,602 | 30/64 | 0,469 | — | L | L | L |
| can-earn? | e48a92eb | a1389f56 | 15.999 | 6 | 6 | 0,375 | 33/114 | 0,289 | P | G | G | G |
| can-earn? | cf141201 | bd33b747 | 14.514 | 5 | 5 | 0,344 | 12/209 | 0,057 | M | G | G | G |
| can-earn? | dd6984a7 | 9d93f7fe | 17.692 | 6 | 6 | 0,339 | 31/123 | 0,252 | P | G | G | G |
| can-earn? | 74e06ffd | 9f6a21c9 | 13.273 | 6 | 6 | 0,452 | 29/283 | 0,102 | P | G | G | G |
| can-earn? | 7f2f8ee7 | 94ee459e | 8.271 | 4 | 4 | 0,484 | 19/53 | 0,358 | — | G | G | G |
| can-earn? | c74c4af5 | f551991c | 14.364 | 8 | 8 | 0,557 | 34/181 | 0,188 | P | L | G | L |
| can-earn? | 1be3cead | 6d534f14 | 12.983 | 10 | 10 | 0,770 | 48/249 | 0,193 | P | L | G | L |
| can-earn? | 78d36219 | 57b685b5 | 12.510 | 13 | 13 | 1,039 | 67/261 | 0,257 | P+M | L | G | L |
| can-earn? | a5e3d446 | 61a55034 | 11.274 | 9 | 9 | 0,798 | 52/141 | 0,369 | — | L | L | L |
| can-earn? | 6c4e3823 | 108bd14f | 10.934 | 6 | 6 | 0,549 | 38/180 | 0,211 | P+M | L | G | L |
| chirpy | ce08a4f2 | 7cc5c1d5 | 11.680 | 8 | 8 | 0,685 | 15/168 | 0,089 | — | L | G | G |
| chirpy | 9eee1a59 | f7e02fc3 | 3.077 | 0 | 0 | 0,000 | 0/16 | 0,000 | — | G | G | G |
| chirpy | c025b3f8 | c6d213c0 | 13.099 | 1 | 1 | 0,076 | 3/76 | 0,039 | — | G | G | G |
| chirpy | add7ec35 | 314024e4 | 14.478 | 8 | 11 | 0,760 | 41/246 | 0,167 | — | L | G | L |
| chirpy | 06c77ec8 | 37dce0fa | 15.309 | 11 | 11 | 0,719 | 29/107 | 0,271 | — | L | G | L |
| chirpy | 48ed73c9 | 5b219615 | 26.689 | 30 | 30 | 1,124 | 156/376 | 0,415 | — | L | L | L |
| chirpy | c5c7b466 | 38f7d21f | 7.821 | 5 | 20 | 2,557 | 23/50 | 0,460 | — | L | L | L |
| chirpy | 0502b66c | 31072e67 | 11.947 | 6 | 8 | 0,670 | 19/204 | 0,093 | — | L | G | G |
| chirpy | d20a32eb | 0e901710 | 15.305 | 8 | 8 | 0,523 | 29/185 | 0,157 | M | L | G | L |
| chirpy | 666d4214 | 59279b57 | 12.427 | 7 | 7 | 0,563 | 26/82 | 0,317 | M | L | L | L |
| chirpy | e3f8b6d6 | 356c90fc | 13.558 | 11 | 12 | 0,885 | 18/57 | 0,316 | — | L | L | L |
| chirpy | 29cf883a | 1782ccf2 | 18.645 | 10 | 10 | 0,536 | 47/137 | 0,343 | — | L | L | L |
| chirpy | cb37a451 | bd33b747 | 20.471 | 11 | 11 | 0,537 | 39/255 | 0,153 | M | L | G | L |
| chirpy | b5218f53 | 9f6a21c9 | 16.542 | 11 | 11 | 0,665 | 56/317 | 0,177 | — | L | G | L |
| chirpy | 45b8b339 | f551991c | 17.684 | 8 | 8 | 0,452 | 53/300 | 0,177 | — | G | G | G |
| chirpy | c26282dc | 1287c2ae | 18.192 | 5 | 8 | 0,440 | 11/101 | 0,109 | M | G | G | G |
| chirpy | bde49175 | 9c02a42e | 27.394 | 7 | 7 | 0,256 | 10/155 | 0,065 | P+M | G | G | G |
| chirpy | 989c016c | 61a55034 | 7.881 | 8 | 8 | 1,015 | 46/124 | 0,371 | P+M | L | L | L |
| megumii | 51a6c56b | 2c7efc3e | 9.053 | 6 | 9 | 0,994 | 18/75 | 0,240 | — | L | G | L |
| megumii | f2c86d00 | 1d3efb52 | 8.399 | 2 | 2 | 0,238 | 11/141 | 0,078 | M | G | G | G |
| megumii | 6bdaad35 | 60fa9935 | 11.145 | 6 | 23 | 2,064 | 29/132 | 0,220 | M | L | G | L |
| megumii | e5abc76e | 8c9c01f2 | 9.047 | 4 | 12 | 1,326 | 12/43 | 0,279 | M | L | G | L |
| megumii | b754e066 | 1d758352 | 10.062 | 5 | 6 | 0,596 | 7/128 | 0,055 | M | L | G | G |
| megumii | 912de77e | 5869b52e | 14.459 | 7 | 20 | 1,383 | 25/129 | 0,194 | M | L | G | L |
| megumii | 283ae9d5 | 1f58031d | 11.291 | 7 | 10 | 0,886 | 84/179 | 0,469 | — | L | L | L |
| megumii | 53b55fb0 | e20d251f | 10.655 | 12 | 17 | 1,595 | 40/84 | 0,476 | M | L | L | L |
| megumii | 73320834 | d854b19a | 9.844 | 4 | 4 | 0,406 | 9/152 | 0,059 | — | G | G | G |
| megumii | d1fc0957 | c6d213c0 | 8.408 | 4 | 4 | 0,476 | 2/41 | 0,049 | — | G | G | G |
| megumii | b35446b1 | 5b219615 | 10.221 | 7 | 7 | 0,685 | 28/71 | 0,394 | — | L | L | L |
| megumii | f8caf142 | 31072e67 | 7.222 | 4 | 6 | 0,831 | 20/84 | 0,238 | — | L | G | L |
| megumii | b42a0b08 | 38f7d21f | 7.767 | 2 | 10 | 1,287 | 27/85 | 0,318 | M | L | L | L |
| megumii | 0cd580d3 | 37dce0fa | 7.832 | 3 | 3 | 0,383 | 10/27 | 0,370 | — | G | G | G |
| megumii | 18fb1312 | d91de605 | 10.010 | 2 | 2 | 0,200 | 14/52 | 0,269 | M | G | G | G |
| megumii | 8c2782ba | e46c0387 | 8.850 | 9 | 16 | 1,808 | 38/102 | 0,373 | M | L | L | L |
| megumii | a731f092 | e25d35d6 | 10.155 | 3 | 3 | 0,295 | 21/167 | 0,126 | — | G | G | G |
| megumii | 0c0d4c88 | a1389f56 | 9.244 | 4 | 4 | 0,433 | 12/111 | 0,108 | — | G | G | G |
| megumii | e3ee1558 | 1c5f15d2 | 8.770 | 3 | 7 | 0,798 | 20/81 | 0,247 | M | L | G | L |
| megumii | 97184a55 | 356c90fc | 10.540 | 2 | 2 | 0,190 | 7/104 | 0,067 | — | G | G | G |
| megumii | 10372962 | 693c0d6b | 12.683 | 2 | 3 | 0,237 | 9/101 | 0,089 | M | G | G | G |
| megumii | de8a59a7 | cd871256 | 8.923 | 2 | 2 | 0,224 | 12/146 | 0,082 | M | G | G | G |

## Lampiran B — Semua jawaban FALSIFIED agen yang sama (64)

| Agen | ISO | ISR | Kar | URL | Sit | Kepadatan | Terikat | Rasio | K-1 | @0,30 | @0,15 |
|---|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|
| Adam Reinhard | 509b71b7 | 1d758352 | 6.191 | 12 | 12 | 1,938 | 12/26 | 0,462 | L | L | L |
| Discord 1 | 68f65646 | e46c0387 | 37.485 | 16 | 17 | 0,454 | 27/348 | 0,078 | G | G | G |
| Discord 1 | 3755e583 | 59279b57 | 4.549 | 1 | 1 | 0,220 | 2/41 | 0,049 | G | G | G |
| Discord 1 | bfce8ac9 | 356c90fc | 5.040 | 2 | 2 | 0,397 | 7/53 | 0,132 | G | G | G |
| Discord 1 | 98492b48 | 1c5f15d2 | 4.778 | 1 | 1 | 0,209 | 2/28 | 0,071 | G | G | G |
| Discord 1 | 0c555bc0 | f696d1fd | 5.553 | 1 | 1 | 0,180 | 2/29 | 0,069 | G | G | G |
| Discord 1 | c084152a | 25384417 | 5.430 | 1 | 1 | 0,184 | 0/22 | 0,000 | G | G | G |
| Febriyan | a1598c6f | 2c7efc3e | 6.749 | 5 | 14 | 2,074 | 7/13 | 0,538 | L | L | L |
| Febriyan | 38dd66dd | 472b29a0 | 22.364 | 9 | 25 | 1,118 | 21/68 | 0,309 | L | L | L |
| Febriyan | 43a66b31 | f80ac8d3 | 10.305 | 10 | 10 | 0,970 | 21/53 | 0,396 | L | L | L |
| Febriyan | 2c037371 | aa59f63f | 10.389 | 7 | 7 | 0,674 | 20/155 | 0,129 | L | G | G |
| Febriyan | e175194c | e46c0387 | 9.934 | 8 | 14 | 1,409 | 40/106 | 0,377 | L | L | L |
| Febriyan | d06a8638 | d91de605 | 12.198 | 9 | 9 | 0,738 | 11/106 | 0,104 | L | G | G |
| Febriyan | 159184c2 | 1466d58a | 12.395 | 10 | 10 | 0,807 | 58/185 | 0,314 | L | L | L |
| GaBot | 7852a52d | 472b29a0 | 7.993 | 16 | 26 | 3,253 | 18/35 | 0,514 | L | L | L |
| GaBot | d114910b | a1389f56 | 10.138 | 16 | 16 | 1,578 | 52/119 | 0,437 | L | L | L |
| Gufran The Legend | 6c1d0641 | 8aacc7f8 | 4.821 | 1 | 1 | 0,207 | 4/35 | 0,114 | G | G | G |
| Gufran The Legend | a1fe4979 | f6940d0d | 7.056 | 0 | 0 | 0,000 | 0/42 | 0,000 | G | G | G |
| Gufran The Legend | 16d2f444 | d6d8c636 | 8.858 | 1 | 1 | 0,113 | 4/122 | 0,033 | G | G | G |
| Gufran The Legend | 2eef6657 | 42e493d2 | 7.565 | 2 | 2 | 0,264 | 4/138 | 0,029 | G | G | G |
| Gufran The Legend | 20a68c40 | 0a7b338f | 3.586 | 2 | 2 | 0,558 | 4/37 | 0,108 | L | G | G |
| HIMANSHU | 503f8209 | e46c0387 | 955 | 0 | 0 | 0,000 | 0/15 | 0,000 | G | G | G |
| HIMANSHU | b7c9e7c6 | dbd4f6b9 | 5.762 | 0 | 2 | 0,347 | 0/27 | 0,000 | G | G | G |
| HIMANSHU | d11958f8 | 693c0d6b | 4.397 | 5 | 5 | 1,137 | 34/53 | 0,642 | L | L | L |
| HIMANSHU | 7bb1ca5a | e25d35d6 | 5.293 | 0 | 0 | 0,000 | 0/58 | 0,000 | G | G | G |
| HIMANSHU | 0710a02b | a1389f56 | 5.625 | 6 | 6 | 1,067 | 22/38 | 0,579 | L | L | L |
| HIMANSHU | ecf87aed | cd871256 | 6.574 | 0 | 0 | 0,000 | 0/139 | 0,000 | G | G | G |
| HIMANSHU | 2e0b1995 | 970d09db | 1.119 | 2 | 2 | 1,787 | 16/63 | 0,254 | L | G | L |
| HIMANSHU | 370bfa2c | 84fc0b61 | 3.400 | 0 | 0 | 0,000 | 0/38 | 0,000 | G | G | G |
| HIMANSHU | 6f6b9c7d | d76187e8 | 2.542 | 0 | 0 | 0,000 | 0/43 | 0,000 | G | G | G |
| HIMANSHU | afa1d64f | e8364b30 | 2.970 | 0 | 0 | 0,000 | 0/49 | 0,000 | G | G | G |
| HIMANSHU | 7efa71e4 | 1287c2ae | 3.480 | 0 | 2 | 0,575 | 1/37 | 0,027 | G | G | G |
| Mauldrop | 64494279 | f80ac8d3 | 6.245 | 10 | 11 | 1,761 | 17/38 | 0,447 | L | L | L |
| Mauldrop | 78fcaba4 | 79437a33 | 7.357 | 8 | 8 | 1,087 | 18/127 | 0,142 | L | G | G |
| Mauldrop | a7714553 | 0e901710 | 3.086 | 4 | 4 | 1,296 | 10/25 | 0,400 | L | L | L |
| Rodeo | 73e79f3b | bd33b747 | 9.791 | 4 | 4 | 0,409 | 0/47 | 0,000 | G | G | G |
| Rodeo | de29c045 | 9f6a21c9 | 8.476 | 3 | 4 | 0,472 | 2/82 | 0,024 | G | G | G |
| Rodeo | f3dc26c4 | 358e0bce | 6.372 | 10 | 10 | 1,569 | 30/88 | 0,341 | L | L | L |
| SyntaxZ | d65d4ebf | 60fa9935 | 10.121 | 5 | 11 | 1,087 | 16/176 | 0,091 | L | G | G |
| can-earn? | 3101431c | d854b19a | 12.450 | 7 | 7 | 0,562 | 12/113 | 0,106 | L | G | G |
| can-earn? | 1d418559 | d91de605 | 18.433 | 5 | 5 | 0,271 | 17/106 | 0,160 | G | G | G |
| can-earn? | 2eea202f | e46c0387 | 15.505 | 6 | 6 | 0,387 | 21/179 | 0,117 | G | G | G |
| can-earn? | 777cadfb | 1c5f15d2 | 12.203 | 9 | 19 | 1,557 | 48/86 | 0,558 | L | L | L |
| can-earn? | 476a19df | 25384417 | 12.392 | 6 | 6 | 0,484 | 27/52 | 0,519 | G | G | G |
| can-earn? | 7658edb5 | 693c0d6b | 12.099 | 9 | 9 | 0,744 | 37/113 | 0,327 | L | L | L |
| can-earn? | a53a849d | e25d35d6 | 12.762 | 4 | 4 | 0,313 | 11/124 | 0,089 | G | G | G |
| can-earn? | f52e7b13 | e9509814 | 13.752 | 6 | 6 | 0,436 | 18/91 | 0,198 | G | G | G |
| can-earn? | 9a90fad5 | 7d657a7f | 13.235 | 6 | 6 | 0,453 | 6/49 | 0,122 | G | G | G |
| can-earn? | dd3edf2e | 970d09db | 2.447 | 0 | 0 | 0,000 | 0/48 | 0,000 | G | G | G |
| chirpy | 185a18f4 | 21ef1f75 | 20.767 | 13 | 13 | 0,626 | 39/336 | 0,116 | L | G | G |
| chirpy | d31cf3d4 | dbd4f6b9 | 22.331 | 6 | 9 | 0,403 | 11/63 | 0,175 | G | G | G |
| chirpy | c04cdab2 | d91de605 | 23.904 | 6 | 6 | 0,251 | 52/208 | 0,250 | G | G | G |
| chirpy | fc516890 | e46c0387 | 16.555 | 5 | 5 | 0,302 | 27/250 | 0,108 | G | G | G |
| chirpy | 19582b9c | 25384417 | 16.940 | 9 | 9 | 0,531 | 53/122 | 0,434 | L | L | L |
| chirpy | fdcb38c4 | bf7cc34f | 12.373 | 9 | 9 | 0,727 | 35/107 | 0,327 | L | L | L |
| chirpy | a699f24e | cd871256 | 13.557 | 8 | 8 | 0,590 | 39/166 | 0,235 | L | G | L |
| chirpy | e95f6c95 | 693c0d6b | 17.173 | 5 | 5 | 0,291 | 29/156 | 0,186 | G | G | G |
| chirpy | f83a354b | a1389f56 | 14.850 | 8 | 8 | 0,539 | 42/117 | 0,359 | L | L | L |
| chirpy | 48d44c17 | e25d35d6 | 14.293 | 8 | 8 | 0,560 | 33/160 | 0,206 | L | G | L |
| chirpy | 322ab7c6 | e9509814 | 34.877 | 13 | 13 | 0,373 | 46/267 | 0,172 | G | G | G |
| megumii | 6afd47f1 | f80ac8d3 | 11.436 | 5 | 5 | 0,437 | 9/105 | 0,086 | G | G | G |
| megumii | b629d727 | 7cc5c1d5 | 10.621 | 4 | 4 | 0,377 | 9/112 | 0,080 | G | G | G |
| megumii | 53dc364d | f7e02fc3 | 9.377 | 3 | 3 | 0,320 | 9/92 | 0,098 | G | G | G |
| megumii | c1a7740a | 21ef1f75 | 9.460 | 1 | 1 | 0,106 | 3/167 | 0,018 | G | G | G |

---

Catatan reproduksi: agregat dihitung dari `/tmp/champion_corpus_analysis.json` yang dihasilkan skrip analisis sesi ini atas dua artefak belajar di atas dengan `mechanical_floor` wrapper produksi. File korpus ini adalah keluaran bernama yang dipertahankan; skrip sementara tidak dijadikan sumber kebenaran kedua.
