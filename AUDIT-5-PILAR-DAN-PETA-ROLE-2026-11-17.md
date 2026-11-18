# Dialectica — Audit 5 Pilar + Peta Role (2026-11-17)

> Perintah user 2026-11-17 01:57–02:08 WIB: konsep role make.fun dibawa ke Dialectica, TAPI 3 pilar dicek dulu; user lalu bertanya apakah 3 pilar cukup (game Dialectica beda dari make.fun) dan MENYETUJUI struktur 5 pilar + aturan berdiri baru: **5 pilar wajib dicek dulu setiap mengerjakan tugas Dialectica.**
> Audit dijalankan 5 lini paralel dari file primer di disk; berkas per pilar di `audit-pilar-sementara/` (PILAR-1/2/3 + PILAR-TAMBAHAN-A/B).
> Keadaan akun yang dikutip = bacaan dokumen terakhir (MEKANISME §127, tutup 16 Nov 23:00 WIB) — BUKAN bacaan live.

## 1. JAWABAN SOAL BENTUK GAME: SATUANNYA PER JAWABAN, BUKAN PER TUGAS

Dialectica TIDAK punya "tugas" terpisah seperti bounty make.fun. Satu arena hidup (`general`), satu akun Expert, dan earning-nya dihitung **per peristiwa atas satu jawaban (ISO)**:

- Satu tembakan = satu klaim one-shot ATAU satu generasi serve atas satu pertanyaan (ISR).
- Bayaran per tembakan, hanya bila jawabannya verified DAN menempati selnya: **Pioneer +20** (verified pertama) · **Innovator +10** (verified + novelty ≥15%) · **Marathon Winner +10** (verified terakhir saat marathon conclude). Verified biasa = **$0**. Falsified = **−1 rangkap tiga** (saldo, LifetimeEarned, Expertise).
- Maka "tugas" di Dialectica = **setiap jendela hunt dan setiap tembakan di dalamnya**. Cek 5 pilar berlaku per jendela/per tembakan — dengan kadar berbeda per pilar (§3).

## 2. VONIS 5 PILAR

| Pilar | Status | Vonis audit |
|---|---|---|
| 1 — Data Tugas (TERKUNCI) | SETENGAH | Inti nol konflik: peran Expert/ISP arena general, strategi dynamic, hanya 3 sel membayar, cap serve 10 gen/hari-UTC (rem operasi), plafon RAMP 10 klaim/hari, caps server none/unlimited. Bukan LOLOS karena 9 temuan K1–K9 antar dokumen sendiri (caps tertulis 1 vs 20 vs none; operator masih innovation_focus vs live dynamic; prioritas kelas 3 versi; C13 masih "serve OFF" vs pilot jalan; snapshot saldo basi di MASTER/SISTEM-KENDALI). Lipatan satu giliran (P12) menaikkan ke LOLOS. |
| 2 — Data Penilaian (TERKUNCI) | SETENGAH | Kuat di sisi falsified: panel verifier, 4 cek arena (A_CITATION/A_REASONING/A_UNCERTAINTY/A_SCOPE), clean sheet empiris (verified ⟺ ≥2 support + 0 refutasi; 1 refutasi membunuh; sensus 467 ISO 0 penyimpangan), falsified −1×3 terukur 7/7. Bolong di sisi resmi-positif: ambang agregasi resmi null (L-01), ukuran panel tak diketahui (L-02), SLA verdict tak ada (L-05), reputation tak terjelaskan (L-07), metrik Surprise Gauge tak dipublikasikan (L-10), akun sendiri 0 verified seumur rezim (L-08). Gerbang internal: lab menahan 4/4 falsified serve di semua lapis; lapis isi klaim hanya menahan 1/3 falsified (spesies semantik lolos) + CELAH C5. |
| 3 — Booster juara konsisten (TIDAK terkunci) | ADA-SEBAGIAN | Jangkar: Adam Reinhard 67 $TRUED/hari × 21 hari; Añoñi 38/hari × 17 hari; burst Mauldrop 703/hari-aktif, Febriyan #1 eksternal 14 Nov, DodolDuren pengecualian Pioneer. Resep terbukti ≥3 tarikan: Marathon-first (median pangsa 100%), masuk ramai viso ±3 (bukan viso-0), header 79%, ≥1 URL 77–89%, sitasi kuartil terakhir 89,7%, angka terikat 800 kar terakhir 84,2%. Bidik: verdict rate ≥55%, earn berkelanjutan 38–131/hari. Tertahan dari ADA-TERBUKTI: tak ada tarikan kohort penuh sesudah 14 Nov; Innovator tak terukur; peta jam basi dalam 3,5 hari. Konflik (booster kalah semua): lantai K-2 tetap 0,30; volume burst vs STOP TOTAL + cap serve; panjang frame banjir vs template R3; Pioneer 94% era segar tak menggeser R1 Marathon > R2 Pioneer. |
| 4 — Keadaan Akun & Risiko (TERKUNCI, baca live) | LAYAK PILAR SENDIRI | Keadaan terakhir tercatat: saldo −1,8788; LE 0; Expertise 0; RAR 118 = REL −5 + Availability 29 + Reputation 94 (RAR total MENIPU — naik selama 0 verified; yang mengikat REL −5 + suspensionCount 5 menuju tangga permanent ban tak terpublikasi); caps unlimited [used 0]; 22 jawaban serve masih revealed = paparan −22 potensial. Kill-metric: (a) 0/10 tidak tercapai, (b) JEDA AKTIF + STOP TOTAL klaim, (c) RAR total aman tapi REL tepat −5, (d) jalur ask tertutup. Bukti sejarah menentukan: spending limit 8 Nov, caps rem 20→3→1 disangka kuota platform, innovation_focus menolak one-shot, falsified #3 → STOP TOTAL sampai hari ini. Aturan konflik: **keadaan akun menang atas rencana tembak.** |
| 5 — Waktu & Liveness (TERKUNCI prosedural-live) | LAYAK PILAR SENDIRI | Yang dikunci = prosedurnya, bukan nilainya (nilai membusuk dalam menit): otoritas detail ISR + endsAt, baca-ulang live saat keputusan, fail-closed, semua angka berstempel jam. Pioneer = balap latensi (eksternal median 3,75 dtk; masuk viso-0 kini cuma 13%); jendela spending 24 jam bergulir (usage = otoritas, bukan jam dinding); verdict 85 dtk – 20 jam 43 mnt tanpa SLA; marathon jendela ±500 dtk, maxEndsAt bergerak; filter liveness 3-field menggugurkan 9/9–10/10 kandidat per jendela 15 Nov; falsified SENYAP → 4 permukaan pantau wajib. Memegang HAK VETO atas eksekusi. Di dalam pilar ini, peta gelombang jam berstatus booster-grade (mengarahkan staging, tidak memveto). Bukti sejarah: slot fdf32ba4 kalah oleh waktu 8 Nov; serve 14 Nov menjawab 25 pertanyaan mati (−4 falsified susulan). |

**Struktur final Dialectica: 4 pilar terkunci (1, 2, 4, 5) + 1 booster (3).** Booster kalah pada setiap konflik dengan keempatnya.

## 3. PROTOKOL CEK 5 PILAR PER JENDELA / PER TEMBAKAN (aturan berdiri user 2026-11-17)

- **Pilar 1 & 2 (stabil):** cek penuh saat dokumen/lab berubah (revisi mingguan); per jendela cukup konfirmasi tak ada perubahan + gerbang tembak turunannya jalan (lantai K-1/K-2, self-VFP, liveness, trace/E3). Keputusan menggantung: ambang K-2 0,30 vs rekomendasi lab 0,15 (menunggu keputusan final sesi utama/user — sampai saat itu 0,30 yang mengikat).
- **Pilar 4 (berubah tanpa aksi kita):** WAJIB baca live di awal tiap jendela — /api/node/scores (saldo/LE/Expertise), RAR PER KOMPONEN (bukan total), suspensionCount, caps + usage silang-cek, strategyType, status kill-metric berangka, cacah revealed terbuka. Keadaan akun yang melarang = tidak ada tembakan, titik.
- **Pilar 5 (membusuk dalam menit):** WAJIB baca live per target pada detik keputusan — liveness 3-field atas detail ISR (bukan listing), endsAt, jendela spending dari usage, verdict jendela sebelumnya di 4 permukaan (status ISO, scores, jobs, usage) dengan stempel jam baca.
- **Pilar 3 (arah):** angka bidik dipakai per tembakan (Marathon-first, viso ±3, struktur sitasi); resepnya sendiri disegarkan per tarikan kohort berkala — tarikan penuh terakhir 14 Nov = SUDAH BASI, penyegaran adalah utang pertama kursi Pengamat Juara.

## 4. PETA ROLE DIALECTICA (di dalam arena 5 pilar)

| Kursi | Melayani pilar | Pemilik sekarang | Bukti terpasang | Bolong |
|---|---|---|---|---|
| Penjaga Keadaan Akun | 4 | Pembuka tiap run hunt (gerbang live) + day-close | Bacaan scores/usage tiap jendela; STOP TOTAL + JEDA dipegang | RAR wajib per komponen (total menipu); paparan 22 revealed belum tertutup |
| Pengintai Lapangan & Waktu | 5 | Scan hunt tiap ±2 jam + learning-watch | Filter liveness 3-field fail-closed (backtest 11/11); 4 permukaan pantau | Peta gelombang basi; verdict watch masih per jendela, bukan penangkap peristiwa |
| Penilai Internal (Judge) | 2 | Drill per jendela + lab mingguan + serve_gate.py | Lab menahan 4/4 falsified serve semua lapis; suite 142/142; E3 teradopsi | **C5: self-VFP semantik jalur serve belum terpasang**; lapis isi klaim hanya 1/3 tangkap |
| Penulis Jawaban (Writer) | 1 (bentuk) | Tangga lane Vyce → OpenRouter → Cloudflare → Z.ai + wrapper sitasi | Wrapper + gerbang kualitas terpasang; template R3 | 0 verified seumur rezim — mutu isi belum pernah lolos panel beneran |
| Eksekutor Klaim One-Shot | 1 + 4 | Hunt (disiplin A8: satu tembakan → verifikasi completed) | Jalur resmi dynamic-only dipahami persis | Kursi TERKUNCI Pilar 4 (STOP TOTAL) — bukan bolong, memang ditahan |
| Pilot Serve | 1 + 5 | systemd serve + serve_gate, hanya di dalam jendela hunt | Pilot tergating jalan 16 Nov, kill-switch falsified pertama | 0 generasi seharian 16 Nov (semua kandidat gugur liveness); spot-check manual 3 jawaban pertama masih menunggu generasi pertama |
| Pengamat Juara (Booster Keeper) | 3 | Tarikan kohort berkala + korpus juara | Resep kohort ≥3 tarikan terdokumentasi | Tarikan penuh terakhir 14 Nov — BASI; Innovator tak terukur |
| Manajer Bahan Bakar / Lane | pendukung 1 | Probe lane per jendela (tangga klaim F12) | Tangga live terverifikasi; DashScope keluar permanen dari tangga klaim (sisa peran drill) | Lane Vyce historis mati berjam-jam; kesiapan = probe, bukan asumsi |
| Penjaga Klausul (Guard) | lintas pilar | Weekly-revision (audit SISTEM-KENDALI) | 65 klausul, audit berkala, DAFTAR PERBAIKAN | Utang lipatan K1–K7 audit ini → masuk DAFTAR PERBAIKAN sebagai P12 |
| Pengambil Keputusan | di atas semua pilar | User + sesi utama | — | Yang menunggu: vonis final K-2; bentuk C5; buka/tahan STOP bila syaratnya terpenuhi |

Kursi make.fun yang TIDAK ada di sini: Judge/Creator gambar, Submitter (perannya menyatu ke Eksekutor Klaim), Claim Executor ala payout (tidak ada payout — $TRUED belum bisa diekspor on-chain).

## 5. UTANG YANG DIBUKA AUDIT INI (urutan)

1. **P12** — lipat konflik dokumen K1–K7 (caps, strategi, prioritas kelas, C13 serve, snapshot saldo) ke operator prompt + SISTEM-KENDALI → Pilar 1 naik LOLOS.
2. **Penyegaran booster** — tarikan kohort penuh baru (terakhir 14 Nov) sebelum angka bidik dipakai lebih jauh.
3. **C5** — keputusan bentuk self-VFP semantik serve (keputusan lab/sesi utama; serve pilot tetap tergating penuh selama C5 terbuka).
4. **K-2** — keputusan final 0,30 vs 0,15 (syarat tinjau §45: menunggu klaim baru; STOP TOTAL membuat syarat itu sendiri tertahan — nyatakan eksplisit di revisi mingguan).

Sumber per pilar: `audit-pilar-sementara/PILAR-1-DATA-TUGAS.md`, `PILAR-2-DATA-PENILAIAN.md`, `PILAR-3-BOOSTER.md`, `PILAR-TAMBAHAN-A-KEADAAN-AKUN-RISIKO.md`, `PILAR-TAMBAHAN-B-WAKTU-LIVENESS.md`.
