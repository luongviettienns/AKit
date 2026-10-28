"""Record real command-based verification evidence locally; never claim synthetic passes."""
from __future__ import annotations
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run_checks(project: Path, command: list[str], output: Path, timeout: int = 180) -> dict:
    if not command or any(not x for x in command):
        raise ValueError("Expected explicit executable and arguments")
    if not (1 <= timeout <= 900):
        raise ValueError("Timeout out of bounds")
    project = project.resolve()
    if not project.is_dir():
        raise FileNotFoundError(project)
    if output.is_symlink():
        raise ValueError("Refusing symlinked output")
    started = datetime.now(timezone.utc).isoformat()
    try:
        proc = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=timeout,
                              errors="replace", check=False)
        status = "passed" if proc.returncode == 0 else "failed"
        exit_code = proc.returncode
        stdout, stderr = proc.stdout[-8000:], proc.stderr[-8000:]
    except subprocess.TimeoutExpired as exc:
        status, exit_code = "timeout", None
        stdout, stderr = "", f"Timed out after {timeout} seconds"
    result = {"kind":"command_execution_evidence", "command":command, "cwd":str(project),
              "started_utc":started, "finished_utc":datetime.now(timezone.utc).isoformat(),
              "status":status, "exit_code":exit_code, "stdout_tail":stdout, "stderr_tail":stderr,
              "disclaimer":"A passing command is only evidence for this check, not a security or production guarantee."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an explicitly supplied local verification command and write evidence")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command after --, e.g. -- python -m unittest discover")
    args = parser.parse_args()
    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not command:
        parser.error("Specify command after --")
    result = run_checks(args.project, command, args.out, args.timeout)
    print(json.dumps({"status":result["status"], "exit_code":result["exit_code"], "evidence":str(args.out)}))
    if result["status"] != "passed":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
