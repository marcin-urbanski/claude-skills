#!/usr/bin/env python3
"""List and condense this repo's Claude Code transcripts so /playbook can find recurring tasks and fixed failures.

Usage, from anywhere inside the repo:
    history.py --list              # this repo's sessions (main checkout and its worktrees), oldest first
    history.py <session-id>...     # what the user asked and which commands ran, per session

Only the user's prompts, shell commands (marked [failed] when they errored) and edited file paths are printed.
Tool results, command output and Claude's own text are never printed, because they are where query results
and client data live. Obvious secrets in commands (passwords, tokens, credentials in URLs) are redacted.
"""
import glob
import json
import os
import re
import subprocess
import sys

PROJECTS = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
USER_LIMIT = 500
COMMAND_LIMIT = 1500
# Text that is not the user's own words: notices injected by Claude Code and the app (a task notification carries a
# subagent's result), and the output of `!` and slash commands. Pasted text may be a client's email, so it is dropped.
NOT_TYPED = re.compile(
    r"<(system-reminder|task-notification|side-sessions-event|artifact-view-context|recent-project-folders"
    r"|bash-stdout|bash-stderr|local-command-stdout|local-command-stderr)\b[^>]*>.*?</\1>", re.S)
PASTED = re.compile(r"<pasted_content\b[^>]*>.*?</pasted_content\b[^>]*>", re.S)
TAGS = re.compile(r"</?(?:bash-input|command-name|command-message|command-args)>")
EDIT_TOOLS = {"Edit": "edit", "MultiEdit": "edit", "Write": "write", "NotebookEdit": "edit"}
SECRETS = [
    (re.compile(r"(\b(?:mysql|mysqldump|mysqladmin|mariadb)\b[^\n|;&]*?\s-p)(?!\s)\S+"), r"\1[redacted]"),
    (re.compile(r"(?i)((?:pass(?:word|wd)?|secret|token|api[_-]?key)\w*\s*[=:]\s*)([\"']?)[^\s\"']+"),
     r"\1\2[redacted]"),
    (re.compile(r"(?i)(bearer\s+)\S+"), r"\1[redacted]"),
    (re.compile(r"(://[^/\s:@]+:)[^@\s/]+@"), r"\1[redacted]@"),
]


def project_key(path):
    """The folder name Claude Code uses under ~/.claude/projects for a working directory."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def git_out(*args, cwd=None):
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return ""


def common_dir(cwd):
    return git_out("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=cwd)


def main_checkout(cwd):
    """The repo's main checkout, from the main checkout itself or any linked worktree; None if there is none."""
    common = common_dir(cwd)
    if not common:
        return None
    if common == git_out("rev-parse", "--path-format=absolute", "--git-dir", cwd=cwd):
        return git_out("rev-parse", "--show-toplevel", cwd=cwd)
    if git_out("--git-dir", common, "config", "core.worktree"):
        return git_out("--git-dir", common, "rev-parse", "--show-toplevel", cwd=cwd)
    if os.path.basename(common) == ".git":
        return os.path.dirname(common)
    return None


def entries(path):
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def session_cwd(path):
    return next((entry["cwd"] for entry in entries(path) if entry.get("cwd")), "")


def sessions(projects_dir, main):
    """Transcripts of the main checkout and its worktrees, removed nested worktrees included.

    A folder named after the main checkout belongs to it. A folder that only starts with that name may be a
    worktree (`app--claude-worktrees-x`, `app-feature`) or another project (`app-admin`), so each of its sessions
    counts only when its working directory is inside the main checkout or still shares the repo's git folder.
    """
    key, common, found = project_key(main), common_dir(main), []
    for folder in sorted(os.listdir(projects_dir)) if os.path.isdir(projects_dir) else []:
        if folder != key and not folder.startswith(key + "-"):
            continue
        for path in sorted(glob.glob(os.path.join(projects_dir, folder, "*.jsonl"))):
            cwd = session_cwd(path)
            if folder == key or cwd.startswith(main + os.sep) or (os.path.isdir(cwd) and common_dir(cwd) == common):
                found.append(path)
    return found


def redact(command):
    for pattern, replacement in SECRETS:
        command = pattern.sub(replacement, command)
    return command


def short(text, limit):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + "…"


def user_text(content):
    if isinstance(content, str):
        text = content
    else:
        text = " ".join(block.get("text", "") for block in content
                        if isinstance(block, dict) and block.get("type") == "text")
    return TAGS.sub(" ", PASTED.sub("[pasted text]", NOT_TYPED.sub(" ", text))).strip()


def digest(path):
    """Lines for one transcript: USER prompts, `$ command` (with [failed]) and edited files, in order."""
    lines, command_line = [], {}
    for entry in entries(path):
        content = (entry.get("message") or {}).get("content")
        if not content:
            continue
        if entry.get("type") == "user" and not entry.get("isMeta"):
            if isinstance(content, list):
                for block in content:
                    if (isinstance(block, dict) and block.get("type") == "tool_result" and block.get("is_error")
                            and block.get("tool_use_id") in command_line):
                        lines[command_line[block["tool_use_id"]]] += " [failed]"
            text = user_text(content)
            if text:
                lines.append(f"USER: {short(text, USER_LIMIT)}")
        elif entry.get("type") == "assistant" and isinstance(content, list):
            for block in content:
                if not (isinstance(block, dict) and block.get("type") == "tool_use"):
                    continue
                name, inp = block.get("name"), block.get("input") or {}
                if name == "Bash" and inp.get("command"):
                    command_line[block.get("id")] = len(lines)
                    lines.append(f"$ {short(redact(inp['command']), COMMAND_LIMIT)}")
                elif name in EDIT_TOOLS and (inp.get("file_path") or inp.get("notebook_path")):
                    lines.append(f"{EDIT_TOOLS[name]} {inp.get('file_path') or inp.get('notebook_path')}")
    return lines


def first_timestamp(path):
    return next((entry["timestamp"] for entry in entries(path) if entry.get("timestamp")), "")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    main_dir = main_checkout(os.getcwd())
    if not main_dir:
        print("Not inside a git repo with a main checkout.", file=sys.stderr)
        return 1
    found = sorted(sessions(PROJECTS, main_dir), key=first_timestamp)
    if args[0] == "--list":
        if not found:
            print(f"No transcripts for {main_dir} in {PROJECTS}.")
            return 0
        print(f"{len(found)} sessions of {main_dir}, {first_timestamp(found[0])[:10]} to "
              f"{first_timestamp(found[-1])[:10]}:")
        for path in found:
            prompts = sum(line.startswith("USER: ") for line in digest(path))
            print(f"{os.path.basename(path)[:-6]}  {first_timestamp(path)[:10]}  {prompts} prompts  "
                  f"{session_cwd(path)}")
        return 0
    by_id = {os.path.basename(path)[:-6]: path for path in found}
    for session_id in args:
        if session_id not in by_id:
            print(f"## {session_id}: not a session of {main_dir}", file=sys.stderr)
            continue
        path = by_id[session_id]
        print(f"## {session_id} {first_timestamp(path)[:10]} {session_cwd(path)}")
        print("\n".join(digest(path)) or "(nothing)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
