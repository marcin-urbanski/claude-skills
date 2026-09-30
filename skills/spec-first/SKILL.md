---
name: spec-first
description: Plan code changes before writing them, scaled to the size of the task. Use when starting a feature, a behaviour change, a new module or a larger project in a codebase. A small fix goes straight to tdd; a feature gets a short spec in chat with acceptance criteria and a task list; an epic gets a spec and plan in docs/ and task-by-task execution with independent review. Not for questions, explanations or one-off scripts.
---

# Spec-first

Agile in miniature: agree what "done" means, find what already exists, split the work into small testable tasks, build each task with `tdd`, review, open a PR.

## 1. Size the task

Say the size in one line so the user can correct it, then follow that path.

| Size | Looks like | Path |
|---|---|---|
| **Fix** | bug, typo, config value, a change inside one function | No spec. Reuse check, then `tdd` (or `systematic-debugging` for a bug). |
| **Feature** | a user story: new endpoint, form, screen, integration step | Short spec **in chat** → user approves → task list in chat → build with `tdd` |
| **Epic** | new module, several stories, schema redesign, anything spanning sessions | Spec file → user approves → plan file → build task by task with review per task |

If a fix turns out bigger than it looked, stop and say so, then move up a size. Do not ask for approval of a fix; just do it well.

## 2. Reuse check (every size, before designing anything)

The worst outcome is rebuilding something the project already has. Before proposing new code:

1. Search the codebase for what already does this or something close: services, helpers, components, traits, hooks, validators, API clients, migrations, config. Search by domain words and by likely names (`grep`/`rg`, the framework's usual folders, existing tests).
2. Check installed dependencies (`composer.json`, `package.json`, framework built-ins) before adding a library or writing a utility.
3. In the spec or in chat, list what you will **reuse**, what you will **extend**, and what is genuinely **new**, with file paths. Anything new must say why the existing code does not fit.

If existing code nearly fits, extend it rather than write a parallel version. If it is broken, fix it rather than work around it. Never leave two implementations of the same thing.

## 3. Feature: spec in chat

Keep it to what the user needs to approve (about 10–25 lines):

- **Story**: who wants what, and why (one or two sentences).
- **Acceptance criteria**: 3–7 checkable statements ("Given…, when…, then…" or plain bullets). These become the tests.
- **Reuse**: from step 2.
- **Approach**: files to touch, data changes, anything the user must decide.
- **Security**: what input is untrusted, who may do this (authorisation), what data is sensitive. Write "none" only if that is true.
- **Out of scope**: what you will not do.

Ask only questions whose answers change the design, and ask them before the spec, one message with all of them. Then wait for approval. After approval, give a numbered task list (each task small enough for one red-green-refactor cycle or a few) and start.

## 4. Epic: spec and plan files

1. Write the spec to `docs/specs/YYYY-MM-DD-<topic>.md` with the same sections as above, plus data model, integrations, error handling and migration/rollout where relevant. Ask the user to review it; wait for approval.
2. Write the plan to `docs/plans/YYYY-MM-DD-<topic>.md`:
   - Header: goal, link to the spec, branch name, global constraints (exact values, formats, security rules every task must respect).
   - Tasks, each with: files, what to reuse, acceptance criteria covered, the tests to write first, and a done check (command + expected result).
   - Tasks ordered so each leaves the app working and tests green.
3. Commit spec and plan on the feature branch only if the project keeps docs in git; otherwise leave them untracked.

Follow the project's CLAUDE.md for locations if it names others.

## 5. Build

Create the branch first (per global git rules). Then, per task:

**Default (fix, feature):** do the task in this session with `tdd`, then a self-review against `reviewer-checklist.md` in this folder: reuse, security, best practices, spec compliance. Fix what you find. Commit with a conventional message. Next task.

**Epic:** for each task, dispatch one implementer subagent and then one fresh reviewer subagent:

- Implementer prompt: the task text from the plan, global constraints, the reuse list, "follow TDD, show RED and GREEN output, commit when green, report files changed and anything unclear". It must not spawn subagents.
- Reviewer prompt: `reviewer-prompt.md` in this folder, filled in with the task, constraints and the commit range. The reviewer is read-only.
- Critical or Important findings go back to the implementer; re-review only the fix. Minor findings are listed for the user.
- Do not trust any report: check `git diff` and the test output yourself before moving on.

Use `handoff` between sessions on epics.

## 6. Finish (every size)

1. `verification-before-completion`: full test suite, linters/static analysis the project uses, build if there is one. Read the output.
2. Independent review of the whole branch: dispatch one reviewer subagent with `reviewer-prompt.md` against `main...HEAD`. For a one-line fix, the self-review checklist is enough.
3. Walk through the acceptance criteria one by one and say how each is met (test name or manual check).
4. Push and open the PR with `gh pr create`: summary, acceptance criteria with status, reuse decisions, security notes, anything the reviewer flagged that you did not fix. Do not merge.
