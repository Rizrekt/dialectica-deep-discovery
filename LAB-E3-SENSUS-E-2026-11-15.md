# LAB LINI B — E3 + SENSUS E1 + PINTU (e)
### Dialectica · disusun 2026-11-15 malam (untuk lab Senin 2026-11-16)
### Sumber SAH: DRILL-LOG.md (dibaca penuh, entri terakhir = drill 19:00 15 Nov), MEKANISME-DAN-LAPANGAN.md (§82, §96–§105 + grep E1/E3/(e)), KORPUS-JUARA-2026-11-14.md (§8 + tabel butir 135), VERDICT-LEDGER.md (baris #5–#8), QUALITY.md baris 147–153 (definisi + ambang E3, dibaca saja — TIDAK diedit), file drill run-2026-11-13/14/15 di hidden_files goal.
### Aturan: tidak ada klaim/serve/config yang diubah dokumen ini. Angka tanpa sumber file tidak ditulis.

---

# BAGIAN 1 — E3: PUTUSAN USUL ADOPSI "PENUTUP EVASIF SUMBER"

## 1.1 Definisi + ambang (QUALITY.md baris 147–153)

E3 = eksperimen di QUALITY.md: "Penutup evasif sumber = gagal (e) + bendera (d)". Celah asal: probe Gemini §29.2 — penutup berbentuk "note on sources" yang MENGHINDARI penyebutan sumber persis, alih-alih menamai kebaruan; rubrik (e) v1 tidak punya cek negatif untuk bahasa penghindaran sumber.

**Ambang adopsi tertulis di QUALITY.md:** ≥2 kemunculan pada jawaban GAGAL verdict, **ATAU** 1 kemunculan pada jawaban KITA yang falsified/gagal-aturan. Kemunculan yang ternyata lolos verified berulang → hipotesis ditolak beralasan.

Frasa verbatim yang menjadi spesimen: *"Note on sources: this answer relies on widely documented, independently checkable public records and scholarship rather than on any single citation, and it avoids pinpoint references that cannot be verified from the text alone."* (teks terkirim f0bb3586, run-2026-11-14-0900/answer-f0bb3586.txt; dikutip juga di VERDICT-LEDGER baris #7/#8 dan DRILL-LOG 15 Nov 07:00).

## 1.2 Kemunculan di jawaban KITA yang falsified — 4/4 (100% falsified serve)

| # | ISO kita | ISR | Verdict | Panel | Bukti penutup evasif |
|---|---|---|---|---|---|
| 1 | f0bb3586 | 1287c2ae (LRT leverage cascades) | FALSIFIED 14 Nov 08:09 | 0 sup / 2 ref / 2 ver (amendemen 15 Nov; awalnya panel 1) | Penutup verbatim "avoids pinpoint references" — VERDICT-LEDGER #5; DRILL-LOG 14 Nov 09:00; MEKANISME §82 |
| 2 | 7d81c51d | 30fe9eea (semikonduktor) | FALSIFIED 15 Nov 04:49 | 0/4/5 | Penutup evasif sumber ("avoids pinpoint references") — VERDICT-LEDGER #6; MEKANISME §96 |
| 3 | 5b5e8212 | a361a16b (NFT mints young chain) | FALSIFIED 15 Nov 06:03 | 0/4/6 | Penutup evasif verbatim yang sama — VERDICT-LEDGER #7; DRILL-LOG 15 Nov 07:00 |
| 4 | a3b8b34a | 3884b6c3 (holder token Solana) | FALSIFIED 15 Nov 06:43 | 0/6/6 | Penutup evasif verbatim yang sama — VERDICT-LEDGER #8; DRILL-LOG 15 Nov 07:00 |

DRILL-LOG 15 Nov 07:00 menyatakan eksplisit: "E3 DIPERKUAT — kini 4 instance pada jawaban KITA yang falsified… **4/4 = 100% falsified serve.** Ambang adopsi E3 (≥2 pada jawaban gagal, atau 1 pada jawaban kita yang falsified) kini terpenuhi ×4."

Catatan cakupan: keempatnya jawaban SERVE Vyce pagi 14 Nov (jalur tanpa gerbang saat itu). Nol kemunculan pada 3 klaim one-shot kita yang falsified (fcb7b015, 097df475, 0d76cc7c — VERDICT-LEDGER #1–#3 tidak mencatat penutup evasif; 0d76cc7c justru menutup dengan penamaan kebaruan "Baru dalam jawaban ini:…" — DRILL-LOG 14 Nov 19:00). Jadi sinyal E3 sejauh ini spesifik spesies serve-mentah, bukan pola umum jawaban kita.

## 1.3 Kemunculan di jawaban VERIFIED publik — 0 (false-positive rate 0,0%)

- **KORPUS-JUARA-2026-11-14.md baris 135:** "Penutup evasif sumber (regex frasa eksplisit): **0/203 verified** dan 0/64 falsified pada panel ini". Baris 175–177 (§8 korpus): regex frasa eksplisit menemukan 0/203 verified — korpus eksternal tidak menambah maupun membantah bukti E3; dasar adopsi bertumpu pada bukti internal.
- **Drill 13–15 Nov:** setiap drill yang memeriksa menyatakan 0× "avoids pinpoint references" pada jawaban publik yang dibedah (verified maupun falsified) — a.l. DRILL-LOG 15 Nov 09:00 ("0× 'avoids pinpoint references' + 0× 'Let Me' di keempat jawaban"), 11:00, 13:00, 15:00, 17:00, 19:00 (semua: "E3: tetap TERPENUHI ×4 (0× 'avoids pinpoint references'…)" atas jawaban publik di ISR 2d968d7e).
- **Satu-satunya kemunculan bahasa penundaan-verifikasi pada verified publik BUKAN frasa verbatim dan BUKAN di penutup:** 0006fe08 (verified, sup 4, DRILL-LOG 11 Nov 07:00) memuat "verify exact current values in the live docs" di badan §0 — dicatat drill sebagai "penundaan verifikasi gaya E3 di badan". Implikasi presisi gerbang: cek E3 wajib dibatasi pada (i) frasa verbatim/keluarga eksplisit dan (ii) posisi penutup/seksi sumber — BUKAN sembarang bahasa penundaan di badan, agar false-positive tetap 0.

**False-positive rate terukur: 0/203 = 0,0%** (panel KORPUS-JUARA) + 0 pada semua set verified yang di-drill 13–15 Nov.

## 1.4 Kemunculan di jawaban FALSIFIED publik — 0 verbatim; 1 varian keluarga

- **Verbatim: 0/64** pada panel falsified KORPUS-JUARA (baris 135).
- **Varian keluarga (pengakuan penghindaran sumber dengan redaksi berbeda): 1 instance terdokumentasi** — e9fed6e7 (falsified publik, panel 1, DRILL-LOG 14 Nov 13:00; teks di run-2026-11-14-1300/drill-ans-e9fed6e7.txt): *"I had no live web access in this session and did not open any page or dataset… I give no URLs for that reason."* — pengakuan eksplisit tidak-bisa-mensitasi di kepala jawaban; terhitung sebagai E1 klasik ke-33 di drill itu. Redaksinya berbeda dari frasa verbatim serve kita, jadi regex verbatim saja TIDAK menangkapnya — keluarga frasa harus mencakup pola pengakuan "no live web access / I give no URLs / cannot verify from the text" dan sejenisnya.

## 1.5 VONIS E3: **ADOPSI — sebagai KEDUANYA (sinyal tahan gerbang serve + cek negatif rubrik)**

Alasan berangka:
1. Ambang tertulis QUALITY.md terlampaui **×4** di cabang terkuatnya (1 kemunculan di jawaban kita yang falsified saja cukup; teramati 4, dan itu 4/4 = 100% falsified serve kita).
2. False-positive terukur **0,0%** (0/203 verified KORPUS-JUARA; 0 di semua drill 13–15 Nov) — syarat diam-diam setiap gerbang keras: tidak membunuh jawaban yang akan verified.
3. Sinyal ini MURAH dan mekanis (regex frasa) — tidak butuh penilaian semantik; cocok sebagai lapis tahan, bukan sebagai vonis isi.
4. Batas jujur: korpus eksternal TIDAK mengoroborasi (0/64 falsified publik verbatim) — adopsi bertumpu pada bukti internal 4/4, persis seperti dirumuskan KORPUS-JUARA §8. Karena itu bentuk adopsinya ganda dan berlapis, bukan pengganti (d): penutup evasif tidak pernah menjadi satu-satunya alasan sebuah jawaban dinyatakan buruk isinya; ia memicu tahan + periksa-(d).

Bentuk adopsi yang diputuskan:
- **(A) Gerbang serve (dan wrapper klaim): SINYAL TAHAN KERAS.** Draf yang memuat frasa verbatim atau keluarga penghindaran sumber di penutup/seksi sumber = TAHAN (tidak terkirim), tanpa pengecualian — spesies ini 4/4 falsified di jalur serve, dan serve tidak punya kesempatan koreksi manusia per draf.
- **(B) Rubrik (e)/(d): CEK NEGATIF.** Penutup evasif sumber = (e) GAGAL + bendera (d) (seluruh angka badan diperiksa ulang), sesuai rumusan asal E3 di QUALITY.md. Bukan pintu mati mandiri di luar (e)/(d).

## 1.6 Draf teks butir gerbang (untuk dimasukkan lab ke QUALITY.md — DRAF, file ini tidak mengedit QUALITY.md)

> **E3 — DIADOPSI (lab 2026-11-16). Penutup evasif sumber = TAHAN di gerbang + gagal (e) + bendera (d).**
> Sebuah draf DITAHAN (jalur serve: tidak dikirim; jalur klaim: sendable=false) bila penutup atau seksi sumbernya memuat penghindaran sumber eksplisit, termasuk namun tidak terbatas pada: frasa "avoids pinpoint references", "cannot be verified from the text alone", "relies on widely documented … rather than on any single citation", "no live web access", "I give no URLs", atau pengakuan setara bahwa sumber persis tidak bisa/tidak akan disebutkan.
> Dalam penilaian rubrik, penutup semacam itu = (e) GAGAL dan memicu pemeriksaan ulang (d) atas seluruh angka di badan.
> Dasar: 4/4 falsified serve kita (f0bb3586, 7d81c51d, 5b5e8212, a3b8b34a) membawa penutup verbatim yang sama; 0/203 verified + 0/64 falsified pada panel KORPUS-JUARA-2026-11-14 (false-positive 0,0%); 1 varian keluarga pada falsified publik (e9fed6e7). Cek dibatasi pada frasa eksplisit di penutup/seksi sumber — bahasa penundaan di badan (mis. "verify exact current values in the live docs" pada verified 0006fe08) BUKAN pemicu.
> Regex hanya menangkap frasa eksplisit; penghindaran terparafrase lolos dari cek ini dan tetap wilayah (d) manual.

---

# BAGIAN 2 — SENSUS E1 TERBARU (hitung ulang dari semua drill 10–15 Nov di DRILL-LOG)

Garis banding resmi (drill 19:00 15 Nov, entri terakhir DRILL-LOG): E1 stabil 43 · anomali (e) 23/24 · kalibrasi T12 observasi ke-10 · falsified-with-support #3 · E1-p 4 · E3 TERPENUHI ×4.
**Hasil hitung ulang: SEMUA item COCOK dengan garis banding — delta 0 di semua item.** Tidak ada entri drill sesudah 19:00 15 Nov di DRILL-LOG, jadi sensus 19:00 adalah sensus terbaru dan hitung ulang ini adalah verifikasi, bukan pembaruan angka.

## 2.1 E1 klasik (seri penomoran berjalan di DRILL-LOG) — **43** (Δ 0)

Rantai penomoran terverifikasi dari teks drill: ke-1…ke-5 (10–11 Nov) → ke-6 (12 Nov 07:00, 575fd2af) → ke-7+ke-8 (12 Nov 09:00, 0be4bf85 + 755b3f19) → ke-9 (12 Nov 11:00, 520bf8d5) → ke-10 (12 Nov 13:00, 9a0bff32) → ke-11 (12 Nov 15:00, 4e56a565) → ke-12+ke-13 (12 Nov 17:00, 967bceaa + 01e1e8aa) → ke-14 (12 Nov 19:00, 8539092c) → ke-15 (12 Nov 21:00, 14d80f68) → ke-16 (13 Nov 07:00, 71bcad0b) → ke-17+ke-18 (13 Nov 09:00, 6abad527 + 6bb64cff) → ke-19+ke-20 (13 Nov 11:00, ca2a8aa2 + 5a5f2f74) → ke-21 (13 Nov 13:00, 1e0e3edf) → ke-22 (13 Nov 15:00, 9fc90965) → ke-23+ke-24 (13 Nov 17:00, a82107d3 + 3c1e9431) → ke-25+ke-26 (13 Nov 19:00, 26b8230a + 813800bb) → ke-27 (13 Nov 21:00, 9650c6c7) → ke-28+ke-29 (14 Nov 07:00, 96392f0a + 7ed2e27a) → ke-30 (14 Nov 09:00, f0bb3586 — jawaban KITA) → ke-31+ke-32 (14 Nov 11:00, 8c00c646 + ed016bc7) → ke-33 (14 Nov 13:00, e9fed6e7) → ke-34+ke-35 (14 Nov 15:00, b17d0bdc + 7852a52d) → ke-36+ke-37 (14 Nov 17:00, d65d4ebf + da8abe7f) → ke-38 (14 Nov 19:00, 24a0e59a) → ke-39 (14 Nov 21:00, cd923ee6) → ke-40+ke-41 (15 Nov 07:00, 5b5e8212 + a3b8b34a — jawaban KITA) → ke-42+ke-43 (15 Nov 09:00, ef958ba0 + b02dc28e).
Drill 15 Nov 11:00/13:00/15:00/17:00/19:00 semuanya menyatakan "E1: tetap 43" (kandidat Odd Sequence/Octane di 11:00 terselesaikan sebagai BUKAN E1 di 13:00 sesudah buka-dan-baca). **Δ lawan garis banding: 0.**
Catatan komposisi: ke-42 (ef958ba0) adalah kemunculan pola E1 pada jawaban **VERIFIED + AWARDED** (data kalibrasi (d), bukan falsified) — seri E1 menghitung kemunculan pola, bukan hanya falsified. Dari 43: 3 di antaranya jawaban kita (ke-30, ke-40, ke-41).

## 2.2 E1-p "pinjam angka dari jawaban lain" — **4 instance** (Δ 0)

| # | Jawaban | Drill | Milik siapa |
|---|---|---|---|
| 1 | b17d0bdc (15.039 kar, 0 URL; angka "disitasi" ke Answer 1/2/3/4/5/6) | 14 Nov 15:00 (sub-pola lahir di sini) | Publik, falsified |
| 2 | 24a0e59a (klaim dirujuk "per Answer 4/6/2") | 14 Nov 19:00 ("E1-p — instance ke-2") | Publik, falsified |
| 3 | 5b5e8212 (22× "Answer 41" sebagai sumber angka poros) | 15 Nov 07:00 | **KITA (serve), falsified** |
| 4 | a3b8b34a (43× kutipan "Answer N": 21/33/41/43/44/45/46/47/49/51/53/55) | 15 Nov 07:00 | **KITA (serve), falsified** |

Koreksi atas ringkasan garis banding: E1-p BUKAN "semua di falsified serve kita" — 2 instance publik + 2 instance kita. Drill 15 Nov 07:00: "E1-p kini 4 instance — pola DOMINAN di jawaban serve-mentah (2/2 drill ini)". Kalibrasi definisi (drill 15 Nov 11:00): 6× "Answer N" pada F2 9014180c adalah ringkasan meta, BUKAN peminjaman angka → tidak dihitung. Terbuka untuk lab: apakah E1-p sub-bentuk E1-h atau varian terpisah (diminta drill 15 Nov 07:00). **Δ: 0.**

## 2.3 E1-c — **label bertabrakan: 2 sub-pola memakai nama yang sama** (Δ 0 instance baru sejak 14 Nov)

DRILL-LOG memakai "E1-c" untuk DUA hal berbeda — lab wajib membereskan penamaan ini:
- **E1-c (makna pertama, lahir 12 Nov 13:00): "angka benar, atribusi mekanisme/kausal salah"** — instance: 9a0bff32 (Rari Fuse $80M benar, dilabel manipulasi TWAP padahal reentrancy) = #1; komponen kausal-salah juga dicatat di dalam entri E1 ke-14 atas 8539092c (12 Nov 19:00: MISO 2021 disebut "migration bug" — insidennya exploit lelang; Fei 2021 disebut "TWAP oracle manipulation at graduation" — masalahnya genesis/PCV) = kemunculan ke-2 (tidak dinomori terpisah). Drill-drill 15 Nov memeriksa eksplisit: "E1-c: TIDAK ada instance baru" (dengan makna ini).
- **E1-c (makna kedua, lahir 14 Nov 17:00): "klaim-korpus-salah-baca"** — d65d4ebf mengklaim "the dump has 0 hits for Arbitrum, Optimism, OP Stack, EIP-4844…" yang salah pada bacaan natural (5 jawaban lain menyebut Arbitrum). 1 instance. Drill 14 Nov 21:00 sudah mencatat utang penamaan terkait: "E1-a/E1-b TIDAK ditemukan definisinya di DRILL-LOG/MEKANISME/QUALITY.md — seri bernama yang tercatat dimulai di E1-c; lab diminta menamai/mengonfirmasi."
**Δ lawan garis banding: 0** (garis banding tidak membawa angka E1-c tunggal; kedua makna dilaporkan apa adanya: kausal 2 kemunculan, korpus 1 instance).

## 2.4 Falsified-with-support — seri berlabel **#3** (Δ 0); sensus penuh jauh lebih banyak

Seri penomoran eksplisit di drill 15 Nov: **#1** 800139cc (sup 1/ref 1/ver 2 — DRILL-LOG 15 Nov 09:00), **#2** 9014180c (sup 1/ref 1/ver 2 — 15 Nov 11:00), **#3** 043fa4d0/F8 (sup 1/ref 1/ver 2 — 15 Nov 19:00). **Δ lawan garis banding #3: 0.**
Kejujuran cakupan: angka #3 adalah seri berlabel 15 Nov, BUKAN total historis. Sensus ISR penuh di DRILL-LOG mencatat banyak falsified-dengan-support sebelumnya, a.l.: 509b71b7 (1/1), d6b530d6 (1/1), 4e56a565 (1/1), 66111a1d (1/1), 108d98c8 (1/1), 16d99053 (2/2), 02104185 (1/1), 4019e71c (1/1), 2c07b25c (1/1), 0a787e44 (1/1), 49b1b911 (1/1), 141c8e30 (1/1), dd2f013d (1/1), c3a24e8c (1/1), 23c21370 (1/1), 7dce194b (1/1), 0f9e1d03 (1/1), 38dd66dd (2/2), 7852a52d (3/1), fcb7b015 (2/2 — klaim #1 KITA). Pola yang bertahan di semua: ≥1 refutasi = falsified, support tidak pernah menyelamatkan.

## 2.5 Panel-1 falsified — seri drill-scored 5 observasi s/d 17:00 15 Nov; sensus ISR menambah lebih banyak (Δ 0 sejak 19:00)

- Drill-scored/berlabel seri: f0bb3586 (KITA — "panel verifier = 1 pertama kali teramati", 14 Nov 09:00); 49c5ba76 (14 Nov 21:00); ccba9ede + b02dc28e ("panel-1 falsified ke-3 + ke-4 dalam seri", 15 Nov 09:00); e7fc0deb (15 Nov 17:00 — entri itu menyebut "panel-1 falsified kini 5 observasi dalam seri termasuk f0bb3586").
- Instance sensus-ISR (bukan drill-scored): 89a16c1f (14 Nov 21:00); e9fed6e7 (ver 1, 14 Nov 13:00); 5× di ISR 48c80dc6 (8c00c646, ed016bc7, b8ad62b0, 36c1c4cc, d072cd11 — sensus 14 Nov 11:00); 3× di ISR 2d968d7e (01a18d93, c90751de, b1485c03 — 15 Nov 15:00).
- 19:00 15 Nov: TIDAK ada panel-1 baru (F8 043fa4d0 = panel 2). Sisi verified panel-1 MASIH belum teramati (L-02 terbuka; 36492578 masih revealed sup 1/ref 0/ver 1 per drill 19:00). **Δ: 0.**

## 2.6 Sensus ISO ber-verdict (aturan clean sheet) — **391 iso, 0 penyimpangan** (Δ 0)

Rantai kumulatif di DRILL-LOG: 77 (3 ISR, 12 Nov 21:00) → 102 (13 Nov 09:00) → 143 (13 Nov 11:00) → 157 (13 Nov 13:00) → 190 (13 Nov 15:00) → 217 (13 Nov 17:00) → 244 (13 Nov 19:00) → 276 (13 Nov 21:00) → 280 (14 Nov 07:00) → 283→291 (14 Nov 09:00/11:00) → 296 (14 Nov 13:00) → 316 (14 Nov 15:00) → 339 (14 Nov 17:00) → 354 (14 Nov 19:00) → 363 (14 Nov 21:00) → 372 (15 Nov 09:00) → 377 (15 Nov 11:00) → 379 (15 Nov 13:00) → 387 (15 Nov 15:00) → 390 (15 Nov 17:00) → **391 (15 Nov 19:00)**. Aturan "verified ⟺ ≥2 support DAN 0 refutasi" + "1 refutasi membunuh" bertahan di panel 1, 2, 3, 4, 5, 6 tanpa satu pun penyimpangan. **Δ lawan garis banding: 0** (garis banding tidak membawa angka sensus; angka terakhir tercatat memang 391).

## 2.7 Item garis banding lain — verifikasi

| Item | Garis banding 19:00 | Hitung ulang | Δ |
|---|---|---|---|
| E1 klasik | 43 | 43 (§2.1) | 0 |
| E1-p | 4 | 4 (§2.2) | 0 |
| E3 | TERPENUHI ×4 | ×4 (§1.2) | 0 |
| Anomali (e) | 23/24 verified gagal (e) | 23/24 (drill 19:00: "was 21/22" → +V10/V11 gagal = 23/24) | 0 |
| Kalibrasi T12 | observasi ke-10 | ke-10 (V10 densitas 0,37 gagal K-1 tapi VERIFIED — drill 19:00) | 0 |
| Falsified-with-support | #3 | #3 (§2.4) | 0 |
| Proksi-(i) disagreement | ke-11 (dari drill 15:00) | ke-11; 17:00 + 19:00 menyatakan tidak ada yang baru | 0 |
| Spesies "jawaban terpotong" | ke-16 + kandidat pra-penutup ke-17/18/19/20/21 menunggu klasifikasi lab | sama (19:00: tidak ada kandidat baru, tetap ke-21) | 0 |

---

# BAGIAN 3 — PINTU (e): PENAMAAN KEBARUAN EKSPLISIT "Baru dalam jawaban ini:"

## 3.1 Keadaan data: (e) gagal di 23/24 verified — pintu ini hampir tidak memprediksi verdict

Anomali berjalan di DRILL-LOG: 11/12 (14 Nov 21:00) → 12/13 (15 Nov 09:00) → 14/15 (11:00) → 16/17 (13:00) → 18/19 (15:00) → 21/22 (17:00) → **23/24 (19:00)** verified GAGAL (e) v2. Penyebab dominan kegagalan BUKAN premis palsu, melainkan PENEMPATAN: penutup berupa daftar References/Sources, atau kebaruan dinamai hanya di pembuka. (e) membedakan penuh hanya di 2-dari-9 ISR (14 Nov 07:00 sebagian, 14 Nov 11:00 penuh bersama (d)); di ISR lain ia mati total atau TERBALIK (memb
...[truncated 8189 chars]