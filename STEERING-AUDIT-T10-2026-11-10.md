# AUDIT STEERING STAGED vs STANDAR T10 — 2026-11-10 (±19:35 WIB)

Pemicu: aturan kerja §41 yang belum dikerjakan — "audit SEMUA file steering staged terhadap hardening terbaru sebelum klaim berikutnya" — dijalankan sebagai pekerjaan paralel atas perintah distribusi kerja user 2026-11-10 19:32 WIB.
Standar penilai: **ADDENDUM T10.2** (paket operator — gerbang self-VFP: sitasi harus MENDUKUNG klaimnya; klaim dominasi/komposisi bernama-rantai = Tier-1 wajib sitasi dokumen rantai itu sendiri; kuantifier absolut wajib hedge di titik klaim; kontras eksklusivitas wajib lolos cek counterexample) + **pengerasan §37 butir 4(viii)** (larangan keras ikatan 700 gas ↔ EIP-2929; runtime EIP-1167 = 45 byte; penutup wajib penanda kebaruan persis "Baru dalam jawaban ini" / "kontribusi baru") + pita panjang QUALITY.md (baku 4.500–8.000 kar; 10.000–12.000 hanya marathon ramai viso ≥5).
Sifat: READ-ONLY. Tidak ada file steering yang diubah — keluaran = vonis + daftar perbaikan.
Latar pembanding: BEDAH-TOTAL-2026-11-10.md (ISO fcb7b015 falsified; pembunuh = klaim Tier-1 bernama-rantai §2 diikat ke EIP-2028/EIP-4844 yang tidak memuat klaimnya — pola P1; sekunder P2 kuantifier absolut, P3 kontras CREATE2).

---

## 1. ENUMERASI — file ada / tidak ada

Folder: `~/workspace/research/dialectica/provider/steering/` — **5 file ada**.

| Target antrean (§41) | File steering | Status |
|---|---|---|
| 472b29a0 (primer) | ADA (4.136 B, staged 8 Nov) | diaudit di bawah |
| 71f472d6 (cadangan) | ADA (3.275 B, staged 8 Nov) | diaudit di bawah |
| c44f4399 | **TIDAK ADA** | belum pernah di-steering |
| 2c7efc3e | ADA (3.579 B, staged 10 Nov 02:46) | diaudit di bawah |
| 26fe6c71 | **TIDAK ADA** | belum pernah di-steering |
| 530bed9e | **TIDAK ADA** | belum pernah di-steering |
| da81169c | **TIDAK ADA** | belum pernah di-steering |
| 60fa9935 (sudah ditembak) | ADA (6.684 B, di-hardening 10 Nov 12:01) | diaudit di bawah — riwayat |

Di luar daftar antrean, ada 1 file tambahan: **fdf32ba4** (steering jawaban Binance Agentic Wallet / baw — 4.800 B, staged 8 Nov) — ikut diaudit.

**Temuan enumerasi:** 4 dari 7 target antrean yang belum ditembak (c44f4399, 26fe6c71, 530bed9e, da81169c) tidak punya steering sama sekali — antrean §41 sebagian adalah daftar target, bukan daftar steering siap. Klaim apa pun ke empat target itu butuh steering baru dari nol (ditulis langsung di bawah standar T10).

---

## 2. VONIS PER FILE

### 2.1 — 472b29a0 (Agent ID-gated free mints, BNB Chain; marathon, 5 verified) → **PERBAIKI**

Isi steering umumnya berdisiplin tinggi (perintah eksplisit: angka hanya dari catatan operator, sisanya klaim mekanisme, dilarang mengarang statistik/sitasi). Tidak ada pelanggaran ban keras §37 (tidak ada angka 700, tidak ada klaim EIP-1167). Tiga cacat:

1. **(T10.2-a — risiko tertinggi file ini) Klaim penopang berupa reportase catatan operator yang TIDAK bisa diuji-dukung verifier.** Angka 155.758 gas/klaim, ±0,09 gwei, ±0,000014 BNB, lonjakan ±9,75 gwei, pergerakan suplai 4.959 → 5.028, dan klaim §2 "owner bisa menarik seluruh sisa reserve sesuka hati (fungsi bergaya withdrawVolt)" + "5.000 token per klaim dari reserve di dalam kontrak" adalah klaim Tier-1 spesifik tanpa sumber bernama yang bisa dibuka verifier — bentuk strukturalnya sama dengan pembunuh fcb7b015 (klaim spesifik, dukungan tak terjangkau penguji). Perbaikan persis:
   - Bingkai setiap angka/catatan itu DI TITIK KLAIM sebagai reportase audit operator ("in the operator's own audit of one such contract the same evening, …"), bukan fakta telanjang — steering sekarang hanya membingkainya di paragraf penutup file, bukan memerintahkannya per klaim.
   - Ganti "a withdrawVolt-style function" → frasa generik "a reserve-withdrawal function" (nama fungsi dari kontrak tak bernama = presisi yang tidak bisa diverifikasi siapa pun).
   - Angka turunan "roughly 100x" lolos (9,75/0,09 ≈ 108×, dibulatkan jujur) — pertahankan kata "roughly".
2. **(§37 viii) Penutup TANPA penanda kebaruan persis.** Seksi 4 (kriteria sukses terukur) ditunjuk sebagai penutup, tapi steering tidak memerintahkan frasa "Baru dalam jawaban ini" / "kontribusi baru". Perbaikan: tambah perintah penutup wajib dibuka frasa persis itu.
3. **(QUALITY (c)) Tidak ada sasaran panjang sama sekali di file.** Perbaikan: tambah baris LENGTH — target marathon viso ≥5 → 10.000–12.000 kar; bila viso saat tembak <5 → pita baku 4.500–8.000 kar.

Kuantifier absolut: "on-chain indistinguishable from a Sybil farm" (§3) = penalaran mekanisme Tier-0, lolos. Tidak ada klaim dominasi bernama-rantai kelas P1 (BNB Chain adalah topik pertanyaan, bukan klaim komposisi biaya).

### 2.2 — 71f472d6 (program AI ritel; marathon, 4 verified) → **PERBAIKI (ringan)**

File paling bersih soal disiplin sitasi: perintah eksplisit "labeli setiap angka sebagai hipotesis perencanaan", "jangan mengarang sitasi/URL/DOI/statistik", "bila angka tak bisa disumberi persis, nyatakan mekanismenya tanpa angka". Hampir seluruh isi = Tier-0 (mekanisme + aturan preskriptif). Angka yang muncul adalah milik pertanyaan (20%) atau konstruk perencanaan ("dua siklus shadow+live", "bulan ke-25", "dua-tiga kuartal") — bukan statistik dunia. Tidak ada klaim bernama-rantai, tidak ada kuantifier absolut faktual tanpa penopang (klaim preskriptif "kill if…" adalah aturan yang diusulkan jawaban, bukan asersi fakta). Dua cacat saja:

1. **(§37 viii) Penutup (seksi 5, masalah bulan-25) tanpa perintah penanda kebaruan persis.** Tambah perintah frasa "Baru dalam jawaban ini" / "kontribusi baru" di penutup.
2. **(QUALITY (c)) Tidak ada sasaran panjang.** Tambah baris LENGTH sesuai kelas target saat tembak (baku 4.500–8.000; 10–12 rb hanya bila viso ≥5).

Sesudah dua tambahan administratif itu, file ini SIAP.

### 2.3 — 2c7efc3e (VC vs soulbound NFT; Pioneer viso 0) → **PERBAIKI (ringan)**

Isi = penalaran mekanisme Tier-0 yang kokoh + reportase praktik operator yang dibingkai eksplisit sebagai praktik ("operational fact from running issued agent identities daily"; penutup file: reportase hanya dari sumber yang bisa disebut persis). Deskripsi sifat VC (presentasi holder-controlled, selective disclosure, cek status/revokasi registri issuer) benar di level mekanisme model data VC; klaim soulbound di-hedge di titik yang tepat ("most soulbound designs do not"). Kontras VC-vs-soulbound bukan kontras eksklusivitas palsu kelas P3 — file justru memerintahkan rekomendasi hybrid dan kejujuran Sybil. Tiga perbaikan:

1. **(§37 viii) Tidak ada perintah penutup sintesis berpenanda kebaruan persis.** File berakhir di seksi 5 (Sybil) tanpa instruksi penutup. Tambah: penutup 2–3 kalimat dibuka frasa "Baru dalam jawaban ini:".
2. **(QUALITY (c)) Tidak ada sasaran panjang.** Tambah baris LENGTH (Pioneer viso 0 → pita baku 4.500–8.000 kar).
3. **(T10.2-a, penguat opsional tapi disarankan)** Bila draf menyebut sifat VC/soulbound sebagai reportase standar, sebut sumber persisnya — W3C Verifiable Credentials Data Model dan EIP-5192 (Minimal Soulbound NFTs) — agar klaim sifat tidak berdiri sebagai asersi tanpa nama. Steering sekarang melarang sitasi karangan tapi tidak menamai dua sumber yang memang ada dan relevan ini.

### 2.4 — fdf32ba4 (integrasi Binance Agentic Wallet; di luar antrean §41) → **PERBAIKI**

File berdisiplin sitasi eksplisit (seksi CITATION DISCIPLINE: hanya dua sumber bernama yang boleh disebut — paket npm `@binance/agentic-wallet` + distribusi binance-skills-hub; dilarang mengarang URL/DOI/versi di luar v1.12.0; klaim praktik operasional wajib dibingkai "in verified operational use"). Blok "VERIFIED FACTS" konsisten dengan catatan operasi kita sendiri (baw v1.12.0, sesi ganda via BINANCE_BAW_DIR, jendela verifikasi ±5 menit, contract-call dua fase preview→requestId, Developer Mode berbatas waktu). Tidak ada ban keras yang dilanggar. Tiga cacat:

1. **(§37 viii) Tidak ada penutup berpenanda kebaruan persis.** Struktur berakhir di "Security trade-offs summary" tanpa perintah menamai kebaruan dengan frasa penanda. Tambah perintah penutup "Baru dalam jawaban ini:".
2. **(QUALITY (c)) Sasaran panjang "roughly 6,000–10,000 characters" melanggar pita di ujung atas** kecuali targetnya marathon ramai viso ≥5 — viso target ini tidak tercatat di file. Perbaikan: persempit ke 4.500–8.000, atau catat viso target di file dan batasi 10.000 hanya bila viso ≥5 terbukti saat tembak.
3. **(T10.2-c, kecil) Kuantifier posisi pembuka "signing happens … after explicit user approval in the Binance app"** berdiri agak absolut di samping fakta file sendiri bahwa `baw sign-message` berjalan TANPA tap terpisah — ketegangan internal ini harus diurai di titik klaim (persetujuan berlaku untuk transaksi; penandatanganan pesan EIP-712 berjalan dalam sesi terpasang), supaya verifier tidak menangkapnya sebagai kontradiksi A_REASONING.

### 2.5 — 60fa9935 (EIP-1167 vs standalone; SUDAH DITEMBAK → FALSIFIED) → **BUANG (pensiunkan)**

Satu-satunya file yang memuat pengerasan §37 secara lengkap (HARD BANS eksplisit ✓, penutup dibuka frasa persis "Baru dalam jawaban ini:" ✓, sasaran panjang 6.000–12.000 untuk marathon viso 6 ✓) — dan tetap mati, karena cacatnya hidup di kelas yang §37 tidak menjangkau dan T10 baru lahir sesudahnya:

- **(T10.2-b — FAIL, pembunuh P1)** §2 steering memerintahkan klaim dominasi bernama-rantai ("On Arbitrum, Optimism and Base, deployment cost is dominated by L1 data cost") diikat ke EIP-2028 + EIP-4844. Kedua EIP itu nyata dan angkanya benar (EIP-2028: calldata 16 gas/byte non-nol; EIP-4844: blob) — tapi TIDAK SATU PUN memuat/memutuskan komposisi biaya deployment di rantai mana pun. Sitasi ada, dukungan tidak ada. Ini persis kegagalan yang dibedah di BEDAH-TOTAL §2.1 (P1).
- **(T10.2-c — FAIL, P2)** Kuantifier absolut "GROWS" / "nearly VANISHES" / "the exact opposite balance" diperintahkan tanpa hedge di titik klaim; hedge baru muncul di kalimat batas di ujung seksi.
- **(A_REASONING — P3)** §3 memerintahkan kontras eksklusivitas CREATE2 ("deterministic cross-chain addresses that standalone deployments cannot match without extra coordination") — dikotomi palsu: standalone via CREATE2 mencapai determinisme yang sama; pabrik clone pun mensyaratkan alamat pabrik identik lintas rantai (koordinasi yang sama).
- **(P4, sekunder)** §1 membingkai beacon proxy sebagai "anggota kedua keluarga minimal-proxy" yang membaca alamat "at the ERC-1967 beacon slot on every call" — pembingkaian kategori longgar (BeaconProxy bukan stub 45-byte; EIP-1967 menstandardisasi slot, bukan keluarga proxy).

Vonis BUANG: targetnya sendiri sudah settled dan klaimnya sudah dieksekusi (falsified 19:07:55 WIB) — tidak ada tembakan berikutnya dari file ini. Bila ISR sejenis dibuka lagi, steering-nya wajib ditulis ulang dari nol di bawah T10 (khususnya: klaim repricing L2 diturunkan ke Tier-0 tanpa nama rantai, atau diikat ke dokumentasi fee rantai itu sendiri), BUKAN ditambal. File dipertahankan di folder sebagai bukti audit, tidak dipakai lagi.

---

## 3. RINGKASAN VONIS

| File | Vonis | Cacat utama |
|---|---|---|
| 472b29a0 | PERBAIKI | reportase operator tak teruji-dukung sebagai klaim penopang; tanpa penanda penutup; tanpa LENGTH |
| 71f472d6 | PERBAIKI (ringan) | tanpa penanda penutup; tanpa LENGTH |
| 2c7efc3e | PERBAIKI (ringan) | tanpa penanda penutup; tanpa LENGTH; sumber standar tak dinamai |
| fdf32ba4 | PERBAIKI | tanpa penanda penutup; pita panjang 6–10 rb tak bersyarat viso; ketegangan approval-vs-sign-message |
| 60fa9935 | **BUANG** | T10.2-b FAIL (pembunuh P1) + P2 + P3; target settled, klaim sudah falsified |

**Nol file berstatus SIAP apa adanya.** Empat file bisa naik SIAP dengan perbaikan terbatas di atas (tidak ada fondasi yang cacat di keempatnya); satu file pensiun.

## 4. TIGA POLA TERPENTING

1. **Pengerasan §37 hanya pernah diterapkan ke SATU file — yang ditembak.** Semua steering lain yang staged (8 Nov) mendahului §37 viii: 4 dari 5 file tidak memuat penanda penutup persis, dan 3 dari 5 tidak punya sasaran panjang sama sekali. Tanpa audit ini, klaim berikutnya dari antrean akan jalan dengan steering pra-hardening — persis celah prosedural yang §41 butir 9 sudah peringatkan ("audit SEMUA file steering staged sebelum klaim berikutnya") tapi belum pernah dikerjakan sampai malam ini.
2. **File yang paling ter-hardening justru yang mati — kelas cacat penentunya berada DI LUAR daftar cek lama.** 60fa9935 lolos semua ban §37 (45 byte benar, tak ada ikatan 700↔EIP-2929, penanda penutup persis) tapi membawa klaim Tier-1 bernama-rantai yang sitasinya tidak mendukung. Disiplin lama semua file berbentuk "jangan mengarang" (kehadiran/keaslian sitasi); belum ada satu pun file yang diperintah/diaudit dengan uji DUKUNGAN (buka-dan-baca). T10.2 menutup kelas ini — dan audit ini adalah penerapan pertamanya ke seluruh antrean.
3. **Risiko sisa terbesar di antrean yang belum ditembak BUKAN di file yang paling longgar, tapi di 472b29a0** — target primer berikutnya. Sudutnya (akuntansi forensik dari catatan operator) memang baru dan kuat, tapi klaim penopangnya adalah angka + fakta kontrak dari catatan internal yang tidak bisa dibuka verifier mana pun; bentuk strukturalnya identik dengan §2 jawaban yang falsified (spesifik di permukaan, tak terjangkau di dukungan). Sebaliknya 71f472d6 dan 2c7efc3e hampir murni Tier-0 — permukaan refutasinya kecil bawaan desain. Urutan tembak sesudah jeda dicabut sebaiknya menimbang ini: perbaiki-dan-uji-dukung 472b29a0 dulu, atau dahulukan target berpermukaan Tier-1 terkecil sesuai syarat klaim pertama pasca-jeda (usul bedah #10).
