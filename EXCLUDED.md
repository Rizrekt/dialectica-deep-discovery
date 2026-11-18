# EXCLUDED — Berkas yang Tidak Terkumpul Utuh / Tidak Terarsip

## 1. Berkas parsial (ukuran > 10 MB) — 18 berkas

Berkas-berkas ini adalah dump JSON respons API platform yang tersimpan sebagai SATU baris JSON raksasa (0 karakter newline), sehingga cuplikan "2.000 baris pertama" tidak dapat diterapkan secara harfiah. Yang terarsip adalah **cuplikan 2.000.000 byte (2 MB) pertama** dari setiap berkas, byte-for-byte dari aslinya (selain redaksi pada butir yang dicatat di REDACTION-LOG.md). Ukuran asli dicatat di bawah dan juga di kolom Redaksi pada MANIFEST.md.

| Path relatif | Ukuran asli (byte) | Yang terarsip |
|---|---|---|
| `belajar-2026-11-14/isos_by_isr.json` | 47.048.234 | cuplikan 2 MB pertama |
| `belajar-2026-11-14/run2-1037/isos_by_isr.json` | 30.925.119 | cuplikan 2 MB pertama |
| `belajar-2026-11-14/run3-1837/isos_by_isr.json` | 17.277.260 | cuplikan 2 MB pertama |
| `belajar-2026-11-14/run4-0237/isos_by_isr.json` | 22.563.230 | cuplikan 2 MB pertama |
| `belajar-2026-11-15/run5-1037/isos_by_isr.json` | 30.439.583 | cuplikan 2 MB pertama |
| `belajar-2026-11-15/run6-1837/isos_by_isr.json` | 38.422.622 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run7-0237/isos_by_isr.json` | 54.625.798 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run7-0237/isrs.json` | 11.029.622 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run8-1037/isrs.json` | 11.676.634 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run8-1037/isos_by_isr.json` | 58.937.788 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run9-1837/isrs.json` | 12.053.293 | cuplikan 2 MB pertama |
| `belajar-2026-11-16/run9-1837/isos_by_isr.json` | 51.151.474 | cuplikan 2 MB pertama |
| `belajar-2026-11-17/run10-0237/isrs.json` | 12.996.326 | cuplikan 2 MB pertama |
| `belajar-2026-11-17/run10-0237/isos_by_isr.json` | 78.219.606 | cuplikan 2 MB pertama |
| `belajar-2026-11-17/run11-0717/isrs.json` | 13.662.201 | cuplikan 2 MB pertama |
| `belajar-2026-11-17/run11-0717/isos_by_isr.json` | 85.632.580 | cuplikan 2 MB pertama |
| `belajar-2026-11-18/antrean-verdict/listing.json` | 16.454.431 | cuplikan 2 MB pertama |
| `belajar-2026-11-18/antrean-verdict/isos_by_isr.json` | 55.426.177 | cuplikan 2 MB pertama |

## 2. Artefak bytecode Python — 65 berkas (tidak diarsipkan)

Berkas `*.pyc` di dalam folder `__pycache__` adalah artefak kompilasi Python, bukan bukti; source `.py` pasangannya terarsip lengkap. Daftar:

- `belajar-2026-11-17/run10-0237/__pycache__/analyze10.cpython-312.pyc`
- `belajar-2026-11-17/run10-0237/__pycache__/pull10.cpython-312.pyc`
- `belajar-2026-11-17/run10-0237/__pycache__/supp10.cpython-312.pyc`
- `belajar-2026-11-17/run10-0237/__pycache__/sweep10.cpython-312.pyc`
- `provider/__pycache__/ask_driver.cpython-312.pyc`
- `provider/__pycache__/audit_sent_draft.cpython-312.pyc`
- `provider/__pycache__/calibrate_checker_crowllm.cpython-312.pyc`
- `provider/__pycache__/calibrate_checker_gptoss.cpython-312.pyc`
- `provider/__pycache__/calibrate_content_verify.cpython-312.pyc`
- `provider/__pycache__/calibrate_semantic_c5.cpython-312.pyc`
- `provider/__pycache__/citation_verify.cpython-312.pyc`
- `provider/__pycache__/cloudflare_provider.cpython-312.pyc`
- `provider/__pycache__/cloudflare_serve_common.cpython-312.pyc`
- `provider/__pycache__/cloudflare_serve_prepare.cpython-312.pyc`
- `provider/__pycache__/cloudflare_serve_provider.cpython-312.pyc`
- `provider/__pycache__/cloudflare_serve_ready.cpython-312.pyc`
- `provider/__pycache__/content_verify.cpython-312.pyc`
- `provider/__pycache__/crosstest_ask_drafts.cpython-312.pyc`
- `provider/__pycache__/crowllm_checker.cpython-312.pyc`
- `provider/__pycache__/dashscope_provider.cpython-312.pyc`
- `provider/__pycache__/doctrine_a.cpython-312.pyc`
- `provider/__pycache__/freshness_gate.cpython-312.pyc`
- `provider/__pycache__/gemini_provider.cpython-312.pyc`
- `provider/__pycache__/launcher_test.cpython-312.pyc`
- `provider/__pycache__/novelty_context.cpython-312.pyc`
- `provider/__pycache__/novelty_context.py.cpython-312.pyc`
- `provider/__pycache__/openrouter_provider.cpython-312.pyc`
- `provider/__pycache__/openrouter_wrapper.cpython-312.pyc`
- `provider/__pycache__/rate_trigger.cpython-312.pyc`
- `provider/__pycache__/run_novelty_ab.cpython-312.pyc`
- `provider/__pycache__/run_serve.cpython-312.pyc`
- `provider/__pycache__/serve_gate.cpython-312.pyc`
- `provider/__pycache__/smoke_gemini.cpython-312.pyc`
- `provider/__pycache__/smoke_vyce.cpython-312.pyc`
- `provider/__pycache__/target_picker.cpython-312.pyc`
- `provider/__pycache__/test_checker_chain.cpython-312.pyc`
- `provider/__pycache__/test_cloudflare_claim_path.cpython-312.pyc`
- `provider/__pycache__/test_cloudflare_serve.cpython-312.pyc`
- `provider/__pycache__/test_content_verify.cpython-312.pyc`
- `provider/__pycache__/test_dashscope_claim_path.cpython-312.pyc`
- `provider/__pycache__/test_frontier_fold.cpython-312.pyc`
- `provider/__pycache__/test_improve_20261116.cpython-312.pyc`
- `provider/__pycache__/test_length_floors_perkelas.cpython-312.pyc`
- `provider/__pycache__/test_openrouter_claim_path.cpython-312.pyc`
- `provider/__pycache__/test_openrouter_wrapper.cpython-312.pyc`
- `provider/__pycache__/test_semantic_check.cpython-312.pyc`
- `provider/__pycache__/test_serve_gate.cpython-312.pyc`
- `provider/__pycache__/test_zai_claim_path.cpython-312.pyc`
- `provider/__pycache__/vyce_provider.cpython-312.pyc`
- `provider/__pycache__/vyce_serve_common.cpython-312.pyc`
- `provider/__pycache__/vyce_serve_prepare.cpython-312.pyc`
- `provider/__pycache__/vyce_serve_provider.cpython-312.pyc`
- `provider/__pycache__/vyce_serve_ready.cpython-312.pyc`
- `provider/__pycache__/zai_provider.cpython-312.pyc`
- `provider/lib/__pycache__/citation_patch.cpython-312.pyc`
- `provider/lib/__pycache__/clean_answer.cpython-312.pyc`
- `provider/lib/__pycache__/clean_smoke.cpython-312.pyc`
- `provider/verifier/__pycache__/lane_drafter.cpython-312.pyc`
- `provider/verifier/__pycache__/register_ivsp.cpython-312.pyc`
- `provider/verifier/__pycache__/run_verifier.cpython-312.pyc`
- `provider/verifier/__pycache__/self_dealing_gate.cpython-312.pyc`
- `provider/verifier/__pycache__/test_verifier_kit.cpython-312.pyc`
- `provider/verifier/__pycache__/verdict_drafter.cpython-312.pyc`
- `provider/verifier/__pycache__/verifier_common.cpython-312.pyc`
- `skill-audit/pkg/dialectica/scripts/__pycache__/trued.cpython-312.pyc`

## 3. Berkas murni rahasia — TIDAK ADA

Pindaian pola rahasia atas seluruh pohon sumber (pola: API key `sk-`/`ghp_`/`github_pat_`/`AKIA…`, blok `PRIVATE KEY`, JWT, penugasan `key/token/secret/password = "…"`, nilai header `Bearer`/`X-Active-Session`, nama berkas rawan `*.env`/`*session*`/`*credential*`/`*.pem`/`*.key`/`agent.json`) **tidak menemukan satu pun berkas yang isinya murni kredensial** di dalam pohon `research/dialectica/`. Karena itu tidak ada berkas yang dikeluarkan dengan alasan murni rahasia. Nilai sensitif yang tersisip di dalam berkas bukti ditangani dengan redaksi pada salinan (lihat REDACTION-LOG.md); berkas asli tidak diubah.

## 4. Di luar cakupan sumber

- Folder `~/.dialectica/` (berisi kredensial sesi live) **bukan** bagian dari sumber arsip dan tidak pernah dibuka/disalin dalam perakitan ini.
- Berkas di luar `~/workspace/research/dialectica/` dan `~/workspace/user/dialectica-operator-prompt.md` tidak termasuk perintah pengarsipan.
