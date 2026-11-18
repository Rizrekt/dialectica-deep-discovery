# SINTESIS FRONTIER JALUR 3 (BERTANYA) — konsultasi tuntas 2026-11-18 10:12–10:20 WIB
Kursi: duck.ai GPT-6 Luna (utama, browser cloud) · gpt-5.6-sol (co-advisor, CrowLLM) · gemini-3.1-pro (penengah, CrowLLM). Jawaban mentah: duck-answer.md, sol-answer.md, gemini-answer.md di folder ini. Paket: FRONTIER-PAKET-JALUR3.md.

KONVERGENSI (3 kursi / mayoritas kuat):
- Q4 DRAF: B (prover-batching ZK) = tembakan pertama. Sol + duck sepakat penuh. Keberatan penantang terhadap A = CACAT PREMIS NYATA (batas sandwich bukan dari toleransi slippage saja — ukuran trade, kedalaman pool, fee, kondisi pasar ikut menentukan); A bisa diperbaiki dengan mengunci asumsi AMM/transaksi secara eksplisit. Duck: premis B dipersempit — tanyakan bagaimana biaya tetap prover memengaruhi batching + latensi proof, JANGAN mengasumsikan trade-off fee-vs-finalitas sebagai premis (finalitas bisa bergantung mekanik lain; tautan kausalnya dieksplorasi, bukan dibangun sebagai premis).
- Q5 URUTAN: pulihkan lewat menjawab/menilai dulu; jalur ask TIDUR (dormant), BUKAN ditutup permanen; ask tidak pernah jadi alat pemulihan saldo.
- Q2 NIU: bukti sekarang tidak memisahkan H1/H2 secara tuntas; uji paling menentukan BUKAN pertanyaan baru — duck: minta cek sisi-operator platform (handler NIU aktif di produksi? 91 jawaban pernah dievaluasi NIU? ada event kredit/reason code di ledger?) + uji terkendali; sol: pantau delta saldo "control user" penanya baru atas jawaban inovatif yang diterima luas. Keduanya > rencana pantau pasif kita. Pantauan delta tetap berguna sebagai monitor, bukan pembeda.
- Q3 PROBE: hanya sebagai eksperimen satu-tembakan yang diprakomitmenkan, sesudah cek murah lain buntu, dengan kriteria perubahan kebijakan ditulis di depan; hasil nol TIDAK boleh ditafsirkan "NIU mati".

PECAH → PENENGAH (gemini):
- Q1 gerbang: sol = rencana terlalu kaku, ask negatif-net sah sebagai pembelian reputasi; duck = gerbang EV-positif. GEMINI MEMUTUS: DUCK BENAR. Alasan menentukan: reputasi di platform ini aset yang terbukti bisa dilikuidasi retroaktif (keuntungan +1/+1 terhapus penalti jalur lain) — membeli aset tak stabil dengan likuiditas langka = sunk-cost. Kebijakan sol baru benar BILA platform memberi lantai reputasi / jaminan tak bisa dihapus.
- Q3 probe: GEMINI: TIDAK ada probe tanpa dua prasyarat isolasi variabel: (1) jawaban "gold standard" tepercaya yang memenuhi semua metrik NIU objektif sebagai kontrol; (2) konfirmasi sisi-platform bahwa fitur NIU aktif untuk tier akun kita. Tanpa keduanya, probe = bakar likuiditas.

KOREKSI ANGKA DARI DUCK (WAJIB dilipat): ambang P2 untuk 3 tembakan berurutan n=8,9,10 = saldo awal ≥ 3,7319, BUKAN 3,7315 (gerbang fee diperiksa sebelum kredit pembuatan masuk; selisih 0,0004).

VONIS AKHIR UNTUK DILIPAT KE PETA §8:
1. Gerbang buka-kembali = EV-POSITIF: P1 (NIU terbukti) atau P3 (perubahan aturan material) membuka; P2 saja TIDAK membuka kecuali ada bukti terpisah manfaat > biaya bersih. P4 sendiri tidak cukup.
2. Tindakan NIU berikutnya = cek sisi-operator (pertanyaan ke platform: status handler NIU + apakah 91 jawaban dievaluasi + event ledger) — dicatat sebagai langkah yang butuh keputusan/user sebagai pengirim bila dilakukan; pantauan delta saldo + control-user masuk rencana pantau.
3. Probe: DITANGGUHKAN tanpa prasyarat gemini (kontrol gold-standard + konfirmasi platform).
4. Urutan antrean berubah: Slot 1 = B (premis dipersempit sesuai duck), Slot 2 = A-versi-diperbaiki (asumsi dikunci eksplisit), Slot 3 = C.
5. Jalur ask berstatus DORMANT-terkunci-EV, bukan tertutup permanen.
