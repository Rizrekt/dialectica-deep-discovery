# PETA JALUR 3 — BERTANYA (ASKER) — BEDAH KOMPLEKS, LIVE 2026-11-18

Perintah user 2026-11-18 09:58 WIB. Read-only total: tidak ada pertanyaan dibuat,
tidak ada assist loop dijalankan, tidak ada fee tercharge dalam penyusunan peta ini.

**Sumber & tanggal tarikan:**
- LIVE sesi ini (2026-11-18 ±09:58–10:03 WIB): `GET /api/node/scores`,
  `GET /api/node/notifications`, `GET /api/node/isr/<id>` + `GET /api/node/isos/<id>`
  untuk ke-7 ISR kita — mentah tersimpan di `belajar-2026-11-18/peta-ask/`
  (`isr-detail-live-2026-11-18.json`, `scores-notif-fresh-2026-11-18.json`).
- LIVE 09:53–10:00 WIB (tarikan PETA-EARN): `arenas-live.json` di
  `belajar-2026-11-18/peta-earn/` (aturan arena versi server).
- DOKUMEN RESMI klien v0.22.4: `references/api.md` (§Ask assist loop, §Ask create,
  §Fee for asking, FAQ), `references/rules-of-the-game.md`,
  `references/arenas.md`, `SKILL.md`, dan kode `scripts/trued.py` (`cmd_ask`).
- LEDGER lapangan: MEKANISME-DAN-LAPANGAN.md §21, §22, §24, §25 — hanya petunjuk
  arah; setiap angka bebannya diverifikasi ulang ke sumber di atas.

**Tanda bukti:** TERBUKTI-LIVE = terbaca dari API sesi ini · DOKUMEN-RESMI = tertulis
di dokumen/kode resmi klien · BELUM-TERBUKTI = tidak ada bukti yang bisa ditarik.

---

## 0. VONIS JALUR (ringkas)

Jalur bertanya **berstatus DORMANT-terkunci-EV** (vonis frontier, §8 — tidur,
bukan tertutup permanen) dan **tertutup hari ini oleh dua kunci sekaligus**:
1. **Kunci saldo (keras, server-side):** saldo −1,8788 < fee pertanyaan ke-8 (1,3504).
   Create akan ditolak `VALIDATION_FAILED` sebelum apa pun ditulis — bertanya ke-8
   secara harfiah **tidak mungkin** dieksekusi hari ini, bukan sekadar tidak bijak.
2. **Kunci ekonomi (matematis):** sejak n=8, fee > kredit +1 secara permanen
   (fee naik monoton menuju plafon 10, kredit tetap +1). Satu-satunya penyeimbang
   resmi — bonus NIU +1 per jawaban lolos NIU — terbukti **$0** di akun kita
   padahal 91 jawaban terverifikasi di 7 pertanyaan kita dan 72 slot marathon
   terbayar ke penjawab senilai total 2.268,7178 $TRUED terbit di pertanyaan yang sama.

Jalur ini hanya hidup lagi bila salah satu pemicu terukur di §5 berbunyi.

---

## 1. TANGGA FEE UTUH + POSISI AKUN KITA

### 1.1 Rumus resmi (DOKUMEN-RESMI, api.md §Fee for asking)

```
Fee = 10 × (n − 1)³ / ((n − 1)³ + 13³)  $TRUED, dibulatkan 4 desimal
n   = pertanyaan BERBAYAR ke-n si penanya, SEUMUR HIDUP
```

- n=1 persis 0 (pertanyaan pertama gratis — tetap dihitung "charged" untuk tangga).
- Yang dikenai harga hanya `POST /api/node/isr` (create). Assist loop tidak mencharge.
- n adalah hitungan **per-orang seumur hidup**, sama untuk jalur API dan website;
  tidak ada field request yang memengaruhi charge — diturunkan server dari akun
  yang login. Kutipan yang berlaku adalah objek `fee` di curiosityToken, bukan
  prediksi klien ("Read the quoted fee rather than predicting one" — api.md).
- Fee dipotong dari Wallet (`scores.coins` = spendable). **Fee tidak pernah
  memotong Lifetime Earned** (api.md). Kredit pembuatan +1 sebaliknya menaikkan
  Lifetime Earned (terbukti di ladder §22: LE 1→7 selama n=1..7).

### 1.2 Tangga n=1..25 (dihitung dari rumus; dicocokkan: tabel api.md n=2/3/6/11/14/21
identik, dan fee aktual notifikasi n=2..7 identik)

| n | Fee | Net (kredit +1 − fee) | Kumulatif fee | Kumulatif net sejak n=1 |
|---|---|---|---|---|
| 1 | 0,0000 | +1,0000 | 0,0000 | +1,0000 |
| 2 | 0,0045 | +0,9955 | 0,0045 | +1,9955 |
| 3 | 0,0363 | +0,9637 | 0,0408 | +2,9592 |
| 4 | 0,1214 | +0,8786 | 0,1622 | +3,8378 |
| 5 | 0,2831 | +0,7169 | 0,4453 | +4,5547 |
| 6 | 0,5383 | +0,4617 | 0,9836 | +5,0164 |
| 7 | 0,8952 | +0,1048 | **1,8788** | **+5,1212** |
| **8** | **1,3504** | **−0,3504** | 3,2292 | +4,7708 |
| 9 | 1,8900 | −0,8900 | 5,1192 | +3,8808 |
| 10 | 2,4915 | −1,4915 | 7,6107 | +2,3893 |
| 11 | 3,1279 | −2,1279 | 10,7386 | +0,2614 |
| 12 | 3,7727 | −2,7727 | 14,5113 | −2,5113 |
| 13 | 4,4025 | −3,4025 | 18,9138 | −5,9138 |
| 14 | 5,0000 | −4,0000 | 23,9138 | −9,9138 |
| 15 | 5,5535 | −4,5535 | 29,4673 | −14,4673 |
| 16 | 6,0571 | −5,0571 | 35,5244 | −19,5244 |
| 17 | 6,5088 | −5,5088 | 42,0332 | −25,0332 |
| 18 | 6,9100 | −5,9100 | 48,9432 | −30,9432 |
| 19 | 7,2637 | −6,2637 | 56,2069 | −37,2069 |
| 20 | 7,5740 | −6,5740 | 63,7809 | −43,7809 |
| 21 | 7,8454 | −6,8454 | 71,6263 | −50,6263 |
| 22 | 8,0826 | −7,0826 | 79,7089 | −57,7089 |
| 23 | 8,2896 | −7,2896 | 87,9985 | −64,9985 |
| 24 | 8,4705 | −7,4705 | 96,4690 | −72,4690 |
| 25 | 8,6287 | −7,6287 | 105,0977 | −80,0977 |

Catatan teliti:
- Titik impas marginal: **n=8** (fee pertama yang melewati kredit +1). Kumulatif
  sejak n=1 baru negatif di **n=12** — sisa panen lama menyerap n=8..11, tapi itu
  uang yang sudah hilang (lihat 1.3), bukan alasan membuka.
- Koreksi kecil atas ledger lama: MEKANISME §24 menulis fee n=10 = 2,4911; hitungan
  rumus yang benar = **2,4915** (7290/2926 = 2,49146…). Selisih 0,0004 ikut
  menggeser angka "saldo akhir n=8–10" §24 (2,3897 → 2,3893). Tidak mengubah vonis.

### 1.3 Posisi akun kita — TERBUKTI-LIVE

- **n terpakai = 7.** Bukti: 6 notifikasi `ask_fee_charged` dengan `feeIndex` 2..7
  (n=1 gratis, tanpa notifikasi fee), fee aktual persis tangga di atas:
  0,0045 / 0,0363 / 0,1214 / 0,2831 / 0,5383 / 0,8952 — total **1,8788**.
- **Saldo live: coins = −1,8788**, Lifetime Earned = 0, RAR 123, Expertise general 0,
  suspensionCount 5 (scores sesi ini; identik dengan tarikan 09:53).
- **Rekonsiliasi menutup persis:**
  `0 (saldo awal, §21) + 7 (kredit pembuatan) − 1,8788 (fee) − 7 (7 falsified × −1
  dari jalur menjawab) = −1,8788` ✓ = coins live.
  (Lifetime Earned 7→0 karena penalti falsified memotong LE juga — tercatat di
  ledger: LE 7→4 sesudah 3 falsified pertama; fee sendiri tidak memotong LE.)
  Tidak ada sisa ruang untuk kredit NIU berapa pun dalam rekonsiliasi ini: kalau
  satu saja kredit NIU pernah masuk, saldo akhir tidak akan menutup di −1,8788.
- **Pertanyaan berikutnya = n=8, fee 1,3504, net −0,3504** (tanpa NIU).

### 1.4 Syarat saldo / gerbang affordable — apakah bertanya ke-8 MUNGKIN hari ini?

**Tidak. Tertahan di server, dua lapis (DOKUMEN-RESMI api.md):**

1. **Di fase ready:** giliran assist yang mencapai `ready` membawa `askFee`:
   `feeTrued` (kutipan), `spendableTrued` (saldo yang dibandingkan), dan
   `affordable`. Bila `affordable: false`, server **tidak menerbitkan
   curiosityToken sama sekali** — tidak ada struk untuk di-create; memutar ulang
   giliran yang sama tidak mencetaknya. Obatnya bukan mengganti kata-kata draf,
   melainkan menambah isi Wallet.
2. **Di create:** bila Wallet lebih kecil dari fee, create gagal
   `VALIDATION_FAILED` dengan pesan menyebut fee-nya; penolakan terjadi
   **sebelum apa pun ditulis** — tidak ada pertanyaan tercipta, tidak ada charge.

Dengan coins **−1,8788** (negatif) lawan fee **1,3504**: kekurangan persis
**3,2292 $TRUED**.

**Bukti LIVE gerbang ini (assist run 2026-11-18, Slot 1 antrean):** server
mengutip untuk pertanyaan berikutnya persis `feeTrued 1,3504, feeIndex 8,
profile standard` — tangga dan posisi n kita dikonfirmasi oleh kutipan server
sendiri, bukan hitungan kami. Kutipan yang sama menyatakan
`affordable: false`, `spendableTrued: "0.0000"` (server menyajikan saldo
terpakai sebagai 0,0000, bukan −1,8788), dan notice: *"Posting this Question
carries a Fee of 1,3504 $TRUED, and your Wallet doesn't have that much
available to spend right now. Nothing has been charged."* Fase mencapai
`ready`, curiosityToken **ditahan** — persis mekanik §2. Saldo sesudah assist
tetap −1,8788 (nol charge, terbukti). Transkrip:
`belajar-2026-11-18/peta-ask/ASSIST-LIVE-SLOT1-2026-11-18.txt`.

Yang harus terjadi dulu, salah satu:
- penghasilan bersih ≥ +3,2292 dari jalur lain (menjawab/menilai) masuk ke Wallet, atau
- kredit NIU pertama benar-benar mendarat (lihat §3/§5), atau
- perubahan aturan platform (fee/gerbang) yang terbaca di dokumen/server.

Baru sesudah spendable ≥ 1,3504 pertanyaan ke-8 bisa *dicoba* — dan tetap
bernilai −0,3504 kecuali NIU hidup. (Soal clamp saldo: TERBUKTI-LIVE sesudah
assist run di atas — server menyajikan `spendableTrued 0,0000` untuk saldo
−1,8788; gerbang membandingkan fee lawan angka itu.)

### 1.5 Bisakah n turun / reset secara sah?

**Tidak ada mekanisme yang terdokumentasi, dan bukti menentangnya (DOKUMEN-RESMI +
TERBUKTI-LIVE).** n diturunkan server dari hitungan pertanyaan berbayar seumur
hidup per-orang; api.md menegaskan hitungan yang sama untuk API dan website dan
bahwa n hanya maju seiring orang bertanya. Tidak ada decay, tidak ada reset
musiman, tidak ada penghapusan pertanyaan yang menurunkan n (ke-7 pertanyaan kita
pun tidak bisa dihapus dari hitungan — semuanya settled dan permanen di ledger
platform). Satu-satunya "reset" adalah akun/orang yang berbeda — itu bukan
penurunan n akun ini dan berada di luar jalur sah yang dipetakan di sini.

---

## 2. MEKANIK ASSIST LOOP UJUNG-KE-UJUNG + ATURAN LIVE + BEDAH 7 PERTANYAAN KITA

### 2.1 Alur (DOKUMEN-RESMI api.md §Ask + kode `cmd_ask` trued.py)

**Endpoint:** `POST /api/node/isrs/assist` (per giliran) →
`POST /api/node/isr` (create, satu-satunya titik uang bergerak).

Per giliran, pemanggil mengirim: `arenaId` (wajib), `userMessage` (percakapan),
`clientState.questionDraft` (**kata-kata yang dinilai giliran itu — wajib dikirim
setiap giliran**, kalau tidak draf membeku di versi giliran pertama), dan
`conversationId` (omit di giliran pertama, echo sesudahnya). Pemanggil memiliki
draf; saran asisten (`questionSuggestion`) tidak pernah diadopsi otomatis oleh
klien — keputusan kata-kata ada di pemanggil.

**Fase** (`assistantState.phase`): `drafting` → `spec-building` → `ready`.
Di Forecasting, `spec-building` membangun `resolutionSpec` (sumber resolusi,
deadline, tipe outcome) — pertanyaan asisten soal itu diteruskan ke user, tidak
boleh dikarang. Fase terminal versi klien: `rejected`, `blocked`, `duplicate`,
`error` (`TERMINAL_PHASES` di trued.py) — asisten berhenti dan tidak akan mencapai
ready.

**Yang dinilai per giliran:** `ruleChecklist` (aturan mutu arena + pass state-nya),
`specBlockers` (celah spek yang bisa dibaca manusia, per `path`), `draftStatus`
(`empty`/`ai-approved`/`user-edited`/`has-issues`), `canSubmit`.

**Gerbang keunikan (duplikat = terminal):** aturan sistem `SYS_UNIQUENESS`
(disuntikkan server di tengah giliran; bukan aturan statis arena). Bila gagal
dengan sitasi duplikat (`citedDuplicates`), klien berhenti total dan menampilkan
pertanyaan yang sudah ada — **dilarang mengganti kata-kata untuk mengakali
gerbang ini** (api.md: "Do not reword to evade the uniqueness gate"; trued.py:
`fail("duplicate — do not reword to get past the uniqueness gate")`). Kegagalan
SYS_UNIQUENESS tanpa sitasi (mis. draf terlalu pendek untuk dibandingkan) bukan
duplikat dan boleh diperbaiki.

**Reklasifikasi arena:** server dapat memindahkan draf ke arena lain
(`arenaReclassification`). Create wajib memakai arena hasil penetapan server,
bukan arena yang diminta — token dicetak terhadap arena penetapan itu. Alasan
`ineligible` berarti arena yang diminta tidak terbuka untuk posting akun ini.

**curiosityToken + kutipan fee (hanya di fase `ready`):** token berisi `token`,
`issuedAtMs`, dan `fee {feeTrued, feeIndex, profile}`. `ready` ≠ janji token:
token ditahan bila (a) vonis keunikan terhadap kata-kata final belum tercapai,
atau (b) fee di luar Wallet (lihat 1.4). `askFee` di giliran yang sama membedakan
kedua sebab itu.

**Create — titik persis uang bergerak:** `POST /api/node/isr` dengan `content`
(draf final), `arenaId` (penetapan), `curiosityToken` **di-echo persis tanpa
edit**, plus `outputSchema` untuk General (arena General tidak mendefinisikan
skema; klien mengirim skema klasik `{"answer": string}` — server memberi default
bila omit, tapi klien memasangnya eksplisit) dan `resolutionSpec` untuk
Forecasting. Di sinilah — dan hanya di sini — fee dipotong dan kredit +1 masuk.
Mengedit `feeTrued`/`feeIndex` atau membuang objek `fee` → `Curiosity token
rejected`; mengganti `profile` bisa lolos tak terdeteksi bila harganya sama —
tetap dilarang, echo apa adanya. Semua kegagalan create berbentuk
`VALIDATION_FAILED`; pesannya yang membedakan sebabnya; **tidak satu pun
kegagalan create menciptakan pertanyaan atau mencharge apa pun**.

**Kutipan basi → `refresh_token`:** bila fee quote tidak lagi kini (penanya
membuat pertanyaan berbayar lain di antaranya, atau objek fee diedit), create
menolak sebagai quote basi — ini **bisa** diulang: panggil assist sekali lagi
dengan `action: "refresh_token"`, lalu create dengan token + fee segarnya.
Beda dengan kasus Wallet-kurang (tidak bisa diulang; tambah isi Wallet dulu).
Catatan implementasi: `refresh_token` dan `go_back` terdokumentasi di api.md
sebagai action assist, tetapi **tidak muncul di kode trued.py v0.22.4**
(`grep` = 0) — `cmd_ask` tidak mengeksposnya; memakainya berarti memanggil
endpoint assist secara mentah.

**Perilaku klien `cmd_ask`:** SATU giliran per pemanggilan. Ia mencetak balasan
asisten, draf berjalan, aturan yang gagal, saran, dan spec blockers; bila belum
ready ia berhenti dan menyuruh pemanggil memutuskan kata-kata berikutnya lalu
melanjutkan dengan `--continue <conversationId> --draft "..."`. Bila ready, ia
langsung create di pemanggilan yang sama dan mencetak fee yang tercharge
(`feeIndex: 0` = sentinel "tidak ada yang bisa dicharge" = ask gratis).

### 2.2 Aturan pertanyaan LIVE arena general (TERBUKTI-LIVE, arenas-live.json)

Arena `general`: `version 3`, `isActive: true`, `kind: standard`,
`eligibility.postISR: "anyone"`, `outputSchema: null` (karena itu create wajib
membawa skema klasik), `marathonTurns: null`. `questionRules` utuh:

1. **Q_CLARITY** — "Question is clearly stated and answerable by a knowledgeable
   agent. Any claim the Question states as fact about the world (events, laws,
   institutions, people), including inside a memo, quote or document it supplies,
   must be one a public source confirms, or else be framed as hypothetical; the
   asker's own code, data or private text to analyse is fine."
   - compliant: pertanyaan spesifik tentang topik terdefinisi baik dengan jawaban
     yang bisa ditentukan.
   - non-compliant: ambigu/multi-tafsir → ubah kata; beberapa sub-pertanyaan tak
     terkait digabung → pecah jadi pertanyaan terpisah.
2. **Q_GOOD_FAITH** — "Question seeks genuine knowledge or understanding. It does
   not ask Experts or Verifiers to reveal their own environment, whether directly
   (user account, files, permissions, tools, credentials) or by running code
   there and reporting a result that reveals it, though asking what code would
   output by reasoning about it is fine."
   - compliant: pertanyaan rasa-ingin-tahu tentang cara kerja proses alamiah;
     pertanyaan retoris yang sudah memuat jawabannya — compliant bila sungguh
     mencari pemahaman lebih dalam dari premisnya.
   - non-compliant: dirancang memanipulasi, melecehkan, atau memperoleh konten
     berbahaya.
3. **Q_NON_TRIVIAL** — "Answer requires reasoning or synthesis beyond a single
   lookup."
   - compliant: menuntut sintesis banyak sumber / langkah penalaran; pertanyaan
     "why" tentang fakta terkenal yang menuntut penalaran kausal.
   - non-compliant: satu fakta yang selesai dengan satu query pencarian —
     terlalu trivial untuk arena.
4. **Q_PROHIBITED** — "Question contains no prohibited content."
   Daftar terlarang persis: Child Sexual Abuse Material; Obscenity; Sex
   Trafficking Content. Pelanggaran = ditolak seketika.

(Panduan penulisan arenas.md menambahkan: satu pertanyaan, cukup spesifik
sehingga expert tahu kapan ia terjawab, dan cukup menuntut sehingga jawabannya
memerlukan menghubungkan sumber/langkah penalaran.)

### 2.3 Bedah 7 pertanyaan kita — kenapa lolos, dan keadaan LIVE-nya kini

Pola bersama (ledger §21–22, konsisten dengan aturan live): sebelum ladder, tiap
topik dicek kebaruannya lewat pencarian — tetangga terdekat (wiki/pertanyaan
eksis) selalu beda topik, tidak ada yang menjawab topik yang sama. Keenam topik
n=2..7 dan topik n=1 semuanya: **satu pertanyaan tunggal berbentuk "why/how"**
tentang mekanisme kripto/DeFi/keamanan yang jawabannya menuntut sintesis
(Q_NON_TRIVIAL), **tanpa klaim faktual yang dinyatakan sebagai premis** —
mekanisme ditanyakan, bukan ditegaskan (Q_CLARITY), rasa-ingin-tahu murni
(Q_GOOD_FAITH), nol konten terlarang (Q_PROHIBITED). Hasilnya: **ketujuh draf
lolos assist dalam SATU giliran** (langsung `ready` → created, tanpa revisi) —
bukti lapangan bahwa pola ini melewati ruleChecklist + SYS_UNIQUENESS sekaligus.

Keadaan LIVE per pertanyaan (tarikan sesi ini, 2026-11-18):

| n | ISR (8) | Topik | Fee aktual | Status | Verified | Falsified | Revealed | Abandoned | Marathon concluded | Slot marathon awarded (ke penjawab) | truedIssued (ke penjawab) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1d758352 | Bias produser blok BSC atas randomitas mint NFT (blockhash/timestamp) | 0,0000 | settled | 12 | 7 | 20 | 8 | ya | 9 | 281,1377 |
| 2 | c3730bab | Persistensi base fee EIP-1559 sesudah lonjakan demand surut | 0,0045 | settled | 13 | 5 | 32 | 15 | ya | 9 | 316,6480 |
| 3 | 3f3c4628 | Matematika divergence loss AMM constant-product + konveksitasnya | 0,0363 | settled | 10 | 13 | 29 | 16 | ya | 9 | 290,7693 |
| 4 | d397e561 | Biaya modal manipulasi oracle TWAP vs panjang jendela + strategi sisa | 0,1214 | settled | 12 | 6 | 34 | 16 | ya | 9 | 309,9157 |
| 5 | 8c9c01f2 | Royalti ERC-721/ERC-2981 tak bisa ditegakkan kontrak token; transfer ≠ sale | 0,2831 | settled | 16 | 5 | 33 | 17 | ya | 13 | 382,3299 |
| 6 | d9909cbc | Soft confirmation sequencer L2 terpusat vs finalitas L1 | 0,5383 | settled | 13 | 7 | 26 | 21 | ya | 11 | 321,8802 |
| 7 | 64bd68ac | Paradoks multisig: signer + threshold naik bisa gagal menaikkan keamanan riil | 0,8952 | settled | 15 | 11 | 30 | 18 | ya | 12 | 366,0370 |
| | | **TOTAL** | **1,8788** | **7/7 settled** | **91** | 54 | 204 | 111 | **7/7** | **72** | **2.268,7178** |

Catatan: `marathonActive` dan `marathonConcluded` terbaca **True bersamaan** di
ke-7 ISR (pasangan flag basi yang sudah dikenal di ledger) — yang dipakai di sini
adalah `marathonConcluded: true` + entri `awarded` berstempel waktu, bukan flag
active-nya. Kolom "awarded" dihitung dari `marathonEligibleIsos[].awarded == true`
pada detail ISR live; jumlah entri eligible per pertanyaan persis sama dengan
jumlah verified-nya (12/13/10/12/16/13/15 = 91).

---

## 3. BEDAH NIU SAMPAI AKAR

### 3.1 Definisi resmi persis (DOKUMEN-RESMI)

NIU hanya muncul sebagai **prosa aturan**, di dua tempat:

- **rules-of-the-game.md §Rewards:** "Asking earns too: a unique Question earns
  its asker **+1 $TRUED** when it is created, and each Answer to it that passes
  the **NIU** check (Novelty, Inventiveness, Utility) earns the asker another
  +1 — in the Forecasting Arena, only once the Question resolves and only for an
  Answer that proved right and is still Verified."
- **SKILL.md:** kalimat yang sama, ditambah kata "later" — kredit NIU datang
  **sesudah** jawabannya, bukan bersamaan dengan verifikasi.

Yang **tidak** ada (terverifikasi dengan pencarian teks sesi ini):
- **api.md tidak menyebut NIU sama sekali** — tidak ada field, endpoint, tipe
  notifikasi, atau ambang NIU di referensi API. Satu-satunya yang api.md katakan
  soal kredit bertanya adalah FAQ: "+1 $TRUED reward for creating a unique
  Question appears in your balance but does not create an inbox notification"
  — itu tentang kredit **pembuatan**, dan menegaskan kredit bisa masuk **senyap**
  (tanpa notifikasi). Konsekuensinya: ketiadaan notifikasi bonus **bukan** bukti
  NIU nol; buktinya adalah rekonsiliasi saldo (§1.3) yang menutup persis tanpa NIU.
- **Checklist verifikasi arena general (LIVE) hanya 4 butir** — A_CITATION,
  A_REASONING, A_UNCERTAINTY, A_SCOPE. **NIU bukan butir checklist verifier.**
  NIU juga tidak muncul di `questionRules` maupun di snapshot aturan pada detail
  ISR kita.
- Mekanisme bernama terdekat adalah **Surprise Gauge** (rules §Rewards +
  SKILL.md): jawaban sesudah Pioneer hanya dibayar bila "add genuinely new
  information over what's already verified"; jawaban paraphrasing berhenti di
  Surprise Gauge dan tidak pernah diperiksa lebih lanjut. Apakah "NIU check"
  adalah nama sisi-asker dari komputasi yang sama dengan Surprise Gauge:
  **BELUM-TERBUKTI** — tidak ada dokumen yang menyamakannya; keduanya istilah
  berbeda di dokumen yang sama. (Angka "novelty ≥15%" yang beredar di dokumen
  proyek kita berasal dari studi lapangan jalur menjawab, bukan dari dokumen
  resmi NIU.)

### 3.2 Siapa menilai NIU, dan kapan (vonis bukti)

- **Siapa:** BELUM-TERBUKTI secara eksplisit. Yang bisa disingkirkan: bukan
  verifier manusia/agent lewat checklist arena (NIU tidak ada di checklist), dan
  bukan penanya. Sisa kandidat yang konsisten dengan bukti: penilaian otomatis
  server-side (sekelas Surprise Gauge / paraphrasing check yang memang berjalan
  server-side — `hasParaphrasingResult` ada di payload ISO live).
- **Kapan:** SKILL.md bilang "another +1 **later**". Kandidat momen: saat jawaban
  terverifikasi, saat marathon pertanyaan conclude, atau batch berkala. Bukti
  lapangan kita meniadakan dua momen pertama untuk 91 kasus (lihat 3.3): semua
  verifikasi sudah lama selesai dan ke-7 marathon sudah concluded, tetap nol.
  Momen "batch berkala yang belum pernah jalan" tidak bisa dibedakan dari
  "tidak ada yang lolos" — lihat 3.4.

### 3.3 Bukti lapangan (TERBUKTI-LIVE, tarikan sesi ini)

Di 7 pertanyaan kita sendiri, per hari ini:
- **91 jawaban Verified** (12+13+10+12+16+13+15) — semuanya kandidat NIU menurut
  definisi prosa (jawaban di pertanyaan kita yang, bila lolos NIU, memberi +1).
- **7/7 marathon concluded**, dengan **72 entri `awarded: true`** berstempel
  `awardedAt` di `marathonEligibleIsos` — marathon di pertanyaan kita **membayar
  penjawab secara nyata dan berulang** (rentang awardedAt 2026-11-09 s/d
  2026-11-16).
- **`truedIssued` total 2.268,7178 $TRUED** terbit di 7 pertanyaan ini — seluruhnya
  aliran ke penjawab (Pioneer/marathon/dll.), bukan ke penanya.
- **Kredit NIU ke kita: 0.** Saldo menutup persis tanpa NIU (§1.3); 79 notifikasi
  seumur akun hanya berisi 68 `subscribed_isr_marathon`, 6 `ask_fee_charged`,
  5 `user_suspended` — nol tipe kredit/bonus apa pun (dengan catatan 3.1: kredit
  pembuatan saja yang resmi dinyatakan senyap; rekonsiliasi saldo adalah bukti
  yang mengikat, bukan ketiadaan notifikasi).
- Nol jawaban milik agent kita sendiri di ke-7 pertanyaan (`isOwnAgent` = 0 ISO)
  — sesuai larangan konflik kepentingan (§4).

### 3.4 Dua hipotesis, diuji lawan bukti

- **H1 — Jalur kredit NIU belum hidup di platform.** Didukung: NIU absen total
  dari api.md (nol permukaan teknis), absen dari checklist arena, dan 91/91
  kandidat di akun kita menghasilkan 0 — termasuk jawaban-jawaban yang cukup
  bernilai sampai memenangkan 72 slot marathon berbayar. Bila NIU menilai
  kebaruan, sulit menjelaskan 0/91 sementara mesin kebaruan sisi penjawab
  (marathon award) menyala 72 kali di pertanyaan yang sama.
- **H2 — Jalur hidup, tapi tidak ada satu pun dari 91 verified yang lolos NIU.**
  Tidak bisa disingkirkan penuh: NIU mungkin menilai sesuatu yang lebih sempit
  daripada kelayakan marathon (mis. kebaruan terhadap seluruh korpus, bukan
  terhadap pertanyaan itu saja), dan ambangnya tidak dipublikasikan. Tetapi H2
  menuntut tingkat kegagalan 100% pada sampel yang terbukti bernilai menurut
  dua pengukur lain (verified + marathon-awarded) — beban penjelasannya berat.
- **Bukti pembeda yang akan memisahkan keduanya:**
  1. Satu kredit +1 yang teramati masuk ke saldo penanya mana pun yang dapat
     dihubungkan ke jawaban lolos NIU (bukan ke pembuatan pertanyaan) → H1 gugur.
     Untuk akun kita bentuknya paling bersih: **coins atau Lifetime Earned naik
     tanpa peristiwa lain** (tidak ada ask/answer/verify baru) — karena 91
     kandidat kita sudah terlanjur ada, aktivasi retroaktif akan terlihat persis
     seperti itu.
  2. Dokumentasi resmi berubah: NIU muncul di api.md / changelog klien / aturan
     arena dengan field atau ambang → jalur dinyatakan hidup oleh platform.
  3. Sebaliknya, bila platform suatu hari mempublikasikan hasil NIU per jawaban
     (field di payload ISO) dan 91 jawaban kita terbaca "tidak lolos" → H2 menang.
  4. **Cek sisi-operator platform (ditambahkan vonis frontier, §8 Q2):** jawaban
     resmi platform atas tiga hal — handler NIU aktif di produksi atau tidak,
     apakah ke-91 jawaban kita pernah dievaluasi NIU, dan apakah ada event
     kredit/reason code NIU di ledger — memisahkan H1/H2 dari sisi dalam. Ini
     tindakan NIU berikutnya yang disepakati frontier; pengirimannya adalah
     langkah yang butuh keputusan user sebagai pengirim bila dilakukan.
- **Cara memantau (tanpa cron baru — lihat §5.3):** cek delta `coins` +
  `lifetimeEarned` lawan baseline abadi **−1,8788 / 0** pada setiap pembacaan
  `trued status`/scores yang memang sudah terjadi di sesi proyek ini, ditambah
  bonus-NIU watch yang sudah terdaftar sebagai butir revisi mingguan
  (MEKANISME §25/§27). Kenaikan saldo yang tidak bisa dijelaskan peristiwa lain
  = picu bedah NIU di hari yang sama.

### 3.5 Syarat kredit NIU: general vs forecasting (DOKUMEN-RESMI)

- **General:** +1 per jawaban yang lolos NIU di pertanyaan kita. Tidak ada syarat
  tambahan tertulis (tidak menunggu resolusi — general tidak beresolusi).
- **Forecasting:** +1 hanya **sesudah pertanyaan resolve**, dan hanya untuk
  jawaban yang **terbukti benar** dan **masih Verified** saat itu. Plus hambatan
  akses: eligibility LIVE forecasting `postISR: "admin"` — akun kita tidak bisa
  bertanya di sana sama sekali hari ini, jadi cabang forecasting NIU tertutup
  dua kali untuk kita.

---

## 4. SISI ASKER SESUDAH PERTANYAAN HIDUP

- **Notifikasi `subscribed_isr_marathon` (68 di akun kita, TERBUKTI-LIVE):**
  notifikasi langganan yang menempel pada ISR milik kita — isinya hanya
  `{isrId, title}`. Fungsinya: memberi tahu penanya bahwa satu putaran marathon
  di pertanyaannya selesai/berlangsung. Distribusinya per pertanyaan kita:
  Q1 8, Q2 9, Q3 9, Q4 9, Q5 12, Q6 10, Q7 11 (= 68), membentang 2026-11-09 s/d
  2026-11-16 — hampir satu-per-satu mengikuti 72 entri marathon awarded
  (selisih kecil konsisten dengan langganan yang aktif sesudah peristiwa
  pertama di sebagian pertanyaan; pemetaan persisnya BELUM-TERBUKTI). Ini
  notifikasi informasi, bukan kredit: tidak ada field jumlah uang di dalamnya.
  Aturan resmi menambahkan penanya juga dinotifikasi **in-app dan email** saat
  verifikasi pertanyaan settle (rules-of-the-game).
- **Kendali asker selama marathon: tidak ada.** Tidak ada giliran (turn) untuk
  penanya, tidak ada persetujuan, tidak ada tuas di dokumen/API untuk
  memengaruhi, mempercepat, atau menghentikan marathon pertanyaan sendiri.
  Marathon adalah putaran evaluasi server atas jawaban-jawaban eligible
  (jendela ±500 detik per entri pada data kita: `startedAt`→`endsAt`), berjalan
  lama sesudah pertanyaan settled. Penanya murni penonton yang dinotifikasi.
- **Kapan pertanyaan settled (FAQ api.md + LIVE):** status ISR menjadi `settled`
  — ke-7 pertanyaan kita semuanya `settled` hari ini. Penting: **`settled` tidak
  menutup pertanyaan untuk jawaban baru** (api.md: "`settled` does not close
  that Question to new Answers"), dan marathon bisa sudah pernah dimenangkan
  sementara satu lagi masih berjalan ("marathons:1 (one running)"). Terbukti di
  data kita: aktivitas terakhir (`lastActivityAt`) ke-7 ISR masih bergerak
  sampai 2026-11-18 walau statusnya settled sejak November awal.
- **Larangan konflik kepentingan (DOKUMEN-RESMI, rules-of-the-game §COI):**
  "a user cannot answer their own Question, nor verify their own Answer. These
  checks run on the **owning user**, not the client or agent used — asking
  through this skill counts exactly like asking on the website." Jadi: bertanya
  lewat klien ini = bertanya sebagai user yang sama; agent kita tidak bisa
  menjawab pertanyaan kita sendiri dan tidak bisa memverifikasi jawaban kita
  sendiri, lewat jalur apa pun. Terverifikasi patuh di lapangan: 0 ISO milik
  agent kita di ke-7 pertanyaan kita (tarikan live sesi ini).

---

## 5. RENCANA BUKA-KEMBALI SIAP EKSEKUSI

### 5.1 Pemicu terukur (semuanya bisa dicek read-only; syarat kecukupan diubah vonis frontier — lihat catatan sesudah tabel dan §8)

| # | Pemicu | Ambang persis | Cara cek |
|---|---|---|---|
| P1 | Kredit NIU pertama terbukti | `coins` atau `lifetimeEarned` naik dari baseline −1,8788 / 0 tanpa peristiwa ask/answer/verify baru yang menjelaskannya; atau satu kredit +1 teramati yang terikat jawaban lolos NIU | `trued status` / `GET /api/node/scores` |
| P2 | Saldo pulih ke ambang tembak | `coins ≥ 1,3504` (fee n=8 bisa dibayar) — perlu kenaikan bersih **+3,2292** dari hari ini; ambang nyaman untuk 3 tembakan berurutan: `coins ≥ 3,7319` (lihat 5.2; angka dikoreksi konsultasi frontier, §8) | scores |
| P3 | Aturan berubah | Rumus fee, kredit pembuatan, gerbang affordable, atau definisi/ambang NIU berubah di dokumen resmi klien versi baru atau aturan arena live (general kini versi 3) | diff references klien saat upgrade + tarik ulang arenas |
| P4 | Eligibility forecasting berubah | `postISR` forecasting bukan lagi `admin` (membuka cabang NIU-forecasting) | tarik ulang arenas-live |

Catatan keras: **P2 saja tidak cukup secara ekonomi** — saldo pulih membuat
ask #8 *mungkin*, bukan *untung* (net tetap −0,3504). P2 menjadi layak-eksekusi
hanya digabung P1 (NIU hidup ⇒ tiap pertanyaan berpotensi +1 × jumlah jawaban
lolos NIU, menutup fee) atau P3 (matematika tangganya berubah). Tanpa itu,
membuka jalur = membakar saldo dengan kepastian matematis.
**Gerbang resmi sesudah vonis frontier (§8, Q1):** yang MEMBUKA jalur hanya
**P1 atau P3**. P2 tidak membuka kecuali ada bukti terpisah bahwa manfaatnya
> biaya bersih; **P4 sendiri juga tidak cukup** (eligibility forecasting yang
terbuka hanya membuka cabang, bukan menghidupkan matematikanya). Rumusan awal
"salah satu pemicu cukup" dicabut untuk P2 dan P4.

### 5.2 Urutan 3 pertanyaan pertama bila dibuka (angka tangga §1.2)

Prasyarat bertingkat (saldo minimum SEBELUM tembakan, tanpa NIU di tengah jalan):

| Urutan | n | Fee | Net | Saldo minimum sebelum tembak ini | Saldo minimum sebelum urutan dimulai |
|---|---|---|---|---|---|
| 1 | 8 | 1,3504 | −0,3504 | ≥ 1,3504 | ≥ 3,7319 |
| 2 | 9 | 1,8900 | −0,8900 | ≥ 1,8900 (sesudah net #1) | (sudah termasuk di atas) |
| 3 | 10 | 2,4915 | −1,4915 | ≥ 2,4915 (sesudah net #1+#2) | (sudah termasuk di atas) |

Total bakar bersih 3 tembakan (tanpa NIU): **−2,7315**. (Koreksi frontier
2026-11-18: ambang saldo awal urutan = **3,7319**, bukan 3,7315 — gerbang fee
diperiksa sebelum kredit pembuatan masuk; koreksi ini datang dari konsultasi
frontier, lihat §8.) Dengan NIU hidup, tiap
+1 yang mendarat mengurangi kebutuhan saldo tembakan berikutnya satu-satu —
hitung ulang dari scores live sebelum tiap tembakan, jangan dari tabel ini.

Prosedur per tembakan (siap jalan, sesuai §2):
1. Cek kebaruan topik lewat pencarian dulu (pola §21–22: tetangga wiki/ISR harus
   beda topik; duplikat = ganti topik, jangan akali kata-kata).
2. Topik mengikuti pola terbukti: satu pertanyaan "why/how" mekanisme
   kripto/DeFi/keamanan yang menuntut sintesis, tanpa premis faktual.
3. `trued ask "<teks>" --arena general` per giliran; putuskan kata-kata sendiri
   dari feedback; berhenti total bila duplikat terminal atau fase terminal.
4. Di `ready`: baca `askFee` — pastikan `affordable: true` dan `feeTrued` sama
   dengan tangga (1,3504 / 1,8900 / 2,4915); token tertahan = berhenti dan
   diagnosis dari `askFee`, jangan putar ulang membabi buta.
5. Create terjadi di dalam pemanggilan yang mencapai ready — **hanya atas kata
   user** (create = uang bergerak). Sesudah create: verifikasi saldo server
   (harus bergerak persis +1 − fee) sebelum tembakan berikutnya; menyimpang
   > 0,05 dari rumus = berhenti (aturan berhenti ladder §22).
6. Catat ISR id + fee aktual + saldo sesudah ke ledger, seperti format §22.

### 5.3 Memantau pemicu TANPA cron baru

Semua cron Dialectica dihapus user 2026-11-17 — **tidak ada cron dibuat oleh
peta ini.** Pemantauan menempel pada permukaan yang sudah ada:
- **Setiap pembacaan status/scores di sesi proyek mana pun** (serve, revisi,
  audit): bandingkan `coins`/`lifetimeEarned` lawan baseline abadi
  **−1,8788 / 0**; selisih tak terjelaskan = bedah NIU hari yang sama (P1).
- **Revisi mingguan** yang sudah berjalan: bonus-NIU watch memang butir
  terdaftar di badannya (MEKANISME §25/§27) — tambahkan cek P3/P4 (diff dokumen
  klien + eligibility forecasting) ke putaran yang sama.
- **Saat upgrade klien** (versi > 0.22.4): grep `NIU` di references baru —
  kemunculan NIU di api.md adalah sinyal P3 terkuat yang bisa datang sendiri.
- **Pantau control-user (vonis frontier, §8 Q2):** penanya baru yang
  pertanyaannya menerima jawaban inovatif yang diterima luas — delta saldo
  mereka (bila teramati) adalah monitor NIU tambahan. Berguna sebagai monitor,
  BUKAN pembeda H1/H2; pembeda yang disepakati adalah cek sisi-operator
  (§3.4 butir 4).

### 5.4 Probe NIU — DITANGGUHKAN (vonis frontier, §8 Q3)

Probe satu pertanyaan demi menguji NIU **tidak dijalankan**. Ia hanya sah
sebagai eksperimen satu-tembakan yang diprakomitmenkan — kriteria perubahan
kebijakan ditulis di depan, dan hasil nol TIDAK boleh ditafsirkan "NIU mati" —
dan hanya sesudah cek murah lain buntu serta DUA prasyarat isolasi variabel
dari penengah terpenuhi: (1) jawaban "gold standard" tepercaya yang memenuhi
semua metrik NIU objektif sebagai kontrol; (2) konfirmasi sisi-platform bahwa
fitur NIU aktif untuk tier akun kita. Tanpa keduanya, probe = bakar
likuiditas. Tidak ada slot antrean yang dialokasikan untuk probe.

---

## 6. DAFTAR BELUM-TERBUKTI (jujur, supaya tidak jadi klaim diam-diam)

1. Siapa/apa persisnya menilai NIU dan pada momen apa (otomatis server-side
   adalah sisa kandidat, bukan fakta).
2. Apakah NIU check = Surprise Gauge dengan nama lain (dokumen tidak menyamakan).
3. Ambang/syarat lolos NIU di general (tidak dipublikasikan di mana pun).
4. ~~Apakah spendable dibandingkan sebagai coins mentah atau di-clamp ≥0~~ —
   TERTUTUP oleh assist live 2026-11-18: server mengutip `spendableTrued
   0,0000` untuk saldo −1,8788 (disajikan ter-clamp di 0).
5. Pemetaan persis 68 notifikasi marathon ↔ 72 entri awarded (selisih 4;
   penjelasan langganan-timing masuk akal tapi tidak terbukti).
6. Apakah kredit NIU, bila jalurnya hidup suatu hari, berlaku surut untuk 91
   verified yang sudah ada (skenario terbaik P1; tidak ada dokumen yang
   menjanjikannya).

---

## 7. BANGUNAN SIAP — SISA LANGKAH SAAT USER BANGUN

Kit siap-jalan sudah dibangun dan diuji (perluasan perintah 10:01 WIB):

| Komponen | Berkas | Status |
|---|---|---|
| Preflight live (read-only) | `provider/ask_preflight.py` | JALAN — vonis tercetak TIDAK, exit 1, self-audit fee COCOK; bukti bertanggal: `belajar-2026-11-18/peta-ask/PREFLIGHT-2026-11-18.txt` |
| Driver assist + hard stop | `provider/ask_driver.py` | JADI — assist berhenti struktural di ready; create hanya lewat subcommand terpisah dengan `--user-word` + `--confirm-fee` cocok + `--live` |
| Uji driver | `provider/test_ask_driver.py` | **19/19 LOLOS** (fixture, offline) |
| 3 draf siap pilih | `ANTREAN-BERTANYA-SIAP-2026-11-18.md` | JADI — cek aturan butir-per-butir + catatan pencarian duplikat + uji silang 2 lane + kartu fee per slot |
| Uji silang model lain | `provider/crosstest_ask_drafts.py` | JALAN — Nemotron pass 3/3; penantang qwen BREAK 3/3, adjudikasi tercatat per slot; mentah: `belajar-2026-11-18/peta-ask/crosstest-2026-11-18.json` |
| Bukti assist live Slot 1 | `belajar-2026-11-18/peta-ask/ASSIST-LIVE-SLOT1-2026-11-18.txt` | ready satu giliran; struk ditahan karena saldo; **nol charge** (saldo tetap −1,8788) |
| Paket konsultasi frontier | `FRONTIER-PAKET-JALUR3.md` + sintesis `belajar-2026-11-18/frontier-jalur3/SINTESIS-FRONTIER-JALUR3.md` | TUNTAS 2026-11-18 10:12–10:20 WIB — vonis dilipat di §8 |

**Sisa langkah saat user bangun — persis dua, dan hanya bila pemicu §5.1
berbunyi:**
1. User **pilih slot** (1/2/3) dari ANTREAN dan berkata jalan.
2. Create dijalankan lewat `ask_driver.py create` (state dari assist segar
   di giliran yang sama — struk Slot 1 yang sekarang TIDAK diterbitkan
   karena saldo; assist harus diulang sesudah saldo cukup, lalu create
   dengan `--confirm-fee` sesuai kutipan barunya).

**Catatan jujur penghalang:** hari ini langkah 2 **belum bisa** dijalankan
bahkan bila user berkata jalan — fee 1,3504 > spendable 0,0000; server akan
menahan struk dan menolak create. Pemulihnya, satu-satunya: saldo naik
bersih ≥ +3,2292 dari jalur menjawab/menilai (atau kredit NIU pertama
mendarat / aturan berubah — pemicu P1/P3 §5.1). Tidak ada jalan pintas
yang sah; driver sengaja tidak bisa mengakali gerbang ini.

## 8. VONIS FRONTIER & PERUBAHANNYA

**STATUS: FINAL — konsultasi TUNTAS 2026-11-18 10:12–10:20 WIB** (Klausul
F-31D terpenuhi). Kursi: duck.ai GPT-6 Luna (utama, browser cloud) ·
gpt-5.6-sol (co-advisor, CrowLLM) · gemini-3.1-pro (penengah, CrowLLM).
Paket: `FRONTIER-PAKET-JALUR3.md`. Jawaban mentah tiap kursi + sintesis yang
menjadi otoritas lipatan ini: `belajar-2026-11-18/frontier-jalur3/`
(`duck-answer.md`, `sol-answer.md`, `gemini-answer.md`,
`SINTESIS-FRONTIER-JALUR3.md`). Di bawah: vonis per pertanyaan, titik
konvergen/pecah, dan PERUBAHAN KONKRET yang diberlakukan ke peta + antrean —
bukan ringkasan tempel.

### Q1 — Gerbang buka-kembali: EV-positif vs membeli reputasi

- **duck (utama):** gerbang EV-positif — jalur hanya dibuka bila nilai
  harapannya positif.
- **sol (co-advisor):** PECAH — rencana pra-konsultasi dinilai terlalu kaku;
  ask net-negatif sah sebagai pembelian reputasi.
- **gemini (penengah): MEMUTUS DUCK BENAR.** Alasan menentukan: reputasi di
  platform ini adalah aset yang terbukti bisa dilikuidasi retroaktif
  (keuntungan +1/+1 kita terhapus oleh penalti jalur lain) — membeli aset tak
  stabil dengan likuiditas langka adalah sunk cost. Kebijakan sol baru benar
  BILA platform memberi lantai reputasi / jaminan tak bisa dihapus — tidak
  ada bukti itu ada.
- **PERUBAHAN DIBERLAKUKAN:** gerbang §5.1 diketatkan. Yang MEMBUKA jalur
  hanya **P1** (NIU terbukti) atau **P3** (perubahan aturan material). **P2**
  (saldo pulih) saja TIDAK membuka kecuali ada bukti terpisah manfaat >
  biaya bersih; **P4** sendiri tidak cukup. Rumusan pra-konsultasi "salah
  satu pemicu cukup" dicabut untuk P2 dan P4.

### Q2 — Uji pembeda NIU (H1 jalur mati vs H2 tak ada yang lolos)

- **Konvergen 3 kursi:** bukti yang ada sekarang TIDAK memisahkan H1/H2
  secara tuntas, dan uji paling menentukan BUKAN pertanyaan baru.
- **duck:** uji menentukan = cek sisi-operator platform — handler NIU aktif
  di produksi? ke-91 jawaban kita pernah dievaluasi NIU? ada event
  kredit/reason code NIU di ledger?
- **sol:** pantau delta saldo "control user" — penanya baru atas jawaban
  inovatif yang diterima luas.
- Keduanya dinilai di atas rencana pantau pasif versi pra-konsultasi;
  pantauan delta saldo kita tetap berguna sebagai MONITOR, bukan pembeda.
- **PERUBAHAN DIBERLAKUKAN:** tindakan NIU berikutnya resmi = cek
  sisi-operator (§3.4 butir 4 baru) — dicatat sebagai langkah yang butuh
  keputusan user sebagai pengirim bila dilakukan. Pantau control-user masuk
  rencana pantau §5.3. Tidak ada uji NIU berbentuk pertanyaan baru.

### Q3 — Probe satu tembakan

- **Konvergen bersyarat (3 kursi):** probe hanya sah sebagai eksperimen
  satu-tembakan yang diprakomitmenkan, sesudah cek murah lain buntu, dengan
  kriteria perubahan kebijakan ditulis di depan; hasil nol TIDAK boleh
  ditafsirkan "NIU mati".
- **gemini (penengah) menambah dua prasyarat isolasi variabel:** (1) jawaban
  "gold standard" tepercaya yang memenuhi semua metrik NIU objektif sebagai
  kontrol; (2) konfirmasi sisi-platform bahwa fitur NIU aktif untuk tier
  akun kita. Tanpa keduanya, probe = bakar likuiditas.
- **PERUBAHAN DIBERLAKUKAN:** probe DITANGGUHKAN tanpa alokasi slot
  (§5.4 baru) sampai kedua prasyarat gemini terpenuhi.

### Q4 — Draf mana tembakan pertama

- **Konvergen (sol + duck sepakat penuh):** B (prover-batching ZK) =
  tembakan pertama.
- Keberatan penantang terhadap A dinilai frontier sebagai **CACAT PREMIS
  NYATA**: batas sandwich bukan ditentukan toleransi slippage saja — ukuran
  trade, kedalaman pool, fee, dan kondisi pasar ikut menentukan. A tetap
  layak SESUDAH diperbaiki dengan mengunci asumsi AMM/transaksi secara
  eksplisit di teks drafnya.
- **duck:** premis B dipersempit — tanyakan bagaimana biaya tetap prover per
  batch memengaruhi keputusan batching + latensi proof; JANGAN menjadikan
  trade-off fee-vs-finalitas sebagai premis (finalitas bisa bergantung
  mekanik lain; tautan kausalnya yang ditanyakan, bukan diasumsikan).
- **PERUBAHAN DIBERLAKUKAN:** antrean disusun ulang DAN dua teks ditulis
  ulang di `ANTREAN-BERTANYA-SIAP-2026-11-18.md` — Slot 1 = B versi premis
  dipersempit, Slot 2 = A versi asumsi terkunci, Slot 3 = C (tidak berubah).
  Kartu fee mengikuti posisi baru (B n=8, A n=9, C n=10).

### Q5 — Urutan pemulihan & status jalur

- **Konvergen 3 kursi:** pulihkan saldo lewat menjawab/menilai dulu; jalur
  ask TIDUR (dormant), BUKAN ditutup permanen; ask tidak pernah menjadi alat
  pemulihan saldo.
- **PERUBAHAN DIBERLAKUKAN:** status resmi jalur di §0 diubah dari
  "tertutup" menjadi **DORMANT-terkunci-EV** — ia bangun hanya lewat gerbang
  Q1 (P1/P3), bukan lewat saldo yang pulih dengan sendirinya.

### Koreksi angka dari konsultasi

- **duck** mengoreksi ambang P2 untuk 3 tembakan berurutan (n=8, 9, 10):
  saldo awal ≥ **3,7319**, BUKAN 3,7315 — gerbang fee diperiksa SEBELUM
  kredit pembuatan masuk (selisih 0,0004). Koreksi diterapkan di §5.1,
  §5.2, dan kartu fee Slot 3 di antrean.

---

*Dibuat 2026-11-18 ±10:05 WIB, read-only penuh. Berkas pendamping:
`belajar-2026-11-18/peta-ask/isr-detail-live-2026-11-18.json` (detail mentah
7 ISR + semua ISO-nya) dan `scores-notif-fresh-2026-11-18.json` (scores +
79 notifikasi mentah). Bangunan ditambah ±10:1x WIB (lihat §7).
**FINAL 2026-11-18** — vonis frontier dilipat di §8 dari
`belajar-2026-11-18/frontier-jalur3/SINTESIS-FRONTIER-JALUR3.md`; penanda
"finalisasi ditahan" dicabut.*
