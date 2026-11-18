# SPOT-CHECK MANUAL PILOT SERVE — 2 JAWABAN SISA (d21135d5 + 5e905bef)

**Tanggal periksa:** 2026-11-17 (sore, sesudah spot-check 3 pertama).
**Bahan:** teks persis terkirim dari `provider/serve-cache/` (`d21135d5-5d4e-4a54-9da1-c54b4fc466f8.txt`, `5e905bef-7e0a-4b31-839c-d59a6688c70d.txt`) + teks pertanyaan penuh via `trued.py question` (read-only).
**Metode:** identik dengan `SPOTCHECK-PILOT-2026-11-17.md` — checklist D (buka tiap URL; dukungan kalimat per angka terikat; premis kebaruan; penutup sintesis; nol jejak) + aturan vonis (d) yang sama: GAGAL bila (i) angka/klaim salah, atau (ii) ≥2 cacat penunjuk independen, atau (iii) menimpa sitasi poros; LOLOS-BERSYARAT bila satu penunjuk periferal salah dan semua klaim independen benar. Ditambah: kedua draf dijalankan lewat lapis sitasi (`citation_verify`, mode block, fetcher nyata) + lapis isi (`content_verify`, mode block, tahap-2 lane Nemotron sendiri) dan vonis mekanisnya dibaca berdampingan.
**Status verdict server saat diperiksa:** kedua ISO kita masih `revealed` (cek terakhir 21:08: 0 support / 0 refutasi). Semua ramalan di berkas ini dilabeli RAMALAN.

---

## Tabel vonis

| # | ISR | Kelas / panjang | Vonis manual | Vonis mekanis (sitasi / isi) | Butir penentu |
|---|-----|-----------------|--------------|------------------------------|---------------|
| 4 | d21135d5 (preview menyetujui call jahat — siapa menanggung rugi) | PIONEER / 8.088 kar (di atas pita 3.435–7.297 — catatan (c) saja) | **GAGAL (d)** — kelas paling ringan dari set pilot | findings / findings (tidak ada block) | Nomor pasal MiCA karangan (62, seharusnya 75) + label instrumen 93/13 salah di Sources |
| 5 | 5e905bef (preview berumur pendek — loop gagal eksekusi) | PIONEER / 8.215 kar (di atas pita — catatan (c) saja) | **LOLOS** | findings / clean (tidak ada block) | Tidak ada cacat penunjuk yang ditemukan manual; satu-satunya temuan mekanis = positif-palsu lapis |

**Jawaban atas pertanyaan pola:** pola karangan penunjuk presisi GLM **berlanjut di d21135d5** (spesies yang sama: pengenal presisi digenerate dari plausibilitas — kali ini nomor pasal), dan **putus di 5e905bef** (7/7 penunjuk benar dokumen + benar isi). Skor set pilot penuh: **4 dari 5 jawaban membawa ≥1 fabrikasi penunjuk presisi; 1 dari 5 bersih total.**

---

## 4. Jawaban d21135d5 — preview persetujuan call jahat: siapa menanggung kerugian — **GAGAL (d), kelas ringan**

Pertanyaan (259 kar): *"When an agentic wallet's off-chain risk preview approves a contract call that turns out to be malicious, who bears the loss, and what preview or signing records would the user need to dispute it?"*

### Yang lolos
- **(a)** Pembuka tesis langsung menjawab helai pertama: kerugian menetap di user dalam hampir semua kasus; pergeseran hanya di skenario sempit (kustodial berduties undang-undang, representasi "safe" afirmatif, agen melampaui delegasi) dan semuanya berputar pada kit bukti off-chain.
- **(b)/(h)** Cakupan PENUH: §1 alokasi bawaan (self-custody, posisi vendor preview/TOCTOU, lapis agensi), §2 empat skenario pergeseran, §3 enam record sengketa yang diminta pertanyaan (payload preview, artefak vonis preview, record penandatanganan, bukti timing/state, record delegasi, trace on-chain), §4 jalannya sengketa. Kedua helai pertanyaan terjawab eksplisit.
- **(e)** Penutup "New in this answer" = sintesis yang menamai kebaruan (hash-match linchpin: digest EIP-712 / hash signing EIP-155 payload bertanda vs payload preview sebagai artefak tunggal penentu arah sengketa) — bukan daftar referensi; tanpa frasa E3.
- **Isi substantif terverifikasi benar semua:** TOCTOU sebagai batas teknis preview; agensi mengikat prinsipal dalam cakupan delegasi; Reg E (12 CFR Part 1005, dibuka manual di eCFR — "Electronic Fund Transfers (Regulation E)", kerangka error-resolution §1005.11) tidak menjangkau transaksi kripto self-custody; permit ERC-2612 memang tanda tangan EIP-712 ber-deadline; peran Etherscan/revoke.cash generik benar. A_REASONING runtut; A_UNCERTAINTY terkalibrasi ("typically", "plausible", "becomes plausible"); A_SCOPE bersih.
- **Sitasi terverifikasi mendukung:** EIP-7702 (dibuka — Final, "Set Code for EOAs", delegasi kode ke EOA persis seperti diklaim); EIP-712 (Final, typed structured data); ERC-2612 (Final, permit extension); ethereum.org/docs/transactions (dibuka — raw signed transaction + signature hash); MiCA pada URL yang benar (Regulation (EU) 2023/1114 di EUR-Lex); Directive 93/13/EEC pada URL yang benar.

### Temuan penentu — (d) GAGAL: dua cacat apparatus independen (aturan (ii))
1. **Nomor pasal MiCA karangan (pinpoint salah, isi benar).** Jawaban menulis: *"EU MiCA Article 62 imposes safekeeping and segregation duties on crypto-asset service providers providing custody and administration on behalf of clients"*. Dibuka di EUR-Lex: pasal kustodi adalah **Article 75** — judulnya persis "Providing custody and administration of crypto-assets on behalf of clients", dengan para 3 (custody policy/safekeeping), para 7 (segregation), para 8 (liability ke klien) — persis duties yang dideskripsikan jawaban. **Article 62** adalah pasal aplikasi otorisasi CASP (yang dinilai Article 63) — tidak ada hubungan dengan kustodi. Spesies persis pola GLM: pengenal presisi (nomor pasal) digenerate dari plausibilitas, bukan retrieval; klaim hukumnya benar, penunjuknya karangan. Ini satu-satunya dasar skenario kustodial §2.
2. **Label instrumen 93/13 salah dua kali.** Badan menamai *"Unfair Contract Terms Directive"*; Sources menulis *"Regulation (EU) 93/13/EEC"*. Dokumen yang dibuka: **COUNCIL DIRECTIVE 93/13/EEC of 5 April 1993 on unfair terms in consumer contracts** (judul pendek EUR-Lex: "Unfair Terms Directive") — sebuah **Directive**, bukan Regulation, dan nama resminya bukan yang ditulis. URL-nya benar dan dokumennya benar; labelnya karangan — spesies yang sama dengan cacat subjudul DeSoc di jawaban 2 (yang di sana dihitung sebagai cacat penunjuk).

### Temuan tambahan
- **Sitasi Consensys longgar (cacat ketiga, paling lunak).** §1 + Sources mengutip `https://consensys.net/terms-of-use/` untuk klaim "describe MetaMask as a self-custody wallet and disclaim liability for transaction outcomes and third-party integrations". URL hidup (fetcher lapis: HTTP 200; hari ini ber-redirect ke situs korporat baru). Terms of Use Consensys yang berlaku (consensys.com/terms-of-use, dibuka) memang memuat disclaimer §9 + limitation of liability §10 + third-party at own risk §7 — tetapi deskripsi "MetaMask sebagai platform self-custodial" hidup di dokumen lain (MetaMask Terms of Use, metamask.io: "operates the MetaMask platform for self-custodial finance", Consensys Software Inc. dba MetaMask). Penunjuk: perusahaan benar, keluarga dokumen benar, dukungan tidak persis — dicatat sebagai ketidaktepatan dokumen pendukung, bukan karangan.
- **(c)** 8.088 kar di atas ujung pita Pioneer → catatan (c) saja (sama seperti jawaban 2).
- **RAMALAN panel:** isi 100% benar, cacat murni pinpoint/label → cenderung verified **±60–70%**; risiko falsified dari apparatus ceroboh tetap ada tetapi lebih rendah dari jawaban 1–2.

### Vonis mekanis berdampingan (d21135d5)
- **Lapis sitasi: `findings`, block=false** — 10 penunjuk, 8 verified; 2 temuan = kedua URL EUR-Lex ditandai "malformed — host tanpa TLD dikenal". **Keduanya positif-palsu lapis** (whitelist TLD lapis tidak mengenal `.eu`; URL EUR-Lex kanonis dan hidup). Lapis **melewatkan** cacat asli (nomor pasal 62) — di luar jangkauannya: ia memverifikasi URL/dokumen, bukan pinpoint pasal di dalam regulasi 10.305 baris.
- **Lapis isi: `findings`, block=false** — 1 klaim terekstrak (kalimat Reg E / 12 CFR 1005): tahap-2 vonis "unsupported" **karena fetcher kena CAPTCHA eCFR** (kutipan sumber = halaman access-denial) → turun sebagai temuan non-poros. Manual membuktikan klaimnya **benar** (eCFR dibuka langsung sesi ini). Vonis mekanis "unsupported" di sini artefak dinding-fetch, bukan cacat draf.
- **Kesesuaian:** mekanis dan manual sama-sama tidak mem-block; tetapi temuan mekanisnya derau (2 positif-palsu + 1 artefak fetch) sementara cacat asli yang ditemukan manual tidak terlihat oleh kedua lapis. Untuk jawaban ini, jaring manual tetap satu-satunya yang menangkap spesiesnya.

---

## 5. Jawaban 5e905bef — preview berumur pendek dan loop gagal eksekusi — **LOLOS**

Pertanyaan (328 kar): *"Why do short-lived transaction previews in agentic wallets cause repeated failed executions for users who respond slowly, and what design changes would remove that failure loop without weakening the guarantee that the user confirms the exact transaction they sign?"*

### Yang lolos — semua butir
- **(a)** Pembuka tesis = reframe yang persis menjawab: loop adalah ketidakcocokan latensi struktural (preview hanya benar selama state volatil tak berubah; latensi konfirmasi manusia menit-skala dan heavy-tailed) = livelock, bukan bug timer.
- **(b)/(h)** Cakupan PENUH: §1 kenapa preview pendek menghasilkan eksekusi gagal berulang (snapshot state volatil, TTL sebagai mekanisme kejujuran, latensi manusia vs validitas mesin, kerusakan sekunder nonce churn + approval fatigue), §2 kenapa jendelanya pendek (jaminan WYSIWYS), §3 tujuh perubahan desain (envelope yang bisa ditegakkan on-chain, ikat tanda tangan ke calldata persis, cek kesegaran di waktu eksekusi, order berdiri yang bisa dibatalkan, re-konfirmasi delta, pisahkan fee/nonce via abstraksi akun, perbaikan operasional), §4 kenapa jaminan transaksi-persis bertahan (dua lapis: digest kriptografis + batas semantik on-chain) — menjawab klausa kendala pertanyaan secara eksplisit, §5 tradeoff.
- **(c)** 8.215 kar — di atas ujung pita Pioneer 7.297 → **catatan (c) saja**; lantai jauh terlampaui.
- **(e)** Penutup sintesis menamai kebaruan (TTL sebagai mekanisme kejujuran preview titik-estimasi + penggantian validitas berbasis timer dengan jaminan dua lapis) — bukan daftar referensi; tanpa frasa E3.
- **Semua penunjuk terverifikasi hidup + dokumen benar + isi cocok (7/7):**
  - EIP-7683 (dibuka — ERC-7683 "Cross Chain Intents", Draft; intents diselesaikan solvers/fillers dalam kendala yang ditetapkan user) ✓
  - CoW Protocol docs `https://docs.cow.fi/` (dibuka — dokumentasi resmi CoW Protocol; order bertanda tangan dengan jendela validitas yang dieksekusi solver hanya dalam syarat bertanda) ✓
  - EIP-712 (dibuka — Final, typed structured data hashing and signing) ✓
  - EIP-2612 (dibuka — Final; fungsi permit memang membawa `deadline`, "current blocktime ≤ deadline") ✓
  - Uniswap Permit2 `https://github.com/Uniswap/permit2` (dibuka — repo resmi; README: "Expiring Approvals", allowances jumlah-persis/per-spender/berdurasi via AllowanceTransfer) ✓
  - ERC-4337 (dibuka — Final, "Account Abstraction Using Alt Mempool"; UserOperation, bundlers, paymasters, nonce 2D semi-abstracted) ✓
  - EIP-7702 (dibuka — Final, Set Code for EOAs) ✓
- **Angka presisi:** hampir tidak ada — dan satu-satunya angka, "p95", ditulis eksplisit sebagai **rekomendasi desain** ("at least a high percentile like p95, not an assumed few seconds"), bukan klaim fakta tentang sistem nyata. Tidak ada persen preseden, nomor paper, tanggal, atau ambang yang diklaim sebagai fakta. **Tidak ada bahan karangan untuk spesies GLM.**
- **A_REASONING / A_SCOPE / A_UNCERTAINTY:** rantai sebab runtut per seksi; nol laporan lingkungan Expert; klaim dinyatakan sebagai desain ("should", "let") dengan tradeoff diakui di §5 — kalibrasi pas. Nol jejak proses.
- **RAMALAN panel:** tertinggi dari kelima — cenderung verified **±65–75%**. Catatan upside: ISR ini sudah settled dengan 1 verified pesaing (af1a63ac, supported 2 / refuted 0) — slot Pioneer +20 (verified pertama) kemungkinan sudah direbut; verdict verified untuk ISO kita tetap mungkin, bayaran Pioneer-nya yang gugur bila pesaing settle lebih dulu.

### Vonis mekanis berdampingan (5e905bef)
- **Lapis sitasi: `findings`, block=false** — 7 penunjuk, 6 verified; 1 temuan = `docs.cow.fi` ditandai "malformed — host tanpa TLD dikenal". **Positif-palsu lapis** (`.fi` tidak ada di whitelist TLD lapis; domain hidup dan resmi — dibuka manual sesi ini). Manual: penunjuk itu benar penuh.
- **Lapis isi: `clean`** — 0 klaim terekstrak (draf ini nyaris tanpa token presisi terikat-sitasi; presisinya berupa nomor EIP yang tidak dipasangkan lapis sebagai klaim angka) → tidak ada yang diuji, konsisten dengan temuan manual bahwa tidak ada angka fakta yang bisa dikarang.
- **Kesesuaian:** vonis akhir sama (tidak ter-block, layak kirim); satu-satunya selisih = temuan mekanis cow.fi yang manual nyatakan keliru.

---

## 6. Lintas-jawaban — pola GLM di set pilot penuh (5/5)

| # | ISR | Vonis manual | Fabrikasi penunjuk presisi |
|---|-----|--------------|-----------------------------|
| 1 | 2777178d | GAGAL | Angka preseden Hop 50%/10% (karangan, nempel sumber asli) + domain `proofofhumanity.site` mati |
| 2 | d94d7e34 | GAGAL | DOI Meiklejohn mati/salah + subjudul DeSoc salah + URL Worldcoin tanpa TLD |
| 3 | 635a010d | LOLOS-BERSYARAT | Nomor ePrint 2020/940 menunjuk paper lain |
| 4 | d21135d5 | GAGAL (ringan) | Nomor pasal MiCA 62 (seharusnya 75) + label "Regulation (EU) 93/13/EEC" |
| 5 | 5e905bef | **LOLOS** | **Tidak ada** |

- **Pola berlanjut lalu putus.** Empat jawaban pertama (02:37–02:58Z) semuanya membawa ≥1 fabrikasi penunjuk presisi; jawaban kelima (03:02Z) bersih total. Satu sampel bersih tidak cukup untuk menyatakan pola berakhir — tetapi ia membuktikan GLM **bisa** menulis tanpa mengarang penunjuk, dan profilnya berbeda terukur: jawaban 5 topiknya desain sistem (sumber = standar EIP yang nomornya terkenal) sedangkan 1–4 menuntut preseden/pasal/DOI yang harus di-retrieval persis. Hipotesis kerja yang konsisten dengan kelima sampel: fabrikasi muncul saat jawaban menuntut pengenal presisi yang jarang/tidak kanonis (pasal regulasi, DOI, nomor ePrint, angka skema preseden), dan absen saat pengenalnya kanonis-terkenal (nomor EIP arus utama).
- **Kekuatan GLM konsisten 5/5** (menguatkan bacaan spot-check pertama): pembuka tesis/reframe tajam, struktur memetakan sub-pertanyaan 1:1, cakupan PENUH 5/5, penutup sintesis menamai kebaruan, nol jejak, nol pelanggaran scope, kalibrasi ketidakpastian jujur. Isi substantif: 5/5 benar pada semua klaim yang diperiksa manual sesi ini dan sesi sebelumnya.
- **Premis kebaruan:** kedua ISR viso 0 saat dipilih; log semantik mencatat `novelty_chars = 0` untuk keduanya (02:58:51Z / 03:02:05Z, clean) — status sama dengan tiga pertama: PLAUSIBLE, tidak terverifikasi lawan revealed pesaing (kerumunan saat kirim: 23 dan 46 revealed).

### Perbandingan manual vs mekanis (agregat 2 jawaban ini)
- **Block:** mekanis 0 block, manual 0 block-ekivalen pada level kirim (GAGAL (d) di sini adalah vonis mutu checklist, bukan cacat yang membuat draf tak terkirim — tiga pertama pun terkirim dengan vonis sama). Konsisten.
- **Yang hanya dilihat manual:** nomor pasal MiCA (di dalam dokumen yang benar), label jenis instrumen di Sources, ketidaktepatan dokumen pendukung Consensys.
- **Yang hanya dilihat mekanis — dan keliru:** 3 positif-palsu (EUR-Lex `.eu` ×2, CoW `.fi` ×1 — whitelist TLD lapis sitasi tidak mengenal keduanya) + 1 "unsupported" artefak CAPTCHA eCFR pada klaim yang benar. Rekomendasi turunan (usulan tertulis, bukan perubahan yang dilakukan pemeriksa): whitelist TLD lapis sitasi perlu `.eu` dan `.fi` (dan audit TLD ccTLD lain), dan vonis tahap-2 lapis isi atas sumber CAPTCHA/access-denial sebaiknya turun kelas ke "tak terverifikasi" bukan "unsupported".

### Catatan rezim (bukan cacat draf)
Log gerbang kesegaran (cek ulang pasca-pasang) mencatat kedua ISR ini **hari ini tertahan** oleh aturan kerumunan (23 dan 46 jawaban hidup ≥ garis 20) — di bawah pipa sekarang kedua target tidak akan dipilih pada keadaan kerumunan ini. Itu vonis tentang ruang kebaruan sekarang, bukan tentang mutu kedua draf.

---

*Pemeriksaan ini lab murni: tidak mengubah kode/config/serve apa pun, tidak menyalakan serve (tetap STOP), tidak mengirim apa pun. URL yang dibuka manual sesi ini: EUR-Lex Regulation 2023/1114 (termasuk Article 62 + Article 75 dibaca persis), EUR-Lex Directive 93/13/EEC, Consensys Terms of Use (consensys.com) + MetaMask Terms of Use (via hasil pencarian), eCFR 12 CFR Part 1005, EIP-712, ERC-2612, EIP-7683, EIP-7702, ERC-4337, ethereum.org/docs/transactions, docs.cow.fi, github.com/Uniswap/permit2. Hasil mekanis mentah: `/tmp/spotcheck-sisa-mechanical.json` + log `/tmp/spotcheck-sisa-citation-log.jsonl`, `/tmp/spotcheck-sisa-content-log.jsonl`.*

---

## 7. Perbaikan turunan (dilaksanakan 2026-11-17 malam — lab murni, serve tetap STOP)

Kedua rekomendasi turunan di §6 dilaksanakan malam yang sama. Keduanya koreksi klasifikasi atas positif-palsu yang terbukti di berkas ini — bukan perubahan ambang, garis, atau mode gerbang mana pun.

### 7.1 Lapis sitasi — pengenalan TLD (`provider/citation_verify.py`)
- **Masalah:** whitelist `KNOWN_TLDS` tidak mengenal `.eu` dan `.fi` → 2 URL EUR-Lex (d21135d5) + `docs.cow.fi` (5e905bef) ditandai "malformed — host tanpa TLD dikenal". Ketiganya positif-palsu (TLD sah, URL hidup, dokumen benar).
- **Perbaikan:** helper `_tld_recognized()` — label akhir dua-huruf dikenali lawan himpunan **ISO 3166-1 alpha-2** (`CCTLD_ALPHA2`, 252 kode: 249 assigned + eu/uk/su yang hidup di root zone); label lebih panjang tetap lawan whitelist gTLD `KNOWN_TLDS` (ditambah gTLD umum: tech, club, store, shop, space, life, fun, email, group, tools, agency, design, solutions, company). Dipakai oleh `_host_malformed()` dan cabang ekstraksi domain-telanjang.
- **Yang TIDAK longgar:** host tanpa TLD tetap malformed (`whitepaper.worldcoin` — kasus jawaban 2 — tetap tertahan); kode dua-huruf yang tidak terdaftar di ISO (`.xq`, `.zz`) tetap malformed; label karangan lain tetap malformed.
- **Bukti tes:** `test_citation_verify.py` 44/44 → **55/55** — 11 cek baru: `.eu`/`.fi` + ccTLD assigned lain dikenali; `.xq`/`.zz` ditolak; host EUR-Lex & cow.fi tidak malformed; end-to-end URL EUR-Lex `.eu` verified (clean) dan domain telanjang `docs.cow.fi` verified; URL `.xq` karangan tetap temuan malformed.

### 7.2 Lapis isi — halaman CAPTCHA/challenge (`provider/content_verify.py`)
- **Masalah:** klaim Reg E (d21135d5) divonis tahap-2 "unsupported" karena fetcher menerima **HTTP 200 berisi halaman CAPTCHA eCFR** — yang dinilai tahap 2 adalah halaman access-denial, bukan isi Regulation E; klaimnya sendiri terbukti benar saat eCFR dibuka manual.
- **Perbaikan:** detektor `_challenge_marker()` dipanggil di `_fetch_source_text()` sebelum teks diterima sebagai isi sumber. Halaman 200 yang badannya interstitial CAPTCHA/challenge/access-denied turun kelas ke **tak-terverifikasi** (kelas yang sama dengan bot-wall 403/status dinding lain): penanda kuat (artefak widget `h-captcha`/`g-recaptcha`/`cf-challenge`/`cf-turnstile`/`px-captcha`, frasa interstitial seperti "checking your browser before accessing", "verify you are not a robot", "complete the security check") menghukum di segala panjang halaman; penanda lemah ("captcha", "access denied", "just a moment", dll.) hanya pada halaman pendek (<3.000 karakter teks terekstrak) — artikel panjang yang sekadar membahas captcha tidak ikut turun kelas. Konsekuensi mekanis: klaim atas sumber challenge menjadi `unverifiable`, tahap 2 **tidak pernah berjalan** atasnya, dan vonis "unsupported" kini hanya bisa lahir bila teks sumber benar-benar terambil dan isinya tidak mendukung.
- **Bukti tes:** `test_content_verify.py` 41/41 → **46/46** — 5 cek baru: halaman CAPTCHA eCFR → klaim unverifiable + `stage2_calls == 0` + verdict "unverified" + tidak memblokir; interstitial Cloudflare "just a moment" → unverifiable; halaman access-denied pendek (HTTP 200) → unverifiable; penjaga arah sebaliknya: artikel panjang tentang captcha/bot-detection yang memuat angka klaim tetap `fetched` dan vonis akhir `supported`.

### 7.3 Regresi
Suite penuh provider sesudah perbaikan: semua berkas ALL PASS, identik dengan baseline pra-perbaikan kecuali dua modul sasaran yang bertambah (total cek bernomor 417 → **433**; sitasi 55/55, isi 46/46). Satu-satunya berkas tak-terjalan tetap `test_improve_20261116.py` §3 — tersandung cap serve NYATA 10/10 (keadaan operasional yang sama seperti sebelum perbaikan, bukan regresi). Backup: `citation_verify.py.bak-20261117-tldfix`, `content_verify.py.bak-20261117-challengefix` (+ backup kedua berkas tes dengan pola sama). Tidak ada ambang/garis/mode yang diubah; serve tidak dinyalakan; tidak ada submit.
