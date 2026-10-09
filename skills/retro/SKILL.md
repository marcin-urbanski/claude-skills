---
name: retro
description: Retrospective on a coding session, and optionally its PR review comments. Proposes changes to the agent's environment (automated checks, coding standards, reviewer checklist, skills, CLAUDE.md, tool access) so the same mistake cannot happen again. Proposes only; nothing changes until the user picks.
disable-model-invocation: true
---

# Retro

Adapted from Matt Pocock's `retro` skill (mattpocock/skills, MIT).

A retro changes the **environment**, never the code from the session. For every place the session struggled, ask what in the environment allowed it, and propose the check, rule or pointer that prevents it next time. A bug in the code itself is a follow-up issue (global CLAUDE.md), not a retro finding.

The goal is that a human never writes the same review comment twice.

## Steps

1. **Read the session.** Run the digest in this skill's folder:
   ```bash
   python3 ~/.claude/skills/retro/digest.py [session-id or path]
   ```
   With no argument it takes the newest session of the current directory, which is this session. The user may name another one. If this session is already long, suggest running `/retro` from a fresh session on this one's id instead. The digest lists subagents at the end: digest the ones with errors too. Open the raw `.jsonl` only to read a specific moment the digest points at.
2. **Read the PR review**, when the user names a PR or the session opened one:
   ```bash
   gh pr view <n> --comments
   gh api repos/{owner}/{repo}/pulls/<n>/comments --jq '.[] | {path, line, body}'
   ```
   Every human review comment is a candidate. It ends as a check, a rule, or a stated decision that it was a one-off.
3. **Read the environment** before proposing anything, so you extend what exists instead of reinventing it:
   - the project's `CLAUDE.md` / `AGENTS.md` and `CODING_STANDARDS.md` (or `CONTRIBUTING.md`);
   - its check commands: `composer.json` / `package.json` scripts, `Makefile`, CI workflows, pre-commit config, `.claude/settings.json` hooks;
   - the global `~/.claude/CLAUDE.md` and the skills and agents the session used (sources in `~/Developer/claude-skills`).

   A check that exists but is not wired into CI or a hook is the finding. A repo with no guardrail at all (no pre-commit hook and no CI job running lint, static analysis and tests) is a finding of its own.
4. **Find the moments**: errors, `[repeat]` calls, long searches for a file or fact, `[result Nk chars]` reads, places where the user corrected the agent or said the same thing twice, review comments, and anything the reviewer subagent missed that a human caught.
5. **Trace each moment to its cause** and place the fix with the table below. Drop any candidate you cannot tie to a specific moment: generic advice is noise.
6. **Present the candidates**, most severe first. Severity order: a shipped bug or security gap, then work a human had to redo or review twice, then wasted time or tokens, then friction. For each candidate:
   - **Moment**: time from the digest and a one-line quote or description;
   - **Cause**: what in the environment allowed it;
   - **Change**: the target file and the exact rule text, check or pointer to add, change or delete.
7. **Stop and let the user pick.** Apply only what they choose. Changes to skills, agents or the reviewer checklist go through a worktree as `~/Developer/claude-skills/CLAUDE.md` describes; changes to a project go on a branch per its rules.

## Where a fix belongs

| What happened | Fix | Where |
|---|---|---|
| A mistake a tool could catch (banned API, import shape, file location, naming pattern, formatting) | Automated check | The project's linter or static analysis rule, a pre-commit hook, a CI job, or a Claude Code hook in `.claude/settings.json` |
| The reviewer missed a judgement call specific to this project | Rule | The project's `CODING_STANDARDS.md` (create it if missing) |
| The reviewer missed a judgement call that applies to every project | Rule | `skills/spec-first/reviewer-checklist.md` in claude-skills |
| A long search for a file, command or fact | Navigation pointer | One line in a file the agent already reads (`CLAUDE.md`, a skill), naming where the thing lives |
| A skill or agent did the wrong thing, or skipped a step | Skill fix | The skill or agent file in claude-skills |
| A crucial fact was out of reach (server logs, a third-party service, test output) | Information access | Write logs to a file, add read-only access, or a script that fetches it |
| An expensive tool call (huge output, many retries of the same call) | Tool economy | A narrower command, a script, or a flag that trims output |
| A rule in `CLAUDE.md` that implementation does not need | Move it | To the reviewer (standards or checklist) or to a check; keep `CLAUDE.md` for navigation pointers |
| A steering line the model already obeys without being told | No-op | Delete the sentence |

Prefer a check over prose: a failing check holds every time, a sentence holds when the model notices it. Write prose only for genuine judgement calls.

Coding standards belong to the reviewer, not the implementer. The implementer explores, writes and debugs, so every extra rule in its context costs. The reviewer receives a diff and has room for rules. Each line in `CLAUDE.md` loads into every session, so a new line there must earn it.

## Writing the proposed text

- State the target behaviour ("store money as integer cents"); a prohibition alone puts the wrong behaviour in front of the model.
- One meaning in one place: when a rule already exists, sharpen it instead of adding a second one.
- Cut what the environment already says (config, scripts, directory layout); restate only what the agent cannot find by looking.
- A retro sees one session, so it cannot tell whether an old rule or check is obsolete. Flag a line for deletion only when this session shows it changed nothing.
