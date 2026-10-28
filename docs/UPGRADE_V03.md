# AKit v0.3 changes

## What changed

- New skill `akit-prior-art` (28 total) with three references: report template, GitHub search cheatsheet, seed list of reference repositories.
- New principle: for unfamiliar features do not write from zero; search GitHub for open-source projects and compare ideas first. Wired into `akit-router`, `akit-implement`, `akit-architecture`, `akit-plan`, `akit-scout` (cross-reference), `AKIT_AGENT_GUIDANCE.md` and `examples/AGENTS.snippet.md`.
- `akit-prior-art` joins the `core` profile (now 11 skills), so `frontend` (17) and `backend` (19) include it too.
- Three new activation fixtures in `skills/akit-eval/references/activation-cases.jsonl` (15 total) and three in `evals/activation_cases.jsonl`.

## Upgrading a managed install

```powershell
py -m akit.install --target antigravity --profile core --project "D:\MyApp" --with-agents --upgrade --dry-run
py -m akit.install --target antigravity --profile core --project "D:\MyApp" --with-agents --upgrade
```

Unchanged managed skills are updated with backups; skills you edited are reported as `modified` and left alone. The new `akit-prior-art` is installed as a new directory. Router, implement, architecture and plan changes reach you through the same managed upgrade.

## Limits

- Not live-tested in Antigravity or Codex: whether agents actually trigger `akit-prior-art` is measured only by offline fixtures, not real sessions.
- The reference repository list was checked by web search on 2026-10-28 and is unverified for license and maintenance quality.
- The skill reduces reinvention risk; it does not make copied or adapted code safe. Review license, security and tests as usual.
