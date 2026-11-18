# Audit client resmi Dialectica — trued.py v0.22.4 (2026-11-08)

Sumber: tarball resmi https://dialectica.xyz/skills/dialectica.tar.gz (132.524 byte), dibongkar di skill-audit/pkg/ — AUDIT STATIS, belum pernah dijalankan.
Isi paket persis 6 file: LICENSE, SKILL.md, references/{api,arenas,rules-of-the-game}.md, scripts/trued.py. Tidak ada file lain, tidak ada biner.

## Temuan

- **trued.py: 6.369 baris, Python stdlib murni.** Impor hanya: argparse, atexit, collections, http.client, datetime, email.utils, json, os, re, shutil, signal, subprocess, sys, threading, time, urllib. Tidak ada package pihak ketiga.
- **Host jaringan di kode hanya dialectica.xyz** (base API, bisa dioverride DIALECTICA_BASE_URL, wajib https; handler redirect MEMBUANG header X-Active-Session/Authorization saat redirect lintas origin). Host lain (code.claude.com, developers.openai.com, github.com) cuma tautan dokumentasi di komentar.
- **Kata "gemini"/"openrouter" = 0 kemunculan di client.** Client TIDAK punya integrasi LLM bawaan selain dua provider CLI: `claude` dan `codex`. Model penjawab sepenuhnya urusan operator lewat DIALECTICA_PROVIDER_CMD (kontrak: prompt di stdin → jawaban di stdout; dijalankan list-args, shell=False).
- **Kredensial dua lapis:** (1) token sesi akun di ~/.dialectica/session (header X-Active-Session, umur ±7 hari, dari halaman /connect-agent); (2) kredensial kerja Expert di ~/.dialectica/agent.json — menurut desain client, cakupannya cuma cari kerja / ambil kerja / baca job sendiri; tidak bisa belanja saldo, tidak bisa ubah setting. Cakupan ini properti SERVER (client "bertanya, bukan mengasumsikan") — tidak bisa dibuktikan dari kode client saja.
- **Provider `claude` dikeraskan dari argv:** --strict-mcp-config (MCP server operator mati), --setting-sources "" (settings operator mati), tools default HANYA WebSearch + WebFetch. Kode mendokumentasikan insiden nyata: deny-list basi pernah membiarkan Question orang membaca file kredensial dari disk operator — diganti --tools "" untuk kasus kosong.
- **serve:** polling kerja (interval default 5 mnt, lantai 30 dtk), patuh 429 (retry_after_ms dibaca persis), satu serve per kredensial (file lock ~/.dialectica/serve.lock), job yang sudah diambil WAJIB diselesaikan (ditinggal = reliability turun). Cap bawaan Expert dari skill: maxIsrs24h=20; bisa diturunkan (agent caps).
- **Strategi `dynamic`:** platform TIDAK mengirim kerja sama sekali; sesi serve sendiri yang mencari (opportunities) + mengklaim. Push hanya untuk strategi lain.
- **Aturan main terverifikasi dari references:** Pioneer = jawaban terverifikasi pertama (reward terbesar); jawaban berikutnya hanya dibayar bila lolos Surprise Gauge (novel); jawaban falsified memotong Expertise/RAR; nanya unik +1 TRUED; fee nanya pertama gratis lalu naik ke plafon 10 (n=14 → 5,0). Dilarang menjawab Question sendiri / memverifikasi jawaban sendiri (cek di level user pemilik).

## Keputusan arsitektur (versi kita)

- Provider = **wrapper Gemini buatan sendiri** (provider/gemini_provider.py): stdin→Gemini API→stdout, grounding Google Search, backoff 20/45/90 dtk untuk 429/503, fallback model berantai. Wrapper TIDAK punya akses file/shell — lebih sempit daripada provider claude/codex bawaan. Claude Code (berbayar) tidak dipakai.
- Kredensial masuk lewat **Secure Vault** (bukan paste chat): token Dialectica diregistrasi sebagai kredensial API (header X-Active-Session, host dialectica.xyz) dan key Gemini sebagai kredensial API (header x-goog-api-key, host generativelanguage.googleapis.com). File ~/.dialectica/session nantinya berisi SURROGATE hsurr: yang ditukar runtime di egress — pola yang sama dengan connector Exa yang sudah jalan. Wajib dites read-only (whoami/status) sebelum signin.
- Serve pertama = smoke test cap ketat (maxIsrs24h kecil), bukan 24/7. Gas final tetap persetujuan user.

## Risiko sisa (jujur)

- Perilaku server tidak bisa dibuktikan dari kode client (cakupan kredensial kerja, rate reward aktual, jadwal konversi token).
- Skill upstream bisa berubah versi → audit ulang wajib setiap VERSION berubah.
- $TRUED tetap poin internal tanpa harga/pool terdanai (vonis BREAKDOWN.md tidak berubah): setup ini murah dan terukur, bukan bukti worth grind jangka panjang.

## Vonis

**LOLOS audit statis** untuk dipakai dengan batasan di atas: stdlib-only, host tunggal, desain kredensial masuk akal, provider bisa diganti wrapper sempit buatan sendiri.
