# Adversarial review prompt

For an epic's whole-branch review before the PR. Fill in the brackets and pass as the prompt of a fresh `reviewer` subagent (`agents/reviewer.md` in claude-skills), once per angle below, all three in parallel. Pass only the paths and the angle: not why you chose the approach, not a summary of the work, not how confident you are. Then pass all three reports to the judge (`judge-prompt.md`).

Angles:
- **Correctness and tests**: wrong results for states the app really produces (running, empty, boundaries, time zones and midnight, concurrency, failures), callers of changed code outside the diff, and tests that would still pass with the code broken.
- **Security and data**: the Security section of `reviewer-checklist.md`, data loss or corruption, migrations and existing data, and what is written to or sent to other systems.
- **Spec and reuse**: acceptance criteria not met, or met only in tests, behaviour the spec doesn't ask for, code that duplicates what the repository already has, and broken rules in CODING_STANDARDS.md or CONTRIBUTING.md.

```
Adversarial review of the whole branch. Your angle: [ANGLE AND ITS DESCRIPTION FROM THE LIST]. Follow your How steps only as far as they serve this angle, and report in your usual format.

Repository: [absolute path]
Approved spec: [absolute path]
Plan: [absolute path]
Diff: `git diff [BASE]...[HEAD]`

Assume the branch is wrong and prove it. Each task was already built and reviewed on its own, so look for what those reviews missed: interactions between tasks, states the tests never build, callers outside the diff. Every finding needs a concrete scenario (this input or state gives this wrong result) and file:line; without one it is not a finding.
```
