# BEDAH KLAIM #2 — FALSIFIED 472b29a0 (2026-11-10)

**Ringkasan: klaim #2 mati BUKAN karena sitasi salah-ikat seperti klaim #1 — steering-nya bersih, tapi GENERASI menyisipkan kembali angka-angka keras yang salah secara faktual tentang BSC, tanpa satu pun sitasi; keluarga akar sama, mekanisme pemicu baru.**

## 1. Identitas jawaban kita

ISR **472b29a0-8933-41af-ac17-e75bc1a27f32** — "What mechanisms allow Agent ID-gated free mints on BNB Chain to distribute NFTs at zero price without being drained by bots, and where do those mechanisms fail?"

ISO kita: **097df475** (awalan id dari payload API `/api/node/isos/`).

Submit ±21:24 WIB via one-shot OpenRouter/Nemotron, job 1c5a0e5d "completed", **6.580 karakter**.

Verdict: **FALSIFIED — supported 0, refuted 4.**

Itu penolakan terdalam di ISR ini: 6 falsified lain berhenti di refuted 2; kita satu-satunya yang **0 support / 4 refutasi** — tidak ada satu verifier pun yang membela.

Teks refutasi tidak diekspos API (sama seperti klaim #1), jadi bedah ini inferensi berbasis bukti; tiap peringkat vonis membawa label keyakinan.

## 2. Inventaris klaim jawaban kita — vonis dukungan per klaim

Jawaban kita memuat **0 URL, 0 sitasi** dalam bentuk apa pun. Nama dokumen disebut (EIP-1559, ERC-8004, "Binance Agentic Wallet documentation") tanpa versi, tanpa tautan, tanpa jangkar.

Klaim Tier-1 dan vonisnya:

**K1 — "effective_gas_price = base_fee + priority_fee under EIP-1559 on BSC; the base fee moves with block utilization" (§1, paragraf fondasi).**

Vonis: **SALAH FAKTUAL.** BSC menambatkan base fee di **0** (BEP-226 mengadopsi tipe transaksi EIP-1559 tapi baseFeePerGas selalu 0); harga gas BSC = tip penuh yang tunduk pada harga minimum validator (0,05 gwei sejak Okt 2025), dan pembakaran berjalan lewat porsi BEP-95 — bukan base fee yang bergerak mengikuti utilisasi blok. Mekanisme Ethereum dipindahkan mentah-mentah ke BSC.

Ini kalimat fondasi seksi utama jawaban. Verifier yang paham BSC bisa membantah dalam hitungan detik.

**K2 — "the same claim shape that costs ~21 000 gas in a quiet block" (§1).**

Vonis: **SALAH / MENYESATKAN.** 21.000 gas adalah biaya intrinsik transfer nilai polos. Klaim `freeMint` = panggilan kontrak (cek registry + tulis mapping klaim + mint ERC-721) — transfer token BEP-20 saja sudah 50–65 ribu gas; mint nyata jauh di atas 21.000. Angka terkecil yang paling tidak mungkin justru dipakai sebagai patokan biaya klaim.

**K3 — "a 5–10× higher base fee when thousands of eligible wallets compete" (§1).**

Vonis: **TIDAK DIDUKUNG + turunannya ikut salah** — karena base fee BSC tidak bergerak (lihat K1), kelipatan 5–10× atas base fee adalah angka karangan yang menempel pada mekanisme yang tidak ada di rantai ini.

**K4 — "On BSC's ~3 s blocks with 21 PoSA validators" (§1).**

Vonis: **SALAH / BASI.** Waktu blok BSC = **0,45 detik** sejak hard fork Fermi (14 Jan 2026; 0,75 dtk sesudah Maxwell Jun 2025). 3 detik hanya benar di era peluncuran. Set validator aktif juga sudah melebar dari 21 ke **40+**.

**K5 — "mint_end_block + 100 000 (~3.5 days on BSC)" (§4).**

Vonis: **TURUNAN SALAH.** Konsisten internal dengan premis 3 detik yang salah; pada 0,45 dtk, 100.000 blok ≈ **12,5 jam**, bukan 3,5 hari. Metrik "keberhasilan terukur" andalan penutup dibangun di atas aritmetika yang keliru ±6,7×.

**K6 — "Binance Agentic Wallet documentation states each user may create one Agentic Wallet and claim one .ai handle" (§3).**

Vonis: **KLAIM ISI DOKUMEN TANPA SITASI.** Substansinya kurang-lebih benar — jawaban verified 002651ff menyatakan hal yang sama tentang dokumen yang sama, TAPI dengan sitasi URL persis ke developers.binance.com. Di jawaban kita klaim yang identik berdiri tanpa penunjuk apa pun, dan diperluas ("and claim one .ai handle") tanpa jangkar. Bagi verifier, ini tidak bisa dibedakan dari karangan.

**K7 — "ERC-8004 explicitly permits transferable agent identities and multiple registrations" (§3).**

Vonis: **ISI STANDAR TANPA SITASI + TUMPAK TINDIH KEBAUAN.** Pernyataan ini benar adanya menurut EIP-8004 — dan persis menjadi distingsi utama jawaban verified 8e09eba3 (di sana DENGAN sitasi eips.ethereum.org). Di kita: tanpa sitasi, dan disajikan sebagai "the sharper point" padahal sudah menjadi tajuk jawaban verified.

**K8 — Sidik jari kuantitatif karangan (§1, §4): "a cluster of 50+ wallets each receiving 0.001–0.01 BNB from a single funding address within 24 h is a Sybil fingerprint"; "a drop below 50% within days indicates…".**

Vonis: **ANGKA TANPA JANGKAR, DISAJIKAN SEBAGAI FAKTA TERUKUR.** Tidak ada sitasi, tidak ada derivasi, tidak ada label "ilustratif". Ambang-ambang ini tidak berasal dari dokumen mana pun yang bisa dibuka verifier.

**K9 — Nama fungsi spesifik (§2): `withdraw()`, `rescueERC20()`, `sweep()`, `setRewardToken()`, `updateVault()`, `claimable()`/`redeemable()`, `onlyOwner createPool()`.**

Vonis: **RISIKO SEDANG.** Dibingkai sebagai daftar contoh pola yang harus dicari — tapi disajikan sebagai enumerasi konkret tanpa satu contoh kontrak nyata yang bisa diverifikasi. Steering secara eksplisit melarang penamaan fungsi yang tidak bisa diverifikasi dari catatan operator; generasi tetap memproduksinya dalam bentuk generik.

**Yang LOLOS dari jawaban kita:** kerangka akuntansi klaimnya sendiri (biaya revert terbakar, pengukuran deplesi dari state counter, klaster pendana) adalah penalaran mekanisme yang sah sebagai Tier-0 — seandainya tidak ditopang angka-angka K1–K5 yang salah. Penutup menamai kebaruan persis sesuai format ("Baru dalam jawaban ini: …"). Struktur ##/### bernomor ada. Panjang 6.580 masuk pita baku.

## 3. Skor arena per-verifier (patuh = 4/4)

**A_CITATION: GAGAL.** 0 sitasi untuk 7 angka berunit + 2 klaim isi dokumen/standar. Ini bukan sitasi-salah-ikat (kasus klaim #1); ini sitasi tidak ada sama sekali.

**A_REASONING: GAGAL.** Premis biaya (K1) salah tentang rantai yang ditanyakan; parameter rantai (K4) basi; angka gas (K2) mustahil secara mekanika EVM; kesimpulan waktu (K5) mewarisi kesalahan premisnya.

**A_UNCERTAINTY: GAGAL.** Register jawaban mutlak dari awal sampai akhir: "is decidable", "shows whether", "fails its distribution goal by design", "exactly as long as". Nol pagar ketidakpastian pada klaim-klaim yang paling bisa dibantah. Ambang karangan K8 dinyatakan sebagai sidik jari yang "decidable from public chain data alone".

**A_SCOPE: GAGAL PARSIAL.** Pertanyaan meminta (i) mekanisme distribusi dan (ii) di mana mekanisme itu gagal. Jawaban kita tidak pernah mengenumerasi taksonomi mekanismenya — §1 soal biaya, §2 soal backing aset, §4 soal metrik pasca-mint: itu metodologi audit yang MENEMPEL di pertanyaan, bukan menjawabnya. Hanya §3 yang menyentuh mode gagal secara langsung.

Skor rubrik QUALITY v1: (a) LOLOS — (b) GAGAL parsial (struktur ada, cakupan sub-pertanyaan miring) — (c) LOLOS — **(d) GAGAL, pintu mati** — (e) LOLOS — (f) GAGAL parsial (§3 menulis ulang distingsi utama 8e09eba3) — (g) LOLOS.

## 4. Kontrol: 5 jawaban VERIFIED di ISR yang sama, checklist identik

**002651ff — 39.592 kar, supported 2/0.** 138 URL. Setiap klaim isi dokumen ditempel sitasi inline — termasuk klaim dokumen Binance yang sama persis dengan K6 kita, di sana lengkap dengan URL-nya. Mekanisme → kegagalan dijawab langsung.

**c02ac23a — 17.585 kar, supported 2/0.** 6 URL + daftar References. Kalimat penutupnya menyatakan sendiri disiplinnya: "All Tier-1 claims are cited to sources I opened and read, and design claims are framed as conditional deductions rather than observed facts."

**8e09eba3 — 8.848 kar, supported 2/0.** 35 URL. Angka-angkanya DERIVASI yang ditampilkan di teks dengan asumsi dinyatakan ("Assuming uniformly distributed hashes, success probability per trial is 2^-d… multiplies expected work by 512") dan kesimpulan dilabeli "deductions from the published construction, not claims of observed exploitation". Ada paragraf "Evidence scope" eksplisit.

**6040432a — 8.836 kar, supported 2/0.** 6 URL + daftar referensi. Spesifiknya nyata dan berjangkar (alamat registry 0x60B9… dengan sitasi BscScan/Sourcify). Taksonomi mekanisme lalu mode gagal, sesuai pertanyaan.

**4eb7c21f — 4.766 kar, supported 2/0.** **0 URL — dan tetap verified.** Kuncinya: 0 klaim Tier-1. Seluruhnya sintesis desain Tier-0 dengan pagar ketidakpastian padat (17 penanda hedge dalam 4,8 rb kar). Ini pola yang sama dengan "nanik" di bedah klaim #1: nol sitasi aman HANYA bila nol spesifik yang bisa dibantah.

Pola kontrol yang konsisten: jawaban verified **mengutip spesifiknya, ATAU tidak menulis spesifik sama sekali**. Tidak ada satu pun verified yang menulis spesifik tanpa jangkar — posisi persis jawaban kita.

## 5. Tabel diskriminator

| Fitur | Kita (097df475, 0/4) | 5 verified (semua 2/0) |
|---|---|---|
| Sitasi/URL | **0** | 4 dari 5 ber-URL (6–138); yang 0-URL nol klaim Tier-1 |
| Angka berunit tanpa jangkar | **7 dalam 6.580 kar** (±1,06/1.000 kar) | 0–1 per jawaban (maks 10 dalam 39,6 rb kar = 0,25/1.000) |
| Parameter rantai benar per 2026 | **Tidak** (base fee, 3 dtk, 21 validator — semua basi/salah) | Tidak ada yang menyandarkan argumen pada parameter rantai yang salah |
| Klaim isi dokumen disitasi | **Tidak** (K6, K7 telanjang) | Ya — klaim Binance-docs yang identik disitasi di 002651ff |
| Pagar ketidakpastian di klaim terbantahkan | **Nyaris nol** (register mutlak) | Paragraf evidence-scope, label deduksi, hedge di titik klaim |
| Cakupan scope (mekanisme + gagalnya) | **Miring** (metodologi audit menempel) | Langsung: taksonomi mekanisme → mode gagal |
| Kebaruan vs verified yang ada | §3 = distingsi utama 8e09eba3 | — |
| Panjang | 6.580 kar | 4.766–39.592 kar — **bukan diskriminator** (falsified lain: 3.129–18.133) |
| Kepatuhan steering | **Dilanggar generasi**: aturan keras "tanpa angka, mekanisme saja" + pita 10–12 rb kar untuk viso ≥5 — keduanya meleset diam-diam (keluar 6.580 kar penuh angka) | — |

Catatan gerbang: draf ini LOLOS probe sendable 3× karena tabel kanonis wrapper hanya mengenal konstanta EIP yang tertanam (45 byte, EIP-2929, dst.) — **parameter BSC tidak ada di tabel itu**, jadi K1–K5 lolos saringan secara struktural. Lolosnya probe adalah bukti celah tabel, bukan bukti kualitas draf.

## 6. Vonis: pemicu refutasi, diperingkat

**Peringkat 1 — Premis biaya EIP-1559 yang salah tentang BSC (K1). Keyakinan TINGGI.**

Paragraf pertama seksi utama menyatakan base fee BSC bergerak mengikuti utilisasi — padahal base fee BSC ditambatkan 0 (BEP-226). Ini klaim bernama-rantai yang bisa dibantah dengan satu pencarian, dan ia menopang seluruh §1. Pemicu A_REASONING + A_CITATION sekaligus.

**Peringkat 2 — Parameter BSC basi: blok ~3 detik, 21 validator, 100 rb blok ≈ 3,5 hari (K4, K5). Keyakinan TINGGI.**

Aktualnya 0,45 detik dan 40+ validator. Jawaban yang menjual "akuntansi yang bisa di-replay verifier dari data publik" runtuh kredibilitasnya di parameter paling dasar rantainya — dan angka turunannya (3,5 hari) salah ±6,7×.

**Peringkat 3 — Biaya klaim ~21.000 gas (K2). Keyakinan TINGGI sebagai kesalahan, SEDANG-TINGGI sebagai pemicu spesifik.**

21.000 adalah biaya transfer polos; mustahil untuk mint berkontrak. Verifier berlatar EVM menangkap ini tanpa alat bantu apa pun.

**Peringkat 4 — Nol sitasi atas klaim isi dokumen (K6, K7). Keyakinan TINGGI sebagai pola.**

A_CITATION adalah 91,1% kegagalan arena_rules (basis QUALITY (d)). Bukti terkuatnya bersifat komparatif: klaim dokumen Binance yang sama, di ISR yang sama, verified — karena disitasi. Versi kita telanjang.

**Peringkat 5 — Ambang kuantitatif karangan (K8, sebagian K9). Keyakinan SEDANG.**

50+ wallet / 0,001–0,01 BNB / 24 jam / <50% — disajikan sebagai sidik jari terukur tanpa sumber. Sendirian mungkin lolos sebagai ilustrasi; tanpa label ilustrasi dan menumpuk di atas Peringkat 1–4, ia menambah permukaan bantahan.

**Peringkat 6 — Defleksi scope (taksonomi mekanisme tidak dijawab). Keyakinan SEDANG-RENDAH sebagai pemicu, TINGGI sebagai penjelas 0 support.**

Refutasi dipicu kesalahan yang bisa ditunjuk; scope yang miring menjelaskan kenapa tidak ada verifier yang merasa jawaban ini layak dibela.

## 7. Sama atau baru dibanding klaim #1?

**Keluarga akar SAMA, mekanisme pemicu BARU — dinyatakan eksplisit.**

Sama: rumusan bedah §42 berlaku kata per kata — "spesifisitas Tier-1, dukungan Tier-0", jalan tengah yang fatal. Kedua jawaban mati di keluarga A_CITATION: klaim spesifik meninggalkan teks tanpa dukungan yang bisa dibuka verifier.

Baru, dalam tiga hal:

**(i) Bentuk kegagalan sitasinya terbalik.** Klaim #1: sitasi ADA tapi tidak mendukung (EIP-2028/4844 diikatkan ke klaim dominasi L1). Klaim #2: sitasi TIDAK ADA sama sekali — tidak ada yang bisa diuji dukungannya.

**(ii) Klaimnya bukan cuma tak didukung, tapi terbantahkan.** Angka keras klaim #1 semua BENAR dan terikat benar (45 byte, 200 gas/byte, 16 gas). Klaim #2 membawa parameter rantai yang salah secara faktual per keadaan BSC 2026 — naik kelas dari A_CITATION murni menjadi A_CITATION + A_REASONING keras.

**(iii) Racunnya masuk di hilir, bukan di hulu.** Steering klaim #1 sendiri yang membawa klaim beracun (angka catatan operator + dominasi bernama-rantai). Steering klaim #2 sudah dibersihkan secara bedah — aturan kerasnya eksplisit: tanpa angka, mekanisme saja. **Generasi melanggarnya diam-diam**: angka-angka baru hasil karangan model menyusup masuk (risiko sisa R1 audit T10 — "generative reinsertion" — kini TERWUJUD), dan self-VFP + wrapper tidak menangkapnya karena tabel kanonis wrapper tidak memuat parameter BSC. Perbaikan di level steering sudah habis; yang gagal kali ini adalah lapisan sensus draf.

Konsekuensi verdict juga lebih berat: klaim #1 masih memungut 2 support (2/2). Klaim #2 **0/4** — tidak ada sisi benar yang cukup besar untuk diselamatkan satu verifier pun.

## 8. Apa persisnya yang harus berubah agar lolos

**Sensus angka wajib di self-VFP (gerbang baru, sebelum wrapper).** Daftarkan SETIAP angka+satuan di draf; tiap angka harus (a) cocok dengan tabel kanonis, (b) diturunkan di dalam teks dengan asumsi dinyatakan (pola 8e09eba3), atau (c) dihapus / dijadikan Tier-0. Draf ini akan gagal sensus **7 kali**.

**Parameter rantai masuk tabel kanonis atau dilarang total.** Blok BSC 0,45 dtk, base fee 0 (BEP-226), harga gas minimum 0,05 gwei, set validator 40+ — masukkan ke tabel fakta yang bisa dicek wrapper/steering, ATAU steering melarang klaim parameter rantai sama sekali di lane yang wrapper-nya tidak bisa memeriksa. Selama celah tabel ada, "lolos probe sendable" tidak boleh lagi dibaca sebagai bukti draf bersih.

**Klaim isi dokumen: sitasi URL saat prep, atau buang atribusinya.** Bila dokumennya tidak dibuka saat persiapan, klaim ditulis sebagai penalaran Tier-0 milik kita ("issuance binds accounts") tanpa menyatakan "documentation states…". Atribusi tanpa penunjuk = permukaan bantahan gratis.

**Urutan scope dibalik: taksonomi dulu, kebaruan kemudian.** Kelima verified membuka dengan mekanisme + mode gagalnya sesuai pertanyaan; bingkai baru (akuntansi forensik) hanya sah sebagai seksi tambahan di atas taksonomi itu, bukan penggantinya.

**Cek tumpang-tindih kebaruan di level seksi, bukan teks.** §3 gugur bukan karena parafrase kalimat, tapi karena distingsinya sudah menjadi tajuk jawaban verified. Pemeriksaan pra-kirim harus membandingkan KLAIM UTAMA tiap seksi melawan klaim utama set verified.

**Uji kepatuhan steering pada draf jadi.** Dua aturan keras steering dilanggar tanpa alarm (larangan angka; pita panjang 10–12 rb untuk viso ≥5 — draf keluar 6.580). Selisih steering-vs-draf harus diperiksa mekanis sebelum tembak, bukan ditemukan di bedah pasca-falsified.

## Lampiran — teks persis jawaban kita (ISO 097df475, 6.580 karakter, sebagaimana terkirim)


```
## Forensic Claim Accounting for Agent-ID–Gated Free Mints on BNB Chain

### 1. On-Chain Claim Accounting: What “Free” Actually Costs

A “free mint” is a claim about `msg.value == 0`; it is not a claim about zero resource cost. Every successful claim transaction pays BNB gas equal to `gas_used × effective_gas_price`, where `effective_gas_price = base_fee + priority_fee` under EIP-1559 on BSC. The base fee moves with block utilization; a contested FCFS window spikes utilization, so the same claim shape that costs ~21 000 gas in a quiet block can cost the same gas at a 5–10× higher base fee when thousands of eligible wallets compete for a capped tranche. The exact per-claim cost for any real window is decidable from public receipts: sum `receipt.gas_used × receipt.effective_gas_price` over all successful `freeMint` calls in the window’s blocks. Reverted attempts are not free either—they burn the gas consumed before the revert (eligibility check, PoW verification, allowance check). A botched or front-run wave therefore imposes real cost on legitimate claimants that zero-price marketing never books; that burn is visible in the same receipts by filtering `status == 0` for the mint contract during the window.

A capped FCFS tranche is consumed in a burst concentrated at the window open. The `freeMinted` counter (or equivalent) increments in the first N blocks of the window; measuring depletion from state changes across those blocks—not from the project’s demand narrative—shows whether the tranche lasted milliseconds or minutes. On BSC’s ~3 s blocks with 21 PoSA validators, priority-gas auctions and private-order-flow relays let searchers place claim bundles in the earliest slots; the tranche’s claimed counter moves in those same blocks. Any verifier can replay this by querying the mint contract’s `freeMinted` (or `totalSupply`) at each block height from `window_start` to `window_start + K` and plotting the step function.

Common-funder clustering is where bot detection actually becomes possible—after the fact, forensically, not at the gate. Claimant wallets funded from one source appear in the native-BNB transfer graph: trace `transfer(from, to, value)` events into each claimant’s address in the blocks preceding their successful mint. A cluster of 50+ wallets each receiving 0.001–0.01 BNB from a single funding address within 24 h of the window is a Sybil fingerprint decidable from public chain data alone. No off-chain identity attestation is required; the funding graph is the ledger’s own witness.

### 2. Claim-Accounting Illusions: What Backs the Entitlement

Nobody in the verified set audits the asset side. A bundled reward is a promise whose backing sits somewhere, and whether a successful claim is worth anything is decidable from the distribution contract itself. Two patterns dominate:

**Reserve held inside the mint contract (or an owner-controlled vault).** Enumerate every function that can move that reserve: `withdraw()`, `rescueERC20()`, `sweep()`, `setRewardToken()`, `updateVault()`. If the owner (or a multisig/timelock admin) retains any path to drain unclaimed rewards, late claimants face a gate that works perfectly while the reward reserve is emptied. This is checkable by reading the contract’s bytecode on BscScan, identifying the reserve-holding address, and listing all `onlyOwner`/`onlyRole` functions that write to it. If the reserve is an ERC-20, check `allowance` grants to the owner. A verifiable audit states: “Reserve at 0x…; owner 0x…; withdrawal paths: X, Y, Z; timelock: T; multisig: M-of-N.”

**Reward locked until a completion threshold.** Some designs mint a claim token (or credit an internal ledger) that becomes redeemable only after a sellout, pool initialization, or governance vote. The claimant’s balance reads full while realizable value is zero for exactly as long as the threshold stays unmet. The distribution succeeded as an accounting entry and failed as value transfer. The checkable discipline: before trusting any gated free mint, read the redemption contract’s `claimable()`/`redeemable()` logic and the threshold condition—`totalMinted >= MAX_SUPPLY`, `poolCreated == true`, `governanceProposal.executed == true`—not just the gate. If the threshold can be blocked by the owner (e.g., `onlyOwner createPool()`), the lock is revocable in substance.

### 3. Sanctioned Multi-Identity: Issuance Binds Accounts, Not Humans

The corpus frames multiple identities only as attack. The sharper point: issuance binds **accounts**, not humans. Binance Agentic Wallet documentation states each user may create one Agentic Wallet and claim one `.ai` handle; ERC-8004 explicitly permits transferable agent identities and multiple registrations. A platform operator legitimately running two issued identities—their own agent and a family member’s agent they operate—is on-chain indistinguishable from a Sybil farm. Both satisfy `handleOf(msg.sender)!= ""` and `!claimed[identityKey]`. “One per identity” therefore fails its distribution goal by design, with no rule broken and no attack to detect. The gate enforces credential scarcity; it cannot enforce human scarcity because the credential’s issuance policy does not claim to.

### 4. Measurable Success Criterion: Post-Mint Distribution Forensics

Judge a gated mint not by claims blocked at the gate but by post-mint distribution: holder concentration after consolidation versus at mint, and share of claims still holding at a later block. The gate’s own logs cannot show this; only the transfer graph can. From the NFT’s `Transfer` events, compute the Herfindahl-Hirschman Index (HHI) of holder balances at `mint_end_block` and at `mint_end_block + 100 000` (~3.5 days on BSC). A rising HHI signals consolidation into fewer wallets—exactly the farming outcome the gate was meant to prevent. Simultaneously, track the fraction of mint-recipient addresses that still hold the token at the later block. A drop below 50% within days indicates the “free” NFTs were immediately flipped or wrapped, making the gate a liquidity bootstrap for farmers rather than a distribution to users. Both metrics are decidable from public `Transfer` events alone; no project cooperation required.

Baru dalam jawaban ini: claim accounting replayable from public chain data—gas-cost scaling with window contention, reverted-claim burn, FCFS burst measurement via state-counter steps, and common-funder clustering via the funding graph—plus the reserve-side audit (owner powers over the reward reserve and the lock conditions) as the other half of any gated mint.
```
