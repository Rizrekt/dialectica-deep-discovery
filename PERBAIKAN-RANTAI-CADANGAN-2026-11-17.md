# PERBAIKAN RANTAI CADANGAN PENULIS (R1) — 2026-11-17

Revisi persiapan R1, disetujui user 2026-11-17 08:36 + intel katalog Vyce 08:38 (screenshot user). Fase testing: nol serve live/submit/klaim. Semua angka di bawah terukur sesi ini.

## 1. Cacat → perbaikan

**Sebelum** (`vyce_provider.py`, rantai model satu-provider):

```python
for m in ("glm-5.3-flash", "deepseek-v4.1"):
```

deepseek-v4.1 mati definitif (HTTP 403 "requires lite tier or higher"). Akibat terbukti: generasi target 3dd05619 mati total (GLM kosong → fallback deepseek 403 → rc=1). GLM kolaps stokastik ±1/3 percobaan malam 17 Nov.

**Sesudah:**

- `vyce_provider.candidate_models()` — deepseek-v4.1 DIBUANG; rantai bawaan tinggal `["glm-5.3-flash"]` (jujur: satu model hidup). Ditambah `VYCE_MODEL_CHAIN` (daftar persis, koma) untuk memaksa rantai tertentu; `VYCE_MODEL` tetap didahulukan bila tak ada chain.
- `vyce_serve_common.WriterFallback` — rantai penulis ANTAR-provider di jalur serve, stateful per pipeline (regenerasi tetap di lane yang selamat, tidak membakar ulang kegagalan primer):

```
vyce (GLM 5.3 Flash) → vyce gpt-oss-120b → cloudflare gpt-oss
```

## 2. Titik pasang + pemicu

- Titik pasang: `vyce_serve_common.vyce_pipeline` — membungkus generator produksi (dan setiap pemanggilan yang menyuntik `fallback_fns`); generator suntikan tes tanpa `fallback_fns` dipakai telanjang persis seperti sebelumnya. Kedua pintu serve (prepare + provider fallback live) lewat pipeline ini, jadi keduanya tercover.
- Pemicu: kegagalan TOTAL primer (pengecualian sesudah retry internal provider: kosong/error/403/timeout). Setiap perpindahan tercatat di stderr: `fallback: <lane> gagal → <lane> (<sebab>)`.
- Jatuhan 1 (Vyce gpt-oss): lewat mesin provider yang sama persis (`generate_vyce(..., model_chain="gpt-oss-120b")`) — steering, citation_patch, gerbang format semua berlaku; tercatat `lane="vyce-serve"` model `gpt-oss-120b` → **terhitung cap serve**.
- Jatuhan 2 (Cloudflare gpt-oss): `cloudflare_provider.generate(lane="cloudflare-serve", budget_lanes=("cloudflare-gptoss","cloudflare-serve"))` — paritas prompt dirakit di `_generate_cloudflare_gptoss` (kontrak format + steering); tercatat di penghitung §39 + anggaran neuron akun (abort pra-bakar >9.000 neuron oleh providernya sendiri), **bukan** di cap Vyce. Drafnya menghadapi `gate_answer` yang sama persis.
- Flag: `DIALECTICA_WRITER_FALLBACK` bawaan AKTIF; `=0` memulihkan perilaku lama persis (kegagalan Vyce naik, target dilewati).

## 3. Probe katalog (aturan putus intel 08:38)

Katalog `GET /v1/models` Vyce sesi ini = 6 model: `deepseek-v4-flash-lr` (id baru deepseek; label LITE di screenshot — konsisten 403, tetap di luar rantai), `glm-5.3-flash`, `gpt-oss-120b`, `nemotron-3.5-super-vl`, `grok-imagine-2`, `qwen3.8-27b`.

| Probe (call_vyce langsung) | Hasil |
|---|---|
| `gpt-oss-120b` trivial | **HIDUP** — 128 kar, 4,1 dtk, usage 202 token |
| `qwen3.8-27b` trivial ×2 | **KOSONG dua kali** (stream selesai, konten 0 kar, 5,4 + 2,2 dtk) — kandidat BELUM terbukti, TIDAK dipasang; probe ulang wajib sebelum pemakaian apa pun |

## 4. Uji kering nyata (bukti gerbang untuk jatuhan 1)

Driver uji memaksa primer gagal total (monkeypatch di driver — bukan kode produksi: panggilan tanpa chain → `VyceGenerationError` simulasi; panggilan ber-chain diteruskan ke fungsi asli), lalu `vyce_serve_prepare.prepare_row` atas target live dari tarikan target_picker (60 baris; kandidat core-topic viso-0 pertama), liveness live, C5 armed shadow, cache ke direktori sementara — berhenti di prepare, nol klaim/submit.

- Target: ISR `dfbe5197-a447-4148-8848-810ee8bcc62b` — rc=0 dalam 101,5 dtk, percobaan pertama langsung berhasil.
- Log perpindahan persis: `fallback: vyce gagal → vyce gpt-oss-120b (VyceGenerationError: SIMULASI R1: GLM gagal total (dipaksa driver uji kering))`.
- Draf: **5.386 kar final** (5.445 kar mentah sebelum citation_patch) — **lolos gerbang serve penuh (sendable)**, tercatat di token-usage sebagai model `gpt-oss-120b`, lane `vyce-serve`.
- C5 shadow atas draf ini: performed ✓, available ✓, checker `openrouter-nemotron`, verdict akhir **clean** (vonis mentah model "fatal", 1 temuan gugur pada verifikasi kutipan — mesin verifikasi bekerja sebagaimana dirancang; shadow tidak memblokir).
- Artefak: `provider/r1-fallback-drytest-2026-11-17.json` + `provider/r1-fallback-drytest-2026-11-17-draft.txt`.

**Aturan putus terpenuhi untuk jatuhan 1** (probe hidup + draf nyata lolos gerbang lewat jalur fallback) → rantai terpasang = Vyce gpt-oss dulu (satu provider, lebih sederhana), Cloudflare gpt-oss kedua (terbukti lebih dulu oleh §39 + PERBAIKAN-PENGHAMBAT langkah 2: 8.032 kar, gerbang OK).

## 5. Panggilan per lane + bahan bakar

| Lane | Panggilan | Hasil / biaya |
|---|---|---|
| Vyce direct (probe, tak tercatat token-usage) | katalog 1×; gpt-oss trivial 1×; qwen trivial 2× | gpt-oss OK; qwen 2× kosong |
| Vyce serve (lane `vyce-serve`) | 1 generasi (gpt-oss, jatuhan 1) | cap serve hari-UTC: **0/10 → 1/10**; kegagalan primer SIMULASI → 0 panggilan GLM nyata, 0 cap terbakar untuk kegagalan |
| Cloudflare | 0 generasi | neuron **0** terpakai tugas ini (saldo hari berjalan 2.535,9 n = sisa pemakaian kalibrasi item-3, tak berubah); plafon tugas 600 n tak tersentuh |
| OpenRouter (pemeriksa C5 shadow) | 1× atas draf kering | available, verdict clean |
| Klien trued | tarikan opportunities 60 baris (percobaan gabungan pertama timeout jaringan, tarikan terpisah berhasil percobaan 1) + fetch detail liveness 1 kandidat | — |

## 6. Tes

- Baru: `provider/test_writer_fallback.py` — **11/11** (candidate_models tanpa deepseek + chain pin; rantai: primer OK tak menyentuh cadangan, primer gagal → prompt sama ke cadangan + log perpindahan, regenerasi menetap di lane selamat, dua jatuhan berurutan, semua gagal → error terakhir naik; pipeline: draf cadangan mock lolos gerbang asli, flag=0 → perilaku lama).
- Suite penuh provider: **281/281 hijau** (basis 270 + 11 baru; test_openrouter_wrapper 30 PASS "GAGAL: tidak ada", sisanya ALL PASS per berkas).
- Backup: `vyce_provider.py.bak-20261117-r1`, `vyce_serve_common.py.bak-20261117-r1`.
- Grep akhir: tak ada lagi rute deepseek hidup di generasi provider mana pun; sebutan deepseek yang tersisa di `serve_gate.py` = komentar/docstring historis lane PEMERIKSA (rute hidupnya Nemotron, bukan deepseek) — di luar cakupan generasi, tidak diubah.

## 7. Sisa risiko

1. **gpt-oss-120b di Vyce berlabel PROMO $0.00** — promo bisa berakhir / model bisa naik tier seperti deepseek; jatuhan 2 (Cloudflare) menutup persis risiko ini, dan rantai kini tak lagi menyembunyikan model mati.
2. **Pemicu hanya kegagalan total** — GLM yang lambat-tapi-hidup tidak memicu fallback; batasnya `GEN_TIMEOUT_S` 1200 dtk di generate_vyce.
3. **Kegagalan primer yang SIMULASI** — yang terbukti sesi ini: mekanisme perpindahan + generasi jatuhan nyata + gerbang nyata. Spesimen kolaps GLM alami ujung-ke-ujung menunggu hari pilot live (mode gagalnya sendiri sudah terbukti ada: insiden 3dd05619).
4. **Qwen 3.8 27B** — 2× kosong; jangan pasang tanpa probe ulang + bukti draf gerbang.
5. **Akuntansi cap asimetris** — jatuhan Cloudflare tercatat di penghitung §39/neuron, bukan cap Vyce; pada hari pilot, total generasi serve = cap Vyce (maks 10) + jatuhan Cloudflare (terikat anggaran neuron + penghitung §39). Dinyatakan apa adanya, bukan disembunyikan.
6. Draf jatuhan Cloudflare tidak melewati citation_patch (sama seperti desain lane §39) — ia langsung menghadapi `gate_answer`; standar gerbangnya identik, langkah hulunya berbeda.
