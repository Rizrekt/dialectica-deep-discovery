#!/usr/bin/env python3
"""Shared plumbing for the Dialectica Verifier (IVSP) kit — Jalur 2
(built 2026-11-18; design: PETA-JALUR-2-VERIFIER-2026-11-18.md).

WHAT THIS MODULE IS. Read-only API access (session token, the same
one the Expert lane uses — never printed, never logged) plus the
PURE payload parsers that turn platform shapes into verifier work
items. Nothing in this module writes to the platform: the only API
verbs used here are GETs. Registration and verdict submission live
in their own modules behind explicit locks (register_ivsp.py,
run_verifier.py --send) and are NOT reachable from here.

PLATFORM SHAPES (evidence: references/api.md of client v0.22.4;
trued.py job/gateway code; live pulls 2026-11-18 saved in
belajar-2026-11-18/peta-jalur-2/):

- A jobs-endpoint record is {id, type, jobStatus, input, output?,
  error?}. `type` names the OUTPUT entity: "ISO" = a job that
  produces an Answer (every job our Expert has ever run), "VFP" = a
  job that produces a Verification. Our account's 40-job history
  holds 40 ISO and 0 VFP (live, 2026-11-18).
- An answering job's input is {isrId, isrContent, isrAuthor,
  domainTags}. A verification job's input has never been observed
  on this account (BELUM-TERBUKTI); the gateway opportunity for a
  verification names the Answer in `targetIsoId` beside `isrId`
  (trued.py job_ids_from_opportunity), so the parser accepts both
  spellings and keeps whatever arrived verbatim under `raw`.
- Gateway events (Matrix room messages from the system user) come
  in three kinds — evaluate-request, execute-job, schema-correction
  — classified exactly as trued.py's classify_event does.
"""
import json
import os
import urllib.parse
import urllib.request

BASE = os.environ.get("DIALECTICA_BASE_URL", "https://dialectica.xyz").rstrip("/")
SESSION_PATH = os.path.expanduser("~/.dialectica/session")

# The home a future IVSP credential will live in. Deliberately NOT
# ~/.dialectica: that directory holds the Expert's agent.json and
# serve.lock, and one home directory = one credential = one serve
# process (trued.py _hold_serve_lock). This kit never writes here;
# the path exists so the runner can REPORT that no IVSP is set up.
IVSP_HOME = os.path.expanduser("~/.dialectica-ivsp")
IVSP_STATE_PATH = os.path.join(IVSP_HOME, "agent.json")


def _session_token():
    """The operator's session token, or None. Read from the same
    file the Expert client uses; the value is never returned to a
    log or a print anywhere in this kit."""
    try:
        with open(SESSION_PATH) as fh:
            return fh.read().strip() or None
    except OSError:
        return None


def api_get(path, params=None, timeout=60):
    """One authenticated GET against the node API. Returns the
    envelope's `data` dict, or raises RuntimeError with the server's
    error code/message. Reads only — there is no write helper here
    on purpose."""
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, method="GET")
    token = _session_token()
    if token:
        req.add_header("X-Active-Session", token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:  # noqa: BLE001 - surface the status only
            raise RuntimeError(f"HTTP {exc.code} on GET {path}") from exc
    if not payload.get("success", False):
        err = payload.get("error") or {}
        raise RuntimeError(
            f"{err.get('code', 'API_ERROR')}: {err.get('message', '')}".strip())
    return payload.get("data") or {}


# ─── Pure payload parsers ────────────────────────────────────────────

def answer_body(iso_row):
    """The Answer text of an ISO row, whichever schema the arena
    used: classic `answer`, or forecasting `reasoning` (+prediction).
    Returns "" when the row carries no revealed body."""
    structured = (((iso_row or {}).get("reveal") or {}).get("data") or {}
                  ).get("structured_data") or {}
    if structured.get("answer"):
        return structured["answer"]
    parts = [structured.get("reasoning") or "",
             structured.get("prediction") or ""]
    return "\n".join(p for p in parts if p).strip()


def parse_iso_row(iso_row, question=None):
    """Normalise one Answer row (GET /api/node/isos/:isrId shape)
    into a verifier candidate. Pure."""
    iso_row = iso_row or {}
    question = question or {}
    return {
        "kind": "VFP-candidate",
        "isrId": iso_row.get("isrId") or question.get("id"),
        "isoId": iso_row.get("id"),
        "question": question.get("content") or "",
        "questionAuthor": question.get("author"),
        "answer": answer_body(iso_row),
        "answerAuthor": iso_row.get("author"),
        "answerOwnerName": iso_row.get("ownerName"),
        "isOwnAgent": bool(iso_row.get("isOwnAgent")),
        "status": iso_row.get("status"),
        "verifierCount": iso_row.get("verifierCount"),
        "supportedCount": iso_row.get("supportedCount"),
        "refutationCount": iso_row.get("refutationCount"),
        "marathonEligible": iso_row.get("marathonEligible"),
        "raw": iso_row,
    }


def parse_job_record(job):
    """Normalise one jobs-endpoint record. `type` is the OUTPUT
    entity: ISO = answering job, VFP = verification job. Pure."""
    job = job or {}
    inp = job.get("input") or {}
    jtype = str(job.get("type") or "").upper()
    return {
        "kind": "VFP" if jtype == "VFP" else ("ISR" if jtype == "ISO" else jtype),
        "jobId": job.get("id"),
        "jobStatus": job.get("jobStatus"),
        "isrId": inp.get("isrId") or inp.get("targetIsrId"),
        "isoId": inp.get("targetIsoId") or inp.get("isoId"),
        "question": inp.get("isrContent") or "",
        "questionAuthor": inp.get("isrAuthor"),
        "answer": inp.get("isoContent") or inp.get("answer") or "",
        "raw": job,
    }


def parse_gateway_event(event, system_user_id):
    """Classify one gateway (Matrix) event exactly as the Expert
    client does: only the Dialectica system user issues work, and
    anything else is dropped before its body can reach a model.
    Returns a work item dict or None. Pure."""
    if not system_user_id or not isinstance(event, dict):
        return None
    if event.get("sender") != system_user_id:
        return None
    content = event.get("content") or {}
    kind = content.get("org.dialectica.type")
    data = content.get("org.dialectica.data") or {}
    if kind == "evaluate-request" and data.get("requestId"):
        return {"kind": "evaluate", "requestId": data["requestId"],
                "opportunity": data.get("opportunity")}
    if kind == "execute-job":
        if not data.get("jobId"):
            return None
        opp = data.get("opportunity") or {}
        return {
            "kind": "job",
            "jobId": data.get("jobId"),
            "rootEventId": event.get("event_id"),
            "prompt": content.get("body") or "",
            "jobKind": opp.get("type"),
            "isrId": opp.get("targetIsrId") or opp.get("isrId"),
            "isoId": opp.get("targetIsoId"),
            "opportunity": opp,
        }
    if kind == "schema-correction":
        return {"kind": "correction", "jobId": data.get("jobId"),
                "rootEventId": event.get("event_id"),
                "prompt": content.get("body") or ""}
    return None
