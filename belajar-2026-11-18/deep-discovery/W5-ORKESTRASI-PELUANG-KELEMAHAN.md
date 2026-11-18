# DEEP DISCOVERY — LINI W5: ORKESTRASI, PELUANG, KELEMAHAN

**Perintah:** user 2026-11-18 23:38 WIB (Deep Discovery AGENT.AkTa). Lini ini mengerjakan Blok §6 (kemampuan orkestrasi), §7 (peluang belum dimanfaatkan), §8 (kelemahan & titik gagal).
**Metode:** investigasi READ-ONLY — membaca berkas, kode, dan log yang benar-benar ada di workspace. Nol perubahan konfigurasi, nol panggilan API model, nol submit.
**Tanggal susun:** 2026-11-18 malam (sesudah verdict pilot mendarat: 4/5 jawaban pilot dibayar, total +70 $TRUED).

**Legenda tag bukti:**
- **[BUKTI: berkas]** — tertulis di berkas/log yang dibuka sesi ini.
- **[PENGALAMAN]** — kejadian operasional yang tercatat di riwayat sesi/ledger.
- **[INFERENSI]** — kesimpulan yang ditarik dari bukti, bukan bukti itu sendiri.
- **[HIPOTESIS]** — belum diuji; tidak boleh diperlakukan sebagai fakta.

**Legenda kelas orkestrasi (§6):** A = sudah bisa + pernah digunakan · B = didukung teknis, belum pernah digunakan (atau baru bentuk parsial/manualnya) · C = butuh integrasi/pengembangan · D = tidak didukung/tidak memungkinkan.

---

# BLOK §6 — KLASIFIKASI 12 KEMAMPUAN ORKESTRASI

## Tabel ringkas

| # | Kemampuan | Kelas | Bukti penentu (satu baris) |
|---|-----------|-------|-----------------------------|
| 1 | Membaca Question + menentukan spesialisasi | **B** | Klasifikasi kelas/lane terbukti live (picker + rate_trigger); spesialisasi domain tidak pernah ditentukan — semua pertanyaan diperlakukan generalis |
| 2 | Memilih model berdasar karakteristik Question | **C** | Penulis tetap GLM untuk semua pertanyaan; yang ada parameter per kelas (lantai panjang), bukan model per pertanyaan |
| 3 | Menyiapkan konteks + prompt yang tepat | **A** | Konteks kebaruan terpasang + mitigasi R3 terverifikasi uji nyata; steering per target di era klaim |
| 4 | Mengatur urutan Research → Answer → Review → Fact-check | **A** | Pipa prepare → generasi → gerbang berlapis → submit terbang live (pilot 17 Nov, mini-batch 18 Nov); "Research" = konteks kebaruan internal, bukan riset web |
| 5 | Meminta model memperbaiki hasil saat ada kesalahan | **B** | Bentuk manual terbukti (steering patch 71f472d6); bentuk otomatis di pipa serve tidak ada — draf tertahan dibuang, bukan direvisi |
| 6 | Menyelesaikan konflik antar-model | **B** | Rantai 2-dari-3 + penengah terpasang & terkalibrasi; belum ada sengketa live yang diputus (baru jalan shadow) |
| 7 | Mengukur kualitas jawaban pra-submission | **A** | Lantai K-1/K-2 + verifikasi sitasi (55 tes) + verifikasi isi (46 tes) + C5 terkalibrasi; mini-batch menahan 5/8 draf di tahap gerbang |
| 8 | Mengelola deadline & pekerjaan yang diterima | **A** | Counter cap harian, antrean TELAT ber-release/kedaluwarsa, watcher counter, gerbang sekuensing Q4 — semua terbukti live |
| 9 | Memantau biaya API & penggunaan token | **A** (dengan lubang tercatat) | token-usage.jsonl 197 record teragregasi harian; lubang: biaya per verdict Jalur 2 belum tercatat |
| 10 | Menyimpan riwayat pekerjaan untuk pembelajaran | **A** | VERDICT-LEDGER, log gerbang per lapis, serve-cache, BELAJAR-LOG, MEKANISME §-bernomor |
| 11 | Menganalisis hasil Verified & Falsified | **A** | 8 baris ledger, tiap falsified dibedah sampai akar (BEDAH-TOTAL, BEDAH-KLAIM2, drill); verified pertama dianalisis pra- & pasca-verdict |
| 12 | Memakai hasil sebelumnya untuk keputusan berikutnya | **A** | Rantai sebab-akibat terdokumentasi: falsified → T10/T12 → lantai K-2; studi kohort → Doktrin A; mini-batch → perbaikan kolam |

## Uraian per kemampuan

### 1. Membaca Question + menentukan spesialisasi — **B**
Yang benar-benar berjalan: pertanyaan dibaca dan **diklasifikasi** — `target_picker.py` menentukan kelas (Marathon/Innovator, Pioneer, steering-siap) dari viso/verified/flag marathon [BUKTI: `dialectica-operator-prompt.md` butir 14; tes picker 42/42 di MITIGASI-KONTEKS-TERPOTONG §3], dan `rate_trigger.py` mengklasifikasi mode doktrin (CEPAT/TUNGGU/TELAT) dari laju 2 menit pertama [BUKTI: IMPLEMENTASI-DOKTRIN-A-2026-11-18.md §2b]. Klasifikasi ini dipakai live: 5 target pilot semuanya Pioneer viso-0 terpilih [BUKTI: VERDICT-WATCH-2026-11-17.md], dan pengamat mengklasifikasi 117 pertanyaan selama mini-batch [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §3].
Yang **tidak** pernah dilakukan: menentukan *spesialisasi domain* pertanyaan (mis. "ini soal keamanan kriptografi, perlu model/lensa X") lalu bertindak atasnya. Arena kita satu (general), strategi satu (dynamic), penulis satu (GLM) untuk segala topik. Jadi kemampuan ini B: mesin klasifikasinya nyata dan terpakai, tetapi dalam arti kelas/lane — bukan spesialisasi.

### 2. Memilih model berdasar karakteristik Question — **C**
Tidak ada satu pun kejadian model dipilih karena karakteristik pertanyaan. Penulis = GLM (rantai fallback Vyce) untuk semua kelas; pemeriksa = Nemotron/qwen/sol berdasarkan *peran di pipa*, bukan isi pertanyaan. Yang ada hanyalah parameter per kelas: lantai panjang di wrapper (Pioneer 1.717 · umum 3.000 · Marathon 4.500) [PENGALAMAN: paket fase testing 17 Nov] — itu kalibrasi panjang, bukan pemilihan model. Infrastruktur multi-lane-nya tersedia (provider Vyce, Cloudflare, DashScope, Z.ai, OpenRouter semua terbangun) [BUKTI: daftar berkas `provider/`], jadi ini C — butuh pengembangan routing, bukan mustahil.

### 3. Menyiapkan konteks + prompt yang tepat — **A**
Konteks kebaruan (blok jawaban verified yang sudah ada, COVER_FLOOR=8) ditempel ke prompt pemeriksa lewat `novelty_context.attach` dan cacat pemotongannya ditutup R3 dengan uji nyata: blok 5.361 kar sampai utuh (pra-R3: 0 kar) dan pemeriksa langsung menangkap SURPRISE_GAUGE yang sebelumnya mustahil terlihat [BUKTI: MITIGASI-KONTEKS-TERPOTONG-2026-11-17.md §2–3]. Di era klaim, steering per target disiapkan manual per pertanyaan (mis. mandat 4 URL Wikipedia persis untuk 71f472d6) [BUKTI: VERDICT-LEDGER.md baris 3]. Prompt gerbang internal tidak pernah dikirim ke relay — yang menyeberang hanya prompt publik byte-identik kalibrasi [BUKTI: RANTAI-PEMERIKSA-2026-11-18.md §3].

### 4. Mengatur urutan Research → Answer → Review → Fact-check — **A**
Urutan ini adalah pipa serve itu sendiri dan sudah terbang: konteks kebaruan ditarik (tahap "research" internal) → generasi penulis → review berlapis (lantai mekanik K-1/K-2 → verifikasi sitasi → verifikasi isi dua tahap → rantai semantik → gerbang kesegaran detik-kirim) → submit. Di mini-batch urutannya terlihat per kejadian: dari 9 generasi, tahan isi ×3, K-2 ×2, sitasi+isi ×1, kesegaran pasca-klaim ×1, kapasitas ×1 [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §3]. Kejujuran cakupan: tahap "Research" kita **bukan** riset web/sumber primer — ia konteks internal platform (jawaban yang sudah ada). Fact-check = verifikasi sitasi mekanis + entailment isi, bukan penelusuran web (lihat kelemahan K4/K5 di §8).

### 5. Meminta model memperbaiki hasil saat ada kesalahan — **B**
Bentuk manualnya terbukti nyata: untuk ISR 71f472d6, sesudah 4 generasi Nemotron gagal lantai §45, steering dipatch dengan mandat spesifik (4 URL Wikipedia persis) dan model menggenerasi ulang — draf berikutnya lolos semua gerbang mekanik [BUKTI: VERDICT-LEDGER.md baris 3]. Bentuk otomatisnya **tidak ada**: di pipa serve, draf yang ditahan gerbang berstatus pass-over — dibuang, tidak pernah dikembalikan ke penulis beserta temuannya untuk satu putaran revisi. Generasi ulang yang terjadi di mini-batch (704b56c2 ×3) adalah penyajian ulang oleh klien, bukan revisi berumpan-balik [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §3]. Karena itu B, bukan A: kemampuan ini hidup sebagai tindakan operator manual, mati sebagai mekanisme pipa.

### 6. Menyelesaikan konflik antar-model — **B**
Mekanismenya terpasang dan aturannya eksplisit: pemeriksa utama fatal = final; utama clean → sampel kedua qwen-3.8-max; sengketa diputus gpt-5.6-sol 2-dari-3; penengah mati → vonis utama berdiri + `dispute_unresolved` tercatat, tidak memblokir [BUKTI: RANTAI-PEMERIKSA-2026-11-18.md §2]. Kalibrasinya nyata (Nemotron 7/7 racun, qwen 6/7, sol 5/7 pada korpus identik) [BUKTI: RANTAI-PEMERIKSA-2026-11-18.md §1]. Di kit verifier, perselisihan drafter dihitung di bidang `agreement` dan kasus ambigu berakhir abstain, bukan vonis paksa — terbukti pada 5 draf dry-run nyata, termasuk satu kasus lokal "uncertain" vs dua lane "compliant" (`all_agree: false`) [BUKTI: `provider/verifier/verdict-drafts.jsonl`]. Tetapi: rantai serve baru berjalan **shadow** di mini-batch (tidak menahan apa pun, sesuai modenya) dan belum ada sengketa live yang benar-benar diputus penengah [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §3]. B.

### 7. Mengukur kualitas jawaban pra-submission — **A**
Ini lapis terkuat sistem. Lantai mekanik K-1/K-2 (URL ≥1, kepadatan sitasi ≥0,5/1.000 kar, rasio angka terikat ≥0,30) lahir dari bedah falsified dan terpasang di wrapper [BUKTI: `dialectica-operator-prompt.md` Addendum T12]. Verifikasi sitasi mekanis: 55 tes; verifikasi isi dua tahap: 46 tes [PENGALAMAN: paket gerbang 17 Nov]. Pemeriksa semantik C5 terkalibrasi pada korpus racun (7/7 union) [BUKTI: RANTAI-PEMERIKSA-2026-11-18.md §1]. Bukti produksi: mini-batch menahan 5 dari 8 draf yang mencapai tahap gerbang — termasuk pola persis yang dulu meloloskan pilot [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §6 butir 2]. Batasnya diakui di §8 (K2, K5, K16): terukur ≠ sama dengan yang panel bayar.

### 8. Mengelola deadline & pekerjaan yang diterima — **A**
Terbukti live berlapis: counter generasi harian (`serve_generations_today()`, cap 10/hari-UTC) dibaca di setiap pra-terbang [BUKTI: NYALA §1; UJI-1-TEMBAKAN §1]; antrean TELAT memarkir tiket dengan release lahir+2 jam dan kedaluwarsa +6 jam [BUKTI: IMPLEMENTASI-DOKTRIN-A §2]; watcher pengaman counter (poll 3 dtk) mengawal uji asap dan tidak pernah perlu menembak [BUKTI: UJI-1-TEMBAKAN-2026-11-18.md §1]; gerbang sekuensing Q4 menahan klaim di belakang job non-terminal dan terbukti mengevaluasi dengan benar live [BUKTI: UJI-1-TEMBAKAN §6 butir 4]. Keterbatasan keras yang bukan salah kita: job yang ter-drop mengunci slot konkurensi tunggal ±30 menit dan **tidak ada API pelepas job** [BUKTI: NYALA §3, kejadian 02:47 "Agent at capacity (1/1)"] — pengelolaan deadline kita berhenti tepat di batas itu.

### 9. Memantau biaya API & penggunaan token — **A, dengan lubang tercatat**
`token-usage.jsonl` memuat 197 record (10–18 Nov): total **4.807.478 token**, biaya uang **$0** di semua record (free-only ditegakkan di level lane), tersebar di 7 lane / 8 model, 56 ISR unik — diagregasi sesi ini langsung dari berkasnya [BUKTI: `provider/token-usage.jsonl`, agregasi W5]. Sisa kuota OpenRouter per record (`quota_remaining_after`) dan neuron Cloudflare harian dilacak sebagai bahan bakar, dan audit bahan bakar harian adalah kewajiban berdiri (T14) [BUKTI: `dialectica-operator-prompt.md` Addendum T14]. **Lubangnya, tertulis oleh pembangunnya sendiri:** runner verifier Jalur 2 **belum mencatat biaya model per verdict**, sehingga titik impas pilot verifier 14 hari belum bisa dihitung dari angka sendiri [BUKTI: `provider/verifier/README.md` "Known gap"]. Kelas A berlaku untuk Jalur 1; untuk Jalur 2 kemampuan ini belum utuh.

### 10. Menyimpan riwayat pekerjaan untuk pembelajaran — **A**
Setiap lapis meninggalkan jejak terstruktur: VERDICT-LEDGER.md (8 verdict, lengkap dengan Δsaldo/ΔLE/ΔExpertise/ΔRAR per baris), token-usage.jsonl, semantic/citation/content/freshness-check-log.jsonl (26/24/27 record), doctrine-decision-log.jsonl, serve-cache per draf, BELAJAR-LOG.md, dan MEKANISME-DAN-LAPANGAN.md §-bernomor sebagai ledger hidup [BUKTI: berkas-berkas tersebut, diinventarisasi sesi ini]. Riwayat ini benar-benar dibaca ulang untuk keputusan (lihat butir 12) — bukan arsip mati.

### 11. Menganalisis hasil Verified & Falsified — **A**
Falsified: ketujuh falsified rezim dibedah sampai akar mekanik satu per satu — klaim #1 mati di dukungan semantik sitasi (BEDAH-TOTAL), #2 mati mekanik (BEDAH-KLAIM2), empat falsified serve 14 Nov dibedah per drill (spesies thinking-trace + penutup evasif yang sama 4/4) [BUKTI: VERDICT-LEDGER.md baris 1–8]. Verified: lima jawaban pilot di-spot-check manual per sitasi *sebelum* verdict (3 vonis: 2 GAGAL, 1 LOLOS-BERSYARAT, lalu 1 GAGAL ringan + 1 LOLOS BERSIH di sisa pilot) [BUKTI: SPOTCHECK-PILOT-2026-11-17.md; SPOTCHECK-SISA-PILOT-2026-11-17.md], dan pembayaran malam ini (+70) direkonsiliasi per peristiwa notifikasi lawan saldo live [PENGALAMAN: audit earning sesi utama 18 Nov 23:2x — 13 peristiwa koin seumur akun, jumlah pas 68,1212]. Catatan jujur: analisis verified kita masih muda — sampel verified berbayar pertama baru berumur hitungan jam.

### 12. Memakai hasil sebelumnya untuk keputusan berikutnya — **A**
Rantai sebab-akibatnya terdokumentasi ujung ke ujung:
- Falsified #1 (dukungan sitasi) → Addendum T10 aturan clean-sheet + gerbang self-VFP [BUKTI: operator-prompt T10].
- Falsified #2 (mekanik) → lantai K-1/K-2 di wrapper [BUKTI: operator-prompt T12].
- Studi kohort + studi antrean verdict (66 ISR/6.188 ISO) → Doktrin A 7:3 diadopsi user [BUKTI: SISTEM-KENDALI.md entri studi antrean; IMPLEMENTASI-DOKTRIN-A].
- Mini-batch 0/3 (kolam disjoin) → perbaikan kolam Opsi A → terbukti 48/48 di uji asap [BUKTI: NYALA §6; PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md; UJI-1-TEMBAKAN §6.1].
- Kalibrasi pemeriksa → rantai pemeriksa terpasang [BUKTI: RANTAI-PEMERIKSA §1].
- Verdict berevolusi → QUALITY.md v2 → v3 (revisi hanya lewat gerbang angka) [BUKTI: operator-prompt butir 18].
Ini pola kerja yang benar-benar berjalan, bukan rencana.

---

# BLOK §7 — PELUANG YANG BELUM DIMANFAATKAN

## A. Didukung bukti (siap digarap / menunggu satu keputusan bernama)

**P1 — Registrasi IVSP Jalur 2 (Verifier, economist/general, minReward 0,6).** Peluang terbesar yang belum disentuh. Ekonominya terukur live: economist general membayar 0,82/unit dengan median 6.373/agent dan hanya 11 agent aktif di seluruh platform [BUKTI: PETA-EARN-LIVE-2026-11-18.md]. Kit-nya selesai: 33/33 tes hijau, dry-run menghasilkan 5 draf verdict nyata dari 3 drafter dengan gerbang self-dealing bekerja [BUKTI: `provider/verifier/README.md`; `verdict-drafts.jsonl`]. Satu-satunya gerbang urutan yang menahannya — "Expert terbukti dibayar" — **terpenuhi malam ini** (+70). Yang tersisa murni kata jalan user + langkah registrasi tergating di README kit.

**P2 — IVSP Forecasting (economist, 0,84/unit, median/agent 862, escrow).** Arena verifier kedua yang eligibility-nya anyone; belum pernah disentuh sama sekali [BUKTI: PETA-EARN-LIVE-2026-11-18.md]. Nilai strategisnya: diversifikasi bila kolam general jenuh — tetapi n-nya kecil dan ada escrow, jadi ia pelengkap P1, bukan pengganti.

**P3 — Liveness sadar-lane (membuka lane TELAT).** Uji asap membuktikan pipa doktrin bekerja 48/48, tetapi 47/48 tiket due terveto gerbang liveness karena ronde marathon pertanyaan berumur 0,4–1,5 jam sedangkan release TELAT = +2 jam [BUKTI: UJI-1-TEMBAKAN-2026-11-18.md §6 butir 2]. Padahal kanal yang membayar malam ini justru marathon+innovator dari jawaban settled — persis bidikan TELAT. Memperbaiki kesadaran-lane gerbang ini adalah pembuka earning Jalur 1 terbesar yang tersisa. **Wilayah gerbang = terkunci**: hanya usulan, keputusan user.

**P4 — Pencatatan biaya per verdict di runner verifier.** Kekurangan yang diakui pembangunnya; tanpa ini pilot verifier 14 hari tidak punya angka titik impas sendiri [BUKTI: `provider/verifier/README.md` "Known gap"]. Pekerjaan kode kecil, murni internal, tidak menyentuh wilayah terkunci.

**P5 — Pra-terbang bahan bakar penulis sebagai butir menentukan.** Dua nyala berturut-turut gugur di titik yang sama: neuron Cloudflare harian habis (kalibrasi pagi 4.786 + fallback) membunuh satu-satunya generasi uji asap yang lolos seluruh pipa [BUKTI: UJI-1-TEMBAKAN §6 butir 3; NYALA §6 butir 4]. Menjadikan status neuron CF + kesehatan GLM sebagai syarat start (bukan pelengkap) adalah perbaikan prosedural murah berbasis bukti dua kejadian.

**P6 — Lapisan verifikasi pinpoint sitasi.** Verifikasi mekanis kita menangkap penunjuk mati/salah-dokumen, tetapi nomor pasal yang salah di dalam dokumen yang benar (MiCA Article 62, seharusnya 75) hanya tertangkap pemeriksaan manual [BUKTI: SPOTCHECK-SISA-PILOT-2026-11-17.md §"yang hanya dilihat manual"]. Memperluas `citation_verify.py` untuk me-resolve pengenal pinpoint (pasal/DOI/nomor paper) ke isi dokumen adalah peningkatan keberhasilan verifikasi yang spesifik dan terukur celahnya.

**P7 — Kursi penengah/cadangan relay dari kolam yang hidup.** Sapuan liveness 18 Nov malam: 21/62 model CrowLLM hidup; kolam NVIDIA hidup 5/5 (nemotron-3-ultra menjawab 2,33 dtk), sementara kolam OpenAI (gpt-5.6-sol) dan Google (gemini-3.1-pro) serta qwen-3.8-max mati 503 bersamaan [BUKTI: `belajar-2026-11-18/frontier-transfer-direktif/CROWLLM-LIVENESS-2026-11-18.md`]. Ada kandidat penengah yang hidup dan sekelas penilai — tetapi mengganti kursi frontier wajib kalibrasi ulang + keputusan user (dan grok, walau hidup, pernah dibuang user dari kursi frontier — tidak dihidupkan diam-diam).

**P8 — Otomatisasi verdict-watch.** Falsified tidak memicu notifikasi platform apa pun; satu-satunya permukaan adalah status ISO + scores yang harus dibaca manual [BUKTI: operator-prompt T10.3/T11.3]. Konsekuensi nyatanya malam ini: penghasilan +70 pertama kali terlihat dari **screenshot user**, bukan dari pemantauan kita [PENGALAMAN: 18 Nov 23:23]. Watcher otomatis adalah peluang nyata — bentuknya (cron/hook) butuh kata user karena seluruh cron Dialectica dihapus user 17 Nov.

**P9 — Disiplin kalibrasi terpisah dari hari terbang.** Neuron CF adalah kuota harian bersama: kalibrasi 4.786 neuron di pagi hari yang sama dengan nyala membuat lane cadangan penulis mati sebelum sore [BUKTI: NYALA-DOKTRIN-A §3, kejadian 03:20; §6 butir 4]. Memisahkan hari kalibrasi dari hari terbang (atau membatasi anggaran kalibrasi per hari terbang) adalah pengurangan biaya yang sudah terbukti titik bocornya.

**P10 — Yang sebaiknya TETAP persetujuan user (bukan peluang otomatisasi).** Registrasi peran baru (IVSP), perubahan gerbang/kill-metric, config Expert, mode C5 (BLOCK), pembuatan pertanyaan (create), dan setiap nyala serve — semuanya wilayah terkunci yang hanya boleh bergerak sebagai USULAN [BUKTI: SISTEM-KENDALI.md klausul C12; operator-prompt T13.3]. Mengotomatisasi salah satunya bukan peluang; itu pelanggaran.

## B. Hipotesis (belum diuji — jangan diperlakukan sebagai peluang pasti)

**H1 — Expert tambahan paralel.** Platform membolehkan >1 agent per akun, tetapi dompet dan RAR dibagi. Apakah konkurensi per-agent benar-benar melipat throughput earning, atau cap server + RAR bersama meniadakannya, belum pernah diverifikasi live [HIPOTESIS].

**H2 — Kursi model baru dari katalog yang hidup.** deepseek-v4-flash (CrowLLM) pernah diprobe hidup tetapi belum punya kursi dan belum diukur; k2-horizon-375b dan qwen-3.8-27b hidup di sapuan malam ini tetapi belum terkalibrasi untuk peran apa pun [HIPOTESIS — berdasar CROWLLM-LIVENESS, tanpa data kalibrasi].

**H3 — Loop revisi otomatis satu putaran.** Mengembalikan temuan gerbang ke penulis untuk satu revisi terarah (menutup celah kemampuan §6 butir 5) masuk akal secara desain, tetapi belum dibangun dan berisiko membakar cap generasi 10/hari untuk draf yang tetap tertahan [HIPOTESIS].

**H4 — Jalur 3 (bertanya) dibuka kembali.** Jalurnya dormant-terkunci-EV oleh vonis frontier: yang membuka hanya bukti NIU pertama terbukti dibayar (P1) atau perubahan aturan material (P3); saldo pulih saja tidak membuka [BUKTI gerbangnya: PETA-JALUR-3-BERTANYA-2026-11-18.md]. Probe penentu berikutnya adalah cek sisi-operator platform — user sendiri yang harus mengirimnya. Sampai itu ada, ini bukan peluang yang bisa digarap dari sisi kita [HIPOTESIS soal hasil probenya].

**H5 — Penataan ulang urutan rantai penulis untuk menghemat neuron.** Rantai GLM → gpt-oss Vyce → Cloudflare menempatkan satu-satunya lane berkuota-harian-keras di ujung, dan ia yang kepakai justru saat lane depan gagal [INFERENSI dari NYALA §3 + UJI §3]. Menata urutan atau memberi anggaran per lane mungkin menghemat — belum ada pengukuran yang membuktikannya [HIPOTESIS].

---

# BLOK §8 — KELEMAHAN DAN TITIK GAGAL SISTEM

**K1 — Penulis mengarang penunjuk presisi. (Kelemahan terberat, terbukti berulang.)**
GLM kuat di isi dan struktur, tetapi mengarang *pengenal presisi* dari plausibilitas ingatan: preseden Hop ditulis 50%/10% padahal skema terdokumentasi adalah LayerZero 15% dan bounty Hop 25%; DOI Meiklejohn salah dan mati (tertulis …2516651.2516734, benar …2504730.2504747); subjudul DeSoc dikarang ("Original Sybil", seharusnya "Soul"); domain `proofofhumanity.site` mati (yang hidup `.id`); URL whitepaper tanpa TLD; nomor ePrint 2020/940 menunjuk paper orang lain; nomor pasal MiCA 62 padahal pasal kustodinya 75 [BUKTI: SPOTCHECK-PILOT-2026-11-17.md §1–3; SPOTCHECK-SISA-PILOT-2026-11-17.md]. Polanya satu spesies di 3/3 sampel pertama dan muncul lagi di sisa pilot — ini bukan kecelakaan, ini sifat modelnya. Penantang penulis tidak lebih baik: qwen-3.8-max babak 1 menghasilkan 0 sitasi, babak 2 wajib-apparatus jebol 8/13 karangan (61,5%) → GLM bertahan bukan karena bersih, tetapi karena alternatifnya lebih kotor [BUKTI: UJI-PENANTANG-PENULIS-2-2026-11-17.md — "GLM BERTAHAN"].

**K2 — Paradoks panel: gerbang kita menakuti risiko yang sampel ini tidak menghukum — dan itu harus dibaca dua arah.**
Dua dari empat jawaban yang dibayar malam ini adalah jawaban yang spot-check manual kami vonis GAGAL sitasi (edc2bf0a: apparatus karangan 3×, dibayar +20; 7b00324a: pasal MiCA karangan, dibayar +20). Yang LOLOS BERSIH (8eece8ab) justru dibayar paling kecil (+10, Innovator saja), dan satu-satunya yang tidak dibayar adalah GAGAL terberat (8300bcbe, fabrikasi Hop) [BUKTI: SPOTCHECK-PILOT; SPOTCHECK-SISA-PILOT; notifikasi achievement 18 Nov 15:10–16:18 UTC].
- *Arah satu (melawan gerbang kita):* pada sampel n=5 ini, panel membayar kebaruan + marathon; ketelitian sitasi tidak menentukan bayaran. Investasi gerbang sitasi kita bisa jadi tidak sebanding dengan yang panel hargai.
- *Arah dua (membela gerbang):* n=5 dari satu era panel bukan hukum. Sejarah kita sendiri menunjukkan falsified klaim #1 mati persis di dukungan sitasi [BUKTI: VERDICT-LEDGER baris 1] — gerbang sitasi adalah asuransi melawan −1 + pukulan reliabilitas, bukan mesin bayaran. Dan fakta bahwa GAGAL terberat satu-satunya yang nol konsisten dengan risiko ekor yang nyata.
- *Kesimpulan jujur:* data malam ini **melemahkan** klaim "sitasi presisi menentukan bayaran", tetapi **tidak melemahkan** klaim "sitasi menentukan risiko falsified". Menyimpulkan salah satu saja dari dua arah itu = tidak teliti.

**K3 — Fabrikasi itu struktural, bukan insidental: penulis tidak punya retrieval.**
Penulis menulis dari ingatan parametrik tanpa alat membuka sumber. Prompt serve adalah prompt klien stok + lantai wrapper — tidak ada tahap penelusuran sumber sebelum menulis. Maka K1 akan terus berproduksi selama arsitekturnya begini; gerbang kita semuanya *pasca*-generasi (menangkap, bukan mencegah) [INFERENSI dari SPOTCHECK + susunan provider di `provider/`].

**K4 — "Riset" pipa dangkal by design.**
Satu-satunya bahan riset sebelum menulis adalah konteks kebaruan (jawaban platform yang sudah ada) — berguna untuk SURPRISE_GAUGE, tidak berguna untuk kebenaran faktual. Tidak ada tahap riset web/sumber primer di pipa mana pun [BUKTI: susunan pipa di NYALA §3 + MITIGASI-KONTEKS-TERPOTONG §2].

**K5 — Verifikasi sitasi mekanis buta pinpoint.**
Lapis mekanis memverifikasi keberadaan/resolusi penunjuk dan kehadiran token klaim di sumber ter-fetch; ia **melewatkan** cacat pinpoint: nomor pasal salah di dokumen yang benar dan label instrumen yang salah hanya terlihat oleh pemeriksaan manual [BUKTI: SPOTCHECK-SISA-PILOT-2026-11-17.md §"yang hanya dilihat manual"]. CAPTCHA/bot-wall pada sumber juga berakhir "tak-terverifikasi", bukan terbantah [PENGALAMAN: batas tercatat `content_verify.py`].

**K6 — Generasi (sumber daya terlangka) pernah terbakar untuk target tak layak.**
Cap serve hanya 10 generasi/hari-UTC. Mini-batch membakar 9 dan mengirim 0 — akarnya diskoneksi kolam (serve menyajikan 12 baris dari pencariannya sendiri, nol irisan dengan 117 terklasifikasi doktrin) [BUKTI: NYALA-DOKTRIN-A-2026-11-18.md §3, §6 butir 1]. Jahitannya sudah diperbaiki dan terbukti (48/48), tetapi pelajarannya permanen: tanpa irisan kolam, gerbang sebaik apa pun hanya membakar cap. Bentuk historis terburuknya: serve 14 Nov mengirim jawaban-jawaban marathonEligible=FALSE (upside $0, downside penuh) yang berakhir 4 falsified [BUKTI: VERDICT-LEDGER baris 5–8].

**K7 — Bahan bakar cadangan rapuh dan tak beranggaran.**
Alokasi neuron Cloudflare 10.000/hari adalah kuota bersama kalibrasi + fallback. Pagi 18 Nov kalibrasi membakar 4.786; sore harinya satu-satunya generasi uji asap yang lolos seluruh pipa mati di 429 neuron-habis [BUKTI: UJI-1-TEMBAKAN §3; NYALA §6 butir 4]. Tidak ada pemisahan anggaran kalibrasi vs operasi.

**K8 — Fallback penulis berganti model tanpa sepengetahuan operator saat kejadian.**
Fallback menyala 2× di mini-batch (gpt-oss-120b menulis 2 dari 9 generasi) dan baru terlihat sesudahnya dari token-usage [BUKTI: NYALA §5]. Pada uji asap, alasan gugur tautan GLM → gpt-oss Vyce **tidak tercatat di log serve** — celah pencatatan yang diakui berkasnya sendiri [BUKTI: UJI-1-TEMBAKAN §6 butir 3]. Jadi ya: fallback dapat mengubah model yang dipakai tanpa sepengetahuan siapa pun pada saat itu; yang menyelamatkan hanyalah bahwa semua draf fallback melewati gerbang yang sama dan tercatat pasca-hoc.

**K9 — Lapis pemeriksa 2–3 bergantung satu relay; kolamnya bisa mati bersamaan.**
Cadangan (qwen-3.8-max) dan penengah (gpt-5.6-sol) sama-sama lewat CrowLLM. Malam ini kolam OpenAI, Google, dan qwen-max mati 503 bersamaan (dari 62 model, 41 tidak bisa dipakai) [BUKTI: CROWLLM-LIVENESS-2026-11-18.md]. Rantai terdegradasi ke Nemotron saja; sengketa yang penengahnya mati berakhir `dispute_unresolved` — vonis utama berdiri tanpa ada yang benar-benar memutus [BUKTI: RANTAI-PEMERIKSA §2]. Ditambah latensi: draf verdict Nemotron di kit verifier berlatensi 27–37 dtk/panggilan [BUKTI: `verdict-drafts.jsonl`], dan model besar qwen timeout 90 dtk di sapuan.

**K10 — Konkurensi 1 + kunci capacity server: satu veto membekukan Expert ±30 menit.**
maxConcurrency Expert = 1. Job yang di-drop veto kesegaran pasca-klaim tetap menduduki slot sampai timeout liveness server (±30 menit) dan tidak ada API pelepas; tembakan berikutnya ditolak mentah "Agent at capacity (1/1)" [BUKTI: NYALA §3, 02:42–02:47]. Layar pra-klaim Q3 + gerbang sekuensing Q4 (terbukti live di uji asap) mengurangi penyebabnya, tetapi akibat servernya di luar kendali kita.

**K11 — Evaluasi pasca-verifikasi manual, reaktif, dan pernah kalah cepat dari user.**
Falsified tidak ber-notifikasi by design platform [BUKTI: operator-prompt T10.3]; VERDICT-LEDGER diisi oleh run pertama yang kebetulan mengamati. Tidak ada watcher otomatis (cron dihapus user 17 Nov — keputusan user yang sah, tetapi konsekuensinya nyata): verdict pilot yang mendarat 22:10–23:18 WIB malam ini pertama kali diketahui sesi utama dari screenshot user pukul 23:23 [PENGALAMAN]. Sistem yang tidak tahu ia baru dibayar sampai pemiliknya menunjukkan dashboard bukanlah sistem pemantauan.

**K12 — Informasi hilang antar-model di tiga titik.**
(a) Blok konteks kebaruan **dilucuti** dari prompt yang dikirim ke lane relay (pagar: prompt gerbang/rubrik tidak boleh terlihat operator relay) — akibatnya pemeriksa relay menilai draf tanpa bahan SURPRISE_GAUGE sama sekali [BUKTI: RANTAI-PEMERIKSA §3]. (b) Pemadatan konteks pada ISR padat mengorbankan peta *covered* 24 → 0 demi mempertahankan kutipan — pemeriksa kehilangan peta 25 jawaban demi 4 kutipan dalam [BUKTI: MITIGASI-KONTEKS-TERPOTONG §4]. (c) Prompt publik relay ≠ prompt internal: kalibrasi hanya menyertifikasi rezim publik; kemampuan lane relay di bawah rubrik internal tidak pernah diukur dan tidak diklaim [BUKTI: RANTAI-PEMERIKSA §3].

**K13 — Tembok struktural liveness vs marathon: doktrin TELAT terhalang aturan yang premisnya usang untuk kanalnya.**
Release TELAT = lahir+2 jam; ronde marathon pertanyaan general berumur ±0,4–1,5 jam. Hasilnya 47/48 tiket due terveto pra-generasi pada populasi malam uji [BUKTI: UJI-1-TEMBAKAN §6 butir 2]. Premis aturan liveness ("target pasca-ronde, upside $0") menargetkan slot ronde — tetapi tesis TELAT menargetkan kanal penugasan verdict berkala atas ISR settled, dan malam ini kanal itulah yang membayar (marathon winner di pertanyaan settled). Selama liveness tidak sadar-lane, lane TELAT tidak akan pernah mencapai generasi pada populasi seperti ini, sebagus apa pun jahitannya. Perbaikannya wilayah terkunci (P3).

**K14 — Skip 6 jam klien stok: biaya sebenarnya belum terukur.**
`PREPARE_SKIP_TTL_S` di klien stok membuat baris yang di-pass-over tidak disajikan ulang selama 6 jam per sesi, dan lapisan kita tidak bisa menimpanya dengan bersih. Penghitung tiket-hilang-pasca-skip (`count_lost_after_skip()`) sudah dibangun, tetapi datanya nol — pada uji asap ia tidak menghalangi (48 baris semuanya baris baru), jadi kerugian nyatanya pada populasi lain belum diketahui [PENGALAMAN: keterbatasan tercatat perbaikan kolam; UJI-1-TEMBAKAN §6 butir 5]. Kelemahannya bukan terbukti merugikan — kelemahannya adalah kita belum bisa mengukurnya.

**K15 — Infrastruktur ephemeral: /etc hilang dua kali dalam satu hari.**
Restart VM menghapus unit systemd + drop-in dua kali pada 18 Nov (±02:15 dan ±12:44 UTC); proses pengamat mati di tengah klasifikasi dua kali juga [BUKTI: NYALA §3; UJI-1-TEMBAKAN §2]. Pemulihan selalu berhasil dari salinan induk di `provider/` — tetapi manual, di giliran yang sama, dan bergantung operator menyadarinya. Tidak ada mekanisme pasang-ulang otomatis.

**K16 — Titik buta pemeriksa dibagi semua model: konsensus prompt-sama bukan validasi.**
Pada kalibrasi rezim prompt publik, racun #1 (preseden Hop karangan) lolos dari **semua** kandidat pemeriksa — Nemotron, qwen, gpt-oss, sol [PENGALAMAN: kalibrasi pemeriksa final 17–18 Nov]. Tiga model yang menyetujui draf yang sama di bawah prompt yang sama bukan tiga validasi independen; itu satu validasi yang diulang. Inilah akar yang kemudian dikunci sebagai aturan konsultasi berperan-beda (T1 addendum transfer) [BUKTI konteks: RANTAI-PEMERIKSA §1 — skor per lane diukur pada korpus & prompt yang sama].

**K17 — Yield terkonsentrasi ekstrem: volume tanpa seleksi = bakar cap.**
Dari 34 jawaban seumur akun, 30 menghasilkan $0; seluruh penghasilan datang dari 4 jawaban pilot lewat dua kanal (Innovator +10 ×4, Marathon +10 ×3) [PENGALAMAN: audit earning 18 Nov malam; dashboard Expert: 34 jawaban, 4 verified]. Verified biasa membayar $0 by design platform. Artinya satu-satunya tuas earning Jalur 1 adalah *pemilihan target*, dan setiap generasi yang jatuh ke bentuk tak-bayar adalah kerugian murni terhadap cap 10/hari.

**K18 — Risiko akun tipis dan biaya ekor yang berjalan diam-diam.**
Reliability kini −6, suspensionCount 6, dan ambang ban permanen tidak terpublikasi [PENGALAMAN: scores live 18 Nov]. Slash REL-005 terbaru tercatat ±3 menit *sesudah* unit mini-batch berhenti — biaya job ter-drop tetap datang bahkan pada nyala yang laporannya "nol kerusakan" [PENGALAMAN: notifikasi 18 Nov 10:31:51 WIB]. Setiap klaim yang gagal di tengah jalan punya harga reliabilitas yang tidak terlihat sampai notifikasi susulan datang.

---

## Penutup lini W5

Sistem orkestrasi kita nyata dan sebagian besarnya terpakai (8 dari 12 kemampuan kelas A), tetapi dua kemampuan yang paling menentukan arah — memilih model per pertanyaan (C) dan revisi berumpan-balik (B, manual saja) — belum menjadi mekanisme. Peluang terbesar berikutnya bukan di Jalur 1 melainkan Jalur 2 yang gerbangnya baru terbuka malam ini (P1). Kelemahan paling menentukan bukan lagi mutu draf, melainkan tiga hal struktural: tembok liveness-vs-marathon (K13), pemantauan verdict yang manual (K11), dan penulis yang mengarang penunjuk presisi tanpa retrieval (K1/K3) — dengan catatan jujur K2 bahwa panel, pada sampel pertama ini, tidak menghukum K1 seberat yang gerbang kita takutkan.
