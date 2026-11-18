# NYALA MINI-BATCH 3 — DOKTRIN A (2026-11-18)

**Izin:** kata user 2026-11-18 09:04 WIB — "Nyala mini-batch 3 — Doktrin A" (tercatat SISTEM-KENDALI.md "NYALA MINI-BATCH 3 DISETUJUI"). Batas keras: tepat **3 tembakan**, semua gerbang ter-arm (sitasi block, isi block, kesegaran sadar-lane, rantai pemeriksa mewarisi shadow), kill-metric bersenjata + peringatan dini refutasi. Bukan izin: tembakan ke-4+, ubah mode gerbang, ubah cap, nyala lanjutan.

**Status berkas: TUNTAS — unit berhenti 03:28 UTC, keadaan akhir terverifikasi API primer (§5).**
**Hasil satu baris:** nyala berjalan 02:13–03:28 UTC (dua sesi, satu jeda pengawas) — **0 tembakan terkirim dari 3 yang diizinkan**; 9 generasi terbakar (1 slot cap tersisa); BUKAN karena doktrin gagal di lane-nya, melainkan karena **himpunan target yang disajikan poller serve tidak pernah beririsan dengan kolam terklasifikasi doktrin** (12/12 baris yang disajikan tak-terklasifikasi — pertanyaan lama/ramai di luar jendela pengamat), dan setiap draf yang lahir ditahan gerbang yang memang dirancang menahannya (isi ×3, K-2 ×2, sitasi+isi ×1, kesegaran ×1 pasca-klaim, kapasitas platform ×1). Nol eksposur verdict baru; saldo tidak bergerak.

---

## 1. Pra-terbang (2026-11-18 02:05–02:12 UTC — semua hijau)

- **Sesi Expert hidup:** `trued.py status` → saldo **−1,8788 $TRUED** (persis baseline), RAR **123**, Expertise 0, notifikasi belum-terbaca 0.
- **Identitas:** `agent show` → Expert **8522c990-d4f6-4155-a326-3c3c9802b950**, nama **AGENT.AkTa**, strategyType **dynamic**, enabled True, state configured, **tidak suspended**; caps server unlimited [used 5 ISR/24 jam — kiriman kemarin masih di jendela geser]; contextWindowTokens 160.000; maxConcurrency 1; arena general.
- **Counter generasi serve hari ini (UTC): 0** (`vyce_serve_common.serve_generations_today()`, lane `vyce-serve`) — jatah mini-batch utuh.
- **Unit systemd:** `/etc/systemd/system/dialectica-serve.service` ADA (identik dengan salinan induk `provider/dialectica-serve.service`, ExecStart lane Vyce tergating) — loaded, **inactive, disabled** (tidak perlu pasang ulang).
- **Arming Doktrin A:** drop-in `/etc/systemd/system/dialectica-serve.service.d/doctrine-a.conf` (`Environment=DIALECTICA_DOCTRINE_A=1`) dipasang + daemon-reload; `systemctl show` mengonfirmasi env unit memuat `DIALECTICA_DOCTRINE_A=1`. `run_serve.py` cabang gated meng-arm sendiri: semantik C5 (mode warisan `DIALECTICA_SEMANTIC_MODE` = shadow, tidak diubah), `DIALECTICA_CITATION_CHECK=1`, `DIALECTICA_CONTENT_CHECK=1`, `DIALECTICA_FRESHNESS_CHECK=1`, `DIALECTICA_CHECKER_CHAIN=1`, dan meneruskan `DIALECTICA_DOCTRINE_A=1` dari env operator.
- **Keputusan waktu start (dicatat terbuka):** unit distart ±02:57 UTC, beberapa menit sebelum jendela lepas TELAT pertama (03:03:35 UTC) — meminimalkan paparan alur-lama pada target tak-terklasifikasi sebelum ada tiket yang jatuh tempo, tanpa mengorbankan satu pun jendela lepas. Pengamat laju jalan lebih dulu (sejak 02:12 UTC) supaya klasifikasi segar seutuhnya.

## 2. Antrean (store doctrine_a, dibaca 02:05 UTC)

- `late-queue.json`: **23 entri `parked`**, semua terbaca sehat — warisan dry-run 08:26–08:45 WIB, lahir 01:03:35–01:43:04 UTC, jendela lepas **lahir+2 jam s.d. +6 jam** → lepas pertama **03:03:35 UTC** (b8fdea26), terakhir 03:43:04 UTC; kedaluwarsa 07:03–07:43 UTC. Belum ada yang kedaluwarsa; semua masih di dalam jendela pada jam start.
- `trigger-store.json`: 23 record klasifikasi (semua TELAT — rezim banjir pagi).
- `lane-budget.json`: belum ada (token lane pertama diambil hanya sesudah draf lolos gerbang — perilaku terdesain).
- Pengamat `rate_trigger.py` dijalankan pendamping sejak 02:12 UTC (poll 45 dtk, read-only; log `belajar-2026-11-18/doktrin-a/observer-nyala-2026-11-18.log`) untuk mengklasifikasi pertanyaan segar selama nyala.

## 3. Jurnal nyala

**Insiden pra-start (±02:15 UTC):** layanan/VM restart di tengah masa tunggu — berkas unit + drop-in di `/etc` HILANG (sifat ephemeral /etc, persis risiko yang diantisipasi tugas) dan proses pengamat pertama mati. Keadaan workspace utuh: antrean justru bertambah jadi **31 entri parked** (pengamat pertama sempat mengklasifikasi 8 pertanyaan TELAT baru sebelum mati; lepas pertama tetap 03:03:35 UTC, terakhir 04:00:06 UTC), counter tetap **0**, tidak ada log serve (serve tidak pernah start — nol tembakan tak disengaja). Pemulihan di giliran yang sama: unit dipasang ulang dari salinan induk + drop-in Doktrin A ditulis ulang + daemon-reload (terverifikasi inactive + disabled + env memuat `DIALECTICA_DOCTRINE_A=1`); saldo dibaca ulang **−1,8788 / RAR 123** (sesi selamat); pengamat kedua dijalankan (poll 45 dtk, log `observer-nyala2-2026-11-18.log`) dan langsung mengklasifikasi TELAT baru. Jam VM terbaca ±5 menit lebih muda sesudah restart — jendela lepas dihitung dari epoch platform di store, dampaknya hanya pergeseran menit di dalam jendela 2–6 jam, tidak mengubah keabsahan tiket.

**Start pertama 02:13 UTC** (dimajukan dari rencana 02:57 karena tiket CEPAT live pertama muncul: ISR `126b77b4-d48d-4cd7-abed-6d17d564da10`, first2min=0, terklasifikasi 02:12:34 UTC — tiket cepat mudah busuk). Log start mengonfirmasi arming penuh: "DOKTRIN A armed oleh operator" + semantik shadow + rantai pemeriksa + sitasi/isi/kesegaran mode block. MainPID 2192.

**Fase 02:13–02:20 UTC — nol tembakan, unit dihentikan sementara oleh pengawas (keputusan tercatat):**
- Poller serve menyajikan baris dari pencariannya sendiri (q=wallet) yang himpunannya TIDAK sama dengan feed picker yang diklasifikasi pengamat. Dua baris pertama yang disajikan **tak-terklasifikasi** (tidak ada di trigger store): `704b56c2` (lahir 17 Nov 17:55 UTC, 89 ISO — di luar segala jendela doktrin) dan `43531ab2`.
- `704b56c2`: generasi GLM 6.617 kar (counter 0→1) → **ditahan gerbang serve** di tahap withhold (pass-over sebelum klaim, 02:19 UTC) — gerbang bekerja persis sebagaimana dirancang atas target di luar doktrin. `3e6c5c64` gugur liveness (pola flag basi, sama seperti kemarin).
- `43531ab2`: generasi gpt-oss-120b (fallback penulis menyala) 02:19:47 (counter 1→2), masih di tahap gerbang saat unit dihentikan → prepare diabandon oleh klien, **tidak ada klaim/submit** (grep "submitted" di log = 0; lane-budget belum ada = nol token lane terambil).
- **Keputusan pengawas 02:20 UTC: unit STOP sementara, restart ±03:01 UTC.** Alasan: pada laju bakar saat itu, cap generasi harian (10) terancam habis oleh draf tertahan di baris tak-terklasifikasi SEBELUM satu pun tiket TELAT jatuh tempo (lepas pertama 03:03:35) — mengalahkan maksud izin (3 tembakan lane terklasifikasi). Sisa anggaran generasi 8 disimpan untuk jendela saat tiket TELAT benar-benar due. Tiket CEPAT 126b77b4 tidak disajikan poller selama 8 menit fase ini; slot cepat memang boleh hangus, tidak dipaksa.
- Pengamat diperlebar di tengah fase: net maxAge 6 jam (observer3, sejak ±02:17 UTC) — antrean tumbuh 36 → **76 parked**; sebagian tiket observer3 (lahir ±00:20 UTC) sudah melewati jam lepasnya (lahir+2 jam) dan akan berstatus due seketika saat serve restart.

**Restart 02:23 UTC** (PID 3136; keputusan dimajukan dari 03:01 karena observer3-net-lebar menemukan 44 tiket TELAT sudah due — lahir ±00:20 UTC, lepas lahir+2 jam sudah lewat). Jurnal fase kedua (semua jam UTC):

| Jam | Kejadian |
|---|---|
| 02:24 | `704b56c2` disajikan ulang (skip-TTL per-sesi hilang saat restart) → generasi GLM #3 (7.682 kar) |
| ±02:29 | `704b56c2` **ditahan gerbang isi** (1 klaim poros unsupported) — tahan isi kedua untuk ISR ini |
| 02:30 | `43531ab2` generasi gpt-oss #4 (5.960 kar) → **ditahan lantai K-2** (rasio 0,119 < 0,30) |
| 02:37 | `bce59190` generasi GLM #5 (7.984 kar) → **ditahan gerbang sitasi (3 temuan penunjuk poros mati/salah-dokumen) + gerbang isi** sekaligus |
| 02:42 | `a9408129` generasi GLM #6 (9.077 kar) → draf LULUS semua gerbang prepare → **klaim job `68be9cbe`** → **gerbang kesegaran detik-kirim MENAHAN** (kelas PIONEER viso-0, tapi kerumunan 79 jawaban hidup ≥ garis 20) → job di-drop provider, **tidak ada yang terkirim**; ISO intent `e3287902` tertinggal di server (artefak klaim, tanpa isi jawaban) |
| 02:47 | `556b8068` generasi GLM #7 (9.391 kar) → draf lulus prepare → **klaim DITOLAK platform: "Agent at capacity (1/1)"** — slot tunggal Expert masih diduduki job drop a9408129 sampai timeout liveness servernya (±30 mnt, s.d. ±03:14) |
| 02:52 | `166fb876` generasi GLM #8 (7.459 kar) → **ditahan lantai K-2** (rasio 0,286 < 0,30 — 2 dari 7 token angka) |
| 02:56 | `81cbb4ae` generasi GLM #9 (9.572 kar) → **ditahan gerbang isi** (1 klaim poros unsupported) |
| sela | Pass-over liveness (0 generasi): `3e6c5c64` ×2, `b3f1fcc3`, `8fda999b`, `7b02512e`, `baa4f0f2` — semua pola flag basi pasca-ronde |
| ±03:05 | Log: **"everything that matched has already been tried"** — himpunan cocok sesi ini habis; serve masuk loop cari-ulang 60 dtk (429 platform berlanjut) |
| 03:20 | `556b8068` disajikan ulang (satu-satunya baris "not tried recently") → prepare ulang gagal di **generasi**: rantai penulis jatuh ke lane Cloudflare → **429 "daily free allocation of 10,000 neurons" habis** → GenerationError, pass-over, counter tetap 9 |
| 03:28 | **Unit STOP oleh pengawas** (keputusan jendela-terbatas, lihat §4) — loop idle berlanjut tanpa baris baru; tidak ada kejadian tertunda |

**Gerbang yang terbukti jalan LIVE pertama kali di nyala ini:** verifikasi isi mode block (3 tahan) · verifikasi sitasi mekanis mode block (1 tahan, berbagi dengan isi) · gerbang kesegaran detik-kirim mode block (1 tahan pasca-klaim) · rantai pemeriksa berjalan di dalam tahap semantik shadow (tidak menahan — sesuai mode warisannya). Gerbang lama: K-2 (2 tahan), liveness (6 pass-over). **Lane doktrin: TIDAK PERNAH terpicu** — 0 dari 12 baris tersaji ada di trigger store; `lane-budget.json` tidak pernah terbentuk (nol token lane terambil); 0 tiket antrean ter-release lewat prepare.

**Pengamatan pendamping:** trigger store akhir memuat **113 TELAT + 4 CEPAT** (3 tiket CEPAT tambahan terklasifikasi selama nyala — tidak satu pun disajikan poller serve). Antrean akhir: 113 `parked` (kedaluwarsa sendiri mulai 07:03 UTC).

## 4. Pemicu berhenti — hasil

- (a) tembakan ke-3 terkonfirmasi → **tidak tercapai** (0 tembakan).
- (b) falsified pertama atas jawaban batch ini → **tidak bunyi** (tidak ada jawaban terkirim untuk difalsifikasi).
- (c) refutasi pertama pada jawaban batch ini → **tidak bunyi** (tidak ada jawaban revealed milik batch ini).
- (d) mismatch identitas / preview kotor → **tidak bunyi** (identitas terverifikasi konsisten; tidak ada transaksi di luar gas — serve tidak menyentuh dana sama sekali).
- **Yang menghentikan nyala:** keputusan pengawas jendela-terbatas 03:28 UTC — himpunan target yang dapat dijangkau sesi ini terbukti habis ("everything that matched has already been tried" berulang sejak ±03:05, satu-satunya penyajian ulang gagal di generasi karena neuron Cloudflare harian habis), bayangan kapasitas sudah lewat tanpa baris baru, dan restart hanya akan membakar slot generasi terakhir pada baris basi yang sama. Slot cap ke-10 sengaja DISIMPAN (reset 00:00 UTC). Status sesudah tutup: **BUKAN JEDA kill-metric** — tidak ada falsified/refutasi; ini penghentian operasional bersih dengan nol tembakan.

## 5. Keadaan akhir terverifikasi (API primer, 03:28–03:31 UTC)

- **Saldo −1,8788 $TRUED, RAR 123, Expertise 0** — persis baseline pra-terbang; tidak bergerak seharian.
- **Counter generasi serve hari ini: 9/10** (9 record `vyce-serve` di token-usage: GLM ×7, gpt-oss-120b ×2 — fallback penulis menyala 2×; rincian per generasi di §3).
- **Tembakan terkirim: 0.** Verifikasi per ISR dari endpoint ISO: 11 dari 12 ISR tersaji memuat **0 ISO milik Expert kita**; satu-satunya artefak = ISO `e3287902` status **`intent`** di `a9408129` (sisa klaim job 68be9cbe yang di-drop gerbang kesegaran — tanpa isi jawaban, tidak bisa di-verdict; akan berstatus abandoned oleh timeout server, biaya reliabilitas sesuai catatan klien, bukan eksposur falsified).
- **Tidak ada jawaban batch ini** → tidak ada yang perlu dipantau verdict/refutasinya dari batch ini. (22 jawaban revealed lama + 5 pilot tetap urusan verdict-watch sesi utama seperti sebelumnya — di luar nyala ini.)
- **Unit:** `inactive` + `disabled` (autostart tidak pernah di-enable selama nyala ini) ✓. Drop-in `doctrine-a.conf` dibiarkan terpasang (tidak berpengaruh saat unit mati; mencatat arming untuk nyala berikut). Proses pengamat dimatikan bersih.
- **Yang TIDAK berubah:** cap 10, mode semantik shadow, config Expert, strategi, status klaim one-shot (STOP TOTAL tidak disentuh).

## 6. Temuan struktural untuk sesi utama (bahan keputusan, bukan eksekusi)

1. **Diskoneksi kolam target:** pencarian serve (q=wallet, jendela 3 hari) dan feed picker/pengamat (query kapabilitas, ≤6 jam) menghasilkan himpunan yang **praktis disjoin** pagi ini — doktrin mengklasifikasi 117 pertanyaan, serve menyajikan 12, irisannya **nol**. Selama jembatan ini tidak ada, lane doktrin tidak akan pernah terpicu oleh serve apa pun arming-nya. Ini temuan penerbangan pertama yang menentukan: perbaikannya keputusan desain sesi utama/user (mis. serve diarahkan ke kolam picker, atau pengamat diperluas ke himpunan serve), BUKAN sesuatu yang boleh diubah dari dalam nyala.
2. **Gerbang baru lulus uji produksi:** isi + sitasi + kesegaran (semua mode block, pertama kali terbang) menahan 5 dari 8 draf yang mencapai tahapnya — termasuk pola persis yang dulu meloloskan pilot (klaim poros unsupported + penunjuk mati). Tanpa mereka, nyala ini kemungkinan besar mengirim 2–4 jawaban ke ruangan mati/ramai.
3. **Biaya ekor veto pasca-klaim:** job yang di-drop gerbang kesegaran menduduki slot konkurensi tunggal ±30 menit dan meninggalkan ISO intent — veto detik-kirim bekerja, tapi harganya nyata; kandidat pertimbangan desain (veto setara di tahap prepare untuk kelas/kerumunan yang sudah terbaca ramai saat pick — pick-state a9408129 sebenarnya sudah mencatat kerumunan 79 saat pick, sebelum klaim).
4. **Neuron Cloudflare harian habis** sebelum 03:20 UTC (gabungan pemakaian pagi: kalibrasi 4.786 + jalur fallback serve) — lane cadangan penulis terakhir tidak tersedia di sisa hari ini; GLM juga gagal sesekali (fallback menyala 2×). Ketahanan rantai penulis = bahan perhatian untuk nyala berikut.
