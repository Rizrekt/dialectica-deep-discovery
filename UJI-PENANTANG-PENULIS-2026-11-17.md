# UJI PENANTANG PENULIS — qwen-3.8-max (CrowLLM) vs GLM (Vyce) — 2026-11-17

**Perintah:** user 2026-11-17 21:15 "coba testing ulang".
**Sifat:** lab murni. Serve STOP dan tetap STOP; nol submit; TIDAK ada integrasi
yang dipasang; rantai penulis serve TIDAK diubah.
**Pertanyaan tes:** sebagai PENULIS, apakah draf qwen-3.8-max lebih bersih
penunjuk presisinya daripada draf GLM (glm-5.3-flash, penulis utama serve)?
**Artefak kerja:** `penantang-penulis-2026-11-17/` (prompt, draf qwen, JSON
mentah per percobaan, `scores.json`, `citation-ab-log.jsonl`, driver
`run_qwen_writer.py`, penilai `score_ab.py`).

---

## 1. Rancangan

- **3 pertanyaan uji** = 3 pertanyaan pilot yang draf GLM aslinya ada persis di
  disk (`PILOT-SPOTCHECK-2026-11-17/`, teks persis yang terkirim serve
  2026-11-17 pagi, penulis glm-5.3-flash via Vyce, semua kelas PIONEER viso 0):
  1. `2777178d` — metode deteksi multi-account farming whitelist NFT.
  2. `d94d7e34` — membedakan banyak wallet agen AI satu orang vs banyak orang.
  3. `635a010d` — akses wallet MPC agen AI lintas restart mesin.
  Sisi GLM memakai draf asli itu — BUKAN generasi ulang.
- **Sisi qwen:** jawaban baru untuk pertanyaan yang sama via CrowLLM
  `qwen-3.8-max:free`, instruksi penulis versi publik-aman (tesis pembuka,
  cakupan penuh per seksi, sitasi presisi — URL/DOI/nomor paper/judul persis,
  hanya sumber yang diyakini ada — penutup sintesis, target ±5.000–7.000 kar,
  nol jejak proses). Prompt gerbang/rubrik internal TIDAK dikirim ke relay.
- **Transport qwen:** jeda ≥13–14 dtk antar panggilan; Q1 sukses percobaan 1
  (200, 5,8 dtk), Q2 sukses percobaan 1 (200, 37,6 dtk), Q3 = 503 → 503 →
  400 (percobaan streaming; jalur stream model ini membalas 400, konsisten
  dengan probe awal) lalu **sukses percobaan 4** sesudah cooldown 60 dtk
  (200, 5,9 dtk). Semua kegagalan tercatat di JSON mentah per percobaan.
- **Penggaris (sama persis dua sisi):** `provider/citation_verify.py` versi
  disk, mode `block`, fetcher nyata (pola `calibrate_citation_verify.py`).
  Skor utama = penunjuk karangan per draf (status dead / wrong_document /
  malformed), dipisah poros vs pinggiran; vonis TAHAN = `fatal`/`block`.
  Pendamping: panjang vs lantai+pita kelas PIONEER (lantai 1.717 kar; pita
  patokan (c)-PK1 3.435–7.297 kar) + scan jejak proses.

## 2. Tabel skor A/B

| # | Pertanyaan | Sisi | Kar | Penunjuk total | Verified | Karangan poros | Karangan pinggiran | Total karangan | Vonis lapis |
|---|-----------|------|-----|---------------|----------|---------------|--------------------|---------------|-------------|
| 1 | 2777178d (NFT sybil) | GLM | 6.673 | 19 | 14 | 0 | **3** | **3** | findings (lolos, tercatat) |
| 1 | | qwen | 5.111 | **0** | 0 | 0 | 0 | **0** | clean |
| 2 | d94d7e34 (wallet satu vs banyak orang) | GLM | 7.570 | 11 | 8 | **1** | **1** | **2** | **fatal — TAHAN** |
| 2 | | qwen | 5.167 | **0** | 0 | 0 | 0 | **0** | clean |
| 3 | 635a010d (MPC lintas restart) | GLM | 6.964 | 10 | 8 | **1** | **1** | **2** | **fatal — TAHAN** |
| 3 | | qwen | 4.971 | **0** | 0 | 0 | 0 | **0** | clean |
| | **AGREGAT** | GLM | — | **40** | 30 (75%) | **2** | **5** | **7 (17,5% penunjuknya)** | 2/3 draf TAHAN |
| | | qwen | — | **0** | — | **0** | **0** | **0** | 0/3 draf TAHAN |

Rincian karangan GLM (identik dengan temuan spot-check manual sesi utama):
- Q1 pinggiran: domain `proofofhumanity.site` mati (2 bentuk) +
  `https://docs.passport.gitcoin.co` mati. (2 penunjuk lain unverified —
  bot-wall, bukan vonis.)
- Q2 poros: DOI `10.1145/2516651.2516734` mati (404 Crossref + doi.org);
  pinggiran: `https://whitepaper.worldcoin/` malformed (tanpa TLD).
- Q3 poros: ePrint `2020/940` wrong_document (klaim MPC vs paper Fei Meng);
  pinggiran: `https://docs.web3auth.com/` mati.

Panjang: qwen 5.111 / 5.167 / 4.971 kar — semua di dalam pita PIONEER
3.435–7.297 dan di atas lantai 1.717. GLM 6.673 (di pita) / 7.570 (di atas
pita — catatan (c) saja) / 6.964 (di pita). Jejak proses: **0 di keenam draf**
(scan thinking/reasoning/meta = bersih dua sisi); draf qwen terstruktur
(tesis → seksi → sintesis) dan nyaris tanpa klaim numerik presisi di prosa
(satu-satunya temuan: "100%" di Q2).

## 3. Vonis

Di penggaris utama tes ini — penunjuk karangan per draf — **qwen-3.8-max
menang mutlak: 0 berbanding 7** (GLM: 2 poros + 5 pinggiran; 2 dari 3 drafnya
akan TAHAN di gerbang sitasi, konsisten dengan spot-check manual). TETAPI
mekanisme kemenangannya harus dibaca persis: **qwen tidak menyitasi sama
sekali** — nol URL, nol DOI, nol nomor paper, nol rujukan bernama di ketiga
drafnya — jadi vonis "clean"-nya adalah clean karena tidak ada penunjuk yang
bisa salah, bukan bukti kemampuan menyitasi secara presisi. GLM sebaliknya
menyitasi padat (40 penunjuk, 75% terverifikasi baik) dengan 17,5% karangan
termasuk 2 penunjuk poros. Artinya tes ini membuktikan qwen **tidak mengarang
penunjuk**, sekaligus menunjukkan risiko tukarnya: draf tanpa apparatus
sitasi sama sekali terpapar kelas cacat arena yang berbeda (klaim tanpa
dukungan penunjuk yang bisa diverifikasi) yang TIDAK bisa dinilai oleh lapis
mekanis ini. Perbandingan yang adil untuk mutu sitasi positif (menyitasi
banyak DAN presisi) belum terjawab oleh tes ini — itu butuh prompt penulis
yang mewajibkan apparatus sitasi eksplisit per klaim poros, dan/atau penilaian
dukungan-klaim semantik (C5) di atas kedua sisi.

## 4. Kaveat

- **Sampel n=3 pertanyaan** (6 draf) = sinyal awal yang kuat arahnya, bukan
  vonis final soal pergantian penulis.
- Sisi qwen dinilai di bawah **prompt publik** (instruksi penulis umum yang
  setara perlakuan, bukan prompt serve persis + steering internal) — kaveat
  yang sama dengan kalibrasi pemeriksa CrowLLM.
- Skor GLM adalah skor draf pilot ASLI (sudah termasuk keadaan serve pagi
  itu); bukan GLM yang di-generasi ulang hari ini.
- Lapis sitasi hanya menilai penunjuk yang ADA; klaim prosa tanpa penunjuk
  (dua sisi) di luar jangkauannya.
- Satu pertanyaan (Q3) butuh 4 percobaan transport (503 kanal upstream) —
  kesehatan kanal CrowLLM bervariasi, tercatat apa adanya.
