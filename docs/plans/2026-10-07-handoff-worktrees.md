# Plan: handoffs for parallel sessions in git worktrees

Goal: one handoff file per thread of work in the main checkout's `docs/handoffs/`, loaded by branch or chosen from a list at session start, so parallel worktree sessions and their successors can continue each other's work.

Spec: [docs/specs/2026-10-07-handoff-worktrees.md](../specs/2026-10-07-handoff-worktrees.md)
Branch: `feature/handoff-worktrees` (worktree `~/Developer/claude-skills-handoff-worktrees`). One PR.

## Global constraints

- Hooks run under macOS `/bin/bash` 3.2: no associative arrays, no `mapfile`/`readarray`, no `${var,,}`. Keep `#!/usr/bin/env bash` and `set -euo pipefail` in `handoff-load.sh`.
- Quote every variable. Never `eval` or execute content read from handoff files, branch names or file names.
- Main checkout = `dirname "$(git -C "$dir" rev-parse --path-format=absolute --git-common-dir)"`, `dir="${CLAUDE_PROJECT_DIR:-$PWD}"`. Linked worktree when `--git-dir` and `--git-common-dir` (both absolute) differ.
- Thread files: `<main>/docs/handoffs/<slug>.md`, slug `[a-z0-9-]+`. Overview: `<main>/docs/handoffs/_overview.md`. Legacy: `$dir/docs/handoff.md`.
- Fixed keys and values stay English: `# Handoff:`, `# Overview:`, `Status:`, `Updated:`, `Branch:`, `in-progress`, `done`, `## Next steps` and the other `##` headings.
- Keep today's framing lines of `handoff-load.sh` word for word where the spec does not change them (treat as notes, summarise-and-ask, `spec-first` line for `docs/plans/`, 14-day warning, `head -n 120`).
- Thread list: in-progress only, newest mtime first, at most 10 lines.
- Hook output goes to stdout; the hook always exits 0 when it has nothing to say.
- Tests must never touch real repos or `~/.claude`: everything in `mktemp -d`, removed by `trap`. Local git identity inside the temp repo.
- No new dependencies. `jq` is already required by the hooks.
- Repo files in English. Conventional commits, no `Co-Authored-By`.
- Skill behaviour changes are tested with subagents as `CLAUDE.md` says: baseline on `main`'s version first, then the worktree version at least 2 runs per scenario. Test subagents read the skill from the worktree path.

## Tasks

### Task 1: Test harness and loading a thread by branch

**In short:** a session in any worktree loads the handoff whose branch it is on, even after the old worktree is gone.

- Files: `tests/handoff-load.test.sh` (new), `hooks/handoff-load.sh`.
- Reuse: the existing body of `handoff-load.sh` becomes a function `load_file <path> <label>` used for every file the hook loads.
- Covers AC 1, 3, 8.
- Tests first (`tests/handoff-load.test.sh`, plain bash, own `assert_contains` / `assert_not_contains` / `assert_empty` helpers, exit 1 on any failure, prints a summary):
  - fixture: temp main repo with one commit, worktrees `wt-a` on `feature/a` and `wt-b` on `feature/b`; `docs/handoffs/` in the main checkout.
  - in-progress `a-thing.md` with `Branch: feature/a`: hook run with `CLAUDE_PROJECT_DIR=wt-a` prints the file content and the framing lines.
  - same file, `wt-a` removed with `git worktree remove` and a new worktree on `feature/a` created: still loaded.
  - the same file marked `Status: done`: not loaded.
  - no handoffs at all, in a worktree and in the main checkout: empty output, exit 0.
  - outside a git repo with no legacy file: empty output, exit 0.
- Done check: `bash tests/handoff-load.test.sh` → all pass; `bash -n hooks/handoff-load.sh` → no output.

### Task 2: List of open threads and branches open in another worktree

**In short:** when nothing matches the current branch, the session shows open threads and asks which one to continue.

- Files: `hooks/handoff-load.sh`, `tests/handoff-load.test.sh`.
- Reuse: `git worktree list --porcelain` for which branch is checked out where (`worktree`, `branch refs/heads/...`, `prunable` lines).
- Covers AC 2, 3, 4.
- Tests first:
  - from a third worktree on `cc/new`: two in-progress threads and one done thread → list has exactly the two, newest first, each with slug, branch, age, first `1.` item of `## Next steps`; the ask-the-user and "if the first message names a thread" lines are present; the done slug is absent.
  - a thread whose branch is checked out in `wt-b` → its line names `wt-b`'s path and says to continue in that session or close that worktree.
  - a thread whose worktree folder was deleted with `rm -rf` (registered but prunable) → its line mentions `git worktree prune`.
  - 12 in-progress threads → 10 lines listed.
  - detached HEAD → list shown, no crash.
- Done check: `bash tests/handoff-load.test.sh` → all pass.

### Task 3: Orchestrator overview, legacy file and compaction

**In short:** the main-folder session loads the orchestrator overview; old handoff files still load; compaction stays quiet.

- Files: `hooks/handoff-load.sh`, `tests/handoff-load.test.sh`.
- Reuse: `load_file` from Task 1; `jq -r '.source // empty'` on stdin, skipped when stdin is a terminal or `jq` is missing.
- Covers AC 5, 6, 7.
- Tests first:
  - main checkout on `main`, in-progress `_overview.md` → overview loaded, then the thread list, then the three-way question (orchestrate / take a thread / something new).
  - same overview from `wt-b` → overview not loaded; `_overview.md` never appears as a thread in the list.
  - overview with `Status: done` → not loaded.
  - legacy in-progress `docs/handoff.md` in the session folder, no match → loaded with today's framing, before the list.
  - legacy done → today's one-line note.
  - stdin `{"source":"compact"}`: with a branch match → file loaded; without a match → empty output.
  - stdin `{"source":"startup"}` and no stdin → same as today's startup.
- Done check: `bash tests/handoff-load.test.sh` → all pass.

### Task 4: Stop hook wording

**In short:** the long-session reminder asks for "the handoff of this thread" instead of the old file name.

- Files: `hooks/handoff-nudge.sh`, `tests/handoff-nudge.test.sh` (new, small).
- Covers AC 14.
- Tests first: a fake transcript above `HANDOFF_NUDGE_BYTES`, a unique `session_id` and `TMPDIR` set to a temp dir → output JSON has `decision: block` and a reason that mentions the handoff skill and does not mention `docs/handoff.md`; a second run with the same session → no output.
- Done check: `bash tests/handoff-nudge.test.sh` → all pass; `bash -n hooks/handoff-nudge.sh` → no output.

### Task 5: Handoff skill writes per-thread files and the orchestrator overview

**In short:** the handoff skill saves each thread's notes in the main folder, plus a separate overview for the orchestrator.

- Files: `skills/handoff/SKILL.md`.
- Reuse: keep the existing Rules, Format, language rules and the "After writing" structure; change location, naming, exclude, legacy move, overview, prompt.
- Covers AC 9, 10, 11, 12, 13.
- Tests first (subagents, per `CLAUDE.md`): baseline with `main`'s skill, then the worktree version, at least 2 runs each, in a temp repo with a main checkout and two worktrees:
  1. a worker session in `wt-a` on `feature/a` finishing a task → file lands in `<main>/docs/handoffs/<slug>.md` with `Branch: feature/a`, `docs/handoffs/` added to the common `info/exclude`, nothing written inside `wt-a`; prompt names the slug.
  2. the same thread continued on a new branch `feature/a-part-2` → same file, `Branch:` updated.
  3. a new thread whose natural slug is already taken by another in-progress thread → new file with a suffix; the other file untouched.
  4. a legacy `docs/handoff.md` in the worktree for the same work → content moved to the thread file, legacy file deleted, final message says so.
  5. an orchestrator session in the main checkout coordinating two workers → `_overview.md` with the thread table and merge queue; workers' thread files untouched.
- Done check: all five scenarios pass in both runs; record baseline vs new results in the PR description.

### Task 6: spec-first always commits spec and plan

**In short:** an epic's spec and plan go into git on the feature branch, so other worktrees can open them.

- Files: `skills/spec-first/SKILL.md` (step 4.3, and the order in step 5 if needed so the branch exists before the commit).
- Covers AC 15.
- Tests first (subagents): baseline and new version, 2 runs each, on a temp repo with no `docs/` in git: after spec approval and plan writing, are spec and plan committed on the feature branch? Baseline expected: left untracked.
- Done check: both new runs commit `docs/specs/...` and `docs/plans/...` on the feature branch.

### Task 7: README and final check

**In short:** the README describes the new handoff layout, the orchestrator overview and how to run the hook tests.

- Files: `README.md`.
- Covers documentation for all AC; housekeeping rule in `CLAUDE.md` (tables up to date).
- Tests first: none (docs). Check that every path in README exists.
- Done check: `bash tests/handoff-load.test.sh && bash tests/handoff-nudge.test.sh` → all pass; `bash -n hooks/*.sh`; links in README resolve (`grep -o '](\([^)]*\))' README.md` paths exist).

## After merge

1. `git -C ~/Developer/claude-skills pull`, remove the worktree and branch as in `CLAUDE.md`.
2. Build `~/Downloads/handoff.zip`, I re-upload it to claude.ai, then `diff -r` against the app's copy.
