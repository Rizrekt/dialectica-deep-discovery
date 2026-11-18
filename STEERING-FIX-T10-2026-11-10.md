# PERBAIKAN STEERING PASCA-AUDIT T10 — 2026-11-10 (±19:4x WIB)

Pelaksana: pekerjaan paralel (distribusi kerja user 2026-11-10 19:34). Sumber perbaikan yang diikuti persis: **STEERING-AUDIT-T10-2026-11-10.md** (vonis + daftar perbaikan per baris-klaim) + standar **ADDENDUM T10.2** (paket operator) + **QUALITY.md** butir (c)/(d)/(e). Lingkup: hanya 4 file bervonis PERBAIKI. **60fa9935 TIDAK disentuh** (vonis BUANG — pensiun; file dipertahankan sebagai bukti audit). Tidak ada steering baru dibuat untuk target tanpa file (c44f4399/26fe6c71/530bed9e/da81169c — di luar lingkup). Tidak ada klaim/serve/ask/ubah config dalam pekerjaan ini.

Metode nilai-ulang: tiap file yang diperbaiki dibaca kembali utuh / disapu grep (angka catatan operator, ikatan terlarang 700↔EIP-2929, runtime EIP-1167, penanda penutup, LENGTH) lalu dinilai butir-per-butir lawan checklist T10.2: (1) klasifikasi Tier-0/Tier-1 tiap klaim spesifik; (2) sitasi mendukung klaimnya; (3) nol klaim dominasi bernama-rantai tanpa dokumen rantainya; (4) kuantifier absolut ter-hedge di titik klaim; (5) nol ikatan terlarang; (6) penanda penutup persis ada; (7) LENGTH ada.

---

## 1. 71f472d6 — PERBAIKI (ringan) → **SIAP**

**Perbaikan yang diterapkan (persis daftar audit §2.2):**
1. Blok **CLOSING MARKER (mandatory)** ditambahkan: sintesis penutup 2–3 kalimat wajib dibuka frasa persis "Baru dalam jawaban ini:" dan menamai kebaruan (spine integritas program di bawah insentif adversarial) — menutup cacat §37 viii (penutup lama = seksi bulan-25 tanpa penanda).
2. Baris **LENGTH** ditambahkan: 4.500–8.000 kar; pita 10.000–12.000 hanya bila viso ≥5 saat tembak — menutup cacat QUALITY (c).

**Skor checklist T10.2:** (1) Tier — hampir seluruh isi Tier-0 (mekanisme + aturan preskriptif usulan jawaban); angka 20% = milik pertanyaan; konstruk perencanaan wajib dilabeli hipotesis perencanaan di file. LOLOS. (2) Sitasi — tidak ada sitasi diklaim; larangan mengarang eksplisit. LOLOS. (3) Dominasi bernama-rantai — tidak ada. LOLOS. (4) Kuantifier — tidak ada asersi faktual absolut; "kill if…" adalah aturan yang diusulkan jawaban, bukan klaim fakta. LOLOS. (5) Ikatan terlarang — tidak ada. LOLOS. (6) Penanda penutup — ADA. LOLOS. (7) LENGTH — ADA. LOLOS.
**Vonis akhir: SIAP.**

## 2. 2c7efc3e — PERBAIKI (ringan) → **SIAP**

**Perbaikan yang diterapkan (persis daftar audit §2.3):**
1. Blok **CLOSING MARKER (mandatory)** ditambahkan di akhir file: sintesis 2–3 kalimat dibuka frasa persis "Baru dalam jawaban ini:" menamai kebaruan (pemisahan instrumen waktu-bayar vs jangkar publik, dari praktik operasi) — file lama berakhir di seksi Sybil tanpa instruksi penutup.
2. Baris **LENGTH** ditambahkan: 4.500–8.000 kar (Pioneer viso 0 — pita baku).
3. **Penamaan standar di titik reportase:** §1 kini menamai **W3C Verifiable Credentials Data Model** di klaim sifat VC (presentasi holder-controlled, selective disclosure, cek status/revokasi) dan **EIP-5192 (Minimal Soulbound NFTs)** di klaim sifat soulbound; paragraf disiplin akhir mengulang kewajiban menamai kedua sumber itu bila sifat dinyatakan sebagai reportase standar.

**Skor checklist T10.2:** (1) Tier — penalaran mekanisme Tier-0 kokoh + praktik operator dibingkai eksplisit sebagai praktik. LOLOS. (2) Sitasi — dua sumber yang dinamai adalah dokumen yang memang mengatur sifat yang diklaim (model data VC; antarmuka soulbound EIP-5192): kehadiran DAN dukungan kini sejajar. LOLOS. (3) Dominasi/eksklusivitas — kontras VC-vs-soulbound bukan dikotomi palsu; file memerintahkan rekomendasi hybrid (lolos cek counterexample). LOLOS. (4) Kuantifier — "most soulbound designs do not" ter-hedge di titik klaim. LOLOS. (5) Ikatan terlarang — tidak ada. LOLOS. (6) Penanda — ADA. LOLOS. (7) LENGTH — ADA. LOLOS.
**Vonis akhir: SIAP.**

## 3. fdf32ba4 — PERBAIKI → **SIAP**

**Perbaikan yang diterapkan (persis daftar audit §2.4):**
1. Blok **CLOSING MARKER (mandatory)** ditambahkan: sintesis sesudah ringkasan trade-off dibuka frasa persis "Baru dalam jawaban ini:" menamai kebaruan (KETIADAAN material kunci di sisi agen, bukan isolasi enclave-vs-file).
2. **LENGTH dibuat bersyarat viso:** pita lama "roughly 6,000–10,000" diganti di paragraf FORMAT menjadi baku **4.500–8.000**; pita 10.000–12.000 hanya bila viso target ≥5 saat tembak — dengan perintah eksplisit memverifikasi viso saat tembak (viso tidak tercatat di file) dan default ke pita baku bila ragu.
3. **Ketegangan approval-vs-sign-message diurai di titik klaim (POSITION):** klaim persetujuan kini dibatasi eksplisit ke TRANSAKSI ("TRANSACTION signing … after explicit user approval"), dan `baw sign-message` dinyatakan di kalimat yang sama sebagai pengecualian by-design (menandatangani EIP-712 di bawah sesi terpasang, TANPA tap terpisah) — persetujuan mengatur transaksi, sesi terpasang adalah otoritas berdiri untuk pesan. Konsisten dengan blok VERIFIED FACTS file sendiri dan daftar risiko session-token di struktur §3 (A_REASONING bersih).

**Skor checklist T10.2:** (1) Tier/reportase — klaim reportase dibatasi dua sumber bernama yang boleh disebut (paket npm `@binance/agentic-wallet` + distribusi binance-skills-hub); praktik operasional dibingkai "in verified operational use". LOLOS. (2) Sitasi mendukung — tidak ada klaim yang diikat ke sumber yang tidak memuatnya. LOLOS. (3) Dominasi bernama-rantai — tidak ada. LOLOS. (4) Kuantifier — klaim approval tidak lagi absolut (ter-scope di titik klaim). LOLOS. (5) Ikatan terlarang — tidak ada. LOLOS. (6) Penanda — ADA. LOLOS. (7) LENGTH — ADA (bentuk bersyarat viso di paragraf FORMAT). LOLOS.
**Vonis akhir: SIAP.**

## 4. 472b29a0 — PERBAIKI (BERAT, target primer antrean) → **SIAP di level steering; lolos uji-dukung penuh untuk klaim penopang; risiko sisa = generatif (di bawah)**

**Perbaikan yang diterapkan:**
1. **Semua klaim penopang berbasis catatan operator DITURUNKAN ke sintesis Tier-0 tanpa angka / dibuang** (mengikuti instruksi tugas yang lebih ketat dari opsi pembingkaian audit §2.1): angka gas 155.758, ±0,09 gwei, ±0,000014 BNB, lonjakan ±9,75 gwei dan turunan "roughly 100x", gerakan suplai 4.959 → 5.028, jumlah 5.000 token per klaim, ambang 11.000 shares, dan nama fungsi "withdrawVolt-style" — SEMUA hilang dari file (sapu grep pasca-tulis: bersih).
2. **§1 ditulis ulang sebagai penalaran mekanisme Tier-0 yang tetap baru:** akuntansi forensik klaim sebagai latihan yang bisa di-replay verifier mana pun dari data rantai publik — (a) "free" = klaim harga, bukan biaya: biaya diskalakan satu-banding-satu oleh rumus fee terhadap harga gas jendela (angka persis jendela mana pun terdecidable dari receipts-nya: gas used × effective gas price); (b) attempt revert tetap membakar gas — biaya riil yang tidak pernah dibukukan pemasaran harga-nol, terlihat di receipts yang sama; (c) tranche terbatas FCFS terkuras dalam ledakan terkonsentrasi di buka jendela — ukur dari perubahan state antar-blok, bukan dari klaim proyek; (d) clustering common-funder di graf pendanaan = tempat deteksi bot sesungguhnya, forensik sesudah fakta. Sudut ini tetap wilayah yang tidak dimasuki 5 jawaban verified (mereka berhenti di level desain) — kebaruan ≥15% dipertahankan TANPA penopang privat.
3. **§2 ditulis ulang sebagai prosedur terdecidable, bukan asersi tentang kontrak tertentu:** enumerasi kuasa owner atas reserve reward (jalur withdraw/rescue/sweep apa pun = hak yang belum diklaim revocable secara substansi; terdecidable dengan membaca fungsi mana yang bisa menggerakkan reserve dan siapa yang boleh memanggilnya) + aset terkunci sampai ambang penyelesaian yang mungkin tak pernah tercapai (saldo terbaca penuh, nilai terealisasi nol). Nama fungsi generik; nol internal kontrak spesifik yang tidak bisa ditunjuk ke verifier.
4. **Paragraf disiplin akhir diganti aturan keras "NO FIGURES FROM OPERATOR RECORDS"** — melarang memasukkan kembali angka/catatan privat sebagai klaim penopang dalam bentuk apa pun, dan melarang menamai fungsi/kontrak/wallet/proyek/orang dari catatan operator.
5. Blok **CLOSING MARKER (mandatory)** ditambahkan: sintesis dibuka frasa persis "Baru dalam jawaban ini:" menamai kebaruan (akuntansi klaim replayable dari data publik + audit sisi-reserve sebagai separuh lain gated mint).
6. Baris **LENGTH** ditambahkan: target marathon — 10.000–12.000 kar bila viso ≥5 saat tembak; viso <5 → pita baku 4.500–8.000 kar.
7. Baris pembingkai jawaban ("built on measured evidence…") diganti: dibangun di atas claim accounting yang replayable publik; "NO figure from any private record may carry the argument."
§3 (multi-identitas tersanksi) dan §4 (kriteria sukses terukur dari graf transfer) tidak berubah isi — keduanya sudah Tier-0 menurut audit.

**Skor checklist T10.2:** (1) Tier — nol klaim penopang Tier-1 berbasis catatan privat tersisa; §1 metode+mekanisme, §2 prosedur-cek, §3 mekanisme, §4 kriteria dari data publik. LOLOS. (2) Sitasi — tidak ada sitasi diklaim, jadi tidak ada sitasi yang gagal mendukung; larangan mengarang + aturan NO FIGURES eksplisit. LOLOS. (3) Dominasi bernama-rantai — tidak ada (BNB Chain = topik pertanyaan, bukan klaim komposisi biaya; pola P1 tidak berulang). LOLOS. (4) Kuantifier — "on-chain indistinguishable from a Sybil farm" (§3) = penalaran mekanisme Tier-0 (audit menilai lolos); "costs a large multiple" (§1a) = turunan aritmetika rumus fee (skala 1:1 dengan harga gas), bukan statistik dunia. LOLOS. (5) Ikatan terlarang — file tidak menyebut 700/EIP-2929/EIP-1167 sama sekali. LOLOS. (6) Penanda — ADA. LOLOS. (7) LENGTH — ADA. LOLOS.
**Vonis akhir: SIAP (level steering).**

**Risiko sisa 472b29a0 — dinyatakan persis:**
- **(R1 — generatif, risiko utama yang tersisa)** Steering sekarang bersih, tetapi model penyusun draf saat tembak masih bisa tergoda memasukkan kembali angka "ilustratif" dari pengetahuannya sendiri. Ini TIDAK bisa dihilangkan di level steering; mitigasinya = aturan keras NO FIGURES di file ini + gerbang self-VFP saat tembak (butir 4A badan hunt) yang wajib menolak draf berangka-tak-terdukung. Vonis SIAP berlaku untuk file steering, bukan untuk draf masa depan.
- **(R2 — kecil)** §3 memuat contoh praktik operator yang dibingkai generik (satu operator menjalankan dua identitas terbitan, mis. miliknya + milik anggota keluarga yang ia operasikan). Audit menilai bentuk ini lolos sebagai penalaran mekanisme (identitas mengikat akun, bukan manusia) dan tidak ada spesifik yang bisa dibantah (tanpa nama, angka, atau klaim terukur) — risiko refutasi dinilai rendah, bukan nol, bila verifier membacanya sebagai reportase. Dibiarkan karena ia adalah penopang sudut §3; membuangnya akan membuang poin yang sah secara mekanisme.

---

## RINGKASAN

| File | Vonis audit | Vonis akhir | Catatan |
|---|---|---|---|
| 71f472d6 | PERBAIKI (ringan) | **SIAP** | penanda + LENGTH |
| 2c7efc3e | PERBAIKI (ringan) | **SIAP** | penanda + LENGTH + W3C VC DM & EIP-5192 dinamai |
| fdf32ba4 | PERBAIKI | **SIAP** | penanda + LENGTH bersyarat viso + ketegangan approval/sign-message terurai |
| 472b29a0 | PERBAIKI (berat) | **SIAP (level steering)** | seluruh penopang catatan operator turun Tier-0/dibuang; §1–§2 ditulis ulang sebagai mekanisme; sisa risiko = generatif (R1) + contoh §3 (R2) |
| 60fa9935 | BUANG | tidak disentuh | pensiun; dipertahankan sebagai bukti audit |

Antrean pasca-perbaikan: 4 steering SIAP menunggu pencabutan jeda (kill-metric ii) + gerbang self-VFP saat tembak. Usul urutan tembak tetap mengikuti audit §4 butir 3 (permukaan Tier-1 terkecil lebih dulu) — keputusan sesi utama.
