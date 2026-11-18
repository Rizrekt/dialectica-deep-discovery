#!/usr/bin/env python3
"""Gemini free-tier provider for Dialectica's trued.py (DIALECTICA_PROVIDER_CMD).

Contract (from the audited trued.py): read the prompt on stdin, write ONLY the
answer on stdout. All diagnostics go to stderr.

The API key is injected at runtime through the GEMINI_API_KEY environment
variable by the launcher, which fetches the vault surrogate for the
custom.google-gemini credential; the real key is swapped in on egress to
generativelanguage.googleapis.com and never stored in this file or on disk.

Behaviour:
- POST /v1beta/models/<model>:generateContent with header x-goog-api-key.
- Google Search grounding requested by default (GEMINI_GROUNDING=0 disables);
  if the API rejects the tools field, retry once without it.
- 429/503 retried with 20/45/90 s backoff (the free tier is congested).
- A hard failure on one model falls through to the next candidate model.
- The wrapper has no file, shell, or network access beyond the Gemini API:
  the answering model cannot reach anything on this machine.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
BACKOFF_S = [20, 45, 90]
TIMEOUT_S = 240


def candidate_models():
    primary = os.environ.get("GEMINI_MODEL", "").strip()
    models = [primary] if primary else []
    for m in ("gemini-3-flash-preview", "gemini-3.8-flash", "gemini-flash-latest"):
        if m not in models:
            models.append(m)
    return models


WORLD_KEYWORDS = ("price", "market", "current", "today", "latest", "news",
                  "forecast", "election", "weather", "score", "odds",
                  "will ", "by 20", "before 20", "http", "search", "online")


def call_gemini(model, prompt, api_key, grounding):
    # Grounded answers bill like ~20 plain requests against the free-tier
    # ~20 RPD quota (verified live 2026-11-08: grounded -> 429 quota while
    # the same key answers the same prompt plain in <1s). Ground ONLY
    # prompts that genuinely ask about the outside world.
    if grounding:
        low = prompt.lower()
        grounding = any(k in low for k in WORLD_KEYWORDS)
    body = {"contents": [{"parts": [{"text": prompt}]}],
            # Output bound (2026-11-16, audit S2): previously no
            # generationConfig at all — the server default decided.
            "generationConfig": {"maxOutputTokens": 8192}}
    if grounding:
        body["tools"] = [{"google_search": {}}]
    req = urllib.request.Request(
        f"{API_BASE}/{model}:generateContent",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("x-goog-api-key", api_key)
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    candidates = payload.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"no candidates in response: {json.dumps(payload)[:300]}")
    parts = (candidates[0].get("content") or {}).get("parts") or []
    # Thought-part filter (2026-11-16, audit S2): Gemini thinking
    # models return thought parts (thought=true) in the same parts
    # list; joining ALL parts would mix the raw thinking monologue
    # into the answer — the f0bb3586 species through another door
    # (the same leak the Vyce reasoning_content fallback had).
    text = "".join(p.get("text", "") for p in parts
                   if not p.get("thought")).strip()
    if not text:
        raise RuntimeError("empty answer text from model")
    return text


def main():
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("gemini_provider: empty prompt on stdin", file=sys.stderr)
        return 2
    # AUDIT S1 FENCE (2026-11-16): like vyce_provider, this provider's
    # stdout is submitted directly on the one-shot claim path — no
    # wrapper/floor/trace gate runs there. Lane dormant (grounding
    # disabled §29.4); do not re-activate for claims without a gate.
    print("gemini_provider: PERINGATAN S1 — jalur jawaban LANGSUNG "
          "tanpa wrapper/gerbang mekanik (lane tertidur; lihat "
          "AUDIT-SABOTASE-PIPA-2026-11-16 S1/S2).", file=sys.stderr)
    if os.environ.get("GEMINI_KEY_FALLBACK"):
        fk = os.environ.get("GEMINI_KEY_FALLBACK", "").strip()
        if fk:
            os.environ["GEMINI_API_KEY"] = fk
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("gemini_provider: GEMINI_API_KEY not set", file=sys.stderr)
        return 2
    grounding = os.environ.get("GEMINI_GROUNDING", "1") == "1" and any(k in prompt.lower() for k in WORLD_KEYWORDS)
    last_error = None
    for model in candidate_models():
        for attempt in range(len(BACKOFF_S) + 1):
            try:
                answer = call_gemini(model, prompt, api_key, grounding)
                from citation_patch import clean as _clean
                answer, _hits = _clean(answer)
                if _hits:
                    print(f"gemini_provider: citation_patch v2 removed {_hits}", file=sys.stderr)
                print(f"gemini_provider: answered with {model}", file=sys.stderr)
                sys.stdout.write(answer + "\n")
                return 0
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")[:300]
                last_error = f"{model} HTTP {e.code}: {detail}"
                if e.code in (429, 503) and attempt < len(BACKOFF_S):
                    wait = BACKOFF_S[attempt]
                    print(f"gemini_provider: {last_error} - retry in {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                if e.code == 400 and grounding:
                    print("gemini_provider: grounding rejected, retrying without tools", file=sys.stderr)
                    grounding = False
                    continue
                print(f"gemini_provider: {last_error}", file=sys.stderr)
                break
            except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
                last_error = f"{model}: {e}"
                print(f"gemini_provider: {last_error}", file=sys.stderr)
                break
    print(f"gemini_provider: all models failed; last error: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
