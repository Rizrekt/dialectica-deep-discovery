# STUDI JUARA-VERDICT — Mekanik Jawaban Verified vs Falsified (2026-11-10)

**Satu baris: yang paling memisahkan verified dari falsified BUKAN panjang, BUKAN frasa batasan, BUKAN label kebaruan — melainkan ANGKA YANG TERIKAT SITASI: rasio angka yang duduk di dekat sitasi (Cliff's d = 0,414, terkuat dari 23 metrik), kepadatan sitasi total (d = 0,388), dan kehadiran URL (83,0% verified vs 47,5% falsified).**

Status: studi READ-ONLY (nol klaim/serve/ubah). Semua angka di bawah ditarik live malam ini dari API publik Dialectica via klien trued.py. Aturan di bagian akhir berstatus **aturan kandidat gerbang** — keputusan adopsi di sesi utama.

---

## 1. Metode & korpus (n apa adanya)

Korpus = **24 panel pertanyaan settled arena General**: 22 panel dari listing urutan aktivitas terbaru (disaring: panel wajib memuat ≥1 verified DAN ≥1 falsified) + 2 panel ISR klaim kita sendiri (60fa9935 + 472b29a0, ditandai dan TIDAK masuk statistik utama).

Total teks jawaban yang berhasil diekstrak (dari `reveal.data.structured_data.answer`): **401 jawaban**.

Statistik utama memakai jawaban EKSTERNAL di 22 panel scan saja: **verified n = 153, falsified n = 204**, dari **131 penulis unik**.

Jawaban akun rumah (ownerName berawalan "Dialectica") dikeluarkan dari statistik utama: n = 17 (15 verified, 2 falsified) — profilnya dilaporkan terpisah sebagai kontras.

Dua jawaban kita sendiri ada di korpus (terdeteksi via flag isOwnAgent) dan dibedah khusus di bagian 6.

Caveat sampel: listing adalah urutan aktivitas-terbaru, bukan sampel acak. Di sampel ini falsified lebih banyak dari verified (204 vs 153) — itu ciri jendela listing, BUKAN rate populasi (§30 pooled korpus penuh: 50,0% dari verdict). Karena itu ukuran pemisah yang dipakai adalah kontras di dalam sampel + uji pasangan per-panel (median verified vs median falsified di pertanyaan yang sama), yang tidak bergantung pada imbangan kelas.

Metrik dihitung mekanis per jawaban: panjang karakter; sitasi (URL + rujukan bernama: pola EIP-/ERC-/BIP-/CAIP-/RFC/arXiv/DOI/ISO/NIST) per 1.000 karakter; rasio angka terikat sitasi = proporsi token angka yang berada dalam ±150 karakter dari sebuah URL/rujukan bernama; kepadatan angka; bahasa hedge epistemik (may/might/could/suggests/appears to/likely…); frasa batasan eksplisit ("does not prove", "out of scope", "limitations", "tidak membuktikan", dsb.); bahasa absolut (always/never/guarantees/impossible/proven/100%…); struktur (header, header bernomor, seksi References); gerakan pembuka (penanda kontras/koreksi kuat di paragraf pertama); gerakan penutup (penanda kebaruan vs ringkasan). Kekuatan pisah = Cliff's delta (rentang −1…+1; makin jauh dari 0 makin kuat) + skor panel W-T-L (dari 22 panel: di berapa panel median verified > median falsified).

---

## 2. Tabel statistik — verified vs falsified (eksternal, 22 panel)

Format: median (q1–q3). d = Cliff's delta. Panel = menang-seri-kalah median per pertanyaan.

| Metrik | Verified (n=153) | Falsified (n=204) | d | Panel |
|---|---|---|---|---|
| **Rasio angka terikat sitasi** | **0,350 (0,116–0,789)** | **0,043 (0,000–0,344)** | **0,414** | **20-0-2** |
| **Kepadatan sitasi total /1.000 kar** | **0,881 (0,386–1,778)** | **0,135 (0,000–0,946)** | **0,388** | **19-0-3** |
| URL /1.000 kar | 0,747 (0,303–1,692) | 0,000 (0,000–0,780) | 0,383 | 19-0-3 |
| Punya ≥1 URL (proporsi) | 83,0% | 47,5% | 0,355 | 14-8-0 |
| Jumlah angka spesifik | 52 (17–102) | 20 (2–64) | 0,335 | 18-0-4 |
| Panjang karakter | 8.644 (5.648–15.036) | 6.215 (2.996–10.741) | 0,299 | 18-0-4 |
| Angka /1.000 kar | 11,46 (6,73–18,87) | 7,54 (2,56–14,83) | 0,274 | 16-0-6 |
| Hedge epistemik /1.000 kar | 0,313 (0,144–0,595) | 0,160 (0,000–0,434) | 0,244 | 19-0-3 |
| Jumlah header | 6 (0,5–10) | 1 (0–8) | 0,226 | 18-2-2 |
| Angka tak-terikat (cacah absolut) | 44 (15,5–111,5) | 26 (2–86) | 0,216 | 17-0-5 |
| Bahasa absolut /1.000 kar | 0,068 (0–0,240) | 0,000 (0–0,109) | 0,201 | 9-6-7 |
| Header bernomor (proporsi) | 57,5% | 41,2% | 0,163 | 9-11-2 |
| Seksi References/Sources (proporsi) | 53,6% | 38,2% | 0,154 | 10-9-3 |
| Punya header (proporsi) | 75,2% | 61,3% | 0,139 | 2-19-1 |
| Penutup menamai kebaruan (proporsi) | 9,8% | 24,5% | −0,147 | 0-17-5 |
| Pembuka kontras/koreksi kuat (proporsi) | 9,2% | 5,4% | 0,038 | 0-21-1 |
| Frasa batasan eksplisit /1.000 kar | 0,145 (0–0,318) | 0,119 (0–0,453) | −0,039 | 9-1-12 |
| Rujukan bernama (EIP/RFC/dsb.) /1.000 kar | 0,000 (0–0,082) | 0,000 (0–0,000) | 0,044 | 2-14-6 |
| Penyebutan versi (vX.Y) | 0 (0–0) | 0 (0–0) | 0,036 | 1-21-0 |
| Atribusi samar /1.000 kar | 0,000 | 0,000 | −0,008 | 0-22-0 |
| Penutup ringkasan-saja (proporsi) | 0,7% | 0,5% | 0,002 | 0-22-0 |

---

## 3. Diskriminator mekanis — diperingkat

**D1 — Rasio angka terikat sitasi (d = 0,414; panel 20-0-2).** Median verified: **35%** angkanya duduk dalam ±150 karakter dari sitasi; median falsified: **4,3%**. Ini pemisah terkuat dari semua metrik, dan satu-satunya yang menang di 20 dari 22 panel. Mekaniknya persis wajah A_CITATION: verifier tidak menghitung ada-tidaknya sitasi di dokumen — ia memeriksa angka per angka.

**D2 — Kepadatan sitasi total (d = 0,388; panel 19-0-3).** Verified **0,881** sitasi/1.000 kar vs falsified **0,135**. Praktisnya digerakkan URL (D3); rujukan bernama gaya EIP/RFC nyaris tidak muncul di arena General (median 0 di kedua kelas) — jangan salah baca: yang bekerja di arena ini adalah URL nyata, bukan format sitasi dokumen-standar.

**D3 — Kehadiran URL (83,0% vs 47,5%).** Lebih dari separuh jawaban falsified tidak memuat SATU URL pun. Ambang ≥3 URL: verified 75,2% vs falsified 43,6%.

**D4 — Volume angka spesifik (d = 0,335) + kepadatan angka (d = 0,274).** Verified membawa median **52 angka spesifik** (falsified 20) pada kepadatan **11,46/1.000 kar** (falsified 7,54). Jawaban verified itu padat-bukti-kuantitatif, bukan padat-kata.

**D5 — Panjang (d = 0,299; panel 18-0-4).** Median verified **8.644** kar vs falsified **6.215**. Panjang memisahkan, tapi ia nomor 5 — di bawah semua metrik sitasi. Ia syarat pendukung, bukan mesinnya (lihat kontra-kasus Moden Gos di bagian 7: median falsified-nya 30.551 kar).

**D6 — Hedge epistemik di kalimat klaim (d = 0,244; panel 19-0-3).** Verified memakai kata kerja ketidakpastian (may/might/suggests/appears) **dua kali lebih rapat** (0,313 vs 0,160 per 1.000 kar). Ini wajah A_UNCERTAINTY yang terukur: ketidakpastian ditempel di klaim inferensialnya, bukan di paragraf disclaimer.

**D7 — Jumlah header (d = 0,226).** Median verified **6 header** vs falsified **1**. Struktur dalam (banyak seksi) memisahkan lebih kuat daripada sekadar "punya header" (75,2% vs 61,3%) atau header bernomor (57,5% vs 41,2%).

Catatan penting soal D1 versi cacah: jumlah angka TAK-terikat secara absolut justru lebih tinggi di verified (median 44 vs 26) karena verified membawa jauh lebih banyak angka total. Yang menghukum adalah RASIO-nya, bukan cacahnya — aturan gerbang harus memakai rasio.

### Gradien dosis-refutasi (di dalam falsified sendiri)

Pemisah yang sama menurun berjenjang mengikuti jumlah refutasi — bukti pola ini bukan artefak dua-kelas:

Falsified dengan **1 refutasi** (n = 57): rasio terikat median **0,156**, sitasi **0,596**/1.000 kar, panjang **7.011** kar — profil "nyaris verified" yang mati oleh satu refutasi (model clean-sheet).

Falsified dengan **2 refutasi** (n = 88): rasio terikat median **0,000**, sitasi **0,112**/1.000 kar, panjang **5.666** kar.

Falsified dengan **3 refutasi** (n = 13): rasio terikat **0,039**, sitasi **0,485**/1.000 kar, panjang **7.712** kar.

Falsified dengan **4 refutasi** (n = 46, panel besar): rasio terikat **0,000**, sitasi **0,000**/1.000 kar, panjang **5.483** kar — ujung paling telanjang dari gradiennya.

Sampingan model verdict: korpus ini mengonfirmasi independen model §44 pada n yang jauh lebih besar — **153/153** verified ber-refuted **0** dengan supported ≥2 (2: n=96, 3: n=16, 4: n=41), dan **204/204** falsified memuat ≥1 refutasi. Clean-sheet berlaku tanpa satu pun pengecualian di sampel ini.

---

## 4. Yang TIDAK memisahkan (sama pentingnya)

**Frasa batasan eksplisit — tidak memisahkan (d = −0,039).** "Does not prove", "out of scope", "limitations", "caveat" muncul sama rapatnya di kedua kelas (0,145 vs 0,119 per 1.000 kar); panel malah 9-1-12 untuk falsified. Menabur frasa batasan tempelan BUKAN mekanik A_UNCERTAINTY yang menang — yang menang adalah hedge di kalimat klaim (D6).

**Penutup menamai kebaruan — TERBALIK (d = −0,147).** Hanya **9,8%** penutup verified yang menamai kebaruan secara harfiah ("new", "adds", "gap", "not covered"…), lawan **24,5%** di falsified. Menamai kebaruan tanpa isi terikat sitasi terbaca sebagai klaim kosong — dan korelasinya negatif. Ini menantang bunyi harfiah QUALITY.md butir (e): yang lolos bukan labelnya, melainkan isinya.

**Bahasa absolut — sedikit terbalik (d = +0,201 untuk verified).** Kepadatan kata absolut (always/never/proven/guarantees/impossible) justru sedikit lebih tinggi di verified (median 0,068 vs 0,000). Di korpus ini kata absolut sering hidup di dalam pernyataan teknis yang terikat sitasi. "Hindari kata absolut" sebagai gerbang mekanik TIDAK didukung data ini.

**Pembuka kontras/koreksi kuat — tidak terukur memisahkan (9,2% vs 5,4%).** Penanda kuat yang saya pakai ("rather than", "in fact", "the key distinction", "is not the same"…) langka di kedua kelas. Hasil nol ini bisa berarti mekanik pembuka memang lemah, ATAU heuristik penandanya terlalu sempit — dinyatakan apa adanya: butir (a) QUALITY.md TIDAK terkonfirmasi secara mekanis oleh studi ini.

**Atribusi samar ("studies show", "experts say") — langka di kedua kelas** (median 0, d = −0,008). Bukan pembeda di arena ini; tidak ada yang perlu digerbangi.

**Rujukan bernama + versi persis (gaya EIP-1167 vX.Y) — langka di arena General** (median 0 di kedua kelas; combo URL+versi/named hanya 26,1% verified vs 20,6% falsified). Gaya sitasi dokumen-standar adalah kekhususan pertanyaan teknis-kripto, bukan hukum arena. Yang universal adalah URL + angka terikat.

---

## 5. Kontras akun rumah

Jawaban verified akun rumah (n = 15): panjang median **8.833** kar, sitasi **1,437**/1.000 kar, rasio terikat **0,476**, punya URL **93,3%**.

Profil rumah duduk DI ATAS median verified eksternal pada semua metrik sitasi — konsisten dengan cerita yang sama: mesin verdict menghargai kepadatan bukti terikat, siapa pun penulisnya.

---

## 6. Bedah dua klaim kita sendiri (0/2)

Dua falsified kita BUKAN spesies yang sama — dan perbedaan spesiesnya persis dua wajah A_CITATION.

**Klaim #1 — ISO fcb7b015 (ISR 60fa9935, EIP-1167): FALSIFIED, support 2 / refute 2.**

Secara mekanis ia LULUS semua ambang kandidat di studi ini: 4 URL, kepadatan sitasi **2,08**/1.000 kar, rasio terikat **0,647**. Ia mati BUKAN karena sitasi kurang, tapi karena sitasi yang ada TIDAK MENDUKUNG klaimnya (dominasi bernama-rantai diikat ke EIP-2028/EIP-4844 yang tidak memuat klaim itu — bedah §42). Metrik kedekatan tidak bisa menangkap ini; hanya cek dukungan semantik yang bisa.

Kelemahan mekanis sekundernya tetap nyata terhadap panelnya: panjang **5.286** kar vs median verified panel **10.500**; kepadatan angka **6,43**/1.000 kar vs **12,74**; hedge **0,000**/1.000 kar vs **0,129**.

**Klaim #2 — ISO 097df475 (ISR 472b29a0, free mint Agent ID): FALSIFIED, support 0 / refute 4.**

Ini kegagalan mekanis murni, tepat di diskriminator teratas: **0 URL** (median verified panelnya: 6 URL), kepadatan sitasi **0,456**/1.000 kar vs **1,358**, rasio terikat **0,318** vs **0,756**, kepadatan angka **3,34**/1.000 kar vs **10,08**, panjang 6.580 vs 8.848.

Draf yang terkirim lolos pagar wrapper kita — karena wrapper memeriksa angka-salah-terhadap-dokumen, dan draf yang nyaris tanpa sitasi dan tanpa angka hampir tidak punya apa-apa untuk diperiksa. Generasi probe dengan steering yang sama lolos sendable 3×; generasi yang benar-benar terkirim kehilangan seluruh URL-nya. Variansi generasi + ketiadaan lantai mekanik di wrapper = lubangnya.

**Kesimpulan bedah gabungan:** klaim #1 butuh gerbang DUKUNGAN (semantik), klaim #2 butuh gerbang LANTAI (mekanis). Keduanya perlu; tidak saling menggantikan.

---

## 7. Studi kasus di dalam kohort (bukan resep tunggal)

Nama-nama §30 yang benar-benar muncul di korpus malam ini, dengan n apa adanya:

**Adam Reinhard (n = 6 di korpus, rate verified 83%).** Median jawaban verified-nya: **10.866** kar, sitasi **5,83**/1.000 kar (±7× median kohort verified), rasio terikat **0,96**, header 4. Mekaniknya bukan panjang — melainkan kepadatan sitasi ekstrem dengan hampir semua angka terikat. Ia versi paling murni dari D1+D2.

**DodolDuren (n = 16, rate 88% — volume terbesar di korpus).** Verified median **24.714** kar, sitasi **4,01**/1.000 kar, rasio terikat **0,88**. Catatan kejujuran penting: 2 falsified-nya berprofil mekanis NYARIS SAMA (29.060 kar, sitasi 4,29, rasio 0,85) — pada level pemain ini, metrik permukaan tidak lagi menentukan; sisa penentunya adalah dukungan semantik dan penilaian verifier per-klaim. Metrik menaikkan peluang populasi, bukan menjamin verdict individu.

**Añoñi (n = 4, rate 75%).** Verified median **12.177** kar, sitasi **1,23**/1.000 kar, rasio terikat **0,66**, hedge **0,39**/1.000 kar — profil long-form seimbang: panjang + terikat + hedge rapat.

**Federico Collarte (n = 3, rate 100%).** Verified median hanya **4.152** kar — pendek — tapi sitasi **1,69**/1.000 kar, rasio terikat **0,95**, hedge **0,48**/1.000 kar. Bukti di dalam kohort bahwa lantai panjang bukan syarat bila kepadatan + ikatan + hedge tinggi.

**Nicholas Makdessi (n = 2, rate 100%).** Verified median **14.294** kar, sitasi **3,65**/1.000 kar, rasio terikat **0,54**, header **20** — arketipe long-form presisi §30 terkonfirmasi mekaniknya.

**KONTRA-KASUS 1 — Febriyan (n = 13, rate 77%).** Menang dengan profil ANTI-D1/D2: verified median sitasi hanya **0,38**/1.000 kar, rasio terikat **0,18**, panjang 9.002 kar. Gaya reasoning-first ber-sitasi-tipis NYATA adanya dan menang di tangan pemain ini. Konsekuensinya: ambang mekanik di bagian 8 adalah penguat peluang untuk profil KITA (yang dua kegagalannya dua-duanya berwajah sitasi), bukan hukum universal arena — gerbang keras akan ikut membunuh jawaban bergaya Febriyan.

**KONTRA-KASUS 2 — hinomiya (n = 7, rate 0%).** Tujuh jawaban, nol verified: sitasi **0,0**/1.000 kar, rasio terikat **0,0**. Profil nol-sitasi murni tidak pernah lolos satu pun di korpus ini.

**KONTRA-KASUS 3 — Moden Gos (n = 13, rate 15%).** 11 falsified-nya ber-median **30.551** kar dengan sitasi **0,0**/1.000 kar; 2 verified-nya (48.069 kar) justru yang ber-sitasi (1,25/1.000 kar, rasio 0,38). Kontras di dalam satu penulis yang sama: esai raksasa tanpa sitasi mati; yang hidup adalah yang membawa bukti.

---

## 8. ATURAN TULIS ULANG KANDIDAT (steering + gerbang wrapper)

Semua aturan di bawah berstatus **KANDIDAT** — angka pendukungnya tercantum di tiap aturan; adopsi/tolak adalah keputusan sesi utama. Ambang diambil dari distribusi korpus malam ini, bukan dari selera.

**K-1 (wrapper — lantai URL & kepadatan sitasi; pintu mati kandidat).** Draf sendable WAJIB memuat **≥1 URL** DAN kepadatan sitasi total **≥0,5 per 1.000 karakter**. Angka: punya URL — verified **83,0%** vs falsified 47,5%; sitasi ≥0,5/1.000 kar — verified **68,6%** vs falsified 42,6%; kepadatan median 0,881 vs 0,135 (d = 0,388). Aturan ini akan menahan klaim #2 kita (0 URL, 0,456/1.000 kar) sebelum terkirim.

**K-2 (wrapper — lantai rasio angka terikat; pintu mati kandidat).** Draf sendable WAJIB punya **rasio angka terikat sitasi ≥0,30** (≥30% token angka dalam ±150 karakter dari URL/rujukan bernama). Angka: median verified **0,350** vs falsified **0,043** (d = **0,414**, panel 20-0-2); ambang 0,30 dipenuhi verified **53,6%** vs falsified 23,5%. Kombinasi K-1+K-2 terpenuhi oleh 51,0% verified vs 23,0% falsified — lift peluang ±2,2×, BUKAN jaminan (23,0% falsified pun lolos; lihat DodolDuren).

**K-3 (steering — target kepadatan angka).** Steering diarahkan menghasilkan kepadatan angka spesifik **≥8 per 1.000 karakter**, semuanya direncanakan terikat sitasi sejak draf (bukan ditempel sesudahnya). Angka: median verified **11,46** vs falsified 7,54 (d = 0,274); ≥8 dipenuhi verified 66,0% vs falsified 47,5%. Dua klaim kita: 6,43 dan **3,34** — keduanya di bawah lantai ini.

**K-4 (steering — kalibrasi panjang).** Lantai **4.500** kar dipertahankan (dipenuhi 86,3% verified vs 64,7% falsified); target kerja digeser ke **6.000–10.000** kar mengikuti median verified 8.644 — dan panjang >12.000 TIDAK dikejar sebagai strategi: median falsified Moden Gos 30.551 kar membuktikan panjang ekstrem tanpa sitasi tetap mati; pengecualian long-form (DodolDuren 24,7 rb, Adam 10,9 rb) selalu berpasangan dengan kepadatan sitasi 4–6/1.000 kar, bukan panjang sendirian.

**K-5 (rubrik QUALITY (e) — usul revisi bunyi).** Ganti syarat "penutup MENAMAI kebaruan" menjadi "penutup MEMUAT satu mekanisme/angka yang tidak ada di jawaban verified panel itu, dan angka itu terikat sitasi". Angka: penanda kebaruan harfiah di penutup muncul di **9,8%** verified vs **24,5%** falsified (d = −0,147, terbalik). Label kebaruan tanpa isi terikat adalah pola falsified, bukan pola juara.

**K-6 (steering — hedge di kalimat klaim, bukan disclaimer).** Instruksikan model menempelkan hedge epistemik (may/might/suggests/appears to) pada klaim inferensial di badan, target **≥0,25 per 1.000 karakter**; JANGAN menambah paragraf batasan generik. Angka: hedge median verified **0,313** vs falsified 0,160 (d = 0,244, panel 19-0-3); frasa batasan eksplisit tidak memisahkan sama sekali (d = −0,039). Klaim #1 kita: hedge **0,000** — steril dari ketidakpastian di kalimat klaimnya.

**K-7 (gerbang dukungan semantik — DIPERTAHANKAN, tidak tergantikan metrik).** Self-VFP/cek dukungan sitasi-per-klaim tetap wajib dan berdiri sendiri di atas K-1/K-2. Angka pembuktinya adalah klaim #1 kita sendiri: lolos semua ambang mekanik kandidat (4 URL, rasio 0,647) dan tetap falsified (2 refutasi) karena sitasinya tidak mendukung klaimnya. K-1/K-2 adalah lantai perlu; K-7 adalah syarat cukup yang tidak bisa diwakilkan angka kedekatan.

**K-8 (kalibrasi adopsi — pagar anti-overfit).** Jangan jadikan K-1/K-2 satu-satunya penentu pemilihan target/gaya: **23,0%** falsified lolos kombo itu dan seorang pemenang rate-77% (Febriyan) bermain di bawah kedua lantai. Usul pemakaian: K-1/K-2 sebagai penahan draf KELUAR (menghentikan spesies gagal klaim #2), K-7 sebagai penilai isi, dan evaluasi ulang ambang sesudah 5 klaim berikutnya memakai ledger verdict kita sendiri.

**Yang secara eksplisit TIDAK diusulkan** (karena datanya tidak mendukung): gerbang "hindari kata absolut" (d terbalik, +0,201 untuk verified); kewajiban frasa batasan/disclaimer (d = −0,039); kewajiban format sitasi dokumen+versi gaya EIP di arena General (langka di kedua kelas, d = 0,044); kewajiban pembuka koreksi-premis sebagai gerbang mekanik (tidak terkonfirmasi, 9,2% vs 5,4% — tetap boleh sebagai selera steering, bukan pintu mati).

---

## 9. Keterbatasan studi

Sampel = panel settled aktivitas-terbaru (24 panel; statistik utama 22 panel eksternal, n = 357 jawaban ber-verdict) — bukan sampel acak seumur platform; imbangan kelas sampel (V 153 : F 204) tidak mencerminkan rate populasi §30.

Semua metrik adalah proksi mekanis: "terikat sitasi" = kedekatan ±150 karakter, BUKAN dukungan semantik (klaim #1 kita adalah bukti hidup perbedaan keduanya); klasifikasi pembuka memakai penanda sempit sehingga hasil nolnya lemah sebagai bukti ketiadaan.

Studi kasus nama §30 ber-n kecil (2–16 jawaban per nama di jendela listing ini) — dibaca sebagai ilustrasi mekanik di dalam statistik kohort, bukan sebagai bukti tersendiri.

Korelasi bukan sebab: diskriminator menandai profil yang lolos panel verifier; apakah menaikkan metrik secara artifisial (menempel sitasi tanpa dukungan) ikut menaikkan verdict TIDAK dijawab studi ini — justru K-7 dipasang untuk menutup celah itu.
