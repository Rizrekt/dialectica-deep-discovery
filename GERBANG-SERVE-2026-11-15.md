# GERBANG KUALITAS JALUR SERVE — Dialectica

**Tanggal:** 2026-11-15 (persiapan lab Senin 2026-11-16)
**Status serve sesudah tugas ini: TETAP OFF** — terverifikasi di akhir: `systemctl is-active dialectica-serve` = inactive, unit = not-found, `provider/serve.pid` tidak ada, 0 proses `run_serve`/`trued serve`. Tugas ini membangun remnya; tidak ada serve yang dinyalakan, tidak ada klaim/answer live, tidak ada ambang/config Expert/kill-metric yang diubah (ambang K-2 tetap 0,30).

**Pemicu:** falsified serve f0bb3586 (14 Nov 08:09, MEKANISME §82) — jalur serve Vyce mengirim jawaban TANPA gerbang apa pun: thinking-trace 38.591 karakter, 0 URL, 0 sitasi, 557 angka tak terikat, lolos terkirim dan difalsifikasi dalam ±85 detik. Jalur klaim one-shot punya wrapper gerbang penuh; jalur serve tidak. Celah struktural kedua dari §82: 11/11 jawaban serve pagi itu mendarat di pertanyaan yang ronde maratonnya SUDAH berakhir (`marathonEligible=false`, upside $0, downside penuh) karena tidak ada verifikasi liveness target.

---

## 1. Desain gerbang per lapis

Satu modul bersama: **`provider/serve_gate.py`** — dipakai kedua jalur serve (Vyce + Cloudflare §39). Prinsip: **tidak ada standar kedua** — gerbang isi adalah wrapper klaim itu sendiri, dipakai ulang verbatim; yang ditambahkan hanya lapis yang di jalur klaim disediakan oleh operator manusia.

### Lapis 1 — LIVENESS target (baru, serve-spesifik)

`serve_gate.liveness_check(detail)` — filter tiga-field dari KULIT-SISTEM-2026-11-14 edge #2 atas detail ISR (`/api/node/isr/<id>`):

- **LIVE** hanya bila: (i) ada ronde di `marathonEligibleIsos[]` dengan `endsAt` masih di masa depan (ini juga mencakup ronde BARU di pertanyaan yang `marathonConcluded=true` — bukan diblokir membabi buta), ATAU (ii) pertanyaan tanpa dimensi maraton yang statusnya masih terbuka (`in_progress`/`open`).
- **MATI**: pola flag basi §82 (`marathonActive=true` + `marathonConcluded=true` + semua `endsAt` lewat); pertanyaan `settled` tanpa ronde live; pertanyaan maraton tanpa satu pun `endsAt` masa depan yang bisa ditunjukkan (**fail-closed**); detail tidak tersedia (**fail-closed**).

Pengambilan detail: `serve_gate.fetch_isr_detail()` — tri-state (`ok`/`failed`/`disabled`), hanya menyentuh jaringan bila launcher meng-arm dengan env `DIALECTICA_SERVE_GATE_FETCH=1` (di-set `run_serve` untuk KEDUA mode serve). Kegagalan fetch ditangkap sebagai data (klien `trued.call` exit-on-error), bukan crash.

**Asimetri yang disengaja** (doktrin §39: selesaikan pekerjaan yang sudah diterima; gerbang struktural ada di prepare, sebelum klaim):

| Titik | Fetch gagal/disabled | Detail terbukti mati |
|---|---|---|
| Prepare (belum ada job; pass-over gratis) | **fail-closed penuh**: fetch gagal = skip; disabled = vonis dari field baris pencarian sendiri (baris masih bisa membuktikan kematian) | skip |
| Fallback provider (job sudah ada) | lanjut + peringatan (menjatuhkan job karena fetch tak terverifikasi = membakar reliabilitas tanpa bukti) | **blokir**: exit 1, stdout kosong |

### Lapis 2 — Deteksi THINKING-TRACE (baru, serve-spesifik)

`serve_gate.detect_thinking_trace(text)` → satu finding severity `THINKING-TRACE`, span None (= unpatchable dalam semantik sendable jalur yang sudah berlaku → draf ditahan utuh). Empat keluarga sinyal, satu saja cukup — masing-masing adalah sifat yang tidak dimiliki jawaban jadi:

1. **Pembuka jejak penalaran** — blok pertama mulai dengan monolog proses ("Let me think about this task carefully.", "let me analyze…", "hmm, let me…").
2. **Monolog ketidakpastian orang-pertama** — ≥2 penanda distinct ("i genuinely don't remember", "i don't recall", "i really can't reproduce", "i'm not sure", …).
3. **Dump kode mentah dominan** — ≥15 baris mirip kode DAN ≥30% dari baris tak-kosong DAN tanpa struktur `##` bernomor (jawaban terstruktur yang sah kebal lewat syarat terakhir).
4. **Penutup rencana-bukan-jawaban** — blok terakhir berupa rencana ("Decision: I will structure…", "I will now write/draft…", "my plan is…", padanan Indonesianya).

Deteksi berjalan atas teks FINAL (sesudah citation patch) — teks yang persis akan dikirim.

### Lapis 3 — Isi: wrapper klaim verbatim (standar yang sama, bukan standar kedua)

`serve_gate.gate_answer(text, regen_fn)` membungkus `openrouter_wrapper.wrap_answer` persis seperti jalur klaim:

- normalisasi mojibake → length guard (lantai 4.500 kar, maks 1 regenerasi) → audit angka/sitasi + citation patch;
- **lantai mekanik §45/T12** sebagai finding FLOOR span-None: K-1(a) URL ≥1; K-1(b) kepadatan sitasi ≥0,5/1.000 kar; **K-2 rasio angka terikat ≥0,30 (ambang TIDAK diubah — U2 wilayah lab)**; diukur atas teks sesudah patch;
- skor rubrik (a)–(g) termasuk gerbang format/struktur 4A yang bisa dicek mekanis di (g);
- **semantik sendable identik jalur klaim**: `status == "OK"` DAN nol finding audit yang bertahan (finding apa pun = tidak sendable — konservatisme fail-closed §35/§37 yang disengaja) DAN `(g) == LOLOS` — kini dihitung atas finding yang SUDAH digabung lapis trace.

### Lapis 4 — Self-VFP semantik: TIDAK diklaim, dinyatakan jujur

Di jalur klaim, self-VFP semantik (T10.2 / T12 butir 5) **bukan** panggilan model di dalam wrapper — ia penilaian agen operator dalam workflow hunt: buka setiap sitasi, tunjuk kalimat pendukung per klaim terikat. Serve berjalan unattended, tanpa agen di lingkaran, jadi titik ini **tidak bisa dibuat setara secara mekanis** dan gerbang ini tidak berpura-pura bisa:

- setiap hasil `gate_answer` membawa `gate.semantic_vfp = {performed: False, mode: "not-performed-mechanical-only"}` — tertulis di kode dan di logika, bukan hanya di laporan ini;
- `gate_answer` menerima parameter `semantic_check` (callable) sebagai titik pasang: tahap semantik yang disetujui lab nanti bisa dipasang tanpa redesign. Saat ini **sengaja dikosongkan**.

---

## 2. Titik pasang

### Jalur Cloudflare §39 (sudah ber-hook; gerbang ditanam di dalamnya)

| File | Perubahan |
|---|---|
| `cloudflare_serve_common.py` | `serve_pipeline()` kini lewat `serve_gate.gate_answer` (dulu `wrap_answer` + hitung sendable lokal) — semantik identik + lapis trace. |
| `cloudflare_serve_prepare.py` | `prepare_row(row, detail_fetcher=...)`: langkah liveness SESUDAH layar Kelas 2, SEBELUM cek cap + generasi. Target mati/fetch gagal = pass-over, nol generasi. |
| `cloudflare_serve_provider.py` | Fallback: blokir proven-dead SEBELUM gerbang cap + pipeline live. Jalur cache-hit tidak berubah. |
| `run_serve.py` (`_run_cloudflare_serve`) | Env `DIALECTICA_SERVE_GATE_FETCH=1` di launch + tercetak di dry-run. |

### Jalur Vyce serve (sebelumnya TANPA hook sama sekali — dicerminkan ke arsitektur §39)

| File | Peran |
|---|---|
| `vyce_serve_common.py` (baru) | Pipeline serve Vyce: generasi = subprocess `vyce_provider.py` (mesin klaim yang sama persis, termasuk steering via `DIALECTICA_ISR_ID`, timeout 1.200 dtk) → `gate_answer`. Cache memakai direktori serve-cache yang sama dengan §39 (kedua jalur tidak pernah jalan bersamaan — aturan pensiun §39). |
| `vyce_serve_prepare.py` (baru) | `DIALECTICA_PREPARE_CMD`: sanity baris → **liveness fail-closed** → generasi → gerbang → cache. Tanpa saringan Pioneer viso-0: cakupan serve Vyce historis adalah maraton dari poller kata kunci; mempersempitnya = keputusan lab, bukan tugas ini. Tidak ada cap 10 §39 ditambahkan ke Vyce (wilayah terkunci — lihat §4). |
| `vyce_serve_ready.py` (baru) | `DIALECTICA_READY_CMD`: memakai hook ready §39 itu sendiri (semantik + cache yang sama; implementasi kedua hanya akan jadi tempat semantik menyimpang). |
| `vyce_serve_provider.py` (baru) | `DIALECTICA_PROVIDER_CMD` saat job: cache-hit dicetak; fallback (koreksi skema / tanpa prepare) = blokir proven-dead → generasi prompt job asli → gerbang → cetak, atau exit 1 stdout kosong. |
| `run_serve.py` (main) | Mode serve Vyce saja yang di-wire: `PROVIDER_CMD`/`PREPARE_CMD`/`READY_CMD` menunjuk trio di atas + `DIALECTICA_SERVE_GATE_FETCH=1` + baris log "gated Vyce serve". Mode `--answer` Vyce **tidak berubah sama sekali** (terbukti tes runserve di bawah). |

**Jalur klaim tidak disentuh perilakunya** — tidak ada file provider klaim yang diubah; satu-satunya file bersama yang berubah adalah `cloudflare_serve_common.serve_pipeline` (fungsi khusus-serve).

Cadangan: `cloudflare_serve_common.py.bak-20261115`, `cloudflare_serve_prepare.py.bak-20261115`, `cloudflare_serve_provider.py.bak-20261115`, `run_serve.py.bak-20261115`. `py_compile` bersih untuk 9 file baru/diubah + file tes.

---

## 3. Hasil tes (semua dijalankan 2026-11-15, generasi + fetch di-stub, nol serve diluncurkan)

### Suite baru — `test_serve_gate.py`: **37/37 LULUS**

- **Liveness (14):** flag basi → MATI; concluded + ronde baru (endsAt masa depan) → LIVE; pertanyaan terbuka tanpa maraton → LIVE; settled tanpa ronde → MATI; maraton tanpa endsAt terbukti → MATI fail-closed; detail None → MATI; gate-for-row: stale ter-arm → tutup, live ter-arm → buka, fetch gagal → tutup fail-closed, baris membuktikan mati (unarmed) → tutup, baris terbuka (unarmed) → buka; fallback: proven-dead → alasan blokir, live → tanpa blokir, fetch gagal → TANPA blokir (asimetri terdokumentasi).
- **Detektor trace (4):** rekonstruksi pola f0bb3586 dari kutipan §82 (pembuka "Let me think…" + monolog "I genuinely don't remember / I don't recall / I really can't reproduce" + penutup "Decision: I will structure…") → terdeteksi (3 keluarga sinyal dalam 1 finding); fixture klaim bersih → 0 finding; dump kode dominan → terdeteksi; penutup rencana saja → terdeteksi.
- **Gerbang (5):** fixture bersih jalur klaim (`good_text()`) → sendable True; self-VFP dilaporkan `performed: False`; **kasus kontrol**: fixture yang sama diberi pembuka trace + penutup rencana LOLOS wrapper polos (status OK, 0 finding, (g) LOLOS) tetapi **DITAHAN oleh lapis trace** di `gate_answer` — membuktikan lapis inilah yang menghentikan spesies f0bb3586; draf 0-URL → ditahan lantai K-1(a) (finding `LANTAI K-1(a)`, plus K-1(b)/K-2).
- **Prepare Cloudflare ter-arm (4):** target stale → pass-over, **0 generasi**; fetch gagal → pass-over, 0 generasi; target live → exit 0 + cache tertulis; draf trace → pass-over, cache kosong.
- **Prepare Vyce (3):** stale → pass-over tanpa generasi; trace → pass-over tanpa cache; live + bersih → exit 0 + cache tertulis.
- **Provider (5):** Vyce cache-hit → teks cache; Vyce fallback proven-dead → exit 1, stdout kosong, 0 generasi; Vyce fallback bersih → exit 0; Vyce fallback trace → exit 1, stdout kosong; Cloudflare fallback proven-dead → exit 1, stdout kosong, 0 generasi.
- **run_serve (2):** dry-run serve Vyce menampilkan wiring hook + `DIALECTICA_SERVE_GATE_FETCH`; dry-run `--answer` Vyce TIDAK menampilkan hook serve apa pun (jalur klaim utuh).

### Regresi — semua suite lama tetap lulus, tanpa diubah

| Suite | Hasil |
|---|---|
| `test_cloudflare_serve.py` | **33/33** |
| `test_cloudflare_claim_path.py` | **8/8** |
| `test_openrouter_claim_path.py` | **10/10** |
| `test_openrouter_wrapper.py` | **30/30** |
| `test_dashscope_claim_path.py` | **11/11** |
| `test_zai_claim_path.py` | **13/13** |

**Total keseluruhan: 142/142 cek lulus.** Kompatibilitas tes lama dijaga oleh desain fetcher: tanpa env arming dari launcher, fetcher berstatus "disabled" (nol panggilan jaringan) sehingga perilaku lama persis utuh.

---

## 4. Sisa risiko (jujur)

1. **Self-VFP semantik TIDAK terpasang.** Gerbang ini mekanis saja: lantai K-1/K-2 + audit angka/sitasi + trace + format. Klaim jalur klaim #1 dulu lolos semua ambang mekanis dan mati di dukungan semantik — spesies kegagalan itu **masih bisa lolos gerbang serve ini**. Inilah risiko sisa terbesar dan alasan serve tidak boleh hidup hanya bermodal gerbang ini tanpa keputusan lab.
2. **Rubrik (h)/(i) tidak dinilai mekanis** — tetap wilayah verdict-watch seperti di jalur lain; gerbang tidak menilainya.
3. **Fallback provider hanya memblokir yang TERBUKTI mati.** Job yang tiba tanpa prepare (assigned di luar jalur poll) dengan fetch gagal tetap diselesaikan lewat pipeline live tergating — pilihan reliabilitas yang disengaja; perlindungan strukturalnya adalah prepare.
4. **Detektor trace bersifat pola, bukan pemahaman.** Varian monolog dengan kosakata lain bisa lolos keluarga sinyal saat ini; sebaliknya draf sah yang sangat tidak lazim bisa kena (mitigasi: syarat dump kode menuntut dominasi + tanpa struktur; monolog menuntut ≥2 penanda). Perluasan pola = pekerjaan lab dengan korpus nyata.
5. **Liveness bergantung pada field detail ISR** (`marathonEligibleIsos[].endsAt`) sesuai sampel hunt yang terverifikasi; bila skema API berubah, cabang fail-closed menutup prepare (aman, tapi serve bisa mati total tanpa bunyi selain baris pass-over "gerbang liveness" di log prepare).
6. **Cap serve 10/hari §39 tidak dicerminkan ke Vyce** — di luar cakupan tugas ini dan menyentuh wilayah keputusan terkunci; serve Vyce yang hidup lagi tanpa cap adalah paparan bakar yang harus diputuskan lab secara eksplisit.
7. **Fetch liveness menambah 1 panggilan API per baris prepare** (timeout 30 dtk, di dalam jendela prepare klien s/d 3.600 dtk) — biaya latensi per pertanyaan, bukan per job.

---

## 5. KEPUTUSAN YANG DIMINTA DARI LAB (syarat serve boleh hidup lagi)

1. **Semantik:** apakah serve boleh jalan dengan gerbang mekanis saja (menerima risiko sisa #1 secara tertulis), atau wajib ada tahap self-VFP dulu — dan bila wajib, bentuknya apa (panggilan model penilai dengan cap bakar tertulis, atau serve semi-otomatis dengan tinjauan agen)? Titik pasangnya sudah tersedia (`semantic_check` di `gate_answer`).
2. **Jalur mana yang hidup:** Vyce (kini tergating penuh), Cloudflare §39 (tergating + cap), atau tetap keduanya bergantian sesuai aturan pensiun §39?
3. **Cap bakar Vyce:** apakah serve Vyce perlu cap generasi harian seperti §39 (10/hari), dan angkanya berapa?
4. **Ambang U2 (K-2)** tetap berlaku juga sebagai lantai serve — konfirmasi tidak ada ambang khusus-serve.
5. **Uji live pertama:** serve perdana pasca-gerbang dijalankan terawasi (satu jendela poll, log prepare/provider dibaca baris demi baris, jawaban pertama diperiksa manual sebelum serve dibiarkan unattended) — dan kill-metric serve tetap berlaku atas hasilnya.
6. **Korpus trace:** kumpulkan draf serve nyata (lolos + falsified historis) sebagai korpus uji detektor sebelum mengandalkan pola saat ini.

---

*File terkait: `provider/serve_gate.py`, `provider/vyce_serve_common.py`, `provider/vyce_serve_prepare.py`, `provider/vyce_serve_ready.py`, `provider/vyce_serve_provider.py`, `provider/test_serve_gate.py`; cadangan `*.bak-20261115` untuk 4 file yang diubah.*
