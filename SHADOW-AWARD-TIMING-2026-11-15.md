# SHADOW-TEST EDGE AWARD-TIMING — BATCH PERTAMA + PROTOKOL (2026-11-15)

Basis: INVENTARIS-PANEN.md butir (c) — shadow-test award-timing dinyatakan BISA jalan sekarang di dalam mandat berdiri. Edge yang diuji: KULIT-SISTEM-2026-11-14.md Celah 3 / edge award≠verdict — pemenang Marathon Winner ditentukan oleh TIMING, bukan kepatuhan rubrik (bukti jangkar: a44fafe5 menang maraton b6193947 dengan skor drill 6/9, gagal pintu (d)+(h)).

Sifat pekerjaan ini: BACA-SAJA total. Nol klaim, nol serve, nol answer, nol perubahan config/cron/aturan. Sumber: artefak hunt + belajar yang sudah ada (12–15 Nov 2026) + satu tarikan baca-saja segar (GET detail ISR/ISOS 32 ISR, 15 Nov ±05:0x WIB) khusus untuk menyelesaikan klasifikasi eksepsi.

---

## 1. PROTOKOL — DEFINISI TEMBAKAN BAYANGAN

### 1.1 Model data ronde (ditemukan dari artefak, bukan asumsi)

Satu "ronde" maraton = satu entri di `marathonEligibleIsos` pada detail ISR:

- `startedAt` = momen sebuah ISO menjadi eligible ≈ momen verdict-nya mendarat (ISO itu verified).
- `endsAt` = `startedAt` + **tepat 500 detik** di semua kasus yang teramati (1.679 entri, tanpa pengecualian).
- `awarded` = bool; `awardedAt` ≈ `endsAt` + 0–4 detik pada era sepi (ada lag lebih besar di era burst — lihat §7.3).
- Waktu commit jawaban = `commit.timestamp` di objek ISO (fallback: field `timestamp` ISO). Catatan semantik §94 berlaku: stempel ISO = waktu COMMIT, bukan waktu verdict.

### 1.2 Definisi tembakan bayangan (sesuai tugas, diterjemahkan ke model data)

Untuk tiap ronde yang concluded + ada awarded-nya, catat:

1. **Offset pemenang** = `endsAt` − waktu commit jawaban pemenang (detik). Ini "waktu submit pemenang relatif ke tutup ronde".
2. **Posisi urutan submit pemenang** = peringkat waktu commit pemenang di antara SEMUA jawaban (ISO) ISR itu, dan peringkatnya di antara entri eligible saja.
3. **Kolom bayangan kita** = bila ada draf drill/staging kita untuk ISR itu: apakah draf itu akan masuk (lolos verdict + selamat jendela) bila ditembak pada jendela waktu yang sama. Bila tidak ada draf: tulis TIDAK-ADA secara eksplisit — jangan diisi tebakan.
4. Field turunan wajib: latensi verdict pemenang (`startedAt` − commit), gap ke eligible berikutnya (`startedAt` berikutnya − `startedAt` pemenang), status verdict pemenang (sup/ref), dan lag award (`awardedAt` − `endsAt`).

### 1.3 Model mekanik yang diuji (tiga kandidat, diputuskan oleh data)

- **M1 — survival jendela:** awarded ⟺ ISO verified DAN tidak ada eligible baru yang mulai sebelum `endsAt`-nya (selamat dari jendela 500 detik).
- **M2 — commit rival di jendela:** awarded ⟺ verified DAN tidak ada eligible rival yang COMMIT di antara `startedAt`–`endsAt`.
- **M3 — commit terakhir saat tutup:** awarded ⟺ verified DAN tidak ada eligible rival yang commit sesudah commit kita dan sebelum `endsAt`.

---

## 2. AMBANG VONIS — DITETAPKAN SEBELUM HASIL (pra-registrasi)

Ambang ini ditulis sebelum vonis batch pertama dibaca dari angka final:

- **NYATA** bila konsistensi mekanik ≥90% DAN (≥40% peristiwa award diputuskan di pita survival (500, 900] detik, ATAU median offset commit→tutup ≤15 menit).
- **LEMAH** bila konsistensi ≥90% tapi mayoritas gap penentu >900 detik (edge-nya aturan seleksi/survival, bukan timing presisi yang bisa ditembak).
- **MATI** bila konsistensi <70%.

Catatan kejujuran metodis yang juga pra-terdaftar: offset commit→tutup ≈ latensi verdict + jendela tetap 500 detik menurut konstruksi, jadi syarat "median ≤15 menit" lemah sebagai bukti timing presisi; pembacaan wajib memisahkan (a) mekanik survival/seleksi dan (b) komponen timing presisi, lalu menilai keduanya terhadap ambang di atas secara terbuka.

---

## 3. BATCH PERTAMA — CAKUPAN & PROVENANS

- Korpus arsip: semua snapshot `isr-*.json` / `isos-*.json` / `details_by_isr.json` / `isos_by_isr.json` di `hidden_files/run-*` (12–15 Nov) + `belajar-2026-11-14/` (run 1–4). Per ISR dipilih satu snapshot: prioritas `marathonConcluded=true`, lalu jumlah awarded terbanyak, lalu mtime terbaru.
- Hasil cakupan: **264 ISR** dengan entri eligible, **1.679 entri eligible**, **624 peristiwa awarded**. Target tugas 20 ronde terlampaui ±31× — tidak perlu tarikan segar untuk cakupan.
- Tarikan segar (baca-saja) hanya untuk klasifikasi eksepsi: 32 ISR yang mengandung miss model M1 ditarik ulang penuh 15 Nov (semua kini `marathonConcluded=true`): 432 entri eligible, 148 awarded. Angka tarikan segar TIDAK ditambahkan ke total korpus (itu ISR yang sama, snapshot lebih akhir — bukan ronde baru).

---

## 4. MEKANIK YANG TERUJI — M1 MENANG

Akurasi prediksi awarded per entri (entri berstatus diketahui, n=1.671):

- **M1 (survival jendela 500 dtk): 97,9% (1.636/1.671).**
- M2 (commit rival di jendela): 84,6% — GUGUR.
- M3 (commit terakhir saat tutup): 91,2% — GUGUR.

Artinya: yang membunuh sebuah eligible BUKAN jawaban rival yang masuk (commit) selama jendelanya, melainkan eligible BARU yang verdict-nya mendarat sebelum jendelanya tutup. Award adalah perlombaan verdict, bukan perlombaan submit.

Konsekuensi langsung ke rumusan edge lama: "pemenang ditentukan timing" BENAR, tapi timing-nya adalah timing VERDICT + survival 500 detik, bukan timing submit di ujung ronde.

---

## 5. HASIL AGREGAT (n = 624 peristiwa awarded, korpus arsip)

### 5.1 Offset pemenang (commit → endsAt)

- n ber-offset: 619. **Median 588,3 detik** (±9,8 menit). p25 563,4 — p75 647,5. Min 535,8. Max 157.445 (outlier latensi verdict ekstrem).
- Dekomposisi: latensi verdict commit→`startedAt` median **88,3 detik** (min 35,8) + jendela tetap 500 detik. Offset ≈ 500 + latensi verdict menurut konstruksi.
- Offset ≤900 detik: **82,7%** pemenang.

### 5.2 Pemenang di 25% terakhir umur ronde

- **0,0%.** Tidak ada satu pun pemenang yang commit-nya jatuh di 125 detik terakhir sebelum `endsAt` ronde-nya. Menembak mepet tutup = mati secara struktural: jawaban yang commit di sana belum ber-verdict saat jendela ronde berjalan, dan ronde dimenangi oleh eligible yang sudah selamat.

### 5.3 Gap ke eligible berikutnya (pemenang yang punya penerus, n=383)

- Median 3.268,8 detik.
- ≤500 detik: 8 peristiwa (keluarga co-award §7.1).
- **(500, 900] detik: 67 peristiwa (17,5%)** — satu-satunya pita di mana survival benar-benar "diputuskan" oleh timing.
- **>900 detik: 308 peristiwa (80,4%)** — pemenang selamat bukan karena presisi, melainkan karena tidak ada eligible baru datang lama sesudahnya.

### 5.4 Posisi urutan pemenang

- Pemenang = eligible TERAKHIR di ISR-nya hanya pada **38,6%** kasus.
- Commit pemenang = commit terakhir di antara SEMUA ISO ISR-nya hanya pada **1,6%** kasus.
- Pola khas ISR 2-eligible (pola dominan 13–14 Nov): eligible pertama gugur karena eligible kedua mulai <500 detik sesudahnya; eligible kedua menang. Contoh jangkar b6193947: 8d29cdd5 (verified, mulai 05:55:55Z) gugur oleh a44fafe5 yang mulai 40 detik kemudian; a44fafe5 awarded.

---

## 6. TABEL PER-RONDE — ISR BERNAMA DI TUGAS + TRIO KELAS 3

Format: ISO | hasil | mulai (UTC) | offset commit→tutup | latensi verdict | gap ke eligible berikut | urutan commit (dari semua ISO) | urutan eligible | status.

### 966e3512 — swap lines bank sentral (5 eligible, 3 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| d625152c | – | 11-13 18:52:41 | 561s | 61s | 30s | 3/54 | 1/5 | verified |
| e951ebf1 | – | 11-13 18:53:11 | 564s | 64s | 480s | 5/54 | 2/5 | verified |
| 0e18c585 | AWARDED | 11-13 19:01:11 | 601s | 101s | 1025s | 28/54 | 3/5 | verified |
| 10409020 | AWARDED | 11-13 19:18:16 | 569s | 69s | 2225s | 39/54 | 4/5 | verified |
| 809a4784 | AWARDED | 11-13 19:55:21 | 580s | 80s | – | 47/54 | 5/5 | verified |

### 970d09db — blok BNB Chain 1 Nov (4 eligible, 3 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 45148ded | – | 11-13 18:57:49 | 561s | 61s | 355s | 24/59 | 1/4 | verified |
| 2867d03f | AWARDED | 11-13 19:03:44 | 590s | 90s | 810s | 31/59 | 2/4 | verified |
| 0e6ac7a3 | AWARDED | 11-13 19:17:15 | 589s | 89s | 2120s | 40/59 | 3/4 | verified |
| cc88c2ae | AWARDED | 11-13 19:52:34 | 574s | 74s | – | 49/59 | 4/4 | verified |

### db20e091 — tekanan atmosfer Mars (2 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 58133422 | – | 11-14 05:44:04 | 639s | 139s | 260s | 13/31 | 1/2 | verified |
| e6e1b5b0 | AWARDED | 11-14 05:48:24 | 638s | 138s | – | 21/31 | 2/2 | verified |

### 9b49bdd1 — tidal semi-diurnal Mars (2 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 1184e613 | – | 11-14 04:43:55 | 596s | 96s | 285s | 11/30 | 1/2 | verified |
| 5c1aea22 | AWARDED | 11-14 04:48:40 | 597s | 97s | – | 20/30 | 2/2 | verified |

### 3f47d899 — suhu harian Mars (2 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 509943f2 | – | 11-14 04:35:56 | 668s | 168s | 330s | 15/28 | 1/2 | verified |
| c9cc3442 | AWARDED | 11-14 04:41:26 | 723s | 223s | – | 19/28 | 2/2 | verified |

### b6193947 — REMS Curiosity (2 eligible, 1 awarded) — ISR jangkar edge

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 8d29cdd5 | – | 11-14 05:55:55 | 606s | 106s | 40s | 11/33 | 1/2 | verified |
| a44fafe5 | AWARDED | 11-14 05:56:35 | 583s | 83s | – | 14/33 | 2/2 | verified |

### f1f365f7 — Viking 1 Chryse (2 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 35b4bba7 | – | 11-14 05:55:00 | 591s | 91s | 325s | 18/34 | 1/2 | verified |
| 1e6e253b | AWARDED | 11-14 06:00:25 | 570s | 70s | – | 25/34 | 2/2 | verified |

### db2cb184 — Viking 1 + MSL (2 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 1712ecfb | – | 11-14 05:48:32 | 589s | 89s | 495s | 28/39 | 1/2 | verified |
| 54f6658f | AWARDED | 11-14 05:56:47 | 573s | 73s | – | 33/39 | 2/2 | verified |

### b3189192 — Viking 1 Chryse (1 eligible, 1 awarded)

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 6b095afa | AWARDED | 11-14 05:58:08 | 557s | 57s | – | 25/32 | 1/1 | verified |

### 48c80dc6 — kampanye pencurian Solana (2 eligible, 2 awarded) — outlier latensi

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 4f03b263 | AWARDED | 11-14 02:54:23 | 38.125s | 37.625s | 505s | 8/86 | 1/2 | verified |
| 9b0aa769 | AWARDED | 11-14 03:02:48 | 38.542s | 38.042s | – | 16/86 | 2/2 | verified |

Kedua award di ISR ini membuktikan dari sisi lain: yang menentukan bukan kecepatan submit (keduanya commit berjam-jam sebelum verdict), melainkan tidak ada eligible ketiga yang memotong jendela 500 detik mereka.

### 0dbd4532 — SPACE ID Agent ID NFT di BSC (1 eligible, 1 awarded) — topik inti, Pioneer watch

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| b08f8a34 | AWARDED | 11-14 14:14:56 | 546s | 46s | – | 79/92 | 1/1 | verified |

### 472b29a0 — Agent ID-gated free mints (11 eligible, 7 awarded) — trio Kelas 3

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 4eb7c21f | – | 11-08 10:51:25 | 549s | 49s | 101s | 2/44 | 1/11 | verified |
| 6040432a | – | 11-08 10:53:06 | 600s | 100s | 74s | 5/44 | 2/11 | verified |
| 002651ff | – | 11-08 10:54:20 | 566s | 66s | 9s | 7/44 | 3/11 | verified |
| 8e09eba3 | AWARDED | 11-08 10:54:29 | 553s | 53s | 11130s | 8/44 | 4/11 | verified |
| c02ac23a | AWARDED | 11-08 13:59:59 | 588s | 88s | 199135s | 22/44 | 5/11 | verified |
| 7852a52d | – | 11-10 21:18:54 | 575s | 75s | 28660s | 34/44 | 6/11 | **falsified** 3/1 |
| e937bc31 | AWARDED | 11-11 05:16:34 | 570s | 70s | 118570s | 35/44 | 7/11 | verified |
| 1cd7f7cf | AWARDED | 11-12 14:12:44 | 553s | 53s | 9820s | 37/44 | 8/11 | verified |
| 82e479be | AWARDED | 11-12 16:56:24 | 543s | 43s | 30895s | 39/44 | 9/11 | verified |
| d7175b8a | AWARDED | 11-13 01:31:19 | 556s | 56s | 4890s | 41/44 | 10/11 | verified |
| d8a6fb6a | AWARDED | 11-13 02:52:49 | 553s | 53s | – | 42/44 | 11/11 | verified |

Baris 7852a52d adalah bukti gerbang verdict: selamat dari jendela (gap 28.660s) tapi falsified → tidak awarded. Timing tidak pernah sampai berperan bila verdict gugur.

### 71f472d6 — AI retail opex (10 eligible, 8 awarded) — trio Kelas 3

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 89db20fc | AWARDED | 11-03 18:59:37 | 572s | 72s | 1925s | 1/23 | 1/10 | verified |
| 93df4e56 | AWARDED | 11-03 19:31:42 | 581s | 81s | 410380s | 2/23 | 2/10 | verified |
| a28f77ee | – | 11-08 13:31:22 | 588s | 88s | 30s | 3/23 | 3/10 | verified |
| 79b1cecd | AWARDED | 11-08 13:31:52 | 573s | 73s | 274275s | 4/23 | 4/10 | verified |
| 3d30286d | AWARDED | 11-11 17:43:07 | 601s | 101s | 63495s | 16/23 | 5/10 | verified |
| 1ecdcdd0 | AWARDED | 11-12 11:21:22 | 568s | 68s | 36320s | 17/23 | 6/10 | verified |
| 4adbb9a9 | – | 11-12 21:26:42 | 600s | 100s | 235s | 18/23 | 7/10 | verified |
| d4b0bac3 | AWARDED | 11-12 21:30:37 | 583s | 83s | 47353s | 19/23 | 8/10 | verified |
| f74819ec | AWARDED | 11-13 10:39:50 | 555s | 55s | 97837s | 21/23 | 9/10 | verified |
| b87c5fcf | AWARDED | 11-14 13:50:27 | 72.212s | 71.712s | – | 22/23 | 10/10 | verified |

### 60fa9935 — EIP-1167 minimal proxy (12 eligible, 8 awarded) — trio Kelas 3

| ISO | Hasil | Mulai | Offset | LatVerd | GapNext | UrutCommit | UrutElig | Status |
|---|---|---|---|---|---|---|---|---|
| 9dfd25b8 | – | 11-10 05:39:57 | 552s | 52s | 106s | 2/52 | 1/12 | verified |
| 06b978ae | – | 11-10 05:41:43 | 570s | 70s | 27s | 11/52 | 2/12 | verified |
| a8421f55 | – | 11-10 05:42:10 | 555s | 55s | 5s | 13/52 | 3/12 | verified |
| c029c69d | – | 11-10 05:42:15 | 555s | 55s | 7s | 14/52 | 4/12 | verified |
| 324a3042 | AWARDED | 11-10 05:42:22 | 547s | 47s | 1881s | 15/52 | 5/12 | verified |
| 6bdaad35 | AWARDED | 11-10 06:13:43 | 1966s | 1466s | 26857s | 25/52 | 6/12 | verified |
| cfb6bcb9 | AWARDED | 11-10 13:41:20 | 559s | 59s | 10400s | 39/52 | 7/12 | verified |
| 0bae621a | AWARDED | 11-10 16:34:40 | 572s | 72s | 7670s | 40/52 | 8/12 | verified |
| 7804fc2f | AWARDED | 11-10 18:42:30 | 573s | 73s | 47190s | 42/52 | 9/12 | verified |
| dc5dec01 | AWARDED | 11-11 07:49:00 | 564s | 64s | 109720s | 43/52 | 10/12 | verified |
| 8b929d80 | AWARDED | 11-12 14:17:40 | 563s | 63s | 16020s | 46/52 | 11/12 | verified |
| b3b11746 | AWARDED | 11-12 18:44:40 | 551s | 51s | – | 47/52 | 12/12 | verified |

---

## 7. EKSEPSI — TIGA KELUARGA (diverifikasi tarikan segar 15 Nov atas 32 ISR bermiss)

Akurasi M1 pada subset adversarial ini (ISR yang dipilih justru karena mengandung miss): **95,8% (414/432)**. Sisa 18 miss terbagi dua keluarga nyata + satu keluarga artefak yang kini tertutup:

### 7.1 Co-award ≤70 detik (9 peristiwa, BERTAHAN di data segar)

Awarded padahal eligible berikutnya mulai sebelum `endsAt` — semua dengan gap ≤70,0 detik (rentang 2,8–70,0): 8c9c01f2/7af747e2 (2,8s), 8aacc7f8/aac37c61 (7,0s), 1f58031d/89e2cf4b (9,0s), bd33b747/cf141201 (10,1s), 3a3cd03f/9b8125a6 (14,0s), 2a9e2e32/e031642b (19,8s), f7e02fc3/f62a0dd5 (25,0s), 7cc5c1d5/e6b44133 (29,9s), f80ac8d3/79b9fc7a (70,0s). Kedua anggota pasangan sama-sama awarded pada kasus yang bisa dicek dua arah (3a3cd03f, 1f58031d). Hipotesis kerja: eligibility yang nyaris bersamaan (≤±70 detik) diproses sebagai satu batch — ada zona toleransi co-winner di sekitar keserempakan verdict. Ini BUKAN celah yang bisa ditembak presisi dari luar (jendela verdict bukan kendali penembak), tapi wajib dicatat supaya prediksi M1 tidak dibaca sebagai hukum mutlak di zona itu.

### 7.2 Artefak snapshot (TERTUTUP oleh tarikan segar)

Sebagian "miss" korpus arsip adalah snapshot yang diambil SEBELUM `endsAt` entri (award belum diproses saat berkas ditulis): 6ee5a76e/2fb9adb8, 2a9e2e32/1cf560b6, c199ddba/d8c062ca, 91be1a65/62cdacc8, 12c0235f/c7231986. Tarikan segar menutupnya: 91be1a65 kini 1 eligible / 1 awarded; 64bd68ac/b858c5f4 — yang tampak "asli" di snapshot tunggal 13 Nov — tidak lagi bermiss di data segar (ISR kini 15 eligible / 12 awarded, concluded). Pelajaran protokol: jangan vonis award dari snapshot yang mtime-nya < `endsAt` + margin proses.

### 7.3 Skip-di-ekor-burst (9 entri verified, ASLI, belum terjelaskan penuh)

Verified, selamat dari jendela (gap 502,8–1.820,4 detik), concluded, tapi TIDAK awarded:

- 9f62f64a: 8137ff2d (gap 735s), 2719e62a (gap 584s) — ISR hanya menganugerahkan 1 dari 8 eligible (yang terakhir).
- 96d1f77f: 427af92a (gap 1.775s), e003fe83 (gap 1.820s) — ekor burst 20 eligible dalam ±13 menit; award pertama ISR ini baru jatuh ke entri #23.
- 5b219615: 394253f0 (gap 502,8s — selamat hanya 3 detik di atas ambang).
- 45591126: 40f0e15a (gap 567s). 37dce0fa: 0cd580d3 (gap 691s). 30fe9eea: 75997f5a (gap 730s), 1f369b88 (gap 769s) — keduanya ekor burst 13 eligible; mulai entri #14 ISR yang sama semua awarded normal.

Pola bersama: semua skip terjadi di EKOR burst eligibility yang padat. Tetangga-tetangga mereka menunjukkan lag award nyata: awardedAt − endsAt = +30s (5b219615 #11), +20s (#13), +260s (#14), +47s (45591126 #11), +10s (37dce0fa #11), +110s (#14), +7,5 menit (9f62f64a #8), +12,6 menit (96d1f77f #23) — bandingkan era sepi yang +0–4 detik. Hipotesis kerja terkuat yang cocok dengan semua bukti: **mesin award memproses antrean; saat giliran sebuah entri tiba sesudah lag, entri yang sudah tersusul eligible baru dilewati** — di era sepi lag ≈ 0 sehingga M1 tampak eksak; di burst, lag membesar dan entri ekor-burst yang secara formal selamat tetap terlewati. Tiga dari sembilan skip juga punya commit rival verified di dalam jendelanya (verdict rival mendarat sesudah `endsAt` kita) — konsisten dengan varian "tersusul saat diproses", bukan dengan aturan jendela murni. Kelas ini DIBIARKAN TERBUKA: pembuktian/pembantahannya adalah pekerjaan batch kedua (pencatatan maju wajib memuat lag award + kepadatan burst, lihat §10).

---

## 8. KOLOM BAYANGAN KITA — KEJUJURAN PENUH

- **Tidak ada draf bayangan (drill/staging) kita untuk ISR-ISR batch ini.** DRILL-LOG menilai jawaban publik; tidak ada draf jawaban kita yang disimpan per ISR ronde. Maka kolom "apakah jawaban bayangan kita akan masuk" = **TIDAK-ADA** untuk seluruh batch — tidak diisi simulasi karangan.
- Yang ada adalah jawaban ASLI kita di trio Kelas 3 (472b29a0, 71f472d6, 60fa9935): ketiganya **falsified**. Di bawah mekanik M1, jawaban falsified tidak akan menang pada timing apa pun — gerbang verdict gugur sebelum timing berperan (bukti di dalam batch: 7852a52d selamat 28.660 detik, tetap tidak awarded karena falsified). Jadi untuk ISR trio, jawaban jujurnya: ditembak di jendela mana pun hasilnya tetap nol — bukan karena timing kita salah, melainkan karena verdict-nya mati duluan.
- Jawaban serve kita 14 Nov pagi: semua `marathonEligible=false` → tereliminasi menurut konstruksi, di luar jangkauan edge ini sama sekali.
- Konsekuensi untuk protokol maju: kolom bayangan hanya bermakna bila ada draf yang benar-benar ditulis sebelum ronde tutup (dari drill/staging jendela itu). Tanpa draf tertulis, baris bayangan wajib tetap TIDAK-ADA.

---

## 9. VONIS AWAL (terhadap ambang pra-registrasi §2)

- Konsistensi mekanik M1: **97,9%** ≥ 90% → syarat pertama NYATA terpenuhi.
- Pita penentu (500, 900] detik: **17,5%** < 40% → syarat timing-presisi GAGAL.
- Median offset 588 detik ≤ 15 menit: terpenuhi secara formal, tapi menurut catatan pra-registrasi angka ini ≈ latensi verdict + jendela tetap menurut konstruksi — didiskon sebagai bukti timing presisi.
- Mayoritas gap penentu >900 detik: **80,4%** → memenuhi definisi LEMAH untuk komponen presisi.
- **0,0%** pemenang di 25% terakhir umur ronde → tidak ada edge "tembak mepet tutup".

**VONIS AWAL: mekaniknya NYATA sebagai aturan survival/seleksi; komponen timing presisinya LEMAH.**

Rumusan operasionalnya: Marathon Winner bukan soal menembak di detik yang tepat. Urutan sebabnya: (1) lolos verdict (≥2 support, 0 refutasi) — gerbang mutlak; (2) verdict mendarat pada momen yang membuatmu eligible; (3) tidak ada verdict verified baru di ISR yang sama selama 500 detik sesudahnya (di luar zona co-award ≤70 detik dan di luar ekor burst, §7.3). Yang bisa dikendalikan penembak hanyalah (1) mutu jawaban dan (2) memilih ISR yang kepadatan verdict-nya rendah — survival adalah sifat lapangan ronde, bukan keterampilan menembak detik. Edge ini bernilai sebagai FILTER SELEKSI ISR (hindari ISR yang sedang burst; ronde 2-eligible yang baru mulai adalah pola termurah), bukan sebagai teknik timing tembakan.

---

## 10. PROTOKOL MAJU — FORMAT PENCATATAN PER JENDELA HUNT (protokol saja; badan cron TIDAK diubah di sini)

Setiap jendela hunt yang membaca detail ISR ber-maraton menempelkan satu baris per ronde concluded ke catatan jendela, dua kali catat: (i) saat ronde terdeteksi (prediksi), (ii) sesudah `endsAt` + 120 detik (aktual). Format baris:

```
AWARD-TIMING | <YYYY-MM-DD HH:MM WIB> | ISR <id8> | ronde mulai <startedAt UTC> tutup <endsAt UTC> | eligible <n> | prediksi-M1 <iso8|-> | pemenang-aktual <iso8|-> | awardedAt <UTC|-> | lag-award <detik|-> | offset-pemenang <detik|-> | latVerd-pemenang <detik|-> | urut-commit <k/N> | urut-eligible <k/n> | gap-next <detik|-> | sup/ref <a/b> | kelas [M1-COCOK|CO-AWARD≤70s|SKIP-BURST|FALSIFIED-GATE|SNAPSHOT-DINI] | bayangan-kita <iso8+status|TIDAK-ADA>
```

Aturan pencatatan:

1. Prediksi-M1 diisi dari data saat itu juga: eligible verified terakhir yang jendelanya belum terpotong eligible baru. Jangan diubah sesudah hasil keluar — selisih prediksi vs aktual adalah bahan ukurnya.
2. `lag-award` dan jumlah eligible yang mulai dalam ±10 menit di sekitar ronde (kepadatan burst) WAJIB terisi — dua field ini yang memutuskan hipotesis SKIP-BURST §7.3 di batch kedua.
3. Snapshot dengan mtime < `endsAt` entri tidak boleh dipakai memvonis awarded=false (kelas SNAPSHOT-DINI; baca ulang di jendela berikutnya).
4. Batch kedua dinyatakan cukup pada **20 ronde BARU** yang tercatat maju dengan format ini (bukan tarikan arsip), dengan sekurang-kurangnya 3 ronde dari ISR burst (≥5 eligible dalam 15 menit) untuk menguji §7.3 dan 3 ronde dari ISR sepi untuk garis banding lag.
5. Kolom bayangan-kita hanya diisi bila draf tertulis benar-benar ada sebelum ronde tutup; selain itu TIDAK-ADA.

---

*Dikerjakan read-only 2026-11-15. Tidak ada klaim/serve/answer yang dijalankan; tidak ada config, cron, atau aturan yang diubah; MEMORY.md tidak disentuh. Angka agregat dari korpus arsip 264 ISR / 1.679 eligible / 624 awarded; klasifikasi eksepsi diverifikasi tarikan segar 32 ISR / 432 eligible / 148 awarded (15 Nov).*
