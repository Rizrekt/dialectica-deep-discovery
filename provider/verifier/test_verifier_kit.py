#!/usr/bin/env python3
"""Unit tests for the Verifier kit (Jalur 2, 2026-11-18).

Pure parts only: payload parsers, the self-dealing gate, the local
verdict drafter, the lane reply parser + agreement comparison, the
registration gate, and the runner's send lock. No network anywhere
— transports and preflights are stubbed where a code path would
otherwise reach for one.

Run: python3 -m unittest test_verifier_kit -v   (from this folder)
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lane_drafter  # noqa: E402
import register_ivsp  # noqa: E402
import run_verifier  # noqa: E402
import self_dealing_gate as gate  # noqa: E402
import verdict_drafter as vd  # noqa: E402
import verifier_common as vc  # noqa: E402

OUR = "5fb160401bc13c5720b9c9fd879b414e54190b5f"
OTHER = "fcee15bc6b6993a383e4cbfb021babfacb00fbf4"
IDENTITY = {"user_ids": {OUR}, "usernames": {"rizrekt"},
            "iso_ids": {"own-iso-1"}, "isr_ids": {"own-isr-1"}}


def iso_row(**kw):
    base = {"id": "iso-x", "isrId": "isr-x", "author": OTHER,
            "ownerName": "someone", "isOwnAgent": False,
            "status": "revealed", "verifierCount": 0,
            "supportedCount": 0, "refutationCount": 0,
            "reveal": {"data": {"structured_data": {"answer": "text"}}}}
    base.update(kw)
    return base


class TestParsers(unittest.TestCase):
    def test_iso_row_classic(self):
        cand = vc.parse_iso_row(iso_row(), {"id": "isr-x",
                                            "content": "Why?",
                                            "author": OTHER})
        self.assertEqual(cand["answer"], "text")
        self.assertEqual(cand["isoId"], "iso-x")
        self.assertFalse(cand["isOwnAgent"])

    def test_iso_row_forecasting_shape(self):
        row = iso_row(reveal={"data": {"structured_data": {
            "reasoning": "because markets", "prediction": "Yes"}}})
        cand = vc.parse_iso_row(row, {})
        self.assertIn("because markets", cand["answer"])
        self.assertIn("Yes", cand["answer"])

    def test_job_record_answering(self):
        job = {"id": "j1", "type": "ISO", "jobStatus": "completed",
               "input": {"isrId": "q1", "isrContent": "Q?",
                         "isrAuthor": OTHER}}
        parsed = vc.parse_job_record(job)
        self.assertEqual(parsed["kind"], "ISR")
        self.assertEqual(parsed["isrId"], "q1")

    def test_job_record_verification(self):
        job = {"id": "j2", "type": "VFP", "jobStatus": "running",
               "input": {"isrId": "q1", "targetIsoId": "a1"}}
        parsed = vc.parse_job_record(job)
        self.assertEqual(parsed["kind"], "VFP")
        self.assertEqual(parsed["isoId"], "a1")

    def test_gateway_event_from_system_user(self):
        ev = {"sender": "@system:dialectica.xyz", "event_id": "$e1",
              "content": {"org.dialectica.type": "execute-job",
                          "org.dialectica.data": {
                              "jobId": "j9",
                              "opportunity": {"type": "VFP",
                                              "isrId": "q1",
                                              "targetIsoId": "a1"}},
                          "body": "prompt"}}
        item = vc.parse_gateway_event(ev, "@system:dialectica.xyz")
        self.assertEqual(item["jobId"], "j9")
        self.assertEqual(item["isoId"], "a1")
        self.assertEqual(item["jobKind"], "VFP")

    def test_gateway_event_wrong_sender_dropped(self):
        ev = {"sender": "@mallory:dialectica.xyz",
              "content": {"org.dialectica.type": "execute-job",
                          "org.dialectica.data": {"jobId": "j9"}}}
        self.assertIsNone(vc.parse_gateway_event(ev, "@system:x"))

    def test_gateway_event_job_without_id_dropped(self):
        ev = {"sender": "@system:x",
              "content": {"org.dialectica.type": "execute-job",
                          "org.dialectica.data": {}}}
        self.assertIsNone(vc.parse_gateway_event(ev, "@system:x"))

    def test_gateway_event_evaluate(self):
        ev = {"sender": "@system:x",
              "content": {"org.dialectica.type": "evaluate-request",
                          "org.dialectica.data": {"requestId": "r1"}}}
        item = vc.parse_gateway_event(ev, "@system:x")
        self.assertEqual(item["kind"], "evaluate")


class TestGate(unittest.TestCase):
    def cand(self, **kw):
        base = {"isOwnAgent": False, "answerAuthor": OTHER,
                "questionAuthor": OTHER, "isoId": "iso-x",
                "isrId": "isr-x", "answerOwnerName": "someone"}
        base.update(kw)
        return base

    def test_clean_candidate_allowed(self):
        self.assertTrue(gate.check_candidate(self.cand(), IDENTITY)["allowed"])

    def test_is_own_agent_flag_refused(self):
        out = gate.check_candidate(self.cand(isOwnAgent=True), IDENTITY)
        self.assertFalse(out["allowed"])
        self.assertTrue(any("isOwnAgent" in r for r in out["reasons"]))

    def test_own_answer_author_refused(self):
        out = gate.check_candidate(self.cand(answerAuthor=OUR), IDENTITY)
        self.assertFalse(out["allowed"])

    def test_own_question_author_refused(self):
        out = gate.check_candidate(self.cand(questionAuthor=OUR), IDENTITY)
        self.assertFalse(out["allowed"])

    def test_denylist_iso_refused(self):
        out = gate.check_candidate(self.cand(isoId="own-iso-1"), IDENTITY)
        self.assertFalse(out["allowed"])

    def test_denylist_isr_refused(self):
        out = gate.check_candidate(self.cand(isrId="own-isr-1"), IDENTITY)
        self.assertFalse(out["allowed"])

    def test_username_match_refused(self):
        out = gate.check_candidate(
            self.cand(answerOwnerName="rizrekt"), IDENTITY)
        self.assertFalse(out["allowed"])


class TestDrafter(unittest.TestCase):
    Q = ("Why does extending a TWAP oracle window raise the cost of "
         "manipulation for an attacker?")

    def test_citation_fail_numbers_no_citations(self):
        answer = ("The cost rises to 4.7 million dollars in 2023 because "
                  "the attacker must hold the position for 30 percent "
                  "longer across every block in the window, and therefore "
                  "the capital lock-up grows with the window length.")
        out = vd.check_citation(answer)
        self.assertEqual(out["status"], "fail")

    def test_citation_unknown_when_sources_present(self):
        answer = ("The cost reached $4.7 million in 2023 "
                  "(https://example.org/paper) because capital must be "
                  "held longer, therefore the lock-up grows.")
        out = vd.check_citation(answer)
        self.assertEqual(out["status"], "unknown")

    def test_reasoning_fail_too_short(self):
        out = vd.check_reasoning("It just costs more.")
        self.assertEqual(out["status"], "fail")

    def test_reasoning_fail_no_connectives(self):
        answer = ("The window is long. The price is sampled many times. "
                  "The attacker holds a large position. The blocks pass. "
                  "The average moves slowly. The protocol reads the "
                  "average. The cost is high. The trade is unprofitable.")
        out = vd.check_reasoning(answer)
        self.assertEqual(out["status"], "fail")

    def test_uncertainty_fail_absolute_over_claims(self):
        answer = ("This always guarantees a 40 percent saving in 2024 "
                  "and never fails, because the mechanism is proven in "
                  "every single case without exception.")
        out = vd.check_uncertainty(answer)
        self.assertEqual(out["status"], "fail")

    def test_scope_fail_no_overlap(self):
        out = vd.check_scope(self.Q, "Bananas are yellow fruit that "
                                     "grow in tropical climates and "
                                     "are rich in potassium.")
        self.assertEqual(out["status"], "fail")

    def test_scope_fail_environment_report(self):
        out = vd.check_scope(self.Q, "I cannot access the files in my "
                                     "home directory, so here is a "
                                     "general note about oracles.")
        self.assertEqual(out["status"], "fail")

    def test_full_draft_noncompliant_on_any_fail(self):
        draft = vd.draft_verdict(self.Q, "It just costs more.")
        self.assertEqual(draft["verdict"], "non-compliant")

    def test_full_draft_compliant_shape(self):
        answer = ("Extending the window raises the manipulation cost "
                  "because the attacker must hold a distorted price "
                  "across many more blocks, and therefore the capital "
                  "committed grows roughly with the window length. "
                  "This tends to make short-lived distortions "
                  "unprofitable, although the exact effect may vary "
                  "with liquidity, since thin markets behave "
                  "differently from deep ones.")
        draft = vd.draft_verdict(self.Q, answer)
        self.assertEqual(draft["checks"]["A_REASONING"]["status"], "pass")
        self.assertEqual(draft["checks"]["A_SCOPE"]["status"], "pass")
        self.assertEqual(draft["verdict"], "compliant")


class TestLaneParsing(unittest.TestCase):
    GOOD = json.dumps({"checks": {
        "A_CITATION": {"pass": True, "reason": "ok"},
        "A_REASONING": {"pass": True, "reason": "ok"},
        "A_UNCERTAINTY": {"pass": False, "reason": "stated as fact"},
        "A_SCOPE": {"pass": True, "reason": "ok"}}})

    def test_parse_and_recompute(self):
        parsed, note = lane_drafter.parse_lane_reply(self.GOOD)
        self.assertEqual(note, "ok")
        self.assertEqual(parsed["verdict"], "non-compliant")
        self.assertFalse(parsed["checks"]["A_UNCERTAINTY"]["pass"])

    def test_parse_all_pass_compliant(self):
        good = json.dumps({"checks": {
            k: {"pass": True, "reason": "ok"}
            for k in lane_drafter.CHECKS}})
        parsed, _ = lane_drafter.parse_lane_reply(good)
        self.assertEqual(parsed["verdict"], "compliant")

    def test_parse_missing_check_rejected(self):
        bad = json.dumps({"checks": {"A_CITATION": {"pass": True}}})
        parsed, note = lane_drafter.parse_lane_reply(bad)
        self.assertIsNone(parsed)
        self.assertIn("missing-check", note)

    def test_parse_garbage_rejected(self):
        parsed, _ = lane_drafter.parse_lane_reply("no json here")
        self.assertIsNone(parsed)

    def test_compare_drafts_detects_disagreement(self):
        local = {"drafter": "local-mechanical-v1", "verdict": "compliant",
                 "checks": {k: {"status": "pass"}
                            for k in lane_drafter.CHECKS}}
        lane = {"lane": "qwen", "verdict": "non-compliant",
                "available": True,
                "checks": {k: {"pass": k != "A_CITATION"}
                           for k in lane_drafter.CHECKS}}
        out = lane_drafter.compare_drafts([local, lane])
        self.assertFalse(out["all_agree"])
        self.assertIn("A_CITATION", out["check_disagreements"])


class TestLocks(unittest.TestCase):
    def test_registration_refused_without_markers(self):
        env_ok, file_ok = register_ivsp.approval_state(
            env={}, approval_file="/nonexistent/USER-APPROVAL-IVSP.txt")
        self.assertFalse(env_ok)
        self.assertFalse(file_ok)
        self.assertEqual(register_ivsp.main(), 3)

    def test_registration_execute_disabled_as_delivered(self):
        self.assertFalse(register_ivsp.EXECUTE_ENABLED)

    def test_registration_armed_dry_makes_no_registration(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt",
                                         delete=False) as fh:
            fh.write(register_ivsp.APPROVAL_PHRASE)
            path = fh.name
        old_file = register_ivsp.APPROVAL_FILE
        old_preflight = register_ivsp.preflight
        try:
            register_ivsp.APPROVAL_FILE = path
            register_ivsp.preflight = lambda: {"stubbed": True}
            os.environ[register_ivsp.APPROVAL_ENV] = "1"
            self.assertEqual(register_ivsp.main(), 4)
        finally:
            register_ivsp.APPROVAL_FILE = old_file
            register_ivsp.preflight = old_preflight
            os.environ.pop(register_ivsp.APPROVAL_ENV, None)
            os.unlink(path)

    def test_send_lock(self):
        self.assertEqual(run_verifier.main(["--send"]), 5)


if __name__ == "__main__":
    unittest.main()
