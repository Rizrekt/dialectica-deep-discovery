# PERBAIKAN KOLAM DOKTRIN — Diskoneksi Serve-vs-Picker (2026-11-18)

> Satu baris: **diskoneksi terbukti struktural di lima jahitan kode (bukan kebetulan jendela) — perbaikan paling konservatif yang menutupnya SUDAH DIBANGUN di belakang `DIALECTICA_DOCTRINE_A=1` yang sama (filter unit diselaraskan ke pita 2–6 jam + prepare fail-closed untuk baris tak-terklasifikasi + layar kesegaran pra-klaim), dry-run live membuktikan irisan kolam kini 70/70 tiket DUE (dari 0/113 saat nyala), suite 595/595 hijau. DESAIN KINI FINAL (2026-11-18, §7): vonis frontier duck + gpt-5.6-sol KONVERGEN 4/4 dan sudah dilipat ke bangunan (reconsideration Q2 sisi kita + log keputusan terukur, tag fase Q3, gerbang sekuensing Q4) — suite 23/23 berkas rc=0, tes lipatan baru 13/13, dry-run irisan diulang tetap 20/20 DUE. Serve TIDAK dinyalakan; nol klaim/submit selama tugas ini.**

Perintah: berdiri user (temuan kesalahan Jalur 1 = langsung perbaiki), pemicu NYALA-DOKTRIN-A-2026-11-18 §6.1. Keadaan nyala yang dibedah: 02:13–03:28 UTC, poller serve menyajikan 12 pertanyaan, pengamat mengklasifikasi 117 (113 TELAT + 4 CEPAT) dan memarkir 113 tiket — irisan nol, nol tiket ter-release, `lane-budget.json` tak pernah terbentuk, 9 generasi terbakar.

---

## 1. BEDAH JAHITAN — di mana tiap kolam ditentukan, dan kenapa irisannya nol secara struktural

### 1.1 Kolam serve ditentukan oleh argv unit, dibekukan saat start

`provider/dialectica-serve.service` (pra-perbaikan):

```
ExecStart=... run_serve.py arenaIds=general questionMaxAgeMs=259200000 'q=wallet' ...
```

`run_serve.py` meneruskan argv itu apa adanya ke `trued serve`. Di klien (`skill-audit/pkg/dialectica/scripts/trued.py`):

- `resolve_claim_plan()` (baris 4832): query poller dibangun SEKALI dari filter argv — `ensure_search_bound(build_opportunity_query(parse_assignments(filters), capabilities))` — **tanpa limit** (halaman server bawaan = 20 baris, terukur di dry-run §4).
- `_claim_round()` (baris 4567): tiap ronde = `search_opportunities(agent_id, query)` dengan query yang sama; baris yang dicoba dibatasi `attempts = candidates[:MAX_CLAIM_ATTEMPTS_PER_ROUND]` dengan `MAX_CLAIM_ATTEMPTS_PER_ROUND = 3` (baris 4442); urutan = urutan server (untuk pencarian kata kunci: relevansi, bukan kesegaran).
- `_attempt()` (baris 4656): hook `DIALECTICA_PREPARE_CMD` jalan per baris SEBELUM klaim; pass-over dicatat `skip_until[row] = now + PREPARE_SKIP_TTL_S` dengan `PREPARE_SKIP_TTL_S = 6 jam` (baris 2988) — **di memori sesi** (hilang saat restart; jurnal nyala membuktikan: `704b56c2` disajikan ulang sesudah restart).

### 1.2 Kolam doktrin ditentukan oleh feed picker, proses terpisah

- `rate_trigger.run_observer()` (bawaan `max_age_ms=1800_000` = 30 mnt; nyala memakai jaring s.d. 6 jam): poll `target_picker.pull_candidates()` — query kapabilitas `build_opportunity_query([arenaIds=general, questionMaxAgeMs], caps, limit=100)`, **tanpa `q`**, dibatasi `ensure_search_bound`.
- `rate_trigger.MAX_CLASSIFY_AGE_S = 6 jam`: pertanyaan yang pertama teramati lebih tua dari 6 jam **ditolak diklasifikasi** (`skipped_old`) — kolam doktrin secara definisi hanya berisi pertanyaan muda.
- Hasilnya hidup di store JSON (`trigger-store.json`, `late-queue.json`) yang hanya dibaca picker, pengamat, dan prepare.

### 1.3 Satu-satunya jembatan adalah prepare — dan ia filter, bukan sumber

`vyce_serve_prepare._doctrine_lane_decision()` (pra-perbaikan) hanya berjalan untuk baris yang SUDAH dipilih poller. Untuk baris tak-terklasifikasi ia mengembalikan `(None, None)`:

```python
    rec = doctrine_a.trigger_record(store, isr_id)
    if rec is None:
        return None, None        # -> "tak terklasifikasi -> alur lama persis"
```

Tidak ada kode di mana pun yang membaca `doctrine_a.due_entries()` dan menyodorkannya ke poller; `doctrine_a.release()` hanya dipanggil dari prepare ketika serve kebetulan menyajikan ISR itu. Tiket parkir tidak pernah bisa *menarik* pekerjaan — ia hanya bisa *menumpang* pencarian orang lain.

### 1.4 Lima sebab struktural irisan nol (masing-masing cukup sendiri)

1. **Semantik query berbeda.** Serve: kata kunci `q=wallet` (subset topik sempit, urutan relevansi). Doktrin: tanpa kata kunci, jendela kesegaran. Dua himpunan yang dibangun dari aturan berbeda.
2. **Jendela umur berlawanan.** Serve ≤3 hari (didominasi pertanyaan tua/ramai — baris pertama tersaji lahir 17 Nov 17:55 UTC, 89 ISO). Doktrin menolak mengklasifikasi apa pun yang pertama terlihat >6 jam. Irisan umur yang bisa diklasifikasi DAN disajikan sempit sejak desain.
3. **Kedalaman halaman + top-3 per ronde.** Halaman serve 20 baris, yang dicoba ≤3/ronde dalam urutan server; baris kepala yang sama berulang tiap ronde (skip hanya sesudah dicoba, dan hilang saat restart). Tiket doktrin yang — andaikan masuk halaman — duduk di bawah posisi 3 tak akan tersentuh.
4. **Arah jahitan terbalik.** Prepare adalah veto hilir atas pilihan poller, bukan antrean kerja. Klasifikasi tidak pernah menjadi masukan pencarian.
5. **Lem prepare melegalkan kebocoran.** `(None, None)` untuk tak-terklasifikasi = alur lama berjalan penuh (generasi + gerbang warisan) di bawah bendera doktrin. 9 generasi mini-batch 3 terbakar persis di baris ini.

Kesimpulan bedah: mengganti arming, mode, atau ambang apa pun tidak akan mengubah hasil — selama query serve dan feed doktrin berbeda, lane doktrin tidak terpicu. Perbaikan harus menyentuh **query serve** dan/atau **arah jahitan**.

### 1.5 Ekor (a) — veto kesegaran pasca-klaim vs fakta yang sudah terbaca saat pick

Kejadian: ISR `a9408129`, job `68be9cbe` — draf lulus prepare → klaim → `vyce_serve_provider._freshness_block_reason()` menahan di detik kirim (kelas PIONEER viso-0, kerumunan 79 ≥ `CROWD_CAP` 20) → job di-drop, ISO intent `e3287902` tertinggal.

Fakta kuncinya: **seluruh masukan veto itu sudah ada saat pick.** `prepare_row` mengambil daftar ISO untuk sidecar (`freshness_gate.pick_state_from_row` mencatat `answers_at_pick` = revealed+verified) — jurnal §6.3 mencatat pick-state a9408129 sudah memuat kerumunan 79 SEBELUM klaim. Aturan yang menembak di detik kirim (`check_freshness`: PIONEER crowd ≥ 20) akan menembak identik bila dievaluasi atas payload pick. Yang tidak bisa dilihat layar pick hanyalah pertumbuhan kerumunan SELAMA generasi — itulah alasan veto detik-kirim tetap dipertahankan; layar pra-klaim adalah pintu keluar lebih awal, bukan pengganti.

**Vonis ekor (a): bisa, dan seharusnya.** Evaluasi aturan yang sama (kode yang sama, bukan implementasi ulang) atas payload pick, sebelum generasi: pass-over gratis — nol generasi terbakar, nol klaim, nol slot terkunci. Dibangun (§3).

### 1.6 Ekor (b) — slot kapasitas tunggal terkunci ±30 menit

Mekanisme, dari kode klien + konfigurasi platform:

- Klaim = `POST /api/node/agents/{id}/process-opportunity` (`claim_opportunity`, trued.py baris 4457). Sekali `assigned`, job + ISO intent lahir di server.
- Job yang provider-nya keluar 1 (veto kesegaran) dihitung `dropped` oleh `worker()` (trued.py baris 5650). Teks klien sendiri: *"The server abandons an unanswered job after its liveness timeout (~30 min), and an abandoned job costs reliability — this is not free."*
- **Tidak ada panggilan pelepas job di klien**: satu-satunya endpoint relevan adalah process-opportunity (klaim) dan daftar jobs (baca). Slot tidak bisa dikembalikan dari sisi kita.
- Expert kita `maxConcurrency = 1` (agent show, jurnal §1) → selama job drop belum timeout di server, klaim berikutnya ditolak platform: *"Agent at capacity (1/1)"* (kejadian 02:47, job `556b8068`; bebas ±03:14 ≈ 02:42 + 30 mnt; konsisten dengan `CLAIM_SKIP_TTL_S = 1800` yang dipasang klien untuk baris tertolak).

**Vonis ekor (b):** pelepasan hanya milik server (timeout liveness ±30 mnt) — tidak ada tuas kode di pihak kita. Satu-satunya mitigasi nyata adalah mencegah klaim yang akan di-drop: layar pra-klaim (ekor a) menutup persis jalur drop ini untuk sebab kerumunan/kelas; sebab lain (keadaan tak terbaca saat kirim, ruangan terisi selama generasi) tetap mungkin dan harganya tetap ±30 mnt slot + biaya reliabilitas job abandoned. Ini dicatat sebagai risiko sisa di §5.

---

## 2. OPSI DESAIN

### Opsi A — Selaraskan query serve ke pita doktrin + prepare fail-closed + layar pra-klaim **[DIBANGUN]**

- **Perubahan persis:** (i) ExecStart unit: `arenaIds=general questionMinAgeMs=7200000 questionMaxAgeMs=21600000` (buang `q=wallet` + jendela 3 hari) — serve kini mensurvei persis pita umur jendela lepas TELAT; `questionMinAgeMs` terverifikasi ada di filter teriklan server. (ii) `_doctrine_lane_decision`: tak-terklasifikasi saat doktrin armed → pass-over fail-closed (di pita selaras, baris sah sudah punya ≥2 jam untuk diklasifikasi pengamat yang poll-nya 45 dtk). (iii) `_preclaim_freshness_screen` di prepare (ekor a). Semua di belakang `DIALECTICA_DOCTRINE_A=1`; env mati = perilaku byte-for-byte lama.
- **Menutup:** lane TELAT (7 dari 10 jatah doktrin) secara struktural — dry-run §4: halaman pita berisi 70/70 tiket DUE.
- **Trade-off:** lane CEPAT tidak lagi disajikan poller (jendelanya <2 jam, di luar pita) — slot cepat hangus tak terpakai, persis perlakuan doktrin terhadap slot cepat yang tak menemukan pertanyaan sepi ("tidak dipaksa"); CEPAT memang belum pernah terverifikasi live. Kolam kata-kunci warisan (q=wallet) pensiun: nilai terukurnya 0 tembakan / 9 generasi terbakar / 12 baris tak-terklasifikasi.
- **Risiko:** balapan lag klasifikasi (baris pita yang belum sempat diklasifikasi pengamat → pass-over + skip 6 jam klien → bisa kehilangan tiket yang diklasifikasi beberapa menit kemudian); kedalaman halaman 20 lawan populasi pita (terukur 70 DUE — poller hanya perlu mencapai segelintir per hari; cap TELAT 7/hari; pass-over memutar halaman lewat skip-TTL). Keduanya di §5 + paket frontier.
- **Uji kering:** dry-run irisan live (§4) + tes unit jahitan (§3).

### Opsi B — Driver tiket di atas klaim one-shot (`trued answer <isrId>`)

- **Perubahan persis:** proses driver baru yang menonton store: tiket DUE / klasifikasi CEPAT → panggil jalur one-shot untuk ISR persis itu (`cmd_serve(one_shot_target=...)`, trued.py baris 5742). Irisan eksak menurut konstruksi, dua lane terlayani.
- **Trade-off/risiko:** jalur one-shot TIDAK melewati hook PREPARE (`claim_asking_again` langsung, tanpa `_attempt`) — generasi terjadi di job-time lewat provider jalur answer, dan veto kesegaran detik-kirim hanya terpasang di provider serve. Mengadopsi B berarti memasang ulang gerbang yang terbukti (prepare + veto) ke pipa berbeda = risiko regresi gerbang terbesar + bangunan terbesar. Serve lock juga berarti driver MENGGANTIKAN poller, bukan menemaninya. Bukan yang paling konservatif; kandidat bila frontier menilai lane CEPAT layak diperjuangkan.

### Opsi C — Hanya fail-closed di prepare (tanpa penyelarasan query)

- **Perubahan persis:** butir (ii) Opsi A saja.
- **Trade-off:** menghentikan kebocoran (9 generasi → 0 terbuang) tapi TIDAK menutup diskoneksi: halaman serve tetap terikat kata kunci — dry-run query A: ∩DUE = 1, dan itu insidental (satu pertanyaan wallet yang kebetulan terklasifikasi). Lane doktrin tetap tak terpicu. **Tidak cukup sendirian**; komponen prepare-nya sudah termasuk di A.

---

## 3. YANG DIBANGUN (Opsi A — di belakang `DIALECTICA_DOCTRINE_A=1`, backup `*.bak-20261118-poolfix`)

| Berkas | Perubahan |
|---|---|
| `provider/vyce_serve_prepare.py` | `_doctrine_lane_decision`: tak-terklasifikasi → pass-over fail-closed (alasan tercatat). Baru `_preclaim_freshness_screen()`: menjalankan `freshness_gate.check_freshness` (kode aturan yang sama persis) atas payload pick SEBELUM generasi; withhold → pass-over pra-klaim. Sidecar kini mencatat pick-state yang dinilai layar (satu fetch ISO, dipakai ulang — tidak ada fetch kedua). Env mati: semua cabang ini terlewati, perilaku lama utuh. |
| `provider/dialectica-serve.service` | ExecStart diselaraskan ke pita 2–6 jam (header rekonsiliasi 2026-11-18). File induk saja — unit TIDAK dipasang/dinyalakan (nyala = kata user). |
| `provider/test_doctrine_a.py` | Satu ekspektasi diperbarui: "tanpa klasifikasi → alur lama" menjadi "→ FAIL-CLOSED" (ekspektasi lama adalah kontrak yang dibuktikan nyala sebagai diskoneksi; versi pra-perbaikan utuh di `.bak-20261118-poolfix`). Jumlah cek tetap 50. |
| `provider/test_pool_seam.py` | BARU — 8 cek jahitan (§ di bawah). |
| `provider/dryrun_pool_intersection.py` | BARU — alat bukti irisan read-only (§4). |

**Tes jahitan baru (8/8):** armed+tak-terklasifikasi → dilewati, generasi 0 · doktrin mati+tak-terklasifikasi → alur lama persis (regresi terkunci) · CEPAT viso-0 kerumunan 79 saat pick → layar pra-klaim menahan, generator TIDAK dipanggil, tak ada sidecar · CEPAT ruangan sepi → disiapkan, sidecar = pick yang dinilai layar · TELAT due kerumunan 49 → layar TIDAK menahan (semantik lane), disiapkan · keadaan tak terbaca → tidak sampai generasi.

**Suite penuh: 22/22 berkas rc=0 — 595/595 cek hijau** (baseline repo 587 + 8 baru; `test_doctrine_a.py` tetap 50/50). `run_serve.py --dry-run` dengan argv unit baru terverifikasi mencetak rencana exec yang benar dan tidak meluncurkan apa pun.

**Yang TIDAK berubah (anti-regresi, disengaja):** gerbang isi/sitasi/K-2/liveness/rantai pemeriksa (tidak disentuh); veto kesegaran detik-kirim di `vyce_serve_provider.py` (tidak disentuh — layar pra-klaim adalah tambahan, bukan pengganti); `freshness_gate.py`, `doctrine_a.py`, `rate_trigger.py`, `target_picker.py` (tidak diubah); cap 10, mode semantik shadow, config Expert.

---

## 4. BUKTI DRY-RUN IRISAN LIVE (read-only, 2026-11-18 03:33 UTC)

Alat: `provider/dryrun_pool_intersection.py` — tiga query ditarik lewat jahitan klien yang sama dengan produksi, diiriskan lawan store doktrin hidup di disk (117 terklasifikasi, 113 parked, **70 DUE** pada jam tarik). Log: `belajar-2026-11-18/doktrin-a/dryrun-irisan-kolam.log`.

| Query | Baris | ∩ terklasifikasi | ∩ parked | ∩ DUE |
|---|---|---|---|
| A — serve saat ini (`q=wallet`, ≤3 hari) | 20 | 2 | 2 | **1** (insidental) |
| B — pengamat/picker (≤30 mnt, limit 100) | 4 | 4 | 1 | 0 |
| C — pita selaras 2–6 jam (tanpa limit) | 20 | 20 | 20 | **20** |
| C2 — pita selaras 2–6 jam (limit 100) | 70 | 70 | 70 | **70 = seluruh set DUE** |

Serve produksi memakai query tanpa limit (halaman bawaan 20) — baris C adalah angka yang akan dilihat poller sesudah perbaikan: **setiap baris di halamannya adalah tiket DUE terklasifikasi** (20/20), lawan 1/20 insidental pada query lama dan 0/12 tersaji saat nyala. Irisan tidak lagi bergantung pada kebetulan kata kunci: pita umur query = jendela lepas antrean, menurut konstruksi.

Catatan jujur: angka 70/70 adalah potret jam 03:33 UTC (populasi pita pagi itu kebetulan seluruhnya warisan klasifikasi pengamat). Klaim strukturalnya lebih sempit dan tahan: query pita hanya dapat mengembalikan pertanyaan berumur 2–6 jam — himpunan yang sama yang boleh dilepas antrean — dan fail-closed prepare menjamin baris di luar klasifikasi tidak membakar generasi.

---

## 5. RISIKO SISA & YANG DITAHAN

1. **Balapan lag klasifikasi:** baris pita yang disajikan sebelum pengamat mengklasifikasinya → pass-over fail-closed + skip 6 jam klien (PREPARE_SKIP_TTL) → tiket bisa lewat jendelanya. Mitigasi terukur: pengamat poll 45 dtk dengan jaring 6 jam; pada dry-run, halaman pita 100% terklasifikasi. **SUDAH DIPUTUS FRONTIER (Q2, §7): fail-closed FINAL + reconsideration sisi kita diterapkan; sisa risiko ini kini terukur lewat `count_lost_after_skip`, bukan diterima buta.**
2. **Lane CEPAT yatim di Opsi A:** tidak ada mekanisme penyaji untuk tiket <2 jam. **SUDAH DIPUTUS FRONTIER (Q1, §7): dibiarkan hangus FINAL; Opsi B ditunda bersyarat (dibangun hanya bila run terukur membuktikan nilai peluang cepat yang hilang melebihi cakupan telat + biaya B).**
3. **Drop pasca-klaim sebab lain tetap berharga ±30 mnt slot** (ekor b): layar pra-klaim menutup sebab kerumunan/kelas/tak-terbaca-saat-pick; ruangan yang terisi SELAMA generasi hanya terlihat veto detik-kirim, dan drop-nya tetap mengunci slot sampai timeout server. Tidak ada tuas pelepas di pihak kita (terbukti §1.6). **Mitigasi tambahannya kini GERBANG SEKUENSING Q4 (§7): tidak ada klaim/ganache baru di atas job yang belum terminal-pasti.**
4. **PENETAPAN DESAIN: FINAL per 2026-11-18 (§7)** — vonis duck + gpt-5.6-sol konvergen 4/4 (penengah tidak dipanggil) dan pelipatannya sudah diterapkan + teruji. Tidak ada nyala ulang dalam tugas ini — izin batch 3 sudah habis sebagai jendela (0 tembakan); nyala berikutnya kata user terpisah.

## 6. Keadaan akhir

- Serve: **STOP** (tidak dinyalakan selama tugas ini; unit tidak dipasang ulang).
- Nol klaim, nol submit, nol perubahan config Expert; tarikan API hanya pencarian peluang read-only + baca store.
- Berkas baru/diubah: `PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md` (ini), `FRONTIER-PAKET-PERBAIKAN-JALUR1.md`, `provider/vyce_serve_prepare.py`, `provider/dialectica-serve.service`, `provider/test_doctrine_a.py`, `provider/test_pool_seam.py` (baru), `provider/dryrun_pool_intersection.py` (baru); backup `*.bak-20261118-poolfix` untuk ketiga berkas yang diubah.
- **Pelipatan frontier (§7, 2026-11-18):** `provider/vyce_serve_prepare.py` (keputusan tercatat + gerbang sekuensing Q4), `provider/freshness_gate.py` (tag fase Q3), `provider/doctrine_a.py` (log keputusan + `count_lost_after_skip`), `provider/test_pool_seam.py` (env log diarahkan ke tmp), `provider/test_frontier_fold.py` (BARU, 13 cek); backup `*.bak-20261118-frontierfold` untuk keempat berkas yang diubah.

---

## 7. VONIS FRONTIER & DESAIN FINAL (2026-11-18 — FINAL)

Konsultasi F-31D tuntas 10:38–10:42 WIB: duck.ai GPT-6 Luna (kursi utama) + gpt-5.6-sol via CrowLLM (co-advisor), paket publik-aman yang sama ke dua kursi. **KONVERGEN 4/4 — penengah gemini-3.1-pro TIDAK dipanggil.** Otoritas: `belajar-2026-11-18/frontier-perbaikan-jalur1/SINTESIS-FRONTIER-PERBAIKAN-JALUR1.md` (+ mentah `duck-answer.md` / `sol-answer.md` di folder yang sama). Status berkas ini: **FINAL per 2026-11-18** — penetapan di bawah mengikat; yang berubah dari status pra-konsultasi dinyatakan eksplisit per butir.

### Q1 — Struktur: Opsi A vs B

- **duck:** A sekarang; B ditunda. A menutup kegagalan terukur (irisan 1 vs 70/70) dan 7 dari 10 jatah tanpa jalur klaim kedua; nilai sel cepat 0,88–0,93 layak diukur, tidak cukup membenarkan bangunan + risiko regresi terbesar B sebelum lane telat bekerja. Pembatal: run terukur yang menunjukkan nilai peluang cepat yang hilang > cakupan telat sesudah biaya implementasi + reliabilitas B dihitung.
- **sol:** A; lane cepat dibiarkan hangus. Infrastruktur fast-entry (latensi sub-detik, sinkronisasi presisi) terlalu mahal untuk arsitektur slot-tunggal; drift mengejar cepat akan mengkanibal hasil telat yang lebih stabil (0,50). Pembatal: kenaikan ≥15% volume peluang harian di pita <2 jam yang tidak tertangkap klasifikasi kolam pengamat.
- **PENETAPAN FINAL: OPSI A FINAL.** Lane cepat dibiarkan hangus untuk sekarang; Opsi B **ditunda bersyarat** — dibangun hanya bila syarat pembatal salah satu kursi terbukti dari run terukur. **Perubahan dari pra-konsultasi:** status A naik dari "dibangun, penetapan ditahan" menjadi FINAL; B turun dari "kandidat desain terbuka" menjadi "tertunda bersyarat dengan pemicu tertulis".

### Q2 — Fail-closed + reconsideration

- **duck:** fail-closed TETAP selama doktrin armed — TAPI skip 6 jam jangan diterima sebagai kebijakan lag final: baris yang dilewati harus bisa **dipertimbangkan ulang** saat klasifikasinya berubah atau tiketnya jatuh tempo (reconsideration, bukan fail-open ke pipa warisan). Pembatal: hitungan terukur tiket jatuh-tempo yang baru terklasifikasi sesudah skip pertamanya lalu hilang sebelum jendela tutup, dengan nilai hilang > biaya fail-open terbatas ketat.
- **sol:** fail-closed. Fail-open berbasis ambang aman ditolak: laju bakar 9/10 adalah bencana yang tak boleh diulang; melindungi jatah generasi yang terbatas lebih penting daripada tangkapan marjinal jendela lag klasifikasi. Pembatal: run uji fail-open dengan probabilitas verdict >0,40 pada baris tak-terklasifikasi tersaring urutan relevansi server.
- **PENETAPAN FINAL: FAIL-CLOSED FINAL + PENYEMPURNAAN DUCK (reconsideration) WAJIB.** Fail-open terukur **ditolak dua kursi** — tidak dibangun dalam bentuk apa pun.
- **Penerapan (butir a):**
  - **TERAPAN — sisi kita tidak ikut mengunci.** `_doctrine_lane_decision` kini membaca ulang trigger store pada SETIAP panggilan dan memutuskan dari record TERKINI: record klasifikasi ditimpa pengamat tanpa syarat (`record_classification` menimpa; TUNGGU diputus ulang pengamat pada +30 mnt), dan status jatuh-tempo TELAT dihitung live dari antrean saat prepare. Baris yang dilewati saat tak-terklasifikasi/TUNGGU/belum-due diputus FRESH pada penyajian berikutnya. Dibuktikan tes: pass-unclassified → klasifikasi TELAT-due masuk → penyajian ulang disiapkan; pass-TUNGGU → record diputus ulang jadi TELAT-due → disiapkan (`test_frontier_fold.py` Q2, 2 cek).
  - **TERAPAN — keputusan kini tercatat & terukur.** Setiap keputusan doktrin di prepare (pass/proceed/hold + kelas alasannya: `unclassified`/`wait`/`not_due`/`lane_spent`/`due`/`fast_ok`/`job_sequence`) ditambahkan ke log keputusan append-only (`doctrine_a.log_decision`, bawaan `provider/doctrine-decision-log.jsonl`, env `DIALECTICA_DOCTRINE_LOG`). `doctrine_a.count_lost_after_skip()` menghitung persis ukuran pembatal duck: tiket yang pernah dilewati saat belum actionable, lalu KEDALUWARSA di antrean tanpa pernah di-proceed di dalam jendelanya [release_at, expires_at] (tiket yang di-proceed di dalam jendela tidak dihitung hilang; yang masih parkir belum hilang). Tes fixture: hitungan tepat 1 dari 3 skenario.
  - **KETERBATASAN TERCATAT — skip 6 jam klien stok tidak bisa ditimpa dari lapisan kita.** Mekanismenya hidup penuh di klien stok: konstanta `PREPARE_SKIP_TTL_S = 6 jam` (trued.py:2988, tanpa jahitan env), peta `skip_until` di memori sesi thread klaim, diset pada SETIAP pass-over prepare (trued.py:4680), dan baris tersaring dari kandidat SEBELUM prepare dipanggil (trued.py:4588) — selama skip aktif, prepare tidak pernah dipanggil untuk baris itu, jadi tidak ada kode lapisan kita yang bisa memicu reconsideration di dalam jendela skip. Skip hilang hanya saat kedaluwarsa atau sesi serve restart (memori sesi; jurnal nyala membuktikan `704b56c2` tersaji ulang sesudah restart). Menambalnya berarti mengedit klien stok — di luar lapisan kita dan di luar konservatisme perbaikan ini; TIDAK dipaksa. **Ukuran yang memutuskannya:** `count_lost_after_skip()` atas log keputusan + store + antrean dari run produksi berikutnya — bila hitungan tiket hilang pasca-skip > 0 dengan nilai (jatah TELAT 7/hari × peluang verdict telat ±0,50) melebihi biaya fail-open terbatas menurut ambang pembatal duck, pertanyaan Q2 dibuka lagi ke frontier dengan angka itu, bukan dengan cerita.

### Q3 — Evaluasi ganda: tata cara

- **duck:** layar dipakai + veto dipertahankan; "lolos pick, gagal kirim" adalah race yang diharapkan. Utamakan data pick yang SUDAH tercatat sebelum menambah bacaan API; LOG kedua vonis + alasan bedanya. Pembatal: ukuran produksi bahwa bacaan tambahan menunda polling / menghilangkan tiket jatuh-tempo melebihi nilai drop pasca-klaim yang dicegah.
- **sol:** evaluasi dua kali; manfaat mitigasi mengalahkan risikonya. Rasa aman palsu adalah risiko proses yang dikelola lewat dokumentasi; biaya baca API dapat diabaikan dibanding penalti kelumpuhan 30 menit. Pembatal: bottleneck terukur di mana logika evaluasi-ganda konsisten mendorong latensi klaim melewati ambang rebut pesaing.
- **PENETAPAN FINAL: EVALUASI GANDA FINAL** (layar pra-klaim + veto detik-kirim, keduanya menjalankan kode aturan yang sama) dengan tata cara duck sebagai kewajiban tercatat.
- **Penerapan (butir b):**
  - **TERPENUHI (sudah begini sejak perbaikan kolam) — prioritas data pick.** Layar menilai payload pick yang diambil SATU kali; sidecar mencatat persis pick yang dinilai layar (bukan fetch kedua), dan veto detik-kirim menilai lawan pick tercatat itu sebagai baseline (`vyce_serve_prepare.prepare_row` + `freshness_gate.armed_freshness_veto` membaca sidecar). Tidak ada bacaan API baru per baris di luar satu fetch layar.
  - **TERAPAN — kedua vonis tercatat di log yang sama dengan fase + alasan.** `check_freshness` menerima parameter `phase` yang ditulis ke record log: layar memanggil dengan `phase="pra-klaim"`, veto detik-kirim (termasuk record crash-nya) dengan `phase="detik-kirim"` — keduanya masuk `freshness-check-log.jsonl` yang sama, masing-masing membawa `reasons`-nya sendiri. Divergensi antar-dua record satu ISR (mis. sepi saat pick, kerumunan 79 saat kirim → layar fresh, veto stale-menahan) terbaca langsung dari log sebagai race normal. Tes: kedua fase tercatat di berkas log yang sama, record detik-kirim menahan dengan alasannya (`test_frontier_fold.py` Q3, 2 cek).

### Q4 — Sekuensing klaim konservatif

- **duck:** WAJIB — layar saja tidak cukup. Jangan klaim lagi selagi hasil job sebelumnya belum pasti; tunggu hasil terminal definitif atau timeout liveness server. Pembatal: jaminan server terbukti bahwa klaim terlepas atomik / tak bisa menempati slot sesudah job drop — yang menurut setup ini tidak ada.
- **sol:** WAJIB — gerbang cek-keadaan yang mencegah inisiasi klaim-draf sampai hasil job sebelumnya (sukses/gagal) terkonfirmasi lewat polling status; layar pra-klaim adalah pencegahan, bukan fail-safe. Pembatal: data log bahwa 90% drop pasca-klaim terjadi karena heartbeat server tiba sebelum sinyal lepas klaim.
- **PENETAPAN FINAL: SEKUENSING KONSERVATIF WAJIB.** Layar saja dinyatakan TIDAK CUKUP oleh dua kursi.
- **Penerapan (butir c) — DIBANGUN (bukan sudah dijamin):** alur serve yang ada TIDAK menjamin sekuensing ini. Buktinya struktural: di klien stok, `claim_poller` berjalan di thread-nya sendiri paralel dengan loop penjawab job ("It runs on its own thread; the poll keeps running underneath" — komentar trued.py di atas `report_outcomes`), dan `_claim_round`/`_attempt` tidak memeriksa keadaan job apa pun sebelum prepare + klaim; kejadian nyala 02:47 (klaim ditolak "Agent at capacity (1/1)" oleh server sesudah prepare jalan) adalah perilaku itu terukur. Karena itu gerbang dibangun di satu-satunya hook pra-klaim milik lapisan kita — prepare, SESUDAH keputusan lane dan SEBELUM layar + generasi (`_job_sequence_block` di `vyce_serve_prepare.py`):
  - Membaca daftar jobs Expert sendiri lewat jahitan klien yang sama dengan fetch gerbang lain (`GET /api/node/agents/{id}/jobs`, hanya saat fetching ter-arm `DIALECTICA_SERVE_GATE_FETCH=1` — run_serve meng-arm-nya untuk lane tergating).
  - Job dalam keadaan terminal memakai kosakata klien sendiri: `TERMINAL_JOB_STATES = {completed, failed, cancelled, abandoned}` (trued.py:4286). **Ada job apa pun di luar himpunan itu (atau tanpa status terbaca) → baris DITAHAN** (pass-over + tercatat `hold/job_sequence` di log keputusan). **Daftar jobs tak terbaca → DITAHAN juga** (tak terbaca = belum terminal-pasti, persis pemicu gerbangnya). Hanya "disabled" (launcher tidak meng-arm fetching — konfigurasi peluncuran, bukan ketidakpastian runtime) yang membuat gerbang nonaktif.
  - Biaya jujur, dicatat: baris yang ditahan menerima skip sesi klien seperti pass-over lain, jadi baris TELAT yang ditahan di belakang job sekarat bisa kehilangan jendelanya untuk sesi itu. Vonis frontier menerima sekuensing konservatif dengan mekanik skip di atas meja; alternatifnya (generasi dulu, ditolak at-capacity kemudian) membakar generasi DAN tetap men-skip barisnya.
  - Tes: job `assigned` → tahan sebelum generasi + tercatat; daftar tak terbaca → tahan; semua terminal (`completed` + `abandoned`) → jalan; disabled → nonaktif (`test_frontier_fold.py` Q4, 5 cek).

### Angka akhir pelipatan

- **Tes lipatan baru: 13/13 hijau** (`provider/test_frontier_fold.py`: Q2 ×6, Q3 ×2, Q4 ×5).
- **Suite penuh: 23/23 berkas rc=0, nol regresi** — terhitung 627 cek hijau (546 dari 20 berkas format ALL PASS + ask_driver 19 + length_floors 32 + openrouter_wrapper 30). Tiga suite yang disentuh langsung tetap utuh: jahitan kolam 8/8, doktrin 50/50, kesegaran 39/39.
- **Dry-run irisan diulang** (2026-11-18 03:45 UTC, read-only, log `belajar-2026-11-18/doktrin-a/dryrun-irisan-frontierfold.log`): query pita C = 20/20 DUE di halaman produksi; C2 = 73/73 DUE dari store hidup (73 due saat tarik); query lama A tetap 1 insidental. Jahitan kolam tidak berubah oleh pelipatan.
- **Larangan dipatuhi:** serve tetap MATI, nol klaim/submit, nol config Expert, nol panggilan relay selama pelipatan (konsultasi sudah selesai — ini pelipatan vonisnya). Semua perubahan di belakang `DIALECTICA_DOCTRINE_A=1`, backup `*.bak-20261118-frontierfold`.
