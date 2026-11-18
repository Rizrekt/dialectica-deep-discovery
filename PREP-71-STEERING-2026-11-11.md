# PREP §7.1 BUTIR 1 — STEERING BERMANTAT-URL — 2026-11-11

**Lingkup:** PERSIAPAN SAJA atas keputusan user LANJUT BERSYARAT (2026-11-11 12:50). **Nol klaim, nol serve, nol submit, nol perubahan cron, nol perubahan MEMORY.md dalam pekerjaan ini.** Klaim tetap STOP sampai sesi utama memverifikasi §7.1 lengkap (butir 2–6 di luar laporan ini).
**Pola yang diikuti:** EVALUASI §7.1 butir 1 + §2 (deadlock lantai) + MEKANISME §50.7 (revisi 2c7efc3e), §52 (novelty 2c7efc3e gugur), §53 (revisi 1d3efb52: jaminan URL + potongan per-seksi).
**Metode verifikasi URL:** `curl -L` lewat proxy egress VM, User-Agent browser, 2026-11-11 ±12:5x WIB. Hanya URL berstatus **200** yang dimandatkan. Steering klaim lama (472b29a0, 60fa9935, 71f472d6) TIDAK disentuh.

---

## Ringkasan status

| Target | Berkas steering | Status §7.1(1) |
|---|---|---|
| 1d3efb52 | direvisi (6 seksi + anggaran + jaminan URL) | **SIAP** (sisi steering) |
| 2c7efc3e | direvisi (sudut kandidat baru + 4 URL) | **BELUM SIAP PENUH** — novelty kandidat belum terbukti (lihat §2) |
| 1d758352 | BARU ditulis | **SIAP-BERSYARAT** — novelty dicek hanya lawan pasangan terbedah |
| fdf32ba4 | direvisi (mandat URL ditambahkan) | **SIAP** (sisi steering) |
| 5fbb2531 | tidak ada | **TIDAK BISA DISIAPKAN** — data soal tidak ada |
| 26fe6c71 | tidak ada | **TIDAK BISA DISIAPKAN** — data soal tidak ada |
| 530bed9e | tidak ada | **TIDAK BISA DISIAPKAN** — data soal tidak ada |

"Sisi steering" = berkas memenuhi pola §7.1(1). Kepatuhan model saat generasi tetap varians (pelajaran §53: mandat-URL pernah menghasilkan 0 URL) — jaminan sisi-generasi adalah utang §7.1 butir 6, bukan berkas ini.

---

## 1. 1d3efb52-8a6d-41ee-a55e-2a0115bd365c — bonding curve — SIAP

**Perubahan dari versi 11:00:** struktur 8 → **6 seksi** dengan plafon karakter per seksi (menutup overshoot drill 11:26: 9.307 kar); mandat URL diperkeras jadi **jaminan penempatan**: URL verbatim polos ≥2× per URL (total ≥8), di kalimat yang sama dengan klaimnya, + baris cadangan "Sources cited:" berisi keempat URL verbatim sebelum penutup. Sensus digit dipertahankan (daftar ANGKA YANG BOLEH DIPAKAI; larangan 700 gas/EIP-2929/EIP-1167).

**URL dimandatkan + status HTTP (cek 2026-11-11):**

| URL | Status |
|---|---|
| https://docs.moonshot.cc/developers/bonding-curve-solana | **200** |
| https://docs.flaunch.gg/ | **200** |
| https://docs.pump.fun/ | **200** |
| https://docs.meteora.ag/core-products/dbc/migration-and-liquidity | **200** |

⚠️ **Penggantian tercatat:** URL lama `https://pump.fun/docs/bonding-curve` mengembalikan **403** ke pengambilan otomatis (dinding bot) — TIDAK lolos syarat "diverifikasi HTTP 200 saat ditulis", jadi diganti beranda docs resmi `https://docs.pump.fun/` (200). Isi klaim Pump.fun di steering tidak berubah; penyebutan di berkas mencatat alasan penggantian ini.

**Pita panjang:** 6.300–7.300 kar (selaras LENGTH_SUFFIX 5.500–7.500; pita marathon 10–12 rb sengaja TIDAK dipakai — tabrakan dicatat di berkas, sesuai §7.1 butir 5). Anggaran seksi: ≤1.100 / ≤950 / ≤1.250 / ≤1.000 / ≤1.050 / ≤600 + pembuka ≤350.

**Novelty:** tidak berubah dari drill 11:26 — sudut spektrum bentuk kurva + put-formula terverifikasi manual LOLOS lawan 8/8 verified (DRILL-LOG 11:26, (f) manual LOLOS bersyarat, risiko §4 termitigasi framing).

**Sisa kekurangan:** tidak ada di sisi steering. Risiko generasi (URL=0) tetap ada → butuh jaminan sisi-generasi (butir 6) atau probe kelas-klaim sebelum tembak.

---

## 2. 2c7efc3e-f25a-440c-aedd-61a2bbb7dac8 — VC vs SBT — BELUM SIAP PENUH (novelty)

**Yang sudah selesai:** mandat URL lengkap + jaminan penempatan (≥8 penempatan, baris "Sources cited:"), sensus digit diperbarui, anggaran per seksi ditambahkan, struktur ditulis ulang di sekitar sudut baru.

**URL dimandatkan + status HTTP:**

| URL | Status |
|---|---|
| https://www.w3.org/TR/vc-data-model/ | **200** |
| https://www.w3.org/TR/did-core/ | **200** (baru) |
| https://www.w3.org/TR/vc-bitstring-status-list/ | **200** (baru) |
| https://eips.ethereum.org/EIPS/eip-5192 | **200** |

**Pita panjang:** 10.000–12.000 kar (marathon viso 8); tabrakan LENGTH_SUFFIX dicatat eksplisit di berkas per §7.1 butir 5. Anggaran: pembuka ≤400; seksi ≤2.000 / ≤2.800 / ≤2.400 / ≤2.200; penutup ≤300.

**Sudut novelty — temuan pekerjaan ini:**
- Tiga sudut revisi 07:00 terkonfirmasi MATI dari data lokal: kompromi-kunci = 9b0497ad §3.3; kejujuran Sybil = 9ec75755 §3; hibrida = a4705223/9ec75755. Pemenang terbaru juga sudah mengambil: arus reputasi dinamis (1d7fc985), FATF + solvabilitas (bbb2c4d4), atomisitas settlement (d573782c). Steering baru MELARANG mengklaim keenamnya sebagai kebaruan.
- **Sudut kandidat baru yang ditulis ke steering:** *lapisan kepercayaan verifier + liveness pemeriksaan status* — (i) daftar penerbit yang diterima verifier sebagai objek tata-kelola (kurasi, propagasi pencabutan penerbit, reputasi tidak portabel antar kebijakan kepercayaan walau format portabel); (ii) pemeriksaan status credential sebagai dependensi liveness (daftar status di-host penerbit; kebijakan fail-open / fail-closed / cache harus dipilih sebelum pembayaran pertama). Jangkar sitasi barunya nyata: DID Core + Bitstring Status List (keduanya 200).
- **KENAPA BELUM BISA DINYATAKAN TERBUKTI:** inventaris sudut di atas mencakup 6 dari 8 verified. Dua verified — **51a6c56b** dan **4ea50749** — tercatat pernah "dibaca penuh" (jendela 07:00, MEKANISME §50 butir 6) tetapi **tidak ada catatan isi keduanya yang bertahan di satu pun berkas lokal** (dicari di seluruh research/dialectica + drills/: hanya daftar ID). Ketiadaan sudut kandidat di kedua jawaban itu **tidak bisa dibuktikan dari data lokal**. Mengarang kepastian di sini = mengulang kesalahan premis gugur §52.
- **Konsekuensi (tertulis juga di CATATAN OPERATOR berkas steering):** 2c7efc3e **JANGAN ditembak** sebelum novelty diverifikasi ulang dengan membaca penuh 51a6c56b + 4ea50749 di ISR live. Bila salah satu menempati sudut kandidat → **target uji pertama harus diganti**; kandidat pengganti terkuat = **1d3efb52** (novelty terverifikasi 8/8, steering kini SIAP).

**Sisa kekurangan:** (1) verifikasi novelty 2 verified (di atas) — pekerjaan sesi utama/jendela hunt berikutnya, butuh akses ISR live; (2) sisanya sama dengan target lain (jaminan sisi-generasi = butir 6).

---

## 3. 1d758352-7ed6-415d-9446-6c382d7e1fc6 — BSC block producer vs NFT mint — BARU, SIAP-BERSYARAT

**Soal persis tersedia** (MEKANISME §awal): *"How can the producer of a BNB Smart Chain block bias the outcome of an NFT mint whose trait randomness is derived from blockhash or block.timestamp, when those values appear unpredictable before the block is published?"* — jadi steering bisa ditulis dari soal nyata, bukan karangan.

**Isi steering:** tesis ekonomi-bias (grinding dibatasi laju segel; bias terkuat = seleksi pembuangan blok dengan harga terukur; tangga mitigasi + sisa keuntungan produser per anak tangga); daftar FAKTA KANONIS (vanity 32 byte + segel 65 byte per EIP-225; laju signing 10⁴–10⁵/dtk/core sebagai rentang; blockhash 256 blok; era sub-detik/40+ validator dari bedah klaim #2); **larangan angka keras** menyalin persis kesalahan falsified 66f46c3e (28 byte, 1 μs, 21 validator/3 dtk, fee chart, ~63%).

**URL dimandatkan + status HTTP:**

| URL | Status |
|---|---|
| https://eips.ethereum.org/EIPS/eip-225 | **200** |
| https://docs.soliditylang.org/en/latest/units-and-global-variables.html | **200** |
| https://docs.chain.link/vrf | **200** |

Jaminan penempatan: ≥6 penempatan + baris "Sources cited:".

**Pita panjang:** 10.000–12.000 kar; anggaran: pembuka ≤350; seksi ≤1.800 / ≤2.000 / ≤1.800 / ≤2.200 / ≤1.600; penutup ≤250. Tabrakan LENGTH_SUFFIX dicatat eksplisit di berkas.

**Sisa kekurangan (syarat):** novelty sudut ekonomi-bias terverifikasi hanya lawan pasangan terbedah penuh (0006fe08 verified + 66f46c3e falsified, DRILL-LOG 07:00). Lima verified lain di ISR ini (total 7) tidak punya bedah isi lokal → sebelum ditembak, grep kata kunci sudutnya lawan SEMUA verified di ISR live (pelajaran §52). Karena itu status **SIAP-BERSYARAT**, bukan SIAP.

---

## 4. fdf32ba4-c22e-40ed-aa97-ffe2bdbc80c1 — skill baw — SIAP

**Perubahan:** versi staged lama memuat larangan mengarang URL TANPA daftar yang diizinkan (pola deadlock persis) — revisi menambahkan mandat URL + jaminan penempatan (≥2× per URL + baris "Sources cited:") + anggaran per seksi + sensus digit eksplisit (v1.12.0; chain 56/1/8453; ±5 menit; ±30 hari). Tulang punggung operasional (ketiadaan material kunci; pengecualian sign-message; preview dua fase; Developer Mode; BINANCE_BAW_DIR) dipertahankan utuh.

**URL dimandatkan + status HTTP:**

| URL | Status |
|---|---|
| https://github.com/binance/binance-skills-hub | **200** |
| https://registry.npmjs.org/@binance%2fagentic-wallet | **200** |

⚠️ Halaman web `https://www.npmjs.com/package/@binance/agentic-wallet` mengembalikan **403** — TIDAK dimandatkan; diganti catatan registry npm resmi (200) + repo hub (200). Kedua URL hanya menopang klaim distribusi/identitas paket (aturan penempatan mengikatnya ke seksi itu); klaim operasional tetap dinyatakan sebagai praktik terverifikasi, tidak dihias sitasi — dicatat di berkas agar penempatan tidak mengambang (risiko (d)).

**Pita panjang:** 10.000–12.000 kar (viso live 8 per §53; pita baku 4.500–8.000 versi lama dicabut dengan alasan tertulis). Anggaran: pembuka ≤350; seksi ≤1.500 / ≤3.000 / ≤3.200 / ≤2.000; penutup ≤300. Tabrakan LENGTH_SUFFIX dicatat eksplisit.

**Sisa kekurangan:** novelty (ketiadaan material kunci) bersumber dari audit operasional kita, bukan perbandingan isi 8 verified ISR ini — cek grep cepat (private key / session / custodial) lawan verified set disarankan sebelum tembak; tertulis di berkas.

---

## 5. Target yang TIDAK BISA DISIAPKAN — 5fbb2531, 26fe6c71, 530bed9e

**Status: TIDAK BISA DISIAPKAN dalam pekerjaan ini. Tidak ada berkas steering yang dibuat untuk ketiganya.**

Alasan (satu pola untuk ketiganya): data lokal hanya memuat **label topik + cacah**, bukan soal:
- **5fbb2531** — label "Uniswap fee" (viso 6→7, fiso 20→21, 59 isos). UUID penuh: **tidak tercatat** di berkas mana pun.
- **26fe6c71** — label "ERC-4337" (viso 6→7). UUID penuh: **tidak tercatat** (STEERING-AUDIT-T10: "belum pernah di-steering").
- **530bed9e** — label "ERC-4626/L2" (viso 8). UUID penuh: **tidak tercatat** (idem).

Dicari di: MEKANISME-DAN-LAPANGAN.md §28–§53, STEERING-AUDIT-T10, STEERING-FIX-T10, DRILL-LOG, drills/, provider/ (termasuk lib/), dan grep UUID-penuh di seluruh ~/workspace — nihil untuk soal persis, UUID penuh, maupun isi verified set ketiganya.

Menulis steering dari label topik saja = mengarang ruang lingkup soal — persis spesies gagal C (scope miss) yang membunuh klaim #3. **Yang dibutuhkan sebelum ketiganya bisa disiapkan:** satu tarikan detail ISR live per target (soal persis + daftar/isi verified set) pada jendela hunt berikutnya — pekerjaan baca-saja, di luar lingkup berkas ini. Sesudah data itu ada, pola steering-nya mengikuti §1/§3 laporan ini.

---

## 6. Peta §7.1 sesudah pekerjaan ini

- **Butir 1 (steering bermandat-URL):** 1d3efb52 **SIAP** · fdf32ba4 **SIAP** · 1d758352 **SIAP-BERSYARAT** · 2c7efc3e **BELUM** (novelty 2 verified belum terbaca) · 5fbb2531/26fe6c71/530bed9e **BELUM** (data soal belum ditarik). → Butir 1 **belum terpenuhi seluruhnya**; jalur uji §7.2 yang realistis: klaim 1 = **1d3efb52** (bila novelty 2c7efc3e gagal verifikasi) atau 2c7efc3e (bila lolos verifikasi ulang), klaim 2 = 1d3efb52.
- **Di luar lingkup berkas ini (pengingat, tidak dikerjakan):** butir 2 (rubrik v2 + (h)/(i) di QUALITY.md), butir 3 (audit draf-terkirim), butir 4 (lane tunggal Cloudflare — siap per §53), butir 5 (tabrakan LENGTH_SUFFIX — kini TERCATAT eksplisit di semua berkas steering yang disiapkan; perbaikan suffix-nya sendiri tetap utang provider), butir 6 (rincian temuan stderr provider + jaminan URL sisi-generasi + pola NOVELTY_MARKERS "baru dalam jawaban ini").
- **Tidak ada klaim/serve/submit/cron/MEMORY yang disentuh pekerjaan ini.** Semua berkas keluaran: 4 berkas di `provider/steering/` + laporan ini.
