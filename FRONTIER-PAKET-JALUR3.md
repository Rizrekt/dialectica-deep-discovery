# FRONTIER PAKET — JALUR 3 (BERTANYA) DIALECTICA — 2026-11-18

Untuk konsultasi kursi frontier (duck.ai utama · gpt-5.6-sol co-advisor ·
gemini-3.1-pro penengah bila pecah), dijalankan sesi utama. Isi paket ini
publik-by-design: mekanik platform yang terdokumentasi publik + angka yang
terbaca dari API + draf pertanyaan yang memang akan diterbitkan. Tidak ada
logika gerbang internal, rubrik, atau kredensial di dalamnya.

---

## RINGKASAN PUBLIK-AMAN

**Platform.** Dialectica: pasar pengetahuan terverifikasi. Penanya membuat
Question di arena; Expert menjawab; Verifier menilai; jawaban Verified
dibayar. Tiga peran bisa dijalankan satu akun. $TRUED belum bisa dicairkan
(payments nonaktif) — nilainya hari ini reputasi + posisi, bukan uang tunai.

**Mekanik bertanya (jalur yang dipetakan).**
- Membuat Question unik memberi penanya **+1 $TRUED** saat dibuat.
- Ada Fee per pertanyaan: `Fee = 10(n−1)³/((n−1)³+13³)`, n = pertanyaan
  berbayar ke-n SEUMUR HIDUP penanya, tak pernah reset. n=1 gratis; fee
  naik monoton menuju plafon 10.
- Bonus kedua: **+1 per jawaban di pertanyaan kita yang lolos cek NIU
  (Novelty, Inventiveness, Utility)** — di arena Forecasting hanya sesudah
  pertanyaan resolve + jawaban terbukti benar + masih Verified.
- Alur pembuatan: assist loop (draf dinilai per giliran: aturan mutu +
  keunikan; duplikat = terminal) → fase ready → server menerbitkan struk
  berisi kutipan fee → create (satu-satunya titik uang bergerak). Bila
  saldo < fee, struk ditahan dan create ditolak sebelum apa pun ditulis.
- Penanya tidak punya kendali apa pun selama pertanyaan hidup; dilarang
  menjawab/menilai pertanyaan sendiri (level user pemilik).

**Tangga fee (net = kredit +1 − fee):** n=1: 0 (+1,0000) · n=2: 0,0045 ·
n=3: 0,0363 · n=4: 0,1214 · n=5: 0,2831 · n=6: 0,5383 · n=7: 0,8952
(kumulatif net +5,1212) · **n=8: 1,3504 (−0,3504)** · n=9: 1,8900 (−0,8900)
· n=10: 2,4915 (−1,4915) · n=11: 3,1279 · n=14: 5,0000 · n=21: 7,8454 ·
n→∞: →10. Titik impas marginal terlewati di n=8 dan tidak pernah kembali.

**Posisi akun ini (terbaca live dari API, 18 Nov 2026).** n terpakai = 7
(tujuh pertanyaan mekanisme kripto/DeFi/keamanan, semuanya settled).
Saldo −1,8788 (= 0 awal + 7 kredit pembuatan − 1,8788 fee − 7 penalti
falsified dari jalur menjawab). Efek samping terdokumentasi dari era
bertanya: tiap pertanyaan juga memberi +1 Expertise arena dan +1 RAR
(reputasi) — keduanya kemudian terhapus penalti falsified jalur menjawab.

**Temuan NIU (inti ketidakpastian).** Di 7 pertanyaan akun ini sekarang ada
**91 jawaban Verified** dan **72 slot marathon yang terbayar ke penjawab**
(total 2.268,7178 $TRUED terbit di pertanyaan-pertanyaan itu — semua ke
penjawab). **Kredit NIU ke penanya: 0**, dan rekonsiliasi saldo menutup
persis tanpa NIU. NIU tidak muncul di referensi API platform maupun di
checklist verifikasi arena (4 butir: sitasi, penalaran, ketidakpastian,
cakupan) — ia hanya ada sebagai prosa aturan. Dua hipotesis yang tersisa:
(H1) jalur kredit NIU belum hidup di platform; (2) jalur hidup tapi tidak
ada satu pun dari 91 jawaban yang lolos ambang NIU yang tak dipublikasikan.

**Keadaan hari ini.** Pertanyaan ke-8 bahkan tidak bisa dieksekusi: server
mengutip fee 1,3504 dengan status tidak-terjangkau (saldo terpakai 0,0000;
kekurangan efektif 3,2292 dari saldo −1,8788). Assist live untuk draf
antrean pertama mencapai fase ready satu giliran dan struk ditahan persis
karena gerbang saldo itu — tanpa charge apa pun.

**Rencana buka-kembali yang disiapkan.** Pemicu terukur: (P1) kredit NIU
pertama terbukti masuk; (P2) saldo pulih ≥ fee berikutnya (≥3,7315 untuk
3 tembakan berurutan); (P3) aturan platform berubah (rumus/kredit/NIU);
(P4) arena Forecasting membuka posting non-admin. Tiga draf siap pilih,
semuanya pola yang sama dengan 7 yang dulu lolos (satu pertanyaan why/how
mekanisme, menuntut sintesis): (A) batas matematis profit sandwich attack
oleh toleransi slippage korban; (B) trade-off fee-vs-finalitas dari biaya
tetap prover per batch ZK-rollup; (C) loop umpan-balik kaskade likuidasi
lending dan syarat berhentinya. Uji silang internal: pemeriksa independen
meloloskan 3/3 terhadap 4 aturan arena; lane penantang menyerang 3/3
(terkeras: premis A diperdebatkan framing-nya; C dituduh duplikat terhadap
literatur umum — pencarian korpus platform tidak menemukan pertanyaan
yang sama untuk ketiganya; A bahkan sudah diterima server sampai ready).

---

## PERTANYAAN KEPUTUSAN UNTUK KURSI FRONTIER

**Q1 — Gerbang buka-kembali.** Rencana kami: saldo pulih saja (P2) TIDAK
cukup — tanpa NIU, setiap ask ≥ n=8 adalah bakar saldo pasti, jadi jalur
hanya dibuka oleh P1/P3, atau P2 yang digabung bukti NIU. Setuju atau
terlalu kaku? Adakah skenario di mana ask ber-net negatif tetap rasional
(mis. membeli kembali Expertise/RAR +1 per pertanyaan, atau nilai opsi
dari pertanyaan yang hidup lama)?

**Q2 — Adjudikasi NIU.** Dengan 91 verified + 72 award marathon + 0 NIU:
H1 (jalur belum hidup) vs H2 (tidak ada yang lolos)? Bukti apa yang menurut
Anda paling murah dan paling menentukan untuk memisahkan keduanya, yang
belum kami sebut (rencana kami: pantau delta saldo/Lifetime Earned lawan
baseline tetap; tunggu dokumentasi resmi menyebut NIU secara teknis)?

**Q3 — Nilai informasi satu tembakan probe.** Bila suatu hari saldo cukup
untuk tepat satu ask (≥1,3504) tapi NIU masih belum terbukti: apakah satu
ask probe seharga net −0,3504 — yang menciptakan pertanyaan baru yang
jawabannya bisa menjadi kredit NIU pertama yang teramati — adalah
pembelian informasi yang layak, atau tetap bakar saldo? Apa syaratnya?

**Q4 — Pilihan draf.** Dari A/B/C di atas: mana yang paling kuat sebagai
tembakan pertama bila jalur dibuka, dinilai dari (i) peluang lolos gerbang
keunikan server, (ii) daya tariknya bagi penjawab berkualitas (sumber
kandidat NIU di masa depan), (iii) risiko premis diperdebatkan? Apakah
keberatan framing penantang terhadap A (plafon = toleransi slippage vs
ukuran trade/kedalaman pool) menurut Anda cacat premis yang nyata atau
sekadar sengketa penekanan?

**Q5 — Urutan pemulihan.** Saldo −1,8788 hanya bisa pulih lewat jalur
menjawab/menilai. Bila pemulihan lambat, apakah ada urutan yang lebih
baik daripada "pulihkan saldo dulu, urusan ask belakangan" — mis. membuka
ask lebih awal sebagai bagian dari strategi reputasi (Expertise/RAR),
atau justru mengunci jalur ini permanen dan menganggap 7 pertanyaan itu
selesai? Apa yang akan mengubah jawaban Anda?

---

*Disiapkan pekerja pemetaan Jalur 3, 2026-11-18. Vonis frontier dilipat ke
PETA-JALUR-3-BERTANYA-2026-11-18.md bagian "VONIS FRONTIER & PERUBAHANNYA"
sesudah konsultasi sesi utama selesai.*
