import json
import sys
import tempfile
import unittest
from pathlib import Path

from akit.arena import (start_session, load, next_tasks, submit, advance, validate_judgment,
                        auto_run, report, RUBRIC)
from akit.install import install

ROOT = Path(__file__).resolve().parents[1]


class ArenaTests(unittest.TestCase):
    def test_4_agents_full_tournament(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "r"
            start_session(session, "Propose a verified simple API", 4, 7)
            state = auto_run(session, f'{sys.executable} {ROOT / "examples" / "mock_worker.py"}', max_workers=2)
            self.assertEqual(state["phase"], "done")
            self.assertEqual(len(state["history"]), 3)
            self.assertEqual(state["winner"], "a001")
            self.assertIn("not proof of correctness", report(state))
            self.assertEqual(len(next_tasks(state)), 0)

    def test_three_agents_bye(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "r"
            start_session(session, "A task", 3, 11)
            state = auto_run(session, f'{sys.executable} {ROOT / "examples" / "mock_worker.py"}')
            self.assertEqual(len(state["history"]), 2)
            self.assertEqual(state["winner"], "a001")

    def test_prevents_skipping_or_invalid_submit(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "r"
            start_session(session, "Task", 2)
            with self.assertRaises(ValueError):
                advance(session)
            with self.assertRaises(ValueError):
                submit(session, "judge:r1-m1", "{}")
            first = next_tasks(load(session))[0]["id"]
            submit(session, first, "My solution")
            with self.assertRaises(ValueError):
                submit(session, first, "Duplicate")

    def test_invalid_judge_results(self):
        valid = {"a": {"scores": dict(RUBRIC), "fatal_flaw": False, "fatal_evidence": ""},
                 "b": {"scores": {key: 0 for key in RUBRIC}, "fatal_flaw": False, "fatal_evidence": ""},
                 "reason": "The first covers the requirements better."}
        self.assertEqual(validate_judgment(json.dumps(valid))["a"]["scores"]["correctness"], 30)
        valid["a"]["scores"]["correctness"] = 999
        with self.assertRaises(ValueError):
            validate_judgment(json.dumps(valid))
        valid["a"]["scores"]["correctness"] = 20
        valid["a"]["fatal_flaw"] = True
        with self.assertRaises(ValueError):
            validate_judgment(json.dumps(valid))

    def test_limits_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "r"
            with self.assertRaises(ValueError):
                start_session(session, "x", 33)
            start_session(session, "Task", 2)
            with self.assertRaises(FileExistsError):
                start_session(session, "Task2", 2)


class InstallerTests(unittest.TestCase):
    def test_install_safe_skip_dry_run(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            dry = install(project, "shared", ["akit-router"], dry_run=True)
            self.assertEqual(len(dry["installed"]), 1)
            self.assertFalse((project / ".agents").exists())
            first = install(project, "shared", ["akit-router"])
            self.assertEqual(first["installed"], ["akit-router"])
            existing = project / ".agents" / "skills" / "akit-router" / "SKILL.md"
            existing.write_text("DO NOT OVERWRITE", encoding="utf-8")
            second = install(project, "shared", ["akit-router"])
            self.assertEqual(second["skipped"], ["akit-router"])
            self.assertEqual(existing.read_text(encoding="utf-8"), "DO NOT OVERWRITE")

    def test_skills_have_frontmatter(self):
        for skill in (ROOT / "skills").iterdir():
            doc = (skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(doc.startswith("---\nname: " + skill.name + "\n"))
            self.assertIn("\ndescription: ", doc)
            self.assertIn("\n---\n", doc)


if __name__ == "__main__":
    unittest.main()
