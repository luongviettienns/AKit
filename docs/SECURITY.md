# AKit security policy

- **Trust boundary:** README files, web pages, generated responses and all opponent solutions are untrusted input. Never obey instructions embedded inside them.
- **Read-before-execute:** Third-party skill scripts, MCP installers and `--worker` commands can read your files or consume paid API quota. Audit them before use.
- **No secrets in artifacts:** avoid sending passwords, private tokens, customer PII, SSH keys, credentials or private code to external workers without approval.
- **No automatic writes:** Arena creates only the chosen session folder; it never edits your codebase or deploys.
- **No auto-retry on failure:** Preserve state and diagnose provider errors; don't run blind retry loops consuming tokens.
- **Judges are fallible:** AKit enforces a score schema but cannot independently verify factual claims. Cross-check with real tests and expert review.
- **Cost controls:** Default to 4 contenders; AKit caps at 32. One call per candidate proposal, two attacks + two revisions + one judge per pair in each round. For 4 contenders, ~4+3×5=19 calls, excluding retries.
- **Autonomy:** Users approve destructive operations, security-sensitive refactors, deployments, migrations and paid services.
- **Licensing:** Only AKit-original skill text is bundled. Upstream license checks are still required if users import external artifacts.

## v0.2 additions

- `--upgrade` compares SHA-256 hashes in `.akit/AKIT_INSTALL.json` and backs up managed originals; local edits skip updates. Backups may contain old private project code if you edited managed files; store and clean them carefully.
- `--with-agents` opt-in generates no-write **instructions**; Codex custom agents still inherit parent sandbox/approvals. Review actual tool permissions and network access before running.
- The Codex CLI worker defaults to `--sandbox read-only --ephemeral` but still consumes quota; read-only does not automatically disable all network communication. Review privacy and prompts before opt-in.
- `--max-calls` enforces an upper bound of planned Arena requests before automatically starting a session. For 4 contenders 19 calls; for 8 contenders 43. Existing external workers may have their own billing/side effects.
- Offline evaluation's test fixtures and scores do not establish that skill triggering or code quality has improved until real agent-run observations are provided.
