# Judge prompt

After the adversarial reviews of an epic (`adversarial-review-prompt.md`). Fill in the brackets and pass as the prompt of one fresh `reviewer` subagent (`agents/reviewer.md` in claude-skills), with the three reports pasted verbatim. Add nothing of your own: not which findings you agree with, not what you already fixed.

```
Judge the findings below. Do not review the branch from scratch: follow these steps and this report format instead of the ones for a diff review.

Repository: [absolute path]
Approved spec: [absolute path]
Diff: `git diff [BASE]...[HEAD]`

Reports from three adversarial reviewers:
[THE THREE REPORTS, VERBATIM]

For each finding, read the code it points at and the spec, then decide:
- Stands: its scenario happens with this code and the spec does not ask for that behaviour. Keep its severity or correct it.
- Rejected: its scenario cannot happen (say what prevents it, with file:line), or the spec asks for this behaviour.
- Open: it depends on a question the spec leaves open. Say the question.
Merge duplicates. Add a finding of your own only if it is Critical.

Report:
### Stands
Most severe first. Each: severity, file:line, the scenario, the fix.
### Open
Each: the finding and the question for the user.
### Rejected
One line each: the finding and why.
```
