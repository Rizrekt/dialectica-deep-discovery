# Ukur contextWindowTokens — 2026-11-17 (PERINTAH USER 02:24: "ukurlah, jangan pakai tebakan!")

> Sifat: pengukuran dari data produksi sendiri + metadata provider resmi. Nol angka tebakan.
> Keputusan yang ditutup: butir (b) keputusan menunggu dari AUDIT-PROFIL-EXPERT-2026-11-17 (contextWindowTokens tidak terdeklarasi).

## 1. Semantik field (sumber: SKILL.md klien resmi, baris 347)

- `contextWindowTokens` = **seluruh jendela model (prompt + balasan)**, minimum 8.000.
- **Tidak dideklarasikan** → server menjaga prompt tiap job di bawah ±75.000 token dengan membuang Answer lama (Verified dipertahankan dulu, lalu yang terbaru yang muat; prompt menyebut berapa yang dibuang).
- Dideklarasikan W → Answer lama dibuang sampai prompt muat di W.
- **≥100.000 = batas standar** ("to go back to the standard limit, set 100,000 or more").
- Question + aturan arena + format selalu dikirim utuh; bila itu saja melebihi W, pertanyaan tidak dikirim / klaim ditolak dengan alasan — **biaya nol**.

## 2. Ukuran prompt NYATA kita (token-usage.jsonl, 131 record ber-usage)

| Model (lane) | n | median | p95 | maks prompt | maks completion |
|---|---|---|---|---|---|
| glm-5.3-flash (Vyce — serve) | 57 | 23 | 149.005 | **156.313** | 10.048 |
| @cf/openai/gpt-oss-120b (Cloudflare) | 14 | 2.189 | 70.765 | 70.765 | — |
| nvidia/nemotron-3-ultra:free (OpenRouter) | 41 | 343 | 3.208 | 75.668 | — |
| deepseek-v4.1 (Vyce) | 4 | 1.231 | 1.231 | 1.231 | — |
| glm-4.7-flash (Z.ai) | 1 | 133 | 133 | 133 | — |

- Record terbesar = job serve NYATA 14 Nov (ISR `8f4b9221`, answer 35.333 kar): **prompt 156.313 + completion 10.048 = 166.361 token dalam SATU request yang SUKSES** di jalur produksi persis (server → Vyce GLM 5.3 Flash). Lima record teratas semuanya 143–156 rb prompt, completion mentok 10.048 (= cap max_tokens lama).
- **Lantai terukur jendela GLM 5.3 Flash (jalur serve kita): ≥166.361 token.** Ini bukti eksekusi, bukan katalog.

## 3. Metadata provider (resmi, ditarik 17 Nov 02:2x WIB)

- OpenRouter `/api/v1/models` (publik): gpt-oss-120b context_length **131.072** · z-ai/glm-4.7-flash **200.000** (top-provider 131.072) · nemotron-3-ultra:free top-provider **1.000.000** (model 262.144).
- Vyce `GET /v1/models` = **403** untuk kunci kita → katalog Vyce tidak bisa ditarik; untuk GLM 5.3 Flash yang berlaku adalah lantai terukur §2 (jalur yang sama persis dengan produksi).

## 4. Nilai yang diset + alasannya

**contextWindowTokens = 160.000**

- Di bawah lantai terukur GLM (166.361) dengan margin ±6,3 rb → server tidak akan pernah menyusun prompt+balasan melebihi yang sudah TERBUKTI muat di model serve kita.
- Di atas ambang standar 100.000 → perilaku standar server berlaku penuh.
- Lane serve pilot = GLM saja (lane lain answer-only, dipilih per tembakan sesudah ukuran prompt terlihat) → jendela yang mengikat memang GLM.
- Efek yang dicari: pada pertanyaan marathon, server boleh mengirim LEBIH BANYAK Answer lama ke kita (naik dari trim ±75 rb) — bahan bedah kebaruan Pioneer/Innovator (novelty ≥15% butuh tau apa yang sudah dikatakan orang).

## 5. Risiko sisa (tercatat, bukan disembunyikan)

- Penghitung token server vs tokenizer GLM bisa berbeda pada konten ekstrem; margin 6,3 rb + fakta 5 record ≥143 rb sukses membuat risiko ini kecil. Bila generasi serve berikutnya gagal karena konteks, nilai diturunkan ke 131.072 (angka katalog gpt-oss/GLM-4.7 top-provider) di giliran yang sama.
- Nilai ini deklarasi kapasitas, BUKAN ubah strategi/caps/arena — wilayah final user tidak disentuh.

## 6. LIPATAN 02:31 — angka resmi GLM 5.3 Flash (menutup celah §3)

Sesudah user menantang ketelitian ("udh teliti dan detail? jangan karna mau cepat aja"), celah katalog GLM ditutup: **jendela resmi GLM-5.3-Flash = 1.000.000 token** (kartu model resmi Zhipu di Hugging Face `zai-org/GLM-5.3-Flash`; dikonfirmasi silang Benchgen, Requesty, LLMTR yang menyitir dokumentasi Z.AI; rilis 26 Agu 2026, MIT).

Konsekuensi pada vonis: modelnya sendiri BUKAN batas (1M >> 160 rb). Segmen yang belum terbukti di atas 166.361 hanyalah **cap router Vyce** — dan justru itu alasan 160.000 (terbukti end-to-end lewat pipa produksi) tetap angka yang benar, BUKAN 1M: deklarasi 1M akan membiarkan server menyusun prompt yang belum pernah terbukti lewat Vyce. Bila suatu saat perlu >160 rb, uji pipa dulu (satu generasi uji berprompt besar), baru naikkan deklarasi.
