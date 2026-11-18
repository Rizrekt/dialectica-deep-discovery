# PAKET RESTART SERVE — Dialectica (dirakit lab 15 Nov 2026 malam; lab dimajukan dari Senin 16 Nov atas perintah user 19:10 WIB)

**STATUS: SIAP TEMBAK, BELUM DINYALAKAN.** Serve tetap MATI sampai user mengangguk atas vonis lab. Paket ini tidak menyentuh klaim — klaim tetap STOP TOTAL.

## 1. Basis vonis (backtest LAB-BACKTEST-2026-11-15.md, n efektif 29/29)

- Falsified serve **4/4 TERTAHAN** sebelum terkirim — setiap lapis menahan keempatnya secara mandiri (liveness 4/4 MATI pola flag basi; trace 4/4; lantai wrapper 4/4). Saldo −4 itu tidak akan terjadi di bawah gerbang ini.
- Revealed serve **22/22 ikut tertahan**, tetapi **0/22 tertahan HANYA oleh liveness** — semua gugur juga di gerbang isi (seluruh jawaban serve pagi itu 0 URL, marathonEligible=False semua, upside $0).
- Korpus serve historis **0/26 lolos gerbang isi** → laju false-block atas draf serve yang BAIK **tidak terukur** dari backtest ini (sel kosong). Risiko ini dinyatakan terbuka: pilotlah yang mengisinya.
- Pembanding klaim (jalur lain, catatan saja): gerbang isi menahan **1/3** — 2 klaim falsified LOLOS isi (fcb7b015 5/6, 0d76cc7c 6/6) dan mati di semantik = **risiko sisa #1 dokumen gerbang, terkonfirmasi terukur**.
- Dokumen GERBANG-SERVE-2026-11-15.md tidak menetapkan ambang numerik backtest; lawan kriteria kualitatifnya sendiri (§5–§6): spesies f0bb3586 tertahan redundan 3 lapis = TERPENUHI; target mati tersaring 25/26 di prepare = TERPENUHI; butir 6 (korpus trace) = backtest ini sendiri.

## 2. Konfigurasi serve di bawah gerbang

- **Lane: Vyce** (tergating penuh: `vyce_serve_prepare.py` / `vyce_serve_ready.py` / `vyce_serve_provider.py` + modul bersama `provider/serve_gate.py`, fail-closed). Cloudflare §39 = cadangan mati (0 neuron 15 Nov), tidak dipakai paket ini.
- **Urutan lapis per jawaban:** (1) liveness tiga-field di prepare (marathonActive + marathonConcluded + endsAt; fail-closed, fallback hanya blokir bila terbukti mati); (2) generasi via wrapper klaim verbatim — lantai T12 penuh, **K-2 tetap 0,30** (rekomendasi U2 lab → 0,15 BELUM diputuskan; tidak dipakai paket ini); (3) deteksi thinking-trace 4 keluarga sinyal; (4) **sinyal E3 (ADOPSI lab lini B)**: frasa penutup evasif sumber eksplisit di penutup/seksi sumber = TAHAN.
- **Semantik (§5 butir 1 dokumen gerbang):** tahap self-VFP semantik permanen (C5) BELUM terpasang — `semantic_check` disiapkan tapi `performed=False`. Bentuk pilot yang paket ini siapkan: gerbang mekanis + **spot-check semantik manual 3 jawaban pertama** oleh sesi kolom/utama (warisan desain T16). Mengangguk paket ini = menerima risiko sisa semantik secara tertulis untuk masa pilot.

## 3. Pre-flight (WAJIB semua hijau sebelum nyala pertama)

- **P1** — Tambalan sinyal E3 masuk `serve_gate.py` + tes lulus (suite terakhir 142/142; tambalan menaikkan hitungan, regresi nol).
- **P2** — Unit systemd `dialectica-serve` terpasang (VM ganti membunuh unit — terakhir dipasang ulang 19:00 15 Nov: loaded+enabled+inactive; cek ulang di jendela nyala).
- **P3** — Probe Vyce GLM lolos di jendela itu (terakhir 19:00: OK 2,2 dtk).
- **P4** — Saldo + RAR dibaca ulang tepat sebelum nyala (jangkar lab 19:11: **−1,8788 / RAR 118 / Exp 0**).
- **P5 (ditambahkan IMPROVE 2026-11-16, MEKANISME §113)** — Perbaikan pipa terpasang: `citation_patch` **v2** (sitasi tidak lagi dibuang; note evasif v1 tidak ditempel lagi — v1 terbukti akar E3 + URL 0), fallback `reasoning_content` Vyce dimatikan, kontrak format serve universal aktif di `vyce_serve_common`. Suite kini **170/170** (bukan 153; lipatan audit S1–S7 §114 menaikkan hitungan + cap serve kini ditegakkan di kode, bukan hanya disiplin). Checklist jendela pilot: `CHECKLIST-PILOT-2026-11-16.md`.

## 4. Jendela pertama + pengawasan (§5 butir 5 dokumen gerbang)

- Jendela hunt pertama sesudah anggukan, **satu jendela poll saja, terawasi penuh**: log prepare/provider dibaca baris demi baris; **3 jawaban pertama diperiksa manual** (isi + semantik) sebelum serve dibiarkan jalan sendiri; sesudah itu pun serve hanya jalan di dalam jendela hunt, bukan 24 jam.
- **Seleksi target:** hanya ISR lolos liveness tiga-field + topik inti; prioritas Pioneer viso-0 (satu-satunya jalur +20 — sub-cek lab: balik ke saldo ≥0 butuh ≥1 Pioneer atau ≥2 slot +10, nol falsified di antaranya). Marathon-live non-inti = lewati. **[Catatan P12 2026-11-17: prioritas Pioneer di paket ini = profil PARAMETER jalur serve (`target_picker --priority pioneer`), BUKAN urutan kelas global. Urutan kelas yang mengikat lintas jalur: Kelas 1 Marathon/Innovator > Kelas 2 Pioneer > Kelas 3 steering-siap (badan hunt; SISTEM-KENDALI F6).]**

## 5. Kill-metric bersenjata + cap

- **Falsified pertama di bawah gerbang → serve OFF di giliran yang sama**, JEDA (ii) berlaku lagi, lapor segera. Tidak ada "coba sekali lagi".
- **2 jawaban tertahan berturut** oleh lapis trace/E3 → jeda + bedah sebelum lanjut (sinyal generasi memburuk).
- **Cap bakar: maks 10 generasi serve/hari-UTC** selama pilot (meniru cap §39; counter persisten `token-usage.jsonl` — restart tidak mereset). Berhenti di cap walau jendela masih jalan.
- Verdict watch 0F tetap jalan tiap hunt atas semua jawaban pilot + 22 revealed lama.

## 6. Yang TIDAK berubah oleh paket ini

- Klaim one-shot: STOP TOTAL (fase TERKUNCI-MATEMATIS — syarat naik fase A5 gugur permanen; pencabutan hanya lewat jalur tertulis dokumen operatif sesudah bedah, bukan wewenang paket ini).
- U1 jendela malam: TUNDA (komponen serve-nya moot sampai paket ini dinyalakan + data malam non-banjir ada).
- U2 ambang K-2: rekomendasi lab 0,15 menunggu keputusan user/sesi utama; paket berjalan di 0,30.
- Config Expert, strategi dynamic, arenas general: tidak disentuh.

*File terkait: LAB-BACKTEST-2026-11-15.md · LAB-E3-SENSUS-E-2026-11-15.md · LAB-FASE-U1U2-KENDALI-2026-11-15.md · GERBANG-SERVE-2026-11-15.md · MEKANISME §106.*
