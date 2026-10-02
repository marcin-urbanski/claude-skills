#!/usr/bin/env python3
"""Report which skills Claude Code invoked, per session, from the local transcripts.

Usage:
    scripts/skill-usage.py                       # all projects, last 14 days
    scripts/skill-usage.py TimeTracker           # projects whose folder name contains "TimeTracker"
    scripts/skill-usage.py TimeTracker --since 2026-09-30
"""
import argparse
import datetime
import glob
import json
import os
import re

PROJECTS = os.path.expanduser("~/.claude/projects")
WATCHED = ["spec-first", "tdd", "systematic-debugging", "verification-before-completion", "handoff"]
CODE_FILE = re.compile(r"\.(php|js|jsx|ts|tsx|vue|swift|py|rb|go|rs|css|scss|sql)$")
GIT_COMMIT = re.compile(r"(^|&&|;|\n)\s*git commit\b")


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
    s = {"main_skills": set(), "sub_skills": set(), "code_edits": 0, "commits": 0, "subagents": len(files) - 1}
    for path in files:
        skills = s["main_skills"] if path == main_file else s["sub_skills"]
        for name, inp in tool_uses(path):
            if name == "Skill":
                skills.add(inp.get("skill", "?").split(":")[-1])
            elif name in ("Edit", "Write", "MultiEdit") and CODE_FILE.search(inp.get("file_path", "")):
                s["code_edits"] += 1
            elif name == "Bash" and GIT_COMMIT.search(inp.get("command", "")):
                s["commits"] += 1
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", default="", help="substring of the project folder name")
    parser.add_argument("--since", help="YYYY-MM-DD (default: 14 days ago)")
    args = parser.parse_args()
    since = args.since or (datetime.date.today() - datetime.timedelta(days=14)).isoformat()

    rows = []
    for project in sorted(os.listdir(PROJECTS)):
        if args.project.lower() not in project.lower():
            continue
        for main_file in glob.glob(os.path.join(PROJECTS, project, "*.jsonl")):
            started = first_timestamp(main_file)
            if not started or started[:10] < since:
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
    print(f"\nSubagents run in those sessions: {sum(s['subagents'] for s in worked)}.")
    print("Edits counts Edit/Write calls on code files only; code written through Bash (sed, heredocs) is not counted.")


if __name__ == "__main__":
    main()
