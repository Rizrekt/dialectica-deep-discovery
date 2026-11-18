#!/usr/bin/env python3
"""Uji fixture ask_driver — offline penuh, nol jaringan, nol create nyata.

Menjalankan: python3 test_ask_driver.py  (exit 0 = semua lolos)
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ask_driver as ad  # noqa: E402

FAILED = []


def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {extra}" if extra and not cond else ""))
    if not cond:
        FAILED.append(name)


def step(phase, token=None, askfee=None, state_extra=None, **kw):
    st = {"phase": phase, "questionDraft": kw.get("draft", "draf uji"),
          "ruleChecklist": kw.get("rules", []),
          "specBlockers": kw.get("blockers", [])}
    if state_extra:
        st.update(state_extra)
    out = {"conversationId": "conv-1", "assistantState": st}
    if token is not None:
        out["curiosityToken"] = token
    if askfee is not None:
        out["askFee"] = askfee
    if kw.get("reclass"):
        out["arenaReclassification"] = kw["reclass"]
    if kw.get("suggestion"):
        out["questionSuggestion"] = {"text": kw["suggestion"]}
    return out


TOKEN = {"token": "tok-abc", "issuedAtMs": 123,
         "fee": {"feeTrued": "1.3504", "feeIndex": 8, "profile": "standard"}}
FEE_OK = {"feeTrued": "1.3504", "affordable": True, "spendableTrued": "5.0000"}
FEE_NO = {"feeTrued": "1.3504", "affordable": False, "spendableTrued": "-1.8788"}

# 1. drafting -> NEEDS_WORDING, blockers tersalur
t = ad.FixtureTransport([step("drafting", blockers=[{"path": "q", "message": "terlalu umum"}])])
r = ad.run_assist(t, "general", "draf uji")
check("drafting->NEEDS_WORDING", r["outcome"] == "NEEDS_WORDING")
check("blockers tersalur", r["specBlockers"][0]["message"] == "terlalu umum")
check("assist hanya 1 panggilan", len(t.calls) == 1 and t.calls[0]["path"] == "/api/node/isrs/assist")

# 2. ready + token -> READY_STOP, dan TIDAK ada panggilan create
t = ad.FixtureTransport([step("ready", token=TOKEN, askfee=FEE_OK)])
r = ad.run_assist(t, "general", "draf uji")
check("ready+token->READY_STOP", r["outcome"] == "READY_STOP")
check("nol panggilan create dari assist",
      all(c["path"] != "/api/node/isr" for c in t.calls))

# 3. ready tanpa token, affordable=false -> READY_WITHHELD + sebab fee
t = ad.FixtureTransport([step("ready", askfee=FEE_NO)])
r = ad.run_assist(t, "general", "draf uji")
check("ready withheld (saldo)", r["outcome"] == "READY_WITHHELD"
      and "Wallet" in r["withheldReason"] and "1.3504" in r["withheldReason"])

# 4. ready tanpa token, affordable=true -> READY_WITHHELD + saran reword
t = ad.FixtureTransport([step("ready", askfee=FEE_OK)])
r = ad.run_assist(t, "general", "draf uji")
check("ready withheld (keunikan)", r["outcome"] == "READY_WITHHELD"
      and "bukan penghalangnya" in r["withheldReason"])

# 5. duplikat tersitasi -> DUPLICATE_TERMINAL
rules = [{"rule_id": "SYS_UNIQUENESS", "passed": False,
          "citedDuplicates": [{"id": "isr-existing-1"}]}]
t = ad.FixtureTransport([step("drafting", rules=rules)])
r = ad.run_assist(t, "general", "draf uji")
check("duplikat->DUPLICATE_TERMINAL", r["outcome"] == "DUPLICATE_TERMINAL"
      and r["duplicates"] == ["isr-existing-1"])

# 6. fase terminal -> TERMINAL
t = ad.FixtureTransport([step("blocked")])
r = ad.run_assist(t, "general", "draf uji")
check("blocked->TERMINAL", r["outcome"] == "TERMINAL")

# 7. reklasifikasi arena diikuti
t = ad.FixtureTransport([step("ready", token=TOKEN, askfee=FEE_OK,
                              reclass={"arenaId": "forecasting",
                                       "arenaName": "Forecasting"})])
r = ad.run_assist(t, "general", "draf uji")
check("reklasifikasi diikuti", r["settledArena"] == "forecasting"
      and r["arenaNote"] is not None)

# 8. create: tanpa user-word -> ditolak; fee salah -> ditolak; benar -> jalan
state = {"draft": "draf uji", "settledArena": "general", "token": TOKEN,
         "askFee": FEE_OK, "resolutionSpec": None}
t = ad.FixtureTransport([])
try:
    ad.create_question(t, state, "1.3504", user_word=False)
    check("create tanpa user-word ditolak", False)
except PermissionError:
    check("create tanpa user-word ditolak", True)
try:
    ad.create_question(t, state, "9.9999", user_word=True)
    check("create fee salah ditolak", False)
except ValueError:
    check("create fee salah ditolak", True)
created = ad.create_question(t, state, "1.3504", user_word=True)
check("create benar jalan", created.get("id") == "fixture-isr-id")
body = t.calls[-1]["json_body"]
check("token di-echo persis", body["curiosityToken"] == TOKEN)
check("skema klasik general terpasang",
      body["outputSchema"] == ad.CLASSIC_OUTPUT_SCHEMA)
check("create tanpa token ditolak", _ := True)
state_notoken = dict(state, token=None)
try:
    ad.create_question(t, state_notoken, "1.3504", user_word=True)
    check("create state tanpa token ditolak", False)
except ValueError:
    check("create state tanpa token ditolak", True)

# 9. refresh_token diteruskan sebagai action
t = ad.FixtureTransport([step("ready", token=TOKEN, askfee=FEE_OK)])
r = ad.run_assist(t, "general", "", conversation_id="conv-1",
                  action="refresh_token")
check("refresh_token action terkirim",
      t.calls[0]["json_body"].get("action") == "refresh_token")

# 10. state file tertulis mode 0600 dan memuat token
t = ad.FixtureTransport([step("ready", token=TOKEN, askfee=FEE_OK)])
r = ad.run_assist(t, "general", "draf uji")
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "state.json")
    ad.write_state(r, p)
    mode = os.stat(p).st_mode & 0o777
    saved = json.load(open(p))
check("state file 0600 + token tersimpan",
      mode == 0o600 and saved["token"] == TOKEN)

print()
if FAILED:
    print(f"GAGAL: {len(FAILED)} uji: {FAILED}")
    sys.exit(1)
print("SEMUA UJI LOLOS")
