---
name: handoff
description: Write or update this thread's handoff file in docs/handoffs/ in the repo's main checkout (or, for an orchestrator session, docs/handoffs/_overview.md) so the next Claude Code session, in any worktree of the repo, can continue this work from a clean context. Use when the user says handoff, wrap up, save progress, or before /clear on unfinished work, when a task or part of a plan is finished and the rest continues in a new session, or when a hook asks for a handoff.
---

# Handoff

Write the state of the current work to this thread's handoff file, so a fresh session can pick it up without re-reading this conversation. Then give the user a prompt to paste into that session.

A **thread** is one line of work with a goal (for example "best score"); it may span several branches, one per PR of a plan. Each thread has one file, `docs/handoffs/<slug>.md`, in the repo's **main checkout**: `dirname "$(git rev-parse --path-format=absolute --git-common-dir)"`, the same folder from every worktree of the repo. Never write a handoff inside a linked worktree: it is deleted with the worktree. Not a git repo: use `docs/handoffs/<slug>.md` in the current folder.

## Rules

- **Overwrite** the file. It describes the current state, not a history. Git holds the history.
- Keep it **under 80 lines**. Be specific: file paths, function names, commands, exact errors. No narrative.
- Only include what the next session needs. Leave out anything already in `CLAUDE.md`.
- Never include secrets, API keys, passwords or `.env` values.
- **Branch** is the branch this thread's commits are on, normally the current branch (`git branch --show-current`), so the file follows a plan onto its next branch. Not a git repo: `none`.
- **Status** is about the whole goal, not the last task. Finishing one task, subtask or part of a plan is `in-progress`. Use `done` only when nothing is left in Next steps; then keep only Goal and Done.
- **Plan in progress** (an epic from `spec-first`, file in `docs/plans/`): the plan and spec are committed on the thread's branch, so name them by repo path (`docs/plans/<plan>.md`); a new session gets them after `git switch <branch>`. If the plan is untracked (older epics), say so under Gotchas. List only the remaining tasks, each as `Task N: <short description>`, numbered as in the plan (for example `Task 5.2`) and with "Task" in the conversation's language. The description is the task's **In short** line from the plan, or, if it has none, one short plain sentence (about 15 words) written from the task's text: the gist of what the user will see or get, not a list of features, no codes or type names they would have to look up, and never only the title. The plan holds the details; do not copy anything else from it.
- **Other threads' files**: never edit, overwrite or delete them.
- **Language**: write the content in the language of this conversation. These parts stay exactly as in the template in every language (the SessionStart hook reads `Status:`, `Branch:` and `## Next steps`, and a fixed layout keeps handoffs comparable): the `# Handoff:` and `# Overview:` title prefixes, the `Status:`, `Updated:` and `Branch:` keys, the values `in-progress` and `done`, and the `##` section headings.

## Which file

If this session is the orchestrator, write `_overview.md` (see Orchestrator below). Otherwise, the first that applies:

1. The thread file in `docs/handoffs/` that the SessionStart hook loaded (not merely listed) and this session continued, or that the user asked this session to continue. This holds after you switched to a new branch too.
2. An in-progress thread file whose `Branch:` is the current branch (the newest, if several), only if this session worked on that thread's goal.
3. A new file. Slug: kebab-case `[a-z0-9-]` from the task name (`best-score`), never from the branch. If `<slug>.md` already exists, it belongs to another thread (done or not): use `<slug>-2`, `<slug>-3`, ..., the first that is free.

## Before writing

1. Check `git status` and `git diff --stat` so "Done" reflects what actually changed.
2. Create `<main checkout>/docs/handoffs/` if it does not exist.
3. Keep handoffs out of the repo: if `git check-ignore -q docs/handoffs/` fails, append the line `docs/handoffs/` to `<git common dir>/info/exclude` (local, shared by all worktrees, never committed). Do not edit `.gitignore` unless the user asks. Not a git repo: skip this.
4. **Legacy file**: if the session's folder has `docs/handoff.md` (the old single-file handoff) for the same work, for example because the hook loaded it, carry its still-relevant content (decisions, gotchas, next steps) into the file you write, then delete `docs/handoff.md`. If it describes other unfinished work, leave it.

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

## Orchestrator

The orchestrator is a session that coordinates worker sessions in other worktrees; it usually runs in the main checkout, and the hook loaded `_overview.md` for it. It writes `<main checkout>/docs/handoffs/_overview.md` instead of a thread file, and reads the workers' thread files for their state but never edits them. Worker sessions never write `_overview.md`. The orchestrator does not run `spec-first`'s build loop itself; the workers do. The Rules above apply; Status is `done` when every thread is merged or dropped.

```markdown
# Overview: <short goal>

Status: in-progress | done
Updated: <YYYY-MM-DD HH:MM>
Branch: <current git branch>

## Goal
One or two sentences.

## Plan
- `docs/plans/<plan>.md`, `docs/specs/<spec>.md`, committed on `<branch>` (or: none)

## Threads
| Thread | Branch | Worktree | Current task | State |
|---|---|---|---|---|
| <slug> | <branch> | <path> | Task N: <short description> | working / PR open <link> / merged / not started |

## Waiting to merge
1. <PR link>: <what it adds; merge order or dependency>

## Next steps
1. <first concrete action>

## Decisions and constraints
- <decision made and why>
```

## After writing

Your final message, including the prompt, is in the language of this conversation and has exactly these parts:

1. **One line**: the full path of the file written, plus, if you found a legacy `docs/handoff.md`, that you moved and deleted it (or left it because it describes other work).
2. **The prompt**, in a fenced `text` block. The shapes below are in English, but write the whole prompt in the conversation's language; only the slug and file paths stay as they are.
   - **Same repo** (the default, any worktree or the main checkout): 1–3 lines naming the slug and the one next step. Shape: `Continue thread <slug> (<absolute path of the thread file>). <for a plan: invoke spec-first, then start with Task N: short description>.` Orchestrator: `Continue orchestrating from <absolute path of _overview.md>; the workers run spec-first, not this session.` plus the next step.
   - **Another repo, another tool, or no git**: the hook will not find the file, so the prompt must stand alone. Include the target folder, the goal, the next steps and the decisions and constraints, taken from the handoff, and for a plan, that `spec-first` comes first. Up to about 25 lines.
3. **How to start**, one or two lines. The hook loads the thread file in any worktree on its branch and otherwise lists it, so the prompt picks it. A branch is checked out in one worktree only: if it still is here, offer `/clear` here, or close this worktree first (archive this session if the app removes its worktree, or `git worktree remove <path>` from the main checkout; in the main checkout, switch branch) and start a new session. Orchestrator: `/clear` or a new session in the main checkout. Stand-alone: "open a new session in <folder> and paste the prompt".

If `Status: done`, skip the prompt: say the work is finished and the handoff is marked done.
