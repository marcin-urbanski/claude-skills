# Plan review prompt

Fill in the brackets and pass as the prompt of the `reviewer` subagent (`agents/reviewer.md` in claude-skills) after an epic's plan is written and before it is committed. Pass only these paths: not why you chose the approach, not a summary of the plan, not how confident you are.

```
Plan review. Nothing is implemented yet, so there is no diff: follow these steps and this report format instead of the ones for a diff review.

Repository: [absolute path]
Approved spec: [absolute path]
Plan: [absolute path]

Find what is wrong with this plan. Assume its author is overconfident: do not validate or summarise it. Read CODING_STANDARDS.md and CONTRIBUTING.md, whichever exist, and check every claim the plan makes about the code against the code itself. Look for:
- An acceptance criterion that no task covers, or whose planned tests would still pass if it were broken.
- A changed function, type or behaviour whose callers the plan does not all list (search with rg).
- New code that duplicates something the repository already has, or a reuse decision in the spec that a task ignores.
- Authorisation or validation that a task leaves out or does differently from the spec and the existing code (the Security section of the spec-first `reviewer-checklist.md`).
- Task order that leaves the app broken or the tests red after a task.
- A task too big for one implementer session, or a done check that would pass with the task undone.
- A task whose approach breaks a rule in CODING_STANDARDS.md or CONTRIBUTING.md.
- A question the spec leaves open that an implementer would have to guess: an edge case, an error path, existing data, what an unchanged screen or output shows.

Report only what would make the build miss its spec, break existing behaviour or a project rule, or force an implementer to guess. If you find nothing after checking, say so.

Report, most severe first. Each finding:
- Where: task number or spec section, plus file:line in the code when relevant.
- Problem: what goes wrong, and when.
- Evidence: what in the code or spec shows it.
- Change: the edit to the plan, or the question for the user when the spec has to change.
Then "Checked and fine": one line per item above that you checked, with how.
```
