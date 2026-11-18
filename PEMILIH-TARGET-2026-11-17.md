# PEMILIH TARGET SEL BAYAR — Dialectica (dibangun 2026-11-17, fase testing)

> Perintah user 2026-11-17 06:19 ("gas satu-satu, jalan", item 1 dari daftar belum-siap). Alat **SHADOW / READ-ONLY**: tidak mengklaim, tidak serve, tidak submit, tidak mengubah config/cron. Kode: `provider/target_picker.py` · tes: `provider/test_target_picker.py` · hasil run mentah: `provider/picker-shadow-2026-11-17.json`.

## 1. Desain

Pemilih menambah **lapisan kelas-bayar** di atas saringan seleksi yang sudah ada — bukan menggantikannya:

- **Liveness** = `serve_gate.liveness_check` (tiga-field, fail-closed) — fungsi yang sama dengan gerbang serve.
- **Topik inti** = `cloudflare_serve_common.CORE_TOPIC_KEYWORDS` — kata kunci yang sama dengan saringan Kelas 2 (identitas/wallet/on-chain/oracle/rollup/keamanan kontrak/token).
- **Tarikan kandidat** = jalur opportunity klien sendiri (`trued.search_opportunities` + `build_opportunity_query` + `ensure_search_bound`, filter `arenaIds=general, questionMaxAgeMs=259200000` — batas yang dipakai poller serve). Tidak ada endpoint/field baru yang dikarang; viso dibaca dari field baris `questionVisoCount` (field yang dicetak `trued.opportunity_line`).

**Klasifikasi** (urutan pertama-cocok; nilai sel dari AUDIT-5-PILAR, terverifikasi ulang ke DATA-LIVE-ARENA-2026-11-17):

1. Liveness mati/tidak terbukti → **NO-PAY**
2. viso tidak terbaca → **NO-PAY** (tidak diklasifikasi buta)
3. viso = 0 → **PIONEER** (+20 — verified pertama)
4. Ronde maraton terbukti terbuka (endsAt eligible di masa depan pada detail) → **MARATHON** (+10 — verified terakhir saat conclude)
5. Estimasi ruang kebaruan ≥ 0,15 → **INNOVATOR** (+10 — verified dengan novelty ≥15%); di bawahnya → **NO-PAY**

Syarat topik inti (aturan seleksi pilot, PAKET-RESTART-SERVE: "hanya ISR lolos liveness tiga-field + topik inti; Marathon-live non-inti = lewati") menggugurkan kelas apa pun di luar topik inti; bisa dimatikan dengan `--no-core-topic`.

**Skor = nilai sel × kelayakan × bobot prioritas kelas.**

Kelayakan adalah **heuristik terkalibrasi fakta lapangan, bukan probabilitas terukur**:

- PIONEER (balap latensi — median verified-pertama eksternal 3,75 dtk; saringan A1 lama menuntut deteksi <2 mnt): umur ≤120 dtk → 0,60 · ≤600 → 0,40 · ≤3600 → 0,20 · lebih tua → 0,08 · umur tak diketahui → 0,20.
- MARATHON (pemenang masuk ronde ramai — pita A1 viso 2–9, median peringkat masuk kohort ±5): viso 2–9 → 0,50 · viso 1 atau 10–15 → 0,35 · viso >15 → 0,20; faktor waktu ke endsAt maksimum: <900 dtk ×0,6 (conclude bisa mendahului generasi kita) · >48 jam ×0,8 (jawaban belakangan menimbun kita — hanya yang TERAKHIR menang) · tak diketahui ×0,7.
- INNOVATOR: 0,6 × ruang(viso), ruang = clamp(0,95 − 0,08×viso; 0,05; 0,95).

**Prioritas kelas = PARAMETER eksplisit** (konflik dokumen K3/P12 tidak dikunci diam-diam): `--priority marathon` (bawaan — versi badan hunt A1/R1: Marathon > Pioneer) memberi bobot MARATHON 1,0 / PIONEER 0,9 / INNOVATOR 0,75; `--priority pioneer` (versi paket pilot: Pioneer dulu) menukar dua bobot pertama. Profil aktif dicetak di setiap run.

## 2. Uji shadow live — 2026-11-17 ±06:31–06:37 WIB

Tarikan: **100 baris** opportunity (general, ≤3 hari). Praranking dari baris, lalu **30 detail ISR teratas diverifikasi** (anggaran detail — lihat keterbatasan 5). Profil: prioritas marathon, topik inti wajib.

| Kelas | Jumlah | Catatan |
|---|---|---|
| PIONEER | **18** | semua terverifikasi detail, viso 0, topik inti |
| MARATHON | 0 | lihat keterbatasan 3 |
| INNOVATOR | 0 | lihat keterbatasan 3 |
| NO-PAY | 82 | 52 gugur topik inti (semua viso-0 di luar inti) · 30 mati/fail-closed |

Detail membuktikan kerja nyatanya di 30 tarikan teratas: 9 demosi topik-inti terkonfirmasi + **3 target terbukti mati pola flag basi oleh detail** (206c07dc, 20c5433b, 269d8337 — marathonActive masih menyala tapi semua endsAt ronde sudah lewat; persis jebakan §82).

Peringkat teratas (semua PIONEER, detail terverifikasi):

| Skor | ISR | Viso | Inti |
|---|---|---|---|
| 10.80 | 5eeabb36 | 0 | ya |
| 7.20 | 27da0f6a | 0 | ya |
| 7.20 | 45cb9a4a | 0 | ya |
| 7.20 | d1b8a81a | 0 | ya |
| 7.20 | d4e2aa43 | 0 | ya |
| 7.20 | dde95039 | 0 | ya |
| 7.20 | e04850a2 | 0 | ya |
| 3.60 | 3e6c5c64 | 0 | ya |
| 3.60 | 639000ba | 0 | ya |
| 3.60 | 7da10ef7 | 0 | ya |
| 3.60 | 89d45a6f | 0 | ya |
| 3.60 | 90820afc | 0 | ya |
| 3.60 | ac076ec1 | 0 | ya |
| 3.60 | de047edf | 0 | ya |
| 3.60 | e1e035e5 | 0 | ya |
| 3.60 | e79fdc83 | 0 | ya |
| 1.44 | 17b92c63 | 0 | ya |
| 1.44 | 9671827c | 0 | ya |

## 3. Validasi silang — target dry-run kemarin 8a4e9623

ID penuh `8a4e9623-772d-446b-9cdd-4d72e93371bb` (NFT marketplace/kustodi). Kemarin (dry-run terpadu) ia viso 0 dan lolos liveness = bentuk Pioneer. **Datanya sudah berubah, dilaporkan apa adanya:** tarikan barusan — status **settled**, marathonConcluded=true, endsAt ronde maksimum 2026-11-16T21:38:25Z (sudah lewat), daftar ISO = 77 revealed / 8 abandoned / 1 falsified / **1 verified** (viso kini 1 — slot Pioneer sudah diambil orang lain dan rondenya tutup). Pemilih mengklasifikasikannya **NO-PAY (mati, pola flag basi)** — perilaku yang benar: alat yang sama akan menyebutnya PIONEER kemarin dan menolaknya hari ini.

## 4. Tes

- `test_target_picker.py`: **24/24** — fixture viso 0 (PIONEER + skor persis), viso 6 + ronde terbuka (MARATHON), viso 5 (INNOVATOR), viso 14 (NO-PAY ruang tipis), detail basi (NO-PAY mati), maraton tanpa endsAt terbukti (fail-closed), detail None dua arah, demosi topik inti + matikan parameternya, profil prioritas pioneer, viso tak terbaca, unit kelayakan/ruang/rank.
- Suite penuh provider: **237/237 hijau** (basis 213 + 24 baru; test_openrouter_wrapper menghitung dengan format PASS-nya sendiri: 30 PASS, "GAGAL: tidak ada").

## 5. Keterbatasan (jujur)

1. **Kelayakan bukan probabilitas terukur** — angka 0,60/0,50/dst. adalah heuristik yang ditambatkan ke fakta lapangan (latensi median, pita viso A1), bukan hasil ukur laju-menang per kelas dari data kita. Skor mengurutkan, bukan meramal.
2. **Novelty sejati tidak bisa diukur dari data yang tersedia.** Surprise Gauge membandingkan ISI jawaban; pemilih hanya punya cacah + cakupan baris. Estimasi "ruang kebaruan" = proksi keramaian dari viso semata. Innovator memang tidak punya penanda publik per jawaban (KORPUS-JUARA, catatan bias 4: "Innovator tidak terukur") — kelas INNOVATOR-CANDIDATE adalah kandidat, bukan janji +10.
3. **MARATHON/INNOVATOR = 0 di run ini BUKAN bukti selnya kosong.** Tiga sebab bertumpuk: (a) urutan bawaan pencarian opportunity mengutamakan pertanyaan segar viso-0; (b) mayoritas baris berflag maraton tidak bisa membuktikan ronde terbuka dari field baris (fail-closed warisan gerbang) — klasifikasinya butuh detail; (c) anggaran detail (30) habis di praranking teratas yang didominasi PIONEER. Run dengan anggaran detail lebih besar / filter server `questionMarathonActive` + `questionMinVisos` akan melihat kelas lain — belum dijalankan.
4. **viso hanya menghitung verified yang sudah settle.** Jawaban rival yang masih revealed/in-flight tidak terlihat — slot Pioneer bisa sudah "diambil" tanpa tanda (kasus 8a4e9623 di §3 adalah buktinya dalam 24 jam).
5. **API lambat, terukur:** panggilan opportunity-filters 16,8 dtk; detail 1,5–11,1 dtk per panggilan. Run pertama (100 detail tanpa praranking) dibunuh sesudah ±10 menit karena tidak praktis — desain praranking + `--detail-cap` adalah jawabannya, dan kegagalan itu dicatat di sini sesuai aturan lapor-di-langkahnya. Jumlah panggilan run pertama tidak terukur persis (keluaran tertahan buffer); run kedua: filters 1 + search 1 + 30 detail = 32 panggilan GET read-only lewat klien trued (lane sesi custom.dialectica). Validasi §3: 3 panggilan (1 detail gagal format UUID awalan, 1 detail, 1 daftar ISO). Nol generasi serve terbakar; cap serve tidak tersentuh.
6. Baris opportunity bisa membawa status pertanyaan `verified` — `liveness_check` memperlakukannya mati fail-closed (status tidak dikenal), konsisten dengan gerbang yang ada; dicatat apa adanya, bukan ditambal di pemilih.
7. Skor **tidak** memasukkan peluang draf KITA lolos panel (itu wilayah gerbang serve + C5) — pemilih mengurutkan nilai sel target, bukan peluang tembakan.

## 6. Cara pakai (shadow)

```
cd provider
python3 target_picker.py [--limit 100] [--detail-cap 30] \
    [--priority marathon|pioneer] [--no-core-topic] [--json-out file.json]
```

Tidak ada mode eksekusi — sengaja. Menyambungkan peringkat ini ke serve live adalah keputusan fase berikutnya, bukan bagian alat ini.
