# Claude skills

The skills, subagents and hooks I use every day with [Claude Code](https://code.claude.com). This repo is also where they live: the folders in `~/.claude/skills` on my Mac are symlinks to it, so every change is tracked in git.

## Skills

| Skill | What it's for |
|---|---|
| [handoff](skills/handoff/SKILL.md) | Writes one handoff per thread of work to `docs/handoffs/<slug>.md` when a session gets long or a task is finished, then gives you a prompt to paste into the next session. The file lives in the repo's main checkout, so it survives the worktree being deleted. A session that coordinates parallel worktree sessions writes `docs/handoffs/_overview.md` instead. Works with the two hooks below. |
| [spec-first](skills/spec-first/SKILL.md) | Plans a change before any code is written, scaled to its size: a small fix goes straight to tests, a feature gets a short spec, an epic gets a spec and a plan committed on its feature branch, and a review per task. An epic in a project without `CODING_STANDARDS.md` starts one from [a template](skills/spec-first/coding-standards-template.md) with Core candidates for Swift/SwiftUI, Laravel, WordPress and Next.js. |
| [design-check](skills/design-check/SKILL.md) | Turns a Claude Design handoff export in `docs/design` into work: a spec for a new project, a report of what changed when a new export lands, and a design check before a UI pull request. |
| [tdd](skills/tdd/SKILL.md) | Red, green, refactor for every change to production code. |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | Find the root cause before fixing anything. |
| [verification-before-completion](skills/verification-before-completion/SKILL.md) | Run the tests, linters and build before saying something works. |
| [ux-principles](skills/ux-principles/SKILL.md) | My UI/UX rulebook: avoiding generic AI-looking design, conversion psychology within honest limits, visual craft, interaction and app patterns, e-commerce product pages and checkout, and native iPhone, iPad and Mac apps. |
| [pr](skills/pr/SKILL.md) | The format for a pull request body that a human can review fast: a small visual of the change (pseudocode, call tree, Mermaid, a diff of the shape), before-and-after evidence, and a merge danger call (one-way or two-way door, blast radius). `spec-first` uses it when it opens a PR. |
| [retro](skills/retro/SKILL.md) | `/retro` after a hard session or a PR review: reads a digest of the session transcript (`digest.py`) and the PR's review comments, then proposes, most severe first, the automated check, coding standard, reviewer rule, skill fix or `CLAUDE.md` pointer that stops the same mistake from happening again. It keeps `CODING_STANDARDS.md` within its template's limit by sharpening, merging or replacing rules. Only you can invoke it, and it changes nothing until you pick. |

## Subagents

`spec-first` delegates each task of an epic to these two. Defining them as files, instead of writing the instructions into every delegation prompt, means the implementer always starts with the `tdd` and `verification-before-completion` skills loaded (the `skills` frontmatter field), whether or not it would have invoked them itself.

| Subagent | What it's for |
|---|---|
| [implementer](agents/implementer.md) | Builds one task from a plan test-first, following the project's `CODING_STANDARDS.md`, verifies, commits, and reports RED/GREEN output. Cannot spawn subagents. |
| [reviewer](agents/reviewer.md) | Read-only review of a diff for reuse, security, the project's own `CODING_STANDARDS.md`, tests that cannot fail, code smells and spec compliance, with a verdict and findings by severity. |

## Hooks

The first two hooks belong to `handoff`.

- [`handoff-load.sh`](hooks/handoff-load.sh) (SessionStart) loads the thread whose `Branch:` matches the current branch, from any worktree of the repo. Otherwise it lists the open threads (slug, branch, age, next step) so Claude can ask which one to continue, and warns when a thread's branch is checked out in another worktree. In the main checkout it also loads `_overview.md` for the orchestrator. It still reads an old `docs/handoff.md`, skips anything marked `done`, and after compaction loads only a branch match. When the handoff continues a plan in `docs/plans/`, it also tells Claude to invoke `spec-first` first.
- [`handoff-nudge.sh`](hooks/handoff-nudge.sh) (Stop) asks Claude to write this thread's handoff once the session transcript passes about 2.5 MB. Change the limit with `HANDOFF_NUDGE_BYTES`.

They need `jq`. Register them in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|clear|compact",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/handoff-load.sh" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "~/.claude/hooks/handoff-nudge.sh" }] }
    ]
  }
}
```

To test them, run `bash tests/handoff-load.test.sh` and `bash tests/handoff-nudge.test.sh`. They build temporary repos with worktrees and need only bash, git and `jq`.

### Seeing which skills Claude invoked

A skill call is easy to miss in the chat. This inline hook (no script needed) prints a line like `🔧 skill: tdd` each time Claude invokes a skill, marked `(subagent)` when a subagent did:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Skill",
        "hooks": [{ "type": "command", "command": "jq -c '{systemMessage: (\"🔧 skill: \" + (.tool_input.skill // \"?\") + (if .agent_id then \" (subagent)\" else \"\" end))}'" }] }
    ]
  }
}
```

## Scripts

- [`skill-usage.py`](scripts/skill-usage.py) reads the local transcripts in `~/.claude/projects` and reports, per session, which skills the main session and its subagents invoked, next to the number of code edits and commits. Bash commands that write code files (`>`, `tee`, `sed -i`, Python writes) count as edits. Use it to check whether the skills are actually used: `scripts/skill-usage.py TimeTracker --since 2026-10-05T07:31` (UTC; a plain date works too). Tests: `python3 -m unittest discover -s tests -p 'test_*.py'`.

## Install

Clone the repo and link the skills you want into your personal skills folder:

```bash
git clone https://github.com/marcin-urbanski/claude-skills.git ~/Developer/claude-skills
ln -sfn ~/Developer/claude-skills/skills/handoff ~/.claude/skills/handoff
```

Link the hooks the same way into `~/.claude/hooks/`, and the subagent files into `~/.claude/agents/`. Claude Code follows symlinked skill folders, so `git pull` is enough to update.

For claude.ai, zip a skill folder (for example `handoff/` with its `SKILL.md`) and upload it under Customize → Skills. claude.ai rejects a description with XML-like tags, so run `bash tests/skill-frontmatter.test.sh` first: it fails if any skill description contains `<` or `>` or is longer than 1,024 characters (Claude Code's limit), or if a skill's `name` differs from its folder.

## Credits

`tdd`, `systematic-debugging` and `verification-before-completion` are adapted from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

`pr` and `retro` are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock (MIT). The Summary visuals in `pr` come from Dex Horthy's [`show-me`](https://github.com/humanlayer/skills) (MIT), via Matt's skill. The test-smell and code-smell sections of the reviewer checklist follow Matt's `code-review` skill and his talk on the PR bottleneck. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

`ux-principles` builds on uxpeak's [UI/UX Playbook](https://www.uxpeak.com) (free preview) and their video [The UX Psychology Behind Apps People Can't Stop Using](https://www.youtube.com/watch?v=2TlIg3VokY8), rewritten and extended in my own words. Its app-pattern and Apple-platform references are based on Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/), paraphrased as rules.

For animation and motion work I also use [emilkowalski/skills](https://github.com/emilkowalski/skills).

## Licence

[MIT](LICENSE)
