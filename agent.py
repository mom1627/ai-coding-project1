#!/usr/bin/env python3
"""Approval-based local command runner for iSH."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "status": ["git", "status", "--short"],
    "files": ["ls", "-la"],
    "tests": ["python3", "-m", "unittest", "discover", "-v"],
    "python": ["python3", "--version"],
}

def main():
    print("Commands:", ", ".join(COMMANDS))
    while True:
        name = input("Command (exit to quit): ").strip()
        if name == "exit":
            return
        if name not in COMMANDS:
            print("Unknown or disallowed command")
            continue
        command = COMMANDS[name]
        print("Proposed:", " ".join(command))
        if input("Run? Type yes: ").strip() != "yes":
            continue
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                    text=True, timeout=30, shell=False)
            print((result.stdout + result.stderr)[-10000:])
            print("Exit code:", result.returncode)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print("Error:", exc)

if __name__ == "__main__":
    main()
