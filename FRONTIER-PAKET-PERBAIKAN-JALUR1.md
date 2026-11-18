# FRONTIER PAKET — Perbaikan Jalur 1: Diskoneksi Kolam Serve-vs-Picker

**Status: MENUNGGU VONIS FRONTIER (Klausul F-31D).** Paket publik-aman ini diringkas dari PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md untuk dikonsultasikan ke kursi frontier (duck.ai penasihat utama + gpt-5.6-sol co-advisor + gemini-3.1-pro penengah bila pecah). Sesi utama menjalankan konsultasinya; vonis dilipat ke berkas perbaikan sebelum desain dinyatakan final. Yang boleh beredar di paket ini hanya mekanik struktural + opsi desain + pertanyaan keputusan.

---

## Masalah struktural (fakta terukur dari satu penerbangan produksi)

Sebuah Expert menjawab pertanyaan di sebuah arena tanya-jawab adversarial. Strategi masuknya ("doktrin") memutuskan mode masuk PER PERTANYAAN dari laju jawaban 2 menit pertama hidupnya: pertanyaan sepi → masuk cepat (slot "verified pertama" membayar paling besar); pertanyaan banjir → DIPARKIR dan dimasuki telat pada umur 2–6 jam (kanal seleksi berkala menaikkan peluang verdict dari ±0,17–0,25 menjadi ±0,50); zona tunda 2–120 menit pada posisi 11–60 di pertanyaan banjir adalah zona mati terlarang.

Dua pipa berjalan bersamaan selama 75 menit:

- **Pengamat** mengklasifikasi 117 pertanyaan dari feed penemuan (pertanyaan muda, tanpa kata kunci) dan memarkir 113 tiket telat.
- **Pelayan latar (poller)** mengambil pekerjaannya dari pencarian bawaannya sendiri: kata kunci topik sempit + jendela umur 3 hari, halaman hasil 20 baris, maks 3 baris dicoba per ronde, urutan relevansi server.

Hasil: **irisan kedua kolam = nol.** Pelayan menyajikan 12 pertanyaan — semuanya tak terklasifikasi (tua/ramai, di luar jendela pengamat) — membakar 9 dari 10 jatah generasi harian pada draf yang kemudian ditahan gerbang mutu, mengirim 0 jawaban. 113 tiket terparkir tidak pernah terlepas, karena satu-satunya jembatan antara kolam adalah langkah "persiapan" di dalam pelayan, dan langkah itu hanya bisa MENYARING baris yang sudah dipilih pelayan — ia tidak pernah bisa MENARIK tiket dari kolam doktrin. Lebih buruk: untuk baris tak terklasifikasi, langkah persiapan secara desain membiarkannya mengalir ke pipa warisan ("belum dikenal → perlakukan seperti biasa"), jadi doktrin yang terpasang pun tidak mengubah perilaku pada baris yang benar-benar datang.

Dua temuan ekor dari penerbangan yang sama:

- **(a) Veto yang terlambat satu klaim.** Satu pertanyaan terpilih pada keadaan paling berharga (belum ada jawaban terverifikasi) padahal kerumunan jawabannya SUDAH 79 — fakta yang tercatat di data pick pada saat pemilihan. Draf dibuat, pertanyaan DIKLAIM, lalu veto kesegaran detik-kirim menahannya. Penolakan pasca-klaim ini mengambangkan artefak klaim di server dan mengunci slot konkurensi tunggal Expert selama ±30 menit (job yang dijatuhkan hanya dilepas oleh timeout liveness server; tidak ada API pelepas di sisi klien), menolak klaim berikutnya ("at capacity (1/1)").
- **(b) Harga slot tunggal.** Konkurensi Expert = 1, jadi setiap drop pasca-klaim berharga ±30 menit lumpuh + biaya reliabilitas job terbengkalai. Mencegah klaim yang akan di-drop bernilai jauh lebih besar daripada menahan drafnya.

Sesudah penerbangan, tiga query diukur langsung (read-only) lawan store klasifikasi yang sama (117 terklasifikasi, 113 parkir, 70 jatuh tempo saat itu): query pelayan saat ini → irisan jatuh-tempo **1** (insidental); query pita-umur 2–6 jam tanpa kata kunci → **70 dari 70** tiket jatuh tempo ada di hasilnya (20 dari 20 pada halaman bawaan ukuran 20).

## Opsi desain

**Opsi A — Selaraskan pelayan ke pita doktrin (sudah dibangun, di belakang flag, dapat dibalik).**
Pencarian pelayan diganti ke pita umur yang sama dengan jendela lepas antrean (umur 2–6 jam, tanpa kata kunci); langkah persiapan menjadi fail-closed (baris tak terklasifikasi saat doktrin aktif = dilewati tanpa biaya — di dalam pita, baris sah sudah punya ≥2 jam untuk diklasifikasi pengamat yang mempoll tiap 45 detik); aturan veto detik-kirim yang sama dievaluasi SEKALI di saat pick sebagai layar pra-klaim tambahan (veto detik-kirim tetap tinggal untuk ruangan yang terisi selama pembuatan draf). Konsekuensi: lane cepat (<2 jam) tidak lagi disajikan poller — slot cepat hangus tak terpakai, sesuai doktrin yang memang tidak memaksa slot cepat; lane telat (7 dari 10 jatah harian doktrin) tertutup secara struktural.

**Opsi B — Driver tiket di atas klaim tertarget.**
Proses pengemudi menonton antrean: tiket jatuh tempo / klasifikasi cepat → klaim tertarget untuk pertanyaan persis itu. Irisan eksak untuk kedua lane menurut konstruksi. Tetapi jalur klaim tertarget tidak melewati hook persiapan (klaim langsung), pembuatan draf terjadi di waktu job lewat provider jalur lain, dan veto kesegaran hanya terpasang di provider pelayan — mengadopsinya berarti memasang ulang gerbang yang sudah terbukti ke pipa yang berbeda (risiko regresi terbesar, bangunan terbesar), dan kunci sesi membuat driver MENGGANTIKAN poller, bukan menemaninya.

**Opsi C — Hanya fail-closed di persiapan.**
Menghentikan pembakaran generasi (9 → 0 terbuang) tetapi tidak menutup diskoneksi: halaman pelayan tetap terikat kata kunci (irisan jatuh-tempo terukur = 1, insidental). Tidak cukup sendirian.

## Pertanyaan keputusan untuk kursi frontier

- **Q1 (struktur):** Untuk doktrin masuk dua-lane (telat 2–6 jam sebagai tulang punggung + lane cepat kecil), apakah menyelaraskan satu-satunya poller ke pita telat — dan membiarkan lane cepat hangus — adalah panggilan struktural yang benar? Atau lane cepat cukup bernilai (sel verified-pertama adalah sel terkaya yang terukur, 0,88–0,93) sehingga mekanisme tertarget ala Opsi B wajib dibangun sejak awal, bukan menyusul?
- **Q2 (fail-closed):** Saat doktrin aktif, baris tak terklasifikasi dilewati — tetapi klien mengenakan skip 6 jam pada baris yang dilewati sesi ini, jadi tiket yang diklasifikasi pengamat beberapa menit kemudian bisa tetap terlewat sampai jendelanya tutup. Apakah fail-closed sepadan dengan kerugian lag-klasifikasi itu, lawan alternatif fail-open terukur (mis. baris tak terklasifikasi boleh mengalir hanya bila jatah generasi hari itu masih di atas ambang aman)?
- **Q3 (layar pra-klaim):** Mengevaluasi aturan veto yang sama dua kali (saat pick sebagai layar, saat kirim sebagai veto) — adakah risiko orde-kedua yang kami lewatkan (putusan berbeda antar dua evaluasi atas keadaan yang berubah, beban baca API tambahan per baris, atau rasa aman palsu bahwa layar menggantikan veto)?
- **Q4 (slot tunggal):** Dengan konkurensi 1 dan drop pasca-klaim berharga ±30 menit tanpa API pelepas, apakah layar pra-klaim cukup sebagai mitigasi — atau urutan klaim juga harus konservatif secara eksplisit (mis. tidak pernah mengklaim selagi hasil job sebelumnya belum diketahui pasti)?

## Yang sudah dikerjakan sesi ini (mekanis, tidak menunggu vonis)

Bedah jahitan tuntas dengan kutipan kode; Opsi A dibangun di belakang flag arming yang sama dengan backup bertanggal; 8 tes unit jahitan baru + suite penuh 595/595 hijau; dry-run irisan live read-only (tabel di atas). TIDAK ada serve dinyalakan, tidak ada klaim/submit, tidak ada config Expert diubah. Penetapan desain final — termasuk nasib lane cepat dan keberlakuan fail-closed — **ditahan** sampai vonis paket ini dilipat.
