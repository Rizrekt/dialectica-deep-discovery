# PERBAIKAN URUTAN PEMILIH — R2 (2026-11-17, fase testing)

> Revisi persiapan R2, disetujui user 2026-11-17 08:36. **SHADOW / READ-ONLY**: nol serve/submit/klaim; rumus klasifikasi kelas TIDAK diubah — yang diperbaiki hanya **siapa yang mendapat giliran baca-detail, dalam urutan apa**. Kode: `provider/target_picker.py` (backup: `target_picker.py.bak-20261117-r2`) · tes: `provider/test_target_picker.py` · hasil run mentah: `provider/picker-shadow-r2-2026-11-17.json`.

## 1. Cacat yang diperbaiki

Pada uji shadow item 1 (PEMILIH-TARGET-2026-11-17.md §5 butir 3), `--priority marathon` hanya membobot **skor akhir**. Urutan pengeluaran anggaran detail mengikuti praranking skor dari field baris — dan kandidat pita Marathon (viso 2–9 berflag maraton) terklasifikasi NO-PAY (skor 0) dari barisnya sendiri, karena baris tidak bisa membuktikan ronde terbuka (fail-closed warisan gerbang). Akibatnya 30/30 slot detail habis di baris viso-0 dan MARATHON/INNOVATOR terbaca 0 — padahal prioritas resmi proyek adalah Marathon dulu (SISTEM-KENDALI F6) dan lapangan menebal di Marathon (5,85 slot/pertanyaan, STUDI-KOHORT-2026-11-17.md).

## 2. Urutan berburu — sebelum → sesudah

**Sebelum (kedua profil sama):** praranking skor global dari field baris → detail untuk N teratas praranking itu. Profil prioritas hanya mengubah bobot skor.

**Sesudah:** kandidat dikelompokkan ke **pita berburu** menurut apa yang bisa dibuka oleh satu baca-detail, lalu anggaran detail dibagi per pita (rumus §3) dan dibaca dalam urutan profil:

| Pita | Isi |
|---|---|
| MARATHON | viso ≥1 + dimensi maraton di baris (flag active/concluded atau daftar eligible). Di dalam pita: kelompok viso utama 2–9 → viso 1 / 10–15 → viso >15; di dalam kelompok: ronde sudah terbukti terbuka dari baris → belum terbukti (tanpa endsAt di baris) → basi-di-baris |
| INNOVATOR | viso ≥1, tanpa dimensi maraton, estimasi ruang kebaruan ≥ lantai 0,15 |
| PIONEER | viso 0 |
| SISA | sisanya yang masih bisa diinformasikan detail (mis. viso >10 tanpa dimensi maraton) — jatah 0, hanya dari sisa anggaran |

Detail **tidak** dibelanjakan di tempat ia tidak bisa mengubah kelas bayar: baris tanpa id, viso tidak terbaca (detail tidak membawa viso), baris di luar topik inti selama aturan pilot menyala (demosi dihitung dari teks baris sendiri), dan pertanyaan yang barisnya sendiri membuktikan settled tanpa dimensi maraton.

**Urutan per profil (eksplisit, juga tertulis di docstring modul):**
- `marathon` (bawaan): MARATHON → INNOVATOR → PIONEER → SISA.
- `pioneer`: PIONEER → MARATHON → INNOVATOR → SISA — perilaku item 1 (viso-0 segar dibaca lebih dulu) dipertahankan.

Di dalam pita (selain sub-urutan MARATHON di atas), kandidat mengikuti urutan skor praranking yang sudah ada.

## 3. Rumus jatah anggaran detail

N = `--detail-cap`. Dua lintasan:

- **Lintasan 1 — jatah minimum per pita, searah urutan profil:** pita pertama ⌈N/2⌉, pita kedua ⌈N/4⌉, pita ketiga sisanya (N − ⌈N/2⌉ − ⌈N/4⌉), SISA 0.
  - marathon, N=30 → **MARATHON 15 · INNOVATOR 8 · PIONEER 7**
  - pioneer, N=30 → **PIONEER 15 · MARATHON 8 · INNOVATOR 7**
  - marathon, N=10 → MARATHON 5 · INNOVATOR 3 · PIONEER 2 (tercetak di run §4)
- **Lintasan 2 — sisa bebas:** anggaran yang tidak terpakai (pita lebih kecil dari jatahnya) dibagikan lagi searah urutan profil yang sama, jadi jatah tidak pernah hangus dan total tidak pernah melewati N.

## 4. Bukti sapuan shadow live — profil marathon, 2026-11-17 ±08:55–09:02 WIB

**Keadaan API (dilaporkan apa adanya):** tiga percobaan cakupan penuh (limit 100, cap 30) gagal berturut-turut — HTTP 500 dari `opportunity-filters`, lalu 2× timeout baca. Percobaan keempat dengan cakupan tereduksi (**limit 30 baris, detail-cap 10**) yang tuntas; pacing dijaga (satu proses, jeda 0,3 dtk antar-detail bawaan alat). Hitungan kelas di bawah karena itu **tidak sebanding angka-demi-angka** dengan item 1 (100 baris) — yang dibandingkan adalah **urutannya**.

**Urutan aktual baca-detail (dari JSON run, field `detail_seq`/`hunt_band`):**

| Seq | ISR | Pita | Viso | Hasil detail | Kelas akhir |
|---|---|---|---|---|---|
| 1 | a8110268 | MARATHON | 1 | **timeout** — jatuh ke field baris | NO-PAY (fail-closed) |
| 2 | b3c7560f | MARATHON | 1 | **timeout** — jatuh ke field baris | NO-PAY (fail-closed) |
| 3 | 23e1b737 | PIONEER | 0 | timeout — liveness dari baris | PIONEER |
| 4 | 8a83ba7b | PIONEER | 0 | terverifikasi | PIONEER |
| 5 | c23cf4f1 | PIONEER | 0 | timeout — liveness dari baris | PIONEER |
| 6 | 7e3b08c0 | PIONEER | 0 | terverifikasi | PIONEER |

Rencana yang tercetak sebelum pengambilan: jatah MARATHON 5 · INNOVATOR 3 · PIONEER 2 — terisi MARATHON 2 (hanya 2 kandidat pita itu yang lolos syarat detail di tarikan ini), INNOVATOR 0 (tidak ada kandidatnya), lalu sisa anggaran mengalir ke PIONEER (2 jatah + 2 sisa = 4). Total 6 detail ≤ cap 10.

**Hitungan kelas akhir (30 baris): PIONEER 4 · MARATHON 0 · INNOVATOR 0 · NO-PAY 26.**
Banding item 1 (100 baris, kode lama): PIONEER 18 · MARATHON 0 · INNOVATOR 0 · NO-PAY 82, dengan 30/30 detail mendarat di baris viso-0.

**Kenapa MARATHON tetap 0 — kali ini terbukti dari urutannya, bukan kehabisan anggaran:**
1. Hanya **2 kandidat pita Marathon** di seluruh tarikan yang memenuhi syarat detail (viso ≥1 + dimensi maraton + topik inti): a8110268 dan b3c7560f. Keduanya dibaca **paling pertama** (seq 1–2) — di kode lama keduanya berpraranking skor 0 dan tidak akan pernah terbaca.
2. Detail keduanya **timeout** (2 dari 4 timeout jaringan di run ini), sehingga klasifikasi jatuh kembali ke field baris = fail-closed mati (`marathonActive=True` tanpa endsAt masa depan yang bisa ditunjukkan). Apakah ronde mereka sebenarnya terbuka **tidak terukur** di run ini — dibedakan tegas dari "tidak ada": kandidatnya ada, gilirannya dapat, verifikasinya yang gagal di jaringan.
3. Empat baris berflag maraton lain di tarikan (136e5967, 353d467f, 75fad077, e03a46c7) berada **di luar topik inti** → memang tidak bisa menjadi kelas bayar di bawah aturan pilot, jadi tidak memakan detail; dari barisnya pun polanya sama (tidak terbukti terbuka).

## 5. Tes

- `test_target_picker.py`: **42/42** (24 lama + **18 baru**): rumus jatah kedua profil (cap 30 + cap 6), pemetaan pita per kandidat (termasuk pengecualian: viso tak terbaca, luar topik inti dua arah, settled), urutan pita profil marathon (M,M,I,I,P,P pada cap 6 — jatah + aliran sisa), urutan profil pioneer (P,P,P,M,M,I), sub-urutan dalam pita MARATHON (terbuka > belum-terbukti > basi > kelompok viso sebelah), SISA hanya dari sisa anggaran, cap dihormati tanpa duplikat.
- Suite penuh provider: **299/299 hijau** (basis 281; test_openrouter_wrapper 30 PASS "GAGAL: tidak ada", sisanya ALL PASS per berkas).

## 6. Keterbatasan

1. **Bukti live tereduksi oleh keadaan API.** Tiga percobaan cakupan penuh gagal (HTTP 500 + 2 timeout) dan 4 dari 6 detail pada run yang tuntas pun timeout. Urutan berburu terbukti bekerja di data live (pita Marathon dibaca pertama), tetapi verifikasi detail kandidat Marathon-nya sendiri digagalkan jaringan — run ulang pada API sehat masih diperlukan untuk melihat apakah ada MARATHON yang benar-benar terklasifikasi.
2. **Sampel tarikan kecil dan bias segar.** 30 baris bawaan pencarian opportunity mengutamakan pertanyaan segar; hanya 2 kandidat pita Marathon bertopik-inti yang muncul. Angka 5,85 slot/pertanyaan dari studi kohort diukur di frame settled, bukan di frame opportunity segar ini — kedua frame memang berbeda populasi.
3. **Jatah adalah kebijakan, bukan hasil ukur.** Pecahan ½/¼/sisa dipilih agar pita prioritas tidak pernah kelaparan sambil tetap menyisakan giliran pita lain; belum ada data laju-temu per pita untuk mengkalibrasinya. Bila run-run berikutnya menunjukkan pita Marathon bertopik-inti rutin <5 kandidat, jatahnya bisa diturunkan — itu keputusan berbasis data berikutnya, bukan sekarang.
4. Semua keterbatasan PEMILIH-TARGET-2026-11-17.md §5 (kelayakan heuristik, novelty tak terukur publik, viso hanya menghitung yang sudah settle, skor bukan peluang lolos panel) tetap berlaku utuh.
