#!/usr/bin/env bash
# Stop hook: once per session, when the conversation gets long, ask Claude
# to update docs/handoff.md before it stops, so you can /clear and continue.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)

# Never loop: if we already blocked this stop, let Claude finish.
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0

session=$(printf '%s' "$input" | jq -r '.session_id // empty')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty')
[ -n "$session" ] && [ -f "$transcript" ] || exit 0

# Fire only once per session.
marker="${TMPDIR:-/tmp}/claude-handoff-${session}"
[ -e "$marker" ] && exit 0

# "Long" = transcript file above this size. Tune with HANDOFF_NUDGE_BYTES.
limit="${HANDOFF_NUDGE_BYTES:-2500000}"
size=$(wc -c < "$transcript" | tr -d ' ')
[ "$size" -lt "$limit" ] && exit 0

touch "$marker"
jq -n '{decision: "block", reason: "This session is getting long. Before stopping, use the handoff skill to write or update docs/handoff.md with the current state of the work. Then finish exactly as the After writing section of the skill says, including the prompt to paste into the new session."}'
