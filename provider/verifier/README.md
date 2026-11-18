# Verifier Kit — Jalur 2 (IVSP), Dialectica

Built 2026-11-18. Map + verdicts: `../../PETA-JALUR-2-VERIFIER-2026-11-18.md`.
Raw live evidence: `../../belajar-2026-11-18/peta-jalur-2/`.

## State of this build: DRY-RUN ONLY

No IVSP exists on the account. Nothing here registers one, submits a
verification, or changes any platform config — by construction:

| Piece | File | Lock |
|---|---|---|
| Read-only API + payload parsers | `verifier_common.py` | GET-only; no write helper exists |
| Self-dealing gate (pure) | `self_dealing_gate.py` + `ours.json` | refuses own answers/questions, incl. stricter house policy |
| Local verdict drafter (pure) | `verdict_drafter.py` | offline; unopened source = "unknown", never a pass |
| Model-lane drafter | `lane_drafter.py` | public prompt only (relay fence); verdict recomputed locally |
| Registration | `register_ivsp.py` | needs env + approval file + `EXECUTE_ENABLED` code edit; as delivered it can only refuse (exit 3) or preflight-and-print (exit 4) |
| Runner | `run_verifier.py` | `--dry-run` default; `--send` refuses unconditionally (exit 5) |
| Tests | `test_verifier_kit.py` | 33 tests, all green at delivery |

## Run the dry-run

```bash
cd ~/workspace/research/dialectica/provider/verifier
python3 -m unittest test_verifier_kit            # 33 tests
python3 run_verifier.py --dry-run                # live public reads -> drafts
python3 run_verifier.py --dry-run --lanes        # + Nemotron & qwen drafts (paced, shared relay budget)
python3 run_verifier.py --send                   # refuses — the lock is the point
python3 register_ivsp.py                         # refuses — markers absent
```

Drafts land in `verdict-drafts.jsonl` (append-only).

## Verdict posture (frontier-folded 2026-11-18, map §6 Q2)

Strict 4-check posture. On ambiguous cases there is **no forced
verdict**: if the lanes disagree on an ambiguous case, the outcome
is abstain / draft-only — never a forced majority. Anticipated
consensus may be logged as a confidence signal; it never drives a
verdict. The checklist decides, not a guess at the panel's mood.

## Known gap — per-verdict model cost is NOT recorded yet

The runner does not record model cost per verdict (no cost field in
`verdict-drafts.jsonl`; the lane drafter does not log per-call cost
either). This is a **recorded shortcoming, not a feature**: the
14-day pilot's break-even can only be computed from our own numbers
once per-verdict lane cost is logged, from dry-run onward. Until
then, break-even rests on the platform-side realized figure alone
(0.8217 $TRUED per submitted verdict, map §3.3). Closing this gap
is a code task for the pilot phase — it is deliberately not claimed
as built here.

## Go-live (user's act, in the open — see the map's checklist)

**Sequence gate (frontier Q4, map §5 step 5):** registration may be
prepared, but do NOT arm any send path until the Expert lane is
proven paid (first paid verified from the Doctrine A mini-batch /
doctrine). Dry-run drafting is exempt — it runs now.

1. User says jalan for Jalur 2.
2. Create `USER-APPROVAL-IVSP.txt` with the exact phrase from
   `register_ivsp.py`, set `DIALECTICA_IVSP_USER_APPROVED=1`, flip
   `EXECUTE_ENABLED`, wire + review the execute path, run it.
3. Configure the new IVSP via its own schema — never via the
   Expert's config. Frontier DEFAULT-USULAN (map §6 Q1/Q3):
   strategy `economist`, arenas `general`, `minReward` **0.6**.
   This is a written proposal weighed by both frontier seats,
   **not a decision** — the user's registration gate decides.
4. Give the runner its live work source (gateway connection from
   `~/.dialectica-ivsp/`) and a separately reviewed send path.
   Neither exists in this build, deliberately.
