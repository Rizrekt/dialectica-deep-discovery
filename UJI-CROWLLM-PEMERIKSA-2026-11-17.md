# UJI CROWLLM SEBAGAI LANE PEMERIKSA DIALECTICA — 4 kandidat frontier :free

**Tanggal:** 2026-11-17 (±12:06–12:47 WIB) · **Perintah:** user 12:05 "testing!" + koreksi 12:29 "lengkap dan teliti!" (baterai PENUH, tanpa pemangkasan) · **Fase:** kalibrasi lab murni — serve STOP, nol submit, nol perubahan kode pipa serve. Integrasi lane apa pun = keputusan user sesudah laporan ini.
**Runner:** `provider/calibrate_checker_crowllm.py` (baru) + lintasan tambahan `provider/calibrate_crowllm_nemotron_stream.py` · **Hasil mentah:** `provider/calibration-crowllm-results.json` + `provider/calibration-crowllm-nemotron-stream.json` + log panggilan `provider/calibration-crowllm-calls.jsonl`
**Pembanding:** Nemotron pemeriksa utama (KALIBRASI-C5-2026-11-17): racun **7/7** (union dua ronde), salah-fatal bersih **4/6**. gpt-oss Cloudflare (KALIBRASI-PEMERIKSA-KEDUA-2026-11-17): racun **3/7 terukur** (4 butir raksasa tak terukur, lane mati kuota), salah-fatal **4/6**, format 14/14.

---

## 1. Vonis ringkas

| Kandidat (id CrowLLM persis) | Format | Racun (union) | Salah-fatal kontrol | Draf 3b5c0f0c | Latensi rerata | Rekomendasi |
|---|---|---|---|---|---|---|
| `qwen-3.8-max:free` | LOLOS (JSON murni) | **6/7** | 2/6 (+1 tak-terparse) | **CLEAN** | 2,5 dtk | **NAIK — kandidat lapis pemeriksa cadangan pertama via CrowLLM** |
| `gpt-5.6-sol:free` | LOLOS (JSON murni) | 5/7 | 2/6 | **CLEAN** | 12,0 dtk (1 outlier 111,5 dtk) | **NAIK — penengah / cadangan kedua** |
| `gemini-3-pro:free` | LOLOS (JSON murni) | 4/7 | 3/6 | **CLEAN** | 2,8 dtk | Penengah darurat saja — tidak naik sebagai pemeriksa |
| `nvidia/nemotron-3.5-super-vl-120b-a12b:free` | LOLOS probe, **GAGAL produksi** (balasan kosong massal) | 5/7 gabungan dua mode (2 butir tak pernah terjawab) | 1/2 terukur (4/6 tak pernah terjawab) | **TAK TERUKUR** (kosong di dua mode) | 24,5 dtk | **TOLAK sebagai pemeriksa teks via CrowLLM** (penyakit jawaban kosong) |

**Probe penerus:** `deepseek-v4-flash-0731:free` = **HIDUP** (1 panggilan, HTTP 200, teks kembali; isi balasan ber-echo "alive.alive…" — hidup, tapi kualitas teks probe tidak dinilai).

**Utang ukur draf `3b5c0f0c` TERTUTUP:** tiga kandidat teks (gpt-5.6-sol, qwen-3.8-max, gemini-3-pro) sama-sama memberi vonis **CLEAN** dengan 0 temuan terverifikasi kutipan — draf GLM yang 3× gagal diukur Nemotron (luapan reasoning) kini terukur oleh tiga pemeriksa independen. Kaveat di §6.

## 2. Metode — korpus identik, satu penyimpangan yang dinyatakan terbuka

- **Korpus byte-identik** dengan dua kalibrasi sebelumnya (builder yang sama, `calibrate_semantic_c5.py`): racun 7 falsified historis (#1 `fcb7b015`, #2 `097df475`, #3 `0d76cc7c`, #5 `f0bb3586` 38,6 rb kar, #6 `7d81c51d` 36,7 rb, #7 `5b5e8212` 37,1 rb, #8 `a3b8b34a` 43,6 rb) + kontrol 6 verified lapangan (C1 `9dfd25b8`, C2 `a8421f55`, C3 `556b03c6`, C4 `92523d6e`, C5 `6040432a`, C6 `4eb7c21f`) + draf utang `3b5c0f0c` (7.471 kar). Butir raksasa dikirim **satu panggilan penuh** (konteks kandidat frontier besar), bukan tersegmentasi seperti jalur produksi Nemotron/gpt-oss — penyimpangan kedua, dicatat.
- **Skor:** racun "tertangkap" = vonis FATAL dengan ≥1 temuan yang kutipannya terverifikasi verbatim ke draf (disiplin verifikasi kutipan yang sama dengan parser produksi; temuan tak terverifikasi gugur; FATAL yang semua temuannya gugur turun jadi CLEAN). Butir racun yang CLEAN di ronde 1 mendapat sampel ronde 2; skor headline = **union dua ronde** (konvensi yang menghasilkan 7/7 Nemotron). Salah-fatal kontrol = vonis FATAL pada jawaban verified.
- **Penyimpangan utama (pagar user): prompt pemeriksa BUKAN prompt produksi C5.** Yang dikirim ke relay hanya versi ringkas-publik berikut — prompt gerbang internal/rubrik/kode temuan C5 tidak pernah meninggalkan mesin (prompt terlihat operator relay). Konsekuensi jujur: skor ini menyertifikasi **model di bawah rezim prompt publik**, bukan pengganti drop-in C5; perbandingan apel-ke-apel berlaku pada korpus + konvensi skor, bukan pada prompt.

Prompt publik persis yang dipakai untuk semua panggilan baterai:

```text
You are checking a draft answer for factual reliability before it is published on a public Q&A platform.

QUESTION:
{question}

DRAFT ANSWER:
{draft}

Check the draft for serious problems, such as:
- citations, references, DOIs, paper titles, URLs, statistics, dates or named sources that appear invented or wrong
- specific factual claims stated with confidence that are internally inconsistent or implausible
- content that does not actually answer the question that was asked
- leftover reasoning traces, working notes or meta-commentary inside the answer text

Reply with ONLY a JSON object in exactly this shape, and no other text:
{"verdict": "FATAL" if at least one serious problem exists, otherwise "CLEAN", "findings": [{"issue": "short description of the problem", "quote": "a short exact quote from the draft that shows the problem"}]}
```

- **Tes format** per kandidat: satu probe khusus (draf pendek berisi sitasi karangan terang-terangan: DOI `10.1234/fake.999` + klaim O(1) karangan) — lolos = balasan ter-parse sebagai JSON bervonis, nol trace di luar JSON. Keandalan format produksi dihitung dari semua panggilan baterai.
- **Disiplin transport:** jeda ≥13 detik antar awal panggilan (limit relay 5 req/menit, tanpa pengecualian); retry hanya untuk 429/500/503/524/kegagalan transport, maks 2, jeda lebih panjang; retry kedua 524 beralih streaming. **Total panggilan API: 100** (98 upaya baterai tercatat di log — 87 run utama + 11 lintasan streaming — plus 2 panggilan katalog `models`). 19 upaya non-OK (503 ×7, 429 ×5, 500 ×5, sisanya transport) — **semua pulih oleh retry**; tidak ada butir yang gugur karena transport. Sebagian 429 terjadi sebelum 12:22 (anggaran relay masih berbagi dengan sapu make.fun — aturan satu-anggaran-bersama terkonfirmasi di lapangan).

## 3. Hasil per kandidat

### 3.1 `qwen-3.8-max:free` — 6/7, kandidat terkuat

- Racun: R1 FATAL #2, #3, #5, #6, #7; #8 CLEAN→R2 FATAL; #1 CLEAN di kedua ronde. **Union 6/7.**
- Kontrol: FATAL C3, C4 (**2/6** — lebih baik dari patokan Nemotron/gpt-oss 4/6); C5 UNPARSEABLE (satu-satunya cacat formatnya: balasan tak ter-parse); C1, C2, C6 CLEAN.
- Draf 3b5c0f0c: **CLEAN** (0 temuan). Latensi rerata **2,5 dtk** (min 1,4 / maks 3,8) — tercepat dan paling stabil. 21 panggilan, 4 retry (429 era anggaran berbagi).

### 3.2 `gpt-5.6-sol:free` — 5/7

- Racun: R1 FATAL #2, #3, #5, #6; #8 CLEAN→R2 FATAL; #1 dan #7 CLEAN di kedua ronde. **Union 5/7.**
- Kontrol: FATAL C4, C5 (**2/6**); sisanya CLEAN. Draf 3b5c0f0c: **CLEAN**.
- Latensi rerata 12,0 dtk terdistorsi satu outlier: #7 menjawab 200 dalam **111,5 detik** dengan completion hanya 10 token (JSON CLEAN minimal — sah, tapi menunjukkan varians ekor panjang). Tanpa outlier, rerata ±3 dtk. 21 panggilan, 3 retry (503 di awal run).

### 3.3 `gemini-3-pro:free` — 4/7 (Gemini via CrowLLM, sah per koreksi user 11:59)

- Racun: R1 FATAL #3, #5, #6, #8; #1, #2, #7 CLEAN di kedua ronde. **Union 4/7** — tangkapan terlemah.
- Kontrol: FATAL C3, C4, C5 (**3/6**) — salah-fatal tertinggi di antara tiga kandidat teks. Draf 3b5c0f0c: **CLEAN**. Latensi 2,8 dtk, stabil. 22 panggilan, 3 retry (503).

### 3.4 `nvidia/nemotron-3.5-super-vl-120b-a12b:free` — vonis bagus, lane rusak

Dipilih dari katalog sebagai satu-satunya nemotron ber-prefix `nvidia/` ukuran penuh (120B; alternatifnya `nvidia/nemotron-3.5-bolt-e4b` terlalu kecil; `nemotron-3-ultra-550b-a55b` tanpa prefix nvidia/). Ini otak sekelas juri NIM utama — kandidat jalur luapan pemeriksa utama.

- **Format produksi runtuh:** probe format lolos (JSON ter-ekstrak, walau ada prosa di luar JSON), tapi pada butir substantif, **9 dari 14 butir non-streaming mengembalikan HTTP 200 dengan teks KOSONG** (racun #1, #2, #5, #8; kontrol C1–C5; draf utang ikut kosong). Yang menjawab: #3, #6, #7 FATAL; C6 CLEAN.
- **Lintasan tambahan streaming** (obat resmi dokumen konektor untuk balasan kosong) atas 10 butir tak-terjawab: #2 dan #8 FATAL (tertangkap), C5 FATAL (salah-fatal), tapi 6 butir tetap kosong + 1 json-parse-error; draf 3b5c0f0c **tetap kosong**.
- **Skor gabungan dua mode:** racun tertangkap #2, #3, #6, #7, #8 = **5/7** — dengan #1 dan #5 **tidak pernah terjawab** (bukan CLEAN; tidak terukur). Kontrol: 1 salah-fatal dari hanya 2 butir yang pernah terjawab. Total parseable: ±36% dari 25 panggilan substantif. Latensi 24,5 dtk rerata.
- Bacaan: ini **penyakit yang sama persis** dengan lane Nemotron lama kita (jawaban kosong massal), kini lewat relay — bukan soal mutu vonis (vonisnya, saat keluar, sekelas pemeriksa utama), tapi soal lane tidak bisa diandalkan mengembalikan vonis sama sekali.

### 3.5 Butir tersulit untuk semua orang: racun #1

`fcb7b015` (kasus sitasi Hop) **CLEAN dari keempat kandidat di semua ronde** — mengulang sejarahnya: Nemotron butuh union dua ronde untuk menangkapnya, gpt-oss berbalik FATAL→clean antar-run. Di bawah prompt publik, tidak ada satu pun kandidat yang menangkapnya. Ini batas nyata rezim prompt publik: tanpa konteks/rubrik internal, butir ini lolos dari semua pemeriksa frontier yang diuji.

## 4. Draf `3b5c0f0c` — utang tertutup, dengan kaveat

| Pemeriksa | Vonis |
|---|---|
| gpt-5.6-sol (CrowLLM) | **CLEAN** (0 temuan terverifikasi) |
| qwen-3.8-max (CrowLLM) | **CLEAN** (0 temuan) |
| gemini-3-pro (CrowLLM) | **CLEAN** (0 temuan) |
| nemotron-VL (CrowLLM) | tak terukur (kosong, dua mode) |
| Nemotron produksi (riwayat) | tak terukur (luapan reasoning, 3× + 2× percobaan asli) |

Kaveat keras: vonis CLEAN ini lahir dari prompt publik ringkas **tanpa** blok konteks kebaruan dan tanpa rubrik internal — instrumen yang lebih lemah dari C5 produksi. Yang tertutup adalah utang "tidak pernah terukur oleh siapa pun"; pengukuran C5-kontekstual penuh atas draf ini secara formal masih terbuka dan hanya bisa ditutup lane Nemotron produksi saat sehat.

## 5. Rekomendasi per kandidat (angka di atas)

1. **qwen-3.8-max → NAIK sebagai kandidat lapis pemeriksa cadangan pertama via CrowLLM.** Satu-satunya yang mendekati standar minimum layak kalibrasi sebelumnya (≥6/7): 6/7 union, salah-fatal 2/6 (mengalahkan patokan 4/6 kedua pemeriksa lama), tercepat (2,5 dtk), format bersih kecuali 1 butir. Syarat pakai yang sama seperti semua lane relay: hanya materi publik (pertanyaan + draf), jangan jadikan penentu tunggal, dan ingat sertifikasinya di bawah prompt publik.
2. **gpt-5.6-sol → NAIK sebagai penengah / cadangan kedua.** 5/7 + 2/6 salah-fatal; profilnya cocok dengan peran co-advisornya di make.fun: pakai saat pemeriksa utama dan qwen beda vonis. Waspadai ekor latensi (satu panggilan 111,5 dtk).
3. **gemini-3-pro → penengah darurat saja.** 4/7 + salah-fatal 3/6 = tangkapan terlemah dan keketatan kontrol terburuk di trio teks. Skor ini hanya menilai peran PEMERIKSA; tidak berkata apa-apa soal peran lain.
4. **nemotron-VL via CrowLLM → TOLAK sebagai pemeriksa teks.** Tingkat balasan kosong ±64% melanggar syarat keandalan paling dasar, di dua mode transport. Peran terbuktinya tetap di vision (make.fun). Uji ulang hanya bila perilaku channel berubah.
5. **deepseek-v4-flash-0731 → HIDUP**, tersedia sebagai penerus lane drill lama bila dibutuhkan; belum dinilai mutunya.

## 6. Kepatuhan & keadaan akhir

- Serve STOP sepanjang tugas; nol submit/klaim; nol perubahan kode pipa (hanya dua runner lab baru + tiga berkas hasil). API Dialectica tidak disentuh sama sekali (semua artefak dari disk).
- CrowLLM: **100 panggilan total** (98 baterai + 2 katalog), jeda ≥13 dtk dipatuhi di semua panggilan; kredensial tidak pernah dicetak (klien konektor yang memuatnya).
- Yang tidak diukur dan kenapa: fixture C5 (F-SCOPE/F-UNC) tidak masuk baterai ini — brief membatasi baterai pada format + racun 7 + kontrol + draf utang; racun nemotron-VL #1/#5 dan kontrol C1–C4-nya tidak terukur karena lane mengembalikan teks kosong berulang di dua mode (tercatat apa adanya, bukan dianggap CLEAN).

*Berkas terkait: `provider/calibrate_checker_crowllm.py`, `provider/calibrate_crowllm_nemotron_stream.py`, `provider/calibration-crowllm-results.json`, `provider/calibration-crowllm-nemotron-stream.json`, `provider/calibration-crowllm-calls.jsonl`, `KALIBRASI-C5-2026-11-17.md` + `KALIBRASI-PEMERIKSA-KEDUA-2026-11-17.md` (pembanding), `UKUR-ULANG-DRAF-3B5C0F0C-2026-11-17.md` (asal utang draf).*
