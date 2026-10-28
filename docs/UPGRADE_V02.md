# AKit v0.2 migration and limitations

## What changed

- 12 new detailed skills and 9 reference templates (27 total skills).
- Antigravity read-only custom agent profiles (optional, **not** a verified automatic native adapter).
- Local runtime installed into `<project>/.akit/runtime`, with working `arena`, `doctor`, `eval`, `checks` CLI commands.
- Installer hash manifest and cautious `--upgrade` behavior. Modified managed skills are preserved. No automatic changes to `AGENTS.md`.
- Cross-platform `--worker-argv` JSON mode for Windows paths; default worker-call budget and no shell.
- Evidence recorder `checks`, optional eval activation, more quality gates.

## Installing fresh

```powershell
py -m akit.install --target antigravity --profile core --with-agents --project "D:\MyApp" --dry-run
py -m akit.install --target antigravity --profile core --with-agents --project "D:\MyApp"
py "D:\MyApp\.akit\runtime\akit_cli.py" doctor --project "D:\MyApp"
```

For Codex change `--target codex`. `--with-agents` optionally installs supported `.codex/agents/*.toml` profiles. `--profile full` installs all 27 skills; not recommended as a default because metadata overhead and ambiguous triggers grow.

## Updating a v0.2 managed install

```powershell
py -m akit.install --target antigravity --profile core --project "D:\MyApp" --upgrade --dry-run
py -m akit.install --target antigravity --profile core --project "D:\MyApp" --upgrade
```

Only unchanged managed skill directories are replaced; replaced versions are backed up under `.akit/backups/` and original user edits remain untouched. If you installed v0.1, that version had no hash manifest, so existing directories will be skipped rather than overwritten. Back up the old AKit skills and decide which to replace explicitly before using v0.2. The installer does not uninstall or clean previous files.

## Unverified areas

- The optional Antigravity roles may require workspace reload and runtime permissions changes; **not live-tested in Antigravity**.
- The Codex UI skill activation and actual AI answer quality have **not** been benchmarked with a live Codex run.
- Native Codex subagent and full automated Antigravity Arena delegation remain **manual/operator-mediated** rather than an independently working API bridge.
- Context7, Serena, Playwright, Semgrep and other tools are **not bundled**. Check licenses, versions and network boundaries before enabling.
