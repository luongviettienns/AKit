# Arena worker setup: manual, local or API

The AKit Arena core is independent from Claude, Antigravity, Gemini, Codex, Ollama, ChatGPT, etc. An external worker is a separate process that consumes one isolated task in JSON and responds with JSON `{"text":"..."}`. Every worker call is a separate LLM inference request if you use `openai_compatible_worker.py`. This is multi-candidate debate, not a guarantee of different base model identities or perfect independence.

## Mode A — no API, fully manual

```bash
python -m akit.arena init --session .akit/runs/demo --agents 4 --task "Choose database migration strategy"
python -m akit.arena tasks --session .akit/runs/demo --out .akit/runs/demo/tasks.json
# For each task, provide the JSON to an AI agent and save its answer in a UTF-8 file.
python -m akit.arena submit --session .akit/runs/demo --id propose:a001 --file .akit/runs/demo/answer-a001.txt
# Repeat for every task returned by `tasks`, then:
python -m akit.arena advance --session .akit/runs/demo
python -m akit.arena tasks --session .akit/runs/demo
# Continue attack, revise, judge, and subsequent rounds.
```

The engine enforces that judges use numeric point ceilings and justify claimed fatal flaws. It cannot externally verify evidence.

## Mode B — Ollama local (if installed and model downloaded)

**PowerShell** (example model name only; use a model actually installed on your machine):

```powershell
$env:AKIT_API_BASE_URL="http://127.0.0.1:11434/v1"
$env:AKIT_MODEL="qwen2.5-coder:7b"
py -m akit.arena init --session .akit/runs/demo-local --agents 4 --task "Compare 4 designs for a NestJS module"
py -m akit.arena run --session .akit/runs/demo-local --worker "py examples/openai_compatible_worker.py" --timeout 180 --max-workers 1
py -m akit.arena export --session .akit/runs/demo-local --out .akit/runs/demo-local/report.md
```

This calls your *local* Ollama endpoint. A small model may return judge JSON incorrectly, in which case the run halts with a validation error and preserves the session. It may be necessary to manually fix/re-submit failed judge outputs or use a model with better structured output capabilities. No unlimited retries occur.

## Mode C — trusted hosted OpenAI-compatible endpoint

Set `AKIT_API_BASE_URL`, `AKIT_MODEL`, and `AKIT_API_KEY` in your shell environment. HTTPS is required for nonlocal endpoints by default. **Do not hardcode keys into project files.** The full prompt and all debate answers are sent to that provider; redact sensitive material first and be aware of token costs.

## Mode D — native sub-agent adapters

Adapt your coding agent's own sub-agent API to the same JSON request/response protocol. This is integration work and is not included as a preconfigured adapter. Never advertise that a native integration works until verified with the installed agent's actual API.

## Token/cost budgeting

For N contenders, there are N proposal calls, and each match uses 2 attacks + 2 revisions + 1 judge call. For 4 agents: 4 + 3*5 = **19** reasoning requests; for 8 agents: 8 + 7*5 = **43**. This excludes failed calls or extra verification. Byes have no matching calls. For 32 agents: 32 + 31*5 = 187 calls. Start with 2–4 agents unless the decision is truly costly.

## Failure and security

- A worker is untrusted executable code. Do not run a worker downloaded from an unknown source.
- Your agent may have repo access, API credentials or network permissions; sandbox appropriately.
- API completion is not test execution. Validate the final recommendation with actual evidence.
- `run` runs the provided worker and may incur fees. It is not executed during `init` or `tasks`.
- Each agent uses the same model unless your worker selects models per candidate; strategies differ.

## Mode E — Codex CLI subprocess worker (v0.2)

An opt-in adapter `examples/codex_cli_worker.py` starts an isolated `codex exec` run per Arena task with `--sandbox read-only --ephemeral --output-last-message`. It requires authenticated Codex CLI, can consume account quota, and is **not** the internal Codex subagent API. In the installed target project, use:

```powershell
py .akit/runtime/akit_cli.py arena run --session .akit/runs/demo --worker "py .akit/runtime/examples/codex_cli_worker.py" --max-workers 1 --timeout 600 --max-calls 25
```

Optional: `AKIT_CODEX_BIN`, `AKIT_CODEX_CWD`, `AKIT_CODEX_SKIP_GIT_CHECK=1`. The last option skips Git repository validation; use only for disposable trusted cases. This worker was tested with a stub CLI, **not** a real authenticated Codex session. Never pass private code to a third-party model without authorization.

## Native subagent orchestration, no fake API claims

Use [`examples/ARENA_NATIVE_ANTIGRAVITY.md`](../examples/ARENA_NATIVE_ANTIGRAVITY.md) or [`examples/ARENA_NATIVE_CODEX.md`](../examples/ARENA_NATIVE_CODEX.md) as recipes. Neither is currently a fully automatic native API adapter. All generated task responses must be submitted and judged through the file-backed Arena protocol.
