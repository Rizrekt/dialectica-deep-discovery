# SAPUAN ULANG PEMILIH — SISA KECIL 1 (2026-11-17, fase testing)

> Pengulangan sapuan bukti R2 pada API sehat. **SHADOW / READ-ONLY murni**: nol serve/submit/klaim, nol generasi — cap serve tidak terpakai sama sekali. **Nol perubahan kode.** Alat: `provider/target_picker.py` pasca-R2, profil `marathon`, limit 100, detail-cap 30. Run mentah: `provider/picker-shadow-sisakecil1-2026-11-17.json`.

## 1. Kesehatan API (cek pendahuluan, ±09:27 WIB)

| Uji | Hasil |
|---|---|
| Tarikan daftar (limit 10) | **OK** — 10 baris, 8,44 dtk, tanpa notice degradasi |
| Baca detail 1d3be0c0 | OK — 1,26 dtk |
| Baca detail eaa812f3 | OK — 1,53 dtk |
| Baca detail c9946a57 | OK — 3,32 dtk |

**Vonis: API sehat** (bandingkan sapuan R2 08:55–09:02: HTTP 500 dari opportunity-filters + timeout dominan). Sapuan penuh dijalankan.

## 2. Sapuan penuh — hasil

- 100 baris tertarik; rencana berburu tercetak: jatah MARATHON 15 · INNOVATOR 8 · PIONEER 7 · SISA 0.
- Detail benar-benar dibaca: **25** (10 pita MARATHON + 15 pita PIONEER; pita INNOVATOR berisi **0 kandidat** di tarikan ini, jadi jatahnya mengalir ke PIONEER sesuai rumus lintasan 2). **Detail gagal/timeout: 0** (R2: 4 dari 6).
- Durasi run ±146 detik, satu proses, jeda 0,3 dtk antar-detail.

**Hitungan kelas akhir: PIONEER 15 · MARATHON 2 · INNOVATOR 0 · NO-PAY 83.**

### Urutan baca aktual — pita MARATHON dibaca pertama (seq 1–10), semua tuntas terverifikasi

| Seq | ISR | Viso | Hasil detail | Kelas akhir |
|---|---|---|---|---|
| 1 | dfbd70c2 | 2 | ronde maraton **terbuka** (berakhir 4 mnt lagi) | **MARATHON** |
| 2 | 04565c79 | 1 | pola flag basi (semua endsAt lewat) | NO-PAY |
| 3 | 1d3be0c0 | 1 | ronde maraton **terbuka** (berakhir 5 mnt lagi) | **MARATHON** |
| 4 | 20303005 | 1 | pola flag basi | NO-PAY |
| 5 | 2a31bf4d | 1 | pola flag basi | NO-PAY |
| 6 | 85ad239d | 1 | pola flag basi | NO-PAY |
| 7 | a8110268 | 1 | pola flag basi (endsAt maks 01:59Z) | NO-PAY |
| 8 | b14a5bab | 1 | pola flag basi | NO-PAY |
| 9 | b3c7560f | 1 | pola flag basi (endsAt maks 01:56Z) | NO-PAY |
| 10 | c23cf4f1 | 1 | pola flag basi | NO-PAY |
| 11–25 | 15 baris viso-0 | 0 | terverifikasi | PIONEER ×15 |

## 3. Vonis kandidat Marathon — tegas, dari saringan, bukan jaringan

1. **MARATHON tidak lagi 0.** Untuk pertama kalinya kelas Marathon terklasifikasi dari bukti live: **2** (dfbd70c2, 1d3be0c0), keduanya detail-terverifikasi dengan ronde terbuka yang endsAt-nya tinggal 4–5 menit — sel bayar +10 itu nyata dan jendelanya sempit.
2. **8 kandidat pita sisanya gugur oleh saringan dengan detail terverifikasi**, sebabnya satu pola: `marathonActive=True, marathonConcluded=False`, tetapi semua endsAt ronde sudah lewat = **pola flag basi** (flag server tidak menutup ronde yang sudah berakhir). Termasuk **a8110268 dan b3c7560f** — dua kandidat yang di sapuan R2 timeout dan fail-closed tak terukur; kali ini terbukti mati oleh flag basi, bukan oleh jaringan.
3. **INNOVATOR 0 karena pitanya kosong di tarikan ini** (tidak ada baris viso ≥1 tanpa dimensi maraton dengan ruang kebaruan ≥0,15), bukan karena anggaran — jatah 8-nya tidak terpakai dan mengalir ke PIONEER.
4. Komposisi NO-PAY (83): **52** di luar topik inti · **23** baris maraton di luar topik inti yang fail-closed dari field baris (tanpa detail memang by-design — di luar cakupan pilot) · **8** flag basi detail-terverifikasi.

## 4. Perbandingan tiga sapuan

| Sapuan | Baris | PIONEER | MARATHON | INNOVATOR | NO-PAY | Keadaan bukti |
|---|---|---|---|---|---|---|
| Item 1 (kode lama) | 100 | 18 | 0 | 0 | 82 | 30/30 detail habis di viso-0; Marathon tak pernah terbaca |
| R2 (urutan baru, API degradasi) | 30 | 4 | 0 | 0 | 26 | urutan terbukti (Marathon dibaca seq 1–2), detailnya timeout → fail-closed jaringan |
| **Sisa kecil 1 (urutan baru, API sehat)** | **100** | **15** | **2** | **0** | **83** | **25/25 detail terverifikasi, 0 gagal; Marathon terbukti dari saringan** |

Pada ukuran tarikan yang sama dengan item 1 (100 baris), MARATHON bergerak 0 → 2 murni karena urutan berburu R2 + API yang sehat; dan nol-nya Innovator serta gugurnya 8 kandidat Marathon kini berpenyebab tertulis per kandidat.

## 5. Keterbatasan

1. Dua MARATHON yang terklasifikasi berjendela sangat sempit (ronde berakhir 4–5 menit sesudah dibaca) — bukti kelasnya sah, tetapi sebagai target serve nyata mereka hampir pasti sudah tertutup saat dibaca laporan ini; yang dibuktikan di sini adalah **kemampuan pemilih menemukan dan membuktikan kelasnya**, bukan ketersediaan targetnya.
2. Frame tetap opportunity segar (bias pertanyaan baru); angka 5,85 slot/pertanyaan dari studi kohort diukur di frame settled — populasi berbeda, jangan dicampur.
3. Pola flag basi mendominasi kematian pita Marathon (8/10): bila server suatu saat membersihkan flag tepat waktu, laju temuan Marathon bisa naik tanpa perubahan di pihak kita.
