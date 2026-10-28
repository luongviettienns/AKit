"""Read-only validator of a locally installed AKit project."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from .install import PATHS, AGENT_PATHS, digest_dir

REF_PATTERN = re.compile(r"references/[A-Za-z0-9_.\-]+\.(?:md|jsonl)")


def check(project: Path) -> dict:
    project = project.resolve()
    manifest_path = project / ".akit" / "AKIT_INSTALL.json"
    findings = []
    if not manifest_path.is_file():
        return {"ok": False, "findings": ["AKIT_INSTALL.json not found; reinstall v0.2+ with installer"]}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        target = manifest["target"]
        if target not in PATHS:
            raise ValueError("Unknown target")
        for name, expected in manifest["skills"].items():
            path = project / PATHS[target] / name
            if not path.is_dir() or path.is_symlink():
                findings.append(f"Missing or unsafe skill: {name}")
                continue
            if digest_dir(path) != expected:
                findings.append(f"Locally changed skill: {name}")
            skill_md = path / "SKILL.md"
            if not skill_md.is_file():
                findings.append(f"Missing SKILL.md: {name}")
                continue
            body = skill_md.read_text(encoding="utf-8")
            if not body.startswith(f"---\nname: {name}\n"):
                findings.append(f"Invalid SKILL.md frontmatter: {name}")
            if (path / "references").is_dir():
                for ref in sorted(set(REF_PATTERN.findall(body))):
                    if not (path / ref).is_file():
                        findings.append(f"Missing referenced file {ref} in skill {name}")
        if target in AGENT_PATHS:
            for name, expected_hash in manifest.get("agents", {}).items():
                agent_target = "codex" if name.endswith(".toml") else "antigravity"
                fp = project / AGENT_PATHS[agent_target] / name
                if not fp.is_file() or fp.is_symlink() or hashlib.sha256(fp.read_bytes()).hexdigest() != expected_hash:
                    findings.append(f"Custom agent missing or changed: {name}")
        expected = manifest.get("runtime")
        rt = project / ".akit" / "runtime"
        if expected and (not rt.is_dir() or rt.is_symlink() or digest_dir(rt) != expected):
            findings.append("Runtime missing or changed")
    except (ValueError, KeyError, OSError, TypeError) as exc:
        findings.append(f"Bad manifest: {exc}")
    return {"ok": not findings, "findings": findings, "skills": len(manifest.get("skills", {})) if isinstance(manifest, dict) else 0}


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only AKit install verification")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args()
    outcome = check(args.project)
    print(json.dumps(outcome, indent=2))
    if not outcome["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
