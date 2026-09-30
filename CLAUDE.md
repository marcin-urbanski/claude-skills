# claude-skills

This repo is the source of truth for my Claude skills (`handoff`, `spec-first`, `tdd`, `systematic-debugging`, `verification-before-completion`, `ux-principles`) and the `handoff` hooks (`handoff-load.sh`, `handoff-nudge.sh`). Files in this repo (skills, README, commits) are written in English.

## How the repo is wired to Claude

- `~/.claude/skills/<skill>` and `~/.claude/hooks/*.sh` are symlinks into `~/Developer/claude-skills`. Every Claude Code session on this Mac loads whatever is checked out there, uncommitted edits included.
- `ux-principles` has no local symlink. It reaches Claude through claude.ai sync. `handoff` is both symlinked and uploaded to claude.ai.
- `~/.claude/skills/synced/` has not updated since 21.09 and has no effect on the app. Ignore it.

## Branches and worktrees

`~/Developer/claude-skills` always stays on `main`. Do all changes in a separate worktree, so sessions never load a work-in-progress branch:

```bash
git worktree add ../claude-skills-<name> -b feature/<name> main
```

Commit, push and open the PR from the worktree. After I merge the PR:

```bash
git -C ~/Developer/claude-skills pull
git -C ~/Developer/claude-skills worktree remove ../claude-skills-<name>
git -C ~/Developer/claude-skills branch -d feature/<name>
```

The change reaches sessions only after that `pull`, because the symlinks point at `~/Developer/claude-skills`. GitHub deletes the remote branch on merge. `branch -d` refuses to delete a branch that is not merged, so if it fails, stop and tell me instead of forcing it with `-D`.

## After changing `handoff` or `ux-principles`

These two also live in claude.ai, so a change is not live there until re-uploaded.

1. Build a ZIP whose top-level folder is named after the skill, from the checkout that has the change (the worktree, or `~/Developer/claude-skills` after the pull):
   ```bash
   cd skills && zip -r ~/Downloads/<skill>.zip <skill> -x '*.DS_Store'
   ```
2. I delete the old skill in claude.ai (Customize → Skills) and upload the ZIP.
3. Check the app's copy matches the repo:
   ```bash
   ls -dt ~/Library/Application\ Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/<skill>
   diff -r <newest path from above> skills/<skill>
   ```
   There are several `skills-plugin/*/*` folders, so the skill can show up more than once. Check the newest.

`ux-principles/SKILL.md` ends with a `## Sources` section. Keep it: claude.ai gets the skill folder without the README, so the credits must live in the skill itself.

## Testing skill changes

Test every change to a skill's behaviour with subagents:

1. Baseline first: run a subagent on each scenario the change targets with the current version (the one on `main`) and record what it does.
2. Make the change in the worktree. The installed skill is still `main`'s, so tell the test subagents to read the skill from the worktree path.
3. Run each scenario at least 2 times with the new version, or 5 times when the change is only rewording, and compare with the baseline.

When a skill misbehaves in real use but not in tests, read the real transcripts in `~/.claude/projects/<project>/*.jsonl` (the folder name is the project path with `/` replaced by `-`) to see what the model actually did.

## What stays out of this repo

- `humanize-text`: its sources' licences are unclear.
- Emil Kowalski's animation skills (`animate`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `review-animations` in `~/.claude/skills`): they are copies of [emilkowalski/skills](https://github.com/emilkowalski/skills).

If asked to publish all skills, list these exclusions with their reasons and ask before going further.

## Housekeeping

- When adding, renaming or removing a skill or hook, update the tables in `README.md`.
- Adapted skills keep their credit in `README.md` and `THIRD_PARTY_NOTICES.md`.
