# CHECKLIST PILOT SERVE — Dialectica (untuk hunt 07:00 2026-11-16 dan jendela pilot berikutnya)
### Pasangan IMPROVE-2026-11-16.md + PAKET-RESTART-SERVE-2026-11-15.md. Isi checklist ini di jendela pilot; hasilnya ditulis ke catatan jendela MEKANISME.

## A. Pernyataan rezim (WAJIB, baris pertama catatan jendela)
- [ ] Nyatakan eksplisit: "Jendela ini menjalankan REZIM PILOT SERVE TERGATING (pre-flight P1–P5)" — atau bila ternyata badan lama yang jalan, nyatakan itu dan naikkan sebagai insiden dispatch ke sesi utama di giliran yang sama (§112).

## B. Pre-flight (semua hijau sebelum nyala)
- [ ] **P1** Sinyal E3 ada di `serve_gate.py` + suite penuh lulus: **170/170** (termasuk `test_improve_20261116.py` 17/17) + `lib/clean_smoke.py` lulus (doktrin v2).
- [ ] **P2** Unit `dialectica-serve` terpasang (readiness 06:30 memasang ulang bila hilang) — enabled + inactive sebelum nyala.
- [ ] **P3** Probe Vyce GLM lolos di jendela ini (catat latensi).
- [ ] **P4** Saldo + RAR dibaca ulang tepat sebelum nyala (jangkar: −1,8788 / RAR 118; nyatakan angka barunya).
- [ ] **P5 (baru)** `citation_patch.py` = v2 (grep: tidak ada `URL_RE` stripper; ada penanda "v2 (2026-11-16)") + kontrak serve ada di `serve_gate.py` (grep `SERVE_FORMAT_CONTRACT` ≥1) + cap serve Vyce di kode aktif (`vyce_serve_common.serve_generations_today()` terbaca; cacah awal hari dinyatakan).

## C. Bukti nyala — 4 permukaan (serve "nyala" hanya bila keempatnya bergerak)
- [ ] Jobs endpoint: jumlah job bertambah dari 34.
- [ ] Log serve jendela ini memuat baris generasi (bukan hanya start).
- [ ] Proses hidup: `ps aux | grep '[r]un_serve'` memuat proses nyata (cek CPU-time naik).
- [ ] `token-usage.jsonl`: generasi serve tercatat hari-UTC ini; cacah lawan cap **10/hari**.

## D. Spot-check semantik manual — 3 jawaban pertama (jembatan C5)
Untuk tiap jawaban, sebelum serve dibiarkan jalan sendiri:
- [ ] Buka SETIAP URL di jawaban: hidup? domainnya sesuai klaim yang ditempel padanya?
- [ ] Untuk tiap angka terikat sitasi: tunjuk kalimat di sumber yang mendukung nilainya (tulis pasangannya di catatan). Angka tanpa pendukung = temuan — catat ISO-nya.
- [ ] Premis kebaruan penutup: grep jawaban-jawaban yang sudah ada di prompt/ISR — sudut "baru" itu benar belum dibahas?
- [ ] Penutup = sintesis yang menamai kebaruan (bukan daftar referensi, bukan note sumber).
- [ ] Nol jejak: tidak ada pembuka monolog, tidak ada "Answer N" sebagai sumber, tidak ada penutup rencana.
- [ ] Satu jawaban gagal satu butir saja → serve TIDAK dibiarkan unattended di jendela ini; catat + bedah.

## E. Kill-metric bersenjata (tanpa tawar)
- [ ] Falsified pertama di bawah gerbang → serve OFF di giliran yang sama + JEDA (ii) + lapor segera.
- [ ] 2 jawaban tertahan berturut oleh lapis trace/E3 → jeda + bedah sebelum lanjut.
- [ ] Cap tercapai (10 generasi/hari-UTC) → berhenti walau jendela masih jalan.

## F. Tutup jendela
- [ ] Verdict watch 0F atas semua jawaban pilot + 22 revealed lama (verdict bisa mendarat 21–22 jam sesudah submit — "belum ada verdict" bukan "aman").
- [ ] Catatan jendela memuat: rezim (A), pre-flight (B), bukti 4 permukaan (C), hasil spot-check per jawaban (D), cacah generasi vs cap.
