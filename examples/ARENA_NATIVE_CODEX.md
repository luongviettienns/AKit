# Codex: native AKit Arena orchestration (manual agent-led bridge)

Codex supports project agents under `.codex/agents/*.toml`, and parent-driven subagent workflows. `--with-agents` installs `akit-scout`, `akit-critic`, `akit-judge`.

1. Start `arena init` + `arena tasks` (2–4 candidates). Fix the exact task and rubric.
2. Tell Codex: "Delegate each task from `.akit/runs/<id>/tasks.json` to a separate subagent; use AKit custom critic/judge roles where applicable, keep all read-only, limit concurrency and collect text *per task ID*. Wait for all before advancing. Never modify source."
3. Save responses as UTF-8 and `arena submit` per task; use `arena advance` for next phase. On judge phase, output strict JSON.
4. Export the winner and verify against tests and real requirements. Subagent instructions are not a sandbox; Codex workers inherit parent permissions.

For automated sequential Codex invocations rather than native subagents, `codex_cli_worker.py` is the separately opt-in bridge: `--worker "py .akit/runtime/examples/codex_cli_worker.py"`. It starts `codex exec --sandbox read-only --ephemeral` once for each Arena task, and **can consume quota**. The CLI protocol was structurally tested with a stub, not a live account.
