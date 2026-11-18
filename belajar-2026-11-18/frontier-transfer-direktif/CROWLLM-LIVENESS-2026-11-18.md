# CROWLLM LIVENESS — Sapuan Free Tier, 18 Nov 2026 ±21:11–21:38 WIB

**Metode:** daftar model dari endpoint resmi `GET /v1/models` via klien CrowLLM (status 200, latensi 1,16 dtk — endpoint katalog HIDUP). Probe per model: `chat` dengan prompt persis "Reply with exactly: OK", sekuensial, jeda ≥13 detik antar awal panggilan, timeout 90 detik. 57 model diprobe sapuan ini; 5 sisanya terkonfirmasi 503 oleh sesi utama pada 21:04–21:10 WIB (tidak diulang, sesuai aturan sapuan). Total katalog: **62 model**.

## Ringkasan angka

- **HIDUP (200): 21 dari 62**
- MATI / tidak bisa dipakai: 41 dari 62
  - 503: 22 (17 sapuan ini + 5 terkonfirmasi sesi utama)
  - 429 (model menolak, "high demand"): 6
  - Timeout 90 detik (tidak menjawab sama sekali): 5
  - 403 (izin upstream): 4
  - 500 (upstream rusak sementara): 2
  - 400 (id ditolak sebagai tidak sah oleh jalur chat): 2

## Daftar yang HIDUP (21)

| Model | Latensi (dtk) |
|---|---|
| qwen-3.8-27b:free | 0,80 |
| qwen3-8-omni-flash:free | 6,15 |
| ernie-5.5-flash-preview:free | 8,17 |
| laguna-xs-2.1:free | 1,17 |
| nvidia/mistral-large-4-1t-a52b:free | 48,29 |
| nemotron-3-ultra-550b-a55b:free | 2,33 |
| nemotron-3.5-super-vl:free | 2,31 |
| nvidia/nemotron-3.5-bolt-e4b:free | 1,59 |
| nvidia/nemotron-3.5-super-vl-120b-a12b:free | 1,80 |
| dots-3-note-preview:free | 5,14 |
| jais-3-mova-36b-a4b:free | 20,49 |
| k2-horizon-375b-a23b:free | 1,56 |
| openai/gpt-oss-safeguard-20b:free | 1,28 |
| particle-1:free | 2,68 |
| typhoon-v2.5-30b-a3b-instruct | 1,75 |
| hy4-flash:free | 5,99 |
| solar-mini4:free | 20,27 |
| grok-4.7-fast:free | 4,76 |
| grok-4.7:free | 3,84 |
| glm-4.6v-flash:free | 11,09 |
| glm-4.7-flash:free | 3,73 |

Semua membalas persis "OK" pada probe.

## Tabel lengkap (62 model)

| Model | Status | Latensi (dtk) | Catatan |
|---|---|---|---|
| qwen-3.5-397b-a17b:free | timeout90 | 90,07 | tidak menjawab |
| qwen-3.6-27b:free | timeout90 | 90,05 | tidak menjawab |
| qwen-3.6-plus:free | 503 | 40,48 | error komunikasi upstream |
| qwen-3.8-27b:free | **200** | 0,80 | OK |
| qwen-3.8-max:free | 503 | 39,99 | error komunikasi upstream |
| qwen3-8-omni-flash:free | **200** | 6,15 | OK |
| ernie-5.5-flash-preview:free | **200** | 8,17 | OK |
| laguna-xs-2.1:free | **200** | 1,17 | OK |
| deepseek-v4-flash-0731-thinking:free | 429 | 0,96 | high demand |
| deepseek-v4-flash-0731:free | 429 | 1,14 | high demand |
| gemini-2.0-flash:free | 503 | 40,15 | error komunikasi upstream |
| gemini-2.5-pro:free | 503 | 38,94 | error komunikasi upstream |
| gemini-3-flash:free | 503 | 0,86 | "system cpu overloaded" 95,6% |
| gemini-3-pro:free | 429 | 31,11 | high demand |
| gemini-3.1-flash-lite:free | 403 | 3,36 | tidak ada izin akses |
| gemini-3.1-pro:free | 503 | — | terkonfirmasi sesi utama 21:04–21:10 |
| gemini-3.5-flash-lite | 503 | 3,33 | "system cpu overloaded" 93,4% (id tanpa sufiks :free, tetap di katalog) |
| gemini-3.5-flash-lite:free | 403 | 1,77 | AI Studio balas HTTP 403 |
| gemini-3.5-flash:free | 503 | 40,05 | error komunikasi upstream |
| gemini-3.7-flash:free | 503 | 0,76 | "system cpu overloaded" 91,3% |
| gemini-3.8-flash:free | 403 | 2,29 | tidak ada izin akses |
| gemini-4-hydrogen:free | 403 | 1,87 | tidak ada izin akses |
| gemini-flash-latest:free | 503 | — | terkonfirmasi sesi utama 21:04–21:10 |
| muse-spark-1.1:free | 503 | 39,94 | error komunikasi upstream |
| llama-3.3-70b-instruct:free | timeout90 | 90,05 | tidak menjawab |
| llama-3.3-70b:free | timeout90 | 90,09 | tidak menjawab |
| minimax-m2.5:free | 503 | 40,19 | error komunikasi upstream |
| minimax-m3.1-flash:free | timeout90 | 90,05 | tidak menjawab |
| mistral-medium-3.5:free | 503 | 38,95 | error komunikasi upstream |
| nvidia/mistral-large-4-1t-a52b:free | **200** | 48,29 | OK (lambat) |
| runpod/kimi-k3 | 503 | 39,87 | error komunikasi upstream (id tanpa sufiks :free) |
| nemotron-3-ultra-550b-a55b:free | **200** | 2,33 | OK |
| nemotron-3.5-super-vl:free | **200** | 2,31 | OK |
| nvidia/nemotron-3.5-bolt-e4b:free | **200** | 1,59 | OK |
| nvidia/nemotron-3.5-super-vl-120b-a12b:free | **200** | 1,80 | OK |
| dots-3-note-preview:free | **200** | 5,14 | OK |
| flint-v1.0:free | 500 | 83,63 | upstream "temporarily" rusak |
| gpt-4.1-mini:free | 503 | — | terkonfirmasi sesi utama 21:04–21:10 |
| gpt-4o-mini:free | 503 | 39,58 | error komunikasi upstream |
| gpt-4o:free | 429 | 30,93 | high demand |
| gpt-5.6-sol:free | 503 | — | terkonfirmasi sesi utama 21:04–21:10 |
| jais-3-mova-36b-a4b:free | **200** | 20,49 | OK |
| k2-horizon-375b-a23b:free | **200** | 1,56 | OK |
| liquid/lfm-2.5-2.6b-thinking:free | 400 | 0,88 | id ditolak jalur chat |
| liquid/lfm-2.5-2.6b:free | 400 | 1,56 | id ditolak jalur chat |
| longcat-2.5:free | 500 | 19,05 | upstream "temporarily" rusak |
| o3:free | 503 | 39,66 | error komunikasi upstream |
| o4-mini:free | 503 | 39,91 | error komunikasi upstream |
| openai/gpt-oss-20b:free | 503 | 0,87 | "system cpu overloaded" 99,3% |
| openai/gpt-oss-safeguard-20b:free | **200** | 1,28 | OK |
| particle-1:free | **200** | 2,68 | OK |
| typhoon-v2.5-30b-a3b-instruct | **200** | 1,75 | OK (id tanpa sufiks :free) |
| xing4.0-29b-a4b:free | 503 | 0,88 | "system cpu overloaded" 92,7% |
| hy4-flash:free | **200** | 5,99 | OK |
| solar-mini4:free | **200** | 20,27 | OK |
| grok-4.7-fast:free | **200** | 4,76 | OK |
| grok-4.7:free | **200** | 3,84 | OK |
| caw/glm-5.3-flash-thinking:free | 429 | 1,44 | high demand |
| caw/glm-5.3-flash:free | 429 | 1,43 | high demand |
| glm-4.6v-flash:free | **200** | 11,09 | OK |
| glm-4.7-flash:free | **200** | 3,73 | OK |
| glm-5.3-flash:free | 503 | — | terkonfirmasi sesi utama 21:04–21:10 |

## Pola (jawaban atas dugaan "relay down menyeluruh")

**BUKAN mati menyeluruh.** Pintu depan relay sehat (katalog 200 dalam 1,16 dtk) dan 21 model menjawab normal. Yang mati terkumpul per kolam upstream:

- **Keluarga Gemini: MATI TOTAL** — 12 varian Gemini di katalog, 0 hidup (campuran 503 lambat, 503 cepat "system cpu overloaded", 429, dan 403 dari AI Studio). Jalur Google putus/kelebihan beban di semua bentuk kegagalan sekaligus.
- **Keluarga OpenAI arus utama: MATI TOTAL** — gpt-5.6-sol, gpt-4.1-mini, gpt-4o-mini, o3, o4-mini semua 503; gpt-4o 429. Satu-satunya OpenAI yang hidup = gpt-oss-safeguard-20b (kolam beda).
- **Keluarga NVIDIA/Nemotron: HIDUP TOTAL** — 5 dari 5 (mistral-large lambat 48 dtk, sisanya 1,6–2,3 dtk).
- **Grok: HIDUP 2/2.** GLM: flash kecil hidup (4.6v, 4.7), lini 5.3 mati (429/503). Qwen: yang kecil hidup (3.8-27b, omni-flash), yang besar timeout/503 — termasuk **qwen-3.8-max 503** (pemeriksa cadangan rantai). DeepSeek: 429 dua-duanya (endpoint merespons, model menolak karena beban). Llama + MiniMax: timeout/503.

Dua kelas 503 berbeda terlihat: **503 lambat (±40 dtk)** = relay menunggu upstream yang tidak menjawab; **503 cepat (<5 dtk)** dengan pesan "system cpu overloaded (91–99%)" = host relay sendiri menolak di muka untuk rute tertentu.

**Implikasi langsung buat kursi frontier proyek ini:** dua kursi yang dibutuhkan — gpt-5.6-sol (co-advisor) dan gemini-3.1-pro (penengah/kritikus pengganti) — dua-duanya berada di kolam yang mati total malam ini. Yang hidup dan setara kelasnya untuk peran penilai malam ini: nemotron-3-ultra-550b, grok-4.7, k2-horizon-375b, qwen-3.8-27b (bukan max). Keputusan penggantian kursi = wewenang sesi utama/user, bukan sapuan ini.
