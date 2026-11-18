# PERBAIKAN PENGHAMBAT — 2026-11-17 (Paket fase testing, perintah user 04:27)

Urutan wajib 1 → 3 → 2 → 4 dipatuhi. Nol submit/answer/claim; nol perubahan
config Expert/cron/cap/kill-metric. Semua panggilan model free ($0).
Backup kode: `provider/serve_gate.py.bak-20261117-blockfix`,
`provider/test_serve_gate.py.bak-20261117-blockfix` (Langkah 1) +
`provider/serve_gate.py.bak-20261117-c5` (Langkah 3).

**Suite tes — sebelum paket: 204/204. Sesudah paket: 213/213.**
Per berkas (sebelum → sesudah): test_cloudflare_claim_path 8/8 → 8/8 ·
test_cloudflare_serve 33/33 → 33/33 · test_dashscope_claim_path 11/11 → 11/11 ·
test_improve_20261116 17/17 → 17/17 · test_openrouter_claim_path 10/10 → 10/10 ·
test_openrouter_wrapper 30/30 ("GAGAL: tidak ada") → sama ·
test_semantic_check 34/34 → **40/40** · test_serve_gate 48/48 → **51/51** ·
test_zai_claim_path 13/13 → 13/13.

**Bahan bakar awal paket:** kuota OpenRouter terverifikasi sisa **1**
(`orp.quota_remaining()`) — lane pemeriksa OpenRouter menolak sendiri bila
sisa <2, jadi seluruh pemeriksaan paket ini berjalan di lane Vyce; panggilan
OpenRouter yang terbakar selama paket = **0**.

---

## LANGKAH 1 — Bug thinking-trace "decision:" DIPERBAIKI

**Diagnosis.** Di `provider/serve_gate.py`, regex `_TRACE_PLAN_CLOSING`
memuat alternatif telanjang `decision\s*:` yang diterapkan ke blok penutup
draf. Kalimat sintesis yang DIWAJIBKAN kontrak serve memuat frasa
"…as a single design decision: the same carve-out…" → `decision:` tertembak
→ draf 1 dry-run (ISR `8a4e9623`, 8.390 kar) ditahan sebagai kebocoran trace
padahal isinya sintesis sah.

**Perubahan** (serve_gate.py): alternatif telanjang `decision\s*:` dibuang
dari `_TRACE_PLAN_CLOSING`; ditambah dua pola sempit yang diperiksa di
`detect_thinking_trace` atas blok penutup saja:
- `_TRACE_DECISION_LABEL` — "Decision:" hanya di posisi label (awal
  baris/blok, boleh di belakang markdown `>`/`#`/`-`/`*`).
- `_TRACE_DECISION_PLAN` — "decision:" diikuti bahasa rencana orang-pertama
  (i will/shall/plan to/am going to/i'll/my plan).

**Bukti tes dua arah** (test_serve_gate.py, 48 → 51 tes, semua lulus):
- (a) Blok sintesis PERSIS dari draf 1 (`DRAFT1_SYNTHESIS`, memuat kalimat
  *"It frames the lock and the dedicated marketplace as a single design
  decision: the same carve-out that enables trading is what blocks
  third-party venues."*) → `detect_thinking_trace` = 0 temuan, LOLOS.
- (b) `DECISION_PLAN_MID` ("Decision: I shall organize…") tertangkap;
  `DECISION_LABEL_LOWER` ("decision:" di awal baris) tertangkap; fixture
  lama SPECIMEN/PLAN_ONLY tetap tertangkap.

**Gate ulang atas teks draf 1 tersimpan** (tanpa generasi baru):
sebelum = sendable False, 1 temuan trace → **sesudah = status OK, (g) LOLOS,
audit findings 0, sendable=True**.

**Vonis: SELESAI, terbukti dua arah.**

## LANGKAH 3 — Pemeriksa C5 stabil di draf raksasa + ramalan dituntaskan

**Diagnosis.** 5 item ramalan ronde 1 unavailable. Penyebab terukur: pemeriksa
Nemotron via Vyce (`nemotron-3.5-super-vl`) membakar budget di
`reasoning_content` (25–33 rb kar) → konten kosong → lane gagal; lane
OpenRouter terhalang kuota sisa 1 < 2 (4 item) / balasan tak terparse (1
item). Draf ke-5 item: 39.070–42.261 kar.

**Perubahan** (serve_gate.py): `_SEMANTIC_SEGMENT_CHARS = 10000`;
`_split_draft_segments` (pecah di batas blok; segmen = substring persis draf;
blok raksasa dipotong keras); `_sources_tail` (seksi Sources draf, cap 4.000
kar) ditempel ke tiap segmen supaya sitasi ekor tidak memicu S-1 palsu;
`build_semantic_prompt(segment_note=...)`; `_run_semantic_segments`
menggabungkan temuan lintas segmen — kutipan tetap diverifikasi terhadap
draf UTUH; hasil kini memuat `segments`/`segments_ok`; gagal sebagian
tercatat di `error`; unavailable hanya bila SEMUA segmen gagal. 6 tes mock
baru → test_semantic_check 34 → 40/40.

**Ronde 2 atas 5 item** (pemeriksa Vyce-first, mode shadow; hasil mentah di
`dryrun-2026-11-17/ramalan22-round2-results.json` + `ramalan22-round2b-*.json`
+ `ramalan22-round2c-*.json`; sudah ditulis sebagai §6 di
RAMALAN-22-REVEALED-2026-11-17.md):

| Item | Draf (kar) | Segmen ok | Vonis | Kode (gabungan) | Waktu |
|---|---|---|---|---|---|
| 8671364d | ±39–42 rb | 4/5 | FATAL | CR ×1, A_CITATION ×11 (S-1 ×9) | 79,4 dtk |
| f18b1675 | ±39–42 rb | 2/5 | FATAL | A_CITATION ×3 (S-1 ×1) | 82,6 dtk |
| f5224761 | ±39–42 rb | 2/5 | FATAL | A_CITATION ×2, CR ×1 (S-1 ×1, S-4 ×1; dropped 1) | 75,9 dtk |
| f8801972 | ±39–42 rb | 0/5 → ulang 1/5 | FATAL | A_CITATION ×6 (S-4 ×5, S-1 ×1) | 85,6 dtk |
| f131675d | ±39–42 rb | 0/5 → ulang (5 rb asli) 1/9 | FATAL | A_CITATION ×4 (S-1 ×2, S-4 ×2) | 150,5 dtk |

**Agregat akhir 22/22 = 22 FATAL, 0 clean, 0 unavailable**; temuan gabungan
93 (65 ronde 1 + 28 ronde 2). Proyeksi dent diperbarui di RAMALAN §6: lunak
−13,8788 · tengah ±−15,88 · keras literal −23,8788.

**Kegagalan di tengah jalan, dilaporkan apa adanya:** (1) upaya pertama
berlabel "5 rb" sebenarnya mengulang konfigurasi 10 rb —
`_split_draft_segments` mengikat argumen default cap saat definisi fungsi,
jadi patch konstanta modul tidak berlaku; angka 5 rb yang asli hanya
f131675d (fungsi pembaginya di-patch langsung). (2) Service restart
menghapus /tmp termasuk run 2b pertama — f8801972/f131675d dijalankan ulang
dari workspace. (3) Diagnosis akhir: kolaps lane Vyce bersifat STOKASTIK per
panggilan (reasoning 26–33 rb kar), tidak murni digerakkan ukuran draf;
segmentasi mengubah gagal-total menjadi cakupan parsial (temuan per item =
lantai bawah; vonis fatal tetap sah karena ≥1 temuan terverifikasi).

**Vonis: SELESAI — ramalan tuntas 22/22; pemeriksa kini selalu menghasilkan
vonis atau cakupan parsial tercatat, bukan unavailable buta.**

## LANGKAH 2 — Penulis cadangan DIPUTUSKAN

Prompt uji = pertanyaan target dry-run (ISR `8a4e9623`) + SERVE_FORMAT_CONTRACT
persis seperti yang ditempel pipa produksi. Hasil mentah:
`dryrun-2026-11-17/step2-writers-results.json`.

| Kandidat | Hasil generasi | Gerbang | C5 |
|---|---|---|---|
| deepseek-v4.1 (Vyce, `call_vyce` langsung) | **HTTP 403** — `{"error":{"message":"This model requires lite tier or higher. Upgrade your account to access it.","type":"permission_error","code":"tier_required"}}` | tidak ada draf | — |
| Nemotron-Vyce (dari dry-run 03:48) | hidup tapi stub 531 kar mentah (final 1.380) | GAGAL-LANJUT lantai | FATAL 1 (A_CITATION/S-1, sah) |
| gpt-oss-120b (Cloudflare `generate`) | **8.032 kar mentah**, 188,09 neuron, 1 generasi (tanpa regen) | status OK, (g) LOLOS, final 8.005 kar, trace bersih; **sendable=False HANYA oleh lantai K-2: rasio 0,238 < 0,30 (10 dari 42 token angka terikat sitasi)** | **tidak terukur** — 2 percobaan unavailable (percobaan 1: balasan pemeriksa non-JSON; percobaan 2: reasoning pemeriksa meluap 29.787 kar → konten kosong; lane OpenRouter terkunci kuota 1) |

**Konflik deepseek TERPUTUS:** dari runtime/akun ini deepseek-v4.1 = 403
tier. Probe 02:44 yang membaca "rc=0" hampir pasti mengukur provider, bukan
modelnya: `vyce_provider` mencoba kandidat berurutan dengan GLM pertama —
probe level-provider sukses lewat GLM walau deepseek mati. Panggilan langsung
per-model adalah instrumen definitifnya. (Pola yang sama terlihat live di
Langkah 4: log provider mencetak 403 deepseek persis sesudah GLM kosong.)

**Vonis: penulis cadangan LAYAK = Cloudflare gpt-oss-120b** — panjang masuk
pita target (8.032 kar), bentuk lolos penuh, satu-satunya penahan adalah
lantai K-2 pada ambang 0,30 yang sedang dalam tinjauan U2 (pada 0,15 draf
ini lolos: 0,238 > 0,15 — dicatat sebagai fakta, keputusan U2 bukan wilayah
paket ini). Kelemahan terukur gpt-oss: angka-angkanya lebih longgar terikat
sitasi daripada GLM (0,238 vs draf GLM yang lolos lantai). C5 atas drafnya
belum terukur — utang ukur, bukan vonis buruk.

## LANGKAH 4 — Sampel draf sendiri ditambah (n=3)

Seleksi: sapuan explore-search 12 query topik inti (101 baris unik, 89
lolos filter kata kunci inti) → liveness tiga-field terpasang
(`liveness_gate_for_row`, fetch terpasang). Catatan kejujuran: kolom viso
tidak terbaca dari proyeksi baris yang dipakai runner ini (semua None) —
prioritas Pioneer viso-0 TIDAK bisa diterapkan terukur di langkah ini;
target dipilih dari yang LIVE + topik inti. Endpoint `/api/node/question`
untuk baca-balik field ternyata tidak ada (ENDPOINT_NOT_FOUND) — viso
kedua target = **tidak terukur**.

| # | Target | Pertanyaan (awal) | Generasi | Gerbang | C5 (shadow) |
|---|---|---|---|---|---|
| 1 | 8a4e9623 (dry-run 03:48) | NFT contract blocks transfers… | GLM 8.390 kar | OK, sendable=True (sesudah perbaikan Langkah 1) | **CLEAN** 0 temuan |
| 2 | 3b5c0f0c | How do zero-knowledge proofs reduce the cost of verifying cross-chain bridge… | GLM final 7.471 kar, audit 0, trace bersih | OK, **sendable=True** | **tidak terukur** — 2 percobaan, pemeriksa unavailable dua-duanya (reasoning meluap 31.207 lalu 29.015 kar) |
| 3 | 26cc93f2 | How does the effectiveness compare between the use of automated transaction simulation… | GLM final 7.682 kar, audit 0, trace bersih | OK, **sendable=True** | **CLEAN** 0 temuan |

**Percobaan yang gagal di tengah jalan:** target pertama sapuan,
3dd05619 (EIP-4844 blob fee market), generasinya GAGAL total — GLM membalas
kosong (reasoning 60.093 kar), fallback provider jatuh ke deepseek (403),
provider mati (`VyceGenerationError`, rc=1, stdout 0 kar). Target pengganti
26cc93f2 yang menutup sampel. Laju sukses generasi GLM berbentuk serve malam
ini: 2 dari 3 percobaan (yang gagal spesies reasoning-meluap yang sama
dengan kolaps pemeriksa).

**Tabel salah-fatal C5 di draf sendiri: 0 dari 2 yang terukur** (2 CLEAN,
1 tidak terukur). Angka penentu blocking bertambah dari n=1 menjadi n=2
terukur — masih kecil; syarat diskusi blocking belum kuat, dan 1 sampel
masih utang ukur karena lane pemeriksa, bukan karena drafnya.

## Panggilan per lane selama paket (rekap)

- Vyce GLM (generasi serve): 3 panggilan pipa (1 gagal kosong, 2 sukses);
  cap serve hari-UTC 2026-11-17 bergerak 1/10 → **3/10** (percobaan gagal
  tidak menaikkan cap).
- Vyce deepseek-v4.1: 2 panggilan (1 langsung Langkah 2, 1 fallback provider
  Langkah 4) — keduanya HTTP 403.
- Vyce Nemotron (pemeriksa C5): ronde 2 ramalan ±25 panggilan segmen + ±14
  panggilan pengulangan (jumlah persis **tidak terukur** — sebagian log run
  2b pertama hilang bersama /tmp) + 2 percobaan draf gpt-oss + 3 percobaan
  Langkah 4 (2 gagal, 1 sukses).
- OpenRouter: **0** panggilan terbakar (kuota tetap 1; lane menolak sendiri).
- Cloudflare gpt-oss-120b: 1 generasi = **188,09 neuron** (dari jatah free
  10.000/hari-UTC).

## Sisa utang yang paket ini TIDAK menutup

1. C5 atas draf gpt-oss-120b + draf 3b5c0f0c: belum terukur (lane pemeriksa
   Vyce stokastik kolaps; lane OpenRouter terkunci sisa kuota 1).
2. Pemeriksa C5 masih satu-satunya di Nemotron-Vyce untuk praktiknya —
   klausul jangan-bertumpu-satu-model berlaku juga ke PEMERIKSA, bukan
   cuma penulis; lane pemeriksa cadangan teruji berkala belum ada.
3. GLM sendiri kolaps stokastik saat generasi (1 dari 3 percobaan malam
   ini) — penulis utama pun tidak kebal spesies gagal yang sama.
