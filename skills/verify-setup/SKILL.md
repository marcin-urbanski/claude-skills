---
name: verify-setup
description: Give a project its own verify skill in .claude/skills/verify - how to start the app with safe data, drive the flow that changed and read the result, a feature map of what to check, and checks.sh with the fast checks the verify-gate hook runs when Claude finishes a turn. Use when a project has no .claude/skills/verify, when a change could not be checked in the running app (a report or PR says not verified), when the user asks to set up verification, end-to-end checks or a smoke test, or when a verify skill is slow, flaky or missed a bug that reached the user.
---

# Verify setup

Tests can pass while the feature is broken, because the test and the code were written with the same misunderstanding. The check that catches it is the one a person would do: start the app, use the changed flow, look at the result. This skill writes that check down per project, so every session runs it the same way, fast and reliably.

It writes two files in the project's repo, which the project commits like any other code:

- `.claude/skills/verify/SKILL.md`: the project's verify skill, from `${CLAUDE_SKILL_DIR}/verify-template.md`. Claude Code loads it from the repo for anyone who clones it.
- `.claude/skills/verify/checks.sh`: the fast checks. The `verify-gate` hook in this plugin runs it whenever Claude finishes a turn that changed the repo, and sends Claude back when it fails.

An existing verify skill is improved, never replaced by a second one.

## 1. Read the project

- `CLAUDE.md`, README, build files (`package.json`, `composer.json`, `Package.swift`, `Makefile`), the CI workflow and the scripts folder. What CI runs is the starting point for `checks.sh`.
- Reuse what exists: a script that starts, seeds or screenshots the app is called from the verify skill, never rewritten. Claude Code's built-in `run` skill covers launching common project types; the verify skill adds what is specific to this project.
- Find safe data: a demo, seed or fixture mode, a test database, a local environment. The verify skill never uses real user data or production. If there is none, say so and propose the smallest seed the flows need.
- Pick the tool that drives this kind of app: the browser tools for a web app, the iOS Simulator tools for an iPhone app, the project's UI test or screenshot scripts (or computer use) for a Mac app, and for a backend or CLI, running it locally and calling it (`curl`, the CLI itself).

## 2. Write checks.sh

- Fast and deterministic: unit tests, linter, type checks. Aim for under a minute, because it runs at the end of every turn that changed code. A full build, end-to-end runs and anything slower stay in the verify skill and CI.
- `#!/usr/bin/env bash`, `set -euo pipefail`, then `cd "$(dirname "$0")/../../.."` so it runs from the repo root. Exit non-zero on any failure and print the failing lines: Claude sees the last 40 lines of output.
- No prompts, no network beyond package registries, no reading secrets, no writes outside the repo's build folders.
- The hook runs the copy committed on the base branch, so a branch cannot weaken the check that judges it. An edit to `checks.sh` takes effect for the gate once it is merged; on a branch that adds the file, the working copy runs.

## 3. Write the verify skill

Fill in the template. It has four parts: **Start** (exact commands, how to tell the app is up, how to stop it), **Drive** (how to reach each flow), **Inspect** (what to read afterwards: the screenshot, runtime errors or console log, a database query, the response) and the **Feature map**.

The feature map lists the main user flows, five to fifteen rows: the flow in the user's words, how to reach it (URL, menu path, shortcut, demo state, command) and the expected result. It is both the guide for driving the app and the rubric for "done". Start with the flows the project's recent bugs and PRs touched.

## 4. Stress-test it before calling it done

1. Run `checks.sh` three times. Same result each time; note how long it takes.
2. From a clean state (app not running), follow the verify skill on one flow from the map three times. Same outcome each time.
3. Break that flow on purpose with a change a user would notice, run the verify skill again and confirm it reports the break (and `checks.sh`, when a test covers it). Restore the code.
4. A flaky step gets its cause fixed: wait for a condition instead of a fixed delay, freeze the clock, seed fixed data. Never add retries or sleeps until it passes.

Report the durations, the break you made and how it was caught, and every step that needed the user (a permission to grant, a sign-in) as a TODO for them.

## 5. Keep it working

- When a bug reaches the user that the verify skill should have caught, add its flow to the feature map or a test to `checks.sh`, in the same PR as the fix.
- Drop flows that no longer exist. A map that only grows gets slow and stops being read.

## Safeguards

- Never write real data or secrets into either file. Refer to a secret by its variable name or by where the team keeps it.
- Never add `allowed-tools` or hooks to the project skill's frontmatter. A project skill's `allowed-tools` apply even in a folder nobody trusted.
- Mark each step that writes data outside the app's own demo or test data **writes data**, and each step that sends data outside the machine **sends data out**.
