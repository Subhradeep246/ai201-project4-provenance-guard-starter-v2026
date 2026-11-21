"""Report regressions: real saved observations and synthetic failure responses.

No model loading, API traffic, or audit-log changes are needed.
"""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import run_attacks


class AttackReportTests(unittest.TestCase):
    def test_human_fixtures_are_only_accused_by_ai_label(self):
        for family in ("false_positive", "lumpy_human"):
            for guess, expected in (("human", "HELD"), ("unsure", "HELD"), ("ai", "BROKE")):
                with self.subTest(family=family, guess=guess):
                    verdict, note = run_attacks.auto_verdict(200, {"guess": guess}, None, family)
                    self.assertEqual(verdict, expected)
                    self.assertTrue(note)

    def test_ai_and_evasion_fixtures_require_ai_label(self):
        for family in ("clearly_ai", "evasion_typos", "evasion_break", "evasion_quote"):
            for guess, expected in (("human", "BROKE"), ("unsure", "BROKE"), ("ai", "HELD")):
                with self.subTest(family=family, guess=guess):
                    self.assertEqual(run_attacks.auto_verdict(200, {"guess": guess}, None, family)[0], expected)

    def test_rejections_do_not_masquerade_as_classification_success(self):
        self.assertEqual(run_attacks.auto_verdict(429, {}, None, "evasion_break")[0], "REVIEW")
        self.assertEqual(run_attacks.auto_verdict(400, {}, None, "false_positive")[0], "BROKE")
        for payload in ({}, {"guess": "unknown"}, {"guess": []}, []):
            with self.subTest(payload=payload):
                self.assertEqual(run_attacks.auto_verdict(200, payload, None, "clearly_ai")[0], "BROKE")

    def test_malformed_and_flood_have_distinct_expectations(self):
        cases = [("malformed", 400, "HELD"), ("malformed", 200, "BROKE"),
                 ("malformed", 429, "REVIEW"), ("flood_same_creator", 429, "HELD"),
                 ("flood_same_creator", 200, "BROKE")]
        for family, status, expected in cases:
            with self.subTest(family=family, status=status):
                self.assertEqual(run_attacks.auto_verdict(status, {}, None, family)[0], expected)
        self.assertIn("not a limiter failure", run_attacks.auto_verdict(200, {}, None, "flood_same_creator")[1])

    def test_unknown_families_and_operational_errors_are_explicit(self):
        self.assertEqual(run_attacks.auto_verdict(200, {"guess": "ai"}, None, "new_family")[0], "REVIEW")
        for status, payload, error in [(None, None, "ConnectionError: down"),
                                       (None, None, None), (200, None, "not JSON"),
                                       (503, {}, None)]:
            self.assertEqual(run_attacks.auto_verdict(status, payload, error, "malformed")[0], "BROKE")

    def test_saved_before_after_are_judged_without_changing_observations(self):
        attacks, problems = run_attacks.load_attacks(Path("attack_set"))
        self.assertFalse(problems)
        for filename, fp02 in [("attack_run_2026-11-12_1236_before.md", "BROKE"),
                               ("attack_run_2026-11-12_1237_after.md", "HELD")]:
            path = Path("results") / filename
            original = path.read_bytes()
            rows = run_attacks.rejudge_report(path, attacks)
            self.assertEqual(len(rows), 36)
            self.assertTrue(all(r["verdict"] and r["note"] for r in rows))
            by_id = {r["id"]: r for r in rows}
            self.assertEqual(by_id["FP02"]["verdict"], fp02)
            self.assertEqual(by_id["EV03"]["verdict"], "BROKE")
            self.assertEqual(by_id["FL11"]["verdict"], "HELD")
            blocks = run_attacks.re.findall(r"```json\s*\n(.*?)\n```", original.decode("utf-8"), run_attacks.re.S)
            for row, block in zip(rows, blocks):
                saved = json.loads(block)
                for field in ("status", "content_id", "guess", "confidence", "model_score", "style_score"):
                    self.assertEqual(row.get(field), saved.get(field))
            self.assertEqual(path.read_bytes(), original)

    def test_saved_duplicates_are_rejected(self):
        attacks = [{"id": "X", "family": "malformed", "targets": "crash"}]
        block = '```json\n{"id":"X","status":400}\n```\n'
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate.md"
            path.write_text(block * 2, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                run_attacks.rejudge_report(path, attacks)

    def test_live_runner_records_nonobject_json_without_crashing(self):
        # Synthetic HTTP response checks the harness, not detector quality.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(run_attacks.config, "ROOT", root), \
                 patch.object(run_attacks.config, "RESULTS_DIR", root / "results"), \
                 patch("sys.argv", ["run_attacks.py", "--set", "attack_set", "--id", "FP01"]), \
                 patch("requests.get", return_value=Mock(json=lambda: {"rate_limiting": True})), \
                 patch.object(run_attacks, "send", return_value=(200, [], None)), \
                 contextlib.redirect_stdout(io.StringIO()):
                run_attacks.main()
            report = next((root / "results").glob("*.md")).read_text(encoding="utf-8")
            self.assertIn("BROKE", report)
            self.assertIn("response must be a JSON object", report)

    def test_reports_expose_reasons_and_saved_source(self):
        attacks, _ = run_attacks.load_attacks(Path("attack_set"))
        source = Path("results/attack_run_2026-11-12_1237_after.md")
        rows = run_attacks.rejudge_report(source, attacks)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(run_attacks.config, "ROOT", root), \
                 patch.object(run_attacks.config, "RESULTS_DIR", root / "results"), \
                 contextlib.redirect_stdout(io.StringIO()):
                path = run_attacks.write_report(rows, SimpleNamespace(label="test", rejudge=source))
            report = path.read_text(encoding="utf-8")
            self.assertIn("| Verdict | Reason |", report)
            self.assertIn("no new API requests", report)
            self.assertIn("**10 accepted**, **2 blocked (429)**", report)
            self.assertIn('"note":', report)


if __name__ == "__main__":
    unittest.main()
