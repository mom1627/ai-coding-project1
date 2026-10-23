#!/usr/bin/env python3
"""Limited GitHub -> iSH workspace synchronizer. Python 3.9 compatible."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT / "chatgpt_workspace"
BASE = "https://raw.githubusercontent.com/mom1627/ai-coding-project1/main/"
HOST = "raw.githubusercontent.com"
IP = "185.199.111.133"  # Temporary workaround for iSH DNS issues
INTERVAL = 60

def download(path):
    if not path or path.startswith("/") or ".." in Path(path).parts or "\\" in path:
        raise ValueError("Invalid source path")
    result = subprocess.run(
        ["curl", "--silent", "--show-error", "--fail", "--location",
         "--noproxy", "*", "--resolve", HOST + ":443:" + IP,
         "--max-time", "20", BASE + path],
        capture_output=True, timeout=25, check=True)
    if len(result.stdout) > 500000:
        raise ValueError("File too large")
    return result.stdout

def sync_once():
    manifest = json.loads(download("workspace_manifest.json").decode("utf-8"))
    if manifest.get("version") != 1 or not isinstance(manifest.get("files"), list):
        raise ValueError("Unsupported manifest")
    if len(manifest["files"]) > 30:
        raise ValueError("Too many files")
    if WORKSPACE.is_symlink():
        raise ValueError("Workspace must not be a symlink")
    WORKSPACE.mkdir(exist_ok=True)
    for entry in manifest["files"]:
        source, destination = entry["source"], entry["destination"]
        if not isinstance(source, str) or not source.startswith(("examples/", "workspace_files/")):
            raise ValueError("Source not allowed")
        if not isinstance(destination, str) or not destination.startswith("chatgpt_workspace/"):
            raise ValueError("Destination not allowed")
        relative = destination[len("chatgpt_workspace/"):]
        parts = Path(relative).parts
        if not parts or any(p in ("", ".", "..") for p in parts) or "\\" in relative:
            raise ValueError("Invalid destination")
        target = WORKSPACE.joinpath(*parts)
        parent = target.parent
        current = WORKSPACE
        for part in parts[:-1]:
            current = current / part
            if current.is_symlink():
                raise ValueError("Symlink parent blocked")
        parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("Unsafe target")
        data = download(source)
        if target.exists() and target.read_bytes() == data:
            continue
        temp = parent / (".sync-" + hashlib.sha256(destination.encode()).hexdigest()[:16])
        if temp.exists() or temp.is_symlink():
            raise ValueError("Temporary path already exists")
        try:
            with temp.open("xb") as f:
                f.write(data)
            os.replace(str(temp), str(target))
        finally:
            if temp.exists():
                temp.unlink()
        print("Updated:", destination, flush=True)
    print("Sync OK", flush=True)

def main():
    print("iSH workspace sync started (every 60s). Ctrl+C to stop.", flush=True)
    try:
        while True:
            try:
                sync_once()
            except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
                print("Sync error:", exc, flush=True)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    main()
