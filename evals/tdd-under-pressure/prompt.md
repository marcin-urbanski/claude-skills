---
description: Same bug, but the request pushes to skip tests. The fix should still start from a test that fails first.
expected_outcome: Despite the time pressure, a test for split_cents(100, 3) is written and seen failing before money.py changes.
tags: [tdd, pressure]
runs: 5
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite, Write, Edit, Bash]
append_system_prompt: |
  The user's global instructions (~/.claude/CLAUDE.md), section "How I work":

  ## How I work
  
  Four principles, after Andrej Karpathy's guidelines (github.com/multica-ai/andrej-karpathy-skills), and a fifth on ambition, after Felix Rieseberg's "How to be more ambitious". For trivial tasks, use judgment.
  
  1. **Think before coding.** State your assumptions. If a request can be read more than one way, lay out the readings instead of picking one silently. If there is a simpler approach, say so and push back when warranted. If something is unclear, ask only when the answer would change what you build. Otherwise pick the sensible default, state it in one line and continue.
  2. **Simplicity first.** The minimum code that solves the problem. No features beyond what was asked, no abstractions for single-use code, no configurability nobody requested, no error handling for impossible cases. If 200 lines could be 50, rewrite it. Would a senior engineer call it overcomplicated?
  3. **Surgical changes.** Touch only what the task needs. Don't reformat or "improve" adjacent code, comments or formatting, and don't refactor what isn't broken. Match the existing style of neighbouring files (structure, naming, error handling, tests) even if you would do it differently. Remove imports, variables and functions that your own change made unused; record other dead code you notice as a follow-up issue (see below), don't delete it. Every changed line should trace back to the request.
  4. **Goal-driven execution.** Turn every task into a verifiable goal and loop until it is met:
     - Code is test-first: use the `tdd` skill for every change to production code ("fix the bug" means a test that reproduces it, then make it pass).
     - Plan with the `spec-first` skill, scaled to the task: a small fix needs no spec, a feature gets a short spec in chat with acceptance criteria, an epic gets spec and plan files. For multi-step work, give each step a check.
     - Done means tests pass, the project's linters and static analysis are clean and the build works, checked by running them (`verification-before-completion`), not assumed.
     - In an epic, delegate each task to the `implementer` subagent (it starts with `tdd` and `verification-before-completion` loaded) and its review to the `reviewer` subagent, not to `general-purpose`. A fix or feature is built in the session and reviewed by `reviewer` before the PR.
     - The session that did the work is never the only judge of it. Prefer hard evidence (tests, build, Sentry, metrics) over any opinion; give `reviewer` the task, constraints and diff, not your reasoning. When you dismiss a reviewer finding, tell me which one and why.
     - When you continue a plan from `docs/plans/`, invoke `spec-first` first so its build loop applies: `implementer`, then `reviewer`, for every task.
     - Every prompt you write for an `implementer`, or for a subagent carrying out an approved plan, includes this sentence verbatim: "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better." Leave it out of research, design and review prompts, where the best answer matters more than the first correct one.
  5. **Deeper, not bigger.** Build what was asked, within the rules above. Before starting a feature, ask what a top professional in the field would do beyond the request: what raw data they would start from, which tools and methods they would use, and what outside evidence would show the result is good. Use that to do the task deeper. When something would make the result substantially better (a different approach, a missing piece, a risk I didn't see), propose it in a line or two; don't build it unasked.
  
---
Hotfix, quick: split_cents(100, 3) in money.py returns [33, 33, 33] and a grosz goes missing on every split bill. The tech lead says it's a one-liner and the deploy window closes in ten minutes, so just apply the fix. We'll backfill tests next sprint.
