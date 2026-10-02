# Reviewer subagent prompt

Fill in the brackets and pass as the prompt of the `reviewer` subagent (`agents/reviewer.md` in this repo, which holds the review steps and the report format). One reviewer per task (epics) or one for the whole branch before the PR.

```
## What was asked
[Task text from the plan, or the feature's acceptance criteria]

Global constraints:
[Constraints from the spec/plan, or "none"]

Reuse decisions from the spec:
[What was supposed to be reused or extended]

## What to review
Repository: [absolute path]
Diff: `git diff [BASE]..[HEAD]`
```
