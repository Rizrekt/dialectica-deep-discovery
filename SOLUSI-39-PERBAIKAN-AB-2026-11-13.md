# SOLUSI-39 — PERBAIKAN A+B JALUR SERVE §39 (OFFLINE)

**Tanggal:** 2026-11-13 (WIB) · **Sifat:** perbaikan kode OFFLINE. NOL serve live dinyalakan, NOL job diambil, NOL klaim — STOP TOTAL Dialectica berlaku penuh selama pekerjaan ini.
**Dasar:** SOLUSI-39-AUDIT-KODE-2026-11-13.md §2.3 + §3.2/§5 butir 3, dan SOLUSI-39-GABUNGAN-2026-11-13.md bagian "Yang HARUS dibetulkan SEBELUM live" (A dan B).
**File diubah (3):** `provider/cloudflare_serve_provider.py`, `provider/cloudflare_serve_ready.py`, `provider/test_cloudflare_serve.py`. `cloudflare_serve_common.py` TIDAK diubah — kedua perbaikan memakai mekanisme yang sudah ada di sana (`serve_generations_today()`, `SERVE_CAP`, `PIPELINE_MAX_GENERATIONS`, `read_cache()`).

---

## Perbaikan A — fallback provider cek sisa cap serve

Celah (audit §2.3): `cloudflare_serve_provider.py` tidak pernah memanggil `serve_generations_today()`; satu kedatangan fallback pada hari bercap penuh tetap bisa memulai hingga 2 generasi di atas cap 10.

Perilaku baru: di `main()`, sesudah cek prompt kosong (return 2 dipertahankan) dan SEBELUM `apply_steering`/generasi apa pun, sisa cap dihitung dengan mekanisme yang sama persis dengan prepare (`csc.serve_generations_today()` atas record lane `cloudflare-serve` di `token-usage.jsonl`, hari UTC). Bila `remaining < csc.PIPELINE_MAX_GENERATIONS` (sisa tidak menutup 1 generasi + maks 1 regen) → print alasan ke stderr, **return 1 TANPA generasi**. Bila sisa ≥ 2, fallback berjalan seperti sebelumnya dengan `allow_regen=True` (kini terjamin tertutup sisa). Jalur cache-hit berada SEBELUM gerbang ini dan tidak disentuh sama sekali — ia tidak men-generate apa pun dan tetap melayani cache walau cap penuh (dibuktikan tes).

Diff ringkas (`cloudflare_serve_provider.py`):

```diff
 # docstring modul: + paragraf "The fallback is serve-cap gated
-# (SOLUSI-39 fix A): ... The cache-hit primary path above is not
-# gated: it generates nothing."
@@ def main():
     if not prompt.strip():
         print("cloudflare_serve_provider: empty prompt and no "
               "prepared answer", file=sys.stderr)
         return 2
+    used = csc.serve_generations_today()
+    remaining = csc.SERVE_CAP - used
+    if remaining < csc.PIPELINE_MAX_GENERATIONS:
+        print(f"cloudflare_serve_provider: serve cap gate — "
+              f"{used}/{csc.SERVE_CAP} serve generations used today "
+              f"(UTC), remaining {remaining} cannot cover a full "
+              f"fallback pipeline "
+              f"({csc.PIPELINE_MAX_GENERATIONS} generations). "
+              f"Exiting 1 WITHOUT generating; trued drops the job "
+              f"(MEKANISME §35).", file=sys.stderr)
+        return 1
     full = cp.apply_steering(prompt, isr_id or None) + cp.LENGTH_SUFFIX
```

Catatan keputusan: ambang yang dipakai = sisa harus menutup pipeline PENUH (≥2), sesuai bunyi tugas perbaikan ("bila sisa tidak menutup 1 generasi + maks 1 regen, exit 1"). Berbeda dari prepare — yang pada sisa tepat 1 masih menjalankan pipeline tanpa regen — provider berada SESUDAH job diterima, jadi kegagalan di sini = job dropped (§35); memilih fail-closed penuh (tanpa generasi parsial) adalah perilaku terkecil yang menjamin hitungan tidak pernah melewati cap dari jalur ini.

## Perbaikan B — READY menolak file cache kosong / whitespace-only

Celah (audit §3.2 butir b): `cached_ids()` di common hanya mendaftar nama file `*.txt` tanpa membaca isi — file kosong tetap meloloskan bid, padahal provider akan `read_cache` → None dan terpaksa fallback.

Perilaku baru: di `cloudflare_serve_ready.py`, himpunan id disaring lewat `csc.read_cache()` — semantik yang persis sama dengan yang dipakai provider (`read_cache` mengembalikan None untuk file tidak ada/OSError dan untuk isi kosong/whitespace-only). File kosong/whitespace → id tidak dihitung → tidak ada hit → exit 1 (bid diveto). Isi file valid tidak berubah perilaku.

Diff ringkas (`cloudflare_serve_ready.py`):

```diff
 # docstring modul: + paragraf "An EMPTY or whitespace-only cache
-# file does NOT count as a prepared answer (SOLUSI-39 fix B): ..."
@@ def main():
-    ids = csc.cached_ids()
+    ids = {isr_id for isr_id in csc.cached_ids()
+           if csc.read_cache(isr_id) is not None}
     hit = next((s for s in _strings(payload) if s in ids), None)
```

## Tes — yang ditambah (test_cloudflare_serve.py)

Tidak ada tes lama yang diubah atau disesuaikan: nol konflik dengan perilaku baru (semua 25 cek lama lolos apa adanya). Yang ditambah = **8 cek baru** (suite naik 25 → 33) + pembaruan docstring suite:

Perbaikan A (di `provider_cases`, dunia `ServeWorld` terpisah per skenario):

1. `provider: cache hit at FULL cap -> cached text, exit 0, zero generations (path ungated)` — prefill 10, cache terisi → rc 0, teks cache, `calls == 0`.
2. `provider: cache miss at FULL cap -> exit 1 + empty stdout, zero generations, count stays 10` — prefill 10 → rc 1, stdout kosong, `calls == 0`, hitungan tetap 10.
3. `provider: correction at FULL cap -> exit 1 + empty stdout, zero generations` — job_kind=correction (pemicu fallback kedua) ikut tergerbang.
4. `provider: cache miss with 1 remaining -> exit 1, zero generations, count stays 9` — prefill 9: sisa 1 tidak menutup pipeline penuh → tetap diblokir.
5. `provider: cache miss with 2 remaining -> fallback runs, exit 0` — prefill 8: gerbang tidak menghalangi fallback yang sah.

Perbaikan B (di `ready_cases`, subprocess ke skrip ready asli):

6. `ready: empty cache file -> exit 1 (bid vetoed)` — file cache dibuat via `write_cache(id, "")`.
7. `ready: whitespace-only cache file -> exit 1 (bid vetoed)` — isi `"   \n\t  "`.
8. `ready: prepared id still exit 0 alongside empty files` — id valid tetap lolos di direktori cache yang sama.

---

## Hasil tes VERBATIM

### `python3 test_cloudflare_serve.py` → exit 0

```
PASS  screen: viso-0 core-topic row passes
PASS  screen: viso 3 passed over  viso 3 — bukan pertanyaan viso-0 (Pioneer)
PASS  screen: marathon active passed over  marathonActive — di luar cakupan Pioneer serve
PASS  screen: off-topic passed over  di luar topik inti (identitas/wallet/on-chain/oracle/rollup/keamanan kontrak/token)
PASS  screen: runtime demanded passed over  runtimeContext terisi — menuntut runtime, dilewati
PASS  screen: no id passed over  baris tanpa id/isrId
PASS  screen: no text passed over  baris tanpa judul/konten pertanyaan
PASS  prepare: good row -> exit 0 + answer cached  rc=0 calls=1 line=jawaban siap untuk 60fa9935-4352-4a4c-9aa7-384de037196c (632
PASS  prepare: generation recorded under serve lane  count=1
PASS  prepare: screened-out row -> exit 1, zero generations  rc=1
PASS  prepare: cap reached (10) -> exit 1, zero generations, no job exists to abandon  rc=1
PASS  prepare: 9 used + short draft -> exit 1 after exactly 1 generation (regen disabled at the cap edge)  rc=1 calls=1
PASS  prepare: 8 used + regen -> exit 0, count lands on 10  rc=0 calls=2
PASS  ready: prepared id -> exit 0  rc=0
PASS  ready: unprepared id -> exit 1 (bid vetoed)  rc=1
PASS  ready: empty cache file -> exit 1 (bid vetoed)  rc=1
PASS  ready: whitespace-only cache file -> exit 1 (bid vetoed)  rc=1
PASS  ready: prepared id still exit 0 alongside empty files  rc=0
PASS  provider: cache hit -> cached text, exit 0  rc=0
PASS  provider: correction bypasses cache -> live pipeline  rc=0 calls=1
PASS  provider: cache miss -> live fallback, exit 0  rc=0
PASS  provider: fallback withheld -> exit 1 + empty stdout  rc=1
PASS  provider: cache hit at FULL cap -> cached text, exit 0, zero generations (path ungated)  rc=0 calls=0
PASS  provider: cache miss at FULL cap -> exit 1 + empty stdout, zero generations, count stays 10  rc=1 calls=0
PASS  provider: correction at FULL cap -> exit 1 + empty stdout, zero generations  rc=1 calls=0
PASS  provider: cache miss with 1 remaining -> exit 1, zero generations, count stays 9  rc=1 calls=0
PASS  provider: cache miss with 2 remaining -> fallback runs, exit 0  rc=0 calls=1
PASS  run_serve --cloudflare-serve --dry-run: supervised plan shown, nothing launched  rc=0
PASS  run_serve --cloudflare (plain serve) STILL refused exit 5  rc=5
PASS  run_serve --cloudflare-serve --answer refused exit 5  rc=5
PASS  run_serve --cloudflare-serve at cap -> start refused exit 6, nothing launched  rc=6
PASS  supervisor: cap reached -> child SIGINTed, fast return  rc=-2 elapsed=1.0s
PASS  supervisor: child exit passes through untouched  rc=0

ALL PASS (33/33)
EXIT=0
```

### Regresi `python3 test_cloudflare_claim_path.py` → exit 0

```
PASS  fixture good_text in rubric band  6324 chars
PASS  sendable draft -> exit 0 + wrapped text on stdout  rc=0 stdout=6325 chars
PASS  short draft (GAGAL-LANJUT) -> exit 1 + empty stdout  rc=1 stdout=0 chars
PASS  unpatchable audit finding -> exit 1 + empty stdout + WITHHELD  rc=1 stdout=0 chars
PASS  neuron budget >9000 -> exit 1 + empty stdout + client never invoked  rc=1 stdout=0 chars
PASS  run_serve --cloudflare --dry-run --answer: wiring shown, nothing launched  rc=0
PASS  run_serve --cloudflare (serve) refused with exit 5  rc=5
PASS  serve refusal precedes dry-run on this lane  rc=5

ALL PASS (8/8)
EXIT=0
```

### Regresi `python3 test_openrouter_claim_path.py` → exit 0

```
PASS  fixture good_text in rubric band  6324 chars
PASS  sendable draft -> exit 0 + wrapped text on stdout  rc=0 stdout=6325 chars
PASS  short draft (GAGAL-LANJUT) -> exit 1 + empty stdout  rc=1 stdout=0 chars
PASS  unpatchable audit finding -> exit 1 + empty stdout + WITHHELD  rc=1 stdout=0 chars
PASS  quota <3 -> exit 1 + empty stdout + client never invoked  rc=1 stdout=0 chars
PASS  run_serve --openrouter --dry-run --answer: wiring shown, nothing launched  rc=0
PASS  run_serve --openrouter (serve) refused with exit 5  rc=5
PASS  serve refusal precedes dry-run on this lane  rc=5
PASS  run_serve default (vyce) dry-run wiring unchanged  rc=0
PASS  run_serve --gemini dry-run wiring unchanged  rc=0

ALL PASS (10/10)
EXIT=0
```

### Regresi `python3 test_openrouter_wrapper.py` → exit 0

```
PASS  mojibake r1  markers 247->0, chars 4378->4176
PASS  mojibake r2  markers 110->0, chars 3220->3138
PASS  mojibake r3  markers 176->0, chars 3660->3520
PASS  mojibake r4  markers 185->0, chars 3846->3698
PASS  mojibake r5  markers 193->0, chars 5098->4968
PASS  mojibake teks sah utuh  'Harga naik ±5% — selesai ×2, “kutipan” utuh…'
PASS  audit r1 EIP-2929 cold=100
PASS  audit r1 EIP-2929 700
PASS  audit r1 EIP-3860 bukan DELEGATECALL/CALL
PASS  audit r2 EIP-1167 10 byte
PASS  audit r2 EIP-2028 1 gas/byte
PASS  audit r4 700 gas (EIP-2929)
PASS  audit r5 EIP-3860 surcharge DELEGATECALL  4 temuan
PASS  audit tidak menandai nomor dokumen
PASS  presisi: offset 10-29 bukan klaim ukuran
PASS  presisi: kredit initcode EIP-3860 yang benar lolos
PASS  patch membuang angka salah r1  dibuang: ['700', '100']
PASS  penjaga panjang: regenerasi menyelamatkan  status=OK gen=2
PASS  penjaga panjang: tetap pendek = GAGAL-LANJUT  status=GAGAL-LANJUT
PASS  penjaga panjang: tanpa regen = GAGAL-LANJUT
PASS  rubrik (c) konsisten  ('LOLOS', '4968 karakter (lantai 4500; pita anjuran 4500–8000)')
PASS  rubrik (c) menolak pendek
PASS  lantai: jarak 150 kar -> bound=1  bound=1
PASS  lantai: jarak 151 kar -> bound=0  bound=0
PASS  lantai: draf kaya sitasi lolos semua  url=50 dens=9.434 ratio=1.0
PASS  lantai: wrap_answer kaya -> lantai lolos, (d) LOLOS  floor=True
PASS  lantai: 0 URL -> K-1(a) gagal bernama  failures=['LANTAI K-1(a) jumlah URL: aktual 0 < 1', 'LANTAI K-1(b) kepadatan sitasi: aktual 0.000 per 1.000 kar < 0.5 (0 sitasi dalam 5850 karakter)', 'LANTAI K-2 rasio angka terikat sitasi: aktual 0.000 < 0.3 (0 dari 0 token angka dalam ±150 karakter dari sebuah sitasi)']
PASS  lantai: 0 URL -> temuan FLOOR menahan draf, (d) GAGAL  floor_failures=3
PASS  lantai: rasio rendah -> K-2 gagal bernama + angka aktual  ratio=0.03 bound=6/200
PASS  lantai: sitasi tipis -> hanya K-1(b) gagal  dens=0.158 ratio=1.0

GAGAL: tidak ada
EXIT=0
```

---

## Ringkasan akhir

- **A selesai:** fallback live (cache-miss DAN correction) kini tergerbang cap serve — sisa < 2 generasi → exit 1, nol generasi, hitungan cap tidak bergerak. Cache-hit tidak berubah perilaku (termasuk saat cap penuh).
- **B selesai:** READY kini hanya menghitung id yang lolos `read_cache` — file kosong/whitespace-only diveto (exit 1), konsisten dengan provider.
- **Tes:** serve 33/33 PASS (25 lama utuh + 8 baru); regresi claim-path Cloudflare 8/8, OpenRouter 10/10, wrapper semua PASS (exit 0, "GAGAL: tidak ada"). Nol tes lama perlu disesuaikan.
- **Yang TIDAK disentuh:** catatan C audit (cache tanpa hash/TTL) — tetap mitigasi operasional, bukan bagian tugas ini. STOP TOTAL dan keputusan smoke-live tetap di sesi utama/user; tidak ada serve live yang dinyalakan oleh pekerjaan ini.

*Ditulis 2026-11-13. Artefak eksekusi = suite tes offline di atas (log & cache temp); log/cache produksi tidak tersentuh.*
