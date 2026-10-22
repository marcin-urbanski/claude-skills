# Judge prompt

After the adversarial reviews of an epic (`adversarial-review-prompt.md`). Fill in the brackets and pass as the prompt of one fresh `reviewer` subagent (`agents/reviewer.md` in claude-skills), with the three reports pasted verbatim. Add nothing of your own: not which findings you agree with, not what you already fixed.

```
Judge the findings below. Do not review the branch from scratch: follow these steps and this report format instead of the ones for a diff review.

Repository: [absolute path]
Approved spec: [absolute path]
Plan: [absolute path]
Diff: `git diff [BASE]...[HEAD]`

Reports from three adversarial reviewers:
[THE THREE REPORTS, VERBATIM]

For each finding, read the code it points at and the spec, then decide:
- Stands: its evidence holds in this code (the scenario happens, the duplicate or broken rule is there, the weak test stays green) and neither the spec nor the plan asks for it. Keep its severity or correct it.
- Rejected: its evidence does not hold (say what prevents it, with file:line), the spec asks for this behaviour, or the plan header records it as an accepted trade-off.
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
