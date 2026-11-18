# SINTESIS FRONTIER JALUR 2 (VERIFIER) — konsultasi tuntas 2026-11-18 10:15–10:21 WIB
Kursi: duck.ai GPT-6 Luna (utama, browser cloud) · gpt-5.6-sol (co-advisor, CrowLLM). Penengah gemini TIDAK dipanggil: tidak ada perpecahan level-keputusan (kedua kursi searah di kelima pertanyaan; satu nuansa Q2 dicatat, bukan sengketa). Mentah: duck-answer.md + sol-answer.md di folder ini. Paket: FRONTIER-PAKET-JALUR2.md.

VONIS PER PERTANYAAN (konvergen):
- Q1 STRATEGI MASUK = economist, ambang bawaan 0,6 (minReward). consensus_builder ditolak sebagai utama (sampel 42 tak sahih + 0,64/unit). first_responder DITOLAK KERAS dua kursi: kolam kosong bukan peluang — agent rumah punya latensi yang tak bisa disaingi relay model multi-lane (jebakan kecepatan). Pembatal terukur: bila ≤14 hari economist per unit turun < 0,50 (ambang sol) atau bersih per jam-operator economist < gap-filling (ambang duck) → evaluasi ulang.
- Q2 POSTUR = KETAT pada checklist 4 cek; verdict paksa pada kasus ambigu DILARANG — abstain/draf saja (duck eksplisit; desain runner kita memang multi-lane + abstain, sesuai). Nuansa sol (anticipasi konsensus sebagai sinyal keyakinan) dicatat sebagai SINYAL, bukan pengemudi verdict. Reputasi bersama = alasan penguat dua kursi.
- Q3 ARENA PERTAMA = General. Selisih 0,02/unit tak pernah sepadan escrow berbulan-bulan Forecasting untuk tujuan membuktikan jalur hidup tercepat.
- Q4 URUTAN = SEKUENSIAL untuk operasi LIVE: verifier live hanya sesudah doktrin Expert terbukti dibayar; dry-run draf verifier tetap jalan dari sekarang. Paralel live bersyarat ganda (Expert bersih-positif stabil + pilot verifier terkendali bersih-positif).
- Q5 SKALA = pilot terbatas terukur, bukan asumsi bisnis. CATATAN UKUR DUCK (wajib masuk peta): 0,8217/unit dari analitik kita adalah rata-rata TEREALISASI per verdict TERKIRIM (sudah memuat yang meleset) → EV per kiriman = 0,8217, JANGAN dikali 0,909 lagi. Sol memperkirakan kebutuhan ±200 verdict/hari untuk menutup overhead infrastruktur multi-lane pada asumsi biayanya — perlakukan sebagai hipotesis biaya yang harus diukur dari log biaya kita sendiri, bukan fakta. Median seumur 6.373 tanpa basis waktu ≠ bukti untung harian.

IMPLIKASI KE BANGUNAN (untuk dilipat ke §6 peta):
1. Konfigurasi awal runner: strategi economist, minReward 0,6, arena general — sebagai DEFAULT TERTULIS di peta (keputusan final tetap di gerbang user saat registrasi).
2. Postur abstain dipertegas sebagai aturan desain (sudah ada di drafter: lokal abstain-naik; pertegas: ketidaksepakatan lane pada kasus ambigu = TIDAK ADA verdict, bukan mayoritas paksa).
3. Checklist bangun §5 ditambah gerbang urutan Q4: registrasi boleh disiapkan, tetapi ARMING mode kirim menunggu bukti Expert dibayar (sesuai doktrin yang sedang diuji mini-batch 3) — selaraskan redaksi checklist dengan ini.
4. Tambahkan butir ukur biaya: runner wajib mencatat biaya model per verdict sejak dry-run agar titik impas Q5 bisa dihitung dari angka sendiri pada uji 14 hari.
