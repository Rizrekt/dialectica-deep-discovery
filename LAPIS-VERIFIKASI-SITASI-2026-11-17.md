# LAPIS VERIFIKASI SITASI MEKANIS — 2026-11-17

**Keputusan user 2026-11-17 10:39** (usulan SPOTCHECK-PILOT-2026-11-17.md diterima): bangun lapis verifikasi sitasi mekanis untuk pipa serve. Serve STOP sejak 10:07 (konsekuensi checklist D spot-check) dan **tetap STOP** selama pembangunan ini — lapis dibangun + diuji + dikalibrasi saja, tidak ada nyala, tidak ada submit/klaim.

## 1. Musuh yang ditutup (terukur dari spot-check)

Penulis GLM kuat isi/struktur 3/3 tetapi mengarang **penunjuk presisi** 3/3: domain mati `proofofhumanity.site` (yang hidup `.id`), DOI karangan `10.1145/2516651.2516734` (404; yang benar 10.1145/2504730.2504747), URL `whitepaper.worldcoin/` tanpa TLD, pinpoint "Lindell, IACR ePrint 2020/940" yang menunjuk paper Fei Meng. C5 semantik menilai clean 3/3 karena C5 meniru pola, bukan me-resolve penunjuk. Lapis ini me-resolve penunjuk secara mekanis terhadap registry/sumber aslinya.

## 2. Rancangan

**Modul:** `provider/citation_verify.py` (±950 baris). **Titik pasang:** tahap tambahan di `serve_gate.gate_answer(..., citation_check=...)`, berdampingan dengan tahap semantik C5 dan mengikuti kontrak yang sama persis: callable mengembalikan dict; hanya `block=True` yang menahan draf; callable crash → tahap dicatat tidak-terlaksana dan **tidak pernah** menahan. `vyce_serve_common.vyce_pipeline` meneruskan `serve_gate.armed_citation_check()`; `run_serve.py` meng-arm `DIALECTICA_CITATION_CHECK=1` di cabang gated Vyce serve (bersama arming C5).

**Arming (mengikuti pola C5):**
- `DIALECTICA_CITATION_CHECK=1` → lapis aktif; tanpa itu tahap tidak berjalan sama sekali.
- `DIALECTICA_CITATION_MODE` → bawaan **`block`** (menahan); `shadow` hanya bila diset eksplisit (mencatat, tak menahan).

**Ekstraksi:** URL (termasuk yang terbungkus kurung prosa/markdown — di-trim dari tanda baca kalimat dan kurung penutup tak-seimbang, sementara kurung/segmen-sudut SEIMBANG dipertahankan karena DOI gaya AMS sah memuatnya: `10.1175/1520-0469(1993)050<3625:MVATAS>2.0.CO;2`), DOI telanjang + via doi.org, IACR ePrint (URL + tekstual), arXiv (URL + tekstual), domain telanjang (TLD dari set dikenal; ekstensi berkas dikecualikan). Dedupe per (jenis, nilai). Klaim judul/penulis diambil dari aparatus sitasi yang menempel (kutipan terakhir ≤420 kar sebelumnya + nama keluarga penulis).

**Verifikasi per jenis:**
- **DOI** → Crossref: judul + penulis dibandingkan. Crossref 404 **bukan** vonis mati sendirian (Crossref hanya satu agen registrasi) → konfirmasi doi.org: doi.org 404 juga = mati; doi.org menjawab status apa pun = DOI terdaftar (judul tak terbanding, dicatat).
- **ePrint** → halaman abstrak: meta `citation_title`/`citation_author` dibandingkan klaim. **arXiv** → API ekspor Atom, sama.
- **URL polos** → fetch; perbandingan `<title>`/og:title hanya bila judul kutipan benar-benar aparatus sitasi URL itu ("near": celah kutipan→penunjuk ≤80 kar/≤10 kata/tanpa putus kalimat **dan** ada nama penulis menempel) — aturan ketat subset-token: cocok bila satu himpunan token memuat yang lain; beda total = salah-dokumen; abu-abu (mis. subjudul tertukar satu kata) = **tak terverifikasi**, dilaporkan terbuka.
- **Domain telanjang** → yang diklaim hanya keberadaan domain: jawaban HTTP apa pun (termasuk 404 di root) = hidup; mati hanya bila apex **dan** `www.` gagal di level koneksi.

**Klasifikasi POROS** (salah satu cukup): P1 pinpoint registry (DOI/ePrint/arXiv); P2 angka hadir di kalimat yang sama; P3 penanda preseden ("precedent", "reference case", "canonical", "clearest", "landmark", …); P4 sesudah penanda "New in this answer".

**Aturan tahan (mode block):** ≥1 penunjuk POROS berstatus dead / wrong_document / malformed → draf DITAHAN. Penunjuk pinggiran mati/salah = temuan tercatat, tidak menahan.

**Doktrin kegagalan pemeriksa (cermin doktrin C5 — cek yang tak jalan tak boleh menyamar jadi lolos, pemeriksa mati tak boleh membunuh draf sehat):**
- 401/403/429/5xx = bot-wall/rate-limit → **unverifiable**, bukan mati: tercatat terbuka, bukan temuan, tak menahan.
- Canary (Crossref + doi.org atas DOI asli yang dikenal) jalan duluan; egress mati → seluruh run `verdict=unverified, available=False`, nol blokir.
- ≥40% fetch mati di level koneksi dalam satu run → status dead-karena-koneksi diturunkan jadi unverifiable; verdict `unverified`.
- Semua penunjuk poros tak terverifikasi (dan ≥1 poros ada) → verdict `unverified`, tetap tak menahan.
- Setiap run tercatat ke `provider/citation-check-log.jsonl`.

**Etika resolver:** pacing 0,34 dtk antar-fetch, cache per run, 1 retry, timeout 20 dtk, badan dibatasi 300 KB, User-Agent jujur `DialecticaCitationVerify/1.0 (mechanical citation checker; operator research)`.

## 3. BATAS TEGAS

Lapis ini memverifikasi **penunjuk** (apakah DOI/URL/nomor paper itu ada dan menunjuk dokumen yang diklaim). Lapis ini **TIDAK memverifikasi isi klaim lawan isi sumber** — spesies angka Hop (sumber hidup dan benar, tetapi angka yang dikutip tidak ada di dalamnya) berada di luar lingkup dan **tidak tertangkap** lapis ini. Itu lapis berbeda (per aturan ketat user 10:50, wujud berikutnya yang wajib dibangun sebelum serve diskalakan).

## 4. Kalibrasi (fetcher nyata, 2026-11-17; hasil mentah `provider/calibration-citation-results.json`)

| Kasus | Target | Hasil | Rincian |
|---|---|---|---|
| 2777178d | tertangkap (domain mati) | ✅ findings, tidak ditahan (sesuai desain — penunjuknya pinggiran) | 19 penunjuk: 14 verified, **3 temuan asli** (`proofofhumanity.site` domain+URL mati, `docs.passport.gitcoin.co` mati — cocok catatan spot-check), 2 unverified (layer3.xyz, fractal.id — 403 bot-wall). **0 salah-temuan.** |
| d94d7e34 | tertangkap (DOI 404 + URL tanpa TLD) | ✅ **fatal — DITAHAN** | DOI poros `10.1145/2516651.2516734` mati (Crossref 404 **dan** doi.org 404); `whitepaper.worldcoin` malformed. SSRN unverified (403/ChunkedEncodingError dari VM — subjudul DeSoc tak bisa divonis dari VM, dilaporkan terbuka). 8 verified. |
| 635a010d | tertangkap (ePrint salah dokumen) | ✅ **fatal — DITAHAN** | ePrint 2020/940 poros = wrong_document (klaim "Secure Multiparty Computation (MPC)" vs aktual paper Fei Meng); `docs.web3auth.com` mati (cocok spot-check). 8 verified. |
| Kontrol Danis (VERIFIED lapangan) | tidak ditahan | ✅ clean | 3/3 penunjuk verified. |
| Kontrol kasnapp (VERIFIED lapangan) | tidak ditahan | ✅ clean, tidak ditahan | 6 verified; 2 unverified bot-wall (science.org, pubs.usgs.gov — 403) tercatat terbuka. |
| Kandidat kontrol Sushil (VERIFIED lapangan) | — | ⚠️ **gugur sebagai kontrol, secara sah** | 4 DOI-nya 404 di Crossref **dan** doi.org; query bibliografis Crossref membuktikan DOI asli salah satu papernya `10.1029/93je01084` ≠ `10.1029/93JE00547` yang dikutip. Jawaban lapangannya sendiri membawa penunjuk cacat → lapis BENAR menahannya; ini temuan kalibrasi tentang korpus lapangan, bukan salah-tahan. Syarat brief (≥2 kontrol sehat tak ditahan) terpenuhi oleh Danis + kasnapp. |

**Tiga cacat lapis sendiri ditemukan kalibrasi putaran 1 dan diperbaiki + dites sebelum putaran final di atas:** (A) perbandingan judul halaman untuk semua URL → salah-temuan pada kutipan prosa tak terkait — diperbaiki aturan judul-near + syarat penulis + aturan subset ketat; (B) ekstraksi memotong DOI/URL di `)` → DOI sah berkurung seimbang (gaya AMS) tertangkap utuh sekarang; (C) semantik domain telanjang → jawaban HTTP apa pun = hidup + fallback `www.` sebelum vonis mati.

**Salah-tahan final: 0** pada kontrol yang sah. **Tangkapan wajib: 3/3.**

## 5. Tes

- `provider/test_citation_verify.py` (baru, jaringan mock deterministik): **44/44 ALL PASS** — ekstraksi (termasuk DOI AMS berkurung, aturan near), vonis (DOI mati 404-ganda menahan di block / tak menahan di shadow, DOI warisan Crossref-404-doi.org-hidup lolos, ePrint salah-dokumen menahan, domain 404-root hidup, domain www-fallback, subjudul tertukar = unverifiable), doktrin kegagalan (canary mati, egress massal), pengawatan gerbang + arming + mode.
- **Suite penuh provider: 407 cek lolos / 0 gagal / 9 tak-terjalan.** Yang tak-terjalan: `test_improve_20261116.py` berhenti di §3 karena tersandung **cap serve NYATA 10/10 yang habis oleh pilot pagi ini** (tes itu me-mock subprocess tetapi membaca log pemakaian asli; 8 dari 17 ceknya lolos sebelum berhenti). Keadaan operasional, **bukan regresi** lapis ini — berkas itu tidak menyentuh kode sitasi; akan hijau lagi pada hari UTC baru. Basis suite sebelum tugas ini 372 cek; kini 416 (bertambah 44 cek sitasi).
- Backup: `serve_gate.py.bak-20261117-citverify`, `vyce_serve_common.py.bak-20261117-citverify`, `run_serve.py.bak-20261117-citverify`. K-1/K-2/C5/QUALITY tidak disentuh. Kredensial tidak dicetak. Serve tidak pernah di-start selama tugas ini (terverifikasi `inactive` di akhir).

## 6. Sisa risiko (terbuka)

1. **Bot-wall**: SSRN, science.org, beberapa penerbit menjawab 403 dari VM → penunjuk di belakangnya hanya bisa berstatus unverified (termasuk subjudul DeSoc — tak tervonis dari VM). Bila penunjuk poros satu-satunya gelap semua, verdict run = unverified dan draf tetap lewat dengan catatan keras di log — keputusan sadar doktrin, bukan celah diam.
2. **Latensi**: 4–36 dtk per draf teramati di kalibrasi (terburuk putaran awal 95 dtk sebelum cache/pacing stabil) — menambah waktu per generasi serve; cap pilot harian tidak berubah.
3. **Rate-limit resolver**: Crossref/doi.org/ePrint dipakai dengan pacing + cache per run; run serve massal tetap harus menghormati kuota sopan mereka (UA jujur terpasang).
4. **Judul abu-abu**: tukar-subjudul satu kata pada URL polos hanya bisa unverifiable dari aritmetika token — vonis tegasnya butuh mata manusia atau lapis isi (butir 3).
5. **DNS VM me-resolve semua nama ke proxy** → kematian domain hanya bisa divonis di level HTTP/koneksi, sudah ditangani (apex + www).

## 7. Cara arming untuk nyala berikutnya

Sudah terpasang: nyala gated Vyce berikutnya otomatis meng-arm `DIALECTICA_CITATION_CHECK=1` (run_serve) dengan mode bawaan **block**. Untuk menjalankan lapis ini dalam mode catat-saja pada nyala tertentu: set `DIALECTICA_CITATION_MODE=shadow` di env unit sebelum start. Untuk mematikan total: hapus/kosongkan `DIALECTICA_CITATION_CHECK`. **Keputusan start tetap di tangan user — serve saat laporan ini ditulis masih STOP.**
