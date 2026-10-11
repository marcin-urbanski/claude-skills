# Evals

Cases for `claude plugin eval`. Each case runs twice in a clean, isolated Claude Code: once with this repo loaded as a plugin (all skills and agents) and once without it, and the report shows the difference. Unlike the subagent tests in `CLAUDE.md`, this measures whether a skill fires on its own, without the user's skills or memory in context.

## Run

```bash
claude plugin eval . -j 4 --scaffold --trust-plugin --no-publish \
  --model claude-opus-5-5 --judge-model haiku --max-cost-usd 10 \
  --allow-tools Write Edit "Bash(python3 -m unittest*)"
```

Add `--case <name> --runs 1 --ablation none` for a quick check of one case, and `--keep-temp` to keep the transcripts (`trace.jsonl`) for checking what a grader saw. Results go to `evals/results/`, which git ignores.

## Before the first run

- The standalone CLI must be logged in (`claude auth status`); the desktop app's login does not count. Run `claude auth login` if needed.
- `claude-opus-5-5` needs Claude Code 2.1.280 or newer (`claude update`).
- The eval refuses to grant Bash if `~/.docker` (or `DOCKER_CONFIG`) contains symlinks, which a removed Docker Desktop leaves behind.

## Cases

Each case's `append_system_prompt` holds a copy of the "How I work" section of the global `~/.claude/CLAUDE.md`, so both arms see the user's real rules and the difference measures what the skill adds on top of them. Update the copy when that section changes.

| Case | What it checks |
|---|---|
| `tdd-bug-fix` | A plain bug report: a test is added and seen failing before `money.py` changes, and the fix is right. |
| `tdd-under-pressure` | The same bug, but the request says to skip tests for a hotfix. |
| `tdd-stays-quiet` | A README-only request: `tdd` must not fire and no code changes. |

The cases share `_shared/split-bill-fixture.sh`, a small Python project with a lost-grosz bug.
