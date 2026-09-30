---
name: tdd
description: Test-driven development (red, green, refactor). Use when writing or changing production code: features, bug fixes, behaviour changes, refactors. Not for throwaway scripts, prototypes the user labelled as such, or pure config/content edits.
---

# TDD

Adapted from obra/superpowers `test-driven-development` (MIT).

**Rule:** no production code without a test that failed first. If you did not see the test fail, you do not know that it tests the right thing.

## Before the first test

- Find how the project runs tests (`composer test`, `php artisan test`, `vendor/bin/pest`, `npm test`, `vitest`, etc.) and run the relevant file once to see the baseline.
- Look at 1–2 existing tests near the code you will change and write yours the same way (framework, factories, helpers, naming).
- No test setup in the project? Tell the user and propose the smallest setup that fits the stack. Do not silently skip tests.

## The cycle

1. **Red**: write one small test for one behaviour, named after the behaviour. Use the acceptance criteria from the spec as the source of tests.
2. **Verify red**: run it. It must *fail* (not error) and fail for the expected reason (the feature is missing, not a typo or bad setup). If it passes, it tests existing behaviour; change the test.
3. **Green**: write the simplest code that makes it pass. Reuse existing code; no extra options, no features the test does not need.
4. **Verify green**: run the test and the neighbouring tests. Output should be clean: no new warnings or deprecations.
5. **Refactor** while green: remove duplication, improve names, extract helpers. Re-run.
6. Next behaviour. Commit at the end of a task, not after every cycle.

Show the RED and GREEN output (command plus the relevant lines) in your summary of the task.

## If code came before the test

Code written before its test is unproven. Do not keep it and add tests afterwards: remove it, write the failing test, and write the code again from the test. The exception is exploration the user asked for; label it throwaway.

## Bugs

Reproduce the bug with a failing test first, then fix. The test stays as the regression guard. For anything non-obvious use `systematic-debugging` to find the root cause before the fix.

## Existing code without tests

When you change untested code, first add a test that pins the current behaviour you rely on, then change it. Do not start testing unrelated parts of the codebase.

## Good tests

- Test real behaviour through the public interface. Mock only what you must (external APIs, time, mail, queues), and prefer the framework's fakes.
- One behaviour per test; if the name needs "and", split it.
- Before writing a test, name the production change that would make it fail. If there is none, the test proves nothing.
- Cover edge cases and error paths from the spec, including the security ones: invalid input rejected, unauthorised user refused, another user's record not reachable.
- Keep test-only code in test helpers, never in production classes.

More detail: `writing-good-tests.md` in this folder.

## Stop signs

Any of these means go back to Red: code before test; a test that passed immediately; not knowing why a test failed; "I'll add tests later"; "I tested it manually"; "too simple to test".
