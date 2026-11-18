#!/usr/bin/env python3
"""DIALECTICA_PREPARE_CMD for the gated Vyce serve lane (2026-11-15).

trued runs this BEFORE claiming, with the search row as JSON on
stdin; no job exists yet. Exit 0 = we hold a prepared, gate-sendable
answer for this Question (cached for the provider) and trued may
claim it. Exit nonzero = pass the Question over at zero cost.

Gate order (all BEFORE any claim; generation only after liveness):
1. Row sanity: an id and question text must be present.
2. LIVENESS (serve_gate.liveness_gate_for_row): the three-field
   filter over the fetched ISR detail — a target whose marathon
   round already ended is passed over here, never answered (the
   §82 trap: 11/11 sampled serve answers were post-round). Armed
   by run_serve (DIALECTICA_SERVE_GATE_FETCH=1); a failed fetch is
   fail-closed — passing over costs nothing.
3. Generation through vyce_provider.py (claim machinery, steering
   included) + the shared serve gate. A withheld draft (thinking
   trace, §45 floor, audit findings, format) = pass-over.

Unlike the §39 lane there is NO Class-2 Pioneer screen here: the
Vyce serve's coverage is the keyword poller's (marathon included) —
narrowing it would change serve coverage, a lab decision. The
liveness gate is what keeps that coverage from answering dead
rounds.

PICK STATE (2026-11-17, aturan ketat user 10:50/10:52): a sendable
prepare also records the pick-time state (class, viso, answer
baseline) as a sidecar next to the cached answer — the send-time
freshness gate (freshness_gate, in vyce_serve_provider) judges the
room against the room as picked, not as found. Recording is
best-effort: a failed sidecar degrades the send-time check to its
conservative class rules, never blocks a prepare.

POOL SEAM + PRE-CLAIM SCREEN (2026-11-18, PERBAIKAN-KOLAM-DOKTRIN;
Doktrin A armed only — with the env off this module is exactly its
pre-doctrine self): (1) an unclassified row passes over
fail-closed — while the doctrine is armed, the doctrine pool is
the only pool (mini-batch 3: 12 unclassified serve rows burned 9
generations, 0 of 113 parked tickets were ever presented);
(2) before generation, the send-time freshness rules run once
against the pick-time payloads (_preclaim_freshness_screen) — a
room already dead at pick (the a9408129 pattern: viso 0, crowd 79
at pick, withheld only after its claim stranded the single
concurrency slot for ~30 min) is passed over at zero cost. The
send-time veto itself is unchanged and still guards the
generation window.

FRONTIER FOLD (2026-11-18, F-31D — SINTESIS-FRONTIER-PERBAIKAN-
JALUR1; duck + gpt-5.6-sol convergent 4/4, desain FINAL):
(3) Q2 reconsideration — every doctrine decision is appended to
the doctrine decision log (doctrine_a.log_decision) with its
reason class, and the lane decision re-reads the trigger store
on EVERY call: a row passed over while unclassified / TUNGGU /
not-yet-due is decided FRESH from its current classification
whenever the poller presents it again — this layer never caches
a pass. (The stock client's in-session 6 h prepare-skip cannot
be lifted from here — prepare is simply never invoked while it
holds the row; recorded as a limitation in PERBAIKAN-KOLAM-
DOKTRIN §7, with count_lost_after_skip as the deciding
measurement.) (4) Q3 tata cara — the screen's verdict is logged
with phase "pra-klaim" into the same freshness log the
send-time veto writes with phase "detik-kirim", each with its
reasons; the pick data the screen judged is the recorded
baseline (no second fetch). (5) Q4 claim sequencing — before
generation, the Expert's own job list is read
(_job_sequence_block): any previous job not yet in a terminal
state (or an unreadable job list) holds this row — no claim is
stacked on an outcome that is not yet certainly known.
"""
import json
import os
import sys
import time

import cloudflare_serve_common as csc
import doctrine_a
import freshness_gate
import novelty_context
import serve_gate
import vyce_serve_common as vsc
from openrouter_wrapper import format_withhold_breakdown


def _doctrine_lane_decision(isr_id, now):
    """Doktrin A lane glue (2026-11-18; called ONLY while the
    doctrine is armed). Returns (lane, pass_reason, reason_class):
    lane is CEPAT / TELAT / None; pass_reason non-None means
    prepare must pass the question over at zero cost. TELAT
    questions live in the late queue: not-yet-due = pass (the
    queue releases them at delay 2–6 h); due = prepare now under
    the TELAT lane. TUNGGU (grey zone, re-evaluation pending) =
    pass. A lane whose daily allotment is spent = pass (slots
    are never forced).

    POOL SEAM (2026-11-18, PERBAIKAN-KOLAM-DOKTRIN): an
    UNCLASSIFIED question under an armed doctrine now passes
    over too — fail-closed. The original glue returned
    (None, None) for it ("tak terklasifikasi -> alur lama
    persis"), and mini-batch 3 proved what that costs: the
    poller's own search (q=wallet, 3-day window) presented 12
    unclassified rows, the doctrine pool was never entered,
    and 9 generations burned on legacy flow while 113 parked
    tickets went unreleased. While the doctrine is armed the
    doctrine pool is the ONLY pool; a row the observer has
    not classified is outside it by definition. (The serve
    search is band-aligned to the same pool — questionMinAgeMs
    2 h / questionMaxAgeMs 6 h in the unit — so a legitimate
    row has had its whole young life to be classified before
    the poller can present it.)

    RECONSIDERATION (FRONTIER FOLD 2026-11-18, Q2 — duck's
    refinement of fail-closed): the trigger store is re-read
    on EVERY call and the decision is taken from the CURRENT
    record — a pass is never cached on this side. A row passed
    while unclassified, TUNGGU, or not-yet-due is decided
    fresh whenever it is presented again: a classification
    that landed in the meantime (the observer overwrites
    records; TUNGGU is re-decided at +30 min) or a ticket that
    has since come due changes the answer. Every decision is
    appended to the doctrine decision log with its reason
    class, so tickets lost to the one lock this layer cannot
    lift — the stock client's in-session 6 h prepare-skip —
    are countable after the fact (doctrine_a.
    count_lost_after_skip)."""
    store = doctrine_a.load_trigger_store()
    rec = doctrine_a.trigger_record(store, isr_id)
    if rec is None:
        doctrine_a.log_decision(isr_id, "pass", "unclassified",
                                now=now)
        return None, ("Doktrin A: pertanyaan TIDAK terklasifikasi "
                      "pengamat — di luar kolam doktrin; dilewati "
                      "tanpa biaya (jahitan kolam 2026-11-18)"), \
            "unclassified"
    mode = rec.get("mode")
    if mode == doctrine_a.MODE_WAIT:
        doctrine_a.log_decision(isr_id, "pass", "wait", mode=mode,
                                now=now)
        return None, ("Doktrin A: mode TUNGGU — klasifikasi abu-abu "
                      "belum diputus ulang; pertanyaan dilewati"), \
            "wait"
    if mode == doctrine_a.LANE_LATE:
        birth = rec.get("birth_ts")
        entry = doctrine_a.park(isr_id, birth, now=now) \
            if birth is not None else None
        due = entry is not None and \
            entry["release_at"] <= now <= entry["expires_at"]
        if not due:
            doctrine_a.log_decision(isr_id, "pass", "not_due",
                                    lane=doctrine_a.LANE_LATE,
                                    mode=mode, now=now)
            return None, ("Doktrin A: mode TELAT — pertanyaan "
                          "diparkir di antrean telat sampai jendela "
                          "tunda 2–6 jam; belum jatuh tempo"), \
                "not_due"
        if doctrine_a.lane_remaining(doctrine_a.LANE_LATE, now) <= 0:
            doctrine_a.log_decision(isr_id, "pass", "lane_spent",
                                    lane=doctrine_a.LANE_LATE,
                                    mode=mode, now=now)
            return None, ("Doktrin A: jatah lane TELAT hari ini "
                          "habis (7) — pertanyaan dilewati"), \
                "lane_spent"
        doctrine_a.log_decision(isr_id, "proceed", "due",
                                lane=doctrine_a.LANE_LATE,
                                mode=mode, now=now)
        return doctrine_a.LANE_LATE, None, "due"
    if mode == doctrine_a.LANE_FAST:
        if doctrine_a.lane_remaining(doctrine_a.LANE_FAST, now) <= 0:
            doctrine_a.log_decision(isr_id, "pass", "lane_spent",
                                    lane=doctrine_a.LANE_FAST,
                                    mode=mode, now=now)
            return None, ("Doktrin A: jatah lane CEPAT hari ini "
                          "habis (3) — slot cepat tidak dipaksa; "
                          "pertanyaan dilewati"), "lane_spent"
        doctrine_a.log_decision(isr_id, "proceed", "fast_ok",
                                lane=doctrine_a.LANE_FAST,
                                mode=mode, now=now)
        return doctrine_a.LANE_FAST, None, "fast_ok"
    doctrine_a.log_decision(isr_id, "proceed", "mode_tak_dikenal",
                            mode=mode, now=now)
    return None, None, "mode_tak_dikenal"


def _preclaim_freshness_screen(row, isr_id, lane, detail_fetcher=None,
                               isos_fetcher=None, now=None):
    """Layar kesegaran PRA-KLAIM (2026-11-18, PERBAIKAN-KOLAM-
    DOKTRIN — ekor temuan (a) mini-batch 3). Runs the SEND-time
    freshness rules (freshness_gate.check_freshness, the exact
    rule code — no re-implementation) against the PICK-time
    payloads, BEFORE generation and BEFORE any claim exists.

    Why this exists: in mini-batch 3 the row a9408129 was picked
    at viso 0 with a crowd of 79 ALREADY recorded in its pick
    state, generated, claimed — and only then withheld by the
    send-time veto. The drop stranded an intent ISO on the
    server and locked the Expert's single concurrency slot for
    the job's ~30-min liveness timeout, refusing the next claim
    ("Agent at capacity (1/1)"). Every fact the veto used was
    knowable at pick time; the screen moves that knowledge
    earlier, where a pass-over is free (no generation burned,
    no claim, no slot). The send-time veto in
    vyce_serve_provider STAYS: it alone sees a room that fills
    DURING generation. This screen is an earlier exit, never a
    replacement.

    Doctrine-armed only (the caller gates). Returns
    (verdict, pick, (isos, state)): the fetched ISO list is
    handed back so the post-generation sidecar reuses it
    instead of fetching twice. Fetchers follow the
    serve_gate.fetch_isr_detail / novelty_context.fetch_isos
    contract; an unreadable state is judged by check_freshness
    itself (unverified withholds in block mode — at prepare a
    pass-over costs nothing, so fail-closed is free)."""
    det_fetcher = detail_fetcher or serve_gate.fetch_isr_detail
    iso_fetcher = isos_fetcher or novelty_context.fetch_isos
    detail, d_state = det_fetcher(isr_id)
    isos, i_state = iso_fetcher(isr_id)
    pick = freshness_gate.pick_state_from_row(
        row, isos=isos if i_state == "ok" else None, now=now,
        lane=lane)
    verdict = freshness_gate.check_freshness(
        isr_id, pick_state=pick,
        detail_fetcher=lambda _i: (detail, d_state),
        isos_fetcher=lambda _i: (isos, i_state),
        now=now, doctrine=True, phase="pra-klaim")
    return verdict, pick, (isos, i_state)


# The stock client's own terminal vocabulary (trued.py
# TERMINAL_JOB_STATES) — a job in any other state, or with no
# readable state, is NOT terminal-certain.
TERMINAL_JOB_STATES = frozenset(
    {"completed", "failed", "cancelled", "abandoned"})


def _fetch_own_jobs():
    """(jobs, state) — this Expert's job list via the audited
    client, on the serve_gate fetch contract ("ok" / "failed" /
    "disabled"). Only touches the network when the launcher
    armed fetching (DIALECTICA_SERVE_GATE_FETCH=1 — run_serve
    sets it for the gated lane, the same arming the liveness
    and freshness fetches ride on); the client's call() exits
    on API error, so BaseException is caught — a failed fetch
    is data for the gate, not a crash."""
    if os.environ.get(serve_gate.FETCH_ENV) != "1":
        return None, "disabled"
    if serve_gate.TRUED_DIR not in sys.path:
        sys.path.insert(0, serve_gate.TRUED_DIR)
    try:
        import trued
        agent_id = trued.resolve_agent_id(None)
        data = trued.call(f"/api/node/agents/{agent_id}/jobs",
                          timeout=30)
    except BaseException:  # noqa: BLE001 - includes SystemExit
        return None, "failed"
    if not isinstance(data, dict) \
            or not isinstance(data.get("jobs"), list):
        return None, "failed"
    return data["jobs"], "ok"


def _job_sequence_block(jobs_fetcher=None):
    """GERBANG SEKUENSING KLAIM (FRONTIER FOLD 2026-11-18, Q4 —
    ditetapkan WAJIB oleh dua kursi frontier): a hold reason
    when a claim must NOT be stacked on the previous job, else
    None.

    Why this gate has to live here: the stock client's claim
    poller runs on its own thread, in parallel with the loop
    that answers jobs — nothing in the client sequences a new
    claim behind the previous job's outcome (mini-batch 3: the
    claim after a post-claim drop was attempted into a slot the
    dropped job still held, and only the server's "at capacity
    (1/1)" refusal stopped it — after prepare had already run).
    Prepare is the one pre-claim hook this layer owns, so the
    check lives here, BEFORE generation: while any job of this
    Expert is not yet in a terminal state, this row is held
    (passed over + recorded in the doctrine decision log) —
    generating into a claim that cannot land burns the day's
    scarcest resource for nothing. An UNREADABLE job list
    holds too: "not terminal-certain" is the gate's exact
    trigger, and an unreadable list is precisely that. Only
    "disabled" (the launcher never armed fetching — a launch
    configuration, not a runtime uncertainty) leaves the gate
    inactive.

    Honest cost: a held row takes the stock client's session
    prepare-skip like any pass-over, so a TELAT row held behind
    a dying job may miss its window for this session. The
    frontier verdict accepted conservative sequencing with the
    skip mechanics on the table; the alternative (generate
    first, be refused at capacity after) burns a generation
    AND still skips the row."""
    fetcher = jobs_fetcher or _fetch_own_jobs
    jobs, state = fetcher()
    if state == "disabled":
        return None
    if state != "ok" or not isinstance(jobs, list):
        return ("gerbang sekuensing klaim (Q4): keadaan jobs "
                "Expert TIDAK terbaca — hasil job sebelumnya "
                "belum terminal-pasti; klaim DITAHAN dan dicatat")
    pending = [j for j in jobs if isinstance(j, dict)
               and str(j.get("jobStatus") or "")
               not in TERMINAL_JOB_STATES]
    if not pending:
        return None
    states = sorted({str(j.get("jobStatus") or "?")
                     for j in pending})
    return (f"gerbang sekuensing klaim (Q4): {len(pending)} job "
            f"sebelumnya belum terminal-pasti (status: "
            f"{', '.join(states)}) — klaim DITAHAN sampai hasil "
            f"job itu pasti; tidak ada klaim baru di atas job "
            f"yang belum selesai")


def prepare_row(row, detail_fetcher=None, generate_fn=None,
                isos_fetcher=None, doctrine=None, now=None,
                jobs_fetcher=None):
    """(exit_code, final_line). Split from main() for tests; the
    fetcher/generator default to the real, launcher-armed ones.
    `doctrine` (Doktrin A) defaults to the arming env; while the
    doctrine is off, every lane behaviour below is skipped and
    this function is byte-for-byte its pre-doctrine self."""
    isr_id = csc.row_isr_id(row)
    if not isr_id:
        return 1, "baris tanpa id/isrId"
    text = (str((row or {}).get("title") or "") + "\n"
            + str((row or {}).get("content") or "")).strip()
    if not text:
        return 1, "baris tanpa judul/konten pertanyaan"
    ok, reason = serve_gate.liveness_gate_for_row(
        row, detail_fetcher=detail_fetcher, isr_id=isr_id)
    if not ok:
        return 1, f"gerbang liveness: {reason}"
    if doctrine is None:
        doctrine = doctrine_a.doctrine_armed()
    lane = None
    screen_pick = None
    screen_isos = None
    if doctrine:
        now = time.time() if now is None else now
        lane, pass_reason, _reason_class = \
            _doctrine_lane_decision(isr_id, now)
        if pass_reason is not None:
            return 1, pass_reason
        # Claim-sequencing gate (FRONTIER FOLD Q4): no claim —
        # and no generation toward one — while the previous
        # job's outcome is not yet certainly known.
        seq_block = _job_sequence_block(jobs_fetcher)
        if seq_block is not None:
            doctrine_a.log_decision(isr_id, "hold", "job_sequence",
                                    lane=lane, now=now)
            return 1, seq_block
        # Pre-claim freshness screen (2026-11-18): judge the
        # room as picked, with the send-time rules, BEFORE the
        # generation burns a cap slot and before any claim can
        # strand a job. A withhold here is a free pass-over.
        verdict, screen_pick, screen_isos = \
            _preclaim_freshness_screen(
                row, isr_id, lane, detail_fetcher=detail_fetcher,
                isos_fetcher=isos_fetcher, now=now)
        if verdict["withhold"]:
            return 1, (f"layar kesegaran PRA-KLAIM menahan "
                       f"(status={verdict['status']}): "
                       f"{'; '.join(verdict['reasons'])} — "
                       f"pertanyaan dilewati sebelum generasi, "
                       f"tidak ada klaim")
    prompt = csc.prompt_from_row(row)
    try:
        result = vsc.vyce_pipeline(prompt, isr_id,
                                   generate_fn=generate_fn)
    except Exception as ex:  # noqa: BLE001 - a failed prepare is a pass
        return 1, f"generasi Vyce gagal ({type(ex).__name__}: {ex})"
    if not result["sendable"]:
        return 1, (f"draf ditahan gerbang serve "
                   f"(status={result['status']}, "
                   f"{format_withhold_breakdown(result['report'])}; "
                   f"alasan: "
                   f"{'; '.join(result['gate']['reasons'][:3])}) — "
                   f"pertanyaan dilewati, bukan diklaim")
    if doctrine and lane is not None:
        # Consume the lane token + close the queue entry only now
        # that a sendable answer exists — a failed generation must
        # not burn a daily slot or a parking.
        doctrine_a.lane_take(lane, now)
        if lane == doctrine_a.LANE_LATE:
            doctrine_a.release(isr_id, now=now)
    csc.write_cache(isr_id, result["text"])
    # Pick state for the send-time freshness gate (best-effort; see
    # module docstring). The pick-time ISO list gives the answer
    # baseline; an unarmed/failed fetch records honest Nones. The
    # Doktrin A lane rides along so the send-time check can judge
    # the room by the lane's rules while the doctrine is armed.
    try:
        if screen_pick is not None:
            # The pre-claim screen already fetched and judged
            # this exact pick state — record THAT (the send-time
            # veto then compares against the state the screen
            # saw, and no second ISO fetch is spent).
            freshness_gate.record_pick_state(isr_id, screen_pick)
        else:
            fetcher = isos_fetcher or novelty_context.fetch_isos
            isos, _state = fetcher(isr_id)
            freshness_gate.record_pick_state(
                isr_id, freshness_gate.pick_state_from_row(
                    row, isos=isos if _state == "ok" else None,
                    lane=lane))
    except Exception:  # noqa: BLE001 - recording never blocks prepare
        pass
    return 0, (f"jawaban siap untuk {isr_id} "
               f"({result['report']['chars_final']} karakter, "
               f"gerbang serve lolos)")


def main():
    raw = sys.stdin.read()
    try:
        row = json.loads(raw) if raw.strip() else {}
    except ValueError:
        print("payload prepare bukan JSON — pertanyaan dilewati")
        return 1
    rc, line = prepare_row(row)
    print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
