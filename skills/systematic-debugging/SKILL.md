---
name: systematic-debugging
description: Find the root cause before fixing. Use when a bug, failing test, build failure or unexpected behaviour is not obvious at first glance, or when a first fix did not work.
---

# Systematic debugging

Adapted from obra/superpowers `systematic-debugging` (MIT).

**Rule:** no fix before you can say what the root cause is and why. Fixing a symptom leaves the bug in place.

## 1. Investigate

1. Read the whole error: message, stack trace, file and line, codes, warnings before it.
2. Reproduce it reliably and write down the exact steps. If you cannot reproduce it, gather more data; do not guess.
3. Check what changed: `git log`, `git diff`, dependency updates, config and environment differences.
4. With several layers (request → controller → service → database; CI → build → deploy), log what enters and leaves each boundary once, to see *where* it breaks before asking why.
5. Trace a bad value back to where it originates and fix it there. See `root-cause-tracing.md`.

## 2. Compare

Find similar code in the same project that works. List every difference between the working and the broken case, including the ones that "can't matter". When following a library or framework pattern, read its documentation in full (Context7 / official docs) rather than skimming.

## 3. Hypothesis

State one hypothesis: "X is the cause because Y." Test it with the smallest possible change, one variable at a time. If it is wrong, form a new one; do not stack fixes on top of each other. If you do not understand something, say so.

## 4. Fix

1. Write a failing test that reproduces the bug (`tdd`).
2. Make one fix, at the root cause. No "while I'm here" changes.
3. Run the test and the suite (`verification-before-completion`).
4. Consider validation at other layers so the same bad data cannot get in elsewhere: `defense-in-depth.md`. For flaky timing issues: `condition-based-waiting.md`.

## When fixes keep failing

After three failed fixes, stop. Repeated failures that each reveal a new problem somewhere else point at the design, not at the bug. Tell the user what you tried, what each attempt showed, and what you think is structurally wrong, and decide together before trying again.

## Stop signs

"Just try X and see", several changes at once, "probably X" without evidence, skipping the reproduction test, a fourth fix attempt. Each of these means going back to step 1.
