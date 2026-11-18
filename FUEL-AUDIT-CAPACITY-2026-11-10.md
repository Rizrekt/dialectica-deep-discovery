# AUDIT BAHAN BAKAR vs KAPASITAS EXPERT DILONGGARKAN — Dialectica (2026-11-10 ±19:0x WIB)

Perintah user 2026-11-10 19:00: "liat juga nanti bahan bakar kita cukup gak kalau kita rubah semua limit capacity nya dan yang ada disitu". **READ-ONLY TOTAL** — audit ini tidak mengubah config Expert, tidak menyentuh cron, tidak menjalankan klaim/serve/generasi apa pun (run hunt 19:00 sedang jalan; nol panggilan API provider baru diterbitkan). Semua angka dari file: MEKANISME-DAN-LAPANGAN.md (§24/§25/§30/§35/§37/§39/§40), `provider/token-usage.jsonl`, BENCH OpenRouter, BENCH+ELIGIBILITY Cloudflare, ZAI-BENCH, DASHSCOPE-BENCH + DASHSCOPE-STOCK.

## 0. Inventaris setting halaman Expert (yang mau dilonggarkan)

| Item halaman | Sekarang | Rentang UI | Status/sumber |
|---|---|---|---|
| Entry Strategy | **Dynamic** | 6 strategi | Tetap — bukan tuas bahan bakar |
| Daily limit (`maxIsrs24h`) | **20** | sampai ∞ (`none` = unlimited diterima server, §24) | Topi yang KITA pasang; platform menegakkan angka kita, bukan kuota platform (§24 butir 3) |
| Max Concurrency | **1** | 1–10 | Config kita (`agent show`, §24); serial 1 job pada satu waktu |
| Advanced cost limits (`maxTokens24h`/`maxUsd24h`/warn) | **unlimited (null)** | — | Terverifikasi dari server 2026-11-10 13:45–13:46 (§24.1): "maxUsd24h/maxTokens24h tetap unlimited". **Tidak ada yang perlu dilonggarkan di sini — memang sudah terbuka penuh.** |

Catatan pembaca angka: dua unit dipakai di seluruh audit. **(a) Unit TERUKUR** = konsumsi nyata generasi kelas-klaim dari bench/log kita. **(b) Unit WORST-CASE platform** = prompt job ±75 rb token (§24/§25.6 — prompt memuat pertanyaan + jawaban yang sudah ada; siklus koreksi sampai 3 putaran) → ±83 rb token sekali jalan, ±249 rb token bila 3 putaran penuh. Unit (b) adalah skenario ekstrem untuk uji ketahanan, BUKAN ramalan.

## 1. Tabel per lane — kapasitas, sisa, jam hangus

| Lane | Bahan bakar | Unit (a) terukur per generasi | Kapasitas (a) | Unit (b) worst-case | Kapasitas (b) | Sisa per audit ini | Jam hangus / reset |
|---|---|---|---|---|---|---|---|
| **Vyce GLM 5.3 Flash (promo)** | 10 jt token/hari, $0 | Siklus klaim penuh ±30–80 rb token (§24/§25.6, estimasi struktural — provider Vyce tidak mencatat usage) | **±125–300 klaim/hari** | ±249 rb token/klaim (75 rb × 3 putaran + 8 rb out/putaran) | ±40 klaim/hari (sekali jalan 83 rb → ±120) | Penuh tiap hari (berulang) | Reset **07:00 WIB** harian. ⚠️ Lane-nya sendiri sedang DOWN (downtime resmi) — kapasitas ini di atas kertas sampai Vyce pulih |
| **Vyce saldo promo (deepseek-v4.1 dkk)** | Saldo **$109,3485** (stok, bukan harian) | $0,012–0,037 per jawaban (§25) | **±2.900–9.000 jawaban total stok** | Sama (tarif per token tetap) | Sama | $109,3485 utuh (klaim v4.1 belum jalan) | Tidak hangus harian; terbakar per pemakaian saja |
| **OpenRouter free (Nemotron)** | 50 request/hari (counter hanya bergerak bila generasi benar-benar berjalan — gagal pra-generasi 403/429 TIDAK memotong, terukur di BENCH) | 1 request = 1 generasi; regen wrapper = request terpisah. Token/generasi terukur 3.262–5.296 (log) — tak relevan ke kuota | **50 generasi/hari** → pada pola Nemotron (mentah di bawah lantai panjang 4/5 run → regen sering) efektif **±25–50 klaim/hari** | Kuota berbasis request, bukan token: worst-case = semua generasi regen → tetap 50 request, klaim efektif turun ke ±25 | 50 request (sama) | **Sisa 40/50** per `token-usage.jsonl` terakhir pra-run 19:00 (11:58 UTC, `quota_remaining_after: 40`); run 19:00 yang sedang jalan bisa menguranginya — tidak bisa dibaca tanpa panggilan baru | Reset 00:00 UTC = **07:00 WIB** |
| **Cloudflare (gpt-oss-120b)** | 10.000 neuron/hari account-wide | Median **187,04 neuron/generasi** (bench 3 run: 177,29/207,70/187,04; generasi lebih pendek terukur 128,56) | **±53 generasi/hari** total akun; pagar provider abort >9.000 neuron/hari-UTC → praktis **±48** | Prompt 75 rb token ≈ 75 rb × 31,818/jt (in) + 8 rb × 68,182/jt (out) ≈ **±2.931 neuron/generasi** | **±3 generasi/hari** (ekstrem — prompt nyata kita ±562 token masuk) | Belanja platform hari ini ±735,5 neuron pra-hunt (§37, termasuk generasi client-langsung di luar log lane); sisa efektif ±9.264 neuron sebelum run 19:00 | Reset **00:00 UTC** (= 07:00 WIB). **Jatah klaim vs serve berbagi kolam yang sama** (lihat §2) |
| **DashScope — deepseek-v4-pro-0813** (satu-satunya kandidat klaim lane ini) | Stok token sekali pakai | Bench: 3.687/4.770/4.187 token per generasi penuh (median ±4.187); buku stok memakai unit maksimal ±6,5 rb | **±982.045 token → ±150–218 generasi total** (bukan per hari) | 83 rb token/generasi sekali jalan | ±11 generasi total | **±982.045 token** (987.129 pasca-bench − 5.084 uji asap §40), tercatat di log lane `dashscope-deepseekpro` | **HANGUS 2026-11-12** — jendela bakar tersisa ±1 hari; sesudah itu stok ini nol berapa pun sisanya |
| **DashScope — 10 model lain** (drill/belum claim-grade) | Stok token sekali pakai | Belum ada unit klaim terukur (semua model reasoning, thinking default ON; hanya qwen3.8-flash terbukti menghasilkan konten utuh — 999.677 token sisa) | Total tangki di luar deepseek-pro **±9,999 jt token** — kapasitas DRILL, bukan klaim | Sama seperti di atas per generasi | — | Total seluruh tangki (11 model bisa-bakar) **±10,98 jt token** | Bertingkat: 2026-11-17 (27b, kimi-k3) → 11-22 (glm-5.3) → 11-24 (flash) → 11-30 (max) → Des–Feb (flash-1017, kimi-k3.1-pro). qwen3.8-2.4t-a95b (±1 jt, hangus 2026-11-11) **ditulis-off: tidak bisa dibakar** (thinking tak bisa dimatikan, generasi tak selesai) |
| **Z.ai (glm-4.7-flash)** | Tanpa kuota terukur — model $0, limit = **konkurensi 1** (tabel resmi, addendum bench) | Kapasitas = fungsi WAKTU: latensi generasi sukses 20,5–35,2 dtk (bench); dengan 1× retry 1305 (+60 dtk tunggu) siklus generasi terburuk ±240 dtk | Waktu murni: **±15–100+ generasi/jam** — jauh di atas kebutuhan; yang membatasi adalah KETERSEDIAAN kolam: bench 6/10 attempt kena 429-1305, hanya 1/3 run bench tuntas | Tidak ada unit token — worst-case-nya adalah hari jenuh total (1305 terus) = kapasitas efektif mendekati 0 pada jendela itu | Sama (ketersediaan, bukan stok) | Tidak ada stok untuk dihabiskan | Tidak ada jam hangus; berulang tanpa reset terbit |

**Siapa habis duluan (bila satu lane memikul sendirian):** DashScope deepseek-pro habis oleh KALENDER (2026-11-12) berapa pun lajunya → Cloudflare oleh neuron (±53 generasi/hari) → OpenRouter oleh request (50/hari, efektif ±25 klaim pada pola regen Nemotron) → Z.ai oleh ketersediaan (acak, bukan stok) → Vyce GLM praktis tidak pernah habis pada appetite kita (125–300/hari terukur).

## 2. Jahitan Cloudflare: klaim vs serve berbagi satu kolam

Pagar §39: serve pengganti Cloudflare **cap keras 10 generasi/hari-UTC** (3 lapis penegakan) — cap itu membatasi JUMLAH generasi serve, tetapi neuronnya keluar dari kolam 10.000 yang sama dengan klaim. Aritmetika hari penuh: 10 generasi serve × 187 neuron ≈ **1.870 neuron**, menyisakan ±8.130 neuron ≈ **±43 generasi klaim** sebelum kolam platform habis (pagar provider klaim menghitung lane-nya sendiri pada 9.000; serve menghitung gabungan — §39). Jadi di lane Cloudflare, klaim + serve TIDAK bisa sama-sama maksimal: gabungan realistisnya **±53 generasi/hari untuk keduanya**.

## 3. Vonis per skenario kebutuhan

Definisi generasi: 1 generasi = 1 panggilan model menghasilkan draf; 1 klaim bisa memakan sampai 2 generasi (generasi awal + 1 regenerasi wrapper).

### Skenario A — tangga internal sekarang (PENUH 15–20 klaim/hari + drill 5 + serve)
Kebutuhan: 20 klaim × ≤2 generasi = ≤40 + drill 5 → **≤45 generasi/hari** (khas: ±25–35, karena regen tidak selalu terpicu — Cloudflare bench 0/3 regen, DashScope 0 regen; Nemotron yang sering). Serve: Vyce = tanpa cap proses (generasinya ikut kolam promo yang sama); Cloudflare = cap 10 (masuk hitungan kolam neuron di atas).

| Lane memikul sendirian | Vonis A | Alasan angka |
|---|---|---|
| Vyce GLM (bila pulih) | **CUKUP** | 45 gen × 30–80 rb = 1,35–3,6 jt dari 10 jt token/hari. Bahkan unit (b) ekstrem: 45 × 249 rb = 11,2 jt — hanya skenario ekstrem yang menembus, dan saldo deepseek menyerap limpahan ($0,012–0,037/jawaban) |
| OpenRouter | **TIPIS** | 45 dari 50 request = muat tanpa slack (vonis bench sendiri); satu hari regen-ramai menembus 50 → klaim terakhir hari itu gugur |
| Cloudflare | **TIPIS** | 45 gen klaim+drill × 187 = 8.415 neuron (84% kolam) — lolos sendirian; DITAMBAH serve cap penuh 10 gen (±1.870) = 10.285 > 10.000 → **gabungan klaim-maks + serve-maks TIDAK muat**; salah satu harus di bawah maks |
| DashScope deepseek-pro | **CUKUP untuk ±1 hari saja** | 45 gen × ±4,5 rb ≈ 202 rb token/hari vs stok 982 rb — cukup ±4–5 hari pada laju itu, TAPI hangus 2026-11-12 memotongnya jadi booster satu hari (±150–218 generasi total), bukan lane harian |
| Z.ai | **TIPIS (ketersediaan)** | Waktu cukup (≤±2,5 jam generasi murni untuk 45 gen pada siklus retry terburuk); 1305 yang memutuskan, bukan stok |

**Vonis A: CUKUP** — dengan pool rotasi (tangga probe §40), tidak ada lane yang wajib memikul sendirian; dua titik tipisnya teridentifikasi: OpenRouter tanpa slack dan Cloudflare bila klaim+serve sama-sama dimaksimalkan.

### Skenario B — daily limit dibuka ∞, appetite generasi maksimal kita 45/hari
Kebutuhan generasi identik dengan A-worst: **45 generasi/hari**. Agregat kapasitas harian berulang (di luar stok DashScope): Vyce ±125–300 + OpenRouter 50 + Cloudflare ±53 + Z.ai berbasis waktu = **≥228 generasi/hari terukur — ±5× appetite**.

**Vonis B: CUKUP, bahan bakar BUKAN pengikat.** Yang mengikat sesudah cap server dibuka bukan bahan bakar, melainkan (dari §24/§25/§30): (1) **pasokan** — pertanyaan General baru hanya ±15–25/hari platform-wide; 45 generasi ≠ 45 klaim bermakna; (2) **serialitas** — siklus job ±10–25 menit pada konkurensi 1 (±4/jam teoritis); (3) **tangga internal** RAMP 4–10 / PENUH plafon 15–20 (kebiasaan 8–12) yang memang sengaja di bawah appetite; (4) **rem REL-005**. Satu-satunya catatan bahan bakar di B: bila Vyce mati DAN Cloudflare diminta memikul klaim + serve sekaligus, neuron habis duluan (±53 gabungan) — appetite 45 masih muat, tanpa cadangan untuk drill di lane yang sama.

### Skenario C — Max Concurrency >1
- **Kebutuhan bahan bakar harian: TIDAK berubah oleh konkurensi.** Total generasi/hari ditentukan tangga + cap serve, bukan oleh berapa job berjalan paralel. Yang berubah adalah BENTUK bebannya: serve bisa menerima beberapa job SEKALIGUS saat batch pertanyaan terbit bersamaan (batch memang datang berkelompok, §24) → lonjakan generasi paralel (mis. 3 tangkapan Pioneer = 3 generasi serentak).
- **Per lane:** Vyce menyerap lonjakan dengan mudah (kolam 10 jt). Cloudflare serve: cap 10 generasi/hari-UTC §39 tetap mengikat — konkurensi tidak menaikkan satu pun generasi tambahan, hanya mempercepat habisnya cap; neuron tetap ±1.870 untuk 10 generasi. OpenRouter/DashScope/Z.ai = one-shot saja, serve ditolak exit 5 di kode (§35/§37/§40) → konkurensi server **tidak berpengaruh apa-apa** ke tiga lane ini. Z.ai bahkan menolak paralel secara API: konkurensi model = 1, panggilan paralel = tabrakan buatan sendiri.
- **Risiko (yang sebenarnya bergerak):** siklus serial sekarang ±10–25 menit/job → konkurensi 1 ≈ ±4 job/jam. Konkurensi N menaikkan throughput teoritis ke ±4N/jam, TAPI setiap job in-flight wajib tuntas dalam timeout platform (generate ≤15 menit; liveness one-shot ±30 menit) — dan modus kegagalan terbukti kita adalah job diambil-tak-selesai (6/6 abandoned 8 Nov pada konkurensi **1**). Kematian satu proses/koneksi pada konkurensi N meng-abandon **N job sekaligus** = kerusakan REL N× lipat dalam satu kejadian, melawan bantalan kita yang tipis (REL −3, 3 suspensi tercatat; kill-metric (iv): 1 abandoned baru = STOP hari itu). Latensi generasi kita juga tidak kecil (Nemotron median 85 dtk; DashScope ±87 dtk; Z.ai sampai ±240 dtk dengan retry) — paralel menumpuk antrean API/VM 1,5-CPU dan menggerus margin timeout 15 menit.
- **Vonis C: bahan bakar CUKUP, RISIKO yang KURANG.** Konkurensi adalah tuas reliabilitas, bukan tuas bahan bakar — menaikkannya tidak membeli satu generasi pun yang tidak sudah bisa dibeli konkurensi 1 dalam sehari.

## 4. Rekomendasi setting final per item (REKOMENDASI SAJA — tidak dieksekusi di audit ini)

| Item | Rekomendasi | Alasan bahan bakar + mekanik |
|---|---|---|
| **Daily limit (`maxIsrs24h`)** | **Naikkan 20 → `none` (unlimited)** | Bahan bakar surplus ±5× appetite maksimal (Skenario B) — cap server tidak melindungi stok apa pun. Ia justru pernah melukai kita: usage menghitung job yang GAGAL juga (3 ISR warisan serve gagal mengunci jendela 8 Nov, §24), jadi cap rendah = risiko kunci-diri. Pengatur volume yang sah tetap **tangga internal di badan hunt** (RAMP 4–10; PENUH plafon 15–20, kebiasaan 8–12) + kill-metric — keduanya sadar-kualitas, cap server tidak. Syarat pendamping: gerbang hunt yang hari ini membaca "usage < caps 20" harus dinyatakan ulang sebagai "usage dibaca + dibandingkan lawan tangga internal" pada saat perubahan dieksekusi, supaya tidak ada dua pengatur yang bertabrakan |
| **Max Concurrency** | **TETAP 1** | Nol keuntungan bahan bakar (Skenario C); keuntungan throughput-nya tidak bisa dipakai karena pasokan (±15–25 pertanyaan baru/hari) berada jauh di bawah kapasitas serial (±4/jam). Kerugiannya terukur: paparan abandoned berlipat per kejadian melawan REL −3. Tinjau ulang HANYA sesudah (a) klaim pertama terbukti "completed" dan bantalan completed mulai terbangun, dan (b) ada uji paralel provider yang terukur — bukan karena halaman UI menawarkannya sampai 10 |
| **Advanced cost limits (`maxTokens/maxUsd`)** | **BIARKAN unlimited (null) — jangan diisi** | Status terverifikasi §24.1 memang sudah null. Tidak ada eksposur uang asli untuk dilindungi: seluruh lane berjalan di kredit promo + free tier ($0 kas). Pagar anggaran yang nyata sudah hidup di tempat yang benar — provider Cloudflare abort >9.000 neuron, OpenRouter abort sisa kuota <3, DashScope Stop-on-Exhaust (konsol), cap serve §39. Cap biaya di level Expert adalah rem tumpul kedua yang menghitung dengan satuan berbeda dan bisa mengunci di tengah siklus — pola yang sama dengan pelajaran caps 8 Nov |
| **Entry Strategy** | **Tetap Dynamic** | Di luar mandat audit bahan bakar; dicatat hanya untuk menegaskan tidak ada rekomendasi perubahan dari sisi bahan bakar (strategi tidak mengubah konsumsi per generasi) |

## 5. Ringkasan satu layar

- Bahan bakar agregat berulang **≥228 generasi/hari terukur** lawan appetite maksimal **45/hari** → surplus ±5×; stok sekali pakai DashScope menambah **±982 rb token claim-grade (±150–218 generasi, hangus 2026-11-12)** + ±10 jt token drill-grade bertingkat sampai 2027-02-01.
- Titik tipis nyata cuma dua: **OpenRouter 50 request/hari tanpa slack** dan **kolam neuron Cloudflare bila klaim + serve sama-sama maksimal (±53 generasi gabungan)**.
- Membuka daily limit ke ∞ **aman dari sisi bahan bakar**; membuka konkurensi **tidak membeli apa-apa dan menjual reliabilitas** — pisahkan kedua keputusan itu.
- Pengikat hasil sesudah pelonggaran bukan bahan bakar: pasokan pertanyaan, serialitas siklus, tangga internal, dan rem REL-005.
