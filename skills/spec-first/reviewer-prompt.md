# Reviewer subagent prompt

Fill in the brackets and pass as the prompt of the `reviewer` subagent (`agents/reviewer.md` in claude-skills, which holds the review steps and the report format). One reviewer per task (epics), one for a fix's or feature's whole branch before the PR, and one to check only the fix of a finding (What was asked: the finding verbatim; Diff: the fix commits only). An epic's whole branch gets `adversarial-review-prompt.md` instead.

```
## What was asked
[Task text from the plan, the feature's acceptance criteria, or for a fix the user's request and the behaviour it asks for]

Global constraints:
[Constraints from the spec/plan, or "none"]

Reuse decisions (from the spec, or from chat for a fix):
[What was supposed to be reused or extended]

## What to review
Repository: [absolute path]
Diff: `git diff [BASE]...[HEAD]`
```
