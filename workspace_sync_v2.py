#!/usr/bin/env python3
"""iSH workspace synchronizer v2. Python 3.9, no external Python packages."""
import base64
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST_ROOT = ROOT / "chatgpt_workspace"
API = "https://api.github.com/repos/mom1627/ai-coding-project1/contents/"
HOST = "api.github.com"
IP = "140.82.121.5"  # temporary iSH DNS workaround

def fetch(path):
    if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/") or "\\" in path:
        raise ValueError("Invalid path")
    cmd = ["curl", "-fLsS", "--noproxy", "*", "--resolve", HOST + ":443:" + IP,
           "--max-time", "20", "-H", "Accept: application/vnd.github+json",
           "-H", "Cache-Control: no-cache", API + path + "?ref=main"]
    out = subprocess.run(cmd, capture_output=True, timeout=25, check=True)
    if len(out.stdout) > 800000:
        raise ValueError("API response too large")
    obj = json.loads(out.stdout.decode("utf-8"))
    if obj.get("encoding") != "base64" or not isinstance(obj.get("content"), str):
        raise ValueError("Unexpected GitHub API response")
    data = base64.b64decode(obj["content"], validate=False)
    if len(data) > 500000:
        raise ValueError("File too large")
    return data

def sync_once():
    manifest = json.loads(fetch("workspace_manifest.json").decode("utf-8"))
    entries = manifest.get("files")
    if manifest.get("version") != 1 or not isinstance(entries, list) or len(entries) > 30:
        raise ValueError("Invalid manifest")
    if DEST_ROOT.is_symlink():
        raise ValueError("Workspace symlink not allowed")
    DEST_ROOT.mkdir(exist_ok=True)
    for entry in entries:
        src = entry.get("source")
        dst = entry.get("destination")
        if not isinstance(src, str) or not src.startswith(("examples/", "workspace_files/")):
            raise ValueError("Source not allowed")
        if not isinstance(dst, str) or not dst.startswith("chatgpt_workspace/"):
            raise ValueError("Destination not allowed")
        parts = dst[len("chatgpt_workspace/"):].split("/")
        if not parts or any(x in ("", ".", "..") for x in parts) or "\\" in dst:
            raise ValueError("Invalid destination")
        target = DEST_ROOT
        for segment in parts[:-1]:
            target = target / segment
            if target.is_symlink():
                raise ValueError("Directory symlink not allowed")
        target.mkdir(parents=True, exist_ok=True)
        file = target / parts[-1]
        if file.is_symlink() or (file.exists() and not file.is_file()):
            raise ValueError("Unsafe target")
        data = fetch(src)
        if file.exists() and file.read_bytes() == data:
            continue
        tmp = target / (".sync-" + parts[-1] + ".tmp")
        if tmp.exists() or tmp.is_symlink():
            raise ValueError("Temporary path exists")
        try:
            with tmp.open("xb") as handle:
                handle.write(data)
            os.replace(str(tmp), str(file))
        finally:
            if tmp.exists():
                tmp.unlink()
        print("Updated:", dst, flush=True)
    print("Sync OK", flush=True)

def main():
    print("iSH workspace sync v2 running. Checks every 60 seconds.", flush=True)
    try:
        while True:
            try:
                sync_once()
            except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
                print("Sync error:", exc, flush=True)
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    main()
