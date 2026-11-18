# BEDAH TOTAL DIALECTICA — 2026-11-10 (pasca-FALSIFIED pertama rezim)

Pemicu: perintah user 19:16 WIB ("bedah total itu dialectica, bikin lu yang paham bukan gw") sesudah user sendiri melihat saldo turun −1 $TRUED tanpa laporan dari kami.
Cakupan: anatomi verdict ISO fcb7b015, bedah isi lawan 6 jawaban verified di ISR yang sama + QUALITY.md v1, rekonsiliasi ledger akun penuh dari data server, peta mekanisme segar, usul keputusan operasional.
Metode: READ-ONLY total ke platform (tanpa klaim/serve/ask/ubah config). Semua angka dari API resmi lewat klien `trued.py` (`api_call`), dibaca 2026-11-10 ±19:2x–19:4x WIB. Kredensial tidak pernah dicetak.
Dokumen resmi yang dipakai: `skill-audit/pkg/dialectica/SKILL.md`, `references/api.md`, `references/rules-of-the-game.md`, `references/arenas.md`, objek arena live `GET /api/node/arenas/general` (version 3, termasuk `verificationRules`), wiki platform halaman `dialectica-reputation-and-verification-systems`.

---

## 1. ANATOMI VERDICT — ISO fcb7b015-115d-4dc9-a54b-440f82ae5aac

### 1.1 Garis waktu (semua dari API)

| Momen | Waktu | Bukti |
|---|---|---|
| Klaim dieksekusi (job edddc38b) | 19:0x WIB | §41 |
| ISO submit (timestamp ISO) | 2026-11-10T12:03:32Z = **19:03:32 WIB** | `timestamp` 1794312212114 |
| Commit tercatat | 12:04:46Z (commit ts 1794312286820) | field `commit` |
| **Verdict FALSIFIED** (`updatedAt` ISO) | 2026-11-10T12:07:55Z = **19:07:55 WIB** | `updatedAt` — **4 menit 23 detik sesudah submit** |
| Hunt 19:00 lapor ke user | ran_at 19:08:03 WIB, status dilaporkan "PENDING" | handoff jendela 19:00 — jujur pada saat ditulis; verdict mendarat ±bersamaan |

Penghitung akhir di ISO: `verifierCount` **4**, `supportedCount` **2**, `refutationCount` **2**, `marathonEligible` **false**.

### 1.2 Siapa mendukung/membantah, dan alasan refutasi — TIDAK terekspos

- Endpoint per-verifikasi **tidak ada**: `GET /api/node/iso/<id>`, `/api/node/vfps`, `/api/node/isos/<id>/vfps`, `/api/node/iso/<id>/verifications` semuanya **404 ENDPOINT_NOT_FOUND**. Baris ISO hanya membawa cacah agregat (vc/sc/rc), bukan identitas verifier, bukan urutan verdict, bukan teks feedback.
- Padahal teks feedback itu **ada** di server: `verdict_logic` arena mewajibkan verifier yang memberi non-compliant untuk menamai klaim spesifik yang gagal ("Feedback must name the specific claim or gap that caused failure"). Feedback itu tidak dapat kami baca dari API — **inilah batas penglihatan kita yang sesungguhnya**: kita tahu jawaban mati, kita tidak bisa membaca surat kematiannya.
- Falsified juga **tidak menghasilkan notifikasi inbox**: 50 notifikasi terakhir hanya berisi `subscribed_isr_marathon` (30), `ask_fee_charged` (6), `user_suspended` (3). `trued status` pasca-verdict: "No unread notifications." Satu-satunya permukaan tempat falsified terlihat = status ISO + `/api/node/scores`. **Ini penjelasan mekanis kenapa −1 tidak terlapor real-time**: jendela hunt melaporkan verdict sebagai PENDING (benar saat itu), verdict mendarat 4 menit kemudian, tidak ada alarm platform, dan penangkap berikutnya dalam rutinitas adalah jendela 21:00. User melihat saldo duluan dari sistemnya sendiri.

### 1.3 Aturan verdict — yang TERBUKTI

**Lapisan 1 — verdict per verifier (dokumenter, arena `verificationRules.verdict_logic`, version 3):**
Satu verifier menilai 4 cek — A_CITATION, A_REASONING, A_UNCERTAINTY, A_SCOPE — masing-masing dengan prosedur tertulis. `"compliant"` (support) hanya bila **keempatnya lolos**; `"non-compliant"` (refutasi) bila **salah satu saja gagal**. Jadi satu refutasi = minimal satu dari empat aturan arena gugur di mata verifier itu.

**Lapisan 2 — agregasi ke status ISO (empiris, n=32 jawaban ber-verdict di 2 ISR settled: 60fa9935 n=14 + 64bd68ac n=18):**

| Status akhir | (supported, refuted) yang teramati | n |
|---|---|---|
| verified | **(2, 0)** — satu-satunya pola | 15 |
| falsified | (0, 1) | 2 |
| falsified | (0, 2) | 12 |
| falsified | (1, 1) | 2 |
| falsified | (2, 2) — jawaban kita | 1 |

- **Verified ⟺ tepat 2 support DAN 0 refutasi. Tanpa satu pun pengecualian di 32 kasus.**
- **Falsified ⟺ refutationCount ≥ 1. Tanpa satu pun pengecualian**: setiap jawaban falsified memuat ≥1 refutasi; tidak ada jawaban verified yang memuat refutasi.
- **Kesimpulan aturan: verifikasi adalah lembar bersih (clean sheet), bukan voting.** Jawaban harus mengumpulkan 2 support tanpa satu pun refutasi. **Satu refutasi saja sudah menentukan** — framing "imbang 2 lawan 2" (yang tersirat di laporan §41/handoff) SALAH: dua support kita tidak pernah berada di jalur verified begitu refutasi pertama masuk. Ini konsisten dengan ringkasan esai resmi §10 di catatan kita sendiri ("verified = 2 mendukung; 1 membantah = falsified") — bedah ini menaikkan ringkasan itu dari kutipan menjadi hukum terukur (n=32).
- **Yang TIDAK terbukti/terekspos:** (i) urutan kedatangan verdict (tidak ada timestamp per-verifikasi) — di bawah aturan lembar-bersih urutan tidak relevan bagi hasil; (ii) kenapa panel kita berisi 4 verifier sementara mayoritas jawaban berpanel 2 (satu ISO pending lain di ISR yang sama juga vc=4; mekanisme eskalasi panel tidak terdokumentasi di paket skill maupun arena) — dugaan "panel membesar saat pasangan pertama split" masuk akal tapi **tidak terbukti**, dan tidak mengubah hasil: pada cacah akhir berapa pun, rc≥1 = mati; (iii) ambang untuk panel 4 (apakah (3,0) di panel 4 bisa verified) — tidak ada sampel; jangan diasumsikan.

**Konsekuensi desain yang mengubah kalkulus:** karena SATU klaim yang bisa dibantah = kematian, setiap klaim Tier-1 spesifik di jawaban adalah permukaan serangan. Musuh kita bukan "mayoritas verifier", melainkan **verifier paling teliti yang membuka sitasi kita**.

---

## 2. BEDAH ISI — jawaban kita vs 6 verified vs QUALITY.md

Pertanyaan (ISR 60fa9935): *"What are the trade-offs between using an EIP-1167 minimal proxy versus deploying a full standalone contract for a token launch, in terms of gas cost, upgradeability, and auditability?"* — ISR settled, viso 6, fiso 8 (kita fiso ke-8), 37 ISO, 64 VFP.

Jawaban kita: 5.286 karakter, 4 seksi bernomor, 4 tautan sitasi (EIP-1967, EIP-2028, EIP-4844, EIP-1167) + rujukan bernama OpenZeppelin Contracts v5.0.2.

### 2.1 Klaim yang bisa dibantah — diberi peringkat dari paling mematikan

**(P1) §2 — klaim dominasi bernama-rantai tanpa sitasi pendukung → pelanggaran A_CITATION (prosedur arena sendiri).**
Kutipan persis: *"On Arbitrum, Optimism and Base, deployment cost is dominated by **L1 data cost**, not the 200-gas-per-byte code deposit."* dan *"…the clone's advantage **GROWS on the deployment side** … while its lifetime tax nearly **VANISHES on the execution side** — the exact opposite balance from the L1 case the thread analysed."*
- Sitasi yang menempel di seksi ini: EIP-2028 (calldata 16 gas/byte non-nol) dan EIP-4844 (blob). **Kedua dokumen itu diam total soal komposisi biaya deployment di Arbitrum/Optimism/Base.** Prosedur verifikasi A_CITATION arena (langkah 1) berbunyi persis: *"a source that exists but does not state or support the claim = non-compliant."*
- Klaimnya sendiri Tier-1 (spesifik, bernama, bisa salah) — bukan Tier-0. Ini bukan sitasi karangan (penyakit E1 klasik); sitasinya nyata tapi **tidak mendukung klaim yang ditempelinya**. Persis celah yang dirumuskan eksperimen **E1** di QUALITY.md ("sitasi harus mengikat ANGKA/klaim-nya, bukan sekadar ada di dekatnya") — kini terbukti di jawaban kita sendiri.

**(P2) §2 — kuantifier absolut atas mekanisme spekulatif → pelanggaran A_UNCERTAINTY.**
*"GROWS"*, *"nearly VANISHES"*, *"the exact opposite balance"* — klaim prediktif/kontestabel dinyatakan sebagai fakta tuntas. Prosedur A_UNCERTAINTY arena: klaim SPECULATIVE/PREDICTIVE wajib memakai penanda ketidakpastian ("may", "possibly", …) di titik klaim. Hedge kita baru muncul di ujung paragraf ("exact per-chain figures vary…") — sesudah tiga klaim absolut. Verifier kedua bisa membunuh dari sini walau menerima P1.

**(P3) §3 — kontras CREATE2 yang menyesatkan → pelanggaran A_REASONING.**
Kutipan: *"…deterministic cross-chain addresses that standalone deployments cannot match without extra coordination."* Deployment standalone via CREATE2 (deployer + salt + initcode yang sama) mencapai determinisme lintas-rantai yang sama; pabrik clone pun hanya mencapainya bila **alamat pabriknya sendiri sama di semua rantai** — prasyarat koordinasi yang identik. Kontras "clone bisa, standalone tidak" adalah dikotomi palsu yang bisa dinamai verifier kata per kata (prosedur A_REASONING langkah 2: kesimpulan tidak mengikuti premis).

**(P4) §1 — pembingkaian kategori tesis → permukaan A_REASONING/A_CITATION sekunder.**
*"The minimal-proxy family contains a second member, the EIP-1967 beacon proxy"* + beacon *"reads it from a separate beacon contract at the ERC-1967 beacon slot on every call"*. BeaconProxy OpenZeppelin bukan proxy minimal 45-byte (runtime-nya kontrak proxy penuh yang memanggil `IBeacon.implementation()` per panggilan), dan EIP-1967 menstandardisasi **slot penyimpanan**, bukan keluarga proxy. Tesis beacon-nya sendiri sah dan baru; bingkai kategorinya longgar — cukup untuk ditandai verifier yang teliti, walau sendirian mungkin bukan pembunuh.

### 2.2 Yang BENAR di jawaban kita (jangan ikut dibuang)

- Angka hasil pengerasan steering §37 semuanya **benar dan terikat benar**: runtime EIP-1167 **45 byte**; code deposit **200 gas/byte**; calldata **16 gas per byte non-nol (EIP-2028)**. Tidak ada ikatan 700-gas-ke-EIP-2929. **E1 klasik ABSEN.**
- Jalur OpenZeppelin nyata: v5.0.2, `contracts/proxy/beacon/BeaconProxy.sol`, `UpgradeableBeacon.sol`, `IBeacon.sol` — semua ada.
- Kebaruan itu **nyata**: dari 6 verified, hanya Adam Reinhard menyebut beacon — satu klausa bawahan sebagai arsitektur terpisah. Sudut beacon-sebagai-opsi-ketiga + repricing L2 memang absen dari thread (sesuai §36/§41). Surprise gauge bukan pembunuhnya.
- Angka "~10% cold" diatribusikan ke thread (premise pertanyaan), bukan dinyatakan sebagai fakta dunia — sesuai pengecualian A_CITATION untuk teks pertanyaan.
- Penutup menamai kebaruan dengan penanda persis ("Baru dalam jawaban ini: …") ✓.

### 2.3 Kontras dengan yang LOLOS di ISR yang sama

| Jawaban | Kar | Tautan | Pola yang membuatnya hidup |
|---|---|---|---|
| 9dfd25b8 (T04435) verified | 5.521 | 7 | angka terikat sitasi bernomor, rentang diakui ("45–55 bytes") |
| a8421f55 (DodolDuren) verified | 24.041 | 69 | permukaan besar, tapi semua klaim terikat |
| c029c69d (Moden Gos) verified | 25.389 | 10 | long-form, sitasi per klaim |
| 06b978ae (nanik) verified | 5.349 | **0** | **nol sitasi tapi nol klaim Tier-1**: semua kuantitas berupa rentang ("low hundreds of thousands or less", "hundreds to a few thousand gas"), tidak ada klaim bernama-rantai — murni sintesis Tier-0 |
| 324a3042 (Adam Reinhard) verified | 7.765 | 13 | **setiap** angka terikat sitasi bernomor + hedge eksplisit di titik klaim ("That size is an illustration, not an ERC-20 benchmark", "not a complete deployment transaction", "Benchmark the actual bytecode … rather than treating the illustrative costs above as a November 2026 fee quote") |
| 6bdaad35 (Katou Megumi) verified | 11.145 | 6 | identitas kuantitatif diturunkan eksplisit (ΔG = 200(B−45)) — klaim berupa derivasi, bukan asersi |
| **fcb7b015 (KITA) FALSIFIED** | 5.286 | 4 | jalan tengah yang fatal: **spesifisitas Tier-1 + nama rantai, dengan dukungan bukti kelas Tier-0** |

Dua jalan terbukti lolos: (i) ikat SETIAP klaim spesifik ke sitasi yang benar-benar memuatnya (Reinhard), atau (ii) jangan buat klaim spesifik sama sekali (nanik). Kita mengambil jalan ketiga yang tidak ada di daftar lolos.

### 2.4 Skor ulang QUALITY.md v1 — mekanis (4A saat kirim) vs substantif (bedah ini)

| Butir | 4A §41 | Bedah substantif | Catatan |
|---|---|---|---|
| (a) pembuka tesis ≤3 kalimat | LOLOS | LOLOS | tesis tajam dan bisa salah |
| (b) struktur mencakup semua sub-pertanyaan | LOLOS | LOLOS | gas/upgradeability/auditability + aturan keputusan |
| (c) panjang | LOLOS (5.286) | LOLOS | pita baku |
| (d) sitasi | LOLOS (wrapper 0 temuan) | **GAGAL** | gerbang memeriksa KEHADIRAN sitasi + pola salah-atribusi yang dikenal; arena memeriksa DUKUNGAN sitasi ke klaim (buka-dan-baca). §2 gugur di uji kedua |
| (e) penutup menamai kebaruan | LOLOS | LOLOS mekanis | ironisnya kebaruan yang dinamai (repricing L2) adalah seksi yang tak didukung itu |
| (f) bukan parafrase | LOLOS | LOLOS | sudut benar-benar baru |
| (g) format skema | LOLOS | LOLOS | JSON klien patuh; job completed |

### 2.5 Vonis akar penyebab (bisa diuji)

> **Jawaban ini mati bukan karena angka yang salah — semua angka kerasnya benar — melainkan karena dua klaim penopang §2 adalah klaim Tier-1 bernama-rantai yang sitasinya (EIP-2028/EIP-4844) tidak memuat dan tidak mendukung isi klaimnya, sehingga satu verifier yang menjalankan prosedur A_CITATION arena apa adanya sudah cukup menjatuhkan refutasi, dan di bawah aturan lembar-bersih satu refutasi adalah penentu tunggal.**
> Uji ke depan: terapkan uji buka-dan-baca (self-VFP, usul 4) ke semua draf; bila pola "sitasi ada tapi tak mendukung" masih muncul di ≥1 klaim penopang sesudah gerbang itu dipasang, vonis ini salah dan akarnya ada di hulu (steering), bukan di gerbang.

Catatan pembatas: karena teks refutasi tidak terekspos API (§1.2), atribusi ke P1 (dan sekunder P2/P3) adalah inferensi terkuat dari perbandingan isi + prosedur arena — bukan kutipan surat verifier. P1 adalah satu-satunya titik di mana jawaban kita melanggar prosedur tertulis arena secara objektif dan dapat ditunjuk barisnya.

---

## 3. REKONSILIASI LEDGER AKUN PENUH (data server, dibaca ulang malam ini)

### 3.1 Saldo — setiap gerakan seumur akun

| # | Peristiwa | Δ | Saldo | Bukti |
|---|---|---|---|---|
| 1 | 7 pertanyaan unik dibuat (kredit asker +1 per pertanyaan) | **+7,0000** | 7,0000 | aturan ask (api.md); 7 ISR kita settled (§24) |
| 2 | Fee ask n=2..7 (n=1 gratis): 0,0045 + 0,0363 + 0,1214 + 0,2831 + 0,5383 + 0,8952 | **−1,8788** | **5,1212** | 6 notifikasi `ask_fee_charged` 2026-11-09 (jumlah persis 1,8788) |
| 3 | Falsified fcb7b015 (2026-11-10 19:07:55 WIB) | **−1,0000** | **4,1212** | `scores.coins` = 4,1212 malam ini ✓ |

Tidak ada gerakan lain seumur akun: tidak ada Pioneer/Innovator/Marathon yang pernah terkredit (lifetimeEarned tidak pernah di atas 7), tidak ada penarikan, jalur ask ditutup di n=7 (n=8 tidak pernah disentuh).

### 3.2 Angka lawan angka (lama → sekarang)

| Ukuran | §41 pra-klaim (19:0x) | Pasca-klaim completed (19:0x) | **Malam ini (pasca-verdict)** | Δ total |
|---|---|---|---|---|
| coins | 5,1212 | 5,1212 | **4,1212** | −1,0000 |
| lifetimeEarned | 7 | 7 | **6** | **−1 (falsified memotong lifetimeEarned juga — baru teramati)** |
| Expertise general | 7 | 7 | **6** | −1 |
| RAR | 4 | 5 | **7** | +3 |
| — reliability (REL) | −3 | −3 | **−3** | 0 |
| — availability | 0 | **1** | 1 | +1 (job completed) |
| — reputation | 7 | 7 | **9** | **+2** |
| Usage ISR (jendela 24 jam bergulir) | 0 | 1 | 1 | jendela API: 2026-11-09T12:21:17Z → 2026-11-10T12:21:17Z |
| suspensionCount | 3 | 3 | 3 | terakhir berakhir 2026-11-08T12:44:50Z |

### 3.3 Kenapa RAR NAIK (4 → 7) sementara saldo & expertise TURUN

RAR adalah jumlah tiga ledger yang **berbeda urusan** (REL + availability + reputation = −3 + 1 + 9 = 7):
- **Reliability (−3, beku)** menghukum disiplin penyelesaian JOB (era abandoned 8 Nov), **bukan** kebenaran jawaban. Falsified tidak menyentuhnya — terbukti: REL identik sebelum dan sesudah verdict.
- **Availability (0 → 1)** naik karena job klaim pertama **completed** (siklus tuntas) — dicatat §41.
- **Reputation (7 → 9, +2)** naik bertepatan **persis** dengan 2 verdict "compliant" (support) yang diterima jawaban kita. Mekanisme resmi kenaikan reputation tidak terdokumentasi di paket skill/wiki; korelasinya 1:1 dengan supportedCount kita (hipotesis terkuat: +1 per verdict mendukung; **ditandai sebagai hipotesis, bukan bukti**).
- Hukuman falsified berjalan di rel lain: **coins −1, expertise −1, lifetimeEarned −1** (pola wiki: "Falsified answers result in a penalty of −1 $TRUED and a loss of Expertise" — bedah ini menambah: lifetimeEarned ikut terpangkas).
Kesimpulan: tidak ada kontradiksi — akun dihukum di dompet dan keahlian, dihadiahi di reputasi/ketersediaan karena job-nya tuntas dan dua verifier menyatakan jawabannya compliant.

### 3.4 Riwayat suspensi (REL-005, 2026-11-08) — dari notifikasi

| # | Tercatat (UTC) | Berakhir (UTC) | Durasi | Alasan persis |
|---|---|---|---|---|
| 1 | 12:30:02 | 12:30:05 | 3 detik | "Slash from rule REL-005 (suspension #1)" |
| 2 | 12:38:54 | 12:38:55 | 1 detik | "Slash from rule REL-005 (suspension #2)" |
| 3 | 12:44:47 | 12:44:50 | 3 detik | "Slash from rule REL-005 (suspension #3)" |

Suspensi berupa slash sesaat (detik), bukan kurungan panjang; warisan permanennya adalah REL −3. Tidak ada suspensi sesudah 8 Nov.

### 3.5 Cacah jawaban kita seumur akun

| Status | Jumlah | Keterangan |
|---|---|---|
| verified | **0** | belum pernah |
| falsified | **1** | fcb7b015 (rezim ini, klaim pertama) |
| abandoned | **6** | era serve 8 Nov (§23/§24; permukaan ISO) |
| intent/revealed menggantung | 0 | — |
| **Total ISO** | **7** | permukaan jobs berbeda: 4 job tercatat (3 failed 8 Nov + 1 completed) — jobs menghitung penugasan, ISO menghitung jawaban; keduanya benar di permukaannya |

Rezim caps-20→none: klaim disiplin **1**, verdict **1**, verified **0** → **verdict rate berjalan 0/1 (0%)**.

---

## 4. PETA MEKANISME SEGAR (terverifikasi API/dokumen malam ini; ⚠️ = berubah dari §41 ke bawah)

| Mekanisme | Aturan terbukti | Sumber |
|---|---|---|
| Verdict per verifier | compliant ⟺ 4/4 cek lolos (A_CITATION, A_REASONING, A_UNCERTAINTY, A_SCOPE); 1 gagal = non-compliant + wajib menamai klaim | arena version 3, `verificationRules` |
| Agregasi verdict | **verified ⟺ supported=2 ∧ refuted=0; refuted≥1 = falsified** (n=32, nol pengecualian) | hitungan API 2 ISR settled ⚠️ mengoreksi framing "2 vs 2" §41 |
| Penalti falsified | −1 coins, −1 expertise arena, −1 lifetimeEarned; REL/RAR tidak bergerak | scores malam ini + wiki ⚠️ lifetimeEarned ikut turun (baru) |
| Hadiah menjawab | Pioneer +20 / Innovator +10 / Marathon Winner +10 saat settle; verified non-novel = 0 | wiki + §25 (tidak berubah) |
| REL-005 | menghukum job diambil-tak-tuntas (abandoned) → slash + suspensi sesaat berjenjang; kebenaran jawaban di luar REL | notifikasi suspensi + scores |
| Availability/Reputation | job completed +1 availability (teramati); support verdict berkorelasi +1 reputation per support (hipotesis) | scores lintas §41→malam ini |
| Caps pasca-flip | maxIsrs24h **null/unlimited** [used 1]; maxUsd24h/maxTokens24h null; maxConcurrency **1**; warningThresholdPct 80; isActive true | `GET /api/spending/limits` + `agent show` malam ini ⚠️ flip 20→none (19:15–19:16, persetujuan user) |
| Jendela usage | bergulir 24 jam (windowStart/End eksplisit dari API); usage malam ini isrs 1, tokens 0, usd 0 | `GET /api/spending/usage/agent/<id>` |
| Notifikasi | falsified jawaban sendiri **tidak** memicu notifikasi; yang tercatat hanya milestone tertentu (marathon langganan, fee, suspensi) | 50 notifikasi terakhir ⚠️ celah pelaporan baru dipetakan |
| Kill-metric kita (keadaan) | (i) klaim tanpa settle 0/10 (klaim ini settle — sebagai falsified); (ii) **TERPICU: 1 falsified sejak klaim terakhir → JEDA**; (iii) RAR 7 ≫ −5 aman; (iv) abandoned baru 0 | hitungan bedah ini |
| Strategi/config lain | strategyType dynamic, arenas general, enabled true — tidak berubah | `agent show` |

---

## 5. KEPUTUSAN OPERASIONAL YANG DITUNTUT DATA (usul untuk sesi utama — TIDAK dieksekusi di bedah ini)

1. **Jendela 21:00 = JEDA klaim penuh (kill-metric ii).** Isi jendela: scan + pantau + drill bedah saja; bedah akarnya adalah dokumen ini. Antrean §41 (472b29a0 → 71f472d6 → c44f4399 → …) tetap staged, **tidak ditembak**. Pencabutan jeda = keputusan sesi utama sesudah membaca bedah ini, bukan otomatis di jendela berikutnya.
2. **Posisi RAMP dinyatakan apa adanya:** verdict rate **0/1 (0%)** lawan ambang pemenang **≥55%** (R8). n=1 belum vonis statistik, tetapi arahnya negatif dan klaim berikutnya tidak boleh dipakai "mengejar rate" — volume naik di atas isi yang belum diperbaiki = mengulang falsified dengan biaya −1 per kejadian.
3. **Pasang GERBANG VERIFIKASI-DIRI (self-VFP) mendahului wrapper** di jalur klaim semua lane: draf dinilai dengan checklist `verificationRules` arena persis seperti verifier menilai — buka setiap tautan sitasi, klasifikasikan setiap klaim Tier-0/Tier-1, dan untuk tiap klaim Tier-1 tunjuk kalimat pendukung di sumbernya. Satu klaim penopang gagal uji dukung = tulis ulang sebagai sintesis Tier-0 atau buang, sebelum wrapper berjalan. Wrapper mekanis terbukti tidak bisa menangkap kelas kegagalan ini (§41 butir 9 + kasus ini).
4. **Perkerasan steering baru (spesifik, dari baris yang mati):** (a) klaim komposisi/dominasi bernama-rantai atau bernama-protokol ("di Arbitrum/Optimism/Base biaya didominasi X") DILARANG tanpa sitasi dokumen rantai/protokol itu sendiri yang memuat klaimnya; kata kerja dominasi komparatif (dominates/grows/vanishes) diperlakukan sebagai klaim Tier-1; (b) kontras eksklusivitas ("X tidak bisa dicapai Y") wajib lolos cek counterexample tertulis di steering (kasus CREATE2); (c) kuantifier absolut atas mekanisme spekulatif wajib hedge di titik klaim, bukan di ujung paragraf.
5. **QUALITY.md / lab mingguan 2026-11-16:** daftarkan fcb7b015 sebagai **kasus adopsi E1 ke-1** (ambang adopsi E1 = 2 kasus falsified berakar "angka/klaim tanpa sitasi pendukung langsung" — satu lagi kasus serupa dan sub-cek (d) "sitasi harus mendukung klaim spesifiknya (uji buka-dan-baca)" wajib naik versi). Catat di ANTRIAN EKSPERIMEN, jangan menunggu lab untuk mulai menerapkan self-VFP (usul 3) sebagai praktik jendela.
6. **Koreksi model mental di semua dokumen hidup:** verdict = **lembar bersih (2 support, 0 refutasi)**; hapus framing skor imbang dari cara kita membaca supported/refutation. Konsekuensi seleksi target & template: minimalkan jumlah klaim Tier-1 per jawaban; yang tersisa harus terikat sitasi pendukung langsung. Jumlah klaim spesifik — bukan panjang — adalah permukaan serangan kita.
7. **Restatement badan cron hunt (ranah sesi utama, di luar bedah ini):** CONFIG LIVE "caps maxIsrs24h=20" → **none/unlimited**; butir 1 "…tunduk pada sisa anggaran harian + sisa caps (usage < 20)" → tunduk pada **tangga internal + kill-metric** (caps server tidak lagi mengikat; usage tetap dibaca sebagai meter, bukan gerbang); judul cron "…caps 20" diperbarui. Tanpa restatement ini, jendela 21:00 akan membaca config yang sudah tidak ada.
8. **Tutup celah pelaporan verdict:** verdict mendarat ±5 menit sesudah klaim (kasus ini 4 mnt 23 dtk) dan **tidak ada notifikasi platform** untuk falsified. Jadikan baris tetap di badan hunt butir 0: "status verdict klaim terakhir (ISO + scores) dibaca dan dilaporkan SEBELUM scan baru" — dan untuk klaim yang verdict-nya belum mendarat saat jendela pelapor tutup, jendela berikutnya wajib membuka laporannya dengan verdict itu (bukan menunggu user melihat saldo).
9. **Tidak ada perubahan config Expert dari bedah ini.** Flip caps sudah terverifikasi server (unlimited [used 1]); concurrency tetap 1 — dengan caps tak terbatas, rem yang tersisa persis tangga internal + kill-metric, dan kill-metric (ii) sedang aktif. Menaikkan concurrency sekarang tidak ditopang data apa pun.
10. **Syarat klaim pertama sesudah jeda dicabut** (bila sesi utama mencabutnya): target Kelas 1 dengan permukaan refutasi terkecil yang tersedia hari itu + steering lolos usul 4 + draf lolos self-VFP (usul 3) dengan catatan per klaim; klaim itu diperlakukan sebagai uji gerbang perbaikan, bukan kelanjutan volume.

---

## Bukti & rujukan file

- Data mentah bedah ini: `/tmp/bedah/` (isos.json, isr.json, arena_general.json, scores.json, notifications50.json, answer_mine.txt, answer_ver_*.txt) — salinan jawaban kita juga terekam di reveal ISO fcb7b015 via `GET /api/node/isos/60fa9935-4352-4a4c-9aa7-384de037196c`.
- Catatan jendela asal: MEKANISME-DAN-LAPANGAN.md §41 (klaim) — bedah ini adalah tindak lanjutnya dan diringkas sebagai **§42** di file yang sama.
- Rubrik: QUALITY.md v1 (butir (d) + eksperimen E1).
