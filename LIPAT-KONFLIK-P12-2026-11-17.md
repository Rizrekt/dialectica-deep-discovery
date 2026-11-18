# LIPAT KONFLIK P12 — K1–K7 (2026-11-17)

**Paket:** P12 dari AUDIT-5-PILAR-DAN-PETA-ROLE-2026-11-17.md (rincian konflik: audit-pilar-sementara/PILAR-1-DATA-TUGAS.md §4.2). Item 4/5 perintah user 2026-11-17 "gas satu-satu". Fase testing — bedah dokumen murni; nol serve/klaim/kode/config berubah.

**Bacaan live penentu (aturan data live: yang live menang), ditarik 2026-11-17 ±07:20 WIB via klien resmi `skill-audit/pkg/dialectica/scripts/trued.py`:**
- `agent show`: Expert 8522c990…b950, name AGENT.AkTa, state configured, arenas general, **strategyType dynamic**, maxConcurrency 1, contextWindowTokens 160000, **caps maxIsrs24h/maxUsd24h/maxTokens24h = unlimited [used 0]**.
- `status`: **Balance −1,8788 $TRUED | RAR 118 | Expertise 0 (general 0)**.

## Tabel pelipatan

| K | Dokumen diubah | Teks yang menang | Dasar |
|---|---|---|---|
| **K1 — caps 1 vs 20 vs none** | operator prompt b.16 + b.17; MASTER §7.1 (verifikasi ulang ditambahkan); SISTEM F3 sudah benar (tanpa edit) | Caps server = **none/unlimited semua field [used 0]**; rem volume = tangga internal + kill-metric. "Tetap 1" = rem disiplin era pasca-suspensi (dicabut); "20 plafon platform" = salah label (20 = default awal skill) | Live `agent show` 2026-11-17; flip 2026-11-10 19:16 (MASTER §7.1) |
| **K2 — strategi innovation_focus vs dynamic** | operator prompt b.12 (penanda TERTIMPA di tempatnya, pola P8b); SISTEM F9 sudah benar | **dynamic** yang mengikat; teks b.12 = sejarah keputusan user 2026-11-09 | Live `agent show` 2026-11-17 (dynamic); flip-back §24.1 (2026-11-10) |
| **K3 — prioritas kelas 3 versi** | operator prompt b.14 (ditulis ulang); SISTEM F6 (ditulis ulang); PAKET-RESTART §4 (catatan penjelas) | **Kelas 1 Marathon/Innovator > Kelas 2 Pioneer viso-0 > Kelas 3 steering-siap** (badan hunt, kalibrasi §30/R1–R2). Prioritas Pioneer di PAKET-RESTART = profil **parameter** serve (`target_picker --priority`, bawaan marathon) — bukan urutan saingan | Badan hunt butir 3 + SISTEM F6; target_picker terbangun §130 |
| **K4 — "serve OFF" vs pilot** | SISTEM C13 (ditulis ulang dua lapis) | (i) **Pilot tergating DISETUJUI** (anggukan user 2026-11-15 19:20; lab 16 Nov §120 butir 11.4; dinyalakan 5× 16 Nov, 0 generasi). (ii) **Eksekusi live DITAHAN fase testing** (pernyataan user 2026-11-17 03:33; sah = uji komponen/kalibrasi/dry-run/shadow) | MEKANISME §106/§116–§120/§127 + blok fase testing SISTEM-KENDALI |
| **K5 — snapshot saldo/RAR basi** | MASTER §5.3 (penanda), MASTER §6.1 (penanda), SISTEM-KENDALI catatan keadaan 2026-11-15 (penanda bertanggal) | Angka mengikat = **saldo −1,8788; RAR 118 (REL −5/Avail 29/Rep 94); LE 0; Expertise 0; jobs 34**. Snapshot lama (4,1212/RAR 7 era falsified pertama; −0,8788/RAR 109 per 15 Nov) diberi penanda tanggal, tidak dihapus | Live `trued status` 2026-11-17; rekonsiliasi MEKANISME §127 |
| **K6 — kill-metric (i) "tanpa settle"** | operator prompt b.13(a); SISTEM C1(a) | **Settle = verdict mendarat**; klaim settled berverdict (termasuk falsified) tidak dihitung; abandoned terminal bukan tanpa-settle. Hitungan mengikat: **0/10 — TIDAK tercapai**; penanda lama "(sudah berlaku)" gugur | Koreksi lab §106-5; MEKANISME §120/§127 |
| **K7 — cap serve menunjuk Cloudflare mati** | SISTEM C14 (ditulis ulang); MASTER §7.4 (ditulis ulang) | Cap 10 generasi/hari-UTC = **rezim pilot Vyce**, dikunci di kode (counter token-usage.jsonl; PAKET-RESTART §5). Asal angka = §39 Cloudflare (kini cadangan mati). **Pemakaian 2026-11-17: 6/10 oleh generasi dry-run/kalibrasi — bukan serve live, bukan nol** | PAKET-RESTART §5; catatan cap §130–§132 |

## Nilai ulang Pilar 1 (Data Tugas)

**LOLOS** (naik dari SETENGAH). Inti yang sudah terkunci sejak audit kini bebas konflik di pinggirnya: caps, strategi, prioritas kelas, status serve, snapshot saldo, definisi kill-metric (i), dan cakupan cap serve berbunyi sama di operator prompt, SISTEM-KENDALI, MASTER, dan paket pilot. Di luar P12: K8 = batas pengetahuan platform (berlabel tidak-terdokumentasi di MASTER — bukan konflik dokumen); K9 (ambang K-2) sudah ditutup keputusan user 2026-11-17 06:12 (tetap 0,30).

## Yang TIDAK disentuh (historis)

MEKANISME-DAN-LAPANGAN.md (selain entri baru §133), VERDICT-LEDGER, DRILL-LOG, BELAJAR-LOG, berkas audit/lab bertanggal (termasuk GERBANG-SERVE-2026-11-15.md yang baris statusnya adalah laporan keadaan di akhir tugas bertanggal itu), log serve/klaim, folder audit-pilar-sementara + belajar-*.

## Temuan samping di luar K1–K7

1. **P8(a)/(c) di SISTEM-KENDALI kini moot** — keduanya menunjuk badan cron (weekly-revision/AGENTS.md) sementara semua cron Dialectica dihapus user 2026-11-17 03:33. P8(b) tertutup oleh pelipatan K2. Dicatat di blok penutup P12 SISTEM-KENDALI; teks P8 sendiri dibiarkan sebagai catatan audit bertanggal.
2. **GERBANG-SERVE-2026-11-15.md baris 4** masih berbunyi "Status serve: TETAP OFF" — itu laporan keadaan terverifikasi di akhir tugas 15 Nov (historis, benar pada tanggalnya), bukan rumusan rezim; tidak diubah, rezim kini dibaca dari C13.
3. Tidak ditemukan konflik baru antar dokumen hidup di luar K1–K7 pada sapuan grep (caps/strategi/prioritas/serve/saldo/settle/cap) sesi ini.
