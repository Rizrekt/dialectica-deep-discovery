#!/usr/bin/env python3
"""Smoke tests for the temporary Cloudflare SERVE lane (MEKANISME §39).

Proves, WITHOUT taking any real job:
- the Class-2 screen (prepare gate) passes viso-0 core-topic rows and
  passes over everything else BEFORE any generation;
- the 10/day serve generation cap is enforced in the prepare gate
  (pass-over, no claim, no provider failure after a job exists), with
  the final pipeline running regeneration-disabled so the count can
  never exceed the cap;
- prepared answers are cached; the READY hook vetoes unprepared bids
  AND bids whose cache file is empty/whitespace-only (fix B);
- the job-time provider serves the cache, and only corrections /
  unprepared arrivals fall back to the live pipeline — which is
  serve-cap gated: a remainder that cannot cover a full pipeline
  (1 generation + at most 1 regen) exits 1 with zero generations,
  while the cache-hit path stays ungated (fix A);
- run_serve: plain --cloudflare serve is STILL refused (exit 5),
  --cloudflare-serve takes no --answer (exit 5), --dry-run shows the
  supervised plan, and a reached cap refuses the start (exit 6);
- the supervisor SIGINTs a child when the cap is reached and returns
  a child's own exit untouched otherwise.

Generation is stubbed in-process; run_serve is only ever run with
--dry-run or into a refusal. NO real serve is launched here — the
live never-match smoke is a separate, supervised step (§39).
Run: python3 test_cloudflare_serve.py (exit 0 = all pass).
"""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cloudflare_provider as cp  # noqa: E402
import cloudflare_serve_common as csc  # noqa: E402
import cloudflare_serve_prepare as prep  # noqa: E402
import cloudflare_serve_provider as serve_provider  # noqa: E402

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


def serve_record():
    return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "lane": "cloudflare-serve", "model": cp.MODEL,
            "isr": None, "usage": {"neurons": 130.0},
            "answer_chars": 6200, "neurons_today_after": None}


class ServeWorld:
    """Temp usage log + temp cache, wired into both counting paths."""

    def __init__(self, prefill_serve=0):
        self.tmp = tempfile.mkdtemp(prefix="cf-serve-test-")
        self.log = os.path.join(self.tmp, "token-usage.jsonl")
        self.cache = os.path.join(self.tmp, "cache")
        with open(self.log, "w", encoding="utf-8") as fh:
            for _ in range(prefill_serve):
                fh.write(json.dumps(serve_record()) + "\n")
        self._old = {k: os.environ.get(k) for k in
                     ("DIALECTICA_TOKEN_USAGE_LOG",
                      "DIALECTICA_SERVE_CACHE_DIR")}
        os.environ["DIALECTICA_TOKEN_USAGE_LOG"] = self.log
        os.environ["DIALECTICA_SERVE_CACHE_DIR"] = self.cache
        self._old_usage_log = cp.USAGE_LOG
        cp.USAGE_LOG = self.log

    def close(self):
        cp.USAGE_LOG = self._old_usage_log
        for key, val in self._old.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val


def fake_generate_factory(texts, world, calls):
    """cp.generate stand-in: serves `texts` in order (last repeats),
    logs a serve-lane usage record per call like the real one."""
    def _gen(prompt, isr_id=None, lane=None, budget_lanes=None):
        calls.append(prompt)
        text = texts[min(len(calls) - 1, len(texts) - 1)]
        with open(world.log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(serve_record()) + "\n")
        return {"text": text, "usage": {"neurons": 130.0},
                "latency_s": 0.0, "neurons_before": 0.0,
                "neurons_after": 130.0}
    return _gen


def exploding_generate(*a, **k):
    raise AssertionError("generation attempted behind a closed gate")


GOOD_ROW = {"id": ISR, "title": "Minimal proxy clones for a wallet "
            "vault fleet", "content": "When should a wallet platform "
            "deploy EIP-1167 clones per user wallet instead of one "
            "contract per wallet?", "questionVisoCount": 0,
            "questionMarathonActive": False, "arenaName": "general"}


def screen_cases():
    ok, _ = csc.screen_row(GOOD_ROW)
    check("screen: viso-0 core-topic row passes", ok)
    for name, row in (
            ("viso 3", {**GOOD_ROW, "questionVisoCount": 3}),
            ("marathon active", {**GOOD_ROW,
                                 "questionMarathonActive": True}),
            ("off-topic", {**GOOD_ROW, "title": "Best pasta sauce",
                           "content": "How do I cook pasta well?"}),
            ("runtime demanded", {**GOOD_ROW,
                                  "runtimeContext": {"image": "x"}}),
            ("no id", {"title": "wallet", "content": "wallet?"}),
            ("no text", {"id": ISR, "questionVisoCount": 0})):
        ok, reason = csc.screen_row(row)
        check(f"screen: {name} passed over", not ok, reason)


def prepare_cases():
    good = good_text()

    world = ServeWorld()
    try:
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, line = prep.prepare_row(GOOD_ROW)
        check("prepare: good row -> exit 0 + answer cached",
              rc == 0 and csc.read_cache(ISR) is not None
              and len(calls) == 1,
              f"rc={rc} calls={len(calls)} line={line[:60]}")
        check("prepare: generation recorded under serve lane",
              csc.serve_generations_today() == 1,
              f"count={csc.serve_generations_today()}")
    finally:
        world.close()

    world = ServeWorld()
    try:
        with mock.patch.object(cp, "generate", exploding_generate):
            rc, _ = prep.prepare_row({**GOOD_ROW,
                                      "questionVisoCount": 5})
        check("prepare: screened-out row -> exit 1, zero generations",
              rc == 1 and csc.serve_generations_today() == 0,
              f"rc={rc}")
    finally:
        world.close()

    world = ServeWorld(prefill_serve=10)
    try:
        with mock.patch.object(cp, "generate", exploding_generate):
            rc, line = prep.prepare_row(GOOD_ROW)
        check("prepare: cap reached (10) -> exit 1, zero generations, "
              "no job exists to abandon",
              rc == 1 and "cap serve" in line
              and csc.serve_generations_today() == 10, f"rc={rc}")
    finally:
        world.close()

    # 9 used: one generation left -> pipeline runs WITHOUT regen, so a
    # short draft ends GAGAL-LANJUT after exactly ONE generation and
    # the count lands exactly on the cap, never above it.
    world = ServeWorld(prefill_serve=9)
    try:
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory(["Jawaban "
                                                      "singkat."],
                                                     world, calls)):
            rc, _ = prep.prepare_row(GOOD_ROW)
        check("prepare: 9 used + short draft -> exit 1 after exactly "
              "1 generation (regen disabled at the cap edge)",
              rc == 1 and len(calls) == 1
              and csc.serve_generations_today() == 10,
              f"rc={rc} calls={len(calls)}")
    finally:
        world.close()

    # 8 used: regen allowed -> short then good = 2 generations, exit 0.
    world = ServeWorld(prefill_serve=8)
    try:
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory(["Jawaban "
                                                      "singkat.", good],
                                                     world, calls)):
            rc, _ = prep.prepare_row(GOOD_ROW)
        check("prepare: 8 used + regen -> exit 0, count lands on 10",
              rc == 0 and len(calls) == 2
              and csc.serve_generations_today() == 10,
              f"rc={rc} calls={len(calls)}")
    finally:
        world.close()


def ready_cases():
    world = ServeWorld()
    try:
        csc.write_cache(ISR, "jawaban siap")
        env = dict(os.environ)
        script = os.path.join(HERE, "cloudflare_serve_ready.py")
        hit = subprocess.run([sys.executable, script], input=json.dumps(
            {"opportunity": {"isrId": ISR}}), capture_output=True,
            text=True, env=env, timeout=30)
        miss = subprocess.run([sys.executable, script], input=json.dumps(
            {"opportunity": {"isrId": "00000000-0000-0000-0000-"
                            "000000000000"}}), capture_output=True,
            text=True, env=env, timeout=30)
        check("ready: prepared id -> exit 0", hit.returncode == 0,
              f"rc={hit.returncode}")
        check("ready: unprepared id -> exit 1 (bid vetoed)",
              miss.returncode == 1, f"rc={miss.returncode}")

        # Fix B: an empty / whitespace-only cache file is NOT a
        # prepared answer (read_cache semantics) — READY must veto,
        # even while a genuinely prepared id in the same cache dir
        # still passes.
        empty_id = "22222222-3333-4444-5555-666666666666"
        ws_id = "33333333-4444-5555-6666-777777777777"
        csc.write_cache(empty_id, "")
        csc.write_cache(ws_id, "   \n\t  ")
        for name, bad_id in (("empty", empty_id),
                             ("whitespace-only", ws_id)):
            bad = subprocess.run(
                [sys.executable, script],
                input=json.dumps({"opportunity": {"isrId": bad_id}}),
                capture_output=True, text=True, env=env, timeout=30)
            check(f"ready: {name} cache file -> exit 1 (bid vetoed)",
                  bad.returncode == 1, f"rc={bad.returncode}")
        hit2 = subprocess.run(
            [sys.executable, script],
            input=json.dumps({"opportunity": {"isrId": ISR}}),
            capture_output=True, text=True, env=env, timeout=30)
        check("ready: prepared id still exit 0 alongside empty files",
              hit2.returncode == 0, f"rc={hit2.returncode}")
    finally:
        world.close()


def run_provider_main(env_extra, prompt="Prompt pekerjaan uji."):
    out_buf, err_buf = io.StringIO(), io.StringIO()
    old_stdin, old_env = sys.stdin, dict(os.environ)
    sys.stdin = io.StringIO(prompt)
    os.environ.pop("DIALECTICA_ISR_ID", None)
    os.environ.pop("DIALECTICA_JOB_KIND", None)
    os.environ.update(env_extra)
    try:
        with contextlib.redirect_stdout(out_buf), \
                contextlib.redirect_stderr(err_buf):
            rc = serve_provider.main()
    finally:
        sys.stdin = old_stdin
        os.environ.clear()
        os.environ.update(old_env)
    return rc, out_buf.getvalue(), err_buf.getvalue()


def provider_cases():
    good = good_text()
    world = ServeWorld()
    try:
        csc.write_cache(ISR, "ISI CACHE SIAP")
        rc, out, _ = run_provider_main({"DIALECTICA_ISR_ID": ISR})
        check("provider: cache hit -> cached text, exit 0",
              rc == 0 and out.strip() == "ISI CACHE SIAP", f"rc={rc}")

        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": ISR,
                 "DIALECTICA_JOB_KIND": "correction"})
        check("provider: correction bypasses cache -> live pipeline",
              rc == 0 and "ISI CACHE" not in out and len(calls) == 1,
              f"rc={rc} calls={len(calls)}")

        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": "11111111-2222-3333-4444-"
                                      "555555555555"})
        check("provider: cache miss -> live fallback, exit 0",
              rc == 0 and len(out) >= 4500 and len(calls) == 1,
              f"rc={rc}")

        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory(["Jawaban "
                                                      "singkat."],
                                                     world, calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": "11111111-2222-3333-4444-"
                                      "555555555555"})
        check("provider: fallback withheld -> exit 1 + empty stdout",
              rc == 1 and out == "", f"rc={rc}")
    finally:
        world.close()

    # Fix A: the live fallback is serve-cap gated. A full pipeline
    # costs up to PIPELINE_MAX_GENERATIONS (1 + at most 1 regen);
    # when the day's remainder cannot cover that, the fallback must
    # exit 1 WITHOUT generating. The cache-hit path generates
    # nothing and must stay ungated even at a full cap.
    world = ServeWorld(prefill_serve=10)
    try:
        csc.write_cache(ISR, "ISI CACHE SIAP")
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main({"DIALECTICA_ISR_ID": ISR})
        check("provider: cache hit at FULL cap -> cached text, "
              "exit 0, zero generations (path ungated)",
              rc == 0 and out.strip() == "ISI CACHE SIAP"
              and len(calls) == 0, f"rc={rc} calls={len(calls)}")

        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": "11111111-2222-3333-4444-"
                                      "555555555555"})
        check("provider: cache miss at FULL cap -> exit 1 + empty "
              "stdout, zero generations, count stays 10",
              rc == 1 and out == "" and len(calls) == 0
              and csc.serve_generations_today() == 10,
              f"rc={rc} calls={len(calls)}")

        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": ISR,
                 "DIALECTICA_JOB_KIND": "correction"})
        check("provider: correction at FULL cap -> exit 1 + empty "
              "stdout, zero generations",
              rc == 1 and out == "" and len(calls) == 0
              and csc.serve_generations_today() == 10,
              f"rc={rc} calls={len(calls)}")
    finally:
        world.close()

    # 9 used: remainder 1 covers a bare generation but NOT the full
    # pipeline (1 + regen) -> still blocked, zero generations.
    world = ServeWorld(prefill_serve=9)
    try:
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": "11111111-2222-3333-4444-"
                                      "555555555555"})
        check("provider: cache miss with 1 remaining -> exit 1, "
              "zero generations, count stays 9",
              rc == 1 and out == "" and len(calls) == 0
              and csc.serve_generations_today() == 9,
              f"rc={rc} calls={len(calls)}")
    finally:
        world.close()

    # 8 used: remainder 2 covers the full pipeline -> fallback runs.
    world = ServeWorld(prefill_serve=8)
    try:
        calls = []
        with mock.patch.object(cp, "generate",
                               fake_generate_factory([good], world,
                                                     calls)):
            rc, out, _ = run_provider_main(
                {"DIALECTICA_ISR_ID": "11111111-2222-3333-4444-"
                                      "555555555555"})
        check("provider: cache miss with 2 remaining -> fallback "
              "runs, exit 0",
              rc == 0 and len(out) >= 4500 and len(calls) == 1,
              f"rc={rc} calls={len(calls)}")
    finally:
        world.close()


def runserve(args, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run([sys.executable, RUN_SERVE] + args,
                          capture_output=True, text=True, timeout=60,
                          env=env)
    return proc.returncode, proc.stdout + proc.stderr


def runserve_cases():
    world = ServeWorld()
    try:
        env = {"DIALECTICA_TOKEN_USAGE_LOG": world.log}
        rc, out = runserve(["--cloudflare-serve", "--dry-run",
                            "arenaIds=general",
                            'q="zxqwkj-never-match"'], env)
        check("run_serve --cloudflare-serve --dry-run: supervised "
              "plan shown, nothing launched",
              rc == 0 and "cloudflare_serve_prepare.py" in out
              and "cloudflare_serve_provider.py" in out
              and "DRY-RUN" in out and "launching" not in out,
              f"rc={rc}")
        rc, out = runserve(["--cloudflare"])
        check("run_serve --cloudflare (plain serve) STILL refused "
              "exit 5", rc == 5 and "answer-only" in out, f"rc={rc}")
        rc, out = runserve(["--cloudflare-serve", "--answer", ISR], env)
        check("run_serve --cloudflare-serve --answer refused exit 5",
              rc == 5 and "launching" not in out, f"rc={rc}")
    finally:
        world.close()

    world = ServeWorld(prefill_serve=10)
    try:
        env = {"DIALECTICA_TOKEN_USAGE_LOG": world.log}
        rc, out = runserve(["--cloudflare-serve", "arenaIds=general",
                            'q="wallet"'], env)
        check("run_serve --cloudflare-serve at cap -> start refused "
              "exit 6, nothing launched",
              rc == 6 and "REFUSED" in out and "launching" not in out,
              f"rc={rc}")
    finally:
        world.close()


def supervisor_cases():
    spec = importlib.util.spec_from_file_location("run_serve_mod",
                                                  RUN_SERVE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    proc = subprocess.Popen(["sleep", "30"])
    started = time.monotonic()
    rc = mod.supervise_serve(proc, lambda: 99, 10, poll_s=0.1,
                             drain_timeout_s=10)
    elapsed = time.monotonic() - started
    check("supervisor: cap reached -> child SIGINTed, fast return",
          rc == -2 and elapsed < 5 and proc.poll() is not None,
          f"rc={rc} elapsed={elapsed:.1f}s")

    proc = subprocess.Popen(["sleep", "0.3"])
    rc = mod.supervise_serve(proc, lambda: 0, 10, poll_s=0.1,
                             drain_timeout_s=10)
    check("supervisor: child exit passes through untouched",
          rc == 0, f"rc={rc}")


if __name__ == "__main__":
    screen_cases()
    prepare_cases()
    ready_cases()
    provider_cases()
    runserve_cases()
    supervisor_cases()
    print(f"\n{'ALL PASS' if not FAILURES else 'FAILURES: ' + str(FAILURES)}"
          f" ({CHECKS[0] - len(FAILURES)}/{CHECKS[0]})")
    sys.exit(1 if FAILURES else 0)
