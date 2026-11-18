# LAB BACKTEST GERBANG SERVE — Dialectica (lini A)

**Tanggal:** 2026-11-15 malam WIB (lab dimajukan dari Senin 2026-11-16 atas perintah user 19:10 WIB).
**Cakupan:** replay `provider/serve_gate.py` (dibangun 2026-11-15, dokumen `GERBANG-SERVE-2026-11-15.md`) atas seluruh korpus jawaban kita yang verdict-nya diketahui/belum: **29 ISO = 26 serve (22 revealed + 4 falsified) + 3 klaim one-shot falsified (pembanding)**.
**Keadaan akun saat lab (terverifikasi live sesi kolom malam ini):** Expert `8522c990-d4f6-4155-a326-3c3c9802b950`, akun rizrekt, strategyType=dynamic, arenas=general; **saldo −1,8788 $TRUED, RAR 118, Expertise 0**. Backtest ini READ-ONLY: tidak ada klaim/serve/answer dijalankan, tidak ada config/systemd/cron disentuh, serve tetap OFF.

---

## 1. Metode & sumber (semua angka bisa ditelusur)

- **Teks terkirim:** `jobs-0900.json` (run-2026-11-14-0900, field `output.structuredData.answer` per job) — divalidasi silang lawan teks reveal API di sweep `isos-<isr>.json` (run-2026-11-15-0500): **panjang identik 29/29**, dan panjang keempat falsified serve cocok persis dengan VERDICT-LEDGER (38.591 / 36.679 / 37.098 / 43.623 kar; job 6ff4d06e / 0a835ed7 / 5f5cd4d8 / cd115d7e — sama dengan catatan ledger). File teks tersimpan `answer-f0bb3586.txt`, `sent-5b5e8212.txt`, `sent-a3b8b34a.txt` konsisten.
- **Verdict asli:** `verdicts-0500.json` (sweep 05:00 15 Nov) + koreksi ledger baris #7/#8: `5b5e8212` dan `a3b8b34a` masih "revealed" di sweep 05:00 tetapi verdict falsified mendarat 06:03 dan 06:43 WIB → status final falsified. Sweep 19:00 15 Nov mengonfirmasi keadaan akhir: **22 revealed + 7 falsified**.
- **Lapis isi:** `serve_gate.gate_answer(teks)` persis seperti produksi (wrapper klaim verbatim + deteksi thinking-trace + lantai §45/T12: K-1(a) URL ≥1; K-1(b) kepadatan sitasi ≥0,5/1.000 kar; **K-2 rasio angka terikat ≥0,30**), `regen_fn=None` (lihat peringatan §6 — tidak ada satu pun teks korpus di bawah lantai panjang 4.500 kar, jadi ketiadaan regenerasi tidak mengubah satu baris pun).
- **Lapis liveness:** `serve_gate.liveness_check(detail, now=waktu submit)` atas detail ISR tersimpan paling awal per ISR (folder run-2026-11-14-0700/0900/1300 di hidden_files goal; diambil 1–5 jam sesudah submit). Agar setia ke keadaan saat submit, daftar `marathonEligibleIsos` disaring ke ronde dengan `startedAt ≤ waktu submit` (waktu submit = stempel ISO; untuk falsified cocok dengan ledger sampai detik). Field `marathonActive/marathonConcluded` adalah keadaan saat fetch — caveat §6.
- **`marathonEligible` per ISO** di tabel = flag ISO pada sweep 05:00 15 Nov: **False untuk 29/29** (termasuk 4 falsified serve, sesuai ledger).

---

## 2. Angka wajib

### (a) Falsified serve — 4/4 TERTAHAN sebelum terkirim, oleh SETIAP lapis secara mandiri

| Lapis | Tertangkap | Rincian |
|---|---|---|
| **Liveness** (prepare, sebelum generasi) | **4/4 MATI** | Keempatnya pola flag basi verbatim: `marathonActive=True, marathonConcluded=True`, semua `endsAt` ronde sudah lewat jauh sebelum submit (maks endsAt: f0bb3586 → 13 Nov 22:02Z vs submit 14 Nov 01:07Z; 7d81c51d → 14 Nov 00:37Z vs submit 14 Nov 01:05Z; 5b5e8212 → 13 Nov 03:05Z vs submit 01:31Z; a3b8b34a → 13 Nov 09:41Z vs submit 01:42Z). Serve tidak akan pernah mengambil pertanyaan-pertanyaan ini. |
| **Thinking-trace** | **4/4 terdeteksi** | f0bb3586 + 5b5e8212: pembuka jejak penalaran ("Let me…"); 7d81c51d + a3b8b34a: monolog ketidakpastian orang-pertama (≥2 penanda). |
| **Lantai wrapper (K-1/K-2 @0,30)** | **4/4 GAGAL** | K-1(a) URL: 4/4 gagal (0 URL semua). K-1(b) densitas: 3/4 gagal (f0bb3586 lolos 1,32 — sitasi semu gaya "(Answer N)" ikut terhitung wrapper). K-2 rasio: 3/4 gagal (f0bb3586 lolos tipis 0,31). |
| **Gerbang isi gabungan** (`sendable=False`) | **4/4** | Skor rubrik wrapper (a–g) falsified: 2–3 LOLOS dari 6 yang dinilai (f selalu N-A), (d) GAGAL 4/4, (g) LOLOS 4/4. |
| **Gabungan semua lapis** | **4/4 TAHAN** | **Saldo −4 tidak akan terjadi di bawah gerbang ini** — bahkan satu lapis saja (mana pun) cukup untuk menahan keempatnya pada korpus ini. |

### (b) Revealed serve — 22/22 ikut TERTAHAN (false-block mentah), tetapi 0 yang tertahan HANYA oleh liveness

| Lapis | Terblokir | Catatan |
|---|---|---|
| Liveness | 21/22 MATI | Satu-satunya LIVE: `2549fe17` (ISR 0dbd4532 — pertanyaan `in_progress` tanpa dimensi maraton pada detail 09:00). |
| Thinking-trace | 21/22 | Satu-satunya bersih: `49740377`. |
| Lantai wrapper | **22/22 GAGAL** | K-1(a) URL 22/22 gagal — **seluruh jawaban serve pagi itu 0 URL**; mayoritas juga gagal K-1(b)+K-2 sekaligus (aktual tipikal: densitas 0,0–0,06; rasio 0,00–0,02). |
| **Hanya liveness (isi LOLOS)** | **0/22** | Tidak ada satu pun jawaban revealed yang lolos gerbang isi tetapi mati di liveness. |
| Lolos semua lapis | 0/22 | — |

**Pembacaan yang jujur atas (b):** angka 22/22 BUKAN bukti gerbang terlalu kasar terhadap jawaban bagus. Ke-22 jawaban ini (i) belum berverdict — "revealed" bukan "verified", statusnya tidak diketahui; (ii) semuanya keluaran mentah jalur serve tanpa gerbang sama sekali (spesies yang sama dengan yang falsified: 21/22 terdeteksi trace, 22/22 tanpa URL); (iii) semuanya `marathonEligible=False` — upside $0 bahkan bila verified, kecuali award Pioneer/Innovator/Marathon yang mensyaratkan eligible. Korpus serve **tidak memuat satu pun draf bersih** (0/26 lolos gerbang isi), jadi laju false-block gerbang atas draf serve yang BAIK tidak bisa diukur dari backtest ini (sel kosong — lihat §6). Bukti bahwa gerbang meloloskan teks bersih datang dari jalur klaim: fixture klaim teruji di suite gerbang (37/37) + 2 dari 3 teks klaim nyata di bawah.

### (c) Pembanding klaim one-shot falsified (jalur klaim TIDAK memakai gerbang serve — catatan saja)

| ISO | Vonis gerbang isi bila diterapkan | Rincian |
|---|---|---|
| fcb7b015 (klaim #1) | **LOLOS KIRIM** (sendable) | Skor 5/6 dinilai. Konsisten dengan sejarahnya: lolos semua ambang mekanis, mati di dukungan semantik (A_CITATION) — risiko sisa #1 dokumen gerbang, terkonfirmasi ulang malam ini. |
| 0d76cc7c (klaim #3) | **LOLOS KIRIM** (sendable) | Skor 6/6 dinilai — teks terbersih korpus; tetap falsified di platform (1 refutasi, panel 2). Lantai perlu, bukan cukup — persis catatan ledger. |
| 097df475 (klaim #2) | TAHAN (lantai url+density+ratio) | Teks terkirim versi sweep: 0 URL terhitung, densitas 0,456, rasio 0,174. Nuansa: yang "lolos probe sendable 3×" di ledger adalah draf steering saat itu di bawah wrapper pra-lantai-§45; teks final terkirim di bawah wrapper+lante §45 hari ini gugur di ketiga sub-lantai. |

**Skor gerbang isi atas klaim: menahan 1/3.** Dua yang lolos adalah bukti terukur bahwa gerbang mekanis saja tidak menghentikan spesies falsified semantik — inilah tepatnya keputusan lab §5 butir 1 di dokumen gerbang.

---

## 3. Tabel per jawaban (29 baris)

Kolom: verdict asli (support/refutasi/verifier dari sweep 05:00; panel bisa tumbuh sesudahnya — f0bb3586 kini 0/2/2) · URL = hitungan wrapper atas teks final · Liveness = replay saat submit · Trace = deteksi lapis 2 · Lantai = sub-gagal + aktual (url; densitas/1.000 kar; rasio terikat) · Skor = rubrik wrapper a–g (f = N-A untuk semua, tidak ada tuntutan JSON pada job serve/klaim ini).

| ISO | ISR | Jenis | Verdict asli (s/r/v) | Panjang | URL | Liveness | Trace | Lantai §45 | Skor a–g | Vonis gerbang |
|---|---|---|---|---|---|---|---|---|---|---|
| 8671364d | 026fa1a2 | serve | revealed (0/0/0) | 42,178 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.024, rasio=0.01) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 0c4d45b8 | 087ce951 | serve | revealed (0/0/4) | 41,927 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.024, rasio=0.021) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 2549fe17 | 0dbd4532 | serve | revealed (0/0/3) | 31,139 | 0 | LIVE | YA | GAGAL url,density,ratio (url=0, dens=0.064, rasio=0.003) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| f0bb3586 | 1287c2ae | serve | falsified (0/2/2) | 38,591 | 0 | MATI | YA | GAGAL url (url=0, dens=1.32, rasio=0.31) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 49740377 | 1f58031d | serve | revealed (0/0/6) | 42,003 | 0 | MATI | tidak | GAGAL url,ratio (url=0, dens=0.763, rasio=0.104) | a✓ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| d68a165a | 2133a697 | serve | revealed (0/0/0) | 34,507 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✓ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 1b7476cf | 30608eca | serve | revealed (0/0/3) | 45,257 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 7d81c51d | 30fe9eea | serve | falsified (0/4/5) | 36,679 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| a94e95bf | 3883f4d9 | serve | revealed (0/0/3) | 35,426 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.057, rasio=0.001) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| a3b8b34a | 3884b6c3 | serve | falsified (0/0/0) | 43,623 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✓ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 097df475 | 472b29a0 | klaim | falsified (0/4/4) | 6,580 | 0 | — | tidak | GAGAL url,density,ratio (url=0, dens=0.456, rasio=0.174) | a✓ b✗ c✓ e✓ f– g✓ d✗ | **TAHAN** |
| 5c9cdb9e | 530e95ec | serve | revealed (0/0/0) | 42,855 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.07, rasio=0.025) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| fcb7b015 | 60fa9935 | klaim | falsified (2/2/4) | 5,286 | 4 | — | tidak | LOLOS | a✓ b✗ c✓ e✓ f– g✓ d✓ | **LOLOS KIRIM** |
| 0d76cc7c | 71f472d6 | klaim | falsified (0/2/2) | 5,147 | 7 | — | tidak | LOLOS | a✓ b✓ c✓ e✓ f– g✓ d✓ | **LOLOS KIRIM** |
| f8e22374 | 7401386a | serve | revealed (0/0/4) | 41,037 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.219, rasio=0.092) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| a1fe6c64 | 77f1e68b | serve | revealed (0/0/0) | 41,712 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.168, rasio=0.102) | a✓ b✓ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 5e8c32a5 | 79f751ce | serve | revealed (0/0/0) | 41,947 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.119, rasio=0.042) | a✓ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 9ebb44a0 | 8f4b9221 | serve | revealed (0/0/3) | 34,975 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✓ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 1869839d | 970d09db | serve | revealed (0/0/0) | 34,685 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| f5224761 | a1770c04 | serve | revealed (0/0/0) | 39,917 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.1, rasio=0.002) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 5b5e8212 | a361a16b | serve | falsified (0/0/0) | 37,098 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.027, rasio=0.001) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 1a502a51 | a5f24a48 | serve | revealed (0/0/4) | 41,087 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.146, rasio=0.055) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| a5ed3b79 | c1ef7bd8 | serve | revealed (0/0/0) | 42,485 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.071, rasio=0.096) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 26d732da | c5927d00 | serve | revealed (0/0/6) | 39,639 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.051, rasio=0.009) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| f8801972 | c6b0eadc | serve | revealed (0/0/4) | 39,070 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| f131675d | c7cc33a2 | serve | revealed (0/0/0) | 41,134 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| ce1c34f3 | cc856ac0 | serve | revealed (0/0/3) | 42,467 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| 02b24949 | d854b19a | serve | revealed (0/0/1) | 40,021 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.0, rasio=0.0) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
| f18b1675 | e20d251f | serve | revealed (0/0/2) | 42,261 | 0 | MATI | YA | GAGAL url,density,ratio (url=0, dens=0.45, rasio=0.115) | a✗ b✗ c✓ e✗ f– g✓ d✗ | **TAHAN** |
Catatan tabel: kolom "Lantai" untuk baris yang lolos ditulis LOLOS; aktual K-1(b)/K-2 f0bb3586 (1,32 / 0,31) menunjukkan ia lolos dua sub-lantai itu dan hanya gugur di K-1(a) + trace + liveness. Skor (d) GAGAL di 29/29 baris — konsekuensi definisi wrapper: (d) gugur bila ada finding audit/lantai/trace apa pun yang bertahan.

---

## 4. (d) Jawaban yang teksnya TIDAK ditemukan — TIDAK ADA

- **Teks ditemukan: 29/29** (26/26 serve + 3/3 klaim), tervalidasi silang dua sumber independen (output job vs reveal API, panjang identik 29/29).
- **Liveness direplay: 26/26 serve** (detail ISR tersimpan untuk semua ISR serve; klaim = N/A jalur, bukan "tidak bisa direplay").
- **n efektif backtest = 29 untuk lapis isi; 26 untuk lapis liveness.** Tidak ada sel yang hilang; satu-satunya sel yang kosong secara substantif adalah "draf serve bersih yang lolos gerbang isi" (0/26) — itu temuan, bukan kekurangan data (lihat §6 butir 1).

---

## 5. (e) Vonis akhir lawan ambang dokumen gerbang

**Dokumen `GERBANG-SERVE-2026-11-15.md` TIDAK menetapkan ambang penerimaan numerik untuk backtest.** Kata "ambang" di dokumen itu hanya merujuk (i) ambang K-2 yang tidak diubah — kutipan persis §4 catatan status: *"(ambang K-2 tetap 0,30)"*; dan (ii) §5 butir 4: *"Ambang U2 (K-2) tetap berlaku juga sebagai lantai serve — konfirmasi tidak ada ambang khusus-serve."* Syarat hidup-lagi yang dokumen tetapkan berbentuk **daftar keputusan lab** (§5), bukan angka lolos:

> *"## 5. KEPUTUSAN YANG DIMINTA DARI LAB (syarat serve boleh hidup lagi)"* — butir 1: *"Semantik: apakah serve boleh jalan dengan gerbang mekanis saja (menerima risiko sisa #1 secara tertulis), atau wajib ada tahap self-VFP dulu…"*; butir 6: *"Korpus trace: kumpulkan draf serve nyata (lolos + falsified historis) sebagai korpus uji detektor sebelum mengandalkan pola saat ini."* — **backtest ini adalah pelaksanaan butir 6 itu.**

Maka vonis (e) dinyatakan berdampingan dengan kriteria yang benar-benar ada:

| Kriteria (dari dokumen gerbang sendiri) | Angka backtest | Vonis |
|---|---|---|
| Spesies f0bb3586 harus tertahan oleh lapis trace (kasus kontrol §3 dokumen: fixture ber-trace *"LOLOS wrapper polos … tetapi DITAHAN oleh lapis trace"*) | Di korpus nyata: trace menahan **4/4 falsified serve** + 21/22 revealed; dan keempat falsified juga tertahan liveness DAN lantai secara mandiri | **TERPENUHI, dengan redundansi 3 lapis** |
| Target mati tidak boleh dilayani (desain lapis 1, §1: pola flag basi = MATI, fail-closed) | **25/26** pertanyaan serve MATI pada jam submitnya; 1 LIVE (0dbd4532, pertanyaan terbuka non-maraton) — dan drafnya tetap tertahan lapis isi; flag ISO `marathonEligible=False` 26/26 | **TERPENUHI** untuk tujuan gerbang (tidak ada draf yang akan terkirim ke target mati) |
| Risiko sisa #1 dokumen (§4 butir 1): *"Klaim jalur klaim #1 dulu lolos semua ambang mekanis dan mati di dukungan semantik — spesies kegagalan itu masih bisa lolos gerbang serve ini."* | Terkonfirmasi terukur: **2/3 teks klaim falsified LOLOS gerbang isi** (5/6 dan 6/6) | **RISIKO SISA NYATA — bukan kegagalan backtest, melainkan batas yang dokumen sendiri nyatakan.** Keputusan menerimanya = §5 butir 1, wewenang lab/user, bukan angka backtest |
| Ambang numerik backtest (mis. "tertangkap ≥X/4") | **Tidak ada di dokumen** | Tidak bisa dinyatakan lolos/gagal terhadap ambang yang tidak pernah ditetapkan; menetapkannya sekarang adalah keputusan lab |

**Kesimpulan lini A:** sebagai *rem*, gerbang ini bekerja pada 100% korpus historis yang merugikan kita: 4/4 falsified serve tertahan (masing-masing oleh tiga lapis independen), 25/26 target mati tersaring di prepare, dan tidak satu pun dari 26 jawaban serve historis yang akan terkirim — konsisten dengan fakta bahwa 26/26 memang tidak layak kirim (0 URL, mayoritas trace mentah, 0 eligible). Yang backtest TIDAK bisa buktikan: (1) laju false-block atas draf serve yang baik (sel kosong — korpus tidak memuat draf serve bersih); (2) ketahanan terhadap falsified semantik (2/3 klaim lolos) — keduanya persis dua hal yang dokumen gerbang serahkan ke keputusan lab §5 butir 1 dan uji live terawasi §5 butir 5.

---

## 6. Peringatan metodologis (baca sebelum memakai angka ini)

1. **Revealed ≠ verified.** Ke-22 "false-block" di (b) adalah jawaban tanpa verdict; menyebutnya "jawaban bagus yang terblokir" tidak didukung data. Yang terukur: gerbang menahan 22/22 keluaran mentah tak-tergerbang yang upside-nya memang $0.
2. **Liveness adalah replay, bukan rekaman.** Detail ISR diambil 1–5 jam sesudah submit; ronde disaring ke `startedAt ≤ submit`, tetapi flag `marathonActive/marathonConcluded` adalah keadaan saat fetch. Untuk 4 falsified, alasan MATI-nya adalah `endsAt` maksimum yang lewat sebelum submit (fakta waktu absolut, tidak tergantung flag) — kesimpulan untuk (a) kokoh. Untuk baris revealed, arah kesalahan yang mungkin: ronde yang saat submit masih terbuka tetapi detailnya terambil sesudah ronde itu berakhir akan terbaca MATI — artinya hitungan 21/22 MATI bisa sedikit melebihkan; ini tidak mengubah (a) dan tidak mengubah vonis gabungan (b) karena 22/22 tetap gugur di lapis isi.
3. **Keanggotaan ronde:** ISO kita tidak muncul di `marathonEligibleIsos` pada detail tersimpan untuk 26/26 serve (daftar itu mencerminkan ronde pada snapshot detail) — konsisten dengan flag ISO `marathonEligible=False` 26/26; serve pagi itu berjalan dari flag basi poller kata kunci, di luar set eligible.
4. **Regenerasi:** produksi memberi 1× regenerasi untuk draf di bawah lantai panjang; backtest tanpa `regen_fn`. Teks terpendek korpus 5.147 kar > lantai 4.500 → status wrapper OK 29/29; peringatan ini tidak berdampak ke satu baris pun.
5. **Skor (g)** dinilai dengan asumsi prosa (bawaan `gate_answer` tanpa kwargs) — skema keluaran job hanya menuntut field `answer` string; tidak ada tuntutan JSON pada prompt job yang tersimpan.
6. **Panel verdict bisa tumbuh** sesudah sweep 05:00 (contoh: f0bb3586 0/1/1 → 0/2/2); status final falsified/revealed yang dipakai di sini adalah keadaan terkonfirmasi terakhir (sweep 19:00 15 Nov: 22 revealed + 7 falsified).

---

*Artefak kerja: skrip + hasil mentah backtest dijalankan dari `provider/serve_gate.py` atas korpus `jobs-0900.json` + sweep `isos-*.json` + `verdicts-0500.json` + detail `isr-*.json` (hidden_files goal, run-2026-11-14-0700/0900/1300 + run-2026-11-15-0500). File terkait: `GERBANG-SERVE-2026-11-15.md`, `VERDICT-LEDGER.md` baris #5–#8, `MEKANISME-DAN-LAPANGAN.md` §82/§97/§98.*
