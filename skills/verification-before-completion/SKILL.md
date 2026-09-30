---
name: verification-before-completion
description: Evidence before claims. Use before saying code works, a bug is fixed or tests pass, and before committing, pushing or opening a PR.
---

# Verification before completion

Adapted from obra/superpowers `verification-before-completion` (MIT).

**Rule:** do not claim a result you have not just checked. Run the command now, read the output, then report what it says.

## Steps

1. Name the command that proves the claim.
2. Run it in full: the whole suite, not a subset, unless you say which subset and why.
3. Read the output: exit code, number of failures, warnings.
4. Report the actual state with the evidence ("312 passed, 0 failed", "build exit 0"). If something failed or was skipped, say so plainly.

| Claim | Needs | Not enough |
|---|---|---|
| Tests pass | test run just now with 0 failures | an earlier run, "should pass" |
| Bug fixed | the reproduction test now passes, and failed before | "code changed" |
| Lint / types clean | linter and static analysis output | the tests passing |
| Build works | build command exit 0 | lint passing |
| Requirements met | each acceptance criterion checked one by one | tests passing |
| Subagent finished | `git diff` and test output checked by you | the subagent's report |

## Before a PR

Also check: `git status` is clean apart from intended changes, no debug output or commented-out code, no secrets or `.env` values in the diff (`git diff main...HEAD` and search for keys, tokens, passwords), migrations run both ways if the project uses them.

Words like "should", "probably", "looks right" or "Done!" before you have run the check mean you have not verified.
