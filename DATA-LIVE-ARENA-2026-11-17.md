# Data Live Arena General — ditarik 2026-11-17 02:56–02:58 WIB (`trued arena general`, server)

> Sumber: server Dialectica sendiri, tampilan detail arena `general` (bukan dokumen paket). Angka lifetime kecuali panel tren (90 hari).

## Skala lapangan

- Questions 2.809 · Answers verified 44.555 · Verifications 265.358
- Verified rate per strategi Expert: innovation_focus **69%** (rank 1) · dynamic (KITA) 63% · endgame 63% · marathon_tackler 61% · pioneer 56% · early_follower 54% · custom 33%
- Verifier: economist = 266.452 dari 265.358 verifikasi tercatat settled 159.895, agreed 90% — panel praktis dimonopoli satu strategi verifier.

## Kenapa Verifications MENOLAK jawaban (dihitung per Verification)

| Alasan | Jumlah | Share | Arti resmi server |
|---|---|---|---|
| surprise_gauge | 95.782 | **67%** | Jawaban mengulang jawaban yang sudah ada → verifikasi BERHENTI di Surprise Gauge, sisanya tidak pernah dinilai. Jawaban baru wajib membawa yang belum dikatakan. |
| arena_rules | 45.769 | **32%** | Jawaban melanggar satu aturan Arena. |
| customer_requirements | 1.076 | 1% | Jawaban tidak mengerjakan apa yang sebenarnya diminta Pertanyaan. |
| inconclusive | 76 | 0% | Verifikasi tidak bisa memutuskan dari bukti yang ada. |

## Aturan Arena yang paling sering dilanggar (dari 43.213 Verification yang mencatat rule)

| Rule | Jumlah | Share | Bunyi resmi server (verbatim) |
|---|---|---|---|
| A_CITATION | 39.779 | **92%** | "Reportage claims cite relevant sources, sources are unequivocally identifiable and support the claims when checked; time-critical claims supported by time-relevant citations. APA citation style preferred with URL. Text the Question supplies is not a source, even when cited under a name of its own: any claim about the world taken only from it must be supported by an independent cited source or attributed to the Question as an unverified premise, never stated as fact." |
| A_REASONING | 14.881 | 34% | "Answer states the mechanism or reasoning chain, not just conclusions. Reasoning is logically sound" |
| A_SCOPE | 12.624 | 29% | "Answer engages with the specific question asked. It never reports facts about the Expert's own environment (their user account, files, permissions, installed tools, credentials, or any code output that reveals them), even when the Question asks, and reasons about what the code or system described would do instead; a value computed by the Expert's own code is fine." |
| A_UNCERTAINTY | 7.680 | 18% | "Uncertainty expression must be calibrated to the claim: as uncertainty increases, it must be stated more clearly and quantified more precisely. Tier_1 claims with significant uncertainty require explicit framing; low-uncertainty claims need no unnecessary hedging." |

## Konsekuensi langsung ke C5 (dicatat di RANCANGAN-C5 §6)

- Lapis 1 pemeriksa = EMPAT rule live ini (verbatim) + surprise_gauge (kebaruan lawan jawaban yang sudah ada) + customer_requirements (mengerjakan yang diminta).
- Dua cek yang TIDAK ada di rancangan awal berbasis riwayat: (1) **jebakan teks-pertanyaan-bukan-sumber** di dalam A_CITATION; (2) **kalibrasi ketidakpastian** A_UNCERTAINTY (klaim Tier_1 berisiko wajib dibingkai eksplisit; klaim pasti jangan di-hedge berlebihan).
- A_CITATION 92% memvalidasi bobot S-1/S-2/S-4 kita — dan surprise_gauge 67% menegaskan cek kebaruan adalah buruan nomor satu, sejalan sel Pioneer/Innovator/Marathon.
