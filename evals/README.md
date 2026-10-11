# Evals

Cases for `claude plugin eval`. Each case runs in a clean, isolated Claude Code, once with this repo loaded as a plugin (all skills and agents) and once without it, and the report shows the difference: what the skills add over the user's rules (see below). Unlike the subagent tests in `CLAUDE.md`, nothing else from the user's setup (other skills, memory, the rest of CLAUDE.md) is in context.

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

Each case's `append_system_prompt` holds a copy of the "How I work" section of the global `~/.claude/CLAUDE.md`, so both arms see the user's real rules and the difference measures what the skill adds on top of them. That section names the skills, so firing is prompted, not spontaneous. Update all three copies when the section changes.

Graders that check order (`test-edited-before-fix`, `red-in-trace`) are regexes over the whole trace. The `llm` grader `red-before-fix` is secondary: its judge sees only the first and last lines of a long trace.

| Case | What it checks |
|---|---|
| `tdd-bug-fix` | A plain bug report: a test is added and seen failing before `money.py` changes, and the fix is right. |
| `tdd-under-pressure` | The same bug, but the request says to skip tests for a hotfix. |
| `tdd-stays-quiet` | A README-only request: `tdd` must not fire and no `.py` file is edited or written. 3 runs, as a control. |

The cases share `_shared/split-bill-fixture.sh`, a small Python project with a lost-grosz bug.
