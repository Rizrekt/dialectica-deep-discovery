#!/usr/bin/env python3
"""Tests for the R1 writer fallback chain (2026-11-17).

Proves, WITHOUT any network or real model call (all generators are
injected stubs):

- vyce_provider.candidate_models: deepseek-v4.1 is GONE from the
  default chain; VYCE_MODEL still leads; VYCE_MODEL_CHAIN pins the
  exact chain (the fallback rung's mechanism).
- WriterFallback: a totally-failing Vyce primary hands the SAME
  prompt to the fallback and the draft flows on; a succeeding
  primary never touches the fallback; after a switch, the next
  call (the gate's regeneration) stays on the surviving lane; a
  switch is logged with the "fallback: <lane> gagal -> <lane>"
  line; when every lane fails, the last error propagates.
- vyce_pipeline integration: failing primary + mock fallback ->
  the fallback's clean draft passes the real serve gate
  (sendable); DIALECTICA_WRITER_FALLBACK=0 -> the primary's
  failure propagates unwrapped (pre-R1 behaviour).

Run: python3 test_writer_fallback.py (exit 0 = all pass).
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import test_cloudflare_serve as tcs  # noqa: E402  (fixtures only)
import vyce_provider  # noqa: E402
import vyce_serve_common as vsc  # noqa: E402

CHECKS = [0]
FAILURES = []


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append(name)
        print(f"FAIL: {name} {detail}")


class Env:
    """Temporarily set/unset env vars (None = unset)."""

    def __init__(self, **kw):
        self.kw = kw
        self.saved = {}

    def __enter__(self):
        for k, v in self.kw.items():
            self.saved[k] = os.environ.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        return self

    def __exit__(self, *a):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def failing_gen(calls, msg="simulasi GLM gagal total"):
    def _gen(prompt, isr_id=None):
        calls.append(("primary", prompt))
        raise vsc.VyceGenerationError(msg)
    return _gen


def ok_gen(calls, label, text):
    def _gen(prompt, isr_id=None):
        calls.append((label, prompt))
        return text
    return _gen


def candidate_model_cases():
    with Env(VYCE_MODEL=None, VYCE_MODEL_CHAIN=None):
        chain = vyce_provider.candidate_models()
    check("candidate_models: default chain = [glm-5.3-flash], "
          "deepseek-v4.1 gone", chain == ["glm-5.3-flash"],
          f"chain={chain}")
    with Env(VYCE_MODEL="gpt-oss-120b", VYCE_MODEL_CHAIN=None):
        chain = vyce_provider.candidate_models()
    check("candidate_models: VYCE_MODEL leads, GLM follows, no "
          "deepseek", chain == ["gpt-oss-120b", "glm-5.3-flash"],
          f"chain={chain}")
    with Env(VYCE_MODEL=None, VYCE_MODEL_CHAIN="gpt-oss-120b"):
        chain = vyce_provider.candidate_models()
    check("candidate_models: VYCE_MODEL_CHAIN pins the exact chain",
          chain == ["gpt-oss-120b"], f"chain={chain}")
    with Env(VYCE_MODEL="diabaikan", VYCE_MODEL_CHAIN="a, b"):
        chain = vyce_provider.candidate_models()
    check("candidate_models: VYCE_MODEL_CHAIN wins over VYCE_MODEL",
          chain == ["a", "b"], f"chain={chain}")


def chain_cases():
    good = tcs.good_text()

    # Primary succeeds -> fallback never called, no log line.
    calls = []
    chain = vsc.WriterFallback(
        ok_gen(calls, "primary", good),
        [("cloudflare gpt-oss", ok_gen(calls, "fb", "CADANGAN"))])
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        out = chain("prompt-1", "isr-x")
    check("chain: primary OK -> its text, fallback untouched, no "
          "fallback log", out == good
          and [c[0] for c in calls] == ["primary"]
          and "fallback:" not in err.getvalue(),
          f"calls={calls} err={err.getvalue()[:80]}")

    # Primary fails totally -> fallback gets the SAME prompt; the
    # switch is logged; the next call stays on the fallback.
    calls = []
    chain = vsc.WriterFallback(
        failing_gen(calls),
        [("cloudflare gpt-oss", ok_gen(calls, "fb", good))])
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        out = chain("prompt-2", "isr-x")
        out2 = chain("prompt-2-regen", "isr-x")
    check("chain: primary gagal -> fallback, prompt sama, log "
          "'fallback: vyce gagal'", out == good and out2 == good
          and [c[0] for c in calls] == ["primary", "fb", "fb"]
          and calls[1][1] == "prompt-2"
          and "fallback: vyce gagal → cloudflare gpt-oss"
          in err.getvalue(),
          f"calls={[c[0] for c in calls]} err={err.getvalue()[:120]}")

    # Two rungs: rung 1 also fails -> rung 2 answers; both switches
    # logged in order.
    calls = []

    def failing_fb(prompt, isr_id=None):
        calls.append(("fb1", prompt))
        raise RuntimeError("gpt-oss vyce 403 pura-pura")

    chain = vsc.WriterFallback(
        failing_gen(calls),
        [("vyce gpt-oss-120b", failing_fb),
         ("cloudflare gpt-oss", ok_gen(calls, "fb2", good))])
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        out = chain("prompt-3", None)
    log = err.getvalue()
    check("chain: dua jatuhan berurutan, log berurutan",
          out == good
          and "fallback: vyce gagal → vyce gpt-oss-120b" in log
          and "fallback: vyce gpt-oss-120b gagal → cloudflare gpt-oss"
          in log, f"log={log[:200]}")

    # Every lane fails -> the LAST error propagates.
    chain = vsc.WriterFallback(
        failing_gen([]),
        [("cloudflare gpt-oss", failing_fb)])
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            chain("prompt-4", None)
        raised = None
    except Exception as ex:  # noqa: BLE001
        raised = ex
    check("chain: semua lane gagal -> error terakhir naik",
          isinstance(raised, RuntimeError)
          and "403 pura-pura" in str(raised), f"raised={raised}")


def pipeline_cases():
    good = tcs.good_text()
    prompt = "Pertanyaan uji: mekanisme apa yang menentukan?"

    # Failing primary + mock fallback -> fallback draft passes the
    # real serve gate.
    calls = []
    with Env(DIALECTICA_WRITER_FALLBACK=None,
             DIALECTICA_SEMANTIC_CHECK=None):
        result = vsc.vyce_pipeline(
            prompt, "isr-uji",
            generate_fn=failing_gen(calls),
            fallback_fns=[("cloudflare gpt-oss",
                           ok_gen(calls, "fb", good))])
    check("pipeline: primary gagal -> draf fallback lolos gerbang "
          "serve (sendable)", result["sendable"]
          and result["text"] == good
          and [c[0] for c in calls] == ["primary", "fb"],
          f"status={result['status']} calls={[c[0] for c in calls]}")

    # Fallback disabled -> primary failure propagates (pre-R1).
    calls = []
    raised = None
    with Env(DIALECTICA_WRITER_FALLBACK="0",
             DIALECTICA_SEMANTIC_CHECK=None):
        try:
            vsc.vyce_pipeline(
                prompt, "isr-uji",
                generate_fn=failing_gen(calls),
                fallback_fns=[("cloudflare gpt-oss",
                               ok_gen(calls, "fb", good))])
        except Exception as ex:  # noqa: BLE001
            raised = ex
    check("pipeline: DIALECTICA_WRITER_FALLBACK=0 -> kegagalan "
          "primary naik, fallback tidak tersentuh",
          isinstance(raised, vsc.VyceGenerationError)
          and [c[0] for c in calls] == ["primary"],
          f"raised={raised} calls={[c[0] for c in calls]}")

    # Default rung labels/order are the proven chain.
    labels = [lbl for lbl, _ in vsc.default_writer_fallbacks()]
    check("default_writer_fallbacks: [vyce gpt-oss-120b, "
          "cloudflare gpt-oss]",
          labels == ["vyce gpt-oss-120b", "cloudflare gpt-oss"],
          f"labels={labels}")


if __name__ == "__main__":
    candidate_model_cases()
    chain_cases()
    pipeline_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
