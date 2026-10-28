import json
import os
import subprocess
import sys
import tempfile
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9-3.10: runtime works; TOML parser test deferred
    tomllib = None
import unittest
from pathlib import Path
from unittest.mock import patch

from akit.arena import start_session, auto_run
from akit.doctor import check
from akit.eval import score, read_jsonl
from akit.install import install, PROFILES, ROOT, VERSION


class InstallerV02Tests(unittest.TestCase):
    def test_core_is_compact_all_skills_nonempty(self):
        available = [p for p in (ROOT / 'skills').iterdir() if (p / 'SKILL.md').is_file()]
        self.assertEqual(len(available), 30)
        self.assertEqual(len(PROFILES['core']), 12)
        for name, group in PROFILES.items():
            if name != 'full':
                self.assertEqual(len(group), len(set(group)))
                self.assertTrue(set(group).issubset({x.name for x in available}))

    def test_prior_art_principle_is_wired_everywhere(self):
        from akit.install import GUIDANCE
        self.assertIn('akit-prior-art', PROFILES['core'])
        for profile in ('frontend', 'backend'):
            self.assertIn('akit-prior-art', PROFILES[profile])
        for skill in ('akit-router', 'akit-implement', 'akit-architecture', 'akit-plan'):
            text = (ROOT / 'skills' / skill / 'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('akit-prior-art', text, skill)
        self.assertIn('akit-prior-art', GUIDANCE)
        self.assertIn('akit-prior-art', (ROOT / 'examples/AGENTS.snippet.md').read_text(encoding='utf-8'))
        refs = ROOT / 'skills/akit-prior-art/references'
        for name in ('prior-art-report.template.md', 'github-search-cheatsheet.md', 'reference-repos.md'):
            self.assertTrue((refs / name).is_file(), name)

    def test_antigravity_and_codex_agents_and_runtime(self):
        for target in ('antigravity', 'codex'):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                result = install(path, target, profile='core', with_agents=True, with_guidance=True)
                self.assertEqual(len(result['installed']), 12)
                self.assertEqual(len(result['agents']['installed']), 6)
                self.assertTrue(check(path)['ok'])
                self.assertTrue((path / '.akit' / 'runtime' / 'akit_cli.py').is_file())
                self.assertTrue((path / 'AKIT_AGENT_GUIDANCE.md').is_file())
                self.assertFalse((path / 'AGENTS.md').exists())
                agent_dir = path / ('.codex/agents' if target == 'codex' else '.agents/agents')
                for agent in agent_dir.iterdir():
                    if target == 'codex':
                        if tomllib is not None:
                            data = tomllib.loads(agent.read_text(encoding='utf-8'))
                            self.assertTrue(all(data.get(k) for k in ('name', 'description', 'developer_instructions')))
                    else:
                        body = agent.read_text(encoding='utf-8')
                        self.assertIn('subagent: true', body)
                        self.assertIn('mainAgent: false', body)
                        self.assertIn('commandExecutionPolicy: off', body)
                run = subprocess.run([sys.executable, str(path / '.akit/runtime/akit_cli.py'), 'doctor', '--project', str(path)],
                                     text=True, capture_output=True, check=False)
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_codex_then_antigravity_keeps_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            install(project, 'codex', profile='core', with_agents=True)
            old = project / '.agents' / 'skills' / 'akit-router' / 'SKILL.md'
            old.write_text('CUSTOM', encoding='utf-8')
            result = install(project, 'antigravity', profile='core', with_agents=True, upgrade=True)
            self.assertIn('akit-router', result['modified'])
            self.assertEqual(old.read_text(encoding='utf-8'), 'CUSTOM')
            self.assertEqual(len(result['agents']['installed']), 6)
            self.assertFalse(check(project)['ok'])  # detects modified tracked skill
            self.assertEqual((project/'.akit/AKIT_INSTALL.json').exists(), True)

    def test_managed_upgrade_no_changes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            install(project, 'codex', profile='quality', with_agents=True)
            outcome = install(project, 'codex', profile='quality', upgrade=True, with_agents=True)
            self.assertFalse(outcome['updated'])
            self.assertIn(outcome['runtime'], ('unchanged', 'skipped'))
            agent = project / '.codex/agents/akit-scout.toml'
            agent.write_text('owned by user', encoding='utf-8')
            outcome = install(project, 'codex', profile='quality', upgrade=True, with_agents=True)
            self.assertIn('akit-scout.toml', outcome['agents']['modified'])
            self.assertEqual(agent.read_text(encoding='utf-8'), 'owned by user')

    def test_real_upgrade_produces_backup_and_new_hash(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            project = temp/'project'
            install(project, 'codex', ['akit-router'], with_runtime=False)
            previous = (project/'.agents/skills/akit-router/SKILL.md').read_text(encoding='utf-8')
            replacement_root = temp/'new-source'
            new_skill = replacement_root/'skills/akit-router'
            new_skill.mkdir(parents=True)
            (new_skill/'SKILL.md').write_text(previous+'\n# New version marker\n', encoding='utf-8')
            from akit import install as installer_module
            with patch.object(installer_module, 'ROOT', replacement_root):
                change = install(project, 'codex', ['akit-router'], upgrade=True, with_runtime=False)
            self.assertEqual(change['updated'], ['akit-router'])
            self.assertTrue((project/'.agents/skills/akit-router/SKILL.md').read_text(encoding='utf-8').endswith('# New version marker\n'))
            backups = list((project/'.akit/backups').rglob('SKILL.md'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding='utf-8'), previous)
            self.assertTrue(check(project)['ok'])

    def test_dry_run_no_side_effects_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = install(project, 'codex', profile='full', with_agents=True, dry_run=True)
            self.assertEqual(len(result['installed']), 30)
            self.assertEqual(list(project.iterdir()), [])

    def test_installed_runtime_supports_arena(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, 'codex', profile='core')
            cli = root / '.akit/runtime/akit_cli.py'
            run = subprocess.run([sys.executable, str(cli), 'arena', 'init', '--session', str(root/'.akit/runs/a'),
                                  '--agents', '2', '--task', 'Choose test framework'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((root/'.akit/runs/a/state.json').is_file())


class ArenaAndEvalV02Tests(unittest.TestCase):
    def test_call_budget_blocks_more_than_four_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'eight'
            start_session(path, 'Discuss architecture', 8)
            with self.assertRaisesRegex(ValueError, '43 worker calls'):
                auto_run(path, 'python testworker.py')
            self.assertEqual(json.loads((path/'state.json').read_text())['phase'], 'propose')

    def test_eval_metrics_not_fake_agent_quality(self):
        cases = [{'id':'1','expected':['akit-debug']},{'id':'2','expected':['akit-security']},{'id':'3','expected':[]}]
        observations = [{'id':'1','selected':['akit-debug']}, {'id':'2','selected':['akit-review']}]
        out = score(cases, observations)
        self.assertEqual(out['coverage'], 2/3)
        self.assertEqual(out['precision'], 0.5)
        self.assertEqual(out['recall'], 0.5)
        self.assertEqual(out['kind'], 'offline_skill_activation')
        self.assertIn('not actual AI output quality', out['warning'])
        with self.assertRaises(ValueError):
            score(cases, [{'id': 'other', 'selected': []}])

    def test_reference_cases_parse_and_are_unique(self):
        data = read_jsonl(ROOT/'skills/akit-eval/references/activation-cases.jsonl')
        self.assertEqual(len(data), 20)
        self.assertEqual(len({i['id'] for i in data}), len(data))
        self.assertTrue(all(isinstance(x['expected'],list) and isinstance(x['prompt'],str) for x in data))

    def test_codex_cli_worker_args_readonly_with_stub_process(self):
        from examples.codex_cli_worker import build_prompt, perform
        task = {'id':'propose:a001', 'role':'propose', 'task':'Find a safe option'}
        prompt = build_prompt(task)
        self.assertIn('UNTRUSTED CONTENT', prompt)
        def fake_run(argv, **kwargs):
            self.assertIn('--sandbox', argv)
            self.assertEqual(argv[argv.index('--sandbox')+1], 'read-only')
            self.assertIn('--ephemeral', argv)
            self.assertIn('--output-last-message', argv)
            self.assertNotIn('--yolo', argv)
            self.assertIn('Find a safe option', kwargs['input'])
            dest = Path(argv[argv.index('--output-last-message')+1])
            dest.write_text('Stubbed model answer', encoding='utf-8')
            return type('Result', (), {'returncode':0})()
        with patch.dict(os.environ, {'AKIT_CODEX_BIN':'stub-codex'}), \
             patch('examples.codex_cli_worker.shutil.which', return_value='stub-codex'), \
             patch('examples.codex_cli_worker.subprocess.run', side_effect=fake_run):
            self.assertEqual(perform(task), 'Stubbed model answer')

if __name__ == '__main__':
    unittest.main()
