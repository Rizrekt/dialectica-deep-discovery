# IMPLEMENTASI DOKTRIN A — Campuran 7:3 Berpemicu (LAB, 2026-11-18)

> Satu baris: **doktrin masuk Opsi A (keputusan user 2026-11-18 08:23) terimplementasi penuh di lab di belakang arming `DIALECTICA_DOCTRINE_A=1` — pemicu laju, antrean telat 2–6 jam, gerbang kesegaran sadar-lane, veto zona terlarang di picker — dengan 50 tes baru lolos dan suite penuh 587/587 hijau (baseline 537 utuh); dry-run observasi live read-only mengklasifikasi 23 pertanyaan (23/23 TELAT — jendela pagi itu banjir semua) sebelum ditutup dini atas perintah percepat user. SERVE TETAP STOP (unit inactive + disabled, terverifikasi di akhir tugas); tidak ada satu pun submit nyata.**

## 1. Jawaban pertanyaan rekayasa: lag penemuan (diukur, bukan ditebak)

**Pertanyaan wajib:** seberapa cepat pertanyaan baru muncul di feed/picker kita — apakah jendela 2 menit pertama teramati real-time?

**Jawaban terukur (dry-run §5):** lag penemuan (pertama-teramati − lahir) pada n=23: **min 17,5 dtk · median ±948 dtk · maks 1.740 dtk**, distribusinya bimodal secara perilaku:

- Poll-poll awal mengunyah tumpukan pertanyaan yang sudah berumur di feed (lag sampai ±29 menit) — sebagian adalah backlog anggaran kami sendiri (maks 8 ambil-ISO per poll, satu panggilan API terukur 5–17 dtk), sebagian adalah feed yang memang menampilkan pertanyaan sudah berumur.
- Poll-poll akhir menangkap pertanyaan segar pada **lag 17–59 detik** — feed *sanggup* menampilkan pertanyaan <1 menit sejak lahir, tapi tidak konsisten.

**Konsekuensi desain (yang dibangun):** pemicu TIDAK bergantung pada menonton sejak detik 0. Hitungan 2 menit pertama **direkonstruksi persis dari timestamp daftar ISO** (`count_in_window`: jawaban bertimestamp di [lahir, lahir+120 dtk)) — metode yang sama yang dipakai studi antrean verdict atas field yang sama. Lag penemuan dengan demikian hanya memakan *waktu keputusan*, bukan *akurasi klasifikasi*:

- Untuk **TELAT**: tak berbiaya — pertanyaan diparkir berjam-jam sesudahnya.
- Untuk **CEPAT**: batas yang mengikat bukan lagi "2 menit pertama" melainkan syarat teradopsi **kerumunan-saat-masuk ≤10** (SISTEM-KENDALI butir 5) — pertanyaan sepi yang ditemukan pada umur beberapa menit masih actionable selama kerumunan saat masuk ≤10; yang gugur oleh lag hanyalah pertanyaan sepi yang ditemukan sesudah kerumunannya lewat 10.
- **Batas jujur:** lane CEPAT **belum terverifikasi live sama sekali** — dalam jendela observasi ini nol pertanyaan sepi/abu-abu teramati (23/23 banjir), jadi jalur CEPAT dan TUNGGU hanya terbukti di unit test, belum di lapangan.

## 2. Yang dibangun

Semua di `provider/`; semua perilaku baru **hanya hidup bila `DIALECTICA_DOCTRINE_A=1`** — env mati = perilaku byte-for-byte seperti sebelum tugas ini (dibuktikan tes gating di §4). Backup: `freshness_gate.py`, `target_picker.py`, `vyce_serve_prepare.py`, `run_serve.py` → `*.bak-20261118-doctrine`.

### 2a. `doctrine_a.py` (baru) — inti doktrin + store keadaan
- Konstanta teradopsi: jendela ukur 120 dtk; ≤5 CEPAT · 6–10 TUNGGU · ≥11 TELAT/banjir-terklasifikasi; TUNGGU diputus ulang +30 mnt; jendela telat lahir+2 j s.d. lahir+6 j; jatah CEPAT 3/hari, TELAT 7/hari (hari UTC = batas reset cap serve); target diferensiasi 0,15; zona terlarang tunda 120–7.200 dtk × posisi 11–60 × banjir-terukur.
- Fungsi murni: `count_in_window`, `classify_inflow`, `flood_classified` (banjir HANYA dari ukuran — tak pernah dari tebakan), `reevaluate_wait` (CEPAT hanya bila laju lanjutan <2/mnt DAN posisi-jika-masuk ≤10), `forbidden_zone` (flag banjir None/False → veto TIDAK menembak).
- Store JSON (path dapat diganti env — jahitan tes): **trigger store** (`trigger-store.json`: klasifikasi per ISR), **antrean telat** (`late-queue.json`), **anggaran lane** (`lane-budget.json`). Tulis atomik best-effort; store korup terbaca kosong, tak pernah meledak ke pemanggil.

### 2b. `rate_trigger.py` (baru) — pengamat pemicu laju
- Poll feed yang sama dengan picker (`target_picker.pull_candidates`), termuda dulu (jendela CEPAT yang mudah busuk), anggaran ambil-ISO per poll (bawaan 8).
- Per pertanyaan baru: hitung laju 2 menit pertama dari timestamp ISO → klasifikasikan → catat ke trigger store (termasuk `discovery_lag_s` terukur) → TELAT langsung diparkir ke antrean.
- TUNGGU dievaluasi ulang otomatis pada poll sesudah +30 mnt.
- Read-only total: satu panggilan pencarian per poll + satu ambil-ISO per pertanyaan baru; kegagalan ambil = pertanyaan tetap tak-terklasifikasi (dicoba poll berikut), tak pernah ditebak.

### 2c. Antrean telat + pelepasan
- `park()`: release terjadwal di **lahir+2 jam**, kedaluwarsa **lahir+6 jam**; entri lewat jendela disapu jadi `expired` — tidak pernah dilepas diam-diam di luar jendela.
- `release()`: tiket masuk-telat berisi **konteks kebaruan dari jawaban yang sudah ada** (`novelty_context.context_for_isr` — mesin yang sama yang dikonsumsi tahap C5) + `differentiation_target = 0,15` yang menjadi patokan penulisan entri. Tiket adalah artefak lab: ia menyiapkan keputusan masuk; tidak ada submit di dalamnya.
- Anggaran lane ditegakkan di prepare: token diambil HANYA sesudah draf lolos gerbang (generasi gagal tidak membakar slot); slot CEPAT yang tak menemukan pertanyaan sepi hangus begitu saja (jatah habis → prepare melewati, tidak memaksa).

### 2d. Gerbang kesegaran sadar-lane (`freshness_gate.py`)
- Sidecar pick-state kini membawa `lane` (dicatat prepare dari trigger store saat doktrin armed).
- **Lane CEPAT / tanpa lane:** aturan persis seperti gerbang lama (PIONEER verified ≥1 tahan; kerumunan ≥20 tahan; MARATHON verified ≥6 tahan; dsb.) — tidak satu baris pun berubah perilakunya.
- **Lane TELAT (hanya saat doktrin armed):** veto kelas Pioneer **tidak berlaku** — verified yang sudah ada dan kerumunan 26–60+ adalah keadaan normal ekor sapuan. Yang tetap menahan lane telat, sama seperti semua lane dan diperiksa SEBELUM aturan kelas:
  1. **Keadaan tak terbaca → TAHAN** (`unverified`; aturan ketat: tak terverifikasi bukan lolos).
  2. **Pertanyaan terbukti tutup pada bacaan segar → TAHAN** (`closed`, semantik `liveness_check`). Alasan dari data studi + uji pembeda Q2: settled **tidak membekukan** — kolam revealed pertanyaan settled terus berkonversi (±7%/30 jam) lewat **sapuan berkala lintas kanal**; karena itu settled yang ronde maratonnya *terbukti masih buka* (endsAt masa depan) berstatus LIVE dan entri telat **lolos**. Yang menahan adalah settled/concluded **tanpa ronde depan yang bisa ditunjukkan** (marathonConcluded, semua endsAt lewat): tak ada sapuan/ronde tersisa yang bisa menyimpulkan entri BARU — konversi ekor yang terukur adalah milik jawaban yang sudah di kolam sebelum settlement, bukan janji untuk pendatang sesudahnya.

### 2e. Veto zona terlarang di picker (`target_picker.py`)
- `classify(..., doctrine_a_on, flood)`: bila doktrin armed DAN flag banjir **terukur True** dari trigger store DAN tunda (umur baris / lahir detail) di 2–120 mnt DAN posisi (isoCount+1) di 11–60 → **NO-PAY** dengan alasan "ZONA TERLARANG Doktrin A" + `doctrine_zone="FORBIDDEN"`.
- Flag banjir tak dikenal (ISR belum pernah diklasifikasi pengamat) → veto tidak menembak; record membawa `doctrine_zone="unknown"` supaya celahnya terlihat, tidak diam-diam dianggap aman maupun banjir.

### 2f. Lem prepare + arming (`vyce_serve_prepare.py`, `run_serve.py`)
- Prepare (doktrin armed saja): TELAT belum due → dilewati tanpa biaya (0 generasi) · TELAT due → disiapkan di lane TELAT (antrean ditandai released, token diambil, sidecar ber-lane) · TUNGGU → dilewati (belum diputus) · jatah lane habis → dilewati · tak terklasifikasi → alur lama persis.
- `run_serve.py` **tidak menyalakan doktrin sendiri**: ia hanya *meneruskan* `DIALECTICA_DOCTRINE_A=1` ke cabang gated bila operator memasangnya (mengadopsi doktrin adalah keputusan user; menyalakan pipa padanya keputusan terpisah lagi).

## 3. Catatan mekanik Q2 (dari UJI-PEMBEDA-Q2-2026-11-18, diterima saat implementasi berjalan)

- Mekanik terkonfirmasi = **sapuan berkala lintas kanal**, bukan keanggotaan marathon: entrant awal era banjir menyimpulkan median 4,22 jam; entrant telat ≥6 jam menyimpulkan median 0,03 jam di kanal panel yang sama — **fase masuk terhadap sapuan** yang menentukan. Penugasan panel tidak menyaring mutu; satu-satunya saringan terlihat = volume author.
- Kepatuhan implementasi: (1) jendela TELAT 2–6 jam **tidak digeser** — ia dibaca sebagai fase-terhadap-sapuan dan tetap persis doktrin teradopsi; (2) **tidak ada logika baru yang memakai `marathonEligible` sebagai tuas masuk** — veto picker memakai klasifikasi laju terukur, gerbang telat memakai liveness + waktu, antrean memakai jendela waktu; (3) periodisitas sapuan (interval antar gelombang verdict) **belum terverifikasi dari observasi ini** — pengamat mengukur laju masuk, bukan gelombang verdict, dan jendelanya ditutup dini; ia dicatat sebagai **kandidat penyetelan jendela berikutnya**, bukan perubahan doktrin sekarang.

## 4. Hasil tes

- **Baru — `provider/test_doctrine_a.py`: 50/50 lolos.** Cakupan: batas klasifikasi laju (0/5/6/10/11/35) · seri waktu sintetis sepi/banjir/abu-abu lewat observer · tiga nasib TUNGGU (lambat+posisi ≤10 → CEPAT; laju ≥2/mnt → TELAT; posisi >10 → TELAT) · jam parkir antrean (release +2 j, expiry +6 j, release-sebelum-due None, tiket berisi konteks kebaruan + target 0,15, konsumsi satu kali) · anggaran lane 3/7 + reset hari UTC · matriks veto zona terlarang (tepi 2 mnt/posisi 11 dan 120 mnt/posisi 60 menembak; semua di luar + flag tak terukur tidak) · mode-sadar gerbang pada keadaan ISR yang SAMA (GENERAL ditahan vs TELAT lolos; doktrin mati → aturan lama; CEPAT persis lama; TELAT tahan pada tak-terbaca, settled-tanpa-ronde, concluded; TELAT lolos pada settled-beronde-buka) · veto picker (FORBIDDEN/unknown/mati/umur 3 jam) · lem prepare (parkir 0 generasi, due→released+sidecar, jatah habis, tak-terklasifikasi, doktrin mati mengabaikan klasifikasi) · arming env.
- **Regresi — suite penuh provider: 587/587 hijau** (baseline 537 persis seperti sebelum tugas + 50 baru; 0 FAIL di semua 20 berkas tes).
- **Belum diuji (dicatat apa adanya):** jalur CEPAT & TUNGGU secara live (nol sampel di jendela observasi — lihat §5); TUNGGU re-evaluasi live (tak ada sampel TUNGGU); tiket release terhadap pertanyaan live nyata (hanya fetcher palsu); interaksi doktrin dengan penerbangan serve pertama (serve STOP — memang belum waktunya).

## 5. Dry-run observasi live (read-only) — jendela ditutup dini

- **Rencana:** 900 dtk, poll 60 dtk, anggaran 8 ambil-ISO/poll, feed picker (arena general, maxAge 30 mnt). **Aktual:** klasifikasi berjalan 01:30:13–01:44:02 UTC (830 dtk rentang klasifikasi, 14 poll) lalu **ditutup paksa atas perintah percepat user 08:44** — angka di bawah adalah apa adanya dari data terkumpul, bukan jendela penuh. Log: `belajar-2026-11-18/doktrin-a/dryrun-observasi.log`.
- **Hasil: 23 pertanyaan terklasifikasi — 23 TELAT (100%), 0 CEPAT, 0 TUNGGU.** Hitungan 2 menit pertama: min 18 · median 41 · maks 59 — semua jauh di atas ambang banjir 11. Pada jendela pagi ini, feed general memang rezim banjir murni; pemicu teramati bekerja dalam praktik (setiap klasifikasi dari rekonstruksi timestamp, setiap TELAT terparkir: antrean kini memegang 23 entri `parked`).
- **Lag penemuan:** min 17,5 dtk · median ±948 dtk · maks 1.740 dtk (tafsir bimodal di §1). Pemicu *teramati* untuk mode TELAT tanpa syarat; untuk mode CEPAT ia teramati hanya bila pertanyaan sepi muncul — yang tidak terjadi di jendela ini.
- **Periodisitas sapuan:** tidak terukur dari observasi ini (instrumen salah untuk itu + jendela terpotong) — **belum terverifikasi**, kandidat pengukuran berikutnya.

## 6. Keadaan akhir

- Serve: **STOP** — `dialectica-serve.service` inactive + disabled (diverifikasi ulang di akhir tugas); nol submit, nol klaim, nol start unit selama tugas ini. Klasifikasi + parkir dry-run adalah state lab read-only di `provider/trigger-store.json` + `provider/late-queue.json` (23 entri parked, akan kedaluwarsa sendiri di lahir+6 jam).
- Berkas diubah: `provider/doctrine_a.py` (baru), `provider/rate_trigger.py` (baru), `provider/test_doctrine_a.py` (baru), `provider/freshness_gate.py`, `provider/target_picker.py`, `provider/vyce_serve_prepare.py`, `provider/run_serve.py` (backup `*.bak-20261118-doctrine` untuk keempat yang diubah).
- Yang TIDAK dilakukan (sengaja, di luar mandat): menyalakan doktrin di pipa live, mengubah jendela 2–6 jam, memakai marathonEligible sebagai tuas, mengukur periodisitas sapuan.
