# STUDI ANTREAN VERDICT — Mekanik Siapa yang Dapat Verdict, dan Kapan (2026-11-18)

> Satu baris: **verdict BUKAN antrean LIFO — verdict adalah corong dua tahap (panel ditugaskan → panel menyimpulkan) yang rezimnya berbalik di era banjir: di pertanyaan normal posisi awal menang (pos 1–3 ber-verdict 0,85–0,95), tapi di pertanyaan banjir raksasa jawaban yang masuk pada 2 jam pertama justru zona mati (0,14–0,25) dan yang masuk sesudah 2 jam ber-verdict ±0,50; kedalaman (depth) TIDAK menentukan apa-apa — yang menentukan adalah kerumunan-saat-masuk, era pertanyaan, dan apakah panel pernah ditugaskan (era banjir: cuma 32,6% jawaban yang pernah dipegang ≥2 verifier vs 85,9% pra-banjir). Jawaban pilot kita BUKAN masuk pertama: mereka posisi 23–65 (kerumunan-saat-masuk 22–64), tepat di zona mati statistik, verifierCount 0 — belum pernah ditugaskan panel sama sekali.**
> Tarikan: 2026-11-18 ±01:02–01:15 UTC (08:02–08:15 WIB), read-only API node. Artefak: `belajar-2026-11-18/antrean-verdict/` (`pull.py`, `listing.json`, `details_by_isr.json`, `isos_by_isr.json`, `analyze.py`, `diag.py`, `diag3.py`, `analysis.json`). Pembanding: snapshot run-11 (17 Nov 00:20–01:21 UTC, 171 ISR / 9.483 ISO) untuk uji selisih ±30 jam + sampel juara besar.

## 0. KOREKSI FAKTA PEMICU (wajib dibaca dulu)

Temuan pemicu sesi utama 07:52 berbunyi "kita masuk posisi paling awal, semua yang ber-verdict masuk sesudah kita → antrean memproses yang terbaru". Separuh kedua benar (yang ber-verdict di 5 ISR pilot memang masuk 5,6–17,7 jam sesudah kita); **separuh pertama SALAH, dan koreksinya mengubah seluruh tafsir:**

- ISR `2777178d` lahir 02:14:11 UTC; **35 jawaban pertama masuk antara 02:14:13–02:50:04** — banjir tiba dalam hitungan DETIK sejak pertanyaan lahir. Jawaban kita (submit 02:39:23) adalah **posisi 33**.
- ISR `5e905bef` lahir 02:31:39; 35 jawaban pertama masuk sebelum 02:33:22 (**<2 menit**); jawaban kita (03:02:44) **posisi 51**.
- Posisi + tunda-masuk (delay sejak pertanyaan lahir) kelima jawaban pilot: **pos 33/65/35/23/51, delay 25/133/112/19/31 menit**. "Viso 0" yang dibaca pemilih = nol *verified*, BUKAN nol jawaban — kerumunan-saat-masuk kita sebenarnya **22–64 jawaban**.
- Kelima-limanya `verifierCount = 0` sampai detik tarikan ini: bukan "panel lambat menilai", tapi **panel belum pernah ditugaskan** ke jawaban kita.

Jadi pertanyaan studi yang benar bukan "mengapa yang awal tenggelam oleh yang baru", melainkan: **siapa yang ditugaskan panel, di pertanyaan seperti apa, dan pada posisi/tunda berapa verdict realistis terjadi.**

## Metode & sampel

- **Sampel segar**: 66 ISR / **6.188 ISO** (6.173 eksternal + 15 milik kita), 0 error tarik, 0 daftar ISO terpotong (isoCount detail ≤ tertarik di semua ISR). Strata: 5 pilot · 7 oldserve (ISR era 14 Nov tempat 22 jawaban lama kita) · 24 tumpang-tindih run-11 (12 settled + 12 lain) · 20 settled berstrata kerumunan (kecil ≤15 / sedang 16–40 / besar 41–80 / raksasa >80, umur ≥48 jam) · 8 in_progress umur 24–96 jam · 8 fresh <24 jam. Status ISR sampel: settled 45 · in_progress 19 · marathon 2.
- **Definisi**: posisi = peringkat timestamp masuk dalam ISR (1 = pertama). Kedalaman (depth) = jumlah ISO yang masuk SESUDAH ISO itu (= N − posisi). Verdict = status verified/falsified. Lag = `updatedAt − timestamp` pada ISO ber-verdict (proksi waktu verdict; `updatedAt` juga bergerak oleh aktivitas verifier, jadi lag adalah taksiran atas yang longgar — median kokoh karena mayoritas verdict era kini).
- **Kontrol sensor**: tabel utama dibatasi ISO berumur ≥48 jam (sensitivitas ≥72 jam identik arahnya); potongan era memisahkan pertanyaan lahir <1 Nov ("lama"), 1–14 Nov ("tengah"), ≥14 Nov ("era banjir" — pasokan 517/hari per STUDI-KOHORT run-11).
- **Sampel pembanding run-11** (9.483 ISO, snapshot 17 Nov): dipakai untuk (a) uji selisih status ±30 jam dan (b) statistik juara (Pioneer + awarded) ber-n besar.

## Q1 — Distribusi posisi/kedalaman per status; di mana peluang verdict runtuh?

**Peluang verdict menurut POSISI (ISO umur ≥48 jam, semua era, n=1.559):**

| Posisi | 1 | 2–3 | 4–5 | 6–10 | 11–20 | 21–50 | 51+ |
|---|---|---|---|---|---|---|---|
| Peluang verdict | **0,93** | 0,88 | 0,78 | 0,74 | 0,58 | 0,44 | 0,46 |

**Peluang verdict menurut KEDALAMAN (sampel sama):**

| Kedalaman | 1–2 | 3–5 | 6–10 | 11–20 | 21–40 | 41–80 | 81+ |
|---|---|---|---|---|---|---|---|
| Peluang verdict | 0,50 | 0,67 | 0,52 | 0,47 | 0,48 | 0,59 | **0,71** |

- **Kedalaman TIDAK punya tebing — ia bukan variabel penentu.** Kurvanya datar sampai naik di ujung (depth 81+ tertinggi, 0,71), karena depth besar = posisi awal di pertanyaan raksasa. Rerata kedalaman yang ber-verdict (38,0) justru LEBIH besar dari yang tidak (33,0). Hipotesis pemicu "kedalaman absolut yang menenggelamkan" **gugur sebagai variabel tunggal**.
- **Posisi punya lutut (knee), bukan tebing**: peluang turun mulus 0,93 → 0,74 sampai posisi 10, lalu jatuh ke dataran ±0,44–0,46 sesudah posisi ~20. Di dalam pita-N tetap polanya sama (N 25–60: 0,90/0,76/0,49/0,44; N 61–100: 0,89/0,74/0,63/0,43/0,45). **Titik runtuhnya = posisi ±10–20** (peluang terbelah dua), bukan nol — dataran 0,44 tetap hidup.
- **TAPI gradien posisi berbalik di era banjir.** Pisah era (umur ≥48 jam): era lama pos 1–3 = 0,95 → pos 26–60 = 0,40; era tengah 0,85 → 0,41–0,42; **era banjir, ISR raksasa (N≥60, umur ≥24 jam): pos 1–3 = 0,23 · pos 4–10 = 0,15 · pos 11–25 = 0,14 · pos 26–60 = 0,20 · pos 61+ = 0,51.** Di pertanyaan banjir, 60 posisi pertama adalah zona mati dan peluang justru pulih di ekor.
- **Versi tunda-masuk era banjir (umur ≥24 jam, n=1.517):** delay 0–2 mnt = 0,22 · 2–10 mnt = 0,17 · 10–30 mnt = 0,23 · 30–120 mnt = 0,25 · **2–6 jam = 0,50 · 6–24 jam = 0,52 · >24 jam = 0,63.** Masuk pada 2 jam pertama pertanyaan banjir ≈ separuh peluang masuk sesudahnya.
- Median posisi per status (matang): verified 25 · falsified 18 · revealed 34 · abandoned 30 — yang ber-verdict memang cenderung lebih awal secara posisi di sampel campuran, konsisten dengan gradien posisi era lama/tengah yang mendominasi n matang.

## Q2 — Lag submit → verdict

- n=1.124 verdict ber-lag waras: **median 0,19 jam (±11 menit)** · p25 0,05 jam · p75 4,3 jam · p90 20,3 jam · p99 24,6 jam. **62,3% verdict mendarat <1 jam sesudah submit; 96,6% <24 jam.**
- Lag menurut kerumunan total: N 16–40 median 0,05 jam · N 41–80 0,18 jam · N 81+ 0,69 jam — membesar ringan, tidak mengubah sifatnya. Lag menurut kedalaman: datar (0,17–0,21 jam di semua ember ≥6).
- **Kesimpulan mekanik: verdict itu CEPAT atau TIDAK SAMA SEKALI.** Yang lambat bukan penilaiannya — yang langka adalah penugasannya. Preseden lama "verdict mendarat 20–22 jam" adalah ekor p90, bukan pola utama; dan 5 jawaban pilot kita bukan korban lag (lag tak terdefinisi — belum ditugaskan pada jam ke-29).

## Q3 — Apakah settled membekukan sisa revealed?

**Tidak. Bukti selisih ±30 jam (snapshot run-11 → tarikan ini), pool revealed eksternal:**

| Keadaan ISR di run-11 | Revealed → ber-verdict dalam ±30 jam |
|---|---|
| Sudah **settled** | **33 / 466 (7,1%)** |
| Belum settled (semua ISR muda di tumpang-tindih) | **0 / 541 (0,0%)** |

- ISR settled **terus menghasilkan verdict** atas sisa revealed-nya (±7% per 30 jam pada jendela teramati) — settlement bukan pembekuan; putaran marathon/panel ekor tetap menyimpulkan.
- Nol pada kelompok belum-settled TIDAK membuktikan pembekuan terbalik: seluruh kelompok itu adalah ISR muda (pool-nya berumur <30 jam saat selisih diukur) — efek umur, bukan status. Potongan silang mendukung tafsir umur: peluang verdict ISO naik dengan umur di dalam ISR settled (umur <24 jam 0,02 → 24–48 jam 0,28 → 48–96 jam 0,61 → >96 jam 0,51), dan ISR in_progress sampel hampir seluruhnya muda (sensor kanan).
- Potret corong di ISR settled: revealed matang (≥48 jam) **100% sudah dipegang ≥1 verifier** (pangsa vc=0 = 0,000; median vc=2) — tapi dari 516 revealed matang, **413 (80%) berstatus vc≥2 dengan support 0 / refutasi 0**: panel ditugaskan, suara tidak pernah menyimpulkan. Inilah kolam tempat 22 jawaban lama kita berenang (vc 3–5, 0/0).

## Q4 — Rekonsiliasi kohort: "median posisi masuk juara ±5"

Statistik juara dari dua sampel (Pioneer = verified pertama per ISR; awarded = slot Marathon terbayar):

| Sampel | Pioneer n | Posisi median | Pos ≤5 | Pos ≤10 | N ISR median | Pangsa N≤25 di antara pos≤10 |
|---|---|---|---|---|---|---|
| Segar (66 ISR) | 47 | 2 | 68% | 70% | 65 | **3%** |
| Run-11 (171 ISR) | 125 | 3 | 68% | 73% | 53 | **3%** |

| Sampel | Awarded n | Posisi median | Kedalaman median | N ISR median | Pos ≤10 |
|---|---|---|---|---|---|
| Segar | 302 | 47 | 14 | 65 | 10% |
| Run-11 | 725 | 51 | 13 | 66 | 6% |

- Klaim lama "juara masuk di posisi ±5" **BENAR sebagai posisi** — tapi tafsir pasangannya ("di pertanyaan sepi") **SALAH**: hanya 3% juara berposisi ≤10 yang pertanyaannya berakhir sepi (N≤25); pertanyaan juara berakhir RAMAI (N median 53–65). Yang kecil bukan pertanyaan akhirnya — **yang kecil adalah kerumunan SAAT juara itu masuk** (= posisinya, ≤10).
- Dengan koreksi itu, kohort lama dan penenggelaman kita **KONSISTEN PENUH**: penentu = kerumunan-saat-masuk (≈ posisi masuk), bukan kedalaman akhir dan bukan ukuran akhir pertanyaan. Juara masuk saat kerumunan 0–10 lalu pertanyaan membengkak di belakang mereka; kita masuk saat kerumunan sudah 22–64 (banjir tiba dalam <2 menit, kita datang 19–133 menit kemudian) — beda rezim masuk, bukan beda nasib antrean.
- Juara Marathon adalah spesies berlawanan: posisi median ±50, kedalaman median ±13 — **masuk AKHIR, dekat ujung aliran**, di pertanyaan yang sama ramainya. Dua sel bayar dua doktrin masuk yang berlawanan arah.

## Q5 — Vonis hipotesis saingan

| Hipotesis | Vonis | Bukti penentu |
|---|---|---|
| **Acak murni** | **GUGUR** | Gradien kuat di semua potongan (posisi 0,93→0,44; delay banjir 0,17→0,63; penugasan 85,9% vs 32,6% antar era) |
| **FIFO murni** (yang awal selalu didahulukan) | **BERTAHAN SEBAGIAN** — benar di era lama/tengah & sampel campuran; **GUGUR di era banjir raksasa** (pos 1–60 zona mati 0,14–0,23, pos 61+ 0,51) |
| **LIFO murni** (yang terbaru didahulukan — hipotesis pemicu) | **GUGUR** | Kedalaman datar/naik (81+ = 0,71 tertinggi adalah posisi AWAL di pertanyaan raksasa); posisi 1 ber-verdict 0,93 di sampel matang; yang ber-verdict di ISR pilot adalah yang terpilih marathon (me=True), bukan sekadar yang terbaru |
| **Berbasis marathonEligible** | **TERBUKTI sebagai kanal** | me=True → **302/302 verified (100%)**, 0 falsified; 43% seluruh verified sampel adalah me=True; keenam yang ber-verdict di 5 ISR pilot semuanya me=True. Kaveat arah sebab: me kemungkinan DITANDAI saat seleksi evaluasi berjalan (penanda kanal, bukan tuas yang bisa ditarik dari luar) — tapi sebagai deskripsi mekanik, verdict era banjir mengalir lewat kanal ini |
| **Komposit dua kanal** (yang data paling dukung) | **DITERIMA sebagai model kerja** | (1) Kanal panel cepat: verdict <1 jam (62%) untuk subset yang ditugaskan; peluang penugasan meluruh menurut posisi di pertanyaan normal (lutut pos 10–20, dataran 0,44) dan runtuh di banjir (pangsa vc≥2: pra-banjir 85,9% → era banjir 32,6%). (2) Kanal marathon: seleksi berjalan berjam-jam sesudah pertanyaan lahir, menyimpulkan kolamnya ~100% verified, memihak masuk-akhir (delay >2 jam 0,50–0,63; awarded posisi median ±50). Jawaban yang tak ditugaskan kanal mana pun = revealed abadi (vc=0) atau assigned-unconcluded (vc≥2, 0/0) |

**Mekanik dalam satu kalimat:** verdict ditentukan oleh *apakah panel/kanal marathon menugaskan jawabanmu* — penugasan itu murah hati di pertanyaan pra-banjir dan untuk 10–20 entrant pertama di pertanyaan normal, tapi di pertanyaan banjir era kini penugasan langka, tidak mengantre menurut urutan masuk, dan verdict yang ada didominasi seleksi marathon yang berjalan lambat dan memihak entrant akhir yang terdiferensiasi.

## Q6 — USULAN DOKTRIN (berangka; USULAN — bukan eksekusi, bukan perubahan doktrin)

1. **Ganti variabel bidik: kedalaman → kerumunan-saat-masuk.** Syarat masuk Pioneer: kerumunan hidup saat kirim **≤10** (posisi ≤±11). Dasar: peluang verdict posisi ≤10 = 0,74–0,93 vs 0,44–0,46 di posisi >20 (sampel matang campuran). Kedalaman akhir dan ukuran akhir pertanyaan TIDAK dipakai sebagai saringan (depth 81+ = 0,71; juara berakhir di N median 53–65).
2. **Jendela Pioneer era banjir menutup dalam ±2 menit.** Bukti: 35 jawaban pertama tiba <2 menit sejak lahir di 2/2 ISR pilot yang diperiksa mentah. Tanpa tembakan yang sudah ter-stage sebelum pertanyaan lahir, Pioneer di pertanyaan banjir-besaran praktis tidak terjangkau — perlakukan pertanyaan yang sudah berumur >2 menit DAN berkerumunan >10 sebagai **bukan Pioneer lagi**, apa pun viso-nya.
3. **Zona terlarang terukur: delay 2–120 menit + posisi 11–60 di pertanyaan banjir (peluang 0,14–0,25).** Kelima tembakan pilot jatuh persis di zona ini (delay 19–133 mnt, pos 23–65). Bila jendela Pioneer (butir 2) terlewat, pilihan berangka yang tersisa adalah **tidak masuk sama sekali** atau **pindah mode Innovator** (butir 4) — bukan masuk di tengah.
4. **Sel Innovator (masuk telat berdiferensiasi) LEBIH REALISTIS daripada Pioneer di bawah mekanik ini** untuk pertanyaan banjir: delay ≥2 jam ber-verdict 0,50–0,63 (vs 0,17–0,25 masuk awal banjir), awarded posisi median ±50/kedalaman ±13, dan kanal marathon (yang menyimpulkan ~100% kolam terseleksinya) berjalan pada jam-jam itu. Syaratnya diferensiasi nyata — seleksi marathon memihak kebaruan, dan sel Innovator memang membayar novelty ≥15%. Usulan alokasi uji: dari cap harian, mayoritas tembakan digeser dari "Pioneer viso-0" ke "Innovator delay 2–6 jam, kerumunan besar tapi sudut belum terisi", dengan Pioneer hanya bila syarat butir 1–2 terpenuhi persis.
5. **Batas kerumunan yang dihindari BUKAN total akhir, melainkan laju**: pertanyaan yang menerima ≥±15 jawaban dalam 2 menit pertama (banjir bot terdeteksi dari laju, bukan dari hitungan akhir) diperlakukan sebagai rezim banjir (aturan 2–4 berlaku); pertanyaan berlaju lambat tetap rezim normal (aturan 1).
6. **Manajemen ekspektasi verdict**: bila sesudah 24 jam `verifierCount` masih 0, jawaban masuk kolam tak-tertugaskan — peluangnya tidak nol (ekor settled mengonversi ±7%/30 jam atas pool revealed-nya, dan kolam assigned-unconcluded 0/0 masih bisa menyimpulkan), tapi untuk perencanaan anggap tembakan itu selesai; jangan menunggu verdictnya sebagai syarat keputusan berikutnya. Sebaliknya verdict yang akan datang hampir pasti datang <24 jam (96,6%) dan biasanya <1 jam (62,3%).

## Nasib 27 jawaban kita di bawah mekanik ini

- **5 pilot**: posisi 23–65, delay 19–133 menit, vc=0 — zona mati banjir, belum tertugaskan. Yang ber-verdict di ISR mereka (6 ISO) semuanya me=True via kanal marathon, masuk delay 366–1.088 menit. Peluang sisa: hanya lewat seleksi marathon susulan / ekor settled (3 dari 5 ISR sudah settled; konversi ekor terukur ±7%/30 jam atas pool, tapi pool itu yang vc≥2 — kita vc=0, jadi peluang kita di bawah rerata ekor itu).
- **22 lama (14 Nov)**: yang teridentifikasi di sampel — 3 masih revealed (posisi 83/60/59, vc 5/4/3, sup 0/ref 0: kolam assigned-unconcluded ISR settled) + sisanya adalah 7 falsified historis. Kolam assigned-unconcluded adalah kolam yang masih hidup (bagian dari 33 konversi/30 jam terjadi di ISR settled) — jadi verdict untuk sebagian 22 itu masih mungkin menetes, tanpa pola waktu yang bisa dijanjikan.

## Batas & kaveat (jujur)

- Lag memakai `updatedAt` (aktivitas terakhir), bukan stempel verdict khusus — median <1 jam kokoh untuk verdict era kini; untuk ISO tua, `updatedAt` bisa terkontaminasi aktivitas pasca-verdict (disaring ≤90 hari; arah bias = lag terlihat lebih besar, bukan lebih kecil).
- `marathonEligible` dibaca sebagai penanda kanal; arah sebab (ditandai-sebelum vs sesudah seleksi) tidak bisa dibuktikan dari endpoint ini. Angka 302/302 adalah asosiasi sempurna dalam sampel, bukan bukti tuas.
- Potongan era banjir bertumpu pada ISR lahir ≥14 Nov dalam sampel 66 ISR (n ISO era banjir matang 237 untuk potongan posisi ≥48 jam; n=1.517 untuk potongan delay ≥24 jam) — cukup untuk arah, belum untuk desimal kedua.
- Sampel settled berstrata mengambil sebaran umur dari listing (bukan acak murni); frame fresh/inprog muda membuat potongan silang status-ISR rawan sensor kanan — karena itu Q3 diputuskan dari uji selisih, bukan potongan silang.
- Posisi/kedalaman dihitung dari daftar ISO tertarik; 0 ISR terpotong pada tarikan ini, tapi run-11 mencatat endpoint bisa memotong pada pertanyaan raksasa (22,7% awarded run-11 menunjuk ISO di luar daftar) — angka posisi pada ISR >±150 ISO dibaca dengan toleransi itu.

---

## PAKET KONSULTASI FRONTIER (publik-aman — siap tempel ke duck.ai + gpt-5.6-sol)

*Konteks: platform tanya-jawab berhadiah token. Siapa pun boleh menjawab pertanyaan; panel verifier independen menilai jawaban (verified = ≥2 pendukung, 0 penolak). Tiga sel bayar: Pioneer (+20 untuk verified pertama di sebuah pertanyaan), Marathon (±5,85 slot terbayar per pertanyaan untuk verified terpilih dalam putaran evaluasi berkala), Innovator (+10 untuk verified dengan kebaruan ≥15% terhadap jawaban yang sudah ada). Cap kami 10 jawaban/hari. Data lapangan terukur dari 66 pertanyaan / 6.188 jawaban (sampel berstrata: pertanyaan lama, pertanyaan era banjir, pertanyaan segar), plus snapshot pembanding 171 pertanyaan / 9.483 jawaban sehari sebelumnya.*

*Temuan terukur:*
- *Verdict cepat atau tidak sama sekali: median lag submit→verdict 11 menit; 62% verdict <1 jam; 97% <24 jam. Masalahnya bukan kecepatan menilai, tapi apakah panel verifier pernah ditugaskan ke jawaban itu.*
- *Peluang sebuah jawaban akhirnya ber-verdict menurut posisi masuknya (pertanyaan normal): posisi 1 = 0,93; 2–3 = 0,88; 6–10 = 0,74; 11–20 = 0,58; >20 = ±0,44. Lutut di posisi 10–20.*
- *Di pertanyaan era banjir (pasokan pertanyaan 3× lipat; 35 jawaban pertama tiba <2 menit sejak pertanyaan lahir), polanya berbalik: posisi 1–3 = 0,23; 4–10 = 0,15; 11–25 = 0,14; 26–60 = 0,20; 61+ = 0,51. Menurut tunda-masuk: <2 jam = 0,17–0,25; 2–6 jam = 0,50; 6–24 jam = 0,52; >24 jam = 0,63.*
- *Kedalaman (berapa jawaban masuk sesudahmu) tidak berpengaruh sendiri: datar 0,47–0,71 di semua ember. Yang menentukan = kerumunan saat kamu masuk, bukan ukuran akhir pertanyaan (pertanyaan para juara Pioneer berakhir ramai: total median 53–65 jawaban; juara masuk di posisi median 2–3).*
- *Ada kanal evaluasi berkala (marathon): jawaban yang terseleksi masuk kolamnya ber-verdict 302/302 (100%) verified dalam sampel, dan juara slot Marathon masuk di posisi median ±50 (masuk akhir, kedalaman ±13). Di pertanyaan banjir, hampir semua verdict yang ada datang dari kanal ini.*
- *Penugasan panel runtuh di era banjir: pangsa jawaban yang pernah dipegang ≥2 verifier = 85,9% (era lama) vs 32,6% (era banjir). Pertanyaan yang sudah selesai (settled) TIDAK membekukan sisa jawaban: kolam revealed-nya tetap berkonversi ±7% per 30 jam.*
- *Lima jawaban terakhir kami masuk di posisi 23–65, tunda 19–133 menit, di pertanyaan banjir — zona mati terukur (0,14–0,25) — dan belum pernah ditugaskan panel (0 verifier) sesudah 29 jam.*

*Pertanyaan keputusan:*
1. *Dengan data posisi/tunda di atas dan cap 10 jawaban/hari, doktrin masuk mana yang memaksimalkan nilai harapan per jawaban: (a) masuk instan <2 menit mengejar Pioneer, (b) masuk telat berdiferensiasi pada tunda 2–6 jam mengejar seleksi marathon/Innovator, atau (c) alokasi campuran — dan sinyal teramati apa (laju jawaban masuk per menit? ukuran kerumunan saat itu?) yang harus memicu perpindahan mode di antara keduanya?*
2. *Keunggulan masuk-telat di pertanyaan banjir lebih baik dijelaskan oleh (i) waktu seleksi kanal marathon yang memang berjalan lambat, atau (ii) runtuhnya mutu banjir awal (jawaban bot massal di 2 menit pertama yang disaring keluar)? Pengukuran tambahan apa yang paling tajam membedakan kedua penjelasan itu?*
3. *Bila hambatannya adalah penugasan panel (bukan mutu penilaian), apakah strategi "lebih sedikit jawaban, lebih telat, lebih terdiferensiasi" mengalahkan strategi volume di bawah cap harian yang keras — dan pada angka peluang berapa (0,44 dataran posisi vs 0,50–0,63 masuk telat) titik baliknya?*
