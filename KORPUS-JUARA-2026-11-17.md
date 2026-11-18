# KORPUS JUARA 2026-11-17 — Referensi Resep Kohort Berdiri (12 Agen Inti, 5/5 Snapshot)

> Pasangan `STUDI-KOHORT-2026-11-17.md`. Frame: jawaban milik 12 agen kohort inti (muncul di top-100 pada kelima snapshot: 14 Nov 02:40 · 14 Nov 10:37 · 16 Nov 18:37 · 17 Nov 02:37 · 17 Nov 07:20 WIB; hadir di run-10 & run-11) di dalam 171 pertanyaan sampel run-11 (48 settled pertama + 80 segar sejak 2026-11-16T19:37Z + 48 monitored run-10). **Verified kohort n=377 · falsified kohort n=105.** Ditambah korpus bayar-baru: **71 jawaban verified yang slot Pioneer/Marathon-nya baru settle sejak run-10** (settle = `updatedAt` ≥ 2026-11-16T19:37Z) dari semua agen. Angka banding = `KORPUS-JUARA-2026-11-14.md` (verified panel n=203 / falsified n=64). Pengukuran memakai fungsi yang sama persis dengan gerbang kita (`mechanical_floor` dari wrapper OpenRouter; pola kebaruan QUALITY (e); detektor E3 dari gerbang serve).

## 1. Agregat resep — verified kohort, run-11 vs 14 Nov

| Fitur | Run-11 (n=377) | 14 Nov (n=203) | Geser |
|---|---|---|---|
| Karakter median (q1–q3) | 8.937 (6.122–12.397) | 9.549 | −6% — tetap |
| Pita <3.000 / 3.000–4.499 | 1,1% / 9,0% | — / — | lantai 3.000 QUALITY v3 menampung 98,9% |
| Pita 4.500–8.000 / 8.000–12.000 / >12.000 | 32,6% / 30,5% / 26,8% | — | massa di 4,5–12 rb |
| URL median | 6 | 6,0 | tetap |
| Densitas sitasi median | 0,754 | 0,842 | −10% |
| Rasio sitasi terikat median | 0,189 | 0,212 | −11% |
| Lolos K-1 | 70,6% | 72,4% | tetap |
| Lolos lantai penuh @0,30 | 26,5% | 32,5% | −6,0pp |
| Lolos lantai penuh @0,15 | 53,3% | 57,6% | −4,3pp |
| Bagian (header) median | 7 | — | — |
| Header ada / bernomor | 80,6% / 62,3% | 78,8% / 57,6% | tetap / +4,7pp |
| Sitasi di 1.000 kar pertama | 23,1% | 34,5% | **−11,4pp** |
| Sitasi di kuartil terakhir | 83,3% | 89,7% | −6,4pp |
| Sitasi ≥3 kuartil | 31,6% | 39,9% | −8,3pp |
| Angka terikat di 800 kar terakhir | 76,4% | 84,2% | −7,8pp |
| Proksi pivot kebaruan | 76,7% | 76,8% | tetap |
| Penamaan kebaruan di penutup | 4,0% | 0,5% (ketat) | tetap langka* |
| E3 penutup evasif | 0,0% | 0,0% | tetap nol |
| Penutup memuat sitasi | 80,1% | — (tak diukur) | — |
| Penutup = daftar sumber | 34,7% | — (tak diukur) | — |
| Memuat hedge / hedge di penutup | 61,8% / 13,5% | — | — |
| Heading ketidakpastian | 19,6% | — | — |
| Hedge per 1.000 kar median | 0,122 | — | — |

\* Pengukuran 14 Nov memakai pola ketat QUALITY (e) lama; run-11 memakai pola penanda kebaruan longgar yang sama dengan konteks kebaruan C5 — 4,0% adalah batas atas longgar; kesimpulan "tetap langka" aman di kedua definisi.

**Bacaan**: resep agregat nyaris tidak bergerak dalam 3 hari (semua median bergeser ≤11%). Satu-satunya pergeseran struktural yang layak dicatat: **sitasi makin jarang membuka jawaban** (sitasi di 1.000 karakter pertama 34,5% → 23,1%) dan sebaran sitasi lintas-kuartil menyusut (≥3 kuartil 39,9% → 31,6%) — juara kini lebih sering menumpuk sitasi di badan/penutup daripada menyebar merata. Ini konsisten dengan temuan panel studi (gap sitasi-kuartil-terakhir tetap besar) dan TIDAK mengubah satu pun butir QUALITY v3.

## 2. Daya pisah gerbang di dalam korpus kohort (verified vs falsified kohort sendiri)

| Ukuran | Verified (377) | Falsified (105) | Gap run-11 | Gap 14 Nov (korpus) |
|---|---|---|---|---|
| K-1 | 70,6% | 58,1% | +12,5pp | +28,7pp |
| K-2 saja @0,30 / @0,15 | 27,6% / 59,9% | 27,6% / 47,6% | 0,0 / +12,3pp | +4,8 / +22,8pp |
| Lantai penuh @0,30 | 26,5% | 27,6% | **−1,1pp** | +4,4pp |
| Lantai penuh @0,15 | 53,3% | 42,9% | +10,4pp | +24,8pp |
| Karakter median | 8.937 | 5.848 | d = 0,373 | — |
| Densitas / rasio median | 0,754 / 0,189 | 0,651 / 0,142 | d = 0,132 / 0,175 | — |
| URL≥1 | — | — | +22,5pp | — |
| Header | 80,6% | 75,2% | +5,4pp | — |

**Bacaan jujur**: di dalam kohort inti, falsified mereka adalah jawaban agen kuat yang gagal secara semantik — lantai mekanik kita TIDAK memisahkannya (@0,30 bahkan berbalik −1,1pp). Ini bukan vonis "lantai tak berguna": pada frame lapangan penuh (studi F5) lantai tetap memisah +5,3pp @0,30 / +17,3pp @0,15, dan fungsi lantai adalah membunuh spesies gagal KITA (sitasi tempel, rasio runtuh), bukan meniru kegagalan juara. Konsekuensi workflow: untuk meniru juara, yang ditiru adalah resep §1; untuk tidak mati seperti kita dulu, yang dipakai tetap lantai + C5.

## 3. Per-agen (verified; kolom kanan = angka 14 Nov agen yang sama)

| Agen | nV/nF | Kar | Dens | Rasio | K-1 | @0,30 | @0,15 | Slot (P/M/—) | 14 Nov: kar · dens · rasio · K-1 · @0,30 · @0,15 |
|---|---|---|---|---|---|---|---|---|---|
| Febriyan | 38/9 | 11.846 | 0,821 | 0,206 | 78,9% | 21,1% | 57,9% | 1/10/27 | 11.816 · 0,893 · 0,159 · 70,8% · 20,8% · 50,0% |
| HIMANSHU | 41/11 | 10.592 | 0,595 | 0,111 | 61,0% | 4,9% | 29,3% | 0/19/22 | 6.253 · 1,065 · 0,203 · 84,6% · 15,4% · 61,5% |
| Mauldrop | 42/11 | 5.150 | 1,079 | 0,352 | 81,0% | 57,1% | 78,6% | 3/16/23 | 4.890 · 1,181 · 0,494 · 94,7% · 63,2% · 94,7% |
| Gufran The Legend | 39/20 | 7.921 | 0,894 | 0,189 | 84,6% | 7,7% | 61,5% | 0/19/20 | 4.357 · 0,519 · 0,140 · 52,9% · 11,8% · 29,4% |
| GaBot | 26/4 | 7.310 | 1,228 | 0,437 | 96,2% | 76,9% | 92,3% | 1/13/12 | 8.223 · 1,500 · 0,416 · 88,2% · 58,8% · 76,5% |
| megumii | 41/11 | 9.053 | 0,412 | 0,078 | 41,5% | 7,3% | 22,0% | 1/13/27 | 9.544 · 0,641 · 0,229 · 54,5% · 22,7% · 50,0% |
| Danis | 28/6 | 5.602 | 0,560 | 0,173 | 60,7% | 7,1% | 53,6% | 0/5/23 | di luar panel 14 Nov |
| Adam Reinhard | 28/3 | 10.853 | 4,066 | 0,677 | 100% | 96,4% | 100% | 1/6/21 | 11.499 · 4,425 · 0,790 · 100% · 100% · 100% |
| zoya khan | 28/6 | 13.958 | 0,565 | 0,128 | 53,6% | 14,3% | 25,0% | 0/16/12 | di luar panel 14 Nov |
| SyntaxZ | 20/2 | 11.452 | 0,601 | 0,177 | 55,0% | 15,0% | 40,0% | 0/20/0 | 12.079 · 1,014 · 0,222 · 80,0% · 20,0% · 50,0% |
| kuru | 19/20 | 10.756 | 0,754 | 0,174 | 68,4% | 10,5% | 52,6% | 0/15/4 | di luar panel 14 Nov |
| gisa | 27/2 | 12.454 | 0,632 | 0,133 | 66,7% | 7,4% | 33,3% | 0/15/12 | di luar panel 14 Nov |

Gerakan fenotipe terbesar per agen (3 hari):
- **HIMANSHU berubah spesies**: 6.253 → 10.592 karakter, densitas 1,065 → 0,595, rasio 0,203 → 0,111, lolos @0,15 61,5% → 29,3% — sambil koinnya naik ×5,4 ke #9. Bukti lapangan terkuat saat ini bahwa ada lebih dari satu fenotipe pemenang; resep agregat §1 tetap menjadi acuan, bukan agen tunggal mana pun.
- **megumii melonggar**: rasio 0,229 → 0,078, @0,15 50,0% → 22,0% — tetap #13. Konsisten dengan temuan 14 Nov tentang Febriyan: lantai membunuh spesies gagal kita, bukan hukum universal arena.
- **Gufran bergerak MENUJU resep**: 4.357 → 7.921 karakter, K-1 52,9% → 84,6%, @0,15 29,4% → 61,5%.
- **Adam Reinhard tidak berubah sama sekali** (densitas ±4, rasio 0,677, 96,4% @0,30) — fenotipe ekstrem-sitasi tetap hidup dan dibayar (Marathon 6 + Pioneer 1 di frame ini saja).
- **Mauldrop tetap fenotipe pendek-padat** (±5.150 kar, rasio 0,352, @0,30 57,1%) — yang paling dekat ke templat QUALITY kita di antara kohort.

## 4. Slot di dalam korpus kohort (label dari detail pertanyaan; "—" = tak terbaca, BUKAN bukti bukan-Innovator)

| Slot | n | Kar median | Dens | Rasio | K-1 | @0,30 | @0,15 | 14 Nov (kar · dens · rasio · K-1 · @0,30 · @0,15) |
|---|---|---|---|---|---|---|---|---|
| Pioneer saja | 7 | 4.094 | 1,130 | 0,413 | 85,7% | 71,4% | 85,7% | 32 jawaban: 9.496 · 0,746 · 0,191 · 68,8% · 18,8% · 50,0% |
| Marathon saja | 167 | 10.071 | 0,682 | 0,166 | 67,7% | 22,2% | 46,7% | 103: 8.770 · 1,052 · 0,250 · 80,6% · 37,9% · 67,0% |
| Tak terbaca | 203 | 8.538 | 0,810 | 0,203 | 72,4% | 28,6% | 57,6% | 82: 10.188 · 0,700 · 0,178 · 65,9% · 31,7% · 50,0% |

Pioneer kohort kini PENDEK dan sangat terikat (n kecil = 7; median 4.094 kar, rasio 0,413, sitasi di 1.000 kar pertama 71,4%, tanpa header di 71,4%) — fenotipe "jawab cepat, sitasi rapat, tanpa upacara". Marathon kohort memanjang (10.071 kar) dengan struktur paling berheader (85,0%, bernomor 72,5%).

## 5. Pemenang sel bayar BARU settle sejak run-10 (n=71, semua agen)

Slot: Pioneer 35 · Marathon 30 · P+M 6. Penyebaran: peraih terbanyak hanya 5 (satu uid di luar papan); 44/71 diraih agen di luar top-100 snapshot (nama tak terbaca dari papan) — **sel bayar segar menyebar ke agen kecil**, bukan monopoli kohort.

| Fitur | Pioneer (35) | Marathon (30) | P+M (6) |
|---|---|---|---|
| Karakter median (q1–q3) | 7.410 (2.792–14.047) | 10.499 (5.806–14.719) | 5.760 (4.646–8.017) |
| Pita <3.000 kar | **25,7%** | 3,3% | 0% |
| URL median | 6 | 7,5 | 4,5 |
| Densitas / rasio median | 0,946 / 0,250 | 0,736 / 0,173 | 0,676 / 0,290 |
| K-1 / @0,30 / @0,15 | 71,4% / 42,9% / 57,1% | 70,0% / 13,3% / 53,3% | 50,0% / 16,7% / 50,0% |
| Bagian median · header bernomor | 2 · 28,6% | 8,5 · 63,3% | 0 · 33,3% |
| Sitasi kuartil terakhir | 88,6% | 86,7% | 66,7% |
| Angka terikat 800 kar terakhir | 80,0% | 83,3% | 33,3% |
| Hedge ada / per 1.000 kar | 74,3% / 0,254 | 80,0% / 0,215 | 83,3% / 0,316 |
| Heading ketidakpastian | 17,1% | 36,7% | 0% |

Bacaan: (i) **seperempat Pioneer yang baru dibayar berukuran <3.000 karakter** — di sel Pioneer, kecepatan + kepadatan sitasi mengalahkan panjang (konsisten §4); lantai panjang 3.000 QUALITY v3 adalah lantai DRAF KITA, bukan syarat sel — jangan dibaca terbalik. (ii) Marathon bayar-baru adalah yang paling panjang dan paling terstruktur, dan paling sering membawa heading ketidakpastian (36,7%) — penanganan ketidakpastian yang terlihat (bukan sekadar hedge tersebar) adalah fitur Marathon yang naik. (iii) Gabungan 71: hedge/1.000 kar median 0,241 — lebih tinggi dari korpus kohort (0,122); jawaban yang baru dibayar terdengar lebih terkalibrasi.

## 6. Pola struktural (verified kohort) — tabel banding §6 korpus lama

| Pola | Run-11 | 14 Nov | Vonis |
|---|---|---|---|
| Memuat header | 80,6% | 78,8% | tetap |
| Header bernomor | 62,3% | 57,6% | naik tipis |
| Sitasi di kuartil terakhir | 83,3% | 89,7% | tetap dominan |
| Angka terikat di 800 kar terakhir | 76,4% | 84,2% | tetap dominan |
| Proksi pivot kebaruan | 76,7% | 76,8% | tetap persis |
| Sitasi ≥3 kuartil | 31,6% | 39,9% | turun |
| Sitasi di 1.000 kar pertama | 23,1% | 34,5% | **turun −11,4pp** |
| Penamaan kebaruan di penutup | 4,0% | 0,5%* | tetap langka |
| E3 evasif | 0,0% | 0,0% | tetap nol |
| Penutup = daftar sumber | 34,7% | tak diukur | sepertiga jawaban juara ditutup daftar sumber polos dan tetap verified/dibayar |

\* Definisi pola berbeda (lihat §1) — vonis "langka" berlaku di kedua definisi.

## 7. Akibat buat workflow (semua di dalam keputusan terkunci; bukan perubahan)

- **QUALITY v3 tidak perlu revisi dari data ini**: lantai 3.000 menampung 98,9% resep kohort; (e) hasil reformulasi cocok (penamaan tetap langka, pivot substantif 76,7%); E3 tetap 0% di lapangan. Satu catatan tempel untuk siklus berikutnya: sitasi pembuka makin jarang di resep juara (23,1%) — draf kita tidak dirugikan oleh sitasi awal (gerbang kita tidak menghukumnya), jadi ini CATATAN, bukan usulan ubah.
- **Templat dua fenotipe kini berangka segar**: Pioneer = pendek-padat-cepat (4.094 kar, rasio 0,413) vs Marathon = panjang-terstruktur (10.071–10.499 kar, header bernomor ±2/3, heading ketidakpastian 36,7% pada bayar-baru). Pemilih target (item 1) sudah memisahkan kelasnya; yang bisa disiapkan di fase testing adalah varian templat per kelas — **USULAN berlabel** untuk siklus rancangan berikutnya, bukan eksekusi studi ini.
- **K-2 tetap 0,30** (keputusan user): data run-11 tidak memberi alasan membuka keputusan itu — gap @0,30 stabil, dan kelemahan K-2 ada di dalam-K-1 (isu lama), bukan di pilihan ambang.

## 8. Batas & daftar negatif korpus

- n Pioneer kohort hanya 7 — semua angka §4 kolom Pioneer adalah indikatif, bukan resep final.
- 166/732 slot Marathon awarded menunjuk ISO di luar daftar tertarik → atribusi pemenang Marathon tidak lengkap (22,7% gelap).
- Innovator tetap tidak terukur publik; 203/377 verified kohort berlabel "—".
- Frame campuran (settled lama + segar + monitored) — korpus ini potret resep yang *sedang dibayar*, bukan resep *semua* jawaban kohort; jawaban revealed kohort tidak masuk.
- Rate verdict sejati per-agen tidak diukur ulang run ini (perlu tarikan riwayat pekerjaan per agen; lihat studi F6).


## Lampiran A — Baris per jawaban: verified kohort inti (377)

| Agen | Slot | Kar | URL | Dens | Rasio | K1 | @0,30 | @0,15 | Settle (updatedAt) |
|---|---|---|---|---|---|---|---|---|---|
| Adam Reinhard | — | 19651 | 84 | 4.427 | 0.88 | L | L | L | 2026-11-15T17:46:11.031Z |
| Adam Reinhard | M | 19062 | 62 | 3.357 | 0.562 | L | L | L | 2026-11-03T19:40:05.539Z |
| Adam Reinhard | — | 17267 | 80 | 4.633 | 0.853 | L | L | L | 2026-11-16T17:23:14.673Z |
| Adam Reinhard | M | 17225 | 78 | 4.528 | 0.846 | L | L | L | 2026-11-15T04:52:34.120Z |
| Adam Reinhard | — | 16473 | 77 | 4.674 | 0.75 | L | L | L | 2026-11-16T23:59:28.987Z |
| Adam Reinhard | M | 15897 | 71 | 4.592 | 0.686 | L | L | L | 2026-11-15T08:05:01.270Z |
| Adam Reinhard | — | 15658 | 97 | 6.259 | 0.797 | L | L | L | 2026-11-13T07:04:32.903Z |
| Adam Reinhard | — | 13746 | 70 | 5.165 | 0.864 | L | L | L | 2026-11-11T20:35:07.070Z |
| Adam Reinhard | — | 12792 | 42 | 3.283 | 0.569 | L | L | L | 2026-11-13T10:28:02.929Z |
| Adam Reinhard | — | 12789 | 40 | 3.362 | 0.667 | L | L | L | 2026-11-12T02:46:59.866Z |
| Adam Reinhard | — | 12652 | 53 | 4.189 | 0.521 | L | L | L | 2026-11-16T17:45:13.985Z |
| Adam Reinhard | — | 11899 | 46 | 3.866 | 0.643 | L | L | L | 2026-11-16T17:40:39.803Z |
| Adam Reinhard | — | 11812 | 55 | 4.656 | 0.781 | L | L | L | 2026-11-11T20:37:33.529Z |
| Adam Reinhard | — | 11465 | 35 | 3.227 | 0.875 | L | L | L | 2026-11-12T05:15:00.247Z |
| Adam Reinhard | — | 10241 | 10 | 0.976 | 0.381 | L | L | L | 2026-11-11T10:55:52.429Z |
| Adam Reinhard | — | 10026 | 55 | 5.486 | 0.583 | L | L | L | 2026-11-11T10:58:50.625Z |
| Adam Reinhard | — | 9362 | 7 | 0.748 | 0.395 | L | L | L | 2026-11-13T02:33:52.427Z |
| Adam Reinhard | — | 9217 | 13 | 1.736 | 0.667 | L | L | L | 2026-11-11T08:10:42.660Z |
| Adam Reinhard | — | 9103 | 44 | 4.834 | 0.838 | L | L | L | 2026-11-15T08:34:39.299Z |
| Adam Reinhard | M | 8848 | 35 | 4.408 | 0.833 | L | L | L | 2026-11-08T11:02:50.958Z |
| Adam Reinhard | — | 8643 | 17 | 2.43 | 0.412 | L | L | L | 2026-11-14T18:02:29.696Z |
| Adam Reinhard | — | 8538 | 21 | 2.46 | 0.636 | L | L | L | 2026-11-11T11:48:19.051Z |
| Adam Reinhard | M | 7981 | 47 | 5.889 | 0.814 | L | L | L | 2026-11-15T07:24:27.925Z |
| Adam Reinhard | M | 7765 | 13 | 3.091 | 0.837 | L | L | L | 2026-11-10T05:50:45.775Z |
| Adam Reinhard | — | 7355 | 29 | 3.943 | 0.594 | L | L | L | 2026-11-16T22:29:35.505Z |
| Adam Reinhard | — | 7353 | 6 | 0.816 | 0.182 | L | G | L | 2026-11-16T03:54:47.393Z |
| Adam Reinhard | P | 7297 | 11 | 1.507 | 0.448 | L | L | L | 2026-11-16T10:06:14.704Z |
| Adam Reinhard | — | 5696 | 29 | 5.091 | 0.974 | L | L | L | 2026-11-13T10:49:24.849Z |
| Danis | — | 8937 | 7 | 0.783 | 0.203 | L | G | L | 2026-11-16T17:41:28.967Z |
| Danis | M | 8040 | 3 | 0.498 | 0.057 | G | G | G | 2026-11-15T08:49:18.191Z |
| Danis | — | 7834 | 5 | 0.638 | 0.272 | L | G | L | 2026-11-15T15:16:34.113Z |
| Danis | — | 7463 | 5 | 1.072 | 0.55 | L | L | L | 2026-11-15T17:48:36.038Z |
| Danis | — | 7443 | 2 | 0.269 | 0.057 | G | G | G | 2026-11-13T06:56:08.040Z |
| Danis | — | 7166 | 6 | 0.837 | 0.28 | L | G | L | 2026-11-16T10:21:59.709Z |
| Danis | — | 7154 | 4 | 0.559 | 0.1 | L | G | G | 2026-11-16T04:22:02.878Z |
| Danis | — | 6289 | 2 | 0.477 | 0.111 | G | G | G | 2026-11-15T02:00:39.284Z |
| Danis | — | 6157 | 3 | 0.487 | 0.186 | G | G | G | 2026-11-16T09:13:04.057Z |
| Danis | — | 6016 | 4 | 0.665 | 0.171 | L | G | L | 2026-11-16T12:48:26.563Z |
| Danis | — | 5814 | 3 | 0.516 | 0.4 | L | L | L | 2026-11-16T11:23:12.953Z |
| Danis | — | 5745 | 2 | 0.348 | 0.407 | G | G | G | 2026-11-16T12:59:17.763Z |
| Danis | — | 5647 | 4 | 0.708 | 0.175 | L | G | L | 2026-11-16T11:49:30.302Z |
| Danis | — | 5604 | 4 | 0.714 | 0.298 | L | G | L | 2026-11-16T14:26:16.914Z |
| Danis | M | 5600 | 2 | 0.357 | 0.063 | G | G | G | 2026-11-14T12:20:19.586Z |
| Danis | — | 5498 | 3 | 0.546 | 0.287 | L | G | L | 2026-11-17T00:32:37.434Z |
| Danis | — | 5360 | 3 | 0.56 | 0.17 | L | G | L | 2026-11-16T12:19:01.133Z |
| Danis | — | 5298 | 4 | 0.755 | 0.189 | L | G | L | 2026-11-16T13:28:12.284Z |
| Danis | — | 4780 | 4 | 0.837 | 0.233 | L | G | L | 2026-11-16T15:16:23.117Z |
| Danis | M | 4700 | 4 | 0.851 | 0.165 | L | G | L | 2026-11-15T12:37:11.079Z |
| Danis | — | 4693 | 2 | 0.426 | 0.111 | G | G | G | 2026-11-15T08:40:31.159Z |
| Danis | — | 4654 | 4 | 0.859 | 0.28 | L | G | L | 2026-11-15T08:37:48.654Z |
| Danis | — | 4647 | 2 | 0.43 | 0.095 | G | G | G | 2026-11-13T02:34:22.417Z |
| Danis | — | 4440 | 4 | 0.901 | 0.237 | L | G | L | 2026-11-15T01:12:33.021Z |
| Danis | — | 4366 | 3 | 0.687 | 0.106 | L | G | G | 2026-11-16T04:00:30.076Z |
| Danis | M | 4247 | 2 | 0.471 | 0.078 | G | G | G | 2026-11-15T08:48:48.039Z |
| Danis | M | 4047 | 1 | 0.247 | 0.027 | G | G | G | 2026-11-13T08:26:10.408Z |
| Danis | — | 3874 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T06:04:37.966Z |
| Febriyan | M | 21443 | 18 | 0.839 | 0.259 | L | G | L | 2026-11-12T15:34:33.807Z |
| Febriyan | — | 19396 | 8 | 0.412 | 0.051 | G | G | G | 2026-11-13T07:00:34.532Z |
| Febriyan | M | 19101 | 14 | 0.995 | 0.37 | L | L | L | 2026-11-12T15:33:02.692Z |
| Febriyan | — | 18076 | 15 | 0.83 | 0.205 | L | G | L | 2026-11-16T10:12:19.738Z |
| Febriyan | — | 17968 | 12 | 0.946 | 0.245 | L | G | L | 2026-11-15T17:44:01.036Z |
| Febriyan | — | 17037 | 10 | 0.587 | 0.116 | L | G | G | 2026-11-16T14:24:07.156Z |
| Febriyan | — | 17019 | 11 | 0.764 | 0.252 | L | G | L | 2026-11-16T13:42:59.565Z |
| Febriyan | — | 16328 | 12 | 0.796 | 0.328 | L | L | L | 2026-11-12T10:18:20.768Z |
| Febriyan | M | 15519 | 13 | 0.967 | 0.156 | L | G | L | 2026-11-10T16:50:52.033Z |
| Febriyan | — | 15229 | 11 | 0.722 | 0.097 | L | G | G | 2026-11-16T22:16:25.499Z |
| Febriyan | M | 15111 | 3 | 0.331 | 0.027 | G | G | G | 2026-11-12T16:02:03.828Z |
| Febriyan | P | 14591 | 6 | 0.959 | 0.413 | L | L | L | 2026-11-16T23:42:26.143Z |
| Febriyan | M | 13776 | 9 | 0.653 | 0.088 | L | G | G | 2026-11-12T15:43:38.539Z |
| Febriyan | — | 13505 | 15 | 1.925 | 0.354 | L | L | L | 2026-11-12T05:17:34.121Z |
| Febriyan | — | 13022 | 14 | 1.075 | 0.144 | L | G | G | 2026-11-13T02:32:47.422Z |
| Febriyan | M | 12930 | 7 | 0.541 | 0.081 | L | G | G | 2026-11-14T18:51:09.234Z |
| Febriyan | M | 12700 | 7 | 0.551 | 0.257 | L | G | L | 2026-11-12T16:19:50.238Z |
| Febriyan | — | 12413 | 2 | 0.161 | 0.216 | G | G | G | 2026-11-08T13:31:22.407Z |
| Febriyan | — | 12191 | 4 | 0.492 | 0.1 | G | G | G | 2026-11-13T10:27:43.052Z |
| Febriyan | — | 11500 | 8 | 1.304 | 0.262 | L | G | L | 2026-11-11T20:35:42.619Z |
| Febriyan | — | 11487 | 20 | 2.699 | 0.413 | L | L | L | 2026-11-12T02:45:45.007Z |
| Febriyan | — | 11074 | 11 | 0.993 | 0.325 | L | L | L | 2026-11-13T11:40:55.805Z |
| Febriyan | — | 11041 | 10 | 0.996 | 0.125 | L | G | G | 2026-11-13T08:59:40.281Z |
| Febriyan | M | 10500 | 8 | 3.048 | 0.604 | L | L | L | 2026-11-10T13:49:42.063Z |
| Febriyan | — | 10240 | 8 | 1.758 | 0.258 | L | G | L | 2026-11-16T14:47:53.986Z |
| Febriyan | M | 10071 | 5 | 0.496 | 0.14 | G | G | G | 2026-11-12T16:09:45.841Z |
| Febriyan | — | 9924 | 14 | 1.411 | 0.138 | L | G | G | 2026-11-17T00:27:32.431Z |
| Febriyan | — | 9610 | 15 | 1.561 | 0.141 | L | G | G | 2026-11-14T14:37:20.045Z |
| Febriyan | — | 8896 | 8 | 0.899 | 0.413 | L | L | L | 2026-11-13T10:49:39.763Z |
| Febriyan | — | 7729 | 2 | 0.259 | 0.086 | G | G | G | 2026-11-11T10:54:42.677Z |
| Febriyan | — | 7680 | 7 | 0.911 | 0.174 | L | G | L | 2026-11-15T08:37:48.115Z |
| Febriyan | — | 7410 | 6 | 0.81 | 0.219 | L | G | L | 2026-11-15T01:11:47.941Z |
| Febriyan | — | 7103 | 2 | 0.282 | 0.057 | G | G | G | 2026-11-11T11:46:59.000Z |
| Febriyan | — | 6151 | 5 | 0.813 | 0.211 | L | G | L | 2026-11-15T08:37:53.540Z |
| Febriyan | — | 5709 | 4 | 0.701 | 0.207 | L | G | L | 2026-11-15T08:40:15.901Z |
| Febriyan | — | 5666 | 1 | 0.176 | 0.061 | G | G | G | 2026-11-11T10:57:20.494Z |
| Febriyan | M | 3792 | 3 | 0.791 | 0.2 | L | G | L | 2026-11-15T04:09:22.117Z |
| Febriyan | — | 3169 | 3 | 0.947 | 0.239 | L | G | L | 2026-11-14T19:20:46.242Z |
| GaBot | — | 13252 | 22 | 1.66 | 0.487 | L | L | L | 2026-11-14T14:42:01.487Z |
| GaBot | M | 10866 | 17 | 1.565 | 0.571 | L | L | L | 2026-11-16T16:00:57.609Z |
| GaBot | M | 10716 | 8 | 0.84 | 0.119 | L | G | G | 2026-11-15T15:31:41.340Z |
| GaBot | — | 9917 | 20 | 2.42 | 0.627 | L | L | L | 2026-11-15T17:55:16.033Z |
| GaBot | — | 9734 | 15 | 1.541 | 0.19 | L | G | L | 2026-11-11T11:00:52.459Z |
| GaBot | — | 9661 | 16 | 1.656 | 0.699 | L | L | L | 2026-11-12T10:20:08.681Z |
| GaBot | M | 8881 | 9 | 1.013 | 0.289 | L | G | L | 2026-11-11T21:22:10.705Z |
| GaBot | — | 8652 | 8 | 1.387 | 0.634 | L | L | L | 2026-11-14T18:00:44.700Z |
| GaBot | M | 8414 | 5 | 0.594 | 0.168 | L | G | L | 2026-11-11T16:13:45.620Z |
| GaBot | — | 8255 | 8 | 0.969 | 0.417 | L | L | L | 2026-11-16T12:05:10.329Z |
| GaBot | M | 7938 | 8 | 1.008 | 0.377 | L | L | L | 2026-11-15T01:25:26.487Z |
| GaBot | — | 7357 | 7 | 0.951 | 0.281 | L | G | L | 2026-11-15T15:18:19.032Z |
| GaBot | M | 7319 | 5 | 4.236 | 0.779 | L | L | L | 2026-11-11T07:57:20.540Z |
| GaBot | M | 7301 | 8 | 1.096 | 0.686 | L | L | L | 2026-11-12T06:53:18.200Z |
| GaBot | M | 7290 | 13 | 1.92 | 0.688 | L | L | L | 2026-11-12T06:39:01.914Z |
| GaBot | — | 6773 | 9 | 1.329 | 0.312 | L | L | L | 2026-11-16T17:55:38.986Z |
| GaBot | M | 6489 | 6 | 0.925 | 0.344 | L | L | L | 2026-11-15T17:10:59.699Z |
| GaBot | M | 6299 | 10 | 1.588 | 0.457 | L | L | L | 2026-11-11T11:42:26.352Z |
| GaBot | — | 6220 | 15 | 2.412 | 0.639 | L | L | L | 2026-11-16T22:36:55.492Z |
| GaBot | — | 6055 | 7 | 1.156 | 0.54 | L | L | L | 2026-11-16T18:05:29.958Z |
| GaBot | M | 5988 | 8 | 1.336 | 0.406 | L | L | L | 2026-11-11T08:27:55.068Z |
| GaBot | M | 5845 | 7 | 1.198 | 0.333 | L | L | L | 2026-11-11T08:02:10.884Z |
| GaBot | M | 5561 | 7 | 1.259 | 0.5 | L | L | L | 2026-11-16T15:56:50.370Z |
| GaBot | — | 4516 | 4 | 0.886 | 0.403 | L | L | L | 2026-11-15T08:31:29.769Z |
| GaBot | — | 3820 | 1 | 0.262 | 0.118 | G | G | G | 2026-11-11T11:52:50.326Z |
| GaBot | P | 3539 | 4 | 1.13 | 0.525 | L | L | L | 2026-11-16T16:29:39.109Z |
| Gufran The Legend | M | 17584 | 10 | 0.569 | 0.141 | L | G | G | 2026-11-15T02:54:33.008Z |
| Gufran The Legend | M | 13028 | 10 | 0.768 | 0.107 | L | G | G | 2026-11-15T14:58:07.028Z |
| Gufran The Legend | — | 12112 | 10 | 0.826 | 0.202 | L | G | L | 2026-11-16T11:14:47.957Z |
| Gufran The Legend | — | 11133 | 10 | 0.898 | 0.194 | L | G | L | 2026-11-16T04:21:47.445Z |
| Gufran The Legend | M | 10894 | 10 | 0.918 | 0.2 | L | G | L | 2026-11-15T14:48:59.293Z |
| Gufran The Legend | M | 10585 | 10 | 0.945 | 0.129 | L | G | G | 2026-11-15T07:28:38.203Z |
| Gufran The Legend | — | 10240 | 9 | 0.879 | 0.165 | L | G | L | 2026-11-16T12:17:06.123Z |
| Gufran The Legend | — | 10231 | 9 | 0.88 | 0.21 | L | G | L | 2026-11-16T17:19:34.714Z |
| Gufran The Legend | — | 9924 | 10 | 1.008 | 0.292 | L | G | L | 2026-11-16T10:20:34.713Z |
| Gufran The Legend | M | 9713 | 6 | 0.618 | 0.148 | L | G | G | 2026-11-15T14:51:40.108Z |
| Gufran The Legend | M | 9495 | 10 | 1.053 | 0.25 | L | G | L | 2026-11-15T02:09:37.838Z |
| Gufran The Legend | M | 8857 | 4 | 0.452 | 0.113 | G | G | G | 2026-11-15T15:00:45.678Z |
| Gufran The Legend | — | 8667 | 10 | 1.154 | 0.378 | L | L | L | 2026-11-16T14:25:41.883Z |
| Gufran The Legend | — | 8445 | 10 | 1.184 | 0.219 | L | G | L | 2026-11-16T15:16:02.579Z |
| Gufran The Legend | M | 8333 | 4 | 0.48 | 0.103 | G | G | G | 2026-11-15T02:35:30.482Z |
| Gufran The Legend | — | 8223 | 10 | 1.216 | 0.206 | L | G | L | 2026-11-15T12:27:25.010Z |
| Gufran The Legend | — | 8071 | 6 | 0.743 | 0.0 | L | G | G | 2026-11-11T10:55:57.463Z |
| Gufran The Legend | M | 8059 | 10 | 1.241 | 0.346 | L | L | L | 2026-11-15T14:42:18.772Z |
| Gufran The Legend | — | 8056 | 10 | 1.241 | 0.189 | L | G | L | 2026-11-16T22:19:35.498Z |
| Gufran The Legend | — | 7921 | 9 | 1.136 | 0.253 | L | G | L | 2026-11-16T13:27:42.154Z |
| Gufran The Legend | M | 7775 | 10 | 1.286 | 0.25 | L | G | L | 2026-11-15T14:54:41.384Z |
| Gufran The Legend | M | 7591 | 1 | 0.132 | 0.036 | G | G | G | 2026-11-12T16:32:54.042Z |
| Gufran The Legend | — | 7557 | 10 | 1.323 | 0.201 | L | G | L | 2026-11-16T17:41:13.994Z |
| Gufran The Legend | — | 6628 | 2 | 0.604 | 0.134 | L | G | G | 2026-11-13T09:04:13.941Z |
| Gufran The Legend | — | 6232 | 5 | 0.802 | 0.105 | L | G | G | 2026-11-13T10:26:12.971Z |
| Gufran The Legend | M | 6187 | 5 | 0.97 | 0.118 | L | G | G | 2026-11-14T14:14:28.807Z |
| Gufran The Legend | — | 6169 | 4 | 0.811 | 0.156 | L | G | L | 2026-11-15T08:30:54.363Z |
| Gufran The Legend | M | 6162 | 5 | 0.974 | 0.091 | L | G | G | 2026-11-12T20:52:37.045Z |
| Gufran The Legend | M | 5970 | 4 | 1.005 | 0.179 | L | G | L | 2026-11-13T02:16:30.701Z |
| Gufran The Legend | M | 5963 | 9 | 2.348 | 0.394 | L | L | L | 2026-11-16T10:13:08.068Z |
| Gufran The Legend | — | 5892 | 6 | 1.018 | 0.286 | L | G | L | 2026-11-16T11:46:45.318Z |
| Gufran The Legend | — | 5854 | 5 | 0.854 | 0.295 | L | G | L | 2026-11-16T17:39:19.783Z |
| Gufran The Legend | M | 5595 | 5 | 0.894 | 0.25 | L | G | L | 2026-11-12T17:11:52.607Z |
| Gufran The Legend | — | 5164 | 3 | 0.581 | 0.167 | L | G | L | 2026-11-16T12:58:27.754Z |
| Gufran The Legend | M | 5070 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-12T14:47:25.339Z |
| Gufran The Legend | — | 4663 | 2 | 0.429 | 0.094 | G | G | G | 2026-11-15T01:10:33.105Z |
| Gufran The Legend | M | 4624 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-12T17:10:02.334Z |
| Gufran The Legend | M | 4624 | 3 | 0.649 | 0.292 | L | G | L | 2026-11-13T10:48:13.275Z |
| Gufran The Legend | — | 3304 | 3 | 0.908 | 0.227 | L | G | L | 2026-11-13T10:49:09.801Z |
| HIMANSHU | M | 21964 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T12:04:01.180Z |
| HIMANSHU | — | 18992 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T10:39:49.722Z |
| HIMANSHU | — | 16946 | 4 | 0.236 | 0.036 | G | G | G | 2026-11-16T12:55:41.558Z |
| HIMANSHU | — | 15926 | 8 | 0.502 | 0.247 | L | G | L | 2026-11-16T12:27:06.138Z |
| HIMANSHU | M | 15846 | 13 | 0.82 | 0.282 | L | G | L | 2026-11-12T01:32:42.140Z |
| HIMANSHU | — | 15351 | 11 | 0.717 | 0.11 | L | G | G | 2026-11-16T22:30:22.158Z |
| HIMANSHU | M | 14783 | 6 | 0.406 | 0.227 | G | G | G | 2026-11-16T04:12:54.550Z |
| HIMANSHU | — | 14119 | 13 | 0.921 | 0.243 | L | G | L | 2026-11-16T12:20:55.327Z |
| HIMANSHU | M | 14080 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T13:41:24.040Z |
| HIMANSHU | — | 13697 | 14 | 1.022 | 0.211 | L | G | L | 2026-11-16T17:58:28.995Z |
| HIMANSHU | — | 13632 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T17:52:44.762Z |
| HIMANSHU | — | 13420 | 7 | 0.522 | 0.085 | L | G | G | 2026-11-16T15:18:07.787Z |
| HIMANSHU | M | 13246 | 10 | 1.132 | 0.18 | L | G | L | 2026-11-16T14:28:10.575Z |
| HIMANSHU | M | 12901 | 9 | 0.698 | 0.136 | L | G | G | 2026-11-16T13:02:41.794Z |
| HIMANSHU | — | 12397 | 12 | 0.968 | 0.075 | L | G | G | 2026-11-16T23:54:53.821Z |
| HIMANSHU | M | 12104 | 6 | 0.578 | 0.103 | L | G | G | 2026-11-16T02:03:11.352Z |
| HIMANSHU | M | 11116 | 8 | 0.72 | 0.121 | L | G | G | 2026-11-15T18:55:25.839Z |
| HIMANSHU | M | 11063 | 11 | 0.994 | 0.171 | L | G | L | 2026-11-16T13:46:45.514Z |
| HIMANSHU | — | 10919 | 6 | 0.55 | 0.073 | L | G | G | 2026-11-16T04:03:35.070Z |
| HIMANSHU | — | 10836 | 5 | 0.461 | 0.091 | G | G | G | 2026-11-12T00:31:28.583Z |
| HIMANSHU | — | 10592 | 7 | 0.661 | 0.236 | L | G | L | 2026-11-16T14:28:51.881Z |
| HIMANSHU | — | 10526 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T17:55:58.980Z |
| HIMANSHU | M | 10475 | 6 | 0.668 | 0.218 | L | G | L | 2026-11-16T22:55:20.540Z |
| HIMANSHU | M | 8856 | 7 | 0.79 | 0.06 | L | G | G | 2026-11-12T19:13:55.315Z |
| HIMANSHU | — | 8665 | 7 | 0.808 | 0.0 | L | G | G | 2026-11-11T10:56:52.519Z |
| HIMANSHU | — | 8267 | 5 | 0.605 | 0.145 | L | G | G | 2026-11-15T17:16:36.066Z |
| HIMANSHU | — | 8172 | 5 | 0.612 | 0.385 | L | L | L | 2026-11-12T10:18:13.225Z |
| HIMANSHU | M | 7161 | 2 | 0.279 | 0.101 | G | G | G | 2026-11-15T08:46:58.033Z |
| HIMANSHU | — | 7044 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T08:37:23.031Z |
| HIMANSHU | M | 6914 | 4 | 1.446 | 0.5 | L | L | L | 2026-11-12T19:07:22.923Z |
| HIMANSHU | M | 6609 | 5 | 0.757 | 0.057 | L | G | G | 2026-11-11T17:22:19.271Z |
| HIMANSHU | M | 6253 | 5 | 1.439 | 0.111 | L | G | G | 2026-11-13T02:15:58.087Z |
| HIMANSHU | M | 6230 | 6 | 2.087 | 0.273 | L | G | L | 2026-11-12T18:53:03.610Z |
| HIMANSHU | — | 6194 | 2 | 0.323 | 0.058 | G | G | G | 2026-11-11T11:07:55.510Z |
| HIMANSHU | — | 6122 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T08:30:48.452Z |
| HIMANSHU | — | 5551 | 3 | 1.081 | 0.25 | L | G | L | 2026-11-12T05:55:58.826Z |
| HIMANSHU | — | 5466 | 2 | 0.366 | 0.15 | G | G | G | 2026-11-11T11:46:23.988Z |
| HIMANSHU | M | 5044 | 3 | 0.595 | 0.12 | L | G | G | 2026-11-11T15:03:23.718Z |
| HIMANSHU | — | 4748 | 1 | 0.421 | 0.118 | G | G | G | 2026-11-11T15:52:49.017Z |
| HIMANSHU | M | 4326 | 2 | 0.462 | 0.157 | G | G | G | 2026-11-13T03:01:12.152Z |
| HIMANSHU | M | 4285 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T05:28:40.180Z |
| Mauldrop | — | 9435 | 8 | 0.848 | 0.341 | L | L | L | 2026-11-12T10:17:14.192Z |
| Mauldrop | — | 8667 | 18 | 2.077 | 0.412 | L | L | L | 2026-11-11T20:35:22.941Z |
| Mauldrop | M | 8090 | 2 | 0.247 | 0.131 | G | G | G | 2026-11-15T07:06:37.550Z |
| Mauldrop | — | 7988 | 5 | 0.751 | 0.151 | L | G | L | 2026-11-11T10:57:52.698Z |
| Mauldrop | — | 7717 | 5 | 0.648 | 0.213 | L | G | L | 2026-11-12T04:18:14.517Z |
| Mauldrop | M | 7472 | 4 | 0.535 | 0.194 | L | G | L | 2026-11-11T17:51:28.052Z |
| Mauldrop | — | 7471 | 4 | 1.205 | 0.44 | L | L | L | 2026-11-12T02:51:49.882Z |
| Mauldrop | — | 7115 | 11 | 1.546 | 0.55 | L | L | L | 2026-11-11T11:55:09.108Z |
| Mauldrop | M | 7060 | 12 | 1.7 | 0.459 | L | L | L | 2026-11-11T12:00:03.897Z |
| Mauldrop | M | 6772 | 7 | 1.181 | 0.611 | L | L | L | 2026-11-11T05:24:58.697Z |
| Mauldrop | — | 6454 | 7 | 1.859 | 0.612 | L | L | L | 2026-11-15T17:42:41.149Z |
| Mauldrop | — | 6316 | 8 | 1.267 | 0.483 | L | L | L | 2026-11-16T11:13:33.276Z |
| Mauldrop | — | 6241 | 11 | 1.763 | 0.533 | L | L | L | 2026-11-16T10:10:34.720Z |
| Mauldrop | — | 6213 | 2 | 0.322 | 0.034 | G | G | G | 2026-11-17T00:24:32.455Z |
| Mauldrop | M | 5926 | 1 | 0.169 | 0.019 | G | G | G | 2026-11-15T01:04:06.754Z |
| Mauldrop | M | 5574 | 7 | 1.256 | 0.351 | L | L | L | 2026-11-15T13:34:15.447Z |
| Mauldrop | M | 5505 | 4 | 0.727 | 0.294 | L | G | L | 2026-11-15T12:39:46.630Z |
| Mauldrop | — | 5484 | 6 | 1.094 | 0.6 | L | L | L | 2026-11-11T07:46:25.399Z |
| Mauldrop | M | 5339 | 6 | 1.124 | 0.373 | L | L | L | 2026-11-15T06:45:27.084Z |
| Mauldrop | M | 5316 | 2 | 0.376 | 0.085 | G | G | G | 2026-11-15T06:31:45.717Z |
| Mauldrop | M | 5193 | 6 | 1.348 | 0.273 | L | G | L | 2026-11-15T12:15:54.241Z |
| Mauldrop | M | 5108 | 2 | 0.392 | 0.077 | G | G | G | 2026-11-15T06:23:22.132Z |
| Mauldrop | — | 4876 | 4 | 0.82 | 0.216 | L | G | L | 2026-11-16T12:15:31.134Z |
| Mauldrop | — | 4660 | 9 | 2.575 | 0.956 | L | L | L | 2026-11-12T05:55:12.980Z |
| Mauldrop | M | 4657 | 5 | 1.074 | 0.354 | L | L | L | 2026-11-14T15:20:31.460Z |
| Mauldrop | M | 4381 | 6 | 1.37 | 0.624 | L | L | L | 2026-11-15T03:22:59.016Z |
| Mauldrop | M | 4266 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T06:16:11.284Z |
| Mauldrop | — | 4170 | 4 | 1.199 | 0.389 | L | L | L | 2026-11-16T17:18:24.536Z |
| Mauldrop | M | 4116 | 2 | 0.486 | 0.233 | G | G | G | 2026-11-15T12:51:19.255Z |
| Mauldrop | P | 4094 | 4 | 0.977 | 0.326 | L | L | L | 2026-11-11T18:25:18.593Z |
| Mauldrop | — | 3960 | 1 | 0.253 | 0.146 | G | G | G | 2026-11-17T00:44:54.778Z |
| Mauldrop | — | 3912 | 5 | 1.278 | 0.595 | L | L | L | 2026-11-13T07:07:46.158Z |
| Mauldrop | — | 3845 | 4 | 1.04 | 0.108 | L | G | G | 2026-11-13T09:07:16.079Z |
| Mauldrop | — | 3828 | 3 | 0.784 | 0.412 | L | L | L | 2026-11-16T11:33:30.304Z |
| Mauldrop | — | 3789 | 3 | 0.792 | 0.393 | L | L | L | 2026-11-16T12:58:07.903Z |
| Mauldrop | M | 3693 | 4 | 1.083 | 0.214 | L | G | L | 2026-11-13T20:41:57.877Z |
| Mauldrop | P | 3435 | 11 | 3.202 | 0.818 | L | L | L | 2026-11-15T12:27:05.008Z |
| Mauldrop | — | 3300 | 2 | 0.606 | 0.375 | L | L | L | 2026-11-15T02:00:34.036Z |
| Mauldrop | — | 3202 | 5 | 1.562 | 0.66 | L | L | L | 2026-11-15T08:37:53.026Z |
| Mauldrop | — | 2738 | 6 | 2.191 | 0.571 | L | L | L | 2026-11-13T10:49:24.962Z |
| Mauldrop | P | 2558 | 3 | 1.173 | 0.288 | L | G | L | 2026-11-14T19:20:06.326Z |
| Mauldrop | — | 2266 | 2 | 0.883 | 0.227 | L | G | L | 2026-11-16T15:14:57.541Z |
| SyntaxZ | M | 19529 | 10 | 0.512 | 0.108 | L | G | G | 2026-11-13T07:04:34.090Z |
| SyntaxZ | M | 17752 | 8 | 0.451 | 0.149 | G | G | G | 2026-11-14T11:36:32.351Z |
| SyntaxZ | M | 17251 | 13 | 0.927 | 0.285 | L | G | L | 2026-11-13T05:43:40.049Z |
| SyntaxZ | M | 14998 | 9 | 0.6 | 0.222 | L | G | L | 2026-11-15T06:35:20.733Z |
| SyntaxZ | M | 14981 | 6 | 0.401 | 0.178 | G | G | G | 2026-11-15T02:27:58.896Z |
| SyntaxZ | M | 14188 | 9 | 0.634 | 0.358 | L | L | L | 2026-11-15T06:39:50.964Z |
| SyntaxZ | M | 13018 | 4 | 0.307 | 0.09 | G | G | G | 2026-11-13T11:04:20.296Z |
| SyntaxZ | M | 12524 | 5 | 0.399 | 0.387 | G | G | G | 2026-11-15T17:25:22.456Z |
| SyntaxZ | M | 12311 | 12 | 0.975 | 0.156 | L | G | L | 2026-11-13T04:31:10.395Z |
| SyntaxZ | M | 11756 | 0 | 0.681 | 0.443 | G | G | G | 2026-11-13T10:34:50.092Z |
| SyntaxZ | M | 11149 | 0 | 0.538 | 0.084 | G | G | G | 2026-11-16T16:35:26.368Z |
| SyntaxZ | M | 10862 | 18 | 1.657 | 0.492 | L | L | L | 2026-11-13T13:15:50.788Z |
| SyntaxZ | M | 9777 | 6 | 0.614 | 0.24 | L | G | L | 2026-11-13T03:05:33.993Z |
| SyntaxZ | M | 9749 | 7 | 0.718 | 0.049 | L | G | G | 2026-11-14T18:34:44.522Z |
| SyntaxZ | M | 9507 | 10 | 1.052 | 0.149 | L | G | G | 2026-11-13T10:25:07.319Z |
| SyntaxZ | M | 9253 | 4 | 0.432 | 0.2 | G | G | G | 2026-11-16T18:33:31.190Z |
| SyntaxZ | M | 7972 | 7 | 1.882 | 0.435 | L | L | L | 2026-11-13T03:39:24.543Z |
| SyntaxZ | M | 6647 | 4 | 0.602 | 0.177 | L | G | L | 2026-11-16T19:02:13.226Z |
| SyntaxZ | M | 4669 | 2 | 0.428 | 0.093 | G | G | G | 2026-11-16T16:43:18.439Z |
| SyntaxZ | M | 4603 | 2 | 0.434 | 0.015 | G | G | G | 2026-11-16T14:02:24.748Z |
| gisa | M | 22999 | 16 | 0.696 | 0.193 | L | G | L | 2026-11-13T02:15:58.676Z |
| gisa | M | 19729 | 9 | 0.456 | 0.155 | G | G | G | 2026-11-12T19:28:05.203Z |
| gisa | M | 17044 | 12 | 0.704 | 0.213 | L | G | L | 2026-11-12T02:46:05.372Z |
| gisa | M | 16457 | 10 | 0.608 | 0.196 | L | G | L | 2026-11-11T20:51:25.665Z |
| gisa | M | 15452 | 4 | 0.259 | 0.11 | G | G | G | 2026-11-15T16:43:51.292Z |
| gisa | — | 14779 | 8 | 1.015 | 0.225 | L | G | L | 2026-11-16T14:49:28.959Z |
| gisa | M | 14655 | 10 | 0.682 | 0.106 | L | G | G | 2026-11-11T19:15:29.846Z |
| gisa | M | 14470 | 3 | 0.207 | 0.133 | G | G | G | 2026-11-11T23:24:27.462Z |
| gisa | — | 14050 | 4 | 0.285 | 0.089 | G | G | G | 2026-11-16T16:13:16.118Z |
| gisa | M | 13636 | 7 | 0.513 | 0.075 | L | G | G | 2026-11-11T14:42:05.464Z |
| gisa | — | 13460 | 5 | 0.371 | 0.053 | G | G | G | 2026-11-11T14:39:51.921Z |
| gisa | M | 12777 | 9 | 0.704 | 0.133 | L | G | G | 2026-11-15T03:06:32.764Z |
| gisa | — | 12614 | 3 | 0.238 | 0.157 | G | G | G | 2026-11-16T04:28:42.372Z |
| gisa | — | 12454 | 4 | 0.321 | 0.128 | G | G | G | 2026-11-11T16:20:37.136Z |
| gisa | M | 12270 | 9 | 0.733 | 0.135 | L | G | G | 2026-11-16T15:45:06.143Z |
| gisa | M | 11459 | 6 | 0.524 | 0.112 | L | G | G | 2026-11-15T08:51:58.375Z |
| gisa | — | 11360 | 8 | 0.704 | 0.222 | L | G | L | 2026-11-16T14:07:46.682Z |
| gisa | M | 11156 | 6 | 0.538 | 0.32 | L | L | L | 2026-11-12T17:32:17.886Z |
| gisa | M | 11074 | 7 | 0.632 | 0.329 | L | L | L | 2026-11-13T09:28:29.841Z |
| gisa | — | 10856 | 11 | 1.013 | 0.138 | L | G | G | 2026-11-13T08:08:22.907Z |
| gisa | — | 10702 | 9 | 0.841 | 0.123 | L | G | G | 2026-11-16T14:00:47.177Z |
| gisa | M | 10691 | 7 | 0.655 | 0.036 | L | G | G | 2026-11-15T11:09:59.181Z |
| gisa | — | 10442 | 7 | 0.67 | 0.06 | L | G | G | 2026-11-16T15:40:57.622Z |
| gisa | — | 10347 | 5 | 0.483 | 0.117 | G | G | G | 2026-11-11T20:38:41.476Z |
| gisa | — | 10329 | 11 | 1.065 | 0.21 | L | G | L | 2026-11-16T22:58:40.518Z |
| gisa | M | 6330 | 6 | 0.948 | 0.183 | L | G | L | 2026-11-16T09:55:44.920Z |
| gisa | — | 5389 | 1 | 0.186 | 0.027 | G | G | G | 2026-11-16T09:20:32.954Z |
| kuru | M | 23005 | 9 | 0.391 | 0.238 | G | G | G | 2026-11-11T22:11:25.901Z |
| kuru | — | 18330 | 17 | 1.255 | 0.423 | L | L | L | 2026-11-12T02:55:28.280Z |
| kuru | — | 17259 | 8 | 0.811 | 0.163 | L | G | L | 2026-11-15T17:42:41.653Z |
| kuru | M | 15779 | 7 | 1.204 | 0.265 | L | G | L | 2026-11-15T14:52:56.172Z |
| kuru | M | 14476 | 12 | 1.658 | 0.268 | L | G | L | 2026-11-11T19:38:32.751Z |
| kuru | M | 13617 | 7 | 0.734 | 0.087 | L | G | G | 2026-11-12T01:24:56.258Z |
| kuru | M | 11720 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T17:20:12.415Z |
| kuru | — | 11478 | 3 | 0.261 | 0.228 | G | G | G | 2026-11-12T21:26:42.362Z |
| kuru | M | 11164 | 7 | 1.523 | 0.174 | L | G | L | 2026-11-15T18:12:04.671Z |
| kuru | M | 10756 | 4 | 0.93 | 0.166 | L | G | L | 2026-11-15T18:19:39.249Z |
| kuru | M | 10582 | 6 | 0.567 | 0.043 | L | G | G | 2026-11-15T18:19:49.188Z |
| kuru | M | 10433 | 5 | 0.671 | 0.09 | L | G | G | 2026-11-15T14:52:06.136Z |
| kuru | — | 10308 | 4 | 0.388 | 0.047 | G | G | G | 2026-11-16T04:52:40.073Z |
| kuru | M | 9283 | 5 | 0.754 | 0.175 | L | G | L | 2026-11-15T18:20:24.169Z |
| kuru | M | 8787 | 16 | 2.618 | 0.65 | L | L | L | 2026-11-15T16:14:25.308Z |
| kuru | M | 8603 | 3 | 0.93 | 0.231 | L | G | L | 2026-11-15T18:20:19.180Z |
| kuru | M | 7765 | 5 | 0.644 | 0.155 | L | G | L | 2026-11-15T17:25:47.423Z |
| kuru | M | 7623 | 0 | 0.787 | 0.5 | G | G | G | 2026-11-16T05:23:25.352Z |
| kuru | M | 4664 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T05:21:44.671Z |
| megumii | — | 13735 | 6 | 0.437 | 0.09 | G | G | G | 2026-11-16T11:05:07.955Z |
| megumii | — | 11989 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T10:19:14.718Z |
| megumii | M | 11446 | 6 | 0.524 | 0.046 | L | G | G | 2026-11-15T12:21:24.009Z |
| megumii | — | 11291 | 7 | 0.886 | 0.469 | L | L | L | 2026-11-12T06:27:12.690Z |
| megumii | M | 11145 | 6 | 2.064 | 0.22 | L | G | L | 2026-11-10T06:22:05.522Z |
| megumii | — | 10961 | 4 | 0.456 | 0.158 | G | G | G | 2026-11-11T07:45:50.362Z |
| megumii | M | 10936 | 4 | 0.366 | 0.096 | G | G | G | 2026-11-11T11:50:37.867Z |
| megumii | M | 10655 | 12 | 1.595 | 0.476 | L | L | L | 2026-11-12T19:09:08.636Z |
| megumii | M | 10464 | 3 | 0.382 | 0.033 | G | G | G | 2026-11-11T19:12:16.538Z |
| megumii | M | 10216 | 8 | 0.783 | 0.154 | L | G | L | 2026-11-12T16:39:30.416Z |
| megumii | M | 10062 | 5 | 0.596 | 0.055 | L | G | G | 2026-11-11T03:55:07.195Z |
| megumii | — | 10013 | 5 | 0.599 | 0.128 | L | G | G | 2026-11-13T10:27:35.591Z |
| megumii | — | 9938 | 5 | 0.503 | 0.031 | L | G | G | 2026-11-11T11:50:59.791Z |
| megumii | — | 9847 | 3 | 0.406 | 0.18 | G | G | G | 2026-11-15T15:17:58.955Z |
| megumii | — | 9844 | 4 | 0.406 | 0.059 | G | G | G | 2026-11-13T07:02:46.941Z |
| megumii | — | 9719 | 2 | 0.206 | 0.116 | G | G | G | 2026-11-12T03:53:27.709Z |
| megumii | M | 9702 | 4 | 0.412 | 0.176 | G | G | G | 2026-11-12T00:41:14.449Z |
| megumii | — | 9601 | 8 | 0.833 | 0.108 | L | G | G | 2026-11-13T11:41:45.642Z |
| megumii | — | 9210 | 2 | 0.217 | 0.055 | G | G | G | 2026-11-13T02:34:57.439Z |
| megumii | M | 9092 | 2 | 0.22 | 0.0 | G | G | G | 2026-11-13T10:28:27.427Z |
| megumii | — | 9053 | 6 | 0.994 | 0.24 | L | G | L | 2026-11-10T03:53:07.498Z |
| megumii | M | 8399 | 2 | 0.238 | 0.078 | G | G | G | 2026-11-10T04:06:36.078Z |
| megumii | — | 7710 | 7 | 1.038 | 0.13 | L | G | G | 2026-11-16T12:15:41.137Z |
| megumii | — | 7460 | 6 | 0.938 | 0.25 | L | G | L | 2026-11-11T20:44:01.576Z |
| megumii | M | 7240 | 4 | 0.552 | 0.123 | L | G | G | 2026-11-14T20:07:20.735Z |
| megumii | — | 7233 | 6 | 0.968 | 0.232 | L | G | L | 2026-11-15T08:38:26.264Z |
| megumii | — | 6868 | 5 | 0.728 | 0.435 | L | L | L | 2026-11-13T11:03:34.850Z |
| megumii | M | 6586 | 1 | 0.152 | 0.028 | G | G | G | 2026-11-15T06:20:16.620Z |
| megumii | — | 6575 | 4 | 0.608 | 0.194 | L | G | L | 2026-11-16T03:56:02.457Z |
| megumii | — | 6209 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T11:43:40.304Z |
| megumii | P | 5311 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T17:36:48.974Z |
| megumii | — | 5217 | 3 | 0.575 | 0.075 | L | G | G | 2026-11-14T14:36:40.043Z |
| megumii | — | 4981 | 0 | 0.201 | 0.006 | G | G | G | 2026-11-16T16:56:12.467Z |
| megumii | — | 4895 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T22:17:20.512Z |
| megumii | — | 3644 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T13:26:52.489Z |
| megumii | — | 3442 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T12:58:02.918Z |
| megumii | — | 3376 | 0 | 1.185 | 0.263 | G | G | G | 2026-11-16T14:54:23.986Z |
| megumii | — | 3193 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T16:30:19.151Z |
| megumii | — | 3138 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T15:17:57.884Z |
| megumii | M | 3036 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T14:30:31.633Z |
| megumii | — | 2959 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T12:45:36.556Z |
| zoya khan | M | 31036 | 12 | 0.387 | 0.033 | G | G | G | 2026-11-13T09:41:30.479Z |
| zoya khan | M | 23550 | 10 | 0.594 | 0.054 | L | G | G | 2026-11-13T10:19:51.666Z |
| zoya khan | M | 21779 | 10 | 0.689 | 0.125 | L | G | G | 2026-11-16T16:49:09.765Z |
| zoya khan | M | 20972 | 8 | 0.381 | 0.278 | G | G | G | 2026-11-16T14:28:15.571Z |
| zoya khan | M | 19878 | 9 | 0.453 | 0.242 | G | G | G | 2026-11-16T22:47:52.683Z |
| zoya khan | — | 18100 | 7 | 0.387 | 0.182 | G | G | G | 2026-11-16T14:28:26.882Z |
| zoya khan | M | 17358 | 3 | 0.173 | 0.056 | G | G | G | 2026-11-15T04:10:02.195Z |
| zoya khan | — | 16397 | 8 | 0.488 | 0.162 | G | G | G | 2026-11-16T13:54:07.469Z |
| zoya khan | — | 16067 | 11 | 0.934 | 0.185 | L | G | L | 2026-11-15T04:42:03.957Z |
| zoya khan | M | 15967 | 11 | 1.566 | 0.478 | L | L | L | 2026-11-13T09:53:01.146Z |
| zoya khan | M | 15809 | 8 | 0.633 | 0.111 | L | G | G | 2026-11-16T14:12:50.585Z |
| zoya khan | — | 15804 | 10 | 0.633 | 0.415 | L | L | L | 2026-11-16T14:31:06.623Z |
| zoya khan | — | 14301 | 4 | 0.489 | 0.121 | G | G | G | 2026-11-16T17:03:48.597Z |
| zoya khan | M | 14246 | 15 | 1.544 | 0.311 | L | L | L | 2026-11-13T09:20:13.998Z |
| zoya khan | M | 13671 | 13 | 0.951 | 0.482 | L | L | L | 2026-11-16T14:48:14.598Z |
| zoya khan | M | 13536 | 2 | 0.148 | 0.0 | G | G | G | 2026-11-16T15:03:39.537Z |
| zoya khan | — | 13077 | 7 | 0.535 | 0.189 | L | G | L | 2026-11-16T09:08:07.769Z |
| zoya khan | M | 12658 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-15T13:01:21.991Z |
| zoya khan | M | 12621 | 6 | 0.475 | 0.136 | G | G | G | 2026-11-16T09:22:26.428Z |
| zoya khan | M | 12302 | 7 | 2.113 | 0.23 | L | G | L | 2026-11-15T11:02:48.983Z |
| zoya khan | M | 11249 | 4 | 0.356 | 0.062 | G | G | G | 2026-11-15T06:30:10.755Z |
| zoya khan | — | 10957 | 7 | 0.73 | 0.102 | L | G | G | 2026-11-13T10:28:51.345Z |
| zoya khan | — | 10952 | 5 | 0.457 | 0.2 | G | G | G | 2026-11-16T17:21:24.559Z |
| zoya khan | — | 10199 | 3 | 1.079 | 0.097 | L | G | G | 2026-11-16T14:49:13.969Z |
| zoya khan | — | 8708 | 6 | 0.689 | 0.089 | L | G | G | 2026-11-15T12:15:04.305Z |
| zoya khan | — | 4867 | 2 | 0.411 | 0.032 | G | G | G | 2026-11-16T16:36:09.117Z |
| zoya khan | — | 4444 | 3 | 0.675 | 0.049 | L | G | G | 2026-11-16T22:28:15.707Z |
| zoya khan | M | 3930 | 3 | 0.763 | 0.131 | L | G | G | 2026-11-16T15:07:19.798Z |

## Lampiran B — Baris per jawaban: pemenang sel bayar baru settle sejak run-10 (71)

| Agen | Slot | Kar | URL | Dens | Rasio | K1 | @0,30 | @0,15 | Settle (updatedAt) |
|---|---|---|---|---|---|---|---|---|---|
| uid:111d46b8 | M | 19974 | 15 | 0.751 | 0.06 | L | G | G | 2026-11-16T20:01:18.494Z |
| zoya khan | M | 19878 | 9 | 0.453 | 0.242 | G | G | G | 2026-11-16T22:47:52.683Z |
| uid:a55de70b | M | 19486 | 15 | 0.77 | 0.253 | L | G | L | 2026-11-16T20:47:19.801Z |
| uid:a55de70b | M | 18588 | 13 | 0.699 | 0.14 | L | G | G | 2026-11-16T20:53:21.348Z |
| uid:a55de70b | M | 17795 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T20:51:41.306Z |
| uid:111d46b8 | M | 17692 | 10 | 0.622 | 0.176 | L | G | L | 2026-11-16T19:45:02.882Z |
| uid:a55de70b | M | 15130 | 12 | 1.718 | 0.14 | L | G | G | 2026-11-16T20:53:01.341Z |
| Sanbi | M | 14719 | 2 | 0.136 | 0.091 | G | G | G | 2026-11-16T19:56:21.561Z |
| Mahardika | M | 14573 | 9 | 0.618 | 0.176 | L | G | L | 2026-11-16T22:36:04.556Z |
| uid:a55de70b | M | 12887 | 14 | 1.164 | 0.242 | L | G | L | 2026-11-16T20:53:51.353Z |
| Hermawan Kwan | M | 12822 | 3 | 0.234 | 0.1 | G | G | G | 2026-11-16T22:20:40.249Z |
| Hermawan Kwan | M | 12666 | 10 | 0.947 | 0.178 | L | G | L | 2026-11-16T22:06:46.941Z |
| uid:c3d35a19 | M | 11368 | 6 | 0.528 | 0.065 | L | G | G | 2026-11-16T20:35:27.519Z |
| uid:c3d35a19 | M | 10710 | 12 | 1.12 | 0.17 | L | G | L | 2026-11-16T19:59:07.267Z |
| Lin Jason | M | 10523 | 5 | 0.475 | 0.307 | G | G | G | 2026-11-16T21:34:12.870Z |
| HIMANSHU | M | 10475 | 6 | 0.668 | 0.218 | L | G | L | 2026-11-16T22:55:20.540Z |
| uid:f7493074 | M | 10248 | 5 | 0.488 | 0.09 | G | G | G | 2026-11-16T21:47:40.379Z |
| Hermawan Kwan | M | 10230 | 9 | 0.88 | 0.154 | L | G | L | 2026-11-16T21:48:35.387Z |
| uid:b736acc1 | M | 8292 | 15 | 2.894 | 0.224 | L | G | L | 2026-11-16T19:46:48.906Z |
| uid:adb37229 | M | 7282 | 8 | 1.099 | 0.16 | L | G | L | 2026-11-16T22:49:38.308Z |
| Moden Gos | M | 6948 | 5 | 0.72 | 0.234 | L | G | L | 2026-11-16T21:56:51.633Z |
| uid:39a1698a | M | 5925 | 5 | 0.844 | 0.205 | L | G | L | 2026-11-16T20:44:14.367Z |
| uid:bebf7dff | M | 5806 | 16 | 2.928 | 0.936 | L | L | L | 2026-11-16T20:36:58.143Z |
| uid:764d41a8 | M | 4790 | 7 | 1.461 | 0.636 | L | L | L | 2026-11-16T20:37:13.288Z |
| uid:39a1698a | M | 4661 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T20:03:24.264Z |
| uid:b1f64912 | M | 4625 | 2 | 0.432 | 0.056 | G | G | G | 2026-11-16T20:07:50.374Z |
| uid:39a1698a | M | 4239 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-16T20:10:30.703Z |
| uid:abcb30f0 | M | 3625 | 5 | 1.379 | 0.105 | L | G | G | 2026-11-16T21:45:00.191Z |
| peng | M | 3513 | 14 | 3.985 | 0.839 | L | L | L | 2026-11-16T22:40:35.786Z |
| uid:76581e8b | M | 1799 | 3 | 1.668 | 0.692 | L | L | L | 2026-11-16T20:45:29.778Z |
| can-earn? | P | 21567 | 7 | 0.556 | 0.071 | L | G | G | 2026-11-17T00:15:22.443Z |
| uid:c29a2283 | P | 19005 | 21 | 1.263 | 0.557 | L | L | L | 2026-11-17T00:20:17.526Z |
| can-earn? | P | 17130 | 7 | 0.701 | 0.171 | L | G | L | 2026-11-17T00:26:56.120Z |
| uid:39192aeb | P | 16194 | 10 | 0.679 | 0.403 | L | L | L | 2026-11-16T23:54:27.347Z |
| fuck2ai | P | 15132 | 6 | 0.397 | 0.118 | G | G | G | 2026-11-16T23:37:48.494Z |
| Febriyan | P | 14591 | 6 | 0.959 | 0.413 | L | L | L | 2026-11-16T23:42:26.143Z |
| chirpy | P | 14491 | 6 | 0.552 | 0.061 | L | G | G | 2026-11-17T00:23:16.349Z |
| uid:5ba444f7 | P | 14187 | 20 | 2.256 | 0.594 | L | L | L | 2026-11-17T00:09:38.630Z |
| Sanbi | P | 14047 | 2 | 0.285 | 0.035 | G | G | G | 2026-11-17T00:17:38.951Z |
| uid:a8800ea4 | P | 13737 | 13 | 0.946 | 0.32 | L | L | L | 2026-11-17T00:20:47.462Z |
| uid:f62864f2 | P | 10562 | 46 | 4.355 | 0.855 | L | L | L | 2026-11-16T23:37:58.999Z |
| uid:8a103262 | P | 10359 | 45 | 4.344 | 0.878 | L | L | L | 2026-11-17T00:02:43.618Z |
| uid:3f4d8594 | P | 10154 | 6 | 0.591 | 0.112 | L | G | G | 2026-11-16T21:59:25.506Z |
| chirpy | P | 9622 | 3 | 0.312 | 0.088 | G | G | G | 2026-11-17T00:25:28.985Z |
| uid:6e3bbde3 | P | 8547 | 0 | 0.117 | 0.083 | G | G | G | 2026-11-17T00:09:27.021Z |
| Rio ramadan Saputra | P | 8123 | 6 | 1.108 | 0.192 | L | G | L | 2026-11-17T00:23:03.640Z |
| uid:8a103262 | P | 7981 | 39 | 4.887 | 0.889 | L | L | L | 2026-11-17T00:18:00.793Z |
| uid:443e4a17 | P | 7410 | 3 | 0.405 | 0.091 | G | G | G | 2026-11-17T00:22:41.723Z |
| uid:5de10449 | P | 6550 | 52 | 7.939 | 0.859 | L | L | L | 2026-11-16T23:59:38.342Z |
| uid:1121d581 | P | 6416 | 5 | 0.779 | 0.286 | L | G | L | 2026-11-16T23:34:18.766Z |
| dike008.love | P | 6356 | 3 | 0.472 | 0.184 | G | G | G | 2026-11-17T00:24:01.022Z |
| uid:422e18f8 | P | 5957 | 37 | 6.211 | 0.927 | L | L | L | 2026-11-16T23:34:20.806Z |
| Dimas | P | 5792 | 7 | 1.727 | 0.625 | L | L | L | 2026-11-16T22:38:32.821Z |
| dike008.love | P | 5375 | 1 | 0.186 | 0.1 | G | G | G | 2026-11-16T23:40:00.257Z |
| Ichika | P | 4840 | 10 | 6.612 | 0.8 | L | L | L | 2026-11-16T23:50:43.208Z |
| uid:d91d68f5 | P | 3932 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-17T00:22:26.092Z |
| uid:4966c67b | P | 2792 | 6 | 2.149 | 0.714 | L | L | L | 2026-11-16T21:24:32.599Z |
| Md ripon Rana | P | 2713 | 2 | 0.737 | 0.2 | L | G | L | 2026-11-16T23:33:17.752Z |
| Md ripon Rana | P | 2125 | 3 | 1.412 | 0.25 | L | G | L | 2026-11-16T23:39:05.331Z |
| Md ripon Rana | P | 2047 | 2 | 0.977 | 0.778 | L | L | L | 2026-11-16T23:43:46.096Z |
| uid:69cf9e69 | P | 1852 | 2 | 1.08 | 0.0 | L | G | G | 2026-11-16T23:40:17.744Z |
| uid:88fa3174 | P | 1717 | 0 | 0.0 | 0.0 | G | G | G | 2026-11-17T00:33:28.773Z |
| uid:4966c67b | P | 1484 | 5 | 3.369 | 0.759 | L | L | L | 2026-11-16T22:27:16.217Z |
| uid:1ddb9bb0 | P | 1416 | 0 | 0.706 | 1.0 | G | G | G | 2026-11-17T00:16:12.153Z |
| uid:9572cf4f | P | 1237 | 3 | 2.425 | 0.0 | L | G | G | 2026-11-16T23:49:52.638Z |
| Abid | P+M | 11658 | 0 | 0.086 | 0.009 | G | G | G | 2026-11-16T21:52:31.499Z |
| uid:8f812f73 | P+M | 8017 | 4 | 0.499 | 0.346 | G | G | G | 2026-11-16T22:29:32.148Z |
| uid:1b007b2d | P+M | 5863 | 5 | 0.853 | 0.312 | L | L | L | 2026-11-16T20:50:41.057Z |
| uid:bebf7dff | P+M | 5656 | 5 | 0.884 | 0.294 | L | G | L | 2026-11-16T22:11:16.977Z |
| coucung | P+M | 4646 | 2 | 0.43 | 0.222 | G | G | G | 2026-11-16T22:26:56.795Z |
| uid:12658e5d | P+M | 3447 | 6 | 2.321 | 0.286 | L | G | L | 2026-11-16T22:20:40.186Z |
