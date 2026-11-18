# STUDI KOHORT 2026-11-17 — Tarikan Segar (run-11): Kohort Berdiri, Diskriminator Penentu Ketiga, Resep Juara Segar

> Satu baris: **lapangan tidak runtuh dan tidak meledak — ia MENEBAL: pasokan 517 pertanyaan/hari (3× era 14 Nov), kohort inti 12 agen 5/5 snapshot bertahan semua, dan diskriminator K-1/K-2 BERTAHAN (gap lantai penuh stabil tiga run berturut) — yang berubah besar adalah KECEPATAN VERIFIKASI (latensi Pioneer segar 14,3 dtk → 178,7 dtk) dan KEPADATAN MARATHON (5,85 slot/pertanyaan panel, naik dari 3,17).**
> Tarikan: 2026-11-17 00:20–01:21 UTC (07:20–08:21 WIB), read-only lewat klien `trued`. Artefak: `belajar-2026-11-17/run11-0717/` (`pull11.py`, `analyze11.py`, `analysis11.json`, `compare14.json` = transkrip verbatim angka 14 Nov). Pembanding: `STUDI-KOHORT-2026-11-14.md` + `KORPUS-JUARA-2026-11-14.md` + run-9 (16 Nov 18:37 WIB) + run-10 (17 Nov 02:37 WIB).

## Metode & frame (sebanding studi 14 Nov)

- **Frame**: (a) 48 ISR settled pertama urutan aktivitas listing (frame panel); (b) 80 ISR terbaru sejak run-10 mulai (cut 2026-11-16T19:37Z); (c) 48 ISR monitored run-10. Union sesudah dedup: **171 pertanyaan**, **9.483 ISO** (9.400 eksternal): verified 2.124 · falsified 942 · abandoned 1.225 · revealed 5.134 · intent 58.
- **Kegagalan tarikan (jujur)**: 2 panggilan gagal sesudah 4 retry — detail 1 pertanyaan (`fd93556b…`) + daftar ISO 1 pertanyaan (`79de0e3f…`); 169/171 pertanyaan lengkap. Dua percobaan tarikan awal gugur total (timeout di panggilan state/leaderboard) sebelum helper retry menangkap `SystemExit` diperbaiki; percobaan ketiga tuntas dalam 61 menit (API lambat: detail 1,5–11 dtk/panggilan pada studi lama, konsisten).
- **Snapshot leaderboard untuk kohort**: 5 tarikan — 14 Nov 02:40, 14 Nov 10:37, run-9 16 Nov 18:37, run-10 17 Nov 02:37, run-11 17 Nov 07:20 (semua WIB). "Muncul N/5" = jumlah snapshot tempat agen ada di top-100 eksternal.
- **Bias yang sama seperti 14 Nov, dinyatakan ulang**: frame settled-pertama bias ke pertanyaan tua (umur median sampel panel studi lama 29,5 hari); frame segar bias ke gelombang massal; angka "rate" frame TIDAK sebanding dengan rate papan (lihat F6).

## Cermin kita (tarikan sesi ini, tak berubah)

Saldo **−1,8788**, lifetimeEarned **0**, Expertise **0**, RAR **118** (reliability −5 · availability 29 · reputation 94), jobs **34**. Tidak ada satu pun angka cermin yang bergerak sejak run-10 — semua temuan di bawah adalah tentang lapangan, bukan tentang kita.

## F1 — Pasokan: 517/hari sejak 14 Nov, dan gelombang kini datang PAGI

- Listing total **3.131** pertanyaan (14 Nov: 1.462). ID baru sejak 14 Nov: **1.669 dalam 3,23 hari = 517,0/hari** (studi 14 Nov mengukur era segarnya sendiri 172,6/hari → pasokan ±3× lipat). Penanya unik era ini **344**, pangsa rumah **0,0%** — pasokan tetap organik penuh.
- Sejak run-10 (4,7 jam): **+340 pertanyaan baru** dari 115 penanya; histogram jam (WIB): 03:00 = 68 · 04:00 = 47 · 05:00 = 68 · **06:00 = 104** — gelombang massal bergeser dari pola 01:00 (run-10) ke **blok pagi 03:00–07:00 WIB**. Pola denyutnya tetap (gelombang, bukan aliran rata), jamnya bergerak.
- Lantai top-100 eksternal: **1.842** coins (14 Nov: 564 → ×3,3; run-10: 1.819 → +23 saja dalam jendela ini). Agen ≥400 coins: **89** (14 Nov: 91; run-10: 89) — papan atas menebal di puncak, bukan melebar.
- **ADOPSI-CATATAN**: jendela rilis segar untuk dibaca di siklus belajar berikutnya = blok pagi WIB, bukan tengah malam; angka pasokan 517/hari adalah konteks semua hitungan EV serve ke depan.

## F2 — Kohort berdiri: 12 agen inti 5/5, panel lama NOL yang gugur dari papan

**Kohort inti run-11** (muncul 5/5 snapshot + hadir run-10 & run-11; diurutkan peringkat kini; korpus mereka = `KORPUS-JUARA-2026-11-17.md`):

| Agen | # kini | Coins | Δ vs 14 Nov | Wins | Verified di frame |
|---|---|---|---|---|---|
| Febriyan | 8 | 24.558 | +11.807 | 968 | 38 |
| HIMANSHU | 9 | 23.805 | +19.385 | 1.040 | 41 |
| Mauldrop | 10 | 19.111 | +10.449 | 732 | 42 |
| Gufran The Legend | 11 | 15.786 | +11.070 | 679 | 39 |
| GaBot | 12 | 14.637 | +10.128 | 573 | 26 |
| megumii | 13 | 14.549 | +8.991 | 510 | 41 |
| Danis | 14 | 13.604 | +11.950 | 359 | 28 |
| Adam Reinhard | 15 | 12.792 | +6.043 | 490 | 28 |
| zoya khan | 16 | 12.315 | +10.984 | 517 | 28 |
| SyntaxZ | 19 | 11.586 | +7.159 | 594 | 20 |
| kuru | 21 | 10.785 | +7.952 | 565 | 19 |
| gisa | 22 | 9.980 | +4.493 | 547 | 27 |

- **Panel 12 studi 14 Nov: 12/12 masih di top-100.** Yang tergelincir keluar dari inti (masih di papan, bukan gugur): chirpy #34 (7.501), Rodeo #32 (7.839), can-earn? #30 (8.250), Discord 1 #36 (7.337) — keempatnya muncul 5/5 snapshot tapi kalah laju koin dari inti baru. Dari top-15 eksternal 14 Nov, yang jatuh paling jauh: DodolDuren #18→#54, Moden Gos #19→#59, Añoñi ;-) #21→#61.
- **Pendatang konsisten** (absen di kedua snapshot 14 Nov, hadir run-9 + run-10 + run-11): **24 agen** — teratas: **Rohit Prajapati #18** (11.713), **Google News #20** (11.163), **Love8 #28** (8.532), hina #31 (8.016), DegenXBT #39, Canna Catokan #41. Pendatang baru sejak run-10 saja: peng #83, dike008.love #97.
- **Pendaki ≥+300 sejak run-10 (4,7 jam)**: hanya 4 — Lin Jason **+1.622** (→#43), zoya khan +580, hina +510, Love8 +390. Bandingkan run-10: 24 pendaki ≥+300 dalam 8 jam. Laju pendakian melambat di jendela ini walau pasokan naik — koin menumpuk di pemain yang sudah di atas (semua inti Δ positif besar vs 14 Nov).
- **ADOPSI-CATATAN**: daftar pantau kohort diperbarui ke 12 inti di atas + Rohit/Google News/Love8 sebagai lapis kedua; chirpy/Rodeo/can-earn?/Discord 1 turun status dari "inti" ke "papan".

## F3 — Pioneer: tetap milik eksternal (96,8%), tapi verified-pertama kini 12× lebih lambat

- Pioneer teramati di sampel: **121 eksternal vs 4 rumah** (96,8% eksternal; 14 Nov: 93,1% panel / 94,4% era segar). Dari 29 pertanyaan segar yang sudah punya verified, **29/29 eksternal**.
- **Latensi verified-pertama pertanyaan segar: median 178,7 dtk (n=38), hanya 1/38 di bawah 10 dtk.** Run-10 pada frame yang sama: median 14,3 dtk, 35/80 sub-10-dtk. Studi 14 Nov: median eksternal 9,1 dtk. (Seluruh sampel, semua umur: median 4,8 dtk, n=119 — angka itu didominasi pertanyaan tua dan TIDAK sebanding.)
- **HIPOTESIS (mekanisme konsisten, belum dibuktikan)**: pasokan ±3–4× lipat (517/hari; 340 pertanyaan dalam 4,7 jam jendela ini) menjenuhkan antrean panel verifier, sehingga verified pertama mendarat jauh lebih lambat pada pertanyaan segar. Bias sensor bekerja MELAWAN arah temuan (pertanyaan segar yang lambat belum punya verified → terpotong dari n) — median sejati bisa lebih tinggi lagi.
- Akibat praktis bila hipotesis benar: keunggulan "menjawab dalam hitungan detik" menyusut nilainya; yang menentukan Pioneer kini lebih ke **siapa yang jawabannya lolos panel pada gelombang verifikasi pertama**, bukan siapa paling cepat mengetik. Ini menyambung pelajaran run-10 ("kecepatan bukan pembeda lagi") dengan angka yang lebih keras.
- **USULAN (berlabel, tidak dieksekusi)**: siklus belajar berikutnya mengukur latensi verified-pertama per jam rilis untuk memisahkan efek kejenuhan antrean dari efek jam.

## F4 — Marathon: slot per pertanyaan panel naik 3,17 → 5,85

- Di 171 pertanyaan sampel: **732 slot awarded** (719 eksternal); pada 95 pertanyaan yang `marathonConcluded`, rerata **7,63/pertanyaan** (terinflasi pertanyaan monitored tua); pada **46 pertanyaan panel yang concluded: 5,85/pertanyaan** — bandingkan panel settled 14 Nov: **3,17**. Kepadatan bayaran Marathon per pertanyaan naik ±85%.
- Pemenang Marathon terbanyak di sampel: Hermawan Kwan 24, SyntaxZ 20, Rohit Prajapati 20, Gufran 19, HIMANSHU 19, Google News 17, Mauldrop 16, zoya khan 16, gisa 15. **Batas ukur**: 166/732 (22,7%) slot awarded menunjuk ISO yang tidak ada di daftar ISO tertarik (endpoint ISO tampaknya memotong daftar pada pertanyaan raksasa) — pemiliknya tak terbaca; peringkat pemenang di atas adalah peringkat dari 77,3% yang terbaca.
- Versi aturan pertanyaan sampel: v3 = 150, v2 = 20, tak terbaca 1 — v3 kini dominan mutlak.
- **ADOPSI-CATATAN**: Marathon makin menjadi sel bayar bervolume (konsisten dengan prioritas kelas terkunci Marathon > Pioneer); Pioneer tetap ada tapi antrean verifikasinya melambat (F3).

## F5 — DISKRIMINATOR: penentu ketiga — BERTAHAN, tidak runtuh, tidak menguat

Pengukuran persis definisi studi lama (K-1 = densitas sitasi > 0; K-2 = rasio sitasi terikat; lantai penuh = K-1 ∧ K-2). Lantai K-2 yang berlaku tetap **0,30** (keputusan user 06:12) — bagian ini MENGUKUR, bukan mengubah.

**Frame panel-48 (n verified 673 / falsified 350):**

| Ukuran | Verified | Falsified | Gap | 14 Nov (korpus/panel) |
|---|---|---|---|---|
| K-1 lolos | 62,1% | 30,9% | **+31,2pp** | +28,7pp (korpus) |
| Lantai penuh @0,30 | 22,1% | 14,3% | **+7,8pp** | +4,4pp (korpus) · +9,4pp (panel studi) |
| Lantai penuh @0,15 | 44,1% | 24,3% | **+19,8pp** | +24,8pp (korpus) |
| Dalam-K-1 @0,15 | 71,1% | 78,7% | **−7,6pp** | +4,6pp (korpus) |
| d karakter / densitas / rasio | — | — | **0,516 / 0,356 / 0,348** | 0,292 / 0,288 / 0,262 (panel) |
| URL≥1 gap · header gap | — | — | **+39,3pp · +1,1pp** | +32,6pp · — |

**Frame gabungan run-11 (n verified 2.081 / falsified 929) — rangkaian tiga run:**

| Ukuran | Run-9 | Run-10 | Run-11 | Vonis arah |
|---|---|---|---|---|
| K-1 saja (gap) | +24,9pp | +20,9pp | **+25,5pp** | terkuat, melebar lagi |
| Lantai penuh @0,30 (gap) | +6,9pp | +4,6pp | **+5,3pp** | stabil kecil |
| Lantai penuh @0,15 (gap) | +17,9pp | +15,4pp | **+17,3pp** | stabil |
| Dalam-K-1 @0,30 | — | −8,2pp | **−10,6pp** | negatif |
| Dalam-K-1 @0,15 | −2,5pp | −0,5pp | **−3,9pp** | negatif 3 run berturut |
| d karakter / densitas / rasio | 0,387/0,242/0,228 | 0,376/0,202/0,205 | **0,430/0,257/0,244** | sedikit melebar lagi |

- **Vonis penentu ketiga**: dua "selisih material" run-9/run-10 ternyata bergerak MELAWAN acuan korpus 14 Nov, bukan tren yang berlanjut — pada run-11 gap @0,15 kembali ke +17,3pp (di antara run-9 +17,9 dan run-10 +15,4) dan gap @0,30 stabil di +5,3pp. **Diskriminator BERTAHAN sebagai saringan anti-spesies-gagal-kita; ia tidak runtuh.** Yang konsisten tiga run berturut justru sisi negatifnya: **di dalam lolos-K-1, ambang K-2 tidak memisahkan verified dari falsified pada kedua ambang** (dalam-K-1 negatif terus) — nilai tambah K-2 sesudah K-1 tetap TIDAK terbukti, persis seperti keraguan studi 14 Nov butir B2, kini dengan tiga run bukti.
- **Peringatan frame (mengulang run-10, tetap berlaku)**: frame panel-48 dan frame gabungan menjawab pertanyaan berbeda (panel = pertanyaan settled lama; gabungan didominasi monitored+segar). Angka panel run-11 terlihat "lebih kuat" dari 14 Nov sebagian karena falsified panel kini lebih kurus (median 3.405 karakter, densitas median 0,0) — komposisi sampel, bukan hukum arena.
- **Di dalam kohort inti sendiri, lantai hampir tidak memisahkan sama sekali** (korpus: lantai penuh @0,30 verified 26,5% vs falsified 27,6%, gap **−1,1pp**; K-1 gap hanya +12,5pp; rincian di berkas korpus). Kegagalan agen top bersifat semantik, bukan mekanik — lantai kita memang dirancang membunuh spesies gagal KITA, bukan meniru cara juara gagal.

## F6 — Rate verdict frame: JANGAN dibaca sebagai rate arena

Pooled frame gabungan: verified 2.081 / (2.081+929) = **69,1%**; median rate per-agen (n≥5) 78,8%. Angka ini terinflasi frame monitored (pertanyaan tua yang disapu karena ramai pemenang) — studi 14 Nov sudah membuktikan rate sejati per-agen dari riwayat pekerjaan penuh jauh lebih rendah (Febriyan 35,3% saat itu). Tidak ada tarikan riwayat per-agen di run ini; rate sejati kohort TIDAK diukur ulang — dinyatakan sebagai celah, bukan diisi angka frame.

## F7 — Abandoned naik: 12,9% dari ISO sampel

Abandoned 1.225/9.483 = **12,9%** (14 Nov: 9,6%). Sejalan dengan pasokan yang menebal: lebih banyak jawaban menggantung tak terverifikasi pada sampel yang sama. Revealed masih 5.134 — antrean verifikasi memang panjang (konsisten F3).

## Daftar negatif run-11 (yang TIDAK ditemukan / tidak berubah)

- **Nol agen panel lama gugur dari top-100** — tidak ada kematian kohort; yang ada hanya penggelinciran peringkat relatif.
- **Pangsa rumah pada pasokan baru tetap 0,0%** dan Pioneer rumah hanya 4/125 — rumah tidak merebut sel bayar lebih banyak; tidak ada perubahan rezim rumah yang terdeteksi.
- **Innovator tetap tidak terukur publik** (tidak ada penanda per-jawaban) — sama seperti 14 Nov; label slot "—" bukan bukti bukan-Innovator.
- **E3 (penutup evasif) tetap 0,0%** di korpus kohort verified maupun falsified — pola racun kita tidak menular ke lapangan; gerbangnya tetap murah dan spesifik.
- **Penamaan kebaruan eksplisit di penutup tetap langka** (4,0% verified kohort) — adopsi QUALITY v3 butir (e) yang direformulasi (kebaruan substantif, penamaan = anjuran) cocok dengan lapangan; lihat korpus §5.
- Tidak ada versi aturan baru selain dominasi v3 (150/171); tidak ada perubahan cermin kita satu pun.

## Pelajaran (eksplisit — yang berubah dan akibatnya buat workflow kita)

1. **Diskriminator selesai diperdebatkan untuk sekarang**: tiga run berturut gap lantai penuh stabil (@0,15 ±15–18pp, @0,30 ±5–7pp) dan K-1 tetap yang terkuat — energi siklus berikutnya lebih bernilai di C5/semantik daripada mengutak-atik lantai mekanik; K-2 tetap 0,30 bukan karena ia terbukti menambah daya pisah di dalam K-1 (tiga run: tidak), melainkan sebagai rem racun sitasi kita sendiri.
2. **Kecepatan verifikasi, bukan kecepatan menjawab, kini kemacetannya**: latensi verified-pertama segar naik ±12× saat pasokan 3× lipat — strategi Pioneer yang mengandalkan "jawab duluan" kehilangan tuasnya; seleksi target (item 1) dan kesabaran antrean lebih menentukan daripada latensi generasi kita.
3. **Kohort menebal, tidak berganti**: 12/12 panel lama bertahan di papan dan inti baru semuanya wajah 14 Nov juga — resep juara bersifat STABIL lintas 3 hari (korpus §2: median bergeser <10% di hampir semua fitur), jadi QUALITY v3 tidak perlu ditulis ulang dari data ini; yang bergerak adalah fenotipe per-agen (HIMANSHU memanjang, megumii melonggar) — contek resep AGREGAT, bukan satu agen.
4. **Marathon makin padat bayarannya** (5,85 vs 3,17 slot/pertanyaan panel) sementara Pioneer melambat — urutan prioritas kelas terkunci (Marathon > Pioneer) makin didukung data lapangan, bukan makin usang.
5. **Pasokan berdenyut di pagi WIB sekarang** (blok 03:00–07:00) — jendela baca siklus belajar dan jendela pantau serve (bila fase berubah atas kata user) digeser mengikuti denyut ini, bukan jam 01:00 era run-10.

*Berkas pasangan: `KORPUS-JUARA-2026-11-17.md`. Angka mentah: `belajar-2026-11-17/run11-0717/analysis11.json`. Tidak ada keputusan terkunci yang diubah berkas ini (K-2 0,30 · C5 shadow · prioritas Marathon > Pioneer tetap); saran perubahan hanya terbit sebagai USULAN berlabel di F3.*
