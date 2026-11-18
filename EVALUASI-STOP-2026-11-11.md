# EVALUASI TOTAL DIALECTICA PASCA-STOP — 2026-11-11

**Status:** STOP TOTAL sejak 2026-11-11 07:28:57 WIB (falsified klaim uji JEDA #2, per janji day-close §46).
**Penulis:** evaluasi mandiri atas perintah sesi utama. **Nol klaim / nol serve selama evaluasi.**
**Sumber yang dibaca langsung:** MEKANISME-DAN-LAPANGAN.md §24–26, §29.2, §29.4, §30, §32, §34–35, §37, §39–40, §41–50; VERDICT-LEDGER.md; BEDAH-TOTAL-2026-11-10.md; BEDAH-KLAIM2-2026-11-10.md; DRILL-LOG.md; QUALITY.md; dialectica-operator-prompt.md (T1–T12).
**Keadaan akun saat evaluasi (bacaan server 07:30 WIB 2026-11-11, §50):** Expert 8522c990-d4f6-4155-a326-3c3c9802b950, dynamic/general, caps none; saldo **$TRUED 2,1212** (dari 5,1212); lifetimeEarned **4** (dari 7); Expertise **4** (dari 7); **RAR 9** (REL −3, availability 3, reputation 9); suspensionCount 3.

---

## VONIS: (b) LANJUT BERSYARAT — dengan uji 2 klaim dan stop otomatis

Rezim **tidak ditutup**, tetapi **tidak dilanjutkan seperti sebelumnya**. Kelanjutan hanya sah bila seluruh syarat minimum §7 terpenuhi **sebelum** klaim berikutnya, dan uji berikutnya dibatasi **maksimal 2 klaim** dengan aturan stop yang sudah dikunci di muka: **0/2 verified → TUTUP TOTAL (konversi ke (a)), tanpa evaluasi ulang.**

Tiga alasan vonis ini, bukan (a):

1. **Bar impasnya rendah dan terbukti bisa dilewati orang lain.** Break-even verdict rate ≈ **15%** (§6); median agen kohort eksternal **32%** (n=182), pemenang **55%** (§30). Yang harus dibuktikan bukan keunggulan — hanya keluar dari 0%.
2. **Ketiga spesies gagal kini masing-masing punya gerbang bernama yang bisa dibangun.** Spesies A → self-VFP dukungan semantik (sudah ada, perlu penegakan + perluasan cakupan). Spesies B → lantai §45 (sudah dibangun, terbukti menahan). Spesies C → gerbang cakupan sub-pertanyaan + standar bukti empiris (baru, mekanis, murah). Tidak ada spesies yang tanpa obat bernama.
3. **Biaya ujinya terbatas dan tidak memakai uang asli.** Seluruh lane $0/free; yang dipertaruhkan hanya sisa saldo **2,1212** (2 klaim) dan waktu. RAR 9 aman (+14 di atas ambang −5).

Tiga alasan vonis ini **bukan** kelanjutan bebas (kenapa bukan "lanjut biasa"):

1. **Kegagalan tidak konvergen: 3 klaim, 3 spesies, 0 pengulangan.** Setiap perbaikan melahirkan spesies baru — bukan pola yang mengecil. Itu bukti permukaan gagal kita belum terpetakan penuh.
2. **Cacat proses struktural: draf yang digerbang bukan draf yang terkirim.** Klaim one-shot mengundi ulang di dalam `trued answer`; gerbang semantik (4A/self-VFP) dinilai atas draf probe, bukan draf terkirim (§50 klaim uji butir 5: "skor di atas adalah atas draf probe, bukan draf terkirim"). Selama cacat ini hidup, tidak ada gerbang semantik yang bisa menjamin apa pun.
3. **Satu-satunya lane yang menyelesaikan klaim uji adalah cadangan, dan tulang punggung mati 17 jam.** Vyce down sejak 14:04 2026-11-10 (§50). Tidak ada lane yang layak disebut andal.

Bila syarat §7 tidak dipenuhi seluruhnya, vonis ini **otomatis menjadi (a) TUTUP** — tidak ada kelanjutan parsial.

---

## §1. Bedah akar ketiga falsified — satu keluarga, tiga mekanisme, tiga gerbang

### 1.1 Tabel bukti per klaim

| | Klaim #1 — 60fa9935 (fcb7b015) | Klaim #2 — 472b29a0 (097df475) | Klaim #3 — 71f472d6 (0d76cc7c) |
|---|---|---|---|
| Submit / verdict | 19:03:32 → 19:07:55 WIB (263 dtk) | ±21:22 → 21:24:29 WIB (±150 dtk) | 07:26:42 → 07:28:57 WIB (±135 dtk) |
| Panel | 4 verifier; **2 support / 2 refutasi** | 4 verifier; **0 support / 4 refutasi** | 2 verifier; **0 support / 1 refutasi** |
| Panjang terkirim | 5.286 kar | 6.580 kar | 5.147 kar |
| Lantai §45 | **LOLOS semua** (4 URL, densitas 2,08, rasio terikat 0,647 — §45.1) | **GAGAL semua** (0 URL, densitas 0,456, rasio 0,318 — §45.1) | **LOLOS semua** (probe: 10 URL, densitas 1,823, rasio 0,60 — §50 klaim uji butir 5) |
| 4A / self-VFP | 4A LOLOS semua butir (§41.6); self-VFP belum ada saat itu | Steering bersih; generasi melanggar diam-diam | 4A LOLOS penuh; self-VFP tercatat; sensus angka tercatat, "nol angka yatim" |
| Spesies | **A — dukungan semantik** | **B — lantai mekanik + fakta salah** | **C — scope miss + sitasi-tanpa-bukti** |

### 1.2 Klaim #1 — spesies A: sitasi ada, tidak mendukung (A_CITATION)

Bukti (BEDAH-TOTAL §2.1, kutipan persis jawaban kita):

> *"On Arbitrum, Optimism and Base, deployment cost is dominated by **L1 data cost**, not the 200-gas-per-byte code deposit."*
> *"…the clone's advantage **GROWS on the deployment side** … while its lifetime tax nearly **VANISHES on the execution side**."*

Sitasi yang menempel: EIP-2028 (calldata 16 gas/byte) dan EIP-4844 (blob). Bedah: *"Kedua dokumen itu diam total soal komposisi biaya deployment di Arbitrum/Optimism/Base."* Prosedur arena: *"a source that exists but does not state or support the claim = non-compliant."*

Yang penting: **semua angka keras jawaban ini BENAR dan terikat benar** (runtime EIP-1167 45 byte; 200 gas/byte; 16 gas EIP-2028; jalur OpenZeppelin v5.0.2 nyata; sudut beacon + repricing L2 benar-benar baru). Pembunuhnya bukan angka salah — melainkan dua klaim penopang §2 yang merupakan klaim Tier-1 bernama-rantai dengan dukungan Tier-0. Sekunder: kuantifier absolut tanpa hedge di titik klaim (P2, A_UNCERTAINTY); dikotomi CREATE2 palsu (P3, A_REASONING); beacon sebagai "anggota keluarga minimal-proxy" yang longgar kategori (P4).

Kontras yang lolos di ISR yang sama (BEDAH-TOTAL §2.3): Reinhard mengikat **setiap** angka ke sitasi bernomor + hedge di titik klaim (7.765 kar, 13 tautan); nanik lolos dengan **0 sitasi karena 0 klaim Tier-1** (5.349 kar, semua rentang/Tier-0). Dua jalan terbukti lolos — kita mengambil jalan tengah yang fatal: *"spesifisitas Tier-1 + nama rantai, dengan dukungan bukti kelas Tier-0."*

Gerbang yang seharusnya menangkapnya: self-VFP T10.2 (buka-dan-baca sitasi per klaim) — **belum ada** saat klaim #1 dikirim; ia lahir dari bedah ini (BEDAH-TOTAL §5 butir 3).

### 1.3 Klaim #2 — spesies B: tanpa sitasi + fakta rantai salah (A_CITATION + A_REASONING)

Bukti (BEDAH-KLAIM2 §2.2; jawaban memuat **0 URL, 0 sitasi** dalam bentuk apa pun):

| Klaim di jawaban | Nilai salah | Nilai benar | Sumber benar |
|---|---|---|---|
| Base fee BSC bergerak ikut utilisasi (EIP-1559) | base fee bergerak | base fee BSC ditambatkan **0** (BEP-226); harga gas = tip penuh, min **0,05 gwei** sejak Okt 2025; bakar via BEP-95 | BEP-226; BEP-95 |
| Klaim `freeMint` ≈ 21.000 gas | ~21.000 gas | 21.000 = transfer polos; transfer BEP-20 saja **50–65 ribu gas** | Mekanika EVM |
| Base fee naik 5–10× saat ramai | kelipatan 5–10× | turunan dari premis yang tidak ada | Turunan K1 |
| Blok BSC ~3 dtk, 21 validator | ~3 dtk / 21 | **0,45 dtk** sejak Fermi (14 Jan 2026); validator **40+** | Fermi; Maxwell Jun 2025 |
| 100.000 blok ≈ 3,5 hari | 3,5 hari | ≈ **12,5 jam** — salah **±6,7×** | Turunan K4 |
| Ambang Sybil 50+ wallet / 0,001–0,01 BNB / 24 jam | disajikan sebagai fakta terukur | angka tanpa jangkar, tanpa derivasi, tanpa label ilustratif | — (tidak ada) |

Tiga hal baru dibanding #1 (BEDAH-KLAIM2 §7, eksplisit): (i) bentuk kegagalan sitasi terbalik — #1 sitasi ada-tapi-tak-mendukung, #2 sitasi **tidak ada sama sekali**; (ii) klaimnya bukan cuma tak didukung tapi **terbantahkan** (angka keras #1 semua benar; #2 membawa parameter rantai yang salah faktual per keadaan BSC 2026) — naik kelas dari A_CITATION murni ke A_CITATION + A_REASONING; (iii) **racun masuk di hilir, bukan di hulu** — steering #2 sudah bersih ("tanpa angka, mekanisme saja"), generasi menyisipkan kembali angka karangan diam-diam (risiko R1 "generative reinsertion" kini TERWUJUD), dan self-VFP + wrapper tidak menangkapnya karena **tabel kanonis wrapper tidak memuat parameter BSC**.

Akibat verdict: **0/4** — satu-satunya jawaban di ISR itu dengan 0 support; 6 falsified lain berhenti di refuted 2.

### 1.4 Klaim #3 — spesies C: scope miss + sitasi yang tidak membuktikan apa pun (A_SCOPE)

Bukti (§50 klaim uji butir 8; bedah inferensi dari teks terkirim — alasan panel **tidak terekspos API**, dinyatakan apa adanya):

Pertanyaan meminta 3 hal eksplisit: (a) *"most promising applications"*, (b) *"implementation challenges"*, (c) *"measurable success indicators"*. Jawaban terkirim (5.147 kar) **TIDAK MENAMAI SATU PUN aplikasi AI** — tidak ada forecasting, scheduling, copilot, returns-triage, markdown, predictive-maintenance, AP-matching. **Nol.** Steering §16 memerintahkan *"Do NOT re-derive"* portofolio aplikasi — model menafsirkannya sebagai "jangan sebut aplikasi sama sekali". Keempat jawaban verified SEMUANYA menamai aplikasi.

Kandidat pendukung: 8 angka berlabel *"planning hypothesis"* + ambang tanpa angka (*"stays below a floor"*, *"at least a fraction"*) — jawaban ini tidak mengandung **SATU PUN** angka/fakta dunia yang terikat sumber di luar definisi. Goodhart/Campbell/MAPE/HACCP adalah **definisi konsep, bukan bukti empiris**. Lantai mekanik menghitung KEBERADAAN sitasi, bukan KEKUATAN bukti — draf lolos lantai sambil tetap kosong bukti.

Yang GUGUR sebagai penjelasan (§50 klaim uji butir 8): lantai mekanik (lolos semua dengan margin); format/panjang (5.147 kar pita baku, 6 seksi, penutup bermarker); parafrase (spine absen dari verified — grep 0 hit).

Verdict tercepat rezim (±135 dtk; #1 263 dtk, #2 ±150 dtk) pada panel terkecil (2 verifier) dengan 1 refutasi — konsisten dengan penolakan yang jelas dan cepat, bukan antrean.

### 1.5 Apakah ada SATU akar tunggal? — TIDAK. Bukti per klaim

Keluarga akarnya sama — BEDAH-KLAIM2 §7 merumuskan *"spesifisitas Tier-1, dukungan Tier-0"* berlaku kata per kata untuk #1 dan #2 — tetapi **tidak ada satu perbaikan yang mengubah hasil ketiganya**:

- **Perbaikan #2 (lantai §45) tidak mengubah #1 dan #3.** Keduanya lolos semua lantai dengan margin (#1: 4 URL/2,08/0,647; #3: 10 URL/1,823/0,60). Lantai membunuh spesies B saja.
- **Perbaikan #1 (self-VFP dukungan semantik) tidak mengubah #3 — terbukti empiris.** Klaim #3 dikirim DENGAN self-VFP tercatat dan sensus angka tercatat ("nol angka yatim"), tetap falsified. Self-VFP memeriksa apakah sitasi mendukung KONSEP di kalimatnya — tidak memeriksa apakah jawaban MENJAWAB pertanyaan, dan tidak memeriksa apakah ada bukti empiris di luar definisi.
- **Perbaikan #3 (gerbang cakupan) tidak mengubah #1 dan #2.** #1 menjawab semua sub-pertanyaannya (rubrik (b) LOLOS substantif); #2 gagal scope hanya parsial/sekunder — pembunuhnya fakta salah, bukan cakupan.

Kandidat akar proses terdekat — **draf yang digerbang ≠ draf yang terkirim** — pun tidak mencakup ketiganya: ia berkontribusi pada #1 (draf probe lolos 4A; draf terkirim membawa P1) dan #3 (draf probe lolos 4A + self-VFP; draf terkirim melewatkan scope), tetapi #2 akan lolos self-VFP atas draf mana pun karena sensusnya tidak memuat parameter BSC dan lantainya belum ada. Jadi: **satu keluarga, tiga mekanisme, tiga gerbang — plus satu cacat proses yang memperparah dua dari tiga.**

Implikasi vonis: perbaikan tunggal apa pun tidak cukup. Yang dibutuhkan adalah **tumpukan gerbang** (§7) — dan tumpukan itu baru bisa dinilai sesudah diuji hidup, bukan dari alasan.

---

## §2. Gerbang §45 + T12 — nilai tambah vs biaya deadlock (kuantifikasi jendela 07:00)

### 2.1 Nilai tambah: terbukti menahan spesies B — dan hanya spesies B

Bukti penahan (MEKANISME §50.4–§50.5, jendela hunt 07:00 2026-11-11):

- **5/5 draf ditahan lantai, 0 temuan audit angka.** Empat probe (Nemotron ×2, Cloudflare ×1, DashScope ×1) + satu generasi diagnostik — semuanya tepat 3 temuan, semuanya lantai: K-1(a) URL **0** < 1; K-1(b) densitas **0,358** < 0,5 (3 sitasi / 8.380 kar); K-2 rasio terikat **0,286** < 0,30 (2 dari 7 token angka dalam ±150 kar dari sitasi). Audit angka murni: wrong 0, bound-unverified 0.
- Profil klaim #2 (0 URL, 0,456, 0,318) **akan tertahan** oleh lantai ini — spesies B tertutup struktural. Itu nilai tambah yang nyata dan terukur: 1 dari 3 spesies gagal rezim (±33% mode gagal teramati) kini tidak bisa lewat.
- Bukti jalan keluarnya juga terukur: steering 71f472d6 dipatch 07:14 dengan mandat 4 URL Wikipedia persis → klaim uji LOLOS lantai via Cloudflare (job completed 07:27:51). Pola perbaikan = **steering menamai URL persis**, bukan "sebutkan sumber" generik.

Batas nilai tambah (data eksternal + data kita):

- Studi juara-verdict (T12): **23,0% falsified eksternal lolos kombo K-1+K-2** — lantai adalah syarat perlu, bukan penjamin. Klaim #3 adalah kasus yang diramalkan itu, kini dengan data kita sendiri: **1/1 lolos-lantai tetap falsified**.
- Lantai tidak mengukur kebenaran angka, dukungan semantik, cakupan, atau kekuatan bukti. Terhadap spesies A dan C, nilai tambahnya **nol**.

### 2.2 Biaya deadlock: jendela 07:00 lumpuh total sampai steering diperbaiki satu per satu

Akar deadlock (§50.5): **steering melarang mengarang URL/DOI + lantai menuntut ≥1 URL = mustahil oleh konstruksi.** 5/5 draf jendela itu 0 URL — model menaati larangan steering. Lantai diimplementasi 21:5x dan **diuji offline saja** (§45.5); empat probe + satu diagnostik jendela 07:00 adalah uji live PERTAMA — semuanya gagal di lantai. Gerbang yang tidak pernah dilewati satu draf pun bukan gerbang — ia tembok.

Kuantifikasi biaya (jendela 07:00):

- **Sendable rate lane cadangan: 0/4** (Nemotron ×2, Cloudflare ×1, DashScope ×1) sebelum patch steering; 0/5 termasuk diagnostik.
- **Waktu terbakar:** probe Vyce gagal-lambat 112,6 + 220,7 dtk; probe cadangan ±29–80 dtk per generasi; runonce membakar 4 generasi Nemotron (07:08–07:13) + 2 Cloudflare sebelum satu klaim lolos. Total ±30 menit jendela untuk 1 klaim — yang falsified.
- **Biaya perbaikan:** per steering, manual, satu per satu — verifikasi live tiap URL (HTTP 200) + aturan penempatan + sensus digit. 2c7efc3e sudah direvisi mengikuti pola ini (§50.7); sisa antrean (1d3efb52, 5fbb2531, 1d758352, 26fe6c71, 530bed9e) belum.
- **Tabrakan pita panjang (LENGTH_SUFFIX):** suffix provider menuntut 5.500–7.500 kar sementara pita marathon ramai 10–12 rb kar (§50.7). Yang mengikat kelolosan kirim adalah lantai + pintu (d)/(g), bukan presisi pita — tetapi tabrakan ini menambah varians gagal-kirim yang tidak perlu.
- **False-positive lantai pada draf bermutu baik: tidak terukur, tapi bukan nol.** Studi: ≥1 URL hanya di **83,0% verified** (vs 47,5% falsified) — artinya ±17% jawaban verified-grade tidak punya URL dan akan gagal K-1(a) mentah. Di jendela 07:00, tidak ada draf baik yang tertahan secara terbukti (draf diagnostik gagal (b)/(e) juga) — tetapi tidak ada pula draf baik yang muncul untuk diuji. Presisi lantai pada draf baik = **tidak diketahui**.

### 2.3 Neraca gerbang

| Sisi | Angka |
|---|---|
| Spesies gagal yang dibunuh | 1 dari 3 teramati (B) — profil #2 tertahan pasti |
| Spesies gagal yang tidak disentuh | 2 dari 3 (A, C) — keduanya lolos lantai |
| Draf ditahan di jendela 07:00 | 5/5 (100%) — penahan sistematis, bukan varians lane |
| Jendela lumpuh sampai perbaikan steering | 1 jendela penuh (07:00); perbaikan per-target manual |
| False-positive pada verified-grade | ±17% (dari 83,0% verified ber-URL) — estimasi studi, belum terukur di draf kita |
| Uji live sebelum jendela 07:00 | 0 — implementasi 21:5x hanya diuji offline (30/30 PASS) |

**Kesimpulan §2:** lantai bernilai **positif tetapi hanya sebagai lapis dalam tumpukan** — ia mengubah "kadang falsified" menjadi "biasanya tidak bisa kirim" bila steering tidak diperbaiki. Tanpa mandat-URL di steering, lantai adalah deadlock; dengan mandat-URL, lantai adalah filter spesies B yang bekerja. Biaya deadlock-nya **sekali bayar per steering** (bukan per klaim), jadi neracanya membaik sesudah semua steering antrean diperbaiki — tetapi sampai perbaikan itu selesai, lantai menahan 100% throughput.

---

## §3. Lane — tidak ada tulang punggung yang hidup

### 3.1 Vyce (primer desain): MATI 17 jam

Downtime sejak 14:04 2026-11-10 → jam ke-17 pada 07:00 2026-11-11 (§50). GLM 503 *"model currently unavailable"*, deepseek-v4.1 stream kosong, Nemotron-Vyce 503. Modus gagal memburuk: gagal cepat (§36/§41: 0,7–3,2 dtk) → **gagal lambat** (21:00: ±111–218 dtk/lane; 07:00: 112,6 + 220,7 dtk) lewat retry backoff. Saldo promo **$109,3485** (§25.10) tidak bisa dipakai selama lane mati — uang promo yang tidak mengalir sama dengan tidak ada. **Vonis: bukan lane uji.** Kembali hanya bila satu probe lolos di jendela mana pun; sampai itu, Vyce adalah nama di tangga probe, bukan jalur klaim.

### 3.2 OpenRouter / Nemotron: klaim-terbukti ×2, keandalan runtuh di jendela 07:00

Rekam jejak: satu-satunya lane yang menyelesaikan klaim #1 dan #2 (keduanya completed via one-shot, §41/§44). Probe kelas-klaim **3/3 sendable** di 19:00–21:00 2026-11-10 (Nemotron lolos dua kali berturut-turut, §44.10).

Jendela 07:00 2026-11-11: **0/4 sendable** untuk target 71f472d6 — 2× gagal lantai (§50 runonce probe 1–2: 6.157 kar / 5.321 kar, 3 temuan FLOOR) + **2× generasi kosong** (probe 3–4: `no usable answer: status=200 chars=0` sesudah 217 dtk dan 146 dtk — pola E2: HTTP 200 ≠ jawaban). Ditambah probe 17:00 2026-11-10 yang gagal 2× (0 karakter; 3.790 kar < lantai 4.500 sesudah regenerasi).

Kelemahan struktural: (i) varians panjang lebar (benchmark median 3.846 kar, di bawah lantai 4.500; drill v1 6.514 vs v2 11.375 kar prompt sama — §34); (ii) konservatisme wrapper: **temuan audit APA PUN → tidak sendable**, bahkan yang sudah terpatch mekanis (§35.3 — laporan membuang field `span`, jadi patchable vs unpatchable tidak bisa dibedakan); (iii) kuota **50/hari** (reset 00:00 UTC), sisa ±43–45 pada 07:00 — cukup untuk uji, tidak untuk volume.

**Vonis: lane cadangan, BUKAN lane uji.** Syarat pakai: probe kelas-klaim (bukan prompt pendek — §36 membuktikan prompt pendek mengukur konfigurasi yang tidak dipakai klaim) + steering bermandat-URL + kuota ≥3. Fallback bila Cloudflare gagal probe.

### 3.3 Cloudflare / gpt-oss-120b: satu-satunya lane yang menyelesaikan klaim uji

Rekam jejak: bench 3/3 selesai, latensi median **53,5 dtk** (Nemotron 85,4), panjang mentah median **6.147 kar — di pita 3/3 tanpa satu pun regenerasi**, mojibake 0, neuron median **187,04/generasi → kapasitas ±53 generasi/hari** (§37). Di jendela 07:00: probe 1 gagal (d) (K-2 0,261), probe 2 **sendable=true** (5.486 kar; URL 10, densitas 1,823, rasio 0,60) → klaim uji completed 07:27:51. Neuron hari itu ±2.167 dari 9.000 — jauh di bawah pagu.

Kelemahan: (d) mentah **GAGAL 3/3** di bench (penyakit E1 yang sama: 700 gas terikat EIP-2929; runtime EIP-1167 "10 byte") — semua tertangkap + ter-patch wrapper; sendable bench **0/3** (n=3). Artinya lane ini butuh steering keras anti-E1 (§37 butir 4(viii)) untuk menghasilkan draf sendable dengan andal.

**Aset yang belum pernah dipakai: serve pengganti §39.** Arsitektur PREPARE_CMD (generasi SEBELUM klaim → cache → bid hanya bila cache ada) membuat jalur utama serve ini **bebas-abandoned secara struktural** — satu-satunya jalur di rezim ini di mana draf yang digerbang = draf yang terkirim. Cap keras 10 generasi serve/hari-UTC. Status: **SIAP di atas kertas + teruji asap (25/25) + smoke live 0 job — TIDAK PERNAH dinyalakan dengan kata kunci nyata** (§39; day-close §46: serve memang mati sejak awal).

**Vonis: LANE UJI TUNGGAL untuk uji 2 klaim (§7).** Syarat: steering keras anti-E1 aktif + mandat-URL + neuron <9.000 (terpasang di provider). Serve §39 adalah jalur Pioneer uji berikutnya — tetapi baru sesudah satu smoke live berkata-kunci nyata dengan 0 job di jendela hunt.

### 3.4 DashScope / deepseek-v4-pro-0813: stok hangus besok

Stok ±982.045 token sesudah bench (§40); terbakar 2.865 di probe 07:00 → ±979 ribu tersisa; **hangus 2026-11-12**. Overshoot panjang SISTEMATIS (11.792 / 16.188 / 13.626 kar vs pita 4.500–8.000) — model memperlakukan syarat panjang sebagai lantai. (d) mentah GAGAL 3/3 di bench (ikatan EIP-2929). Stop-on-Exhaust **BELUM terbukti menolak** (hanya klaim konsol + dokumentasi 403 — belum pernah teramati live).

**Vonis: lane satu-hari, bakar-atau-hilang.** Hanya untuk target yang mengizinkan 10–12 rb kar (marathon ramai viso ≥5) dan hanya pada 2026-11-11. Bukan lane uji (target uji pertama kita berpita baku). Sesudah 2026-11-12: **pensiun otomatis**.

### 3.5 Z.ai / glm-4.7-flash: ketersediaan belum terbukti

Bench: **6/10 attempt kena 1305** (429 kolam gratis jenuh); jendela 07:00: **1305 ×2** sesudah retry 60 dtk tepat satu kali → lane mati sisa jendela (§50). Kualitas per generasi sukses kompetitif (panjang alami di pita, latensi sukses tercepat 35,2 dtk, mojibake 0; (d) lolos mekanis dengan 2 angka presisi mencurigakan — §40). Kapasitas harian tidak teramati; limit konkurensi resmi = 1 (sekuensial ketat).

**Vonis: PARKIR.** Bukan lane uji; bukan satu-satunya lane di jendela mana pun sampai ketersediaan terbukti lintas ≥3 jendela (rasio sukses/1305 di log lane adalah alat pembuktiannya).

### 3.6 Yang sudah mati / dilarang — tidak dihitung sebagai lane

- **Gemini: DILARANG.** Perintah user 15:03 2026-11-10: *"Gemini TIDAK dipakai sama sekali untuk Dialectica"* (termasuk telemetri/benchmark — §36). Pencabutan klaim §29.4 tetap berlaku. Probe sukses §29.2 (8.568 kar, 19,2 dtk) tidak mengubah apa pun: kemampuan ≠ izin; kuota tak terbaca + REL −3 = EV negatif eksistensial.
- **Sonogami: MATI.** Key dicabut 15:22 2026-11-10; 26× 401 berurutan *"invalid or revoked API key"*; nol pemulihan (§31/§31.1). Grok 4.6-nya pernah menyelesaikan jawaban kelas klaim (2/3) — tetapi tanpa key hidup, lane ini tidak ada.
- **Vyce deepseek-v4.1 / GLM:** lihat §3.1 — mati bersama Vyce.

### 3.7 Ringkasan lane

| Lane | Status 07:00 11 Nov | Klaim completed | Syarat bertahan |
|---|---|---|---|
| Vyce (GLM/deepseek/Nemotron) | MATI 17 jam | 0 (rezim ini) | 1 probe lolos → normal |
| OpenRouter/Nemotron | Generate, 0/4 sendable | 2 (#1, #2) | Probe kelas-klaim + steering URL-mandat; fallback |
| **Cloudflare/gpt-oss-120b** | **Satu-satunya yang menyelesaikan klaim uji** | **1 (#3)** | **Lane uji tunggal; steering anti-E1 + URL-mandat** |
| DashScope | Generate, ditahan lantai | 0 | Hanya 11 Nov, target 10–12 rb kar; pensiun 12 Nov |
| Z.ai | 1305 ×2, mati | 0 | Parkir s/d ketersediaan ≥3 jendela |
| Gemini | Dilarang user | 0 | — (tidak dibuka lagi tanpa perintah eksplisit user) |
| Sonogami | Key dicabut | 0 | — (butuh key baru + jaminan operator) |

---

## §4. Rubrik v1 — buta terhadap pasangan yang menentukan

### 4.1 Bukti kebutaan (DRILL-LOG, jendela 07:00 2026-11-11)

Pasangan bedah 1d758352 — **0006fe08 VERIFIED** (15.519 kar, support 4 / refute 0) vs **66f46c3e FALSIFIED** (14.359 kar, support 0 / refute 2) — skor rubrik v1 **IDENTIK**:

| Butir | 0006fe08 (verified) | 66f46c3e (falsified) |
|---|---|---|
| (a) pembuka ≤3 kalimat | L | L |
| (b) struktur ##/### + lead-in | G | G |
| (c) panjang 4.500–8.000 (10–12 rb marathon) | G | G |
| (d) sitasi (pintu mati) | G | G |
| (e) kebaruan eksplisit | L | L |
| (f) bukan parafrase | L | L |
| (g) format | L | L |

**Skor: (L,G,G,G,L,L,L) vs (L,G,G,G,L,L,L). Rubrik v1 BUTA terhadap pasangan ini.** Pembeda satu-satunya = kebenaran angka: vanity **28 vs 32 byte** per EIP-225 (ruang cari 2²²⁴ vs yang benar); grinding **1 μs** untuk 1.000 kandidat (mengabaikan tiap kandidat butuh segel ECDSA segar) vs sign-dominated **10⁴–10⁵ sign/dtk/core**; **21 validator / 3 dtk** basi; fee 0,5–2 BNB salah atribusi chart BscScan; ~63% dari rumus ad hoc. Rubrik mengukur bentuk + keberadaan sitasi — bukan kebenaran.

### 4.2 Hitungan celah kumulatif (DRILL-LOG, seluruh entri)

| Celah | Kemunculan | Isi |
|---|---|---|
| (b) struktur/lead-in | **×3** (17:00, 21:00 10 Nov; 07:00 11 Nov) | Verified berulang lolos tanpa lead-in tebal / tanpa seksi bernomor sendiri — (b) lebih ketat dari selera verifier |
| (c) panjang | **×4** (koreksi v2 09:26; 17:00; 21:00; 07:00) | Kedua jawaban 07:00 >12 rb kar, satu verified — plafon 12 rb tidak mengikat verifier bahkan untuk jawaban terpanjang |
| (d) sitasi — verified gagal pintu-mati | **×1** (07:00 11 Nov, pertama) | 0006fe08 VERIFIED padahal (d) GAGAL ketat (~$765K Meebits tanpa sitasi; 10⁴–10⁵ sign/dtk/core tanpa dokumen; penundaan verifikasi gaya E3) — (d) biner akan memblokir jawaban 4-support atas angka periferal |
| (e) kebaruan — tidak membedakan | **×1** (07:00 11 Nov, pertama) | 66f46c3e FALSIFIED padahal (e) LOLOS (§8 menamai 6 "kontribusi", semuanya bertumpu angka salah) — menamai kebaruan ≠ kebaruan itu benar |
| (a) pembuka | ×1 (21:00 10 Nov) | cfb6bcb9 verified padahal (a) GAGAL (pembuka 4 kalimat; tesis tajam) — hitung kalimat tesis saja |
| E1 (sitasi harus mengikat angkanya) | **diperkuat ×3** (d9f49e11; 96c384fd; 66f46c3e) | Ambang adopsi (≥2 kasus falsified berakar ini) **TERPENUHI** — tetapi QUALITY.md belum mencatat bump versi / adopsi apa pun |

Catatan penyeimbang: (d) **adalah** pembeda sejati di drill-drill sebelumnya — menangkap d9f49e11 (17:00) dan 96c384fd (21:00) dengan benar. Rubrik tidak sepenuhnya buta; ia buta **tepat di pasangan yang menentukan** dan salah arah di (b)/(c) secara sistematis.

### 4.3 Apakah rubrik masih layak sebagai gerbang? — YA, dengan revisi v2. Apakah revisi itu cukup untuk mengubah verdict rate? — TIDAK, sendirian.

**Layak dipertahankan** karena: (d) terbukti menangkap falsified E1 dua kali sebelum 07:00; (g) menangkap kegagalan format yang nyata dalam sejarah kita (2/3 job lama "reply was not JSON"); struktur (b)/(c) tetap berkorelasi dengan kohort (header 79%, URL 77% — §30). Membuang rubrik berarti membuang satu-satunya saringan pra-kirim yang terukur.

**Revisi v2 yang dibutuhkan (masuk CHANGELOG QUALITY.md sebagai bump bernomor, bukan diam-diam):**

- **(b) longgarkan: cakupan di atas lead-in.** Nilai apakah setiap sub-pertanyaan punya seksinya — bukan apakah tiap seksi dibuka lead-in tebal. (b) ×3 membuktikan lead-in bukan penanda selera verifier.
- **(c) longgarkan: plafon 12 rb jadi anjuran, bukan gagal.** (c) ×4 membuktikan plafon tidak mengikat verifier; yang mengikat adalah pita bawah (jawaban terlalu pendek = tidak ada isi). Pertahankan lantai 4.500; plafon jadi catatan, bukan pintu.
- **(d) timbang sentralitas angka.** Angka poros (yang menopang tesis) wajib entailment sitasi→angka; angka periferal/orde-besaran/estimasi boleh berbingkai estimasi eksplisit + hedge di titik klaim. (d) biner hari ini memblokir jawaban verified-grade (kasus 0006fe08) — false positive yang terukur.
- **(e) kebaruan harus BENAR, bukan dinamai.** Penutup yang menamai kebaruan di atas angka salah = GAGAL (e). Cek: klaim kebaruan harus lolos (d) atas angkanya sendiri.
- **(h) BARU — gerbang cakupan sub-pertanyaan (pintu mati).** Daftar sub-pertanyaan eksplisit soal; draf terkirim (teks reveal, bukan draf probe) WAJIB memuat jawaban untuk masing-masing. Ini gerbang yang akan menangkap spesies C klaim #3. Dinilai atas teks TERKIRIM dalam verdict watch.
- **(i) BARU — standar bukti empiris.** Draf WAJIB memuat ≥1 fakta/angka dunia yang terikat sumber yang menyatakannya — definisi konsep saja (Goodhart/Campbell/MAPE/HACCP tanpa data) tidak cukup. Definisi ≠ bukti.

**Kenapa revisi saja tidak cukup:** rubrik adalah saringan pra-kirim atas teks; tiga kegagalan rezim berakar di (i) generasi yang mengarang/membaca-steering-salah, (ii) steering yang melarang tanpa memandatkan, (iii) proses yang menggerbang draf probe bukan draf terkirim. Revisi rubrik menaikkan lantai — ia tidak memperbaiki generator, tidak menulis steering, dan tidak menutup celah draf-terkirim. Verdict rate hanya bergerak bila revisi rubrik **+** steering bermandat-URL **+** gerbang (h)/(i) **+** lane tunggal yang andal **+** audit draf-terkirim berjalan bersama. Klaim itu diuji oleh uji 2 klaim (§7), bukan oleh argumen.

---

## §5. Model verdict — yang bertahan dan yang gugur

Model agregasi (§43/L-01, direvisi dua kali oleh data):

- **BERTAHAN — clean sheet:** verified ⟺ **≥2 support DAN 0 refutasi**; **1 refutasi membunuh** (falsified dengan 1 refutasi pada panel 2 verifier — klaim #3, 0/1 — memperkuatnya; panel kita: 4, 4, 2 verifier; refutasi: 2, 4, 1). Support tidak pernah menyelamatkan (2/2 tetap falsified — klaim #1).
- **GUGUR — "verified = tepat 2 support":** cfb6bcb9 verified dengan 4 support (21:00 10 Nov); 0006fe08 verified dengan 4 support (07:00 11 Nov). Model revisi ≥2 support bertahan di kedua drill berikutnya.
- **Latensi verdict makin cepat seiring kekosongan isi:** 263 → ±150 → ±135 dtk (median berjalan ±150 dtk; data L-05). Hipotesis: verdict cepat ≈ penolakan jelas.
- **Batas penglihatan struktural:** teks alasan refutasi per verifier **tidak terekspos** (endpoint per-VFP 404 semua — BEDAH-TOTAL §1.2); falsified **tidak memicu notifikasi**. Semua bedah akar adalah inferensi dari teks terkirim, bukan kutipan panel — dan harus dinyatakan sebagai inferensi. Konsekuensinya: gerbang kita tidak akan pernah bisa belajar dari kata-kata verifier; ia hanya bisa belajar dari pola cacah + teks.

---

## §6. Ekonomi rezim — saldo, runway, dan ambang impas

### 6.1 Neraca

| Ukuran | 10 Nov 13:45 (§24) | 11 Nov 07:30 (§50) | Δ |
|---|---|---|---|
| Saldo $TRUED | 5,1212 | **2,1212** | **−3,0000** (3 falsified × −1) |
| LifetimeEarned | 7 | **4** | −3 |
| Expertise (general) | 7 | **4** | −3 |
| RAR | +4 | **9** | +5 (availability 0→3 dari 3 job completed; REL −3 beku; reputation 7→9) |
| Klaim rezim caps-20 | 0 | 3 | 3 completed, **0 verified, 3 falsified, 0 abandoned** |
| Payout masuk | — | 0 | 0 slot (Pioneer/Innovator/Marathon) |
| Token terpakai 10 Nov | — | 202.380 (semua $0) | OpenRouter 179.874; Cloudflare 9.289; DashScope 5.084; Z.ai 8.133; Vyce 0 |

Catatan RAR: **RAR naik MESKI tiga falsified** — availability membayar penyelesaian job, reputasi tidak jatuh. RAR bukan pengukur kualitas jawaban; ia pengukur penyelesaian job. Jangan membaca RAR 9 sebagai "aman untuk terus" — yang menipis adalah saldo, bukan RAR.

### 6.2 Runway — berapa klaim lagi sampai saldo habis

Dengan asumsi tiap klaim falsified (−1) dan tanpa payout masuk:

- Saldo 2,1212 → sesudah 2 falsified: **0,1212** → sesudah falsified ke-3: **−0,8788** (perilaku platform pada saldo negatif **tidak diketahui**; preseden tangga fee bertanya menunjukkan saldo mengikat pengeluaran — fee n=11 sebesar 3,1279 tertahan saat saldo 2,3897, §24.3).
- **Runway efektif pada verdict rate 0%: 2 klaim.** Itu seluruh anggaran uji §7 — bukan pilihan, melainkan aritmetika saldo.
- Jalur bertanya tidak bisa mengisi ulang saldo: tertutup di n=7 (fee n=8 net −0,3504 dan memburuk; bonus NIU terbukti $0 pada 7/7 settled + ≥23 verified — §24/§25.2). Satu-satunya pengisi saldo adalah jawaban yang menang slot.

### 6.3 Ambang impas — verdict rate berapa agar rezim net-positif

Model EV per klaim: `EV = v·s·P − (1−v)·1`, dengan v = verdict rate (verified), s = P(memenangi ≥1 slot | verified), P = payout per slot.

Parameter dari kohort §30 (bukan asumsi): 2.262 marathon wins terbayar / 858 pertanyaan (2,64/pertanyaan); 5.175 verified dari 18.056 jawaban. Maka s_marathon ≈ 2.262/5.175 ≈ **0,44**; slot Pioneer 858/5.175 ≈ 0,17 (tumpang-tindih dengan marathon tidak terukur; stacking **belum terbukti** — §25.1 — jadi s gabungan konservatif ≈ **0,5**). Payout campuran tertimbang (2.262×10 + 858×20)/3.120 ≈ **12,7**.

| Skenario | v | s | P | EV/klaim |
|---|---|---|---|---|
| Kita teramati (0/3) | 0% | — | — | **−1,00** |
| Impas bawah (marathon saja) | 18,5% | 0,44 | 10 | ≈ 0 |
| **Impas tengah** | **~15%** | 0,5 | 12,7 | **≈ 0** |
| Impas atas (semua Pioneer) | 9% | 0,5 | 20 | ≈ 0 |
| Median kohort eksternal | 32% | 0,5 | 12,7 | **+1,16** |
| Pemenang (median) | 55% | 0,5 | 12,7 | **+2,72** |

**Ambang impas ≈ 15% verdict rate** (rentang 9–19% tergantung campuran slot). Catatan jujur: ambang ini mengasumsikan jawaban verified kita mendapat peluang slot rata-rata kohort — yang mensyaratkan timing marathon yang benar (verified TERAKHIR sebelum jendela ±500 dtk tutup) dan sudut novelty ≥15%. Klaim kita masuk di viso median 5 (6, 5, 4) vs patokan kohort ±3 — kelas yang benar, tetapi belum ada bukti kita bisa memenangi slot.

**Risiko ruin pada titik impas:** pada EV ≈ 0 dengan langkah ±1 dan buffer 2,12, peluang kehabisan saldo sebelum berlipat masih tinggi (random walk; secara kasar >40%). Impas dalam ekspektasi ≠ aman. Itulah kenapa uji §7 memakai stop otomatis, bukan "lanjut sampai saldo habis".

### 6.4 Statistik kejujuran: apa yang sebenarnya dibuktikan 0/3

0/3 **tidak membuktikan** true rate kita di bawah 15%: P(0/3 | v=0,15) ≈ 0,61; P(0/3 | v=0,32) ≈ 0,31; P(0/3 | v=0,55) ≈ 0,09. Interval kepercayaan 95% untuk 0/3 membentang kira-kira 0–63%. Yang membuktikan rezim ini bermasalah **bukan** angka 0/3 — melainkan **tiga spesies gagal yang berbeda** (§1) + cacat proses draf-terkirim + Vyce mati 17 jam. Vonis ini bersandar pada mekanisme, bukan pada n=3.

---

## §7. Syarat minimum LANJUT BERSYARAT + rencana uji

Semua syarat **terukur dan bisa dicek** sebelum klaim berikutnya. Satu syarat tidak terpenuhi → vonis menjadi (a) TUTUP.

### 7.1 Syarat minimum (urutan perbaikan)

1. **Steering bermandat-URL di semua target antrean.** Setiap steering staged WAJIB memuat daftar sumber yang BOLEH dikutip (nama + URL persis, masing-masing diverifikasi HTTP 200 saat ditulis) + aturan penempatan (≥1 sitasi per seksi; tiap angka dalam kalimat yang sama dengan sitasinya). Larangan "jangan mengarang sitasi/URL" **tanpa** daftar yang diizinkan = DILARANG (penyebab deadlock §50.5, terbukti). Bukti cek: 2c7efc3e sudah direvisi (§50.7 — W3C VCDM v2.0 + EIP-5192, keduanya diverifikasi live); terapkan pola yang sama ke 1d3efb52, 5fbb2531, 1d758352, 26fe6c71, 530bed9e sebelum dipakai.
2. **Rubrik v2 diadopsi (QUALITY.md, bump bernomor).** Revisi §4.3 butir (b)/(c)/(d)/(e) + gerbang baru **(h) cakupan sub-pertanyaan (pintu mati)** + **(i) standar bukti empiris**. E1 dinyatakan **DIADOPSI** (ambang ≥2 kasus falsified terpenuhi ×3 — d9f49e11, 96c384fd, 66f46c3e) dan sub-cek (d) "sitasi harus mendukung angka spesifiknya (uji buka-dan-baca)" masuk sebagai bagian (d) v2. CHANGELOG mencatat bukti angka pemicu tiap perubahan (aturan penutup lab §32/§33).
3. **Audit draf-terkirim (menutup cacat proses).** Untuk klaim one-shot: sesudah submit, teks reveal ISO **segera** dinilai ulang lawan 4A + self-VFP + (h) + (i) dalam verdict watch; hasilnya ditulis ke VERDICT-LEDGER + MEKANISME. Bila teks terkirim gagal (h) atau (i), klaim berikutnya **diblokir** sampai steering diperbaiki — dan kegagalan itu dihitung sebagai kegagalan gerbang dalam uji §7.3. Untuk target Pioneer (viso-0): utamakan jalur serve §39 (PREPARE_CMD — draf yang digerbang = draf yang terkirim), sesudah satu smoke live berkata-kunci nyata dengan 0 job.
4. **Lane tunggal: Cloudflare/gpt-oss-120b.** Uji berjalan HANYA di lane ini (steering keras anti-E1 §37 viii aktif; neuron <9.000 — terpasang). Nemotron hanya fallback bila probe Cloudflare gagal DAN probe Nemotron kelas-klaim sendable. Vyce hanya bila satu probe lolos. DashScope pensiun 2026-11-12. Z.ai parkir. Gemini tetap dilarang.
5. **Perbaiki tabrakan LENGTH_SUFFIX.** Untuk target uji, pilih target yang pitanya selaras dengan suffix 5.500–7.500 kar (viso 4–5, pita baku) ATAU catat eksplisit di steering bahwa yang mengikat adalah lantai §45 + pintu (d)/(g), bukan presisi pita (§50.7). Jangan biarkan suffix dan pita bertabrakan diam-diam.
6. **Perbaiki alat diagnosis.** Provider mencetak rincian temuan saat withhold (breakdown severity wrong/bound-unverified/floor) di stderr — utang §50.5. Tanpa ini, probe berikutnya butuh generasi mentah + `wrap-file` offline untuk mendiagnosis diri sendiri.

### 7.2 Rencana uji berikutnya (konkret)

- **Target pertama: 2c7efc3e** (viso 8, marathonActive, steering SUDAH direvisi bermandat-URL §50.7; sudut baru terverifikasi lawan 8 verified). Lane: **Cloudflare**. Syarat: probe kelas-klaim sendable + 4A + self-VFP + sensus + (h)/(i) tercatat sebelum tembak.
- **Target kedua (bila klaim pertama verified): 1d3efb52** (viso 8, bonding curve — steering dibangun BARU di bawah aturan §7.1 butir 1–2) atau target viso 4–5 segar dari scan (e4641049 / 7597b4e9 / f66ab00f — §50 klaim uji butir 3) agar pita baku selaras suffix.
- **Tidak ada serve latar** selama uji (one-shot saja; serve §39 hanya untuk target Pioneer, sesudah smoke).
- **Verdict watch ±30 menit** per klaim (latensi median berjalan ±150 dtk) + audit draf-terkirim (§7.1 butir 3) sebelum klaim kedua.

### 7.3 Kriteria stop (dikunci di muka — otomatis, tanpa evaluasi ulang)

- **0/2 verified → TUTUP TOTAL (a).** Saldo tersisa 0,1212; akun dibekukan untuk klaim/serve; yang tersisa hanya scan ringan + drill (tanpa klaim) sampai user memutuskan lain. Tidak ada "satu klaim lagi untuk memastikan".
- **1 abandoned (job dropped / timeout liveness) → STOP hari itu + bedah; uji dianggap GAGAL bila abandoned berasal dari jalur one-shot (draf tertahan pasca-klaim, §35).** REL −3 tidak punya bantalan untuk satu pun abandoned.
- **Spesies gagal ke-4 (di luar A/B/C) pada salah satu klaim uji → STOP + bedah; kelanjutan butuh gerbang baru yang dinamai, bukan janji.**
- **Sukses (≥1 verified, idealnya +slot) → lanjut ke batch 5 klaim** di bawah tumpukan yang sama; evaluasi ulang di n=8 total klaim rezim: <2/8 verified → STOP + bedah isi (bukan tambah volume — R8); ≥2/8 → RAMP normal (4–10 kontes/hari) dengan gerbang yang sama.
- **Pemicu bangun-kembali bila (a) yang akhirnya berlaku:** Vyce pulih + probe lolos 2 jendela berturut-turut, ATAU satu lane baru lolos bench rubrik penuh (sendable ≥2/3 generasi kelas-klaim), ATAU platform membuka teks alasan verifier (menghapus batas penglihatan §5). Tanpa pemicu itu, (a) bersifat final.

### 7.4 Apa yang dilakukan dengan akun/saldo/steering bila akhirnya (a)

- **Akun:** Expert tetap dynamic/general, caps none — tidak ada perubahan config. Tidak ada penarikan/ekspor $TRUED (tidak ada jalurnya — §25.5). Saldo 0,1212–2,1212 dibiarkan sebagai sisa; jalur bertanya tetap tertutup (n≥8 net-negatif).
- **Saldo:** tidak ada aksi. $TRUED bukan uang yang bisa ditarik; nilainya hanya tiket lotre bila rezim hidup lagi lewat pemicu §7.3.
- **Steering:** semua steering staged + patch gelombang 1–2 disimpan sebagai bahan evaluasi (bukan untuk dipakai). Cron slot-hunt + day-close tetap berjalan sebagai **scan ringan + drill** (tanpa klaim/serve) sampai user memutuskan mematikan rutinitas — atau diubah ke mode itu oleh sesi utama bila (a) diputuskan.
- **Pembelajaran yang disimpan:** tumpukan gerbang (§45 + T12 + v2 + (h)/(i)), ledger verdict, dan evaluasi ini — semuanya tetap berlaku sebagai bahan bila platform atau lane berubah.

### 7.5 Yang TIDAK dilakukan dalam vonis ini

- Tidak ada perubahan cron (slot-hunt, day-close, weekly-revision) — perubahan badan cron adalah keputusan sesi utama bersama user.
- Tidak ada perubahan MEMORY.md.
- Tidak ada klaim/serve baru — uji §7.2 baru jalan sesudah sesi utama + user menyetujui syarat §7.1 terpenuhi.
- Tidak ada uang asli dipakai — seluruh lane $0/free; saldo Vyce promo tidak disentuh.

---

## §8. Tiga bukti terkuat (ringkasan untuk sesi utama)

1. **Tiga klaim, tiga spesies, nol pengulangan — dan lantai hanya membunuh satu.** #1 lolos semua lantai tapi mati di dukungan semantik (sitasi EIP-2028/4844 tidak memuat klaim dominasi L1 — BEDAH-TOTAL §2.1). #2 mati tanpa satu pun sitasi + fakta BSC salah (base fee 0, blok 0,45 dtk, 21.000 gas — BEDAH-KLAIM2 §2.2). #3 lolos semua lantai + 4A + self-VFP tapi tidak menjawab sub-pertanyaan (a) — nol aplikasi AI dinamai — dan tidak membawa satu pun bukti empiris (§50 klaim uji §8). Tidak ada satu perbaikan yang mengubah ketiganya (§1.5).
2. **Jendela 07:00 membuktikan deadlock lantai secara live: 5/5 draf ditahan, 0 temuan audit angka.** Steering "jangan mengarang URL" + lantai "wajib URL" = mustahil oleh konstruksi (§50.5). Satu-satunya jalan keluar yang terbukti hidup adalah steering menamai URL persis (klaim uji lolos lantai sesudah patch 07:14) — perbaikan yang harus diterapkan satu per satu ke semua steering antrean.
3. **Rubrik v1 buta terhadap pasangan yang menentukan.** Skor IDENTIK (L,G,G,G,L,L,L) untuk jawaban verified vs falsified di drill 07:00 (DRILL-LOG) — pembedanya hanya kebenaran angka. Sementara itu (b) ×3 dan (c) ×4 membuktikan dua butir rubrik lebih ketat dari selera verifier, dan (d) biner pernah gagal atas jawaban verified 4-support. Rubrik mengukur bentuk, bukan kebenaran — revisi v2 + gerbang (h)/(i) adalah prasyarat, bukan hiasan.

**Angka yang mengikat vonis:** saldo 2,1212 (runway 2 klaim pada rate 0%); ambang impas ≈15% verdict rate; median kohort 32%, pemenang 55%; Vyce mati 17 jam; Cloudflare satu-satunya lane yang menyelesaikan klaim uji; E1 ambang adopsi terpenuhi ×3 tanpa bump versi tercatat.

---

## Lampiran — daftar sumber per klaim faktual

- Saldo/LE/Expertise/RAR 07:30 11 Nov: MEKANISME §50.1.
- Verdict #1 (2/2, 263 dtk): VERDICT-LEDGER baris 1; BEDAH-TOTAL §1–2; MEKANISME §42.
- Verdict #2 (0/4, ±150 dtk): VERDICT-LEDGER baris 2; BEDAH-KLAIM2 §1–2; MEKANISME §44–46.
- Verdict #3 (0/1, ±135 dtk, panel 2): VERDICT-LEDGER baris 3; MEKANISME §50 (kedua entri) butir 7–8.
- Lantai §45 (definisi K-1/K-2, uji 30/30 offline): MEKANISME §45; T12.
- Deadlock lantai + 5/5 ditahan: MEKANISME §50.4–§50.5; DRILL-LOG entri bayangan 07:00 11 Nov.
- Rubrik buta + hitungan celah: DRILL-LOG (rekap §3.7 laporan ekstraksi); QUALITY.md (v1, E1/E2/E3, CHANGELOG).
- Kohort §30: median agen 32% (n=182), pemenang 55%; 2.262 marathon wins / 858 pertanyaan; viso median masuk 3.
- Ekonomi: §24–§25 (payout Pioneer +20 / Innovator +10 / Marathon +10; falsified −1 rangkap tiga; fee ask; NIU $0); §46 (day-close; janji STOP).
- Lane: §29.2/§29.4 (Gemini); §31 (Sonogami key dicabut); §34–35 (Nemotron); §37 (Cloudflare bench); §39 (serve pengganti); §40 (DashScope/Z.ai).
- Model verdict clean sheet + revisi ≥2 support: §42–§44; DRILL-LOG 21:00 10 Nov + 07:00 11 Nov; §43/L-01.
