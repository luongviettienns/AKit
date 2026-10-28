# Sources, Knowledge Integration & Attribution (`AKit v0.4.0`)

AKit v0.4.0 is an independent, original engineering kit designed for **Google Antigravity** and **OpenAI Codex**. It synthesizes proven architectural, testing, security, UI/UX, database, and multi-agent patterns from **24 public GitHub repositories** across **7 functional domains**.

No proprietary upstream code or verbatim `SKILL.md` files are copied into this distribution. License observations below are taken from upstream READMEs and are not legal advice; always verify upstream licenses before importing external code, scripts, or brand assets.

---

## 1. Functional Group Mapping (24 Reference Repositories -> 30 AKit Skills)

| Functional Group | Count | Repositories Integrated | Target AKit v0.4.0 Skills & Components |
| :--- | :--- | :--- | :--- |
| **1. Multi-Agent & Orchestration** | **4** | `Jakeschincariol/arena-skill`, `affaan-m/everything-claude-code`, `wshobson/agents`, `JayZeeDesign/claude-code-vault` | `akit-arena`, `akit-debate` *(New)*, `akit-router`, `akit-context`, 6 Specialist Subagents |
| **2. Agent Engineering & Best Practices** | **6** | `shanraisshan/claude-code-best-practice`, `sickn33/agentic-awesome-skills`, `rmyndharis/antigravity-skills`, `obra/superpowers`, `github/awesome-copilot`, `anthropics/skills` | `akit-implement`, `akit-debug`, `akit-git`, `akit-skillforge`, `akit-eval`, `akit-scout`, Hooks/Rules templates |
| **3. UI/UX & Frontend** | **3** | `VoltAgent/awesome-design-md`, `vercel-labs/agent-skills`, `nextlevelbuilder/ui-ux-pro-max-skill` | `akit-design`, `akit-react`, `akit-performance` |
| **4. Codebase, Documentation & Prompt** | **4** | `upstash/context7`, `oraios/serena`, `Egonex-AI/Understand-Anything`, `dair-ai/Prompt-Engineering-Guide` | `akit-codebase`, `akit-docs`, `akit-prompt`, `akit-prior-art` |
| **5. Security, Testing & Quality** | **4** | `trailofbits/skills`, `getsentry/skills`, `microsoft/playwright-cli`, `semgrep/skills` | `akit-security`, `akit-review`, `akit-simplify` *(New)*, `akit-browser-qa`, `akit-test` |
| **6. Database & Backend** | **2** | `supabase/agent-skills`, `microsoft/postgres-skills` | `akit-postgres`, `akit-data`, `akit-contract`, `akit-architecture`, `akit-observability` |
| **7. Vibe Coding & Product Development** | **1** | `datawhalechina/easy-vibe` | `akit-requirements`, `akit-plan`, `akit-deliver` |

---

## 2. Detailed Attribution of the 24 Reference Repositories

| # | Repository | Core Knowledge Integrated into AKit v0.4.0 | License / Caution Note |
| :--- | :--- | :--- | :--- |
| **1** | [Jakeschincariol/arena-skill](https://github.com/Jakeschincariol/arena-skill) | Single-elimination tournament (`propose -> attack -> revise -> judge`), 100-point rubric, fatal-flaw override (`akit-arena`) | MIT (README; original AKit Python runner) |
| **2** | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | Standardized `DESIGN.md` design-token specification, semantic surface hierarchy, typography/grid rules (`akit-design`) | Curated assets; verify individual brand/file licenses |
| **3** | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | Context discipline, subagent role separation, lifecycle hooks (`hooks.example.json`), atomic workflow gates | Reference guidance only; verify individual file licenses |
| **4** | [upstash/context7](https://github.com/upstash/context7) | Version-pinned official documentation lookup via optional Context7 MCP & lockfile grounding (`akit-docs`) | MIT repo; optional external MCP (not bundled) |
| **5** | [oraios/serena](https://github.com/oraios/serena) | Semantic symbol-level navigation (`find_symbol`, call hierarchy) over full-file dumps (`akit-codebase`, `akit-scout`) | GPL-3.0-or-later; optional external MCP (not bundled) |
| **6** | [datawhalechina/easy-vibe](https://github.com/datawhalechina/easy-vibe) | Structured Vibe Coding: Idea -> BA/PRD (`akit-requirements`) -> Vertical Slices (`akit-plan`) -> Production Handoff (`akit-deliver`) | CC BY-NC-SA 4.0; original AKit playbooks only |
| **7** | [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | Layered codebase knowledge graphs, blast-radius dependency analysis, and guided subsystem tours (`akit-codebase`) | MIT repo; not bundled |
| **8** | [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | Selective domain skill loading instead of mass catalog installation (`akit-router`, `akit-scout`) | MIT index; verify target third-party skill licenses |
| **9** | [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) | Google Antigravity `.agents/skills/` packaging conventions and specialist role taxonomy (`akit-scout`, `akit-skillforge`) | Check individual skill provenance & license |
| **10** | [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | Positive output contracts, Chain-of-Verification (CoVe), grounded RAG citations, untrusted data delimiters (`akit-prompt`) | Reference guide only; no textbook contents copied |
| **11** | [obra/superpowers](https://github.com/obra/superpowers) | Hard-Gate Brainstorming, RED-GREEN-REFACTOR TDD, 4-Phase Systematic Debugging, Git Worktree Isolation, SDO Skill Authoring, Verification-Before-Completion | MIT; independently authored AKit integration |
| **12** | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | Session memory compaction, verified facts vs. ruled-out dead ends, token budget optimization (`akit-context`, `akit-router`) | Reference patterns; no copied hooks or DB |
| **13** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Eliminating async request waterfalls (`Promise.all`/Suspense), Server/Client component boundaries, anti-`useEffect` derivation, Core Web Vitals (`akit-react`, `akit-performance`) | Independently authored procedures |
| **14** | [trailofbits/skills](https://github.com/trailofbits/skills) | Differential security review, trust-boundary invariant tracing, BOLA/IDOR & race hunting, zero false-positive padding (`akit-security`) | CC BY-SA 4.0; concepts only, no material copied |
| **15** | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Separation of Always-On Rules (`GEMINI.md`/`AGENTS.md`) vs. On-Demand Skills vs. Custom Agents (`akit-scout`, `akit-skillforge`) | Reference taxonomy only |
| **16** | [wshobson/agents](https://github.com/wshobson/agents) | Multi-agent specialist personas (`akit-scout`, `akit-critic`, `akit-judge`, `akit-debater`, `akit-architect`, `akit-security`) and parallel file-ownership contracts (`akit-git`) | Original AKit agent definitions |
| **17** | [anthropics/skills](https://github.com/anthropics/skills) | Progressive Disclosure skill structure, Skill Creator A/B evaluation (`akit-skillforge`, `akit-eval`), intentional frontend aesthetics (`akit-design`), Playwright webapp testing | Per-skill licenses vary; no upstream scripts bundled |
| **18** | [getsentry/skills](https://github.com/getsentry/skills) | Zero-behavior-change code simplification (`akit-simplify`), cognitive complexity reduction, two-stage PR diff triage (`akit-review`), and structured error telemetry (`akit-observability`) | Reference patterns; independently written |
| **19** | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Industry-aligned aesthetic palettes, typography scales, 6-state UX completeness matrix, mobile ergonomics (`akit-design`, `akit-react`) | Reference heuristics only |
| **20** | [supabase/agent-skills](https://github.com/supabase/agent-skills) | PostgreSQL Row Level Security (RLS) `(SELECT auth.uid())` `initPlan` caching, FK indexing, lock-safe DDL migrations (`akit-postgres`, `akit-data`) | Original AKit database playbook |
| **21** | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Resilient role/label locators, web-first auto-retrying assertions, viewport overflow & console error gating (`akit-browser-qa`) | Does not bundle or auto-install Playwright |
| **22** | [semgrep/skills](https://github.com/semgrep/skills) | High-signal sink scanning, false-positive reachability triage, and custom YAML guardrail rule authoring (`akit-security`) | Does not bundle or auto-install Semgrep |
| **23** | [microsoft/postgres-skills](https://github.com/microsoft/postgres-skills) | PostgreSQL `B-Tree`/`GIN`/`BRIN`/partial/covering index selection, `EXPLAIN (ANALYZE, BUFFERS)` interpretation, deadlock prevention (`akit-postgres`) | Reference patterns only |
| **24** | [JayZeeDesign/claude-code-vault](https://github.com/JayZeeDesign/claude-code-vault) | Lightweight Triad Debate (`Proposer -> Challenger / Devil's Advocate -> Synthesizer`) in 3 calls (`akit-debate` and `arena init --mode debate`) | Original AKit implementation |
| **25** | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Andrej Karpathy's 4 Laws against LLM coding slop (`Think Before Coding`, `Simplicity First`, `Surgical Changes`, `Goal-Driven Execution`) integrated into `akit-eval --mode karpathy`, `akit-implement`, `akit-simplify`, and auto-installed `.agents/rules/akit.md` | MIT; original AKit Python evaluator & rules |

---

## 3. Prior-Art Reference Repositories Listed in `akit-prior-art` (Pointers Only)

| Repository | Why Listed | Reuse Caution |
| :--- | :--- | :--- |
| [realworld-apps/realworld](https://github.com/realworld-apps/realworld) | 100+ frontend/backend implementations of the same API/UI spec | Reference comparison only |
| [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | FastAPI + React + PostgreSQL + Docker + Playwright CI blueprint | Check license before adapting |
| [brocoders/nestjs-boilerplate](https://github.com/brocoders/nestjs-boilerplate) | NestJS modular auth, TypeORM, mailer, i18n, Docker, E2E layout | Verify canonical repo & license |
| [better-auth/better-auth](https://github.com/better-auth/better-auth) | TypeScript auth, OAuth rotation, 2FA, and multi-tenant organization schemas | MIT (README); prefer as dependency |
| [expo/skills](https://github.com/expo/skills) | Official Expo agent skills for React Native / mobile | Optional external reference via `akit-scout` |
| [full-stack-skills/devops-skills](https://github.com/full-stack-skills/devops-skills) | CI/CD, Docker, Terraform deployment skill ideas | Inspect thoroughly before trusting |
| [prapanch/agent-coda](https://github.com/prapanch/agent-coda) | DevOps pipeline and deployment-safety craft patterns | Inspect thoroughly before trusting |
