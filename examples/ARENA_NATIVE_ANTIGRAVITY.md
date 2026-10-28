# Antigravity Native Debate & Arena Orchestration Recipe (`AKit v0.4.0`)

With `--with-agents`, AKit installs 6 specialist subagents into `.agents/agents/`: `akit-scout`, `akit-critic`, `akit-judge`, `akit-debater`, `akit-architect`, and `akit-security`.

## Quick Prompt for Lightweight Triad Debate (`akit-debate` — 3 Calls)

> Use `akit-debate` in read-only mode. Run `python .akit/runtime/akit_cli.py arena init --session .akit/runs/d1 --mode debate --task "<YOUR QUESTION>"` and export tasks. Delegate `debate:propose` to `akit-debater`, `debate:challenge` to `akit-critic`, and `debate:synthesize` to `akit-judge` using `invoke_subagent`. Submit each real response via `arena submit`, advance after each step, and export `.akit/runs/d1/report.md`. Do not edit source code during debate.

## Quick Prompt for 4-Agent Tournament (`akit-arena` — 19 Calls)

> Use `akit-arena` in read-only mode. Initialize a 4-candidate tournament (`--mode tournament`). Read each phase's `tasks.json`, delegate `propose`/`revise` to `akit-debater`, `attack` to `akit-critic`, and `judge` (strict JSON) to `akit-judge` via `invoke_subagent`. Submit real answers and advance through `propose -> attack -> revise -> judge` until `done`, then export `.akit/runs/<id>/report.md`.
