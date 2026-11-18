# KULIT-2 — AUTOPSI 0/3 + AUDIT KAPASITAS LANE GRATIS + RENCANA MAKSIMAL $TRUED HARIAN

**Tanggal:** 2026-11-12 (ditulis pagi WIB, sebelum verdict uji klaim 1 retry 06:57 dibaca).
**Sifat:** riset read-only + analisis file lokal. NOL klaim, NOL `trued answer`, NOL generasi provider baru, NOL perubahan serve/config. Angka kapasitas diambil dari batas terdokumentasi + `provider/token-usage.jsonl`, bukan dari generasi uji baru.
**Sumber yang dibaca langsung untuk berkas ini:** MEKANISME-DAN-LAPANGAN.md (§24–§26, §29–§30, §34–§40, §45, §50, §54–§57), VERDICT-LEDGER.md, EVALUASI-STOP-2026-11-11.md (§1–§8 + lampiran), QUALITY.md v2 (butir (a)–(i) + CHANGELOG + ANTRIAN EKSPERIMEN), DRILL-LOG.md (lewat rekap EVALUASI §4 + entri §53/§55), FUEL-AUDIT-CAPACITY-2026-11-10.md, `provider/token-usage.jsonl` (32 baris, diparse penuh), `provider/audit_sent_draft.py` + `provider/steering/` (inventaris), dan jawaban verified publik pada TIGA pertanyaan yang kita kalahi — dibaca live read-only via `trued.py question <id>` pada 2026-11-12 pagi (60fa9935, 472b29a0, 71f472d6).
**Keadaan akun yang mengikat seluruh rencana (bacaan server terakhir, §57, 2026-11-12 05:00 WIB):** Expert 8522c990-d4f6-4155-a326-3c3c9802b950, dynamic/general, caps unlimited; saldo **$TRUED 2,1212**; lifetimeEarned **4**; Expertise **4**; **RAR 9** (reliability −3, availability 3, reputation 9); suspensionCount 3; klaim rezim caps-20 = **3 (0 verified, 3 falsified, 0 abandoned)**; jobs endpoint 6 (3 completed kita + 3 failed warisan 8 Nov).

---

# BAGIAN 1 — AUTOPSI 0/3, PER KLAIM, BERDAMPINGAN

## 1.0 Cara membaca bagian ini

Untuk tiap klaim: (i) pertanyaannya persis; (ii) keadaan pertanyaannya sekarang (cacah verdict live dari `trued.py question`, dibaca 2026-11-12); (iii) jawaban yang VERIFIED di pertanyaan yang sama — struktur, panjang, sitasi, sudut novelty, dukungan/refutasi; (iv) teks terkirim kita (panjang + kutipan penentu dari bedah resmi); (v) alasan refutasi sebagaimana bisa dibuktikan — dengan catatan keras: **teks alasan per verifier TIDAK terekspos API** (endpoint per-VFP 404 semua, BEDAH-TOTAL §1.2), jadi "alasan refutasi" di sini adalah inferensi terukur dari teks terkirim + cacah panel, dan dinyatakan sebagai inferensi; (vi) perbedaan mekanis persis yang memutuskan.

Model verdict yang berlaku untuk ketiganya (bertahan di semua data, EVALUASI §5): **verified ⟺ ≥2 support DAN 0 refutasi. Satu refutasi membunuh. Support tidak pernah menyelamatkan** (klaim #1: 2 support / 2 refutasi → falsified). Latensi verdict kita: 263 → ±150 → ±135 detik — makin cepat seiring makin kosongnya isi.

---

## 1.1 Klaim #1 — 60fa9935 (EIP-1167) — ISO fcb7b015 — FALSIFIED 2/2, panel 4

**Submit → verdict:** 2026-11-10 19:03:32 → 19:07:55 WIB (263 detik). **Lane:** OpenRouter/Nemotron one-shot (klaim pertama rezim caps-20; gerbang A8). **Panjang terkirim: 5.286 karakter.** Δ: saldo −1, lifetimeEarned 7→6, Expertise 7→6, RAR +3 (availability +1 dari job completed; reputation +2 bertepatan 2 verdict compliant — hipotesis L-07).

**Pertanyaan (persis):** *"What are the trade-offs between using an EIP-1167 minimal proxy versus deploying a full standalone contract for a token launch, in terms of gas cost, upgradeability, and auditability?"* — tiga sub-pertanyaan eksplisit: gas cost, upgradeability, auditability.

**Keadaan pertanyaan sekarang (live, 2026-11-12):** settled; **verified 10, revealed 18, falsified 8, abandoned 7**. Ini pertanyaan ramai dan sangat kompetitif — 8 jawaban lain juga falsified di sini; lolos di sini bukan hal sepele, tetapi 10 jawaban membuktikan jalannya ada.

**Jawaban verified di pertanyaan yang sama (dibaca live; tiga teratas yang ditampilkan klien + dua yang dibedah penuh di BEDAH-TOTAL §2.3):**

| Verified | Support/Refutasi | Panjang | Struktur & sudut |
|---|---|---|---|
| dc5dec01 | 4 / 0 | 7.319 kar | Innovator murni: membuka *"I take all of that as premises and do not re-derive it"* — TIDAK menurunkan ulang perbandingan dasar; sudut baru = dua varian minimal-proxy yang lebih baru (ERC-7511 PUSH0 clone: runtime 44 byte, hemat 200 gas deploy + 5 gas/call, dengan URL persis https://ercs.ethereum.org/ERCS/erc-7511; EIP-7702 "real minimal proxy") dan risiko inisialisasi varian 7702. Setiap angka menempel ke dokumen primernya. |
| 7804fc2f | 3 / 0 | 10.117 kar | Sama: premis dari korpus verified diambil sebagai given (45 byte, ΔG = 200(B − 45), break-even satu digit, pajak 63/64, dinding stipend 2.300, immutable args, EXTCODEHASH, beacon, repricing L2); yang baru = tiga celah: replay permit EIP-2612 lintas clone lewat caching DOMAIN_SEPARATOR (EIP-712/EIP-2612 dikutip dengan bunyi persis), deterministic addressing, parameter implementasi per-call. |
| 0bae621a | 4 / 0 | 10.004 kar | Dua tambahan: dinding stipend 2.300 gas (transfer Ether ke clone dingin selalu revert: COLD_ACCOUNT_ACCESS_COST 2.600 EIP-2929 > stipend 2.300 — aritmetika ditampilkan eksplisit, sitasi Buterin & Swende 2020 + Solidity 2024) + clones with immutable args. |
| Reinhard (BEDAH-TOTAL §2.3) | lolos | 7.765 kar, 13 tautan | Mengikat **setiap** angka ke sitasi bernomor + hedge di titik klaim. |
| nanik (BEDAH-TOTAL §2.3) | lolos | 5.349 kar, **0 sitasi** | Lolos justru karena **0 klaim Tier-1**: semua rentang/Tier-0, tidak ada angka bernama-rantai yang bisa dipatahkan. |

Dua jalan terbukti lolos di ISR ini: **(jalan Reinhard)** spesifisitas Tier-1 DENGAN dukungan Tier-1 (tiap angka terikat dokumen yang menyatakannya + hedge), atau **(jalan nanik)** nol klaim Tier-1 sama sekali (semua Tier-0/rentang). Jawaban verified lain di ISR ini rata-rata **panjang (7,3–10,1 rb kar)** dan berbentuk "korpus sebagai premis + sudut baru yang bisa dicek ke spesifikasi primer" — mereka tiba SESUDAH korpus terbentuk dan memanen novelty di atasnya.

**Teks terkirim kita (5.286 kar) — yang benar dan yang membunuh:**

Yang BENAR (BEDAH-TOTAL, diakui eksplisit): semua angka kerasnya benar dan terikat benar — runtime EIP-1167 45 byte; 200 gas/byte code deposit; 16 gas EIP-2028; jalur OpenZeppelin v5.0.2 nyata; sudut beacon + repricing L2 benar-benar baru di thread itu. 4A v1 LOLOS semua butir atas draf ini.

Yang MEMBUNUH (kutipan persis dari jawaban kita, BEDAH-TOTAL §2.1):

> *"On Arbitrum, Optimism and Base, deployment cost is dominated by **L1 data cost**, not the 200-gas-per-byte code deposit."*
> *"…the clone's advantage **GROWS on the deployment side** … while its lifetime tax nearly **VANISHES on the execution side**."*

Sitasi yang menempel pada klaim-klaim itu: EIP-2028 (calldata 16 gas/byte) dan EIP-4844 (blob). Bedah membuktikan: **kedua dokumen itu diam total soal komposisi biaya deployment di Arbitrum/Optimism/Base.** Prosedur arena: *"a source that exists but does not state or support the claim = non-compliant"* → A_CITATION. Sekunder: kuantifier absolut tanpa hedge di titik klaim (P2, A_UNCERTAINTY); dikotomi CREATE2 palsu (P3, A_REASONING); beacon disebut "anggota keluarga minimal-proxy" — longgar kategori (P4).

**Perbedaan mekanis yang memutuskan:** kita mengambil **jalan tengah yang fatal** — spesifisitas Tier-1 + nama rantai (Arbitrum/Optimism/Base) dengan dukungan bukti kelas Tier-0 (dokumen yang dikutip tidak memuat klaimnya). Reinhard lolos karena entailment-nya penuh; nanik lolos karena tidak pernah membuat klaim yang butuh entailment. Kita membuat klaim yang butuh entailment dan memberinya sitasi tetangga. Lantai §45 LOLOS semua atas klaim ini (4 URL, densitas 2,08, rasio terikat 0,647 — §45.1): lantai menghitung keberadaan dan kedekatan sitasi, dan keduanya ada; yang tidak ada adalah **dukungan semantik**, dan tidak ada gerbang yang memeriksanya saat itu (self-VFP T10.2 belum lahir — ia lahir DARI bedah klaim ini).

---

## 1.2 Klaim #2 — 472b29a0 (Agent ID-gated free mints, BSC) — ISO 097df475 — FALSIFIED 0/4, panel 4

**Submit → verdict:** 2026-11-10 ±21:24 → ±21:29 WIB (±5 menit; ledger ±150 detik di tabel EVALUASI). **Konteks pengiriman:** ini klaim UJI GERBANG PERBAIKAN pasca-JEDA #1 — JEDA diangkat sesi utama 21:20, tembak Nemotron one-shot 21:22, job 1c5a0e5d **completed**, **6.580 karakter**. Steering lulus uji support T10 penuh + probe sendable 3× — **tetap falsified**. Δ: saldo 4,1212→3,1212, lifetimeEarned 6→5, Expertise 6→5, RAR 7→8. Kill-metric (ii) terpicu → JEDA berlaku lagi malam itu juga.

**Pertanyaan (persis):** *"What mechanisms allow Agent ID-gated free mints on BNB Chain to distribute NFTs at zero price without being drained by bots, and where do those mechanisms fail?"*

**Keadaan pertanyaan sekarang (live):** settled; **verified 6, falsified 9, abandoned 2, revealed 18**.

**Jawaban verified di pertanyaan yang sama (dibaca live):**

| Verified | Support/Refutasi | Panjang | Struktur & sudut |
|---|---|---|---|
| e937bc31 | 4 / 0 | 6.772 kar | Berbasis **berkas proyek primer yang diambil live**: Agent Bestiary (ERC-721 di BNB Chain) — alamat registry persis `0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F` dikutip dari llms.txt proyek di GitHub dengan URL penuh; kuota per-wallet, harga sesudah kuota gratis 0,0003 BNB, maks 5/wallet — semua angka adalah FAKTA PROYEK yang bisa dibuka pembaca. Framing note eksplisit memisahkan klaim dari sumber vs klaim dari framing pertanyaan. |
| c02ac23a | 2 / 0 | 17.585 kar | "Short answer" + tumpukan standar diterima sebagai premis; yang baru = tiga celah yang tidak dijawab tumpukan standar (siapa dapat slot saat permintaan > pasokan; kapan eligibilitas diukur — snapshot pra-pengumuman dengan contoh Solidity; nilai NFT pasca-mint). Klaim defensif sempit dinyatakan eksplisit: *"one allocation per accepted credential, per campaign"* — bukan "one per human". |
| 8e09eba3 | 2 / 0 | 8.848 kar | Distingsi pembuka: *"identity-gated is not bot-proof"*; ERC-8004 dikutip dengan URL (eips.ethereum.org) untuk klaim transferable/multi-registrasi/Sybil; **cakupan bukti dinyatakan bertanggal** ("Evidence scope, November 8, 2026") dan memisahkan aturan terpublikasi proyek dari penegakan teraudit. |

Pola ketiganya: angka-angkanya adalah **angka yang bisa diverifikasi pembaca ke sumber primer yang dinamai** (registry on-chain, llms.txt proyek, EIP), atau tidak ada angka sama sekali dan klaimnya dibingkai sempit + berhedge.

**Teks terkirim kita (6.580 kar) — nol URL, nol sitasi, dan parameter rantai yang SALAH faktual (BEDAH-KLAIM2 §2.2):**

| Klaim di jawaban kita | Nilai yang kita tulis | Nilai benar | Sumber benar |
|---|---|---|---|
| Base fee BSC bergerak ikut utilisasi (EIP-1559) | base fee bergerak | base fee BSC ditambatkan **0** (BEP-226); harga gas = tip penuh, min **0,05 gwei** sejak Okt 2025; bakar via BEP-95 | BEP-226; BEP-95 |
| Klaim `freeMint` ≈ 21.000 gas | ~21.000 gas | 21.000 = transfer polos; transfer BEP-20 saja **50–65 ribu gas** | Mekanika EVM |
| Base fee naik 5–10× saat ramai | kelipatan 5–10× | turunan dari premis yang tidak ada (base fee 0) | Turunan K1 |
| Blok BSC ~3 dtk, 21 validator | ~3 dtk / 21 | **0,45 dtk** sejak Fermi (14 Jan 2026); validator **40+** | Fermi; Maxwell Jun 2025 |
| 100.000 blok ≈ 3,5 hari | 3,5 hari | ≈ **12,5 jam** — salah ±6,7× | Turunan K4 |
| Ambang Sybil 50+ wallet / 0,001–0,01 BNB / 24 jam | disajikan sebagai fakta terukur | angka tanpa jangkar, tanpa derivasi, tanpa label ilustratif | — (tidak ada) |

**Perbedaan mekanis yang memutuskan — racun masuk di HILIR, bukan di HULU:** steering 472b29a0 sudah bersih ("tanpa angka, mekanisme saja"), draf probe lulus gerbang yang ada — tetapi **generasi menyisipkan kembali angka karangan diam-diam** (risiko R1 "generative reinsertion" TERWUJUD), dan tidak ada yang menangkapnya karena **tabel kanonis wrapper tidak memuat parameter BSC** (base fee, waktu blok, jumlah validator bukan entri kanonis yang diaudit). Bentuk gagal sitasinya TERBALIK dari klaim #1: #1 sitasi ada-tapi-tidak-mendukung; #2 sitasi **tidak ada sama sekali** (lantai §45 atas teks terkirim: 0 URL, densitas 0,456, rasio terikat 0,318 — GAGAL semua, §45.1). Dan naik kelas: klaim #1 tidak didukung; klaim #2 **terbantahkan** (A_CITATION + A_REASONING). Hasil panelnya yang terburuk di rezim: **0 support / 4 refutasi** — satu-satunya jawaban di ISR itu dengan 0 support; 6 falsified lain di ISR yang sama berhenti di refuted 2.

---

## 1.3 Klaim #3 — 71f472d6 (retail AI, target −20% biaya operasional) — ISO 0d76cc7c — FALSIFIED 0/1, panel 2

**Submit → verdict:** 2026-11-11 07:26:42 → 07:28:57 WIB (±135 detik — verdict TERCEPAT rezim). **Kendaraan:** runonce klaim uji JEDA #2 06:57 (bukan slot-hunt); job 4ad16461 **completed** 07:27:51; lane **Cloudflare/gpt-oss-120b** one-shot. **Panjang terkirim: 5.147 karakter.** Δ: saldo 3,1212→2,1212, lifetimeEarned 5→4, Expertise 5→4, RAR 8→9 (availability 2→3, reliability −3). **Falsified ini memanggil STOP TOTAL** sesuai janji day-close §46 — dan melahirkan evaluasi total §51 + rezim uji §7 yang masih mengikat hari ini.

Persiapan klaim ini yang paling berat di rezim: steering dipatch 07:14 dengan mandat 4 URL Wikipedia persis sesudah 4 generasi Nemotron gagal lantai §45; draf probe **lolos lantai semua** (10 URL, densitas 1,823, rasio terikat 0,60) + 4A LOLOS penuh + self-VFP tercatat + sensus angka tercatat ("nol angka yatim"). **Tetap falsified.** Lantai perlu, bukan cukup — persis sel yang diramalkan T12 (23% falsified eksternal lolos kombo K-1+K-2).

**Pertanyaan (persis):** *"How can a traditional retail company use artificial intelligence to reduce operational costs by 20% within two years without reducing employee satisfaction or customer experience? Identify the most promising applications, implementation challenges, and measurable success indicators."* — tiga sub-pertanyaan EKSPLISIT: **(a) most promising applications, (b) implementation challenges, (c) measurable success indicators.**

**Keadaan pertanyaan sekarang (live):** settled; **verified 5, falsified 5, revealed 4, abandoned 2**.

**Jawaban verified di pertanyaan yang sama (dibaca live):**

| Verified | Support/Refutasi | Panjang | Struktur & sudut |
|---|---|---|---|
| 3d30286d | 2 / 0 | 7.472 kar | Dibangun di atas **kasus nyata bernama**: Walmart — program "augment, don't replace", kutipan chief people officer, dua artikel Fortune bertanggal dengan URL penuh (12 Jun 2026 + 19 Feb 2026), peringkat kolam biaya dari deployment terdokumentasi, mode gagal "exception tail" yang teramati di Walmart, rencana pengukuran ringkas. |
| 79b1cecd | 2 / 0 | 8.467 kar | **Menamai lima aplikasi** secara eksplisit: returns triage & reverse logistics, shelf compliance, markdown management, equipment maintenance, multi-store labor fluidity — dikopel model governansi yang menjadikan kepuasan karyawan + pengalaman pelanggan kendala mengikat. |
| a28f77ee | 2 / 0 | 12.413 kar | Tiga disiplin baru: feasibility gate per arketipe retailer, realization waterfall, causal rollout design; aturan pengurutan aplikasi; uji mekanisme untuk kendala kepuasan karyawan. Angka yang bukan dari sumber **dilabeli eksplisit** sebagai *"planning hypothesis to be measured in the retailer's own pilots, not as a benchmark"*. |

Keempat/kelima jawaban verified (5 total) **semuanya menamai aplikasi AI** dan semuanya membawa setidaknya satu jangkar dunia-nyata bernama (kasus, deployment, atau kerangka terukur bernama).

**Teks terkirim kita (5.147 kar) — yang gugur sebagai penjelasan dan yang membunuh (§50 klaim uji butir 8; bedah inferensi dari teks terkirim):**

Yang GUGUR sebagai penjelasan (terbukti bukan penyebab): lantai mekanik (lolos semua dengan margin); format/panjang (5.147 kar = pita baku, 6 seksi, penutup bermarker); parafrase (spine jawaban absen dari verified — grep 0 hit).

Yang MEMBUNUH — dua hal:
1. **Scope miss total pada sub-pertanyaan (a):** jawaban terkirim **TIDAK MENAMAI SATU PUN aplikasi AI** — tidak ada forecasting, scheduling, copilot, returns-triage, markdown, predictive-maintenance, AP-matching. **Nol.** Steering §16 memerintahkan *"Do NOT re-derive"* portofolio aplikasi (maksud: jangan menurunkan ulang yang sudah dibahas verified lain); model menafsirkannya sebagai "jangan sebut aplikasi sama sekali". Pertanyaan meminta daftar aplikasi; jawaban menolak memberikan satu pun.
2. **Sitasi tanpa bukti:** kandidat pendukung = 8 angka berlabel *"planning hypothesis"* + ambang tanpa angka (*"stays below a floor"*, *"at least a fraction"*) — jawaban tidak mengandung **satu pun** angka/fakta dunia yang terikat ke sumber yang menyatakannya, di luar definisi. Goodhart/Campbell/MAPE/HACCP adalah **definisi konsep, bukan bukti empiris**. Lantai mekanik menghitung KEBERADAAN sitasi, bukan KEKUATAN bukti — draf lolos lantai sambil tetap kosong bukti.

**Perbedaan mekanis yang memutuskan:** verified menang dengan (aplikasi dinamai) × (jangkar dunia nyata bernama + sitasi yang menyatakannya). Kita kalah dengan (aplikasi tidak dinamai) × (definisi konsep sebagai satu-satunya "bukti"). Panel terkecil rezim (2 verifier) dan verdict tercepat (±135 detik) dengan 1 refutasi membunuh — konsisten dengan penolakan yang jelas-dan-cepat atas jawaban yang tidak menjawab pertanyaan, bukan dengan sengketa kualitas yang ketat. **Data model yang dikunci klaim ini: falsified dengan HANYA 1 refutasi pada panel 2 (0 support / 1 refutasi) — ambang agregasi L-01: satu refutasi membunuh, terlepas dari ukuran panel.**

---

## 1.4 Pola lintas tiga klaim — spesies dominan, dan kejujuran soal "satu spesies"

**Apakah ada SATU spesies yang mendominasi? Jawaban terbukti: TIDAK ada satu mekanisme — ada satu KELUARGA dengan tiga mekanisme, dan keluarga itulah yang dominan.**

Keluarga akarnya dirumuskan BEDAH-KLAIM2 §7 dan berlaku kata per kata untuk #1 dan #2: **"spesifisitas Tier-1, dukungan Tier-0"** — membuat klaim setingkat fakta bernama (nama rantai, parameter protokol, ambang terukur) sambil memberinya dukungan setingkat penalaran umum (sitasi tetangga, atau tanpa sitasi, atau definisi). Klaim #3 adalah cermin keluarga yang sama dari arah berlawanan: pertanyaan menuntut isi Tier-1 (aplikasi bernama + bukti empiris), jawaban memberi isi Tier-0 (kerangka + definisi) — spesifisitas yang dituntut tidak pernah dipasok.

Di dalam keluarga itu, tiga mekanisme berbeda dan **tidak ada satu perbaikan yang mengubah hasil ketiganya** (EVALUASI §1.5, dibuktikan per klaim):

| | Spesies | Mekanisme | Gerbang yang membunuhnya (sesudah lahir) |
|---|---|---|---|
| #1 | **A — dukungan semantik** | Sitasi ADA, tidak mendukung klaim porosnya (A_CITATION) | self-VFP / sub-cek E1 (buka-dan-baca entailment) — lahir DARI bedah #1 |
| #2 | **B — lantai mekanik + fakta salah** | Sitasi TIDAK ADA + parameter rantai salah faktual, disisipkan generasi di hilir steering bersih (A_CITATION + A_REASONING) | Lantai §45 (K-1/K-2) — profil #2 tertahan pasti (0 URL / 0,456 / 0,318) |
| #3 | **C — scope miss + sitasi-tanpa-bukti** | Sub-pertanyaan (a) tidak dijawab sama sekali + nol bukti empiris (A_SCOPE) | Gerbang (h) cakupan sub-pertanyaan + (i) standar bukti empiris — lahir DARI bedah #3 |

Bukti tidak adanya perbaikan tunggal:
- Perbaikan #2 (lantai §45) **tidak mengubah #1 dan #3** — keduanya lolos semua lantai dengan margin (#1: 4 URL/2,08/0,647; #3: 10 URL/1,823/0,60). Lantai membunuh spesies B saja.
- Perbaikan #1 (self-VFP dukungan semantik) **tidak mengubah #3 — terbukti empiris**: klaim #3 dikirim DENGAN self-VFP tercatat dan sensus angka tercatat, tetap falsified. Self-VFP memeriksa apakah sitasi mendukung KONSEP di kalimatnya; ia tidak memeriksa apakah jawaban MENJAWAB pertanyaan, dan tidak memeriksa apakah ada bukti empiris di luar definisi.
- Perbaikan #3 (gerbang cakupan) **tidak mengubah #1 dan #2**: #1 menjawab semua sub-pertanyaannya (rubrik (b) lolos substantif); #2 gagal scope hanya parsial — pembunuhnya fakta salah, bukan cakupan.

**Spesies dominan bila dipaksa satu nama:** keluarga sitasi/dukungan (A_CITATION dan turunannya) — ia membunuh 2 dari 3 klaim kita (#1 spesies A murni; #2 spesies B yang separuhnya A_CITATION), dan data platform menempatkannya jauh di atas segalanya: **A_CITATION = 91,1% dari semua kegagalan arena_rules** (§26), penolakan platform terbesar adalah surprise_gauge 59,2% lalu arena_rules 38,4%. Spesies C adalah pembunuh ketiga yang berbeda — dan justru karena berbeda, ia membuktikan permukaan gagal kita belum terpetakan penuh oleh satu gerbang pun (alasan vonis evaluasi bukan "lanjut biasa").

**Amplifier proses yang memperparah dua dari tiga:** draf yang digerbang ≠ draf yang terkirim. Klaim one-shot mengundi ulang generasi di dalam `trued answer`; gerbang semantik (4A/self-VFP) dinilai atas **draf probe**, bukan draf terkirim. Ia berkontribusi pada #1 (probe lolos 4A; terkirim membawa P1) dan #3 (probe lolos 4A + self-VFP; terkirim melewatkan scope), tetapi tidak menjelaskan #2 (sensus wrapper tidak memuat parameter BSC — draf mana pun lolos). Jadi: **satu keluarga, tiga mekanisme, tiga gerbang — plus satu cacat proses yang memperparah dua dari tiga.**

Catatan statistik kejujuran (EVALUASI §6.4): 0/3 sendiri TIDAK membuktikan true rate kita di bawah ambang impas 15% — P(0/3 | v=0,15) ≈ 0,61; P(0/3 | v=0,32) ≈ 0,31; P(0/3 | v=0,55) ≈ 0,09; CI 95% untuk 0/3 membentang ±0–63%. Yang membuktikan rezim bermasalah adalah tiga spesies berbeda + cacat proses + lane mati — mekanisme, bukan n=3.

---

## 1.5 Apa yang rubrik v2 + audit_sent_draft.py AKAN dan TIDAK AKAN menangkap — per klaim, dengan bukti

Rubrik v2 (QUALITY.md, bump 2026-11-11) = butir (a)–(i), pintu mati (d)/(g)/(h), (i) memblokir klaim berikutnya bila gagal di teks terkirim; alat mekanis pendamping = lantai §45 (K-1 keberadaan sitasi, K-2 ikatan angka ±150 kar), wrapper `score_rubric`, dan `provider/audit_sent_draft.py` (offline, menilai teks TERKIRIM: proksi (h) = ≥60% kata signifikan sub-pertanyaan hadir di dalam seksi ## bernomor; proksi (i) = cacah angka terikat sitasi ≥1).

**Klaim #1 (spesies A):**
- **AKAN tertangkap — hanya oleh sub-cek E1 di (d) v2, dan hanya bila dikerjakan jujur.** Dua klaim fatalnya adalah klaim POROS (menopang §2 jawaban) dengan sitasi yang tidak me-entail-nya. (d) v2 mewajibkan buka-dan-baca: buka EIP-2028/EIP-4844, tunjuk kalimat yang menyatakan dominasi biaya L1 di Arbitrum/Optimism/Base — tidak ada. GAGAL (d) = tidak dikirim.
- **TIDAK akan tertangkap oleh:** lantai §45 (terbukti lolos: 4 URL/2,08/0,647); `audit_sent_draft.py` (proksinya menghitung angka terikat + cakupan kata — entailment semantik bukan hal mekanis; alat ini akan memberi skor lolos pada teks #1); wrapper citation_patch (kedekatan, bukan entailment). Juga tidak tertangkap oleh (h) — #1 menjawab ketiga sub-pertanyaannya — dan tidak oleh (i) — angka-angka dunianya nyata dan terikat.
- **Syarat tangkapnya bersifat manusia/agen, bukan alat:** E1 adalah langkah membaca. Bila penilai (d) memperlakukan "ada sitasi di kalimat yang sama" sebagai entailment, #1 lolos lagi persis seperti sebelumnya.

**Klaim #2 (spesies B):**
- **AKAN tertangkap — oleh tiga lapis sekaligus, secara mekanis.** Lantai §45: GAGAL semua (0 URL < 1; densitas 0,456 < 0,5; rasio 0,318 — angka dari §45.1 atas teks terkirimnya sendiri). (d) v2: parameter rantai presisi tanpa sitasi = angka poros tanpa entailment = GAGAL pintu mati. `audit_sent_draft.py`: cacah angka terikat = 0 → proksi (i) GAGAL. Ini satu-satunya klaim dari tiga yang tertangkap PENUH oleh mesin.
- **Yang TIDAK akan tertangkap oleh gerbang mana pun:** kesalahan faktualnya sendiri. Tidak ada gerbang yang tahu base fee BSC = 0 (BEP-226) atau blok = 0,45 dtk (Fermi) kecuali tabel kanonis memuatnya — dan tabel kanonis wrapper terbukti TIDAK memuat parameter BSC. Perlindungan v2 terhadap spesies ini bersifat tidak langsung tapi struktural: (d) memaksa tiap angka poros **disitasi atau ditulis ulang Tier-0 tanpa angka** — angka yang dipaksa bersitasi menjadi bisa dicek; angka yang tidak bisa disitasi hilang dari teks. Yang lolos dari paksaan itu (angka yang disisipkan generasi SESUDAH gerbang, di draf terkirim yang berbeda dari draf probe) hanya tertangkap oleh audit draf-terkirim — yang memblokir klaim BERIKUTNYA, bukan klaim itu sendiri.

**Klaim #3 (spesies C):**
- **AKAN tertangkap — oleh (h), dengan satu syarat urutan.** `audit_sent_draft.py --subquestions` atas daftar sub-pertanyaan soal ini (aplikasi / tantangan implementasi / indikator terukur): kata signifikan sub-pertanyaan (a) ("applications", nama-nama aplikasi) absen dari teks → (h) GAGAL. Syaratnya: (h) mengikat atas **teks terkirim** — untuk klaim ini ia hanya bisa menangkap SEBELUM kirim bila dinilai atas draf probe, dan draf probe klaim #3 lolos 4A + self-VFP. Apakah draf probe juga melewatkan aplikasi? Bukti tidak langsung kuat: steering §16 yang sama ("Do NOT re-derive") mengendalikan kedua generasi, dan kegagalan terkirim berbentuk kepatuhan-para-instruksi, bukan kecelakaan sampling. Penilaian jujur: (h) atas draf probe = **kemungkinan besar menangkap**; (h) atas teks terkirim = **pasti menangkap, tapi sesudah verdict** — fungsinya memblokir klaim berikutnya + memaksa perbaikan steering (persis desain §7.1 butir 3).
- **SEBAGIAN tertangkap oleh (i) — dan di sinilah proksi mekanisnya tidak cukup.** Proksi (i) di `audit_sent_draft.py` = cacah angka terikat sitasi ≥1: teks #3 punya 10 URL dan rasio terikat 0,60 → **proksi (i) LOLOS**, padahal semangat (i) GAGAL (angkanya "planning hypothesis" tanpa sumber; "buktinya" definisi konsep). (i) hanya menangkap #3 bila dinilai manual dengan standar "fakta dunia yang dinyatakan sumbernya", bukan dengan cacah proksi. Ini celah alat yang nyata dan harus dibaca apa adanya: **(i) mekanis perlu, (i) manual yang memutuskan.**
- **TIDAK akan tertangkap oleh:** lantai §45 (lolos margin), (d) ketat (tidak ada angka poros salah yang ter-entail buruk — masalahnya ketiadaan, bukan kesalahan), (e) v1 (penutup bermarker novelty — lolos; (e) v2 menilai kebenaran kebaruan, dan kebaruan #3 memang ada — spine-nya absen dari verified, grep 0 hit).

**Yang TIDAK akan tertangkap oleh seluruh tumpukan v2, untuk klaim mana pun:** cacat proses draf-probe ≠ draf-terkirim pada jalur one-shot. Semua gerbang pra-kirim menilai teks yang BUKAN teks yang dinilai verifier. `audit_sent_draft.py` adalah kompensasi pasca-kirim (memblokir klaim berikutnya + memaksa perbaikan steering), bukan pencegahan. Satu-satunya penutup struktural yang terdokumentasi adalah jalur serve §39 (PREPARE_CMD: generasi + saringan SEBELUM bid; draf gagal = pertanyaan dilewati sebelum ada job; draf yang digerbang = draf yang terkirim) — dan jalur itu **belum pernah dinyalakan dengan kata kunci nyata** (§39: siap di atas kertas + teruji asap 25/25 + smoke live 0 job).

---

# BAGIAN 2 — AUDIT KAPASITAS LANE GRATIS (per 2026-11-12 pagi)

**Metode:** batas dari dokumentasi lane (§34–§40, §37, §39) + FUEL-AUDIT-CAPACITY-2026-11-10.md + pembacaan penuh `provider/token-usage.jsonl` (32 catatan: 19 openrouter-nemotron, 9 cloudflare-gptoss, 3 dashscope-deepseekpro, 1 zai-glm47flash; 2026-11-10 s/d 2026-11-11). **Nol generasi baru diterbitkan untuk audit ini.** "Generasi kelas-klaim" = satu panggilan model yang menghasilkan draf jawaban penuh (prompt = steering + pertanyaan + jawaban yang sudah ada; keluaran 4.500–12.000+ karakter). Satu klaim terkirim bisa memakan >1 generasi (probe kelas-klaim + generasi kirim + regenerasi wrapper).

## 2.1 Cloudflare / gpt-oss-120b — lane uji tunggal yang hidup

- **Bahan bakar:** 10.000 neuron/hari untuk seluruh akun Cloudflare (reset 00:00 UTC = 07:00 WIB). Pagar provider kita: **abort pra-generasi bila akumulasi hari-UTC > 9.000 neuron** (§37) — jadi anggaran kerja efektif lane = 9.000 neuron/hari.
- **Unit terukur per generasi (dari token-usage.jsonl, kolom `usage.neurons`):**

| Waktu (UTC) | ISR | Neuron | Karakter keluar | Catatan |
|---|---|---|---|---|
| 2026-11-10 10:23 | — (bench) | 177,29 | 5.858 | bench §37 |
| 2026-11-10 10:24 | — (bench) | 207,70 | 6.147 | bench §37 |
| 2026-11-10 10:25 | — (bench) | 187,04 | 6.224 | bench §37 → median bench **187,04** |
| 2026-11-11 00:16 | 2c7efc3e | 194,20 | 8.495 | probe/drill target uji |
| 2026-11-11 00:23 | 71f472d6 | 209,12 | 6.415 | generasi uji klaim #3 |
| 2026-11-11 00:25 | 71f472d6 | 262,07 | 5.494 | generasi uji klaim #3 |
| 2026-11-11 00:27 | 71f472d6 | **1.501,31** | 5.154 | generasi klaim #3 yang terkirim — prompt konteks panjang (pertanyaan + verified yang ada + steering bermandat-URL) |
| 2026-11-11 02:10 | 2c7efc3e | 180,63 | 4.581 | probe target uji |
| 2026-11-11 04:27 | 1d3efb52 | 287,56 | 9.325 | drill bayangan §53 |

- **Pembacaan unit:** generasi prompt-pendek (bench, prompt masuk ±562 token) = 177–208 neuron, median 187 → **±48 generasi/hari** pada pagar 9.000 (±53 pada kolam penuh 10.000). Generasi kelas-klaim nyata 11 Nov = 180–288 neuron untuk 5 dari 6 generasi — TETAPI generasi yang benar-benar terkirim untuk klaim #3 berharga **1.501 neuron** (konteksnya paling panjang). Unit perencanaan yang jujur: **±250 neuron/generasi tipikal; ±1.500 neuron untuk target berkonteks berat**. Pada unit tipikal: 9.000/250 = **±36 generasi kelas-klaim/hari**. Pada hari yang semua targetnya berat: 9.000/1.500 = **6 generasi/hari**. Total terpakai 11 Nov = **2.634,88 neuron** (kolom `neurons_today_after` terakhir) — pemakaian nyata kita jauh di bawah pagar; yang membakar paling banyak justru SATU klaim (#3: 209+262+1.501 = **1.972,5 neuron untuk satu jawaban terkirim**, karena runonce membakar beberapa generasi probe sebelum satu yang lolos lantai).
- **Kualitas per generasi:** latensi median bench 53,5 dtk; panjang mentah median 6.147 kar — di pita 3/3 bench tanpa regenerasi; mojibake 0. Kelemahan terbukti: (d) mentah GAGAL 3/3 di bench (penyakit E1 yang sama: 700 gas terikat EIP-2929; runtime EIP-1167 "10 byte") — semua tertangkap + ter-patch wrapper; sendable bench 0/3 (n=3) → lane ini butuh steering keras anti-E1 (§37 butir 4(viii)) + mandat-URL untuk menghasilkan draf sendable dengan andal. Di jendela 07:00 11 Nov ia satu-satunya lane yang menyelesaikan klaim uji (probe 2 sendable=true: 5.486 kar, 10 URL, densitas 1,823, rasio 0,60).
- **Jahitan serve:** serve pengganti §39 berbagi kolam neuron yang sama; cap keras serve = **10 generasi/hari-UTC** (3 lapis) ≈ 1.870–2.500 neuron → klaim + serve TIDAK bisa sama-sama maksimal di lane ini; gabungan realistis **±36–53 generasi/hari untuk keduanya** tergantung berat konteks.

## 2.2 OpenRouter / Nemotron (nvidia/nemotron-3-ultra-550b-a55b:free) — fallback terbukti-klaim

- **Bahan bakar:** **50 request/hari** (reset 00:00 UTC = 07:00 WIB). Counter hanya bergerak bila generasi benar-benar berjalan (gagal pra-generasi 403/429 tidak memotong — terukur di BENCH). Provider kita abort bila sisa <3.
- **Pemakaian terukur (token-usage.jsonl):** 19 catatan; `quota_remaining_after` terakhir 2026-11-10 = 36 (sesudah 9 generasi hari itu — termasuk 2 generasi klaim #1 pada 09:23/09:26 UTC: 4.652 + 5.296 token); 2026-11-11: 10 catatan, sisa terakhir **39** (06:00:19Z, probe pendek "OK" — probe pendek tidak menggerakkan counter secara material). Token per generasi 3.262–5.296 — tidak relevan ke kuota (kuota berbasis request).
- **Efektivitas per request:** 1 request = 1 generasi; regenerasi wrapper = request terpisah. Masalah struktural lane: panjang mentah Nemotron sering di bawah lantai 4.500 (benchmark median **3.846 kar**) → regenerasi sering → **klaim terkirim efektif ±10–25/hari** bila dipaksa jadi lane utama (FUEL-AUDIT: ±25–50 generasi, efektif ±25 klaim pada pola regen). Varians ekstrem terdokumentasi: drill v1 6.514 kar vs v2 11.375 kar untuk prompt yang sama (§34).
- **Rekam jejak:** satu-satunya lane yang menyelesaikan klaim #1 dan #2 (keduanya job completed). Tetapi jendela 07:00 11 Nov: **0/4 sendable** untuk 71f472d6 (2× gagal lantai + 2× generasi KOSONG: HTTP 200, 0 karakter, sesudah 217 dtk dan 146 dtk — pola E2: HTTP 200 ≠ jawaban). Probe kelas-klaim 19:00–21:00 10 Nov: 3/3 sendable. Keandalan berayun per jendela.
- **Kelemahan struktural lain:** konservatisme wrapper — temuan audit APA PUN → tidak sendable, termasuk yang sudah ter-patch mekanis (§35.3: field `span` dibuang dari laporan, patchable vs unpatchable tidak bisa dibedakan dari luar).

## 2.3 DashScope / deepseek-v4-pro-0813 — stok besar yang HANGUS HARI INI

- **Bahan bakar:** stok token sekali pakai (bukan kuota harian), akun Dialectica. Buku stok (§40 + FUEL-AUDIT): **987.129 token pasca-bench**; uji asap §40 membakar 5.084 → **982.045** per audit 10 Nov.
- **Pemakaian sesudah audit (token-usage.jsonl, lane `dashscope-deepseekpro`, 3 catatan):** 2026-11-10 11:48 = 1.391 token (keluaran 4.406 kar); 2026-11-10 11:49 = 3.693 token (12.276 kar) — dua catatan ini totalnya **5.084 = uji asap §40 itu sendiri**; 2026-11-11 00:18 = **2.865 token** (7.089 kar, ISR 472b29a0 — probe diagnostik jendela 07:00).
- **Sisa stok pagi ini (aritmetika buku stok − log): 982.045 − 2.865 = ±979.180 token.**
- **Kapasitas nominal dari sisa itu:** unit bench per generasi penuh = 3.687 / 4.770 / 4.187 token (median ±4.187) → **±233 generasi**; pada unit buku-stok maksimal ±6,5 rb token/generasi → **±150 generasi**. Itu angka di atas kertas.
- **Kapasitas yang bisa benar-benar dipakai: mendekati NOL untuk rencana ini, karena tiga kunci bertumpuk:**
  1. **Stok hangus 2026-11-12 — HARI INI.** Sesudah hari ini stok ini nol berapa pun sisanya. Satu-satunya jendela bakar = jendela kerja hari ini (07:00–21:00 WIB).
  2. **Gerbang §7.3 mengunci klaim hari ini ke uji (klaim 1 Cloudflare; klaim 2 hanya bila klaim 1 verified)** dan §7.1 butir 4 menetapkan **lane tunggal Cloudflare** untuk uji. DashScope bukan lane uji — ia tidak boleh membawa klaim uji berapa pun sisa stoknya.
  3. **Syarat panjangnya sempit:** overshoot SISTEMATIS (11.792 / 16.188 / 13.626 kar vs pita baku 4.500–8.000 — model memperlakukan syarat panjang sebagai lantai) → hanya sah untuk target yang mengizinkan 10–12 rb kar (marathon ramai viso ≥5). (d) mentah juga GAGAL 3/3 di bench (ikatan EIP-2929). Stop-on-Exhaust BELUM pernah terbukti menolak secara live (klaim konsol + dokumentasi 403 saja).
- **Kesimpulan lane:** ±979 ribu token / ±150–233 generasi adalah kapasitas yang **akan hangus tak terpakai** kecuali skenario oportunistik Bagian 3.6 terjadi. Menyatakannya sebagai kapasitas rencana = menipu diri sendiri; ia booster satu hari yang dikunci gerbang.
- **Tangki drill-grade DashScope (bukan claim-grade):** 10 model lain, total **±9,999 jt token** (termasuk qwen3.8-flash 999.677 token sisa, satu-satunya yang terbukti menghasilkan konten utuh; hangus bertingkat 2026-11-17 → 2026-11-24 (flash) → 2026-11-30 → Des–Feb 2027). Semua model reasoning dengan thinking default ON. Ini kapasitas **drill** (bayangan/bedah), bukan klaim — ia tidak bersaing dengan kolam klaim dan tidak hangus hari ini.

## 2.4 Z.ai / glm-4.7-flash — tanpa kuota, terikat ketersediaan

- **Bahan bakar:** model $0, tanpa kuota token terukur. Limit resmi = **konkurensi 1** (sekuensial ketat; probe dan klaim tidak pernah paralel). Retry 1305 tepat satu kali (+±60 dtk) tertanam di provider.
- **Rekam jejak ketersediaan:** bench **6/10 attempt kena 1305** (429 kolam gratis jenuh), hanya 1/3 run bench tuntas; jendela 07:00 11 Nov: **1305 ×2 sesudah retry → lane mati sisa jendela**. Log token-usage: 1 catatan (bench, 8.133 token, 13.685 kar, `retried_after_1305: true`).
- **Kualitas per generasi sukses:** kompetitif — panjang alami di pita, latensi sukses tercepat 35,2 dtk, mojibake 0; (d) lolos mekanis dengan 2 angka presisi mencurigakan (§40).
- **Kapasitas terencana: 0.** Kapasitas berbasis waktu murni ±15–100+ generasi/jam — tidak bermakna karena yang memutuskan adalah kejenuhan kolam, bukan stok. Vonis berdiri: **PARKIR** sampai ketersediaan terbukti lintas ≥3 jendela (rasio sukses/1305 di log lane = alat buktinya). Ia fallback oportunistik, bukan penopang rencana.

## 2.5 Vyce (GLM 5.3 Flash + deepseek-v4.1 + Nemotron-Vyce) — tulang punggung yang mati

- **Status:** DOWN sejak **2026-11-10 14:04** — pada pagi ini ±40 jam. GLM 503 *"model currently unavailable"*, deepseek-v4.1 stream kosong, Nemotron-Vyce 503/timeout. Modus gagal memburuk dari gagal-cepat (0,7–3,2 dtk) menjadi gagal-lambat (±111–220 dtk per probe lewat retry backoff) — membakar WAKTU jendela, bukan kuota.
- **Kapasitas di atas kertas (bila pulih):** GLM promo **10 jt token/hari** (reset 07:00 WIB) → pada siklus klaim penuh ±30–80 rb token = **±125–300 klaim/hari**; saldo promo **$109,3485** (stok, utuh — klaim v4.1 belum pernah jalan) pada $0,012–0,037/jawaban = **±2.900–9.000 jawaban total**. Ini kapasitas terbesar yang kita "miliki" — dan hari ini nilainya **0** karena lane-nya mati. Saldo promo yang tidak mengalir sama dengan tidak ada.
- **Syarat bangun:** satu probe lolos di jendela mana pun → kembali ke tangga probe sebagai primer. Sampai itu, Vyce adalah nama di tangga, bukan jalur.

## 2.6 Yang mati / dilarang — tidak dihitung sebagai kapasitas

- **Gemini: DILARANG** (perintah user 2026-11-10 15:03 — tidak dipakai sama sekali untuk Dialectica, termasuk telemetri/benchmark; pencabutan klaim §29.4 tetap berlaku). Kemampuan teknisnya (probe §29.2: 8.568 kar, 19,2 dtk) tidak mengubah apa pun: kemampuan ≠ izin. **Kapasitas dihitung: 0, selamanya, sampai user sendiri yang membuka.**
- **Sonogami: MATI** — key dicabut 2026-11-10 15:22 (26× 401 *"invalid or revoked API key"* berurutan, nol pemulihan). Kapasitas: 0.
- **dev.meta.ai: PARKIR** ($0; tidak disentuh — perintah berdiri free-only mutlak).

## 2.7 Total kapasitas berkelanjutan + pengikat sebenarnya

**Agregat generasi kelas-klaim per hari dari lane yang HIDUP dan SAH dipakai (di luar stok hangus DashScope):**

| Lane | Generasi/hari berkelanjutan | Sifat |
|---|---|---|
| Cloudflare gpt-oss-120b | **±36** (unit tipikal 250 neuron; rentang 6 bila semua target berat s/d ±48 prompt ringan) — berbagi dengan serve §39 (cap 10 gen serve) | Harian, reset 07:00 WIB |
| OpenRouter/Nemotron | **50 request** → efektif **±10–25 klaim terkirim** (regen + kekosongan E2) | Harian, reset 07:00 WIB |
| Z.ai | 0 terencana (opportunistik) | Ketersediaan |
| Vyce | 0 (mati; ±125–300 di atas kertas bila pulih) | — |
| **Total bahan bakar** | **±86 generasi/hari** (36 CF + 50 OR) | |

Pada pola bakar terukur (klaim terkirim memakan 1–3 generasi; klaim #3 = 3 generasi CF + 4 generasi Nemotron gagal di runonce yang sama), bahan bakar menopang **±25–40 pengiriman/hari**. Tangga internal tertinggi yang pernah diizinkan rezim (PENUH: plafon 15–20, kebiasaan 8–12 klaim/hari; RAMP: 4–10) membutuhkan ±8–30 generasi/hari. **Bahan bakar BUKAN pengikat** — surplus ±3–5× di atas appetite terencana, persis vonis FUEL-AUDIT Skenario B.

**Pengikat sebenarnya, berurutan:**
1. **Gerbang §7.3 + runway saldo.** Hari ini yang boleh ditembak hanya klaim uji. Saldo 2,1212 = ruang untuk tepat **2 falsified** lagi (2,1212 → 1,1212 → 0,1212); 0/2 verified = TUTUP TOTAL otomatis. Ini pengikat #1 dan tidak bisa dinegosiasi dari dalam rencana.
2. **Kualitas verdict kita sendiri.** 0/3 dengan tiga spesies berbeda; ambang impas ≈15% pun belum terbukti bisa kita lewati (CI 95% 0/3 = 0–63%). Satu-satunya tuas hasil adalah tumpukan gerbang v2 + steering bermandat-URL + audit draf-terkirim — bukan volume.
3. **Pasokan pertanyaan.** Pertanyaan General baru hanya **±15–25/hari platform-wide** (§24/§25/§30); subset topik-inti kita (identitas agen, wallet, klaim on-chain, oracle, rollup, keamanan kontrak, token) lebih kecil lagi; Pioneer viso-0 topik-inti pada dua scan terakhir (13:00 11 Nov, 05:00 12 Nov) = **NOL**. Rencana 10 klaim/hari menuntut hampir semua pasokan inti hari itu tertangkap.
4. **Serialitas siklus job.** Konkurensi Expert = 1 (keputusan bahan bakar C di FUEL-AUDIT: menaikkan konkurensi tidak membeli generasi dan menjual reliabilitas — paparan abandoned berlipat melawan REL −3). Siklus job ±10–25 menit → teoritis ±4 job/jam, ±32–56 job per 8–14 jam kerja — cukup untuk RAMP, menjadi sempit di PENUH.
5. **Baru kemudian bahan bakar** — dan hanya di satu jahitan: kolam neuron Cloudflare bila klaim + serve §39 sama-sama dimaksimalkan (±36–53 generasi gabungan/hari), dan kuota OpenRouter 50/hari tanpa slack bila ia dipaksa jadi penopang.

---

# BAGIAN 3 — RENCANA MAKSIMAL $TRUED HARIAN (di bawah gerbang §7.3 yang terkunci)

## 3.0 Gerbang yang mengikat rencana ini (tidak bisa ditawar dari dalam rencana)

Dari EVALUASI §7.3 + §54 + §56 — aturan yang sudah dikunci di muka, otomatis, tanpa evaluasi ulang:

- **Uji klaim 1 = 2c7efc3e, lane Cloudflare** — retry `dialectica-test-claim1-retry-2026-11-12` menembak **06:57 WIB hari ini (2026-11-12)**, gerbang penuh (probe kelas-klaim sendable + 4A v2 + self-VFP + sensus + (h)/(i) atas draf; audit draf-terkirim sesudah submit; verdict watch ±30 menit).
- **Klaim 2 = 1d3efb52, HANYA bila klaim 1 verified** — dan hanya sesudah porsi sudut put dinaikkan di atas ambang novelty 15% (koreksi §55: tulang punggung klaim 2 = label put + linear sebagai bentuk kurva ke-4 + tabel terpadu; klaim "spektrum itu baru" TERBUKTI berlebihan — fef5fd3b sudah membandingkannya; job terpisah, keputusan sesi utama).
- **Falsified di klaim 1** → uji tinggal **1 tembakan terakhir** (klaim 2 menjadi tembakan penentu, keputusan sesi utama).
- **0/2 verified → TUTUP TOTAL otomatis.** Saldo tersisa 0,1212; akun dibekukan untuk klaim/serve; tidak ada "satu klaim lagi untuk memastikan".
- **1 abandoned → STOP hari itu + bedah; uji dianggap GAGAL bila abandoned berasal dari jalur one-shot.** REL −3 tidak punya bantalan untuk satu pun abandoned.
- **Spesies gagal ke-4 (di luar A/B/C) pada klaim uji mana pun → STOP + bedah; kelanjutan butuh gerbang BARU yang dinamai.**
- **Sukses (≥1 verified) → batch 5 klaim** di bawah tumpukan yang sama; **evaluasi ulang di n=8 total klaim rezim** (3 lama + 2 uji + 3 batch pertama): **<2/8 verified → STOP + bedah isi** (bukan tambah volume — R8); **≥2/8 → RAMP normal (4–10 kontes/hari)** dengan gerbang yang sama.

**Satu konsekuensi struktural yang harus dinyatakan telanjang: fase PENUH tangga A5 (plafon 15–20, kebiasaan 8–12) TIDAK BISA dicapai di bawah aturan yang terkunci.** Syarat PENUH tertulis = "10 klaim pertama rezim menghasilkan ≥3 verified DAN 0 abandoned DAN **0 falsified**". Klaim rezim #1–#3 sudah falsified — syarat 0-falsified pada 10 klaim pertama **sudah mustahil secara aritmetika**, berapa pun hasil uji dan batch. Jalur sukses §7.3 sendiri hanya membuka **RAMP (4–10/hari)**. Rencana maksimal di bawah ini karena itu dibangun di atas langit-langit RAMP 10 klaim/hari; angka PENUH hanya ditampilkan sebagai catatan "terkunci di luar" — membukanya butuh keputusan revisi mingguan (lab 2026-11-16) atau user untuk menata ulang tangga, bukan keputusan rencana ini.

## 3.1 Apa yang dihasilkan fase gerbang itu sendiri: ≈ 0 — dinyatakan apa adanya

Fase uji (hari ini, maksimal 2 klaim) **bukan fase penghasilan**. Aritmetikanya:

- Klaim falsified = **−1**; verified tanpa slot = **0** (payout hanya lewat slot); verified + slot = +10 (Marathon/Innovator) atau +20 (Pioneer — target uji bukan Pioneer).
- Dua klaim uji: hasil terburuk **−2** (saldo 2,1212 → 0,1212, dan 0/2 = TUTUP TOTAL); hasil terbaik realistis **+10 s/d +20** (≥1 verified + slot marathon); nilai harapan pada rate yang belum terbukti (0/3, CI 0–63%) ≈ **−2 s/d 0**.
- Yang dibeli fase ini bukan $TRUED melainkan **informasi yang tidak bisa dibeli cara lain**: apakah tumpukan v2 (lantai §45 + (d)/E1 + (h) + (i) + steering bermandat-URL + audit draf-terkirim) menggerakkan rate kita dari 0%. Tanpa ≥1 verified di uji, tidak ada hari penuh yang pernah ada.

## 3.2 Tanggal pertama rencana penuh bisa jalan

Urutan tercepat yang sah menurut gerbang:

| Langkah | Waktu tercepat | Syarat |
|---|---|---|
| Verdict klaim 1 (2c7efc3e) | **2026-11-12 ±07:00–07:30 WIB** (latensi berjalan ±135–263 detik; watch ±30 menit) | Retry 06:57 benar-benar menembak (bukan ke-skip — pelajaran §56: status scheduler "succeeded" bukan bukti; buktikan dari jobs endpoint + token-usage.jsonl) |
| Klaim 2 (1d3efb52) ditembak | **2026-11-12, jendela 07:00–09:00** | Klaim 1 verified + porsi put steering dinaikkan >15% + keputusan sesi utama + job terpisah |
| Batch 5 klaim | **2026-11-12 sore – 2026-11-13** (jendela kerja 07:00–21:00, one-shot berurutan) | ≥1 verified di uji; steering bermandat-URL untuk 5 target (hanya 2c7efc3e/1d3efb52/fdf32ba4 yang SIAP hari ini — sisanya butuh persiapan per target, ini penentu kecepatan sebenarnya) |
| n=8 tercapai + vonis ≥2/8 | **2026-11-13** (klaim batch ke-3) | ≥2 verified dari 8 |
| **Hari RAMP penuh pertama (4–10 klaim)** | **2026-11-14** (paling awal); realistis **2026-11-15** | RAMP terbuka + antrean steering siap |

Bila klaim 1 falsified: klaim 2 menjadi tembakan terakhir (jadwalnya keputusan sesi utama, bisa 12 Nov juga) — batch tidak ada sampai ada verified; bila 0/2, **tidak ada tanggal** — rencana ini mati di gerbang dan yang tersisa hanya scan ringan + drill (EVALUASI §7.4).

## 3.3 Peringkat kelas target menurut nilai harapan per generasi

Satu generasi kelas-klaim berharga sama di semua kelas (±250 neuron CF atau 1 request OR — lihat Bagian 2), jadi peringkat ditentukan oleh **payout × P(slot | verified) × P(verified | kelas)**, dengan parameter kohort §30 (bukan asumsi): 2.262 marathon wins / 858 pertanyaan (2,64/pertanyaan); 5.175 verified dari 18.056 jawaban; s_marathon ≈ 2.262/5.175 ≈ **0,44**; s_pioneer (encer, lintas semua verified) ≈ 858/5.175 ≈ **0,17**; payout campuran tertimbang ≈ **12,7**.

**Peringkat 1 per generasi — PIONEER viso-0 tangkapan-serve-pertama (+20).** Nilai per klaim verified tertinggi: slot Pioneer hanya ada satu per pertanyaan dan ia milik jawaban pertama yang verified; angka encer 0,17 meremehkan peluang penangkap-pertama yang sungguhan (penyebutnya memuat ribuan jawaban telat). EV kasar per verified ≥ 20 × 0,5 = **10** (memakai s campuran konservatif 0,5) — dua kali Marathon. **Tetapi:** (i) pasokan mendekati nol (viso-0 topik-inti = NOL di dua scan terakhir); (ii) satu-satunya jalur yang sah secara struktural adalah serve §39 (draf digerbang = draf terkirim) dan ia belum pernah live-smoke; (iii) syarat tangkapan pertama membuat jendelanya menit, bukan jam. Peringkat 1 per generasi, peringkat terakhir per volume — ia bonus yang ditangkap sistem, bukan mesin harian.

**Peringkat 1 per volume — MARATHON pada pertanyaan settled topik-inti, viso 2–9, sudut baru ≥15% (+10, s ≈ 0,44 → 4,4 per verified).** Ini mesin hariannya: pasokan terbesar (pertanyaan settled marathonActive di pita = kelas yang selalu ada di listing), syaratnya terukur (marathonActive terbaca di DETAIL ISR — field detail = otoritas; settled + marathonActive=false + concluded=true = MATI, lewati), dan timing-nya bisa dikelola (marathon dimenangi verified TERAKHIR sebelum jendela ±500 detik tutup — klaim di jendela hunt yang memuat akhir jendela marathon pertanyaan itu). Sudut ≥15% wajib dibuktikan dengan **grep kata-kunci sudut ke seluruh teks verified yang ada** (pelajaran §55 — survei ingatan melewatkan fef5fd3b dua kali).

**Peringkat 2 — INNOVATOR (+10) sebagai peluang kedua dari generasi yang sama.** Jawaban marathon yang sudutnya benar-benar baru (≥15%) juga berpeluang di slot Innovator. **Stacking Pioneer/Innovator/Marathon BELUM TERBUKTI (§25.1)** — rencana ini TIDAK menghitungnya ganda: Innovator diperlakukan sebagai peluang kedua atas generasi yang sudah dibayar untuk Marathon, bukan sebagai klaim terpisah. Mengajukan jawaban kedua di pertanyaan yang sama demi Innovator saja = generasi tambahan untuk peluang yang belum terbukti menumpuk — tidak dilakukan.

**Di luar peringkat — yang tidak ditembak:** pertanyaan di luar topik inti (Expertise kita general dengan inti identitas agen/wallet/on-chain/oracle/rollup/keamanan kontrak/token — verdict rate kohort di luar inti tidak punya alasan mengungguli); viso ≥10 (keramaian memakan novelty + slot); runtimeContext yang menuntut eksekusi runtime (image/docker) — LEWATI selalu; tiga ISR yang sudah kita jawab dan falsified (472b29a0/60fa9935/71f472d6 — BUANG permanen); target yang steering-nya belum bermandat-URL (deadlock §50.5: lantai menuntut URL, steering tanpa daftar URL yang diizinkan = mustahil oleh konstruksi).

## 3.4 Hari maksimal (sesudah gerbang lolos — hari RAMP)

Jendela hunt berjalan tiap 2 jam berjangkar jam ganjil WIB. Jendela KERJA = run yang mulai 07:00–21:00 (8 jendela: 07, 09, 11, 13, 15, 17, 19, 21). **Jendela utama kedua = 11:00 + 13:00** (punuk rilis kohort tengah hari: 12:00 = 84 rilis, 13:00 = 67, n=858 korpus §30). Run 17:00 = jendela biasa (demosi §30: hanya 41 rilis).

| Jam (WIB) | Isi hari maksimal |
|---|---|
| **06:57–07:00** | Reset kuota OpenRouter + neuron Cloudflare (00:00 UTC). Baca scores + jobs + usage segar (angka awal hari). **Serve §39 NYALA** di awal jendela 07:00 (pengganti Cloudflare bila Vyce masih mati; cap 10 generasi/hari) untuk tangkapan Pioneer sepanjang jendela kerja. |
| **07:00** | Klaim marathon one-shot **#1–#2** (target staged semalam, steering bermandat-URL sudah jadi). Verdict watch berjalan (latensi ±150 dtk — verdict mendarat di dalam jendela yang sama). |
| **09:00** | Audit draf-terkirim klaim pagi (audit_sent_draft.py + (h)/(i) manual) → ledger. Klaim **#3–#4**. Scan pasokan baru. |
| **11:00** | **Jendela utama kedua, bagian 1.** Kesiapan klaim tertinggi: pertanyaan settled segar dari punuk rilis mulai terbaca. Klaim **#5–#6**. |
| **13:00** | **Jendela utama kedua, bagian 2.** Klaim **#7**. Tindak lanjut bayangan drill kemarin (kewajiban DRILL-LOG). |
| **15:00** | Klaim **#8**. Verdict watch + audit semua klaim hari itu sejauh ini; kill-metric dihitung ulang eksplisit. |
| **17:00** | Klaim **#9** (hanya bila tangga + kill-metric + pasokan sama-sama mengizinkan; jendela biasa — bukan tempat memaksakan volume). |
| **19:00** | Klaim **#10** = plafon RAMP. Sesudah ini tidak ada klaim baru hari itu. |
| **21:00** | Jendela terakhir: verdict watch final, audit draf-terkirim terakhir, steering untuk besok ditulis (bermandat-URL + grep novelty SEBELUM steering penuh — lihat Bagian 4 butir 8). |
| **23:00** | **Day-close:** serve PADAM (SIGINT; verifikasi proses hilang + serve.pid dihapus), rekap tangga (cacah klaim disiplin, verified berjalan vs ambang R8), VERDICT-LEDGER + catatan MEKANISME ditulis, antrean besok dinyatakan eksplisit (penutup siklus T6). |
| **23:00–07:00** | Scan ringan saja (listing + scores + jobs), serve MATI — desain berdiri. Biaya yang diterima sadar: viso-0 topik-inti yang rilis tengah malam tidak bisa ditangkap pertama (serve mati + tanpa pengawasan = paparan abandoned melawan REL −3; kill-metric (iv) membuat satu abandoned menghentikan sehari penuh — tangkapan malam tidak sepadan). |

**Penugasan lane per kelas klaim (hari RAMP):**

| Kelas | Lane | Alasan |
|---|---|---|
| Marathon / Innovator (one-shot) | **Cloudflare gpt-oss-120b** primer | Satu-satunya lane dengan klaim completed di rezim uji + panjang alami di pita (median 6.147, 0 regen di bench) + latensi tercepat yang andal (53,5 dtk). Steering keras anti-E1 §37(viii) + mandat-URL wajib menyertai. |
| Marathon (fallback) | OpenRouter/Nemotron | HANYA bila probe Cloudflare gagal di jendela itu DAN probe Nemotron **kelas-klaim** sendable (bukan prompt pendek — §36) DAN sisa kuota ≥3. Satu kegagalan lane (timeout/5xx/200-kosong) = lane mati sisa jendela. |
| Pioneer (tangkapan serve) | **Serve pengganti §39 (Cloudflare, PREPARE_CMD)** | Satu-satunya jalur di mana draf yang digerbang = draf yang terkirim (generasi + saringan SEBELUM bid; gagal = dilewati sebelum ada job → bebas-abandoned secara struktural). Cap 10 generasi/hari berbagi kolam neuron dengan klaim (±1.870 neuron). **Prasyarat: satu smoke live berkata-kunci nyata dengan 0 job di jendela hunt** — belum pernah dilakukan; dijadwalkan sebagai langkah bernama di hari RAMP pertama, bukan diasumsikan. |
| Semua kelas (bila Vyce pulih) | Vyce kembali jadi primer (one-shot deepseek-v4.1 + serve Vyce) | Satu probe lolos = pensiunkan pengganti §39 (aturan §39 sendiri); kapasitasnya (±125–300 siklus/hari + saldo $109,35) menghapus semua kerempongan neuron/kuota. Sampai hari itu: tidak dihitung. |
| DashScope deepseek-pro | **Pensiun per 2026-11-12** (lihat 3.6) | Stok hangus hari ini; bukan lane uji; syarat panjang sempit. |
| Z.ai | Parkir | Ketersediaan belum terbukti ≥3 jendela. |
| Gemini | **Dilarang** | Perintah user; tidak ada skenario rencana yang membukanya. |

**Titik periksa steering/rubrik yang mengikat SETIAP klaim (urutan tidak bisa ditukar):**
1. Detail ISR dibaca (marathonActive dari field detail; viso; runtimeContext → lewati).
2. Jawaban verified yang ada dibaca PENUH; sudut baru ≥15% dibuktikan **grep kata-kunci** ke seluruh teks verified (bukan survei ingatan).
3. Steering bermandat-URL: daftar sumber yang BOLEH dikutip (nama + URL persis, masing-masing terverifikasi HTTP 200 saat ditulis) + aturan penempatan (≥1 sitasi per seksi; angka dan sitasinya dalam kalimat yang sama). Steering yang hanya melarang tanpa memandatkan = DILARANG ditulis.
4. Daftar sub-pertanyaan eksplisit soal ditulis sebagai file (bahan (h) + `--subquestions`).
5. Probe **kelas-klaim** di lane yang ditugaskan (prompt penuh, bukan prompt pendek) → draf dinilai: lantai §45 + rubrik v2 penuh — (d) dengan **sub-cek E1 buka-dan-baca atas setiap angka POROS** (periferal wajib berbingkai estimasi + hedge di titik klaim); (e) kebaruan harus BENAR (lolos (d) atas dasarnya + terbukti absen dari verified); (g) format persis.
6. Baca ulang usage TEPAT sebelum eksekusi (bacaan awal jendela bisa basi); kuota/neuron lane cukup (OpenRouter sisa ≥3; Cloudflare akumulasi <9.000).
7. Submit one-shot, tangkap exit code. **Baca hasil dari server** (detail ISR + jobs endpoint) — baris log "submitted" bukan bukti; klaim sah hanya bila job terbaca **completed**.
8. Verdict watch ±30 menit → **audit draf-terkirim**: teks reveal ISO dinilai ulang (audit_sent_draft.py + (h)/(i) manual + self-VFP) → tulis ke VERDICT-LEDGER + MEKANISME. **Kegagalan (h) atau (i) pada teks terkirim MEMBLOKIR klaim berikutnya** sampai steering diperbaiki, dan dihitung sebagai kegagalan gerbang.
9. Kill-metric dinyatakan angkanya di catatan jendela: (i) klaim disiplin tanpa settle /10; (ii) falsified sejak klaim terakhir → JEDA + bedah sebelum klaim berikutnya; (iii) RAR vs −5; (iv) abandoned baru → STOP sehari.

## 3.5 Nilai harapan $TRUED/hari — aritmetika ditampilkan

Model (EVALUASI §6.3, parameter kohort §30, bukan asumsi): per klaim, `EV = v·s·P − (1−v)·1`, dengan v = verdict rate kita, s = P(memenangi ≥1 slot | verified) ≈ **0,45** (konservatif; s_marathon murni 0,44), P = payout campuran ≈ **12,7**. Maka EV/klaim = v × 0,45 × 12,7 − (1−v) = **5,715v − (1−v)**.

| Skenario | v (dasar) | EV/klaim | Volume/hari | **EV $TRUED/hari** |
|---|---|---|---|---|
| **Pesimistis** | 0,15 (tepi impas — rate minimum yang membuat rezim net-positif; belum terbukti bisa kita capai) | 5,715×0,15 − 0,85 = **+0,01** | 4 (RAMP bawah) | **≈ 0** (rentang jalan-acak −2 s/d +2; dan pada EV≈0 dengan buffer 2,12, peluang ruin sebelum berlipat tetap **>40%** — impas dalam ekspektasi ≠ aman) |
| **Basis** | 0,32 (median agen kohort eksternal, n=182) | 5,715×0,32 − 0,68 = **+1,15** | 8 (kebiasaan RAMP) | **≈ +9,2 → +9 $TRUED/hari** |
| **Optimistis** | 0,55 (median sub-kohort pemenang) | 5,715×0,55 − 0,45 = **+2,69** | 10 (plafon RAMP) | **≈ +26,9 → +27 $TRUED/hari** |
| Terkunci di luar | 0,55 | +2,69 | 12 (kebiasaan PENUH) | +32 — **tidak tersedia**: syarat PENUH (0 falsified di 10 klaim pertama) sudah mustahil (§3.0); hanya revisi tangga oleh lab mingguan/user yang bisa membukanya |

Catatan kejujuran atas ketiga skenario: (i) semuanya mengasumsikan jawaban verified kita mendapat peluang slot rata-rata kohort — yang mensyaratkan timing marathon yang benar dan sudut ≥15% yang terbukti; belum ada bukti kita bisa memenangi slot (0 verified sejauh ini); (ii) skenario basis/optimistis mengasumsikan v kita meloncat dari teramati 0/3 ke median/pemenang kohort — yang dibuktikan uji + batch adalah apakah tumpukan v2 menggerakkan v sama sekali; angka harian di atas adalah **nilai hari RAMP pada v yang diasumsikan**, bukan ramalan; (iii) pada v di bawah ±0,15, setiap hari RAMP adalah hari ber-EV negatif (pada v=0: −4 s/d −10/hari) — itulah fungsi stop §7.3: mencegah hari-hari itu terjadi lebih dari dua kali.

## 3.6 Skenario oportunistik DashScope hari ini — dinyatakan, lalu ditolak sebagai rencana

Stok deepseek-v4-pro ±979.180 token hangus **hari ini, 2026-11-12**. Satu-satunya skenario ia bisa terbakar secara sah: klaim 1 verified pagi ini **DAN** ada target marathon settled viso ≥5 yang pitanya sah 10–12 rb kar di listing hari ini **DAN** sesi utama menugaskannya secara eksplisit ke satu klaim batch. Tiga syarat itu harus terpenuhi di dalam jendela kerja yang sama dengan persiapan steering + probe kelas-klaim. Nilai harapannya rendah dan ia **tidak dihitung** di kapasitas maupun EV rencana ini. Vonis: **biarkan hangus** kecuali ketiga syaratnya muncul sendiri; mengejar stok hangus dengan melonggarkan syarat target adalah cara klasik mengubah booster gratis menjadi falsified berbayar saldo.

---

# BAGIAN 4 — RISIKO, KONDISI STOP WARISAN, DAN PEMBAKARAN KAPASITAS GRATIS YANG SIA-SIA

## 4.1 Kondisi stop yang diwarisi rencana (semuanya sudah terkunci sebelum rencana ini ditulis)

| Pemicu | Akibat | Sumber |
|---|---|---|
| Uji 0/2 verified | **TUTUP TOTAL otomatis**, tanpa evaluasi ulang; sisa = scan ringan + drill saja sampai user memutuskan | §7.3 |
| 1 abandoned (job diambil tak "completed") | **STOP sisa hari itu** + bedah akar; abandoned dari jalur one-shot = uji GAGAL | §7.3 + kill-metric (iv) |
| Spesies gagal ke-4 pada klaim uji | STOP + bedah; lanjut hanya dengan gerbang baru yang DINAMAI | §7.3 |
| <2/8 verified di evaluasi n=8 | STOP + bedah ISI (bukan tambah volume) | §7.3 / R8 |
| 10 klaim disiplin tanpa settle | **STOP TOTAL** (kill-metric (i)) — cacah berjalan kita: 0/10 (3 klaim, 3 completed/settle) | Badan hunt butir 0d |
| 1 falsified sejak klaim terakhir | **JEDA** — tidak ada klaim jendela itu; bedah akar di catatan sebelum klaim berikutnya (kill-metric (ii)); pada klaim uji, JEDA dieskalasi per janji §46/§50 | Badan hunt + §46 |
| RAR < −5 | JEDA s/d revisi mingguan (kill-metric (iii)) — RAR kini 9, bantalan +14; catatan: RAR NAIK pada ketiga falsified kita (availability membayar job completed) — RAR bukan pengukur kualitas dan bukan bantalan saldo | Badan hunt + EVALUASI §6.1 |
| Saldo menyentuh ±0 | Runway aritmetika: 2,1212 menampung tepat 2 falsified lagi; perilaku platform pada saldo negatif **tidak diketahui** (preseden fee bertanya: pengeluaran tertahan saat saldo kurang — §24.3) | EVALUASI §6.2 |

## 4.2 Risiko yang tidak bisa dihilangkan rencana

1. **Kebutaan alasan verifier.** Teks refutasi per verifier tidak terekspos platform (endpoint 404; falsified tidak memicu notifikasi). Semua pembelajaran kita adalah inferensi dari teks terkirim + cacah panel. Konsekuensinya struktural: gerbang kita belajar dari pola, tidak pernah dari kata-kata juri — spesies gagal ke-4, ke-5 bisa ada dan hanya terlihat sesudah membakar saldo.
2. **Draf terkirim ≠ draf digerbang pada jalur one-shot** (Bagian 1.4/1.5). Audit draf-terkirim adalah kompensasi pasca-kirim; penutup strukturalnya (serve §39) belum live-smoke. Selama uji + batch berjalan one-shot, risiko ini dibawa penuh.
3. **Timing marathon.** Slot marathon dimenangi verified terakhir sebelum jendela ±500 detik tutup; jendela hunt kita 2-jaman dan latensi verdict ±135–263 detik membuat presisi itu sebagian di luar kendali kita. s = 0,44 adalah rata-rata kohort, bukan janji.
4. **Pasokan.** ±15–25 pertanyaan General baru/hari platform-wide; hari tanpa kandidat inti yang sah adalah hari 0 klaim yang SAH (disiplin, bukan kegagalan) — rencana 8–10 klaim/hari akan sering terpotong pasokan, bukan oleh bahan bakar.
5. **Lane tunggal.** Rencana bertumpu pada Cloudflare (satu lane, satu akun, kolam 10.000 neuron bersama serve). Bila Cloudflare mati di satu jendela, fallback-nya adalah lane yang 0/4 sendable di jendela terakhirnya yang terukur (Nemotron) — hari itu menjadi hari scan+drill, dan itu harus diterima sebagai hasil, bukan dipaksa.
6. **Vyce tidak punya tanggal pulih.** Downtime 40+ jam dan memburuk modus gagalnya; tidak ada pemicu bangun yang bisa dijadwalkan selain "satu probe lolos".

## 4.3 Yang MEMBAKAR kapasitas gratis tanpa hasil — vonis keep/kill per item

1. **Probe tiga lane Vyce di SETIAP jendela — KILL (dikurangi).** Sejak jam ke-±20 downtime, tiga probe (GLM + deepseek-v4.1 + Nemotron-Vyce) gagal-lambat ±112–220 detik per lane per jendela, 8 jendela kerja/hari = ±30–45 menit waktu jendela terbakar per hari untuk informasi yang identik: mati. §55 sendiri sudah menandainya. **Putusan: tangga probe Vyce dikurangi menjadi SATU probe GLM per hari** (jendela 07:00) sampai ada satu yang lolos; posisi Vyce sebagai primer tidak berubah, pengulangannya yang dibunuh. Yang dibakar di sini bukan kuota — melainkan waktu jendela, satu-satunya sumber yang tidak bisa diisi ulang.
2. **Drill bayangan di lane Cloudflare — KEEP drill-nya, KILL lane-nya.** Kewajiban drill (§33: jendela tanpa klaim tidak boleh pulang kosong) menghasilkan bukti nyata (tindak lanjut bayangan 1d3efb52 menangkap overclaim novelty SEBELUM klaim 2 ditembak — itu drill yang menyelamatkan saldo). Tetapi bayangan 11 Nov membakar **287,56 neuron Cloudflare** — kolam yang sama dengan klaim uji. **Putusan: drill bayangan pindah lane** — ke OpenRouter (1–2 request dari 50, reset harian, tidak bersaing dengan apa pun kecuali fallback) atau ke tangki drill-grade DashScope (qwen3.8-flash ±999.677 token, hangus 2026-11-24, nol kompetisi dengan klaim). Cloudflare dicadangkan untuk probe + klaim selama ia lane klaim tunggal.
3. **Generasi probe kelas-klaim berulang untuk target yang sama dalam satu jendela — KILL pengulangannya, KEEP satu probe.** Klaim #3 membakar 3 generasi Cloudflare (209 + 262 + 1.501 neuron) + 4 generasi Nemotron gagal untuk SATU jawaban terkirim: ±1.972 neuron + 4 request untuk satu falsified. Sebagian adalah harga sah lantai (probe harus kelas-klaim — §36 membuktikan probe pendek mengukur konfigurasi yang berbeda), tetapi pengulangan sesudah kegagalan lantai kedua adalah mengundi ulang, bukan menggerbang. **Putusan: maksimal 2 generasi per target per jendela (1 probe + 1 regenerasi sesudah perbaikan steering yang bernama); gagal kedua = target di-steer ulang di jendela lain atau dibuang.**
4. **Jendela scan-ringan malam (23:00/01:00/03:00/05:00) — KEEP.** Nol generasi, nol klaim, nol serve; yang dibakar hanya menit komputasi. Nilainya terbukti: backfill §56 bergantung pada scan 01:00; §57 menangkap drift 8ca09770 (viso 8→10, keluar pita) + 4 pertanyaan inti baru untuk jendela 07:00. Ini permukaan peringatan dini rezim, bukan pemborosan.
5. **Drill bedah (bedah jawaban publik ber-verdict) — KEEP.** Nol bakar lane (membaca, bukan menggenerasi). Ia menghasilkan rantai bukti E1 ×5, pasangan pembeda (d)/(i) f80ac8d3, dan koreksi celah rubrik (b) ×5/(c) ×6 yang masuk lab. Biaya = waktu agen; hasil = satu-satunya pembelajaran yang tidak membakar saldo.
6. **Serve §39 terbangun tapi tidak pernah live-smoke — bukan pemborosan, ASET MENGGANGGUR; KEEP + JADWALKAN smoke-nya.** Arsitektur PREPARE_CMD adalah satu-satunya penutup struktural cacat draf-terkirim, teruji asap 25/25, dan belum pernah menyentuh kata kunci nyata (smoke live 0 job). Ia tidak membakar apa pun selama mati — tetapi setiap hari Pioneer dibiarkan mustahil karenanya. **Putusan: satu smoke live berkata-kunci nyata (0 job diharapkan, di jendela hunt biasa) adalah langkah bernama di hari RAMP pertama** — biayanya beberapa generasi di dalam cap serve 10/hari.
7. **Probe pendek OpenRouter ("OK") — KEEP.** Counter kuota tidak bergerak material oleh probe pendek (§55: counter diam); ia membeli kepastian mode jendela dengan harga ~nol.
8. **Persiapan steering untuk target yang mati sebelum ditembak — KEEP persiapannya, UBAH urutannya.** 1d758352: steering ditulis penuh, lalu target GUGUR (sudut tertempati — §54). 5fbb2531/26fe6c71/530bed9e: steering ditunda (benar). 1d3efb52: dua lini persiapan melewatkan fef5fd3b; koreksinya datang dari grep, sesudah steering direvisi. **Putusan: verifikasi novelty dengan grep kata-kunci sudut ke seluruh teks verified WAJIB mendahului penulisan steering penuh** (murah, mekanis, menangkap pola overclaim yang terbukti berulang); steering penuh hanya untuk target yang lolos grep + detail ISR.
9. **Probe Z.ai selama parkir — KEEP apa adanya (tidak diprobe).** Tangga probe terbaru sudah berhenti sebelum Z.ai bila lane di atasnya lolos (§55: tidak diprobe). Tidak ada pemborosan berjalan; jangan mulai memprobenya "untuk data" — datanya (rasio 1305) hanya bermakna bila ia kandidat nyata.
10. **Generasi diagnostik untuk mendiagnosis withhold wrapper — KEEP, dengan batas.** Satu generasi diagnostik di jendela 07:00 11 Nov adalah cara lantai §45 terdiagnosis sebagai deadlock steering (bukan kegagalan lane) — informasi yang mengubah perbaikan dari "ganti lane" menjadi "patch steering". Tetapi §7.1 butir 6 (breakdown temuan di stderr) sudah terpasang — sesudah itu, diagnosis harus datang dari breakdown, bukan dari generasi tambahan. **Putusan: keep sebagai alat terakhir; sesudah stderr breakdown hidup, generasi diagnostik = kill.**

## 4.4 Ringkasan satu layar

- **Autopsi:** 0/3 bukan satu spesies — satu keluarga ("spesifisitas Tier-1, dukungan Tier-0") dengan tiga mekanisme (A dukungan semantik; B tanpa sitasi + fakta salah dari hilir; C scope miss + definisi-sebagai-bukti), diperparah cacat proses draf-probe ≠ draf-terkirim. Keluarga sitasi/dukungan adalah pembunuh dominan (2 dari 3 klaim; 91,1% kegagalan arena_rules platform). Rubrik v2 + audit_sent_draft.py menangkap B penuh secara mekanis, menangkap A hanya lewat E1 yang dibaca jujur, menangkap C lewat (h) (pasti di teks terkirim, kemungkinan besar di draf probe) dan (i) hanya secara manual — proksi mekanis (i) akan MELEWATKAN pola #3.
- **Kapasitas:** lane hidup menopang **±86 generasi kelas-klaim/hari** (Cloudflare ±36 pada unit tipikal + OpenRouter 50 request) ≈ 25–40 pengiriman — surplus 3–5× di atas kebutuhan RAMP. Stok DashScope ±979.180 token (±150–233 generasi) **hangus hari ini** dan terkunci gerbang — kapasitas rencana yang jujur darinya = **0**. Pengikat sebenarnya: gerbang §7.3 + saldo 2,1212 (ruang 2 falsified), lalu kualitas verdict kita, lalu pasokan pertanyaan inti, lalu serialitas konkurensi-1. Bahan bakar terakhir.
- **Rencana:** fase gerbang menghasilkan ≈0 (membeli informasi). Sesudah gerbang: RAMP 4–10 klaim/hari, Marathon sebagai mesin, Pioneer sebagai tangkapan serve, Cloudflare primer, serve §39 di-smoke lalu dinyalakan di jendela kerja, day-close 23:00 mematikan serve. **EV/hari: pesimistis ≈ 0 (v=15%, 4 klaim), basis ≈ +9 (v=32%, 8 klaim), optimistis ≈ +27 (v=55%, 10 klaim)** — semuanya nilai-kondisional pada v yang diasumsikan; PENUH (12/hari → +32) terkunci mustahil oleh syarat 0-falsified yang sudah gugur. Hari RAMP pertama paling awal **2026-11-14**, realistis 2026-11-15 — atau tidak pernah, bila uji berkata 0/2.

---

*Ditulis 2026-11-12 pagi. Berkas pendamping: VERDICT-LEDGER.md; EVALUASI-STOP-2026-11-11.md; BEDAH-TOTAL-2026-11-10.md; BEDAH-KLAIM2-2026-11-10.md; FUEL-AUDIT-CAPACITY-2026-11-10.md; MEKANISME-DAN-LAPANGAN.md §50/§54–§57; QUALITY.md v2. Nol klaim/generasi/serve disentuh oleh penulisan berkas ini; uji klaim 1 retry 06:57 WIB adalah milik runonce terjadwal dan tidak diintervensi.*
