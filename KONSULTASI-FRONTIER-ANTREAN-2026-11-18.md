# KONSULTASI FRONTIER — ANTREAN VERDICT & DOKTRIN MASUK (2026-11-18)

Perintah user 08:05: "tetap ya bro, libatkan model kelas frontier kita" + "ydh jalan" 08:09.
Bahan: PAKET KONSULTASI FRONTIER dari `STUDI-ANTREAN-VERDICT-2026-11-18.md` (publik-aman, byte-sama ke dua kursi).
Kursi: duck.ai GPT-6 Luna (penasihat utama, via browser, Reasoning mode, chat 4e05d957) ·
gpt-5.6-sol via CrowLLM (co-advisor wajib, 1 panggilan, 4,3 dtk) ·
gemini-3.1-pro via CrowLLM (penengah, dipanggil karena Q2 pecah, 1 panggilan, 3,6 dtk).
Anggaran relay hari ini: 2 panggilan konsultasi (sol + gemini) — dalam pagar.

## Vonis per pertanyaan

### Q1 — Doktrin masuk
- **sol: (b) telat 2–6 jam.** Campuran dinilai tidak efisien; zona banjir posisi 1–25 = jebakan 0,14–0,23. Pemicu mode versinya: laju jawaban/menit (>15/mnt dalam 10 mnt pertama → mode tunda; <2/mnt → instan sah karena posisi 1–3 = 0,88–0,93).
- **duck: (c) campuran 7 telat : 3 cepat, pemicu keras per pertanyaan.** Sinyal utama laju 2 menit pertama: ≤5 jawaban → MODE CEPAT (target posisi 1–3); >10 → MODE TELAT (jendela 2–6 jam, diferensiasi ≥15%); 5–10 → tunggu 30 menit lalu putuskan dari laju lanjutan. Sinyal konfirmasi kerumunan saat masuk: ≤10 masuk; 11–60 banjir jangan; 61+ boleh dengan diferensiasi kuat. Slot cepat yang tak menemukan pertanyaan sepi TIDAK dipaksa pakai.
- **Sintesis sesi utama: KONVERGEN pada substansi.** Mesin utama = telat berdiferensiasi; cepat hanya untuk pertanyaan terbukti sepi; pemicu = laju masuk. Bentuk duck (c) adalah perincian dari (b) sol — pemicu sol sendiri mengakui mode instan untuk pertanyaan sepi. Perbedaan sisa hanya soal cadangan slot eksplisit (3 cepat) vs pengecualian ad hoc.

### Q2 — Penjelasan keunggulan telat di banjir — PECAH → penengah
- **duck: (i) utama** (jadwal seleksi marathon berkala), (ii) sekunder-penguat. Argumen: yang runtuh adalah penugasan (85,9%→32,6%) bukan penilaian; juara marathon terkonsentrasi di posisi ±50 = profil jadwal pindai; konversi settled ±7%/30 jam = sidik jari kanal berkala. Pengukuran pembeda tertajam usulan duck: distribusi lag submit→verdict dipisah keanggotaan kolam marathon; pendukung murah: tingkat penugasan menurut mutu independen.
- **sol: (ii) utama** (noise bot awal menyumbat panel). Argumen kuncinya: median lag tetap 11 menit → sistem tidak lambat.
- **gemini (penengah): memihak duck/(i).** Menyebut argumen median-lag sol sebagai **bias survivorship** (lag hanya dihitung dari yang ber-verdict); konversi settled = bukti batching berkala yang tak bisa dijelaskan teori noise; anomali posisi 61+ (0,51) cocok dengan penjaringan pindai tertunda, bukan penyaringan bot.
- **Status: (i) BERDIRI sebagai penjelasan utama** (2 kursi + data); (ii) tetap hidup sebagai penguat sekunder. Pengukuran pembeda duck (lag per kanal) = kandidat lab berikutnya untuk konfirmasi empiris langsung.

### Q3 — Sedikit-telat vs volume di bawah cap keras
- **Keduanya sepakat penuh:** sedikit-telat-terdiferensiasi menang; titik balik = **0,44** (dataran posisi normal); telat 2–6 jam 0,50 sudah melewatinya sebelum bonus Innovator +10 dan akses kolam marathon 302/302 dihitung. Di bawah cap 10, "volume" bukan strategi — tiap slot zona mati (0,14–0,25) adalah pemborosan yang tak tertebus.

## Paket doktrin yang disodorkan ke user (keputusan user, bukan eksekusi)
- **Opsi A — Campuran 7:3 berpemicu (duck):** 7 slot telat 2–6 jam berdiferensiasi ≥15% + maks 3 slot cepat khusus pertanyaan ≤5 jawaban/2 menit pertama; mode diputus per pertanyaan dari laju masuk 60–120 detik pertama.
- **Opsi B — Telat murni (sol):** semua slot telat di rezim banjir; cepat hanya pengecualian langka.
- **Opsi C — Doktrin lama (kejar awal/viso-0):** ditolak data (zona mati 0,14–0,25; pilot jatuh persis di sana).
- Rekomendasi sesi utama: **A** — dasar multi-sumber: studi 66 ISR/6.188 ISO + kohort (juara Marathon posisi median ±50; juara Pioneer posisi 2–3 di pertanyaan berakhir 53–65) + dua kursi frontier konvergen di mesin telat; A satu-satunya yang mempertahankan sel EV tertinggi sistem (posisi 1–3 pertanyaan sepi = 0,88–0,93 × Pioneer +20) tanpa membakar slot di zona mati.
- Adopsi doktrin ≠ nyala: implementasi (picker/jendela tunda/pemicu laju di kode) = kerja lab; nyala tetap kata terpisah user, rezim pilot (mini-batch, kill-metric) tetap berlaku.
