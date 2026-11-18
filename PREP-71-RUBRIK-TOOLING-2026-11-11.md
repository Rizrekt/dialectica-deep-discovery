# PREP §7.1 — RUBRIK v2 + PERBAIKAN TOOLING — 2026-11-11

**Lini:** pekerja rubrik+tooling (persiapan §7.1 butir 2, 3-bagian-alat, 5, 6 EVALUASI-STOP-2026-11-11).
**Batas yang dipatuhi:** PERSIAPAN SAJA — 0 klaim, 0 serve, 0 submit, 0 perubahan cron, 0 perubahan MEMORY.md, 0 perubahan steering (lini pekerja lain). Klaim tetap STOP sampai sesi utama memverifikasi §7.1 lengkap.
**Keputusan yang dilayani:** user memilih LANJUT BERSYARAT 2026-11-11 12:50.

---

## Ringkasan status per butir

| Butir §7.1 | Status di lini ini | Bukti |
|---|---|---|
| (2) Rubrik v2 diadopsi (QUALITY.md, bump bernomor) + E1 DIADOPSI | **SELESAI** | QUALITY.md v2 + entri CHANGELOG v2 beralasan angka |
| (3) Audit draf-terkirim — bagian ALAT | **SELESAI (alat)**; pemakaian hidup menunggu klaim pertama | `provider/audit_sent_draft.py` baru, teruji offline dua arah |
| (5) Tabrakan LENGTH_SUFFIX diperbaiki | **SELESAI** | 4 provider: komentar mekanisme + teks suffix memuat catatan pita eksplisit |
| (6) Provider cetak rincian temuan withhold ke stderr | **SELESAI** | helper `format_withhold_breakdown` + dipakai di semua jalur withhold |
| Utang §52/§53: NOVELTY_MARKERS lewatkan "Baru dalam jawaban ini" | **SELESAI** | pola ditambahkan di `openrouter_wrapper.py`, terverifikasi 4/4 varian |

Butir §7.1 di luar lini ini (tidak disentuh, milik lini/sesi lain): (1) steering bermandat-URL semua target — lini pekerja steering; (4) lane tunggal Cloudflare — sudah SIAP per §52/§53, tidak ada perubahan di sini.

---

## 1. Butir (2) — QUALITY.md: Rubrik v2 (bump bernomor, bukan diam-diam)

File: `~/workspace/research/dialectica/QUALITY.md` — header kini **Versi 2 — 2026-11-11**; entri **CHANGELOG v2** mencatat tiap perubahan + bukti angka pemicunya (aturan penutup lab dipatuhi; lab mingguan 2026-11-16 tetap wajib meninjau v2). Isi persis resep EVALUASI §4.3:

- **(b) dilonggarkan — cakupan di atas lead-in.** Lead-in tebal = anjuran, bukan syarat. Pemicu tercatat: celah (b) ×3 di DRILL-LOG (17:00 + 21:00 10 Nov; 07:00 11 Nov); drill 07:00 kedua jawaban gagal (b) v1, satu verified 4-support.
- **(c) dilonggarkan — plafon jadi anjuran, lantai 4.500 tetap pintu.** Pemicu: celah (c) ×4; kedua jawaban drill 07:00 >12 rb kar, satu VERIFIED (0006fe08, 15.519 kar, support 4/refutasi 0).
- **(d) ditimbang sentralitas angka.** Angka POROS wajib entailment sitasi→angka; angka PERIFERAL boleh berbingkai estimasi eksplisit + hedge di titik klaim. Pemicu: (d) biner ×1 gagal atas jawaban VERIFIED 4-support (0006fe08 — ~$765K Meebits; 10⁴–10⁵ sign/dtk/core, keduanya periferal).
- **(d) sub-cek E1 DIADOPSI** — "sitasi harus mendukung angka spesifiknya (uji buka-dan-baca)" kini bagian (d) v2, dengan pernyataan adopsi eksplisit. Bukti pemicu dicatat: ambang adopsi (≥2) **TERPENUHI ×3 — d9f49e11, 96c384fd, 66f46c3e** (EVALUASI §4.2; §52 mencatat penguatan ×4). Status eksperimen E1 di ANTRIAN EKSPERIMEN diperbarui menjadi **DIADOPSI di v2** (riwayat + cara uji dipertahankan).
- **(e) kebaruan harus BENAR.** Klaim kebaruan dinilai lawan (d) atas dasarnya + ketiadaan nyata di verified yang ada; menamai kebaruan di atas angka salah = GAGAL. Pemicu: celah (e) ×1 — 66f46c3e FALSIFIED dengan (e) v1 LOLOS (6 "kontribusi": vanity 28 vs 32 byte; grinding 1 μs; 21 validator/3 dtk basi).
- **(h) BARU — gerbang cakupan sub-pertanyaan (PINTU MATI)**, dinilai atas **teks TERKIRIM**; gagal (h) pada teks terkirim memblokir klaim berikutnya. Pemicu: klaim #3 (71f472d6) — scope miss total (0 aplikasi AI dinamai), falsified 0/1 ±135 dtk padahal lolos semua lantai + 4A + self-VFP.
- **(i) BARU — standar bukti empiris**: ≥1 fakta/angka dunia terikat sumber yang menyatakannya; definisi konsep saja (Goodhart/Campbell/MAPE/HACCP tanpa data) = GAGAL; gagal (i) pada teks terkirim juga memblokir klaim berikutnya.
- Aturan skor + lembar skor diperbarui ke (a)–(i) dengan dua pintu mati lama (d)/(g) + pintu mati baru (h).

Selarasan mekanis: `openrouter_wrapper.score_rubric` kini menilai v2 — (b) lead-in hanya catatan anjuran (sebelumnya pun tidak menggagalkan, kini eksplisit), (c) hanya lantai 4.500 yang menggagalkan (plafon ditulis sebagai anjuran di catatan skor), label lembar skor menjadi "RUBRIK v2", dan string log drill di `openrouter_provider.py` diperbarui v1→v2. (h)/(i) SENGAJA tidak dinilai di wrapper pra-kirim — keduanya gerbang atas teks terkirim (lihat butir 3).

## 2. Butir (3) bagian alat — audit draf-terkirim: alatnya BELUM ada → DIBANGUN

**Keadaan sebelum:** verdict-watch tidak punya alat untuk menilai teks reveal terkirim lawan (h)/(i) — yang ada hanya skor wrapper atas draf probe (persis cacat proses §50: "draf yang digerbang ≠ draf yang terkirim").

**Dibangun:** `~/workspace/research/dialectica/provider/audit_sent_draft.py` (offline, read-only, tanpa generasi/jaringan/submit).

- Masukan: file teks terkirim (reveal ISO) + `--subquestions <file>` (satu frasa/kata-kunci sub-pertanyaan per baris) + `--expected-sections N` + `--json` opsional.
- Menilai: (a)–(g) mekanis v2 atas teks terkirim itu sendiri ((d) dihitung ulang dari audit angka + lantai §45 atas teks terkirim, TANPA patch); **(h)** per sub-pertanyaan (≥60% kata signifikan hadir DAN muncul di dalam seksi ## bernomor); **(i)** proksi mekanis = ≥1 angka dunia terikat sitasi (definisi K-2 ±150 kar).
- Keluaran: lembar skor v2 (a)–(i) + vonis blokir; **exit 1 bila (h) atau (i) GAGAL** (= blokir klaim berikutnya per §7.1(3)), exit 0 bila tidak, exit 2 kesalahan pakai.
- **Batas jujur alat:** (h) tanpa file sub-pertanyaan = **N-A, cek manual wajib** (tidak pernah dianggap lolos); pencocokan (h) = tumpang-tindih kata harfiah → kata kunci WAJIB ditulis dalam **bahasa jawaban** (terverifikasi: daftar Inggris lawan jawaban Indonesia = 0/3 pada teks yang sebenarnya mencakup penuh; daftar Indonesia = 3/3); (i) adalah **proksi keberadaan bukti**, bukan entailment — entailment sitasi→angka tetap cek manual buka-dan-baca per (d)/E1.
- **Uji offline (2026-11-11):** teks contoh "baik" (aplikasi dinamai + angka dunia terikat sumber) → (h) LOLOS 3/3, (i) LOLOS (3 angka terikat, rasio 0,6), exit 0. Teks contoh pola spesies-C (definisi Goodhart/Campbell/MAPE/HACCP saja, tanpa aplikasi, tanpa angka dunia) → (h) GAGAL 1/3, (i) GAGAL (0 terikat), vonis BLOKIR, exit 1. Tanpa `--subquestions` → exit 0 dengan (h) N-A tercatat.
- **Yang tersisa dari butir (3) (bukan alat):** pemakaian hidupnya — mengambil teks reveal sesudah klaim uji pertama terkirim, menilai, dan menulis hasilnya ke VERDICT-LEDGER + MEKANISME — hanya bisa terjadi sesudah klaim jalan (keputusan + verifikasi sesi utama). Jalur Pioneer/serve §39 (PREPARE_CMD) tidak disentuh di lini ini.

## 3. Butir (5) — Tabrakan LENGTH_SUFFIX (utang §50.7)

- **Diagnosis yang dipertahankan:** suffix 5.500–7.500 kar memang SELARAS untuk target uji (viso 4–5, pita baku) — bagian itu tidak diubah.
- **Perbaikan:** di keempat provider yang mendefinisikan LENGTH_SUFFIX (`openrouter_provider.py`, `cloudflare_provider.py`, `dashscope_provider.py`, `zai_provider.py` — serve Cloudflare memakai milik `cloudflare_provider`, jadi ikut terperbaiki):
  1. **Komentar mekanisme eksplisit** di atas definisi: untuk target marathon pita suffix bersifat ANJURAN; yang mengikat kelolosan kirim = **lantai §45 (4.500 kar) + pintu (d)/(g)**, bukan presisi pita (§7.1 butir 5, opsi pencatatan eksplisit).
  2. **Teks suffix sendiri** kini memuat kalimat "Catatan pita: pita 5.500–7.500 ini pita baku (target viso 4–5); untuk target marathon yang mengikat BUKAN presisi pita ini, melainkan lantai 4.500 karakter + gerbang sitasi/format — jawaban marathon boleh lebih panjang dari pita ini." → tabrakan tidak bisa lagi terjadi diam-diam di sisi generasi.
- **Perilaku kirim: TIDAK berubah** (sendable tetap ditentukan wrapper: status + temuan audit + pintu (g); tidak ada ambang baru). Verifikasi: `"Catatan pita" in LENGTH_SUFFIX` lolos di 4/4 modul.

## 4. Butir (6) — Provider mencetak rincian temuan withhold ke stderr (utang §50.5)

- **Helper baru** di `openrouter_wrapper.py`: `withhold_breakdown(report)` → `{wrong, bound_unverified, floor, total}` dan `format_withhold_breakdown(report)` → satu baris stderr: `withhold breakdown: wrong=<n> bound-unverified=<n> floor=<n> (total <n> temuan)`.
- **Dipakai di semua jalur withhold:** `openrouter_provider.py` (main), `cloudflare_provider.py` (main), `dashscope_provider.py` (main), `zai_provider.py` (main), `cloudflare_serve_provider.py` (fallback), dan `cloudflare_serve_prepare.py` (baris hasil prepare — kanal lapornya memang baris hasil, bukan stderr). Diagnosis probe berikutnya kini cukup membaca stderr provider — tidak perlu lagi generasi mentah + `wrap-file` offline.
- Verifikasi: draf 0-URL lewat `wrap_answer` → `wrong=0 bound-unverified=0 floor=3 (total 3 temuan)` — cocok dengan diagnosis manual §50.5 (3 temuan lantai, 0 audit angka).

## 5. Utang §52/§53 — NOVELTY_MARKERS

- `openrouter_wrapper.NOVELTY_MARKERS` ditambah pola: `baru dalam jawaban ini | baru di jawaban ini | baru pada jawaban ini | baru dalam respons ini` (IGNORECASE menaungi varian kapitalisasi: "Baru…", "BARU…"). 
- Verifikasi: 4/4 varian marker lolos regex; `score_rubric` atas draf berpenutup "Baru dalam jawaban ini: …" kini (e) **LOLOS** (sebelumnya GAGAL = false-negative 2/2 drill bayangan §52/§53).

## 6. Hasil test suite provider (sebelum vs sesudah)

Perintah: `python3 test_*.py` di `provider/` (offline semua).

| Test | Sebelum | Sesudah |
|---|---|---|
| test_openrouter_wrapper.py | 30 PASS, 0 FAIL (exit 0) | 30 PASS, 0 FAIL (exit 0) |
| test_cloudflare_claim_path.py | ALL PASS (8/8) | ALL PASS (8/8) |
| test_cloudflare_serve.py | ALL PASS (25/25) | ALL PASS (25/25) |
| test_dashscope_claim_path.py | ALL PASS (11/11) | ALL PASS (11/11) |
| test_openrouter_claim_path.py | ALL PASS (10/10) | ALL PASS (10/10) |
| test_zai_claim_path.py | ALL PASS (13/13) | ALL PASS (13/13) |

Tidak ada test yang gagal karena perubahan ini; tidak ada test yang diubah. `py_compile` bersih untuk 8 file yang disentuh. Cek perilaku baru tambahan (di luar suite): NOVELTY_MARKERS 4/4 varian; (c) v2 — 13.000 kar LOLOS dengan catatan anjuran, 4.000 kar GAGAL; breakdown sesuai §50.5; suffix 4/4 modul.

## 7. Daftar file yang berubah

- `QUALITY.md` — rubrik v2 penuh + CHANGELOG v2 + status E1 DIADOPSI.
- `provider/openrouter_wrapper.py` — NOVELTY_MARKERS; `score_rubric` v2 ((b)/(c) + label); `RUBRIC_LABELS` (a)–(i); header lembar "RUBRIK v2"; helper `withhold_breakdown`/`format_withhold_breakdown`.
- `provider/audit_sent_draft.py` — **BARU** (alat audit draf-terkirim §7.1(3)).
- `provider/openrouter_provider.py`, `provider/cloudflare_provider.py`, `provider/dashscope_provider.py`, `provider/zai_provider.py` — LENGTH_SUFFIX (komentar + catatan pita) + cetak breakdown withhold; openrouter: string log drill v2.
- `provider/cloudflare_serve_provider.py`, `provider/cloudflare_serve_prepare.py` — cetak breakdown pada jalur withhold serve.

**Tidak disentuh:** steering mana pun, cron mana pun, MEMORY.md, MEKANISME-DAN-LAPANGAN.md, VERDICT-LEDGER.md, run_serve.py, logika sendable di semua provider.

## 8. Sisa kekurangan (jujur)

1. **(h)/(i) belum pernah dinilai atas teks terkirim SUNGGUHAN** — alatnya teruji pada teks contoh offline; penilaian hidup pertama menunggu klaim uji (di luar mandat lini ini). Sampai itu, butir (3) berstatus "alat siap", bukan "terbukti hidup".
2. **(i) mekanis = proksi keberadaan**, bukan kekuatan bukti: angka terikat yang sitasinya tidak menyatakan angka itu lolos proksi (i) dan hanya tertangkap (d)/E1 manual. Ini batas yang dinyatakan di QUALITY.md (i) sendiri.
3. **(d) sentralitas angka tidak dimekanisasi** — klasifikasi poros vs periferal adalah penilaian pembaca (buka-dan-baca); wrapper mekanis tetap fail-closed atas semua temuan audit angka (konservatisme §35 yang disengaja, tidak diubah di sini).
4. **(c) mekanis kini lantai-saja** — konsekuensi yang disengaja dari v2: skor (c) wrapper tidak lagi menandai draf 9–12 rb kar pada target baku sebagai GAGAL; catatan "di atas plafon anjuran" tetap tercetak di note skor.
5. Butir §7.1 (1) steering bermandat-URL = lini pekerja lain; vonis kesiapan §7.1 KESELURUHAN tetap milik sesi utama.
