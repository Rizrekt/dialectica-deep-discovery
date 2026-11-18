# DRY-RUN TERPADU — Fase Testing Dialectica (2026-11-17)

> Perintah user 2026-11-17 03:48 (Opsi A, tugas 1). **DRY-RUN TOTAL: tidak ada submit/answer/claim dalam bentuk apa pun** — yang dipanggil hanya search/detail read-only, generate, `gate_answer`, dan `semantic_check` shadow. Berhenti sebelum submit, sesuai perintah.
> Deviasi satu-satunya dari kabel produksi: urutan lane pemeriksa C5 dibalik jadi **Vyce-dulu** (aturan bahan bakar run ini — sisa OpenRouter free ±12/50 sesudah kalibrasi C5) dan log semantik ditulis ke `/tmp/dryrun1-semantic-log.jsonl`. Semua komponen lain persis pipa asli (`vyce_serve_common.generate_vyce` → `serve_gate.gate_answer` → `serve_gate.semantic_check`).

## 1. Target

Metode: baris pertanyaan live dari permukaan search klien yang sama yang memberi makan serve (`/api/node/explore-search`, 12 query topik inti → **96 baris unik**, 57 lolos saringan kata kunci topik inti), lalu saringan pilot PAKET-RESTART-SERVE: **liveness tiga-field** (`serve_gate.liveness_gate_for_row`, fetch detail ter-arm) + **topik inti**, prioritas Pioneer viso-0.

- Sapuan pertama (8 kandidat teratas hasil 6 query): **8/8 MATI** — semua pola flag basi (marathonActive/Concluded true, semua `endsAt` ronde sudah lewat). Ini spesies §82 yang sama; gerbang liveness menahannya di prepare, nol generasi terbakar.
- Sapuan kedua (jaring dilebarkan): kandidat pertama langsung lolos.

**Target terpilih: ISR `8a4e9623-772d-446b-9cdd-4d72e93371bb`**

- Pertanyaan: *"When an NFT contract blocks all transfers, how can a dedicated marketplace still enable trading of those tokens, and what trust assumptions around custody, operator honesty, or upgrade keys does that trading introduce for buyers and sellers?"*
- Kenapa lolos: **viso = 0** (bentuk Pioneer — satu-satunya jalur +20); **LIVE** — *"pertanyaan terbuka tanpa dimensi maraton (status in_progress)"*; topik inti kena kata kunci `token` (isi pertanyaan memang soal perdagangan token NFT, kustodi, dan kunci upgrade — inti on-chain).

## 2. Draf 1 — penulis GLM via Vyce (pipa asli)

| Ukuran | Hasil |
|---|---|
| Generasi | **Lahir** — 8.390 karakter, 43,4 detik, `glm-5.3-flash`, tanpa regenerasi (1 panggilan, tercatat lane `vyce-serve`; cap serve hari-UTC 0 → 1 dari 10) |
| Gerbang bentuk | status wrapper **OK**, gerbang format (g) **LOLOS**, 1 temuan audit |
| Vonis gerbang | **DITAHAN (sendable = false)** — oleh lapis thinking-trace, lihat temuan di bawah |
| **C5 atas draf ini** | **CLEAN — 0 temuan, 0 gugur** (pemeriksa `vyce-nemotron`, mode shadow) |

**Temuan gerbang yang penting — false-positive terukur di lapis trace:** penutup draf adalah persis blok sintesis yang DIWAJIBKAN kontrak serve ("New in this answer: …"), tetapi detektor penutup-rencana (`_TRACE_PLAN_CLOSING`) menembak kata **`decision:`** dari kalimat sah di dalam sintesis itu (*"…frames the lock and the dedicated marketplace as a single design decision: the same carve-out…"*). Regex `decision\s*:` tidak membedakan "Decision:" sebagai tajuk rencana dari kata benda biasa "decision:" di tengah kalimat. Akibatnya draf GLM yang secara isi **clean di mata C5** tetap tertahan oleh lapis bentuk. Ini gesekan kontrak-vs-detektor yang hanya terlihat di dry-run terpadu — tidak terlihat di uji unit mana pun.

**Angka yang selama ini hilang (salah-fatal C5 di draf SENDIRI):** draf serve GLM asli kita yang pertama diukur = **CLEAN (0 fatal)**. Populasi draf sendiri sejauh ini: 1 clean dari 1 draf penuh (draf 2 di bawah adalah stub pendek, populasi berbeda — lihat §3).

## 3. Draf 2 — penulis lane cadangan: Nemotron via Vyce

| Ukuran | Hasil |
|---|---|
| Generasi | **Lahir tapi sangat pendek** — 531 karakter mentah (kontrak serve menargetkan 6.000–9.000); regenerasi wrapper menembak 1× (total 2 panggilan Nemotron) → teks final 1.380 karakter |
| Gerbang bentuk | **DITAHAN** — status `GAGAL-LANJUT` (panjang di bawah lantai sesudah regenerasi) + temuan lantai K-2 (rasio angka terikat 0,000 < 0,30) |
| C5 atas draf ini | **FATAL — 1 temuan**: `A_CITATION / S-1` atas kutipan *"…pasar yang berdedikasi biasanya mencoba tiga mekanisme"* — cacah spesifik "tiga mekanisme" dinyatakan sebagai fakta tanpa sumber bernama. Kutipan terverifikasi ke draf; tangkapan sah pada teksnya |
| Deepseek | **Tidak perlu dicoba** — penulis Nemotron menjawab (bukan gagal), jadi cabang deepseek tidak terpicu. Konflik catatan probe (sesi utama 02:44 rc=0 vs lini C5 403) TIDAK terputus run ini; yang terputus: Nemotron-Vyce bisa menulis end-to-end |

**Vonis lane cadangan end-to-end:** mekanik **terbukti jalan penuh** — generasi → regenerasi → gerbang → pemeriksa, semua di lane cadangan, tanpa OpenRouter sama sekali. Kualitas **belum**: 531 karakter melawan target 6.000–9.000 berarti `nemotron-3.5-super-vl` sebagai penulis serve menghasilkan stub, bukan jawaban serve; di rezim nyata draf seperti ini tertahan di lantai sebelum semantik bicara. Lane cadangan hari ini adalah cadangan *pemeriksa* yang terbukti dan cadangan *penulis* yang hidup tapi belum layak.

## 4. Bahan bakar (semua free, $0)

| Lane | Panggilan | Rincian |
|---|---|---|
| Vyce — GLM `glm-5.3-flash` (generasi serve, subprocess `vyce_provider`) | 1 | draf 1; tercatat di token-usage lane `vyce-serve` (cap 0→1/10) |
| Vyce — Nemotron `nemotron-3.5-super-vl` (penulis cadangan) | 2 | draf 2 awal + 1 regenerasi wrapper |
| Vyce — Nemotron (pemeriksa C5) | 2 | 1 per draf, keduanya sukses — OpenRouter tidak tersentuh |
| OpenRouter | **0** | cadangan ±12/50 utuh |
| Vyce — deepseek-v4.1 | 0 | tidak terpicu |
| API klien `trued` (read-only) | ±27 | dua sapuan search (6 + 12 query) + fetch detail liveness (8 mati + 1 target) |

## 5. Kesimpulan dry-run

1. **Pipa terpadu jalan end-to-end tanpa submit:** target live tersaring (8 target mati tertahan di prepare, nol biaya), draf lahir, gerbang + C5 menilai, berhenti sebelum kirim.
2. **C5 di draf sendiri: 1 clean (draf penuh GLM) + 1 fatal (stub Nemotron, tangkapan S-1 sah).** Angka salah-fatal atas draf penuh sendiri sementara **0/1** — terlalu kecil untuk vonis blocking; akumulasi shadow tetap jalan yang benar (sejalan vonis KALIBRASI-C5).
3. **Temuan baru di luar C5:** lapis thinking-trace punya false-positive mekanik lawan kontrak serve sendiri (kata `decision:`) — draf patuh-kontrak bisa tertahan. Ini bahan lab, bukan diubah di run ini.
4. **Lane cadangan penulis hidup tapi belum layak panjangnya**; sebagai pemeriksa ia justru yang menanggung seluruh dry-run ini dengan bersih.

---

## Lampiran A — Draf 1 final (GLM, 8.390 karakter, teks utuh sesudah gerbang)

A transfer block only stops the token from moving through the contract's *general* transfer path; a dedicated marketplace can still trade such NFTs whenever the block was written with a carve-out — a privileged operator, an allowlisted vault, or a claim layer above the token — and every one of those designs replaces the chain's "you hold it, you control it" guarantee with trust in a custodian, an operator, and whoever holds the admin or upgrade keys.

## 1. What "blocks all transfers" actually blocks

Under ERC-721, tokens move via `transferFrom`/`safeTransferFrom`, authorized by the owner directly or by an address approved through `approve` / `setApprovalForAll` (EIP-721, https://eips.ethereum.org/EIPS/eip-721). A "locked" NFT is one where the contract reverts on those calls; EIP-5192 standardizes the signal — a `locked(uint256 tokenId) returns (bool)` interface — and requires transfers of locked tokens to revert (https://eips.ethereum.org/EIPS/eip-5192). Implementations split into two families, and the distinction determines everything else:

- **Absolute lock**: every non-mint, non-burn move reverts regardless of approvals. Generic marketplaces cannot settle these at all — even a buyer-approved transfer reverts, and marketplaces that respect EIP-5192 typically disable trading for such items.
- **Carve-out lock**: transfers revert *unless* `msg.sender` (or `from`/`to`) is a privileged address — an admin, a game/settlement contract, or an allowlisted vault. Some such contracts also disable `approve`/`setApprovalForAll` entirely, so the only legal mover is the privileged path.

## 2. How a dedicated marketplace still enables trading

**Pattern A — privileged operator settlement.** The standard design behind first-party game and platform marketplaces: the NFT contract exempts the marketplace's settlement contract from the lock. Trading then looks conventional — the seller signs an off-chain order as typed structured data (EIP-712, https://eips.ethereum.org/EIPS/eip-712), the buyer fills it, and the settlement contract executes the move through the exempt path. Third-party venues stay blocked because their generic `transferFrom` reverts — which is often the point: the lock doubles as marketplace exclusivity and fee capture.

**Pattern B — vault/wrapper.** If the contract permits transfers only to or from an allowlisted vault, the marketplace runs that vault: sellers deposit the NFT (the one move the contract allows), receive a freely tradable wrapped token (ERC-20 or ERC-721), and the wrapper trades on any venue; redemption sends the original back. The marketplace trades the wrapper, never the underlying.

**Pattern C — claim/IOU trading under an absolute lock.** If nothing can move the token, the marketplace trades *claims*: the seller proves control (a signature from the owner address), the marketplace records the sale in its own ledger or mints a derivative IOU token, and settlement of the underlying is deferred until — if ever — the lock is lifted. The on-chain registry keeps showing the seller as owner even after the "sale"; the buyer holds only a promise plus, at best, a contractual or derivative claim.

## 3. Custody trust assumptions

- **Pattern A**: users typically must grant `setApprovalForAll` to the settlement contract — normal marketplace risk, but amplified: the same privileged path that honors your sale can move tokens without your signature if the exemption is not scoped per-order. If the operator role sits on an externally owned key rather than a contract, you are trusting a key, not code.
- **Pattern B**: the vault is the custodian. Wrapper holders trust vault solvency and redeemability; an admin pause, exploit, or key loss strands every wrapper while the underlying sits frozen. Wrappers can also drift from the underlying — metadata changes, royalty changes, or utility that accrues only to the on-chain owner.
- **Pattern C**: full custodial trust. Beneficial ownership and registered ownership permanently diverge: the on-chain owner retains anything that accrues to that address (airdrops, governance votes, future utility) while the buyer holds a claim with no on-chain enforcement. Sellers, symmetrically, trust the operator to pay out.

In all three, the ERC-721 property that possession equals control is gone; the registry no longer tells you who economically owns the asset.

## 4. Operator honesty

A privileged operator is a single chokepoint whose honesty you must underwrite:

- **Censorship and ordering**: it can refuse to fill orders, delay settlement, reorder execution, or prioritize its own positions.
- **Rule changes**: fees, listing rules, and supported order types are whatever the operator says they are, whenever it says so.
- **Double-selling (Pattern C)**: nothing on-chain prevents the operator from selling the same claim to two buyers; an off-chain claim ledger has no consensus layer, so honesty literally replaces it.
- **Key compromise**: whoever holds the operator key can move every token the exemption reaches, or every claim the ledger records.

Mitigations reduce but never eliminate this: EIP-712 signed orders with nonces make orders verifiable and replay-protected; multisigs and timelocks on the operator role slow unilateral action; reserve attestations can discipline vaults. But each mitigation is only as strong as the admin keys that installed it and can modify it.

## 5. Upgrade keys: the lock is a promise, not a law

Contracts with transfer locks are usually ownable (EIP-173, https://eips.ethereum.org/EIPS/eip-173), and many sit behind upgradeable proxies — where the implementation is swappable through the admin slot defined in EIP-1967 (https://eips.ethereum.org/EIPS/eip-1967) or via UUPS hooks per EIP-1822 (https://eips.ethereum.org/EIPS/eip-1822); OpenZeppelin's upgrade tooling documents this mechanics (https://docs.openzeppelin.com/upgrades-plugins/). The key holder can, without anyone's consent:

- **lift the lock**, converting a "soulbound" credential or locked collectible into an ordinary tradable token — destroying exactly the non-transferability that buyers may have paid a premium for (on the intentional non-transferability model, see Buterin, "Soulbound," https://vitalik.ca/general/2022/01/26/soulbound.html);
- **swap the operator allowlist** to a new settlement contract that drains approved tokens;
- **insert fees or siphons** into the previously "blocked" transfer path.

For **buyers**, the checklist is: which pattern is this; does `locked()` exist and what does it return; who can call the unlock and admin functions; is the operator a contract or a key; are there timelocks or multisigs behind those roles. Price the key holder, not the lock. For **sellers**: approving a bypass-capable operator is broader exposure than a normal marketplace approval; under Pattern C you remain the on-chain owner with residual claims attached to that address; and if the admin unlocks the contract after you sold at a "locked" discount, the scarcity story behind your sale changes after the fact.

## Sources

- EIP-721, Non-Fungible Token Standard — https://eips.ethereum.org/EIPS/eip-721
- EIP-5192, Minimal Non-Transferable NFTs — https://eips.ethereum.org/EIPS/eip-5192
- EIP-712, Typed Structured Data Hashing and Signing — https://eips.ethereum.org/EIPS/eip-712
- EIP-173, Contract Ownership Standard — https://eips.ethereum.org/EIPS/eip-173
- EIP-1967, Proxy Storage Slots — https://eips.ethereum.org/EIPS/eip-1967
- EIP-1822, Universal Upgradeable Proxy Standard (UUPS) — https://eips.ethereum.org/EIPS/eip-1822
- Vitalik Buterin, "Soulbound" (vitalik.ca, 2022-01-26) — https://vitalik.ca/general/2022/01/26/soulbound.html
- OpenZeppelin Upgrades Plugins documentation — https://docs.openzeppelin.com/upgrades-plugins/

New in this answer: a three-pattern taxonomy — privileged-operator settlement, vault/wrapper, and custodial claim trading — that maps each way a dedicated marketplace trades locked NFTs to its specific custody failure mode. It frames the lock and the dedicated marketplace as a single design decision: the same carve-out that enables trading is what blocks third-party venues. Finally, it prices the upgrade key for both sides of the trade: "locked" is only as durable as the EIP-1967/EIP-173 admin key behind it, with buyers facing a silent unlock and sellers having sold at a locked discount before one.

## Lampiran B — Draf 2 final (Nemotron-Vyce, 1.380 karakter sesudah regenerasi, teks utuh)

Sebuah pasar NFT yang berdedikasi tetap dapat mengaktifkan perdagangan token yang transfernya diblokir pada tingkat kontrak intan dengan memindahkan eksekusi ke lapisan perantara—seperti kustodian, pembungkus, atau tanda tangan off-chain—tetapi perpindahan ini mengganti jaminan on-chain dengan kepercayaan pada penyimpanan, kejujuran operator, dan kunci upgrade.

## 1. Mekanisme Perdagangan Ketika Transfer Diblokir
**Pembuka:** Ketika fungsi `transferFrom` atau `safeTransferFrom` pada kontrak NFT selalu kembali dengan error, perpindahan langsung antar dompet tidak dapat terjadi, sehingga pasar harus menggunakan perantara yang dapat memindah atau mewakili aset.

Menurut spesifikasi EIP-721 (https://eips.ethereum.org/EIPS/eip-721), `transferFrom`, `safeTransferFrom`, `approve`, dan `setApprovalForAll` adalah antarmuka standar untuk perpindahan token non-fungible. Jika kontrak intan memblokir semua panggilan fungsi tersebut—misalnya melalui modifier yang selalu revert di `_beforeTokenTransfer`—izin on-chain seperti approval tidak cukup, karena panggilan tetap gagal di tingkat kontrak. Untuk itu, pasar yang berdedikasi biasanya mencoba tiga mekanisme.

Pertama, model kustodian atau vault. Pengguna mengunci NFT asli di kontrak yang dikontrol pasar, dan pasar mencetak token wakilan (wrapper) yang mewakili klaim atas NFT tersebut. Perdagangan kemudian dilakukan pada
