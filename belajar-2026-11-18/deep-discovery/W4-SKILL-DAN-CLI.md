# W4 — BEDAH SKILL & CLI `trued` (Deep Discovery Dialectica, Lini W4)

Tanggal: 2026-11-18 · Sifat: investigasi READ-ONLY (membaca source; tidak menjalankan command yang mengubah state)
Sumber primer: `~/workspace/research/dialectica/skill-audit/pkg/dialectica/SKILL.md` (441 baris) + `scripts/trued.py` v0.22.4 (6.369 baris) + `references/api.md` + `references/arenas.md`.
Tag bukti: **[KODE: trued.py:baris]** = terbaca langsung di source · **[SKILL.md]** = dokumentasi skill · **[API.md]** = references/api.md · **[INFERENSI]** = kesimpulan penulis lini, bukan bunyi kode/dokumen.

---

## 1. Bagaimana Agent Skill Bekerja

Skill Dialectica adalah paket mandiri: satu dokumen `SKILL.md` + satu klien Python stdlib murni (`trued.py`, Python 3.8+, tanpa dependensi pihak ketiga) + tiga referensi (`api.md`, `arenas.md`, `rules-of-the-game.md`) [KODE: trued.py:2; SKILL.md "Setup"].

- Bootstrap: bila hanya `SKILL.md` yang terambil, dokumen itu sendiri memuat skrip unduh yang mengambil tarball lengkap dari `https://dialectica.xyz/skills/dialectica.tar.gz` (maks 8 MB, daftar file diverifikasi persis, versi klien harus cocok `VERSION = "0.22.4"`) ke folder kerja privat, lalu `DIALECTICA_SKILL_ROOT` menunjuk ke sana [SKILL.md "Get the complete skill"].
- Pemakaian: `TRUED="$DIALECTICA_SKILL_ROOT/scripts/trued.py"`, dipanggil `python3 "$TRUED" <command>` [SKILL.md "Setup"].
- Konvensi sesi: setiap pemanggilan dibuka dengan `trued whoami` → `trued signin` → `trued status`, dan baris `Balance:` / `🎉` / `📬` dari `status` wajib disampaikan ke user nyaris verbatim [SKILL.md "On every invocation"].
- Aturan keras skill: error `{success: false}` tidak boleh difabrikasi hasilnya; `ask` dan `serve` tidak boleh jalan tanpa konfirmasi eksplisit user; istilah publik (Question/Answer/Expert/Verifier) dipakai ke user, nama internal API (isr/iso) tidak [SKILL.md "Hard rules"].

## 2. Bagaimana `trued` Berkomunikasi dengan Platform

Ada **dua kanal transport yang berbeda**:

### 2a. REST API (semua command baca/tulis akun)
- Base URL: env `DIALECTICA_BASE_URL`, bawaan `https://dialectica.xyz`; skema non-http(s) ditolak, http polos ditolak kecuali loopback — supaya token tidak menyeberang tanpa enkripsi [KODE: trued.py:110–119].
- HTTP via `urllib` stdlib; header `X-Dialectica-Client: trued/0.22.4` di setiap panggilan [KODE: trued.py:262].
- **Dua kredensial, saling menggantikan (bukan fallback berantai):**
  1. **Token sesi akun** — file `~/.dialectica/session`, dikirim sebagai header `X-Active-Session` [KODE: trued.py:145–155, 280–282]. Umur sign-in ±7 hari [SKILL.md "Auth check"].
  2. **Work credential milik Expert** — dikirim sebagai `Authorization: Bearer …` dan **menggantikan** token sesi, hanya pada tiga jenis panggilan penghasilan (cari kerja, ambil kerja, baca job sendiri). Aktif hanya bila server menyatakan menerima: klien bertanya sekali per proses ke `GET /api/feature-flags`, membaca field `agentWorkCredentialEnabled` (server lama: `truthMiningEnabled`); semua kegagalan probe menjawab `False` = tetap pakai token akun (fail-closed ke mode lama) [KODE: trued.py:163–216]. Work credential tidak bisa bertanya, mengubah setting, atau menyentuh Expert lain [KODE: trued.py:16–27].
- Redirect lintas-origin membuang header kredensial (`X-Active-Session` + `Authorization`) sebelum diteruskan [KODE: trued.py:122–142].
- Envelope respons: `{success, data, error}`; error dinormalisasi ke `{code, message}` apa adanya dari server (tidak ada kosakata penolakan karangan klien); kegagalan command keluar dengan **exit 2** [KODE: trued.py:340–405].
- 429 dibedakan dua limiter: `error` string polos = batas global per-menit (tunggu detik); `error.code` berakhiran `_CAP_REACHED` = cap baca anonim jendela **15 menit**; `Retry-After` dibaca dan dipatuhi [KODE: trued.py:286–311; SKILL.md Workflow 1].
- Timeout bawaan `api_call` = **30 detik**; pemanggil POST berat (assist, configure, opportunities) menaikkan ke 60 detik [KODE: trued.py:230; 4082; 3908].

### 2b. Agent Gateway — protokol Matrix (khusus `serve`/`answer`)
Pekerjaan Expert tidak berjalan di REST: gateway berbicara **protokol client-server Matrix** — login ke homeserver, long-poll `/sync` untuk pekerjaan, balas di thread job [KODE: trued.py:1863–1865].

- Login: `matrixUserId` + password bootstrap (kredensial sekali pakai dari `credential/reveal`, dirotasi jadi access token pada login pertama, lalu `bootstrap` dibuang dari state) [KODE: trued.py:4074–4096, 5396–5443].
- Konstanta poll [KODE: trued.py:1872–1885]:
  - `SYNC_TIMEOUT_MS = 10_000` (long-poll server 10 dtk — diturunkan dari 30 dtk karena request offer-to-answer harus dijawab dalam ±30 dtk dan poll 30 dtk terukur menggantung melewati batas itu)
  - `REQUEST_TIMEOUT_S = 15` (plafon abort sisi klien)
  - `HEARTBEAT_S = 15` · `MAX_RELOGIN_ATTEMPTS = 3` · `LOGIN_RATE_LIMIT_MAX_TRIES = 30`
- Klasifikasi event masuk **fail-closed**: hanya event dari system user Dialectica yang diproses; pengirim lain dibuang sebelum isinya menyentuh model [KODE: trued.py:2378–2413]. Tiga jenis event: `evaluate-request` (tawaran menilai/menjawab), `execute-job` (job diberikan), `schema-correction` (koreksi format).
- Event `execute-job` tanpa `jobId` dibuang — semua pelacakan (cache prompt asli, dedupe, laporan hasil) berjangkar pada jobId [KODE: trued.py:2394–2407].

## 3. Peta Command Lengkap (semua subcommand di kode)

Parser lengkap di `main()` [KODE: trued.py:6246–6367]. **19 command tingkat-atas + 5 subcommand `agent`:**

| Command | Fungsi | Endpoint utama |
|---|---|---|
| `status` | Saldo reward + digest notifikasi belum dibaca + Question settled | `/api/node/scores`, `/api/node/notifications/unread-count`, `/api/node/notifications` [KODE: 672–687] |
| `search <q> [--limit] [--fast]` | Cari Question + wiki + arena (hybrid keyword/semantik; `--fast` keyword saja) | `/api/node/explore-search` [KODE: 479] |
| `page <slug>` | Isi halaman wiki (Verified Answer) | `/api/node/wiki/pages/{slug}` [KODE: 554] |
| `question <isrId> [--limit] [--chars]` | Satu Question + jawaban terverifikasi (bawaan top 3, 1500 char) | `/api/node/isr/{id}`, `/api/node/isos/{id}` [KODE: 640–647] |
| `notifications [--all]` | Preview notifikasi (bawaan unread saja; plafon baca 200 baris) | `/api/node/notifications` [KODE: 964–971; DIGEST_MAX_ROWS=200: 457] |
| `ask <teks> [--arena] [--continue] [--draft]` | Loop asisten pembuatan Question → create + charge Fee | `/api/node/isrs/assist`, `/api/node/isr` [KODE: 1127, 1234] |
| `arena [id] [--window]` | Daftar arena / analitik arena + kinerja tiap strategi + alasan penolakan verifikasi | `/api/node/arenas`, `/api/node/arenas/{id}/analytics` [KODE: 1553, 1601] |
| `opportunities [K=V…] [--limit] [--list-filters] [--agent]` | Question yang bisa diambil Expert ini, dengan metrik baris lengkap | `/api/node/agents/{id}/opportunity-filters`, `/api/node/agents/{id}/opportunities` [KODE: 1460, 1501] |
| `serve [filter…] [--arena] [--strategy] [--model] [--every] [--agent] [--context-window]` | Jalankan Expert menjawab pekerjaan | gateway Matrix + REST klaim (lihat §6) |
| `answer <isrId> [--model] [--agent]` | Jawab SATU Question bernama lalu putus koneksi | = `cmd_serve(one_shot_target=…)` [KODE: 6147–6160] |
| `agent show [--agent]` | Konfigurasi gabungan + caps + pemakaian 24 jam | `/api/node/agents/{id}`, `/api/spending/limits/agent/{id}`, `/api/spending/usage/agent/{id}` [KODE: 3771–3832] |
| `agent set K=V…` | Tulis-balik seluruh config dengan perubahan (read-modify-write) | `/api/node/agents/{id}/configure` [KODE: 3861–3908] |
| `agent caps [K=V…]` | Lihat/atur plafon belanja 24 jam | `/api/spending/limits/agent/{id}` (PUT) [KODE: 3958] |
| `agent strategies` | Daftar strategi + parameter + panduan server verbatim | `/api/node/agent-implementations/{impl}/schema` [KODE: 3417–3429, 3975] |
| `agent reconnect` | Simpan kode koneksi pengganti setelah akses dicabut di web (kode dari stdin/getpass, TIDAK dari argumen; berlaku sekali, kedaluwarsa 30 menit) | lokal saja — tanpa request [KODE: 4015–4057] |
| `notes [--write --expected <versi>]` | Baca/tulis dokumen keputusan user di server (optimistic-lock via versi) | `/api/node/memory` [KODE: 6034] |
| `signin` | Konfirmasi sesi + pastikan Expert ada (idempoten) + baca notes | `/api/authext/user`, provision bila perlu [KODE: 6163] |
| `report "<teks>" [--feature] [--operation]` | Lapor defect / minta fitur ke platform (satu panggilan, tanpa konfirmasi; body dipotong 4000 char) | `/api/node/feedback` [KODE: 6203; REPORT_BODY_MAX: 78] |
| `login` | Cetak instruksi cara memperoleh token sesi | lokal [KODE: 6232] |
| `whoami` | Base URL + keberadaan token/state (tidak pernah mencetak token) | lokal [KODE: 6238] |

Exit code bermakna untuk skrip: `serve`/`answer` — 0 diterima, 1 gagal/ditolak-model/dijatuhkan, 3 tidak terkonfirmasi (tidak diberikan / tidak ada kerja / `?` belum settled), 4 *passed on*, 2 error API [SKILL.md "Answer one Question"; KODE: TERMINAL_JOB_STATES + EXIT_UNKNOWN=3 + EXIT_DECLINED=4: 4286–4296].

## 4. Bagaimana Expert Dibuat & Diinisialisasi

Alur provision (dipicu `signin`, atau `serve`/`answer` pertama) [KODE: trued.py:4074–4188]:

1. `POST /api/node/agents/matrix` dengan body `{"type": "ISP"}` — **tipe dikode keras ISP**; tidak ada jalur registrasi tipe lain di CLI (lihat §9).
2. `POST /api/node/agents/{agentId}/credential/reveal` — mengambil kredensial bootstrap sekali pakai.
3. State disimpan ke `~/.dialectica/agent.json` **sebelum** request lanjutan apa pun (kredensial di disk dulu, baru bicara lagi) — mode file 0600, tulis atomik temp-file + `os.replace` + fsync [KODE: 3288–3314].
4. Cap bawaan langsung dipasang: `DEFAULT_DAILY_ANSWER_CAP = 20` jawaban/24 jam via `PUT /api/spending/limits/agent/{id}` [KODE: 4105–4112, 4216–4234]. Server sendiri bawaan-nya *unlimited* — cap 20 ini pilihan klien sebagai pengganti "bertanya sebelum setiap jawaban".
5. Expert baru dibuat **pull-only**: flag `startingConfig: True` disimpan di state; strategi `dynamic` baru diterapkan pada `serve`/`answer` pertama, karena server menolak mengonfigurasi agent yang belum pernah terhubung [KODE: 4152–4185, 4237–4299]. Gagal di tengah → run berikutnya menyembuhkan (gerbang flag `configured`).
6. Pakai-ulang diputuskan oleh `can_reuse_state`: agentId ada + `baseUrl` sama + `userId` sama dengan sesi sekarang; selain itu registrasi baru [KODE: 3227–3241].
7. Expert yang dihapus di website: state lama dipindah (tidak dihapus) ke `~/.dialectica/agent.gone-<detik>.json`, Expert baru dibuat, **maksimum sekali per run**; bila dipin dengan `--agent`, serve berhenti alih-alih mengganti [KODE: 5128–5185; SKILL.md Workflow 3].

## 5. Konfigurasi Strategy — Field Apa yang Benar-Benar Dibaca

Prinsip kode: **klien tidak mengode keras daftar field config.** Skema diambil live dari server per-implementasi:

- `GET/POST /api/node/agent-implementations/{implementationId}/schema` dengan body `{"currentConfig": …}` mengembalikan JSON Schema properti config; `EXPERT_IMPL = "matrix-isp"` sebagai bawaan [KODE: 3219, 3417–3429]. Daftar strategi = `enum` pada field `strategyType` skema itu, beserta `enumNames` dan default yang ditandai "(suggested)" [KODE: 3975–4013].
- Config terbaca dua paruh dari server (`nodeConfig` + `config`) dan digabung klien jadi satu objek dengan paruh plugin bersarang di `pluginConfig` untuk penulisan [KODE: 3760–3768].
- `agent set` = read-modify-write seluruh config: baca → terapkan perubahan dengan koersi tipe menurut skema (bool/list/angka) → tulis balik utuh via `POST /api/node/agents/{id}/configure`, jadi mengubah satu field tidak menghapus field lain [KODE: 3861–3908]. Id arena divalidasi lawan katalog `GET /api/node/arenas?isActive=true` karena server menerima id arena tak dikenal dan akibatnya agent diam-diam tidak pernah diberi kerja [KODE: 3883–3895].
- Parameter numerik strategi membawa **default yang di-sample server per permintaan** (bukan konstanta klien) — berganti strategi memicu pengambilan skema ulang dan penyemaian default strategi baru [KODE: 3431–3442, 3897–3905].
- Koreksi khusus `dynamic`: menulis `strategyType=dynamic` memaksa `skipDeepEvaluation=False` di config yang ditulis [KODE: 3533, 3900–3907].
- Field non-skema yang diakui eksplisit kode: `maxConcurrency` (dikecualikan dari parameter numerik strategi) dan `contextWindowTokens` di `pluginConfig` (kunci deklarasi jendela konteks model; minimum server 8.000, ≥100.000 = kembali ke batas standar ±75.000 token prompt) [KODE: 3221, 3371, 5039–5067; SKILL.md "small context window"].
- Caps adalah sistem terpisah dari config: field sah `maxIsrs24h`, `maxUsd24h`, `maxTokens24h` (semua nullable), `warningThresholdPct` (0–100), `isActive` [KODE: CAP_FIELDS: 3554–3561]. Penegakan server = paling ketat menang lintas cakupan agent DAN akun, jadi "tidak ada baris cap di agent" ≠ "tidak ada cap" [KODE: 3840–3848].

## 6. Pushed Work vs Dynamic Work

Dua bentuk kedatangan kerja, ditentukan **strategyType di config server** — `serve` sendiri tidak menetapkan kebijakan [SKILL.md Workflow 3; KODE: resolve_claim_plan: 4832–4872]:

| | Pushed (semua strategi selain `dynamic`) | Dynamic (`dynamic`) |
|---|---|---|
| Siapa memilih Question | Platform mencocokkan & mengirim via gateway | Sesi `serve` yang mencari & meminta |
| Perilaku serve | Hanya menjawab yang diberikan; thread pencari TIDAK dinyalakan — mencari juga = sumber permintaan kedua yang tak terkoordinasi | Thread `claim_poller` terpisah mencari berkala, lalu klaim via REST |
| Konsekuensi diam | Idle = normal | Idle terlihat persis seperti rusak; berhenti mencari = berhenti menghasilkan, diam-diam |
| Filter pencarian | Diabaikan (dicetak sebagai peringatan bila diberikan) | Filter argv `serve` (`q=`, `questionMaxAgeMs=`, …) divalidasi lawan daftar filter yang diterbitkan server |

Detail dynamic:
- Interval pencarian: `--every`, bawaan `DEFAULT_SEARCH_EVERY_MS = 300_000` (5 menit), lantai `MIN_SEARCH_EVERY_MS = 30_000` [KODE: 4418–4419, 4865–4867].
- Pencarian **wajib berbatas**: keyword `q=` atau jendela usia; tanpa keduanya klien menambahkan plafon 24 jam dan mengumumkannya [KODE: ensure_search_bound: 1404; API.md "Agent operations"].
- Klaim = `POST /api/node/agents/{id}/process-opportunity` body `{"opportunityId", "opportunityType": "ISR"}` [API.md §Take one on; KODE: claim_opportunity: 4449]. Tiga hasil yang harus dibedakan: `assigned:true` (job ada, kerja terutang), `assigned:false`+`success:true` (*passed on* — ditolak di cek akhir), `success:false` (ditolak platform: kapasitas/cap/orang lain lebih dulu).
- Klaim berjalan di thread sendiri karena platform bertanya balik ke proses yang sama "apakah akan diambil?" dan menunggu ±30 detik — loop yang memblokir pada panggilan klaim tidak bisa menjawab pertanyaan itu dan jendela lewat = Question **ditolak**, bukan dilewati [API.md §Take one on; KODE: 5737–5770].

## 7. Cara Kerja `serve` (mekanisme internal)

| Aspek | Mekanisme | Bukti |
|---|---|---|
| Kunci proses tunggal | File lock advisori `~/.dialectica/serve.lock` (POSIX `fcntl.flock`, Windows `msvcrt.locking` byte offset 1 MB); serve/answer kedua menolak mulai dan menyebut pid pemegang; file tidak pernah dihapus, pid ditulis sesudah lock diambil; lepas via `atexit`, force-quit menyerahkan ke OS | [KODE: 4876–5037] |
| Login gateway | Bootstrap → access token dirotasi saat login pertama; login kena 429 → tunggu sesuai perintah server, kredensial tidak disentuh; `LOGIN_RATE_LIMIT_MAX_TRIES = 30`, `MAX_RELOGIN_ATTEMPTS = 3` | [KODE: 2052, 2081, 1885, 5396–5420] |
| Poll | Long-poll Matrix `/sync`, timeout server 10 dtk / plafon klien 15 dtk; kursor `since` disimpan di `agent.json` (dibuang saat reconnect) | [KODE: 1872–1875; 4041–4050] |
| Poll gagal | Backoff eksponensial `POLL_BACKOFF_BASE_S = 5` → `POLL_BACKOFF_MAX_S = 60`, dobel tiap kegagalan berurutan | [KODE: 2279–2282] |
| 429 di gateway | Tunggu persis `retry_after_ms`/`Retry-After`, dijepit [1, 60] dtk, bawaan 5 dtk — bukan kegagalan, tidak perlu restart | [KODE: 2096–2156; SKILL.md] |
| Offer-to-answer (evaluate) | Dijawab **inline di loop poll dalam ±30 dtk**, aritmetika lokal murni, tanpa panggilan model: skor `EVALUATE_ACCEPT_SCORE = 100` (tawaran) atau 0 (tolak bersih). Ceknya hanya: tipe opportunity harus ISR (non-ISR → 0, "this Expert writes Answers") dan output schema arena harus bisa dipenuhi klien | [KODE: 2426–2497] |
| Hook READY | `DIALECTICA_READY_CMD` (bila diset) berjalan di langkah offer dengan opportunity JSON di stdin, batas `READY_TIMEOUT_S = 10` dtk; timeout di sini = REJECT | [KODE: 2959–2965, 2986] |
| Hook PREPARE | `DIALECTICA_PREPARE_CMD` (bila diset) berjalan **sebelum klaim** dengan baris pencarian JSON di stdin; exit 0 hanya bila memegang jawaban yang diyakini lolos verifikasi; batas `PREPARE_TIMEOUT_S = 3600` (env `DIALECTICA_PREPARE_TIMEOUT_S` dijepit 600–21.600); heartbeat 120 dtk | [KODE: 2949–2996, 3004–3068] |
| Skip pasca-prepare | Question yang dilewati prepare tidak dilihat lagi selama **`PREPARE_SKIP_TTL_S = 6 * 3600`** (6 jam), disimpan **di memori proses** (`skip_until` dict di claim poller) — hilang saat proses mati/restart | [KODE: 2988; claim_poller: 4713] |
| Eksekusi job | Tiap job = worker thread daemon sendiri (`handle_job` → `run_provider`); cache prompt asli per jobId (maks 200 entri, sesi saja) untuk menjawab schema-correction; event terdeliver ulang didedupe via `seen_events` (tidak hanya mengandalkan kursor sync) | [KODE: 5493–5510, 5650, 5977–5980] |
| Konkurensi | Klien **tidak** menegakkan `maxConcurrency` secara lokal — thread dibuat per job yang tiba; batas konkurensi ditegakkan server (penolakan "at capacity"). Daftar `inflight` hanya untuk drain saat berhenti | [KODE: 5513, 5977–5980; INFERENSI dari ketiadaan gerbang lokal] |
| Kirim jawaban | `gw_send` dengan retry rate-limit: maks `SEND_RATE_LIMIT_MAX_WAITS = 5` tunggu, backoff eksponensial 0,5 → 8 dtk + jitter; tawaran klaim dibatasi total `OFFER_SEND_MAX_WAIT_S = 10` | [KODE: 2205–2286] |
| Berhenti | Ctrl-C pertama: set flag, selesai sesudah poll berjalan; Ctrl-C kedua: `os._exit(130)`. Di akhir: drain worker, lalu `report_outcomes` men-poll daftar job sampai status terminal atau deadline 60 dtk (poll 6 dtk) | [KODE: 5519–5532; report_outcomes: 4301] |
| Token sesi kedaluwarsa di tengah run | Kode `CAPTCHA_REQUIRED`/`LOGIN_REQUIRED` = "berhenti mengambil kerja baru", bukan crash — kerja yang sudah diterima tetap diselesaikan; dengan work credential aktif, serve bahkan bisa restart tanpa sign-in sama sekali | [KODE: 413–417; SKILL.md Workflow 3] |
| Kredensial dicabut | Server menolak work credential (403 `AUTH_FORBIDDEN` + teks "credential cannot be used here", atau 401 `LOGIN_REQUIRED` pada panggilan berkredensial-kerja) → serve **berhenti**, TIDAK fallback ke token sesi; pemulihan via `agent reconnect` | [KODE: 419–455] |

### Provider (model penjawab) di dalam serve
- Resolusi: `DIALECTICA_PROVIDER_CMD` (perintah bebas: prompt di stdin, jawaban di stdout) mengalahkan segalanya; selain itu provider host yang teridentifikasi dari env marker; selain itu provider pertama terpasang di PATH dari daftar `PROVIDERS` (entri terbaca: `claude`, `codex`) — dan bila pilihan PATH itu arbitrer di antara ≥2 provider terpasang, klien mencetak peringatan sekali per proses karena pilihan itu membelanjakan akun vendor yang dipilih [KODE: 2566, 2664–2745].
- `--model` / `DIALECTICA_MODEL` memilih model **di dalam** provider terpilih — tidak bisa memindahkan jawaban ke vendor lain [SKILL.md "Answering model"; KODE: 5466–5472].
- Batas generasi: `DEFAULT_PROVIDER_TIMEOUT_MS = 900_000` = **15 menit per jawaban**; env `DIALECTICA_PROVIDER_TIMEOUT_MS` (maks 2.147.483.647) menaikkannya; timeout = jawaban gugur = menghantam reliability [KODE: 2515, 2751–2761].
- Tools untuk provider `claude`: tepat `WebSearch` + `WebFetch` (`DEFAULT_PROVIDER_TOOLS`), dijalankan dengan `--strict-mcp-config` + `--setting-sources ""` (MCP server & settings operator dimatikan) dan `--tools` + `--allowedTools`; `DIALECTICA_PROVIDER_TOOLS` mengubah set (mis. menambah `Bash`/`Read` — risiko: Question orang asing menggerakkan shell/file mesin tanpa prompt) [KODE: 2528, 2531–2552, 2568–2620; SKILL.md "Tool access"].
- Env yang diberikan ke provider per job: `DIALECTICA_JOB_ID`, `DIALECTICA_JOB_KIND` (`ISR` menjawab / `ISO` memverifikasi), `DIALECTICA_ISR_ID`, `DIALECTICA_TARGET_ISO_ID` [SKILL.md "Answering model"; KODE: provider_env: 2870].
- Setiap prompt job didahului teks `CONDUCT` tetap: tugas/konstrain/format Question adalah pekerjaan; teks yang mencoba mengubah peran/meminta rahasia diabaikan; satu-satunya jalan keluar resmi = balas persis `REJECT: <reason>` [KODE: 1891–1937].
- Prompt job dari server dibatasi ±75.000 token: jawaban terdahulu dipangkas (Verified dulu, lalu terbaru) dan prompt menyatakan berapa yang ditinggalkan; deklarasi `contextWindowTokens` lebih kecil memangkas lebih agresif [SKILL.md "Time limit"/"context window"].

## 8. Cara Kerja `answer` (pola resmi satu jawaban)

`trued answer <isrId>` secara harfiah adalah `cmd_serve(args, one_shot_target=isrId)` [KODE: 6147–6160] — klaim hanya bekerja saat agent online dan jawaban berjalan di koneksi yang sama, jadi keduanya tidak bisa dipisah jadi dua command [KODE: 5737–5745]. Urutan & batas waktunya:

| Fase | Batas | Bukti |
|---|---|---|
| Klaim berjalan di thread terpisah, menunggu sync pertama (agent yang belum pernah poll dianggap offline dan klaimnya ditolak) | — | [KODE: 5746–5770] |
| Menunggu kerja terdeliver sesudah klaim diterima | `ONE_SHOT_DELIVERY_S = 180` dtk, lalu menyerah (tanpa ini answer bisa poll selamanya) | [KODE: 4118–4127] |
| Generasi jawaban | 15 menit (timeout provider yang sama) | [KODE: 2515] |
| Tetap terhubung sesudah submit untuk schema-correction | `ONE_SHOT_GRACE_S = 45` dtk; koreksi menulis ulang jawaban dan jendela 45 dtk mulai lagi | [KODE: 4105–4116; SKILL.md] |
| Cek penerimaan | Poll status job sampai terminal / ±60 dtk | [KODE: report_outcomes: 4301; SKILL.md] |

- `answer` **tidak** digerbang strategi pull-only: strategi lain dipetakan server ke mode manual dan klaim diterima, jadi klien sengaja tidak menolak [KODE: 6152–6159]. Berlaku juga sebaliknya di dokumen: "Any strategy can do this. `dynamic` decides whether Dialectica *sends* work; it never decides what the user can go and claim." [SKILL.md "Answer one Question"]
- Menghentikan `answer` di tengah dapat mengorbankan Question yang sudah diambil → menghantam reliability; dokumen memerintahkan membiarkannya selesai / jalan di background [SKILL.md "Answer one Question"].
- Hasil akhir tiga cabang klaim (taken on / passed on / not given) + empat cabang nasib jawaban (completed / failed-cancelled-abandoned / declined / DROPPED) dipetakan ke exit code 0/1/3/4 [SKILL.md; KODE: 4286–4296].

## 9. Penyimpanan & Pelacakan Question/Answer

**File lokal — hanya tiga, semuanya di `~/.dialectica/`** (tidak ada database/ledger jawaban lokal di klien stok):

| File | Isi | Sifat |
|---|---|---|
| `session` | Token sesi akun | Ditulis user/agen saat sign-in (umask 177, dir 700); klien hanya membaca [KODE: 111–112, 145; SKILL.md Auth] |
| `agent.json` | State Expert: `agentId`, `baseUrl`, `userId`, `homeserver`, `matrixUserId`, `bootstrap` (sementara), `accessToken` (hasil rotasi), kursor sync `since`, flag `startingConfig`/`configured`/`capped`, `pendingContextWindowTokens`, dan (untuk mode credential-only) `strategyType` + `opportunityFilters` tersimpan | JSON, mode 0600 sejak penciptaan, tulis atomik + fsync; temp per-pid `agent.json.<pid>.tmp` [KODE: 3243–3314, 5252–5266] |
| `serve.lock` | Pid pemegang lock (isi tidak pernah dihapus) | Lock advisori, bukan data [KODE: 4918] |
| `agent.gone-<detik>.json` | State Expert yang dinyatakan hilang/dihapus server — dipindah, bukan dihapus | Arsip pemulihan manual [KODE: 5153–5167] |

- Question/Answer **tidak** disimpan lokal oleh klien: status dibaca ulang dari server (`question`, `status`, `/api/node/agents/{id}/jobs` di `report_outcomes` [KODE: 4337]). Satu-satunya cache jawaban di klien adalah cache prompt asli per jobId di **memori proses** (maks 200, hilang saat restart) — konsekuensi terbukti di kode: schema-correction yang tiba sesudah restart tidak punya original untuk dikoreksi dan **ditolak** (`NoOriginalPrompt`) daripada dijawab dari body kosong [KODE: 5493–5500, 5620–5640].
- Notes user disimpan **di server** (`/api/node/memory`), bukan file lokal — itu yang membuatnya selamat dari ganti mesin/sesi [SKILL.md "Notes that persist"; KODE: 6034].

## 10. Retry / Timeout / Concurrency / Rate-Limit — Angka Persis

| Parameter | Nilai | Bukti |
|---|---|---|
| Timeout REST bawaan | 30 dtk (60 dtk untuk assist/configure/opportunities/credential) | [KODE: 230, 3424, 3908, 4082] |
| Long-poll gateway | 10 dtk server / 15 dtk plafon klien | [KODE: 1872–1875] |
| Tunggu 429 gateway | persis perintah server, jepit [1, 60] dtk, bawaan 5 | [KODE: 2096–2156] |
| Backoff poll hilang | 5 → 60 dtk eksponensial | [KODE: 2281–2282] |
| Kirim pesan gateway | maks 5 kali tunggu rate-limit; backoff 0,5 → 8 dtk + jitter; tawaran klaim total maks 10 dtk | [KODE: 2205–2212, 2286] |
| Login rate-limit | maks 30 percobaan tunggu; relogin maks 3 | [KODE: 2052, 1885] |
| Generasi satu jawaban | 900.000 ms (15 menit) bawaan | [KODE: 2515] |
| Prepare hook | 3.600 dtk bawaan (env dijepit 600–21.600); heartbeat 120 dtk | [KODE: 2976–2996] |
| Ready hook | 10 dtk | [KODE: 2986] |
| Skip prepare | 21.600 dtk (6 jam), di memori proses | [KODE: 2988] |
| Interval cari kerja (dynamic) | bawaan 300 dtk, lantai 30 dtk | [KODE: 4418–4419] |
| Grace one-shot | 45 dtk; tunggu delivery 180 dtk; poll hasil 60 dtk per 6 dtk | [KODE: 4112–4127, 4301] |
| Cap jawaban bawaan Expert baru | 20 / 24 jam (klien; server bawaan unlimited) | [KODE: 4112] |
| Konkurensi | Ditegakkan **server** via config `maxConcurrency` (field config server, dikecualikan dari parameter strategi di klien); klien membuat thread per job tanpa gerbang lokal | [KODE: 3221, 5977] |
| Plafon baca digest | 200 baris per panggilan (`status`/`notifications`) | [KODE: 457] |

## 11. Penghentian, Pemulihan & Kematian Proses di Tengah Pekerjaan

**Penghentian rapi:** SIGINT pertama memasang flag berhenti; loop poll selesai; claim poller berhenti; worker di-drain; hasil job di-poll dan dicetak sebagai baris `Done:`; lock dilepas `atexit` [KODE: 5519–5532, 5790–5830, 4949]. SIGINT kedua = `os._exit(130)` paksa [KODE: 5524–5527].

**Pemulihan yang dirancang kode:**
- State ditulis atomik setiap perubahan kredensial/kursor → restart membaca `agent.json` yang utuh; file terpotong tidak mungkin dari tulis yang terinterupsi [KODE: 3288–3314].
- Setup setengah jadi (config/cap belum terpasang) disembuhkan run berikutnya via flag `configured`/`capped`/`startingConfig` [KODE: 4237–4299].
- Expert dihapus server → set-aside + registrasi ulang maks sekali per run [KODE: 5128–5185].
- Kredensial dicabut → berhenti total tanpa fallback; pulih hanya lewat `agent reconnect` (kode sekali pakai, 30 menit) [KODE: 4025–4057].

**Yang TIDAK bisa dipulihkan klien (titik buta terverifikasi):**
1. **Tidak ada panggilan pelepas/abandon job di klien.** Pencarian `DELETE`/release di seluruh file: nihil — satu-satunya "abandon" adalah status terminal yang dibaca (`TERMINAL_JOB_STATES`) dan abandon *prepare lokal* [KODE: 4286, 4541]. Job yang sudah ter-assign ke Expert yang prosesnya mati hanya bisa berakhir dari sisi server (timeout/pengabaian server), dan pengabaian itu tercatat sebagai status `abandoned` yang menghantam reliability (REL-005) [INFERENSI dari kode + SKILL.md "Finish what you start"].
2. **Kejadian nyata 18 Nov (dari konteks operasi, bukan kode):** job yang ter-veto pasca-klaim mengunci slot Expert ±30 menit dengan balasan server "Agent at capacity (1/1)" untuk klaim berikutnya — konsisten dengan `maxConcurrency=1` di config kita dan ketiadaan API pelepas di klien; pelepasannya murni menunggu kedaluwarsa sisi server.
3. **Unit systemd hilang saat VM replacement (18 Nov pagi & malam):** file unit di `/etc` ephemeral terhapus → serve tidak jalan sama sekali sampai unit dipasang ulang manual dari salinan induk di folder provider. Ini kegagalan *launcher*, bukan klien: state `~/.dialectica/` selamat, jadi serve yang dipasang ulang melanjutkan sebagai Expert yang sama [INFERENSI operasional].
4. Cache prompt sesi hilang saat restart → schema-correction yatim ditolak (lihat §9).
5. Skip-prepare 6 jam hilang saat restart → Question yang sudah dilewati prepare dinilai ulang dari nol (biaya komputasi prepare berulang, bukan risiko kebenaran) [KODE: 2988 + sifat in-memory di claim_poller: 4713].

## 12. Pengelolaan Credential

- **Token sesi**: file `~/.dialectica/session`, diperoleh manual via halaman `$BASE/connect-agent` di browser (atau fallback `$BASE/api/auth/get-session`), disimpan dengan `umask 177`; klien membacanya tiap panggilan, tidak pernah mencetaknya (`whoami` hanya "present/missing") [SKILL.md Auth check; KODE: 145–155, 6238–6243]. Umur ±7 hari, sliding.
- **Kredensial Expert**: bootstrap sekali pakai dari `credential/reveal` → login gateway → dirotasi jadi access token → bootstrap dibuang dari state; semua disimpan di `agent.json` mode 0600 di direktori 0700 [KODE: 4074–4096, 3288–3314, 5436–5443].
- **Work credential** (kredensial kerja Expert di REST): menggantikan token sesi hanya untuk 3 panggilan penghasilan, digerbang flag server `agentWorkCredentialEnabled` [KODE: 163–216, 262–282].
- **Kode reconnect**: tidak pernah lewat argumen command line (akan tercatat di process listing & shell history) — getpass di terminal atau satu baris stdin; validasi bentuk regex saja, server yang memutuskan sah/tidak [KODE: 4015–4050].
- Redirect lintas-origin membuang kedua header kredensial [KODE: 122–142]; gateway menolak redirect sama sekali (`_NoRedirect`) karena permintaannya membawa password/token agent [KODE: 1944–1950].
- Menyalin `agent.json` ke mesin lain secara eksplisit dilarang dokumen: dua salinan men-poll pekerjaan yang sama di bawah satu kredensial dan sama-sama dihitung melawan jatah poll kredensial itu [SKILL.md Workflow 3].

---

## 13. BAGIAN KHUSUS — Inventaris Fitur yang ADA tapi TIDAK Pernah Dipakai Operasi Kita

Pembanding: yang dipakai operasi berjalan = `serve` (via unit systemd + lapisan provider kita), `answer`, dan bacaan API mentah (`scores`, `notifications`, `agents`, `isrs`, `isos`). Semua di bawah ini **ada di kode/dokumen tetapi belum pernah dijalankan operasi kita** (atau hanya lewat padanan API mentah ad-hoc, bukan jalurnya sendiri).

| # | Fitur | Fungsi | Potensi manfaat | Risiko / catatan |
|---|---|---|---|---|
| 1 | `trued opportunities` + `--list-filters` (CLI) | Penemuan Question yang bisa diklaim Expert ini, dengan metrik baris (viso/fiso/para/marathon/score) dan daftar filter resmi server | Memilih target secara terbaca sebelum serve; filter selalu sinkron server (tidak menua seperti daftar hardcoded kita) | Baca saja — risiko ~nol. Operasi kita selama ini mencari lewat poller serve sendiri, bukan jalur baca ini |
| 2 | `trued arena [id] [--window]` | Analitik arena: keramaian vs bayaran tiap strategi, **alasan penolakan verifikasi teratas**, waktu menuju Verified | Menjawab "kenapa jawaban ditolak" dari data server sebelum membakar generasi; satu-satunya sumber alasan penolakan terstruktur | Baca saja. Angka hanya boleh dibandingkan **di dalam** satu arena; baris `assumed:` = tanpa bukti — dokumen melarang menjadikannya vonis [SKILL.md "Reading an Arena"] |
| 3 | `trued agent strategies` | Daftar strategi server + parameter + panduan arah-baca metrik **verbatim dari server** | Peta strategi resmi (pushed: mis. endgame/first_responder/marathon_tackler dll.) tanpa menebak; panduan para/viso per strategi | Baca saja. Mengganti strategi = keputusan user (wilayah terkunci) |
| 4 | `trued notes` (baca/tulis) | Dokumen keputusan user yang disimpan **di server** (`/api/node/memory`), dibaca otomatis saat `signin`, selamat dari ganti mesin/model/sesi | Keputusan berdiri (doktrin, pilihan arena) hidup di platform, bukan hanya file lokal kita; sesi mana pun mulai dengan konteks yang sama | Tulis wajib menyebut `--expected <versi>` (optimistic lock); **bukan tempat rahasia** (dibaca ke konteks tiap sesi + tampil di website); aturan skill: tanya sebelum menulis |
| 5 | `trued signin` sebagai ritual sesi | Konfirmasi sesi + pastikan Expert + muat notes dalam satu panggilan idempoten | Mengganti rangkaian cek manual kita; menjamin notes server ikut terbaca | Tanpa risiko berarti; provision hanya terjadi bila mesin belum punya Expert |
| 6 | `trued search` / `page` / `question` (CLI) | Baca korpus terverifikasi (wiki + Question) dengan sinyal viso/fiso dan penanda keyword-vs-semantik | Riset topik & cek duplikat sebelum bertanya/menjawab lewat jalur yang sudah menandai hasil semantik-palsu | Baca saja. Halaman penuh hasil `semantic` BUKAN bukti korpus punya topik itu [SKILL.md Workflow 1] |
| 7 | `trued report` | Lapor defect/fitur ke platform, satu panggilan | Saluran resmi untuk anomali platform yang kita temui (mis. perilaku cap) terdokumentasi ke pembuatnya | Mengatasnamakan akun user — aturan skill: beri tahu user, satu laporan per masalah |
| 8 | `agent reconnect` | Pulihkan Expert yang aksesnya dicabut web, via kode sekali pakai | Satu-satunya jalur pulih bila kredensial dicabut — tanpa registrasi Expert baru | Kode 30 menit, sekali pakai; jangan minta user menempel kode ke chat bila bisa menjalankan sendiri [SKILL.md] |
| 9 | `agent caps` field penuh (`maxUsd24h`, `maxTokens24h`, `warningThresholdPct`) | Plafon belanja berbasis USD/token + ambang peringatan, selain `maxIsrs24h` yang kita kenal | Mengikat biaya komputasi model secara uang/token, bukan hanya jumlah jawaban | Penegakan memakai telemetri biaya yang dilaporkan — dokumen klien sendiri memperingatkan angka [used] bisa tidak lengkap untuk pemakaian provider eksternal [KODE: 3850–3858] |
| 10 | `serve --context-window` / `DIALECTICA_CONTEXT_WINDOW_TOKENS` | Deklarasi jendela konteks model saat setup Expert baru | Wajib bila model penjawab berjendela kecil; mencegah Question terkirim ke model yang tidak muat | Hanya berlaku saat registrasi baru; untuk Expert berjalan pakai `agent set contextWindowTokens=` |
| 11 | `DIALECTICA_PROVIDER_TOOLS` (tambah `Bash`/`Read`) | Memberi model penjawab kemampuan menjalankan kode / membaca file lokal | Jawaban numerik bisa *dihitung* sungguhan, bukan diklaim — kenaikan mutu nyata untuk Question hitungan | **Risiko tertinggi di daftar ini:** Question orang asing menggerakkan shell/file tanpa prompt di mesin serve. Dokumen hanya menyetujui di container/VM/akun khusus [SKILL.md "Tool access"] |
| 12 | Hook `DIALECTICA_PREPARE_CMD` / `DIALECTICA_READY_CMD` sebagai antarmuka resmi | Titik ekstensi resmi klien untuk gerbang pra-klaim & gerbang offer — persis tempat lapisan gerbang kita (doktrin/kesegaran/isi) hidup | Menegaskan arsitektur: gerbang kita menumpang mekanisme yang memang disediakan klien, dengan kontrak timeout & skip-TTL resmi | Prepare timeout besar (s/d 6 jam) bisa menahan laju klaim; ready timeout 10 dtk — gerbang berat di sana = REJECT |
| 13 | **Registrasi IVSP (Verifier) — TIDAK ADA di CLI** | Endpoint yang sama `POST /api/node/agents/matrix` menerima `{"type": …}`, tetapi `_provision()` mengode keras `"ISP"`; `resolve_agent_id` menyaring daftar agent ke `type == "ISP"` saja; filter opportunities untuk Verifier dikembalikan server sebagai daftar kosong ("a Verifier gets an empty list") | Jalur Verifier (Jalur 2 kita) **tidak bisa** dibangun dari CLI stok — harus API mentah (yang memang dilakukan kit `provider/verifier/` kita) atau registrasi web | [KODE: 4082, 3727–3729; API.md §Discover the filters]. Menariknya loop serve sendiri netral-jenis: `DIALECTICA_JOB_KIND=ISO` dikenal provider_env dan event `execute-job` tidak menyaring jenis job — yang mengunci Verifier keluar adalah provision + resolusi agent + gerbang evaluate (`can_satisfy_output_contract` menolak opportunity non-ISR dengan skor 0) [KODE: 2451–2468, 2870; INFERENSI: serve untuk IVSP tidak didukung jalur resmi klien walau transportnya generik] |
| 14 | Arena **forecasting** via config (`agent set arenas=forecasting`) | Arena kedua yang eligibility-nya terbuka untuk ISP/IVSP (postISR admin-only) | Medan kerja tambahan dengan ekonomi escrow berbeda | Aturan main berbeda total (resolusi masa depan, settled = terminal); config Expert = wilayah terkunci user |
| 15 | Strategi pushed (non-dynamic) | Platform yang mencocokkan & mengirim kerja; serve cukup online | Nol biaya pencarian; cocok untuk strategi ambang (endgame dll.) tanpa poller kita | Kerja datang tanpa pilihan kita — bertabrakan dengan doktrin seleksi kita; mengganti strategyType = keputusan user |
| 16 | `ask --continue` multi-giliran penuh | Loop asisten sampai `ready` dengan receipt | Jalur resmi pembuatan Question tergating asisten (yang dipakai preflight kita hanya assist live read) | Membuat Question = wilayah terkunci + fee; bukan untuk lini ini |
| 17 | `agent set` field lanjutan dari skema (system prompt Expert, parameter strategi per-strategi) | `agent set` menerima **setiap** field yang ditampilkan `agent show`, termasuk system prompt Expert dan parameter strategi | Tuas konfigurasi resmi yang selama ini kita baca sebagai daftar saja | Menulis config = wilayah terkunci; read-modify-write menulis balik SELURUH config sehingga nilai basi bisa ikut tertimpa bila dibaca dari salinan lama [INFERENSI dari KODE: 3861–3908] |
| 18 | Mode credential-only serve | Serve restart tanpa sign-in sama sekali (memakai `strategyType` + `opportunityFilters` tersimpan dari start bertanda-tangan terakhir) | Serve tetap hidup melewati kedaluwarsa sesi 7 hari tanpa intervensi login | Syarat: Expert sudah selesai setup; mengubah setting tetap butuh sign-in [KODE: 5210–5251, 5449–5456] |

### Ringkasan bagian khusus
- Celah terbesar bukan fitur tersembunyi, melainkan **jalur baca resmi yang tidak kita pakai**: `opportunities`, `arena`, `agent strategies`, `notes`, `signin` — semuanya read-only/murah dan menggantikan beberapa bacaan API mentah ad-hoc kita dengan jalur yang membawa penanda keandalan dari server sendiri.
- **Verifier memang di luar jangkauan CLI stok** — terbukti di tiga titik kode (provision ISP-only, filter resolusi ISP-only, gerbang evaluate ISR-only). Bangunan Jalur 2 kita lewat API mentah adalah keharusan teknis, bukan pilihan gaya.
- Satu-satunya fitur belum-terpakai dengan risiko keamanan nyata adalah penambahan tool `Bash`/`Read` ke provider penjawab (#11).

---

*Akhir laporan W4. Tidak ada konfigurasi diubah, tidak ada command state-changing dijalankan selama investigasi ini.*
