#!/usr/bin/env python3
"""Smoke tests for the Cloudflare/gpt-oss claim path (MEKANISME §37).

Proves, WITHOUT any real claim:
- the provider emits the wrapped text on stdout ONLY when the wrapper
  verdict is sendable (exit 0); a short draft (GAGAL-LANJUT), a draft
  with an unpatchable audit finding, and an exhausted neuron budget all
  exit 1 with EMPTY stdout — the state trued treats as "nothing
  submitted";
- run_serve wires --cloudflare to cloudflare_provider.py in --dry-run
  (nothing launched, no credential fetched);
- run_serve refuses serve mode on this lane with exit 5, dry-run
  included (identical fence to the OpenRouter lane, §35).

Generation is stubbed in-process; run_serve is only ever run with
--dry-run or into the serve refusal. NO `trued answer`, NO serve, NO
claim. Run: python3 test_cloudflare_claim_path.py (exit 0 = all pass).
"""
import contextlib
import io
import os
import subprocess
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_provider as cp  # noqa: E402

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
        return {"text": text, "usage": {"neurons": 130.0},
                "latency_s": 0.0,
                "neurons_before": 0.0, "neurons_after": 130.0}
    return _gen


def run_provider_main(prompt="Pertanyaan uji asap: bandingkan dua pola "
                             "penyebaran kontrak untuk armada vault."):
    out_buf, err_buf = io.StringIO(), io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(prompt)
    try:
        with contextlib.redirect_stdout(out_buf), \
                contextlib.redirect_stderr(err_buf):
            rc = cp.main()
    finally:
        sys.stdin = old_stdin
    return rc, out_buf.getvalue(), err_buf.getvalue()


def provider_cases():
    os.environ.pop("DIALECTICA_ISR_ID", None)
    good = good_text()
    check("fixture good_text in rubric band", 4500 <= len(good) <= 8000,
          f"{len(good)} chars")

    with mock.patch.object(cp, "generate", fake_generate(good)):
        rc, out, _ = run_provider_main()
    check("sendable draft -> exit 0 + wrapped text on stdout",
          rc == 0 and len(out) >= 4500 and "## 1." in out,
          f"rc={rc} stdout={len(out)} chars")

    with mock.patch.object(cp, "generate", fake_generate("Jawaban "
                                                          "singkat.")):
        rc, out, _ = run_provider_main()
    check("short draft (GAGAL-LANJUT) -> exit 1 + empty stdout",
          rc == 1 and out == "", f"rc={rc} stdout={len(out)} chars")

    bad = good.replace("## 4.", "EIP-3860 adds a surcharge to every "
                                 "DELEGATECALL.\n\n## 4.", 1)
    with mock.patch.object(cp, "generate", fake_generate(bad)):
        rc, out, err = run_provider_main()
    check("unpatchable audit finding -> exit 1 + empty stdout + WITHHELD",
          rc == 1 and out == "" and "WITHHELD" in err,
          f"rc={rc} stdout={len(out)} chars")

    def no_client(*a, **k):
        raise AssertionError("connector client invoked despite neuron "
                             "budget gate")
    with mock.patch.object(cp, "neurons_spent_today_utc",
                           lambda: 9500.0), \
            mock.patch.object(cp.subprocess, "run", no_client):
        rc, out, _ = run_provider_main()
    check("neuron budget >9000 -> exit 1 + empty stdout + client "
          "never invoked",
          rc == 1 and out == "", f"rc={rc} stdout={len(out)} chars")


def runserve(args):
    proc = subprocess.run([sys.executable, RUN_SERVE] + args,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout + proc.stderr


def runserve_cases():
    rc, out = runserve(["--cloudflare", "--dry-run", "--answer", ISR])
    check("run_serve --cloudflare --dry-run --answer: wiring shown, "
          "nothing launched",
          rc == 0 and "cloudflare_provider.py" in out
          and "DRY-RUN" in out and ISR in out
          and "launching trued" not in out, f"rc={rc}")

    rc, out = runserve(["--cloudflare"])
    check("run_serve --cloudflare (serve) refused with exit 5",
          rc == 5 and "answer-only" in out
          and "launching" not in out, f"rc={rc}")

    rc, out = runserve(["--cloudflare", "--dry-run"])
    check("serve refusal precedes dry-run on this lane",
          rc == 5 and "answer-only" in out, f"rc={rc}")


if __name__ == "__main__":
    provider_cases()
    runserve_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
