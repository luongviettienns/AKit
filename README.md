# AKit v0.4.0 — Google Antigravity + OpenAI Codex Engineering Kit

A comprehensive, original **Agent Skills** toolkit for high-reliability AI-assisted software engineering in **Google Antigravity** and **OpenAI Codex**:
- **30 Progressively Loaded Skills (`SKILL.md` + `references/`):** Every skill contains an 85–150 line operational playbook (SDO frontmatter, Antigravity native tool mapping, step-by-step procedures, Red Flags & Rationalization Counter-Tables) paired with deep reference manuals in `references/` for **100% of skills (30/30)**.
- **6 Specialist Subagents (`.agents/agents/*.md` & `.codex/agents/*.toml`):** `akit-scout`, `akit-critic`, `akit-judge`, `akit-debater`, `akit-architect`, and `akit-security`.
- **Dual-Mode Multi-Agent Reasoning (`akit/arena.py`):**
  - **Lightweight Triad Debate (`akit-debate` / `--mode debate`):** Fast 1-round `Proposer -> Challenger (Devil's Advocate) -> Synthesizer` requiring only **3 calls** (inspired by `JayZeeDesign/claude-code-vault`).
  - **Elimination Tournament (`akit-arena` / `--mode tournament`):** Multi-round `propose -> attack -> revise -> judge` bracket with a 100-point rubric (inspired by `Jakeschincariol/arena-skill`).
- **41 Reference Repositories Integrated Across 7 Functional Domains:** Including deep `obra/superpowers` SDD, `multica-ai/andrej-karpathy-skills` 4-Laws diff evaluation (`akit-eval --mode karpathy`), `vercel-labs/agent-skills` (70 React/Next.js rules across 8 priority categories + 100+ Web Interface Guidelines), `vercel-labs/skills` (`find-skills` / `npx skills`), `anthropics/skills` (`webapp-testing`, `doc-coauthoring`, `web-artifacts-builder`), the **12-Repository Frontend Design, Anti-Slop & Creative Motion Suite** (`pbakaus/impeccable` 24 commands & 61 rules, `nutlope/hallmark` 57 criteria, `Leonxlnx/taste-skill`, `emilkowalski/skills` `scale(0)` ban & springs, `greensock/gsap-skills` `useGSAP`, `DavidHDev/react-bits`, `DavidHDev/canvas-ui` WebGL over DOM, `oso95/scroll-world` `The Seam Rule`, `google-labs-code/design.md`, `VoltAgent/awesome-design-md`, `nexu-io/open-design`, `nextlevelbuilder/ui-ux-pro-max-skill`), mandatory GitHub OSS prior-art comparison (`akit-prior-art`), and automatic `.agents/rules/akit.md` + `GEMINI.md` wiring on install. See [`docs/SOURCES.md`](docs/SOURCES.md) and [`docs/UPGRADE_V04.md`](docs/UPGRADE_V04.md).

Vietnamese quick start: [`QUICKSTART_VI.md`](QUICKSTART_VI.md). Detailed platform notes: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

---

## 1. Install in a Project

Python 3.9+ required (standard library only, zero `pip` dependencies). Run from the `AKit` directory:

```powershell
# Preview operations first (default profile = 'core' with 12 foundational skills)
python -m akit.install --target antigravity --profile core --project "D:\MyProject" --with-agents --dry-run
python -m akit.install --target antigravity --profile core --project "D:\MyProject" --with-agents --with-guidance

# Domain-specialized profiles
python -m akit.install --target antigravity --profile frontend --project "D:\MyProject" --with-agents
python -m akit.install --target antigravity --profile backend --project "D:\MyProject" --with-agents
python -m akit.install --target antigravity --profile full --project "D:\MyProject" --with-agents
```

### Installation Profiles
- **`core` (12 skills):** `akit-router`, `akit-plan`, `akit-implement`, `akit-prior-art`, `akit-debug`, `akit-git`, `akit-context`, `akit-test`, `akit-review`, `akit-simplify`, `akit-security`, `akit-eval`.
- **`frontend` (19 skills):** `core` + `akit-requirements`, `akit-design`, `akit-browser-qa`, `akit-performance`, `akit-contract`, `akit-react`, `akit-debate`.
- **`backend` (21 skills):** `core` + `akit-requirements`, `akit-architecture`, `akit-docs`, `akit-data`, `akit-contract`, `akit-observability`, `akit-performance`, `akit-postgres`, `akit-debate`.
- **`quality` (8 skills):** `akit-router`, `akit-debug`, `akit-test`, `akit-review`, `akit-simplify`, `akit-security`, `akit-eval`, `akit-browser-qa`.
- **`full` (30 skills):** All 30 skills.
- **`--with-agents`:** Installs all **6 specialist subagents** (`.agents/agents/*.md` for Antigravity; `.codex/agents/*.toml` for Codex).
- **`--upgrade`:** Hash-verified managed updates; backs up unmodified managed files to `.akit/backups/` and skips locally modified files without overwriting.

---

## 2. The 7 Functional Domains & 41 Integrated Repositories

| Functional Domain | Repos | Integrated Skills (`skills/akit-*/`) | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **1. Multi-Agent & Orchestration** | 4 | `akit-debate` *(New)*, `akit-arena`, `akit-router`, `akit-context` | 3-step Triad Debate (`claude-code-vault`), 100-pt Tournament (`arena-skill`), Minimal-context routing (`wshobson/agents`), Session memory compaction (`everything-claude-code`) |
| **2. Agent Engineering, Discovery & Discipline** | 13 | `akit-implement`, `akit-debug`, `akit-git`, `akit-skillforge`, `akit-eval`, `akit-scout` | TDD Red-Green-Refactor, 4-Phase Debugging, Worktree Isolation (`obra/superpowers`), Karpathy 4 Laws (`andrej-karpathy-skills`), `find-skills` CLI (`vercel-labs/skills`), Awesome Catalogs (`ComposioHQ`, `travisvn`, `BehiSecc`, `kaichen`, `helloianneo`) |
| **3. UI/UX, Anti-Slop Design & Creative Motion** | 13 | `akit-design`, `akit-react`, `akit-performance` | Dual `DESIGN.md` (`google-labs-code/design.md` + `awesome-design-md`), Impeccable 24 commands & 61 rules (`pbakaus/impeccable`), Hallmark 57 gates (`nutlope/hallmark`), Taste Skill (`Leonxlnx/taste-skill`), Emil Kowalski Motion (`emilkowalski/skills`), GSAP (`greensock/gsap-skills`), React Bits (`DavidHDev/react-bits`), WebGL Canvas UI (`DavidHDev/canvas-ui`), 3D Scroll World (`oso95/scroll-world`), Open Design (`nexu-io/open-design`), 70 React rules + 100+ UI guidelines (`vercel-labs/agent-skills`) |
| **4. Codebase, Docs & Prompt** | 4 | `akit-codebase`, `akit-docs`, `akit-prompt`, `akit-prior-art` | Symbol navigation (`oraios/serena`), Knowledge graphs (`Understand-Anything`), Version-pinned docs (`upstash/context7`), Grounded RAG & CoVe prompting (`Prompt-Engineering-Guide`), GitHub OSS Prior Art |
| **5. Security, Testing & Quality** | 4 | `akit-simplify` *(New)*, `akit-review`, `akit-security`, `akit-browser-qa`, `akit-test` | Zero-behavior-change simplification & two-stage review (`getsentry/skills`), Differential security review (`trailofbits/skills`), Semgrep SAST triage (`semgrep/skills`), Real-browser Playwright E2E (`playwright-cli`) |
| **6. Database & Backend** | 2 | `akit-postgres`, `akit-data`, `akit-contract`, `akit-architecture`, `akit-observability` | PostgreSQL indexing (`B-Tree`/`GIN`/`BRIN`/partial/covering), `EXPLAIN (ANALYZE, BUFFERS)`, RLS `(SELECT auth.uid())` `initPlan` caching (`supabase/agent-skills`, `microsoft/postgres-skills`), Expand-Migrate-Contract |
| **7. Vibe Coding & Product Dev** | 1 | `akit-requirements`, `akit-plan`, `akit-deliver` | Idea-to-PRD (`Given/When/Then`), Bite-sized Vertical Slices, Zero-downtime deployment & rollback handoff (`datawhalechina/easy-vibe`) |

---

## 3. Running Installed Runtime Tools (`.akit/runtime/akit_cli.py`)

```powershell
# 1. Verify installation integrity and skill reference links
python .akit/runtime/akit_cli.py doctor --project .

# 2. Run a fast 3-call Lightweight Triad Debate (akit-debate)
python .akit/runtime/akit_cli.py arena init --session .akit/runs/d1 --mode debate --task "Compare SSE vs WebSockets for live order status"
python .akit/runtime/akit_cli.py arena tasks --session .akit/runs/d1 --out .akit/runs/d1/tasks.json

# 3. Or run a 4-candidate Elimination Tournament (akit-arena)
python .akit/runtime/akit_cli.py arena init --session .akit/runs/t1 --agents 4 --mode tournament --task "Design NestJS multi-tenant RBAC"
```

---

## 4. Verification & Testing

```powershell
python -m unittest discover -s tests -v
python -m akit.eval --cases skills/akit-eval/references/activation-cases.jsonl --observations observations.jsonl
```

MIT License covers original AKit code and instructions (`LICENSE`). See [`docs/SOURCES.md`](docs/SOURCES.md) for full attribution.
