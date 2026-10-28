# AKit v0.2 evaluation scorecard

Scoring method: engineer-reviewed **implementation/readiness** score, 0–10, not proven model accuracy. Category scores based on code inspection, automated unit/integration tests and availability of real-agent evidence.

| Category | Score | Evidence | Limitation |
|---|---:|---|---|
| Skill structure and task coverage | 8.5 | 28 skills; specific triggers, safety gates, references | Some procedures are instructions rather than executable tools |
| Antigravity compatibility | 8 | Official workspace skill path plus optional read-only subagent profiles | No real IDE end-to-end delegation test |
| Codex compatibility | 8 | Same skill path, AGENTS guidance, shared runtime | No real Codex session activation measurement |
| Tournament | 6 | Deterministic rounds and bounded rubric with mock tests | No verified native live bridge, model judges may err |
| Verification discipline | 7 | Unit tests, checks CLI, offline eval rubric | No A/B behavioral benchmark with paid/free AI model yet |
| Security and install safety | 7.5 | No automatic third-party integration, hash-based skip/update, path checks | Tool environment and future skills still need trust review |

Overall readiness judgement: **~7.5/10** for a controlled pilot on low-risk projects. Not production certified; no 100% agent compatibility claim. The next release should prioritize real Antigravity+Codex activation/e2e evaluations rather than more skills.
