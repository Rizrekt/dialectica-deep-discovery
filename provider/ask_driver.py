#!/usr/bin/env python3
"""Driver assist-loop jalur bertanya dengan HARD STOP sebelum create.

Kenapa bukan `trued ask` langsung: cmd_ask klien resmi CREATE di pemanggilan
yang sama begitu fase mencapai "ready" — tidak ada titik berhenti untuk kata
user. Driver ini memisahkan kedua langkah secara struktural:

  * `assist`  — menjalankan giliran assist (POST /api/node/isrs/assist).
    Giliran assist TIDAK mencharge apa pun: yang dihargai platform hanya
    POST /api/node/isr (api.md SS Fee for asking: "What is priced").
    Begitu fase = ready, driver MENULIS state file lalu BERHENTI.
    Ia tidak pernah memanggil create dari jalur assist.
  * `create`  — satu-satunya jalur ke POST /api/node/isr. Menolak jalan
    kecuali SEMUA ini ada: --live, --user-word (kata user sudah didapat),
    dan --confirm-fee yang sama persis dengan kutipan fee di state file.

Mode bawaan = DRY-RUN: tanpa --live dan tanpa --fixture, assist menolak
menyentuh jaringan. --fixture <file.json> memutar ulang respons assist
terekam (list objek step) untuk uji/demonstrasi offline.

State file (JSON, mode 0600): conversationId, settledArena, draft, phase,
askFee, token (struk curiosityToken — kutipan harga, bukan kredensial sesi).

Usage:
  python3 ask_driver.py assist "<draf>" [--arena general] [--live]
                          [--continue <conversationId>] [--fixture F]
                          [--state-out state.json]
  python3 ask_driver.py refresh --continue <conversationId> --live
  python3 ask_driver.py create --state state.json --confirm-fee 1.3504 \
                          --user-word --live
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.expanduser(
    "~/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts"))

CLASSIC_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["answer"],
    "properties": {"answer": {"type": "string", "minLength": 1,
                              "description": "Complete answer"}},
    "additionalProperties": False,
}
TERMINAL_PHASES = {"rejected", "blocked", "duplicate", "error"}
SYS_UNIQUENESS_RULE_ID = "SYS_UNIQUENESS"


# ---------------------------------------------------------------- transport
def live_transport(path, json_body=None, params=None, timeout=180):
    import trued
    return trued.call(path, params=params, json_body=json_body, timeout=timeout)


class FixtureTransport:
    """Memutar ulang respons terekam; mencatat semua panggilan."""

    def __init__(self, steps):
        self.steps = list(steps)
        self.calls = []

    def __call__(self, path, json_body=None, params=None, timeout=180):
        self.calls.append({"path": path, "json_body": json_body})
        if path == "/api/node/isrs/assist":
            if not self.steps:
                raise RuntimeError("fixture habis: tidak ada step tersisa")
            return self.steps.pop(0)
        if path == "/api/node/isr":
            return {"id": "fixture-isr-id"}
        raise RuntimeError(f"fixture: path tak dikenal {path}")


# ---------------------------------------------------------------- inti loop
def duplicate_reference(state):
    for rule in (state.get("ruleChecklist") or []):
        if rule.get("rule_id") != SYS_UNIQUENESS_RULE_ID or rule.get("passed"):
            continue
        return [d.get("id") for d in (rule.get("citedDuplicates") or [])
                if d.get("id")]
    return []


def settled_arena(current, reclassification):
    nxt = (reclassification or {}).get("arenaId")
    if not nxt or nxt == current:
        return current, None
    name = (reclassification or {}).get("arenaName") or nxt
    if (reclassification or {}).get("reason") == "ineligible":
        msg = f'"{current}" tidak terbuka untuk posting akun ini — ' \
              f'dipindah server ke "{name}".'
    else:
        msg = f'asisten memindahkan pertanyaan ke "{name}".'
    return nxt, msg


def withheld_reason(step):
    """Kenapa struk ditahan — dibaca dari vonis fee giliran yang sama."""
    fee = step.get("askFee")
    if not isinstance(fee, dict):
        return ("Giliran ini tidak membawa kutipan fee, jadi sebabnya tidak "
                "terlihat dari sini (penolakan server-side).")
    if fee.get("affordable") is False:
        return (f"Sebab: fee ask ini {fee.get('feeTrued')} $TRUED dan Wallet "
                f"hanya bisa membelanjakan {fee.get('spendableTrued')} $TRUED. "
                "Tambah isi Wallet dulu, lalu tanya lagi — mengganti kata-kata "
                "draf tidak menolong.")
    return ("Fee berada di dalam Wallet, jadi Wallet bukan penghalangnya. "
            "Coba sekali lagi dengan kata-kata yang diubah — itu menjalankan "
            "ulang cek keunikan terhadap kata-kata final. Bila giliran ready "
            "tetap tanpa struk, itu penolakan server-side: laporkan, jangan "
            "berputar mengganti kata.")


def assist_turn(transport, arena_id, conversation_id, user_message,
                draft=None, action=None):
    body = {"arenaId": arena_id, "userMessage": user_message}
    if draft is not None:
        body["clientState"] = {"questionDraft": draft}
    if conversation_id:
        body["conversationId"] = conversation_id
    if action:
        body["action"] = action
    return transport("/api/node/isrs/assist", json_body=body, timeout=180)


def run_assist(transport, arena_id, draft, conversation_id=None,
               action=None):
    """Satu giliran assist + klasifikasi hasil. TIDAK PERNAH create."""
    if action == "refresh_token":
        message = "Please refresh the curiosity token for my ready question."
    elif conversation_id:
        message = f'Please review my edited question:\n\n"{draft}"'
    else:
        message = draft
    step = assist_turn(transport, arena_id, conversation_id, message,
                       draft=draft, action=action)
    state = step.get("assistantState") or {}
    settled, arena_note = settled_arena(arena_id,
                                        step.get("arenaReclassification"))
    result = {
        "conversationId": step.get("conversationId") or conversation_id,
        "settledArena": settled,
        "arenaNote": arena_note,
        "draft": state.get("questionDraft") or draft,
        "phase": state.get("phase"),
        "message": step.get("message"),
        "askFee": step.get("askFee"),
        "token": step.get("curiosityToken"),
        "resolutionSpec": state.get("resolutionSpec"),
        "specBlockers": state.get("specBlockers") or [],
        "suggestion": (step.get("questionSuggestion") or {}).get("text"),
    }
    dups = duplicate_reference(state)
    if dups:
        result["outcome"] = "DUPLICATE_TERMINAL"
        result["duplicates"] = dups
    elif result["phase"] in TERMINAL_PHASES:
        result["outcome"] = "TERMINAL"
    elif result["phase"] != "ready":
        result["outcome"] = "NEEDS_WORDING"
    elif not result["token"]:
        result["outcome"] = "READY_WITHHELD"
        result["withheldReason"] = withheld_reason(step)
    else:
        result["outcome"] = "READY_STOP"  # <<< HARD STOP: menunggu kata user
    return result


def write_state(result, path):
    state = {k: result.get(k) for k in (
        "conversationId", "settledArena", "draft", "phase", "askFee",
        "token", "resolutionSpec")}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(state, f, indent=1)
    return path


def create_question(transport, state, confirm_fee, user_word):
    """Satu-satunya jalur create. Menolak tanpa kata user + fee cocok."""
    if not user_word:
        raise PermissionError(
            "create DITOLAK: --user-word tidak ada. Create hanya jalan atas "
            "kata user yang sudah didapat, bukan atas inisiatif driver.")
    token = state.get("token")
    if not token:
        raise ValueError(
            "create DITOLAK: state tidak membawa curiosityToken (struk "
            "ditahan di fase ready — lihat diagnosis askFee).")
    quoted = (state.get("askFee") or {}).get("feeTrued")
    if quoted is None:
        quoted = (token.get("fee") or {}).get("feeTrued")
    if confirm_fee is None or str(confirm_fee) != str(quoted):
        raise ValueError(
            f"create DITOLAK: --confirm-fee ({confirm_fee}) tidak sama "
            f"persis dengan kutipan di state ({quoted}).")
    body = {
        "content": state.get("draft"),
        "arenaId": state.get("settledArena"),
        "curiosityToken": token,  # echo persis, tanpa edit (api.md)
    }
    if state.get("resolutionSpec"):
        body["resolutionSpec"] = state["resolutionSpec"]
    if state.get("settledArena") == "general":
        body["outputSchema"] = CLASSIC_OUTPUT_SCHEMA
    created = transport("/api/node/isr", json_body=body, timeout=120)
    if not created.get("id"):
        raise RuntimeError("create tidak mengembalikan id")
    return created


# ---------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("assist")
    a.add_argument("draft")
    a.add_argument("--arena", default="general")
    a.add_argument("--continue", dest="conversation_id", default=None)
    a.add_argument("--live", action="store_true")
    a.add_argument("--fixture", default=None)
    a.add_argument("--state-out", default=None)

    r = sub.add_parser("refresh")
    r.add_argument("--continue", dest="conversation_id", required=True)
    r.add_argument("--arena", default="general")
    r.add_argument("--draft", default="")
    r.add_argument("--live", action="store_true")
    r.add_argument("--fixture", default=None)
    r.add_argument("--state-out", default=None)

    c = sub.add_parser("create")
    c.add_argument("--state", required=True)
    c.add_argument("--confirm-fee", default=None)
    c.add_argument("--user-word", action="store_true")
    c.add_argument("--live", action="store_true")

    args = ap.parse_args()

    if args.cmd in ("assist", "refresh"):
        if args.fixture:
            steps = json.load(open(args.fixture))
            transport = FixtureTransport(steps)
        elif args.live:
            transport = live_transport
        else:
            print("DRY-RUN: tanpa --live/--fixture driver tidak menyentuh "
                  "jaringan. Assist live tidak mencharge apa pun (yang "
                  "dihargai hanya create), tapi tetap opt-in eksplisit.")
            return 2
        if args.cmd == "assist":
            result = run_assist(transport, args.arena, args.draft,
                                conversation_id=args.conversation_id)
        else:
            result = run_assist(transport, args.arena, args.draft,
                                conversation_id=args.conversation_id,
                                action="refresh_token")
        print(json.dumps({k: v for k, v in result.items() if k != "token"},
                         indent=1, ensure_ascii=False))
        if result.get("token"):
            print("curiosityToken: DITERBITKAN (tersimpan di state file)")
        if args.state_out:
            write_state(result, args.state_out)
            print(f"state -> {args.state_out}")
        if result["outcome"] == "READY_STOP":
            print("\n*** HARD STOP — fase ready. Driver berhenti di sini. "
                  "Create hanya lewat subcommand `create` dengan --user-word "
                  "+ --confirm-fee yang cocok, sesudah user berkata jalan. ***")
        return 0

    if args.cmd == "create":
        if not args.live:
            print("create DITOLAK: create selalu live; --live wajib.")
            return 2
        state = json.load(open(args.state))
        try:
            created = create_question(live_transport, state,
                                      args.confirm_fee, args.user_word)
        except (PermissionError, ValueError) as e:
            print(str(e))
            return 1
        print(f"Question created -> https://dialectica.xyz/isr/{created['id']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
