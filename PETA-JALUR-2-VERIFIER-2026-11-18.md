# PETA JALUR 2 — VERIFIER (IVSP), Dialectica

Status: **FINAL — 2026-11-18.** Vonis frontier atas
`FRONTIER-PAKET-JALUR2.md` sudah dilipat ke §6 (otoritas:
`belajar-2026-11-18/frontier-jalur2/SINTESIS-FRONTIER-JALUR2.md`,
konsultasi 2026-11-18 10:15–10:21 WIB). Semua bagian tuntas.
Disusun 2026-11-18 (perintah user 09:58 + perluasan bangunan 10:01 + F-31D 10:05).
Memperdalam `PETA-EARN-LIVE-2026-11-18.md` §Jalur 2 — bukan mengulanginya.

Konvensi bukti: **TERBUKTI-LIVE** = tarikan API primer sesi ini (mentah di
`belajar-2026-11-18/peta-jalur-2/`). **DOKUMEN-RESMI** = dokumen/kode yang
dikirim klien v0.22.4 (`skill-audit/pkg/dialectica/`). **LAPANGAN** = catatan
MEKANISME-DAN-LAPANGAN.md (petunjuk arah; beban klaim sudah dicek ulang ke
sumber primer bila dipakai). **BELUM-TERBUKTI** = belum bisa dibuktikan tanpa
mencoba; dilarang diperlakukan sebagai fakta.

READ-ONLY: tidak ada pendaftaran, tidak ada verdict terkirim, tidak ada
config berubah selama pemetaan ini. Yang dibangun = alat + bukti keringnya.

---

## 1. REGISTRASI — bagaimana sebuah IVSP lahir

### 1.1 Kelahiran ISP kita (pola yang terbukti penuh)

Dari kode klien (`trued.py::_provision`, `_run_serve`, `ensure_expert`) dan
cocok dengan agent live kita (TERBUKTI-LIVE: `agents-live.json` — 1 agent,
type ISP, implementationId `matrix-isp`, state configured):

1. `POST /api/node/agents/matrix` body `{"type": "ISP"}` →
   `{agentId, matrixHomeserver, matrixUserId}`.
2. `POST /api/node/agents/{agentId}/credential/reveal` body `{}` →
   kredensial bootstrap sekali-pakai.
3. Login pertama ke gateway Matrix memakai bootstrap; server merotasi jadi
   access token. State lokal: `~/.dialectica/agent.json` (mode 0600) —
   SATU berkas = SATU agent = SATU kredensial.
4. Server MENOLAK konfigurasi sebelum koneksi pertama; config awal
   (strategi + cap `PUT /api/spending/limits/agent/{id}`, bawaan klien
   20 jawaban/24 jam) diterapkan sesudah agent pernah connect.
5. Penolakan yang paling mungkin di langkah 1: `WAITLIST_PENDING` — akun
   belum diaktifkan akses Expert-nya ("Ask the Dialectica team"). Akun kita
   SUDAH punya akses itu (ISP kita ada) — untuk peran Expert.

### 1.2 Pintu IVSP-nya

- **Endpoint yang sama menerima `type` sebagai parameter** (DOKUMEN-RESMI:
  body registrasi memang `{"type": "ISP"}` — bukan endpoint khusus ISP).
  Klien v0.22.4 TIDAK PERNAH mengirim `"IVSP"`; tidak ada flag `--type` di
  `serve`/`answer`/`signin`. Jadi jalur API-nya masuk akal tapi
  **BELUM-TERBUKTI** server menerimanya dari token sesi kita.
- **Katalog implementasi LIVE** (`GET /api/node/agent-implementations`,
  TERBUKTI-LIVE): ada TIGA rasa IVSP —
  `dialectica-ivsp` (managed rumah: "Dialectica managed AI verifier ·
  20 verifications/week · No API key required"),
  `vercel-ai-ivsp` (BYOK: OpenRouter dll.),
  `matrix-ivsp` ("OpenClaw & Hermes Verifier agent via Matrix protocol" —
  rasa yang cocok dengan arsitektur kita, pasangan `matrix-isp`).
- **Skema config `matrix-ivsp` MENJAWAB live** (`POST
  /api/node/agent-implementations/matrix-ivsp/schema`, TERBUKTI-LIVE,
  berkas `schema-matrix-ivsp.json` + per-strategi) — mesin server untuk
  peran ini terpublikasi penuh hari ini.
- **Website**: panel `$BASE/agents` adalah tempat "Manage your Expert and
  Verifier agents" (DOKUMEN-RESMI, SKILL.md). Apakah PEMBUATAN Verifier
  dimulai dari panel itu atau dari endpoint matrix di atas:
  **BELUM-TERBUKTI** dari klien (klien tidak memuat keduanya untuk IVSP).
- **Gerbang akun pernah ada**: catatan lapangan 8–9 Nov (LAPANGAN):
  dashboard akun kita menampilkan "Verifier creation is not open with
  this account during the platform launch phase", dan saat itu endpoint
  skema IVSP tidak ditemukan. Hari ini katalog + skema menjawab live —
  keadaan server BERUBAH sejak catatan itu. Apakah gerbang di level AKUN
  kita sudah terangkat hanya bisa dibuktikan dengan (a) membaca panel
  website (cek mata, nol risiko — di luar jangkauan tugas API ini), atau
  (b) percobaan registrasi tergating di bagian 7. Sampai salah satu
  terjadi: **status akun = BELUM-TERBUKTI, condong terbuka**.

### 1.3 Koeksistensi ISP + IVSP di satu akun

- Model data server mendukungnya (DOKUMEN-RESMI: `GET /api/node/agents`
  mengembalikan semua type; `resolve_agent_id` menyaring `type == "ISP"`
  dengan komentar "a Verifier would otherwise be counted" — penulis klien
  mengantisipasi akun berisi keduanya). **TERBUKTI sebagai model data;
  BELUM-TERBUKTI sebagai keadaan akun kita.**
- Satu rumah `~/.dialectica` TIDAK bisa menampung keduanya: satu
  `agent.json`, satu kredensial, satu `serve.lock` per direktori home
  (DOKUMEN-RESMI). Pesan kunci klien sendiri menyuruh "set up a separate
  Expert under another home directory". CONFIG_DIR klien terpatri dari
  `expanduser("~")` — rumah kedua = HOME kedua. Kit kita memakai rumah
  khusus `~/.dialectica-ivsp` (belum dibuat; runner hanya melapor
  ketiadaannya).
- Klien stok TIDAK bisa mengonfigurasi IVSP sama sekali: `agent
  show/set/caps/strategies` hanya me-resolve agent bertipe ISP.
  Konfigurasi IVSP kelak lewat panel website atau panggilan API mentah
  memakai skema `matrix-ivsp` yang sudah kita tarik — bukan lewat
  `trued.py`.

### 1.4 Biaya / undangan / syarat skor

- Biaya registrasi: tidak ada di dokumen mana pun; registrasi ISP kita
  tidak pernah memungut $TRUED (LAPANGAN + rekonsiliasi saldo).
  Untuk IVSP: **tidak ditemukan** — bukan bukti nol, tapi nol petunjuk.
- Undangan: jalur "Hosted Expert / undangan campaign" di ledger adalah
  jalur MENJALANKAN Expert orang, bukan syarat registrasi peran.
- Syarat RAR/Expertise minimum: **tidak ditemukan di sumber primer mana
  pun** (skema server tidak memuat field semacam itu; dokumen resmi tidak
  menyebut ambang). Gerbang yang terdokumentasi hanya akses akun
  (WAITLIST_PENDING untuk Expert; padanan IVSP-nya BELUM-TERBUKTI).

---

## 2. ALUR KERJA VERIFIER

### 2.1 Pekerjaan datang dari mana — BUKAN dari pencarian

- Endpoint peluang per-Question adalah milik Expert: respons
  `opportunity-filters` menggemakan `agentType: "ISP"` dan api.md
  menegaskan "a Verifier gets an empty list" (DOKUMEN-RESMI; TERBUKTI-LIVE
  untuk agent kita: `our-opportunity-filters.json` → agentType ISP).
- Verifier menerima pekerjaan yang DIDIORONG platform lewat gateway
  agent (protokol Matrix yang sama dengan Expert): pengguna sistem
  mengirim event `evaluate-request` (penawaran untuk dinilai; dijawab
  skor dalam ±30 detik), `execute-job` (pekerjaan; prompt dirender
  server), `schema-correction` (perbaikan format) — klasifikasi persis
  `trued.py::classify_event` (DOKUMEN-RESMI). Kesempatan verifikasi
  menamai Answer-nya di `targetIsoId` di samping `isrId`
  (`job_ids_from_opportunity`).
- Skema IVSP menyebut "Stage 1 qualification" (deskripsi field
  `enabled`: agent nonaktif "skipped in Stage 1 qualification") →
  penugasan bertahap: kualifikasi dulu, lalu penugasan (TERBUKTI-LIVE
  sebagai teks skema; rincian tahap-tahapnya BELUM-TERBUKTI).
- `skipDeepEvaluation` (bawaan true) = "assume acceptance"; dimatikan →
  agent menilai sendiri tiap kesempatan — itulah langkah evaluate di
  atas (TERBUKTI-LIVE sebagai teks skema).

### 2.2 Payload verdict (VFP)

- Hasil pekerjaan — jawaban maupun verdict — dikirim sebagai pesan
  teks ber-thread di room job-nya (`gw_send_threaded_text`,
  DOKUMEN-RESMI). TIDAK ada endpoint REST "submit verification" di
  api.md maupun klien.
- Format keluaran verdict yang persis ditentukan oleh prompt job yang
  dirender server (isi: pertanyaan, Answer yang dinilai, aturan arena,
  format wajib — pola yang sama dengan job menjawab; konteks jendela
  IVSP menyebut hingga 10 verifikasi terdahulu pada Answer yang sama
  ikut dikirim, ±5.000 token, dan Answer selalu dikirim utuh).
  **Bentuk literalnya BELUM-TERBUKTI** — belum pernah ada job VFP di
  akun ini (TERBUKTI-LIVE: riwayat 40 job kita = 40 type ISO (job
  menjawab), 0 VFP — `our-jobs.json`).
- Rekonsiliasi hasil: `GET /api/node/agents/{id}/jobs` (jobStatus:
  completed/failed/cancelled/abandoned) — endpoint yang sama untuk
  kedua peran (DOKUMEN-RESMI).

### 2.3 Konsensus & jendela waktu

- Aturan agregasi (LAPANGAN, terukur n=32 verdict di 2 ISR pantauan):
  verified ⟺ tepat **2 support, 0 refutasi**; falsified selalu memuat
  ≥1 refutasi. Clean sheet — tidak ada seri, tidak ada tie-break.
  Ukuran panel teramati 2–4 (ada eskalasi).
- Arena Forecasting menerbitkan `verificationConsensusThreshold: 2`
  di record arenanya (TERBUKTI-LIVE); General menerbitkan `None` di
  field yang sama — angka 2 untuk General bertumpu pada bukti lapangan
  di atas, bukan pada record arena.
- Kecepatan: verdict atas jawaban kita (Nov, LAPANGAN) mendarat
  +150–263 detik sesudah submit. Analitik live: median timeToVerified
  General 660 detik (n=3.745 pertanyaan), verifikasi-tercatat-sebelum-
  verified = 6; Forecasting timeToVerified 105 detik tetapi
  timeToMarathon ±83 menit dan reward-nya ditahan (lihat §3).

### 2.4 Arti strategi verifier (RESMI — skema server live)

| Strategi | Makna resmi | Parameter |
|---|---|---|
| `first_responder` | "be first to verify" | tidak ada |
| `consensus_builder` | "fill verification gaps" | `maxSupporting` 1–10, bawaan 3 — "Disengage after this many supporting verifications already exist" |
| `economist` | "minimum reward threshold" | `minReward` 0,1–1,0 $TRUED, langkah 0,05, bawaan 0,6 — "Only verify if predicted reward is at least this amount" |
| `challenger` | "challenge verified answers" | tidak ada |

Bersama: `strategyType` bawaan skema = **economist**; `maxConcurrency`
1–10 (bawaan 1); `arenas`; `enabled`; `capabilityMenu`;
`pluginConfig.contextWindowTokens` (lantai praktis ±16.000 token untuk
Answer pendek, dari teks skema). Deskripsi resmi strategyType: "Strategy
for selecting answer verification opportunities. Disable Skip Deep
Evaluation to have the Verifier score each qualifying opportunity
itself."

### 2.5 Checklist yang dinilai (arena General, LIVE)

`verificationRules` arena (TERBUKTI-LIVE, teks penuh di
`general-verification-rules.json`): verdict_logic resmi —
'"compliant" if ALL four checks pass. "non-compliant" if ANY check
fails. Feedback must name the specific claim or gap that caused
failure.' Empat cek: **A_CITATION** (buka sumbernya; sumber ada tapi
tak mendukung klaim = gagal; tak bisa dibuka = unverified, bukan
fabrikasi; klasifikasi klaim Tier-0/time-critical/Tier-1/reasoning),
**A_REASONING** (harus ada mengapa/bagaimana; kesimpulan-tanpa-rantai
= gagal), **A_UNCERTAINTY** (klaim terkontestasi/spekulatif/probabilistik
wajib berkualifikasi; disajikan sebagai fakta pasti = gagal),
**A_SCOPE** (menjawab pertanyaan sebenarnya; melaporkan lingkungan
sendiri = gagal selalu). Forecasting memakai 6 cek AF_*; HLE 7 cek AH_*
(keduanya tertutup/escrow untuk kita — lihat §3).

---

## 3. EKONOMI LIVE (tarikan 2026-11-18 ±10:0x, TERBUKTI-LIVE)

Definisi yang terbukti dari aritmetika payload: `truedPerUnit` =
truedTotal ÷ **submitted** (bukan settled): economist General
257.456,74 ÷ 313.325 = 0,8217 persis. Jadi 0,82 adalah nilai harap
PER VERDICT TERKIRIM — sudah termasuk verdict yang tak pernah settle
dan yang meleset (keduanya bernilai 0).

### 3.1 Per arena (verifier, all-time)

| Arena | Strategi | Agent | Submitted | Settled | SR (sepakat/settled) | $/submitted | Total $ | Median/agent |
|---|---|---|---|---|---|---|---|---|
| general | economist | 11 | 313.325 | 183.063 | 90,9% | **0,8217** | 257.456,74 | **6.372,94** |
| general | consensus_builder | 3 | 42 | 39 | 94,9% | 0,6448 | 27,08 | 2,91 |
| general | first_responder / challenger | 0 | 0 | 0 | — | — | 0 | — |
| forecasting | economist | 8 | 20.779 | 14.358 | 88,6% | 0,8409 | 17.472,86 | 863,15 |
| forecasting | consensus_builder | 1 | 48 | 47 | 80,9% | 0,6358 | 30,52 | 30,52 |
| hle (admin) | economist | 8 | 14.977 | 14.454 | 97,3% | 0,8490 | 12.715,15 | 1.046,35 |

Pulse General: 312.214 verifikasi atas 277.282 jawaban (54.623 verified,
30.437 falsified). Forecasting: `rewardsDeferredToSettlement: true` —
$TRUED dibaca rendah menurut desain sampai Question resolve (escrow
bulan). HLE: semua peran admin — bukan arena kita.

### 3.2 Konsentrasi & volume

- Economist General memegang 313.325 dari 313.367 submission verifier
  teratribusi = **99,99%**. Di dalamnya timpang: rerata/agent 23.405 $
  vs median 6.373 $ → batas bawah aritmetika: 5 agent teratas dari 11
  memegang ≥85% total strategi (6 agent terbawah ≤6 × 6.373).
- Rezim volume sekarang = banjir: analitik berjendela (kohort
  pertanyaan) menaruh 273.285 submission economist pada kohort 7 hari
  terakhir dari 313.325 seumur platform — orde **30–40 rb verdict/hari
  platform** dalam rezim ini, hampir semuanya economist. Bukti papan
  (LAPANGAN, Nov): dua Verifier rumah bergerak +2,3–3,0 rb $/hari ≈
  2,8–3,7 rb verdict/hari per agent pada 0,82/unit. Median agent:
  6.373 $ seumur ≈ 7.757 verdict terkirim seumur (tenure per agent
  tidak terpublikasi — jangan dibaca sebagai laju harian).

### 3.3 Formula & matematika titik impas

- Formula esai resmi (DOKUMEN-RESMI via ledger, entri D-12):
  reward = max(0,1; √(2^(1−x))), x = urutan kedatangan → x=1: 1,0;
  x=2: 0,7071 (persis contoh kanonik "a Verification award is 0.7071"
  di docstring klien); x=3: 0,5; x=4: 0,3536. **TETAPI ledger sendiri
  menandai D-12 KONTRADIKTORI** (wiki reputasi: formula persis tidak
  ditetapkan publik), dan agregat live MEMBANTAH formula itu sebagai
  cerita utuh: total ÷ settled General = 1,4064 $ — di atas plafon
  formula 1,0 (Forecasting 1,2170; HLE 0,8797). Ada komponen lain
  (ronde marathon? bonus konsensus?) yang **BELUM-TERBUKTI**
  mekanismenya. Angka perencanaan yang sah = agregat live 0,8217/
  submitted, bukan formula.
- Biaya verdict yang meleset: **0 $TRUED** — tidak ada biaya/denda
  verifier di dokumen resmi mana pun, dan agregat konsisten dengan
  itu (verdict meleset = tidak dibayar, selesai). Yang dipertaruhkan
  verdict buruk bukan uang melainkan reputasi (lihat §4) + biaya
  komputasi kita sendiri. (Label: DOKUMEN-RESMI + bukti negatif;
  denda reputasi per verdict meleset tidak terkuantifikasi publik.)
- Titik impas $: karena meleset = 0 (bukan negatif), SEMUA SR > 0
  ber-EV positif dalam $TRUED. **PENEGASAN UKUR (vonis frontier §6
  Q5, wajib konsisten di seluruh peta):** 0,8217 adalah nilai
  TEREALISASI per verdict TERKIRIM pada campuran teramati — ia SUDAH
  memuat verdict yang meleset dan yang tak pernah settle, jadi EV
  per kiriman = 0,8217 dan TIDAK boleh dikali tingkat sepakat
  (0,909) sekali lagi. (Bila campuran kita kelak ber-SR lebih
  rendah, realisasi per kiriman turun sebanding — itu proyeksi
  campuran baru, bukan perkalian kedua atas 0,8217.) Titik impas
  yang sesungguhnya BUKAN di SR, melainkan di:
  (a) porsi yang tak pernah settle — adjudicationRate economist
  General hanya 58,4%: 41,6% pekerjaan tidak pernah berujung bayar;
  (b) anggaran relay model kita (5 req/menit bersama semua proyek —
  verdict berbantuan lane model memakan anggaran yang sama dengan
  pemeriksa Expert); (c) risiko reputasi akun (§4). Pada lane free
  (biaya $ nol), impas operasional = volume berapa pun yang tidak
  menggerus (b) dan (c).

---

## 4. RISIKO AKUN KITA

1. **Reputasi dipakai bersama.** Skor (scores) hidup di level USER:
   coins −1,8788, RAR 123 (reliability −5, availability 34,
   reputation 94), suspensionCount 5, Expertise general 0
   (TERBUKTI-LIVE, `scores-fresh.json`). Dokumen resmi: "Bad-faith
   engagement lowers an agent's RAR... escalating exclusion up to a
   permanent ban." Apakah disagreement-rate verifier yang buruk
   memotong reliability pool yang sama dengan yang dipakai Expert
   kita: **BELUM-TERBUKTI mekanismenya** — postur aman kit =
   perlakukan sebagai bersama. Akun ini sudah 5× suspensi; ambang ban
   permanen tidak terpublikasi. Ini risiko terbesar jalur 2, bukan
   biayanya.
2. **Self-dealing dicek di level pemilik** (DOKUMEN-RESMI):
   "a user cannot answer their own Question, nor verify their own
   Answer. These checks run on the owning user." Server menyaring
   penugasan; kit kita mencerminkannya SEBELUM draf (gerbang di
   `self_dealing_gate.py`, 6 sinyal) dan menambah kebijakan lebih
   ketat dari platform: tidak menilai Answer apa pun di 46 ISR yang
   pernah kita tanya (6) atau jawab (40) — termasuk Answer pesaing di
   pertanyaan yang kita jawab (menilai rival langsung dari Answer
   kita sendiri = konflik kepentingan nyata, walau tak dilarang
   platform secara eksplisit). Kebijakan ini pilihan kita, bisa
   dilonggarkan user, tercatat di `ours.json`.
3. **Tumpang-tindih dengan 27 revealed + batch Doktrin A**: jawaban
   kita duduk di kolam yang dinilai verifier lain; IVSP kita tidak
   pernah menyentuhnya (gerbang). Sebaliknya tidak ada jalur di mana
   verdict kita bisa membantu jawaban kita — self-dealing menutupnya
   dua arah.
4. **Anggaran bersama vs terpisah**: allowance polling gateway dihitung
   PER KREDENSIAL (DOKUMEN-RESMI) → kredensial IVSP terpisah = anggaran
   poll terpisah, tidak menggerus Expert. Caps belanja: baris per-agent
   (IVSP dapat barisnya sendiri) + cakupan node/akun yang menang-bila-
   lebih-ketat — cap akun akan mengikat keduanya. Apakah job verifikasi
   memakan `maxIsrs24h` (cap berlabel "questions answered"): server-
   side, **BELUM-TERBUKTI**; field cap klien semuanya berlabel jawaban.
   Anggaran relay CrowLLM (5 req/menit) TETAP bersama semua proyek —
   itu batas yang nyata untuk verdict berbantuan model.
5. **Klien stok tidak bisa menjalankan IVSP**: gerbang evaluate klien
   menolak semua pekerjaan non-ISR ("this Expert writes Answers, and
   this request is for {kind} work"). Bila penugasan verifikasi tiba
   sebagai evaluate-request, klien stok yang terhubung sebagai IVSP
   akan menolak semuanya; bila tiba sebagai execute-job langsung,
   `handle_job`-nya yang agnostik-jenis akan memprosesnya. Bentuk
   mana yang dipakai platform untuk IVSP: **BELUM-TERBUKTI** — inilah
   alasan runner jalur 2 adalah runner baru (bagian 5), bukan mode
   `trued.py`.

---

## 5. BANGUNAN SIAP — `provider/verifier/`

Dibangun mengikuti pola provider yang ada; semua di
`~/workspace/research/dialectica/provider/verifier/`:

| Berkas | Isi | Keadaan kunci |
|---|---|---|
| `verifier_common.py` | Klien baca API (GET saja) + parser murni: baris ISO → kandidat, record jobs (ISO/VFP), event gateway | tak ada helper tulis sama sekali |
| `self_dealing_gate.py` + `ours.json` | Gerbang konflik 6 sinyal; `ours.json` terbenih dari tarikan live (user id, 1 ISO terkonfirmasi isOwnAgent, 46 ISR) | murni, teruji |
| `verdict_drafter.py` | Drafter lokal mekanis 4 cek arena General (tier klaim, sitasi, penalaran, ketidakpastian, cakupan) | sumber tak terverifikasi = "unknown" → verdict maksimal "uncertain", tak pernah compliant semu |
| `lane_drafter.py` | Draf verdict multi-lane via klien CrowLLM yang ada: Nemotron `nvidia/nemotron-3.5-super-vl-120b-a12b:free` + qwen `qwen-3.8-max:free`; prompt publik saja (pagar relay); verdict dihitung ulang lokal dari per-cek; pembanding kesepakatan | pacing ≥13 dtk diwarisi dari `crowllm_checker` |
| `register_ivsp.py` | Stub registrasi tergating | TIGA kunci: env + berkas persetujuan berfrasa persis + konstanta kode `EXECUTE_ENABLED=False`; tanpa ketiganya hanya bisa menolak (exit 3) atau preflight-baca + cetak rencana (exit 4). Jalur eksekusi sengaja tidak dihubungkan di build ini |
| `run_verifier.py` | Runner; `--dry-run` bawaan (baca publik → gerbang → draf → log `verdict-drafts.jsonl`) | `--send` menolak tanpa syarat (exit 5) — jalur kirim belum ada, memang |
| `test_verifier_kit.py` | 33 tes unit | **33/33 hijau** |
| `README.md` | Cara jalan + cara go-live | — |

### Bukti kering (dry-run live read-only, 2026-11-18)

Sumber: pertanyaan General publik `3f831e33` (AI/wearables/integritas
akademik), 3 Answer revealed orang lain dinilai lokal + 2 lane
(rincian: `belajar-2026-11-18/peta-jalur-2/kalibrasi-lane-verdict.json`
+ `dryrun-evidence.json` + `verdict-drafts.jsonl`):

| Answer | Lokal | Nemotron | qwen | Sepakat? |
|---|---|---|---|---|
| 91765e79 (14.007 kar) | non-compliant (A_CITATION) | non-compliant (A_CITATION) | non-compliant (A_CITATION) | **unanim 3/3, cek pemicu sama** |
| a467904f (3.371 kar) | uncertain (A_CITATION unknown) | compliant 4/4 | compliant 4/4 | lane sepakat; lokal abstain-naik sesuai desain |
| 54d58e01 (94 kar, jawaban menolak) | non-compliant (A_REASONING+A_SCOPE) | non-compliant (+A_CITATION) | non-compliant (4/4 fail) | unanim verdict; beda di cek pinggiran |

- Ketersediaan lane 6/6; latensi Nemotron 21–37 dtk, qwen ±3 dtk.
- Gerbang: Answer kita sendiri (8300bcbe) DITOLAK dengan 5 sinyal
  menyala sekaligus; Answer orang di pertanyaan kita (64bd68ac)
  DITOLAK dengan 2 sinyal. Kandidat orang lain di pertanyaan orang:
  lolos.
- Peringatan kalibrasi yang jujur: 91765e79 sudah didukung 1 verifier
  panel (supported 1, refuted 0) sementara 3/3 drafter kita
  non-compliant A_CITATION — selera panel nyata bisa lebih longgar
  daripada checklist ketat. Bahan mentah pertanyaan postur Q2 di
  paket frontier; bukan alasan melonggarkan gerbang tanpa data.

### SISA LANGKAH SAAT USER BANGUN (berhenti di gerbang user)

1. **Kata jalan user untuk Jalur 2** — keputusan; tidak ada langkah
   teknis sebelumnya yang boleh jalan tanpa ini.
2. **Cek mata panel website** (nol risiko, 1 menit): buka
   `https://dialectica.xyz/agents` — apakah pembuatan Verifier
   ditawarkan ke akun kita (baris launch-phase lama sudah hilang?).
   Hasilnya menutup pertanyaan gerbang akun di §1.2 tanpa mencoba
   registrasi.
3. **Registrasi IVSP** (langkah tergating, user hadir): buat
   `provider/verifier/USER-APPROVAL-IVSP.txt` berisi persis
   `SAYA SETUJU REGISTRASI IVSP`, `DIALECTICA_IVSP_USER_APPROVED=1`,
   flip `EXECUTE_ENABLED` di `register_ivsp.py`, hubungkan +
   review jalur eksekusinya di sesi yang sama, jalankan → simpan
   kredensial ke `~/.dialectica-ivsp/agent.json` (0600). Penolakan
   yang mungkin muncul (WAITLIST_PENDING versi IVSP) adalah jawaban
   resmi atas status gerbang — catat apa adanya.
4. **Konfigurasi IVSP**: strategi `economist`, arenas `general`,
   `minReward` **0,6**, `maxConcurrency` 1 — lewat
   panel website atau API configure dengan skema `matrix-ivsp`.
   JANGAN lewat `trued.py` (tidak bisa me-resolve IVSP).
   Kombinasi economist + minReward 0,6 + general adalah
   **DEFAULT-USULAN** vonis frontier (§6 Q1/Q3): usulan tertulis
   yang sudah ditimbang dua kursi frontier, BUKAN keputusan —
   keputusan final tetap di gerbang user pada langkah 1–3.
5. **GERBANG URUTAN (vonis frontier Q4, §6)**: registrasi (langkah
   3) boleh disiapkan, tetapi **arming mode kirim DITAHAN** sampai
   jalur Expert terbukti dibayar — bukti yang ditunggu: mini-batch
   3 / doktrin Expert menghasilkan verified terbayar pertama.
   Dry-run draf verifier tetap jalan dari sekarang; yang ditahan
   hanya kirim live. Paralel live penuh (Expert + verifier
   sama-sama live) bersyarat ganda: Expert bersih-positif stabil
   DAN pilot verifier terkendali bersih-positif. Sesudah gerbang
   urutan lolos: **sambungkan runner ke sumber kerja live**
   (gateway dari rumah kredensial baru) + tulis jalur kirim
   verdict sebagai pekerjaan terpisah yang di-review, dengan
   kill-metric: disagreement-rate dan reliability dibaca ulang
   sesudah 25 verdict pertama; berhenti bila reliability bergerak
   negatif.

---

## 6. VONIS FRONTIER & PERUBAHANNYA

Konsultasi TUNTAS 2026-11-18 10:15–10:21 WIB (F-31D). Kursi:
**duck.ai GPT-6 Luna** (penasihat utama, browser cloud) +
**gpt-5.6-sol** (co-advisor, CrowLLM). Otoritas:
`belajar-2026-11-18/frontier-jalur2/SINTESIS-FRONTIER-JALUR2.md`;
jawaban mentah kedua kursi di folder yang sama (`duck-answer.md`,
`sol-answer.md`); paket: `FRONTIER-PAKET-JALUR2.md`.

**Penengah gemini-3.1-pro TIDAK dipanggil** — alasannya tercatat di
sintesis: tidak ada perpecahan level-keputusan. Kedua kursi searah
di kelima pertanyaan; satu-satunya perbedaan (nuansa Q2 di bawah)
adalah catatan sinyal, bukan sengketa yang butuh penengah.

### Q1 — Strategi masuk: ECONOMIST, minReward 0,6 (KONVERGEN)

- Kedua kursi: masuk sebagai **economist** dengan ambang bawaan
  **minReward 0,6**.
- `consensus_builder` DITOLAK sebagai strategi utama: sampelnya
  (42 submission) tak sahih untuk digeneralisasi + bayarannya lebih
  rendah (0,64/unit).
- `first_responder` **DITOLAK KERAS oleh dua kursi**: kolam kosong
  BUKAN peluang — agent rumah punya latensi yang tak bisa disaingi
  relay model multi-lane kita. Itu jebakan kecepatan, bukan celah.
- Pembatal terukur (kapan vonis ini dievaluasi ulang): bila dalam
  ≤14 hari economist per unit turun **< 0,50** (ambang sol) ATAU
  bersih per jam-operator economist < gap-filling (ambang duck).
- **Perubahan pada peta:** rekomendasi sementara pekerja
  (economist/0,6) TERKONFIRMASI dan kini mengeras jadi
  DEFAULT-USULAN tertulis di §5 langkah 4 + README kit — tetap
  usulan, keputusan final di gerbang user saat registrasi.
  `first_responder` resmi DITUTUP sebagai strategi masuk (bukan
  sekadar "0 agent aktif" seperti bunyi §3.1).

### Q2 — Postur verdict: KETAT, abstain pada ambigu (KONVERGEN + 1 nuansa)

- Kedua kursi: postur **KETAT** pada checklist 4 cek (§2.5).
  Verdict paksa pada kasus ambigu **DILARANG** — abstain / draf
  saja. Duck menyatakannya eksplisit; desain runner kita (multi-
  lane + abstain-naik) dinilai sesuai.
- **Nuansa sol (dicatat, BUKAN sengketa):** antisipasi konsensus
  boleh dipakai sebagai SINYAL keyakinan — dicatat sebagai sinyal,
  tidak pernah menjadi pengemudi verdict. Checklist yang memutus,
  bukan tebakan arah panel. (Ini juga menjawab peringatan kalibrasi
  di §5: selera panel yang lebih longgar TIDAK melonggarkan
  gerbang kita; ia hanya boleh tercatat sebagai sinyal.)
- Alasan penguat dari dua kursi: reputasi dipakai bersama di level
  user (§4 butir 1) — verdict ceroboh membayar dengan mata uang
  yang sama dengan yang dipakai Expert kita.
- **Perubahan pada peta/kit:** aturan abstain DIPERTEGAS di README
  kit sebagai aturan desain tertulis: ketidaksepakatan lane pada
  kasus ambigu = TIDAK ADA verdict (bukan mayoritas paksa).

### Q3 — Arena pertama: GENERAL (KONVERGEN)

- Kedua kursi: **General** dulu. Selisih bayaran Forecasting
  (0,8409 vs 0,8217/unit ≈ 0,02) tidak pernah sepadan dengan
  escrow berbulan-bulan (`rewardsDeferredToSettlement`, §3.1)
  untuk tujuan yang sebenarnya: membuktikan jalur ini hidup
  secepat mungkin.
- **Perubahan pada peta:** §5 langkah 4 mengunci arena `general`
  sebagai default-usulan; Forecasting ditunda sampai jalur terbukti
  di General — bukan arena pembuka.

### Q4 — Urutan vs jalur Expert: SEKUENSIAL untuk live (KONVERGEN)

- Kedua kursi: operasi **live** verifier hanya sesudah doktrin
  Expert terbukti dibayar. Dry-run draf verifier tetap jalan dari
  sekarang (dan memang sudah, §5).
- Paralel live hanya bersyarat ganda: Expert bersih-positif
  stabil + pilot verifier terkendali bersih-positif.
- **Perubahan pada peta:** §5 kini memuat GERBANG URUTAN eksplisit
  (langkah 5): registrasi boleh disiapkan, arming mode kirim
  menunggu bukti Expert terbukti dibayar (mini-batch 3/doktrin).
  Registrasi sendiri tetap langkah gerbang user (langkah 1–3
  tidak berubah).

### Q5 — Skala: PILOT TERBATAS TERUKUR, bukan asumsi bisnis (KONVERGEN)

- Kedua kursi: perlakukan jalur ini sebagai **pilot terbatas
  terukur** (kerangka uji 14 hari dengan pembatal Q1), bukan
  asumsi bisnis yang sudah jadi.
- **CATATAN UKUR DUCK (sudah dilipat ke §3.3):** 0,8217/unit dari
  analitik adalah rata-rata TEREALISASI per verdict TERKIRIM —
  sudah memuat yang meleset — jadi EV per kiriman = 0,8217 dan
  JANGAN dikali 0,909 lagi. Redaksi ekonomi peta diselaraskan ke
  pembacaan ini di semua tempat.
- Perkiraan sol (±200 verdict/hari untuk menutup overhead
  infrastruktur multi-lane, pada asumsi biayanya) diperlakukan
  sebagai **HIPOTESIS BIAYA** yang harus diukur dari log biaya
  kita sendiri — bukan fakta, bukan target.
- Median seumur 6.373 tanpa basis waktu ≠ bukti untung harian
  (sudah sejalan peringatan §3.2).
- **Perubahan pada kit:** kebutuhan pencatatan biaya model per
  verdict ditambahkan ke README kit sebagai syarat ukur titik
  impas uji 14 hari — dan karena kode runner saat ini BELUM
  mencatatnya, ia tertulis di sana sebagai KEKURANGAN TERCATAT,
  bukan fitur yang diklaim ada.

### Ringkasan perubahan yang ditimbulkan vonis ini

1. §5 langkah 4: default-usulan tertulis (economist / 0,6 /
   general) — gerbang keputusan user tidak berubah.
2. README kit: aturan abstain dipertegas (beda lane pada kasus
   ambigu = tidak ada verdict).
3. §5 langkah 5: gerbang urutan Q4 (arming menunggu Expert
   terbukti dibayar).
4. README kit: butir ukur biaya per verdict + kekurangan tercatat.
5. §3.3: penegasan ukur 0,8217 (terealisasi per kiriman; tanpa
   perkalian sepakat kedua).
6. `first_responder` ditutup sebagai strategi masuk; Forecasting
   ditunda sebagai arena pembuka.

---

## 7. PERTANYAAN TERBUKA (hanya bisa dijawab dengan mencoba — dan risikonya)

1. Apakah `POST /api/node/agents/matrix {"type":"IVSP"}` diterima
   dari sesi kita? Risiko mencoba: rendah-sedang — percobaan yang
   ditolak tidak mengubah apa pun; percobaan yang DITERIMA membuat
   agent baru (bisa di-disable; belum pernah ada bukti bisa dihapus
   permanen). Hanya lewat gerbang §5 langkah 3.
2. Apakah ada gerbang akses IVSP per-akun (padanan WAITLIST_PENDING)?
   Risiko: sama dengan #1 — jawabannya justru datang dari percobaan
   itu.
3. Bentuk penugasan verifikasi: evaluate-request atau execute-job
   langsung? Menentukan apakah runner harus menjawab penawaran ±30
   detik. Risiko mencoba: nol verdict — cukup connect dan amati
   (sesudah registrasi + kata jalan).
4. Format keluaran verdict literal di prompt job server. Risiko:
   nol — terbaca dari job pertama; schema-correction adalah jalur
   perbaikan resminya bila format awal meleset (koreksi yang gagal
   berulang membakar reliability — mitigasi: verdict pertama =
   volume 1, diawasi manusia).
5. Komponen reward di atas formula esai (agregat 1,41/settled >
   plafon 1,0). Risiko: nol — terbaca dari riwayat reward sendiri
   sesudah verdict pertama settle.
6. Efek disagreement terhadap reliability/RAR user. Risiko mencoba:
   NYATA — hanya terukur dari verdict yang benar-benar dinilai;
   mitigasi kill-metric §5 langkah 5 (baca ulang sesudah 25 verdict).
7. Apakah job verifikasi memakan cap `maxIsrs24h` agent atau cap
   akun. Risiko: nol-sedang — terbaca dari usage endpoint sesudah
   job pertama.

---

## Lampiran — sumber

Mentah live (2026-11-18): `belajar-2026-11-18/peta-jalur-2/` —
agents-live, schema-matrix-ivsp + 4 per-strategi, analytics 3 arena
(all + berjendela 7d/30d/90d), arenas-fresh, general/forecasting
verification-rules, scores-fresh, notifications (di peta-earn/),
our-jobs, our-opportunity-filters, dryrun-samples, dryrun-evidence,
kalibrasi-lane-verdict. Dokumen resmi: references/{api,arenas,
rules-of-the-game}.md + SKILL.md + scripts/trued.py v0.22.4.
Lapangan: MEKANISME-DAN-LAPANGAN.md (§aturan agregasi, D-12,
sejarah gerbang IVSP) — ditandai LAPANGAN di setiap pemakaian.
