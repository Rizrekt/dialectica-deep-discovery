# Rancangan Backup Lane Serve — 2026-11-17

> Keputusan user 2026-11-17 02:42 WIB (kata user sendiri): **"jangan pernah bertumpu pada satu model bro, uji model kita buat saling ngebackup, bukan jadi cadangan membusuk."**
> Status: RANCANGAN — klausulnya AKTIF di SISTEM-KENDALI; failover di badan hunt BARU boleh dilipat sesudah tiap lane cadangan LOLOS uji di berkas ini. Mengubah rezim pilot tanpa uji = melanggar keputusan itu sendiri.

## 1. Masalah yang dibunuh keputusan ini

Pilot serve sekarang terkunci GLM: probe GLM merah (P3) → serve tidak dinyalakan (kejadian 16 Nov 15:00 + 17:00, insiden §122/§123). Satu model mati = satu hari earning mati. Itu persis pola "bertumpu pada satu model" yang dilarang user.

## 2. Kandidat lane cadangan serve (dari tangga yang sudah ada)

| Lane cadangan | Jalur | Bukti hidup terakhir | Status uji serve |
|---|---|---|---|
| deepseek-v4.1 | Vyce (VYCE_MODEL) | 16 Nov: fallback menjawab tapi 503 ×5 di router | BELUM uji serve |
| nemotron-3.5-super-vl | Vyce (VYCE_MODEL) | 14 Nov probe OK 7,0 dtk; mode NORMAL-NEMOTRON historis buat klaim | BELUM uji serve |
| gpt-oss-120b | Cloudflare (§39, unit dialectica-serve = cadangan) | neuron 0 terpakai 3 hari (tangki penuh); generasi CF terbukti di klaim/drill | BELUM uji serve tergating |
| glm-4.7-flash | Z.ai (answer-only §40) | hidup 16 Nov (18 token, 45 dtk) | answer-only — BUKAN kandidat serve tanpa ubah rezim |

## 3. Definisi "cadangan teruji" (anti-membusuk)

Sebuah lane baru boleh disebut cadangan serve bila SEMUA ini hijau dan BERTANGGAL:

1. **Probe hidup** — rc=0, jawaban nyata, dicatat di readiness harian (06:30). Probe harian = mekanisme anti-busuk: cadangan diuji TIAP HARI, bukan pas dibutuhkan.
2. **Satu generasi uji lewat pipa serve asli** (prepare-hook + gerbang format v2 + cap kode) atas prompt drill — bukan prompt produksi; keluaran lolos `sendable` dan dibaca manusia sekali.
3. **Latensi terukur** dalam batas jendela (generasi serve ±< 15 menit/job).
4. Sesudah lolos: nama lane + tanggal lolos ditulis di berkas ini + badan hunt; failover hanya ke lane yang ada di daftar lolos.

## 4. Aturan failover (rancangan, berlaku sesudah §3 terpenuhi ≥1 lane)

- Di jendela hunt: probe GLM gagal → probe lane cadangan teruji berikutnya (urutan §2) → yang hijau pertama menyalakan serve pilot dengan cap + kill-metric yang SAMA.
- Semua lane mati → serve tidak nyala + insiden naik (aturan lama tetap).
- Kill-metric TIDAK berubah per lane: falsified pertama di bawah gerbang = serve OFF total, lane apa pun.

## 5. Langkah kerja

1. Readiness 06:30 17 Nov: probe SEMUA kandidat §2 (bukan cuma GLM) — hasil = tabel hidup/mati pertama rezim baru.
2. Generasi uji pipa serve (butir §3.2) untuk kandidat yang hidup — dikerjakan sesi kolom/lab, BUKAN di jendela hunt produksi.
3. Lane lolos → lipat failover §4 ke badan `dialectica-slot-hunt` + verifikasi baca-balik (wilayah perubahan rezim: laporkan ke user sebelum/sesudah sesuai klausul konfirmasi yang berlaku).
4. C5 (cek semantik) tetap lubang terpisah — failover TIDAK menutup C5.

## 6. TABEL PROBE PERTAMA REZIM BARU — 2026-11-17 02:44–02:45 WIB (dijalankan SEKARANG atas tantangan user "besok pagi kenapa bro?")

Probe via vyce_provider (prompt "Reply with exactly: OK"), hasil:

| Model | Hasil | Latensi |
|---|---|---|
| glm-5.3-flash | rc=0 "OK" | 3,4 dtk |
| deepseek-v4.1 | rc=0 "OK" (langsung, bukan fallback) | 4,9 dtk |
| nemotron-3.5-super-vl | rc=0 "OK" | 4,5 dtk |

- **Kaki GLM insiden §122/§123 TERBUKTI PULIH di level probe malam ini** (sesudah gagal 3 jendela beruntun kemarin sore).
- Status uji serve (§3): ketiganya baru lolos butir 1 (probe). Butir 2 (generasi uji lewat pipa serve) + butir 3 (latensi generasi) BELUM — belum ada lane yang sah disebut cadangan serve.
- Cloudflare gpt-oss belum diprobe malam ini (jalur §39 terpisah; readiness 06:30 tetap mencakup neuron + lane itu).

## 7. KOREKSI 2026-11-17 05:07 (dari PERBAIKAN-PENGHAMBAT langkah 2) — MEMBATALKAN §6 untuk deepseek

Deepseek-v4.1 via Vyce = **MATI definitif**: panggilan langsung membalas HTTP 403 "This model requires lite tier or higher". Probe §6 sesi utama 02:44 yang membacanya rc=0 hampir pasti mengukur provider/kandidat pertama (GLM), bukan model deepseek itu sendiri — bacaan "deepseek HIDUP" di §6 TIDAK SAH. Penulis cadangan yang terbukti layak = **Cloudflare gpt-oss-120b** (8.032 kar, gerbang OK; tertahan hanya oleh lantai K-2 0,30 pada rasio 0,238 — pada ambang usulan 0,15 ia lolos; U2 tetap wilayah keputusan). Nemotron = cadangan pemeriksa terbukti, penulis tidak layak (stub 531 kar).
