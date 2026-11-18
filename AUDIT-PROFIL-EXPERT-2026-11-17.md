# Audit Profil Expert Dialectica — 2026-11-17 (BACA-SAJA)

> Perintah user 2026-11-17 02:16 WIB: cek dari sisi profil apa yang kurang & apa yang perlu direvisi pada agent kita di Dialectica + "Your Dialectica badges" itu apa dan badge kita apa saja.
> Sifat: BACA-SAJA TOTAL — nol ubah config, nol klaim/serve. Semua bacaan live via klien resmi `trued.py` v0.22.4 + endpoint yang dipakai klien itu sendiri. **Stempel baca: 2026-11-17 02:17–02:26 WIB.**
> Expert kita: `8522c990-d4f6-4155-a326-3c3c9802b950`, user `rizrekt`, arena `general`.

## A. PROFIL LIVE KITA (bacaan 02:17–02:19 WIB)

| Field | Nilai live | Sumber |
|---|---|---|
| Nama Expert (config.name) | **KOSONG ("")** — `agent show` mencetak placeholder "(Agent Name)" | agent show + payload config API |
| Tagline | **null (tidak pernah diisi)** | payload agent API |
| Icon | **null** | payload agent API |
| Nama akun user (level user, beda dari Expert) | `rizrekt` | /api/authext/user |
| Type / state / link | ISP / configured / **offline** (normal di luar jendela serve) | agent show |
| strategyType | **dynamic** (satu-satunya strategi yang mengizinkan klaim one-shot) | agent show |
| Parameter tersimpan (inert di bawah dynamic) | maxVisos 6 · strategyN 2 · minParaphrasing 0 · maxParaphrasing 2 | payload config API; MEKANISME §24.1: parameter innovation_focus, tidak ditampilkan/dipakai di dynamic |
| skipDeepEvaluation | False | agent show |
| maxConcurrency | **1** | agent show |
| contextWindowTokens | **TIDAK TERDEKLARASI** — field tidak ada sama sekali di config payload kita | payload config API (daftar kunci config lengkap terbaca: arenas, enabled, maxConcurrency, maxParaphrasing, maxVisos, minParaphrasing, name, pluginConfig, skipDeepEvaluation, strategyN, strategyType — tanpa contextWindowTokens) |
| Caps 24h | maxIsrs24h/maxUsd24h/maxTokens24h **unlimited [used 0/0/0]**, isActive True | agent show |
| warningThresholdPct | **80** | agent show |
| Saldo / LifetimeEarned / Expertise | **−1,8788 $TRUED / 0 / 0** (general 0) | /api/node/scores + status |
| RAR 118 per komponen | Reliability **−5** · Availability **29** · Reputation **94** | /api/node/scores |
| suspensionCount / suspensionEndsAt | **5** / 2026-11-14T00:43:20Z (sudah lewat — tidak sedang tersuspensi) | /api/node/scores |
| Jobs seumur Expert | **29 completed / 5 failed** (total 34) | payload agent API |
| Expert dibuat / config terakhir berubah | 2026-11-08T11:58Z / **2026-11-14T01:41Z** (profil tak disentuh sejak 14 Nov) | payload agent API |

## B. BADGES — APA ITU, DAN BADGE KITA

### B.1 Definisi resmi: hampir tidak ada — dan itu temuan utamanya

- **Satu-satunya penyebutan "badge" di seluruh sumber primer yang terjangkau adalah SKILL.md baris 138:** *"A Fee never reduces **Lifetime Earned**, which is what the leaderboard ranks and **what badges are gated on**."* Jadi: **badge = tonggak tampilan di profil yang DIGERBANG Lifetime Earned** — metrik yang sama yang menentukan peringkat leaderboard. Fee bertanya tidak menggerus LE, jadi badge tidak bisa turun karena bertanya; LE hanya bergerak oleh earning (+) dan falsified (−1).
- **Katalog badge TIDAK ADA di dokumen klien.** Bukti pencarian menyeluruh (2026-11-17 02:20–02:25 WIB):
  - `grep badge` di SKILL.md + references/{api,arenas,rules-of-the-game}.md → hanya baris 138 di atas.
  - `grep badge` di kode `trued.py` (6.369 baris) → **nol hit**. Klien tidak punya perintah/endpoint badge sama sekali; daftar 33 path API yang dipakai klien tidak memuat satu pun path badge/profil-publik.
  - Dua halaman wiki ekonomi & reputasi (`trued-token-economics`, `dialectica-reputation-and-verification-systems`, dibaca via `trued page`) → **nol penyebutan "badge"**.
  - Slug wiki `badges`, `achievements`, `dialectica-badges`, `reputation-and-badges` → semua NOT_FOUND.
- Yang ada di klien hanyalah notifikasi **`achievement_unlocked`** (trued.py baris 696, 982): notifikasi tonggak perolehan — membawa `scoreType` + `delta`, dan menurut MASTER §12.1 tonggaknya adalah Pioneer / Verified-novel / kemenangan Marathon. Artinya: notifikasi achievement **menyertai peristiwa earning** (+20/+10 itulah bayarannya), bukan pembayaran terpisah.
- **Kesimpulan jujur:** "Your Dialectica badges" di situs adalah seksi tampilan profil web yang isinya digerbang Lifetime Earned; daftar badge, ambang LE per badge, dan tampilannya **tidak dipublikasikan di dokumen/skill/klien/wiki yang bisa kita baca** — hanya bisa dilihat dari halaman profil web itu sendiri. Tidak ada dokumen yang menyatakan badge membayar $TRUED apa pun; payout tetap hanya 3 sel (Pioneer +20 / Innovator +10 / Marathon +10).

### B.2 Badge kita: **NOL — terbukti, bukan dugaan**

- Riwayat notifikasi kita (endpoint resmi, limit 500, terbaca 02:19 WIB): **79 baris** — sensus: 68 `subscribed_isr_marathon`, 6 `ask_fee_charged`, 5 `user_suspended`, **`achievement_unlocked` = 0**.
- `trued status` malam ini juga tidak mencetak baris "🎉 Unread rewards" apa pun.
- Konsisten dengan angka: **LifetimeEarned = 0** → di bawah gerbang badge pertama mana pun; dan 0 verified seumur rezim → tidak ada satu pun tonggak Pioneer/Innovator/Marathon yang pernah tercapai. (Kredit +1 per Question yang dulu kita terima memang datang **tanpa** notifikasi — MASTER §5.2 — jadi absennya achievement bukan artefak senyap; tonggak earning memang belum pernah terjadi.)

## C. PEMBANDING JUARA (dokumen: KULIT-1 2026-11-12, KORPUS-JUARA 2026-11-14)

| Dimensi | Kita (live 17 Nov) | Juara papan (bacaan 12–14 Nov) | Jenis |
|---|---|---|---|
| Expertise general | **0** | 181–425 (Adam 425, Febriyan 407, Mauldrop 394, Añoñi 316, DodolDuren 297) | AKIBAT — +1/verified, −1/falsified; bukan tuas (KULIT-1 §1.5: "akibat volume verified, bukan tuas yang dibuka lebih dulu"; Exp 33 pun cukup untuk #85) |
| LifetimeEarned | **0** | ribuan (Adam coins 5.156 pada 14 Nov) | AKIBAT — hanya naik lewat sel berbayar |
| Availability (bantalan REL) | **29** | 181–784 (Adam 784) | AKIBAT — +1 per job completed |
| Reliability | −5 | −1 s/d −210 (Adam −173, ditenggelamkan AV 784) | AKIBAT — mereka menoleransi REL sangat negatif karena AV raksasa; kita tidak |
| Reputation | 94 | 906–1.747 | AKIBAT — bergerak dengan verdict compliant |
| Verified / volume | 0 verified; 29 job completed seumur akun | pemenang 4,9–10+ jawaban/hari-aktif berkelanjutan | AKIBAT + kapasitas lane |
| Config profil (nama/tagline/icon) | semua kosong | tidak terukur dari dokumen kohort (klien tidak mengekspos profil Expert lain) | CONFIG — tapi tak ada bukti config tampilan memengaruhi payout/seleksi (MASTER: tak ada pengali payout dari strategi/arena/RAR/Expertise; seleksi job = efek strategi, bukan nama) |

## D. DAFTAR KURANG & REVISI (terurut prioritas)

| # | Item | Keadaan kita | Seharusnya / catatan | Jenis | Risiko menyentuh | Rekomendasi |
|---|---|---|---|---|---|---|
| 1 | **contextWindowTokens belum terdeklarasi** | field absen total dari config | MASTER §7.3: bisa dideklarasikan via `trued agent set contextWindowTokens=N`, min 8.000, ≥100.000 = standar. Kode klien (resolve/note_undeclared_context_window): tanpa deklarasi, platform mengukur prompt job ke batas standarnya sendiri, bukan ke model kita — model via provider-cmd bisa masih membaca saat batas job habis | **Config — BUTUH KEPUTUSAN** (nilai harus cocok jendela model lane yang benar-benar dipakai serve; lane berganti Vyce/GLM/dll, jendelanya beda) | Deklarasi terlalu kecil memotong konteks jawaban; terlalu besar dari jendela model nyata = prompt kepanjangan ditolak/truncate diam-diam | Angkat ke lab/revisi mingguan: tetapkan nilai dari jendela model lane utama pilot, baru set. Jangan set malam ini |
| 2 | **Nama Expert kosong** | config.name = "" sejak dibuat 8 Nov; tagline & icon null | Identitas tampil Expert tidak ada (akun user bernama rizrekt, Expert-nya anonim kosong) | **Config-aman** (satu `agent set name=...`) | Rendah; tidak ada efek payout/seleksi yang terdokumentasi. Tetap perubahan config = tulis ke server, lakukan sebagai keputusan bernama, bukan diam-diam | Keputusan user: nama apa. Kandidat wajar: samakan dengan akun (`rizrekt`). Tagline/icon opsional, nilai fungsionalnya tak terbukti — jangan dibesar-besarkan |
| 3 | **warningThresholdPct 80 menggantung tak berguna** | 80, tapi semua caps unlimited → persen dari tak-terhingga tidak pernah memicu peringatan apa pun | Peringatan spending server praktis MATI; rem volume nyata kita adalah rem internal (cap serve 10/hari-UTC + tangga RAMP + kill-metric), bukan server | Config-aman, **tak perlu disentuh sendiri** | Mengubah angka ini saja = nol efek. Bahayanya ilusi aman bila dikira rem | Biarkan; bila suatu hari caps dibuat finite, set ulang threshold bersama keputusan caps-nya |
| 4 | **Caps server unlimited** | unlimited [used 0], isActive True (flip disengaja 10 Nov 19:16) | Bukan kekurangan — keputusan tercatat; jaring pengaman server memang absen BY DESIGN | Config — **jangan diubah tanpa keputusan fase** | Menyetel cap finite dari server bisa mengunci tembakan sah di tengah jendela (pelajaran spending-limit 8 Nov) | Pertahankan; rem tetap di lapisan internal yang bisa diaudit |
| 5 | **maxConcurrency 1** | 1 | Juara tidak terukur config-nya; yang terukur: bantalan AV mereka 181–784 vs kita 29 | Config-aman secara teknis — **rekomendasi JANGAN naikkan** | Menaikkan concurrency melipatgandakan pajanan abandoned SIMULTAN lawan REL −5 + suspensionCount 5 menuju tangga ban yang ambangnya tak dipublikasikan (FUEL-AUDIT: RISK KURANG) | Tetap 1 sampai AV tumbuh besar lewat completed jobs |
| 6 | **strategyType dynamic + parameter innovation_focus inert** | dynamic; maxVisos 6/strategyN 2/paraphrasing 0–2 tersimpan tak dipakai | dynamic = satu-satunya akses klaim one-shot; innovation_focus menolak one-shot di server | **Jangan disentuh tanpa keputusan fase** | Flip ke innovation_focus = mengunci jalur klaim one-shot (terbukti server-side) | Tetap dynamic selama rezim klaim/serve sekarang |
| 7 | **skipDeepEvaluation False** | False | Evaluasi dalam adalah sekutu gerbang mutu | Config-aman | Mengaktifkan skip = melepas satu lapis saringan mutu | Tetap False |
| 8 | **Expertise 0 · LE 0 · verified 0 · badge 0** | semua nol (pernah Expertise 7/LE 7 dari jalur ask, habis oleh 7 falsified) | Juara: Expertise 181–425, LE ribuan | **AKIBAT — tidak bisa direvisi langsung** | Tidak ada jalan config; satu-satunya jalan = verified di bawah gerbang (rezim sekarang: klaim STOP TOTAL, serve pilot tergating) | Bukan item config — ini skor permainan; naiknya menunggu verdict verified pertama |
| 9 | **REL −5, suspensionCount 5, AV baru 29** | bantalan tipis | Tangga REL-005 berakhir ban permanen, anak tangganya tak dipublikasikan | **AKIBAT** | Satu abandoned baru jauh lebih mahal bagi kita daripada bagi juara (AV 29 vs 181–784) | Lindungi lewat disiplin yang sudah ada: serve hanya via hook PREPARE/READY (risiko abandoned struktural nol di jalur utama), nol klaim di luar gerbang |
| 10 | Link offline di luar jendela | offline pada 02:17 WIB | Normal: serve hanya menyala di dalam jendela hunt oleh rezim | Bukan kekurangan | — | Tidak ada tindakan |

### Ringkasan vonis profil

Profil kita **ramping secara config dan nol secara hasil**. Yang benar-benar kurang dan bisa direvisi hanya dua: **(1) contextWindowTokens belum terdeklarasi** (satu-satunya kekurangan config dengan konsekuensi mekanis nyata — masuk keputusan lab) dan **(2) nama/tagline/icon Expert kosong** (identitas, config-aman, menunggu nama pilihan user). Sisanya yang tampak "kurang" (Expertise, LE, RAR komponen, badge) adalah **akibat permainan, bukan setelan** — tidak ada revisi config yang bisa menaikkannya; ia hanya bergerak lewat jawaban verified, yang saat ini diatur rezim STOP TOTAL klaim + pilot serve tergating. Badge kita **nol, terbukti dari 79 notifikasi (0 achievement) + LE 0**.

Sumber: `trued agent show` + payload `/api/node/agents/<id>` + `/api/node/scores` + `/api/authext/user` + `/api/node/notifications` (live 2026-11-17 02:17–02:26 WIB); SKILL.md baris 138; trued.py baris 696/982/5024–5075; DIALECTICA-MASTER §5.2/§7.3/§12.1; KULIT-1-EARN-COHORT-2026-11-12 §1.5; KORPUS-JUARA-2026-11-14; MEKANISME §24.1.
