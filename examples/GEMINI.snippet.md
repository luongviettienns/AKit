# Antigravity Workspace Rules Snippet (`GEMINI.md` / `AGENTS.md`)

Copy the rules below into your project's `GEMINI.md` or `AGENTS.md` (kept well under the 24 KB Antigravity per-file rule limit).

---

```markdown
# Project Engineering Rules (AKit v0.4.0 — Antigravity & Superpowers Deep Edition)

## 1. Proactive Skill Evaluation & Auto Slash-Workflow Orchestration (`akit-router`)
- Khi nhận lệnh từ người dùng, BẮT BUỘC đọc `.agents/skills/akit-router/SKILL.md`, xem xét toàn bộ bộ kỹ năng hiện có để chọn ra phương án kết hợp tối ưu nhất (2–4 skills/lượt), trình bày ngắn gọn phương án tối ưu đó trước khi thực thi.
- **Tự động hóa Slash Workflows (Auto Slash-Command Emulation):** Vì Slash Commands trên Antigravity (`/plan`, `/grill-me`, `/boost`, `/teamwork`, `/goal`, `/browser`, `/compact`, `/schedule`, `/learn`) là UI triggers phía client, Agent KHÔNG chờ người dùng gõ tay mà **tự động kích hoạt luồng công cụ native tương đương** ngay khi ngữ cảnh phù hợp (`references/slash-command-auto-orchestration.md`):
  - Tương đương `/grill-me` -> Tự động kích hoạt `akit-requirements` + gọi tool `ask_question` để làm rõ yêu cầu.
  - Tương đương `/plan` -> Tự động kích hoạt `akit-plan` + tạo Artifact `implementation_plan.md` (kèm nút *Proceed*).
  - Tương đương `/boost` -> Tự động kích hoạt `akit-debate` (Triad Debate) hoặc `akit-arena` + kiểm chứng đa chiều.
  - Tương đương `/teamwork` -> Tự động kích hoạt `invoke_subagent` song song (`akit-scout`, `akit-debater`, `akit-critic`, `akit-security`) hoặc **Subagent-Driven Development (SDD)**.
  - Tương đương `/goal` -> Tự động chạy chế độ **Continuous Execution + SDD Ledger** (`.superpowers/sdd/<plan>/progress.md`), ghi nhận `Ruling:` và kiểm chứng khép kín (`akit-deliver`) cho đến khi hoàn thành.
  - Tương đương `/browser` -> Tự động kích hoạt `akit-browser-qa` (Playwright / Chrome DevTools).

## 2. Quy tắc Bắt buộc: Không viết từ con số 0 (`akit-prior-art`)
- **QUY TẮC BẮT BUỘC:** *"Đối với những chức năng chưa quen thuộc, đừng viết từ con số 0, hãy tìm kiếm các dự án mã nguồn mở trên GitHub để so sánh ý tưởng trước khi bắt tay vào làm."*
- Trước khi thiết kế hoặc viết code cho bất kỳ chức năng/thuật toán/kiến trúc nào chưa có sẵn mẫu chuẩn trong repo (OAuth/PKCE, giữ chỗ/seat locking, hàng đợi webhook, đồng bộ thời gian thực, parser, RBAC đa tầng...), BẮT BUỘC kích hoạt `.agents/skills/akit-prior-art/SKILL.md`:
  1. Tìm kiếm tối thiểu 2–3 dự án mã nguồn mở uy tín trên GitHub (`search_web` với `domain: "github.com"` hoặc `gh search`).
  2. Đọc mã nguồn thực tế và test suite của chúng (không chỉ đọc README).
  3. Lập bảng so sánh kiến trúc, edge cases, giấy phép (License) và chốt quyết định **Adopt (Dùng thư viện) / Adapt (Học kiến trúc & viết lại theo chuẩn repo) / Build (Tự xây dựng)**.

## 3. Deep `obra/superpowers` Engineering Workflow
- **Brainstorming & Scope Check (`akit-requirements`):** Phân loại phạm vi (`Spike` / `Bounded` / `Architectural`), hỏi từng vấn đề cốt lõi qua `ask_question`, và chốt spec trước khi code.
- **Writing Plans (`akit-plan`):** Chia nhỏ thành các task 2–5 phút có đầy đủ đường dẫn file, khối `Consumes` / `Produces`, code test mẫu, lệnh chạy, **Pre-flight Conflict Scan**, và cấm tuyệt đối `TODO`/`TBD`/placeholders.
- **TDD & Subagent-Driven Development (`akit-implement`):**
  - **Iron Law:** `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST` (`RED -> Verify RED -> GREEN -> Verify GREEN -> REFACTOR with akit-simplify`).
  - Khi chạy theo kế hoạch nhiều task: lưu **SDD Ledger** tại `.superpowers/sdd/<plan>/progress.md`, dùng hợp đồng 4 trạng thái (`DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED`), ghi nhận mọi phán quyết bằng `Ruling: <quyết định> — <lý do> — <rủi ro nếu sai>`, và áp dụng vòng lặp sửa lỗi tối đa 5 vòng (**5-Round Fix Loop Breaker**).
- **Systematic Debugging (`akit-debug`):** `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.` Truy ngược call stack về nguồn phát sinh lỗi, áp dụng **4-Layer Defense-in-Depth Validation**, thay `sleep/setTimeout` đoán mò bằng `waitFor()`, và dừng lại xét lại kiến trúc nếu đã thử sửa 3 lần thất bại.
- **Two-Stage Code Review (`akit-review`):** Tách bạch **Stage 1 (Spec Compliance)** và **Stage 2 (Code Quality & Security)**. Khi nhận review, cấm tuyệt đối phản hồi xã giao kiểu *"You're absolutely right!"* — phải xác minh với codebase và kiểm tra YAGNI trước khi sửa.
- **Git Worktree & Branch Finishing (`akit-git`):** Kiểm tra `GIT_DIR != GIT_COMMON` và submodule guard trước khi tạo `.worktrees/` (bắt buộc có trong `.gitignore`). Khi hoàn tất, chạy lại full test suite và trình bày menu 3 lựa chọn tích hợp (Merge local / Push & PR / Keep as-is).
```
