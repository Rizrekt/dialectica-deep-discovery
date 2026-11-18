#!/usr/bin/env python3
"""Driver babak 2: 3 panggilan penulis qwen-3.8-max via CrowLLM dengan
prompt WAJIB-APPARATUS, serial, jeda >=13 dtk antar panggilan.
Retry maks 2 hanya untuk 503/524 (jeda 20 dtk). Simpan JSON mentah
per percobaan + teks jawaban + log panggilan."""
import json, pathlib, subprocess, time

HERE = pathlib.Path(__file__).parent
CLIENT = ["python3", str(pathlib.Path.home() /
          "workspace/custom-connectors/custom.crowllm/bin/client.py")]
MODEL = "qwen-3.8-max:free"
ITEMS = [(1, "2777178d"), (2, "d94d7e34"), (3, "635a010d")]
PACE_S = 14
RETRYABLE = (503, 524)

def call(prompt_file):
    cmd = CLIENT + ["chat", "--model", MODEL, "--prompt-file",
                    str(prompt_file), "--max-tokens", "4000"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    raw = p.stdout or ""
    try:
        return json.loads(raw[raw.find("{"):])
    except Exception:
        return {"status": None, "raw_tail": raw[-500:],
                "stderr": p.stderr[-500:]}

def main():
    log = []
    for n, tag in ITEMS:
        pf = HERE / f"q{n}-{tag}-prompt-qwen2.txt"
        attempts = []
        answer = None
        for attempt in range(3):  # 1 + maks 2 retry
            if attempt:
                time.sleep(20)
            t0 = time.time()
            res = call(pf)
            dt = round(time.time() - t0, 1)
            status = res.get("status")
            attempts.append({"attempt": attempt + 1, "status": status,
                             "latency_s": dt,
                             "finish": res.get("finish_reason")})
            (HERE / f"q{n}-{tag}-qwen2-raw-{attempt+1}.json").write_text(
                json.dumps(res, ensure_ascii=False, indent=1))
            text = res.get("text") or res.get("answer") or ""
            if status == 200 and isinstance(text, str) and len(text) > 500:
                answer = text
                break
            if status not in RETRYABLE:
                break
        if answer:
            (HERE / f"q{n}-{tag}-jawaban-qwen2.txt").write_text(answer)
        log.append({"q": n, "tag": tag, "attempts": attempts,
                    "answer_chars": len(answer) if answer else 0})
        print(json.dumps(log[-1]), flush=True)
        if n != ITEMS[-1][0]:
            time.sleep(PACE_S)
    (HERE / "qwen2-calls-log.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
