# LAPIS VERIFIKASI ISI DUA TAHAP — DIBANGUN + TERKALIBRASI 2026-11-17

**Keputusan:** user 2026-11-17 21:52 — "Opsi A — bangun lapis verifikasi isi dua tahap sekarang" (menjalankan aturan ketat user 10:50: verifikasi isi-klaim-lawan-isi-sumber adalah wujud berikutnya yang wajib ada sebelum serve diskalakan).
**Keadaan saat bangun:** serve STOP dan tetap STOP; nol submit; lapis hanya di-arm lewat env di cabang gated `run_serve.py`, pola yang sama dengan lapis sitasi + gerbang kesegaran.

---

## 1. Lubang yang ditambal

Draf pilot 2777178d menyatakan skema sybil Hop Protocol 2022 sebagai "self-report boleh simpan **50%**, bounty hunter **10%**" dengan sitasi ke docs.hop.exchange yang HIDUP. Angka terdokumentasi sebenarnya beda (hunter Hop dijanjikan **25%**; skema self-report-simpan adalah LayerZero, **15%**). Lapis sitasi membuktikan penunjuk ada + dokumennya benar — tidak membaca isinya. C5 menilai pola — tidak membuka sumber. Racun ini (racun #1 korpus kalibrasi) lolos dari semua pemeriksa pola di dua kalibrasi. Lapis ini membandingkan **isi klaim lawan isi sumber**.

## 2. Arsitektur (persis terbangun)

Modul `provider/content_verify.py` (antarmuka meniru `citation_verify.py`: fungsi check murni + fetcher/model-call sebagai jahitan tes + log `content-check-log.jsonl`).

- **Ekstraksi klaim poros:** draf dipecah kalimat; klaim = kalimat bertoken presisi (persen, desimal, angka bergrup-ribuan, mata uang, tanggal penuh, persen ejaan-kata = token KUAT; tahun telanjang + integer telanjang = token LEMAH, tak pernah menghukum sendirian) yang berpasangan dengan penunjuk sitasi di kalimat yang sama / blok paragraf yang sama (parser penunjuk `citation_verify` dipakai ulang; pasangan memakai SEMUA span kemunculan penunjuk). Span penunjuk dimasker sebelum ekstraksi token (angka di dalam URL/DOI bukan angka klaim). Baris bibliografi seksi Sources tidak membangkitkan klaim. Pengulangan asersi yang sama (kasus Hop: badan §2 + penutup "New in this answer") digabung jadi satu klaim dengan gabungan penunjuknya. Klaim presisi TANPA penunjuk dicatat sebagai unbound (wilayah S-1 milik C5; dicatat di sini, tidak dihukum di sini).
- **TAHAP 1 — MEKANIS:** teks sumber diambil lewat fetcher yang sama dengan lapis sitasi; token dinormalisasi (bentuk digit/kata, pemisah ribuan, varian %) dan dicari di teks sumber. Token persen wajib konteks persen di sumber (angka "50" telanjang tidak membuktikan "50%"). Token KUAT tak ditemukan = temuan poros tahap 1 (kandidat fatal). Sumber tak terambil untuk klaim poros (bot-wall 401/403/429, 5xx) = kelas **tak-terverifikasi** tersendiri — bukan lolos; sumber mati (404/koneksi) = kelas no-source (vonis penunjuk milik lapis sitasi).
- **TAHAP 2 — ENTAILMENT:** klaim ambigu naik ke Nemotron lewat **lane pemeriksa kita sendiri** (`serve_gate.default_semantic_model_call`: OpenRouter — probe-nya menjaga cadangan darurat dan melewati lane itu sendiri saat sisa kuota <2 — + fallback Vyce). **Tidak pernah lewat CrowLLM/relay mana pun** — prompt gerbang internal tidak keluar dari lane sendiri. Vonis supported/unsupported/unclear; "supported" hanya dipercaya bila kutipan buktinya terverifikasi kata-per-kata di teks sumber (doktrin C5), tanpa itu turun jadi unclear. Unsupported pada klaim poros = fatal; unclear = temuan tercatat. Anggaran: maks **6 panggilan tahap-2 per draf** (klaim poros draf serve nyata 1–4; yang terlewati anggaran tercatat "skipped-budget", tidak diam).
- **Integrasi gerbang:** tahap di `serve_gate.gate_answer` di samping tahap sitasi (parameter `content_check`, blok `gate["content_verify"]`); `serve_gate.armed_content_check()` membaca `DIALECTICA_CONTENT_CHECK`; `vyce_serve_common` memasoknya; `run_serve.py` cabang gated meng-arm `DIALECTICA_CONTENT_CHECK=1`. Mode `DIALECTICA_CONTENT_MODE` bawaan **block** ("shadow" = catat saja). Crash callable tidak pernah menahan (doktrin rumah). Backup: `serve_gate.py.bak-20261117-contentverify`, `vyce_serve_common.py.bak-20261117-contentverify`, `run_serve.py.bak-20261117-contentverify`.

## 3. Kalibrasi (fetcher nyata + Nemotron lane sendiri) — GERBANG PENERIMAAN LOLOS

Skrip `provider/calibrate_content_verify.py`; hasil `provider/calibration-content-results.json`. Tiap kasus dijalankan dua rezim: tahap-1+2 penuh dan tahap-1-saja (anggaran tahap-2 = 0).

| Kasus | Jenis | Tahap-1-saja | Tahap-1+2 | Catatan |
|---|---|---|---|---|
| Hop asli (draf penuh 2777178d) | wajib-tangkap | **FATAL** | **FATAL** | 10% ABSENT di sumber (tahap 1); tahap 2 vonis unsupported ("excerpts … no mention of Hop's 2022 airdrop, sybil list, … self-reporting, 50% alloca…"). Klaim Treasury di draf yang sama: supported |
| Hop sintetis (angka diganti 75%/30%, sumber sama) | wajib-tangkap | **FATAL** | **FATAL** | kedua token ABSENT; tahap 2 unsupported |
| Treasury tanggal diganti (Aug 8 → Aug 9) | wajib-tangkap | **FATAL** | **FATAL** | tahap 2 menamai selisihnya persis: "source states August 8, 2022, claim states August 9, 2022" |
| Treasury asli (verbatim) | sehat | clean | clean | tanggal hadir; tahap 2 "supported"-nya tanpa kutipan terverifikasi → turun unclear → tahap 1 menopang: supported |
| BIP-32 tahun 2012 | sehat | clean | clean | token lemah saja; hadir di sumber |
| Kontrol verified Danis (draf penuh) | sehat | findings (tercatat) | findings | 36 klaim, nyaris semua unbound (jawaban model/prediksi) → tercatat, TIDAK ditahan |
| Kontrol verified kasnapp (draf penuh) | sehat | findings (tercatat) | findings | sama — unbound tercatat, TIDAK ditahan |
| Meiklejohn DOI karangan | boundary | clean | clean | sumber MATI → kelas no-source/unverifiable di lapis ini; vonis matinya milik lapis sitasi (di sana memang tertahan) — lapis isi TIDAK menghukum isi atas sumber mati |

**Angka gerbang: must-catch 3/3 (tahap-1-saja) dan 3/3 (tahap-1+2) · salah-tahan fatal pada kontrol sehat 0/4.**

Bacaan jujur atas hasil:
- Kasus Hop asli: token "50%" sempat tercatat OK karena string "50%" muncul di kode JS/boilerplate halaman GitBook mentah — kehadiran token di kode halaman BUKAN dukungan. Yang menghukum: token kedua (10%) absent di tahap 1 + vonis unsupported tahap 2. Inilah alasan klaim preseden tetap naik tahap 2 walau semua token "hadir": kehadiran mekanis hanya bukti lemah di halaman berat-JS.
- Jalur penyelamatan tahap 2 lebih sempit di produksi daripada di tes unit: pada 2/2 panggilan yang condong "supported", kutipan bukti Nemotron tidak lolos verifikasi kata-per-kata (parafrase) → turun unclear. Tahap 2 terbukti menghukum (unsupported tak butuh kutipan) jauh lebih andal daripada menyelamatkan. Konsekuensi praktis: temuan tahap 1 jarang terbalikkan — mode block berarti angka yang tak ditemukan mekanis hampir selalu menahan, kecuali sumber menyatakannya dalam bentuk yang dikenali normaliser.
- Kontrol sehat korpus (Danis/kasnapp) hampir tidak melatih jalur berpasangan (keduanya jawaban komputasi nyaris tanpa sitasi — klaimnya unbound). Bukti sehat-berpasangan bertumpu pada klaim Treasury (di draf Hop + standalone) dan BIP-32. Salah-tahan fatal tetap 0 di semua yang terukur, tetapi n sehat-berpasangan kecil — nyatakan begitu.

## 4. Tes

- `provider/test_content_verify.py`: **41/41** (token, kehadiran, klaim/dedupe/Sources, tahap 1, tahap 2 + anggaran + lane jatuh, doktrin canary, wiring gerbang + arming + mode).
- **Suite penuh provider: 479 cek bernomor lolos / 0 gagal / 9 tak-terjalan.** Yang tak-terjalan: `test_improve_20261116.py` berhenti di §3 (8 cek lolos sebelum berhenti) karena tersandung **cap serve NYATA 10/10** yang habis oleh pilot pagi — keadaan operasional yang sama seperti sebelum tugas ini, bukan regresi (berkas itu tidak menyentuh kode lapis ini).

## 5. Batas tegas (status: cukup untuk apa)

1. **Klaim tanpa token presisi di luar jangkauan** — dukungan parafrase/kualitatif murni (mis. klaim DPAPI di 635a010d) tidak bisa dinilai lapis ini; tetap wilayah spot-check/C5.
2. **Sumber bot-wall = tak-terverifikasi, bukan didukung** — klaim poros atas sumber yang tak bisa diambil tidak menghukum dan tidak meloloskan secara isi; tercatat terbuka di log.
3. **Teks yang dinilai = halaman yang dinamai penunjuk** — sitasi beranda docs untuk klaim dalam dinilai sebagai beranda (aturan A_CITATION diterapkan mekanis); sumber yang benar tapi terlalu umum akan tertahan — itu disengaja.
4. **Kehadiran token di boilerplate/kode halaman = bukti lemah** (kasus "50%" GitBook) — dimitigasi tahap 2 untuk klaim preseden/kebaruan, tetapi klaim poros non-preseden dengan semua token "hadir" di boilerplate bisa lolos tahap 1+2 bila tahap 2 unclear.
5. **Anggaran tahap 2 = 6/draf** — draf patologis dengan klaim poros lebih banyak akan menyisakan klaim "skipped-budget" yang vonisnya bertumpu tahap 1 saja (tercatat, tidak diam).
6. **Status kecukupan:** lapis ini menutup spesies yang terbukti membakar kita (angka preseden karangan pada sumber hidup) dengan gerbang kalibrasi LOLOS dan salah-tahan 0. Ia **cukup untuk pilot skala kecil** di rezim yang sama dengan lapis sitasi. Ia **bukan** verifikasi isi penuh: parafrase tanpa angka, sumber bot-wall, dan boilerplate-match tetap celah tercatat. Keputusan menaikkan skala serve tetap keputusan user dengan peta celah ini di meja.
