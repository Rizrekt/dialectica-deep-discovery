# AUDIT SABOTASE-DIRI PIPA GENERASI SERVE — Dialectica

- Tanggal audit: 2026-11-16 ±04:10–04:20 WIB (audit independen, baca-saja atas kode; satu-satunya file yang ditulis = laporan ini).
- Ruang lingkup: `provider/run_serve.py`, `vyce_serve_*.py`, `vyce_provider.py`, `gemini_provider.py`, `lib/citation_patch.py`, `lib/clean_answer.py`, `cloudflare_serve_*.py`, `cloudflare_provider.py`, `serve_gate.py`, `openrouter_wrapper.py`, `openrouter_provider.py`, `dashscope_provider.py`, `zai_provider.py`; pembanding seperlunya: klien konektor Cloudflare/OpenRouter/Z.ai/DashScope (`custom-connectors/*/bin/client.py`).

## ⚠️ KEADAAN DISK BERUBAH SELAMA AUDIT (wajib dibaca dulu)

Bacaan pertama audit ini (04:10 WIB) masih menangkap versi LAMA dua titik yang sudah dikenal. Pada 04:10–04:11 WIB sesi utama menjalankan improve pass-nya sendiri dan **kedua titik itu sudah DIPERBAIKI di disk**:

| Titik dikenal | Keadaan di disk saat audit ditutup | Bukti |
|---|---|---|
| (1) `citation_patch.clean()` v1 membuang semua URL/DOI + menempel NOTE "avoids pinpoint references" | **SUDAH DIPERBAIKI → v2**: `clean()` kini mempertahankan jawaban persis (URL/DOI/paragraf sitasi utuh), hanya membuang NOTE warisan v1 verbatim + karakter zero-width. v1 tersimpan di `lib/citation_patch.py.bak-20261116-improve`. | `lib/citation_patch.py:54-64` (clean v2), `:45-50` (NOTE hanya konstanta untuk dibuang), `:57-59` (pembuangan note warisan); smoke v2 `lib/clean_smoke.py:22-31` |
| (2) `call_vyce` memakai `reasoning_content` sebagai jawaban bila `content` kosong | **SUDAH DIPERBAIKI**: konten kosong kini `raise RuntimeError` (generasi gagal → pindah model kandidat); reasoning hanya dihitung panjangnya untuk diagnostik, tidak pernah dikirim. | `vyce_provider.py:133-145` |

Timestamp file yang berubah selama audit: `lib/citation_patch.py` 04:10:48, `lib/clean_smoke.py` 04:11:02, `vyce_provider.py` 04:11:11, `gemini_provider.py` 04:11:14 (hanya label log clean v2), `vyce_serve_common.py` 04:11:32 (penambahan `SERVE_FORMAT_CONTRACT` — lihat titik A8). Semua vonis di bawah adalah atas **keadaan disk final 04:11:59 WIB**, diverifikasi ulang baris-per-baris sesudah perubahan berhenti.

---

## TEMUAN BARU (selain dua titik dikenal di atas)

### S1 — Jalur KLAIM Vyce (dan Gemini) tetap TANPA wrapper/gerbang apa pun — **BERMASALAH (sisa terbesar)**

- `vyce_provider.py:246-252`: sesudah `clean()` (kini v2, jinak), jawaban ditulis **langsung** ke stdout. Tidak ada `wrap_answer`, tidak ada lantai 4.500, tidak ada audit angka E1, tidak ada lantai K-1/K-2, tidak ada deteksi thinking-trace, tidak ada `LENGTH_SUFFIX` (grep: nol kemunculan di file ini).
- `gemini_provider.py:97-104`: pola identik — `clean()` lalu tulis langsung; tanpa wrapper, tanpa suffix panjang.
- Kontras lane lain: `openrouter_provider.py`, `cloudflare_provider.py`, `dashscope_provider.py`, `zai_provider.py` semuanya `apply_steering + LENGTH_SUFFIX + run_pipeline(wrap_answer) + sendable fail-closed` (mis. `cloudflare_provider.py` `run_pipeline` + blok WITHHELD di `main()`).
- Dampak: bila `vyce_provider.py` dipakai sebagai `DIALECTICA_PROVIDER_CMD` untuk `trued answer` (mode klaim, `run_serve.py` mode answer), satu-satunya pagar mekanik antara draf mentah dan server adalah operator manusia. Serve aman karena `vyce_serve_common.vyce_pipeline` membungkusnya dengan `serve_gate.gate_answer` — klaim tidak punya padanan itu. Mitigasi yang ada memang doktrin jalur klaim (self-VFP operator, T10.2/T12), jadi ini **inkonsistensi struktural yang terdokumentasi sebagian**, bukan kebocoran senyap — tapi lantai mekanik §45 secara harfiah tidak berjalan di lane klaim Vyce/Gemini.

### S2 — Gemini: semua `parts` digabung tanpa menyaring part berpikir — **BERMASALAH (potensi jejak penalaran, padanan titik dikenal #2 di lane lain)**

- `gemini_provider.py:72-73`: `text = "".join(p.get("text", "") for p in parts)` atas **semua** part kandidat pertama, tanpa memeriksa flag `thought` pada part. Model Gemini kelas Flash berpikir mengembalikan part berpikir (`thought=true`) dalam daftar yang sama; bila API mengembalikannya, monolog berpikir tercampur ke jawaban — spesies yang sama dengan fallback `reasoning_content` Vyce lama, lewat pintu berbeda.
- Belum terbukti live dari artefak di folder ini (tidak ada sampel respons mentah Gemini tersimpan), jadi vonisnya potensi kode, bukan kejadian. Lane ini sedang tidak dipakai serve/klaim aktif (grounding dimatikan, §29.4), sehingga urgensi rendah — tapi jangan aktifkan lane Gemini sebelum penyaringan `thought` dipasang.
- Tambahan: `gemini_provider.py:57` — body request tanpa `generationConfig`/`maxOutputTokens` sama sekali: batas keluaran = default server, tidak selaras dengan lantai 4.500 maupun pita lane lain.

### S3 — Pintu grounding Vyce→Gemini melewati SEMUA pagar lokal — **BERMASALAH (bersyarat, saat ini tertidur)**

- `vyce_provider.py:210-220`: bila `DIALECTICA_GEMINI_GROUNDING=1` dan prompt memuat satu saja `WORLD_MARKERS` (daftar sangat luas, `:37-40` — "will ", "stock", "season", "match", "launch", …), stdout Gemini ditulis **langsung** sebagai jawaban Vyce: melewati `clean()`, melewati `_format_gate` (jawaban JSON bisa rusak format), dan di jalur klaim melewati segalanya (lihat S1). Di jalur serve, `serve_gate` di hilir masih menangkapnya, jadi dampak penuh hanya di klaim.
- Saat ini env tidak diset di mana pun (grounding mati sejak 2026-11-14) → tertidur, bukan aktif. Tapi ini satu-satunya jalur di pipa di mana keluaran satu provider menjadi keluaran final provider lain tanpa satu pun pemeriksaan.

### S4 — Cap 10 generasi/hari pilot serve Vyce TIDAK terpasang di kode — **BERMASALAH**

- `vyce_serve_common.py:24-26` menyatakannya eksplisit: "No generation cap is added here".
- `run_serve.py` jalur serve Vyce (blok `name == "vyce" and mode == "serve"`, berakhir `subprocess.run(args, env=env)` ±baris 339-340): **tanpa** `supervise_serve`, tanpa penolakan start-di-cap — keduanya hanya ada di jalur Cloudflare serve (`_run_cloudflare_serve`, `EXIT_SERVE_CAP_REACHED=6`).
- Lebih dalam: catatan usage Vyce tidak bisa dipakai menghitung cap sekalipun supervisor dipasang — `vyce_provider.py:68-74` record `token-usage.jsonl` Vyce **tidak punya field `lane`**, sedangkan penghitung cap `cloudflare_serve_common.serve_generations_today()` menyaring `lane == "cloudflare-serve"`. Generasi serve Vyce dan klaim Vyce tidak terbedakan di log.
- Dampak: cap pilot 10/hari-UTC yang tertulis di PAKET-RESTART-SERVE hanya ditegakkan oleh badan cron/disiplin sesi, bukan oleh kode. Satu-satunya pagar keras serve Vyce saat ini = gerbang isi (liveness + wrapper + trace + E3).

### S5 — Cache-hit serve tidak memeriksa ulang liveness — **BERMASALAH (ringan, celah urutan)**

- `vyce_serve_provider.py` jalur utama (cache hit, bukan `correction`): cache dicetak verbatim dan `return 0` — pemeriksaan `fallback_dead_reason` hanya berjalan di jalur fallback (cache miss). `cloudflare_serve_provider.py` pola yang sama.
- `cloudflare_serve_common.py` `write_cache`/`read_cache`: tanpa TTL/stempel waktu yang diperiksa; cache bersama dua lane.
- Dampak praktis kecil (prepare→klaim normalnya berdekatan, dan prepare sendiri lolos liveness), tapi secara konstruksi: jawaban yang disiapkan saat ronde masih hidup bisa terkirim sesudah ronde berakhir bila job tertunda lama, dan tidak ada lapisan yang menangkapnya. Saat audit: direktori `serve-cache/` tidak ada → tidak ada cache basi warisan era pra-gerbang yang bisa terkirim. **AMAN untuk keadaan sekarang, BERMASALAH sebagai desain.**

### S6 — Budget token Vyce: reasoning ikut memakan `max_tokens` 8.000, tanpa kontrol thinking — **BERMASALAH (ringan, kini fail-closed tapi boros)**

- `vyce_provider.py:93-98`: body hanya `model/messages/max_tokens=8000/stream` — tidak ada parameter penekan thinking, tidak ada alokasi reasoning terpisah. Modelnya (`glm-5.3-flash`, `deepseek-v4.1`, `:53`) adalah model berpikir: token reasoning dan konten berbagi kuota 8.000 yang sama.
- Kontras: DashScope mengunci `EXTRA_BODY = {"enable_thinking": False}` (`dashscope_provider.py` LOCKED CONFIG A); Z.ai memanggil klien dengan `--thinking disabled` (`zai_provider.py` condition 1); klien Cloudflare/OpenRouter memisahkan reasoning dari teks di sisi klien (lihat A3).
- Sesudah perbaikan titik #2, kegagalannya kini aman (konten kosong = raise → ganti model), tapi benturan nyatanya: `SERVE_FORMAT_CONTRACT` meminta 6.000–9.000 karakter, "up to 12,000" untuk marathon (`vyce_serve_common.py:77`) — jawaban 12.000 karakter + reasoning panjang bisa terpotong di 8.000 token; jawaban terpotong kehilangan blok penutup penamaan kebaruan, dan `sendable` gerbang tidak menilai butir (e) sebagai pintu mati (hanya status + temuan audit + gerbang (g)) → draf terpotong **bisa** lolos mekanik. Risiko, bukan kejadian terukur.

### S7 — Serve Cloudflare tidak punya kontrak format padanan — **BERMASALAH (ringan, inkonsistensi antar-lane serve)**

- Sesudah improve pass, serve Vyce membawa `SERVE_FORMAT_CONTRACT` penuh (anti-trace, struktur ##, ≥2 URL, larangan penutup evasif, penamaan kebaruan) di `vyce_serve_common.py:61-93`, ditempel sekali dengan penanda (`:110-111`).
- Serve Cloudflare hanya menempel `LENGTH_SUFFIX` (panjang saja): `cloudflare_serve_prepare.py:64` dan `cloudflare_serve_provider.py` (fallback). Tidak ada instruksi anti-trace/E3/kebaruan di hulu — lane ini bertumpu penuh pada gerbang hilir untuk cacat yang di Vyce kini dicegah di hulu. Bukan sabotase (gerbangnya sama), tapi dua serve lane kini berjalan dengan standar instruksi berbeda.

### S8 — `_format_gate` Vyce memotong jalan sebelum `clean()` — **AMAN-bersyarat (catatan)**

- `vyce_provider.py:240-245`: bila prompt menuntut JSON, objek hasil ekstraksi dikembalikan sebelum `clean()` berjalan. Di era v1 ini berarti jalur JSON lolos dari stripper (ironisnya justru terlindungi); di era v2 tidak ada lagi yang dilewati selain pembuangan note warisan/zero-width. Konversi `confidence` 0–1 → persen (`:197-199`) sesuai perilaku teramati server. Vonis: AMAN saat ini; catat saja bahwa jalur JSON memang sengaja tanpa pagar sitasi — masuk akal untuk skema terstruktur.

---

## TITIK YANG DIPERIKSA DAN DINYATAKAN AMAN

- **A1 — `openrouter_wrapper.apply_citation_patch`** (`openrouter_wrapper.py`, fungsi patch sitasi): hanya membuang **token angka** yang terikat sintaksis ke dokumen bernama dengan nilai salah/tak-terverifikasi, kanan-ke-kiri, tidak pernah menyisipkan nilai/sumber pengganti, tidak menyentuh URL. Ini pagar E1 yang sah — kebalikan pola v1. **AMAN.**
- **A2 — Lantai mekanik wrapper** (`mechanical_floor` + `floor_findings`, `openrouter_wrapper.py`): K-1(a) ≥1 URL, K-1(b) densitas ≥0,5/1.000 kar, K-2 rasio terikat ≥0,30 diukur atas teks ter-patch (teks yang benar-benar terkirim); kegagalan = temuan FLOOR span-None → menahan draf di semua lane wrapper. **AMAN.**
- **A3 — Klien konektor memisahkan reasoning dengan benar**: Cloudflare `client.py:129-152` (`extract_answer_text` mengambil `message.content` saja; reasoning hanya dihitung karakternya, `:165-175`, teksnya tidak pernah dikembalikan); OpenRouter `client.py:132-181` (`text` = gabungan `content` saja, `reasoning_parts` hanya dihitung); Z.ai & DashScope klien pola sama (teks = `content`, reasoning = penghitung). Jadi di empat lane konektor, **tidak ada** fallback reasoning→jawaban. Satu-satunya tempat pola itu pernah hidup adalah Vyce (sudah diperbaiki) dan potensi Gemini S2. **AMAN.**
- **A4 — Kontrol thinking lane klaim**: DashScope `enable_thinking=false` terkunci; Z.ai `--thinking disabled` + retry 1305 tepat satu kali; keduanya terdokumentasi sebagai syarat bench. **AMAN.**
- **A5 — `serve_gate.py`**: deteksi thinking-trace 4 keluarga + E3 terbatas wilayah penutup/seksi sumber (badan tidak dipindai — false-positive terukur 0/203), liveness tiga-field fail-closed, dan kejujuran `semantic_vfp.performed=False` (celah C5 yang sudah dikenal, dinyatakan terbuka di kode, bukan disembunyikan). Tidak ada sisipan teks apa pun ke draf — gerbang hanya menahan/melepas. **AMAN.**
- **A6 — Sisipan ekor di seluruh pipa**: grep menyeluruh atas pola penempelan teks (NOTE, footer, "Note on", string yang ditambahkan ke jawaban) menemukan hanya: (i) NOTE v1 — sudah jadi konstanta-untuk-dibuang di v2; (ii) `LENGTH_SUFFIX`/`EXPANSION_INSTRUCTION`/`SERVE_FORMAT_CONTRACT`/`OPERATOR STEERING` — semuanya sisipan ke **prompt** (instruksi ke model), bukan ke jawaban terkirim; (iii) `"\n"` penutup baris di `sys.stdout.write`. Tidak ada iklan/footer/note lain yang menempel ke teks jawaban di file mana pun yang diperiksa. **AMAN.**
- **A7 — Stripper lain**: satu-satunya stripper teks jawaban di pipa adalah `citation_patch.clean` (v2, jinak) dan patch angka wrapper A1. `normalize_mojibake` di wrapper hanya memperbaiki run double-encoding yang round-trip persis; karakter sah dibiarkan. `lib/clean_answer.py` kini sekadar meneruskan `clean()` v2 (label stderr "fake citation" di `:10` basi secara kata, fungsi benar). **AMAN** (satu catatan kosmetik).
- **A8 — Batas panjang antar-lane selaras**: lantai 4.500 satu definisi (`LENGTH_FLOOR` wrapper) dipakai semua lane wrapper + gerbang serve; pita suffix 5.500–7.500 identik di empat lane konektor dan dinyatakan advisory untuk marathon. Benturan token yang nyata hanya S6 (Vyce). **AMAN kecuali S6.**
- **A9 — Cache serve saat ini bersih**: `serve-cache/` tidak ada di disk → tidak ada jawaban era pra-gerbang/v1 yang bisa terkirim lewat jalur cache-hit S5. **AMAN (keadaan), desainnya tetap S5.**

## REKAPITULASI VONIS

| # | Titik | Vonis |
|---|---|---|
| dikenal-1 | `citation_patch` v1 stripper + NOTE evasif | SUDAH DIPERBAIKI di disk (v2, 04:10 WIB) |
| dikenal-2 | Vyce fallback `reasoning_content` | SUDAH DIPERBAIKI di disk (raise, 04:11 WIB) |
| S1 | Klaim Vyce/Gemini tanpa wrapper & lantai | **BERMASALAH** |
| S2 | Gemini gabung part berpikir + tanpa batas keluaran | **BERMASALAH** (potensi, lane tertidur) |
| S3 | Bypass grounding Vyce→Gemini | **BERMASALAH** (bersyarat env, tertidur) |
| S4 | Cap 10/hari serve Vyce tidak terpasang + usage tanpa lane | **BERMASALAH** |
| S5 | Cache-hit serve tanpa cek ulang liveness/TTL | **BERMASALAH** ringan (keadaan kini aman) |
| S6 | Vyce `max_tokens` berbagi reasoning, tanpa kontrol thinking | **BERMASALAH** ringan (fail-closed, boros + risiko potong) |
| S7 | Serve Cloudflare tanpa kontrak format | **BERMASALAH** ringan (inkonsistensi) |
| S8 | `_format_gate` mendahului `clean()` | AMAN-bersyarat |
| A1–A9 | Wrapper, lantai, klien konektor, serve_gate, sisipan ekor, stripper lain, batas panjang, cache kini | AMAN |

Prioritas perbaikan yang disarankan (di luar wewenang audit baca-saja ini): S1 (bungkus klaim Vyce dengan wrapper yang sama, atau nyatakan eksplisit di `run_serve` bahwa klaim Vyce = tanpa pagar mekanik), lalu S4 (cap + field lane), lalu S2/S3 sebelum lane Gemini/grounding disentuh lagi.
