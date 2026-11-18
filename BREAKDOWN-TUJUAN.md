# Dialectica — Breakdown Tujuan & Cara Garap (2026-11-08, data LIVE ditarik sendiri)

Sumber: rules-of-the-game.md + arenas.md + api.md (klien resmi teraudit), endpoint
live /api/node/arenas/general/analytics, /api/node/leaderboard, /api/node/isrs,
/api/node/agents/<kita>/opportunities, /api/node/arenas/general (answerRules resmi),
log serve smoke 2026-11-08. Angka di bawah = bacaan live, bukan klaim channel.

## 1. Apa ini & tujuan KITA
Marketplace pengetahuan terverifikasi: Customer bertanya (Question), Expert menjawab
(Answer), Verifier independen mencoba MEMBANTAAH. Jawaban yang selamat = Verified
Answer → jadi halaman Wiki permanen. Reward = $TRUED (poin internal; konversi token
TBA menurut pihak ketiga; TIDAK ada harga/kontrak/pool terpublikasi — vonis lama
tetap: tiket lotre murah, bukan pendapatan).
Tujuan kita: (a) posisi awal murah SEKARANG mumpung platform sepi (leaderboard cuma
10 baris, 7 di antaranya agent RUMAH; manusia asli cuma 3); (b) bangun saldo $TRUED +
Expertise + Marathon wins dari jalur Expert; (c) revisi berbasis data tiap siklus
sampai ada kejelasan tokenomics — baru diputuskan grind penuh atau stop.

## 2. Peta lapangan (live)
- Arena: general (terbuka), hle (benchmark, tertutup), forecasting (tanya tertutup).
- Pulse General: 729 Question, 0 unanswered, 728 punya Verified Answer;
  10.962 Answer, 3.815 verified, 3.004 falsified, 20.673 verifikasi.
- Waktu: jawaban pertama ±2,8 dtk; verified ±85 dtk; marathon ±8,4 mnt;
  rata-rata 6 Answer masuk sebelum ada yang verified; 3 verifikasi per Verified.
- Korpus total 2.980 Question (semua arena). "Settled" di General TIDAK menutup
  pertanyaan — Marathon baru bisa dimenangkan sesudahnya.
- 27 opportunity terbuka ≤24 jam untuk Expert kita; semuanya settled/marathon
  (slot innovation_focus: butuh ≥2 Verified Answer yang sudah ada, maks 6).

## 3. Leaderboard (live, /api/node/leaderboard — HANYA top 10)
#1 Dialectica (Pioneer) 49.423 — rumah, marathon wins 1.826
#2 Dialectica (Innovator) 34.449 — rumah, 1.808
#3 Dialectica (Late Entry) 32.006 — rumah, 1.613
#4 Dialectica (Endgame) 30.349 — rumah, 1.705
#5 Verifier B 20.781 — rumah (verifier)
#6 Verifier A 19.681 — rumah (verifier)
#7 Dialectica (Early Follower) 6.173 — rumah, 230
#8 Adam Reinhard 3.682 — MANUSIA, 247
#9 Añoñi ;-) 3.672 — MANUSIA, 181
#10 Federico Collarte 2.139 — founder, 122
Kita: coins 0, rank 0 (belum masuk papan). Ambang papan = 2.139 (= founder sendiri).
Catatan: reliability SEMUA papan negatif (-3 s/d -209) — reliabilitas bukan
pembeda rank; yang membedakan = coins dari Marathon wins + volume verifikasi.

## 4. Ekonomi per strategi (live, General, all-time)
EXPERT:
- innovation_focus: 32 agent, SR 65,7%, 9.233 TRUED, 4,28/submitted-settled,
  median/agent 27 — STRATEGI TERBAIK per kualitas. (Kita SUDAH pindah ke sini
  2026-11-08 19:2x, terverifikasi via agent show: strategyN=2, maxVisos=6.)
- pioneer: 114 agent, SR 56,7%, total terbesar 30.869 (5,92/unit) tapi marathon
  rate cuma 13,1% — ramai + kompetitif.
- endgame: SR 57,3%, 3,36/unit, median/agent 81.
- early_follower: SR 49,4% (paling buruk di antara yang serius), 5,66/unit.
- dynamic (bekas kita): SR 41,3% TERENDAH, median/agent −1 — strategi pecundang;
  pantas ditinggalkan.
VERIFIER:
- economist: 7 agent, 20.667 verifikasi, SR 93,9%, 17.510 TRUED, 0,85/unit,
  2.501/agent — jalur VOLUME. Butuh agent Verifier (IVSP) — pembuatan Verifier
  BELUM terbuka untuk akun kita (pesan dashboard saat signup). Pantau.
ASKING: pertanyaan unik +1 TRUED; tiap Answer lolos NIU +1 lagi; fee naik
kubik ke plafon 10 (n=1 gratis). Self-dealing dilarang di level user.

## 5. Kenapa Answer MATI (live — ini kurikulum kita)
Penolakan: surprise_gauge 6.817 (jawaban ngulang yang sudah ada — penyebab #1),
arena_rules 4.909, customer_requirements 339.
Aturan gagal: A_CITATION 2.241, A_REASONING 596, A_SCOPE 494, A_UNCERTAINTY 358.
A_CITATION resmi: klaim reportase WAJIB sitasi sumber yang bisa diidentifikasi
jelas + mendukung klaim saat dicek; gaya APA + URL diutamakan; teks dari
Question BUKAN sumber.
Konsekuensi desain: (a) jangan bikin sitasi palsu — cleaner sitasi di wrapper
membersihkan URL/DOI/atribusi jurnal karangan + nota kejujuran (smoke LOLOS
2026-11-08: 11 sitasi palsu kesapu dari draf uji GLM); (b) prompt dunia-data
(forecast/terkini) di-grounding via Gemini (retrieval asli), sisanya GLM bersih;
(c) targetkan sudut yang BELUM dijawab (Surprise Gauge) — baca Answer yang sudah
verified dulu sebelum nulis; (d) nyatakan ketidakpastian terkalibrasi.

## 6. Cara kerjanya (rutinitas kita)
1. Serve jalan dengan strategi innovation_focus (push-based; orchestrator yang
   nawarin kerja — BUKAN dynamic yang harus berburu sendiri).
2. Mesin: Vyce GLM 5.3 Flash (kuota promo 10 jt token/hari) + cleaner sitasi;
   Gemini = grounding untuk prompt data-dunia + cadangan.
3. Caps 3 job/24 jam (dinaikkan bertahap hanya bila SR data kita ≥55%).
4. Siklus revisi: tiap serve selesai → baca hasil (verified/falsified + alasan
   aturan), bandingkan vs benchmark arena (SR 65,7% innovation_focus), revisi
   prompt/wrapper, catat. Gagal berulang di aturan yang sama = ubah pendekatan.
5. Risiko terukur: job diambil WAJIB selesai — abandon = reliability turun
   (bukti: job Gemini 80933caf drop karena kuota 429; reliability kita masih 0
   karena server belum abandon ±30 mnt; dihitung sebagai pelajaran, bukan diulang).
6. Jalur samping (nanti): Verifier economist bila pembuatan Verifier dibuka;
   Asking +1/pertanyaan (fee n=1 gratis, berikutnya naik — hemat, jangan spam).

## 7. Keuntungan kita (jujur, per doktrin worth)
- Yang TERBUKTI: nol biaya riil (kuota gratis dua provider), posisi di platform
  yang papan atasnya masih 70% agent rumah — jendela early-mover nyata.
- Yang BELUM terbukti: nilai $TRUED (belum ada harga/konversi/TGE resmi).
- Maka: garap = akumulasi posisi + belajar murah; BUKAN grind buta. Bila
  tokenomics resmi muncul → breakdown ulang → putuskan lanjut/stop dengan data.
- Target realistis tahap 1: Verified Answer pertama + Marathon win pertama;
  tahap 2: coins > 2.139 (masuk papan, ngalahin founder); tahap 3: kejar
  manusia #8/#9 (±3.600) — perlu ±ratusan Verified/Marathon pada laju
  4,28 TRUED/unit innovation_focus → ini maraton berminggu-minggu, bukan sprint.

## 8. Status eksekusi saat file ini ditulis (2026-11-08 ±19:35 WIB)
- Strategi agent: innovation_focus ✓ (agent show terverifikasi).
- Serve Gemini lama: DIMATIKAN manual (SIGTERM) supaya slot bebas — job drop
  tidak bertambah; status akhir tercatat di log proses.
- Wrapper: cleaner sitasi AKTIF di Vyce + Gemini; grounding Gemini untuk
  prompt data-dunia; launcher run_serve.py default Vyce (--gemini = cadangan).
- Serve Vyce pertama dengan strategi baru: SIAP JALAN (keputusan gas = user,
  sesuai pola serve sebelumnya).


## 9. ADDENDUM FORENSIK 19:45–19:57 — kenapa 3 jawaban ABANDONED (bukti API)
Tarik /api/node/isos per pertanyaan: TIGA jawaban kita, SEMUA status "abandoned",
verifierCount 0, isi KOSONG (tidak pernah terekam server):
1. Gemini 19:04 — Q token Dialectica (General, skema klasik {"answer"}).
2. Vyce job 6257 — "Which artist will be named Spotify's most-streamed global
   artist of 2026?" — FORECASTING multiple_choice.
3. Vyce job 8cad — "Will the 2026 Brazilian presidential election require a
   second-round runoff?" — FORECASTING binary.
AKAR: (a) strategi innovation_focus TIDAK membatasi arena — orchestrator
menawari Forecasting, yang skemanya BEDA TOTAL (wajib answerType, outcomeType,
prediction, confidence 0–100, reasoning; binary prediction pola Yes/No/True/
False/1/0; numeric wajib credibleInterval). Wrapper mengirim esai markdown →
gagal validasi → schema-correction → generate ulang → tetap gagal → jendela
liveness habis → abandoned → slash REL-005. (b) submit 629 char = satu generasi
rusak di tengah loop. (c) Gemini job 1: kuota 429 (penyebab terpisah, sudah jelas).
FIX (dibangun + smoke LOLOS 19:5x): format gate v2 di vyce_provider.py —
deteksi tuntutan skema (json/schema/structured_data/outcomeType), ekstrak objek
JSON terluar, unwrap structured_data, normalisasi confidence 0–1 → 0–100,
kembalikan HANYA objek itu. Tes forecasting multiple_choice: kelima field wajib
hadir, prediction valid. PLUS rantai fallback kunci Gemini diperbaiki
(GEMINI_KEY_FALLBACK dari launcher) supaya grounding tidak mati diam-diam.
ATURAN BARU: serve berikutnya = caps 1, pantau SATU job sampai ada status
terekam server (bukan "submitted" versi klien), baru lanjut.

## 10. ADDENDUM AKAR — forensik web (2026-11-08 ±19:48, sumber primer)
- STATUS PROYEK: "We're pre-seed. The MVP is live." (halaman careers resmi).
  2 lowongan founding, Sydney/Bay Area. TIDAK ada putaran pendanaan Dialectica
  di mana pun (RootData/Crunchbase/Tracxn kosong).
- "Raised from Sequoia" = MILIK BARAJA (perusahaan founder SEBELUMNYA):
  Series A $32 jt, 3 Jan 2019, Sequoia China + Blackbird + Main Sequence,
  Federico Collarte CEO Baraja saat itu. Bukan Dialectica. Identitas orang
  yang sama terverifikasi via Datanyze.
- @flostat3 / ex-Stacker Ventures: TIDAK terverifikasi (3 pencarian nihil).
- WHITEPAPER: cuma 3 dokumen. "A Beautiful Game" (2025): multilateral
  proof-of-work, provider + min 2 verifier, reward terbesar ke provider DAN
  verifier awal, sisanya menurun eksponensial; tangga hukuman = reputasi
  negatif → suspensi sementara → expulsion (persis yang kita alami).
  Esai scarcity (27 Feb 2026): minting $TRUED digerbang Surprise Gauge
  I(x)=−log2 P(x); TIDAK ada cap supply di mana pun.
- TABEL REWARD RESMI (esai + /why + /earn — MENGGANTIKAN klaim channel):
  Pioneer +20 (1 per Question selamanya, tetap milik walau nanti falsified,
  di luar Forecasting); Innovator (novel verified) +10; Marathon winner +10;
  Verifier +max(0,1, sqrt(2^(1−x))) menurut URUTAN KEDATANGAN x; Question
  unik +1; Discovery +1; falsified −1. Verified-tapi-tidak-novel = 0.
  <15% konten baru = Paraphrasing, tidak verified. Verified = 2 verifikasi
  mendukung; 1 membantah = falsified.
- $TRUED: FAQ /why — "On-chain export is currently unavailable"; panduan Earn:
  Wallet tab "has room for a wallet on the Base network", konversi "Coming
  soon", tombol mati. TIDAK ada kontrak/market (DexScreener: nol hasil TRUED;
  GeckoTerminal cuma koin tak berhubungan). WASPADA tiruan: "TRUED" Trumpet
  Doge (BSC, meme 2022) + Trueo $TRUE di Base (eks-Truemarkets) — BUKAN proyek ini.
- KOREKSI atas breakdown pertama kita: klaim "blog mengakui kontrak unaudited
  alpha" TIDAK ditemukan di sumber mana pun — yang benar: tidak ada kontrak,
  audit, atau pengungkapan keamanan yang dipublikasikan sama sekali.
- SKORING: tidak ada halaman "Scoring" di nav situs; aturan hidup di dokumen
  skill GitHub (repo TUNGGAL org dialectica-xyz, 1 commit squash 7 Nov 2026).
  Daftar pukulan reliabilitas di SKILL.md: early stop, DROPPED, REJECT,
  abandon 15 menit, kegagalan berulang. Panduan Earn resmi: "Reliability
  drops if an Answer is started and never delivered." Formula RAR numerik /
  ambang suspensi TIDAK dipublikasikan di mana pun.
- X resmi @DialecticaXYZ: gabung Jan 2026, 220 followers, 504 post; pinned
  30 Okt 2026 = pengumuman Earn "Pre-launch". Blog cuma 2 post (2 & 5 Nov 2026).
  Telegram resmi t.me/dialectica_chat. Discord: tidak ada.
- IMPLIKASI OPERASI: (1) duit Expert ada di NOVELTY + Pioneer + Marathon,
  bukan volume jawaban biasa (yang tidak novel = 0); (2) reward Verifier
  menurun menurut urutan kedatangan → first-responder paling mahal per unit —
  memperkuat tesis celah Verifier; (3) vonis worth TIDAK berubah: pre-seed,
  tanpa token/pool/tanggal — tiket lotre murah, akumulasi pelan, biaya ~nol.


## §12 Addendum — 20:03 WIB: Serve diagnostik SEMUANYA ABANDONED, penyebab akhir terbukti
- Serve diagnostik (izin user, caps 1): 3 bid di-accept, 3 job DIKERJAKAN — format gate menelan schema-correction 3× dan klien melaporkan "Submitted expert answer" — tapi verifikasi server: SEMUA abandoned, isi kosong. /api/node/profile menegaskan: **RAR −6, penalties 6, Expert 6 ITEMS, $TRUED 0, Expertise 0**.
- Bandingkan: pola sebelumnya caps 3 (3 item) vs sekarang caps 1 (6 item) → **caps BUKAN penghitung item serve; cap = jawaban yang ter-SETTLE**, dan orchestrator terus menawari selama serve hidup. "Diagnostik caps 1" itu ilusi kontrol.
- Server EXPERT_ITEMS (6 row, selesai urut): 9ded7dc1 (submit 19:53:08Z), 67601b78 (19:53:33Z), 97cfe468 (19:55:28Z), 78129050 (20:00:06Z), 8200fa4d (20:02:03Z), e4b3e3c5 (20:03:15Z). Status: semuanya **abandoned**, **answersAccepted 0**, **verifierCount 0**, createdAt == updatedAt (tidak pernah ada write). Satu row (e4b3e3c5) punya field unik **runtimeContext** (platform mem-BAKE requirement runtime ke ISR, tidak menampilkannya ke klien) — runtimeContext.image **"dind:node-mcp"** + URDF: job ini menuntut EKSEKUSI runtime/Robotics yang tidak dimiliki provider teks.
- **Bukti rantai transport (decisive)**: TIDAK ADA SATU PUN room Matrix di ~/.dialectica/matrix — file yang ada HANYA state.db (SQLite 53.248 byte, dimodifikasi 20:05). Tidak ada ruang jawaban yang pernah dibuat di klien ini → jawaban tidak pernah benar-benar dikirim sebagai pesan room; "Answer delivered" versi log = upaya SUBMIT klien lokal, bukan konfirmasi transport. Ini meruntuhkan asumsi §9–§11 bahwa jawaban "masuk tapi ditolak skema": yang terbukti sekarang = jawaban tidak pernah ter-deliver.
- Sanksi sama sekali TIDAK muncul di /notifications (daftar kosong total), nol penyebutan di changelog & blog resmi → **REL-005 = reliabilitas murni server-side, penjelasannya tidak dipublikasikan di mana pun** (konfirmasi negatif).
- **Kondisi akun per 20:0x**: RAR **−6** (pelanggaran terdokumentasi publik: reliabilitas buruk → suspensi menaik → ban permanen), penalties **6**, $TRUED **0**. Serve TERHENTI (window habis; TIDAK dihidupkan lagi). Standar serve baru (aturan permanen): bukti transport (room/MessageEvent) + status item server-side terbaca SEBELUM serve apa pun berikutnya; serve tanpa itu = dilarang.


## §12 KOREKSI (20:2x WIB — perintah user: pelajari mekanisme + cara user terbaik dulu)
§12 versi awal mengandung klaim yang DITARIK: "~/.dialectica/matrix hanya state.db, nol room" = path yang tidak pernah ada (room hidup di homeserver remote); "jawaban tidak pernah ter-deliver" diturunkan dari kepastian menjadi TIDAK TERBUKTI — yang terbukti: server tidak pernah mencatat jawaban (createdAt==updatedAt, accepted 0) DAN koneksi selalu mati di tengah siklus (serve #1 dibunuh manual 19:28, #2 dibunuh manual 19:46, diagnostik dipotong timeout eksekusi 1.200 dtk; exit code serve tidak pernah tertangkap karena launcher tanpa pemeriksaan). Studi mekanisme penuh + data lapangan + GERBANG SERVE permanen: MEKANISME-DAN-LAPANGAN.md. Temuan kunci: arenas=(all) membiarkan jebakan Forecasting masuk (tuas resmi: agent set arenas=general); pola resmi satu jawaban = `trued answer <isrId>` (end-by-itself + exit code), BUKAN serve open-ended; leaderboard didominasi expertise HLE (tertutup/admin) + Verifier murni di #5/#6; reliabilitas negatif di semua baris papan (rank = koin, bukan reliabilitas).
