#!/usr/bin/env python3
"""Smoke tests for the Z.ai claim path (MEKANISME §40).

Proves, WITHOUT any real claim:
- the provider emits the wrapped text on stdout ONLY when the wrapper
  verdict is sendable (exit 0); a short draft (GAGAL-LANJUT) and a
  draft with an unpatchable audit finding exit 1 with EMPTY stdout —
  the state trued treats as "nothing submitted";
- generate() calls the connector client with the pinned model
  glm-4.7-flash and thinking DISABLED (verdict condition 1);
- a 1305 (free-pool overload) is retried EXACTLY ONCE after the
  configured wait (condition 2): 1305->200 succeeds and is flagged
  retried_after_1305, 1305->1305 raises GenerationError after two
  attempts, and a non-1305 failure is NOT retried (one attempt);
- usage is logged under lane `zai-glm47flash`;
- run_serve wires --zai to zai_provider.py in --dry-run (nothing
  launched, no credential fetched);
- run_serve refuses serve mode on this lane with exit 5;
- the gemini wiring is unchanged.

The connector client is stubbed in-process (the 60 s retry wait is
patched out); run_serve is only ever run with --dry-run or into the
serve refusal. NO `trued answer`, NO serve, NO claim.
Run: python3 test_zai_claim_path.py (exit 0 = all pass).
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import zai_provider as zp  # noqa: E402

RUN_SERVE = os.path.join(HERE, "run_serve.py")
ISR = "60fa9935-4352-4a4c-9aa7-384de037196c"
FAILURES = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        FAILURES.append(name)


FILLER = ("Setiap instance membawa alamat logika yang sama sehingga "
          "pemeriksaan cukup dilakukan sekali untuk seluruh armada, "
          "sedangkan biaya marjinal per instance hanya menanggung "
          "penyimpanan alamat dan inisialisasi yang tipis. ")

# Bukti terikat sitasi (§45): draf "baik" wajib memuat URL + angka
# terikat — tanpa ini lantai mekanik wrapper menahannya, persis
# seperti draf nyata sejak gerbang K-1/K-2 hidup.
EVIDENCE = ("Acuan terukur seksi ini: akses dingin 2.600 gas, akses "
            "hangat 100 gas, dan batas initcode 49.152 byte — lihat "
            "https://eips.ethereum.org/EIPS/eip-2929 dan "
            "https://eips.ethereum.org/EIPS/eip-3860.")


def good_text():
    opening = ("Klaim inti: untuk armada vault yang identik, klon "
               "minimal-proxy menang pada biaya penyebaran, dan jawaban "
               "berbalik hanya bila logika harus dapat diganti per "
               "instance. Distingsinya bukan harga bytecode, melainkan "
               "siapa yang memegang kendali atas perubahan logika.")
    titles = ["Biaya penyebaran", "Biaya pemakaian harian",
              "Kemampuan mengganti logika", "Permukaan audit",
              "Mode kegagalan", "Kapan jawaban berbalik"]
    bodies = []
    for i, t in enumerate(titles, 1):
        bodies.append(f"## {i}. {t}\n**Tesis seksi {i}.** Mekanisme "
                      f"pada seksi ini menentukan angka akhirnya.\n\n"
                      + FILLER * 3 + EVIDENCE)
    closing = ("Yang baru dari jawaban ini: titik baliknya bukan skala "
               "armada, melainkan kebutuhan mengganti logika per "
               "instance — kebaruan yang belum dibahas dalam jawaban "
               "yang sudah ada.")
    text = "\n\n".join([opening] + bodies + [closing])
    while len(text) < 6200:
        bodies[2] += FILLER
        text = "\n\n".join([opening] + bodies + [closing])
    return text


def fake_generate(text):
    def _gen(prompt, isr_id=None):
        return {"text": text, "usage": None, "latency_s": 0.0,
                "finish_reason": "stop", "reasoning_chars": 0,
                "retried_after_1305": False, "attempts": [200]}
    return _gen


def run_provider_main(prompt="Pertanyaan uji asap: bandingkan dua pola "
                             "penyebaran kontrak untuk armada vault."):
    out_buf, err_buf = io.StringIO(), io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(prompt)
    try:
        with contextlib.redirect_stdout(out_buf), \
                contextlib.redirect_stderr(err_buf):
            rc = zp.main()
    finally:
        sys.stdin = old_stdin
    return rc, out_buf.getvalue(), err_buf.getvalue()


def provider_cases():
    os.environ.pop("DIALECTICA_ISR_ID", None)
    good = good_text()
    check("fixture good_text in rubric band", 4500 <= len(good) <= 8000,
          f"{len(good)} chars")

    with mock.patch.object(zp, "generate", fake_generate(good)):
        rc, out, _ = run_provider_main()
    check("sendable draft -> exit 0 + wrapped text on stdout",
          rc == 0 and len(out) >= 4500 and "## 1." in out,
          f"rc={rc} stdout={len(out)} chars")

    with mock.patch.object(zp, "generate", fake_generate("Jawaban "
                                                          "singkat.")):
        rc, out, _ = run_provider_main()
    check("short draft (GAGAL-LANJUT) -> exit 1 + empty stdout",
          rc == 1 and out == "", f"rc={rc} stdout={len(out)} chars")

    bad = good.replace("## 4.", "EIP-3860 adds a surcharge to every "
                                 "DELEGATECALL.\n\n## 4.", 1)
    with mock.patch.object(zp, "generate", fake_generate(bad)):
        rc, out, err = run_provider_main()
    check("unpatchable audit finding -> exit 1 + empty stdout + WITHHELD",
          rc == 1 and out == "" and "WITHHELD" in err,
          f"rc={rc} stdout={len(out)} chars")


def completed(rc, payload):
    return subprocess.CompletedProcess(
        args=[], returncode=rc, stdout=json.dumps(payload), stderr="")


OK_200 = {"status": 200, "text": "isi jawaban uji",
          "usage": {"prompt_tokens": 10, "completion_tokens": 20,
                    "total_tokens": 30},
          "latency_s": 1.0, "finish_reason": "stop",
          "reasoning_chars": 0}
ERR_1305 = {"status": 429, "body": {"error": {
    "code": "1305",
    "message": "The service may be temporarily overloaded"}}}
ERR_500 = {"status": 500, "body": {"error": {
    "code": "500", "message": "internal error"}}}


def sequenced(results):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        payload = results[len(calls) - 1]
        return completed(0 if payload["status"] == 200 else 1, payload)

    return calls, fake_run


def generate_cases():
    # 1305 -> wait -> 200: succeeds, flagged, thinking disabled on wire.
    calls, fake_run = sequenced([ERR_1305, OK_200])
    sleeps = []
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "usage.jsonl")
        with mock.patch.object(zp, "USAGE_LOG", log), \
                mock.patch.object(zp.subprocess, "run", fake_run), \
                mock.patch.object(zp.time, "sleep", sleeps.append):
            gen = zp.generate("prompt uji")
        with open(log, encoding="utf-8") as fh:
            rec = json.loads(fh.read().strip())
    argv = calls[0]
    check("1305 -> exactly one retry after the wait -> success",
          len(calls) == 2 and sleeps == [zp.RETRY_1305_WAIT_S]
          and gen["retried_after_1305"] is True
          and gen["attempts"] == [429, 200],
          f"calls={len(calls)} sleeps={sleeps} attempts={gen['attempts']}")
    check("client wire: pinned model + thinking disabled",
          argv[argv.index("--model") + 1] == "glm-4.7-flash"
          and argv[argv.index("--thinking") + 1] == "disabled"
          and argv[argv.index("--max-tokens") + 1] == "8000",
          f"argv={argv}")
    check("usage logged under lane zai-glm47flash with retry flag",
          rec["lane"] == "zai-glm47flash"
          and rec["model"] == "glm-4.7-flash"
          and rec["retried_after_1305"] is True
          and rec["usage"]["total_tokens"] == 30,
          f"rec={rec.get('lane')} retried={rec['retried_after_1305']}")

    # 1305 -> 1305: lane gives up after exactly two attempts.
    calls, fake_run = sequenced([ERR_1305, ERR_1305])
    raised = False
    with mock.patch.object(zp.subprocess, "run", fake_run), \
            mock.patch.object(zp.time, "sleep", lambda s: None):
        try:
            zp.generate("prompt uji")
        except zp.GenerationError:
            raised = True
    check("1305 -> 1305 -> GenerationError (no third attempt)",
          raised and len(calls) == 2, f"calls={len(calls)}")

    # Non-1305 failure: NOT retried.
    calls, fake_run = sequenced([ERR_500])
    raised = False
    with mock.patch.object(zp.subprocess, "run", fake_run), \
            mock.patch.object(zp.time, "sleep", lambda s: None):
        try:
            zp.generate("prompt uji")
        except zp.GenerationError:
            raised = True
    check("non-1305 failure -> GenerationError, single attempt",
          raised and len(calls) == 1, f"calls={len(calls)}")


def runserve(args):
    proc = subprocess.run([sys.executable, RUN_SERVE] + args,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout + proc.stderr


def runserve_cases():
    rc, out = runserve(["--zai", "--dry-run", "--answer", ISR])
    check("run_serve --zai --dry-run --answer: wiring shown, "
          "nothing launched",
          rc == 0 and "zai_provider.py" in out
          and "DRY-RUN" in out and ISR in out
          and "launching trued" not in out, f"rc={rc}")

    rc, out = runserve(["--zai"])
    check("run_serve --zai (serve) refused with exit 5",
          rc == 5 and "answer-only" in out
          and "launching" not in out, f"rc={rc}")

    rc, out = runserve(["--zai", "--dry-run"])
    check("serve refusal precedes dry-run on this lane",
          rc == 5 and "answer-only" in out, f"rc={rc}")

    rc, out = runserve(["--gemini", "--dry-run", "--answer", ISR])
    check("run_serve --gemini dry-run wiring unchanged",
          rc == 0 and "gemini_provider.py" in out
          and "launching trued" not in out, f"rc={rc}")


if __name__ == "__main__":
    provider_cases()
    generate_cases()
    runserve_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
