# AKit v0.4.0 — Hướng dẫn Tiếng Việt (Chuyên sâu cho Google Antigravity + Codex)

**AKit v0.4.0** là bộ công cụ kỹ thuật phần mềm gồm **30 Agent Skills** (kèm tài liệu tham chiếu `references/` cho 100% skill), **6 Specialist Subagents**, cùng công cụ tranh biện **Lightweight Triad Debate (`akit-debate`)** và đấu loại **Tournament Arena (`akit-arena`)**, được tích hợp sâu kiến thức từ **24 GitHub Repositories** thuộc **7 nhóm chức năng**.

---

## 1. Cài đặt AKit v0.4.0 vào Google Antigravity

Mở PowerShell tại thư mục `AKit`:

```powershell
# Xem trước thao tác cài đặt (profile core = 12 skills cốt lõi + 6 subagents)
python -m akit.install --target antigravity --profile core --project "D:\DuAnCuaToi" --with-agents --dry-run
python -m akit.install --target antigravity --profile core --project "D:\DuAnCuaToi" --with-agents --with-guidance

# Cài theo chuyên ngành:
# Backend (NestJS/FastAPI + PostgreSQL + RLS + Architecture + Debate = 21 skills)
python -m akit.install --target antigravity --profile backend --project "D:\DuAnCuaToi" --with-agents

# Frontend (React/Next.js + DESIGN.md + UI/UX Pro Max + Playwright QA + Debate = 19 skills)
python -m akit.install --target antigravity --profile frontend --project "D:\DuAnCuaToi" --with-agents

# Cài toàn bộ 30 skills + 6 subagents
python -m akit.install --target antigravity --profile full --project "D:\DuAnCuaToi" --with-agents
```

Sau khi cài đặt:
- `.agents/skills/` chứa các thư mục skill (`SKILL.md` chuyên sâu + `references/*.md` cho 100% skill).
- `.agents/agents/` chứa **6 Specialist Subagents** (`akit-scout`, `akit-critic`, `akit-judge`, `akit-debater`, `akit-architect`, `akit-security`).
- **Tự động gắn Rules (`.agents/rules/akit.md` & `GEMINI.md`):** Bộ cài đặt tự động tạo `.agents/rules/akit.md` (`trigger: always_on`) và tự động cập nhật khối `<!-- AKIT:START --> ... <!-- AKIT:END -->` trong `GEMINI.md` (giữ nguyên mọi nội dung riêng của bạn), kích hoạt sẵn `akit-router`, quy tắc bắt buộc *"Đừng viết từ con số 0"* (`akit-prior-art`), 4 định luật Karpathy (`multica-ai/andrej-karpathy-skills`), và tự động hóa Slash Workflows.
- `.akit/runtime/akit_cli.py` cung cấp công cụ `doctor`, `arena` (`--mode debate` & `--mode tournament`), `eval` (`--mode activation` & `--mode karpathy`), và `checks`.
- Thư mục `examples/` cung cấp mẫu `GEMINI.snippet.md`, `mcp_config.example.json` (Context7, Serena, Playwright, Postgres) và `hooks.example.json`.

---

## 2. Bản đồ 7 Nhóm Chức năng (Tích hợp từ 24 GitHub Repositories)

1. **Multi-Agent & Orchestration (4 repos — `arena-skill`, `everything-claude-code`, `wshobson/agents`, `claude-code-vault`):**
   - `akit-debate` *(Mới)*: Phản biện nhanh 3 bước (`Proposer -> Challenger/Devil's Advocate -> Synthesizer`) chỉ tốn 3 lượt gọi subagent.
   - `akit-arena`: Đấu loại nhiều vòng (`propose -> attack -> revise -> judge`) chấm điểm theo thang 100 điểm.
   - `akit-router` & `akit-context`: Định tuyến tối ưu token, nén bộ nhớ phiên và bàn giao trạng thái.
2. **Agent Engineering & Best Practices (6 repos — `obra/superpowers`, `anthropics/skills`, `claude-code-best-practice`, `agentic-awesome-skills`, `antigravity-skills`, `awesome-copilot`):**
   - `akit-implement` (TDD Red-Green-Refactor), `akit-debug` (4-Phase Systematic Debugging), `akit-git` (Worktree Isolation & File Ownership), `akit-skillforge` (SDO Skill Authoring), `akit-eval`, `akit-scout`.
3. **UI/UX & Frontend (3 repos — `awesome-design-md`, `vercel-labs/agent-skills`, `ui-ux-pro-max-skill`):**
   - `akit-design` (Chuẩn `DESIGN.md`, bảng màu/typography chống AI-slop, ma trận 6 trạng thái UX), `akit-react` (Xử lý async waterfall, Server/Client boundary, chống lạm dụng `useEffect`), `akit-performance` (Core Web Vitals `LCP`, `INP`, `CLS`).
4. **Codebase, Documentation & Prompt (4 repos — `upstash/context7`, `oraios/serena`, `Understand-Anything`, `Prompt-Engineering-Guide`):**
   - `akit-codebase` (Điều hướng theo Symbol & Knowledge Graph), `akit-docs` (Đối chiếu đúng version trong lockfile/Context7), `akit-prompt` (5-Part Subagent Dispatch, RAG grounding, chống Prompt Injection), `akit-prior-art` (Tìm và so sánh mã nguồn mở GitHub trước khi code tính năng lạ).
5. **Security, Testing & Quality (4 repos — `trailofbits/skills`, `getsentry/skills`, `playwright-cli`, `semgrep/skills`):**
   - `akit-simplify` *(Mới)*: Rút gọn độ phức tạp nhận thức (Guard clauses, xóa abstraction thừa) giữ nguyên 100% hành vi sau khi test xanh.
   - `akit-review` (Review 2 giai đoạn: Spec Compliance -> Code Quality), `akit-security` (Differential Security Audit & Semgrep triage), `akit-browser-qa` (Playwright E2E thực tế), `akit-test`.
6. **Database & Backend (2 repos — `supabase/agent-skills`, `microsoft/postgres-skills`):**
   - `akit-postgres` (Ma trận chọn Index `B-Tree`/`GIN`/`BRIN`/Partial/Covering, đọc `EXPLAIN (ANALYZE, BUFFERS)`, tối ưu RLS `(SELECT auth.uid())`, chống deadlock), `akit-data`, `akit-contract`, `akit-architecture`, `akit-observability`.
7. **Vibe Coding & Product Development (1 repo — `datawhalechina/easy-vibe`):**
   - `akit-requirements` (Biến ý tưởng thành PRD & `Given/When/Then`), `akit-plan` (Chia nhỏ theo Vertical Slices có TDD), `akit-deliver` (Checklist bàn giao & kịch bản Rollback độc lập).

---

## 3. Sử dụng Nhanh `akit-debate` (Phản biện 3 bước) vs `akit-arena` (Đấu loại)

```powershell
# Chế độ Debate nhẹ (3 bước: propose -> challenge -> synthesize) — Khuyên dùng cho 2-3 phương án
python .akit/runtime/akit_cli.py arena init --session .akit/runs/debate1 --mode debate --task "Chọn SSE hay WebSockets cho thông báo đơn hàng realtime"
python .akit/runtime/akit_cli.py arena tasks --session .akit/runs/debate1 --out .akit/runs/debate1/tasks.json

# Chế độ Tournament (Đấu loại 4 phương án = 19 lượt)
python .akit/runtime/akit_cli.py arena init --session .akit/runs/tourney1 --agents 4 --mode tournament --task "Thiết kế phân quyền RBAC + RLS đa tổ chức cho NestJS PostgreSQL"
```

---

## 4. Kiểm tra Toàn vẹn & Chạy Test Suite

```powershell
python -m unittest discover -s tests -v
python .akit/runtime/akit_cli.py doctor --project .
```
