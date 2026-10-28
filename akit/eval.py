"""Offline skill-activation eval and Andrej Karpathy 4-Laws code/diff quality evaluator."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

OVERENGINEERED_NAME_RE = re.compile(
    r"\b(?:class|interface)\s+\w*(?:Abstract\w*Factory|FactoryManager|StrategyFactory|Enterprise\w*Manager)\w*\b"
)
SPECULATIVE_TODO_RE = re.compile(r"\b(?:TODO|FIXME|HACK)\b", re.IGNORECASE)
LEFTOVER_DEBUG_RE = re.compile(r"(?:\bconsole\.log\s*\(|\bdebugger\b|\bpdb\.set_trace\s*\()")


def score(cases: list[dict], observations: list[dict]) -> dict:
    expected = {x["id"]: set(x.get("expected", [])) for x in cases}
    observed = {x["id"]: set(x.get("selected", [])) for x in observations}
    if len(expected) != len(cases) or len(observed) != len(observations):
        raise ValueError("Case/observation IDs must be unique")
    if not set(observed).issubset(expected):
        raise ValueError("Observed unknown case IDs")
    true_positive = false_positive = false_negative = 0
    details = []
    for ident, needed in expected.items():
        got = observed.get(ident, set())
        true_positive += len(needed & got)
        false_positive += len(got - needed)
        false_negative += len(needed - got)
        details.append({"id": ident, "matched": sorted(got & needed),
                        "missing": sorted(needed - got), "extra": sorted(got - needed),
                        "observed": ident in observed})
    prec = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    rec = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    return {"kind": "offline_skill_activation", "observed_cases": len(observed), "total_cases": len(expected),
            "coverage": len(observed) / len(expected) if expected else 0.0,
            "precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(2 * prec * rec / (prec + rec), 4) if prec + rec else 0.0,
            "details": details, "warning": "Only measures recorded selected skills, not actual AI output quality."}


def evaluate_karpathy_diff(
    diff_text: str,
    allowed_files: list[str] | None = None,
    evidence: dict | None = None,
    assumptions_stated: bool = True,
    max_added_lines: int = 200,
) -> dict:
    """Score a unified git diff and test evidence against Andrej Karpathy's 4 Laws (multica-ai/andrej-karpathy-skills)."""
    touched_files: list[str] = []
    added_lines: list[str] = []
    removed_lines: list[str] = []

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            fp = line[6:].strip()
            if fp != "/dev/null" and fp not in touched_files:
                touched_files.append(fp)
        elif line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line[1:])

    violations: list[str] = []

    # Law 1: Think Before Coding (25 pts)
    think_score = 25 if assumptions_stated else 10
    if not assumptions_stated:
        violations.append("Law 1 (Think Before Coding): Assumptions and tradeoffs were not explicitly stated before coding.")

    # Law 2: Simplicity First (25 pts)
    simplicity_score = 25
    if len(added_lines) > max_added_lines:
        simplicity_score -= 10
        violations.append(
            f"Law 2 (Simplicity First): Added {len(added_lines)} lines, exceeding max_added_lines={max_added_lines}."
        )
    added_blob = "\n".join(added_lines)
    if OVERENGINEERED_NAME_RE.search(added_blob):
        simplicity_score -= 10
        violations.append("Law 2 (Simplicity First): Speculative over-engineered abstraction detected in added lines.")
    if SPECULATIVE_TODO_RE.search(added_blob):
        simplicity_score -= 5
        violations.append("Law 2 (Simplicity First): Speculative TODO/FIXME/HACK placeholder left in added code.")
    simplicity_score = max(0, simplicity_score)

    # Law 3: Surgical Changes (25 pts)
    surgical_score = 25
    if allowed_files is not None:
        normalized_allowed = {p.replace("\\", "/") for p in allowed_files}
        out_of_scope = [f for f in touched_files if f.replace("\\", "/") not in normalized_allowed]
        if out_of_scope:
            surgical_score -= 15
            violations.append(
                f"Law 3 (Surgical Changes): Out-of-scope files modified: {', '.join(out_of_scope)}"
            )
    if LEFTOVER_DEBUG_RE.search(added_blob):
        surgical_score -= 10
        violations.append("Law 3 (Surgical Changes): Leftover debug print/console.log/debugger statement in diff.")
    surgical_score = max(0, surgical_score)

    # Law 4: Goal-Driven Execution (25 pts)
    goal_score = 25
    has_test_file = any(
        "test" in f.lower() or "spec" in f.lower() for f in touched_files
    )
    if not has_test_file:
        goal_score -= 10
        violations.append("Law 4 (Goal-Driven Execution): Diff includes no test/spec file verification changes.")
    if not evidence or evidence.get("status") != "passed" or evidence.get("exit_code") != 0:
        goal_score -= 15
        violations.append("Law 4 (Goal-Driven Execution): Missing or failing machine-recorded verification evidence.")
    goal_score = max(0, goal_score)

    total = think_score + simplicity_score + surgical_score + goal_score
    return {
        "kind": "karpathy_4_laws_quality",
        "source": "multica-ai/andrej-karpathy-skills",
        "scores": {
            "think_before_coding": think_score,
            "simplicity_first": simplicity_score,
            "surgical_changes": surgical_score,
            "goal_driven_execution": goal_score,
        },
        "total_score": total,
        "passed": total >= 80 and not any(v.startswith("Law 4") for v in violations),
        "touched_files": touched_files,
        "added_lines": len(added_lines),
        "removed_lines": len(removed_lines),
        "violations": violations,
    }


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="AKit Evaluator: skill activation F1 or Karpathy 4-Laws diff quality")
    parser.add_argument("--mode", choices=("activation", "karpathy"), default="activation")
    parser.add_argument("--cases", type=Path, help="Activation benchmark JSONL (for --mode activation)")
    parser.add_argument("--observations", type=Path, help="Recorded observations JSONL (for --mode activation)")
    parser.add_argument("--diff-file", type=Path, help="Unified git diff file (for --mode karpathy)")
    parser.add_argument("--evidence", type=Path, help="Machine verification evidence JSON (for --mode karpathy)")
    parser.add_argument("--allowed-files", nargs="*", default=None, help="Allowed file paths for surgical scope check")
    parser.add_argument("--assumptions-stated", action="store_true", help="Confirm assumptions were explicitly stated")
    parser.add_argument("--max-added-lines", type=int, default=200)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if args.mode == "karpathy":
        if not args.diff_file:
            raise SystemExit("--diff-file is required when --mode karpathy is selected")
        diff_text = args.diff_file.read_text(encoding="utf-8")
        ev = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence and args.evidence.exists() else None
        result = evaluate_karpathy_diff(
            diff_text=diff_text,
            allowed_files=args.allowed_files,
            evidence=ev,
            assumptions_stated=args.assumptions_stated,
            max_added_lines=args.max_added_lines,
        )
    else:
        if not args.cases or not args.observations:
            raise SystemExit("--cases and --observations are required for --mode activation")
        result = score(read_jsonl(args.cases), read_jsonl(args.observations))

    content = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
