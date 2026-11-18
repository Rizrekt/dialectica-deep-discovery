# REDACTION-LOG — Daftar Redaksi pada Salinan Arsip

Redaksi hanya dilakukan pada SALINAN di repository ini. Berkas asli di workspace tidak diubah (terverifikasi: pola yang disensor masih utuh di berkas sumber). Nilai asli tidak ditulis di mana pun dalam arsip ini — yang dicatat hanya berkas, jenis nilai, dan jumlah kemunculan.

| Berkas (salinan arsip) | Jenis nilai yang disensor | Kemunculan | Pengganti |
|---|---|---|---|
| `belajar-2026-11-16/run7-0237/isos_by_isr.json` (cuplikan) | AWS access key ID (pola `AKIA…`) milik pihak ketiga, tertanam dalam URL presigned S3 di dalam teks jawaban platform | 4 | `[REDACTED]` |
| `belajar-2026-11-15/run6-1837/isos-2d968d7e.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-16/run7-0237/isos-2d968d7e.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-16/run7-0237/isos_by_isr.json` (cuplikan) | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-16/run8-1037/isos-2d968d7e.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-16/run9-1837/isos-2d968d7e.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-17/run10-0237/isos-2d968d7e.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-18/peta-jalur-2/pilot-isr-isos.json` | Nilai tanda tangan URL presigned (`X-Amz-Signature=…`) dalam teks jawaban platform | (bagian dari total 28) | `X-Amz-Signature=[REDACTED]` |
| `belajar-2026-11-18/peta-jalur-2/pilot-isr-isos.json` | Alamat email bisnis pihak ketiga di dalam teks jawaban platform | 1 | `[REDACTED-EMAIL]` |
| 7 berkas yang sama dengan baris tanda tangan di atas (`isos-2d968d7e.json` di run6/run7/run8/run9/run10, `isos_by_isr.json` cuplikan run7, `pilot-isr-isos.json`) | Token sesi URL presigned (`X-Amz-Security-Token=…`) dalam teks jawaban platform — ditemukan pada pindaian akhir, disensor dalam putaran kedua | 24 | `X-Amz-Security-Token=[REDACTED]` |

Total kemunculan yang disensor: **4** access key ID + **28** tanda tangan URL presigned + **24** token sesi URL presigned (`X-Amz-Security-Token`) + **1** alamat email = **57 nilai** pada **7 berkas**.

Catatan pola negatif-palsu: pola `sk-[A-Za-z0-9_-]{20,}` menghasilkan puluhan kecocokan di dump API yang setelah diperiksa konteksnya adalah **slug URL** di dalam sitasi teks jawaban (mis. slug artikel "regulatory-risk-…", "arc-risk-…"), bukan kredensial — tidak disensor agar teks bukti tidak rusak. Pola telepon menghasilkan kecocokan berupa deret angka ID/timestamp di data JSON, bukan nomor telepon. Keduanya didokumentasikan di sini agar pemeriksa dapat mengaudit keputusan ini.

Pindaian akhir atas seluruh pohon arsip sesudah redaksi: **nol** kemunculan untuk pola access key ID, tanda tangan presigned, email tersebut, blok PRIVATE KEY, token GitHub, dan JWT.
