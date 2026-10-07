#!/usr/bin/env python3
"""Report which skills Claude Code invoked, per session, from the local transcripts.

Usage:
    scripts/skill-usage.py                       # all projects, last 14 days
    scripts/skill-usage.py TimeTracker           # projects whose folder name contains "TimeTracker"
    scripts/skill-usage.py TimeTracker --since 2026-09-30
    scripts/skill-usage.py TimeTracker --since 2026-10-05T07:31   # sessions started at or after 07:31 UTC
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re

PROJECTS = os.path.expanduser("~/.claude/projects")
WATCHED = ["spec-first", "tdd", "systematic-debugging", "verification-before-completion", "handoff"]
CODE_FILE = re.compile(r"\.(php|js|jsx|ts|tsx|vue|swift|py|rb|go|rs|css|scss|sql)$")
GIT_COMMIT = re.compile(r"(^|&&|;|\n)\s*git commit\b")
# Heuristic over the raw command string, not a shell parser: a code path counts when it is the target of
# `>`/`>>` (not `2>`, `>&2`, `->` or `=>`), an argument of `tee` or `sed -i`, or a Python open(path, "w"/"a"/"x")
# or Path(path).write_text/write_bytes with a literal path. `sed -i` arguments run past `;` on purpose, for
# scripts like `s/a/b/;s/c/d/`; a `|` or `&` inside a sed script can hide the path.
BASH_WRITES = [
    re.compile(r"(?<![0-9>=-])>>?\s*([^\s;|&<>]+)"),
    re.compile(r"\btee\b([^\n;|&]*)"),
    re.compile(r"\bsed[ \t]+(?:[^\s;|&]+[ \t]+)*?-i\S*([^\n|&]*)"),
    re.compile(r"\bopen\(\s*(['\"][^'\"]+['\"])\s*,\s*(?:mode\s*=\s*)?['\"][^'\"]*[wax]"),
    re.compile(r"\bPath\(\s*(['\"][^'\"]+['\"])\s*\)\.write_(?:text|bytes)\("),
]


def tool_uses(path):
    """Yield (tool name, input) for every tool call in one transcript file."""
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                content = (json.loads(line).get("message") or {}).get("content")
            except json.JSONDecodeError:
                continue
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    yield block.get("name"), block.get("input") or {}


def bash_writes_code(command):
    """True when a Bash command writes at least one file with a code extension."""
    return any(CODE_FILE.search(arg.strip("'\";"))
               for pattern in BASH_WRITES for m in pattern.finditer(command) for arg in m.group(1).split())


def since_arg(value):
    """Validate --since and normalise it to YYYY-MM-DD or YYYY-MM-DDTHH:MM, comparable with UTC timestamps."""
    value = value.replace(" ", "T")
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.datetime.strptime(value, fmt).strftime(fmt)
        except ValueError:
            pass
    raise argparse.ArgumentTypeError(f"expected YYYY-MM-DD or YYYY-MM-DDTHH:MM (UTC), got {value!r}")


def first_timestamp(path):
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                ts = json.loads(line).get("timestamp")
            except json.JSONDecodeError:
                continue
            if ts:
                return ts
    return None


def scan_session(main_file):
    """Count skills, code edits, commits and subagents in a session, subagents included."""
    session_dir = main_file[: -len(".jsonl")]
    files = [main_file] + glob.glob(os.path.join(session_dir, "subagents", "*.jsonl"))
    s = {"main_skills": set(), "sub_skills": set(), "code_edits": 0, "commits": 0, "subagents": len(files) - 1,
         "agent_types": collections.Counter()}
    for path in files[1:]:
        # Skills preloaded through an agent's `skills` field never show up as Skill calls,
        # so the agent type is the only trace that, for example, `implementer` had `tdd`.
        try:
            with open(path[: -len(".jsonl")] + ".meta.json") as f:
                s["agent_types"][json.load(f).get("agentType", "?")] += 1
        except (OSError, json.JSONDecodeError):
            s["agent_types"]["?"] += 1
    for path in files:
        skills = s["main_skills"] if path == main_file else s["sub_skills"]
        for name, inp in tool_uses(path):
            if name == "Skill":
                skills.add(inp.get("skill", "?").split(":")[-1])
            elif name in ("Edit", "Write", "MultiEdit") and CODE_FILE.search(inp.get("file_path", "")):
                s["code_edits"] += 1
            elif name == "Bash":
                command = inp.get("command", "")
                s["code_edits"] += bash_writes_code(command)
                s["commits"] += bool(GIT_COMMIT.search(command))
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", default="", help="substring of the project folder name")
    parser.add_argument("--since", type=since_arg,
                        help="UTC start: YYYY-MM-DD or YYYY-MM-DDTHH:MM (default: 14 days ago)")
    args = parser.parse_args()
    since = args.since or (datetime.date.today() - datetime.timedelta(days=14)).isoformat()

    rows = []
    for project in sorted(os.listdir(PROJECTS)):
        if args.project.lower() not in project.lower():
            continue
        for main_file in glob.glob(os.path.join(PROJECTS, project, "*.jsonl")):
            started = first_timestamp(main_file)
            if not started or started[:len(since)] < since:
                continue
            name = project.replace("-Users-" + os.environ.get("USER", "") + "-", "")
            rows.append((started, name, os.path.basename(main_file)[:8], scan_session(main_file)))
    rows.sort()

    if not rows:
        print(f"No sessions matching '{args.project}' since {since}.")
        return

    print(f"{'started (UTC)':16}  {'project':24}  {'session':8}  {'edits':>5}  {'commits':>7}  {'subagents':>9}  skills (main | subagents)")
    for started, name, sid, s in rows:
        main_skills = ", ".join(sorted(s["main_skills"])) or "-"
        sub_skills = ", ".join(sorted(s["sub_skills"])) or "-"
        print(f"{started[:16]:16}  {name[:24]:24}  {sid:8}  {s['code_edits']:5}  {s['commits']:7}  {s['subagents']:9}  {main_skills} | {sub_skills}")

    worked = [s for *_, s in rows if s["code_edits"] or s["commits"]]
    print(f"\n{len(rows)} sessions since {since}, {len(worked)} with code edits or commits. Of those, sessions that invoked:")
    for skill in WATCHED:
        in_main = sum(skill in s["main_skills"] for s in worked)
        in_sub = sum(skill in s["sub_skills"] for s in worked)
        print(f"  {skill:32} {in_main:3} in the main session, {in_sub:3} in a subagent")
    agent_types = sum((s["agent_types"] for s in worked), collections.Counter())
    by_type = ", ".join(f"{name} {n}" for name, n in agent_types.most_common()) or "none"
    print(f"\nSubagents run in those sessions: {sum(s['subagents'] for s in worked)} ({by_type}).")
    print("Skills preloaded by an agent definition (implementer: tdd, verification-before-completion) are not Skill calls and are not counted above.")
    print("Edits counts Edit/Write calls on code files plus Bash commands that write one (>, tee, sed -i, Python open/write_text), one per command.")


if __name__ == "__main__":
    main()
