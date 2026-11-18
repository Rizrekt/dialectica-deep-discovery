# SINTESIS FRONTIER PERBAIKAN JALUR 1 — tuntas 2026-11-18 10:38–10:42 WIB
Kursi: duck.ai GPT-6 Luna (utama, cloud) + gpt-5.6-sol (co-advisor, CrowLLM). KONVERGEN 4/4 — penengah tidak dipanggil. Mentah: duck-answer.md, sol-answer.md. Paket: FRONTIER-PAKET-PERBAIKAN-JALUR1.md.

DESAIN FINAL (ditetapkan dari vonis):
- Q1 = OPSI A FINAL. Lane cepat dibiarkan hangus untuk sekarang; Opsi B ditunda bersyarat (dibangun hanya bila run terukur membuktikan nilai peluang cepat yang hilang melebihi cakupan telat + biaya B).
- Q2 = FAIL-CLOSED FINAL, dengan PENYEMPURNAAN DUCK: skip 6 jam bukan kebijakan akhir — baris yang dilewati WAJIB bisa dipertimbangkan ulang saat klasifikasi berubah / tiket jatuh tempo (reconsideration, bukan fail-open warisan). Fail-open terukur DITOLAK dua kursi (sol: bakar 9/10 adalah bencana yang tak boleh diulang; ambang aman tidak menyelamatkan).
- Q3 = EVALUASI GANDA FINAL (layar pra-klaim + veto detik-kirim), dengan tata cara duck: utamakan data pick yang sudah tercatat sebelum menambah bacaan API; log kedua vonis + alasan perbedaan; "lolos pick, gagal kirim" diperlakukan sebagai race normal.
- Q4 = SEKUENSING KLAIM KONSERVATIF WAJIB: tidak ada klaim baru selagi hasil job sebelumnya belum terminal-pasti (atau timeout liveness server lewat). Layar saja dinyatakan TIDAK CUKUP oleh dua kursi.

TUGAS LIPAT: tetapkan desain final di PERBAIKAN-KOLAM-DOKTRIN-2026-11-18.md + terapkan penyempurnaan Q2 (reconsideration) dan tata cara Q3 (log ganda + prioritas data pick) dan gerbang Q4 (cek keadaan job sebelum klaim) ke bangunan di lapisan provider kita — masing-masing dengan tes; bila satu butir ternyata tidak bisa diterapkan bersih di lapisan kita (mis. skip 6 jam hidup di klien stok), catat sebagai KETERBATASAN TERCATAT + ukuran yang akan memutuskannya, jangan memaksa tambalan kotor. Suite penuh tetap hijau; serve tetap mati; nol klaim.
