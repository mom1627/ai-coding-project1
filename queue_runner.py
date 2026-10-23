#!/usr/bin/env python3
"""Fetch and execute only approved, allowlisted GitHub command requests."""
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = "https://raw.githubusercontent.com/mom1627/ai-coding-project1/main/commands.json"
ALLOWED = {
    "status": ["git", "status", "--short"],
    "files": ["ls", "-la"],
    "tests": ["python3", "-m", "unittest", "discover", "-v"],
    "python": ["python3", "--version"],
}

def main():
    with urllib.request.urlopen(URL, timeout=15) as response:
        data = json.load(response)
    if data.get("version") != 1 or not isinstance(data.get("commands"), list):
        raise ValueError("Invalid queue format")
    seen = set()
    for job in data["commands"][:20]:
        if not isinstance(job, dict):
            continue
        job_id, name = job.get("id"), job.get("name")
        if not isinstance(job_id, str) or job_id in seen or name not in ALLOWED:
            print("Skipped invalid/duplicate job")
            continue
        seen.add(job_id)
        print("\nJob:", job_id, "-", job.get("description", ""))
        print("Command:", " ".join(ALLOWED[name]))
        if input("Execute? Type yes: ").strip() != "yes":
            print("Skipped")
            continue
        try:
            result = subprocess.run(ALLOWED[name], cwd=ROOT, capture_output=True,
                                    text=True, timeout=30, shell=False)
            print((result.stdout + result.stderr)[-10000:])
            print("Exit code:", result.returncode)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print("Error:", exc)

if __name__ == "__main__":
    main()
