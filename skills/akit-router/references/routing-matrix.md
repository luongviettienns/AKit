# AKit Routing Matrix & Complexity Classification (`akit-router`)

Use this reference to map incoming engineering requests to the smallest effective AKit skill set and specialist subagent.

---

## 1. Complexity Sizing Rubric (`S` / `M` / `L` / `Architectural`)

| Size | Characteristics | Approval Gate (`obra/superpowers`) | Max Active Skills | Subagent Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **S (Bounded)** | 1–2 existing files, clear bug or small flag/endpoint, flow already exists in repo | Short 2–3 sentence design in chat $\rightarrow$ confirm | 2–3 | None (Direct execution) |
| **M (Feature Slice)** | 3–8 files across controller/service/UI, new DTO or DB column, clear domain | Concise component/contract design $\rightarrow$ confirm | 3–4 | Optional `akit-scout` (explore) + `akit-critic` (review) |
| **L (Cross-Cutting)** | New subsystem, unfamiliar capability, auth/payment/multi-tenant, >8 files | Full sectioned design spec + `akit-plan` $\rightarrow$ confirm | 4–5 (phased) | `akit-scout` + `akit-debater` (`akit-debate`) + `akit-security` |
| **Architectural** | Greenfield project, major database/framework migration, 4+ competing designs | Full spec + `akit-arena` / `akit-debate` + ADR | Phased per milestone | Full 6-subagent orchestration |

---

## 2. Task-to-Skill Routing Table

| User Request Scenario | Primary Skills (Load First) | Verification & Quality Skills (Load Before Completion) | Recommended Subagent |
| :--- | :--- | :--- | :--- |
| **Unfamiliar feature / new technical capability** | `akit-prior-art` $\rightarrow$ `akit-plan` | `akit-implement` $\rightarrow$ `akit-test` | `akit-scout` |
| **Reproducible bug, test failure, or regression** | `akit-debug` $\rightarrow$ `akit-codebase` | `akit-implement` $\rightarrow$ `akit-test` | `akit-scout` |
| **Compare 2–3 technical options or libraries** | `akit-debate` $\rightarrow$ `akit-architecture` | `akit-docs` | `akit-debater`, `akit-judge` |
| **Major architecture bake-off (4+ strategies)** | `akit-arena` $\rightarrow$ `akit-architecture` | `akit-security` $\rightarrow$ `akit-plan` | `akit-debater`, `akit-critic`, `akit-judge` |
| **New UI page, dashboard, or redesign** | `akit-design` $\rightarrow$ `akit-react` | `akit-browser-qa` $\rightarrow$ `akit-performance` | `akit-critic` |
| **Backend API endpoint + Frontend integration** | `akit-contract` $\rightarrow$ `akit-implement` | `akit-simplify` $\rightarrow$ `akit-test` | `akit-architect` |
| **PostgreSQL schema, slow query, or RLS policy** | `akit-postgres` $\rightarrow$ `akit-data` | `akit-performance` $\rightarrow$ `akit-security` | `akit-architect`, `akit-security` |
| **Auth, RBAC, secrets, webhooks, or SAST triage** | `akit-security` $\rightarrow$ `akit-implement` | `akit-review` $\rightarrow$ `akit-test` | `akit-security` |
| **Post-feature cleanup / over-engineered PR** | `akit-simplify` $\rightarrow$ `akit-review` | `akit-test` | `akit-critic` |
| **Unfamiliar large codebase onboarding** | `akit-codebase` $\rightarrow$ `akit-context` | `akit-docs` | `akit-scout` |
| **Idea-to-MVP product build (Vibe Coding)** | `akit-requirements` $\rightarrow$ `akit-design` $\rightarrow$ `akit-plan` | `akit-implement` $\rightarrow$ `akit-deliver` | `akit-architect` |
| **Create or upgrade an Agent Skill** | `akit-skillforge` $\rightarrow$ `akit-prompt` | `akit-eval` | `akit-critic` |
| **Multi-agent parallel branch execution** | `akit-git` $\rightarrow$ `akit-context` | `akit-review` $\rightarrow$ `akit-test` | `akit-scout` |

---

## 3. Token & Context Budget Discipline (`affaan-m/everything-claude-code`)
1. **Progressive Disclosure:** Load `SKILL.md` first; read `references/<file>` only when executing the specific step that needs the template or deep checklist.
2. **Delegate Heavy Reads:** If exploring >10 files to locate a symbol or dependency chain, delegate to `akit-scout` via `invoke_subagent` so raw file dumps stay out of the main agent's context window.
3. **Checkpoint Before Compaction:** On long sessions, invoke `akit-context` to write verified state to `.akit/project-context.md` before running `/compact`.
