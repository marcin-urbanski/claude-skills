#!/usr/bin/env bash
# SessionStart and Stop hook: when Claude finishes a turn that changed the repo, run the project's fast checks
# (.claude/skills/verify/checks.sh, written by the verify-setup skill) and send Claude back to fix a failure.
# A check that has to hold every time lives here, not in a prompt, because a prompt holds only when the model notices it.
#
# - SessionStart records the working tree's fingerprint, so a turn that changed nothing costs nothing.
# - Stop runs checks.sh when the fingerprint differs from the last one recorded (session start or last green run).
# - checks.sh runs as committed on the base branch when it is there, so a branch cannot weaken the check that judges it.
# - A failure blocks the stop once. If the checks still fail on the stop after that, the stop goes through with a
#   warning, so Claude is never stuck (it may have stopped on purpose, say to ask the user something).
# Projects without checks.sh, and folders outside git, are left alone.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)
event=$(printf '%s' "$input" | jq -r '.hook_event_name // empty')
session=$(printf '%s' "$input" | jq -r '.session_id // empty')
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
active=$(printf '%s' "$input" | jq -r '.stop_hook_active // false')
[ -n "$session" ] && [ -d "$cwd" ] || exit 0
root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" || exit 0

checks_path=.claude/skills/verify/checks.sh
state="${TMPDIR:-/tmp}/claude-verify-gate-${session}"

# The tree's content: HEAD, uncommitted changes and untracked files, hashed with git so it also works in Git Bash.
fingerprint() {
  {
    git rev-parse -q --verify HEAD || echo none
    git diff HEAD --binary 2>/dev/null
    git ls-files --others --exclude-standard
    git ls-files --others --exclude-standard | git hash-object --stdin-paths 2>/dev/null
  } | git hash-object --stdin
}

base_branch() {
  local ref
  ref=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null) && { echo "$ref"; return; }
  for ref in main master; do
    git rev-parse -q --verify "$ref" >/dev/null && { echo "$ref"; return; }
  done
}

now=$(fingerprint)

if [ "$event" = "SessionStart" ]; then
  echo "$now" >"$state"
  exit 0
fi

[ "$(cat "$state" 2>/dev/null)" = "$now" ] && exit 0

base=$(base_branch)
script="${TMPDIR:-/tmp}/claude-verify-gate-${session}.checks.sh"
if [ -n "$base" ] && git show "$base:$checks_path" >"$script" 2>/dev/null; then
  source_note="$checks_path as committed on $base"
elif [ -f "$checks_path" ]; then
  cp "$checks_path" "$script"
  source_note="$checks_path (new on this branch)"
else
  exit 0
fi

output=$(bash "$script" 2>&1)
status=$?
rm -f "$script"

if [ "$status" -eq 0 ]; then
  echo "$now" >"$state"
  exit 0
fi

tail=$(printf '%s\n' "$output" | tail -n 40)
if [ "$active" = "true" ]; then
  jq -n --arg s "$source_note" --arg t "$tail" \
    '{systemMessage: ("verify-gate: the checks still fail (\($s)). Letting this stop through; they need fixing before a commit.\n" + $t)}'
  exit 0
fi

jq -n --arg s "$source_note" --arg c "$status" --arg t "$tail" \
  '{decision: "block", reason: ("verify-gate: \($s) failed (exit \($c)). Fix the cause and finish again; never weaken or skip a check to get past it. If you stopped on purpose with the checks red, for example to ask the user a question, say so and stop again.\n\nLast lines of its output:\n" + $t)}'
