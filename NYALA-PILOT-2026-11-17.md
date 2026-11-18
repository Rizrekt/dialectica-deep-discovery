# NYALA PILOT SERVE — Dialectica (2026-11-17)

**Perintah:** kata tegas user 2026-11-17 09:33 WIB — "SIAP NYALA!!!!!" + "ledakkan medan perangnya!" (sesudah Opsi B 09:30: nyala hanya atas kata tegas; kata itu turun di sini).
**Rezim:** PILOT SERVE TERGATING yang sudah disetujui user 2026-11-15 19:20 (PAKET-RESTART-SERVE-2026-11-15 + GERBANG-SERVE-2026-11-15 + CHECKLIST-PILOT-2026-11-16) — bukan rezim baru. Klaim one-shot tetap STOP TOTAL (tidak disentuh tugas ini).
**Hasil satu baris:** pra-cek hijau semua → unit SISTEM terpasang + active 02:35:38 UTC → jendela pertama ±26 menit menghasilkan **4 jawaban terkirim (semua Pioneer viso-0, semua C5-shadow clean)**, 3 draf ditahan lantai K-2, 10 target gugur liveness; cap tutup **8/10**; kill-metric tidak terpicu; serve **tetap jalan** di bawah systemd sesudah jendela pengamatan.

---

## 1. Pra-cek live (semua hijau sebelum start)

**(a) Akun** — `trued.py status` + `agent show` (02:34 UTC):
- Expert **8522c990-d4f6-4155-a326-3c3c9802b950** ✓, nama **AGENT.AkTa** ✓, strategyType **dynamic** ✓, enabled True, state configured — **TIDAK suspended**.
- Saldo **−1,8788 $TRUED**, RAR **118**, Expertise 0 — persis jangkar P4 (tidak ada dent baru sejak bacaan 07:20).
- Caps none/unlimited [used 0]; contextWindowTokens 160.000; maxConcurrency 1; arena general.

**(b) Cap serve hari ini (UTC)** — dihitung dari `provider/token-usage.jsonl` + fungsi penegak kode `vyce_serve_common.serve_generations_today()`:
- Lane `vyce-serve` (satu-satunya yang dihitung cap pilot Vyce): **1/10** → **sisa 9** saat start. Satu-satunya record = generasi uji kering R1 01:44:43 UTC (gpt-oss-120b).
- Lane `cloudflare-serve` (§39, cadangan mati): 0. Record `cloudflare-gptoss` hari ini (14) = lane klaim/kalibrasi pemeriksa, BUKAN serve — tidak masuk penghitung cap serve.
- Klarifikasi: angka "6/10" di dokumen P12/K7 = tally generasi uji lintas lane sesi utama, bukan penghitung cap; yang mengikat = penghitung kode di atas.

**(c) Config serve** (terverifikasi di kode, bukan dari dokumen):
- `run_serve.py` mode serve Vyce meng-arm `DIALECTICA_SERVE_GATE_FETCH=1` (liveness) + `DIALECTICA_SEMANTIC_CHECK=1` (C5). `DIALECTICA_SEMANTIC_MODE` tidak di-set di unit maupun /etc/environment → bawaan **SHADOW** (keputusan user 06:12 utuh; TIDAK block).
- Konteks kebaruan aktif di dalam tahap semantik serve_gate (blok tahan-potong R3).
- Writer fallback R1: `writer_fallback_enabled() = True` (bawaan; rantai GLM → gpt-oss Vyce → gpt-oss Cloudflare).
- Lantai per-kelas aktif di `openrouter_wrapper.py`: PIONEER 1.717 / GENERAL+INNOVATOR 3.000 / MARATHON 4.500 / tanpa kelas 4.500; **K-2 = 0,30** (`FLOOR_MIN_BOUND_RATIO` baris 410, tidak diubah).
- `citation_patch` = v2 (penanda terverifikasi di `provider/lib/citation_patch.py`); `SERVE_FORMAT_CONTRACT` ada di serve_gate.
- Checklist P1 (E3 di serve_gate + suite) = warisan fase testing tuntas 372/372; P3 probe Vyce GLM di jendela ini: **lolos, rc=0, 15,0 dtk**, model glm-5.3-flash (probe langsung tanpa lane serve — tidak membakar cap).

**(d) systemd:** `--user` mati terverifikasi ("Failed to connect to bus"); systemd sistem = running → unit dipasang sebagai unit SISTEM (sesuai catatan utang F2).

## 2. Bukti start

- `cp provider/dialectica-serve.service /etc/systemd/system/` + `daemon-reload` + `enable` (symlink multi-user.target.wants dibuat) + `start`.
- `systemctl is-active` = **active**, `is-enabled` = **enabled**, sejak **Tue 2026-11-17 02:35:38 UTC**, MainPID **41340** (`run_serve.py … q=wallet`), anak 41344 (`trued.py serve --every 1m arenaIds=general questionMaxAgeMs=259200000 q=wallet`) — lane **Vyce tergating** (tanpa flag `--cloudflare-serve`).
- Log awal (`provider/serve-2026-11-17.log`) bersih: "gated Vyce serve — prepare/ready hooks + serve gate armed (liveness, wrapper, thinking-trace, semantik C5 … default shadow)" → "launching trued serve provider=vyce every=1m" → "Reusing agent 8522c990-d4f6-4155-a326-3c3c9802b950".
- Restart=on-failure + RestartPreventExitStatus=6 (cap-reached tidak bangkit lagi) sesuai file unit.

## 3. Jurnal jendela pertama (02:35:38–03:01 UTC, ±26 menit, terawasi penuh)

Serve memindai tiap 1 menit (q=wallet, arena general, umur maks 3 hari), mencoba s/d 3 target per putaran. 17 target disaring:

**TERKIRIM (4)** — semua lolos liveness + gerbang penuh, status "awaiting validation":

| # | ISR | Job | Kar | Kelas | Penulis | C5 shadow |
|---|-----|-----|-----|-------|---------|-----------|
| 1 | 2777178d-2294-4303-9b94-e877fdac95d0 | cb8a6b41-eeff-4b66-a2b9-6fd0af2017cf | 6.673 | PIONEER (viso 0) | glm-5.3-flash | clean (02:37:18Z) |
| 2 | d94d7e34-01e1-44ef-9666-b0616980bc93 | 995107bc-79ea-4716-b472-1a771d17b1d2 | 7.570 | PIONEER (viso 0) | glm-5.3-flash | clean (02:41:31Z) |
| 3 | 635a010d-fa76-42a3-8ddf-c592e5189637 | 51db68f5-6401-4747-bd9e-ac671fe2053e | 6.964 | PIONEER (viso 0) | glm-5.3-flash | clean (02:47:06Z) |
| 4 | d21135d5-5d4e-4a54-9da1-c54b4fc466f8 | 32ba73d2-e225-4892-a7ef-c25f277b675f | 8.088 | PIONEER (viso 0) | glm-5.3-flash | clean (02:58:51Z) |

**DITAHAN GERBANG (3)** — draf ditahan utuh oleh lantai K-2 (rasio angka terikat < 0,30), pass-over, tidak terkirim:
- 45cb9a4a-7851-426d-9ad7-6c553dfa2ddb — rasio **0,000** (0/6 token); penulis GLM; C5 shadow juga **fatal** (konvergen).
- b3f1fcc3-c8bd-49b7-9270-bfc07aa7a104 — rasio **0,048** (3/62); penulis tercatat gpt-oss-120b.
- 87d16e0a-16d7-46be-ae4e-bacf37104b35 — rasio **0,111** (6/54); penulis tercatat gpt-oss-120b; C5 shadow **fatal**.

**GUGUR LIVENESS (10)** — pola flag basi §82 (semua endsAt ronde lewat), pass-over di prepare, **0 generasi terbakar**: 3e6c5c64, fcbdf0a3, 1d3be0c0 (target yang pagi ini terklasifikasi MARATHON oleh pemilih — rondenya berakhir 02:34:12Z, tepat sebelum nyala; konsisten), 7b02512e, baa4f0f2, 5df44416, e1e035e5, 2bd7b6c9, 74bf3d91, 7cdb4d7b.

**Cap berjalan:** 1/10 (awal) → 8/10 (tutup jendela): 7 generasi jendela (4 terkirim + 3 tertahan), semua tercatat lane `vyce-serve` di token-usage.jsonl. Penulis: GLM ×5, gpt-oss-120b ×2 (dua draf tertahan terakhir — konsisten dengan jatuhan WriterFallback R1 sesudah kegagalan total GLM di dalam proses prepare yang sama; baris log "fallback:" TIDAK tertangkap di log serve — stderr hook tampaknya tidak diteruskan trued ke log ini; dinyatakan terbuka, bukan diklaim).
**Platform:** 3× HTTP 429 M_LIMIT_EXCEEDED dari Dialectica — serve mematuhi perintah lambat (tunggu 5 dtk) tiap kali; bukan batas provider kita.
**Kill-metric:** TIDAK terpicu — 0 falsified (verdict keempat jawaban masih pending), 0 draf tertahan oleh lapis trace/E3 (yang tertahan murni lantai K-2, dan tidak memenuhi pola "2 berturut trace/E3").
**Bukti 4 permukaan (checklist C):** log serve memuat baris generasi + submit ✓; proses hidup (MainPID 41340 + anak trued, `is-active` active di tutup jendela) ✓; token-usage mencatat generasi serve hari ini ✓; jobs endpoint — jumlah job server belum dibaca ulang di tugas ini (bukti submit = baris "submitted for … awaiting validation" di log klien + cache); dinyatakan terbuka di §5.

## 4. Bahan spot-check (item 7)

`~/workspace/research/dialectica/PILOT-SPOTCHECK-2026-11-17/` — indeks `00-INDEKS.md` + per jawaban: teks jawaban persis terkirim (dari serve-cache) + konteks pertanyaan:
- `01-2777178d-jawaban.txt` / `01-2777178d-pertanyaan.txt`
- `02-d94d7e34-jawaban.txt` / `02-d94d7e34-pertanyaan.txt`
- `03-635a010d-jawaban.txt` / `03-635a010d-pertanyaan.txt`

Pemeriksaan manualnya sendiri (checklist D) = langkah sesi utama/user berikutnya; tugas ini hanya menyiapkan bahannya.

## 5. Sisa risiko / terbuka

1. **Verdict belum mendarat** — keempat jawaban "awaiting validation"; verdict bisa tiba jam-jaman sesudah submit. Falsified pertama di bawah gerbang = serve OFF di giliran yang sama + JEDA (kill-metric paket) — kewajiban verdict-watch sesi utama berikutnya, bukan tugas ini.
2. **Serve jalan terus di bawah systemd** sesudah jendela pengamatan (Restart=on-failure), dengan sisa cap hari ini **2/10** — generasi berikutnya hari ini maksimal 2 lagi sebelum cap kode menolak; cap reset 00:00 UTC.
3. **Laju tahan K-2 tinggi di jendela ini**: 3 dari 7 draf tertahan (semua karena angka tak terikat sitasi) — pola yang sama dengan temuan lama K-2; dua draf gpt-oss tertahan paling rendah rasionya. Bahan bedah sesi utama; TIDAK ada ambang yang diubah tugas ini.
4. **Baris "fallback:" tidak ter-log** di log serve (stderr hook prepare tidak diteruskan) — peralihan penulis hanya terlihat dari kolom model token-usage. Kandidat perbaikan logging terpisah.
5. **Jobs endpoint belum dibaca ulang** untuk bukti permukaan ke-4 checklist C (jumlah job 34 → naik); bukti submit saat ini dari log klien + cache + cap counter.
6. **22 jawaban revealed lama** tetap di luar sana (bom verdict lama, di luar kendali pilot) — saldo bisa bergerak oleh mereka kapan saja; verdict-watch tetap wajib.

## 6. Catatan yang diperbarui

- `SISTEM-KENDALI.md`: klausul C13 (keadaan kini → PILOT LIVE) + blok "NYALA PILOT — 2026-11-17 09:33 WIB" di akhir dokumen (fase, cap awal, id jawaban).
- Berkas ini + `PILOT-SPOTCHECK-2026-11-17/`.
- Yang TIDAK diubah: config Expert/caps/strategi server, cap pilot (10), mode C5 (shadow), ambang K-2 (0,30), status klaim (STOP TOTAL).
