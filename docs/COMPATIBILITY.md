# Compatibility — AKit v0.3.0

Primary supported deployment targets: **Antigravity** and **Codex**. Other paths remain for legacy convenience but are not part of this release's integration tests.

| Feature | Antigravity | Codex |
|---|---|---|
| Agent Skills | `.agents/skills/` | `.agents/skills/` |
| Custom subagent definitions | `.agents/agents/*.md` | `.codex/agents/*.toml` |
| Agent invocation | `invoke_subagent` in supported sessions | Built-in subagent delegation or named agents in supported clients |
| Native Arena automation | Step-by-step recipe only; not tested end-to-end | Step-by-step recipe only; not tested end-to-end |
| Autonomous optional worker | API-compatible/Ollama external worker | `codex exec` subprocess worker, read-only sandbox |
| Install/doctor/integrity | Tested local files | Tested local files |
| Live model/subagent E2E | NOT TESTED | NOT TESTED |

Codex custom subagents inherit their parent sandbox/approval settings, regardless of instructions in TOML. Antigravity subagents also inherit parent permissions; verify current environment and do not grant code-write tools to critique-only agents. Skills are selectively loaded by the IDE at session start using metadata, then body on demand.

Official docs checked 2026-10-28:
- https://www.antigravity.google/docs/skills
- https://www.antigravity.google/docs/subagents
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/developer-commands

**Do not assume a native slash command exists for every skill on every Codex client.** Invoking by name/instruction remains the cross-client fallback.
