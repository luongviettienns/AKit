import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from akit.arena import start_session, next_tasks, submit, advance, auto_run, report, load
from akit.doctor import check
from akit.eval import read_jsonl
from akit.install import ROOT, VERSION, PROFILES, install


EXPECTED_24_REPOS = [
    "Jakeschincariol/arena-skill",
    "VoltAgent/awesome-design-md",
    "shanraisshan/claude-code-best-practice",
    "upstash/context7",
    "oraios/serena",
    "datawhalechina/easy-vibe",
    "Egonex-AI/Understand-Anything",
    "sickn33/agentic-awesome-skills",
    "rmyndharis/antigravity-skills",
    "dair-ai/Prompt-Engineering-Guide",
    "obra/superpowers",
    "affaan-m/everything-claude-code",
    "vercel-labs/agent-skills",
    "trailofbits/skills",
    "github/awesome-copilot",
    "wshobson/agents",
    "anthropics/skills",
    "getsentry/skills",
    "nextlevelbuilder/ui-ux-pro-max-skill",
    "supabase/agent-skills",
    "microsoft/playwright-cli",
    "semgrep/skills",
    "microsoft/postgres-skills",
    "JayZeeDesign/claude-code-vault",
]


class AKitV04UpgradeTests(unittest.TestCase):
    def test_version_and_30_skills_catalog(self):
        self.assertEqual(VERSION, "0.4.0")
        skills_dir = ROOT / "skills"
        available = sorted(p.name for p in skills_dir.iterdir() if (p / "SKILL.md").is_file())
        self.assertEqual(len(available), 30)
        self.assertIn("akit-debate", available)
        self.assertIn("akit-simplify", available)
        self.assertIn("akit-simplify", PROFILES["core"])
        self.assertIn("akit-debate", PROFILES["frontend"])
        self.assertIn("akit-debate", PROFILES["backend"])
        self.assertIn("akit-simplify", PROFILES["quality"])

    def test_all_30_skills_are_detailed_and_have_valid_references(self):
        skills_dir = ROOT / "skills"
        ref_pattern = re.compile(r"references/[A-Za-z0-9_.\-]+\.(?:md|jsonl)")
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md in {skill_dir.name}")
            content = skill_md.read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertGreaterEqual(
                len(lines), 60,
                f"Skill {skill_dir.name} has only {len(lines)} lines; expected >= 60 lines of detailed guidance"
            )
            self.assertGreaterEqual(
                len(content), 4500,
                f"Skill {skill_dir.name} has only {len(content)} chars; expected >= 4500 chars"
            )
            refs_dir = skill_dir / "references"
            self.assertTrue(refs_dir.is_dir(), f"Skill {skill_dir.name} is missing references/ directory")
            ref_files = [f for f in refs_dir.iterdir() if f.is_file()]
            self.assertGreaterEqual(len(ref_files), 1, f"Skill {skill_dir.name} has empty references/ directory")
            mentioned_refs = set(ref_pattern.findall(content))
            self.assertGreaterEqual(
                len(mentioned_refs), 1,
                f"Skill {skill_dir.name} does not link to any references/<file> in SKILL.md"
            )
            for rel_ref in mentioned_refs:
                target_ref = skill_dir / rel_ref
                self.assertTrue(
                    target_ref.is_file(),
                    f"Skill {skill_dir.name} references non-existent file {rel_ref}"
                )
                self.assertGreaterEqual(
                    len(target_ref.read_text(encoding="utf-8").splitlines()), 20,
                    f"Reference {skill_dir.name}/{rel_ref} is too thin (< 20 lines)"
                )

    def test_six_specialist_subagents_installed_for_antigravity_and_codex(self):
        expected_agents = {
            "akit-scout", "akit-critic", "akit-judge",
            "akit-debater", "akit-architect", "akit-security"
        }
        for target, ext in (("antigravity", ".md"), ("codex", ".toml")):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as td:
                project = Path(td)
                res = install(project, target=target, profile="core", with_agents=True)
                self.assertEqual(len(res["agents"]["installed"]), 6)
                installed_names = {Path(x).stem for x in res["agents"]["installed"]}
                self.assertEqual(installed_names, expected_agents)
                agent_folder = project / (".agents/agents" if target == "antigravity" else ".codex/agents")
                for stem in expected_agents:
                    fp = agent_folder / f"{stem}{ext}"
                    self.assertTrue(fp.is_file(), f"Missing {fp}")
                    text = fp.read_text(encoding="utf-8")
                    self.assertGreaterEqual(len(text.splitlines()), 20, f"Agent {fp.name} is too brief")

    def test_lightweight_debate_mode_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "debate-1"
            st = start_session(session, "Choose SSE vs WebSockets for live notifications", agents=3, mode="debate")
            self.assertEqual(st["mode"], "debate")
            self.assertEqual(st["phase"], "propose")
            tasks_1 = next_tasks(load(session))
            self.assertEqual(len(tasks_1), 1)
            self.assertEqual(tasks_1[0]["id"], "debate:propose")

            # Run full debate automatically using mock_worker (should take exactly 3 calls: propose, challenge, synthesize)
            done_state = auto_run(
                session,
                worker_argv=json.dumps([sys.executable, str(ROOT / "examples" / "mock_worker.py")]),
                max_calls=3
            )
            self.assertEqual(done_state["phase"], "done")
            self.assertEqual(done_state["winner"], "synthesized")
            md = report(done_state)
            self.assertIn("Debate Report", md)
            self.assertIn("Proposer", md)
            self.assertIn("Challenger", md)
            self.assertIn("Synthesized Decision", md)

    def test_cli_debate_mode_invocation(self):
        with tempfile.TemporaryDirectory() as td:
            session = Path(td) / "cli-debate"
            init_cmd = [
                sys.executable, "-m", "akit.arena", "init",
                "--session", str(session),
                "--mode", "debate",
                "--task", "Compare Redis Streams vs RabbitMQ"
            ]
            res = subprocess.run(init_cmd, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            run_cmd = [
                sys.executable, "-m", "akit.arena", "run",
                "--session", str(session),
                "--worker-argv", json.dumps([sys.executable, str(ROOT / "examples" / "mock_worker.py")]),
                "--max-calls", "3"
            ]
            res_run = subprocess.run(run_cmd, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(res_run.returncode, 0, res_run.stderr)
            self.assertIn("synthesized", res_run.stdout)

    def test_doctor_detects_missing_skill_reference(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install(project, target="antigravity", selected=["akit-router"], with_runtime=False)
            self.assertTrue(check(project)["ok"])
            # Delete a referenced file inside .agents/skills/akit-router/references/ and update manifest hash to isolate link check
            refs = list((project / ".agents/skills/akit-router/references").glob("*"))
            self.assertTrue(refs)
            refs[0].unlink()
            diag = check(project)
            self.assertFalse(diag["ok"])

    def test_all_24_repos_acknowledged_in_sources_md(self):
        sources_text = (ROOT / "docs" / "SOURCES.md").read_text(encoding="utf-8")
        for repo in EXPECTED_24_REPOS:
            self.assertIn(repo, sources_text, f"Missing {repo} in docs/SOURCES.md")

    def test_activation_cases_expanded_to_20(self):
        for rel in ("evals/activation_cases.jsonl", "skills/akit-eval/references/activation-cases.jsonl"):
            cases = read_jsonl(ROOT / rel)
            self.assertEqual(len(cases), 20, rel)
            all_expected = {s for c in cases for s in c["expected"]}
            self.assertIn("akit-debate", all_expected)
            self.assertIn("akit-simplify", all_expected)

    def test_mandatory_github_oss_prior_art_rule_and_slash_auto_orchestration(self):
        gemini_snippet = (ROOT / "examples" / "GEMINI.snippet.md").read_text(encoding="utf-8")
        from akit.install import GUIDANCE
        for doc_name, text in (("GEMINI.snippet.md", gemini_snippet), ("install.GUIDANCE", GUIDANCE)):
            self.assertIn(
                "đối với những chức năng chưa quen thuộc, đừng viết từ con số 0",
                text.lower(),
                f"Missing mandatory Vietnamese prior-art rule in {doc_name}"
            )
            self.assertIn(
                "tìm kiếm các dự án mã nguồn mở trên github để so sánh ý tưởng trước khi bắt tay vào làm",
                text.lower(),
                f"Missing GitHub OSS comparison clause in {doc_name}"
            )

        router_md = (ROOT / "skills" / "akit-router" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/slash-command-auto-orchestration.md", router_md)
        slash_ref = ROOT / "skills" / "akit-router" / "references" / "slash-command-auto-orchestration.md"
        self.assertTrue(slash_ref.is_file(), "Missing slash-command-auto-orchestration.md")
        slash_text = slash_ref.read_text(encoding="utf-8")
        for cmd in ("/plan", "/grill-me", "/boost", "/teamwork", "/goal", "/browser", "/compact", "/schedule", "/learn"):
            self.assertIn(cmd, slash_text, f"Missing {cmd} auto-orchestration mapping")

        prior_art_md = (ROOT / "skills" / "akit-prior-art" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/github-oss-search-playbook.md", prior_art_md)
        self.assertIn("đừng viết từ con số 0", prior_art_md.lower())
        oss_ref = ROOT / "skills" / "akit-prior-art" / "references" / "github-oss-search-playbook.md"
        self.assertTrue(oss_ref.is_file(), "Missing github-oss-search-playbook.md")

    def test_deep_obra_superpowers_mechanisms_present(self):
        # 1. Subagent-Driven Development (akit-implement)
        impl_md = (ROOT / "skills" / "akit-implement" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/subagent-driven-development-protocol.md", impl_md)
        sdd_ref = (ROOT / "skills" / "akit-implement" / "references" / "subagent-driven-development-protocol.md").read_text(encoding="utf-8")
        for token in ("DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED", "Ruling:", "progress.md"):
            self.assertIn(token, sdd_ref, f"Missing SDD token {token}")

        # 2. Writing Plans & Executing Plans (akit-plan)
        plan_md = (ROOT / "skills" / "akit-plan" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/superpowers-plan-spec.md", plan_md)
        plan_ref = (ROOT / "skills" / "akit-plan" / "references" / "superpowers-plan-spec.md").read_text(encoding="utf-8")
        for token in ("Consumes", "Produces", "Global Constraints", "Pre-flight Conflict Scan"):
            self.assertIn(token, plan_ref, f"Missing writing-plans token {token}")

        # 3. Requesting & Receiving Code Review (akit-review)
        rev_md = (ROOT / "skills" / "akit-review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/receiving-and-requesting-review.md", rev_md)
        rev_ref = (ROOT / "skills" / "akit-review" / "references" / "receiving-and-requesting-review.md").read_text(encoding="utf-8")
        self.assertIn("You're absolutely right!", rev_ref)
        self.assertIn("YAGNI", rev_ref)

        # 4. Systematic Debugging: Defense-in-Depth & Condition-Based Waiting (akit-debug)
        dbg_md = (ROOT / "skills" / "akit-debug" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/defense-in-depth-and-waiting.md", dbg_md)
        dbg_ref = (ROOT / "skills" / "akit-debug" / "references" / "defense-in-depth-and-waiting.md").read_text(encoding="utf-8")
        self.assertIn("Defense-in-Depth", dbg_ref)
        self.assertIn("waitFor", dbg_ref)

        # 5. Using Git Worktrees & Finishing a Development Branch (akit-git)
        git_md = (ROOT / "skills" / "akit-git" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/finishing-branch-protocol.md", git_md)
        git_ref = (ROOT / "skills" / "akit-git" / "references" / "finishing-branch-protocol.md").read_text(encoding="utf-8")
        self.assertIn("--show-superproject-working-tree", git_ref)
        self.assertIn("discard", git_ref)

    def test_auto_rules_wiring_on_install_preserves_user_gemini_md(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            res = install(project, target="antigravity", selected=["akit-router"], with_runtime=False)
            self.assertIn(".agents/rules/akit.md", res.get("auto_rules", []))
            self.assertIn("GEMINI.md", res.get("auto_rules", []))

            rule_file = project / ".agents" / "rules" / "akit.md"
            gemini_file = project / "GEMINI.md"
            self.assertTrue(rule_file.is_file(), "Expected .agents/rules/akit.md to be auto-created")
            self.assertTrue(gemini_file.is_file(), "Expected GEMINI.md to be auto-created for antigravity target")

            rule_text = rule_file.read_text(encoding="utf-8")
            self.assertIn("trigger: always_on", rule_text)
            self.assertIn("đối với những chức năng chưa quen thuộc, đừng viết từ con số 0", rule_text.lower())
            for law in ("Think Before Coding", "Simplicity First", "Surgical Changes", "Goal-Driven Execution"):
                self.assertIn(law, rule_text)

            # User adds custom rules around the managed block in GEMINI.md
            initial_gemini = gemini_file.read_text(encoding="utf-8")
            self.assertIn("<!-- AKIT:START -->", initial_gemini)
            self.assertIn("<!-- AKIT:END -->", initial_gemini)
            custom_gemini = "# My Team Custom Header\nKeep API v1 compatible.\n\n" + initial_gemini + "\n# My Team Footer\n"
            gemini_file.write_text(custom_gemini, encoding="utf-8")

            # Re-running install with upgrade=True must preserve custom header/footer and not duplicate markers
            install(project, target="antigravity", selected=["akit-router", "akit-plan"], upgrade=True, with_runtime=False)
            updated_gemini = gemini_file.read_text(encoding="utf-8")
            self.assertIn("# My Team Custom Header", updated_gemini)
            self.assertIn("# My Team Footer", updated_gemini)
            self.assertEqual(updated_gemini.count("<!-- AKIT:START -->"), 1)
            self.assertEqual(updated_gemini.count("<!-- AKIT:END -->"), 1)

    def test_karpathy_four_laws_code_quality_eval_and_skill_integration(self):
        from akit.eval import evaluate_karpathy_diff

        clean_diff = """diff --git a/src/auth.py b/src/auth.py
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,2 +10,5 @@
 def verify_token(token: str) -> bool:
+    if not token or not token.strip():
+        return False
     return token.startswith("tok_")
diff --git a/tests/test_auth.py b/tests/test_auth.py
--- a/tests/test_auth.py
+++ b/tests/test_auth.py
@@ -1,2 +1,6 @@
+def test_rejects_blank_token():
+    assert verify_token("   ") is False
"""
        clean_res = evaluate_karpathy_diff(
            diff_text=clean_diff,
            allowed_files=["src/auth.py", "tests/test_auth.py"],
            evidence={"status": "passed", "exit_code": 0},
            assumptions_stated=True,
            max_added_lines=60,
        )
        self.assertEqual(clean_res["kind"], "karpathy_4_laws_quality")
        self.assertEqual(clean_res["total_score"], 100)
        self.assertTrue(clean_res["passed"])
        self.assertEqual(clean_res["scores"]["think_before_coding"], 25)
        self.assertEqual(clean_res["scores"]["simplicity_first"], 25)
        self.assertEqual(clean_res["scores"]["surgical_changes"], 25)
        self.assertEqual(clean_res["scores"]["goal_driven_execution"], 25)

        sloppy_diff = """diff --git a/src/auth.py b/src/auth.py
--- a/src/auth.py
+++ b/src/auth.py
@@ -1,2 +1,8 @@
+class AbstractTokenValidationFactoryManager:
+    # TODO: implement speculative enterprise plugin strategy later
+    pass
+console.log("debug token")
diff --git a/src/unrelated_billing.py b/src/unrelated_billing.py
--- a/src/unrelated_billing.py
+++ b/src/unrelated_billing.py
@@ -1,2 +1,3 @@
+# reformatted unrelated file
"""
        sloppy_res = evaluate_karpathy_diff(
            diff_text=sloppy_diff,
            allowed_files=["src/auth.py"],
            evidence={"status": "failed", "exit_code": 1},
            assumptions_stated=False,
            max_added_lines=50,
        )
        self.assertFalse(sloppy_res["passed"])
        self.assertLess(sloppy_res["scores"]["think_before_coding"], 25)
        self.assertLess(sloppy_res["scores"]["simplicity_first"], 25)
        self.assertLess(sloppy_res["scores"]["surgical_changes"], 25)
        self.assertLess(sloppy_res["scores"]["goal_driven_execution"], 25)
        self.assertTrue(any("unrelated_billing.py" in v for v in sloppy_res["violations"]))

        # Verify CLI invocation of --mode karpathy
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            diff_fp = td_path / "clean.diff"
            ev_fp = td_path / "evidence.json"
            diff_fp.write_text(clean_diff, encoding="utf-8")
            ev_fp.write_text(json.dumps({"status": "passed", "exit_code": 0}), encoding="utf-8")
            cmd = [
                sys.executable, "-m", "akit.eval",
                "--mode", "karpathy",
                "--diff-file", str(diff_fp),
                "--evidence", str(ev_fp),
                "--allowed-files", "src/auth.py", "tests/test_auth.py",
                "--assumptions-stated",
            ]
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            cli_out = json.loads(proc.stdout)
            self.assertEqual(cli_out["total_score"], 100)

        # Verify akit-eval SKILL.md and SOURCES.md integration
        eval_md = (ROOT / "skills" / "akit-eval" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/karpathy-4-laws-eval-rubric.md", eval_md)
        self.assertTrue((ROOT / "skills" / "akit-eval" / "references" / "karpathy-4-laws-eval-rubric.md").is_file())
        sources_md = (ROOT / "docs" / "SOURCES.md").read_text(encoding="utf-8")
        self.assertIn("multica-ai/andrej-karpathy-skills", sources_md)


if __name__ == "__main__":
    unittest.main()
