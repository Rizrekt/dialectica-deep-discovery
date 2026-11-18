# AUDIT PILAR 2 — DATA PENILAIAN DIALECTICA (terkunci mutlak?)

**Tanggal audit:** 2026-11-17 (dari dokumen di disk; bacaan terakhir dokumen sumber = 2026-11-16)
**Sumber primer yang dibaca:** `MEKANISME-DAN-LAPANGAN.md` (§26, §30, §41–§43, §45, §82, §97, §106, §120–§127), `VERDICT-LEDGER.md` (8 baris), `DRILL-LOG.md`, `GERBANG-SERVE-2026-11-15.md`, `LAB-BACKTEST-2026-11-15.md`, `SISTEM-KENDALI.md` (C1–C16, F5), `QUALITY.md` (rubrik v2), `SHADOW-AWARD-TIMING-2026-11-15.md`, `DIALECTICA-MASTER.md` (§5, §8).
**Pertanyaan pilar:** cara nilai persisnya — siapa menilai, verdict apa, ambang apa, akibatnya apa — apakah terkunci dari sumber primer, atau masih tebakan?

---

## 1. Cara nilai persisnya

### 1.1 Siapa yang menilai
- Jawaban kita terkirim sebagai **ISO** di dalam pertanyaan **ISR**. Yang menilai adalah **panel verifier platform** (bukan admin, bukan penanya, bukan kita): tiap verifier menilai ISO secara independen dan menghasilkan satu vonis **compliant / non-compliant** yang terbaca di permukaan API sebagai **support / refutasi** (`supported` / `refuted` / `verifierCount` pada objek ISO).
- Per-verifier, aturannya tertulis dari snapshot aturan platform sendiri (`arenaRulesSnapshot` di detail ISR, dikutip MEKANISME §43/§82-seri drill): **compliant ⟺ lolos 4/4 cek arena v3**:
  1. **A_CITATION** — sitasi harus ada DAN benar-benar menyatakan/mendukung klaim yang ditempelinya; prosedur verifier = *"OPEN the cited link itself"*; sumber ada tapi tidak mendukung = non-compliant.
  2. **A_REASONING**
  3. **A_UNCERTAINTY**
  4. **A_SCOPE**
  Satu cek gagal = non-compliant untuk verifier itu.
- Di luar panel, ada dua penapis platform lain yang tercatat di analitik arena (§26): **Surprise Gauge** (penolakan terbesar: **59,2%** dari penolakan General) dan **arena_rules** (**38,4%**; di dalamnya A_CITATION = **91,1%** dari kegagalan aturan). Surprise Gauge adalah penilai kebaruan untuk slot Innovator (lihat §2.2) — metrik internalnya tidak dipublikasikan (L-10, lihat §5).

### 1.2 Jenis verdict / status
Status ISO yang teramati di lapangan: **intent → revealed** (terkirim, belum berverdict) **→ verified / falsified**; plus **abandoned** (job mati sebelum ISO terkirim — status jawaban, bukan verdict). Verdict bersifat final pada bacaan ledger (panel bisa tumbuh sesudah verdict awal — baris #5 tumbuh 0/1/1 → 0/2/2 tanpa mengubah status/Δ).

### 1.3 Berapa verifier (panel)
- **Tidak ada angka resmi.** Panel atas ISO kita sendiri teramati: **4, 4, 2** (3 klaim one-shot) dan **1→2, 5, 6, 6** (4 serve) — rentang **1–6**. Di lapangan kohort, panel **2** adalah modus; panel 1, 3, 4, 5 juga teramati.
- Mekanisme penentuan/eskalasi panel = **ledger ketidaktahuan L-02, belum tertutup**: yang teramati hanya bahwa panel bisa **tumbuh 1→2 sebelum verdict** (kasus 36492578, verified+awarded 23:35 WIB 15 Nov; dikonfirmasi instance ke-2, 95435cdf, 16 Nov). Bentuk sempit "verified dengan panel FINAL = 1" = **0 instance** sampai dokumen terakhir.

### 1.4 Ambang lolos — aturan clean sheet (empiris, bukan resmi)
Dari sensus berjenjang di MEKANISME (n=32 awal §41 → **465/0** di revisi mingguan §120, 16 Nov 11:00 → **467/0** di §121–§125, 16 Nov):

> **VERIFIED ⟺ ≥2 support DAN 0 refutasi. FALSIFIED ⟺ refutasi ≥1 — satu refutasi membunuh, berapa pun support-nya.**

- Bukti penopang: verified selalu tepat (2,0) pada n=32 pertama (15/15); falsified selalu memuat refuted ≥1 (17/17; pola (0,1)×2, (0,2)×12, (1,1)×2, (2,2)×1). Sesudah revisi model (verified = ≥2, bukan tepat-2): falsified-dengan-support teramati berulang sampai **seri ke-13** (termasuk 3 support kalah oleh 1 refutasi di panel 4, dan ISO kita sendiri #1: 2 support / 2 refutasi tetap falsified). **Sensus kumulatif terakhir tercatat: 467 iso ber-verdict, 0 penyimpangan.**
- **Tidak ada seri, tidak ada tie-break, tidak ada mayoritas.** Support tidak pernah bisa menyelamatkan jawaban begitu satu refutasi masuk.
- Konsekuensi desain yang sudah jadi doktrin (SISTEM-KENDALI C9 / T10.1): permukaan serangan jawaban = **jumlah klaim Tier-1** di dalamnya, bukan panjangnya; minimalkan klaim Tier-1 per jawaban.

### 1.5 Latensi verdict (SLA)
- **Tidak ada janji resmi** (L-05). Teramati di VERDICT-LEDGER: klaim one-shot cepat — **263 dtk** (#1), **±150 dtk** (#2), **±135 dtk** (#3); serve menyebar ekstrem — **±85 dtk** (#5, tercepat) sampai **±20j43m** (#6), **±21j32m** (#7), **±22j01m** (#8, terpanjang rezim).
- Falsified **tidak memicu notifikasi platform** (senyap by design, MASTER §43) — satu-satunya deteksi adalah membaca ulang ISO + `/api/node/scores` di awal tiap jendela (SISTEM-KENDALI C10 / T10.3).

---

## 2. Akibat nilai

### 2.1 FALSIFIED — pukulan rangkap tiga, terukur persis (VERDICT-LEDGER #1–#8)
Setiap falsified atas ISO kita, tanpa kecuali di 7 kejadian (3 klaim + 4 serve):

| Akibat | Nilai persis |
|---|---|
| Saldo $TRUED | **−1** |
| LifetimeEarned (LE) | **−1** |
| Expertise (arena) | **−1** |
| RAR | **BUKAN hukuman tetap** — komponennya bergerak sendiri (lihat bawah) |

Rekonsiliasi penuh rezim (revisi mingguan §120, 16 Nov): saldo **5,1212 → −1,8788 = tepat 7 × −1**, LE **7 → 0**, Expertise **7 → 0**. Rincian per baris ledger:

| # | Jalur | Panel (sup/ref/ver) | Saldo | LE | Expertise | ΔRAR (komponen) |
|---|---|---|---|---|---|---|
| 1 (10 Nov) | klaim Nemotron | 2/2/4 | −1 | 7→6 | 7→6 | +3 (availability +1 job completed; reputation +2 bertepatan 2 verdict compliant) |
| 2 (10 Nov) | klaim Nemotron | 0/4/4 | −1 (4,1212→3,1212) | 6→5 | 6→5 | +1 (7→8) |
| 3 (11 Nov) | klaim Cloudflare | 0/1/2 | −1 (3,1212→2,1212) | 5→4 | 5→4 | +1 (8→9; availability 2→3, reliability −3, reputation 9) |
| 4 (12 Nov) | uji klaim — **ABANDONED/DROPPED** (0 terkirim) | — | **0** | 0 | 0 | **−1** (9→8; reliability −3→−4) + suspensionCount 3→4 |
| 5 (14 Nov) | serve Vyce | 0/1→2/1→2 | −1 (2,1212→1,1212) | 4→3 | 4→3 | +24 (10→34; availability 5→29, reliability −4→−5, reputation 9→10) + suspensionCount 4→5 |
| 6 (15 Nov) | serve Vyce | 0/4/5 | −1 (1,1212→0,1212) | 3→2 | 3→2 | +38 (42→80; reputation 18→56, tanpa verified baru) |
| 7 (15 Nov) | serve Vyce | 0/4/6 | −1 (0,1212→−0,8788) | 2→1 | 2→1 | +28 (81→109) |
| 8 (15 Nov) | serve Vyce | 0/6/6 | −1 (−0,8788→**−1,8788**) | 1→0 | 1→0 | +9 (109→**118**) |

- **RAR bukan skor mutu jawaban.** RAR = **Reliability + Availability + Reputation** (MASTER §12; MEKANISME §43 butir 7). Falsified tidak menyentuh reliability (REL menghukum job tak-tuntas/abandoned: baris #4 −1 REL + suspensi); availability **naik** +1 per job completed (membayar penyelesaian, bukan kebenaran); reputation bergerak tak-terjelaskan (lihat L-07 di §5). Karena itu RAR kita justru **naik 4 → 118** selama rezim 7 falsified — komponennya menipu bila dibaca sebagai nilai.
- **Rem internal yang dipicu verdict** (SISTEM-KENDALI C1, kill-metric): (i) **10 klaim disiplin tanpa settle → STOP TOTAL** sampai user memutuskan (hitungan resmi kini **0/10** — ketiga klaim disiplin sudah settle berverdict; STOP TOTAL klaim yang berlaku lahir dari evaluasi falsified #3, janji day-close §46); (ii) **1 jawaban falsified → JEDA klaim/serve + bedah akar** sebelum tembakan berikutnya (JEDA (ii) aktif sekarang, dipicu 4 falsified serve sejak klaim terakhir); (iii) **RAR < −5 → jeda s/d revisi mingguan** (kini 118 — tidak terpicu); (iv) jalur bertanya tertutup (aritmetika terpisah: fee n=8 = 1,3504 > kredit +1; bonus NIU terbukti $0).

### 2.2 VERIFIED / berhasil — yang membayar hanya 3 sel (sumber resmi /earn, terverifikasi live berulang; terakhir §120, 16 Nov 11:53 WIB)
| Sel | Syarat definisi | Bayaran |
|---|---|---|
| **Pioneer** | ISO **verified pertama** pada ISR (viso-0) | **+20 $TRUED** |
| **Innovator** | ISO verified yang lolos **Surprise Gauge** = konten baru **≥15%** di atas verified yang sudah ada (<15% = paraphrasing, gugur — juga butir (f) rubrik) | **+10 $TRUED** |
| **Marathon Winner** | ISO verified yang menjadi **eligible terakhir** saat ronde maraton conclude | **+10 $TRUED** |
| Verified biasa | verified tanpa memenangi satu sel pun | **$0** — tidak pernah dilaporkan sebagai progres uang (SISTEM-KENDALI F5) |

- **Kapan settle/bayar:** pembayaran tercatat **saat peristiwa definisinya terjadi** (verified pertama / verified-novel / marathon conclude) — saldo tidak bergerak saat submit maupun saat revealed; satu-satunya gerakan teramati pada ISO kita adalah −1 saat verdict falsified (MASTER §176). Penumpukan (stacking) dua slot pada satu jawaban: **belum terbukti** — tidak dihitung di EV (MEKANISME §25).
- **Marathon diurai mekanis** (`SHADOW-AWARD-TIMING-2026-11-15.md`, korpus 264 ISR / 1.679 entri eligible / 624 award): satu ronde = entri `marathonEligibleIsos`, `startedAt` ≈ momen verdict mendarat, `endsAt` = `startedAt` + **tepat 500 detik** (tanpa pengecualian), `awardedAt` ≈ `endsAt` + 0–4 dtk di era sepi (lag membesar di ekor burst). Model **M1 (survival jendela): awarded ⟺ verified DAN tidak ada eligible baru mulai sebelum `endsAt`-nya — akurasi 97,9% (1.636/1.671)**; M2 84,6% dan M3 91,2% gugur. Jadi verdict adalah gerbang mutlaknya; award adalah perlombaan verdict + survival 500 detik, bukan perlombaan submit. Pengecualian tercatat: zona co-award ≤70 dtk dan skip ekor-burst (kelas dibiarkan terbuka).
- **ΔExpertise/ΔLE untuk verified kita sendiri: BELUM TERUKUR** (L-08/L-12) — akun kita belum pernah punya satu pun verified (minggu 10–16 Nov: **0 verified / 7 falsified**), jadi akibat positif persis di luar nominal slot di atas belum pernah teramati di akun sendiri.
- Jalur bertanya (di luar pilar jawab): pertanyaan unik +1 tercantum di /earn, tetapi bonus NIU asker terbukti **$0** pada n=8 kita — jalur tertutup secara aritmetika (F8).

---

## 3. Skor / leaderboard

- **Yang menentukan rank leaderboard adalah LifetimeEarned, bukan Balance** (MEKANISME §25/MASTER): fee bertanya tidak mengurangi LE; falsified mengurangi LE −1 per kejadian — karena itu 7 falsified menghapus seluruh LE kita.
- **$TRUED belum berharga**: tidak bisa diekspor on-chain, tidak ada pasar/TGE/rate (FAQ resmi /why, terverifikasi live terakhir 16 Nov 11:53–11:55 WIB: *"On-chain export is currently unavailable"*). Yang diakumulasi murni **posisi**.
- **Posisi kita terakhir tercatat di dokumen** (revisi mingguan §120 + jangkar §121–§127, **16 Nov 2026**): saldo **−1,8788 $TRUED**, **LifetimeEarned 0**, **Expertise 0**, **RAR 118** (reliability **−5**, availability **29**, reputation **94**), suspensionCount **5**, **di luar top-100**. Pembanding di dokumen yang sama: ambang #10 = **18.417** koin (HIMANSHU, +16.171 dalam ±6 hari); Adam Reinhard (acuan eksternal) #15 = 12.220; 11 dari top-100 adalah akun rumah. Jarak ke papan **melebar** (−7,0000 kita vs ambang yang naik).
- Rate verified adalah tuasnya (QUALITY.md kepala): median verdict rate per-agen kohort eksternal **32%** (n=182 agen ≥5 verdict) vs sub-kohort pemenang **55%** dan top-15 **64%** (§30); analitik General terakhir (§120): innovation_focus SR 68,5% (n=6.540), dynamic 60,5% (n=36.489). Rate kita minggu ini: **0/7 = 0%**.

---

## 4. Gerbang penilaian internal kita — terbukti menangkap berapa dari berapa

### 4.1 Lantai mekanik (K-1/K-2, §45/T12 — SISTEM-KENDALI C6)
Sendable mensyaratkan semua: **K-1(a) URL ≥1; K-1(b) kepadatan sitasi ≥0,5/1.000 kar; K-2 rasio angka terikat sitasi ≥0,30; panjang ≥4.500 kar**; plus status wrapper OK + nol finding + rubrik (g) LOLOS. Lantai = syarat perlu, **bukan penjamin verdict** (terbukti: klaim #3 lolos semua lantai dan tetap falsified).

### 4.2 Rubrik QUALITY v2 (a)–(i) — alat drill
Sembilan butir LOLOS/GAGAL; pintu mati: **(d)** sitasi+entailment E1, **(g)** format, **(h)** cakupan sub-pertanyaan atas teks terkirim, **(i)** bukti empiris ≥1 fakta dunia terikat. Dipakai di **drill bedah**: tiap jendela tanpa klaim menilai 2 verified terbaru (V1/V2) + 2 falsified terbaru (F1/F2) per ISR, skor /9.
- **(h)+(i) lahir dari klaim #3 dan terbukti menangkap klaim #3 itu sendiri** saat di-reskor sebagai F2 di drill ISR 71f472d6: skor **6/9**, gagal (b)+(h)+(i) — scope-miss yang membunuhnya kini tertangkap gerbang yang ia lahirkan.
- **Skor total TIDAK memisahkan secara konsisten** — dua arah terbukti: drill 15 Nov 09:00 (b1376a5e) **terbalik penuh** (F1 falsified **9/9** vs V1/V2 verified 7/9; akar: rubrik tidak memeriksa keputusan populasi/scope F1); drill 16 Nov 11:00 **memisahkan kuat** (V 7/9 + 8/9 vs F 1/9 + 1/9 + 1/9). Butir yang memisahkan adalah pola per-butir, bukan total: **(d)/E1 terkuat** (akumulasi E1 sampai **ke-43**, 12 sub-pola, diadopsi ke (d) v2 sesudah ambang ×3: d9f49e11, 96c384fd, 66f46c3e); **(e) anti-prediktif** — verified gagal (e) **27/38** di lab §120, memburuk ke **35/50** s/d §125 (penamaan kebaruan ketat hanya 0,5% di korpus juara) → lab memutus reformulasi (e) (U-LAB-02, menunggu adopsi v3); **(h) lemah** (17 celah vs 3 tangkapan s/d lab §120).

### 4.3 Gerbang serve (`serve_gate.py`, GERBANG-SERVE-2026-11-15) + backtest lab 29 jawaban (LAB-BACKTEST-2026-11-15)
Empat lapis: (1) liveness tiga-field fail-closed, (2) deteksi thinking-trace, (3) wrapper klaim verbatim + lantai K-1/K-2, (4) self-VFP semantik — **lapis 4 TIDAK terpasang** (`semantic_check` sengaja kosong; lihat §5). Suite tes: **37/37** serve_gate, total regresi **142/142**; pre-flight pilot 16 Nov menjalankan ulang versi tes yang tumbuh: **48/48**.
Backtest atas korpus nyata **29 ISO** (26 serve: 22 revealed + 4 falsified; + 3 klaim falsified pembanding), teks tervalidasi silang 29/29:

| Kelompok | Hasil gerbang |
|---|---|
| **4 falsified serve** | **4/4 TERTAHAN — oleh SETIAP lapis secara mandiri**: liveness 4/4 MATI (semua pola flag basi, `endsAt` lewat sebelum submit); trace 4/4; lantai 4/4 gagal (K-1(a) 4/4; K-1(b) 3/4; K-2 3/4); gabungan 4/4. **Saldo −4 itu tidak akan terjadi di bawah gerbang ini.** |
| **22 revealed serve** | 22/22 ikut tertahan; **0** yang tertahan HANYA oleh liveness. Bukan false-block terukur: revealed ≠ verified, 22/22 memang 0 URL, 21/22 ber-trace, 26/26 `marathonEligible=False` (upside $0). |
| **3 klaim falsified (pembanding)** | Gerbang isi menahan **1/3** (097df475 gugur di ketiga sub-lantai); **2/3 LOLOS KIRIM** — fcb7b015 (skor 5/6) dan 0d76cc7c (skor **6/6**, teks terbersih korpus) tetap lolos dan keduanya falsified di platform. |
| Liveness replay | **25/26** target serve MATI pada jam submitnya; 1 LIVE (pertanyaan terbuka non-maraton) — drafnya tetap tertahan lapis isi. Di produksi pilot 16 Nov gerbang bekerja berulang: menolak kandidat flag-basi di jendela 07:00, 09:00 (df9cb696), 11:00 (3/3), 13:00, 21:00. |

### 4.4 Kalibrasi yang masih melawan kita
- **K-2 @0,30 terlalu kasar ke verified asli**: di korpus juara (n=203/64), false-rejection verified **67,5% @0,30 → 42,4% @0,15**; gap lantai penuh hanya +4,4pp @0,30 vs +24,8pp @0,15; di jendela-jendela 16 Nov K-2 menolak **3/3 verified di 4 jendela beruntun**. Lab §120 memutus opsi turun ke **0,15 (U2)** — keputusan final di user/sesi utama; paket serve tetap berjalan di 0,30 sampai diputuskan.
- **E3** (penutup evasif sumber = tahan): ambang adopsi terpenuhi **×4** (4/4 falsified serve membawa frasa verbatim yang sama — belakangan teratribusi ke `citation_patch` v1 kita sendiri, jadi tripwire pipa, bukan vonis model), false-positive **0/203** korpus juara → diadopsi sebagai U-LAB-01 oleh lab 16 Nov; sinyalnya terverifikasi ada di `serve_gate.py` pada pre-flight pilot (48/48).

---

## 5. Vonis Pilar 2: **SETENGAH** — sisi hukuman terkunci angka, sisi resmi & sisi positif masih bolong

### Terkunci dari sumber primer (boleh jadi patokan mutlak)
1. **Aturan agregasi empiris clean sheet** — verified ⟺ ≥2 support + 0 refutasi; 1 refutasi membunuh di panel 1–6, termasuk melawan 2–3 support. Sensus **467 iso / 0 penyimpangan** (16 Nov). Ini aturan yang benar-benar dipakai verifier di lapangan, terukur, bukan bunyi dokumen.
2. **Checklist per-verifier 4 aturan arena** (A_CITATION/A_REASONING/A_UNCERTAINTY/A_SCOPE) — berasal dari `arenaRulesSnapshot` platform sendiri, termasuk prosedur buka-dan-baca A_CITATION (= sub-cek E1 kita).
3. **Akibat falsified persis dan rekonsiliasi menutup**: −1 saldo / −1 LE / −1 Expertise per falsified, 7× teramati, saldo 5,1212 → −1,8788 tanpa sisa; abandoned menghukum reliability + suspensi, bukan saldo.
4. **Tabel bayaran resmi** Pioneer +20 / Innovator +10 / Marathon +10, verified biasa $0 — dari /earn resmi, terverifikasi live berulang (terakhir 16 Nov).
5. **Mekanik award Marathon M1** — jendela 500 detik persis, survival, akurasi 97,9% (n=1.671 entri, 624 award).

### Masih belum diketahui persis (celah — jangan diperlakukan sebagai terkunci)
1. **L-01 — Ambang agregasi RESMI tidak dipublikasikan** (field arena null). Clean sheet adalah aturan *empiris kita*; bila platform mengubah agregasi, model basi diam-diam. Inilah alasan vonis bukan LOLOS penuh: cara nilai "persisnya" di tingkat dokumen resmi memang tidak pernah diberikan platform.
2. **L-02 — Ukuran & eskalasi panel tidak diketahui**: kenapa satu ISO dapat 2 verifier dan lain 6; "verified panel final = 1" masih 0 instance.
3. **L-05 — SLA verdict tidak ada**: latensi teramati 85 detik – 22 jam tanpa pola janji; verdict cepat ≈ penolakan jelas hanya hipotesis.
4. **L-07 — Mekanisme Reputation tak terjelaskan**: reputation naik 7 → 94 (termasuk +38 dalam semalam) **tanpa satu pun verified baru**; hipotesis korelasi 1:1 dengan verdict compliant runtuh di data serve. Akibatnya RAR tidak bisa dipakai sebagai proksi nilai — padahal RAR adalah kill-metric (iii).
5. **L-10 — Metrik internal Surprise Gauge tidak diketahui**: ambang ≥15% diketahui, *apa yang dibandingkan* untuk 15% itu tidak; Innovator juga tidak punya penanda publik per-jawaban, jadi pangsa Innovator tidak terukur dari luar.
6. **L-08 — Akibat positif di akun sendiri belum pernah teramati**: 0 verified seumur rezim → ΔExpertise/ΔLE dari verified/Pioneer/Innovator/Marathon dan kemungkinan stacking slot belum terukur satu kali pun.
7. **C5 (SISTEM-KENDALI) — Self-VFP semantik jalur serve belum ada**: gerbang serve mekanis saja; backtest membuktikan spesies falsified semantik lolos 2/3 di lapis isi. Serve tidak boleh dianggap aman hanya bermodal gerbang ini — syarat hidupnya adalah keputusan lab + spot-check manual, persis seperti yang dipraktikkan pilot 16 Nov (0 generasi, spot-check masih menunggu generasi pertama).

**Satu kalimat vonis:** penilai, checklist, ambang empiris, dan harga kegagalannya terkunci berangka dari sumber primer; tetapi dokumen resmi platform tidak pernah mempublikasikan ambang agregasi, panel, SLA, reputation, dan surprise-gauge — dan akun kita belum pernah membuktikan sisi bayarannya sendiri — jadi Pilar 2 berdiri **SETENGAH (kuat di sisi falsified, bolong di sisi resmi-positif)**.
