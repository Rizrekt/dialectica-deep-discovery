# AUDIT PILAR TAMBAHAN A — DATA KEADAAN AKUN & RISIKO (Dialectica)

**Tanggal audit:** 2026-11-17 (dokumen terakhir yang dipakai: MEKANISME §127, tutup hari 2026-11-16 23:00 WIB)
**Sumber primer:** DIALECTICA-MASTER.md §5 (aliran uang), §6 (reputasi/RAR/REL/suspensi), §7 (caps), §8.1 (strategyType), §12 (permukaan pemantauan); SISTEM-KENDALI.md klausul C1, C12, C13, C14, F3, F5, F13; VERDICT-LEDGER.md baris #1–#8; MEKANISME-DAN-LAPANGAN.md §10, §13, §42, §50, §58, §97, §109, §120, §127.
**Catatan tanggal dokumen:** angka di DIALECTICA-MASTER.md adalah potret **2026-11-10** (saldo 4,1212; RAR 7) — sudah tertimpa. Angka terakhir yang mengikat ada di §1 tabel di bawah, dari MEKANISME §120 (jangkar live 2026-11-16 11:44–11:53 WIB) dan §127 (bacaan server 2026-11-16 23:0x WIB, identik jangkar 06:30 hari yang sama).

---

## 1. KEADAAN AKUN YANG BERUBAH TIAP VERDICT & MENGUNCI LANGKAH BERIKUTNYA

Semua angka terakhir dari `/api/node/scores` + `trued agent show` + endpoint usage/jobs, dibaca 2026-11-16 23:0x WIB (MEKANISME §127 butir 1–2):

| Keadaan | Cara bergerak | Angka terakhir tercatat | Sumber/tanggal |
|---|---|---|---|
| **Saldo $TRUED** | Pioneer +20 / Innovator +10 / Marathon +10 / falsified **−1** / fee ask −fee(n) / verified biasa 0 | **−1,8788** (negatif) | §127, 16 Nov 23:00; rekonsiliasi §120: 5,1212 → −1,8788 = tepat 7 falsified × −1 |
| **Lifetime Earned (LE)** | Falsified **−1** (bisa turun — tidak terdokumentasi platform, terbukti empiris); fee ask TIDAK mengurangi LE | **0** (dari 7) | §127; MASTER §5.5; ledger #1–#8: LE turun −1 di SETIAP falsified, 7→0 dalam 8 baris |
| **Expertise (arena general)** | +1 per Question dibuat; **−1 per ISO falsified** di arena itu; delta verified belum terukur (L-08) | **0** (dari 7) | §127; MASTER §6.2; ledger: 7→0 sejajar LE di tiap baris |
| **RAR — Reliability (REL)** | Job abandoned / gagal komitmen; falsified TIDAK menyentuh REL | **−5** (dari −3 era 8 Nov; −1 pada abandoned b4d7ab24 12 Nov, −1 pada serve falsified f0bb3586 14 Nov) | §120 butir 3; §127; MASTER §6.1 |
| **RAR — Availability** | +1 per job completed (dan naik besar dari volume serve: 0→29) | **29** | §127; MASTER §6.1 |
| **RAR — Reputation** | Naik bersamaan verdict compliant yang diterima — **dan terbukti naik TANPA verified baru** (mekanisme resmi tidak terdokumentasi, L-07) | **94** (7 → 94; +38 dan +28 pada dua falsified serve 15 Nov) | §120 butir 3; §127; ledger #6–#8 |
| **RAR total** | REL + Availability + Reputation | **118** (−5 + 29 + 94) | §127 |
| **suspensionCount / tangga suspensi** | Abandoned → suspensi REL-005 (3 suspensi 8 Nov: 3/1/3 detik; #4 12 Nov; #5 14 Nov, berakhir 2026-11-14T00:43:20Z); tangga berakhir **permanent ban**, jumlah anak tangga tidak dipublikasikan (L-09) | **5 suspensi; tidak ada suspensi aktif** | §120 butir 2–3; MASTER §6.3 |
| **Caps (maxIsrs24h / maxUsd24h / maxTokens24h)** | Topi yang diatur SENDIRI, ditegakkan platform di level agent DAN node (paling ketat menang); jendela "last 24h" BERGULIR, bukan hari kalender; yang dihitung = ISR yang disentuh, serve gagal pun mengonsumsi | **unlimited semua [used 0]**; maxConcurrency 1; warningThresholdPct 80 | §127 (`agent show`); MASTER §7.1 |
| **Usage jendela berjalan** | isrs/tokens/usd atas 24 jam bergulir (windowStart/End eksplisit bergeser antar-bacaan) | **isrs 0, tokens 0, usd 0**; window 2026-11-15T15:58:48Z–2026-11-16T15:58:48Z | §127 butir 1 |
| **strategyType** | Menentukan jalur mana yang DIIZINKAN server: di bawah strategi penerima-kerja-otomatis (innovation_focus), `trued answer` one-shot DITOLAK server; di bawah dynamic diizinkan | **dynamic** (arena general, state configured) | MASTER §8.1; §127 |
| **Status rezim operasi (STOP TOTAL / JEDA / tangga volume)** | Ditentukan kill-metric (§2), bukan oleh adanya target: fase teori RAMP 4–10/hari, eksekusi 0 | **STOP TOTAL klaim one-shot + JEDA (ii) AKTIF; fase RAMP (teori); syarat naik PENUH gugur permanen** (10 klaim pertama: 0 verified, 3 falsified, 1 abandoned) | §127 butir 4; §120 butir 4 |
| **Paparan terbuka (revealed belum berverdict)** | Tiap ISO revealed adalah utang risiko berjalan: bisa falsified −1 (rangkap tiga) kapan pun, tanpa notifikasi | **22 jawaban serve pagi 14 Nov masih revealed** (dari 26; 4 sudah falsified) | §127 butir 3c |
| **Jobs** | completed/failed/abandoned = permukaan bukti keadaan, bukan log klien | **34 total (29 completed, 5 failed), 0 in-flight** | §127 butir 1 |

**Sifat khas pilar ini:** keadaannya berubah TANPA aksi kita — verdict serve mendarat 20–22 jam sesudah submit (ledger #6–#8: submit 14 Nov pagi, verdict 14 Nov malam–15 Nov pagi), jendela usage bergeser sendiri, dan falsified TIDAK menghasilkan notifikasi apa pun (MASTER §12.2). Satu-satunya cara melihatnya = empat permukaan pemantauan wajib MASTER §12.3 (status ISO terakhir, `/api/node/scores`, endpoint jobs, endpoint usage), dibaca di awal dan penutup tiap jendela (SISTEM-KENDALI A12/C10).

**Peringatan bacaan — RAR total menipu:** RAR naik 4 → 118 justru selama minggu 7 falsified (§120 butir 3), karena Reputation (+87) dan Availability (+29) menimbun komponen yang mengikat, Reliability (−5). Angka yang benar-benar dekat ke bahaya adalah REL −5 dan bantalan suspensi (suspensionCount 5 menuju tangga yang ujungnya permanent ban, ambangnya tidak dipublikasikan) — bukan RAR 118 yang tampak aman.

---

## 2. RISIKO ASIMETRIS

### 2.1 Satu falsified menghukum rangkap (terukur persis, VERDICT-LEDGER #1–#8)

Setiap falsified, tanpa kecuali di 7/7 baris falsified: **saldo −1, Lifetime Earned −1, Expertise −1** — dilaporkan sebagai "pukulan rangkap tiga" (SISTEM-KENDALI F5). Ditambah akibat rezim: **kill-metric (ii) terpicu → JEDA** (serve/klaim berhenti + bedah akar wajib sebelum tembakan berikutnya). Pada jalur serve, falsified juga terbukti ikut menggerakkan REL −1 + suspensionCount +1 (ledger #5: REL −4→−5, suspensi 4→5).

### 2.2 Verified biasa vs slot berbayar (MASTER §5.1, SISTEM-KENDALI F5)

| Hasil | Bayaran | Catatan |
|---|---|---|
| Verified, bukan pertama/bukan novel/bukan penutup marathon | **$0** | Sel paling sering disalahpahami: "verified" ≠ "dibayar"; TIDAK dilaporkan sebagai progres uang (F5) |
| Pioneer (verified PERTAMA pada ISR) | **+20** | Tetap disimpan walau keadaan ISR berubah sesudahnya |
| Innovator (verified + novelty ≥15% di atas verified yang ada) | **+10** | Diukur Surprise Gauge; metrik internal gauge tidak dipublikasikan (L-10) |
| Marathon Winner (verified TERAKHIR saat marathon conclude) | **+10** | Mesin uang utama lapangan: 2.262 slot pada korpus 858 ISR (§30) |
| Falsified | **−1 rangkap tiga + JEDA** | Lihat 2.1 |
| Abandoned | $0, tapi **REL −1 + anak tangga suspensi** | 6 abandoned era 8 Nov = REL −3 permanen + 3 suspensi |

**Asimetrinya:** upside satu tembakan dibatasi +10/+20 dan hanya cair bila TIGA syarat posisi terpenuhi (pertama/novel/terakhir); downside-nya −1 rangkap tiga PLUS kunci rezim (JEDA/STOP) PLUS paparan berantai — 26 jawaban serve satu pagi menghasilkan 4 falsified terbukti dan 22 utang revealed yang masing-masing masih bisa −1 (potensi −22 lagi, §127 butir 3c). Satu pagi serve mentah (14 Nov) menghapus seluruh saldo yang dibangun jalur ask (+5,1212 → −1,8788 dalam ±30 jam verdict).

### 2.3 Kill-metric (SISTEM-KENDALI C1, paket b.13) — ambang + status kini

| ID | Ambang | Akibat | Status kini (16 Nov 23:00, §127 butir 4–5) |
|---|---|---|---|
| (a) | **10 klaim disiplin tanpa settle** (settle = verdict mendarat; koreksi definisi §120 — bukan "tanpa verified") | STOP TOTAL sampai user memutuskan | **0/10 — TIDAK tercapai** (3 klaim one-shot semuanya settled; abandoned juga terminal) |
| (b)/(ii) | **1 jawaban FALSIFIED** | Jeda + bedah akar sebelum serve/klaim berikutnya | **TERPICU & AKTIF** — 4 falsified serve sejak klaim terakhir; JEDA mengunci klaim; STOP TOTAL klaim one-shot berlaku di atasnya sampai sesi utama mencabut tertulis sesudah bedah |
| (c) | **RAR < −5** | Jeda s/d revisi mingguan | **TIDAK terpicu di angka total** (RAR 118) — TAPI lihat peringatan §1: komponen REL sudah tepat di **−5**; ambang total ini secara empiris sudah tidak sensitif karena Reputation menggembung tanpa verified (L-07) |
| (d) | Jalur bertanya | **TERTUTUP** | **Tetap tertutup** — fee n=8 = 1,3504 > kredit +1; bonus NIU terbukti $0 pada 7/7 ISR settled (87 verified di panel, §120 butir 1); hanya bukti bonus benar-benar dibayar yang membukanya (F8) |

Ambang operasi tambahan yang hidup di luar C1: **1 abandoned → STOP hari itu + bedah** (doktrin §7.3/§7.5, terpicu 12 Nov); **cap serve internal 10 generasi/hari-UTC** (rem buatan kita, 3 lapis, C14 — bukan kuota platform, MASTER §7.4); **plafon RAMP 10 klaim/hari** semua jendela digabung (F13) di atas caps server yang unlimited.

---

## 3. BUKTI SEJARAH: PILAR INI PERNAH MENENTUKAN HASIL

1. **Klaim tertahan spending limit — 2026-11-08 malam (§10).** Bukan target yang kurang: usage jendela bergulir penuh (isrs 3 dari serve gagal kemarin, dihitung sebagai konsumsi) lawan caps maxIsrs24h **1** yang kita pasang sendiri. Klaim menunggu jendela geser berakhir ±20:26 WIB. Pelajaran: keadaan (usage × caps × jendela) memutuskan bisa/tidak menembak, bukan kualitas draf.
2. **Caps = rem pasca-suspensi, bukan kuota platform — 8–10 Nov (§13, §42, MASTER §7.1).** Sesudah 3 suspensi + 6 abandoned 8 Nov, caps diturunkan sendiri **20→3→1**. Selama ±2 hari angka "1" ini dibaca sebagai batas platform; bedah 10 Nov membuktikan 20 hanyalah `DEFAULT_DAILY_ANSWER_CAP` provisi skill dan `none` diterima server. Flip dieksekusi sesi utama atas persetujuan user: 1→20 (10 Nov ±13:45, §24.1) lalu → **unlimited** (10 Nov 19:16 terverifikasi, §42). Yang mengikat sesudah flip = tangga internal + kill-metric (F3/F13).
3. **strategyType mengunci jalur — terbukti empiris (MASTER §8.1, §9 MEKANISME).** Di bawah innovation_focus, server MENOLAK one-shot ("Your Expert's selected strategy receives work automatically and cannot request work itself"); di bawah dynamic diizinkan. Satu field konfigurasi akun menentukan seluruh jalur klaim ada/tidak — dan sempat tercatat berbeda antar dokumen (MEMORY menulis innovation_focus aktif; live sejak 11 Nov = dynamic; diskrepansi ditandai berulang §50–§58).
4. **Falsified pertama → JEDA; falsified klaim uji → STOP TOTAL — 10–11 Nov (ledger #1–#3, §50).** Klaim #1 falsified 10 Nov 19:07 → JEDA. Klaim uji JEDA #2 falsified 11 Nov 07:28:57 → per janji day-close §46, **STOP TOTAL** untuk evaluasi menyeluruh. Tiga klaim rezim caps-20: 3 falsified, saldo 5,1212 → 2,1212 dalam 12 jam. Sejak itu (11 Nov → 16 Nov) klaim one-shot = 0 bukan karena tidak ada target, tapi karena keadaan rezim mengunci.
5. **Abandoned menghukum tanpa menyentuh saldo — 12 Nov (ledger #4, §58).** Job b4d7ab24 DROPPED (draf tertahan wrapper, 0 submitted): saldo/LE/Expertise diam, tapi **REL −3→−4, suspensionCount 3→4**, dan doktrin §7.3 memicu STOP hari itu. Bukti bahwa membaca saldo saja melewatkan hukuman yang sesungguhnya.
6. **Serve mentah satu pagi → 4 falsified + suspensi ke-5 — 14–15 Nov (ledger #5–#8, §97).** 26 jawaban serve Vyce pagi 14 Nov: verdict mendarat bergelombang sampai 22 jam kemudian; 3 falsified terdeteksi dalam jendela 03:00–07:00 15 Nov saat hunt membuka dengan bacaan scores (C10 bekerja). Saldo 2,1212 → **−1,8788**, LE 3→0, Expertise 3→0, REL →−5, suspensi →5. Inilah yang mengubah hold serve T16-A/T16-B menjadi STOP + gerbang serve wajib.
7. **RAR menipu di saat paling berbahaya — 16 Nov (§120 butir 3).** Minggu 0 verified / 7 falsified ditutup dengan RAR **118** (naik dari 4). Siapa pun yang membaca RAR total sebagai "aman" melewatkan REL −5 + suspensionCount 5. Komponen, bukan total, yang mengikat.
8. **Keadaan mengunci di atas tangga volume — 16 Nov (§120 butir 4, §127 butir 4).** Fase teori RAMP (4–10/hari) dan caps server unlimited sama-sama memberi "izin" di atas kertas; eksekusi tetap **0** karena STOP TOTAL + JEDA (ii). Tangga tanpa bacaan keadaan = izin palsu.

---

## 4. VONIS: PILAR TERKUNCI SENDIRI — BUKAN DILIPAT

**Vonis: LAYAK BERDIRI SEBAGAI PILAR TERKUNCI SENDIRI (Pilar Tambahan A), dibaca LIVE tiap jendela dari sumber primer server, dengan status yang sama dengan pilar tugas & penilaian: sekali konflik, keadaan akun yang menang atas rencana.**

### Alasan dari bukti

1. **Dia bukan bagian tugas maupun penilaian — dia adalah umpan-baliknya.** Pilar tugas menjawab "apa yang boleh ditembak", pilar penilaian menjawab "jawaban dinilai bagaimana". Data keadaan menjawab pertanyaan ketiga yang berbeda jenis: **"sesudah semua verdict kemarin, kita sekarang berada di keadaan apa, dan keadaan itu mengizinkan apa?"** Saldo/LE/Expertise/REL/STOP bukan spek dan bukan rubrik; mereka adalah HASIL penilaian yang berubah menjadi SYARAT tugas berikutnya. Melipatnya ke salah satu pilar mengaburkan arah sebab-akibat ini.
2. **Dia berubah tanpa aksi dan tanpa pemberitahuan.** Verdict mendarat 85 detik sampai 22 jam sesudah submit; falsified senyap by design (MASTER §12.2); jendela usage bergeser sendiri; 22 revealed adalah utang berjalan. Data tugas/penilaian relatif statis (dibaca saat kuliti); data keadaan WAJIB dibaca ulang di awal + penutup SETIAP jendela (sudah dipraktikkan sebagai A12/C10 — tapi sebagai klausul prosedur, bukan sebagai pilar patokan; beda status itu yang diusulkan di sini).
3. **Sejarahnya: setiap kali pilar ini dibaca sebagai catatan sampingan, dia menggigit.** Caps dibaca sebagai fakta platform selama 2 hari (§13); spending limit menahan klaim 8 Nov; strategyType tercatat salah antar dokumen; RAR total dibaca aman padahal REL di −5. Empat kejadian, satu pola: keadaan akun diperlakukan sebagai latar, bukan sebagai patokan.
4. **Risiko asimetrisnya tidak simetris dengan pilar lain.** Salah baca pilar tugas = tembakan gugur. Salah baca keadaan = tembakan yang mengunci rezim berhari-hari (STOP TOTAL sejak 11 Nov), menaikkan anak tangga suspensi menuju permanent ban yang ambangnya tidak dipublikasikan, dan membuka paparan berantai (−22 potensial dari revealed). Harga salahnya beda kelas.

### Risiko bila dilipat (pelajaran make.fun, diterapkan)

Di make.fun, sisi bentuk pilar 1 (syarat deliverable: sesi terekam, gerbang transkrip, repo) dilipat ke dalam "data tugas" dan **hampir hilang** — build Salmia berdiri di atas 3 pilar buat data, tapi pijakan submitnya (kursi penulis kosong, syarat bentuk belum dibangun) tidak terbaca sampai bedah khusus memisahkannya. Pola yang sama persis mengancam di sini: bila keadaan akun dilipat ke pilar tugas, dia akan dibaca SEKALI saat kuliti (sebagai "caps 20, RAR aman") lalu tidak dibaca lagi — padahal isinya berubah tiap verdict dan tiap geseran jendela. Bukti Dialectica-nya sudah ada: angka caps/RAR di DIALECTICA-MASTER (10 Nov) hari ini salah semua bila dipakai tanpa stempel tanggal (saldo 4,1212 vs aktual −1,8788; RAR 7 vs 118; caps unlimited [used 1] vs [used 0]).

### Bentuk pilarnya (usulan isi terkunci)

Dibaca live tiap jendela, dari server, bukan dari dokumen — 7 butir: **(1)** saldo + LE + Expertise dari `/api/node/scores`; **(2)** RAR PER KOMPONEN (REL/Availability/Reputation terpisah — total saja = bacaan tidak sah); **(3)** suspensionCount + status suspensi aktif; **(4)** caps + usage jendela bergulir dari `agent show` + endpoint usage (silang-cek keduanya); **(5)** strategyType + arena + maxConcurrency (mismatch dynamic = berhenti); **(6)** status kill-metric (a)–(d) + STOP/JEDA/tangga fase, dinyatakan berangka; **(7)** paparan terbuka: cacah revealed kita yang belum berverdict. Konflik antara bacaan pilar ini dan rencana tembak apa pun → **pilar ini yang menang, tembakan ditahan**, persis perlakuan dua pilar terkunci yang sudah ada.
