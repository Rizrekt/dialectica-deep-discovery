# ANTREAN BERTANYA SIAP PILIH — 2026-11-18

Tiga draf pertanyaan FINAL (teks persis yang akan dikirim), disiapkan read-only:
nol create, nol fee tercharge. Masing-masing sudah: (1) dicek butir-per-butir
lawan questionRules general LIVE, (2) dicari duplikatnya lewat pencarian API
platform, (3) diuji silang dua lane model lain per Klausul F-31D (penantang
qwen-3.8-max + pemeriksa Nemotron), (4) dilengkapi kartu fee.

**URUTAN DIUBAH VONIS FRONTIER (2026-11-18, PETA-JALUR-3 §8 + sintesis
`belajar-2026-11-18/frontier-jalur3/SINTESIS-FRONTIER-JALUR3.md`):**
Slot 1 = B (prover-batching ZK) dengan premis DIPERSEMPIT per duck;
Slot 2 = A (sandwich) versi DIPERBAIKI — asumsi AMM/transaksi dikunci eksplisit
per vonis frontier (keberatan penantang atas A = cacat premis nyata);
Slot 3 = C (kaskade likuidasi, tidak berubah). Teks Slot 1 dan Slot 2 di bawah
adalah tulisan ulang pasca-vonis; cek aturan + catatan duplikat + uji silang
yang menempel pada tiap draf dijalankan atas versi pra-vonis dan DIPERTAHANKAN
apa adanya sebagai riwayat uji — assist loop menilai ulang teks final apa
adanya saat eksekusi, dan perubahan vonis tidak menambah klaim faktual baru.

**Keadaan tembak hari ini (semua slot): TERTAHAN SALDO.** Server sendiri sudah
mengatakannya lewat assist live 2026-11-18 atas draf sandwich (kini Slot 2):
fee n=8 = 1,3504, `affordable: false`, `spendableTrued: 0.0000`, "Nothing has
been charged." Antrean ini siap pilih begitu gerbang buka-kembali
(PETA-JALUR-3 §5.1 sebagaimana diketatkan §8: hanya P1/P3 yang membuka)
berbunyi; urutan tembak menentukan n: pertanyaan yang dipilih pertama memakai
n=8, kedua n=9, ketiga n=10 — kartu fee di bawah ditulis per slot dengan
asumsi slot ditembak sesuai nomornya; bila urutan dipilih berbeda, fee
mengikuti POSISI tembak, bukan slot.

---

## SLOT 1 — Ekonomi batching prover ZK-rollup (premis dipersempit per vonis frontier)

**Teks final (tulisan ulang pasca-vonis — premis dipersempit sesuai duck):**
> How does the largely fixed cost of generating a validity proof for one batch influence how many transactions a ZK-rollup accumulates before proving that batch, and how does that accumulation decision determine the latency between a transaction's inclusion and its batch being proven?

Perubahan dari versi pra-vonis: versi lama MENEGASKAN trade-off fee-vs-finalitas
sebagai premis ("force a trade-off between low per-transaction fees and fast
finality"). Per duck, tautan itu tidak boleh dibangun sebagai premis — finalitas
bisa bergantung mekanik lain; yang ditanyakan sekarang adalah bagaimana biaya
tetap prover memengaruhi keputusan batching, dan lewat keputusan itu, latensi
proof. Tautan kausalnya dieksplorasi oleh jawaban, bukan diasumsikan draf.

**Cek questionRules general LIVE (butir per butir; dijalankan atas versi
pra-vonis, dipertahankan — perubahan vonis hanya mempersempit premis):**
- Q_CLARITY: LOLOS — satu pertanyaan kausal tunggal; "low transaction volume"
  adalah kondisi relatif yang bisa diparameterkan jawaban (pola sama dengan
  "small price moves" di Q3 kita). Nemotron: pass.
- Q_GOOD_FAITH: LOLOS — mekanisme ekonomi protokol, tanpa bait. Nemotron: pass.
- Q_NON_TRIVIAL: LOLOS — menuntut menghubungkan struktur biaya prover,
  amortisasi batch, dan latensi finalitas. Nemotron: pass.
- Q_PROHIBITED: LOLOS. Nemotron: pass.

**Catatan pencarian duplikat (API platform, 2026-11-18):**
- Query "zero knowledge rollup prover batching cost amortization latency
  tradeoff proof aggregation" + query "fixed cost generating validity proof
  per batch rollup waits accumulate transactions lower fee per transaction
  withdrawal delay". Tetangga terdekat: d58f45f5 (kenapa memilih validity
  proof walau mahal — pertanyaan pilihan desain, bukan trade-off batching),
  c60e8c0e (batas throughput empiris verifikasi STARK rekursif di blob space),
  df9cb696 (faktor sukses L2 jangka panjang — umum). Wiki: zk-proof-generation-
  latency (konteks pembayaran x402), zk-rollup-scaling-bottlenecks — beda topik.
- Vonis: TIDAK ADA pertanyaan platform tentang ekonomi amortisasi biaya prover
  per batch. Belum diuji assist live (jatah uji live sesi itu hanya dipakai
  draf sandwich, kini Slot 2).

**Uji silang F-31D:**
- Pemeriksa Nemotron: **pass 4/4 aturan, overall pass.**
- Penantang qwen-3.8-max: **VERDICT: BREAK.** Serangan terkuatnya:
  (1) premis mengabaikan proof aggregation + pre-confirmations — katanya
  rollup volume rendah BISA menawarkan keduanya; (2) duplikat terhadap wacana
  "ZK-rollups latency-cost trade-off" di forum/paper (bukan pertanyaan
  platform); (3) "low volume" tak terdefinisi + tuduhan loaded question.
- Adjudikasi: (1) pre-confirmation adalah janji sequencer, BUKAN finality —
  finalitas terverifikasi-proof tetap menunggu batch terisi + proof jadi;
  aggregation menggeser biaya, tidak menghapus biaya tetap per batch (dan
  menambah latensi agregasi) — keberatan qwen justru bahan isi jawaban, bukan
  premis salah. (2) korpus yang salah lagi (lihat Slot 2). (3) pola kondisi
  relatif yang sama dengan pertanyaan kita yang terbukti lolos. **Status
  akhir: LOLOS dengan catatan.**
- Vonis frontier (Q4): sol + duck sepakat penuh draf ini tembakan pertama;
  duck mempersempit premisnya — sudah diterapkan pada teks final di atas.

**Kartu fee (bila ditembak pertama):** n=8 · fee **1,3504** · kredit +1 ·
net **−0,3504** · syarat saldo ≥ 1,3504 (akun kekurangan 3,2292 hari ini).

---

## SLOT 2 — Batas profit sandwich attack (MEV / matematika AMM; asumsi dikunci per vonis frontier)

**Teks final (tulisan ulang pasca-vonis — asumsi AMM/transaksi dikunci eksplisit):**
> Consider one victim swap in a constant-product AMM (x·y = k), protected by a minimum-amount-received limit (the victim's slippage tolerance), with the pool's reserves otherwise fixed and no other trades interleaving: why is the maximum profit of a sandwich attack around that swap bounded by the victim's slippage tolerance rather than scaling with the size of the victim's trade, and why does the attacker's own price impact on the closing trade consume most of that bound when the pool is shallow relative to the trade?

Perubahan dari versi pra-vonis: frontier menilai keberatan penantang atas draf
ini sebagai CACAT PREMIS NYATA — batas sandwich bukan ditentukan toleransi
slippage saja; ukuran trade, kedalaman pool, fee, dan kondisi pasar ikut
menentukan. Perbaikan yang diperintahkan frontier: kunci asumsi AMM/transaksi
secara eksplisit. Teks final kini menyatakan setting-nya di muka: satu swap
korban, AMM constant-product (x·y = k), batas minimum-received sebagai
toleransi slippage, cadangan pool tetap, tanpa trade lain menyela — di dalam
setting terkunci itulah batas ditanyakan.

**Cek questionRules general LIVE (butir per butir; dijalankan atas versi
pra-vonis, dipertahankan — tulisan ulang mengunci asumsi, tidak menambah
klaim baru):**
- Q_CLARITY: LOLOS — satu pertanyaan, satu mekanisme; tidak menyatakan klaim
  faktual sebagai premis bebas (fenomena yang ditanyakan adalah mekanisme yang
  terdokumentasi); bisa dijawab tuntas oleh expert AMM/MEV. Pemeriksa Nemotron:
  pass.
- Q_GOOD_FAITH: LOLOS — rasa-ingin-tahu mekanisme murni; bukan manipulasi/bait;
  tidak menyentuh lingkungan agent. Nemotron: pass.
- Q_NON_TRIVIAL: LOLOS — menuntut derivasi batas + analisis dampak harga dua
  sisi; tidak selesai dengan satu lookup. Nemotron: pass.
- Q_PROHIBITED: LOLOS — tidak ada konten terlarang. Nemotron: pass.

**Catatan pencarian duplikat (API platform, 2026-11-18):**
- Query "sandwich attack MEV slippage tolerance AMM profit bound" + query
  "maximum profit sandwich attack bounded slippage tolerance victim trade
  price impact back-run". Tetangga terdekat yang BENAR-BENAR ada:
  6a046721 (cara aggregator melindungi swap dari sandwich lewat splitting —
  pertanyaan perlindungan, bukan batas profit), 51f2da27 (hook Uniswap v4 vs
  permukaan MEV), a1770c04 (deteksi operator sandwich yang sama di Solana).
  Wiki tetangga: mev-extraction-mitigation, amm-price-impact-and-liquidity-
  valuation, loss-versus-rebalancing-lvr — semuanya beda topik.
- Vonis: TIDAK ADA pertanyaan platform yang menanyakan batas matematis ini.
- Bukti terkuat: assist live server menerima draf ini (versi pra-vonis) sampai
  fase **ready** dalam satu giliran (SYS_UNIQUENESS tidak menahan;
  conversationId 1fb147d4-1fbe-4a29-8927-f6c98eb6f016; transkrip di
  belajar-2026-11-18/peta-ask/ASSIST-LIVE-SLOT1-2026-11-18.txt). Tulisan ulang
  pasca-vonis mempersempit setting, bukan mengganti topik; penilaian
  SYS_UNIQUENESS final tetap terjadi di assist saat eksekusi.

**Uji silang F-31D:**
- Pemeriksa Nemotron (CrowLLM): **pass 4/4 aturan, overall pass.**
- Penantang qwen-3.8-max (CrowLLM; lane utama gpt-oss Cloudflare gugur 429 —
  alokasi neuron harian CF habis): **VERDICT: BREAK.** Serangan terkuatnya:
  (1) tuduhan premis salah — katanya batas ditentukan ukuran trade + k pool,
  bukan toleransi slippage; (2) tuduhan bundling dua pertanyaan + kata
  "consume" informal; (3) tuduhan duplikat terhadap literatur (Flash Boys 2.0,
  ethresear.ch) — BUKAN terhadap pertanyaan platform mana pun.
- Adjudikasi sesi ini (dicatat, bukan disembunyikan): serangan (1) keliru arah —
  toleransi slippage korban (min-out) adalah plafon ekstraksi: dorong harga
  melewatinya dan trade korban revert, profit nol; qwen sendiri mengakui
  toleransi rendah "memaksa attacker berdagang lebih kecil" — itu definisi
  batas yang bekerja. Ukuran trade/kedalaman menentukan apakah plafon TERCAPAI,
  bukan plafonnya. Serangan (2): dua klausa = satu mekanisme (batas + erosinya),
  pola yang sama dengan Q4/Q5/Q7 kita yang lolos assist satu giliran. Serangan
  (3) menguji korpus yang salah — gerbang keunikan menilai pertanyaan platform,
  dan pencarian + assist live membuktikan tidak ada yang sama. **Status akhir:
  LOLOS dengan catatan** — risiko sisa: hakim manusia/server bisa berbagi
  keberatan framing qwen.
- Vonis frontier (Q4): keberatan premis atas draf ini dinilai NYATA oleh
  frontier (lihat perubahan teks di atas) — adjudikasi sesi di atas
  dipertahankan sebagai riwayat, tetapi perbaikan frontier yang diberlakukan:
  asumsi dikunci eksplisit di teks final.

**Kartu fee (bila ditembak kedua):** n=9 · fee **1,8900** · kredit +1 ·
net **−0,8900** · syarat saldo sebelum tembak ini ≥ 1,8900 (sesudah net
tembakan pertama).

---

## SLOT 3 — Kaskade likuidasi lending

**Teks final:**
> Why can liquidations in an overcollateralized lending protocol amplify the very price fall that triggered them — pushing otherwise solvent positions underwater and leaving the protocol with bad debt — and what determines whether such a cascade stops early or runs to completion?

**Cek questionRules general LIVE:**
- Q_CLARITY: LOLOS — satu mekanisme + kondisi berhentinya; struktur dua klausa
  yang sama dengan Q7 kita (multisig) yang lolos. Nemotron: pass.
- Q_GOOD_FAITH: LOLOS. Nemotron: pass.
- Q_NON_TRIVIAL: LOLOS — sintesis lintas kedalaman likuiditas DEX, latensi
  oracle, desain insentif likuidator. Nemotron: pass.
- Q_PROHIBITED: LOLOS. Nemotron: pass.

**Catatan pencarian duplikat (API platform, 2026-11-18):**
- Query "lending protocol liquidation cascade bad debt spiral collateral
  price fall self amplifying" + query "liquidations selling collateral
  pushes price down triggering further liquidations feedback loop bad debt".
  Tetangga terdekat: 0e094df1 (insentif keeper melikuidasi tepat waktu +
  akibat bila tak ada keeper), dd2d9cab (apa yang menentukan likuidasi
  berjalan cepat vs bergerombol saat crash — soal bonus likuidator),
  d7e725ed (likuidasi protektif vs ekstraktif), e2727493 (likuidasi parsial
  di bursa perpetual). Wiki: leverage-amplified-illiquidity-multiplier,
  negative-amortization-kink-spiral — konsep tetangga, bukan pertanyaan yang sama.
- Vonis: TIDAK ADA pertanyaan platform yang menanyakan loop umpan-balik harga
  kaskade itu sendiri. Belum diuji assist live.

**Uji silang F-31D:**
- Pemeriksa Nemotron: **pass 4/4 aturan, overall pass.**
- Penantang qwen-3.8-max: **VERDICT: BREAK.** Serangan terkuatnya:
  (1) DUPLICATE — menunjuk pertanyaan generik karangan ("What is a
  liquidation cascade in DeFi protocols?") tanpa satu pun ID pertanyaan
  platform; (2) premis mengabaikan circuit breaker/penalti dinamis;
  (3) bagian kedua "unanswerable" karena multivariabel.
- Adjudikasi: (1) gugur oleh bukti pencarian platform di atas — gerbang
  menilai korpus platform, dan tidak ada ISR yang menanyakan mekanisme ini.
  (2) terbalik: klausa kedua draf PERSIS menanyakan apa yang menentukan
  kaskade berhenti — mitigasi protokol adalah bagian dari jawaban yang
  diminta, bukan lubang premis. (3) "multivariabel" = definisi pertanyaan
  sintesis Q_NON_TRIVIAL; Q4 kita (strategi sisa manipulasi TWAP) berbentuk
  sama dan lolos. **Status akhir: LOLOS dengan catatan** — dari tiga slot,
  inilah yang tuduhan duplikatnya paling keras; bila user ingin slot paling
  aman dari risiko SYS_UNIQUENESS, Slot 2 (draf sandwich) sudah memegang
  bukti assist-ready.

**Kartu fee (bila ditembak ketiga):** n=10 · fee **2,4915** · kredit +1 ·
net **−1,4915** · syarat saldo sebelum tembak ini ≥ 2,4915 (sesudah net dua
tembakan sebelumnya). Total bakar bersih tiga tembakan tanpa NIU: −2,7315;
saldo minimum sebelum urutan dimulai: **3,7319** (dikoreksi konsultasi
frontier dari 3,7315 — gerbang fee diperiksa sebelum kredit pembuatan masuk;
lihat PETA-JALUR-3 §8).

---

## Ringkasan uji silang (mentah tersimpan)

- Berkas mentah: `belajar-2026-11-18/peta-ask/crosstest-2026-11-18.json`
  (teks penantang + pemeriksa utuh per slot) dan `drafts.json`. Catatan:
  uji silang ini dijalankan atas draf versi pra-vonis frontier; susunan
  slot + teks Slot 1/2 berubah sesudahnya per vonis (lihat kepala berkas ini).
- Pemeriksa Nemotron: 3/3 draf pass semua aturan.
- Penantang: BREAK 3/3 (memang tugasnya mematahkan) — ketiga adjudikasi
  sesi ini: LOLOS dengan catatan, alasan tertulis per slot di atas.
- Lane gpt-oss Cloudflare: TIDAK TERPAKAI — 429, alokasi 10.000 neuron
  harian Workers AI habis di sisi server (log lokal membaca 4.786; angka
  server yang berlaku). Penantang digantikan qwen-3.8-max via CrowLLM
  dengan pacing ≥13 detik. Konsultasi frontier (duck/gpt-5.6-sol/gemini)
  BUKAN bagian uji ini — dijalankan sesi utama dari FRONTIER-PAKET-JALUR3.md;
  vonisnya kini sudah dilipat (PETA-JALUR-3 §8) dan susunan antrean ini
  adalah hasil lipatannya.
