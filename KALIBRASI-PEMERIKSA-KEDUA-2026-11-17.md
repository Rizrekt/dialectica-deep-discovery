# KALIBRASI PEMERIKSA KEDUA C5 — gpt-oss-120b (Cloudflare) sebagai Kandidat Lane Pemeriksa Cadangan

**Tanggal:** 2026-11-17 (±07:05–07:50 WIB) · **Konteks:** item 3 dari 5, perintah user "gas satu-satu" · **Fase:** testing — kalibrasi offline/shadow; nol serve/submit/klaim; C5 tetap shadow; lane pemeriksa produksi TIDAK diubah oleh berkas ini.
**Runner:** `provider/calibrate_checker_gptoss.py` (baru) · **Hasil mentah:** `provider/calibration-c5-gptoss-results.json` + probe `/tmp/gptoss-probe.json` · **Log pemeriksa:** `provider/calibration-gptoss-semantic-log.jsonl`

**Vonis akhir: LAYAK BERSYARAT** — layak jadi lane pemeriksa cadangan (fallback ke-2) untuk draf ukuran klaim/serve-pendek, dengan syarat tertulis di §6. TIDAK tersertifikasi untuk draf raksasa (jejak serve 37–44 rb kar) karena korpusnya tidak sempat terukur — lane mati di tengah run oleh kuota akun, bukan oleh perilaku model (§5).

---

## 1. Ukuran keberhasilan (dinyatakan di awal, sesuai brief)

| Ukuran | Target | Pembanding Nemotron (KALIBRASI-C5-2026-11-17) |
|---|---|---|
| (a) Tangkapan racun falsified | setara 7/7; minimum layak 6/7 dengan yang lolos dianalisis | 7/7 lintas dua ronde |
| (b) Salah-fatal di 6 verified lapangan | ≤ 4/6 = setara; < 4/6 = lebih baik | 4/6 |
| (c) Keandalan | fraksi invokasi unavailable / gagal-parse sekecil mungkin | lane Vyce: reasoning-overflow berulang (item 2 kemarin: 10/14 unavailable) |
| (d) Biaya | neuron per pemeriksaan + total kalibrasi ≤ 3.000 | — (OpenRouter: kuota request, bukan neuron) |

## 2. Metode — dan setiap penyimpangan, terukur

- **Jalur kode produksi, tanpa fork:** pemeriksaan berjalan lewat `serve_gate.semantic_check` persis seperti produksi (prompt pemeriksa yang sama byte-per-byte, parser + verifikasi kutipan yang sama, mode shadow). Yang diganti hanya seam `model_call`: satu panggilan per segmen ke `@cf/openai/gpt-oss-120b` lewat klien connector Cloudflare terdaftar, `max_tokens` 8000 (sama dengan lane pemeriksa OpenRouter). Klien connector sudah memisahkan field `reasoning` dari `content` — reasoning tidak pernah tercampur ke balasan yang diparse; panjangnya dicatat sebagai diagnostik.
- **Korpus identik** dengan kalibrasi Nemotron (builder yang sama di `calibrate_semantic_c5.py`): 7 falsified historis + 6 verified lapangan + 3 fixture, ditambah 2 draf utang ukur dari PERBAIKAN-PENGHAMBAT.
- **Penyimpangan 1 — jalur tersegmentasi, bukan satu panggilan 28 rb.** Angka Nemotron dihasilkan pra-segmentasi (satu panggilan, cap 28 rb kar). Run ini memakai jalur produksi SAAT INI (segmen 10 rb kar) — jalur yang benar-benar akan dipakai gpt-oss bila dipasang. Konsekuensi: perbandingan bersifat "gpt-oss sebagaimana akan bertugas" vs "Nemotron sebagaimana terkalibrasi", bukan A/B satu panggilan.
- **Penyimpangan 2 — urutan item diatur ulang demi anggaran.** Biaya terukur probe: **221,7 neuron untuk SATU panggilan segmen** (4.708 token; reasoning ±1.800 dari 1.976 token completion) → korpus penuh 34 panggilan mustahil muat di plafon 3.000. Urutan dijalankan: racun pendek (#1–#3) → bersih (segmen-tunggal dulu) → draf utang → fixture → racun raksasa (#5–#8). Urutan tidak mengubah kondisi per item; ia menentukan apa yang keburu terukur bila anggaran/kuota habis — dan kuota memang habis (§5).
- **Penyimpangan 3 — item #1 diukur dua kali.** Probe awal (221,7 n) + run utama (219,8 n) — keduanya panggilan nyata, keduanya terhitung ke plafon. Hasilnya berbeda (lihat §3) dan keduanya dilaporkan; tidak ada yang dibuang.
- **Cacat runner yang ditemukan:** pesan error lane hanya menangkap stderr klien, padahal badan error API (429) ditulis klien ke stdout — selama run, kegagalan terbaca sebagai "client rc=1: (kosong)". Diagnosis §5 didapat dari panggilan manual. Setiap pemasangan produksi wajib memperbaiki ini (syarat §6.4).

## 3. Hasil (a) — korpus racun: TIDAK TUNTAS (3 dari 7 item terukur)

| Item | Ekspektasi | gpt-oss | Neuron | Catatan |
|---|---|---|---|---|
| #1 `fcb7b015` | S-2 | probe: **FATAL** (A_CITATION/S-1) · run utama: **clean** (3 temuan gugur di verifikasi kutipan) | 221,7 + 219,8 | **Varians antar-run nyata** — item yang sama berbalik vonis. Dengan konvensi union dua ronde yang sama seperti kalibrasi Nemotron (#3 mereka: clean R1 → FATAL R2, dihitung tertangkap): tertangkap 1 dari 2 sampel. Sebagai sampel tunggal: lolos. |
| #2 `097df475` | S-1+S-3 | **FATAL** (S-1 ×3; 2 gugur) | 188,9 | S-1 kena padat; S-3 (EIP-1559-di-BSC) tidak terlabel — pola yang sama persis dengan Nemotron (tertangkap sebagai A_CITATION tanpa label S-3) |
| #3 `0d76cc7c` | ≥1 temuan | **FATAL** (CUSTOMER_REQUIREMENTS) | 146,8 | Kode tangkapan identik dengan Nemotron ronde 2 (draf menyimpang dari yang diminta) |
| #5 `f0bb3586` (38,6 rb kar, 4 segmen) | S-1 | **tidak terukur** — lane mati | 0 | §5 |
| #6 `7d81c51d` (36,7 rb kar, 4 segmen) | S-1 | **tidak terukur** — lane mati | 0 | §5 |
| #7 `5b5e8212` (37,1 rb kar, 4 segmen) | S-1+S-4 | **tidak terukur** — lane mati | 0 | §5 |
| #8 `a3b8b34a` (43,6 rb kar, 5 segmen) | S-1+S-4 | **tidak terukur** — lane mati | 0 | §5 |

**Skor yang bisa dinyatakan:** item terukur 3/3 tertangkap secara union (2/3 pada sampel tunggal run utama). **Skor 7/7 atau 6/7 TIDAK bisa dinyatakan** — empat item tak terukur adalah justru kelas terberat (jejak serve raksasa), kelas yang sama yang membuat Nemotron-Vyce kolaps reasoning-overflow. Syarat minimum layak 6/7 **belum terpenuhi buktinya** — bukan karena gagal, karena belum diuji. Estimasi biaya menuntaskannya: 17 panggilan segmen × ±190 n ≈ **±3.200 neuron** (satu anggaran tugas penuh lagi, di hari UTC baru).

## 4. Hasil (b) — korpus bersih: 4/6 fatal = SETARA Nemotron

| Item | Nemotron R2 | gpt-oss | Kode gpt-oss |
|---|---|---|---|
| C1 `9dfd25b8` | FATAL | **FATAL** | A_CITATION/S-2 |
| C2 `a8421f55` (24,0 rb kar, 3 segmen) | clean | **FATAL** | A_CITATION/S-2 + CUSTOMER_REQUIREMENTS |
| C3 `556b03c6` (13,4 rb kar, 2 segmen) | clean | clean | — (1 gugur) |
| C4 `92523d6e` | FATAL | **FATAL** | A_CITATION/S-1 ×2 |
| C5 `6040432a` | FATAL | clean | — (1 gugur) |
| C6 `4eb7c21f` | FATAL | **FATAL** | A_CITATION/S-1 |

**Skor: fatal 4/6 — persis sama dengan Nemotron (4/6), memenuhi kriteria "setara".** Himpunan itemnya berbeda (irisan fatal: C1, C4, C6; C5 lolos di gpt-oss tapi fatal di Nemotron; C2 sebaliknya) — konsisten dengan dua pemeriksa sama-ketat yang mengambil sampel berbeda, bukan dengan satu yang lebih longgar. Interpretasi KALIBRASI-C5 tetap berlaku: mayoritas temuan fatal di korpus bersih adalah setia-rubrik-lebih-ketat-dari-panel (jawaban ini VERIFIED karena panel meloloskan, bukan karena sempurna terhadap rubrik) — jadi 4/6 di sini adalah angka keketatan, bukan angka kesalahan.

## 5. Hasil (c)+(d) — keandalan & biaya, dan peristiwa matinya lane

**Fase hidup (14 panggilan: 1 probe + 13 run utama): sempurna secara format.**
- 14/14 panggilan menghasilkan balasan terparse: **0 non-JSON, 0 konten kosong, 0 reasoning-overflow** — dua spesies gagal yang berulang kali membunuh lane Nemotron (di paket penghambat: balasan non-JSON + reasoning 29.787 kar → kosong; di item 2: 10/14 unavailable) **tidak muncul satu kali pun** di gpt-oss. Reasoning per panggilan 1.257–7.188 kar — selalu ada, tidak pernah memanggang habis budget konten pada `max_tokens` 8000.
- Temuan gugur di verifikasi kutipan: 11 dari 11 item terukur (0–3 per item) — bukti lemah dibuang seperti desain; arahnya aman.
- Latensi: 15–64 detik per item (segmen tunggal 15–44 dtk).

**Peristiwa mati lane (sesudah 14 panggilan sukses):** mulai item D-GLM, 21 panggilan berturut-turut gagal dalam ±1 detik. Diagnosis terverifikasi (panggilan manual ke klien, 2026-11-17 ±07:4x WIB):

> HTTP **429**, code **4006**: *"you have used up your daily free allocation of 10,000 neurons, please upgrade to Cloudflare's Workers Paid plan"* — alokasi free harian **akun** habis.

Akuntansi: pemakaian termeter kalibrasi ini = **2.536,0 neuron** dari 10.000 pool akun. `token-usage.jsonl` hari UTC ini hanya memuat 2.536,0 itu — jadi ±7.464 neuron sisanya terpakai lewat jalur di luar pencatatan berkas ini (konsumen lain di akun yang sama). Matinya lane **bukan** perilaku model dan **bukan** plafon tugas (3.000 tidak terlampaui: total 2.536,0; sisa plafon 464,0 tidak bisa dipakai karena lane sudah mati sampai reset 00:00 UTC).

**Fraksi unavailable, dinyatakan dua cara:**
- Per invokasi `semantic_check`: 19 invokasi dicoba (1 probe + 18 run utama) → 11 ber-vonis, 8 unavailable — **semua 8 dari satu peristiwa kuota akun yang sama**, 0 dari perilaku model.
- Per panggilan segmen: 35 dicoba → 14 sukses, 21 gagal (seluruhnya 429 yang sama).

**Biaya (d):**
- Per panggilan segmen sukses: **123–291 neuron** (rerata ±181). Per item: segmen-tunggal 123,3–221,7; C3 (2 segmen) 351,0; C2 (3 segmen) 581,5.
- Total kalibrasi: **2.536,0 neuron** (di bawah plafon 3.000).
- Implikasi produksi: satu pemeriksaan draf raksasa (4–5 segmen) ≈ **760–970 neuron ≈ 8–10% pool harian akun per cek**. Pilot 10 generasi/hari yang seluruhnya jatuh ke lane ini bisa memakan 1.200–9.700 neuron/hari — ujung atasnya menabrak seluruh pool. Lane ini hanya masuk akal sebagai fallback, bukan primer.

## 6. Draf utang ukur (dari PERBAIKAN-PENGHAMBAT)

| Draf | Hasil gpt-oss | Catatan |
|---|---|---|
| D-GPTOSS — draf penulis gpt-oss, 8.005 kar (ISR 8a4e9623) | **CLEAN** (0 temuan terverifikasi, 1 gugur; 178,4 n) | Utang TERTUTUP — tapi dengan caveat keras: ini **model memeriksa tulisannya sendiri** (penulis = pemeriksa = gpt-oss), bukan cek silang. Hasil clean-nya bukti lemah; ia menutup utang "pernah terukur", bukan utang "terukur secara independen". |
| D-GLM `3b5c0f0c` — draf GLM, 7.471 kar | **tidak terukur** — panggilan pertama sesudah lane mati (429) | Utang TETAP TERBUKA. Ironisnya inilah item cek-silang yang sebenarnya (GLM ditulis, gpt-oss memeriksa). Penyebab: kuota akun (§5), bukan draf, bukan pemeriksa. |

## 7. Vonis: LAYAK BERSYARAT — syarat pemakaian

gpt-oss-120b **layak menjadi lane pemeriksa cadangan** dengan syarat:

1. **Posisi: fallback ke-2 (lane ketiga keseluruhan)** — sesudah OpenRouter-Nemotron dan Vyce-Nemotron. Bukan primer (biaya neuron per cek + pool akun bersama), bukan satu-satunya fallback untuk draf >28 rb kar (belum tersertifikasi di kelas itu).
2. **Sertifikasi racun belum lengkap:** sebelum lane ini boleh diandalkan sebagai penentu apa pun (apalagi mendekati blocking), tuntaskan #5–#8 di hari UTC baru (anggaran ±3.200 n) dengan target union ≥6/7. Sampai itu, statusnya: terbukti di draf ≤24 rb kar (racun pendek 3/3 union, bersih 4/6 setara Nemotron, format 14/14).
3. **Vonis clean dari lane ini = satu sampel, bukan pembebasan.** Varians terukur (#1 berbalik FATAL→clean antar dua run): dalam tugas fallback, vonis fatal-nya boleh ditindaklanjuti; vonis clean-nya berbobot lebih ringan daripada clean Nemotron.
4. **Pre-flight neuron wajib + perbaikan pelaporan error:** sebelum memanggil lane ini, cek pemakaian akun hari-UTC (pool 10.000 dibagi semua lane Cloudflare); dan badan error klien ada di **stdout**, bukan stderr — pemasangan yang membaca stderr saja akan buta terhadap 429 seperti runner kalibrasi ini sempat buta.
5. **Metering per panggilan wajib** ditulis ke `token-usage.jsonl` (runner ini melakukannya, lane `cloudflare-gptoss`, tag `c5calib-*`) supaya abort-line 9.000 di `cloudflare_provider` tetap jujur.
6. **Utang lanjutan:** D-GLM `3b5c0f0c` + fixture 3/3 + racun #5–#8 — satu run penuntas di hari UTC baru menutup semuanya (estimasi total ±3.900 n termasuk D-GLM ±190 dan fixture ±600).

**Rancangan pasang (USULAN — tidak dipasang oleh tugas ini):** di `default_semantic_model_call`, tambah tahap ketiga `("cloudflare-gptoss", _semantic_call_cloudflare)` yang: (i) menolak jalan bila pemakaian neuron akun hari-UTC + estimasi segmen melampaui ambang aman (mis. sisa pool < 1.500); (ii) memanggil klien connector dengan prompt yang sama, `max_tokens` 8000; (iii) menangkap badan error dari stdout; (iv) mencatat neuron per panggilan ke `token-usage.jsonl`. Urutan fallback menjadi: OpenRouter-Nemotron → Vyce-Nemotron → Cloudflare-gpt-oss. Mode tetap shadow; tidak ada perubahan urutan dua lane pertama.

## 8. Kepatuhan & keadaan akhir

- OpenRouter: **0 panggilan** (kuota sisa 1 tidak disentuh). Vyce: 0 panggilan. Cloudflare: 35 panggilan dicoba, **2.536,0 neuron** total — di bawah plafon tugas 3.000.
- Kode produksi: **tidak ada yang diubah** — hanya berkas baru `provider/calibrate_checker_gptoss.py` (tidak ada file lama yang dimodifikasi, jadi tidak ada backup yang perlu dibuat). Suite provider sesudah tugas: **270/270 hijau** (test_cloudflare_claim_path 8 · cloudflare_serve 33 · dashscope_claim_path 11 · improve_20261116 17 · novelty_context 33 · openrouter_claim_path 10 · openrouter_wrapper 30 · semantic_check 40 · serve_gate 51 · target_picker 24 · zai_claim_path 13) — sama dengan basis.
- Yang TIDAK selesai dan penyebabnya, diringkas: racun #5–#8, fixture ×3, D-GLM — semuanya satu penyebab: **alokasi neuron harian akun Cloudflare habis (429/code 4006) di tengah run**, terverifikasi manual; bukan kegagalan model, bukan plafon tugas.

---

*Berkas terkait: `provider/calibrate_checker_gptoss.py`, `provider/calibration-c5-gptoss-results.json`, `provider/calibration-gptoss-semantic-log.jsonl`, `KALIBRASI-C5-2026-11-17.md` (pembanding Nemotron), `PERBAIKAN-PENGHAMBAT-2026-11-17.md` (asal dua draf utang), `provider/cloudflare_provider.py` (lane penulis cadangan, abort-line neuron).*

---

## 9. ADDENDUM PENUNTAS — 2026-11-18 (persetujuan user eksplisit 07:17 WIB: "Lanjut — jalankan kalibrasi racun Cloudflare #5–#8")

Utang §6.2 + §6.6 DITUNTASKAN. Run penuntas memakai runner, korpus, prompt, dan penggaris yang identik dengan ronde 2026-11-17; hasil per invokasi di berkas terpisah `provider/calibration-c5-gptoss-20261118-a.json` (A), `-b.json` (B), `-c.json` (C).

**Kejujuran prosedural (dua penyimpangan, dinyatakan terbuka):**
1. **Probe tak terencana.** Pemanggilan `calibrate_checker_gptoss.py --help` di awal sesi ternyata BUKAN no-op — runner mem-parse argumen secara manual dan tidak mengenal `--help`, sehingga ia mulai menjalankan korpus dari item pertama. Proses dihentikan paksa sesudah **1 panggilan nyata** (racun #1, 211,5 neuron, vonis **FATAL** A_CITATION ×2). Panggilan itu sekaligus menjadi verifikasi pool hari baru (lane menjawab 200) dan sampel ketiga untuk item #1.
2. **Berkas hasil lama tertimpa sebagian.** Run terputus itu menulis ulang `calibration-c5-gptoss-results.json` menjadi hanya 1 hasil (#1 hari ini). Angka ronde 2026-11-17 TIDAK hilang: terdokumentasi lengkap di §3–§6 dokumen ini dan log append-only `calibration-gptoss-semantic-log.jsonl` tetap utuh. Semua invokasi penuntas sesudahnya memakai `--out` terpisah.

**Hasil per butir (semua segmen utuh, 0 error, 0 unavailable):**

| Item | Ekspektasi | Vonis | Neuron | Segmen |
|---|---|---|---|---|
| #5 `f0bb3586` | S-1 | **FATAL** (A_CITATION padat, S-1 terlabel; +S-4) | 947,9 | 4/4 |
| #6 `7d81c51d` | S-1 | **FATAL** (A_CITATION, S-1 ×18) | 991,4 | 4/4 |
| #7 `5b5e8212` | S-1+S-4 | **FATAL** (S-1 + S-4, keduanya terlabel) | 1.048,6 | 4/4 |
| #8 `a3b8b34a` | S-1+S-4 | **FATAL** (S-1 + S-4, keduanya terlabel) | 1.106,3 | 5/5 |
| D-GLM `3b5c0f0c` | (utang ukur) | **FATAL** (A_CITATION/S-1 + A_UNCERTAINTY) | 171,2 | 1/1 |
| F-SCOPE `fixture-scope` | A_SCOPE | **FATAL** (A_SCOPE persis) | 95,1 | 1/1 |
| F-UNC-BAD `fixture-unc-bad` | A_UNCERTAINTY | **FATAL** (A_UNCERTAINTY + A_CITATION/S-1 + A_REASONING) | 131,5 | 1/1 |
| F-UNC-OK `fixture-unc-ok` | clean | **CLEAN** (kontrol fixture tidak salah-fatal) | 82,4 | 1/1 |

**Skor racun FINAL gpt-oss-Cloudflare: 7/7 secara union** — syarat minimum §6.2 (union ≥6/7) **TERPENUHI**. Kelas raksasa yang dulu tak terukur kini **4/4 FATAL dengan label ekspektasi terpenuhi penuh**. Satu-satunya catatan varians tetap item #1: clean pada sampel tunggal run utama 17 Nov, FATAL pada probe 17 Nov dan run 18 Nov (2 dari 3 sampel) — peringatan §6.3 (vonis clean lane ini = satu sampel berbobot ringan) tetap berlaku penuh.

**Salah-fatal bersih FINAL: 4/6** (korpus bersih tuntas 17 Nov, tidak diukur ulang) + kontrol fixture F-UNC-OK clean.

**Kontras rezim pada D-GLM `3b5c0f0c`:** draf yang sama divonis **CLEAN oleh 3 pemeriksa CrowLLM** di baterai prompt-publik (UJI-CROWLLM-PEMERIKSA-2026-11-17) dan **FATAL di sini** pada rezim prompt produksi penuh. Bukan kontradiksi — bukti terukur bahwa rezim prompt mengubah vonis; skor prompt-publik memang bukan drop-in C5, persis kaveat dokumen CrowLLM itu. Utang ukur 3b5c0f0c dengan ini TERTUTUP di kedua rezim.

**Keandalan & biaya hari ini:** 22/22 panggilan sukses terparse (0 gagal format, 0 unavailable) — digabung fase hidup 17 Nov: **36/36 panggilan sukses bersih secara format** (di luar peristiwa kuota akun). Total neuron hari ini **4.786,0** (probe 211,5 + A 1.939,3 + B 2.154,9 + C 480,3), rerata ±218/panggilan; satu cek draf raksasa terbukti **±950–1.100 neuron ≈ 10% pool harian akun** — angka §5 terkonfirmasi, bukan estimasi lagi.

**Tabel final berdampingan:**

| Pemeriksa | Racun | Salah-fatal bersih | Biaya/latensi | Lane |
|---|---|---|---|---|
| Nemotron | **7/7** (dua ronde) | 4/6 | kuota request | milik sendiri |
| qwen-3.8-max | 6/7 | **2/6** | 2,5 dtk | CrowLLM (relay) |
| gpt-5.6-sol | 5/7 | **2/6** | ±12 dtk | CrowLLM (relay) |
| gpt-oss-120b (Cloudflare) | **7/7** (union; #1 varians) | 4/6 | ±218 n/panggilan; raksasa ±1.000 n/cek | milik sendiri |

**Vonis posisi FINAL: cadangan terakhir (lapis ke-4)** — Nemotron → qwen-3.8-max → gpt-5.6-sol → **gpt-oss-Cloudflare**. Alasan angka: tangkapan setara Nemotron, tetapi (i) salah-fatal 4/6 = terkotor di antara para cadangan → tidak layak jadi penengah sengketa; (ii) biaya neuron nyata lawan pool bersama 10.000/hari → tidak layak di depan lane relay yang gratis dan lebih bersih; (iii) varians antar-run di #1. Nilai uniknya yang tidak dimiliki cadangan lain: **satu-satunya cadangan di lane milik sendiri (bukan relay) yang kini tersertifikasi penuh termasuk kelas raksasa** — penutup bila seluruh jalur relay mati. Status naik dari "LAYAK BERSYARAT, sertifikasi belum lengkap" menjadi **TERSERTIFIKASI sebagai cadangan terakhir**; syarat §6.3–§6.5 (clean = satu sampel, pre-flight neuron + error dari stdout, metering per panggilan) tetap mengikat. Pemasangan fallback ini ke `default_semantic_model_call` TIDAK dilakukan oleh tugas ini (kalibrasi saja) — keputusan pasang terpisah.

*Berkas hasil penuntas: `provider/calibration-c5-gptoss-20261118-a.json`, `-b.json`, `-c.json`.*
