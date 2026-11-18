# AUDIT BAHAN BAKAR DIALECTICA — INVENTARIS SISA SEMUA LANE (LIVE)

**Waktu audit:** 2026-11-14 ±04:53–04:56 WIB (2026-11-13T21:53–21:56Z).
**Sifat:** read-only + maks 1 probe pendek per lane, hanya di lane tanpa bacaan tanpa-generasi. NOL klaim, NOL serve dinyalakan/diubah, NOL perubahan config/kode.
**Sumber yang dibaca langsung:** MEKANISME-DAN-LAPANGAN.md §37/§39/§40 + §67–§76 (status lane per jendela 13 Nov); KULIT-2-AUTOPSI-KAPASITAS-2026-11-12.md Bagian 2 (GARIS PEMBANDING WAJIB); `provider/token-usage.jsonl` diparse penuh (63 record s/d 13 Nov 14:02Z + 1 record probe audit ini); CONNECTOR.md × 4 (openrouter, cloudflare-workers-ai, alibaba-dashscope, z-ai); buku stok `~/workspace/research/free-lanes/DASHSCOPE-STOCK-2026-11-10.md`.
**Satuan pola pakai untuk runway:** hunt 8 jendela kerja/hari; probe OpenRouter terukur −2 request/jendela; serve §39 cap 10 generasi/hari-UTC; drill bayangan ±1 generasi; 1 klaim one-shot = 1 generasi kelas-klaim (±3,3–8 rb token / ±187–290 neuron khas) + kemungkinan 1 regenerasi wrapper.

## RINGKASAN

| Lane | Sisa sekarang (sumber) | Status |
|---|---|---|
| Vyce — GLM 5.3 Flash | **HIDUP lagi** — probe 04:55 WIB lolos 3,2 dtk (saldo $ TAK BISA DICEK) | HIDUP (bukti probe pendek tunggal) |
| Vyce — deepseek-v4.1 / Nemotron-Vyce | Tak diprobe pagi ini; obs terakhir 21:00 13 Nov = TIMEOUT-130 | TAK BISA DICEK (pagi ini) |
| OpenRouter / Nemotron | **36 dari 50 request** (endpoint key live) | CUKUP |
| Cloudflare gpt-oss-120b (+ serve §39) | **0 neuron terpakai hari-UTC ini** → 10.000 utuh per log lokal (anggaran kerja 9.000) | CUKUP |
| DashScope deepseek-v4-pro-0813 (lane klaim) | **HANGUS terkonfirmasi live** — 403 free quota exhausted | MATI |
| DashScope model lain (drill saja) | ±9,99 jt token di 10 model belum kedaluwarsa (buku stok, tak terverifikasi live) | CUKUP (drill) |
| Z.ai glm-4.7-flash | **HIDUP** — probe 04:54 WIB 200 "OK" tanpa 1305; kuota memang tak terbit | HIDUP / runway TAK BISA DICEK |

**Vonis agregat:** bahan bakar TETAP BUKAN pengikat (sama seperti vonis KULIT-2: surplus di atas appetite terencana) — pengikat tetap STOP TOTAL formal + kualitas verdict (0/3) + pasokan pertanyaan. Dua perubahan struktural sejak KULIT-2: (1) **Vyce GLM menjawab lagi** sesudah 8 jendela berturut-turut 503 — kondisi pensiun serve §39 ("satu probe Vyce lolos") kini terpicu di level probe; tindak-lanjutnya wilayah sesi utama/hunt, BUKAN audit ini; (2) **lane klaim DashScope resmi mati** — tangga probe efektif kini: Vyce → OpenRouter → Cloudflare → Z.ai.

---

## 1. VYCE (GLM 5.3 Flash / deepseek-v4.1 / Nemotron-Vyce)

**(1) Sisa + sumber + stempel:** TIDAK ADA jalur baca saldo dalam perkakas kita — provider Vyce hanya chat-completions; tidak ada endpoint panel/API saldo yang pernah terdokumentasi di file kita. Angka terakhir yang tercatat: saldo promo **$109,3485** (stok, FUEL-AUDIT 10 Nov, dikutip KULIT-2 §2.5) + jatah promo GLM **10 jt token/hari** (reset 07:00 WIB) — keduanya **TIDAK terverifikasi ulang pagi ini dan tidak bisa diverifikasi tanpa panel user**. Yang terverifikasi live pagi ini adalah KETERSEDIAAN, lewat 1 probe pendek (aturan audit): `probe_vyce_rung.py glm-5.3-flash`, prompt "OK", **2026-11-14 04:55 WIB → rc=0, latensi 3,2 dtk, jawaban "OK" (2 kar), usage 64 token** (23 prompt / 41 completion), tercatat di token-usage.jsonl 21:55:24Z.

**(2) Laju bakar khas:** probe 64 token; siklus klaim penuh ±30–80 rb token (FUEL-AUDIT via KULIT-2 §2.5 — angka lama, tak diukur ulang).

**(3) Runway:** bila GLM bertahan hidup: 10 jt token/hari ÷ 30–80 rb = **±125–300 siklus klaim/hari di atas kertas** — jauh di atas tangga internal tertinggi (RAMP 4–10/hari). Runway hari: tidak mengikat dalam skenario apa pun yang sah.

**(4) Reset/hangus:** jatah harian reset 07:00 WIB; saldo promo $ = stok tanpa tanggal hangus yang tercatat (tak terverifikasi).

**(5) Status per model:**
- **GLM 5.3 Flash: HIDUP** — probe pertama yang LOLOS sesudah **503 eksplisit 8 jendela berturut-turut** (13 Nov 07:00–21:00, §67–§74) dan mati total sejak 10 Nov 14:04. Kejujuran wajib: ini SATU probe prompt-pendek; generasi kelas-klaim (prompt panjang, streaming) BELUM terbukti pagi ini, dan lane ini punya riwayat mati di tengah pola. Vonis = hidup-di-probe, belum hidup-terbukti-klaim.
- **deepseek-v4.1: TAK BISA DICEK pagi ini** (slot probe lane ini dipakai GLM). Observasi terakhir: TIMEOUT-130 di jendela 21:00 13 Nov (7–8 jendela beruntun); anomali tercatat 13 Nov pagi — ia MENJAWAB 2 probe (07:02 + 08:59 WIB) tetapi completion hanya 1–2 token (record tanpa-label-lane di log: prompt 1.231, completion 1–2) → klasifikasi terakhir: menjawab-tapi-tidak-andal.
- **Nemotron-Vyce: TAK BISA DICEK pagi ini.** Observasi terakhir: TIMEOUT-130, 21:00 13 Nov.

**Status lane: HIDUP BERSYARAT (GLM) / saldo TAK BISA DICEK.**

## 2. OPENROUTER / NEMOTRON (nvidia/nemotron-3-ultra-550b-a55b:free)

**(1) Sisa + sumber + stempel:** endpoint key resmi, TANPA generasi — `client.py key`, **2026-11-13T21:53Z (04:53 WIB)**: `is_free_tier=true`, `free_model_daily_requests = {used: 14, limit: 50, remaining: 36}`. Angka used=14 cocok persis dengan log kita hari-UTC ini (14 record probe 13 Nov = 7 jendela × 2) — buku dan server sepakat.

**(2) Laju bakar khas:** kuota berbasis REQUEST, bukan token: 1 generasi = 1 request (percobaan gagal pun terhitung sesudah generasi berjalan). Generasi kelas-klaim terukur 3.262–5.296 token (tak relevan ke kuota); probe hunt terukur konsisten **−2 request/jendela** (pola §73/§74, terkonfirmasi log 12–13 Nov). Provider kita abort bila sisa <3 → sisa pakai efektif harian 47.

**(3) Runway:** sisa 36 → pola probe saja (16/hari) = lebih dari cukup sisa hari-UTC ini (reset ±2 jam lagi). Sesudah reset: 50/hari − probe 16 − drill 1–2 = **±32 request ≈ 10–25 klaim terkirim efektif** (regen wrapper + kekosongan E2 memakan request ekstra; rentang sama seperti KULIT-2 §2.2 — tidak berubah).

**(4) Reset:** 00:00 UTC = **07:00 WIB hari ini** (tiap hari).

**(5) Status: CUKUP.** Lane ini juga yang membawa mode NORMAL-NEMOTRON di semua jendela 13 Nov (generasi uji lolos tiap jendela) — ketersediaannya saat ini adalah yang paling stabil terukur dari semua lane.

## 3. CLOUDFLARE / gpt-oss-120b (klaim §37 + serve §39 — satu kolam neuron)

**(1) Sisa + sumber + stempel:** **TIDAK ADA bacaan resmi sisa neuron akun** — API/connector tidak mengekspos pemakaian alokasi harian (perintah `accounts` hanya cek kesehatan token: **200, success=true, 04:53 WIB**). Sumber angka = log lokal `token-usage.jsonl` (itulah yang dipakai provider sendiri untuk pagarnya). Hari-UTC berjalan (2026-11-13): **0 record** di kedua lane Cloudflare (`cloudflare-gptoss` + `cloudflare-serve`) → **0 neuron terpakai; sisa 10.000 penuh per log; anggaran kerja provider 9.000** (abort pra-generasi >9.000, cadangan keamanan 1.000). Pembanding: hari-UTC kemarin (12 Nov) terpakai **5.617,80 neuron** (5 generasi 2c7efc3e, dua di antaranya konteks-berat 2.403–2.432 neuron). Serve §39 sepanjang 13 Nov: **0 generasi** (semua kandidat tersaring pra-generasi — cap serve terbaca 0/10 di §76).

**(2) Laju bakar khas (dari log):** generasi kelas-klaim tipikal **177–288 neuron** (bench median 187,04; angka rencana KULIT-2 ±250); generasi konteks-berat terukur **1.501–2.432 neuron** (prompt ±40–70 rb token). Generasi serve = pipeline yang sama, pita yang sama.

**(3) Runway:** anggaran 9.000/hari ÷ 250 = **±36 generasi/hari gabungan klaim + serve**. Serve maksimal (cap 10 gen ≈ 1.870–2.500 neuron) menyisakan **±26 generasi klaim**; hari yang semua targetnya konteks-berat: total bisa jatuh ke **±6 generasi/hari**. Reset harian membuat runway = 1 hari berjalan + penuh lagi besok — tidak ada akumulasi.

**(4) Reset:** 00:00 UTC = **07:00 WIB tiap hari**. Cap serve 10 generasi juga per hari-UTC (counter persisten dari file log — vonis kode 13 Nov 19:22).

**(5) Status: CUKUP** (tangki penuh pagi ini per satu-satunya buku yang ada). Jahitan akuntansi yang tetap harus dibaca apa adanya (warisan §37): generasi lewat client connector LANGSUNG (di luar provider kita) tidak masuk log lane — sejak 12 Nov tidak ada generasi semacam itu yang diketahui; angka 0 hari ini adalah angka log, bukan angka panel Cloudflare.

## 4. DASHSCOPE (workspace Alibaba Model Studio, Singapore)

### 4a. deepseek-v4-pro-0813 — model yang ter-wire ke jalur klaim (§40)

**(1) Sisa + sumber + stempel:** **0 — HANGUS, terverifikasi LIVE pagi ini.** Probe tunggal audit (prompt "OK", max 64 token, `enable_thinking:false`) **2026-11-14 ±04:54 WIB → HTTP 403, code `insufficient_quota`: "The free quota has been exhausted…"** — ditolak pra-generasi, **0 token terbakar**. Ini konsisten dengan buku stok (kedaluwarsa **2026-11-12**) dan sekaligus **bukti live PERTAMA bahwa Stop-on-Exhaust benar-benar menolak alih-alih menagih** (di §40 statusnya masih "belum pernah teramati live"; permukaan error-nya lewat API kompatibel-OpenAI berkode `insufficient_quota`, bukan string `AllocationQuota.FreeTierOnly` dari dokumentasi — semantiknya identik: kuota gratis habis, tidak ada tagihan). Sisa buku ±979.180 token (aritmetika KULIT-2 §2.3: 987.129 pasca-bench − 5.084 uji asap − 2.865 probe 11 Nov) kini **bernilai nol** — jatahnya kedaluwarsa, bukan terpakai.

**(2) Laju bakar khas (historis):** 1.391–4.770 token/generasi (median ±4.187) — kini tak relevan untuk model ini.

**(3) Runway lane klaim DashScope: 0 generasi, 0 hari.** Tidak ada model DashScope lain yang ter-wire ke jalur klaim.

**(4) Hangus:** terkonfirmasi per hari ini (grant berakhir 2026-11-12).

**(5) Status: MATI.**

### 4b. Model lain — tangki DRILL (bukan klaim; tidak ter-wire, §40/KULIT-2 §2.3)

Sisa dari buku stok 10 Nov dikurangi pemakaian terukur di file itu; **API tidak mengekspos sisa kuota — angka di bawah ini aritmetika buku, TIDAK terverifikasi live pagi ini** (memverifikasi satu model = membakar stoknya; aturan audit melarangnya di luar 1 probe/lane yang sudah dipakai 4a):

| Model | Sisa buku (token) | Kedaluwarsa |
|---|---|---|
| qwen3.8-27b | 1.000.000 | 2026-11-17 |
| kimi-k3 | 1.000.000 | 2026-11-17 |
| glm-5.3 | 999.906 | 2026-11-22 |
| qwen3.8-flash | 999.677 | 2026-11-24 |
| qwen3.8-max-0902 | 1.000.000 | 2026-11-30 |
| deepseek-v4.1-flash | 999.890 | 2026-12-12 |
| qwen3.8-omni-flash | 1.000.000 | 2026-12-16 |
| qwen3.8-omni-flash-realtime | 1.000.000 | 2026-12-20 |
| deepseek-v4.1-flash-1017 | 1.000.000 | 2027-01-16 |
| kimi-k3.1-pro | ±1.000.000 (pemakaian probe 10 Nov TIDAK terukur server) | 2027-02-01 |

**Total ±9,99 jt token** ≈ pada unit drill ±4,5 rb token/generasi ≈ **±2.200 generasi drill**, tersebar menurut jendela kedaluwarsa (±5 jt hangus ≤30 Nov). qwen3.8-2.4t-a95b: kedaluwarsa 2026-11-11 + dinyatakan tidak bisa dibakar sejak bench — dikeluarkan. **Status tangki drill: CUKUP** (dengan catatan buku-di-atas). Semua model ini reasoning/thinking-default — drill tetap butuh disiplin `enable_thinking` per model; tidak satu pun mengubah runway KLAIM.

## 5. Z.AI / glm-4.7-flash

**(1) Sisa + sumber + stempel:** lane ini **tidak punya kuota yang bisa dibaca** — Z.ai tidak menerbitkan limit angka untuk model $0 dan tidak ada respons yang pernah membawa header rate-limit (CONNECTOR.md + §40). Bacaan tanpa-generasi yang ada = katalog `models` (**200, 04:53 WIB** — key sehat; katalog memang hanya memuat model berbayar, Flash $0 tidak tampil, sesuai dokumentasi). Verifikasi ketersediaan = 1 probe pendek audit: **2026-11-14 ±04:54 WIB → HTTP 200, "OK", latensi 24,1 dtk, 18 token total, TANPA 1305** (thinking disabled, sesuai syarat lane).

**(2) Laju bakar khas:** bukan stok — model $0. Generasi kelas-klaim terukur 8.133 token (bench, completion mentok 8.000). Yang dikonsumsi adalah KESEMPATAN (kolam gratis bersama), bukan token.

**(3) Runway:** **tidak bisa dinyatakan dalam generasi/hari** — tidak ada penyebutnya. Pembanding historis: bench 10 Nov kena 1305 pada 6/10 attempt; jendela 07:00 11 Nov mati sesudah 1305 ×2 (sesudah retry). Pagi ini percobaan pertama langsung lolos — keadaan kolam membaik pagi ini, tanpa jaminan apa pun untuk jendela berikutnya. Perlakuan rencana tetap seperti KULIT-2: **0 terencana, oportunistik** sampai ketersediaan terbukti lintas ≥3 jendela.

**(4) Reset/hangus:** tidak ada (tidak ada jatah bertanggal).

**(5) Status: HIDUP pagi ini / runway TAK BISA DICEK** (jenuh 1305 = sesaat dan terbedakan jelas dari habis permanen: pagi ini tidak terjadi sama sekali).

---

## 6. BAKAR AUDIT INI (akuntansi wajib)

| Aksi | Lane | Terbakar |
|---|---|---|
| `client.py key` (baca, tanpa generasi) | OpenRouter | 0 request |
| `client.py accounts` (cek token) | Cloudflare | 0 neuron |
| `client.py models` (baca katalog) | Z.ai | 0 |
| Probe "OK" glm-5.3-flash (lolos) | Vyce | **64 token** (kolam promo) |
| Probe "OK" deepseek-v4-pro-0813 (**403, ditolak pra-generasi**) | DashScope | **0 token** |
| Probe "OK" glm-4.7-flash (lolos) | Z.ai | **18 token** (model $0) |

Total generasi sukses: 2 (keduanya prompt "OK" 2-karakter). Tidak ada lane yang diprobe lebih dari sekali; Vyce rung deepseek/Nemotron sengaja TIDAK diprobe (aturan maks 1/lane — slot dipakai rung primer GLM).

## 7. DAFTAR NEGATIF — yang TIDAK bisa diverifikasi pagi ini

1. **Saldo $ / sisa token promo Vyce** — tidak ada jalur baca dalam perkakas kita; angka $109,3485 + 10 jt token/hari adalah angka 10 Nov, dinyatakan sebagai angka lama, bukan bacaan.
2. **Sisa neuron resmi Cloudflare dari panel/API** — tidak diekspos connector/API yang kita punya; angka 10.000-utuh berasal dari log lokal (yang memang menjadi buku pagar provider), dengan jahitan generasi-client-langsung yang dicatat di §3(5).
3. **Sisa per-model DashScope selain deepseek-pro** — API tidak mengekspos sisa; semua angka 4b adalah aritmetika buku stok 10 Nov, bukan bacaan live. Kedaluwarsa = tanggal konsol 10 Nov.
4. **Kapasitas harian Z.ai** — tidak diterbitkan provider dan tidak teramati dari header; runway numerik apa pun untuk lane ini adalah karangan, jadi tidak ditulis.
5. **deepseek-v4.1 + Nemotron-Vyce pagi ini** — tidak diprobe (aturan 1 probe/lane); statusnya di file ini adalah observasi terakhir 13 Nov 21:00, diberi label sebagai itu.
6. **Kelas-klaim Vyce GLM** — probe "OK" 64 token tidak membuktikan generasi prompt-panjang/streaming kelas klaim; runway §1(3) adalah aritmetika jatah terdokumentasi, bukan uji beban.

## 8. PERBANDINGAN LAWAN KULIT-2 (2026-11-12) — apa yang berubah

| Butir | KULIT-2 (12 Nov) | Audit ini (14 Nov) |
|---|---|---|
| Vyce | Mati ±40 jam; nilai hari ini 0 | **GLM lolos probe** (3,2 dtk) — perubahan terbesar; 2 rung lain belum dicek |
| OpenRouter | Sisa 39 (11 Nov) | **36 sisa, used 14 — endpoint live**; pola −2/jendela terkonfirmasi 2 hari lagi |
| Cloudflare | Terpakai 2.634,88 (11 Nov) | Hari-UTC ini **0**; kemarin 5.617,80; laju & runway sama (±36 gen/hari) |
| DashScope klaim | ±979 rb token tapi hangus HARI ITU (12 Nov) | **Hangus terkonfirmasi live 403**; Stop-on-Exhaust terbukti menolak (baru) |
| DashScope drill | ±9,999 jt token | ±9,99 jt (sama; 2 hari kedaluwarsa berlalu tanpa pemakaian) |
| Z.ai | Parkir (1305 beruntun) | **Lolos probe tanpa 1305** pagi ini; tetap 0-terencana (belum 3 jendela bukti) |
| Total berkelanjutan | ±86 generasi/hari | ±86 yang sama (CF 36 + OR 50) **+ Vyce hidup-di-probe** (±125–300 siklus di atas kertas bila bertahan) |
| Pengikat | Bahan bakar BUKAN pengikat (surplus 3–5×) | **Tidak berubah** — surplus kini lebih besar; pengikat tetap gerbang/verdict/pasokan |
