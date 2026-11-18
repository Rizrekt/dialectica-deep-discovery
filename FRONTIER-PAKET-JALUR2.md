# PAKET KONSULTASI FRONTIER — JALUR 2 (VERIFIER), Dialectica

Disusun: 2026-11-18 · Untuk: duck.ai (utama) + gpt-5.6-sol (co-advisor) +
gemini-3.1-pro (penengah bila pecah) · Status: MENUNGGU KONSULTASI SESI UTAMA
(F-31D: konsultasi selesai + tercatat SEBELUM sintesis final dilaporkan).

Materi di berkas ini publik-by-design: mekanik platform yang diterbitkan
platform sendiri + statistik analitik publik platform per 2026-11-18.
Tidak ada logika gerbang internal, rubrik internal, kredensial, atau data
akun pribadi di sini.

## Konteks publik

Dialectica adalah marketplace pengetahuan terverifikasi: penanya membuat
Question, Expert menjawab, Verifier independen menilai tiap Answer dengan
checklist arena (di arena General: 4 cek — sitasi, penalaran, ketidakpastian,
cakupan; verdict "compliant" hanya bila keempatnya lolos). Answer menjadi
Verified bila panel mencapai ≥2 support dan 0 refutasi (clean sheet — satu
refutasi membunuh), dan falsified sebaliknya. Verifier dibayar per verifikasi
yang SEJALAN dengan hasil akhir Answer itu; formula esai resmi platform
menurun menurut urutan kedatangan (verifier awal paling mahal per unit,
maksimum 1,0 $TRUED).

Statistik publik arena General (analitik platform, 2026-11-18):
- Strategi verifier "economist" (ambang reward minimum; parameter resmi
  minReward 0,1–1,0, bawaan 0,6): 11 agent aktif, 313 rb verifikasi terkirim,
  tingkat sepakat 90,9%, rata-rata 0,82 $TRUED/unit, median penghasilan
  seumur per agent 6.373, total 257 rb $TRUED.
- "consensus_builder" (mengisi celah verifikasi; berhenti sesudah N support):
  3 agent, 42 terkirim, tingkat sepakat 94,9%, 0,64/unit, median 2,9.
- "first_responder" (tercepat menilai) dan "challenger" (menantang Answer
  yang sudah verified): 0 agent aktif, volume 0.
- Arena Forecasting: economist 0,84/unit, tingkat sepakat 88,6%, TETAPI
  reward ditahan sampai pertanyaan settle terhadap peristiwa dunia nyata
  (horizon bulan). Arena ketiga (benchmark) tertutup untuk publik.
- Volume platform meledak dalam ±7 hari terakhir (mayoritas pertanyaan dan
  verifikasi seumur platform lahir di jendela itu) — rezim banjir, bukan
  rezim sepi.
- Di sisi Expert (menjawab), strategi terbanyak justru median penghasilan
  per agent = 0 — uang terkonsentrasi di segelintir agent atas. Di sisi
  verifier, dua agent skala-rumah terlihat memproses ribuan verdict/hari.

## Desain yang sedang dibangun (ringkasan publik-aman)

Sebuah runner verifier untuk satu akun kecil yang hari ini hanya berperan
sebagai Expert:

1. Dibangun dry-run dulu: menyusun draf verdict atas Answer publik nyata
   tanpa mengirim apa pun; pendaftaran peran verifier adalah langkah
   terpisah yang terkunci di balik keputusan eksplisit pemilik akun.
2. Draf verdict disusun multi-lane (satu drafter mekanis lokal + dua lane
   model berbeda) dan dibandingkan kesepakatannya sebelum ada kepercayaan
   pada satu lane mana pun.
3. Gerbang konflik kepentingan di level pemilik: tidak pernah menilai
   Answer sendiri, Answer di Question sendiri, atau Answer pesaing pada
   Question yang dijawab sendiri — lebih ketat dari larangan minimum
   platform, sebagai pilihan kebijakan.
4. Mode kirim terkunci terpisah dari mode draf; arming-nya adalah tindakan
   tersendiri sesudah pendaftaran, bukan bawaan.
5. Reputasi (skor keandalan akun) bersifat per-pemilik dan dipakai bersama
   oleh peran Expert dan Verifier — kerusakan di satu peran menular ke
   akun yang sama.

## Pertanyaan keputusan untuk kursi frontier

**Q1 — Strategi masuk.** Dengan statistik publik di atas, strategi masuk
yang paling masuk akal untuk operator kecil: economist (main di ambang
reward), consensus_builder (mengisi celah — sampel kecil tapi tingkat
sepakat tertinggi), atau first_responder (kolam kosong total — tidak ada
yang memainkan kecepatan)? Apa alasan terkuat untuk pilihan itu, dan
statistik apa yang akan membuktikan pilihan itu salah dalam 2 minggu?

**Q2 — Postur verdict.** Bayaran verifier mensyaratkan verdict SEJALAN
dengan hasil akhir panel, bukan "benar" secara independen; dan agregasi
panel adalah clean sheet (1 refutasi membunuh). Postur mana yang lebih
baik untuk akun kecil berisiko reputasi bersama: ketat pada checklist
(fail bila ragu pada satu cek) atau mengikuti arus konsensus yang paling
mungkin? Bagaimana menimbang penghasilan per unit lawan risiko menjadi
satu-satunya suara yang berbeda?

**Q3 — Arena pertama.** General (bayar saat verdict, 0,82/unit, banjir)
lawan Forecasting (0,84/unit tapi escrow berbulan-bulan, volume jauh
lebih kecil)? Untuk akun yang tujuannya membuktikan jalur ini hidup
secepat mungkin dengan risiko terkecil, arena mana dulu — dan apakah
perbedaan 0,02/unit pernah sepadan dengan escrow?

**Q4 — Urutan terhadap jalur Expert.** Akun yang sama sedang menjalankan
operasi menjawab (Expert) dengan doktrin antreannya sendiri. Verifier
berbagi: anggaran relay model yang sama, perhatian operator yang sama,
dan reputasi akun yang sama. Jalan paralel dari hari pertama, atau
sekuensial (verifier hanya sesudah doktrin menjawab terbukti dibayar)?
Fakta apa yang harus mengubah jawaban itu?

**Q5 — Skala minimum yang layak.** Penghasilan lane ini terkonsentrasi:
median agent economist 6.373 seumur hidup, tetapi dua agent skala-rumah
memproses ribuan verdict/hari dan kemungkinan memegang mayoritas volume.
Dengan kapasitas realistis operator kecil (puluhan sampai beberapa ratus
verdict/hari memakai lane model), apakah lane ini layak dioperasikan —
di volume harian berapa titik impas operasionalnya (biaya model + waktu
operator) tertutup pada 0,82/unit dan tingkat sepakat ±91%? Bila tidak
layak di skala kecil, kondisi apa yang membuatnya layak?

## Yang diminta dari tiap kursi

Vonis per pertanyaan (pilih satu arah + alasan terkuat + satu bukti yang
akan membatalkan vonis itu). Ketidaksepakatan antar-kursi ditandai untuk
penengah. Hasil konsultasi dilipat ke PETA-JALUR-2-VERIFIER-2026-11-18.md
bagian "VONIS FRONTIER & PERUBAHANNYA" sebelum peta dinyatakan final.
