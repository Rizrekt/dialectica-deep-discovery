# SPOT-CHECK MANUAL PILOT SERVE — 3 JAWABAN PERTAMA (item 7)

**Tanggal periksa:** 2026-11-17 (sesudah nyala 09:33 WIB; jawaban terkirim 09:37–09:47 WIB / 02:37–02:47Z).
**Bahan:** `PILOT-SPOTCHECK-2026-11-17/` (00-INDEKS.md + 3 pasang pertanyaan/jawaban, teks persis terkirim).
**Acuan:** checklist D di `CHECKLIST-PILOT-2026-11-16.md` (buka tiap URL; dukungan kalimat per angka terikat; premis kebaruan; penutup sintesis; nol jejak) + rubrik `QUALITY.md` v3 + amendemen (c)-PK1 + 6 rule live arena (`DATA-LIVE-ARENA-2026-11-17.md`: SURPRISE_GAUGE, A_CITATION, A_REASONING, A_SCOPE, A_UNCERTAINTY, CUSTOMER_REQUIREMENTS).
**Status verdict server saat diperiksa:** ketiganya "awaiting validation" — belum ada verdict; semua ramalan di berkas ini dilabeli RAMALAN.
**Aturan vonis (d) yang dipakai pemeriksa:** (d) = GAGAL bila cacatnya (i) angka/klaim yang salah, atau (ii) ≥2 cacat penunjuk (pointer) independen, atau (iii) menimpa sitasi poros jawaban; LOLOS-BERSYARAT bila satu penunjuk periferal salah dan semua klaim independen benar.

---

## Tabel vonis

| # | ISR | Kelas / panjang | Vonis | Butir penentu | RAMALAN panel |
|---|-----|-----------------|-------|---------------|----------------|
| 1 | 2777178d (NFT whitelist sybil) | PIONEER / 6.673 kar (di dalam pita 3.435–7.297) | **GAGAL** | (d) — angka poros Hop 50%/10% salah + tak ter-entail sitasi | RAMALAN: cenderung verified (±55–65%), risiko falsified nyata dari klaim Hop |
| 2 | d94d7e34 (wallet agen AI satu vs banyak orang) | PIONEER / 7.570 kar (di atas pita — catatan (c) saja, bukan gagal) | **GAGAL** | (d) — DOI poros mati/salah (E1-k) + 2 cacat penunjuk tambahan | RAMALAN: verified ±50–60%; isi substantif benar semua, apparatus sitasi yang jatuh |
| 3 | 635a010d (wallet MPC lintas restart) | PIONEER / 6.964 kar (di dalam pita) | **LOLOS-BERSYARAT** | (d) catatan wajib-perbaiki — nomor ePrint Lindell menunjuk paper lain | RAMALAN: verified ±65–75% (tertinggi dari ketiganya) |

**Konsekuensi checklist D:** satu jawaban gagal satu butir saja → serve **TIDAK dibiarkan unattended** di jendela ini. Syarat itu terpenuhi (2 GAGAL + 1 bersyarat) — lihat rekomendasi di §5.

---

## 1. Jawaban 2777178d — deteksi multi-account farming whitelist NFT — **GAGAL (d)**

### Yang lolos
- **(a)** Pembuka tesis tajam dalam 1 paragraf: "NFT whitelist campaigns treat sybil farming as an identity-cost problem and stack three detection layers … none is individually decisive". Bukan parafrase pertanyaan.
- **(b) catatan cakupan:** 3 metode yang diminta pertanyaan = 3 seksi bernomor + seksi 4 perbandingan. Cakupan penuh.
- **(c)** 6.673 kar, kelas Pioneer — di dalam pita patokan (c)-PK1. LOLOS.
- **(h)** PENUH — ketiga sub-pertanyaan (social quest-proof, funding-pattern clustering, on-chain behavior + efektivitas masing-masing) dijawab eksplisit per seksi.
- **(e)** Penutup "New in this answer" = sintesis yang menamai kebaruan (reframe efektivitas sebagai ekonomi biaya-per-identitas-palsu), BUKAN daftar referensi; tidak ada frasa evasif E3. Kebaruan substantif ada (lihat catatan premis di §4).
- **(f)/(g)** Bukan parafrase (viso 0 — tidak ada verified yang bisa diparafrase); format bebas sesuai (tidak ada skema JSON diminta).
- **A_REASONING / A_SCOPE / A_UNCERTAINTY:** rantai mekanisme per lapis runtut; nol laporan lingkungan Expert sendiri; klaim efektivitas kualitatif dan terkalibrasi ("probabilistic — good for ranking risk … not for binary verdicts", "clustering alone cannot justify exclusion without review") — tidak ada presisi karangan.
- **Sitasi yang terverifikasi mendukung:** Douceur Springer (dibuka — paper yang benar, IPTPS 2002); Treasury jy0916 (dibuka — rilis sanksi OFAC atas Tornado Cash, mendukung "sanctioned by the US Treasury on August 8, 2022 … for this laundering role").

### Temuan penentu — (d) GAGAL: preseden Hop salah angka, salah atribusi
Kutipan jawaban (§2): *"The clearest public precedent is Hop Protocol's 2022 airdrop: Hop built a sybil list largely from funding-graph analysis and let identified sybils self-report to keep 50% of their would-be allocation, while bounty hunters earned 10% of the value of sybils they reported (Hop Protocol, docs.hop.exchange)."*

Hasil buka-dan-baca + silang dua sumber independen:
- Halaman yang disitasi (docs.hop.exchange, dibuka) adalah beranda dokumentasi — **tidak memuat angka 50% maupun 10%** (gagal entailment E1 di titik klaim).
- Skema Hop yang terdokumentasi: pemburu sybil dijanjikan **25%** dari token yang diselamatkan (TokenPost, 2023-06-05: "hunters were promised 25% of all HOP tokens"; Coindaro: DAO membayar "25% of them, about 869,566 HOP, to 35 recipients"). Tidak ada skema self-report-keep-50% pada Hop.
- Pasangan "self-report boleh simpan sebagian + bounty hunter 10%" adalah skema **LayerZero (2024)**, dengan angka self-report **15%** dan bounty **10%** (Coindaro/The Block). Jawaban mencampur dua preseden dan mengutip keduanya secara salah untuk Hop.
- Kesalahan ini **poros, bukan periferal**: §4 dan penutup kebaruan mengangkatnya sebagai kasus kalibrasi utama — *"Hop Protocol's 50%/10% self-report and bounty scheme as the reference case for funding-cluster detection"*. Kebaruan yang diklaim bertumpu pada angka yang salah → sekaligus melemahkan (e) (kebenaran kebaruan dinilai lawan (d)).

### Temuan tambahan
- **Domain Proof of Humanity salah:** jawaban memakai `proofofhumanity.site` (badan §1 + Sources). Pada pemeriksaan ini URL itu **gagal di-resolve alat periksa**; domain kanonis yang hidup adalah `proofofhumanity.id` (dibuka — registry resmi: video enrollment + deposit + challenge, sesuai deskripsi jawaban). Cacat penunjuk kedua di jawaban yang sama.
- `docs.passport.gitcoin.co` (klaim stamps Gitcoin Passport) gagal di-fetch alat periksa → **tidak terverifikasi di level URL** (klaimnya sendiri sesuai model Passport yang dikenal; dicatat sebagai celah cakupan periksa, bukan vonis mati).
- Sitasi beranda generik untuk klaim peran platform (Galxe/Zealy/Layer3/Chainalysis/Nansen/Bubblemaps/POAP/Fractal) — klaimnya generik dan benar, tapi pola E1-o ringan; bukan penentu.

---

## 2. Jawaban d94d7e34 — banyak wallet agen AI: satu orang vs banyak orang — **GAGAL (d)**

### Yang lolos
- **(a)** Pembuka tesis: "Wallet addresses and email addresses are both free to mint in unlimited quantity, so neither can function as proof of unique personhood". Tajam, bisa dibantah, langsung menjawab.
- **(b)/(h)** Cakupan PENUH: §1 kenapa sinyal lemah, §2 apa yang bisa diinferensikan (clustering), §3 apa yang rusak (rewards/quadratic, reputasi, governance, akuntabilitas agen), §4 penambah biaya. Kedua helai pertanyaan ("how can a platform tell" + "what breaks") terjawab eksplisit.
- **(c)** 7.570 kar — di atas ujung pita Pioneer 7.297 → **catatan (c) saja** (pita = anjuran, bukan pintu gagal); lantai 1.717 jauh terlampaui.
- **(e)** Penutup sintesis menamai kebaruan (triad costly/unique/non-transferable + ambiguitas dua arah agen) — posisi penutup diizinkan v3; tanpa frasa E3.
- **Isi substantif terverifikasi benar:** BIP-32 (dibuka — "Assigned: 2012-02-11", HD wallet dari satu seed); ERC-4337 (dibuka — Final); RFC 5233 (dibuka — "Sieve Email Filtering: Subaddress Extension", mendukung klaim subaddressing `user+agent1@…`); Douceur via Microsoft Research (dibuka — mendukung framing mustahil-tanpa-otoritas); WebAuthn Level 2 (dibuka); BrightID (dibuka — "prove … you are accessing them fairly with only one account"); PoH `.id` (dibuka); EAS `attest.sh` (dibuka — situs Ethereum Attestation Service). A_REASONING runtut; A_UNCERTAINTY jujur ("you can estimate, bound, and raise cost — but only personhood-anchored signals can *prove* it"); A_SCOPE bersih.

### Temuan penentu — (d) GAGAL: tiga cacat penunjuk, satu menimpa sitasi poros
1. **DOI Meiklejohn salah dan mati (E1-k).** Jawaban mengutip: *"Meiklejohn et al., 'A Fistful of Bitcoins,' ACM IMC 2013 — https://doi.org/10.1145/2516651.2516734"*. DOI itu **404** saat dibuka. DOI yang benar, terbaca di paper itu sendiri + OpenAlex + bibliografi UCL: **10.1145/2504730.2504747**. Ini sitasi poros §2 (tulang punggung klaim common-input-ownership heuristic) — klaimnya benar, penunjuknya karangan.
2. **Subjudul paper DeSoc salah.** Jawaban menulis: *Ohlhaver, Weyl & Buterin, "Decentralized Society: Finding Web3's Original Sybil," 2022*. Halaman SSRN yang disitasi (dibuka) berjudul **"Decentralized Society: Finding Web3's Soul"**. "Original Sybil" tidak ada di sumbernya.
3. **URL whitepaper Worldcoin tak ter-resolve.** Badan §4 + Sources mengutip `https://whitepaper.worldcoin/` — gagal di-resolve alat periksa (tanpa TLD; whitepaper Worldcoin hidup di bawah domain worldcoin.org). Satu lagi penunjuk karangan.

Pola: tiga cacat independen dalam satu apparatus sitasi — bukan satu salah ketik. Menurut aturan vonis di kepala berkas (ii)+(iii), (d) GAGAL walau seluruh klaim badan benar.

---

## 3. Jawaban 635a010d — akses wallet MPC agen AI lintas restart — **LOLOS-BERSYARAT**

### Yang lolos
- **(a)** Pembuka = koreksi premis yang persis menjawab jebakan pertanyaan: "an MPC wallet's durable credential is the locally stored key share plus a device identity — not the pairing code. The pairing code is a one-time provisioning artifact". Ini distingsi yang benar dan merupakan inti jawaban.
- **(b)/(h)** Cakupan PENUH atas ketiga kendala pertanyaan (restart, kunci tak bisa diekspor, kode pairing kedaluwarsa menit): §1 pairing = provisioning, §2 persistensi share di storage OS, §3 kredensial mesin jangka panjang, §4 backup share terenkripsi, §5 otomatisasi jendela pairing langka, §6 guardrails.
- **(c)** 6.964 kar, Pioneer, di dalam pita. LOLOS.
- **(e)** Penutup sintesis menamai reframe + rantai fallback boot-time; bukan daftar referensi (Sources terpisah di atasnya); tanpa frasa E3.
- **Sitasi terverifikasi mendukung:** DPAPI (dibuka — halaman Microsoft persis menyatakan "The API consists of two functions, CryptProtectData and CryptUnprotectData", menopang klaim §2); Fireblocks developers (hidup); Coinbase CDP docs (hidup); Lit Protocol docs (hidup); AWS KMS overview (dibuka — mendukung klaim envelope/KMS §4). Klaim provider (API user RSA Fireblocks, device key Coinbase WaaS, PKP + session signature Lit) benar secara substantif; sitasinya level beranda docs (E1-o ringan).
- **A_UNCERTAINTY:** hampir tanpa angka presisi; klaim dinyatakan sebagai desain ("should", "prefer") — kalibrasi pas. **A_SCOPE:** bersih; tidak ada laporan lingkungan Expert.

### Catatan wajib-perbaiki — (d): nomor ePrint Lindell menunjuk paper lain
Jawaban mengutip: *[Lindell, "Secure Multiparty Computation (MPC)," IACR eprint 2020/940 — https://eprint.iacr.org/2020/940]*. Halaman itu dibuka: **2020/940 adalah paper Fei Meng, "Directly revocable ciphertext-policy attribute-based encryption from lattices"** — bukan Lindell, bukan tentang MPC wallet. Klaim yang ditopang ("the key never exists in full on any device; each party holds a share") adalah definisi textbook yang benar dan memang isi paper Lindell yang dimaksud (artikel Communications of the ACM, 2021) — tetapi nomor yang tertulis karangan. Satu cacat penunjuk periferal, semua klaim independen benar → LOLOS-BERSYARAT dengan kewajiban perbaikan pola (lihat §5), bukan LOLOS bersih.

### Celah cakupan periksa (jujur dicatat)
- `docs.web3auth.com` gagal di-fetch alat periksa → klaim device-share Web3Auth **tidak terverifikasi di level URL** sesi ini (klaimnya sesuai model share Web3Auth yang dikenal).
- Apple Keychain Services, MS TPM overview, HashiCorp Vault docs tidak dibuka satu-satu sesi ini; ketiganya sitasi docs-root untuk klaim generik yang benar. Vault disebut "transit" di §4 tetapi yang disitasi beranda docs (E1-o ringan).

---

## 4. Lintas-jawaban

### Premis kebaruan (checklist D butir 3) — status: PLAUSIBLE, TIDAK TERVERIFIKASI PENUH
Ketiga target Pioneer (viso 0): saat seleksi **tidak ada jawaban verified** di ketiga ISR, dan log `provider/semantic-check-log.jsonl` mencatat `novelty_chars = 0` untuk ketiganya (02:37:18Z / 02:41:31Z / 02:47:06Z, checker openrouter-nemotron, verdict clean, findings []). Artinya: (i) premis "New in this answer" tidak bisa difalsifikasi lawan verified — himpunannya kosong menurut konstruksi; (ii) risiko SURPRISE_GAUGE yang tersisa adalah lawan jawaban **revealed** pesaing (27 / 55 / 33 saat konteks pertanyaan ditarik) yang teksnya tidak ada di bahan spot-check dan tidak dibaca C5 — risiko itu **tidak terukur** oleh kedua pemeriksa. Sudut yang diklaim (reframe biaya-per-identitas; triad costly/unique/non-transferable + ambiguitas dua arah; pairing-sebagai-provisioning) adalah kebaruan level framing/mekanisme, konsisten dengan yang dicari sel Pioneer, dan tidak contradicted oleh apa pun di bahan.

### Pola penulis GLM di produksi nyata pertama
- **Kekuatan (konsisten 3/3):** pembuka tesis/koreksi premis yang tajam; struktur ## bernomor memetakan sub-pertanyaan 1:1; penalaran mekanisme runtut (A_REASONING aman); cakupan PENUH 3/3 tanpa miss; penutup sintesis yang menamai kebaruan (bukan daftar referensi, bukan note sumber); nol jejak thinking-trace, nol "Answer N" sebagai sumber, nol frasa evasif E3, nol pelanggaran A_SCOPE; kalibrasi ketidakpastian kualitatif yang jujur — tidak ada persen efektivitas karangan.
- **Kelemahan (konsisten 3/3, satu spesies):** **fabrikasi penunjuk presisi** — pengenal yang tampak eksak digenerate dari plausibilitas ingatan, bukan retrieval: angka preseden (Hop 50%/10%), DOI (…2516651.2516734 vs benar …2504730.2504747), nomor paper (ePrint 2020/940 vs paper Meng), subjudul ("Original Sybil" vs "Soul"), domain (proofofhumanity.site vs .id; whitepaper.worldcoin tanpa TLD). Isi konseptualnya benar; **apparatus buktinya yang mengarang**. Ini persis spesies racun historis kita (klaim spesifik percaya-diri + sitasi plausibel yang tidak menopang) yang dulu membakar serve 14 Nov — sekarang muncul dalam bentuk lebih ringan (penunjuk, bukan tesis), tetapi di 3/3 sampel.

### Perbandingan lawan C5 shadow (clean 3/3)
- **Setuju** dengan C5 pada: struktur, reasoning, scope, uncertainty, ketiadaan pola fatal semantik, dan (dengan konteks kosong) novelty-vs-verified.
- **Tidak setuju** bahwa "clean" = aman dikirim tanpa pemeriksaan sitasi: C5 berjalan dengan `novelty_chars = 0` dan — terbukti dari hasil ini — tidak me-resolve URL/DOI/nomor paper ke sumber hidup. Ketiga cacat penentu di atas **tidak terlihat** oleh C5. Ini konsisten dengan kalibrasi C5 yang sudah diketahui (peniru pola semantik, bukan verifier sitasi): checklist D manual tetap satu-satunya jaring untuk spesies cacat ini, dan di sinilah ia menangkap 3/3.

---

## 5. Rekomendasi

**Serve TIDAK dibiarkan unattended; sebelum cap besok ditambah satu lapis verifikasi sitasi mekanis di pipa (resolve setiap URL + cek pinpoint DOI/nomor paper/judul lawan registry/sumbernya, tahan draf yang penunjuk porosnya mati atau salah dokumen) — karena penulis produksi terbukti kuat di isi tetapi mengarang penunjuk presisi di 3/3 jawaban, dan C5 shadow secara struktural tidak bisa melihat cacat itu.**

Catatan pendamping (usulan tertulis, bukan perubahan yang dilakukan pemeriksa):
1. Perbaikan spesifik per jawaban tidak mungkin (sudah terkirim) — pelajaran diteruskan ke generasi berikutnya: angka preseden bernama (skema persen, tanggal, ambang) wajib lolos buka-dan-baca sebelum kirim, atau ditulis ulang sebagai sintesis Tier-0 tanpa angka (sesuai (d)).
2. Verdict watch atas ketiga ISR ini dibaca dengan prior: bila ada falsified, bedah pertama diarahkan ke klaim Hop (jawaban 1) dan DOI Meiklejohn (jawaban 2) sebelum sebab lain.
3. Jawaban ke-4 (d21135d5) di luar set wajib, tetapi lahir dari pipa yang sama — perlakukan sebagai belum-ter-spot-check dengan risiko spesies yang sama.

---

*Pemeriksaan ini tidak mengubah kode/config/serve apa pun dan tidak menyentuh serve yang sedang jalan. URL yang dibuka sesi ini: Treasury jy0916, ePrint 2020/940, docs.hop.exchange, SSRN 4105763, proofofhumanity.id, MS CNG DPAPI, Springer Douceur, Fireblocks developers, RFC 5233, Coinbase CDP docs, Lit Protocol docs, attest.sh, BIP-32, ERC-4337, MS Research Douceur, W3C WebAuthn L2, BrightID, AWS KMS overview. Gagal di-fetch alat periksa (dicatat sebagai tidak terverifikasi, bukan dinyatakan mati): doi.org/10.1145/2516651.2516734 (HTTP 404), whitepaper.worldcoin, proofofhumanity.site, docs.passport.gitcoin.co, docs.web3auth.com.*
