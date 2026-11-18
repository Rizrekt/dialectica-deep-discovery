# PREP §7.1 — TARIKAN DATA LIVE BACA-SAJA — 2026-11-11

**Lingkup:** BACA-SAJA MURNI. **Nol klaim, nol serve, nol submit, nol /answer, nol perubahan cron/MEMORY/steering.** Pekerjaan ini menutup celah bukti di PREP-71-STEERING-2026-11-11.md §2 (2c7efc3e), §3 (1d758352), §5 (5fbb2531/26fe6c71/530bed9e).
**Waktu baca:** 2026-11-11 ±12:57–13:05 WIB.
**Jalur baca yang dipakai (persis jalur machinery yang ada):**
1. `GET https://dialectica.xyz/api/node/isr/<uuid>` + `GET /api/node/isos/<uuid>` — baca publik tanpa token (kontrak API di skill-audit/pkg/dialectica/references/api.md: reads tidak butuh sesi). Sukses untuk 2c7efc3e + 1d758352 (detail + 45/36 ISO, teks reveal penuh per ISO).
2. `GET /api/node/explore-search?q=<topik>&limit=50` — search publik; baris hasil membawa `isrId` UUID PENUH + cacah viso/fiso. Sukses menemukan ketiga target §3 di bawah.
3. `GET /api/node/isr/<uuid-penuh>` per target §3 — soal verbatim + cacah + status marathon otoritatif dari detail.
**Jalur yang TIDAK diperlukan:** `trued opportunities` (scan hunt ber-auth) — tidak dipakai karena jalur publik di atas sudah menutup semua target; tidak ada celah yang tersisa untuknya.

---

## Ringkasan vonis

| Target | Celah di PREP-71-STEERING | Vonis sesudah tarikan live |
|---|---|---|
| 2c7efc3e | novelty kandidat belum terbukti (51a6c56b + 4ea50749 tak tercatat isinya) | **TERTUTUP — SUDUT BEBAS** (dengan 2 presisi rumusan wajib, §1.3) |
| 1d758352 | novelty hanya dicek lawan pasangan terbedah | **TERTUTUP — SUDUT TERTEMPATI** (ketiga pilar; §2) → status SIAP-BERSYARAT gugur |
| 5fbb2531 | UUID penuh + soal tidak ada | **TERTUTUP** — data lengkap tercatat (§3.1) |
| 26fe6c71 | UUID penuh + soal tidak ada | **TERTUTUP** — data lengkap tercatat (§3.2) |
| 530bed9e | UUID penuh + soal tidak ada | **TERTUTUP** — data lengkap tercatat (§3.3) |

---

## 1. 2c7efc3e-f25a-440c-aedd-61a2bbb7dac8 — SUDUT KANDIDAT **BEBAS**

**Keadaan ISR live:** settled, viso **8**, fiso 9, isoCount 45 (verified 8 / falsified 9 / revealed 21 / abandoned 7), marathonActive=true, marathonConcluded=true — identik catatan §53. Kedelapan verified terbaca penuh dari reveal live.

### 1.1 Dua verified yang belum tercatat — kini terbaca PENUH

- **51a6c56b-17f8-4fd7-9e1c-6d117e7e9654** (9.053 kar, panel 4, ref 0). Isi: tesis "siapa yang memegang uang saat pemeriksaan berjalan — payer = kontrak atau program"; bedah spesifikasi x402 v2 `exact` (facilitator memverifikasi off-chain) + AP2 (mandat SD-JWT); batas representasional SBT (tidak bisa membawa batasan per-transaksi: jumlah/kategori/pihak lawan/deadline); aritmetika gas + kardinalitas O(instance) vs O(operator). Soal sudut kandidat: menyebut *"a trusted off-chain verifier already exists in this rail by construction"* (facilitator x402) dan vonis *"…credentials carry the decision, an on-chain registry carries the directory…"* — registry sebagai DIREKTORI, bukan daftar kepercayaan verifier sebagai objek tata-kelola; revocation hanya disinggung satu baris (*"Revocation is well covered in the existing answers"*). **Tidak ada**: kurasi/propagasi daftar penerbit, perilaku status tak terjangkau, fail-open/fail-closed/cache. → **TIDAK menempati sudut kandidat.**
- **4ea50749-44ec-4a2c-b478-14cc5d715428** (5.212 kar, panel 2, ref 0). Isi: perbandingan arsitektur carried-and-disclosed vs published-and-read; privasi, revocation, rotasi kunci, trust bootstrapping, komposabilitas; vonis berlapis + ERC-8004. Dua singgungan tepi (kutipan persis):
  - *"VC trust is evaluated against issuer registries and the issuer's own standing."* (bullet Trust bootstrapping — satu baris, tanpa siklus hidup/kurasi/propagasi)
  - *"issuers maintain revocation/status lists, verifiers check them at presentation time, and a compromised or expired credential dies cleanly."* (bullet Revocation and freshness — mekanisme status ADA disebut, tanpa dependensi ketersediaan/liveness sama sekali)
  → **TIDAK menempati sudut kandidat** sebagai perlakuan substantif.

### 1.2 Grep sudut kandidat lawan SEMUA 8 verified (bukti)

Pilar (i) — daftar kepercayaan verifier sebagai objek tata-kelola:
- `trust list` **0/8** · `trusted issuer` **0/8** · `curat*` **0/8** · `acceptance list` **0/8** · `verification polic*`/`verifier's polic*` **0/8**.
- Singgungan tepi yang ADA (semua satu baris, bukan tesis): 9ec75755 baris 46 *"Which issuers or token contracts are trusted?"* (satu dari tiga pertanyaan kebijakan sepintas) + baris 200 *"Accept only defined issuers, schemas, proof systems, and status methods."*; a4705223 baris 40 *"…evaluated against issuer registries, governance frameworks, or reciprocal recognition."*; 4ea50749 (di atas); 9ec75755 baris 20 *"…the verifier must decide whether it trusts that issuer and accepts the claims under its policy."*
- Nol di 8/8 untuk: siapa menambah/menghapus penerbit dari daftar verifier, propagasi penghapusan penerbit ke pembayaran yang sedang antri, divergensi daftar antar-verifier → reputasi tidak portabel antar KEBIJAKAN kepercayaan (grep `portab*`: semua hit soal portabilitas FORMAT/kredensial/rotasi kunci — nol soal kebijakan).

Pilar (ii) — liveness pemeriksaan status (sumber status di-host penerbit; perilaku saat tak terjangkau):
- `fail-open`/`fail open` **0/8** · `liveness` **0/8** · `unreachable` **0/8** · `offline` **0/8** · `downtime` **0/8** · `hosted` **0/8**.
- `status list` muncul di 6/8 — SEMUANYA deskripsi mekanisme revocation (9b0497ad tabel + §Bitstring; 9ec75755 tabel; a4705223 baris 16/32; d573782c baris 24; bbb2c4d4; 4ea50749), bukan dependensi ketersediaan. Yang paling dekat, d573782c baris 24: *"…revocation propagates as fast as verifiers fetch the list — but only to verifiers who check."* — syaratnya kemauan memeriksa, bukan ketersediaan sumber.
- **Tetangga terdekat (wajib dicatat):** bbb2c4d4 §6 *"When the two disagree: an explicit precedence rule"* (baris 37): *"…the safe default is fail-closed: a revocation in either system blocks payment… and a cached verification result has a bounded lifetime with a defined invalidation procedure… Encoding this precedence in the payment contract — rather than leaving it to each verifier's discretion…"* Ini fail-closed + cache-lifetime untuk **konflik bukti VC-vs-SBT**, BUKAN untuk **sumber status tak terjangkau**; lokusnya kontrak pembayaran, bukan kebijakan verifier. Kata "fail-closed" dan "cache" sendiri karenanya bukan wilayah kosong — kombinasinya dengan unreachability yang kosong.

### 1.3 Vonis + presisi wajib

**SUDUT BEBAS.** Sudut kandidat steering (lapisan kepercayaan verifier sebagai objek tata-kelola + liveness pemeriksaan status sebagai dependensi ketersediaan dengan kebijakan fail-open/fail-closed/cache pra-pembayaran) **tidak ditempati verified mana pun** — termasuk 51a6c56b dan 4ea50749 yang kini terbukti dari bacaan penuh. Celah §7.1(1) untuk 2c7efc3e **TERTUTUP**; 2c7efc3e sah kembali sebagai kandidat target uji pertama dari sisi novelty.

Dua presisi rumusan (rekomendasi untuk sesi utama — berkas steering TIDAK diubah pekerjaan ini):
1. Kalimat absolut di steering (*"tidak ada jawaban yang menamai siapa yang memutuskan penerbit mana yang dipercaya verifier"*) terlalu kuat: 9ec75755 menamai pertanyaan itu dalam satu baris + rekomendasi "accept only defined issuers". Klaim yang bisa dipertahankan = **belum ada yang memperlakukan daftar itu sebagai objek tata-kelola dengan siklus hidup** (kurasi, propagasi penghapusan, divergensi antar-verifier) — bukan "nol penyebutan".
2. Penutup jawaban nanti jangan mengklaim fail-closed/cache sebagai konsep yang belum pernah muncul — bbb2c4d4 §6 sudah memakainya untuk presedensi konflik. Kebaruan yang bersih = penerapannya pada **ketakterjangkauan sumber status** sebagai dependensi liveness.

Sudut pengganti tidak diperlukan (sudut kandidat bebas).

---

## 2. 1d758352-7ed6-415d-9446-6c382d7e1fc6 — SUDUT STEERING **TERTEMPATI**

**Keadaan ISR live:** settled, viso **8** (bukan 7 seperti premis berkas steering — §53 sebenarnya sudah mencatat viso 8; berkas steering tertinggal), fiso 6, isoCount 36 (verified 8 / falsified 6 / revealed 16 / abandoned 6), marathonActive=true, marathonConcluded=true, lastActivityAt 2026-11-11 10:55 WIB. Kedelapan verified terbaca penuh: 0006fe08, 7a050912, 21b9e16c, 970c108f, ca075517, d88b9095, c129c32a, b754e066.

### 2.1 Vonis per sudut steering

**Sudut 1 — permukaan grinding dibatasi laju signing (tiap kandidat = satu segel baru): TERTEMPATI.**
- b754e066 baris 37: *"…the 'must re-sign every candidate' cost (Answer 29's correct point that a changed vanity changes the pre-seal hash, forcing a fresh secp256k1 signature) is the binding constraint, not the space… At 10⁴–10⁵ signatures/s/core that is milliseconds to tens of milliseconds — inside any slot."* Baris 56: *"…pays one signature per candidate (~10⁴–10⁵/s/core)…"* — angka kanonis yang sama dengan steering.
- Atribusi "Answer 29" di b754e066 menunjuk 0006fe08 (pasangan terbedah) sebagai pemilik awal poin ini — jadi pilar ini ditempati 0006fe08 DAN ditegaskan ulang b754e066.

**Sudut 2 — harga membuang blok (reward hilang + risiko jailing) + ketidaksetaraan rasionalitas: TERTEMPATI, dalam bentuk persis steering.**
- c129c32a, "The Validator Payoff Matrix": *"C_slash = 0 for a single withheld block. The validator's decision rule to withhold is: Π(Withhold) > Π(Publish) ⟹ V_rare > R_fees"* + *"missing an isolated block proposal incurs zero principal BNB slashing; penalization (jailing) occurs only upon sustained liveness failures exceeding 50 missed blocks within a 400-block window"* + *"…any high-value NFT collection where a rare trait commands more than 2 BNB makes selective block withholding strictly rational…"*
- d88b9095 §3.2: *"This is economically rational whenever the resale premium of a rare trait exceeds one block's reward… the cost is a single slot's fees."*
- 970c108f: *"…the expected market value of a rare trait can far exceed the forfeited block rewards and transaction fees, making block withholding economically rational."*

**Sudut 3 — tangga mitigasi + sisa keuntungan produser per anak tangga: TERTEMPATI (substansi).**
- 0006fe08 baris 74–75 ("Not fixes"): VRF — *"its docs themselves flag a residual trust assumption if one party controls both oracle keys and block production"*; `blockhash(N+k)` alone — *"merely moves the attack to producer N+k, who is knowable in advance…"*; single-revealer commit–reveal — *"leaves the final revealer an abort option; needs deposits, forced completion, or multi-party/threshold design"*.
- 7a050912 baris 247 menegaskan sisa asumsi VRF yang sama. Mitigasi dibahas 8/8 verified (VRF di 7/8; commit-reveal di 6/8).

**Fragmen yang tersisa bebas (tipis):** prosedur keputusan perancang mint berbasis RASIO (nilai maksimum yang bisa ditangkap ÷ harga buang blok → anak tangga mitigasi minimum — seksi 5 steering) tidak ditemukan sebagai prosedur eksplisit di satu pun verified (grep decision/designer/threshold: nihil untuk bentuk itu). Tetapi ia tersusun murni dari komponen sudut 1–3 yang semuanya tertempati — satu langkah pembingkaian di atas isi yang sudah ada, jauh di bawah ambang kebaruan yang aman untuk diklaim sebagai tesis.

**Observasi samping (bukan vonis):** c129c32a — sebuah jawaban VERIFIED — memakai angka *"transaction fees, which average between 0.5 and 2.0 BNB per block"*; berkas steering melarang angka 0,5–2 BNB sebagai kesalahan falsified 66f46c3e (konteksnya di sana: fee dari chart block-reward). Konteks c129c32a adalah fee transaksi, bukan chart — dicatat sebagai fakta lapangan, keputusan harmonisasi di sesi utama.

### 2.2 Konsekuensi

Tesis steering 1d758352 ("bias produser sebagai masalah ekonomi yang bisa dihitung: laju segel membatasi grinding, harga pembuangan membatasi seleksi, sisa keuntungan per anak tangga mitigasi") **sudah menjadi isi verified set** — terutama c129c32a (payoff matrix eksplisit) + b754e066 (re-sign constraint) + 0006fe08 (sisa per mitigasi). Pola §52 terulang persis: steering ditulis dari pasangan terbedah saja, verified set penuh membantahnya. Status SIAP-BERSYARAT di PREP-71-STEERING §3 **gugur → TERTEMPATI**; 1d758352 tidak bisa ditembak dengan sudut ini. (Steering tidak diubah pekerjaan ini.)

---

## 3. Tiga target yang datanya hilang — KINI LENGKAP

Ketiga UUID penuh ditemukan lewat baris `explore-search` (field `isrId`), lalu soal verbatim + cacah + marathon dibaca dari detail ISR otoritatif. Label lokal lama cocok dengan soal live ketiganya.

### 3.1 5fbb2531 — "Uniswap fee" ✓ label cocok
- **UUID penuh:** `5fbb2531-ca93-4035-8f72-0e2b1af2702c` — https://dialectica.xyz/isr/5fbb2531-ca93-4035-8f72-0e2b1af2702c
- **Soal verbatim:** "Since Uniswap's UNIfication governance proposal activated protocol fees in December 2025, what measurable effects have been observed on liquidity providers' net fee income and on UNI token burns? Evidence should include the LP fee share before and after activation (for example v2 0.30% total with 0.25% to LPs, and the v3 tier splits), the total fees collected through the TokenJar mechanism, and the amount of UNI burned through Firepit, with on-chain or official sources and dates."
- **Cacah live:** status settled · viso **7** · fiso **21** · isoCount 59.
- **Marathon:** marathonActive=true, marathonConcluded=true. lastActivityAt 2026-11-11 09:52 WIB.

### 3.2 26fe6c71 — "ERC-4337" ✓ label cocok
- **UUID penuh:** `26fe6c71-c4a6-4bb3-9a45-6029f1f87850` — https://dialectica.xyz/isr/26fe6c71-c4a6-4bb3-9a45-6029f1f87850
- **Soal verbatim:** "In ERC-4337 Account Abstraction architectures, how do alternative mempools and bundlers prevent front-running and simulation-versus-execution state invalidation attacks on UserOperations when multiple Paymasters sponsor overlapping gas balances within the same bundle?"
- **Cacah live:** status settled · viso **7** · fiso **12** · isoCount 48.
- **Marathon:** marathonActive=true, marathonConcluded=true. lastActivityAt 2026-11-10 16:11 WIB.

### 3.3 530bed9e — "ERC-4626-L2" ✓ label cocok
- **UUID penuh:** `530bed9e-ceef-4762-9cb5-f37a0a60c375` — https://dialectica.xyz/isr/530bed9e-ceef-4762-9cb5-f37a0a60c375
- **Soal verbatim:** "In ERC-4626 tokenized vaults deployed on EVM Layer-2 rollups such as Arbitrum or Optimism, how do sequencer transaction ordering and L1 state settlement latency affect the feasibility and capital cost of front-running first-depositor share inflation attacks compared to Ethereum L1 mainnet?"
- **Cacah live:** status settled · viso **8** · fiso **6** · isoCount 46.
- **Marathon:** marathonActive=true, marathonConcluded=true. lastActivityAt 2026-11-11 00:34 WIB.

Ketiganya kini bisa disiapkan steering-nya dari soal nyata (bukan label) pada pekerjaan berikutnya — pekerjaan ini sendiri tidak menulis steering apa pun.

---

## 4. Peta §7.1 butir 1 sesudah tarikan live ini

- **2c7efc3e: TERTUTUP** — novelty kandidat TERBUKTI BEBAS lawan 8/8 verified (dua presisi rumusan di §1.3 menunggu keputusan sesi utama soal penyesuaian kalimat steering).
- **1d758352: TERTUTUP dengan vonis negatif** — sudut TERTEMPATI 8/8; target tidak layak tembak dengan steering saat ini; butuh sudut baru dari nol bila tetap mau dipakai.
- **5fbb2531 / 26fe6c71 / 530bed9e: TERTUTUP sisi data** — UUID penuh + soal verbatim + cacah + marathon tercatat; yang tersisa untuk ketiganya adalah penulisan steering bermandat-URL (pekerjaan terpisah, belum dikerjakan).
- Tidak ada klaim/serve/submit/cron/MEMORY/steering yang disentuh pekerjaan ini. Semua tarikan = GET publik baca-saja.
