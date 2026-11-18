#!/usr/bin/env python3
"""Uji silang 3 draf pertanyaan Jalur 3 oleh lane model lain (F-31D).

Dua lane per draf, materi publik-by-design saja (teks draf — memang akan
diterbitkan di platform):
  * PENANTANG (gpt-oss-120b via Cloudflare; cadangan qwen-3.8-max via
    CrowLLM bila anggaran neuron CF tidak cukup): mencoba MEMATAHKAN
    draf — menuduh duplikat, menyerang premis faktual, mencari cacat.
  * PEMERIKSA (Nemotron via CrowLLM): menilai kelayakan draf terhadap
    questionRules general LIVE (Q_CLARITY/Q_GOOD_FAITH/Q_NON_TRIVIAL/
    Q_PROHIBITED), butir per butir, keluaran JSON.

Pacing: >=13 detik antar awal panggilan CrowLLM (plafon 5 req/menit
akun relay BERSAMA semua proyek). Panggilan konsultasi frontier BUKAN
bagian skrip ini — itu jalur sesi utama.

Hasil mentah -> belajar-2026-11-18/peta-ask/crosstest-2026-11-18.json
"""
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.expanduser("~/workspace/research/dialectica")
DRAFTS = json.load(open(f"{BASE}/belajar-2026-11-18/peta-ask/drafts.json"))
OUT = f"{BASE}/belajar-2026-11-18/peta-ask/crosstest-2026-11-18.json"
CROW_CLIENT = os.path.expanduser(
    "~/workspace/custom-connectors/custom.crowllm/bin/client.py")
NEMOTRON = "nvidia/nemotron-3.5-super-vl-120b-a12b:free"
QWEN = "qwen-3.8-max:free"
PACE_S = 13.0
_last = [0.0]

CHALLENGER_PROMPT = """You are a hostile reviewer for a public knowledge-arena platform. Your job is to BREAK the draft question below — if it survives you, it is strong.

DRAFT QUESTION:
\"\"\"{q}\"\"\"

Attack it on every front:
1. DUPLICATE: is this substantially the same question as one a knowledge platform would already have on this topic? Name the existing question it would duplicate, or state clearly that you cannot name one.
2. FALSE PREMISE: does it state or assume any factual claim about the world that is wrong or unverifiable?
3. RULE DEFECTS: ambiguity (more than one reading), bundled unrelated sub-questions, triviality (answerable by one lookup), or manipulation/bait character.
4. ANSWERABILITY: could a knowledgeable expert tell when it has been fully answered?

Reply in exactly this shape:
VERDICT: BREAK or SURVIVES
REASONS: <your strongest attacks, numbered; if SURVIVES, say what you tried and why it failed>"""

CHECKER_PROMPT = """You are checking a draft question for a public knowledge arena against the arena's four question rules.

DRAFT QUESTION:
\"\"\"{q}\"\"\"

Rules:
- Q_CLARITY: clearly stated and answerable by a knowledgeable agent; any claim stated as fact about the world must be one a public source confirms, or framed as hypothetical; bundled unrelated sub-questions fail.
- Q_GOOD_FAITH: seeks genuine knowledge or understanding; not manipulation, harassment, bait, or an attempt to make agents reveal their own environment.
- Q_NON_TRIVIAL: the answer requires reasoning or synthesis beyond a single lookup; a 'why' question requiring causal reasoning passes.
- Q_PROHIBITED: contains no prohibited content (child sexual abuse material, obscenity, sex trafficking content).

Reply with ONLY a JSON object in exactly this shape, and no other text:
{{"Q_CLARITY": "pass" or "fail", "Q_GOOD_FAITH": "pass" or "fail", "Q_NON_TRIVIAL": "pass" or "fail", "Q_PROHIBITED": "pass" or "fail", "overall": "pass" or "fail", "notes": "one short sentence per rule that fails, or empty"}}"""


def crowllm(model, prompt):
    wait = PACE_S - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write(prompt)
        path = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, CROW_CLIENT, "chat", "--model", model,
             "--prompt-file", path, "--max-tokens", "2500"],
            capture_output=True, text=True, timeout=600)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        return {"error": f"rc={proc.returncode}: {proc.stderr.strip()[:200]}"}
    try:
        res = json.loads(proc.stdout)
        return {"text": res.get("text") or res.get("body") or proc.stdout}
    except Exception:
        return {"text": proc.stdout}


def main():
    results = []
    # Pilih lane penantang: gpt-oss Cloudflare bila anggaran neuron cukup.
    challenger = "gpt-oss-cloudflare"
    try:
        import cloudflare_provider as cf
        spent = cf.neurons_spent_today_utc()
        print(f"neuron CF terpakai hari ini: {spent}")
        if spent > 7000:
            challenger = "qwen-crowllm"
            print("anggaran CF ketat -> penantang diganti qwen (CrowLLM)")
    except Exception as e:
        challenger = "qwen-crowllm"
        print(f"CF tidak terbaca ({e}) -> penantang qwen (CrowLLM)")

    for d in DRAFTS:
        q = d["draft"]
        print(f"\n===== SLOT {d['slot']}: {d['topic']}")
        if challenger == "gpt-oss-cloudflare":
            import cloudflare_provider as cf
            try:
                gen = cf.generate(CHALLENGER_PROMPT.format(q=q),
                                  lane="ask-crosstest")
                chal = {"text": gen["text"], "neurons": gen["usage"]}
            except Exception as e:
                chal = {"error": str(e)[:300]}
        else:
            chal = crowllm(QWEN, CHALLENGER_PROMPT.format(q=q))
        print("PENANTANG:", str(chal.get("text") or chal.get("error"))[:400])
        chk = crowllm(NEMOTRON, CHECKER_PROMPT.format(q=q))
        print("PEMERIKSA:", str(chk.get("text") or chk.get("error"))[:400])
        results.append({"slot": d["slot"], "topic": d["topic"],
                        "draft": q, "challenger_lane": challenger,
                        "challenger": chal, "checker_lane": "nemotron-crowllm",
                        "checker": chk})
        json.dump(results, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\nTersimpan -> {OUT}")


if __name__ == "__main__":
    main()
