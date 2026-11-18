# RANTAI PEMERIKSA CADANGAN — TERPASANG 2026-11-18

**Keputusan:** user 2026-11-18 07:16 — "ydh pasang" (menyetujui pemasangan
rantai pemeriksa cadangan yang datanya lengkap sejak 2026-11-17 21:14).
**Keadaan saat pasang:** serve STOP, unit `dialectica-serve.service`
disabled + inactive, nol submit. Rantai ini hanya akan menyala pada serve
berikutnya yang user sendiri nyalakan.
**Basis kalibrasi:** UJI-CROWLLM-PEMERIKSA-2026-11-17.md (baterai penuh,
korpus identik KALIBRASI-C5, prompt publik) + rancangan fallback
KALIBRASI-PEMERIKSA-KEDUA-2026-11-17.md §7.

---

## 1. Susunan terpasang

| Urutan | Lane | Model | Kalibrasi (rezim prompt publik) |
|---|---|---|---|
| Utama | lane sendiri (OpenRouter → Vyce) | Nemotron C5, prompt gerbang penuh | racun **7/7** (union), salah-fatal 4/6 |
| Cadangan pertama | CrowLLM | **qwen-3.8-max:free** | racun **6/7** (union), salah-fatal **2/6**, 2,5 dtk |
| Penengah / cadangan kedua | CrowLLM | **gpt-5.6-sol:free** | racun **5/7**, salah-fatal **2/6**, 12,0 dtk |

Kode:

- `provider/crowllm_checker.py` (BARU) — transport + vonis lane relay:
  prompt publik, parser, verifikasi kutipan, retry, pacing. Pola panggil
  di-port **verbatim** dari runner kalibrasi `calibrate_checker_crowllm.py`
  (klien connector yang sama, `--max-tokens 4000`, prompt lewat berkas
  sementara, retry 429/500/503/524 maks 2 dengan jeda membesar, 524 →
  streaming di percobaan berikutnya).
- `provider/serve_gate.py` — fungsi baru `chained_semantic_check()` +
  `checker_chain_enabled()`; `armed_semantic_check()` kini merutekan ke
  rantai bila armed (lihat §3). **Perilaku pemeriksa utama TIDAK diubah:**
  `semantic_check`, prompt internal, segmentasi, dan dua lane Nemotron-nya
  persis seperti sebelum rantai ada.
- `provider/run_serve.py` — arming `DIALECTICA_CHECKER_CHAIN=1` di cabang
  gated Vyce serve, pola yang sama dengan lapis lain.

Model bisa diganti lewat env (`DIALECTICA_CHAIN_BACKUP_MODEL`,
`DIALECTICA_CHAIN_ARBITER_MODEL`) — mengganti model = mengganti lane
tersertifikasi, jadi pergantian apa pun wajib kalibrasi ulang dulu.

## 2. Aturan menyala — persisnya

1. **Utama FATAL (tersedia) = FINAL.** Temuan berkuotasi terverifikasi
   adalah arah yang meyakinkan; tidak ada lane relay yang dibakar untuk
   menebak-nebaknya.
2. **Cadangan (qwen) menyala HANYA bila:**
   - utama **unavailable** (transport mati / luapan konteks — spesies
     kegagalan draf `3b5c0f0c`, yang 3× tidak terukur oleh utama dan
     akhirnya diukur CLEAN oleh tiga pemeriksa CrowLLM), **atau**
   - utama vonis **CLEAN** — satu clean adalah satu sampel, bukan
     pembebasan (aturan §7 butir 3 KALIBRASI-PEMERIKSA-KEDUA: vonis
     clean berbobot lebih ringan daripada fatal), jadi clean selalu
     mendapat sampel kedua dari lane independen.
3. **Sengketa** (utama clean vs cadangan FATAL) diputus **penengah**
   (gpt-5.6-sol): penengah FATAL → rantai FATAL (temuan yang berlaku =
   temuan cadangan); penengah clean → clean utama pulih (2-dari-3).
4. **Kaskade mati lane:** cadangan mati → lane penengah bertugas sebagai
   cadangan kedua langsung. Penengah mati di tengah sengketa → vonis
   utama **berdiri**, sengketa dicatat `dispute_unresolved` beserta
   temuan cadangannya, peringatan keras ke stderr, dan **tidak ada yang
   diblokir** karenanya. Bentuk yang sama berlaku bila cadangan pertama
   mati dan cadangan kedua FATAL melawan clean utama (tidak ada lane
   penengah tersisa).

**Perilaku tak-terukur (rantai habis tanpa vonis), dinyatakan persis:**
bila TIDAK ADA lane yang menghasilkan vonis, rantai mengembalikan hasil
unavailable pemeriksa utama **apa adanya** — `verdict "unavailable"`,
`performed=False`, `block=False` di SEMUA mode. Draf tidak dinyatakan
lolos bersih dan tidak ditahan oleh tahap ini; kegagalannya keras
(peringatan stderr pemeriksa utama + satu record log yang bidang
`chain.lanes`-nya menamai kegagalan tiap lane). Ini doktrin unavailable
lama pemeriksa utama, diwarisi — bukan doktrin baru. Kegagalan transport
relay (503/524/429 sesudah retry, atau balasan tak terparse) adalah kelas
**unavailable** — bukan vonis bersih, bukan tahan otomatis.

**Mode:** rantai mewarisi mode tahap semantik (`DIALECTICA_SEMANTIC_MODE`,
bawaan **shadow** per keputusan user 06:12): `block=True` hanya bila mode
block DAN vonis akhir rantai fatal. Di shadow, rantai tidak pernah
menahan draf — termasuk vonis fatal hasil sengketa.

**Log:** tepat **satu record per cek** ke `semantic-check-log.jsonl`
(cek utama di dalam rantai berjalan dengan log ditekan). Bidang
`checker` menamai lane yang benar-benar memberi vonis akhir (mis.
`openrouter-nemotron`, `crowllm-qwen-3.8-max`, `crowllm-gpt-5.6-sol`,
atau gabungan persetujuan `openrouter-nemotron+crowllm-qwen-3.8-max`);
detail lengkap per lane hidup di bidang `chain` (`lanes`, `dispute`,
`dispute_unresolved`, `decided_by`, `backup_reason`, `disputed_findings`).

## 3. Pagar relay — yang boleh dan tidak boleh menyeberang

- Yang dikirim ke CrowLLM **hanya**: teks pertanyaan (blok konteks
  kebaruan **dilucuti** — rezim kalibrasi hanya membawa pertanyaan +
  draf) dan teks draf. Keduanya publik-by-design (terbit di platform).
- Prompt-nya adalah `PUBLIC_PROMPT` di `crowllm_checker.py` —
  **byte-identik** dengan prompt kalibrasi di
  `calibrate_checker_crowllm.py`. Rubrik live arena, kode temuan,
  pola racun S-1..S-4, dan seluruh prompt gerbang internal **tidak
  pernah** dikirim ke relay (prompt terlihat operator relay).
- Konsekuensi yang dinyatakan terbuka: **skor kalibrasi di §1
  menyertifikasi rezim prompt publik ini** — kemampuan lane relay
  menilai di bawah prompt internal tidak pernah diukur dan tidak
  diklaim. Temuan lane relay karenanya berbentuk `{issue, quote}`
  tanpa kode rubrik (di hasil gerbang: `code=None`, `source=<lane>`) —
  kode tidak dikarang untuk meniru rubrik.
- Cek relay menilai draf **utuh dalam satu panggilan** (persis rezim
  kalibrasinya), bukan per segmen seperti pemeriksa utama.

## 4. Pacing & anggaran bersama

- Jeda **≥13 detik antar awal panggilan** relay, ditegakkan di modul
  (`_pace`, jam monotonik) — limit akun CrowLLM 5 req/menit adalah
  **anggaran bersama semua proyek**; rantai tidak membanjiri: maks
  2 panggilan relay per draf (cadangan + penengah), dan hanya pada
  draf yang lolos aturan menyala §2 (utama fatal = 0 panggilan).
- Retry tidak menambah laju: jeda antar percobaan ≥13 dtk + ekstra
  membesar (30/60 dtk; 429: 45/90 dtk), sama seperti kalibrasi.

## 5. Tes

- `provider/test_checker_chain.py` (BARU): **25/25** — aturan menyala
  (utama fatal final tanpa panggilan relay; clean disampel kedua;
  sengketa dua arah; kaskade; sengketa tak-terselesaikan; semua lane
  mati = tak-terukur), tepat satu record log dengan checker pemutus,
  pelucutan blok kebaruan, arming tiga keadaan, ujung-ke-ujung lewat
  `gate_answer` mode block (sengketa FATAL menahan draf), dan unit
  `crowllm_checker` (prompt = teks kalibrasi, kutipan gugur → clean,
  tak-terparse → unavailable, retry 503, lane mati 524×3, pacing
  ≥13 dtk terbukti via jam palsu). Semua lane di-mock di seam-nya —
  **nol panggilan nyata** ke model/relay selama tes.
- Regresi suite penuh provider: **537 cek bernomor, semua berkas rc=0,
  0 FAIL** — identik baseline pra-pasang (512) + 25 tes baru.
  (`test_improve_20261116.py` tetap 17 PASS dengan §3 terhalang cap
  serve nyata — keadaan operasional lama, bukan regresi.)
- Backup: `serve_gate.py.bak-20261118-chain`,
  `run_serve.py.bak-20261118-chain`.

## 6. Batas yang tersisa (jujur)

- **Sertifikasi cadangan tidak menutup racun #1** (kasus Hop,
  `fcb7b015`): lolos dari SEMUA kandidat relay di semua ronde
  kalibrasi — batas nyata rezim prompt publik. Spesies itu tetap
  wilayah lapis verifikasi isi + sitasi, bukan rantai ini.
- **Varians antar-run lane relay belum diukur di produksi** — kalibrasi
  memakai konvensi union dua ronde untuk skornya; produksi memakai
  satu sampel per lane per draf (sengketa adalah mekanisme koreksinya).
- **Latensi ekor gpt-5.6-sol** (satu outlier 111,5 dtk saat kalibrasi)
  + retry berjenjang berarti satu cek bersengketa bisa memakan
  beberapa menit. Serve berpola polling 1 menit dan cap 10/hari
  menoleransi ini, tapi waktu cek bukan lagi ~detik.
- **Rantai belum pernah jalan live** — pemasangan ini terverifikasi
  unit + regresi saja. Penerbangan pertama terjadi pada serve
  berikutnya yang user nyalakan, dan log rantai (`chain` di
  semantic-check-log.jsonl) adalah bahan bedah pertamanya.
- Kedudukan gpt-oss Cloudflare (rancangan lama §7 KALIBRASI-
  PEMERIKSA-KEDUA: fallback ke-2 di dalam `default_semantic_model_call`)
  **tidak diubah dan tidak dipasang** oleh tugas ini — utang racunnya
  #5–#8 masih terbuka dan jalurnya tetap cadangan di atas kertas.
