# RAMALAN 22 REVEALED — Fase Testing Dialectica (2026-11-17)

> Perintah user 2026-11-17 03:48 (Opsi A, tugas 2). **Ini RAMALAN peniru-verifier (C5 `semantic_check` mode shadow), BUKAN verdict server.** Panel server nyata yang akan memutuskan; ramalan ini mengukur seberapa buruk draf-draf itu terlihat di mata rubrik live arena. Read-only total: tidak ada submit/answer/claim; status live ditarik ulang pagi ini via klien resmi.

## 1. Korpus — 22 dari 22 terkumpul, terverifikasi live

- Sumber teks: snapshot lokal ISO di folder run hunt (artefak serve pra-gerbang 14 Nov) — ISO kita total **29** = 7 falsified + **22 revealed**, cocok persis dengan cacah server (29 completed).
- **Status live pagi ini (tarik ulang `/api/node/isos/<isr>` per item): ke-22nya MASIH `revealed`** — belum satu pun ber-verdict; tidak ada yang berubah sejak sweep run-10 (02:37).
- Teks lengkap ke-22nya ada (31–45 ribu karakter per jawaban — spesies jejak panjang pra-gerbang). Nol teks karangan; nol id hilang.
- Kandidat E1-p: **`00d9335b` dan `24f3a79b` BUKAN bagian dari 22 ini** — keduanya jawaban ahli lain (`isOwnAgent=False`, tarikan run-10 02:37): `00d9335b` masih revealed (support/refute 1/0) di ISR df9cb696; `24f3a79b` **verified** (2/0) — cocok dengan catatan learning-watch run-10 (verified 21:12 16 Nov).

## 2. Hasil per jawaban

Pemeriksa: Nemotron — lane Vyce diutamakan (aturan bahan bakar), jatuh ke OpenRouter hanya saat Vyce gagal per panggilan. Dari 22: **6 vonis via vyce-nemotron, 11 via openrouter-nemotron, 5 unavailable** (lihat §4).

| ISO | ISR | Vonis ramalan | Kode temuan | Sub penekanan |
|---|---|---|---|---|
| `02b24949` | `d854b19a` | fatal | SURPRISE_GAUGE | — |
| `0c4d45b8` | `087ce951` | fatal | CUSTOMER_REQUIREMENTS, A_CITATION×4, SURPRISE_GAUGE | S-4, S-1×3 |
| `1869839d` | `970d09db` | fatal | CUSTOMER_REQUIREMENTS, A_CITATION, A_UNCERTAINTY, SURPRISE_GAUGE | S-4 |
| `1a502a51` | `a5f24a48` | fatal | CUSTOMER_REQUIREMENTS | — |
| `1b7476cf` | `30608eca` | fatal | CUSTOMER_REQUIREMENTS, A_CITATION×4, A_REASONING | S-4×2, S-1×2 |
| `2549fe17` | `0dbd4532` | fatal | A_CITATION×3, CUSTOMER_REQUIREMENTS, A_REASONING, A_UNCERTAINTY | S-4, S-1 |
| `26d732da` | `c5927d00` | fatal | CUSTOMER_REQUIREMENTS | — |
| `49740377` | `1f58031d` | fatal | A_CITATION×9, A_UNCERTAINTY | S-4×3, S-1×5 |
| `5c9cdb9e` | `530e95ec` | fatal | CUSTOMER_REQUIREMENTS, A_CITATION×3, A_SCOPE | S-1×2, S-4 |
| `5e8c32a5` | `79f751ce` | fatal | CUSTOMER_REQUIREMENTS | — |
| `8671364d` | `026fa1a2` | unavailable | — | — |
| `9ebb44a0` | `8f4b9221` | fatal | CUSTOMER_REQUIREMENTS, A_CITATION | S-1 |
| `a1fe6c64` | `77f1e68b` | fatal | CUSTOMER_REQUIREMENTS | — |
| `a5ed3b79` | `c1ef7bd8` | fatal | A_CITATION×5, A_UNCERTAINTY | S-1×3, S-4×2 |
| `a94e95bf` | `3883f4d9` | fatal | CUSTOMER_REQUIREMENTS | — |
| `ce1c34f3` | `cc856ac0` | fatal | CUSTOMER_REQUIREMENTS, A_SCOPE, A_CITATION×3, A_REASONING | S-1×3 |
| `d68a165a` | `2133a697` | fatal | A_CITATION×6, CUSTOMER_REQUIREMENTS | S-1×4, S-4×2 |
| `f131675d` | `c7cc33a2` | unavailable | — | — |
| `f18b1675` | `e20d251f` | unavailable | — | — |
| `f5224761` | `a1770c04` | unavailable | — | — |
| `f8801972` | `c6b0eadc` | unavailable | — | — |
| `f8e22374` | `7401386a` | fatal | CUSTOMER_REQUIREMENTS | — |

**Agregat: 17 terperiksa ber-vonis → 17 FATAL, 0 clean.** Total 65 temuan terverifikasi-kutipan: A_CITATION 39 (sub S-1 ×24, S-4 ×13), CUSTOMER_REQUIREMENTS 14, A_UNCERTAINTY 4, SURPRISE_GAUGE 3, A_REASONING 3, A_SCOPE 2. Profil racunnya persis spesies yang membunuh 4 serve falsified kita: angka tak terikat (S-1) + fakta diatribusikan ke "Answer N" (S-4) — massal, merata, bukan tempelan di satu-dua item.

## 3. Proyeksi dent (saldo kini −1,8788; falsified = −1 per jawaban, terbukti dari ledger: 7 × −1 = −7,0 di dashboard)

| Skenario | Asumsi | Falsified | Dent | Saldo proyeksi |
|---|---|---|---|---|
| **Lunak** | Hanya temuan presisi-tinggi yang dihitung (fatal memuat S-4/S-2/A_SCOPE — sub yang menurut KALIBRASI-C5 §5 paling jarang overreach): 9 item | 9 | −9 | **−10,8788** |
| **Tengah** | PPV kalibrasi murni: pemeriksa menandai fatal 7/7 racun benar dan 4/6 bersih → PPV 7/11 ≈ 0,64 → 17 × 0,64 ≈ 11 | ±11 | ±−11 | **±−12,88** |
| **Keras** | Checker literal: semua 17 fatal jadi falsified; 5 unavailable dianggap lolos | 17 | −17 | **−18,8788** |
| **Keras penuh** | 5 unavailable ikut falsified (tidak terukur — bukan nol, hanya belum terbaca) | 22 | −22 | **−23,8788** |

Jangkar populasi yang menekan skenario tengah ke atas: jawaban serve pagi yang sama yang **sudah** ber-verdict server = **4 falsified dari 4** (f0bb3586, 7d81c51d, 5b5e8212, a3b8b34a — 0 verified). Ke-22 ini lahir dari pipa tanpa gerbang yang sama, pagi yang sama, dan profil temuan C5-nya sebangsa. Skenario tengah PPV mengasumsikan populasi campuran seperti korpus kalibrasi (jawaban ahli lain yang verified) — populasi kita lebih buruk dari itu.

**Dampak RAR:** RAR kini 118 (reliability −5, availability 29, reputation 94), suspensionCount sudah 5. Setiap falsified menekan reliability lebih dalam (besaran persis per falsified tidak dipublikasikan server — tidak diarang di sini); gelombang falsified massal adalah risiko suspensi lanjutan, bukan cuma risiko saldo. Yang pasti terukur: saldo bergerak −1 per falsified dan tidak ada satu pun dari 22 ini yang bisa menghasilkan +20/+10/+10 dalam keadaan revealed — upside-nya sudah mati di liveness sejak awal (§82), downside-nya yang masih hidup.

## 4. Yang tidak terperiksa — 5 unavailable (jujur apa adanya)

| ISO | Sebab |
|---|---|
| `8671364d` | Vyce gagal (konten kosong, reasoning meluap) → OpenRouter menjawab tapi balasannya bukan JSON terparse → cek tidak berjalan |
| `f131675d`, `f18b1675`, `f5224761`, `f8801972` | Vyce gagal (spesies sama: `nemotron-3.5-super-vl` membakar budget di reasoning_content 25–32 ribu karakter, konten kosong) → OpenRouter **menolak berangkat**: sisa kuota free terbaca **1 < 2** — cadangan bahan bakar pemeriksa habis di tengah run |

Pola kegagalannya sendiri adalah temuan: pemeriksa Nemotron-Vyce tidak stabil pada draf raksasa 31–45 ribu karakter (di kalibrasi drafnya lebih pendek dan lane ini hanya jadi cadangan tak terpakai). 22 panggilan Vyce dicoba (1 per item), 15 kali jatuh ke OpenRouter, 11 menghasilkan vonis; kuota free OpenRouter berakhir di sisa 1.

## 5. Batas ramalan ini

1. **Peniru ≠ panel.** C5 meniru rubrik; verifier server menilai bentuk dengan cara mereka sendiri — riwayat kita memuat jawaban yang drill ramalkan sebaliknya dan tetap verified (24f3a79b). Angka di §3 adalah pita skenario, bukan ramalan titik.
2. **Ekor draf tak terbaca pemeriksa:** draf dipotong 28.000 karakter (dari 31–45 ribu) + pertanyaan 12.000 — racun yang menumpuk di ekor lolos dari jangkauan (KALIBRASI-C5 §6.5).
3. **Varians antar-run nyata** (KALIBRASI-C5 §6.1): satu item = satu sampel.
4. **SURPRISE_GAUGE nyaris senyap secara desain:** konteks pemeriksa hanya teks pertanyaan, tanpa jawaban verified yang sudah ada — 3 temuan SURPRISE_GAUGE yang muncul datang dari konteks pertanyaan yang memuat jawaban lain.

*Hasil mentah per item (temuan + kutipan lengkap): `dryrun-2026-11-17/ramalan22-results.json`; log pemeriksa: `/tmp/ramalan22-semantic-log.jsonl` (22 record).*

## 6. Ronde 2 — 2026-11-17 ±04:35–04:52 (PERBAIKAN-PENGHAMBAT langkah 3: pemeriksa tersegmentasi)

Perbaikan: `semantic_check` kini memecah draf >10.000 kar jadi segmen ≤10.000 kar (batas blok; segmen = substring persis draf), memeriksa tiap segmen terpisah, menggabungkan temuan, dan tetap memverifikasi kutipan terhadap teks draf UTUH; seksi Sources draf ikut dibawa di tiap segmen supaya sitasi di ekor tidak membuat angka di kepala kena S-1. Kelima item unavailable ronde 1 diperiksa ulang (pemeriksa Nemotron, lane Vyce diutamakan; OpenRouter tetap terhalang kuota sisa 1 < 2 di semua panggilan):

| ISO | ISR | Lane pemeriksa | Segmen ok/total | Vonis ronde 2 | Kode temuan | Sub penekanan |
|---|---|---|---|---|---|---|
| `8671364d` | `026fa1a2` | vyce-nemotron | 4/5 | **fatal** | CUSTOMER_REQUIREMENTS ×1, A_CITATION ×11 | S-1 ×9 |
| `f18b1675` | `e20d251f` | vyce-nemotron | 2/5 | **fatal** | A_CITATION ×3 | S-1 ×1 |
| `f5224761` | `a1770c04` | vyce-nemotron | 2/5 | **fatal** | A_CITATION ×2, CUSTOMER_REQUIREMENTS ×1 | S-1 ×1, S-4 ×1 (1 kutipan gugur) |
| `f8801972` | `c6b0eadc` | vyce-nemotron | 0/5 → 1/5 (pengulangan konfigurasi sama) | **fatal** | A_CITATION ×6 | S-4 ×5, S-1 ×1 |
| `f131675d` | `c7cc33a2` | vyce-nemotron | 0/5 → 0/5 → 1/9 (segmen 5 rb) | **fatal** | A_CITATION ×4 | S-1 ×2, S-4 ×2 |

**Agregat akhir 22/22: 22 FATAL, 0 clean, 0 unavailable.** Temuan ronde 2: 28 (A_CITATION 26, CUSTOMER_REQUIREMENTS 2; sub S-1 ×14, S-4 ×8) — total gabungan dua ronde **93 temuan terverifikasi-kutipan**.

Proyeksi dent diperbarui (saldo kini −1,8788; basis skenario sama dengan §3):

| Skenario | Asumsi | Falsified | Saldo proyeksi |
|---|---|---|---|
| **Lunak** | Hanya item ber-sub presisi-tinggi (S-4/S-2/A_SCOPE): 9 ronde 1 + 3 ronde 2 (f5224761, f8801972, f131675d) | 12 | **−13,8788** |
| **Tengah** | PPV kalibrasi 0,64 × 22 ≈ 14 | ±14 | **±−15,88** |
| **Keras (checker literal)** | Semua 22 yang kini TERUKUR fatal jadi falsified | 22 | **−23,8788** |

Catatan kejujuran ronde 2 (bahan PERBAIKAN-PENGHAMBAT-2026-11-17.md langkah 3):

1. **Cakupan per item parsial:** segmen yang berhasil cuma 1–4 dari 5–9 — kolaps lane Vyce bersifat stokastik per panggilan (reasoning_content 26–33 rb kar, konten kosong), tidak murni digerakkan ukuran segmen (10 rb vs 5 rb sama-sama pernah 0/total). Temuan per item adalah **lantai bawah**, bukan cacah penuh; vonis fatal tetap sah karena fatal cukup ≥1 temuan terverifikasi-kutipan, tetapi seandainya ada item yang tampak clean dari cakupan parsial, clean-nya tidak akan bisa dipercaya — tidak ada yang clean.
2. **Satu variabel percobaan sempat tercemar:** upaya pertama segmen "5 rb" untuk f8801972/f131675d sebenarnya mengulang konfigurasi 10 rb (argumen default `_split_draft_segments` terikat saat definisi fungsi, patch konstanta modul tidak berlaku) — keberhasilan f8801972 adalah pengulangan 10 rb yang kebetulan 1 segmennya lolos. Angka 5 rb yang asli hanya f131675d (1/9).
3. Hasil mentah ronde 2: `dryrun-2026-11-17/ramalan22-round2-results.json`, `ramalan22-round2b-f8801972.json`, `ramalan22-round2c-f131675d.json`.
