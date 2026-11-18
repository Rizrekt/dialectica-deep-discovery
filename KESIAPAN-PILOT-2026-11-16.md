# KESIAPAN JENDELA PILOT 07:00 — Dialectica, 2026-11-16 04:27–04:45 WIB
### Perintah sesi utama 04:27: tuntaskan (1) unit systemd + (2) konfirmasi tertulis status rezim SEBELUM firing pertama. Firing hanya bila keduanya hijau.

## 1. UNIT SYSTEMD — HIJAU (dipasang ulang lebih awal, bukan menunggu 06:30)

- Keadaan saat dicek 04:28: **HILANG lagi** — `Unit dialectica-serve.service could not be found`, file /etc tidak ada (VM diganti; kehilangan ke-7 yang tercatat).
- Tindakan: `cp` dari salinan folder provider → `daemon-reload` → `enable` **TANPA `--now`** (pola pemasangan ulang era hold: unit dipulihkan sebagai cadangan §39 + syarat pre-flight P2, BUKAN dinyalakan — serve yang dinyalakan hunt 07:00 adalah serve Vyce tergating via aturan NYALA badan hunt, unit ini ExecStart-nya lane Cloudflare §39 yang statusnya TERTAHAN cadangan; menyalakannya sekarang = lane salah).
- Verifikasi baca-balik: **LoadState=loaded · UnitFileState=enabled · ActiveState=inactive · SubState=dead · MainPID=0.** Serve saat ini OFF (0 proses `run_serve` di ps) — sesuai keadaan yang seharusnya sebelum jendela.

## 2. STATUS REZIM TERTULIS — HIJAU (konfirmasi, bukan asumsi)

- **Rezim yang berlaku: PILOT SERVE TERGATING** (PAKET-RESTART-SERVE-2026-11-15). Persetujuan user: ketukan opsi "Gas — nyalakan serve tergating, pilot terawasi" **15 Nov 19:20 WIB**. Badan LIVE cron `dialectica-slot-hunt` memuat teks REZIM PILOT di kepala butir 5 (terverifikasi `cron.view` 03:01 + dibaca ulang 04:30 hari ini: blok REZIM PILOT SERVE TERGATING utuh, pre-flight P1–P4 tertulis di dalamnya).
- **Firing 21:00 15 Nov TIDAK PERNAH TERJADI** — koreksi §109/§112 berlaku penuh: nol jejak di 4 permukaan (jobs tetap 34, log serve 0 generasi, 0 proses, token-usage 0 generasi serve). Yang terjadi = unit hilang + (hipotesis sesi kolom) run membaca cuplikan badan lama. **Jendela 07:00 hari ini = percobaan nyala PERTAMA yang sesungguhnya**, dengan kewajiban hunt menyatakan eksplisit rezim yang ia jalankan + checklist CHECKLIST-PILOT-2026-11-16 (pernyataan rezim butir A, bukti nyala 4 permukaan butir C).
- **Pre-flight jangkar terakhir (15 Nov 19:20): P1–P4 HIJAU.** Keadaan yang berubah sejak itu dan sudah ditangani malam ini:
  - P1 kini membaca suite **170/170** (bukan 153) — termasuk sinyal E3 + tes improve 17/17; dijalankan ulang penuh 04:35, nol regresi.
  - P2: unit hilang → **sudah dipasang ulang** (butir 1 di atas).
  - P3 (probe Vyce) + P4 (saldo/RAR): P4 dibaca ulang barusan 04:44 — **saldo −1,8788 $TRUED, RAR 118, Expertise 0 — identik jangkar**, akun sehat. P3 tetap kewajiban hunt di jendela (probe harus segar di jendela itu, bukan diwarisi dari kesiapan ini).
- **Perbaikan pipa dari audit malam ini SUDAH TERLIPAT sebelum tembakan pertama** (MEKANISME §113–§114, IMPROVE-2026-11-16): citation_patch v2 (akar E3 dicabut), fallback reasoning Vyce mati, kontrak format serve universal (sumber tunggal di serve_gate, dua lane sama), cap 10 generasi/hari serve Vyce **di kode**, saringan part thought Gemini, pagar grounding, cek liveness cache-hit. Sisa terpagar tertulis: S1 (klaim Vyce/Gemini tanpa wrapper — klaim STOP TOTAL, tidak relevan ke serve pilot; syarat wrapper-dulu tercatat), C5 (spot-check manual 3 jawaban pertama = butir D checklist), U1/U2 (lab 11:42 hari ini).
- **Yang TIDAK berubah:** klaim one-shot STOP TOTAL (TERKUNCI-MATEMATIS); config Expert tidak disentuh; kill-metric pilot bersenjata (falsified pertama di bawah gerbang = serve OFF di giliran yang sama); cap 10 generasi/hari-UTC; seleksi hanya ISR lolos liveness tiga-field + topik inti, prioritas Pioneer viso-0.

## VONIS KESIAPAN

**HIJAU — firing 07:00 boleh jalan** di bawah rezim pilot tergating, dengan dua kewajiban hunt yang tidak bisa diwarisi dari dokumen ini: (a) probe Vyce segar (P3) + bacaan saldo tepat sebelum nyala (P4) di jendela itu sendiri; (b) pernyataan rezim eksplisit + bukti nyala 4 permukaan sebelum serve disebut "nyala". Satu saja merah di jendela → tahan, jangan paksa, lapor alasannya (sesuai perintah sesi utama).
