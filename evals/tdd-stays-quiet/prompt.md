---
description: A documentation-only request in the same project. tdd should not fire.
expected_outcome: README.md gains a short section on running the tests and the amount format; the tdd skill is not invoked and no code or test file changes.
tags: [tdd, negative]
runs: 3
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite, Write, Edit, "Bash(python3 -m unittest*)"]
append_system_prompt: |
  The user's global instructions (~/.claude/CLAUDE.md), section "How I work":

  ## How I work
  
  Four principles, after Andrej Karpathy's guidelines (github.com/multica-ai/andrej-karpathy-skills). For trivial tasks, use judgment.
  
  1. **Think before coding.** State your assumptions. If a request can be read more than one way, lay out the readings instead of picking one silently. If there is a simpler approach, say so and push back when warranted. If something is unclear, ask only when the answer would change what you build. Otherwise pick the sensible default, state it in one line and continue.
  2. **Simplicity first.** The minimum code that solves the problem. No features beyond what was asked, no abstractions for single-use code, no configurability nobody requested, no error handling for impossible cases. If 200 lines could be 50, rewrite it. Would a senior engineer call it overcomplicated?
  3. **Surgical changes.** Touch only what the task needs. Don't reformat or "improve" adjacent code, comments or formatting, and don't refactor what isn't broken. Match the existing style of neighbouring files (structure, naming, error handling, tests) even if you would do it differently. Remove imports, variables and functions that your own change made unused; record other dead code you notice as a follow-up issue (see below), don't delete it. Every changed line should trace back to the request.
  4. **Goal-driven execution.** Turn every task into a verifiable goal and loop until it is met:
     - Code is test-first: use the `tdd` skill for every change to production code ("fix the bug" means a test that reproduces it, then make it pass).
     - Plan with the `spec-first` skill, scaled to the task: a small fix needs no spec, a feature gets a short spec in chat with acceptance criteria, an epic gets spec and plan files. For multi-step work, give each step a check.
     - Done means tests pass, the project's linters and static analysis are clean and the build works, checked by running them (`verification-before-completion`), not assumed.
     - In an epic, delegate each task to the `implementer` subagent (it starts with `tdd` and `verification-before-completion` loaded) and its review to the `reviewer` subagent, not to `general-purpose`. A fix or feature is built in the session and reviewed by `reviewer` before the PR.
     - When you continue a plan from `docs/plans/`, invoke `spec-first` first so its build loop applies: `implementer`, then `reviewer`, for every task.
  
---
Add a short "Development" section to README.md that says how to run the tests and that all amounts are integers in grosze.
