#!/usr/bin/env python3
"""GATED registration stub for a Verifier (IVSP) — Jalur 2.

REGISTRATION IS A USER DECISION (perintah user 2026-11-18: wilayah
terkunci — config/registration changes are proposals, never silent
executions). This script therefore CANNOT register anything as
delivered. It exists so that, on the day the user says "jalan",
the step is one deliberate command instead of an improvised one.

THE GATE (all three must hold before even the read-only preflight
runs):
  1. env  DIALECTICA_IVSP_USER_APPROVED=1
  2. file USER-APPROVAL-IVSP.txt beside this script, containing
     exactly the line: SAYA SETUJU REGISTRASI IVSP
  3. EXECUTE_ENABLED below — a code constant, False as delivered.
     Flipping it is a deliberate code edit, part of the go-live
     act itself, so no combination of env/files can arm this
     script by accident or by a stray cron.

With (1)+(2) but not (3), the script runs its READ-ONLY preflight
(session viewer, agent list, "no IVSP exists yet" assertion) and
prints the exact calls it WOULD make, then exits 4 (ARMED-DRY).
Without (1)/(2) it refuses and exits 3, having made no calls.

WHAT REGISTRATION IS (from the Expert's own birth, trued.py
_provision — the same endpoint, the type parameter differs):
  POST /api/node/agents/matrix            {"type": "IVSP"}
      -> {agentId, matrixHomeserver, matrixUserId}
  POST /api/node/agents/{agentId}/credential/reveal   {}
      -> one-time bootstrap credential
  state saved to ~/.dialectica-ivsp/agent.json (mode 0600) —
  a SEPARATE home from the Expert's ~/.dialectica, because one
  home = one credential = one serve lock.
The likeliest refusal is WAITLIST_PENDING (the Expert analogue:
"account can browse but not yet serve — that needs to be enabled
for you"); whether an IVSP-specific access gate exists is
BELUM-TERBUKTI until this step is attempted with approval.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

EXECUTE_ENABLED = False  # go-live edit #1 — see module docstring

APPROVAL_ENV = "DIALECTICA_IVSP_USER_APPROVED"
APPROVAL_FILE = os.path.join(HERE, "USER-APPROVAL-IVSP.txt")
APPROVAL_PHRASE = "SAYA SETUJU REGISTRASI IVSP"

PLANNED_CALLS = [
    ("POST", "/api/node/agents/matrix", {"type": "IVSP"}),
    ("POST", "/api/node/agents/{agentId}/credential/reveal", {}),
]


def approval_state(env=None, approval_file=None):
    """(env_ok, file_ok) — pure enough to test: env is a mapping.
    approval_file resolves against the module global at CALL time,
    so tests (and only tests) can point it elsewhere."""
    env = os.environ if env is None else env
    approval_file = APPROVAL_FILE if approval_file is None else approval_file
    env_ok = env.get(APPROVAL_ENV) == "1"
    file_ok = False
    try:
        with open(approval_file) as fh:
            file_ok = APPROVAL_PHRASE in fh.read()
    except OSError:
        file_ok = False
    return env_ok, file_ok


def preflight():
    """Read-only checks an armed run makes before the POSTs:
    who is signed in, which agents exist, no IVSP yet. Returns a
    report dict; raises RuntimeError on any failed expectation."""
    import verifier_common as vc
    agents_data = vc.api_get("/api/node/agents")
    agents = agents_data.get("agents") or []
    types = [(a.get("type"), a.get("implementationId")) for a in agents]
    ivsp = [a for a in agents if a.get("type") == "IVSP"]
    if ivsp:
        raise RuntimeError(
            f"an IVSP already exists on this account ({ivsp[0].get('id')}) "
            f"— registration would create a second one; stop and look.")
    return {"agents_existing": types, "ivsp_exists": False,
            "session": "ok"}


def main(argv=None):
    env_ok, file_ok = approval_state()
    if not (env_ok and file_ok):
        missing = []
        if not env_ok:
            missing.append(f"env {APPROVAL_ENV}=1")
        if not file_ok:
            missing.append(f"file {os.path.basename(APPROVAL_FILE)} "
                           f"containing '{APPROVAL_PHRASE}'")
        print("REFUSED — registration is a user decision and its "
              "approval markers are not all present. Missing: "
              + "; ".join(missing) + ". No calls were made.")
        return 3
    report = preflight()
    print(f"Preflight OK: {json.dumps(report)}")
    print("Planned calls (NOT made):")
    for method, path, body in PLANNED_CALLS:
        print(f"  {method} {path}  {json.dumps(body)}")
    if not EXECUTE_ENABLED:
        print("ARMED-DRY — EXECUTE_ENABLED is False in this build, so "
              "nothing was registered. The go-live act is: user says "
              "jalan -> flip EXECUTE_ENABLED -> rerun this script -> "
              "then configure the IVSP (strategy economist, arenas "
              "general) and start run_verifier.py against the new "
              "credential home ~/.dialectica-ivsp.")
        return 4
    # Reached only after a deliberate code edit + both markers.
    raise NotImplementedError(
        "execute path intentionally not wired in the delivered "
        "build; wire it in the go-live session, in the open, with "
        "the user present.")


if __name__ == "__main__":
    sys.exit(main())
