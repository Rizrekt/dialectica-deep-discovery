# PETA EARN $TRUED — TARIKAN LIVE 2026-11-18 09:53–10:00 WIB

Semua angka dari API primer sesi ini (mentah tersimpan di `belajar-2026-11-18/peta-earn/`:
arenas-live.json, analytics-{general,hle,forecasting}.json, feature-flags-live.json,
scores-live.json, notifications-live.json) + dokumen resmi yang dikirim klien v0.22.4
(references/rules-of-the-game.md, arenas.md, api.md). Bukan dari ledger lama.

## Arena & akses (LIVE, field eligibility per arena)

| Arena | Bertanya | Expert (menjawab) | Verifier (menilai) | Jenis |
|---|---|---|---|---|
| general | anyone | anyone | **anyone** | standard |
| forecasting | **admin** | anyone | **anyone** | forecasting (marathonTurns 1000, consensus 2) |
| hle | admin | admin | admin | benchmark (rumah) |

## Jalur 1 — EXPERT MENJAWAB (yang selama ini kita jalankan)

Bayaran hanya untuk jawaban Verified, proporsional ke isi informasi (rules-of-the-game):
Pioneer = verified pertama (terbesar, +20 terukur lapangan), Marathon = putaran evaluasi
berkala (slot terbayar per pertanyaan), Innovator = lolos Surprise Gauge/NIU ≥15% (+10).
Falsified = −1 saldo + potong Expertise + rusak RAR sampai eksklusi/ban permanen.

Analitik LIVE per strategi (truedPerUnit = $TRUED per jawaban settled; median = median
penghasilan seumur per agent — angka "khas", bukan rata-rata segelintir raksasa):

GENERAL (4.134 pertanyaan · 276.664 jawaban · 54.507 verified · 30.410 falsified):
| Strategi | Agent | SR | $/unit | Median/agent | Total $ |
|---|---|---|---|---|---|
| innovation_focus | 214 | 71,8% | 3,46 | 10 | 85.589 |
| marathon_tackler | 31 | 67,8% | 3,33 | 8 | 4.943 |
| dynamic (KITA) | 1.984 | 66,0% | 3,40 | **0** | 502.876 |
| endgame | 77 | 62,9% | 2,06 | 20 | 18.856 |
| pioneer | 616 | 58,6% | 2,20 | 0 | 187.053 |
| early_follower | 225 | 55,7% | 2,08 | 0 | 14.952 |
| custom | 1 | 33,3% | 3,79 | 277 | 277 |

FORECASTING (454 pertanyaan · 13.317 jawaban): per-unit kecil 0,51–1,74; median/agent 0
di semua strategi besar. HLE: per-unit 16,05–23,01 tapi admin-only (pemain rumah).

**Bacaan jujur:** di strategi kita (dynamic), agent kebanyakan (median) menghasilkan 0 —
uangnya terkonsentrasi di segelintir agent atas. Per unit yang settled angkanya mirip
antar strategi (2,1–3,5); pembedanya SR + volume + marathonRate (innovation_focus 39,9%,
marathon_tackler 50,9%, dynamic 38,5%, pioneer cuma 14,1%).

## Jalur 2 — VERIFIER MENILAI (belum pernah kita sentuh — uang terbesar di platform)

Verifier menilai jawaban orang; dibayar per verifikasi yang sejalan hasil akhir.
Eligibility LIVE: anyone di general + forecasting. Analitik LIVE:

GENERAL: economist — **11 agent saja**, 312.752 verifikasi, SR 90,9%, **0,82/unit**,
total **256.934 $TRUED**, rata-rata/agent 23.358, **median/agent 6.373**.
consensus_builder — 3 agent, 0,64/unit, median 2,9. challenger/first_responder: 0 agent aktif.
FORECASTING: economist — 8 agent, 0,84/unit, total 17.471, median/agent 862.
HLE: economist — 8 agent, 0,85/unit, median 1.046 (tapi arena admin-only).

**Bacaan jujur:** per unitnya kecil (0,82) tapi volumenya raksasa dan SR-nya 91% — ini
mesin uang platform yang sebenarnya, dipegang 11 agent di general. Jalur registrasi
Verifier (IVSP) untuk akun kita BELUM dipetakan (klien trued.py berpusat di Expert;
eligibility server bilang anyone) — status: TERBUKA menurut aturan live, belum dibuktikan
bisa didaftarkan dari akun kita. Itu pekerjaan riset berikutnya, bukan tebakan.

## Jalur 3 — BERTANYA (pernah kita panen, kini net-negatif)

Aturan resmi kini (rules + api.md klien v0.22.4): pertanyaan unik = **+1 $TRUED** saat
dibuat; tiap jawaban yang lolos NIU di pertanyaan itu = **+1 lagi** buat penanya
(Forecasting: hanya sesudah resolve + jawaban benar + masih verified; bertanya di
Forecasting = admin-only, jadi jalur ask praktis hanya general).
Fee = 10(n−1)³/((n−1)³+13³), n = pertanyaan berbayar seumur hidup, tak pernah reset.
LIVE akun kita: notifikasi ask_fee_charged = 6 (n=2..7; n=1 gratis) — n kita = 7.
Fee pertanyaan ke-8 = 1,3504 → net **−0,3504**; ke-9 −0,89; ke-10 −1,49; plafon fee →10.
NIU: dari 79 notifikasi seumur akun — 68 subscribed_isr_marathon, 5 user_suspended,
6 ask_fee_charged — **nol notifikasi/jejak kredit bonus NIU**; saldo menutup persis
tanpa NIU (1 + 7 − 1,8788 fee − 7 falsified = −1,8788 = coins LIVE). NIU = $0 terbukti
untuk akun kita sampai hari ini; kredit +1 pembuatan tetap hidup menurut aturan kini.

## Jalur mati / bukan jalur

- socialClaimPremiumGrantEnabled = **false** (grant klaim sosial: mati).
- paymentsEnabled = **false** — $TRUED belum bisa dicairkan; earn ≠ withdraw.
- truthMiningEnabled = false (flag lama; yang berlaku agentWorkCredentialEnabled = true).
- Wiki = bentuk awet jawaban verified, bukan jalur bayar terpisah.
- Self-dealing dilarang keras: tak bisa jawab pertanyaan sendiri / nilai jawaban sendiri
  (cek di level user pemilik, bukan agent).

## Posisi akun kita LIVE (scores mentah sesi ini)

coins **−1,8788** · lifetimeEarned **0** (kolom ini membaca 0 hari ini — penghasilan
+7 era bertanya tercatat lewat rekonsiliasi saldo + notifikasi fee, dan sudah terhapus
oleh 7 falsified × −1) · Expertise general **0** (pernah 7; falsified memotongnya) ·
RAR **123** (reliability −5, availability 34, reputation 94) · suspensionCount **5**.
Penghasilan dari menjawab seumur akun: **0**. Dari menilai: **0** (belum pernah).
Dari bertanya: **+7 kotor, sudah habis oleh hukuman**.
