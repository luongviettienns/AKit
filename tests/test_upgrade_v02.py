import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from akit.arena import parse_worker_command, start_session, auto_run
from akit.checks import run_checks
from akit.doctor import check
from akit.eval import score
from akit.install import ROOT, PROFILES, install, digest_dir


class Version2InstallerTests(unittest.TestCase):
    def test_fresh_install_runtime_and_doctor_from_destination(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            result = install(project, 'antigravity', profile='core', with_agents=True, with_guidance=True)
            self.assertEqual(len(result['agents']['installed']), 6)
            self.assertEqual(result['runtime'], 'installed')
            self.assertTrue((project / '.agents/agents/akit-judge.md').exists())
            self.assertEqual(len(result['installed']), len(PROFILES['core']))
            self.assertTrue(check(project)['ok'])
            script = project / '.akit/runtime/akit_cli.py'
            for subcmd, extra in [('doctor', ['--project', str(project)]), ('arena', ['--help']), ('eval', ['--help']), ('checks', ['--help'])]:
                proc = subprocess.run([sys.executable, str(script), subcmd, *extra], capture_output=True, text=True, cwd=project)
                self.assertEqual(proc.returncode, 0, (subcmd, proc.stderr))

    def test_upgrades_managed_skill_with_backup(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install(project, 'codex', ['akit-router'])
            with patch('akit.install.digest_dir', wraps=digest_dir):
                result = install(project, 'codex', ['akit-router'], upgrade=True)
                self.assertEqual(result['skipped'], ['akit-router'])
            self.assertTrue(check(project)['ok'])

    def test_preserves_locally_modified_skill(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install(project, 'antigravity', ['akit-router'])
            p = project/'.agents/skills/akit-router/SKILL.md'
            p.write_text(p.read_text(encoding='utf-8')+'\ncustom user text\n', encoding='utf-8')
            result = install(project, 'antigravity', ['akit-router'], upgrade=True)
            self.assertEqual(result['modified'], ['akit-router'])
            self.assertIn('custom user text', p.read_text(encoding='utf-8'))
            self.assertFalse(check(project)['ok'])

    def test_rejects_parent_symlink(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as external:
            project = Path(td)
            try:
                (project / '.agents').symlink_to(external, target_is_directory=True)
            except OSError:
                self.skipTest('Cannot create symlink in this environment')
            with self.assertRaises(ValueError):
                install(project, 'antigravity', ['akit-router'])

    def test_does_not_overwrite_existing_agent(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)
            target=project/'.agents/agents/akit-judge.md'
            target.parent.mkdir(parents=True)
            target.write_text('I am user supplied')
            result=install(project, 'antigravity', ['akit-router'], with_agents=True)
            self.assertIn('akit-judge.md', result['agents']['skipped'])
            self.assertEqual(target.read_text(), 'I am user supplied')

    def test_target_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)
            install(project,'antigravity',['akit-router'])
            with self.assertRaises(ValueError):
                install(project,'cursor',['akit-router'])

    def test_full_profile_coverage(self):
        available={p.name for p in (ROOT/'skills').iterdir() if (p/'SKILL.md').exists()}
        self.assertEqual(len(available), 30)
        for profile, chosen in PROFILES.items():
            self.assertEqual(set(chosen)-available,set(),profile)


class WorkerAndEvaluationTests(unittest.TestCase):
    def test_windows_path_with_spaces(self):
        cmd=r'"C:\Program Files\Python\python.exe" "D:\My Project\agent.py"'
        self.assertEqual(parse_worker_command(cmd, windows=True),[r'C:\Program Files\Python\python.exe',r'D:\My Project\agent.py'])
        j=json.dumps([r'C:\Program Files\Python\python.exe',r'D:\My Project\agent.py'])
        self.assertEqual(parse_worker_command(worker_argv=j),[r'C:\Program Files\Python\python.exe',r'D:\My Project\agent.py'])
        with self.assertRaises(ValueError):
            parse_worker_command(worker_argv='["cmd",5]')

    def test_worker_explicit_budget(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td)/'run'
            start_session(run,'Task',4)
            with self.assertRaisesRegex(ValueError,'max-calls'):
                auto_run(run, worker_argv=json.dumps([sys.executable, str(ROOT/'examples/mock_worker.py')]), max_calls=4)

    def test_activation_eval_does_not_invent_data(self):
        cases=[{'id':'x','expected':['akit-test']},{'id':'y','expected':['akit-debug']}]
        outcome=score(cases,[{'id':'x','selected':['akit-test']}])
        self.assertEqual(outcome['coverage'],0.5)
        self.assertEqual(outcome['recall'],0.5)
        self.assertEqual(outcome['f1'],round(2*1*0.5/(1+0.5),4))

    def test_command_evidence_success_and_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            ok=run_checks(root,[sys.executable,'-c','print(42)'],root/'.akit/evidence.json')
            self.assertEqual(ok['status'],'passed')
            self.assertEqual(ok['exit_code'],0)
            self.assertEqual(json.loads((root/'.akit/evidence.json').read_text())['stdout_tail'].strip(),'42')
            fail=run_checks(root,[sys.executable,'-c','raise SystemExit(7)'],root/'.akit/fail.json')
            self.assertEqual(fail['status'],'failed')
            self.assertEqual(fail['exit_code'],7)


if __name__ == '__main__':
    unittest.main()
