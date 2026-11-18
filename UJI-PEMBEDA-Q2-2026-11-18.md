# UJI PEMBEDA Q2 — (i) Seleksi Marathon Berkala vs (ii) Saringan Mutu Banjir Awal (2026-11-18)

> Satu baris: **(i) TERKONFIRMASI sebagai penjelasan utama, (ii) GUGUR dalam bentuk kuatnya — tapi sidik jari berkala-nya tidak menempel di kanal marathon saja.** Tiga bukti: (1) distribusi lag verdict era banjir **bimodal** (puncak cepat <15 mnt 28,4% + punuk 2–6 jam 36,5%, lembah 1–2 jam cuma 1,9%; era lama/tengah punuk 2–6 jam cuma 3,8–6,4%); (2) lag ditentukan **fase masuk**, bukan kanal atau mutu — jawaban kanal panel yang masuk awal era banjir menyimpulkan pada median **4,2 jam**, yang masuk telat (≥6 jam) pada median **0,03 jam** (±140× beda, kanal yang sama); (3) penugasan panel ke jawaban banjir awal **tidak menyaring mutu sama sekali** — di semua proksi, kelompok "bermutu" ditugaskan sama atau LEBIH jarang (kombo panjang+bersitasi+novel: **0,0%** dipegang ≥2 verifier, n=18; kombo pendek+tanpa sitasi+tak novel: **24,1%**, n=87). Yang perlu dikoreksi dari bingkai duck: kelompok marathon (me=True) TIDAK berlag lebih panjang dari kanal panel (median 3,5 vs 4,2 jam) dan cuma 23,2% verdict banjir — ritme batch era banjir menjalar ke kesimpulan kanal panel juga, bukan monopoli kanal marathon.
> Data: artefak tarikan studi antrean yang sama (2026-11-18 01:02–01:15 UTC, 66 ISR / 6.188 ISO) — semua kolom yang dibutuhkan sudah ada, tidak ada tarikan baru. Skrip: `belajar-2026-11-18/antrean-verdict/q2_discriminator.py` + `q2_diagnostics.py`, keluaran `q2_discriminator.json`. Read-only, nol submit.

## Metode

- **Era banjir** = ISR lahir ≥14 Nov 2026 (definisi studi induk): 41 ISR / 4.773 ISO; verdict banjir yang terukur lag-nya **419** (296 verified + 123 falsified).
- **M1**: lag = `updatedAt − timestamp` pada ISO ber-verdict (proksi waktu verdict yang sama dengan studi induk; saring 0 ≤ lag ≤ 60 hari). Dipisah `marathonEligible` (me) × era; era lama/tengah sebagai kontrol. Tambahan pemisah yang tidak diminta tapi menentukan: lag kanal panel (me=False) dipisah menurut **delay masuk** (selisih submit terhadap lahirnya ISR).
- **M2**: populasi = ISO eksternal era banjir, umur ≥24 jam saat tarikan, punya teks jawaban, delay masuk ≤2 jam (sub-potongan ≤2 menit ditampilkan juga). Ukuran penugasan = pangsa `verifierCount ≥2`. **Uji utama dibatasi status `revealed`** (belum ber-verdict) supaya penugasan terukur murni — jawaban ber-verdict mekanis ber-vc tinggi dan akan mengotori perbandingan mutu. Proksi mutu (independen dari sistem platform): panjang jawaban (kuartil populasi), keberadaan sitasi URL/DOI (regex), kebaruan leksikal kasar (pangsa kata konten unik yang belum muncul di jawaban-jawaban sebelumnya pada ISR yang sama; stopword dibuang).
- **Prediksi yang diuji** (dari paket konsultasi): (i) memprediksi kelompok marathon berlag panjang/seragam berjam-jam, non-marathon tetap cepat ±11 menit, gabungan bimodal/ekor kanan; dan penugasan rendah **merata** di semua tingkat mutu. (ii) memprediksi kedua kelompok lag tetap cepat; dan penugasan rendah **hanya** di mutu rendah (mutu tinggi ditugaskan mendekati normal era lama, 85,9%).

## M1 — Distribusi lag submit→verdict, dipisah keanggotaan marathon

| Kelompok | n verdict | Median lag | p25–p75 | <1 jam | 1–6 jam | ≥6 jam |
|---|---|---|---|---|---|---|
| **Banjir, me=True** | 97 (semua verified) | **3,50 j** | 0,20–4,91 j | 41,2% | 41,2% | 17,5% |
| **Banjir, me=False** | 322 (199 V + 123 F) | **4,17 j** | 0,10–11,00 j | 36,0% | 37,6% | 26,4% |
| **Banjir, gabungan** | 419 | 4,06 j | 0,18–5,30 j | 37,2% | 38,4% | 24,3% |
| Tengah, me=True | 165 | 0,25 j | 0,18–3,07 j | 72,1% | 8,5% | 19,4% |
| Tengah, me=False | 409 | 0,08 j | 0,04–0,49 j | 75,6% | 8,6% | 15,9% |
| Lama, me=True | 40 | 0,20 j | 0,16–4,53 j | 72,5% | 10,0% | 17,5% |
| Lama, me=False | 91 | 0,02 j | 0,02–0,03 j | 95,6% | 1,1% | 3,3% |

**Histogram lag gabungan (pangsa verdict):**

| Ember lag | <15 mnt | 15–60 mnt | 1–2 j | 2–6 j | 6–24 j | >24 j |
|---|---|---|---|---|---|---|
| **Era banjir** (n=419) | **28,4%** | 8,8% | **1,9%** | **36,5%** | 16,7% | 7,6% |
| Era tengah (n=574) | 66,6% | 8,0% | 2,1% | 6,4% | 16,0% | 0,9% |
| Era lama (n=131) | 86,3% | 2,3% | 0,0% | 3,8% | 6,9% | 0,8% |

**Pemisah penentu — lag kanal panel (me=False) era banjir menurut delay masuk:**

| Delay masuk | n verdict | Median lag | <1 jam | ≥6 jam |
|---|---|---|---|---|
| <2 menit | 166 | **4,22 j** | 32,5% | 35,5% |
| 2 menit–2 jam | 101 | **4,19 j** | 26,7% | 17,8% |
| 2–6 jam | 11 | 3,23 j | 27,3% | 0,0% |
| 6–24 jam | 33 | **0,04 j** | 69,7% | 24,2% |
| >24 jam | 11 | **0,03 j** | 81,8% | 0,0% |
| **Pooled: awal (<2 j)** | **267** | **4,22 j** | 30,3% | 28,8% |
| **Pooled: telat (≥6 j)** | **44** | **0,03 j** | 72,7% | 18,2% |

Bacaan M1:

1. **Bimodalitas gabungan era banjir NYATA** — persis bentuk yang diramalkan (i): puncak cepat + punuk 2–6 jam yang di era lain nyaris tidak ada (36,5% vs 3,8–6,4%), dipisahkan lembah 1–2 jam (1,9%). Di bawah (ii) distribusi ini seharusnya tetap cepat seperti era lama (86,3% <15 menit); kenyataannya cuma 28,4%.
2. **Tapi pemisahnya BUKAN keanggotaan marathon.** Median lag me=True (3,50 j) dan me=False (4,17 j) praktis sama; kelompok marathon tidak "panjang dan seragam" — 41,2%-nya justru <1 jam (sebaran lebar, p25 0,20 j). Dan me=True cuma **97/419 (23,2%)** verdict banjir (32,8% dari verified) — mayoritas verdict banjir datang dari kanal panel biasa yang sama lambatnya. Klaim paket konsultasi "hampir semua verdict banjir dari kanal marathon" tidak bertahan di hitungan langsung sampel ini.
3. **Pemisah sebenarnya adalah FASE MASUK.** Di kanal yang sama (me=False), entrant awal menyimpulkan pada median 4,22 jam sedangkan entrant telat pada 0,03 jam. Lag bukan sifat jawaban dan bukan sifat kanal — ia fungsi posisi submit terhadap jadwal sapuan berkala: yang masuk tepat sesudah sapuan menunggu sapuan berikutnya (berjam-jam), yang masuk menjelang sapuan disimpulkan dalam menit. Ini sidik jari batch/berkala yang lebih umum daripada kanal marathon: **di era banjir, kesimpulan verdict — panel maupun marathon — berjalan dalam gelombang berkala**, dan jawaban awal era banjir hampir selalu lahir tepat sesudah gelombang (karena pertanyaan lahir dan dibanjiri dalam hitungan detik, lalu dievaluasi berjam-jam kemudian).
4. Kontras era menegaskan ini rezim, bukan artefak kolom: kanal panel era lama menyimpulkan pada median 0,02 jam (95,6% <1 jam) — cepat seperti yang (ii) bayangkan — dan perilaku itu **hilang** di era banjir untuk entrant awal, tapi **tetap ada** untuk entrant telat di era yang sama.

## M2 — Penugasan panel jawaban banjir awal menurut proksi mutu

Populasi uji utama: revealed saja, umur ≥24 jam, delay ≤2 jam, **n=930** (sub-potongan delay ≤2 menit: n=502). Pangsa keseluruhan yang dipegang ≥2 verifier: **11,3%** (≤2 menit: 10,2%) — bandingkan kontrol era lama+tengah di bawah.

**Menurut panjang jawaban (kuartil populasi; batas 4.274 / 6.889 / 11.048 karakter):**

| | Q1 terpendek | Q2 | Q3 | Q4 terpanjang |
|---|---|---|---|---|
| n | 232 | 231 | 233 | 234 |
| vc≥2 | **19,0%** | 11,3% | 8,2% | **6,8%** |
| vc=0 (tak pernah ditugaskan) | 61,6% | 67,5% | 71,7% | 73,9% |

**Menurut sitasi:**

| | Ada URL/DOI (n=766) | Tanpa sitasi (n=164) |
|---|---|---|
| vc≥2 | 9,8% | **18,3%** |
| vc=0 | 71,8% | 54,3% |

**Menurut kebaruan leksikal:**

| | <0,3 (n=715) | 0,3–0,5 (n=144) | 0,5–0,7 (n=34) | ≥0,7 (n=37) |
|---|---|---|---|---|
| vc≥2 | **14,4%** | 1,4% | 0,0% | 0,0% |
| vc=0 | 64,2% | 82,6% | 79,4% | 91,9% |

**Kombo ekstrem:** mutu-tinggi (Q4 panjang + bersitasi + novelty ≥0,5): n=18, vc≥2 **0,0%**, vc=0 94,4%. Mutu-rendah (Q1 pendek + tanpa sitasi + novelty <0,5): n=87, vc≥2 **24,1%**, vc=0 52,9%. Sub-potongan ≤2 menit arahnya identik (kombo tinggi 0,0% n=20; kombo rendah 16,3% n=43).

**Latar & kontrol:**

- Menurut delay (revealed, banjir): vc≥2 = 10,2% (<2 mnt, n=502) · 12,6% (2 mnt–2 j, n=428) · **60,0%** (2–6 j, n=15) · **60,9%** (6–24 j, n=23) · **62,5%** (>24 j, n=8). Efek waktu masuk (±5–6×) menenggelamkan semua efek mutu.
- Menurut ukuran ISR (delay ≤2 j): N 16–40 = 0,0% (n=24) · N 41–80 = 5,8% (n=191) · N 81+ = 13,1% (n=715). Semua jauh di bawah norma pra-banjir.
- **Kontrol era lama+tengah** (delay ≤2 j, revealed, umur ≥24 j): n=291, vc≥2 = **100,0% di SEMUA ember mutu** (keempat kuartil panjang 100%; bersitasi 100%; tanpa sitasi 100%). Pra-banjir penugasan bersifat universal dan buta mutu — tidak ada saringan mutu yang berdiri sebagai perilaku platform; yang berubah di era banjir adalah kelangkaan penugasan itu sendiri.

**Cek pengacau (confounder) — dibaca sebelum menafsir gradien terbalik:**

- Kebaruan **terkait mekanis dengan posisi**: ember novelty ≥0,7 bermedian posisi 1 (jawaban pertama ber-novelty 1,0 menurut konstruksi), novelty <0,3 bermedian posisi 27. Jadi sebagian "gradien kebaruan" adalah gradien posisi yang menyamar. Tetapi gradiennya **bertahan di dalam ISR raksasa saja** (N≥41: novelty <0,3 → 14,7% vs ≥0,5 → 0,0%, n=68; panjang Q1 19,5% → Q4 7,0%), jadi posisi bukan seluruh cerita.
- Konsentrasi author: 10 author tersering mencakup 222/930 jawaban populasi dan ditugaskan jauh lebih jarang (vc≥2 3,2%) daripada 708 jawaban sisanya (13,8%). Satu-satunya sinyal "penyaringan" yang terlihat berjalan menurut **volume author**, bukan mutu isi — konsisten dengan penekanan anti-banjir pada pengirim massal, dan itu pun tidak menyelamatkan jawaban bermutu dari author biasa.
- Ember novelty tinggi kecil (n=34–37) dan kombo tinggi n=18 — arahnya tegas (0,0% di semua potongan) tapi jangan dibaca sebagai desimal presisi.

Bacaan M2: prediksi (ii) menuntut jawaban banjir awal yang bermutu ditugaskan mendekati normal dan hanya sampah yang disaring. Data menunjukkan kebalikannya di ketiga proksi: **tidak ada tingkat mutu yang ditugaskan mendekati normal (maksimum 19,0% vs patokan 85,9–100%), dan urutan penugasannya justru terbalik terhadap mutu proksi.** Prediksi (i) "rendah merata" benar pada levelnya (semua ember 0–19%, mayoritas ≤15%) walau tidak datar sempurna — ada gradien terbalik yang sebagian artefak posisi dan sebagian sinyal volume-author. Untuk pertanyaan yang diperselisihkan — *apakah keunggulan masuk telat dijelaskan oleh saringan mutu atas banjir awal* — jawabannya tidak: jawaban awal terbaik pun tidak ditugaskan; yang membedakan jawaban telat adalah mereka tiba saat sapuan berkala berjalan dan kolam sudah terbentuk (penugasan 60%+), bukan karena mereka lolos saringan yang menggugurkan pendahulunya.

## Vonis

**Campuran dengan (i) sebagai utama yang dominan — dan (ii) gugur sebagai penjelasan; sisa (ii) yang bertahan hanya sebagai penekanan volume-author, bukan saringan mutu.**

- **(i) terkonfirmasi pada klaim intinya**: keunggulan masuk telat di era banjir adalah fenomena **waktu seleksi berkala**. Bukti lag bimodal (punuk 2–6 jam 36,5% vs 3,8–6,4% era lain), bukti fase (median lag kanal panel 4,22 jam untuk entrant awal vs 0,03 jam untuk entrant telat di era dan kanal yang sama), dan bukti penugasan (10–13% untuk entrant <2 jam vs 60%+ untuk entrant >2 jam, buta mutu) bertiga menunjuk mekanisme yang sama.
- **Koreksi atas bingkai (i) versi duck**: ritme berkala itu **bukan monopoli kanal marathon**. Kelompok me=True tidak berlag khas (median 3,50 j, 41,2% <1 jam) dan hanya menyumbang 23,2% verdict banjir; kanal panel era banjir menyimpulkan dengan pola gelombang yang sama. Tafsir yang data dukung: di era banjir platform mengevaluasi dalam **putaran berkala per pertanyaan/kohort** (putaran marathon adalah wujud terstrukturnya yang terlihat), dan cap `marathonEligible` menandai subset terseleksi di dalam putaran itu — bukan dua kanal dengan jam kerja berbeda.
- **(ii) gugur dalam bentuk yang diperselisihkan** (runtuhnya mutu banjir awal disaring keluar sehingga yang telat menang): tidak ada saringan mutu pada penugasan — kelompok berkombo mutu tertinggi justru 0,0% tertugaskan, dan kontrol era lama membuktikan penugasan pra-banjir 100% buta mutu. Yang tersisa dari (ii) hanyalah fakta bahwa banjir awal memang berisi jawaban massal (10 author = 24% populasi) dan author bervolume tinggi ditugaskan lebih jarang (3,2%) — penekanan pada *pengirim*, bukan penilaian atas *isi*; efeknya kecil di samping efek fase (60% vs 11%) dan tidak menjelaskan keunggulan telat.
- **Implikasi doktrin** (di luar mandat berkas ini, dicatat karena langsung mengikuti): pemicu mode telat/cepat sebaiknya dibaca sebagai **fase terhadap sapuan berkala** — masuk telat bekerja karena tiba di kolam yang sedang disapu, bukan karena menunggu "sampah tersaring". Ini menguatkan Opsi A sebagaimana dipilih (mesin telat 2–6 jam + cepat hanya di pertanyaan sepi), dengan satu penajaman: tidak ada alasan mengharapkan jawaban awal yang "cukup bermutu" akan tetap dipanen panel — di era banjir, mutu tidak membeli penugasan.

## Batas & kaveat

- Lag memakai `updatedAt` (aktivitas terakhir), bukan stempel verdict khusus — bias arahnya membuat lag terlihat lebih besar, bukan lebih kecil; median antar-kelompok pada era yang sama tetap sebanding karena proksi yang sama. Angka absolut 4,2 jam adalah taksiran atas; kontras 140× antar fase dan bentuk bimodal tidak bergantung pada presisi absolut itu.
- `marathonEligible` dibaca sebagai penanda (kemungkinan dicap saat seleksi berjalan), bukan tuas — sama seperti kaveat studi induk. Karena itu vonis dibingkai pada *ritme berkala*, bukan pada kanal sebagai penyebab.
- Kebaruan leksikal adalah proksi kasar (kata konten, tanpa semantik) dan terkunci mekanis ke posisi awal; ia dipakai hanya sebagai satu dari tiga proksi, dan ketiga proksi searah.
- Sampel era banjir = 41 ISR dari sampel berstrata studi induk (bukan acak murni arena); ember delay telat pada M2 ber-n kecil (8–23) — dipakai sebagai latar arah, bukan angka bidik. Ember inti M1 (n=97–419) dan M2 (n=164–930) cukup untuk arah dan orde besaran.
- Populasi M2 dibatasi umur ≥24 jam agar penugasan punya waktu terjadi; jawaban banjir berumur <24 jam (lahir 17 Nov) berada di luar uji — penugasannya masih bisa bergerak, tapi memasukkannya hanya akan menurunkan semua pangsa secara merata.
