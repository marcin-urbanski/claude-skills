---
name: handoff
description: Write or update docs/handoff.md so the next Claude Code session can continue this work from a clean context. Use when the user says handoff, wrap up, save progress, or before /clear on unfinished work, when a task or part of a plan is finished and the rest continues in a new session, or when a hook asks for a handoff.
---

# Handoff

Write the state of the current work to `docs/handoff.md` in the project root, so a fresh session can pick it up without re-reading this conversation. Then give the user a prompt to paste into that session.

## Rules

- **Overwrite** the file. It describes the current state, not a history. Git holds the history.
- Keep it **under 80 lines**. Be specific: file paths, function names, commands, exact errors. No narrative.
- Only include what the next session needs. Leave out anything already in `CLAUDE.md`.
- Never include secrets, API keys, passwords or `.env` values.
- **Status** is about the whole goal, not the last task. Finishing one task, subtask or part of a plan is `in-progress`. Use `done` only when nothing is left in Next steps; then keep only Goal and Done.
- **Plan in progress** (an epic from `spec-first`, file in `docs/plans/`): name the plan and spec files and list only the remaining tasks, each as `Task N: <short description>`, numbered as in the plan (for example `Task 5.2`) and with "Task" in the conversation's language. The description is the task's **In short** line from the plan, or, if it has none, one short plain sentence (about 15 words) written from the task's text: the gist of what the user will see or get, not a list of features, no codes or type names they would have to look up, and never only the title. The plan holds the details; do not copy anything else from it.
- **Language**: write the content in the language of this conversation. These parts stay exactly as in the template in every language (the SessionStart hook reads `Status:`, and a fixed layout keeps handoffs comparable): the `# Handoff:` title prefix, the `Status:`, `Updated:` and `Branch:` keys, the values `in-progress` and `done`, and the `##` section headings.

## Before writing

1. Check `git status` and `git diff --stat` so "Done" reflects what actually changed.
2. If `docs/` does not exist, create it.
3. Keep the file out of the repo: if `docs/handoff.md` is not already ignored, add it to `.git/info/exclude` (local only, never committed). Do not edit `.gitignore` unless the user asks.

## Format

```markdown
# Handoff: <short task name>

Status: in-progress | done
Updated: <YYYY-MM-DD HH:MM>
Branch: <current git branch>

## Goal
One or two sentences: what we are building or fixing, and what "done" looks like.

## Done
- <change> (`path/to/file`)

## Next steps
1. <first concrete action, with file/function>
2. ...

## Decisions and constraints
- <decision made and why; things the user ruled out>

## Gotchas
- <what failed or misled us, so the next session does not repeat it>

## Verify with
- `<command>`: <what a pass looks like>
```

## After writing

A SessionStart hook loads `docs/handoff.md` automatically, but only when the new session starts in the same folder as the file.

Your final message, including the prompt, is in the language of this conversation and has exactly these parts:

1. **One line**: where the handoff was written.
2. **The prompt**, in a fenced `text` block. Choose the form by where the next session will start:
   - **Same folder** (the default when the user names no other place): 1–3 lines. Name the one next step from Next steps, and for a plan also the plan file and that `spec-first` comes first. Shape: `<continue from docs/handoff.md and docs/plans/<plan>.md>. <invoke spec-first, then start with task N: short description>.`
   - **Different folder, another tool, or the handoff sits in a folder that will be deleted** (for example an app scratch workspace): the hook will not find the file, so the prompt must stand alone. Include the target folder, the goal, the next steps and the decisions and constraints, taken from the handoff, and for a plan, that `spec-first` comes first. Up to about 25 lines.
3. **One line on how to start**: `/clear` or a new session in the same folder, or "open a new session in <folder> and paste the prompt". Say the handoff loads automatically only in the same-folder case.

If `Status: done`, skip the prompt: say the work is finished and the handoff is marked done.
