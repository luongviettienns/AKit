# AKit v0.4.0 Upgrade Guide — Deep Antigravity Edition

## What Changed in v0.4.0

1. **Expanded Catalog to 30 Deep Skills (100% with `references/`):**
   - Added **`akit-debate`** (inspired by `#24 JayZeeDesign/claude-code-vault`): fast 1-round **Triad Debate** (`Proposer -> Challenger / Devil's Advocate -> Synthesizer`) requiring only 3 subagent/worker calls.
   - Added **`akit-simplify`** (inspired by `#18 getsentry/skills`): zero-behavior-change cognitive complexity reduction, guard-clause flattening, and premature-abstraction removal after tests turn green.
   - Upgraded all **30 `SKILL.md` files** from brief 18–35 line stubs to **85–150 line actionable runbooks** (>3,000 chars each) featuring:
     - Skill Discovery Optimization (SDO) frontmatter (`Use when...`).
     - **Antigravity Native Tool Mapping** (`invoke_subagent`, `read_file`, `edit_file`, `run_command`, `search_marketplace`, `ask_question`, slash commands).
     - Step-by-step domain playbooks integrating all **24 reference repositories** across **7 functional groups**.
     - **Red Flags & Rationalization Counter-Tables** (`obra/superpowers`).
     - Dedicated deep reference manuals and templates in `references/` for **100% of skills (30/30)**.
2. **6 Specialist Subagents (`.agents/agents/*.md` & `.codex/agents/*.toml`):**
   - Upgraded `akit-scout`, `akit-critic`, and `akit-judge`.
   - Added `akit-debater`, `akit-architect`, and `akit-security`.
3. **Dual-Mode Arena CLI (`--mode tournament` & `--mode debate`):**
   - `python .akit/runtime/akit_cli.py arena init --session .akit/runs/d1 --mode debate --task "..."` runs the 3-step Triad Debate (`debate:propose`, `debate:challenge`, `debate:synthesize`).
4. **Enhanced `akit.doctor` & 20-Case Activation Benchmark:**
   - `akit.doctor` now verifies that every `references/<file>` link inside every installed `SKILL.md` resolves to a real file on disk.
   - Expanded `evals/activation_cases.jsonl` and `skills/akit-eval/references/activation-cases.jsonl` from 15 to **20 test cases**.
5. **New Antigravity Configuration Examples (`examples/`):**
   - Added `examples/GEMINI.snippet.md`, `examples/mcp_config.example.json` (Context7, Serena, Playwright, Postgres), and `examples/hooks.example.json`.

---

## Upgrading an Existing Managed Project

```powershell
# Preview managed upgrade first
python -m akit.install --target antigravity --profile core --project "D:\MyProject" --with-agents --upgrade --dry-run

# Apply upgrade (backs up unchanged prior files to .akit/backups/ and skips locally modified files)
python -m akit.install --target antigravity --profile core --project "D:\MyProject" --with-agents --upgrade
python "D:\MyProject\.akit\runtime\akit_cli.py" doctor --project "D:\MyProject"
```
