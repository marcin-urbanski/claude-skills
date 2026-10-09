#!/usr/bin/env python3
"""Condense a Claude Code session transcript into a short timeline for /retro.

Usage:
    digest.py                  # the running session (CLAUDE_CODE_SESSION_ID), else the cwd's newest
    digest.py <session-id>     # a session from any project in ~/.claude/projects
    digest.py <path.jsonl>     # a transcript file, e.g. a subagent's

Shows the user's messages, every tool call with its key input, errors, results over 20k characters
and repeated identical calls, then lists the session's subagents. Long text is cut, so the digest
stays small and quotes as little command output as possible.
"""
import collections
import glob
import json
import os
import re
import sys

PROJECTS = os.path.expanduser("~/.claude/projects")
TEXT_LIMIT = 300
LARGE_RESULT = 20_000
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
# The key input that identifies a call, per tool; other tools fall back to their compact JSON input.
KEY_INPUT = {"Bash": "command", "Read": "file_path", "Edit": "file_path", "Write": "file_path",
             "MultiEdit": "file_path", "NotebookEdit": "notebook_path", "Skill": "skill",
             "WebFetch": "url", "WebSearch": "query", "Glob": "pattern"}


def short(text, limit=TEXT_LIMIT):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + "…"


def entries(path):
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def summary(name, inp):
    if name == "Bash":
        return short(inp.get("command", "").splitlines()[0] if inp.get("command") else "")
    if name == "Grep":
        return short(inp.get("pattern", "") + (f" in {inp['path']}" if inp.get("path") else ""))
    if name in ("Agent", "Task"):
        return short(inp.get("description", ""))
    if name in KEY_INPUT:
        return short(inp.get(KEY_INPUT[name], ""))
    return short(json.dumps(inp, ensure_ascii=False), 150)


def result_text(content):
    if isinstance(content, list):
        return " ".join(block.get("text", "") for block in content if isinstance(block, dict))
    return str(content or "")


def user_text(content):
    if isinstance(content, str):
        return content
    return " ".join(block.get("text", "") for block in content
                    if isinstance(block, dict) and block.get("type") == "text")


def scan(path):
    """Return (timeline lines, tool counts, error count) for one transcript."""
    lines, tools, errors, seen = [], collections.Counter(), 0, collections.Counter()
    for entry in entries(path):
        message = entry.get("message") or {}
        content = message.get("content")
        time = (entry.get("timestamp") or "")[11:16]
        if entry.get("type") == "user" and not entry.get("isMeta") and content:
            if isinstance(content, list):
                for block in content:
                    if not (isinstance(block, dict) and block.get("type") == "tool_result"):
                        continue
                    text = result_text(block.get("content"))
                    if block.get("is_error"):
                        errors += 1
                        lines.append(f"[{time}]   ERROR: {short(text)}")
                    elif len(text) > LARGE_RESULT:
                        lines.append(f"[{time}]   [result {len(text) // 1000}k chars]")
            text = REMINDER.sub("", user_text(content)).strip()
            if text:
                lines.append(f"[{time}] USER: {short(text)}")
        elif entry.get("type") == "assistant" and isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text", "").strip():
                    lines.append(f"[{time}] CLAUDE: {short(block['text'], 200)}")
                elif block.get("type") == "tool_use":
                    name, inp = block.get("name", "?"), block.get("input") or {}
                    tools[name] += 1
                    label = f"{name}({inp['subagent_type']})" if inp.get("subagent_type") else name
                    # A retry often rewords the description, so it is not part of what makes a call identical.
                    key = name + json.dumps({k: v for k, v in inp.items() if k != "description"}, sort_keys=True)
                    seen[key] += 1
                    repeat = f" [repeat #{seen[key]}]" if seen[key] > 1 else ""
                    lines.append(f"[{time}] {label}: {summary(name, inp)}{repeat}")
    return lines, tools, errors


def digest(path):
    lines, tools, errors = scan(path)
    by_tool = ", ".join(f"{name} {n}" for name, n in tools.most_common())
    out = [f"# Session {os.path.basename(path)[:-len('.jsonl')]}: {sum(tools.values())} tool calls, "
           f"{errors} errors ({by_tool or 'no tools'}), times in UTC", ""] + lines
    subagents = sorted(glob.glob(os.path.join(path[:-len(".jsonl")], "subagents", "*.jsonl")))
    if subagents:
        out += ["", "## Subagents (digest one by passing its path)"]
    for sub in subagents:
        try:
            with open(sub[:-len(".jsonl")] + ".meta.json") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError):
            meta = {}
        _, sub_tools, sub_errors = scan(sub)
        out.append(f"- {meta.get('agentType', '?')}: {short(meta.get('description', ''), 100)} "
                   f"({sum(sub_tools.values())} tool calls, {sub_errors} errors) {sub}")
    return "\n".join(out)


def session_file(arg, cwd):
    """Resolve a transcript path from a path, a session id, or (no argument) the running session.

    The running session comes from CLAUDE_CODE_SESSION_ID, because Bash may sit in a worktree whose
    project folder differs from the session's; without it, the cwd's newest session is the best guess.
    """
    if arg and os.path.isfile(arg):
        return arg
    arg = arg or os.environ.get("CLAUDE_CODE_SESSION_ID")
    if arg:
        matches = glob.glob(os.path.join(PROJECTS, "*", f"{arg}*.jsonl"))
    else:
        matches = glob.glob(os.path.join(PROJECTS, re.sub(r"[^A-Za-z0-9]", "-", cwd), "*.jsonl"))
    return max(matches, key=os.path.getmtime) if matches else None


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    path = session_file(arg, os.getcwd())
    if not path:
        sys.exit(f"No transcript found for {arg or os.getcwd()} in {PROJECTS}.")
    print(digest(path))


if __name__ == "__main__":
    main()
