# SOLUSI-39 — AUDIT KODE JALUR SERVE §39 (Cloudflare serve)

**Tanggal:** 2026-11-13 (WIB) · **Sifat:** audit READ-ONLY atas kode. NOL serve live dinyalakan, NOL job diambil, NOL klaim — STOP TOTAL Dialectica berlaku penuh selama audit ini.
**File yang dibaca baris demi baris:** `provider/run_serve.py` (297 baris), `provider/cloudflare_serve_prepare.py` (80), `provider/cloudflare_serve_provider.py` (66), `provider/cloudflare_serve_ready.py` (45), `provider/cloudflare_serve_common.py` (212), `provider/test_cloudflare_serve.py` (410). Dependensi penentu yang ikut dibaca pada titik relevan: `cloudflare_provider.py` (`generate`, `_log_usage`, `apply_steering`, `LENGTH_SUFFIX`, budget neuron) dan `openrouter_wrapper.py:548-609` (`wrap_answer`).
**Verifikasi empiris offline yang dijalankan:** `python3 test_cloudflare_serve.py` → **ALL PASS 25/25, exit 0** (generasi di-stub in-process, log & cache di direktori temp) dan `python3 run_serve.py --cloudflare-serve --dry-run` → exit 0, count terbaca **0/10**, "nothing launched, nothing submitted".

---

## VONIS RINGKAS

Klaim "jalur serve §39 membetulkan cacat one-shot (draf digerbang ≠ draf terkirim)" = **BENAR hanya di jalur utama (primary path)**, dengan 3 catatan: (i) provider menambahkan satu `"\n"` di stdout; (ii) cache **tanpa hash/fingerprint/TTL** — yang mengikat draf ke job hanyalah nama file = isrId, jadi teks bisa tertimpa/ basi tanpa terdeteksi; (iii) di luar jalur utama ada **fallback live** yang men-generate ulang di saat job — ia digerbang ulang penuh, tapi kegagalannya berubah jadi job dropped, dan ia **tidak dicek cap serve** sebelum men-generate (celah cap, dirinci di §2).

---

## 1. Apakah draf lolos gerbang PREPARE persis byte-sama dengan yang dikirim provider?

### 1.1 Jalur utama: YA (isi), dengan +1 newline di stdout

Rantai buktinya tertutup:

1. **Teks yang digerbang = teks final wrapper.** `cloudflare_serve_common.serve_pipeline()` (`common.py:188-212`) memanggil `cp.generate(...)` lalu `wrap_answer(first["text"], regen_fn=...)`. `wrap_answer` (`openrouter_wrapper.py:548`) mengembalikan `{"text": patched, ...}` (`openrouter_wrapper.py:608`) — yaitu teks SESUDAH normalisasi mojibake + citation patch + floor §45. `sendable` dihitung atas hasil itu juga (`common.py:206-211`): `status == "OK"` DAN tidak ada temuan audit tanpa `span` DAN skor format (g) == "LOLOS". (Catatan: `wrap_answer` membuang field `span` dari report, jadi secara praktik SEMUA temuan audit yang tersisa = unpatchable = menahan draf — fail-closed, sama seperti lane klaim.)
2. **Hanya teks sendable yang masuk cache.** `cloudflare_serve_prepare.prepare_row()` (`prepare.py:34-65`): bila `not result["sendable"]` → return 1 (pass-over, pertanyaan dilewati SEBELUM ada klaim/job). Bila sendable → `csc.write_cache(isr_id, result["text"])` (`prepare.py:61`) — objek `result["text"]` yang sama persis dengan yang dinilai gerbang, bukan generasi baru.
3. **Provider jalur utama tidak men-generate apa pun.** `cloudflare_serve_provider.main()` (`provider.py:27-38`): bila `DIALECTICA_JOB_KIND != "correction"` dan `read_cache(isr_id)` tidak None → `sys.stdout.write(cached + "\n")`, return 0. Tidak ada panggilan `generate`/`serve_pipeline` di cabang ini (dibuktikan juga tes `provider: cache hit -> cached text, exit 0` dengan generate yang akan meledak bila dipanggil — lulus).

**Deviasi byte yang nyata:** provider menulis `cached + "\n"` (`provider.py:37`). Jadi yang diterima `trued` dari stdout = byte cache + SATU newline tambahan di akhir. Isi jawaban identik; apakah `trued` men-strip newline itu sebelum submit TIDAK bisa diverifikasi dari 6 file ini (itu perilaku klien `trued.py`, di luar cakupan audit). Ini satu-satunya perbedaan byte di jalur utama.

### 1.2 Mekanisme cache: kunci = isrId saja, TANPA hash

- Direktori: `cache_dir()` (`common.py:106-109`) = env `DIALECTICA_SERVE_CACHE_DIR` bila diset, selain itu `provider/serve-cache/`.
- Path: `cache_path(isr_id)` (`common.py:111-112`) = `<cache_dir>/<isr_id>.txt`.
- Tulis: `write_cache()` (`common.py:115-118`) = `open(path, "w", encoding="utf-8")` tulis teks apa adanya. Mode `"w"` = **timpa tanpa syarat**.
- Baca: `read_cache()` (`common.py:121-129`) = file tidak ada/OSError → None; isi kosong/whitespace-only → None; selain itu kembalikan teks utuh (tidak di-strip).
- **Tidak ada** hash, checksum, HMAC, fingerprint prompt, timestamp, TTL, penguncian file, atau penulisan atomik di kelima file serve (grep `hashlib|sha256|md5|hmac|flock|lock` = nol hit relevan). Kunci cache di provider diambil dari env `DIALECTICA_ISR_ID` (`provider.py:29`), bukan dari prompt job.

### 1.3 Cara draf terkirim bisa BERBEDA dari draf yang digerbang prepare

1. **Fallback live** — lihat §2 (penyebab utama, by design).
2. **Tertimpa prepare ulang:** prepare kedua untuk isrId yang sama menimpa file (`"w"`); provider menyajikan versi terakhir di disk, bukan versi yang ada saat bid/READY tertentu — tidak ada pengikatan versi antara READY dan provider.
3. **Cache basi lintas waktu/hari:** tidak ada TTL/pembersihan; file sisa hari sebelumnya tetap dibaca provider dan tetap lolos READY (lihat §3.2) selama isrId sama.
4. **Ketidakcocokan env:** `DIALECTICA_ISR_ID` kosong/salah → `read_cache` None → fallback. `DIALECTICA_SERVE_CACHE_DIR` yang berbeda antara proses prepare dan provider → cache "hilang" → fallback.
5. **File diubah pihak lain / rusak sebagian:** tanpa hash, perubahan apa pun di file `.txt` antara prepare dan job disajikan apa adanya (selama non-kosong).

---

## 2. Fallback live: pemicu + apakah digerbang ulang

### 2.1 Pemicu (semua di `provider.py:31-47`)

Fallback berjalan bila SALAH SATU terjadi:

- **`DIALECTICA_JOB_KIND == "correction"`** — cache dilewati SENGAJA walau ada, karena teks cache justru objek yang sedang dikoreksi skemanya (docstring `provider.py:11-16`).
- **Cache miss** — `read_cache(isr_id)` None: env isrId kosong, file tidak ada, atau file kosong/whitespace. Docstring menamai penyebab terakhir: "arrivals with no prepared cache entry (e.g. work assigned outside the prepare path)".

Syarat lanjut fallback: prompt stdin tidak kosong; prompt kosong + tanpa cache → return 2 (`provider.py:39-42`), tidak ada generasi.

Prompt fallback juga BERBEDA basisnya dari prepare: prepare menyusun prompt sintetis dari baris pencarian (`prompt_from_row`, `common.py:176-185`: judul+konten), sedangkan fallback memakai **prompt job asli dari trued** (`provider.py:43`). Keduanya sama-sama dilewatkan `cp.apply_steering(prompt, isr_id) + cp.LENGTH_SUFFIX` (prepare `prepare.py:47`; provider `provider.py:43`), tapi konteks isi promptnya tidak sama → draf fallback bukan sekadar "generasi ulang dari prompt yang sama".

### 2.2 Gerbang ulang: YA, penuh — tapi konsekuensinya beda kelas

- Fallback memanggil `csc.serve_pipeline(full, isr_id or None, allow_regen=True)` (`provider.py:45-47`) — pipeline yang sama dengan prepare: generate (lane `cloudflare-serve`, budget neuron gabungan claim+serve) → `wrap_answer` → kriteria `sendable` identik (`common.py:206-211`).
- Draf fallback tidak sendable → **exit 1 dengan stdout kosong** (`provider.py:52-61`); menurut docstring + §35, `trued` memperlakukannya sebagai "nothing submitted" dan **job di-drop**. Beda mendasar dari prepare: kegagalan prepare = pass-over gratis sebelum klaim; kegagalan fallback = job yang sudah diterima gugur (kelas abandoned/dropped).
- `NeuronBudgetAbort` / `GenerationError` ditangkap → exit 1, stdout kosong (`provider.py:48-50`). Exception LAIN tidak ditangkap di provider (kontras: prepare menangkap `Exception` generik, `prepare.py:55-56`) → akan lolos sebagai traceback/exit non-nol.

### 2.3 CELAH CAP pada fallback (temuan audit)

Provider fallback **tidak pernah memanggil `serve_generations_today()`** dan tidak ada cek `SERVE_CAP` di `cloudflare_serve_provider.py`; `allow_regen=True` dikunci keras. Artinya satu kedatangan fallback pada hari yang cap-nya sudah penuh tetap bisa memulai **hingga 2 generasi** (1 + 1 regen wrapper) di atas cap 10. Satu-satunya rem yang masih berlaku di titik itu adalah budget neuron di `cp.generate` (abort pra-spend bila total neuron hari itu di kedua lane Cloudflare > 9.000 dari plafon 10.000 — `cloudflare_provider.py:140-157`) dan SIGINT supervisor yang menghentikan proses serve (bukan membatalkan generasi in-flight). Generasi fallback tetap tercatat di bawah lane `cloudflare-serve` (`serve_pipeline`, `common.py:193-201`), jadi ia menggerus hitungan cap secara post-hoc, tapi tidak dicegah oleh cap itu sendiri.

---

## 3. Cap generasi serve/hari + veto READY_CMD

### 3.1 Cap: `SERVE_CAP = 10` generasi klien per hari UTC (`common.py:59`)

- **Penghitung:** `serve_generations_today()` (`common.py:96-104`) menghitung record di `token-usage.jsonl` — path dari `usage_log_path()` (`common.py:72-76`: env `DIALECTICA_TOKEN_USAGE_LOG` bila diset, selain itu `cp.USAGE_LOG`) — yang `lane == "cloudflare-serve"` dan `ts`-nya berawalan tanggal hari ini UTC (`_today_utc`, `common.py:92-93`). Satu record per generasi: `cp.generate` menulis satu record via `_log_usage` setiap panggilan (`cloudflare_provider.py:122-138, 187`); lane klaim memakai label lain (`cloudflare-gptoss`) dan tidak ikut terhitung.
- **Pipeline maks 2 generasi:** 1 generasi + maks 1 regenerasi wrapper (`PIPELINE_MAX_GENERATIONS = 2`, `common.py:60`; `wrap_answer` memanggil `regen_fn` paling banyak sekali, `openrouter_wrapper.py:564-571`).
- **Tiga lapis penegakan:**
  1. **Prepare (pra-klaim, penegak keras utama)** — `prepare.py:40-50`: `remaining = SERVE_CAP - used`; `remaining <= 0` → exit 1 pass-over SEBELUM generasi apa pun. `allow_regen = remaining >= 2`, jadi pada sisa tepat 1, pipeline berjalan TANPA regen dan hitungan mendarat tepat di cap, tidak pernah di atasnya (dibuktikan tes: prefill 9 + draf pendek → tepat 1 generasi, count 10, exit 1; prefill 8 + regen → 2 generasi, count 10, exit 0).
  2. **Start refusal** — `run_serve._run_cloudflare_serve` (`run_serve.py:191-196`): bila count hari ini ≥ cap saat start → serve TIDAK dinyalakan, **exit 6** (`EXIT_SERVE_CAP_REACHED`). Rotasi kata kunci di hari yang sama tidak bisa menghidupkannya lagi.
  3. **Supervisor** — `supervise_serve()` (`run_serve.py:100-159`): polling tiap 2,0 dtk (`SUPERVISOR_POLL_S`); bila `count_fn() >= cap` → SIGINT ke `trued serve` (graceful drain ala klien sendiri), tunggu drain s/d 1.200 dtk (`SUPERVISOR_DRAIN_TIMEOUT_S`) lalu eskalasi SIGTERM/SIGKILL; supervisor TIDAK PERNAH me-relaunch. SIGINT/SIGTERM ke supervisor diteruskan ke child (child tidak pernah yatim). Kegagalan membaca hitungan diperlakukan sebagai "belum cap" (`run_serve.py:127-131`) supaya serve sehat tidak dibunuh oleh log rusak.
- **Lapisan di atas cap:** budget neuron akun — `cp.generate` abort SEBELUM spend bila neuron terpakai hari itu (UTC) di gabungan lane claim+serve > 9.000 (`cloudflare_provider.py:99-119, 149-157`).
- **Kelemahan hitungan:** `_log_usage` menelan `OSError` (hanya print ke stderr, `cloudflare_provider.py:133-138`) sementara generasi tetap dikembalikan sebagai sukses — generasi yang gagal tercatat = tidak terhitung cap. Hitungan juga berbasis record selesai, bukan reservasi; tidak ada pengaman konkurensi antar-proses di kode ini (asumsi kerja: serve tunggal, konkurensi job klien 1).

### 3.2 Veto READY_CMD: murni lookup file (`cloudflare_serve_ready.py:29-44`)

- `trued` menjalankan ini di langkah bid dalam jendela ±10 dtk (docstring `ready.py:1-9`). Implementasinya: baca stdin, parse JSON (gagal parse → payload `{}`), kumpulkan SEMUA string rekursif dari payload (`_strings`, `ready.py:18-26`: str/dict/list/tuple), lalu cocokkan terhadap `cached_ids()`.
- `cached_ids()` (`common.py:132-137`) = himpunan nama file `*.txt` di `cache_dir()` tanpa ekstensi — **isi file tidak dibaca sama sekali**.
- Ada string payload yang persis sama dengan salah satu id cache → print "jawaban siap" + **exit 0** (bid jalan). Tidak ada → exit 1 = **bid diveto (skor 0)**. Jadi Expert tidak bisa memenangi pekerjaan yang jawabannya belum disiapkan — sesuai desain §39. Nol jaringan, nol generasi.
- **Batas veto yang harus diketahui:** (a) pencocokan tidak terikat field — string APA PUN di payload yang kebetulan sama dengan nama file cache memicu exit 0; (b) file `.txt` KOSONG tetap masuk `cached_ids()` → READY bisa meloloskan bid padahal `read_cache` akan None dan provider terpaksa fallback; (c) tidak ada cek kesegaran — cache basi lintas hari tetap meloloskan; (d) tidak ada re-validasi sendable — READY memercayai bahwa hanya prepare-tergerbang yang menulis cache (benar untuk kode prepare saat ini, tapi tidak ditegakkan di titik READY).

---

## 4. Dry-run / smoke offline TANPA mengambil job nyata

Tiga cara aman, semuanya sudah diverifikasi jalan di audit ini:

1. **Suite smoke bawaan (paling lengkap, sepenuhnya offline):**
   `cd ~/workspace/research/dialectica/provider && python3 test_cloudflare_serve.py`
   - `cp.generate` di-stub in-process (`fake_generate_factory`, test `:175-188`); generasi "gagal di gerbang tertutup" memakai `exploding_generate` yang meledak bila gerbang bocor.
   - Log pemakaian + cache diarahkan ke direktori temp via `ServeWorld` (test `:146-172`: env `DIALECTICA_TOKEN_USAGE_LOG` + `DIALECTICA_SERVE_CACHE_DIR`, `cp.USAGE_LOG` di-patch) — log/cache produksi tidak tersentuh.
   - `run_serve` hanya dipanggil dengan `--dry-run` atau ke jalur refusal (exit 5/6); supervisor diuji melawan proses `sleep`, bukan `trued`.
   - Hasil eksekusi 2026-11-13: **ALL PASS (25/25)**, exit 0 — mencakup screen Kelas-2, cap edge 8/9/10, cache hit/miss, correction bypass, fallback withheld (exit 1 + stdout kosong), veto READY, dry-run, refusal exit 5/6, dan SIGINT supervisor.
2. **Dry-run launcher saja:**
   `python3 run_serve.py --cloudflare-serve --dry-run [argumen serve]`
   Mencetak `DIALECTICA_PROVIDER_CMD / PREPARE_CMD / READY_CMD`, hitungan generasi hari ini vs cap, dan argv `trued serve` yang AKAN dieksekusi, lalu exit 0 — tanpa fetch kredensial, tanpa spawn (`run_serve.py:176-189`). Eksekusi audit ini: count **0/10**, exit 0.
3. **Yang TIDAK offline-aman (jangan dipakai sebagai "smoke"):**
   - `run_serve.py --cloudflare-serve` TANPA `--dry-run` = menyalakan `trued serve` sungguhan.
   - Menjalankan `cloudflare_serve_prepare.py` / `cloudflare_serve_provider.py` langsung dengan env/cache asli = generasi jaringan sungguhan (prepare pada baris lolos) atau pipeline live (provider pada cache miss). Untuk uji manual kedua skrip itu, wajib stub `cp.generate` + set env log/cache temp seperti pola `ServeWorld` di suite tes.
   - "Live never-match smoke" yang disebut docstring tes (`test_cloudflare_serve.py:20-21`) adalah langkah terpisah yang terawasi — TIDAK dijalankan di audit ini dan tidak diperlukan untuk menjawab pertanyaan §39.

---

## 5. Kesimpulan untuk keputusan sesi utama

1. Untuk tembakan yang berjalan **prepare → READY hit → provider cache hit, job_kind bukan correction**, cacat struktural one-shot (§1.5 KULIT-2: draf digerbang ≠ draf terkirim) **tertutup oleh konstruksi**: teks yang dinilai gerbang adalah teks yang ditulis ke cache, dan provider jalur utama tidak punya jalur generasi sama sekali. Sisa deviasi: `+"\n"` di stdout provider.
2. Jaminan itu **bukan kriptografis dan bukan versioned**: kunci cache hanya isrId, tanpa hash/TTL/lock. Disiplin operasional yang menjaga jaminan = cache dir yang sama untuk prepare & provider, tidak ada penimpaan manual, dan isrId env yang benar.
3. Fallback adalah pengecualian yang disadari pembuatnya, digerbang ulang penuh, tapi membawa dua harga: job dropped bila ditahan, dan **lubang cap** (hingga +2 generasi di atas cap per kedatangan fallback, hanya direm budget neuron 9.000). Bila jalur ini kelak dinyalakan, dua titik perbaikan terkecil yang ditunjuk audit ini: (a) cek `serve_generations_today()` + hormati sisa cap (`allow_regen` bersyarat) di awal `cloudflare_serve_provider.main()`; (b) READY menolak file cache kosong (selaraskan dengan semantik `read_cache`).
4. Audit ini tidak mengubah vonis rezim: STOP TOTAL tetap urusan keputusan sesi utama/user; kode §39 sendiri, pada jalur utamanya, terbukti melakukan apa yang diklaimnya.

*Ditulis 2026-11-13. Nol file kode diubah; satu-satunya artefak eksekusi = output tes offline (temp) + dry-run read-only di atas.*
