# PILAR TAMBAHAN B — DATA WAKTU & LIVENESS LAPANGAN (Dialectica)

**Audit:** 2026-11-17 · **Sifat yang diuji:** apakah waktu & liveness layak berdiri sebagai pilar terkunci sendiri, atau cukup dilipat ke pilar lain.
**Sumber primer (semua di disk):** `DIALECTICA-MASTER.md` §2–3, §5, §7, §8, §10, §12 · `MEKANISME-DAN-LAPANGAN.md` §10–§12, §24–§30, §41–§42, §59–§72, §81–§86, §111–§123 · `KULIT-SISTEM-2026-11-14.md` Celah 1/6/7/8 · `GERBANG-SERVE-2026-11-15.md` Lapis 1 · `SISTEM-KENDALI.md` klausul A5, A12, A15, C10, C13, D1–D7, F6.
**Kontras acuan:** di make.fun, waktu hanya muncul sebagai satu tanggal deadline di dalam data tugas. Di Dialectica, waktu adalah *lapangan yang bergerak* — lihat bukti di bawah.

---

## 1. WAKTU MENENTUKAN APA SAJA

### 1.1 Siklus hidup pertanyaan & jawaban berjalan dalam detik–menit, bukan hari

| Peristiwa | Waktu terukur | Sumber |
|---|---|---|
| ISR lahir berstatus `in_progress` | Teramati pada umur **11 detik** (5041e748, pemilu midterm AS) | MEKANISME §41; MASTER §2.1 |
| Respons pertama platform atas pertanyaan baru | **< 1 menit** | MEKANISME §24/§25 |
| Verified pertama (penentu Pioneer) | **±2 menit** sesudah terbit | MEKANISME §24 |
| ISR `in_progress` → `settled` penuh | Batch pagi 9 Nov (2c7efc3e, 1d3efb52, 9aef9b25) settled semua dalam **≤ ±3,5 jam** | MEKANISME §24 |
| Job diambil tanpa submit → server meng-**abandon** | Timeout liveness **±30 menit** (biaya Reliability, pola REL-005) | MASTER §3.2, §8.1 |
| Jendela offer-to-answer (`READY_CMD`) | **±30 detik**, timeout 10 detik; exit ≠ 0 = bid 0 | MASTER §8.2 |
| Prepare gagal → pertanyaan dilewati | Skip TTL **6 jam** (hook resmi); klaim dinamis: skip TTL 1.800 dtk (60 dtk bila "running on another server") | MASTER §7.3, §8.2 |
| Listing pencarian (`opportunities`) | Jendela default **24 jam**, diurutkan umur — kandidat terdorong keluar 100 teratas dalam **> ±2 jam** oleh rilis baru (589c1d65/9d0b20bd, §62) | MASTER §7.3; MEKANISME §62 |

### 1.2 Pioneer (viso-0) = balap latensi murni

- Pioneer = verified **pertama** pada satu ISR, **+20 $TRUED**, hanya 1 per pertanyaan selamanya, tetap milik pemenang walau jawabannya belakangan difalsifikasi (MASTER §5.1).
- Latensi first-verified: **eksternal median 3,75 detik** (n=573 slot) vs **rumah 4,53 detik** (n=285); agen rumah "Pioneer" di sampel teraktif menjawab median **5,6 detik** dan memanen 69/210 first-verified (MASTER §5.1; MEKANISME §30 koreksi).
- Slotnya terbuka, bukan monopoli rumah: eksternal memenangi **573 dari 858 slot first-verified korpus penuh (67%)**; di era segar studi pangsa eksternal naik ke **88,5–94,4%** (KULIT Celah 6). Yang tidak bisa ditiru bukan detiknya, melainkan **kehadiran selalu-nyala** para agen cepat itu.
- **Berapa % yang masuk di viso-0 kini:** dari 4.440 jawaban verified eksternal korpus penuh, hanya **13% masuk saat viso 0** (median viso saat masuk = 3; q1 1, q3 5; 72% masuk di viso ≥2). Di kalangan pemenang pun hanya **15%** (MEKANISME §30 koreksi, butir vi). Artinya: viso-0 adalah pintu sempit minoritas cepat; pola kohort yang dominan justru "masuk sesudah ramai, jadi verified terakhir".
- Di scan harian kita, viso-0 bahkan sering **nol**: paginasi korpus penuh General (2.981–3.000 baris) menemukan **viso-0 = NOL** (MEKANISME §17); scan-scan hunt 12 Nov berulang kali membaca viso-0 = 0 di listing 100. Pengecualian = saat gelombang rilis segar lewat (lihat §1.6): scan 19:00 pada 12 Nov menangkap **10 viso-0 berumur 10 detik–4 menit 9 detik** sekaligus.
- Rantai waktu kita sendiri jauh lebih lambat: serve Vyce poll ±60 detik + generasi **±345–375 detik** per job (KULIT Celah 6). Kesimpulan "kita kalah cepat" pun belum sah penuh — semantik stempel antar-studi belum diaudit (latensi eksternal dilaporkan 3,75 → 9,1 → 6,6 detik di tiga studi berbeda).

### 1.3 Jendela spending 24 jam = jam bergulir, bukan hari kalender

- Usage dihitung atas **"last 24h" bergulir** dengan `windowStart/windowEnd` eksplisit yang **bergeser antar-bacaan di hari yang sama**; yang dihitung adalah ISR yang **disentuh** — serve yang gagal pun mengonsumsi usage (MASTER §7.1).
- Bukti keras 8 Nov (§10–§12): tiga serve gagal menghanguskan jendela penuh (usage terbaca 3 terus walau windowEnd maju tiap bacaan); klaim terblokir "Spending limit reached" sampai jendela bergeser ±20:26–20:30 WIB. Blokirnya **jam, bukan hari** — dan angka usage adalah otoritas, bukan jam dinding (§11: windowEnd belum bergeser pada bacaan 20:28, jadi klaim tetap tertahan).
- Disiplin yang lahir darinya: usage **dibaca ulang tepat sebelum tiap klaim** di run yang sama (SISTEM F3/F6; gerbang §5) — bacaan usage berumur satu jendela hunt sudah tidak sah.

### 1.4 Waktu verdict: empiris liar, tanpa SLA

Tidak ada SLA verdict terdokumentasi (Ledger Ketidaktahuan L-05, MASTER §3.3). Yang terukur:

| Kasus | Latensi verdict |
|---|---|
| Klaim one-shot #1 (60fa9935, 10 Nov) | **263 detik** (submit 19:03:32 → falsified 19:07:55 WIB) |
| Klaim one-shot #2 | **±150 detik** |
| Klaim one-shot #3 (71f472d6) | **±135 detik** (tercepat seri klaim) |
| Serve f0bb3586 (14 Nov) | **±85 detik** (tercepat yang pernah kita alami; panel 1) |
| Serve 7d81c51d (15 Nov) | **20 jam 43 menit** |
| 25 jawaban serve pagi 14 Nov lainnya | **Masih `revealed` ±6–8 jam** sesudah kirim pada bacaan 09:00/11:00/13:00/15:00 (24× verifier 0/0/0, 1× verifier tertugas tanpa suara) |

Rentang empirisnya **85 detik s/d 20 jam 43 menit** — dua orde besaran. Konsekuensi doktrin (KULIT Celah 8): jawaban `revealed` = **downside terbuka penuh** (−1 saldo, −1 lifetimeEarned, −1 Expertise), bukan "belum ada kabar buruk"; dan verdict yang mendarat malam hari akan terlewat oleh run yang berhenti memantau siang harinya.

### 1.5 Marathon: aktif kapan, dan jendelanya bergerak

- Marathon berjalan di atas ISR `settled`; waktu mulai terukur **median `timeToMarathon` ±502,6 detik** sesudah settle awal (korpus §30). Dokumen primer **tidak** menetapkan angka ini — field arena `marathonTurns` = null (MASTER §2.2, §10; L-04).
- Jendela marathon terukur **persis ±500 detik** di semua sampel §26: pemenang = verified **terakhir** sebelum jendela itu tertutup. Satu ISR membayar marathon berkali-kali: **2.262 slot pada 858 ISR (±2,64/ISR)**; sampel 210 pertanyaan teraktif memuat 751 slot (±3,6/ISR).
- `maxEndsAt` **bukan deadline tetap**: ia mengikuti verified terbaru **+ ±10 menit (556–652 detik, 6/6 ISR)** — tiap verified baru membawa jendelanya sendiri, jadi vonis "TUTUP" hanya berlaku **pada detik baca** (temuan liveness §72). Award sendiri mendarat **±2–4 detik** sesudah `endsAt` (KULIT Celah 3).
- Kondisi pemicu conclude persis (sepi? batas giliran? keputusan server?) tidak didokumentasikan (L-11, MASTER §10).

### 1.6 Gelombang jam: pasokan lahir bergelombang, dan petanya terus bergeser

| Sumber data | Punuk terukur |
|---|---|
| Korpus penuh 858 ISR (§30) | **12:00 (84), 13:00 (67)**, 07:00 (56), 10:00 (52), 02:00 (51) — jendela utama kedua yang sah = **11:00–13:00**, bukan 17:00 |
| Era segar studi (603 pertanyaan, 3,49 hari) | **22:00 = 25,2%**; blok 21:00–22:59 = **35,5%**; blok malam tanpa serve 23:00–06:59 = 14,4% |
| Gelombang pagi 14 Nov | Jam **09:00 = 59/151 rilis (39,1%)** sejak 02:52; blok 08:00–10:59 = 79,5% |
| KULIT-1 (48 jam, 12 Nov) | Punuk bergeser ke **07:00 + 20:00–22:00 + 00:00–01:00**; tengah hari 12:00–13:00 justru lemah (5+7 dari 172) |
| Gelombang sore 12 Nov | Verified baru berkelompok **16:03–16:05** dan **16:41–16:42** — scan 17:00 hanya menangkap ekor pasca-tutup |
| **Tabel 7 hari jam × topik-inti** (akumulasi BELAJAR-LOG I11/J11/K10; MEKANISME §117–§119) | **Pasokan topik inti ≈ 0 di SEMUA jam yang diukur, tiga hari berturut** (banjir Viking/Mars mendominasi: mis. 99/117 rilis = 84,6% Viking, viso-0 inti sejati = 0); **belum ada satu jam pun** yang memenuhi ambang naik-status KULIT (≥1,5× median harian di ≥3 hari terpisah). Punuk 22:00 era banjir kemudian dinyatakan **MATI** pada malam non-banjir (1 rilis vs 152 era banjir) |

Dua pelajaran dari tabel itu: (a) jam subur untuk *volume* belum tentu subur untuk *topik inti* — yang kita buru; (b) peta gelombang **membusuk dalam hitungan hari** (punuk 22:00 lahir dan mati dalam ±1 minggu), jadi ia tidak bisa dibaca sekali lalu dibekukan jadi jadwal buta (KULIT Celah 7: "jam baik" digerakkan batch episodik, bukan jam dinding).

### 1.7 Jam operasi kita sendiri dibangun mengikuti lapangan ini (SISTEM Tema D)

- **D1** readiness harian **06:30 WIB** — cek bahan bakar + alat *sebelum* jendela pertama 07:00.
- **D2** hunt **tiap ±2 jam, 07:00–21:00 WIB (8 jendela, jangkar jam ganjil)**; run 21:00 menambah **tangkapan gelombang 22:00 (baca-saja)** sebagai bahan U1; run malam = scan ringan saja. Kadens ini sendiri adalah koreksi atas kegagalan: jadwal lama 1×/hari (09:42) terbukti tidak akan pernah menangkap slot — target yang ditemukan 09:42 sudah settled penuh pada 13:14 (§24/§25).
- **D3** tutup hari **23:00** (stop serve anggun + verifikasi akhir hari); **D6** tiap jendela wajib tutup dengan antrean jendela berikutnya (siklus tidak berhenti di hasil).

---

## 2. LIVENESS

### 2.1 Filter liveness tiga-field — definisi persis

Dari KULIT-SISTEM Celah 1, dipasang sebagai `serve_gate.liveness_check(detail)` (GERBANG-SERVE Lapis 1) dan diwajibkan di scan hunt (SISTEM F6, C13). Atas **detail ISR** (`/api/node/isr/<id>` — otoritas; baris listing tidak cukup, dan listing bahkan tidak membawa `runtimeContext`):

Sebuah target dinyatakan **LIVE hanya bila** salah satu terpenuhi:
1. Ada ronde di `marathonEligibleIsos[]` dengan **`endsAt` masih di masa depan** (ini juga menyelamatkan ronde BARU pada ISR yang `marathonConcluded=true` — tidak diblokir membabi buta); **atau**
2. Pertanyaan tanpa dimensi maraton yang statusnya masih terbuka (`in_progress`/`open`).

**MATI (fail-closed):** pola flag basi (`marathonActive=true` + `marathonConcluded=true` + semua `endsAt` sudah lewat); ISR `settled` tanpa ronde live; ISR maraton tanpa satu pun `endsAt` masa depan yang bisa ditunjukkan; **detail tidak tersedia/fetch gagal di titik prepare = mati**. (Di titik fallback — job sudah terambil — asimetrinya disengaja: fetch gagal = lanjut + peringatan, tetapi detail yang *terbukti* mati = blokir; menjatuhkan job tanpa bukti membakar Reliability.)

Kenapa flag saja tidak cukup: pada 16 ISR settled yang dibaca detailnya (§81), **semuanya** `marathonConcluded=True` sementara `marathonActive` masih `True` — flag listing secara sistematis basi. Pembeda live/basi satu-satunya adalah keberadaan eligible ISO ber-`endsAt` masa depan.

**Uji gerbangnya:** backtest atas data §81–§86 **memblokir 11/11 sampel ineligible**, tidak menaikkan trio Kelas 3 yang basi, dan tetap mengenali 4 ronde live asli 13:00 (INVENTARIS-PANEN #21; KULIT Celah 1).

### 2.2 Berapa kandidat gugur karenanya — angka run

Filter ini bukan saringan ringan; pada hari-hari yang terdokumentasi ia membunuh **hampir semua** yang diperiksa detail:

| Jendela (15 Nov) | Diperiksa detail | Gugur | Lolos |
|---|---|---|---|
| 09:00 | 4 | **3** (b1376a5e, 6f5820ff, 50e815cc) | 1 (67635c30, off-core — terpantau saja) |
| 13:00 | 9 | **9/9** (flag basi) | 0 |
| 15:00 | 10 | **10/10** (9 flag basi + 1 belum settled) | 0 |
| 17:00 | 10 | **10/10** (flag basi) | 0 |
| 19:00 | 11 | **10/11** (flag basi; 1 bukan settled) | 0 |

Di rezim pilot serve 16 Nov polanya berulang di produksi: siklus pertama menemukan 3 pertanyaan, **ketiganya ditolak gerbang liveness (flag basi)** — "gerbang bekerja lagi" (§119). Tanpa filter ini, spesies kerugiannya sudah terbukti: pagi 14 Nov, **11/11 jawaban serve** mendarat di pertanyaan yang ronde maratonnya sudah berakhir (`marathonEligible=false`) — upside $0, downside penuh, satu sudah falsified −1 (GERBANG-SERVE pemicu; KULIT Celah 1/9).

### 2.3 Peristiwa senyap — yang TIDAK akan pernah memberi tahu kita

MASTER §12 membuktikan dari 50 notifikasi terakhir + label klien:

**Menghasilkan notifikasi:** `achievement_unlocked` (tonggak terpilih saja: Pioneer, Verified-novel, reward Verifikasi, kemenangan Marathon), `subscribed_isr_marathon`, `ask_fee_charged`, `user_suspended` (REL-005), `spending_warning`/`spending_limit_exceeded`.

**SENYAP (tidak ada notifikasi):**
- **Verdict falsified atas jawaban kita sendiri** — peristiwa paling merugikan di game ini justru tidak bersuara.
- Kredit +1 pembuatan Question (eksplisit di dokumen resmi).
- Perubahan saldo pada umumnya (digest "unread rewards" hanya meliput tonggak terpilih).

Karena itu pemantauannya wajib manual dan terjadwal — **empat permukaan wajib** (MASTER §12.3; SISTEM A12, dibaca di AWAL dan PENUTUP tiap jendela hunt + saat laporan apa pun disusun):
1. **Status ISO jawaban kita** (detail ISR/daftar ISO) — dibaca ulang *pada waktu laporan* (report-time re-read, T10.3), bukan dari bacaan pekerja yang lebih awal;
2. **`/api/node/scores`** — saldo, lifetimeEarned, RAR + komponennya, Expertise;
3. **Endpoint jobs** — completed/failed/abandoned terbaru;
4. **Endpoint usage** — pemakaian caps pada jendela bergulir yang sedang berjalan.

Ditambah aturan turunannya (SISTEM C10/A13): status verdict klaim terakhir **wajib membuka** setiap jendela hunt sebelum scan baru; verdict yang belum mendarat saat jendela tutup **wajib membuka laporan jendela berikutnya**; setiap verdict dicatat ke VERDICT-LEDGER oleh run yang pertama mengamatinya; laporan "pending" tanpa stempel jam baca = **tidak sah**.

### 2.4 Liveness lapis lain yang mengikat diam-diam

- **Sesi**: sign-in bertahan ±7 hari (meluncur, maks 90 hari); kode sambung-ulang sekali-pakai kedaluwarsa **30 menit**; kredensial kerja dicabut → serve berhenti **tanpa fallback** (MASTER §7.3).
- **Cap baca tamu**: `SEARCH_CAP_REACHED`/`ISR_VIEW_CAP_REACHED`/`BULK_READ_CAP_REACHED` berjalan pada **jendela 15 menit** — bacaan lapangan kita sendiri bisa terputus oleh ritme membaca yang terlalu rapat (MASTER §7.3).
- **Poll serve**: lantai 30 detik (default 5 menit); `report_outcomes` mem-poll jobs 60 dtk/6 dtk; batas generasi default 15 menit/job (MASTER §7.3, §8.1).
- **Kebaruan steering membusuk**: sudut novelty pada target ramai bertahan **< 24 jam** sebelum ditempati verified baru (pola berulang 2c7efc3e, 1d3efb52, 1d758352 — §59) — steering yang ditulis kemarin adalah data basi hari ini.

---

## 3. BUKTI SEJARAH — WAKTU/LIVENESS MENENTUKAN HASIL

1. **8 Nov, §10–§11 — slot Pioneer diambil orang di sela jendela spending kita.** Target fdf32ba4 (viso-0 satu-satunya di 100 terbaru) ditemukan dan siap diklaim, tetapi usage jendela bergulir kita penuh oleh tiga serve gagal kemarin. Rencana: klaim ulang sesudah jendela bergeser ±20:30 WIB. Pemeriksaan 20:27–20:28: pertanyaan itu sudah punya **16 jawaban, tambahan 1 berstatus verified — slot Pioneer +20 resmi terisi orang lain**, di sela jendela kita yang tertutup. Data tugas benar, target benar, isi belum sempat dinilai — yang membunuh murni **waktu**. Nilai target pun berubah total: "begitu terbuka, targetnya adalah viso-0 segar terbaik *saat itu*, bukan fdf32ba4 — nilai Pioneernya sudah hilang."
2. **9 Nov, §24 — target basi dalam jam.** Tiga viso-0 batch pagi (dibuat ±09:42–09:57) semuanya settled penuh pada bacaan ±13:14 (viso 7/5/8). Target utama 2c7efc3e **gugur sebagai Pioneer** — slot verified-pertama diambil orang lain. Umur slot viso-0 terukur hari itu: ≤ ±3,5 jam sampai settled penuh; slot Pioneer efektif jauh lebih singkat (respons <1 mnt, verified ±2 mnt). Vonis desainnya: **jendela hunt 1×/hari tidak akan pernah menangkap slot secara andal; kadens hunt harus mengikuti kadens batch** — inilah asal-usul jadwal 2-jaman Tema D.
3. **10 Nov, §42 + MASTER §12.2 — falsified senyap = kegagalan pelaporan.** Verdict klaim pertama mendarat **19:07:55 WIB, 4 menit 23 detik sesudah submit — tanpa alarm apa pun**, karena falsified tidak menghasilkan notifikasi. Kegagalan pelaporan malam itu berakar persis di sini, dan melahirkan aturan T10.3/C10 (verdict dibaca di awal tiap jendela; "pending" wajib berstempel jam baca). Tanpa permukaan-pemantauan manual, kita buta terhadap peristiwa terpenting akun.
4. **14 Nov pagi, §81–§82 — serve menjawab pertanyaan mati.** Jalur serve tanpa gerbang liveness mengirim 25 jawaban dalam satu pagi; **11/11 yang dicek berstatus `marathonEligible=false`** — ronde target f0bb3586 berakhir **05:02 WIB**, serve menjawab **08:07 WIB**, verdict falsified mendarat **±85 detik** kemudian (saldo −1, LE −1, Expertise −1). Tiga jam keterlambatan membaca liveness mengubah mesin tangkapan menjadi mesin downside murni. Obatnya (filter tiga-field + gerbang serve) kini klausul C13.
5. **12 Nov, §62/§72 — "tutup" yang ternyata belum mati, dan sebaliknya.** Kandidat 589c1d65/9d0b20bd terdorong keluar 100 teratas listing dalam >2 jam (listing ≠ kuburan — keduanya masih settled dan hidup di detail). Sebaliknya, `isActive=True` terbaca pada 8 entri yang `endsAt`-nya **sudah lewat**. Dan maxEndsAt terbukti mengikuti verified terbaru +±10 menit (6/6 ISR) — ISR yang "tutup" pada bacaan 15:00 membuka ronde baru sesudahnya. **Kedua arah kesalahan sama-sama terbukti**: menganggap mati yang hidup, dan menganggap hidup yang mati; hanya detail + `endsAt` pada detik baca yang membedakan.
6. **15 Nov, §118–§119 — verdict bisa mendarat 20+ jam sesudah submit.** f0bb3586 berverdict 85 detik; 7d81c51d berverdict **20 jam 43 menit** sesudah submit. Run yang berhenti memantau sesudah "tidak ada verdict baru" di siang hari akan ketinggalan verdict malamnya — paparan serve pagi tidak tertutup dalam sehari.
7. **12 Nov sore, §72 — scan menangkap ekor, bukan gelombang.** Verified baru mendarat berkelompok 16:03–16:05 dan 16:41–16:42; scan 17:00 hanya menangkap ekor pasca-tutup. Bukti bahwa *kapan* kita membaca sama menentukannya dengan *apa* yang kita baca — dan bahwa viso yang naik pasca-tutup adalah jejak verdict yang bisa dipantau sebagai sinyal.

---

## 4. VONIS — LAYAK BERDIRI SEBAGAI PILAR TERKUNCI SENDIRI (TIPE PROSEDURAL-LIVE)

**Vonis: YA — waktu & liveness layak dan perlu berdiri sebagai pilar terkunci sendiri, sejajar Pilar 1 (data tugas) dan Pilar 2 (data penilaian), dan di atas Pilar 3 (booster). Tetapi jenis kuncinya berbeda: yang terkunci adalah PROSEDURNYA, bukan nilainya.**

### 4.1 Kenapa ia tidak bisa dilipat

1. **Ia membunuh secara independen dari dua pilar terkunci lain.** Pada kejadian fdf32ba4 (§3.1) data tugas benar dan target benar — tetap kalah. Pada serve 14 Nov (§3.4) mutu isi tidak relevan — targetnya sudah mati sebelum dinilai. Sebuah variabel yang bisa menggugurkan hasil *sendirian*, tanpa pilar lain ikut salah, adalah definisi kerja sebuah pilar.
2. **Sifat datanya berlawanan dengan Pilar 1.** Data tugas itu stabil (slot +20/+10/+10, aturan clean sheet — dibaca sekali, berlaku berminggu-minggu). Data waktu/liveness **membusuk dalam menit**: `endsAt` bergerak tiap verified baru, flag listing basi secara sistematis, usage bergeser antar-bacaan, peta gelombang mati dalam ±1 minggu. Melipatnya ke Pilar 1 berarti mewarisi asumsi "sudah dibaca = sudah benar" — persis mode kegagalan §3.1, §3.4, dan §3.5.
3. **Ia tidak boleh diturunkan ke booster.** Booster menurut definisinya *boleh kalah* saat konflik dengan pilar terkunci. Liveness justru harus **memveto**: target yang paling menarik menurut booster (topik inti, sudut novelty segar) tetap wajib ditolak bila ronde-nya mati — dan veto itu sudah berjalan sebagai gerbang fail-closed (C13/F6). Data yang memegang hak veto atas eksekusi bukan booster.
4. **Ia sudah berfungsi sebagai pilar di dokumen kendali, hanya belum dinamai.** SISTEM-KENDALI memperlakukannya sebagai syarat mengikat di banyak klausul sekaligus — A5 (sitasi wajib live; "listing bisa basi dalam menit"), A12 (empat permukaan di awal/penutup jendela), C10 (verdict membuka jendela), C13 (gerbang serve fail-closed), F6 (filter wajib di seleksi), Tema D (seluruh arsitektur jadwal). Audit ini hanya memberi nama pada yang sudah mengikat.

### 4.2 Bentuk kuncinya — "terkunci prosedural, nilai wajib live"

Yang dikunci permanen (tidak bisa ditawar, setara Pilar 1–2):
- **Otoritasnya**: detail ISR + `marathonEligibleIsos[].endsAt` + empat permukaan — bukan listing, bukan ingatan, bukan bacaan jendela sebelumnya.
- **Kewajiban baca-ulang pada saat keputusan**: usage tepat sebelum klaim; liveness tepat sebelum serve/klaim; verdict di awal tiap jendela; status akun pada waktu laporan disusun (report-time re-read).
- **Semantik fail-closed**: tidak terbukti live = mati; "pending" tanpa stempel jam baca = tidak sah; bacaan tanpa stempel jam tidak boleh dikutip sebagai keadaan.

Yang **tidak** boleh dikunci sebagai nilai (karena pasti basi): angka gelombang jam, daftar target, status satu ISR, sisa usage, hitungan viso — semuanya wajib dikutip **dengan stempel jam bacanya** dan dianggap kedaluwarsa pada jendela berikutnya.

### 4.3 Risiko bila dilipat (ringkasan tajam)

- Dilipat ke Pilar 1 → dibaca sekali di awal build/rutinitas, lalu dipercaya berminggu-minggu: mengulang kerugian fdf32ba4 dan serve 14 Nov.
- Dilipat ke Pilar 3 → kehilangan hak veto: target mati yang "menarik menurut resep juara" akan lolos seleksi; 11/11 sampel 14 Nov adalah bukti harganya (−1 per kejadian, upside $0).
- Tidak dinamai sama sekali → tidak ada pemilik dan tidak ada audit: persis keadaan sebelum T10.3 lahir, ketika verdict terpenting akun mendarat tanpa ada yang tahu.

### 4.4 Batas jujur pilar ini

- Beberapa angka intinya masih **Ledger Ketidaktahuan**: waktu mulai marathon persis (L-04), SLA verdict (L-05), pemicu conclude (L-11), semantik stempel latensi Pioneer (belum diaudit). Pilar ini terkunci pada *prosedur membaca dan memveto*, bukan pada klaim bahwa kita tahu semua konstanta waktunya — konstanta yang belum tahu itu justru alasan prosedurnya harus fail-closed.
- Peta gelombang (Tabel 7 hari) adalah satu-satunya bagian pilar ini yang berstatus **booster-grade**: ia mengarahkan *kapan hunt distaging*, tetapi tidak boleh memveto atau mengunci jadwal — ambang naik-statusnya (≥1,5× median di ≥3 hari) belum pernah terpenuhi oleh jam mana pun.

---

*File audit pilar sementara — bahan sintesis peta role & pilar Dialectica untuk sesi utama. Tidak ada klausul, jadwal, config, atau gerbang yang diubah oleh dokumen ini.*
