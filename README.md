# Claude skills

The skills and hooks I use every day with [Claude Code](https://code.claude.com). This repo is also where they live: the folders in `~/.claude/skills` on my Mac are symlinks to it, so every change is tracked in git.

## Skills

| Skill | What it's for |
|---|---|
| [handoff](skills/handoff/SKILL.md) | Writes `docs/handoff.md` when a session gets long or a task is finished, then gives you a prompt to paste into the next session. Works with the two hooks below. |
| [spec-first](skills/spec-first/SKILL.md) | Plans a change before any code is written, scaled to its size: a small fix goes straight to tests, a feature gets a short spec, an epic gets a spec, a plan and a review per task. |
| [tdd](skills/tdd/SKILL.md) | Red, green, refactor for every change to production code. |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | Find the root cause before fixing anything. |
| [verification-before-completion](skills/verification-before-completion/SKILL.md) | Run the tests, linters and build before saying something works. |
| [ux-principles](skills/ux-principles/SKILL.md) | My UI/UX rulebook: avoiding generic AI-looking design, conversion psychology within honest limits, visual craft, interaction and app patterns, e-commerce product pages, and native iPhone, iPad and Mac apps. |

## Hooks

Both hooks belong to `handoff`.

- [`handoff-load.sh`](hooks/handoff-load.sh) (SessionStart) loads `docs/handoff.md` into a new session, unless it is marked `done`.
- [`handoff-nudge.sh`](hooks/handoff-nudge.sh) (Stop) asks Claude to write a handoff once the session transcript passes about 2.5 MB. Change the limit with `HANDOFF_NUDGE_BYTES`.

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

- [`skill-usage.py`](scripts/skill-usage.py) reads the local transcripts in `~/.claude/projects` and reports, per session, which skills the main session and its subagents invoked, next to the number of code edits and commits. Use it to check whether the skills are actually used: `scripts/skill-usage.py TimeTracker --since 2026-09-30`.

## Install

Clone the repo and link the skills you want into your personal skills folder:

```bash
git clone https://github.com/marcin-urbanski/claude-skills.git ~/Developer/claude-skills
ln -s ~/Developer/claude-skills/skills/handoff ~/.claude/skills/handoff
```

Link the hooks the same way into `~/.claude/hooks/`. Claude Code follows symlinked skill folders, so `git pull` is enough to update.

For claude.ai, zip a skill folder (for example `handoff/` with its `SKILL.md`) and upload it under Customize → Skills.

## Credits

`tdd`, `systematic-debugging` and `verification-before-completion` are adapted from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

`ux-principles` builds on uxpeak's [UI/UX Playbook](https://www.uxpeak.com) (free preview) and their video [The UX Psychology Behind Apps People Can't Stop Using](https://www.youtube.com/watch?v=2TlIg3VokY8), rewritten and extended in my own words. Its app-pattern and Apple-platform references are based on Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/), paraphrased as rules.

For animation and motion work I also use [emilkowalski/skills](https://github.com/emilkowalski/skills).

## Licence

[MIT](LICENSE)
