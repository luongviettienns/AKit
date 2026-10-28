# Native Antigravity Debate & Arena Workflow (`AKit v0.4.0`)

**Platform Support:** Google Antigravity natively discovers skills in `.agents/skills/<name>/SKILL.md`, custom subagents in `.agents/agents/<name>.md`, and delegates work via the `invoke_subagent` tool.

When installed with `--with-agents`, AKit v0.4.0 provisions **6 read-only specialist subagents** under `.agents/agents/`:
- `akit-scout.md` — Semantic symbol & codebase explorer (`oraios/serena`, `Understand-Anything`)
- `akit-critic.md` — Two-stage adversarial code & design reviewer (`getsentry/skills`, `obra/superpowers`)
- `akit-judge.md` — Impartial 100-point rubric judge & debate synthesizer (`arena-skill`, `claude-code-vault`)
- `akit-debater.md` — Pragmatic Proposer & Devil's Advocate for fast Triad Debates (`claude-code-vault`)
- `akit-architect.md` — Module boundary, API contract & PostgreSQL architect (`wshobson/agents`, `supabase`)
- `akit-security.md` — Differential security & SAST auditor (`trailofbits/skills`, `semgrep/skills`)

---

## Mode 1: Lightweight Triad Debate (`akit-debate` — Recommended for 2–3 Options)

Requires **only 3 subagent calls** (`propose -> challenge -> synthesize`):

```powershell
python .akit/runtime/akit_cli.py arena init --session .akit/runs/debate-1 --mode debate --task "Compare SSE vs WebSockets for live order tracking in NestJS"
python .akit/runtime/akit_cli.py arena tasks --session .akit/runs/debate-1 --out .akit/runs/debate-1/tasks.json
```

1. **Step 1 (`debate:propose`):** Parent agent reads `tasks.json` and delegates `debate:propose` to `akit-debater` via `invoke_subagent`, saves the response to `.akit/runs/debate-1/propose.md`, and runs `arena submit` + `arena advance`.
2. **Step 2 (`debate:challenge`):** Parent fetches the next task and delegates `debate:challenge` to `akit-critic` (or `akit-debater` in Devil's Advocate persona), submits, and advances.
3. **Step 3 (`debate:synthesize`):** Parent delegates `debate:synthesize` to `akit-judge`, submits, advances to `done`, and exports `.akit/runs/debate-1/report.md` via `arena export`.

---

## Mode 2: Full Multi-Agent Tournament (`akit-arena` — For 4 to 8+ Strategies)

```powershell
python .akit/runtime/akit_cli.py arena init --session .akit/runs/tourney-1 --agents 4 --mode tournament --task "Design multi-tenant RBAC and RLS for NestJS + PostgreSQL"
python .akit/runtime/akit_cli.py arena tasks --session .akit/runs/tourney-1 --out .akit/runs/tourney-1/tasks.json
```

Advance through `propose` (`akit-architect` / `akit-debater`) $\rightarrow$ `attack` (`akit-critic`) $\rightarrow$ `revise` (`akit-debater`) $\rightarrow$ `judge` (`akit-judge` returning strict 100-point rubric JSON) until a single winner emerges, then run `arena export`.
