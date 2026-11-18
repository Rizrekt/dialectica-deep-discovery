# GERBANG KESEGARAN DETIK-KIRIM — 2026-11-17

> Pelaksanaan ATURAN KETAT user 2026-11-17 10:50 sebagaimana diklarifikasi 10:52 (SISTEM-KENDALI, "KLARIFIKASI USER 10:52"): tugas wajib diverifikasi MASIH FRESH bukan cuma saat dipilih, tapi di detik sebelum jawaban terkirim. Dibangun saat serve STOP (terverifikasi `inactive`, nol proses) dan serve TIDAK dinyalakan; nol submit, nol generasi — cap serve nyata 10/10 tidak tersentuh. Platform sedang bersiap maintenance (banner resmi): semua bacaan live di bawah berjalan bersih (fetch `ok` di 14/14 cek), kegagalan akan dicatat terbuka bila terjadi.

## 1. Celah yang ditutup

Pemilih (`target_picker.py`) mengklasifikasi sel bayar dan gerbang liveness membuktikan ronde hidup — keduanya pada saat MEMILIH. Generasi sesudahnya makan menit, dan tidak ada cek ulang sebelum send: 5 tembakan pilot 2026-11-17 dipilih saat viso 0, pertanyaannya kebanjiran 23–59 jawaban sesudahnya (VERDICT-WATCH-2026-11-17). Dua kerugian kata user: (1) submit ke tugas kepenuhan → rawan falsified karena kebaruan sudah tertutup jawaban duluan; (2) verified pun $0 karena slot bayar (verified-pertama Pioneer +20) sudah direbut = kerja sia-sia. Gerbang ini membaca ulang keadaan live pertanyaan TEPAT sebelum teks jawaban dicetak untuk submit, dan menahan kiriman yang ruang bayarnya sudah mati.

## 2. Rancangan

- **Modul baru `provider/freshness_gate.py`** — `check_freshness(isr_id, pick_state, detail_fetcher, isos_fetcher, now, mode)` → verdict `{status: fresh|stale|closed|unverified, withhold, reasons, live, fetch}`; setiap cek tercatat satu baris di `provider/freshness-check-log.jsonl` (pola citation-check-log; path bisa dioverride `DIALECTICA_FRESHNESS_LOG`).
- **Keadaan yang dibaca (2 panggilan klien per cek, tanpa retry tambahan):** detail ISR (`serve_gate.fetch_isr_detail`) + daftar ISO (`novelty_context.fetch_isos`) — seam yang sama dengan gerbang liveness dan konteks kebaruan. `verified_now` = **maks** dari penghitung detail (`visoCount`) dan hitungan status `verified` di daftar (daftar ISO diketahui terpotong di pertanyaan raksasa — STUDI-KOHORT F4 — jadi penghitung detail menopang); `crowd_now` = jumlah ISO berstatus `revealed` + `verified` (pesaing hidup; `intent` belum jawaban, `abandoned` sudah ditarik, `falsified` sudah settle — ketiganya tetap tercatat di log untuk audit).
- **Kelas dari saat memilih, bukan saat kirim:** `vyce_serve_prepare` kini mencatat sidecar `serve-cache/<isr>.fresh.json` (kelas hasil derivasi logika sel pemilih: viso 0 → PIONEER; ronde maraton terbukti terbuka → MARATHON; selain itu GENERAL; plus viso/baseline jawaban saat pilih dari satu bacaan ISO best-effort). Tanpa sidecar (kedatangan fallback) kelas = GENERAL — aturan konservatif — dan tidak ada baseline yang diklaim.
- **Titik pasang (bedah terkecil):** `vyce_serve_provider.py`, di KEDUA titik sebelum `sys.stdout.write` — jalur cache-hit (sesudah cek liveness S5 yang sudah ada) dan jalur fallback (sesudah draf dinyatakan sendable, sebelum dicetak). Vonis TAHAN = exit 1 stdout kosong, konsekuensi yang sama persis dengan blok "terbukti mati" yang sudah berdiri (trued membuang job-nya). READY hook tidak disentuh (jendela ±10 dtk, tanpa jaringan by design); gerbang ini memang harus di titik terakhir yang masih bisa jaringan.
- **Arming (pola C5 + sitasi):** `run_serve.py` cabang serve Vyce tergating memasang `DIALECTICA_FRESHNESS_CHECK=1`. Mode `DIALECTICA_FRESHNESS_MODE`: bawaan **block**; `shadow` = catat, tidak pernah menahan.
- **Doktrin kegagalan dua lapis, sengaja dibedakan:** (a) keadaan pertanyaan tak terbaca (API error/timeout/disabled) = data → status `unverified` → **TAHAN** + tercatat (aturan ketat: tak terverifikasi ≠ lolos; ini sengaja MENYIMPANG dari `fallback_dead_reason` yang mengampuni job yang sudah diterima — veto ini pra-kirim, dan aturan user menimpanya); (b) callable gerbangnya sendiri crash (bug) = **tidak menahan**, tercatat sebagai record `crash` (doktrin tahap pemeriksa di serve_gate). K-1/K-2/C5/QUALITY/lapis sitasi tidak diubah perilakunya.

## 3. Tabel ambang per kelas + dasar data

| Kelas | Aturan TAHAN | Angka | Dasar |
|---|---|---|---|
| semua | keadaan live tak terbaca | — | aturan ketat user 10:52: tak terverifikasi ≠ lolos |
| semua | pertanyaan terbukti tutup pada detail segar (`liveness_check` MATI: settled / flag basi / ronde berakhir) | — | mekanik liveness yang sudah terkalibrasi (KULIT-SISTEM celah 1–2, §82) |
| PIONEER | verified_now ≥ 1 | 1 | definisi selnya sendiri: Pioneer = verified-pertama +20 (target_picker); satu verified saja = slot mati, verified kita pun $0 |
| PIONEER | crowd_now ≥ 10 | 10 | model kebaruan pemilih sendiri: `novelty_room(viso) = 0,95 − 0,08·viso` mencapai lantai NO-PAY 0,15 (ROOM_FLOOR) di viso 10 — pemilih menolak pertanyaan non-maraton di garis yang sama; juga ±2× peringkat masuk median pemenang kohort (±5, KORPUS-JUARA/STUDI-KOHORT) |
| MARATHON | verified_now ≥ 6 | 6 = ceil(5,85) | STUDI-KOHORT-2026-11-17 F4: rerata slot Marathon terbayar 5,85/pertanyaan pada 46 pertanyaan panel concluded — verified yang ada sudah memenuhi jatah slot wajar = slot realistis habis |
| MARATHON | (kerumunan saja: TIDAK menahan) | — | pemenang kohort justru masuk ronde rame (median peringkat masuk ±5, pita prima pemilih sampai viso 15); pengikat Marathon = slot verified + ronde terbuka (aturan tutup di atas) |
| INNOVATOR / GENERAL / tak dikenal | verified_now ≥ 6 | 6 | aturan konservatif yang sama (verified-penuh), per perintah tugas |
| INNOVATOR / GENERAL / tak dikenal | crowd_now ≥ 10 | 10 | garis lantai ruang kebaruan pemilih yang sama (0,15) — ruang kebaruan tertutup |

Catatan kejujuran ambang: garis kerumunan memakai model `novelty_room` pemilih yang variabelnya viso (verified), diterapkan di sini ke crowd (revealed+verified) karena di detik kirim daftar ISO memberi hitungan pesaing yang sebenarnya — pemetaan ini kalibrasi awal, dinyatakan terbuka di §6.

## 4. Bukti fungsi live (2026-11-17 ±11:1x WIB, read-only, pacing 1 dtk)

Skrip: `provider/prove_freshness_gate.py` + `prove_freshness_gate2.py`; hasil mentah `freshness-proof-2026-11-17.json` + `freshness-proof2-2026-11-17.json`; semua verdict juga masuk `freshness-check-log.jsonl`. Total panggilan API: 9 cek × 2 + 1 tarikan daftar = 19, semua `ok`.

**Bukti 1 — 5 pertanyaan pilot dalam keadaan SEKARANG (dipilih viso 0): KELIMANYA TERTAHAN.**

| ISR | Kelas | Verified kini | Kerumunan kini | Vonis |
|---|---|---|---|---|
| 2777178d | PIONEER | 0 | 31 | TAHAN — kerumunan ≥10 |
| d94d7e34 | PIONEER | 0 | 59 | TAHAN — kerumunan ≥10 |
| 635a010d | PIONEER | 0 | 35 | TAHAN — kerumunan ≥10 |
| d21135d5 | PIONEER | 0 | 23 | TAHAN — kerumunan ≥10 |
| 5e905bef | PIONEER | 0 | 46 | TAHAN — kerumunan ≥10 |

(Angka kerumunan cocok dengan VERDICT-WATCH 03:10–03:16 UTC: revealed 31/59/34/23/46 — 635a010d bertambah 34→35 di antaranya. Verified masih 0 di kelimanya, jadi yang menangkap murni aturan kerumunan — persis kerugian nomor 1 user.)

**Bukti 2a — 4 kandidat "segar" sapuan pemilih 09:27 (viso 0 saat disapu): KEEMPATNYA TERTAHAN** — eaa812f3 kerumunan 37 · 00a25466 kerumunan 42 · 0157919b kerumunan 71 · 1bdf1032 kerumunan 33. Dalam ±1,5 jam sejak disapu, keempatnya sudah kebanjiran. Ini bukan kegagalan bukti-lolos; ini pengukuran kecepatan lapangan: jendela "segar" di arena ini berumur menit, bukan jam — dan alasan mekanis kenapa cek detik-kirim (bukan cek yang lebih awal) yang diwajibkan aturan user.

**Bukti 2b — pertanyaan benar-benar segar: LOLOS.** Tarikan recency ketat (maxAge 15 menit, 30 baris, 8 baris viso-0 topik-inti): kandidat termuda **540643f2** (umur 110 detik, viso 0) → status `fresh`, verified 0, kerumunan 0, TIDAK ditahan — cek pertama langsung lolos, anggaran coba tidak habis.

## 5. Tes

- Baru: `provider/test_freshness_gate.py` — **36/36 PASS**, semua bermock (fetcher palsu deterministik): segar lolos per kelas · slot mati Pioneer (termasuk penghitung detail menang atas daftar terpotong) · kerumunan di atas/di bawah garis · verified-penuh Marathon/General di atas/di bawah garis · tutup terbukti (flag basi, settled) · tak terbaca → tahan di block / tak menahan di shadow · crash callable tak menahan + tercatat · arming/mode · sidecar round-trip · prepare mencatat sidecar · wiring provider (veto menahan → rc 1 stdout kosong; veto lolos/tak di-arm → jawaban cache terkirim persis seperti sebelumnya).
- Suite penuh provider sesudah pemasangan: **405 cek bernomor hijau** (baseline 369 + 36 baru), nol regresi di 16 berkas lain. Satu-satunya pengecualian sama dengan baseline: `test_improve_20261116.py` tidak terjalan penuh karena cap serve NYATA hari ini 10/10 habis (errornya persis `cap serve tercapai: 10/10`) — keadaan operasional yang memang dilarang "diperbaiki" dengan mengubah cap.
- Backup: `vyce_serve_provider.py.bak-20261117-freshgate`, `vyce_serve_prepare.py.bak-20261117-freshgate`, `run_serve.py.bak-20261117-freshgate`.

## 6. Sisa risiko (jujur)

1. **Balapan cek→kirim tetap ada, terkuantifikasi:** sesudah gerbang membaca keadaan, trued masih harus mengklaim + mengirim — jendela detik (pengiriman cache-hit) sampai menit (klaim ulang). Pada kecepatan banjir terukur hari ini (pertanyaan pilot mencapai 23–59 jawaban dalam ±35–45 menit ≈ 0,6–1,3 jawaban/menit; kandidat sapuan 33–71 dalam ±90 menit), jendela 10 detik membawa ekspektasi ±0,1–0,2 jawaban baru — tidak mengubah vonis ambang kecuali pertanyaan duduk persis di garis. Gerbang memampatkan jendela dari "menit generasi + antrian" menjadi "detik pengiriman"; menghilangkannya total mustahil tanpa dukungan server.
2. **Daftar ISO terpotong di pertanyaan raksasa** (22,7% slot Marathon menunjuk ISO di luar daftar tertarik, STUDI-KOHORT F4): crowd_now bisa KURANG dari sebenarnya → pertanyaan super-rame bisa terbaca di bawah garis. verified_now ditopang penghitung detail (`visoCount`), tapi tidak ada penghitung "revealed" di detail — mitigasi parsial saja. Garis 10 yang rendah adalah kompensasi kalibrasi awalnya.
3. **Ambang kerumunan = kalibrasi awal** dari dua jangkar (lantai ruang kebaruan pemilih + 2× peringkat masuk median pemenang), bukan dari distribusi verdict per tingkat kerumunan — data itu belum ada; log jsonl gerbang ini adalah bahan kalibrasi ulangnya (setiap vonis menyimpan hitungan persisnya).
4. **Kelas INNOVATOR tidak dibedakan mekanis** di pipa serve (tidak ada pengukuran novelty saat pilih di jalur ini) — target Innovator dinilai dengan aturan GENERAL konservatif. Bila jalur klaim manual meneruskan kelas INNOVATOR secara eksplisit lewat sidecar, aturan GENERAL yang sama tetap berlaku (memang begitu rancangannya).
5. **Biaya latensi:** +2 panggilan klien per kiriman (terukur 1,3–3,3 dtk per panggilan pada API sehat pagi ini; saat degradasi/maintenance bisa lebih, dan timeout klien 30 dtk × 2 adalah batas atasnya) — dibayar hanya pada kiriman yang benar-benar akan terkirim, bukan per kandidat.
6. **Interaksi job yang sudah diterima:** pada jalur fallback/cache-hit job SUDAH ada di tangan trued; veto membuangnya (konsekuensi §35 yang sama dengan blok liveness terbukti-mati). Itu pilihan sadar aturan ketat (mencegah falsified + kerja $0), dengan harga sesekali membuang job yang mungkin masih bernilai bila keadaan berubah di detik terakhir — tercatat per kejadian di log untuk ditimbang ulang dari data.

## 7. Keadaan akhir

Serve tetap STOP; gerbang terpasang + ter-arm untuk nyala berikutnya lewat `run_serve` (tidak ada jalur lain yang meng-arm-nya); tidak ada submit/klaim/generasi yang terjadi selama pembangunan ini. Berkas: `provider/freshness_gate.py` (baru) · `provider/test_freshness_gate.py` (baru) · `provider/prove_freshness_gate.py` + `prove_freshness_gate2.py` (baru) · `provider/freshness-proof-2026-11-17.json` + `freshness-proof2-2026-11-17.json` · `provider/freshness-check-log.jsonl` · suntingan `vyce_serve_provider.py`, `vyce_serve_prepare.py`, `run_serve.py` (backup `.bak-20261117-freshgate`) · SISTEM-KENDALI.md (entri gerbang berdiri).

---

## Addendum 2026-11-17 11:57 — Keputusan user "AMBIL RESIKO": garis kerumunan 10 → 20

- **Keputusan:** user, sesudah mendengar dasar ambang (lantai ruang kebaruan pemilih 0,15 di viso 10 + peringkat masuk pemenang), memilih **mengambil risiko**: garis TAHAN kerumunan untuk kelas **PIONEER** dan **GENERAL/INNOVATOR** dilonggarkan dari **10 → 20** jawaban hidup (revealed+verified). 20 = pita atas posisi masuk pemenang kohort; risiko kebaruan di bawah garis ini diterima sadar oleh user.
- **Perubahan kode:** `provider/freshness_gate.py` — konstanta bernama `CROWD_CAP` 10 → 20 + komentar dasar keputusan; docstring (seksi THRESHOLD GROUNDS) dan teks alasan vonis diperbarui ke dasar baru. Backup `.bak-20261117-riskon` (modul + tes).
- **Yang TIDAK berubah:** PIONEER verified ≥1 = TAHAN (slot verified-pertama mati — aritmetika, bukan selera risiko) · MARATHON verified ≥6 = TAHAN, kerumunan tetap tidak menahan Marathon · pertanyaan terbukti tutup = TAHAN · keadaan live tak terbaca = status "unverified" = TAHAN · mode bawaan block · arming `DIALECTICA_FRESHNESS_CHECK=1` sama.
- **Tes:** `test_freshness_gate.py` — kasus kerumunan kini diuji di sekitar garis baru dengan semantik ≥: **19 lolos · 20 tahan · 21 tahan** (Pioneer), General kerumunan 20 tahan + kerumunan 12 kini lolos; total **39/39 PASS** (sebelumnya 36/36). Suite penuh provider: semua berkas hijau; satu-satunya pengecualian tetap `test_improve_20261116.py` yang terhalang cap serve NYATA 10/10 hari ini (keadaan operasional; cap tidak diubah).
- **Bukti live ulang (gerbang versi baru, fetch `ok` 5/5, pacing ≥1 dtk, kelas PIONEER):** kelima pertanyaan pilot **tetap TERTAHAN** — kerumunan segar saat cek: 2777178d **31** · d94d7e34 **59** · 635a010d **35** · d21135d5 **23** · 5e905bef **46**; verified masih **0** di kelimanya, jadi yang menahan murni aturan kerumunan ≥20. Hasil ini memang yang diharapkan secara jujur: kelimanya sudah jauh di atas garis baru — pelonggaran mengubah nasib pertanyaan di pita 10–19, dan bukti ini menunjukkan garis 20 bekerja pada data nyata (vonis tercatat di `freshness-check-log.jsonl`).
- Serve tetap STOP selama perubahan ini; nol submit, nol generasi.
