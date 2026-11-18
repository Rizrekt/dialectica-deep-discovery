# Arsip Investigasi — Dialectica Deep Discovery

Repository ini adalah **arsip read-only** seluruh hasil investigasi *Deep Discovery* atas sistem operasi AGENT.AkTa di platform Dialectica, yang dilakukan pada **18 November 2026** atas perintah user. Investigasi itu membedah cara kerja platform, pipa menjawab (Jalur 1), peta jalur menilai (Jalur 2) dan bertanya (Jalur 3), arsitektur model/provider, skill + CLI `trued`, kemampuan orkestrasi, peluang yang belum dimanfaatkan, dan kelemahan sistem — dari source code, log operasional, konfigurasi, snapshot API, dan pengalaman operasional nyata, bukan dari dokumentasi semata.

> **PERINGATAN KEADAAN:** Arsip ini adalah potret beku per **18 Nov 2026, 23:44 WIB**. Angka akun yang dikutip di dalamnya (saldo **78,1212 $TRUED**, lifetimeEarned **80**, expertise general **9**, reliability **−6**, suspensionCount **6**) adalah tarikan live pada jam itu dan sudah berubah sesudahnya. Laporan ini BUKAN keadaan live. Kredensial: **tidak ada** API key, token, password, session credential, atau private key di repository ini — nilai sensitif yang tersisip dalam berkas bukti sudah disensor pada salinan (lihat `REDACTION-LOG.md`) dan berkas murni rahasia dikeluarkan (lihat `EXCLUDED.md`; hasil pindaian: tidak ditemukan berkas murni kredensial di pohon sumber).

## Cara membaca arsip ini

Empat berkas di akar adalah pintu masuk:

| Berkas | Isi |
|---|---|
| `README.md` | Berkas ini — peta arsip, struktur, sumber bukti, urutan pemeriksaan |
| `MANIFEST.md` | Tabel SEMUA 706 berkas bukti: path, kategori bukti, sumber/asal, status redaksi |
| `EXCLUDED.md` | Berkas yang tidak terkumpul utuh (18 dump API >10 MB → cuplikan 2 MB) atau tidak diarsipkan (65 artefak `.pyc`), beserta alasannya |
| `REDACTION-LOG.md` | Daftar redaksi pada salinan: 57 nilai disensor pada 7 berkas (4 AWS access key ID + 28 tanda tangan + 24 token sesi URL presigned + 1 email bisnis pihak ketiga — semuanya tertanam di teks jawaban platform pihak ketiga) |

**Kategori bukti** (kolom di MANIFEST): `kode` = source code · `log` = log/store/rekaman jalan & hasil ukur · `konfigurasi` = unit systemd & berkas konfigurasi · `API` = snapshot respons API platform · `dokumentasi` = laporan/peta/dokumen/prompt · `inferensi` = disediakan sebagai kategori, tetapi tidak ada berkas yang murni inferensi — berkas sintesis/analisis dikategorikan `dokumentasi` sesuai konvensi arsip.

**Sumber bukti:** seluruh isi repository adalah SALINAN byte-for-byte (kecuali butir redaksi dan cuplikan parsial yang dicatat) dari pohon kerja `~/workspace/research/dialectica/` — struktur folder dan nama berkas dipertahankan persis — ditambah satu berkas dari `~/workspace/user/dialectica-operator-prompt.md` (di folder `user/`). Berkas asli tidak diubah selama perakitan.

## Urutan pemeriksaan yang disarankan

1. **`LAPORAN-DEEP-DISCOVERY-2026-11-18.md`** — laporan utama 14 bagian (ringkasan eksekutif → cara kerja platform → cara kerja AGENT.AkTa → arsitektur model → skill/CLI → mekanisme Expert/arena → strategi earning → orkestrasi → fitur belum dimanfaatkan → kelemahan → arsitektur aktual vs ideal → rekomendasi → keputusan user). Kepala laporan memuat **Peta Asal-Usul**: bagian mana ditulis sesi utama, pekerja bedah W1–W5, dan model frontier.
2. **`belajar-2026-11-18/deep-discovery/`** — lampiran bedah: `W1-MEKANIK-PLATFORM-DAN-STRATEGI.md`, `W2-CARA-KERJA-AKTA.md`, `W3-ARSITEKTUR-MODEL-PROVIDER.md`, `W4-SKILL-DAN-CLI.md`, `W5-ORKESTRASI-PELUANG-KELEMAHAN.md`, `FRONTIER-DUCK-AUDITOR-2026-11-18.md` (audit arsitektur independen oleh model frontier), `prompt-duck-auditor.txt`.
3. **Dokumen penopang vonis** (akar): `PETA-EARN-LIVE-2026-11-18.md` (peta penghasilan live), `PETA-JALUR-2-VERIFIER-2026-11-18.md`, `PETA-JALUR-3-BERTANYA-2026-11-18.md`, `PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md`, `UJI-1-TEMBAKAN-2026-11-18.md` (bukti jahitan kolam live), `NYALA-PILOT-2026-11-17.md` + `NYALA-DOKTRIN-A-2026-11-18.md` (jurnal nyala), `MEKANISME-DAN-LAPANGAN.md` (ledger mekanisme platform, berkas terbesar), `SISTEM-KENDALI.md` (dokumen kendali proyek), `QUALITY.md` (rubrik mutu).
4. **Konsultasi frontier lain** (folder `belajar-2026-11-18/frontier-*`): paket, jawaban mentah, dan sintesis konsultasi untuk Jalur 2, Jalur 3, perbaikan Jalur 1, dan transfer direktif — termasuk `belajar-2026-11-18/frontier-transfer-direktif/CROWLLM-LIVENESS-2026-11-18.md` (sapuan liveness 62 model relay: 21 hidup / 41 mati).
5. **Kode dan log pendukung klaim**: folder `provider/` (lapisan operasi kami di atas klien stok) dan `skill-audit/` (paket skill vendor yang dibedah), lalu snapshot API di folder `belajar-*` untuk memverifikasi angka mentahnya.

## Struktur folder

Struktur di bawah akar mencerminkan persis pohon sumber `research/dialectica/`:

- **`LAPORAN-DEEP-DISCOVERY-2026-11-18.md`** — laporan utama investigasi (lihat urutan pemeriksaan #1).
- **Dokumen proyek di akar (±120 berkas `.md`)** — seluruh riwayat kerja proyek Dialectica: peta (`PETA-*`), jurnal nyala (`NYALA-*`), uji (`UJI-*`), studi (`STUDI-*`, `KORPUS-*`), audit (`AUDIT-*`), perbaikan (`PERBAIKAN-*`), rancangan (`RANCANGAN-*`), kalibrasi (`KALIBRASI-*`), dokumen kendali (`SISTEM-KENDALI.md`, `QUALITY.md` + cadangannya), ledger (`MEKANISME-DAN-LAPANGAN.md`, `VERDICT-LEDGER.md`, `BELAJAR-LOG.md`, `DRILL-LOG.md`), dan `PAKET-DEEP-DISCOVERY-DIALECTICA-2026-11-18.zip` (paket zip laporan + lampiran sebagaimana dibagikan ke user malam investigasi).
- **`provider/` (204 berkas)** — lapisan operasi milik proyek di atas klien stok: `run_serve.py` + modul serve (`vyce_serve_*`, `cloudflare_serve_*`), gerbang (`serve_gate.py`, `freshness_gate.py`, `citation_verify.py`, `content_verify.py`, `crowllm_checker.py`), doktrin (`doctrine_a.py`, `rate_trigger.py`), jalur bertanya (`ask_driver.py`, `ask_preflight.py`), provider model (`vyce_provider.py`, `openrouter_wrapper.py`, `cloudflare_provider.py`, `dashscope_provider.py`, `zai_provider.py`, `gemini_provider.py`), unit systemd `dialectica-serve.service` (+ cadangan), log jalan (`serve-*.log`, `token-usage.jsonl`, `*-check-log.jsonl`, `doctrine-decision-log.jsonl`), store (`trigger-store.json`, `late-queue.json`), hasil kalibrasi (`calibration-*`), subfolder `verifier/` (kit Jalur 2: `run_verifier.py`, `register_ivsp.py` — terkunci, `verdict-drafts.jsonl`, `ours.json`), `lib/`, `steering/` (catatan steering per pertanyaan), `serve-cache/` (draf tersimpan), dan berkas cadangan `.bak-*` untuk hampir semua modul (jejak evolusi kode). Semua key provider dibaca dari environment — tidak ada kredensial tertanam.
- **`skill-audit/` (7 berkas)** — paket skill Dialectica vendor yang diaudit: `pkg/dialectica/SKILL.md`, `references/` (api, arenas, rules-of-the-game), `scripts/trued.py` (klien v0.22.4 yang dibedah W4), `LICENSE`, dan arsip asli `dialectica.tar.gz`.
- **`belajar-2026-11-14/` s.d. `belajar-2026-11-17/`** — folder studi per hari berisi run pengamatan berkala (`run2`–`run11`): snapshot API platform (`isrs.json`, `isos_by_isr.json`, `details_by_isr.json`, `leaderboard.json`), keadaan run (`state.json`), dan hasil olahan (`analysis*.json`, `sweep*.json`, `sample_tags.json`, hasil Exa). Dump terbesar (>10 MB) terarsip sebagai cuplikan — lihat `EXCLUDED.md`.
- **`belajar-2026-11-18/` (104 berkas)** — bahan hari investigasi: `deep-discovery/` (lampiran W1–W5 + frontier), `antrean-verdict/` (studi antrean verdict: listing + ISO), `doktrin-a/` (bahan Doktrin A), `peta-earn/`, `peta-jalur-2/`, `peta-ask/` (tarikan live pemetaan tiga jalur, termasuk `peta-jalur-2/pilot-isr-isos.json` dan `dryrun-samples.json`), dan empat folder konsultasi frontier (`frontier-jalur2/`, `frontier-jalur3/`, `frontier-perbaikan-jalur1/`, `frontier-transfer-direktif/`) berisi prompt, jawaban mentah per model, berkas `.err` (kegagalan relay 503), dan sintesis.
- **`penantang-penulis-2026-11-17/` (35 berkas)** — bahan uji penantang penulis (babak 1–2, termasuk subfolder `babak-2/`).
- **`dryrun-2026-11-17/` (28 berkas)** — bahan dry-run terpadu pra-pilot.
- **`novelty-2026-11-17/` (4 berkas)** — bahan uji konteks kebaruan (C5).
- **`PILOT-SPOTCHECK-2026-11-17/` (7 berkas)** — bahan spot-check manual 5 jawaban pilot.
- **`drills/` (6 berkas)** dan **`audit-pilar-sementara/` (5 berkas)** — bahan drill gerbang dan audit pilar sementara.
- **`user/` (1 berkas)** — `dialectica-operator-prompt.md`: prompt operator proyek (dari `~/workspace/user/`), dokumen peran/jembatan operator yang dirujuk dokumen kendali.

## Integritas arsip

- Total berkas bukti: **706** (dokumentasi 203 · kode 195 · log 144 · API 160 · konfigurasi 4) + 4 berkas arsip (README, MANIFEST, EXCLUDED, REDACTION-LOG) = **710 berkas**.
- Berkas asli di workspace **tidak diubah** — redaksi dan cuplikan hanya terjadi pada salinan (terverifikasi silang sesudah perakitan).
- Pindaian akhir atas seluruh pohon arsip dengan pola rahasia yang sama: **nol temuan** nilai rahasia (detail pola di `EXCLUDED.md` §3 dan `REDACTION-LOG.md`).
