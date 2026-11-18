# REVISI BADAN CRON DIALECTICA — 2026-11-14 (±18:50 WIB)

Perintah user: jadwal yang ada direvisi supaya mencerminkan data segar 14 Nov — jangan monoton terhadap data lama. Metode: cron.view → cron.update (badan lengkap, semua instruksi lama dipertahankan) → cron.view baca-balik terverifikasi + cron.status. **Jadwal/waktu/delivery TIDAK berubah di keempat job.** Wilayah terkunci TIDAK disentuh: STOP TOTAL klaim one-shot, serve DITAHAN MATI (restart hanya perintah sesi utama tertulis/keputusan lab), gerbang A8/4A/lantai T12/kill-metric/tangga volume, cap serve 10, config Expert, mode serve, expert id.

## 1. dialectica-slot-hunt (interval 2 jam; next tetap 19:00 WIB)
- **(a) Butir 0F baru — PANTAU VERDICT SERVE**: tiap jendela kerja cek verdict 25 jawaban serve pagi 14 Nov (VERDICT-LEDGER.md); verdict baru wajib masuk ledger + lapor menonjol; juga ditambah ke isi catatan butir 7 + daftar pemicu lapor segera.
- **(b) FILTER LIVENESS TIGA-FIELD** di Kelas 1: marathonActive=True + marathonConcluded=True + endsAt lewat = INELIGIBLE tegas (KULIT-SISTEM edge #2).
- **(c) Frontier drill 3A(a)**: sensus sub-pola E1 (termasuk E1-c + E1-p), anomali pintu (e), status E3 = bahan drill berjalan.
- **(d) TANGKAPAN GELOMBANG 22:00** di paragraf JENDELA: run 21:00 menambah scan + staging baca-saja rilis 21:00–22:59 (jumlah + komposisi topik) sebagai bahan U1 — tetap nol klaim/serve tambahan (rezim tidak berubah).
- **(e) Garis kohort utama diganti**: STUDI-KOHORT-2026-11-14 + KORPUS-JUARA-2026-11-14 (+ KULIT-SISTEM) masuk daftar WAJIB BACA + butir 3; §30 turun jadi arsip pembanding.

## 2. dialectica-learning-watch (interval 8 jam; next tetap Minggu 02:37 WIB)
- **(a) Butir 2B baru — REFRESH KORPUS**: hitung ulang lolos lantai @0,30 vs @0,15 tiap run lawan acuan korpus (@0,30: 32,5%/28,1%; @0,15: 57,6%/32,8%); selisih ≥5pp = bahan U2; ambang tidak diubah.
- **(b) DISKRIMINATOR sebagai deret waktu** (butir 2B(b)): lanjutkan deret dari run ke-3 (rasio d 0,135 — penyempitan ke-4; kepadatan d 0,159).
- **(c) Rotasi pendaki segar** (butir 2): naik ≥300 poin/jendela masuk kohort amati — garis awal Danis/Rodeo/Mauldrop; chirpy tetap dipantau.
- **(d) Butir 6 baru — TABEL 7 HARI jam × topik-inti** dari tangkapan hunt (bahan edge triase gelombang).

## 3. dialectica-day-close (harian 23:00; next tetap 23:00 WIB)
- **(a) Butir 3c baru — EKSPOSUR VERDICT SERVE**: rekap harian berapa dari 25 sudah ber-verdict (yang berubah hari itu + Δsaldo/RAR) dan sisa revealed.
- **(b)+(c) Butir 4b baru — ANTREAN LAB + GELOMBANG 22:00**: cek kelengkapan daftar usulan lab (item baru hari itu wajib masuk) + rekap rilis 21:00–22:59 + komposisi topik dari catatan jendela 21:00. VERDICT-LEDGER + file lab masuk daftar WAJIB BACA.

## 4. dialectica-weekly-revision (Senin 11:42; next tetap 16 Nov 11:42 WIB)
- **Butir 11 baru — PAKET KEPUTUSAN LAB** (10 item, tiap item diputuskan/ditunda beralasan + file bahannya): (1) U1 jendela malam (LAB-PREP-U1U2), (2) U2 ambang K-2 (LAB-PREP + KORPUS-JUARA angka final; jalur ganda putuskan/tunda §45), (3) E3 adopsi (QUALITY.md), (4) GERBANG SERVE (syarat hidup lagi: gerbang kualitas jalur serve + filter liveness; serve tetap ditahan mati s/d lab memutuskan), (5) filter liveness tiga-field (lab menilai hasil pemakaian), (6) sub-cek aritmetika, (7) taksonomi E1-p/E1-c, (8) anomali (e), (9) unit systemd serve Vyce (parkir), (10) 3 EDGE-SAH KULIT-SISTEM.
- Klausul anti-stagnasi (butir 10e) + panel pertanyaan mingguan (butir 1) dipertahankan utuh.

## Verifikasi (cron.view baca-balik + cron.status, ±18:50 WIB)
- slot-hunt: marker "0F. PANTAU VERDICT SERVE", "FILTER LIVENESS TIGA-FIELD", "TANGKAPAN GELOMBANG 22:00", "FRONTIER DRILL BERJALAN", "GARIS KOHORT UTAMA sejak revisi 2026-11-14" terbaca di badan tersimpan. Status: enabled, 0 failure, next **19:00 WIB 14 Nov**.
- learning-watch: marker "2B. REFRESH KORPUS + DERET DISKRIMINATOR", "ROTASI PENDAKI SEGAR", "6. TABEL 7 HARI JAM × TOPIK-INTI" terbaca. Status: enabled, 0 failure, next **02:37 WIB 15 Nov**.
- day-close: marker "3c. EKSPOSUR VERDICT SERVE", "4b. ANTREAN LAB + GELOMBANG 22:00" terbaca. Status: enabled, 0 failure, next **23:00 WIB 14 Nov**.
- weekly-revision: marker "11. PAKET KEPUTUSAN LAB" dengan 10 item terbaca; butir 10(e) anti-stagnasi + butir 1 panel utuh. Status: enabled, 0 failure, next **Senin 16 Nov 11:42 WIB**.

## Catatan wilayah terkunci (tidak diubah, sesuai aturan ragu = jangan sentuh)
- Badan slot-hunt butir 5 masih memuat aturan NYALA/NYALA PENGGANTI/PENSIUN serve versi lama (termasuk jalur pasang-ulang unit dengan `enable --now`). Kalimat-kalimat itu TIDAK diubah di revisi ini karena menyentuh mode serve (wilayah terkunci); keadaan serve DITAHAN MATI saat ini ditegakkan oleh keputusan sesi utama 09:14 + butir 11(4) badan weekly-revision. Bila sesi utama ingin badan hunt menyebut status tahan-mati secara eksplisit, itu perubahan terpisah atas perintah tertulis sesi utama.
- Angka "caps maxIsrs24h=20 (plafon platform)" di KEADAAN REZIM badan weekly-revision vs "caps none" di badan slot-hunt: inkonsistensi lama, TIDAK diubah (menyentuh config Expert — wilayah terkunci); dicatat di sini untuk keputusan sesi utama/lab.
