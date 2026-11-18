#!/usr/bin/env python3
"""Watcher uji 1 tembakan: bunuh unit serve begitu counter generasi
hari ini mencapai 10 (generasi ke-11 = pelanggaran izin). Poll 3 dtk.
Berhenti sendiri bila unit sudah tidak aktif DAN counter sudah 10,
atau sesudah batas keras 100 menit."""
import subprocess
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/research/dialectica/provider")
import vyce_serve_common as c  # noqa: E402

MARKER = "/home/hatch/workspace/research/dialectica/belajar-2026-11-18/doktrin-a/watcher-uji1.log"
START = time.time()
HARD_LIMIT_S = 100 * 60


def log(msg):
    with open(MARKER, "a") as f:
        f.write("%.1f %s\n" % (time.time(), msg))


def unit_active():
    r = subprocess.run(["systemctl", "is-active", "dialectica-serve"],
                       capture_output=True, text=True)
    return r.stdout.strip() == "active"


log("watcher start; counter=%s" % c.serve_generations_today())
while True:
    try:
        n = c.serve_generations_today()
    except Exception as e:  # noqa: BLE001
        log("counter read error: %r" % (e,))
        n = None
    if n is not None and n >= 10:
        log("counter reached %s -> STOP unit" % n)
        subprocess.run(["sudo", "-n", "systemctl", "stop", "dialectica-serve"],
                       capture_output=True, text=True)
        log("stop issued; active=%s" % unit_active())
        break
    if time.time() - START > HARD_LIMIT_S:
        log("hard limit reached; counter=%s active=%s" % (n, unit_active()))
        if unit_active():
            subprocess.run(["sudo", "-n", "systemctl", "stop",
                            "dialectica-serve"], capture_output=True, text=True)
            log("hard-limit stop issued")
        break
    time.sleep(3)
log("watcher exit")
