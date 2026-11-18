#!/usr/bin/env python3
"""Self-dealing gate for the Verifier kit — Jalur 2 (2026-11-18).

THE RULE (platform, references/rules-of-the-game.md): "The protocol
forbids self-dealing: a user cannot answer their own Question, nor
verify their own Answer. These checks run on the *owning user*, not
the client or agent used." The server enforces it; this gate exists
so the kit never even DRAFTS a verdict it would be forbidden to
submit — a drafted-but-unsubmittable verdict wastes model spend,
and a gate failure discovered after submission would be an account
incident, not a bug.

WHAT COUNTS AS OURS (checked in this order, every hit recorded):
1. The Answer row's own `isOwnAgent` flag — the API sets it when
   the row belongs to an agent of the signed-in account (observed
   live 2026-11-18: our pilot ISO carries isOwnAgent=true).
2. The Answer's `author` (owning-user hash) is one of ours — the
   same hash the scores endpoint reports as our userId.
3. The Question's `author` is one of ours — the brief for this kit
   extends the bar to our own Questions as well: we never verify
   ANY Answer under a Question we asked, whoever wrote it.
4. The Answer id is in our local ISO denylist (our 27 revealed
   answers + every answer our Expert submits from now on).
5. The Question id is in our local ISR denylist (the 7 Questions
   we asked).
6. The Answer's ownerName matches one of our account's display
   names (weak signal — names are not unique — but a verifier that
   profits from ambiguity is not one we run; refuse and flag).

Pure: identity arrives as a plain dict, so tests need no files.
The runner builds the identity from live reads (scores userId) +
the local denylist file (ours.json, maintained by the operator).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OURS_PATH = os.path.join(HERE, "ours.json")


def load_identity(path=OURS_PATH):
    """Identity + denylists from the local file. Missing file =
    empty identity (the gate then relies on the API's own
    isOwnAgent/author signals, and the runner says so loudly)."""
    try:
        with open(path) as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        data = {}
    return {
        "user_ids": set(data.get("user_ids") or []),
        "usernames": set(data.get("usernames") or []),
        "iso_ids": set(data.get("iso_ids") or []),
        "isr_ids": set(data.get("isr_ids") or []),
    }


def check_candidate(candidate, identity):
    """candidate = parse_iso_row output (or any dict carrying the
    same keys). Returns {"allowed": bool, "reasons": [str]} —
    reasons names every signal that fired, so a refusal is
    auditable, not a shrug."""
    reasons = []
    if candidate.get("isOwnAgent"):
        reasons.append("server flag isOwnAgent=true (our own agent's Answer)")
    author = candidate.get("answerAuthor")
    if author and author in identity["user_ids"]:
        reasons.append("Answer author is our own user id")
    q_author = candidate.get("questionAuthor")
    if q_author and q_author in identity["user_ids"]:
        reasons.append("Question author is our own user id")
    if candidate.get("isoId") and candidate["isoId"] in identity["iso_ids"]:
        reasons.append("Answer id is in our local ISO denylist")
    if candidate.get("isrId") and candidate["isrId"] in identity["isr_ids"]:
        reasons.append("Question id is in our local ISR denylist")
    name = candidate.get("answerOwnerName")
    if name and name in identity["usernames"]:
        reasons.append(f"Answer ownerName matches our account name ({name})")
    return {"allowed": not reasons, "reasons": reasons}
