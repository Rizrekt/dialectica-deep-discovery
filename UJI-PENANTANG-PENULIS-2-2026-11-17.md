# UJI PENANTANG PENULIS BABAK 2 (PENENTU) — qwen-3.8-max WAJIB-APPARATUS — 2026-11-17

**Perintah:** user 2026-11-17 21:26 "sekarang" (menjalankan tes penentu yang
diusulkan di UJI-PENANTANG-PENULIS-2026-11-17.md §3).
**Sifat:** lab murni. Serve STOP dan tetap STOP; nol submit; TIDAK ada
integrasi yang dipasang; rantai penulis serve TIDAK diubah.
**Pertanyaan penentu:** bisakah qwen-3.8-max MENYITASI PADAT + PRESISI bila
prompt MEWAJIBKAN apparatus sitasi? (Babak 1: qwen menang 0-vs-7 penunjuk
karangan lawan GLM, tapi dengan menyitasi NOL — clean karena absen, rasio
K-2 0,000, tertahan gerbang sendiri.)
**Artefak kerja:** `penantang-penulis-2026-11-17/babak-2/` (template +
prompt per pertanyaan, draf qwen2, JSON mentah per percobaan, log
panggilan, `scores-babak2.json`, penilai `score_babak2.py`, log sitasi
`citation-babak2-log.jsonl`).

---

## 1. Rancangan

- **3 pertanyaan uji:** IDENTIK babak 1 — pertanyaan pilot PIONEER viso 0
  yang draf GLM aslinya ada persis di disk (`PILOT-SPOTCHECK-2026-11-17/`):
  1. `2777178d` — metode deteksi multi-account farming whitelist NFT.
  2. `d94d7e34` — membedakan banyak wallet agen AI satu orang vs banyak orang.
  3. `635a010d` — akses wallet MPC agen AI lintas restart mesin.
- **Sisi qwen babak 2:** jawaban baru via CrowLLM `qwen-3.8-max:free` dengan
  prompt penulis versi WAJIB-APPARATUS (publik-aman; prompt gerbang/rubrik
  internal TIDAK dikirim ke relay). Teks prompt persisnya:

> You are answering a question in a public expert Q&A arena. Write a thorough, well-structured expert answer to the question below.
>
> Requirements:
> - Open with your central thesis in the first paragraph; do not merely restate the question.
> - Cover every part of the question explicitly, in clear sections.
> - CITATION APPARATUS IS MANDATORY in this answer:
>   (a) Every pivotal claim — every key mechanism, precedent, standard, dataset, or precise figure you rely on — must be supported by a named reference attached to the sentence that makes the claim: a full URL, a DOI, a paper/report number (e.g. an IACR ePrint or arXiv number), or the exact title of an official document.
>   (b) Aim for the citation density of a well-referenced expert answer: roughly 10-19 references spread across the answer, attached where the claims are made — not bunched in a list at the end.
>   (c) NEVER invent a reference. Only cite sources you are confident actually exist, with their exact identifiers. If you do not know the precise source for a claim, state the claim in qualified prose WITHOUT a fabricated precise figure or pointer — an honest uncited claim is acceptable; a made-up DOI, URL, or paper number is not.
> - Close with a short synthesis section stating what is new or decisive in your answer.
> - Length: roughly 5,000-7,000 characters.
> - Output only the answer text. No process notes, no reasoning traces, no meta-commentary.
>
> Question:
> {teks pertanyaan persis, sama dengan babak 1}

- **Transport qwen babak 2:** 3 panggilan, SEMUA sukses percobaan pertama
  (200, finish "stop"; latensi 7,8 / 11,3 / 7,1 dtk), jeda ≥13–14 dtk antar
  panggilan dipatuhi, nol retry terpakai, nol kegagalan. Panjang draf:
  5.778 / 5.384 / 5.893 kar — semua di dalam pita PIONEER 3.435–7.297.
- **Penggaris (identik babak 1 + satu tambahan):**
  (a) `provider/citation_verify.py` mode `block`, fetcher nyata — penunjuk
  total, verified, karangan (dead/wrong_document/malformed) poros vs
  pinggiran, vonis TAHAN = `fatal`/`block`;
  (b) **TAMBAHAN: rasio K-2 persis dari fungsi gerbang**
  `openrouter_wrapper.mechanical_floor()` (`bound_ratio`, lantai
  `FLOOR_MIN_BOUND_RATIO = 0,30`), sekaligus lantai K-1(a) ≥1 URL dan
  K-1(b) kepadatan ≥0,5/1.000 kar;
  (c) panjang vs pita PIONEER; (d) jejak proses
  (`serve_gate.detect_thinking_trace`).
  Untuk tabel tiga sisi, hasil sitasi GLM + qwen babak 1 diambil dari
  `scores.json` babak 1 (fetcher nyata, sudah jalan); lantai mekanis +
  trace keenam draf lama dihitung lokal-deterministik dengan fungsi yang
  sama, supaya **vonis kirim gabungan (lapis sitasi + lantai K-1/K-2 +
  trace)** tiga sisi memakai penggaris yang persis sama.

## 2. Tabel tiga sisi per pertanyaan

### Q1 — 2777178d (NFT sybil)

| Sisi | Kar | Penunjuk | Verified | Karangan poros | Karangan pinggiran | Rasio K-2 | Vonis sitasi | Vonis kirim gabungan |
|------|-----|----------|----------|---------------|--------------------|-----------|--------------|----------------------|
| GLM asli | 6.673 | 19 | 14 | 0 | 3 | 0,429 ✓ | findings | **KIRIM** |
| qwen babak 1 (tanpa apparatus) | 5.111 | 0 | 0 | 0 | 0 | 0,000 ✗ | clean | TAHAN (lantai K-1/K-2) |
| qwen babak 2 (wajib apparatus) | 5.778 | 4 | 2 | **2** | 0 | 0,200 ✗ | **fatal** | TAHAN (sitasi + lantai) |

Karangan poros qwen babak 2 Q1: arXiv `2308.12345` wrong_document (klaim
serangan sybil vs paper "Probing Early Modification of Gravity with
Planck, ACT and SPT") + DOI `10.1109/blockchain55366.2022.00012` dead
(404 Crossref + doi.org).

### Q2 — d94d7e34 (wallet satu vs banyak orang)

| Sisi | Kar | Penunjuk | Verified | Karangan poros | Karangan pinggiran | Rasio K-2 | Vonis sitasi | Vonis kirim gabungan |
|------|-----|----------|----------|---------------|--------------------|-----------|--------------|----------------------|
| GLM asli | 7.570 | 11 | 8 | 1 | 1 | 0,833 ✓ | **fatal** | TAHAN (sitasi) |
| qwen babak 1 (tanpa apparatus) | 5.167 | 0 | 0 | 0 | 0 | 0,000 ✗ | clean | TAHAN (lantai K-1/K-2) |
| qwen babak 2 (wajib apparatus) | 5.384 | 8 | 2 | **2** | **4** | 0,846 ✓ | **fatal** | TAHAN (sitasi) |

Karangan qwen babak 2 Q2: poros = arXiv `2205.00123` wrong_document (klaim
"temporal clustering" vs paper mesoscope komputasional) + DOI
`10.1093/cybsec/tyad001` wrong_document (klaim "hub-and-spoke" vs paper
post-quantum governance); pinggiran = URL `w3.org/Security/wiki/
Humanity_Verification` dead 404, `dci.mit.edu/research/governance-ai`
dead 404, `worldcoin.org/blog/announcements/introducing-world-id` dead
404, `vitalik.eth.limo/...` malformed (host tanpa TLD dikenal menurut
lapis).

### Q3 — 635a010d (MPC lintas restart)

| Sisi | Kar | Penunjuk | Verified | Karangan poros | Karangan pinggiran | Rasio K-2 | Vonis sitasi | Vonis kirim gabungan |
|------|-----|----------|----------|---------------|--------------------|-----------|--------------|----------------------|
| GLM asli | 6.964 | 10 | 8 | 1 | 1 | 0,471 ✓ | **fatal** | TAHAN (sitasi) |
| qwen babak 1 (tanpa apparatus) | 4.971 | 0 | 0 | 0 | 0 | 0,000 ✗ | clean | TAHAN (lantai K-1/K-2) |
| qwen babak 2 (wajib apparatus) | 5.893 | 1 | 1 | 0 | 0 | 0,300 ✓ (pas di lantai) | clean | TAHAN (lantai K-1: URL 0 <1; densitas 0,339 <0,5) |

Q3 qwen babak 2 hanya memuat **1 penunjuk** di seluruh draf (arXiv
`2305.12345`, terverifikasi oleh lapis) — mandat kepadatan praktis tidak
dipatuhi; rasio K-2-nya lolos hanya karena 6 dari 20 token angka kebetulan
berada dalam ±150 kar dari 2 rentang sitasi yang terdeteksi lantai.

### Agregat tiga sisi

| Sisi | Penunjuk | Verified | Karangan total | Karangan poros | Tingkat karangan | K-2 lolos | Kirim gabungan |
|------|----------|----------|---------------|----------------|------------------|-----------|----------------|
| GLM asli | 40 | 30 (75%) | 7 | 2 | 17,5% | 3/3 | **1/3** |
| qwen babak 1 | 0 | — | 0 | 0 | — (tak menyitasi) | 0/3 | 0/3 |
| qwen babak 2 | 13 | 5 (38%) | **8** | **4** | **61,5%** | 2/3 | **0/3** |

Jejak proses: **0 di kesembilan draf**. Panjang: kesembilan draf di dalam
atau di atas pita PIONEER (GLM Q2 7.570 di atas pita — catatan (c) babak 1;
qwen babak 2 ketiganya di dalam pita).

**Kepatuhan kepadatan qwen babak 2:** mandat prompt = ±10–19 penunjuk per
draf; aktual **4 / 8 / 1** — di bawah mandat di 3/3 draf (Q2 paling dekat).
Bentuk karangannya khas generasi-dari-plausibilitas: identifier berbentuk
placeholder/berurutan (`arXiv:2308.12345`, `arXiv:2205.00123`,
`ieee.org/document/10123456`) — pola yang sama dengan karangan GLM, hanya
jauh lebih sering.

## 3. Vonis penentu

**Vonis: (ii) — PADAT-PARSIAL TAPI PRESISI JEBOL. GLM BERTAHAN sebagai
penulis; qwen-3.8-max TETAP di kursi pemeriksa.**

Alasan tegas, mengikuti pohon keputusan tes ini:

- Kriteria (i) — layak pengganti — mensyaratkan rasio K-2 lolos **DAN**
  karangan poros 0 di mayoritas draf. Rasio K-2 memang lolos 2/3
  (0,846 dan 0,300), tetapi karangan poros 0 hanya tercapai di **1/3**
  draf (Q3 — dan itu pun dengan hanya 1 penunjuk). Di Q1 dan Q2 qwen
  mengarang masing-masing **2 penunjuk poros** (arXiv salah-dokumen +
  DOI mati/salah-dokumen). Kriteria (i) **GAGAL**.
- Yang terjadi saat apparatus diwajibkan: qwen memang mulai menyitasi
  (13 penunjuk vs 0 di babak 1 — jadi bukan penolakan total seperti
  kriteria (iii)), tetapi **61,5% penunjuknya karangan** (8/13), 3,5×
  tingkat karangan GLM (17,5%), dengan 4 karangan poros — spesies cacat
  yang persis sama dengan yang membuat 2/3 draf GLM tertahan, dalam
  kadar lebih parah. Dua dari tiga drafnya **fatal** di lapis sitasi;
  vonis kirim gabungannya **0/3** — lebih buruk dari GLM (1/3).
- Kepadatan juga belum patuh: 4/8/1 penunjuk vs mandat 10–19. Q3
  menunjukkan kutub sebaliknya — nyaris tetap enggan menyitasi (1
  penunjuk sedraf) sehingga gugur di lantai K-1 walau bersih.
- Kesimpulan mekanismenya: kebersihan babak 1 qwen adalah sifat
  **menghindar**, bukan sifat presisi. Begitu diwajibkan memproduksi
  identifier presisi, ia mengarang dari plausibilitas sama seperti GLM —
  lebih sering, dan dengan porsi poros lebih besar. Tidak ada dasar
  mengganti penulis. Kursi qwen yang terbukti kuat tetap **pemeriksa**
  (juara kalibrasi CrowLLM 6/7, UJI-CROWLLM-PEMERIKSA-2026-11-17) —
  menilai karangan orang lain ternyata keahliannya; memproduksi sitasi
  presisi bukan.

## 4. Kaveat

- **n=3 pertanyaan (9 draf) = sinyal kuat awal**, bukan vonis final
  pergantian penulis untuk semua kelas/pertanyaan; ketiga pertanyaan
  kelas PIONEER.
- Sisi qwen dinilai di bawah **prompt publik** (instruksi penulis umum
  versi wajib-apparatus, bukan prompt serve persis + steering internal) —
  kaveat yang sama dengan babak 1 dan kalibrasi pemeriksa CrowLLM.
- Skor GLM adalah skor draf pilot ASLI (keadaan serve 2026-11-17 pagi),
  bukan generasi ulang.
- Lapis sitasi hanya menilai penunjuk yang ADA dan teresktrak mekanis
  (URL/DOI/ePrint/arXiv/domain); rujukan berupa judul dokumen tanpa
  identifier tidak terhitung sebagai penunjuk oleh lapis ini, dan
  kebenaran isi klaim prosa di luar jangkauannya (batas tegas lapis,
  sama seperti babak 1).
- Rasio K-2 Q3 qwen babak 2 (0,300) lolos persis di lantai dengan basis
  tipis (2 rentang sitasi) — dicatat sebagai lolos, bukan sebagai bukti
  kepadatan.
