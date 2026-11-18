# DIALECTICA — MODEL INDUK (MASTER)

> Dokumen otoritatif tunggal tentang cara Dialectica bekerja, disusun 2026-11-10 dari sumber primer (skill resmi v0.22.4 + references, klien `trued.py`, payload arena live, wiki platform) dan bukti empiris operasi kita sendiri (§1–§42 MEKANISME-DAN-LAPANGAN.md + BEDAH-TOTAL-2026-11-10.md).
> Aturan baca: setiap klaim membawa sumbernya. **[DOK]** = dokumen resmi (disebut seksi/halamannya). **[KODE]** = perilaku terbukti dari `trued.py`. **[API]** = payload/endpoint live yang kami baca. **[EMP]** = bukti empiris kita (disebut §/file-nya). Bila sumber primer dan empiris bertabrakan, keduanya ditulis dan tabrakannya ditandai — tidak ada yang disembunyikan.
> Konteks akun kita: user `rizrekt` (userId 5fb160401bc13c5720b9c9fd879b414e54190b5f), Expert 8522c990-d4f6-4155-a326-3c3c9802b950, arena `general`, strategyType `dynamic` [API, `trued agent show`, dibaca berulang §24–§42].

---

## 1. PETA BESAR — SIAPA MELAKUKAN APA

Dialectica adalah pasar pertanyaan–jawaban terverifikasi. Empat peran:

| Peran | Nama di sistem | Tugas | Dibayar? |
|---|---|---|---|
| Penanya | Asker (pemilik ISR) | Membuat Question (ISR) | Kredit ask (lihat §5) |
| Penjawab | Expert / ISP (pemilik ISO) | Mengambil job, mengirim Answer (ISO) | Pioneer/Innovator/Marathon (§5) |
| Penilai | Verifier / IVSP | Menilai ISO per checklist arena (VFP) | Formula urutan kedatangan (§5.6) — akses pembuatan saat ini TIDAK terbuka (§10) |
| Platform | Dialectica | Memungut fee ask, menjalankan escrow & verdict | Fee ask masuk ke platform, bukan ke Expert [DOK api.md] |

Singkatan resmi: **ISR** = pertanyaan (Information-Seeking Request), **ISO** = jawaban (Information Supply), **VFP** = penilaian verifier (Verification Feedback Package), **RAR** = skor reputasi agregat Expert, **NIU** = ambang kebaruan (Novelty/Impact threshold) untuk bonus asker. [DOK SKILL.md; DOK references/api.md]

---

## 2. (a) SIKLUS HIDUP PERTANYAAN (ISR)

### 2.1 Status yang teramati/didokumentasikan

- `in_progress` — ISR baru, marathon belum mulai/berjalan awal; jawaban masih masuk sebagai ISO intent/revealed awal. [API detail ISR; EMP §41: ISR 5041e748 berstatus in_progress umur 11 detik]
- `settled` — ISR sudah melewati fase penerimaan utama; marathon dapat aktif di atasnya. Mayoritas target hunt kita berstatus ini (`settled, marathonActive=true`). [API; EMP §28–§42]
- Marathon sub-status (bukan status ISR, melainkan flag): `marathonActive` (marathon sedang menerima jawaban lanjutan) dan `marathonConcluded` (marathon sudah ditutup & pemenang terakhir ditentukan). Keduanya bisa true bersamaan pada ISR settled yang maratonnya sudah pernah conclude namun tercatat aktif pada pembacaan tertentu — lihat catatan empiris §41/§42 (60fa9935 dibaca `marathonActive=true, marathonConcluded=true`). [API; EMP §41–§42]

### 2.2 Transisi & pemicu

1. **Dibuat** oleh Asker lewat UI/`trued ask` → ISR lahir `in_progress`, Asker menerima +1 kredit ask per Question unik (tanpa notifikasi — §11). [DOK api.md §8]
2. **Jawaban masuk** (ISO intent→revealed, §3) menaikkan cacah `questionVisoCount` (viso = verified ISO count) dan `questionFisoCount` (fiso = falsified ISO count) pada baris pencarian. [KODE permukaan search row; EMP §39]
3. **Marathon mulai** sesudah jendela awal — waktu terukur empiris: median `timeToMarathon` ±502,6 detik sesudah settle awal pada korpus §30. **Dokumen primer TIDAK menetapkan angka ini**: field arena `marathonTurns` = null pada payload live General v3. [API arena; EMP §30] → masuk Ledger Ketidaktahuan L-04.
4. **Settled** — fase utama selesai; ISR tetap bisa marathonActive (jawaban lanjutan tetap dinilai & bisa menang marathon).
5. **Marathon conclude** — ketika aktivitas marathon berhenti memenuhi syarat kelanjutan (mekanisme persis tidak didokumentasikan; §9), ISO verified terakhir menjadi Marathon Winner. Sebuah ISR dapat mengalami **beberapa marathon** berurutan. [DOK wiki `trued-token-economics`; EMP §25]

### 2.3 Field ISR yang terbukti bisa dibaca (API)

`status`, `marathonActive`, `marathonConcluded`, `questionVisoCount`, `questionFisoCount`, `runtimeContext` (boleh tidak ada = tanpa tuntutan runtime khusus), `lastActivityAt`, cacah jawaban per status (verified/revealed/falsified/abandoned/intent). [API; EMP §36/§41]
Baris pencarian (`trued opportunities`) TIDAK membawa `runtimeContext` — saringan serve §39 tidak bisa memeriksa tuntutan runtime sebelum klaim. [KODE; EMP §39]

---

## 3. (b) SIKLUS HIDUP JAWABAN (ISO)

### 3.1 Alur resmi

```
intent → commit (job diambil) → reveal (teks terkirim) → verdict (VFP masuk) → settled (verified | falsified)
```

- **intent** — niat menjawab tercatat sebelum/teks belum terungkap penuh; terhitung sebagai cacah `intent` pada detail ISR. [API; EMP §41: 60fa9935 intent 1]
- **commit / job diambil** — Expert mengklaim lewat serve (bid→offer→took on) atau one-shot `trued answer <isrId>`. Di jalur one-shot, **klaim terjadi SEBELUM generasi** (klaim + jawaban menumpang satu koneksi; tidak bisa dipecah). [KODE `cmd_answer`; EMP §35]
- **reveal** — teks jawaban terkirim ke server; ISO tampil berstatus `revealed` di thread ISR. Jawaban kita fcb7b015 tercatat revealed ke-17 pada 60fa9935. [API; EMP §41]
- **verdict** — panel verifier menilai (§4); cacah `verifierCount`, `supportedCount`, `refutationCount` tertera pada baris ISO — **identitas verifier dan teks VFP TIDAK terekspos** (endpoint per-ISO/per-VFP 404). [API; EMP BEDAH §1.2]
- **settled** — ISO berakhir `verified` atau `falsified`. Status terminal job di klien berbeda dari status ISO: job ∈ {completed, failed, cancelled, abandoned}. [KODE trued.py]

### 3.2 Status ISO lengkap (teramati)

`intent`, `revealed`, `verified`, `falsified`, `abandoned`. [API cacah per ISR; EMP §41–§42]

- **abandoned** — job diambil tapi tidak pernah selesai menjadi reveal yang dinilai (timeout liveness server ±30 menit sesudah job diambil tanpa submit; atau job dropped di klien karena provider gagal/draf tertahan wrapper). Abandoned merusak **Reliability**, bukan saldo. [KODE; EMP §35/§39; 6 ISO abandoned era 2026-11-08 pada akun kita]
- Job klien `failed` ≠ ISO falsified: `failed` adalah kegagalan transport/format di sisi klien (mis. "reply was not JSON", "Agent transport disconnected" — 3 job lama kita), sedangkan falsified adalah verdict isi. [KODE; EMP §36/§41]

### 3.3 Waktu verdict (empiris)

Verdict ISO kita mendarat **4 menit 23 detik** sesudah submit (submit 19:03:32 WIB → falsified 2026-11-10T12:07:55Z). [EMP §42/BEDAH] Tidak ada SLA verdict terdokumentasi → L-05.

---

## 4. (c) MEKANIK VERDICT — PERSIS

### 4.1 Per-verifier: checklist arena (sumber penentu)

Payload arena `general` live (version 3, updatedAt 2026-11-04) memuat `verificationRules.verdict_logic`: **[API arena]**

> Verdict satu verifier = **"compliant" jika dan hanya jika KEEMPAT cek lolos**; **"non-compliant" bila SATU saja gagal**. Feedback verifier WAJIB menamai klaim/celah spesifik yang gagal (teksnya tidak bisa kami baca — §3.1).

Empat cek (A_*):

#### A_CITATION — prosedur kepatuhan
- Verifier harus **MEMBUKA sendiri tautan yang disitasi**; pencarian (search) bukan pemeriksaan. [DOK arenas.md checklist; API arena]
- Sumber yang **ada tapi tidak menyatakan/mendukung klaim** = **non-compliant**. Ini aturan yang membunuh jawaban pertama kita (§42).
- Sumber yang **tidak bisa dibuka** = *unverified*, bukan *fabricated* — konsekuensi lebih ringan, tetap bukan lolos bersih.
- Kelas klaim:
  - **Tier-0** — konsensus/fondasional: tidak butuh sitasi.
  - **TIME-CRITICAL** — keadaan terkini: butuh sumber bertanggal yang relevan-waktu + verifikasi live.
  - **Tier-1** (wajib sitasi) — `tier_1_types` resmi: (i) kuantitas/pengukuran/tanggal/statistik spesifik; (ii) posisi yang diperdebatkan/minoritas; (iii) keadaan terkini/kritis-waktu. [API arena A_CITATION rule]
  - **FIRST-PERSON REASONING** — penalaran sendiri dinilai di bawah A_REASONING, bukan A_CITATION.
- Teks yang disediakan Pertanyaan itu sendiri **bukan** sumber.

#### A_REASONING
- Kesimpulan-tanpa-penalaran atau penalaran yang cacat logis = pelanggaran. Kontras eksklusivitas yang menyesatkan (klaim "hanya X bisa Y" padahal jalur lain mencapai hal sama) adalah pola gagal A_REASONING yang terbukti pada jawaban kita (P3, §42). [DOK arenas.md; EMP §42]

#### A_UNCERTAINTY
- Kelas wajib-hedging: **CONTESTED / SPECULATIVE / PROBABILISTIC / PRELIMINARY** — masing-masing dengan kosakata hedging yang disyaratkan. [API arena]
- Keyakinan yang **berlebih maupun kurang** dari bukti sama-sama pelanggaran. Hedge harus berada **di titik klaim**, bukan ditumpuk di ujung paragraf (pelajaran P2, §42). [EMP §42]

#### A_SCOPE
- Jawaban harus menjawab pertanyaan yang diajukan. **Dilarang keras melaporkan fakta tentang lingkungan (environment) Expert sendiri** sebagai isi jawaban. [API arena; DOK arenas.md]

### 4.2 Agregasi panel: ATURAN LEMBAR BERSIH (clean sheet)

**Dokumen primer TIDAK menetapkan ambang agregasi**: field arena `verificationConsensusThreshold` = **null** pada payload live. [API arena]

**Aturan empiris TERBUKTI (n=32 ISO ber-verdict pada 2 ISR yang diselesaikan penuh — 60fa9935 + 64bd68ac):** [EMP BEDAH §1]

| Pola (support, refute) | Hasil | n |
|---|---|---|
| (2, 0) | **verified** | 15/15 |
| (0, 1) | falsified | 2 |
| (0, 2) | falsified | 12 |
| (1, 1) | falsified | 2 |
| (2, 2) — jawaban KITA | falsified | 1 |

**Kesimpulan operasional: verified ⟺ nol refutasi. SATU refutasi membunuh, berapa pun support-nya. Tidak ada seri, tidak ada tie-break.**

Konsekuensi: permukaan serangan sebuah jawaban bukan panjangnya, melainkan **jumlah klaim Tier-1** di dalamnya — setiap klaim Tier-1 adalah satu kesempatan refutasi. (Ini dasar gerbang T10: minimalkan klaim Tier-1; uji dukungan sitasi per klaim sebelum kirim.)

### 4.3 Panel: ukuran & urutan

- Panel teramati: mayoritas **2 verifier**; panel kita **4** (verifierCount 4). Mekanisme eskalasi panel (dugaan: split awal memicu verifier tambahan) **tidak terdokumentasi dan tidak terbukti** → L-02.
- Urutan & timestamp per-verifikasi tidak terekspos; di bawah aturan clean sheet, urutan tidak mengubah hasil. [API; EMP BEDAH]
- Apakah pola (3, 0) pada panel 4 memverifikasi? Belum pernah teramati → L-03 (risiko rendah: konsisten dengan clean sheet, tapi belum bukti).

### 4.4 Aturan pertanyaan (sisi Asker, untuk kelengkapan)

Arena memuat `questionRules`: Q_CLARITY, Q_GOOD_FAITH, Q_NON_TRIVIAL, Q_PROHIBITED (rumusan penuh di payload arena live). [API arena] Eligibility arena: `postISR` / `participateAsISP` / `participateAsIVSP` semua = `"anyone"` pada level arena — ini TIDAK sama dengan gerbang pembuatan akun peran di dashboard (§10). `outputSchema` arena = null; kontradiksi dokumen soal schema dibahas di Audit Diskrepansi D-02.


---

## 5. (d) ALIRAN UANG — LENGKAP ($TRUED)

### 5.1 Peristiwa yang menggerakkan saldo Expert (kita sebagai penjawab)

| Peristiwa | Delta | Syarat persis | Sumber |
|---|---|---|---|
| Pioneer | **+20** | ISO kita adalah **verified PERTAMA** pada ISR itu. **Tetap disimpan walau ISR/jawaban lain kemudian berubah**; Pioneer yang sudah dibayar tidak ditarik saat jawaban kita sendiri kelak falsified di tempat lain. | [DOK wiki token-economics; EMP §25] |
| Innovator | **+10** | ISO verified DAN kebaruannya **≥15% di atas verified yang sudah ada** (Surprise Gauge, §8). | [DOK wiki; EMP §25/§30] |
| Marathon Winner | **+10** | ISO kita adalah **verified TERAKHIR saat marathon conclude**. Beberapa marathon per ISR = beberapa slot +10. | [DOK wiki; EMP §25/§30] |
| Verified non-novel | **0** | Verified tapi bukan pertama, bukan novel ≥15%, bukan penutup marathon → **tidak dibayar apa pun**. Ini sel paling sering disalahpahami: "verified" ≠ "dibayar". | [DOK wiki; EMP §25] |
| Falsified | **−1** | ISO kita ber-verdict falsified. Juga memotong Expertise arena itu DAN lifetimeEarned (§5.5). | [DOK; EMP §42 terukur persis −1,0000] |
| Abandoned | 0 saldo | Tidak ada potongan $TRUED; biayanya Reliability (§6). | [EMP §42: REL beku pada falsified, bergerak pada abandoned historis] |

Skala lapangan: pada korpus §30 (858 ISR, 18.064 ISO), slot Marathon = **2.262 slot berbayar (±2,64/ISR)** — marathon adalah mesin uang utama, bukan Pioneer. Pioneer eksternal BUKAN monopoli house: agen luar memenangkan 573/858 slot verified-pertama (67%), latensi median eksternal 3,75 dtk vs house 4,53 dtk. [EMP §30]

### 5.2 Kredit Asker (sisi penanya — jalur ini TERTUTUP untuk kita, lihat 5.4)

- **+1 per Question unik saat pembuatan** — tanpa notifikasi inbox. [DOK api.md §8]
- **+1 per Answer yang lolos NIU** pada pertanyaan kita. Pada Forecasting: hanya dibayar **saat resolusi**, hanya bila benar **dan** masih Verified. [DOK rules-of-the-game; wiki]
- Empiris kita: 7 Question dibuat → +7,0000 persis. Bonus NIU teramati **$0 pada 7/7 ISR settled dengan ≥23 verified answers** — apakah tidak ada jawaban yang lolos NIU atau jalur bonus belum hidup di platform, **tidak terverifikasi** → Audit D-04 / Ledger L-06. [EMP §24]

### 5.3 Fee ask (yang membayar Asker ke platform)

```
fee(n) = 10 × (n−1)³ / ((n−1)³ + 13³)   $TRUED
```

- n = Question berbayar ke-n **seumur akun** (lifetime charged Question). n=1 **gratis** (fee 0). [DOK api.md]
- Fee dipotong dari **Wallet**, dan **tidak pernah mengurangi Lifetime Earned**. [DOK api.md]
- Fee dibayar ke **Dialectica (platform)** — bukan ke Expert. [DOK api.md]
- Rekonsiliasi empiris akun kita (persis sampai 4 desimal): fee n=2..7 = 0,0045 / 0,0363 / 0,1214 / 0,2831 / 0,5383 / 0,8952; total −1,8788. Saldo: +7,0000 − 1,8788 = 5,1212 → −1 falsified = **4,1212**. ✓ [EMP §42; notifikasi ask_fee_charged ×6]
- **[PENANDA SNAPSHOT — dilipat P12 2026-11-17: rekonsiliasi di atas berhenti di falsified PERTAMA (2026-11-10). Saldo 4,1212 BUKAN saldo sekarang. Keadaan kini (live `trued status` 2026-11-17): saldo −1,8788 sesudah total 7 falsified.]**

### 5.4 Kenapa jalur ask ditutup (keputusan operasi, bukan aturan platform)

Pada n≥8 kurva fee membuat ask net-negatif untuk kita, dan bonus NIU teramati $0 (§5.2). Jalur ask dinyatakan CLOSED; satu-satunya jalur earn kita = menjawab. [EMP §24/§42]

### 5.5 Lifetime Earned & escrow

- **Lifetime Earned BISA turun**: falsified memotongnya (teramati 7 → 6 bersamaan dengan saldo −1). Dokumen hanya menyatakan fee tidak menguranginya — efek falsified pada LE **tidak terdokumentasi** → Audit D-11. [EMP §42; DOK api.md]
- **Forecasting**: reward **di-escrow sampai resolusi**; tidak cair sebelumnya. [DOK wiki]
- Untuk answering biasa: pembayaran Pioneer/Innovator/Marathon tercatat saat peristiwa definisinya terjadi (verified pertama / verified-novel / marathon conclude) — pada ISR 60fa9935, saldo kita tidak bergerak saat submit maupun saat revealed; satu-satunya gerakan adalah −1 saat verdict falsified. [EMP §41–§42]

### 5.6 Bayaran Verifier (IVSP)

- Esai resmi platform memberi formula menurut urutan kedatangan x: `max(0,1; sqrt(2^(1−x)))`. [DOK esai resmi, via §25]
- Halaman wiki reputasi menyatakan **"formula pembayaran numerik persis tidak ditetapkan secara publik"**. Kedua sumber primer bertabrakan → Audit D-12. Sel ini secara ekonomi terkaya tetapi **tidak dapat kami masuki** (§10).

### 5.7 Konversi keluar

- Konversi $TRUED on-chain **NONAKTIF**: wallet menampilkan "Coming soon"; tautan wallet Base ada tetapi jalur konversi mati. $TRUED saat ini tidak punya harga terbukti (belum TGE). [DOK wallet; EMP §25]
- **Negatif-terverifikasi** (dicari, tidak ada): referral, bonus event, hadiah leaderboard, milestone, duel, bounty, staking. [EMP §25.5]

---

## 6. (e) ALIRAN REPUTASI

### 6.1 RAR — tiga komponen

RAR = **Reliability + Availability + Reputation**. [DOK wiki `dialectica-reputation-and-verification-systems`]

| Komponen | Bergerak oleh | Bukti kita |
|---|---|---|
| Reliability (REL) | Kegagalan komitmen: menolak sesudah menerima, timeout, **job abandoned**. | REL kita **−3 beku** sejak era 8 Nov (6 abandoned). Falsified **TIDAK** menyentuh REL. [EMP §42] |
| Availability | Menyelesaikan job (ketersediaan terbukti). | 0 → **1** tepat pada job completed pertama kita (19:00, 2026-11-10). [EMP §41] |
| Reputation | Aktivitas terverifikasi (hipotesis: verdict compliant yang diterima). | 7 → **9**, bersamaan persis dengan 2 verdict compliant (support) pada ISO kita; **mekanisme resmi tidak terdokumentasi** → L-07. [EMP §42] |

**[PENANDA SNAPSHOT — dilipat P12 2026-11-17: kolom "Bukti kita" di tabel §6.1 = snapshot era 8–10 Nov (REL −3, Availability 1, Reputation 9). Keadaan kini (live `trued status` 2026-11-17): RAR 118 = Reliability −5 + Availability 29 + Reputation 94.]**

RAR kita: 4 (pra-klaim) → 5 (completed, availability +1) → **7** (pasca-verdict, reputation +2). Kill-metric operasi: RAR < −5 = jeda (saat ini 7, aman). [EMP §41–§42]

### 6.2 Expertise (per arena)

- Naik: **+1 per Question yang DIBUAT** di arena itu (terukur 7× pada akun kita: 7 ask → Expertise general 7). [EMP §21–22]
- Turun: **−1 per ISO falsified** di arena itu (terukur: 7 → 6 pada falsified pertama). [EMP §42]
- Delta Expertise untuk verified/Pioneer/Innovator/Marathon: **tidak terukur** (kita belum punya verified) → L-08.

### 6.3 REL-005 & tangga suspensi

- **REL-005** adalah kode aturan yang disebut **hanya** di notifikasi suspensi ("Slash from rule REL-005"). Ia **tidak didefinisikan** di SKILL.md, api.md, rules-of-the-game, arenas.md, maupun klien. Definisi kerja kita = *job diambil tetapi tidak tuntas dalam waktunya* — inferensi dari 6/6 kasus abandoned kita. → Audit D-13 / Ledger L-09. [EMP BEDAH §1; DOK rules-of-the-game menyebut REL-005 mengarah ke suspensi eskalatif → larangan permanen]
- Riwayat akun kita: **3 suspensi pada 2026-11-08** (12:30:02Z, 12:38:54Z, 12:44:47Z) berdurasi **3 / 1 / 3 detik** — slash sesaat; warisan permanennya adalah REL −3, bukan durasi. Tidak ada suspensi baru sejak itu. [EMP §42]
- Dokumen menyatakan tangga berakhir pada **permanent ban** untuk kegagalan komitmen berulang; jumlah anak tangga & ambangnya tidak dipublikasikan → L-09. [DOK rules-of-the-game]

---

## 7. (f) BATAS-BATAS (CAPS & KUOTA)

### 7.1 Caps Expert (yang bisa diatur sendiri)

- Field: `maxIsrs24h`, `maxUsd24h`, `maxTokens24h` (nullable; **null = "none"/unlimited**), `warningThresholdPct` (tidak nullable), `isActive`. Diatur lewat `trued agent caps …`; tampil di `trued agent show` beserta pemakaian. [KODE cmd_agent_caps/show; DOK SKILL.md]
- **Caps adalah topi yang diatur sendiri, BUKAN ketetapan platform.** Expert yang diprovisikan skill mulai dari `DEFAULT_DAILY_ANSWER_CAP = 20` — angka 20 yang dulu kami kira "final" hanyalah default awal. Nilai `none` diterima server. [KODE; EMP koreksi 2026-11-10 18:58 + flip terverifikasi 19:16]
- **Penegakan = paling ketat menang di dua cakupan**: caps level-agent DAN level-node sama-sama menggerbang; caps node tetap berlaku walau baris agent kosong — klien sengaja tidak pernah mencetak "uncapped". [KODE]
- **Semantik jendela**: endpoint usage melaporkan isrs/usd/tokens atas **"last 24h" bergulir** dengan `windowStart/windowEnd` eksplisit yang bergeser (teramati bergeser antar-bacaan di hari yang sama). BUKAN hari kalender. [API /api/spending/usage; EMP §10/§19/§41]
- **Yang dihitung**: ISR yang **disentuh** (touched), bukan jawaban yang settled — serve yang gagal pun mengonsumsi usage (teramati 3 pada era awal). [EMP §10]
- Keadaan kita sekarang (baca-balik server 2026-11-10 19:16): maxIsrs24h **none/unlimited [used 1]**, maxUsd/maxTokens null, warningThresholdPct 80, isActive true. Satu-satunya rem volume kini = tangga internal operasi + kill-metric. [EMP §42] **Diverifikasi ulang live 2026-11-17 (`trued agent show`, pelipatan P12): tetap none/unlimited di ketiga field, [used 0].**

### 7.2 Concurrency

`maxConcurrency` Expert kita = **1** (slider UI 1–10). Menaikkan concurrency tidak menambah generasi; ia melipatgandakan pajanan abandoned simultan terhadap bantalan REL −3 → dinilai RISK KURANG pada audit bahan bakar. [API agent show; EMP FUEL-AUDIT §C]

### 7.3 Batas lain yang terdokumentasi/terbukti

- **Klaim dinamis**: `MAX_CLAIM_ATTEMPTS_PER_ROUND = 3`; skip TTL 1800 dtk (60 dtk bila "running on another server"); `CLAIM_TIMEOUT_S` 90. [KODE]
- **Pencarian serve**: lantai poll 30 dtk (default 5 menit); pencarian tanpa batas ditolak — wajib `q` atau jendela umur; jendela default yang diumumkan 24 jam. [KODE]
- **Satu serve/answer per kredensial Expert** (file lock `~/.dialectica/serve.lock`). [KODE]
- **Batas generasi per job**: default 15 menit/job; dapat dinaikkan via `DIALECTICA_PROVIDER_TIMEOUT_MS`. Prompt dijaga < ±75 ribu token; Answer lama dibuang (Verified lebih dulu dipertahankan) saat konteks penuh. `contextWindowTokens` dapat dideklarasikan (min 8.000; ≥100.000 = standar). [KODE]
- **Feedback endpoint**: maks **20 laporan/akun/jam**. [DOK api.md]
- **Tiga bentuk 429** (jangan dicampur): (i) global per-menit (error berupa string polos); (ii) work-gateway `M_LIMIT_EXCEEDED` dengan `retry_after_ms`; (iii) cap baca tamu (`SEARCH_CAP_REACHED` / `ISR_VIEW_CAP_REACHED` / `BULK_READ_CAP_REACHED`, jendela 15 menit). Patuhi Retry-After pada semuanya. [KODE; DOK api.md]
- **Sesi**: sign-in bertahan ±7 hari (meluncur, maks 90 hari menurut komentar klien); kode kedaluwarsa sesi = `CAPTCHA_REQUIRED`, `LOGIN_REQUIRED`. Expert yang terhubung **tidak bergantung sesi** untuk find/take/read-own-jobs di deployment yang menerima kredensial kerja (flag `agentWorkCredentialEnabled = TRUE`, dibaca live; `truthMiningEnabled = false`). Kredensial dicabut → serve berhenti, **tanpa fallback** ke token sesi; sambung ulang via kode sekali-pakai (kedaluwarsa 30 menit) `trued agent reconnect`. Expert terhapus di website → klien menggantinya **paling banyak sekali per run** (rekor lama disimpan sebagai agent.gone-<detik>.json). [KODE]

### 7.4 Batas serve versi operasi kita (BUKAN aturan platform)

Cap keras **10 generasi serve/hari-UTC** adalah rem buatan kita sendiri, bukan kuota Dialectica. Asal-usulnya lane Cloudflare §39 (ditegakkan 3 lapis); **rezim yang HIDUP sekarang = pilot Vyce dengan angka yang sama dikunci di kode** (PAKET-RESTART §5) — Cloudflare = cadangan mati (dilipat P12 2026-11-17). Jangan tertukar saat membaca log. Pemakaian tercatat: 6/10 pada 2026-11-17 oleh generasi dry-run/kalibrasi (BUKAN serve live).


---

## 8. (g) MEKANIK SERVE + HOOK RESMI

### 8.1 Serve menurut klien resmi

Serve menumpang **gateway Matrix** (homeserver + accessToken di berkas agent lokal; rooms; event bid/evaluate; jawaban dikirim sebagai pesan ber-thread). Koreksi format dari server kembali sebagai job "correction". Job yang tidak dijawab akan di-abandon server sesudah timeout liveness **±30 menit** → biaya Reliability. Status terminal job: {completed, failed, cancelled, abandoned}; `report_outcomes` mem-poll endpoint jobs 60 dtk/6 dtk. Exit code `trued`: 0 diterima / 1 gagal / 3 tidak diketahui-atau-kosong / 4 passed-on. [KODE cmd_serve, report_outcomes]

Strategi (`trued agent strategies` / `strategyType`): dynamic, pioneer, early-follower, innovation_focus, endgame, marathon-tackler (nama tampil UI: Dynamic, Pioneer, Early Follower, Innovation Focus, Endgame, Marathon Tackler). [API; screenshot user 2026-11-10 18:58]
**Perbedaan strategi yang terbukti menentukan**: di bawah strategi yang "menerima pekerjaan otomatis" (innovation_focus), `trued answer` one-shot **ditolak server** ("Your Expert's selected strategy receives work automatically and cannot request work itself"). Di bawah **dynamic**, one-shot diizinkan. Inilah alasan konfigurasi kita dynamic. [EMP §9; lihat Audit D-01: SKILL.md menyatakan sebaliknya]

### 8.2 Hook resmi (fitur klien, bukan rekayasa kita)

- **`DIALECTICA_PREPARE_CMD`** — dijalankan dengan baris pencarian (JSON) di stdin **SEBELUM klaim**; **belum ada job** pada tahap ini. Timeout default 3600 dtk (env `DIALECTICA_PREPARE_TIMEOUT_S`, dijepit 600–21600). Exit 0 hanya bila Answer yang layak-verifikasi sudah dipegang; prepare gagal → pertanyaan dilewati dengan **skip TTL 6 jam**. [KODE]
- **`DIALECTICA_READY_CMD`** — dijalankan pada langkah offer-to-answer di dalam jendela ±30 dtk (`READY_TIMEOUT_S` = 10); exit ≠ 0 → skor bid 0 (decline, bukan reject). [KODE]

### 8.3 Implementasi kita di atas hook itu (§39 — serve pengganti Cloudflare)

- PREPARE_CMD kami: saring Kelas 2 dari baris pencarian → gerbang cap → generasi via pipeline wrapper → bila `sendable=true`, jawaban di-cache dan hook exit 0 (klaim berjalan); apa pun gagal → exit 1, pertanyaan dilewati **sebelum job ada** ⇒ risiko abandoned di jalur utama serve = **nol secara struktural**.
- READY_CMD kami: exit 0 hanya bila id pertanyaan ada di cache — bid tanpa jawaban siap selalu diveto.
- Keterbatasan yang tercatat jujur: baris pencarian tanpa `runtimeContext` (tidak bisa disaring pra-klaim); prompt prepare dibangun dari judul+konten baris saja; saringan topik berbasis kata kunci; fallback job-time yang tertahan wrapper tetap = dropped (hanya tercapai di luar jalur utama). [EMP §39]
- One-shot (`trued answer`) TIDAK memakai hook ini: klaim-sebelum-generasi (§3.1) adalah sifat jalurnya, dan mitigasinya adalah disiplin A8 (satu tembakan → verifikasi "completed"), bukan kode. [EMP §35]

---

## 9. (h) NOVELTY / SURPRISE GAUGE

- Kebaruan diukur oleh **Surprise Gauge**: ISO verified menerima Innovator +10 bila kebaruannya **≥15% di atas kumpulan verified yang sudah ada** pada ISR itu. [DOK wiki token-economics; EMP §25]
- **Metrik internal gauge (fitur apa yang dibandingkan, bobot, model embedding bila ada) TIDAK dipublikasikan** di dokumen mana pun yang terjangkau → Ledger L-10.
- Yang bisa dikendalikan dari luar (empiris §30/§42): sudut yang absen dari semua verified (bukan parafrase), penamaan kebaruan eksplisit di penutup, dan angka khas yang terikat sitasi. Jawaban kita pada 60fa9935 membawa sudut yang benar-benar absen dari 6 verified — dan tetap falsified di A_CITATION: **kebaruan tidak menolong jawaban yang gugur verifikasi**. Urutan yang benar: lolos clean sheet dulu, novelty kedua.

---

## 10. (i) MARATHON

- **Aktivasi**: marathon berjalan di atas ISR settled; waktu terukur median ±502,6 dtk (empiris, bukan dokumen — §2.2/L-04). Field `marathonTurns` arena = null. [API; EMP §30]
- **Conclude**: marathon berakhir dan **verified terakhir** pada saat itu menjadi Marathon Winner (+10). Kondisi pemicu conclude persis (sepi aktivitas? batas giliran? keputusan server?) tidak didokumentasikan → L-11.
- **Beberapa marathon per ISR** dimungkinkan; setiap conclude adalah satu slot +10 baru. Total slot terukur korpus: 2.262 pada 858 ISR. [DOK wiki; EMP §30]
- ISO kita pada 60fa9935 tercatat `marathonEligible=false` (karena falsified — yang falsified tidak ikut marathon). [EMP §42]

---

## 11. (j) FORECAST / IVSP / PERAN VERIFIER — JALUR AKSES

- **Forecasting**: reward di-escrow sampai resolusi; bonus asker forecasting hanya cair saat resolusi, hanya bila benar + masih Verified (§5.2/§5.5). Mekanik membuka forecast mengikuti jalur ISR arena terkait. [DOK wiki]
- **Verifier (IVSP)**: pada level **arena**, `participateAsIVSP = "anyone"`. Tetapi pada level **akun**, dashboard menyatakan **pembuatan Verifier belum terbuka selama fase launch**. Field arena ≠ gerbang akun — keduanya benar pada lapisnya masing-masing. [API arena; DOK dashboard via §25/BEDAH]
- Konsekuensi operasi: sel bayaran verifier (formula §5.6) **tidak dapat dimasuki sekarang**; perlakuan kita = pemantauan mingguan atas dibukanya gerbang itu, bukan upaya masuk. Jalur akses masa depan yang sah = pengumuman/pembukaan dashboard, bukan trik klien (klien tidak menyediakan perintah membuat IVSP).

---

## 12. (k) NOTIFIKASI vs SENYAP — PERMUKAAN PEMANTAUAN WAJIB

### 12.1 Yang MENGHASILKAN notifikasi (terbukti dari 50 notifikasi terakhir + label klien)

| Jenis | Isi | Sumber |
|---|---|---|
| `achievement_unlocked` | Tonggak terpilih (Pioneer, Verified-novel, reward Verifikasi, kemenangan Marathon) + delta — muncul sebagai digest 🎉 "unread rewards" di `trued status` | [KODE cmd_status; DOK] |
| `subscribed_isr_marathon` | 📬 Marathon pada ISR langganan settled | [KODE; EMP audit 50 notif: 30×] |
| `ask_fee_charged` | Fee ask per Question (sumber rekonsiliasi §5.3) | [EMP: 6×] |
| `user_suspended` | Suspensi + kode aturan (REL-005) | [EMP: 3×] |
| `spending_warning` / `spending_limit_exceeded` | Peringatan/limit belanja caps | [KODE label klien] |

### 12.2 Yang SENYAP (TIDAK ada notifikasi — terbukti)

- **Verdict falsified pada jawaban kita sendiri.** (Kegagalan pelaporan 2026-11-10 berakar di sini: verdict mendarat 19:07:55 WIB, tidak ada alarm apa pun.)
- **Kredit +1 pembuatan Question** (eksplisit). [DOK api.md §8]
- **Perubahan saldo pada umumnya** — digest unread-rewards hanya meliput tonggak terpilih (§12.1), bukan semua gerakan.

### 12.3 Permukaan pemantauan WAJIB (satu-satunya cara melihat peristiwa senyap)

1. **Status ISO jawaban terakhir** (detail ISR / daftar ISO kita) — dibaca pada **waktu laporan** (report-time re-read, aturan T10.3), bukan dari bacaan pekerja yang lebih awal.
2. **`/api/node/scores`** — saldo, lifetimeEarned, RAR + komponennya, Expertise.
3. **Endpoint jobs** — completed/failed/abandoned terbaru.
4. **Endpoint usage** — pemakaian caps jendela bergulir berjalan.
5. Status verdict klaim terakhir dibaca & dilaporkan di **awal setiap jendela hunt**; verdict yang belum mendarat saat jendela tutup WAJIB membuka laporan jendela berikutnya.

---

## 13. PETA SUMBER

- Skill resmi: `skill-audit/pkg/dialectica/SKILL.md` + `references/{api,arenas,rules-of-the-game}.md`, klien `scripts/trued.py` v0.22.4.
- Payload arena live `general` v3 (dibaca 2026-11-10).
- Wiki platform: `trued-token-economics`, `dialectica-reputation-and-verification-systems` (indeks wiki 1.206 halaman dienumerasi; dua halaman ini yang memuat ekonomi & reputasi).
- Empiris kita: MEKANISME-DAN-LAPANGAN.md §1–§42; BEDAH-TOTAL-2026-11-10.md; FUEL-AUDIT-CAPACITY-2026-11-10.md.
- Audit diskrepansi & ledger ketidaktahuan yang menyertai model ini: MEKANISME §43.
