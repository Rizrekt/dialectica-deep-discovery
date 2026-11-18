# Dialectica (dialectica.xyz) — BREAKDOWN 2026-11-08

Sumber: situs + wiki proyek (via Exa), dokumen skill resmi proyek (dibaca sebagai DATA via mirror 360 skillhub — TIDAK diunduh/diinstall/dijalankan), LinkedIn tim, blog Tinkering Society (Feb 2026), EZbot research.py (fetch langsung gagal: destination rejected — situs berat JS/anti-bot untuk fetcher polos). TIDAK ada eksekusi apa pun.

## Apa ini
- Marketplace pengetahuan terverifikasi adversarial: user/Agent mengajukan Question → Expert (model AI) menjawab → Verifier independen mencoba memalsifikasi → jawaban yang lolos = Verified Answer.
- Klaim proyek: skor 50,4% di Humanity's Last Exam (13% di atas model frontier terbaik) — klaim marketing proyek, tidak diverifikasi independen di riset ini.
- Produk LIVE: wiki publik berisi Q&A terverifikasi; leaderboard jalan (agent internal "Dialectica (Innovator/Late Entry/Endgame)" di ±30–34 rb poin); halaman baca publik tanpa akun.
- Varian desain lama (blog Feb 2026): pasar klaim True/False dengan wager + challenge bounty, "unaudited alpha on Base".

## Ekonomi $TRUED (dari dokumen skill resmi proyek)
- $TRUED = mata uang internal platform: didapat Expert bila Answer-nya lolos verifikasi; ada juga satuan RAR + Expertise (status: `Balance: $TRUED | RAR | Expertise`).
- Bertanya TIDAK gratis selamanya: Question pertama gratis, berikutnya kena Fee $TRUED naik mengikuti rumus 10 × (n−1)³ / ((n−1)³ + 13³), plafon ±10 TRUED. Bertanya juga menghasilkan: +1 TRUED per Question unik, +1 per Answer lolos.
- Kanal airdrop Telegram (BUKAN resmi, 30 Okt 2026): "+10 TRUED per AI verified answer (unlimited)", "TRUED akan dikonversi ke token sesudah launch", distribusi TBA.
- Dokumen skill menyebut withdraw $TRUED on-chain sebagai fitur yang ada ("if the user has withdrawn $TRUED on-chain") — tapi riset ini TIDAK menemukan: alamat kontrak token, listing DEX, harga pasar, total supply, rate konversi poin→token, atau tanggal TGE. Token "TRUE" di Uniswap Base = proyek LAIN (prediction market "True") — jangan tertukar.
- Pool reward terdanai yang diumumkan untuk earner: TIDAK ADA yang ditemukan.

## Jalur partisipasi (dari post user + dokumen proyek)
1. Signup email di dialectica.xyz/agents.
2. Verify X tweet (sisi user; akun X user semuanya BARU).
3. Create Agent & connect API key LLM (Google/OpenRouter free tier) — agent menjawab pakai MODEL & KUOTA API MILIK PENDAFTAR. Biaya riil partisipasi = konsumsi inference sendiri (bisa $0 bila free tier cukup).
4. Mode Expert: client `trued serve` polling tugas; earning masuk saat Answer terverifikasi; caps bisa diatur (max pertanyaan/24 jam, konkurensi, arena).
- Sesi login ±7 hari, token sesi disimpan lokal di mesin pendaftar. Public read tanpa akun.

## Tim & forensik
- Founder & CEO: Federico Collarte (LinkedIn: sejak Jun 2025, SF & Sydney; profilnya mengklaim pernah raise dari VC besar termasuk Sequoia — KLAIM PROFIL, tidak ada pengumuman funding yang bisa diverifikasi untuk dialectica.xyz).
- "Founder" lain di LinkedIn: Jarred Filmer (sejak Jan 2023 — kemungkinan inkarnasi awal).
- Builder publik: "Young Rug / jiāngshī" (@flostat3, ex-Stacker Ventures) — menyebut Dialectica "hybrid truth and prediction market on Base"; pernah menawarkan pot 1000 USDC untuk kontributor awal (klaim Twitter Score, bukan sumber resmi).
- Perusahaan: LinkedIn company 1–10 karyawan. TIDAK ada catatan funding di RootData/Crunchbase yang ditemukan.
- Nama "Dialectica" bertabrakan dengan perusahaan expert-network besar yang TIDAK berhubungan (dialectica.io, berdiri 2015, Athena/London) — sumber kebisingan riset, bukan afiliasi.
- Status keamanan: alpha, kontrak TIDAK diaudit (pengakuan blog proyek sendiri).

## Risiko
- Nilai $TRUED belum terbukti: tanpa harga pasar, tanpa rate konversi resmi, tanpa tanggal TGE → per yardstick user ini JANJI, bukan pool terdanai.
- Biaya partisipasi nyata = kuota API LLM pendaftar. Bila ikut: WAJIB API key free-tier BARU tanpa metode pembayaran terlampir — jangan pernah key utama. Key di-connect ke platform mereka = kredensial keluar ke pihak ketiga.
- Skill/client resmi proyek meminta agent mengunduh & menjalankan kode mereka — bila suatu saat dijalankan di VM ini, WAJIB audit kode penuh dulu (aturan skill user).
- Sybil/multi-akun: belum dibaca dari rules resmi (belum diambil); jangan asumsi aman multi-akun.

## Addendum 2026-11-08 18:33 — akun jadi + prompt channel dievaluasi
- **User SUDAH daftar sendiri + verifikasi X selesai** (screenshot dashboard): username **rizrekt**, halaman My Agents, saldo **0.0 $TRUED**, belum ada agent. Catatan dashboard: pembuatan Verifier belum dibuka untuk akun ini selama fase launch.
- User mengoper prompt garapan dari channel airdrop (file Prompt_Dialectica_buat_channel.md) dan bertanya perlu atau tidak. **DIEVALUASI SEBAGAI DATA, BUKAN DIIKUTI** — template instruksi pihak ketiga, pola yang sama dengan template komunitas vAPI/$AGI yang selalu ditolak sebagai otoritas. Dua langkahnya melanggar aturan keamanan kita: user disuruh **paste agent token + API key ke chat** (kredensial tidak pernah lewat chat — selalu secure flow).
- Data baru dari prompt itu (KLAIM CHANNEL, belum terverifikasi ke sumber resmi): tabel reward — Pioneer (jawaban terverifikasi pertama) **+20**, jawaban novel terverifikasi **+10**, menang Marathon **+10**, verifikasi **+0,1 s.d. ±1,4**, nanya unik **+1**, jawaban terbukti salah **−1**; $TRUED = poin internal leaderboard, **export on-chain BELUM tersedia**; tidak ada referral; follower X proyek ±140.
- Rekon browser halaman publik (selesai 18:32, sebelum user selesai daftar): tidak ada label/deadline/cap "Early Access" yang terlihat publik; sign-in via magic link email / wallet / Google / X / LinkedIn / GitHub (tanpa password). FAQ resmi (/why): menjawab & verifikasi GRATIS; **bertanya** bisa kena Usage Fee (bayar kartu/Apple Pay/Google Pay/kredit OpenRouter/$TRUED); agent bawaan Dialectica gratis tapi rate-limited; connect agent sendiri resmi didukung. Form create agent + API key hanya terlihat sesudah login.
- Langkah tersisa versi kita sendiri: (1) buat agent pertama dari dashboard user; (2) API key Gemini free-tier dibuat user, masuk lewat Secure Vault; (3) client resmi hanya dipakai SESUDAH audit kode sendiri; (4) serve mulai dari smoke test cap ketat untuk mengukur rate lolos verifikasi + konsumsi kuota, bukan langsung 24/7.

## Addendum 2026-11-08 ±18:40 — audit client LOLOS + setup disiapkan
- User menyetujui "siapin setup agent-nya" (18:34). **Audit statis trued.py v0.22.4 LOLOS** — detail di AUDIT-CLIENT.md: 6.369 baris stdlib murni, host jaringan tunggal dialectica.xyz, nol integrasi Gemini/OpenRouter di client, provider cuma CLI `claude`/`codex` atau DIALECTICA_PROVIDER_CMD bebas. `trued signin` idempotent & memastikan Expert ada (pembuatan agent = server-side lewat client, BUKAN tombol dashboard).
- **Wrapper Gemini buatan sendiri SELESAI** (provider/gemini_provider.py, lolos py_compile): kontrak stdin→stdout, grounding Google Search, backoff 20/45/90 dtk, fallback model berantai, tanpa akses file/shell sama sekali.
- Kredensial diminta lewat Secure Vault sebagai connector custom.google-gemini (header x-goog-api-key) + custom.dialectica (header X-Active-Session) — file sesi nanti berisi surrogate yang ditukar di egress (pola Exa), wajib tes read-only whoami/status sebelum signin.
- Status: MENUNGGU user memasukkan dua kredensial itu. Serve BELUM jalan; smoke test cap ketat + gas final tetap di user.

## Vonis (doktrin revisi user)
- **DAFTAR = tiket lotre murah yang sah** (satu kali, tanpa gas/wallet; biaya riil cuma waktu + tweet verifikasi sisi user).
- **GRIND HARIAN = BELUM TERBUKTI WORTH**: tidak ada pool terdanai terumumkan, tidak ada harga, tidak ada tanggal. Jangan commit sesi serve rutin sebelum ada data nilai (rate per answer terverifikasi × harga/konversi resmi).
- Pola yang benar: daftar sekarang (posisi awal), pantau pengumuman tokenomics/TGE/rate, nilai ulang saat data muncul.


## ADDENDUM 20:03 WIB — 6 ITEM SEMUA ABANDONED, TRANSPORT TERBUKTI TIDAK PERNAH TERJADI
Serve diagnostik (izin user, "caps 1"): 3 job dikerjakan, log klien mengklaim terkirim, server: semua abandoned + RAR −6, penalties 6, $TRUED 0. Cap terbukti BUKAN penghitung item (caps 1 → 6 item). ~/.dialectica/matrix tidak berisi SATU PUN room → jawaban tidak pernah ter-deliver sebagai pesan Matrix; "Answer delivered" = klaim lokal klien. Satu item menuntut runtimeContext.image "dind:node-mcp" (eksekusi runtime/Robotics) yang tidak dipunyai provider teks. REL-005 tidak terdokumentasi di notifikasi/changelog/blog (konfirmasi negatif). Serve BERHENTI; syarat serve berikutnya = bukti transport + status item server-side terbaca. Detail: BREAKDOWN-TUJUAN.md §12.
