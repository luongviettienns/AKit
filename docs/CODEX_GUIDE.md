# Codex-specific AKit installation and use

**Skills**: Codex discovers standard Agent Skills under `<project>/.agents/skills`. **Rules**: project `AGENTS.md` is recognized as optional persistent guidance. AKit does **not** overwrite or generate `AGENTS.md` automatically.

```powershell
# From AKit directory, prior to opening Codex on the target project:
py -m akit.install --target codex --profile core --with-guidance --project "D:\MyApp"

# Within D:\MyApp, verify installed skills + runtime:
py .akit/runtime/akit_cli.py doctor --project .
```

To add three Codex custom agent role definitions, use `--with-agents`. These are installed at `.codex/agents/*.toml` and inherit the parent permission/sandbox. The separate `examples/codex_cli_worker.py` runs fresh `codex exec` calls when explicitly selected. These are two different delegation methods.

For a fullstack NestJS + PostgreSQL project, choose `--profile backend` and optionally `--only akit-router akit-plan akit-implement akit-debug akit-git akit-test akit-review akit-security akit-arena akit-postgres akit-contract`.

## Working agreement

- The parent Codex agent should discover `akit-router` and load **only the skills needed** for the task. Use `AGENTS.md` for stable repository rules, not verbose duplicates of skills.
- For Arena, use the shared file-backed JSON task protocol; delegate using whatever capabilities your Codex version supports, or manually pass tasks to independent sessions. This package installs opt-in Codex TOML agent profiles if you pass `--with-agents`, but it **does not automatically connect them to the Arena state machine**.
- For real automated Arena, explicitly configure an allowed external worker via `--worker-argv` and review privacy, cost and permissions. No API accounts are added by AKit.
- Run checks and report observed evidence, and note when a subagent/tool was unavailable. Avoid overstating confidence from model-only evaluation.

Prompt example:

> Use `akit-router` then `akit-codebase` as needed. Implement the smallest safe fix, add a regression test first, perform `akit-review`, and tell me exact test commands and results. Do not push, change schema, or deploy without my approval.

Codex references: https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex and https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
